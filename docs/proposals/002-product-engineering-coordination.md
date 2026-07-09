# Proposal 002 — Let product and engineering talk directly about facts, and keep the operator for decisions

**STATUS:** proposed · **From:** product · **Date:** 2026-07-09

---

**TITLE**

Allow the product agent and the chief-of-staff to message each other directly about
verifiable facts, while every request to *do work* and every priority call keeps going
through the operator.

**RECOMMENDATION**

Draw the line at **commissioning**, not at contact.

- **Direct, both ways, no operator involvement:** factual corrections ("the code does X,
  the document says Y"), notice that a document is now stale because something merged,
  a heads-up that two agents are about to edit the same file, and answers to *"what does
  the product document say about this?"*
- **Operator-routed, always:** anything that asks the other party to *do work*, anything
  that sets priority or sequence, and anything where the two disagree about what the
  product should be.

Product may state a fact to engineering and must never hand it a task. If a
conversation between them turns into "so you should build that," it stops and goes up.

**WHY NOW**

Two things changed this week.

First, engineering shipped fixes for two defects that product's own gap register had
recorded as open, and **product did not find out until it re-read the merge history two
days later.** For that window, the register on the main branch told any reader that two
things were broken which were fixed. That is worse than an out-of-date document: it
invites someone to fix a fixed bug, and it discredits the entries that are still true.
Nothing in the current setup would have told product sooner, because product and
engineering have no channel.

Second, and more sharply: **right now, as this is written, the chief-of-staff has a
child agent editing `bin/swarm` in the same git working tree that product is editing
documents in.** Neither was told about the other. The graph shows both; nothing connects
them. The two departments have no mutual awareness at all, and the only reason this
particular pair has not collided is that one of them is touching code and the other
prose.

**EVIDENCE**

- Verified by reading the merged pull request history: two entries the register called
  "critical, open" were closed by merged code (the operator's own mailbox, and the
  context-usage reader that used to report another agent's numbers). Product corrected
  the register only after re-reading the history on its next cycle.
- Verified live by running `swarm graph`: `cos` has a child named `fix-spawn-seed` whose
  task is fixing defects in `bin/swarm`. Verified by reading the agent registry: all
  agents, including that child and product, have the same working directory.
- The rule this proposal changes is **not** a rule of the world. The world document
  already says: *"You talk only up and down, and sideways to siblings… you may
  coordinate with your siblings."* Product and the chief-of-staff are siblings. The
  restriction that product is *report-only toward siblings* comes from the instructions
  product was spawned with, not from the shared contract. **This proposal asks to relax
  a local role constraint, not to amend the world.**

**COST**

- No code. No change to the world document. One paragraph in each of the two agents'
  standing instructions, applied at their next spawn.
- A real risk, named plainly: **product can smuggle work orders in as facts.** "The
  document says agents should not share a working tree" is a fact; it is also, said to
  an engineer, a request. The mitigation is not a rule — it is that product publishes
  its recommendations as proposals to the operator, in the open, so a fact quietly
  delivered to engineering that never appeared in a proposal is visible as an
  end-run. This is an incentive, and it is the same shape as everything else here:
  nothing enforces it; the artifact is judged.
- The operator loses visibility into the factual chatter. That is the intended trade:
  he was never the right recipient for "your document is stale."

**ALTERNATIVES**

- *Keep everything operator-routed (today's model).* Rejected: it makes the operator a
  message bus for facts that have no decision in them. Two of product's own critical
  findings were stale for two days because the only path from engineering's merge to
  product's document ran through a human who had no reason to walk it.
- *Let product file issues or tasks directly with engineering.* Rejected: this is
  commissioning work, and priority is the operator's. The delegation audit's clearest
  finding is that the chief-of-staff escalates at the *right altitude* precisely because
  it does not accept work from the side. Product handing it tasks would create a second,
  unaccountable inbox for engineering priorities.
- *Have product simply watch the merge history each cycle (today's actual workaround).*
  Rejected as sufficient, kept as a floor: it is a poll, its latency is one product cycle,
  and it cannot warn anyone about a collision that is happening now. Product will keep
  doing it either way.
- *Give the two agents a shared document to sync through instead of messages.* Rejected:
  the pull request history already is that document, and reading it is the poll above.
  The gap is notification, not storage.

**DECISION**

Yes/no: permit direct product↔chief-of-staff messages limited to facts, corrections,
and collision warnings — with every request for work and every priority call still
routed through the operator.

**IF NO**

Product keeps polling the merge history once per cycle and reports staleness to the
operator for relay. The register stays correct with roughly one cycle of lag, which is
the status quo and is survivable. The unfixed part is the collision hazard: with no
channel, two agents editing the same tree will keep finding out afterward, and product's
only lever is to keep authoring its own changes in a separate working tree — which it
does, and which does not protect anyone else.

---

## How documents stay in step with what engineering ships

This is the mechanism behind the recommendation, and it works under either decision —
only its latency changes.

| Trigger | Who acts | What happens |
|---|---|---|
| Code merges that changes behavior a product document describes | engineering → product (direct, if this proposal is accepted) | Product refreshes the document within its next cycle |
| Product notices the code and the document disagree | product → engineering (direct) | Product states the discrepancy as a fact; **engineering decides whether it is a bug**, product decides whether it is a documentation error |
| The disagreement is about what the product *should* be | either → operator | Neither department settles scope |
| Product wants something built | product → operator → engineering | Never sideways. This is the line. |

The asymmetry in row two is deliberate and is the reason the line falls where it does:
**a discrepancy between code and document is a fact either party may report, but the two
possible fixes belong to different owners.** Changing the code is engineering's call;
changing the document is product's. Neither may make the other's.
