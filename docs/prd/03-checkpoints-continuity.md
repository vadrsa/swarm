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
mission is `--role` if given; else `<slug>: <first 100 chars of task>`; else the
task truncated. `tasks[]` starts with one entry `t1` holding the delegated task,
`status: "in-progress"`, `progress: "just spawned"`. Overall `status: "on-track"`,
`progress_summary: "seeded at spawn; not yet reconciled"`.

Seeding matters for a mechanical reason: the restore hook always has a file to
inject, and the agent always starts from a valid envelope rather than inventing
one.

### Restoration

`SessionStart` (matcher: all sources, including `startup` and `compact`) runs
`swarm-hook.cjs restore-state`, which reads `state/<id>.json` and emits it as
`additionalContext`:

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
- **That `context` is the *caller's* context.** See G3.

## Edge cases and known limitations

**G3 — `swarm checkpoint --context` reads the wrong agent's transcript.** The
reader prefers `$CLAUDE_TRANSCRIPT_PATH`. **`swarm spawn` never sets that
variable** — the pane environment carries only `SWARM_DIR`, `SWARM_AGENT_ID`,
`SWARM_AGENT_LABEL`. So the fallback path always executes:

```python
cands = sorted(glob.glob("~/.claude/projects/*/*.jsonl"),
               key=os.path.getmtime, reverse=True)
tp = cands[0]
```

That glob spans **every project on the machine**, and takes the most recently
written transcript. Under a live swarm — where several agents are producing
transcript lines continuously — an agent asking "how full is my context window?"
is routinely answered with a sibling's number, or with an unrelated Claude Code
session in another repo.

The result is printed as bare JSON with no qualification, agents are briefed to
put it in their checkpoint, and parents are told to read the checkpoint as the
judged artifact. A wrong number therefore propagates upward as fact. Because
`tokens_used` is the input to "should I wrap up before my context runs out," a
misreport can cause an agent to hand off early or to run out of window without
warning.

The number *looks* plausible in every case, which is the worst property a wrong
number can have.

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

**Context accounting hardcodes a model→window table** (`opus: 1_000_000`,
`sonnet: 1_000_000`, `haiku: 200_000`) that is then **never used** — the function
returns `{tokens_used, transcript}` and the comment says *"window: caller passes
--model via env if known; else omit pct."* No caller does. So the percentage the
schema implies is never computed, and `WINDOWS` is dead code.

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
