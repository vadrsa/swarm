# PRD 04 — The goal-reconciliation loop

*Landed as PR #13 ("Thread E"), built on the checkpoint substrate from PR #11.*

## The problem

A graph of agents executing tasks will drift. Each node does what it was asked;
none asks whether what it was asked still serves the goal. The specific failure
modes, all observed in practice:

- **Goal drift.** An agent paraphrases its mission as whatever it happens to be
  doing, and the paraphrase is always on-track by construction.
- **Reflexive green.** Asked "are you on track?", a model says yes. It is the
  likeliest completion.
- **Stalled delegation.** A child was spawned three cycles ago, has reported
  `in-flight` each time, and nobody has noticed that `in-flight` never changes.
- **A leaf that should have been a coordinator.** An agent grinding alone on work
  that wanted five agents, because nobody re-examined the decomposition after the
  work turned out bigger than it looked.

The obvious fix — a supervisor that walks the tree and audits everyone — does not
scale and centralizes judgment in the node with the least context about any
particular subtree.

The design instead makes **every agent reconcile its own single layer**. Nobody
walks the tree. The graph stays aligned because each node keeps its own layer
aligned, and misalignment surfaces upward one hop at a time. Recursion is
emergent, not orchestrated.

## Who uses it

**Every agent**, over **its own direct children only**. Grandchildren are somebody
else's problem, by explicit rule.

The **operator** consumes the loop's output as escalations, and as the reconciled
`status` field in each top-layer agent's checkpoint.

## Current behavior

The loop is **prose**. It is not code. It exists in exactly three places, and it
is the same four steps in each:

1. **`WORLD.md` §"Reconcile toward your goal"** — the contract every agent reads.
2. **The spawn briefing** — prepended to every agent's first prompt, under
   `--- RECONCILE, THEN CHECKPOINT ---`.
3. **The `restore-state` hook** — appended to the continuity injection, so a
   restarted or post-compaction agent re-checks its trajectory before resuming.

### The four steps

**1. State your goal from your state file.** Not a paraphrase of what you are
currently doing. The instruction is explicit about why: *"that's how goal drift
hides."* Reading `mission` off disk is a defense against the agent's own narration.

**2. Name the falsifier — before you look.** *"Name the concrete evidence that
WOULD show you are OFF track — the observation that, if you saw it, means this
will not converge."* This is the load-bearing step and the reason the loop is not
a ritual. Committing to a disconfirming observation *first* means "I'm fine"
cannot survive a criterion the agent itself wrote.

**3. Look for it.** Survey your layer: `swarm children`, then read each child's
`state/<child>.json`. Is each checkpoint fresh? Is its status non-blocked? Are its
delegations actually closing? And turn the same suspicion inward: *is your own
progress materially different from last time, or are you repeating yourself?* The
doc supplies one prior: **"a stalled `in-flight` across cycles is presumptively
at-risk, not a pass."**

**4. Verdict, then act.** Name the single biggest risk, then do something about
it. The agent has **full autonomy over its own layer**: steer a child (`swarm
send`), close one and spawn a different one, spawn more. A childless agent that
discovers its task is decomposable delegates *here* — WORLD.md calls this "the
loop working." If the gap exceeds the agent's authority, it escalates.

### When it runs

At every idle boundary, fused with the checkpoint ritual — *reconcile, then
checkpoint* — and whenever the agent is nudged (a restore, or a message).

The output of reconciliation is not a report. It is the `status` and `blockers`
fields of the checkpoint. The design deliberately provides no separate log:
*"status/blockers ARE the reconciliation output; there is no separate log."*

### Escalation

When step 4 exceeds the agent's authority, it sends its parent a structured
message:

```
GOAL: <your objective>
GAP: <the specific way current setup will NOT converge>
EVIDENCE: <the falsifier from step 3 that is now present>
OPTIONS CONSIDERED: <what you weighed and why each is beyond your authority>
ASK: <the specific decision/action you need>
```

The format is chosen so a parent can act without re-deriving the child's
reasoning. The parent consumes it at *its own* survey step — an escalation from
below is evidence in the parent's step 3.

### What is deliberately absent

Per the design decisions recorded in PR #13:

- **No tiering.** Every agent gets the full loop, not a lighter version for
  leaves.
- **No action guardrails.** Total autonomy over the agent's own layer.
- **No enforcement.** There is no hook that checks whether an agent reconciled.
- **No separate log.** Conclusions live in the checkpoint.

## Contracts and guarantees

**Guaranteed:**

- Every agent receives the loop, verbatim, in its spawn briefing.
- Every agent receives the reconciliation nudge on every session start and after
  every compaction.
- Every agent can read `WORLD.md` via `swarm world`.
- The primitives the loop calls for exist: `swarm children` surveys exactly one
  layer (including dead children — a dead child is a re-plan signal), `swarm
  spawn`/`send`/`close` give an agent authority over its own layer.

**Not guaranteed — and this is the design, not an oversight:**

- **That any agent reconciles.** Nothing checks.
- **That reconciliation is honest.** The agent grading itself is the agent being
  graded. PR #13's verification showed a live agent presented with a stalled state
  correctly concluding **OFF-TRACK** — *"the injected on-track status did not
  survive contact with the evidence"* — and producing a correct escalation. That
  is real evidence the loop can bite. It is one observation, not a rate.
- **That an escalation reaches anyone.** See below.

## Edge cases and known limitations

**G2 — top-layer escalation has no destination.** The loop's escape hatch is
`swarm send` to the parent. For every agent directly under the operator — where
scope and direction decisions actually live — the parent is the operator, and
`swarm send operator` fails with `unknown agent: operator`. The operator has no
registry row, no pane, no inbox.

So the loop terminates, at the top, in an instruction that cannot be followed. An
agent that correctly reconciles, correctly finds a gap beyond its authority, and
correctly formats an escalation has nowhere to put it. It falls back to printing
prose into a terminal — which is the failure mode the durable inbox
([PRD 02](02-inbox-messaging.md)) was built to eliminate, reintroduced at the one
layer where the stakes are highest.

Every agent is nonetheless briefed, at spawn and on every restore, to escalate
this way. The instruction is unconditional; the capability is not.

**G6 — the survey step has no verb.** Step 3 says: *"read each child state file at
`state/<child>.json`."* There is no `swarm checkpoint <id>` read mode. `swarm
children` shows liveness, reported state, and last words — but not the child's
mission, task statuses, blockers, or checkpoint age. The single most important
input to reconciliation is reachable only by knowing the on-disk path and parsing
JSON by hand. This is the only place in the product that instructs agents to
bypass the CLI.

**Freshness is undefined.** Step 3 asks whether a child's checkpoint is "fresh."
Nothing defines fresh — no threshold, no unit, and (per **G7**) nothing reads
`updated_ts` or `seq` anyway. The agent invents a criterion each cycle.

**"Materially different from last time" has no anchor.** The agent is asked to
compare its progress to the previous cycle, but the checkpoint holds only *current*
state. The prior cycle's `progress_summary` was overwritten by this one. Detecting
"am I repeating myself" requires a history the schema does not keep. `seq`
increments but carries no payload.

**Cost.** The loop is ~40 lines of briefing prepended to every spawn, plus a
re-injection on every session start, plus (if followed) a `swarm children` call, N
file reads, and a real reasoning pass at every idle boundary. For a one-shot leaf
that ends after a single turn, the reconciliation ritual is a substantial fraction
of its total work. PR #12 accepted this explicitly. Nobody has measured it.

**Self-pacing is unimplemented.** Standing agents in the current swarm were told to
"self-pace ~daily." Nothing in the product schedules an agent, wakes it, or gives
it a clock. An idle agent stays idle until something sends it a message — and the
doorbell that would surface such a message is best-effort. The reconciliation loop
runs "at every idle boundary," but an agent that has gone idle has, by definition,
stopped taking turns.

## Open product questions

1. **Where do top-layer escalations go?** This is the same question as "is the
   operator a node in the graph." Until it is answered, the loop's terminal case
   is undefined. Of everything in this PRD set, this is the gap with the clearest
   product consequence.

2. **Does the loop change behavior, or produce compliant-sounding checkpoints?**
   The mechanism has exactly one defense against ritual — the commit-to-a-falsifier
   step — and one observation that it worked. The honest framing is that this is an
   unmeasured bet on a prompt. A cheap experiment exists: reconciliation *should*
   sometimes produce a plan change (a spawn, a close, a steer, an escalation).
   Counting how often it produces one, versus how often it produces a green status
   and nothing else, would turn the bet into a number. Nothing records this today
   because there is no separate log — a design decision that also removed the
   evidence needed to evaluate the design.

3. **What wakes a standing agent?** Reconciliation is triggered at idle boundaries
   and by nudges. A long-lived agent with no incoming messages has neither. Either
   standing agents need a scheduler, or "self-pacing" needs to mean something the
   product actually provides.

4. **Should the checkpoint keep a short history?** Step 3's "am I repeating
   myself" is unanswerable against a schema that overwrites. A ring buffer of the
   last N `progress_summary` values would make self-repetition mechanically
   detectable — and would give question (2) its data.

5. **Should reconciliation be tiered after all?** PR #13 chose uniformity on the
   grounds that you cannot predict which agents matter. The counter-argument is
   that a leaf with no children has no layer to survey, so steps 3's child-survey
   is vacuous for it, and it pays the full briefing anyway. The uniform loop is
   simpler; whether it is cheaper depends on the spawn:reconcile ratio, which is
   unmeasured.
