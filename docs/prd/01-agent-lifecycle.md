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

Two scopes, since PR #16 collapsed what used to be three:

- **Swarm = project.** One swarm per project, rooted at its `.swarm/` directory
  (`$PWD/.swarm`, override with `SWARM_DIR`). There is no swarm-id and nothing to
  mint.
- **Agent** — one Claude session within the swarm, keyed by its slug id (see
  [PRD 05](05-agent-naming.md)).

On disk, flat:

```
.swarm/
  agents/<id>.json     registry row — id, label, pane, model, cwd, task, parent, role?
  updates/<id>-<ts>-<state>.json   append-only hook events
  settings/<id>.{json,task,launch.sh,status}
  state/<id>.json      the agent's goal-status checkpoint
  inbox/<id>/          durable messages
  names                append-only ledger of every id ever minted
```

**Every verb auto-creates this layout on first use** — `init_swarm_paths` is
idempotent and called by all of them. `swarm start` therefore is never required;
it exists as an explicit init that prints the swarm root, and running it twice is
a no-op. A coordinator can simply begin spawning.

`SWARM_ID` is a **retired** concept. It is deliberately *ignored with a note on
stderr*, never an error: an agent spawned before the cutover carried `SWARM_ID`
baked into its pane environment, which cannot be changed for a running process, so
erroring would have broken every live agent's verbs the instant the CLI advanced.
Machine-read stdout (`start`, `whoami`, `spawn`) stays clean and the exit code is
untouched. The cost was that such an agent printed that note on **every verb call
for the rest of its life** and resolved its state to the wrong root — the hazard
recorded as **G12**, which the operator closed by hand: pre-cutover agents were
closed and the current generation was started fresh, so no live agent carries a
stale `SWARM_ID` today. The tolerance code remains, correctly, for any that
someone revives from an old pane.

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
5. **Create a herdr tab** with `SWARM_DIR` (the swarm root), `SWARM_AGENT_ID`, and
   `SWARM_AGENT_LABEL` baked into the pane environment. These are inherited by
   every shell in the pane and cannot be lost, which is why `swarm whoami` needs
   no state file. The tab inherits `--cwd`, which **defaults to the coordinator's
   own `$PWD`** — see gap **G13**.
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
`lastRecordedState()` exists. `lastRecordedState()` still scans the whole
`updates/` directory on every notification, but since the filename-scan rewrite
it does so with **zero file reads and zero `JSON.parse`** — the id, timestamp and
state it needs are all encoded in `${id}-${ts}-${state}.json`, so a `readdir` is
the entire cost (measured: 500 files, 32.5ms → 0.7ms per call). The hot path no
longer cares how large the directory gets.

What remains open is the **growth itself**, not the read: `updates/` still has no
rotation. PR #16 made that sharper rather than milder — with one flat `.swarm/`
per project it accumulates every event from every agent that has *ever* run in
that repo, across all time. This is now a disk-footprint and
`swarm updates`-readability concern rather than a per-event cost. Retention is
deliberately not implemented: `swarm wait` blocks on an agent's *newest* record,
`swarm updates` is the only history surface, and there is still no archive verb
(see below), so any prune rule risks deleting a record a live reader needs.
Pruning wants a product decision about what history is for, not a hook patch.

**Nothing distinguishes a finished swarm from an abandoned one.** Previously a
swarm was a run with an id, so at least the runs were separable on disk. Now the
project *is* the swarm and its `.swarm/` is permanent, so the registry, the name
ledger, the checkpoints, and the update log all persist indefinitely. `swarm reap`
prunes rows for dead panes; nothing prunes anything else.

**Bare `swarm close` closes every agent in the project** — the caller's siblings,
its parent, and its parent's other children, if invoked by a subagent. Nothing
restricts `close` to the caller's subtree, though WORLD.md's "acting is local"
rule says it should be. The CLI enforces no such scoping, and now that a project
holds exactly one swarm there is no id argument that could accidentally narrow it.

## Open product questions

1. **What is a swarm's terminal state?** `close` keeps state; `reap` prunes rows.
   Neither says "this swarm achieved its goal." Since PR #16 a swarm has no
   lifecycle distinct from its repository's, so a finished run and an abandoned one
   are the same directory, and with standing agents that never naturally end,
   "when is this over" has no answer in the product.

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
