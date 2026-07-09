# PRD 01 — Agent lifecycle

*Spawn, registry, liveness, close, reap.*

## The problem

A coordinating Claude session needs to run other Claude sessions and know, at any
moment, which of them exist. Every naive approach to this fails in a specific
way: screen-scraping a terminal to detect "the agent finished" misreads a
scrollback; a background daemon becomes a thing that can die and take the swarm's
memory with it; an in-memory roster evaporates the moment the coordinator's
context is compacted.

swarm's answer is that **an agent's existence is a file, and an agent's liveness
is a question you ask herdr**. Nothing is inferred from a screen. Nothing is held
in a process.

## Who uses it

**Agents** — every coordinator, at every depth. The verbs are the same whether
you are the operator's root session or an agent five levels down; the world doc
is explicit that this symmetry is the design.

The **operator** uses `list`/`status`/`graph` to observe, and rarely spawns
directly.

## Current behavior

### Scope

Three nested scopes, and confusing them is the source of a real bug class:

- **Project** — the `.swarm/` directory, one per repo. Located at `$PWD/.swarm`
  unless `SWARM_DIR` overrides it.
- **Swarm** — one coordinator run, keyed by a **swarm-id**. `swarm start` mints
  one; every other verb (except `swarm swarms` and `swarm world`) requires
  `SWARM_ID` in the environment.
- **Agent** — one Claude session within a swarm, keyed by its slug id (see
  [PRD 05](05-agent-naming.md)).

On disk:

```
.swarm/swarms/<swarm-id>/
  agents/<id>.json     registry row — id, label, pane, model, cwd, task, parent, role?
  updates/<id>-<ts>-<state>.json   append-only hook events
  settings/<id>.{json,task,launch.sh,status}
  state/<id>.json      the agent's goal-status checkpoint
  inbox/<id>/          durable messages
  names                append-only ledger of every id ever minted
```

`swarm start` creates all five directories plus an empty `names` file, and prints
the swarm-id. The default id is derived from the coordinator's herdr pane id plus
a counter (`HERDR_PANE_ID` with `:` → `-`, then `-1`, `-2`, …), so it is readable
and unique per project without any clock or random source.

### Spawn

`swarm spawn "<task>" [--label L] [--model M] [--cwd DIR] [--role R]`

Preconditions: `HERDR_ENV=1` and `herdr` on PATH. Otherwise it dies — herdr is
the container, not an option.

The sequence, in the order it actually happens:

1. **Mint the id** from `--label` (slugified) or, absent a label, from the task's
   first meaningful words. See [PRD 05](05-agent-naming.md).
2. **Write per-agent settings** to `settings/<id>.json`: five hooks wired to
   `swarm-hook.cjs` — `Stop` → `stop`, `Notification` → `notification`,
   `UserPromptSubmit` → `inbox-check`, `SessionStart` → `restore-state`,
   `PreCompact` → `precompact-marker`. Passed to `claude --settings`, so the
   user's global `~/.claude/settings.json` is **never touched**.
3. **Write the task to a file**, not a command line. This is load-bearing: a
   multibyte or quote-heavy prompt re-parsed through herdr's pane shell breaks,
   and `printf %q` emits `$'…'` ANSI-C literals that can crash the launch. The
   task file is read into a shell variable by a launcher script whose own text is
   pure ASCII. `herdr pane run` only ever sees the launcher's path.
4. **Prepend the briefing** to the task: who you are, that you are in a graph,
   that you may spawn children, that `swarm world` describes the world, and the
   full reconcile-then-checkpoint ritual (see [PRD 04](04-reconciliation-loop.md)).
   The agent's own task follows under a `--- YOUR TASK ---` delimiter.
5. **Create a herdr tab** with `SWARM_DIR` (project root), `SWARM_ID`,
   `SWARM_AGENT_ID`, and `SWARM_AGENT_LABEL` baked into the pane environment.
   These are inherited by every shell in the pane and cannot be lost, which is
   why `swarm whoami` needs no state file.
6. **Register the agent immediately** — before waiting for it to come up. This is
   deliberate: "this agent exists" is the registry plus the hook, never a
   screen-detection poll. A slow-starting but healthy agent is never lost from the
   roster.
7. **Seed the checkpoint** at `state/<id>.json` (see [PRD 03](03-checkpoints-continuity.md)).
8. **Wait for the launcher's own signal.** The launcher writes `launching` to
   `settings/<id>.status` immediately before running `claude`, or `failed: <reason>`
   if `claude` is missing / the settings file is unreadable / `claude` exits
   nonzero. `spawn` polls this file for `SWARM_READY_TIMEOUT` (default 30s).

Step 8's three outcomes are the interesting part, and the asymmetry is correct:

| Status file says | Meaning | What spawn does |
|---|---|---|
| `failed: …` | Confirmed dead | Close the tab, delete the registry row, exit nonzero. **The name stays burned.** |
| `launching` | Confirmed started | Print the id, exit 0. |
| *(nothing, timed out)* | **Ambiguous** | Keep the agent, warn on stderr, print the id, exit 0. |

The `unknown` branch exists because an earlier version tore down live agents on a
slow start. Ambiguity is never treated as death. This is the single most
important reliability property of spawn.

### Liveness

`live_panes()` asks `herdr pane list` for the set of currently-existing pane ids.
An agent is **live** iff its registered pane is in that set, **DEAD** iff it is
not, and **unknown** (`?`) iff herdr did not answer at all. `list`, `status`,
`graph`, and `children` all reconcile against this; the registry alone is never
trusted.

`swarm reap` refuses to run when herdr is unreachable — it cannot distinguish
"dead" from "cannot tell", and deleting on a guess would lose agents.

### Reported state

Each agent's `Stop`/`Notification` hook writes one immutable record per event to
`updates/`. The four states, and precisely what each is worth:

- **`done`** — a `Stop` fired and the trailing assistant text did not look like a
  question. Means *a turn ended*. It is **not** evidence the work is correct or
  complete. WORLD.md says so; every PRD in this set repeats it.
- **`question`** — a `Stop` fired and the trailing text matched a question
  heuristic (ends in `?`, or contains one of ~20 ask-phrases near a `?`/`:`).
  A **guess from prose**, surfaced with an `is_question` flag so readers know.
- **`blocked`** — a `Notification` fired whose message matched
  `permission|needs your|approve|allow|blocked|waiting for your response`.
- **`idle`** — a `Notification` fired that looked like a generic idle ping
  (`waiting for your input|is idle|are you still there`) **or** any notification
  when the agent's last recorded state was already `done`. Non-blocking.

The `idle` state exists because Claude Code emits an idle notification roughly a
minute after any turn ends, and mapping that to `blocked` made every finished
agent look like it needed the coordinator (fixed in PR #6).

`swarm wait <id>` blocks until the agent's newest record *at or after wait's start
time* is one of `done|question|blocked|idle`, then prints it. The "since" mark
means a stale `done` from a previous turn cannot satisfy a fresh wait. It always
has a timeout (default 600s) and never hangs.

### Close and reap

`swarm close <id>` closes `<id>` **and its entire subtree**, by walking the
`parent` edges in the registry. The semantics are "approve and clean up": when
you approve a delegated agent's work, its children were part of producing that
work, so they finish together. `--self` closes only `<id>`. Bare `swarm close`
closes every agent in the swarm. **Close never deletes state** — the swarm
directory remains as a paper trail.

`swarm reap` deletes the registry rows of agents whose panes herdr confirms are
gone. It never touches a live agent, never runs if herdr is silent, and — critically
— **never frees a name**.

## Contracts and guarantees

**Guaranteed:**

- An agent that `spawn` reported successfully is in the registry before `spawn`
  returns. Registration precedes the readiness wait.
- A confirmed spawn failure removes the registry row and closes the tab, but the
  id remains permanently burned in the `names` ledger.
- Liveness reflects herdr, not the registry. A registry row for a dead pane
  reports `DEAD`, and `--live-only` hides it.
- `reap` never deletes a live or indeterminate agent.
- `close` never deletes state.
- `wait` never hangs; it always returns within its timeout.
- Every hook record is written atomically (`tmp` + `rename`), so a reader never
  observes a half-written record.
- A subagent's hooks are scoped to that subagent. The global Claude Code settings
  file is not modified.

**Best-effort / heuristic — do not build on these:**

- `done` vs `question` is a text classifier over the trailing assistant message.
- `blocked` vs `idle` is a regex over Claude Code's human-facing notification
  string.
- The one-line `summary` in `updates` is the agent's own last words, truncated to
  300 characters. WORLD.md: *"a hint, not a verified result."*
- Spawn readiness within 30 seconds. A timeout keeps the agent and warns.

**Explicitly not provided:** no task model, no scheduling, no retry, no
supervision tree, no automatic restart of a dead agent. WORLD.md is direct about
this: a dead child means part of your plan is not being done — re-plan, usually by
spawning a fresh agent, rather than trying to revive the corpse.

## Edge cases and known limitations

**`close <id> --self` does not validate `<id>`** (gap **G4**). The subtree path
computes a target set and dies with `unknown agent: <id>` if it is empty. The
`--self` path assigns `targets="$one"` directly, then the loop skips any id with
no registry file — printing `(nothing to close)` and exiting 0. A typo and a
successful close are indistinguishable to the caller.

**Reaped agents leave orphaned artifacts** (gap **G5**). `reap` removes
`agents/<id>.json` only. The agent's `state/<id>.json`, `inbox/<id>/`, four
`settings/<id>.*` files, and all its `updates/` records remain, and after reaping
nothing in the codebase ever reads them again — `state` is only read by the
restore hook (for a live agent), `inbox` only by the inbox hook (for a live
agent). There is no retention policy, no archive verb, and no way to surface a
reaped agent's final checkpoint, which is the very artifact a parent is told to
judge it by.

**`blocked` can be misclassified as `idle`** (gap **G11**). If Claude Code
reworded a permission notification such that it matched no permission keyword but
did match an idle keyword, a real block would be recorded as `idle` — a terminal
state for `wait`. A coordinator waiting on that agent would return successfully
while the agent sits at a permission prompt. The coupling is to another product's
user-facing copy.

**A `done` immediately followed by an idle notification is normal** and is why
`lastRecordedState()` exists. But `lastRecordedState()` scans the entire
`updates/` directory on every notification, which grows without bound for the
life of the swarm. Not a correctness issue; an O(n) read per event.

**`swarm start` derives its id from `HERDR_PANE_ID`, falling back to `s`.** Two
swarms started outside herdr in the same project therefore contend on `s-1`,
`s-2`, … which is handled (the loop finds a free one) but means swarm-ids are not
meaningful outside herdr.

**Bare `swarm close` closes every agent in the swarm** including the caller's own
siblings and parent's other children, if invoked by a subagent. Nothing restricts
`close` to the caller's subtree, though WORLD.md's "acting is local" rule says it
should be. The CLI enforces no such scoping.

## Open product questions

1. **What is a swarm's terminal state?** `close` keeps state; `reap` prunes rows.
   Neither says "this swarm achieved its goal." `swarm swarms` cannot distinguish
   a finished run from an abandoned one, and with standing agents that never
   naturally end, "when is this over" has no answer in the product.

2. **Should `close` be scoped to the caller's subtree?** WORLD.md tells agents
   they act only on their own layer, but the CLI lets any agent close any agent —
   including its own parent. The doc is a norm; the tool has no opinion. If the
   norm matters, the tool should enforce it; if it does not, the doc overstates.

3. **Should a dead agent's last checkpoint be recoverable through a verb?** Today
   the parent is told to judge by artifact, and the child's final artifact — its
   checkpoint — becomes unreachable through the CLI the moment it is reaped. See
   [PRD 03](03-checkpoints-continuity.md).

4. **Is `unknown` (spawn timed out) observable after the fact?** The warning goes
   to stderr and is gone. Nothing records that an agent's launch was never
   confirmed, so a coordinator reading `status` later cannot tell a confirmed-live
   agent from one that was kept on ambiguity.
