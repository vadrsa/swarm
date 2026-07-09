# PRD 07 — herdr + world integration model

*Why the product is a CLI, a hook, and a document — and nothing else.*

## The problem

To run Claude sessions as a coordinated swarm you need four things: somewhere for
each session to live, a way to reach it, a way to know when it did something, and
a way for it to understand what it is part of.

Every one of those has an obvious heavyweight answer — a process supervisor, an
RPC layer, a message bus, a framework — and swarm declines all four. The README
states the position directly: **"No daemon, no MCP, no git assumptions. Just a CLI,
a hook, and a world doc the agents read."**

The design bet is that the strategy — how to decompose, delegate, judge, integrate —
is the *model's* job, and the tool's only job is to make spawn/send/receive
reliable. Every capability in this PRD set exists to keep that bet honest: if the
primitives are trustworthy, the model can be trusted to use them.

## Who uses it

The **operator** installs it and lives with its prerequisites. **Agents** live
inside it and mostly cannot tell it is there — which is the point.

## Current behavior

### herdr is the container, not a dependency

`swarm spawn` refuses to run unless `HERDR_ENV=1` and `herdr` is on `PATH`. This
is not a soft requirement; herdr is where an agent *is*.

Each agent gets a **herdr tab** (full-width, `--no-focus`, labelled with the
agent's id). The tab's root pane carries four environment variables, and this is
the whole of the agent's identity:

| Var | Value | Consumed by |
|---|---|---|
| `SWARM_DIR` | **project root** (`…/.swarm`) | CLI + hook |
| `SWARM_ID` | active swarm-id | CLI + hook |
| `SWARM_AGENT_ID` | this agent's slug | hook, `whoami`, `parent`, `children`, `send`'s sender field |
| `SWARM_AGENT_LABEL` | same string | hook (record key) |

Because herdr bakes these into the pane environment, **every shell in that pane
inherits them and they cannot be lost.** `swarm whoami` needs no state file; it
reads an env var. An agent that clears its context still knows who it is.

The `SWARM_DIR` semantics were a real bug (PR #6): the hook wanted the swarm's own
directory, the CLI wanted the project root, and children inherited the hook's
flavor with no `SWARM_ID` — so **every spawned child's `swarm` CLI resolved state
one level too deep and failed on every verb**. The fix made `SWARM_DIR` mean
project-root everywhere and had the hook derive `swarms/$SWARM_ID/` itself, with a
legacy fallback (no `SWARM_ID` ⇒ `SWARM_DIR` *is* the swarm dir) so panes spawned
by an older version keep working.

herdr also answers the one question the registry cannot: `herdr pane list` is the
**ground truth for liveness**. And `herdr pane read <pane>` lets an agent look at
another's actual screen.

### The hook is the inbound channel

`bin/swarm-hook.cjs` is registered five ways per agent via `claude --settings`, so
the user's global `~/.claude/settings.json` is never touched:

| Claude event | Verb | Direction |
|---|---|---|
| `Stop` | `stop` | agent → coordinator (state) |
| `Notification` | `notification` | agent → coordinator (state) |
| `UserPromptSubmit` | `inbox-check` | coordinator → agent (messages) |
| `SessionStart` | `restore-state` | disk → agent (continuity) |
| `PreCompact` | `precompact-marker` | agent → disk (marker) |

The doctrine, repeated everywhere in the codebase: **completion is a fired hook
event, never a screen scrape, never a parsed marker line.** The agent needs zero
cooperation for its completion to be detected — it cannot forget to report, cannot
report falsely about *whether a turn ended*, and cannot break reporting by
formatting its output differently.

What the agent *says* is a different matter, and the product is careful about the
line: the record's `summary` is the agent's own last words and WORLD.md calls it
*"a hint, not a verified result."* The event is reliable; the content is not.

The hook writes one immutable file per event, atomically (`tmp` + `rename`), to
`updates/<id>-<ts>-<state>.json`. Readers (`updates`, `wait`, `status`, `graph`,
`children`) just list the directory. **No daemon** — that is what "no daemon"
buys: the channel is a filesystem, and a filesystem does not crash and take the
swarm's memory with it.

### The world doc is an API

`WORLD.md` is loaded, verbatim, into every agent that runs `swarm world`. It is
not documentation *about* the system; it is the system's specification *of itself,
delivered to its own users at runtime*. `RELEASING.md` classifies a change to its
contract as **breaking**, the same as removing a verb — which is the correct call
and an unusual one.

It is deliberately **facts, not procedure**: the verbs, what the states mean, what
is reliable and what is not, how work is judged and approved, who may talk to
whom. It tells an agent what exists, never what to do. The README states the split:
*"The tools give reliable spawn / send / receive; the strategy is the model's."*

Three structural claims in it are worth naming, because everything else follows:

- **Seeing is global; acting is local.** `swarm graph` shows the entire living
  society. But an agent talks only *up* to its parent, *down* to its children, and
  *sideways* to siblings. It never reaches into another branch to command a
  stranger.
- **"Done" means approved, not "a turn ended."** A `DONE` record is a turn ending.
  Work is finished when the delegator judges the artifact and approves it.
- **Judge by the artifact, never by reading the child's context.** If you would
  need a child's conversation to tell whether its work is good, the task was
  delegated wrong. (Reading a pane to see *whether* an agent is stuck is fine —
  just not to judge correctness.)

`WORLD.md` is reached only via `swarm world`, never by path. `cmd_world` resolves it
relative to the *dereferenced* location of `bin/swarm`, so the package stays
portable across install topologies.

### The skill is the entry point

`skill/SKILL.md` is 25 lines. It triggers on "start a swarm," checks `HERDR_ENV=1`,
checks `swarm` is on `PATH`, and then does one thing: **tells the agent to run
`swarm world`.** It contains no strategy. The skill's entire content is a pointer
to the document, which is itself a pointer to the CLI.

## Contracts and guarantees

**Guaranteed:**

- An agent's identity lives in its pane environment and survives any context loss.
- Liveness is herdr's answer, never the registry's guess.
- A turn ending fires a hook. This does not depend on the model cooperating.
- Update records are immutable, atomic, and append-only. Readers never see a
  partial write.
- Per-agent hooks never touch the user's global Claude Code settings.
- `swarm world` works from any install location.
- The hook honors the legacy `SWARM_DIR` contract when `SWARM_ID` is absent, so
  panes spawned by an older version keep reporting.
- No daemon, no background process, no persistent connection. State on disk
  survives every restart, including the coordinator's.

**Best-effort:**

- The doorbell (see [PRD 02](02-inbox-messaging.md)) — the only screen-dependent
  path in the product.
- `herdr pane read` as an inspection aid.

**Explicitly assumed, not enforced:**

- That there is exactly one machine. All timestamps come from local clocks; all
  paths are local; `herdr` is a local socket.
- That `node` and `python3` are on `PATH` at hook time. `install.sh` checks at
  install time and warns; nothing re-checks when a hook fires.

## Edge cases and known limitations

**The product is coupled to three external surfaces it does not own**, and the
coupling is undocumented in `WORLD.md`:

1. **Claude Code's hook payload shape.** `UserPromptSubmit`'s prompt field is
   `prompt`, not `user_prompt` — PR #10 discovered this by dumping real hook stdin
   rather than trusting documentation. `additionalContext` is the injection
   mechanism for both the inbox and the checkpoint restore. If either changes,
   messaging and continuity fail silently (both are wrapped in `try`/`catch` to
   never break a turn, so failure is *by design* invisible).
2. **Claude Code's notification copy.** `blocked` vs `idle` is a regex over
   human-facing English (gap **G11**, [PRD 01](01-agent-lifecycle.md)).
3. **Claude Code's prompt glyph.** `ring_doorbell` greps for `❯` (gap **G9**,
   [PRD 02](02-inbox-messaging.md)).

Each degrades safely. Each fails silently. Together they mean the reliability
doctrine — *the hook is reliable, the screen is not* — holds for the **outbound**
channel and is only partially true for the **inbound** one.

**Harness lock-in.** `WORLD.md` says *"Harness: Claude only for now (other
harnesses/models per agent may come later)."* The launcher hardcodes `claude`, the
settings file is Claude Code's schema, the hook parses Claude Code's transcript
JSONL, and the state classifier reads Claude Code's notification strings. `--model`
selects a Claude model, not a harness. The abstraction boundary that would admit a
second harness does not exist yet, and three of the five hook verbs would need
equivalents.

**`bootstrap.sh` is `curl | sh`.** The README flags this honestly and offers a
manual path. It guards against a dirty or non-git target directory.

**Prerequisites are checked once, at install.** If `python3` disappears from
`PATH` later, `swarm` verbs die with Python errors rather than a diagnostic. Nearly
every verb shells out to Python for JSON handling — an unusual choice for a bash
CLI, and a hard dependency the README lists but the failure mode does not explain.

**Nothing prevents two coordinators sharing a swarm-id** in the same project. The
`names` ledger lock serializes id minting, but two `swarm start` calls that pass
the same `--id` collide, and only the second errors (`swarm '<id>' already
exists`). Concurrent coordinators on one swarm are undefined.

**`.swarm/` must be gitignored by the user.** The README says so; nothing enforces
it, and `install.sh` does not offer. A committed `.swarm/` leaks transcript paths
and every agent's full task text.

## Open product questions

1. **Should the coupling to Claude Code's surface be documented in `WORLD.md`?**
   Agents are told the hook is reliable. Three specific mechanisms are reliable
   *only while another product's copy, glyphs, and payload keys hold still*. Since
   `WORLD.md` is versioned as a contract, and since its central claim is about
   what is trustworthy, the omission is a contract-level one.

2. **Is a second harness a real goal?** If yes, the hook's five verbs are the
   interface to abstract and the notification/prompt/transcript couplings are the
   three things that must be pushed behind it. If no, `WORLD.md` should stop saying
   "for now" and the product should stop paying for the ambiguity.

3. **Should swarm own the `.gitignore` line?** A one-line append during
   `install.sh`, or a warning from `swarm start` when `.swarm/` is not ignored in a
   git repo, would close a small privacy leak with a stated cause.

4. **What happens when herdr is unreachable mid-swarm?** `reap` correctly refuses.
   `list`, `status`, `graph`, and `children` degrade to `?` for liveness. `send`
   still writes durably. `spawn` dies. Nothing *reports* that the container is
   gone — an agent surveying its layer sees `?` and must infer why. A single
   `swarm doctor` that says "herdr is not answering" would collapse several
   confusing failure modes into one clear one.

5. **Why Python inside a bash CLI?** Every JSON read, every slug, every semver
   comparison, every millisecond timestamp on macOS shells out to `python3`. It is
   correct and readable, and it makes `python3` as load-bearing as `bash`. Worth
   stating as a deliberate choice — or reconsidering, since `node` is already a hard
   dependency for the hook and could do all of it.
