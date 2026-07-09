# The philosophy of swarm

*Discovered, not invented.*

This document does not propose an ideology. It **reports** one, reconstructed from
the decisions actually made while building this tool — the operator's answers to 37
design questions in the root session, and the arguments that surrounded them.

Every principle below is grounded in a decision. Where the record shows the
operator overruling a recommendation, that overrule is the evidence, and it is
quoted. Where a principle is contradicted elsewhere in the record, the
contradiction is named rather than smoothed away. A philosophy document that only
records the tidy parts would be an invented one.

**How to read the citations.** `ASK #n` is the *n*-th `AskUserQuestion` in the root
`/swarm` session (`07cbe383`); `root L<n>` is a line in that session's transcript.
Both are quoted verbatim, typos included — the operator's phrasing is the evidence,
and cleaning it up would be editing the record.

---

## 1. Save the goal, not the context

This is the load-bearing principle, and the record contains the exact moment it
was articulated.

The chief-of-staff had designed a state file and asked a tidy schema question:
should it be *"a common shape across all standing agents, or fully bespoke per
role?"* The operator refused both options and reframed the problem:

> **"Let's step back on this, are we trying to save context or save the goal?"**
> — ASK #29

The next question in the session (ASK #30) opens by conceding the point — *"You're
right that the design conflates two different things"* — and asks whether the state
file should be **goal-oriented** rather than **context-efficiency caching**. The
operator: *"Goal-oriented, primarily."*

That single reframe is why `state/<id>.json` holds a mission, a task list, and
blockers rather than a cache of what an agent has already read. The checkpoint is
an instrument for judging whether an agent will meet its goal — not a trick for
making its context window last longer. Context efficiency is a side effect the
design is allowed to enjoy, never a thing it optimizes for.

**The test this gives you:** when a mechanism is proposed to save tokens, ask what
it does for the goal. If the answer is "nothing," it is a cache, and it does not
belong in the contract.

---

## 2. Incentives over guardrails

Asked how aggressively to enforce checkpoint-writing via a `Stop`-hook that exits
nonzero, the operator initially said *"Hard enforcement from the start"* (ASK #29) —
and then, within the same thread, abandoned enforcement entirely for something
better:

> **"I think the model should be simpler, the agent should just know that it has to
> update its checkpoint. Then the gameabolity concern is solved by the parent
> naturally pinging the subagent to post an update if it's waiting for it or it
> hasn't seen an update for a while. We need to setup the right incentives with the
> goal tracking - recursive goal reconcilliation is gonna be the answer."**
> — root L1671 *(sic, throughout — the record is quoted as written)*

Note what is being rejected. Not the *goal* of reliable checkpoints — the
*mechanism* of forcing them. A hook that blocks an agent until it writes a file
produces a written file, not a reconciled agent; it is trivially gamed by writing
anything. The operator's answer is that the parent's own need for a fresh checkpoint
— it cannot reconcile without one — is a stronger and more honest incentive than a
hook that can be satisfied with noise.

When the session pushed once more on how far to go to enforce a prompt-only
convention, offering "Convention + external verification / load-bearing state files
/ real tooling support," the operator **denied the question outright and said
`STOP`** (ASK #25). The question had already been answered; asking it again in
mechanism-flavored clothing was not welcome.

This is why WORLD.md says of the checkpoint: *"There is no enforcement — it's a duty
and a judged artifact."* That sentence is a decision, not an omission.

**The test this gives you:** before adding a guardrail, ask who is incentivized to
notice if it is missing. If someone already is, the guardrail is ceremony. If nobody
is, fix the incentive, not the guard.

---

## 3. The reconciliation loop is the enforcement layer

Follows directly from §2, and the operator specified it himself rather than
choosing from options. Asked what the mechanism should look like, he did not pick;
he dictated:

> **"It's not coordinator specific. It's specific to any agent in the system. It's a
> generic system that makes any agent think what goal it has and what subagents it
> has, what the state of the subagents are, and what the objective of them are. And
> it tries to prove that either it needs more agents or it doesn't need more agents.
> So it needs to naturally or unnaturally by a hook, think about if it's able to
> meet its goal. And if not, it should do something about it, whether it's steering
> an agent in a different direction, closing the agent and opening a few new ones,
> or whatever it would think is the correct option."**
> — root L1731

Three commitments are packed in there, and all three survived into the shipped
briefing:

- **Universal, not privileged.** Every agent reconciles, at every depth. There is no
  reconciler role. (ASK #35 later offered "a dedicated standing reconciler agent" as
  an option; the recommendation was "Every parent, recursively," and the whole
  question was **denied** — the answer was already given here.)
- **It must *prove*, not assert.** The loop asks an agent to argue against itself and
  commit to a falsifier. "All good" is not a reconciliation.
- **It ends in an action.** Steer, close, spawn, or escalate. A reconciliation that
  changes nothing and reports "on track" has not run.

**The test this gives you:** a reconciliation that cannot name the evidence that
would prove it wrong is a status report wearing a costume.

---

## 4. Judge artifacts, never claims

The oldest principle in the codebase, and the one most consistently held. WORLD.md:
*"The hook firing is reliable; what the agent claims in its summary is not — the pane
is ground truth."* And: *"`DONE` means a turn ended — it is NOT proof the work is
correct or complete."*

It has teeth in the spawn contract too. `swarm spawn` never trusts a screen to know
whether an agent came up; it waits for the launcher to write a status file, and it
treats **ambiguity as life, not death** — a timeout keeps the agent and warns, because
an earlier version tore down healthy agents on a slow start.

The operator applies the same standard to himself. When the root session reported
seeing text queued in an agent's prompt box, he did not accept the claim:

> *"There is no queued message there, where did you see it?"* — ASK #10
> *"nothing queued, the text you see is claude's response"* — ASK #11

And when the session persisted, he did not adjudicate the claim — he demanded the
underlying artifact be investigated: *"Probably the same issue this is its response,
investigate why this happens"* (ASK #20).

**The test this gives you:** if you would need to read an agent's conversation to
know whether its work is good, the task was delegated wrong.

---

## 5. Simplicity over machinery; delete the distinction before you configure it

The record shows this three times, each time as a *removal*.

**Standing vs non-standing agents.** The operator asked what `--standing` did, then
*"Why do we need non-standing agents?"*, then closed it:

> **"Let's simplify things for now and only have standing agents"** — root L1897, L1904

Shipped as PR #12, *"remove the --standing distinction."* Every agent is standing.

**Trigger modes.** ASK #31 proposed unifying reactive and self-paced agents "under one
mechanism with a trigger-type field," and the operator agreed to unify. But when the
implementation began to treat the trigger as *configuration*, he stopped it by
recalling the actual decision:

> **"Didn't we decide to not use trigger mode and let it be a happenstance?"** — root L1622

A field you set is machinery. A property that merely *happens* to be true of an agent
— some wait for messages, some wake on a timer — is not worth a schema. ASK #34, which
asked whether to build `trigger_mode: both` now or defer, was **denied**.

**The swarm-id.** *"Actually that becomes that there is no multi swarm idea in a single
project. We just have one swarm per project."* (root L2236) — an entire concept, its
verb (`swarm swarms`), its flag (`--id`), and a directory level, deleted rather than
configured. Shipped as PR #16.

**The test this gives you:** when you reach for a config field, first ask whether the
thing it configures should exist at all. Two modes behind a flag is usually one mode
plus a decision nobody made.

---

## 6. Total agent autonomy, bounded by the graph

Asked a battery of questions about what agents may do, the operator answered without
hedging:

> **"An agent is free to do anything to achieve its goal."** — root L1833

And on who may delegate:

> **"Everyone should get it, as they might decide to delegate if the task has turned
> out to be decomposable."** — root L1833

This is why the reconcile-then-checkpoint briefing is given to *every* agent, not
just coordinators, and why a childless agent that discovers its task is decomposable
is expected to spawn — "that is the loop working."

Autonomy is bounded by **structure, not permission**: seeing is global (`swarm graph`
shows the whole society), but acting is local (up to your parent, down to your
children, sideways to siblings). An agent never reaches into another branch to
command a stranger. The bound is a shape, not a rule enforced by code.

Even the agent cap was refused as a fixed number:

> *"If it makes sense as many as you want, since we don't know the tasks and load at
> each time we will need to fill, we need to start small and think if we need more."*
> — ASK #1

**The test this gives you:** the answer to "may an agent do X?" is almost always yes.
The real question is who it must tell.

---

## 7. Break freely before 1.0 — and the milestone is a decision, not a counter

The project ships breaking changes without ceremony, and has twice declined to spend
its `1.0.0`.

When the release manager recommended cutting v1.0.0 for a genuine MAJOR — proper
migration note, correct classification — the operator overruled:

> **"Go with 0.9.0"** — ASK #37

The same override produced v0.6.0. And when the session worried about running out of
version numbers, the operator's instinct was to interrogate the premise:

> *"Won't we run out of 0.x runway if we continue releasing 0.x versions every time?"*
> — ASK #6

The answer he accepted (ASK #7) is the right one: minor versions are unbounded; the
real lever is **when to graduate to 1.0.0 as a stability signal.** The milestone is
being deliberately preserved as a *signal*, not consumed as a *counter*.

**This principle is in live tension with a shipped mechanism**, and honesty requires
saying so. `swarm update`'s `--major` guard fires only when a tag's major component
increments. Under a standing policy of never incrementing it, the guard can never
fire — it is inert for every release this project will make. Two breaking changes
(v0.6.0, v0.9.0) have carried users across with no prompt. The migration notes now
say so in their own text. **The ideology is coherent; the tooling has not caught up
to it.** See the gap register's G1.

**The test this gives you:** pre-1.0 means the *contract* is cheap to change, not that
the *user* is cheap to strand.

---

## 8. Conventions earn their tooling

Nothing here was built because it seemed principled. It was built after the
convention proved out — and refused when it had not.

- **Checkpoints** began as a prompt-only duty in the spawn briefing. Only after they
  proved useful did `swarm checkpoint --help/--context` appear — and it is still only
  a *schema reference and a reader*. It does not write the file, validate it, or
  enforce it.
- **The reconciliation loop** ships as briefing text. ASK #35 explicitly offered "Full
  reconciliation engine" as an option. It was not taken; the question was denied.
- **`swarm send operator`** was built only after the escalation contract had been
  exercised enough for its missing terminus to become a real, observed failure.
- **ZCode support** was dropped the moment research showed no CLI and no hook:
  *"Drop it — not a fit right now"* (ASK #15). A harness that cannot fire a reliable
  completion signal cannot participate in a design whose first premise is §4.

The corollary is a standing bias: **prompt-level convention first, a visibility verb
second, an engine never** — unless the record shows the convention failing.

**The test this gives you:** if you cannot point to the convention working in practice,
you are not building tooling, you are guessing at a workflow.

---

## 9. Keep the operator's channel clean

The operator's second instruction in the entire project:

> **"Since this session is my channel of communication, I don't want it polluted by
> you validating work that can be done by a subagent. What other options do we have
> to keep this session clean?"** — root L31

That question created the chief-of-staff (ASK #2). The operator's attention is
treated as the scarcest resource in the system — scarcer than tokens, which §1
already refused to optimize for.

Its most important consequence is a standard for what may reach him. Late in the
session, buried in design jargon, he stopped the conversation:

> **"Ok since I am not following all of the internal terminology youve got going.
> Let's get a coherent plan and a set of questions in a report for me so I can
> analyze and answer better."** — root L1773

And earlier, on what *good* looks like:

> *"asking the correct questions, asking good questions, identifying those questions,
> surfacing those to me. That should happen seamlessly. And if it doesn't, then we are
> doing something wrong either on the tool level or on the usage level."*
> — root L869

Read that carefully: a badly-framed question is not a communication slip. It is
**evidence of a defect** in the tool or in how the org is using it. The operator
classifies his own confusion as a bug report.

**The test this gives you:** anything reaching the operator must be readable by someone
who has not been in the room. No internal codenames, no thread letters, no design-version
numbers — define the term or drop it.

---

## 10. Correct the record, even against yourself

The project's own documents were twice corrected *against* the project's interest —
a phantom `v1.0.0` migration note demoted to the `v0.6.0` it actually shipped as
(PR #18), and a missing v0.9.0 note written after the fact (PR #21), both stating
plainly that `swarm update` will not protect the reader.

The same instinct governs the PRDs: *"Where the code and the docs disagree, that
disagreement is recorded as a gap rather than smoothed over."* The gap register keeps
resolved gaps under a **Resolved** heading rather than deleting them — because a
register that forgets what was broken cannot show that the same class of thing broke
twice.

And it is why `swarm checkpoint --context` now prints `{}` and explains itself on
stderr rather than returning a plausible number from the wrong agent's transcript
(PR #19). **An honest unknown beats a plausible wrong value** — a wrong number that
looks right is the worst artifact a system can produce, because §4 depends on
artifacts being trustworthy.

**The test this gives you:** if you cannot prove the number is yours, do not print a
number.

---

## What this philosophy is *not*

Recording an ideology faithfully means recording where it is unfinished.

- **It is not "the operator is always right."** The record contains a decision worth
  revisiting: G13 (all agents share one git working tree) was raised, and the operator
  chose *"Keep the original no-op entirely"* (ASK #36) — after that same shared tree
  had already destroyed an agent's uncommitted work. That is a considered call about
  scope ("not swarm's job"), not an oversight. But §4 says judge the artifact: the
  artifact here is lost work, and the hazard resets at every swarm's birth. The
  decision stands; the register keeps the evidence.
- **It is not complete.** §7's tension between "preserve the milestone" and "the guard
  keys on the major component" is unresolved and cannot be resolved by code alone.
- **It is not enforced.** By §2, that is the point. Every principle here is a duty and
  a judged artifact — including this document.

---

*Maintained by the `product` agent. Grounded in the root `/swarm` session
(`07cbe383`, 37 decision points) and the chief-of-staff sessions. Amend it when the
record changes, not when opinion does.*
