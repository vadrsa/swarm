# VENTURE-01 — what swarm has, who would pay, and how (v2, post-review)

**Author:** `venture`, 2026-07-14. **Research base:** `research/MARKET.md`, `research/BUYERS.md`,
`research/HERDR.md` (all dated 2026-07-14, full sourcing inside), plus this repo's record
(PHILOSOPHY.md, SIMPLEST.md, FLEET-EVAL-V3.md, RND-FORK.md, the POWERS catalogues).

**Review status: adversarially reviewed.** `vent-red` (operator-commissioned, hostile brief) killed
two load-bearing claims, wounded one, and confirmed systematic one-directional cherry-picking in
v1's market sections — full review at `VENTURE-01-RED.md`, and §8 below records what died. I
independently re-verified the review's most load-bearing new fact (the Fora Soft rate card) before
folding it. Evidence tags: **VERIFIED / DOCUMENTED / MEASURED / REASONED**, plus
**VENDOR-REPORTED** (a tier this document lacked in v1, added on the reviewer's finding).

---

## 0. The answer, up front — stated honestly this time

**You cannot sell swarm's code.** The entire market gives orchestration logic away free (VERIFIED,
MARKET.md §1); the money lives in tokens, hosting, and observability; swarm's repo is public with
zero stars.

**The moat question is settled, not open: swarm has no software moat, and the discipline is not
one either.** The house practice — judged artifacts, adversarial review, evidence tags,
retractions kept — is published in this public repo and is reproducible by a competitor in an
afternoon as a system prompt. What is not copyable is the demonstrated ability to *operate* it.
**The moat is the operator's skill. Therefore the business this evidence supports is a
consultancy, and a consultancy does not scale past its operator.** (The red team pressed this to
the end; I concede it rather than rebut it. Whether the discipline can *transfer* to a second
person has never been tested — that experiment is cheap and is now on the list, §6.)

**The market for the recommended offer is not open — it is occupied and priced.** Fixed-price
code audits with explicit AI-agent leverage are sold today at **$2k–$8k (MVP), $8k–$25k (SaaS),
$25k–$60k (enterprise)** by Fora Soft, with competitors from $2,500 (Beesoul, Varyence). Fora
Soft audits AI-generated codebases *weekly*, and reports agent leverage compresses audit
timelines by **~30% — not 10x — while keeping senior human review** ("tools find ~60% of issues,
humans catch the architectural ones"). (VERIFIED — found by the red team, re-verified by me
directly against forasoft.com's published article.) v1 claimed this ground was open; that was
false and is retracted.

**The recommendation, restated with its honest name:** become a **boutique verified-audit
consultancy** — enter the occupied $2k–$60k market with the one asset the red team attacked and
could not bring down: **the deliverable format.** Nobody in the priced competitive set publishes
an adversarial-review section showing which of the auditor's own draft findings died under
attack. That is checkable by a buyer, novel in the category, and it is exactly what this document
itself is. It is a differentiator and a go-to-market window, **not a moat** — a boutique could
copy it in one engagement; windows close, and the plan must move through it, not live in it.

**One blocker before any fixed-price offer (red-team finding, conceded in full):** `bin/swarm`
has **zero cost accounting** — no spend, no budget, no dollar anywhere in its 1,753 lines
(VERIFIED at the source). The observed failure mode is my own subtree burning **$79.72 on one
research question** with nobody steering (MEASURED). A fixed-price contract signed on an
uninstrumented tool makes every overrun the seller's. **Until `swarm ps` shows per-subtree spend
and a spawn can be refused on budget, sell capped-cost or time-and-materials with the cap passed
to the client — never fixed price.** v1 deferred this behind the first sale by a category error
(it filed the cost oracle under "self-reliance" when it is the seller's solvency mechanism); it
is now track zero.

**And the question this analysis cannot answer, which belongs to the operator:** the evidence
names the business that actually exists — *a real, profitable-looking job with good margins,
capped by one person's review attention, whose moat is that person's name.* **Do you want the job
that exists, or should this arm keep looking for the business that doesn't?** Everything below
serves that decision.

---

## 1. What we actually have — the honest inventory

| Asset | What it is | Honest value |
|---|---|---|
| `bin/swarm` | 1,753 lines of Python, 4 verbs, public, 0 stars | As sellable code: ~zero (market price of orchestration is $0, VERIFIED). As design: real, and public. **And it cannot see its own cost** — no spend accounting at all (VERIFIED) — which is now the top build item. |
| The doctrine + record | 10 principles pinned to quoted decisions; a 27→9 concept reduction justified by measured usage; ~230 journals; reviews that flipped verdicts; retractions kept | **Copyable in an afternoon — it is all published.** (Red team, conceded.) The unpublished asset is the operating skill, which is a person, not a property. Whether it transfers to a second person is untested — v1 listed this as an asset; it is a hypothesis. |
| The deliverable format | Evidence-tagged findings + a published adversarial-review section showing which draft claims died | **The one thing the red team attacked and could not kill.** No priced incumbent publishes a record of the auditor being wrong. Differentiator, not moat. |
| The loop mechanisms | 53 invented, 24 killed with reasons, 3 built and red-teamed; the landing-turn triage result (n=1, against the TRIAGE paper's null) | Research-grade credibility; acquihire-grade portfolio; not legal IP. |
| The evals + cost anatomy | FLEET-EVAL-V3 (n=1 per cell, "shapes not rates"); ~$2.58/message delivery cost; 58.6% of spend = cache reads (MEASURED) | Scarce operational knowledge; publish for credibility, don't sell. **Honest addition the red team forced:** Stanford/Contextual (arXiv 2604.02460, VERIFIED in MARKET.md) finds single agents match or beat multi-agent under *equal token budgets* — the swarm may buy some of its results with tokens, not structure. That risk attaches to the org itself and belongs in this table. |
| herdr | Third-party OSS (16,275 stars, Homebrew core, verified by me) | Asset, not elephant: one `brew install`, shallow coupling, sever-to-tmux held in reserve. Depend, don't bundle — GitHub reports the license as "Other/NOASSERTION," so a real read of the LICENSE file precedes any bundling decision (red-team nuance, folded). |
| Releases + first outside user | v1.0→v1.3.2, first stranger's bugs fixed | The beginning of self-reliance; no distribution yet. |

---

## 2. Who the buyer is — sharpened by the review

**The user (validates, does not pay):** the parallel-agent power user — real and named (Karnal,
Chacon, Steinberger, Willison, Schumaker — VERIFIED quotes, BUYERS.md §5). Ceiling of 2–5
supervised agents; the wall is human review attention. They are audience and credibility; the
product class converged at $20/mo; they hand-roll tools. Not the revenue.

**The buyer (pays):** the review's kill of v1's evidence forces precision here, and the precision
helps. The priced incumbent's actual customers are **M&A acquirers, Series A founders, and VCs in
due diligence** (VERIFIED, Fora Soft's own positioning — they cite an audit moving a $4M deal).
That is the right first buyer for us too, for a reason v1 missed: **a diligence buyer is buying
an attestation for a third party, not engineering labor.** The documented discount pressure —
clients demand 50–70% off when agents are disclosed (BUYERS.md §3) — applies to labor, where
"an agent did it" means "it cost you less." It plausibly *inverts* for attestation, where the
question is "can I defend this finding to my investment committee?" and a published
adversarial-review trail is added value. (REASONED — this is the argument v1 needed and never
made. Falsifier: if diligence prospects also lead with the discount demand, the inversion is
wrong and the pricing premise fails with it.)

**Evidence corrections from the review, accepted in full:** LG CNS is **not** proof of
agent-delivered work — it is a 200-engineer org running pods of 5–7 humans per project
(VERIFIED); it proves the opposite: at scale this work currently requires a human pod. Huntley's
$297/$50k is an unaudited self-report of what *he spent*, not what a client *paid* — struck as
margin evidence. Globant remains the best unit-of-sale evidence and remains alone (no imitators,
no number).

---

## 3. The moat — settled

The red team's ruling stands with my concession: **the discipline is copyable; the moat is the
operator's skill; the business is a consultancy.** What survives, correctly named:

1. **The deliverable format** — differentiator, not moat (§0). Real reason a first diligence
   buyer picks us over Fora Soft; copyable by any boutique that decides to eat one engagement's
   embarrassment.
2. **A go-to-market window, not a moat:** incumbents have a live incentive *not* to publish
   their error record or lead with agent involvement (they bill hours; freelancers conceal AI
   use — CHI 2026, DOCUMENTED). Windows close and cannot be defended.
3. **Reputation** — a real moat that accrues to a *person*, which is a consultancy's moat and
   the correct name for what compounds here.
4. **The research portfolio** — credibility/acquihire value; an outcome, not a strategy.

Against the named competitors: Anthropic ships subagents and can ship the discipline as a prompt
template whenever it wants — assume it. LangGraph/CrewAI sell hosting/observability around free
frameworks with nine-figure funding — do not fight there. The service is what they structurally
won't do: accountable delivery on a specific stranger's codebase, with the error record public.

---

## 4. The self-reliance gap — reordered by the review

**Track zero (blocker — before any fixed-price offer, not behind it):**
1. **Cost visibility and control in the main tool.** Per-subtree spend in `swarm ps`; a spawn
   refusable on budget. Not a self-reliance feature — the seller's solvency mechanism. The R&D
   fork's budget wall is the head start; it is not shipped. Until then: capped-cost/T&M only.
2. **Span guard as product doctrine** (~3 children, depth 2, no relay layers — the rule the
   operator imposed on me by hand after the $79.72 runaway). A stranger hits the same failure
   with nobody watching.

**Track one (blocks a stranger, not a sale):** the Claude Max prerequisite stated on the front
page ($100–200/mo — the tool's real entry price); a first-30-minutes walkthrough (nobody has
ever watched a stranger attempt one); CI and a test gate; WSL untested; the trust/permission
story on a stranger's machine.

**Resolved:** herdr (one brew install; depend-don't-bundle pending a LICENSE read).

---

## 5. How it makes money — the map, corrected

| Route | Verdict after review |
|---|---|
| Sell/license the software | Dead — market price is $0. (Unchanged.) |
| Hosted SaaS swarm | Dead — hosting arms race vs $1B+ incumbents, destroys the subscription economics. (Unchanged.) |
| Agent-ops/observability product | Real category, consolidating fast; **and the review adds the disconfirming datapoint v1 omitted: W&B Weave is ~2% of W&B's ARR** — even inside a company built for it, the agent-ops product can lag. Downgraded from "natural second product" to "possible later, evidence mixed." |
| **Boutique verified-audit consultancy** | **RECOMMENDED — with its honest name.** Occupied market ($2k–$60k rate card, VERIFIED), human-in-the-loop confirmed as the throughput unit by the incumbents' own numbers (~30% compression, not 10x), differentiated by the deliverable format, first buyer = due-diligence context. **It is a job with good margins, capped by the operator's attention, and its moat is the operator's name.** Whether that is wanted is the operator's call (§0). |
| Enterprise license / marketplace / sell evals | No path at our scale. (Unchanged.) |
| Acquisition/acquihire | An outcome, not a strategy. The portfolio makes it possible; something above must work first. (Unchanged.) |

**What must be true — revised, with the review's corrections:**
1. A diligence buyer pays the occupied market's going rate for the differentiated deliverable
   (test: 5 pitches priced against the incumbent rate card, not against anecdotes).
2. The attestation-inverts-the-discount argument (§2) survives contact with real prospects.
3. Cost control exists in the tool before any fixed price (track zero; capped-cost/T&M until).
4. Judgment-hours per engagement fall across the first three — **measured on a capped-cost
   contract, not discovered on a fixed-price one.** (The review's point, conceded: the evidence
   base already predicts the human is the bottleneck; do not run the experiment on the client's
   money at our risk.)

**Base rates, stated because a venture doc owes them (omitted in v1, restored):** Gartner —
89% of AI agent pilots fail to reach production; McKinsey — under 10% of enterprises have scaled
any agent to tangible value (DOCUMENTED, MARKET.md §4). The consultancy shape partially sidesteps
these (we sell delivered outcomes, not deployed agents), but they cap every software-flavored
branch of this plan.

---

## 6. What to build first — revised

1. **Track zero: the cost readout** (per-subtree spend in `ps`, budget-refusable spawn). It is
   the cheapest falsifier of the review's strongest surviving objection — "engineering, not
   argument" — and it feeds the engineering arm's build list immediately.
2. **The specimen, rebuilt around the surviving asset:** run the swarm on an unfamiliar,
   AI-generated codebase (the incumbents say that category arrives weekly) and produce the audit
   *with the adversarial-review section as the centerpiece* — which draft findings died, and
   who killed them. Price it against the $2k–$60k rate card. Publish the cost sheet.
3. **The transfer experiment (tests the settled moat claim at almost no cost):** hand the public
   documents to one person who is not the operator; see whether the discipline produces a
   comparable deliverable with no author present. If it transfers, the consultancy has a second
   seat and the "does not scale" ruling weakens. If it doesn't, we know the moat's true radius
   before pricing anything on it. (This is the red team's own falsifier for its ruling A,
   adopted as work.)
4. **Then 5 pitches to diligence buyers** on capped-cost terms. First paid engagement = the
   business exists; 0-for-5 = change the deliverable shape before declaring the route dead.

---

## 7. What would kill this, and how we'd see it coming

| Kill | Watch |
|---|---|
| Anthropic ships judged/verified agent work natively | Claude Code release notes, Agent SDK changelog — standing duty; the operator hears the day it happens. |
| Diligence buyers demand the agent discount anyway (the §2 inversion fails) | The 5 pitches. This is now the recommendation's sharpest single risk. |
| An engagement's cost runs past its cap | Track zero readout; until it exists, no fixed price — structural, not aspirational. |
| Incumbents copy the deliverable format | Their published samples. It costs them one embarrassing engagement; expect it within quarters of our first public specimen. The plan must convert the window into reputation before it closes. |
| One bad public delivery | Adversarial review on every deliverable — non-negotiable, and now demonstrated (this document survived its own). |
| The equal-budget finding generalizes (arXiv 2604.02460): the swarm's structure adds cost, not quality | Replicate FLEET-EVAL under equal-token-budget conditions — an eval-arm task worth commissioning. |
| Operator capacity / the transfer experiment fails | Judgment-hours across first three engagements; §6.3's result. |

---

## 8. What the red team killed — kept, per house law

v1 of this document claimed: the audit market was open ground (**killed** — occupied at
$2k–$60k, VERIFIED); LG CNS proved agent-delivery works (**killed** — it proves a human pod per
project); the scaling question was open (**killed** — the incumbents ran it: ~30%, human kept);
enterprises rank trust above "multi-agent capability itself" per a CrewAI survey (**killed** —
vendor-run, no methodology, and multi-agent was never a ranked option; replaced by the stronger
independent evidence: Merck buys Langfuse for auditability, every agent-ops vendor meters
reliability separately); the moat was "partly" the operator's skill (**wounded** — the "partly"
was the evasion; it is the operator's skill); and v1's synthesis dropped six hostile market
findings, every one cutting the same direction (**confirmed** — METR, Greptile, the discount
finding, Gartner/McKinsey base rates, W&B Weave, and the equal-budget paper are now in the text
above). The reviewer's full arguments: `VENTURE-01-RED.md`. What it could not kill: the
deliverable format — which is why §6 now builds the specimen around it.
