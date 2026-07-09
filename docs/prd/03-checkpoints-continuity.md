# PRD 03 — Goal-status checkpoints & continuity

*Landed as PR #11 (opt-in, `--standing`), made universal by PR #12.*

## The problem

A Claude session has a finite context window. When it fills, Claude Code compacts
it: the conversation is summarized and the details are gone. A long-lived agent
therefore *forgets what it was doing*, and there is no hook that can prevent this —
`PreCompact` fires when the window is already full and cannot inject forward.

Two distinct needs fall out of that, and it is worth separating them because the
product conflates them:

1. **Recovery.** After a compaction or a restart, the agent must be able to
   reconstruct its working state. Its own conversation is no longer a reliable
   record of it.
2. **Judgment.** A parent must be able to tell whether a child is on track without
   reading the child's session — which WORLD.md explicitly forbids as a way of
   judging work. The parent needs an inspectable artifact.

The checkpoint is one file serving both: `state/<id>.json`. Recovery reads it;
judgment reads it too.

## Who uses it

**Every agent** writes its own. PR #12 removed the `--standing` distinction
entirely: predicting at spawn time which agents turn out long-lived was judged the
same trap as predicting which tasks decompose, so everyone gets continuity. The
briefing cost on a one-shot leaf is an accepted loss.

**Every parent** reads its children's, as the survey step of the reconciliation
loop ([PRD 04](04-reconciliation-loop.md)).

## Current behavior

### The schema

`swarm checkpoint --help` prints it. It is a plain JSON file the agent fully
controls; the CLI never writes it after seeding.

```json
{
  "agent": "<slug-id>", "role": "…", "model": "opus",
  "updated_ts": <ms>, "seq": <n++>,
  "mission": "why you exist (stable)",
  "tasks": [{
    "id": "t1", "title": "…",
    "status": "in-progress|done|blocked|at-risk",
    "progress": "one line",
    "delegated_to": [{"agent":"csv-importer","expected_artifact":"PR","status":"…"}],
    "blockers": []
  }],
  "status": "on-track|at-risk|blocked",
  "progress_summary": "overall: is my structure right for my load?",
  "open_threads": [{"id":"…","state":"…"}],
  "context": {"tokens_used": <n>, "transcript": "<path>"},
  "work_cache": {}
}
```

`mission` is stable — the answer to *why does this agent exist*. `tasks[]` is
dynamic and grows as work arrives. `status` and `blockers` are not decoration:
they **are** the output of reconciliation, and the design deliberately provides no
separate log.

### Seeding

`swarm spawn` writes a well-formed checkpoint before the agent's first turn. The
mission is `--role` if given; else it is derived from the task: **the task's first
sentence**, reproduced byte-for-byte when it fits, and otherwise cut at a **word
boundary** with the elision marked. `tasks[]` starts with one entry `t1` holding the
delegated task, `status: "in-progress"`, `progress: "just spawned"`. Overall
`status: "on-track"`, `progress_summary: "seeded at spawn; not yet reconciled"`.

*Until PR #23 the seed was a blind `task[:100]` / `task[:120]` slice.* That is worse
than cosmetic, and the mechanism is instructive: the restore hook re-injects `MISSION`
and `tasks[0].title` into the agent's context on **every** `SessionStart`, so an agent
inherited the mid-word truncation after every compaction and restart, forever, unless
it noticed and hand-repaired its own checkpoint. A seed defect is not a one-time
blemish — it is a permanent input to the continuity mechanism. (Observed directly: the
agent maintaining these PRDs was restored with the mission `"…(the swarm tool: a CLI
+ h"` and had to repair it by hand.)

Seeding matters for a mechanical reason: the restore hook always has a file to
inject, and the agent always starts from a valid envelope rather than inventing
one.

### Restoration

`SessionStart` (matcher: all sources, including `startup` and `compact`) runs
`swarm-hook.cjs restore-state`, which reads `state/<id>.json` and emits **a summary of
it** — not the file — as `additionalContext`:

```
[swarm continuity] You are the standing agent <id> (<role>), resuming
{a session | AFTER A CONTEXT COMPACTION — your prior working memory was just
summarized away, so this checkpoint is your most reliable record}.
MISSION: …
OVERALL STATUS: … — …
CURRENT TASKS:
  - [in-progress] … (BLOCKED: …)
Re-read your full checkpoint at state/<id>.json before proceeding…

RECONCILE now (argue against yourself…)
```

**What it injects, exactly:** `mission`, `status`, `progress_summary`, each task's
**title** and **blockers**, and each `open_threads` entry's `id:state`. It does **not**
inject `progress`, `context`, or `work_cache` — which is why a 46 KB checkpoint yields a
15 KB injection, and why the payload's size tracks task and thread *count* rather than
file size (measured; see **G18**). The trailing instruction to *"re-read your full
checkpoint"* exists precisely because the injection is lossy by design.

The `source == "compact"` branch changes the framing to tell the agent explicitly
that its memory was just destroyed and this file now outranks its recollection.
PR #11 verified this end-to-end: a fresh `claude` session with only the restore
hook recovered its mission and tasks with zero manual priming.

Note that restoration also carries the reconciliation nudge (added in PR #13), so
a restarted agent re-checks its trajectory rather than blindly resuming.

`PreCompact` runs `precompact-marker`, which writes
`state/<id>.compaction-pending` and exits 0. It cannot inject forward and it must
never block compaction (the window is genuinely full). It exists only so that a
compaction leaves a trace.

### Context accounting

`swarm checkpoint --context` reports the agent's own context-window occupancy, to
be pasted into the `context` field. It reads the last `usage` block in the
transcript and sums `cache_read_input_tokens + cache_creation_input_tokens +
input_tokens`.

**Which transcript is "its own" is resolved by identity, never by heuristic**
(since PR #19 — see G3):

1. `$CLAUDE_TRANSCRIPT_PATH`, if the caller explicitly set it (an escape hatch;
   `swarm spawn` does not set it).
2. `state/<my-id>.transcript` — a pointer that `swarm-hook.cjs` writes from the
   `transcript_path` Claude places on **every** hook payload. The hook records it
   before its verb dispatch, so the pointer exists from the agent's first hook
   (`SessionStart`) and every later hook re-records it. It lives under `state/`
   rather than in the `agents/` registry because `reap` deletes `agents/<id>.json`
   but preserves `state/`, and a dedicated single-writer file needs no
   read-modify-write race against `spawn`/`reap`.

If neither resolves, `--context` prints `{}` — the same empty-object shape the
no-usage case has always returned, so `"context": <this>` stays schema-valid — and
explains why on stderr. It never guesses.

A sharp drop between two checkpoints means a compaction happened.

## Contracts and guarantees

**Guaranteed:**

- Every agent has a well-formed checkpoint before its first turn.
- Every agent has `SessionStart` and `PreCompact` hooks registered.
- On any session start, if the checkpoint file exists and parses, its mission,
  overall status, and task list are injected into the agent's context.
- Restoration never breaks session start. A missing or malformed file is a silent
  no-op.
- `PreCompact` never blocks compaction.
- The checkpoint is the agent's own file. Nothing in the CLI overwrites it after
  seeding.

**Best-effort / by design NOT guaranteed:**

- **That the checkpoint is current.** There is no enforcement hook. WORLD.md is
  explicit: *"There is no enforcement — it's a duty and a judged artifact."* An
  agent that never updates its checkpoint is indistinguishable, mechanically, from
  one that reconciled and found nothing changed.
- **That the checkpoint is accurate.** It is self-reported.
- **That `context` is populated at all.** Since PR #19 it is either the caller's
  own occupancy or `{}` — never a sibling's. But `{}` is a legal value: an agent
  whose hook has not yet fired gets an honest unknown, not a number. See G3.

## Edge cases and known limitations

**G3 — `swarm checkpoint --context` read the wrong agent's transcript. Closed by
PR #19 (`5e5f545`).** The reader preferred `$CLAUDE_TRANSCRIPT_PATH`, which
`swarm spawn` never set, so it always fell through to a glob over
`~/.claude/projects/*/*.jsonl` sorted by mtime — **every project on the machine** —
and took the newest. Under a live swarm, where siblings write transcript lines
continuously, an agent asking "how full is my context window?" was routinely
answered with a sibling's number. The result was printed as bare JSON with no
qualification; agents are briefed to put it in their checkpoint and parents to
read the checkpoint as the judged artifact, so a wrong number propagated upward
as fact. Because `tokens_used` is the input to "should I wrap up before my
context runs out," a misreport could cause an agent to hand off early or to run
out of window without warning. The number *looked* plausible in every case, which
is the worst property a wrong number can have.

The fix resolves by identity (see **Context accounting** above): the hook persists
`transcript_path` to `state/<id>.transcript`, and the glob is deleted outright.
When the pointer is absent, `--context` prints `{}` and says why on stderr — an
honest unknown, deliberately preferred to a plausible wrong value.

**The generalizable lesson, worth keeping:** a *project-scoped* glob would not
have fixed this either. Every agent in a project shares one
`~/.claude/projects/<slug>/` directory, so **no path heuristic can distinguish two
siblings** — only an identity handed down by the harness can. Anywhere else in
this product that infers "which agent am I" from the filesystem rather than from
`SWARM_AGENT_ID` has the same bug latent in it.

*Residual, minor:* the rewrite removed the `WINDOWS` model→window table (`opus`,
`sonnet`, `haiku`) that was previously dead code, but left the comment that
described it — `# window: caller passes --model via env if known; else omit pct`
now sits above a `print` with no `pct` and no table anywhere in the file. The
percentage the checkpoint schema implies is still never computed; only the dead
table is gone, not the unbuilt feature.

**G18 — `restore-state` has no cap, and what it injects grows every cycle, forever.**
`inbox-check` budgets its injection at 8,000 characters. `restore-state` budgets nothing.
It injects the mission, every task **title**, every **blocker**, and every
**`open_threads`** entry — joined, unbounded, on every `SessionStart`.

Those fields only grow. The seed writes `"open_threads":[]` and nothing in the CLI or the
hook ever prunes, caps, or ages them; retiring a thread is a convention with no
instrument, exactly as G7 says of the schema generally. Measured on the live swarm:

| Agent | Cycles | Tasks | Open threads | Checkpoint on disk | Injected |
|---|---:|---:|---:|---:|---:|
| `cos` | 7 | 17 | 25 | 46,118 B | **15,415 B** |
| `product` | 3 | 9 | 8 | 8,908 B | 4,936 B |

**The 3× gap between file and payload corrects a natural misreading.** `restore-state`
does *not* inject the `progress` fields, which are most of a checkpoint's bytes. So a
46 KB checkpoint is not a 46 KB injection, and the quantity that matters is not size on
disk — it is task and thread **count**. Empirically the payload crosses 64 KiB at roughly
700 tasks or 300 open threads: implausible for a short-lived child, entirely plausible for
a standing agent that opens a thread per finding and closes none.

Before PR #31 an oversized payload was *destroyed* (see G17 in
[PRD 02](02-inbox-messaging.md)) — the continuity mechanism silently eating its own
restore, which is precisely the goal-drift a checkpoint exists to prevent. That is fixed:
it now arrives whole. But it arrives into a finite context window, every session, and an
agent restored after a compaction pays for every thread it has ever opened.

The product decision here is **retention, not truncation**. A blind cap on the injection
would silently drop the oldest entries, and the oldest entry is the mission. What the
system lacks is a *closing discipline*: an agent should retire an `open_threads` entry when
it resolves, the way it marks a task `done`. Failing that, `restore-state` should prefer
open threads and in-progress tasks over the whole list.

**G7 — the schema has no instrument.** No verb validates a written checkpoint. No
code in the repository reads `updated_ts` or `seq` — the two fields whose entire
purpose is to make staleness detectable. A parent instructed to check whether a
child's checkpoint is "fresh" must open the file and compare timestamps by hand,
against no defined threshold. A malformed checkpoint does not error; the restore
hook catches and no-ops, so the agent silently loses continuity and nobody is
told.

The result is that `seq` and `updated_ts` are ceremony: written by convention,
read by nobody.

**G6 — there is no read verb.** `swarm checkpoint` has exactly two modes,
`--help` and `--context`. There is no `swarm checkpoint <id>` to print another
agent's state, no `--json`, no rollup. The reconciliation loop's central survey
step — "read each child state file at `state/<child>.json`" — is instructed as a
*filesystem path*, not a verb. Every parent hand-rolls a `cat` and a JSON parse.
This is the one place where the product tells agents to reach around the CLI.

**G5 — a reaped agent's checkpoint becomes unreachable.** `reap` removes the
registry row; the checkpoint file remains on disk forever, referenced by nothing.
`graph` hides dead agents; `children` shows them but not their state. So a child
that died having written a final, honest checkpoint — precisely the artifact its
parent is supposed to judge — has that checkpoint accessible only by knowing the
path and the slug. WORLD.md tells the parent to "reconcile what's already been
achieved" against a dead child; the achievement record is the checkpoint, and the
product does not surface it.

**Context accounting still reports no percentage.** It returns
`{tokens_used, transcript}`. The `WINDOWS` model→window table that used to sit
unused beside it was removed by PR #19; its comment (*"window: caller passes
--model via env if known; else omit pct"*) was not, and now describes nothing. An
agent asked to judge "am I running out of window?" is handed an absolute token
count and no denominator — it must know its own model's window size from
elsewhere. The occupancy *percentage* the checkpoint schema gestures at has never
been computed by any version of this code.

**`.compaction-pending` is written and never read.** Nothing consumes the marker.
It is a breadcrumb for a human, not a mechanism.

**The restore hook injects on every `SessionStart`,** including ordinary startups
where the agent has full context. This is correct (it is also the nudge vector)
but it means a short-lived agent pays for the injection twice: once in the spawn
briefing, once on session start.

## Open product questions

1. **Should staleness be observable?** `seq` and `updated_ts` exist to answer "has
   this child checkpointed since last cycle?" and nothing asks. Either surface it —
   `swarm children` could show checkpoint age, and flag a child whose `seq` has not
   advanced across cycles — or drop the fields. Carrying an unread field teaches
   agents that the schema is theatre.

2. **Should `swarm checkpoint` gain a read/validate mode?** A `swarm checkpoint
   <id> [--json]` would give the reconciliation loop's survey step a real verb, and
   a `--validate` would turn a malformed checkpoint from a silent continuity loss
   into an error the agent can see. This is the highest-leverage small addition in
   the product.

3. **Is a self-reported, unenforced, unvalidated artifact sufficient for
   judgment?** The design is deliberate and defensible: enforcement invites
   gaming, and the parent judges the *work*, not the checkpoint. But the parent is
   also told to judge *trajectory* from the checkpoint, and a lazy agent's
   checkpoint reads identically to a diligent one's. There is no proposal here —
   only the observation that the two uses of the file (recovery, judgment) have
   different tolerance for being wrong, and only one of them is the agent's own
   problem.

4. **What is a checkpoint's lifecycle after death?** Retention, archival, and
   whether a swarm's final state should be a rollup of its agents' last
   checkpoints. Relates to the "what is a swarm's end state" question in
   [PRD 01](01-agent-lifecycle.md).
