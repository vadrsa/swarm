# PRD 08 — Product proposals

*How product reaches the operator: a recommendation with a ready yes/no, never an
open question.*

## The problem

Product's job is to find gaps. The failure mode is what it does next: surfacing the
gap as a *question* hands the thinking back to the operator, who then has to
reconstruct the context, weigh options he did not gather, and decide — which is
precisely the work he delegated by having a product department at all.

The record shows the cost. Of 37 decision points in the root session, **four were
denied outright** (ASK #17, #18, #25, #34) and one drew a `STOP`. The pattern in all
four is the same: an implementation choice, dressed as a scope decision, offered as
a menu. And when the options were too narrow, the operator answered *outside* them
three times (ASK #1, #4, #6) — a tell that the question was under-informed rather
than genuinely open.

The operator's own framing:

> *"asking the correct questions, asking good questions, identifying those questions,
> surfacing those to me. That should happen seamlessly. And if it doesn't, then we
> are doing something wrong either on the tool level or on the usage level."*
> — root L869

A badly-framed ask is a **defect**, not a courtesy lapse. This PRD defines the
artifact that replaces it.

## Who uses it

**Product** writes proposals. The **operator** consumes them. `cos` implements what
is accepted, routed by the operator. No agent other than product is obliged to use
this shape — but nothing stops them, and the self-containedness standard (§ below)
binds *anything* operator-facing.

## What a proposal is

A proposal is a **decision, pre-made, with its work shown** — such that the operator's
entire job is to say yes or no. It is not a question with a recommendation attached;
the difference is that a proposal states what product *will do* absent an objection.

Eight fields. All of them, every time. If a field cannot be filled, the proposal is
not ready.

| Field | What it must contain |
|---|---|
| **TITLE** | One line, plain language, no codenames. A stranger knows what this is about. |
| **RECOMMENDATION** | The single thing product thinks should happen, stated as an action. Not a menu. |
| **WHY NOW** | What changed that makes this live today. If nothing changed, it is not a proposal. |
| **EVIDENCE** | The observation that grounds it — a transcript line, a verified command, a merged PR. Not "it seems." |
| **COST** | What it takes to do: whose time, what breaks, what it forecloses. Including "none." |
| **ALTERNATIVES** | What was weighed and *why it lost*. One line each. Rejected options prove the recommendation was chosen, not defaulted to. |
| **DECISION** | The literal yes/no being asked, phrased so that "yes" is unambiguous and actionable. |
| **IF NO** | What product does if declined. Never "then we're stuck." A proposal the operator can decline without cost is easy to decline. |

### The self-containedness standard

Binding on **anything operator-facing** — proposals, escalations, reports, and
`AskUserQuestion` calls alike:

1. **No internal codenames.** Not `G13`, not `Thread C`, not `a17`, not "the v3
   design." Name the *thing*: "all agents share one git working tree."
2. **Define on first use, or don't use it.** If a term is load-bearing and unavoidable
   (`checkpoint`, `reconcile`), define it in a clause. If it is avoidable, avoid it.
3. **Context travels with the ask.** The operator has not read the thread. Include the
   fact that makes the decision decidable, in the ask itself — not as a pointer to a
   file, and not as an assumption about what he remembers.
4. **A stranger test.** Could someone who was in none of the sessions read this and
   render a correct decision? If no, it is not ready to send.

The operator stated the requirement himself, mid-design, when the terminology
outran him:

> *"Ok since I am not following all of the internal terminology youve got going.
> Let's get a coherent plan and a set of questions in a report for me so I can
> analyze and answer better."* — root L1773

Note that reference identifiers are not banned — they are banned *as carriers of
meaning*. "All agents share one working tree (tracked as G13)" is fine. "G13 is still
open" is not.

## Where proposals live

- **In the repo**, under `docs/proposals/NNN-slug.md`, one file per proposal, so the
  decision and its rationale outlive the session that produced it. A proposal is an
  inspectable artifact, per the project's own standard for judged work.
- **Delivered** by `swarm send operator`, which since PR #20 is a durable file inbox
  the operator drains with `swarm updates`. The message carries the proposal's full
  text — not a path to it. Requiring the operator to open a file to read the ask
  violates rule 3 above.
- **Answered** however the operator likes: a reply through the inbox, a line in the
  session, a merged or closed PR. Product records the outcome in the proposal file
  (`STATUS: accepted | declined | superseded`) so the register of decisions stays
  honest, including the declines.

## Contracts and guarantees

**Guaranteed:**

- Every proposal is decidable without reading any other document.
- Every proposal states what happens if it is declined.
- A declined proposal is recorded, not deleted. (Same reasoning as the gap register's
  *Resolved* section: a record that forgets what was rejected cannot show that the
  same idea was rejected twice.)

**Best-effort:**

- That the operator sees it promptly. The operator's inbox has **no doorbell and no
  hook** — it is the one recipient in the graph with no push. A proposal waits for
  `swarm updates` to be run.

**Explicitly not guaranteed:**

- That a proposal is *correct*. It is product's judgment, and the operator overrules
  it freely — as he did on working-tree isolation (`Keep the original no-op entirely`)
  and on spending the 1.0 milestone (`Go with 0.9.0`). **An overruled proposal is the
  format working, not failing:** the operator decided against a stated recommendation
  with its cost and alternatives in front of him, which is strictly better than
  deciding a menu.

## Edge cases and known limitations

**A proposal is not always the right shape.** Three things are legitimately questions,
not proposals, and forcing them into this format would be dishonest:

- **A genuine preference with no product-optimal answer.** ("Should the tool be named
  X or Y?") Product has no evidence to recommend from.
- **A scope boundary only the operator can set.** ("Is mixed-harness support in scope
  at all?") Product can propose *within* a scope; it cannot propose the scope.
- **A factual unknown.** ("What is z code?") Research it first — that is what ASK #12–#14
  should have been, and the operator ended up supplying a URL a web search would have
  found.

The honest rule: **if product has an opinion, it owes a proposal. If it genuinely has
none, the question is legitimate — but it must still pass the stranger test.**

**Proposals can be over-produced.** Four well-formed proposals arriving at once is a
menu wearing a different hat. Product batches: one consolidated delivery per cycle,
ordered by what product would do first.

**The format cannot make a bad recommendation good.** It only makes the badness
visible — a thin EVIDENCE field or an empty ALTERNATIVES field is a proposal that
should not have been sent. That visibility is the point.

## Open product questions

1. **Should `IF NO` ever be "escalate again"?** Product currently treats a decline as
   final until new evidence arrives. But working-tree isolation was declined once,
   then destroyed uncommitted work, and the decline was reaffirmed. The question of
   what *counts* as new evidence sufficient to reopen a settled call is unanswered,
   and it is the difference between persistence and nagging.

2. **Who else should adopt this shape?** The delegation audit found `cos` escalates
   well already — batched, labeled *"I did not decide"*, recommendation attached —
   which is most of this format arrived at independently. Formalizing it for all
   agents would be tooling a convention that has already proven out (which the project
   normally does). But the audit also found the **operator's own dispatcher session**
   is the over-asker, and no format binds a session's `AskUserQuestion` calls.
