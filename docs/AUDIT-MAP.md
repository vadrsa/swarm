# Audit map — messaging, escalation, checkpoints

*Commissioned by the operator for an adversarial contractor with no history in this org.*

**This is a map, not a route.** Nothing here proposes, recommends, or resolves. Where two
shipped things disagree, the disagreement is recorded, not reconciled. Where a decision rests
on a premise, the premise is named so it can be attacked. Where the operator ruled wrong, it
says so.

**Read this first, then attack it.** Product will answer interviews honestly, including about
the operator.

**Written at:** `main@451a2ec`. **Installed clone:** `1af75f8`, seven merges behind — **no live
agent is running any of the ack/rendered code.** `cos` is deliberately holding the fast-forward.

---

## 0. The halt, and why it is the most important entry here

The operator has **paused** the ack/backpressure work and commissioned this audit. His words:

> *"I approved RULING 1 (summary-line nag) and RULING 2 (>=50-unacked send cap) too fast, and I
> now doubt the premise… A one-line nag re-surfaced to the agent that already ignored the full
> body carries LESS information than what it ignored, and is silenced by `swarm inbox ack`
> rather than by compliance. **Silently-lost becomes silently-acked.**"*

And he points the org's own theorem at the fix:

> *"Your own #53/#55 finding: **a claim stored where its subject cannot correct it is a claim
> nobody checks.** That is G22. If it holds for blockers and for approval, it holds for 'did the
> recipient act on the directive' — and then **the reader of that trace cannot be the
> recipient.** Your own theorem indicts the fix I approved. Neither of us applied it here."*

**Product's assessment: he is right, and product did not catch it either.** The nag re-surfaces
*"you have unacked mail"* **to the agent that ignored the mail**, and the agent silences it by
acking. The recipient is both subject and reader of the trace. That is the exact structure G22
condemns.

**What this does not tell you.** It does not follow that the nag is worthless, or that a
recipient-side signal is always wrong. Nobody has argued that. It is an unexamined premise on
both sides.

**State of the halted work.** PR #58 (schema doc), #59 (`rendered/` build), #60 (contract words)
all **merged**. The operator's instruction — *"if it already merged, leave it, do not revert,
build nothing further"* — is satisfiable exactly as-is, because the installed clone is seven
behind. **Nothing an agent executes has changed.** PR-2 (the 50-unacked send cap) was never
written.

---

## 1. Proposals — true status, not header status

**The headers lie.** Every proposal file still says `STATUS: proposed` except 005. Product has
not refreshed them. Ground truth:

| # | Title | True status |
|---|---|---|
| 001 | Self-containedness standard for operator-facing text | **Undecided.** Never ruled. |
| 002 | Product/engineering exchange facts directly | **Undecided.** Never ruled. Practised anyway — see §5. |
| 003 | Bound `swarm updates`; add `swarm archive`; never prune | **REPLACED, not decided.** Operator: *"I am NOT taking your three yes/nos as written. I am replacing the mechanism"* → backpressure. Product's own words: it *"treated the symptom."* The archive verb and the unbounded `updates` output were **never ruled on** and remain open. |
| 004 | `swarm send` quoting hazard (G14) | **Recommendation 1 WITHDRAWN by its author.** Superseded by `--stdin` (PR #50). The doc examples still show the dangerous forms. Never formally closed. |
| 005 | Notify-and-pull for the inbox | **ADOPTED** (all three parts + operator's send-size limit). **Shipped.** Its central incident is **not covered by what shipped** — see §3. |
| 006 | `done` should mean done; stop re-injecting finished tasks | **RULED YES** (D1 as a *test* gating D2; D2 with five riders). **Not built.** |

**Braked:** product has refused to file a seventh proposal for many cycles. That brake is
self-imposed, still holding, and the operator has affirmed it.

---

## 2. Operator rulings, this session

| Ruling | Content | Premise it rests on |
|---|---|---|
| **MINOR standing** | *"Everything is MINOR until I say otherwise."* | That 0.x users tolerate unwarned breaking changes because migration notes exist. |
| **005 adopted** | Explicit cumulative ack; agents keep full-body injection; unify nothing; + a 6000-byte send limit | That the ack fixes the incident that motivated it. **Now doubted — see §3.** |
| **G1 CLOSED** | The `--major` guard's inertness is *the design*, accepted, reopens at 1.0 | That `RELEASING.md` migration notes are the **only** user-facing warning across a breaking minor — and that is **load-bearing**, not incidental. |
| **006 D1** | *"It is not 'write a line in a doc.' It is: add a TEST"* — the test gates D2 | That an invariant with no instrument rots. Evidenced three times in two days. |
| **006 D2** | Filter `status !== "done"` from the injection, with **five riders** | That `tasks[].status = done` means *"I claim I finished this."* **Undocumented anywhere before this session.** |
| **006 fifth rider** | An instrument surfacing `done` tasks with **no parent verdict** in `delegated_to[]` | G22 applied to `done` itself: *"the self-claim must be checkable by someone other than its author."* |
| **003 → backpressure** | ≥50 unacked ⇒ `swarm send` refuses, non-zero, nothing queued; applies to `operator` | That *"unacked"* is a meaningful count. **The operator has since named this his error** — the count's meaning depends on the nag meaning something. |
| **`rendered/` schema** | Three inbox states by directory; `outstanding := inbox/ ∪ rendered/` | That rendering-without-acking is worth distinguishing. **Now the disputed premise.** |
| **THE HALT** | Pause; audit the whole surface | That the session performed *"local optimizations on a system whose global flow may be incoherent."* |

**Where the operator says he ruled wrong, in his own words:**

- *"I approved RULING 1 … and RULING 2 … too fast, and I now doubt the premise."*
- *"I also stacked the send cap on 'unacked', a count whose meaning depends on the nag meaning
  something. **My error.**"*

**Where product ruled wrong and was corrected:**

- Filed a **false defect against a sibling's code in immutable git history** (#48/#49/#51):
  claimed `release-mgr`'s gate used `sort -V`, then **retracted a true statement** because
  retracting *felt* rigorous. `release-mgr` **refused the acquittal** and handed the fault back.
- Wrote *"nobody else produces that state"* after an exhaustive scan. **A scan of a live system
  is a snapshot, not a property.** Two more agents produced it within days.
- Reported `cos` t37 as a **live** blocker; it was **dead**. `cos` checked all three of its
  blockers, not the one named, and found two stale.
- Told `cos` three siblings carried mangled missions. **Never checked.** All four were intact.

---

## 3. Contradictions between shipped things — recorded, not resolved

**C1. 005's scope was drawn around the symptom, not the mechanism.**
The motivating incident: the operator's directive was injected **in full, under the cap**,
auto-acked on render, and never acted on. Item 3 of the directive governs *"what the injection
cap **holds back**."* **Nothing was held back.** So the shipped feature does not touch the case
that produced it. `cos` sharpened this against product, and product had first written it *"is
not the case that motivated it"* — which understated it. **Both agents wrote down the mechanism
(*"shown is not understood"*, G8's third rung) and neither noticed item 3 could not reach it.**

**C2. The nag's reader is its subject.** §0. Unexamined by anyone until the operator.

**C3. The operator inbox and the agent inbox have opposite ack semantics *by design*, and
nobody has argued whether the asymmetry is right.** The operator flagged this himself. Product's
005 verdict was *"unify nothing"* — argued from G17 (unifying the Python and Node read paths
would import a message-loss bug). **That argument is about the read path, not about ack
semantics.** The ack asymmetry was never separately defended.
*Post-ruling-1 it partly collapsed:* only explicit `ack` reaches `read/` for anyone; what
survives is mechanical (agents have a hook, the operator does not). **That change is merged but
not installed.**

**C4. `WORLD.md` currently describes a world that does not exist on `main`.**
Lines 68–72 say *"For an agent, mail is acked automatically the moment the hook injects it…
That asymmetry is deliberate."* PR #59 made that false. The replacement words are written
(`docs/contract-changes-send-inbox.md`, PR #60) but **not applied**. `cos` is holding the
install *because* installing a hook whose contract the docs contradict *"would hand every agent
a false world."*

**C5. Three `done`s, and the one the code filters on is undefined.**

| | `done` | defined where |
|---|---|---|
| 1 | hook record `state=done` | `WORLD.md:128` — *a turn ended* |
| 2 | *"done means approved"* | `WORLD.md:198` — *the parent's verdict* |
| 3 | **`tasks[].status = "done"`** | **nowhere** — and 006's predicate reads it |

**105 tasks org-wide are marked `done`. Every one self-written. Zero parent-approved.** By
`WORLD.md:198`, none of them is done.

**C6. `RELEASING.md`'s own criteria call this work MAJOR; the operator has ruled it MINOR.**
A `.swarm/` directory-layout change and a `WORLD.md` contract invalidation both meet the
document's MAJOR bar. The standing MINOR rule overrides. **Recorded because it is a live
disagreement between a document and a ruling, not because anyone is wrong.**

**C7. A document is a claim about the present, and nothing re-checks it.**
`docs/prd/02` asserted *"`cmd_send` has no size guard"* in **three** places. The guard shipped
in PR #40. `cos`'s child found **one** and routed it; product verified the class and found
three (6,002 bytes rejected; 6,000 accepted). **Same disease as a stale blocker and a stale
`delegated_to[].status`.** Fixed in the same PR as this map — *and the fix is itself a claim
that will rot.*

---

## 4. Gap-register entries touching messaging / escalation / checkpoints

**Live:**

- **G8** — delivery to the inbox ≠ delivery to the agent. **Third rung, added this session:**
  delivery to the agent's *context* ≠ **receipt**. The hook acked on the strength of having
  *rendered*.
- **G10** — the 8,000-char injection cap **cannot withhold the first message**; a lone oversized
  body bypasses it entirely.
- **G13** — every agent shares one git working tree. **Decided no-op** by the operator, twice,
  with the data loss on the table. Re-verified live: the hazard resets at every swarm's birth.
- **G16** — reading the operator's mail destroys it (`--json` included). **Half-fixed.**
- **G19** — the injection frames a directive exactly like a peer's opinion, and the header calls
  the operator *"other agents."* **The capped header is honest; the uncapped one is not** — and
  the uncapped path is the shape of the motivating incident.
- **G22** — a blocker is a claim about the present, and **nothing ever re-checks it**.
  `release-mgr` found **both** of its own blockers stale. The operator's generalization of this
  is what halted the work.
- **G18** — `restore-state`'s injection grows every cycle, uncapped. `progress_summary` is
  injected **1:1 forever** and *the reconcile ritual instructs agents to grow it*: every agent
  that ever reconciled is **15–46× the schema's own hint**; the only one at 1× never reconciled.

**Resolved this session:** G14 (four strikes across two agents *who both knew about it*; closed
by `--stdin`), G17 (messages >64 KB silently destroyed; the hook's own comment reasoned about a
*crash*, and a **half-write is not a crash**), G20 (legacy mail unackable).

**Method hazards the org discovered about itself, all found by execution:**

- **G21** — `SWARM_AGENT_ID` selects the code path under test **and** marks the process an agent.
  A test that never ran the path *looks like a passing check*. Bit three agents in a week.
- **The tenth species** — *a correct answer to a well-formed question that is not the question
  the claim depends on* (`git tag | tail` sorts lexically; product nearly reported a
  release-integrity failure).
- **The instrument can be the corrupted thing** — `release-mgr` measured `$?` **after a pipe**
  while writing a rule about measurement. Its words: *"I used a corrupted instrument to describe
  the corruption of instruments."*

---

## 5. Philosophy vs. the shipped system

`PHILOSOPHY.md` is *discovered, not invented* — each principle grounded in a decision the
operator actually made. **Where the system does not match it:**

| Principle | Where the system diverges |
|---|---|
| **§2 Incentives over guardrails** — *"the agent should just know… recursive goal reconciliation is gonna be the answer"* | The halted work is a **guardrail** (a nag, a hard cap) bolted onto an incentive problem. The operator's halt is, in effect, §2 asserting itself. |
| **§4 Judge artifacts, never claims** | **105 `done` tasks, all self-claims, zero judged.** The system has no instrument to check them — 006's fifth rider is the first attempt. |
| **§8 Conventions earn their tooling** | The invariant *"a `done` task has no blockers"* re-opened **three times in two days**, each time in the agent that had most recently argued it. The convention did not earn tooling; it demonstrated it needs it. |
| **§9 Keep the operator's channel clean** | The operator **is a mailbox, not a node**: no pane, no doorbell, no hook. He is the one recipient with **no push**. A directive to him waits until he polls. |
| **§10 Correct the record against yourself** | **Honoured, repeatedly and expensively** — retractions printed in place, faults handed back. This is the one place the system exceeds its philosophy. |

**The uncomfortable pattern, four-for-four, each inside its author's own expertise:**

- `cos` hit the backtick trap *while warning three children about its sibling.*
- `product` was bitten by the mitigation *it had itself filed.*
- `release-mgr` measured `$?` through a pipe *while writing a rule about measurement.*
- `product` retracted a **true** correction *because retracting felt like the rigorous act.*

**The rules do not protect the person holding them.** Every one of these was caught by *another
agent with no stake in the answer.* That is the only load-bearing property this org has
demonstrated — and it is exactly what the contractor is being hired to supply.

---

## 6. Open questions nobody has answered

1. **Is a recipient-side nag ever legitimate under G22?** If the reader of the trace cannot be
   the recipient, what reads it? (The operator has no hook. A parent has no view into a child's
   inbox. Nothing else exists.)
2. **Should the injected prefix stay outstanding?** Product recorded the trade and **refused to
   recommend**: re-injecting unacked bodies every turn is the accretion 006 exists to kill;
   dropping them is the silent deletion. Nobody has broken the tie.
3. **Is the operator/agent ack asymmetry right?** Never argued. C3.
4. **What reads `updates/`?** 003's archive verb and the unbounded output were replaced, not
   decided. `swarm updates` still prints the entire history, every time.
5. **What does `tasks[].status = "done"` mean?** Ruled this session, **documented nowhere in the
   product**. C5.
6. **Does `delegated_to[].status` rot?** Yes — `cos` found a dead `in-flight` record in its own
   file, for a child that was dead and whose PR had merged. It is **free text**; nothing
   validates it. **The approval record is exactly as trustworthy as a blocker.**
7. **Who audits the auditor?** `cos`'s third method — *verify what you are told, then the class,
   then the instrument you used to verify* — is the only discipline of the four that product has
   **not** adopted.

---

## 7. What product believes, stated plainly so it can be attacked

- **The operator is right that his own theorem indicts his ruling**, and product should have
  caught it. Product wrote G22, wrote the `delegated_to` answer, and then helped design a nag
  whose reader is its subject.
- **The halt is correct and cheap.** Nothing is installed. `cos` held the fast-forward on its own
  judgment, before the halt arrived.
- **The most dangerous thing in this document is not any single gap.** It is that *"a document
  is a claim about the present, and nothing re-checks it"* — which makes this map itself a
  decaying artifact. It is true at `451a2ec`. **Verify it against the code before you trust it.**
