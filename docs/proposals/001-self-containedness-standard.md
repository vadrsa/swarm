# Proposal 001 — Make everything sent to the operator readable by a stranger

**STATUS:** proposed · **From:** product · **Date:** 2026-07-09

---

**TITLE**

Adopt a self-containedness standard for anything sent to the operator, and put it in
the world document every agent reads.

**RECOMMENDATION**

Add a short section to `WORLD.md` — the document every agent loads at birth — stating
that any message to the operator must be understandable by someone who was in none of
the sessions. Four rules: no internal codenames; define any unavoidable term on first
use; include the fact that makes the decision decidable inside the message itself;
and apply a stranger test before sending. Do not add a hook, a linter, or a validator.

**WHY NOW**

The tool just gained a durable operator mailbox (`swarm send operator`, merged as
PR #20). Before it, escalations reached the operator as prose in whatever session
happened to be open, and framing was that session's problem. Now there is a single
channel that every agent in the graph can write to, and the volume will rise. The
standard should exist before the traffic does.

**EVIDENCE**

The operator stopped a design conversation mid-thread because he could not follow it:

> *"Ok since I am not following all of the internal terminology youve got going.
> Let's get a coherent plan and a set of questions in a report for me so I can
> analyze and answer better."*

He also classified this failure himself, and not as a courtesy issue:

> *"asking the correct questions, asking good questions, identifying those questions,
> surfacing those to me. That should happen seamlessly. And if it doesn't, then we
> are doing something wrong either on the tool level or on the usage level."*

Both are verbatim from the root session transcript.

**A correction to the premise I was given.** The task described this as agents framing
questions in their own internal wording. The delegation audit
(`.swarm/delegation-audit/report-cycle-1.md`) finds the opposite distribution: the
chief-of-staff escalated *well* — one interrupting question in 764 turns, everything
else batched into end-of-task reports, each labeled *"I did not decide / your call"*
with a recommendation attached. The over-asker was the **operator's own dispatcher
session**: 27 questions, of which four were denied outright, six chased a tooling
misread the session could have diagnosed itself, and three were answered outside the
options offered.

So the jargon problem is real, but it is **not primarily coming from the departments.**
It comes from the session closest to the operator — the one that accumulates design
context fastest and therefore forgets fastest that nobody else has it. A standard
aimed only at agent escalations would miss its main target.

**COST**

- One paragraph in `WORLD.md`. That file is the contract every agent reads, so the
  change reaches every current and future agent with no code and no migration.
- `RELEASING.md` classifies a change to the world document's contract as **breaking**.
  This is an addition to what agents are told, not a removal or a change of meaning —
  it constrains prose, not verbs. It should ship as a MINOR, and the release manager
  should confirm that reading.
- Ongoing: agents spend a few more sentences per escalation. That is the cost being
  purchased.

**ALTERNATIVES**

- *Put it in the escalation format only (the `GOAL/GAP/EVIDENCE/OPTIONS/ASK` block).*
  Rejected: it would bind escalations and miss reports, proposals, and the dispatcher
  session's own `AskUserQuestion` calls — which the audit identifies as the actual
  worst offender.
- *Build a validator — a hook that rejects operator-bound messages containing `G\d+`,
  `Thread [A-Z]`, or agent ids.* Rejected on the project's own stated grounds: the
  operator abandoned hook-enforcement for checkpoints in favor of incentives, and
  denied the question when it was re-asked as tooling. A regex cannot tell a defined
  term from an undefined one, and would be trivially satisfied by spelling the codename
  out. The incentive already exists and is sharper than any hook: **an unclear ask gets
  a worse decision, and product owns the consequence.**
- *Do nothing; rely on each agent's judgment.* Rejected: judgment is what produced the
  transcript line above. The standard costs a paragraph.

**DECISION**

Yes/no: add the self-containedness section to `WORLD.md`, as prose, with no enforcement
mechanism.

**IF NO**

Product applies the standard to its own output only (it already does — this proposal is
the first instance) and documents it in `docs/prd/08-product-proposals.md`, which lands
regardless. The cost of declining is that the standard binds one department instead of
the graph, and the dispatcher session — the audit's primary offender — stays unbound
either way, since no world-document rule reaches a session that is not a spawned agent.

---

## Draft text for `WORLD.md`

Offered so the decision is a yes/no and not an assignment. Placement: as its own
section after *"Watching your own layer."*

> ## Talking to the operator
>
> The operator is a human who was not in your session. He has not read your thread, does
> not know your internal names for things, and is the scarcest resource in the graph.
> Anything you send up — an escalation, a report, a proposal, a question — must be
> readable by someone who was in none of the sessions.
>
> - **No internal codenames.** Not a gap number, not a thread letter, not an agent id as
>   a stand-in for an idea. Name the thing: *"all agents share one git working tree,"*
>   not *"G13 is still open."* A reference id may accompany the name; it may never
>   replace it.
> - **Define an unavoidable term on first use.** If it is avoidable, avoid it.
> - **Carry the context with the ask.** Include the fact that makes the decision
>   decidable, in the message. Not a path to a file. Not an assumption about what he
>   remembers.
> - **Apply the stranger test before sending.** Could someone who was in none of the
>   sessions read this and make the right call? If not, it is not ready.
>
> Nothing enforces this. An unclear ask simply gets a worse decision, and the agent that
> sent it owns the result.
