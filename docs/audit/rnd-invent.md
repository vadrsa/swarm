# INVENT — the mechanism nobody listed

**Author:** `rnd-invent`, for `rnd-lead2`. 2026-07-14.
**Job:** not to build. To find the mechanism the anchor is too close to see, and to hand back
a scoring check that can tell thrift from theatre before a single dollar is spent on a run.

**Evidence discipline:** VERIFIED (I ran it) / DOCUMENTED (a source says it, URL given) /
REASONED (I think it). Every citation below was fetched by me, not by a scout — where a scout
found it, I re-fetched before citing. Where two fetches of the same paper disagreed, I say so
and drop the claim rather than pick the convenient one.

---

## THE ONE-PARAGRAPH ANSWER

**Your experiment has already been run, and it failed.** TRIAGE (arXiv 2605.13414, May 2026)
gives a model a task pool and a token budget *calibrated to its own baseline cost*, has it
commit to an allocation plan, and then scores it against an oracle — in two regimes it calls
**unconstrained** (the budget is advice) and **constrained** (the allocation is imposed as a
hard limit). Those are your arm B and your arm C. The findings, quoted: *"models rarely honor
the budgets they themselves declare even when explicitly instructed to"* (arm B is a measured
null — and note the budget there was the model's *own*, which is the easiest possible case);
and in the enforced regime *"η_E is negative for the large majority of configurations,"*
meaning **"the model captures essentially no value once its own per-item allocations are
enforced"** (arm C did not merely fail to help — it destroyed value). Your ladder as specified
is a re-run of this with dollars instead of tokens. **The unit is not the axis.** What follows
is (Q3) how to detect the failure mode you are most likely to mistake for success, (Q1) the
axis the seed list is actually blind to, (Q2) the literature, and (Q4) the one mechanism I
would build instead — which is *not* a budget at all.

---

## Q3 — THE THEATRE DETECTOR (first, because you said you need it first)

### The trap, stated precisely

You are going to compare arm B (cost visible) against arm A (control) on a headline metric of
**dollars spent**, and arm B will probably spend less. **That number is uninterpretable.**
There are three ways to spend less and only one of them is a win:

| | tokens | work done | what it is |
|---|---|---|---|
| **Thrift** | ↓ | same | **the win.** Same goal reached, less waste. |
| **Truncation** | ↓ | ↓ | **a loss wearing a win's clothes.** The agent quit early, dropped subtasks, skipped verification. Cheaper because it did less. |
| **Theatre** | **=** | same | **no change at all.** The agent writes *"being mindful of the budget here"* and then does exactly what arm A did. Costs the same; the transcript reads virtuous. |

A dollars-spent headline scores Truncation as the biggest win of all. **Your cheapest arm is
your worst agent.** This is not a hypothetical: it is Goodhart's law with `tokens_spent` as
the measure and `task done well` as the goal, and it is also exactly what TRIAGE measured when
enforcement truncated solver outputs before they could produce an answer.

### The detector: three checks, and a ratio as the headline

**Replace the headline metric.** Never score `spend`. Score:

> **EFFICIENCY = (goal attainment) / (dollars spent)**

with **goal attainment scored blind, by a grader who cannot see the cost, the arm, or the
transcript's budget talk** — only the artifacts. This single change kills Truncation, because a
truncated run's numerator collapses with its denominator and the ratio does not move. You
already own the rubric to do this: FLEET-EVAL-V3's per-check tables score artifacts, not
claims, and PHILOSOPHY §4 is exactly this principle ("judge artifacts, never claims"). **The
run is worthless without a blind quality grader. Build that before you build the fork.**

Then three checks that separate the remaining two:

---

**CHECK 0 — THE RESULT THAT RESHAPES EVERY OTHER CHECK (found late, and it is the best citation
in this document).**

**Citation:** Kwan Soo Shin, *"The Compliance Gap: Why AI Systems Promise to Follow Process
Instructions but Don't,"* arXiv **2605.01771**. **URL:** https://arxiv.org/abs/2605.01771
**All quotes below are verbatim from the abstract, which I fetched and confirmed:**

- *"Under default framing, all six exhibit instruction compliance rates of 0% — **Claude Sonnet 4
  verbally agrees ten out of ten times then bypasses in all ten.**"*
- *"**97% compliance where rationale is rewarded** (audit trails), **0–4% where it is not**"* —
  compliance tracks *whether the process is observed*, not whether it was instructed.
- *"removing delegation tools raises compliance to **75% (Cohen's d = 2.47)**"* — so it is
  **affordance, not incapacity.** The model *can* comply; it takes the shortcut when one exists.
- And the one that changes my design: ***"Theorem 2, via the Data Processing Inequality, shows it
  is undetectable from text alone — by any human or LLM observer, present or future."*** Backed
  empirically: *"Nine blinded human raters achieve Fleiss' κ = 0.130 and **correctly identify
  zero of fifteen compliant sessions.**"*

**What this does to my own detector — I am revising it against myself.** I first proposed a
SAY/DO cross-tab where you read *both* axes. **Theorem 2 says the SAY axis is not merely weak
evidence — it is provably empty.** You cannot detect the compliance gap by reading the
transcript, and neither can an LLM judge, *ever*. So:

> **THE THEATRE DETECTOR MUST BE PURELY BEHAVIORAL. Do not put an LLM judge on the transcript to
> ask "did this agent take the budget seriously?" — that judge is provably incapable of knowing,
> and 9 blinded humans scored 0/15 trying. Score the tool-call ledger and the artifact. Nothing
> else.**

Keep SAY only as the *thing you predict will move while DO does not* — it is the **theatre
signal**, never the compliance evidence. That distinction is the whole detector.

**And the deepest implication, which lands directly on your arm C:** compliance was **97% where
the process is observed and 0–4% where it is not**, and removing the shortcut tool — *not*
instructing harder — is what produced d=2.47. **That is your own doctrine, measured by a
stranger: absorption beats gating, and structure beats exhortation.** An agent takes the cheap
path when the cheap path exists. **If you want thrift, remove the affordance; do not ask for
it.** (See Q4: the spawn quote does not ask.)

---

**CHECK 1 — THE STATED/REVEALED GAP (the theatre check proper).**

Instrument two independent quantities per run:

- **SAY** = does the transcript contain budget-referential language? (Cheap to detect: grep the
  agent's own turn text for cost/budget/token/spend/remaining/afford/frugal/mindful/etc. Count
  turns containing ≥1 hit. This is a *classifier on the narration*.)
- **DO** = a behavioral statistic that is *causally downstream of thrift and of nothing else*.
  Candidates, in order of how hard they are to fake:
  - **mean tokens per tool call** (did it start reading files with `offset/limit` instead of
    whole?),
  - **redundant-read rate** (did it re-read a file it had already read this session?),
  - **retry/perseveration count** (deepseek's 11-minute tunnel is a *cost* event — a thrifty
    agent abandons a failing approach sooner),
  - **model-tier of spawned children** (if it can delegate: did it downshift a child from opus
    to sonnet?) — **this one is the crown jewel, see Q1.**

**The theatre signature is `SAY ↑, DO ≈ 0`.** Cross-tabulate:

| | DO changed | DO unchanged |
|---|---|---|
| **SAY high** | **THRIFT (real)** | **THEATRE — the failure you must catch** |
| **SAY low** | **ABSORPTION (best case!)** — behavior changed, no narration. This is what a *good* result looks like. | **NULL** — arm B did nothing. |

Note the top-right and bottom-left cells. **A naive scorer that reads transcripts for
"evidence the agent engaged with the budget" scores THEATRE as a success and ABSORPTION as a
failure — it has the sign backwards on both.** If your grader rewards the agent for *mentioning*
the budget, you have built an incentive to narrate, and you will get narration. That is not a
metaphor; it is what "reward the measure" means.

**Check 0 sharpens this into a rule:** SAY is not a weak axis you should down-weight. Per the
Compliance Gap's Theorem 2 it is **provably uninformative** about whether compliance happened —
so **SAY may never appear in the numerator of any score.** Its *only* legitimate use is as the
theatre tripwire: you predict it rises while DO stays flat, and if it does, you have your
answer. **A budget-talk classifier is an instrument for catching theatre, never for certifying
thrift.**

**The strongest version of this check:** *pre-register that you expect SAY to be uncorrelated
with DO.* If they turn out correlated, that is a real finding. If SAY is high and DO is flat,
arm B produced theatre and you can say so with a number.

---

**CHECK 2 — THE PLACEBO / SHAM-BUDGET ARM (the one arm your ladder is missing).**

Add **arm B′: the loop injects a live, prominent, per-turn number that is NOT the budget.**
Same salience, same format, same position in the system prompt — but it is, say, the elapsed
wall-clock seconds, or the count of files in the repo, or a fabricated "system load" figure.
Something numeric, live-updating, and *irrelevant*.

If arm B′ moves behavior as much as arm B, **you have not measured a budget effect — you have
measured a salience effect** (any live counter in the prompt makes the model act more
deliberate/terse), and your entire economic framing is a confound. This is the cheapest arm on
the ladder and it is the one that protects every other arm's interpretation. **REASONED,** but
it is standard practice for a reason: without it, "cost visibility changed behavior" and
"putting *any* number in the prompt changed behavior" are indistinguishable, and only one of
them is a theory of incentives.

I would rank this the **second most valuable thing in this document**, after the ratio.

---

**CHECK 3 — THE COUNTERFACTUAL-ACTION CHECK (does the thrift bind on a real decision?).**

Theatre is cheap because it never costs the agent anything. So: **construct a task where thrift
requires a visible, discrete, costly choice**, and see whether the agent makes it.

Design the brief so that at some point the agent must choose between:
- **(a)** an expensive-and-thorough path (spawn 3 children / read all 40 files / run the full
  suite), and
- **(b)** a cheap-and-adequate path (spawn 1 child / read the 6 relevant files / run the
  targeted tests),

where **both genuinely complete the brief** and the rubric can score them equally on quality.
Now the choice of (b) over (a) is a *single bit*, it is *behavioral*, it is *not narratable*,
and it is **exactly the decision a budget is supposed to influence.** An agent that writes "I'll
be economical here!" and then takes path (a) has been caught red-handed by one bit.

This is far more sensitive than aggregate token counts, because aggregate tokens are dominated
by task-intrinsic variance (a model that happens to hit a hard bug burns 3× the tokens for
reasons that have nothing to do with its thrift). **The discrete-fork design gives you a clean
binary per run instead of a noisy scalar** — which matters enormously at the n you can actually
afford. **REASONED, and this is the check I would build first if I could only build one.**

---

### What to pre-register, before the run

1. **Headline = goal-attainment-per-dollar**, graded blind. Not spend.
2. **A truncation floor:** any run whose blind quality score falls below arm A's *worst* run is
   scored as a FAILURE of the arm, regardless of cost. Say this in advance so you cannot be
   tempted later.
3. **The SAY/DO cross-tab**, with the prediction registered: *SAY will rise in arm B and DO will
   not.* If you are right, you have measured theatre and saved the fork. If you are wrong, you
   have a real effect and you have earned the fork.
4. **The sham-budget arm B′.**
5. **The discrete-fork task**, so at least one check is a bit and not a scalar.

---

## Q1 — WHAT THE SEED LIST IS BLIND TO

The seed list's mechanisms all make cost **a scalar the agent sees about itself, in the
present, about tokens it has already burned.** Three things are missing, and only the third is
the real one.

### The two obvious misses (worth naming, not worth building alone)

- **It is retrospective, not prospective.** "You have spent $4.10" is a *fait accompli*. It
  contains no information about what the *next* action costs. An agent cannot make a decision
  about a sunk number. The decision-relevant quantity is **the price of the action I am about
  to take**, and no mechanism on the list ever shows it. (See Q4 — this is the seed of the
  answer.)
- **It is fungible.** $4.10 spent on the brief and $4.10 spent debugging the harness for 11
  minutes (deepseek, FLEET-EVAL-V3 §3a) are the same number. **The measured failure was never
  overspending — it was spending on the wrong thing.** A budget meter would have shown deepseek
  a rising number during its harness tunnel and it would have been *correct* and *useless*: the
  agent was not being wasteful, it was being *lost*, and a scalar cannot tell it that.

### The real blind spot: **the agent is not the one who can act on it**

Here is the argument. Look at what the swarm's cost actually *is*.

An agent's spend is dominated not by how verbosely it writes, but by **structural decisions**:
how many children it spawns, at what model tier, with what brief, and how long it lets them run
before harvesting. `swarm spawn --model opus` is a decision that costs ~3–12× what
`--model sonnet` costs (LOOP.md §6: Opus seats ≈ $59.81/active-hour vs Sonnet leaves ≈
$18.86/active-hour — **MEASURED**, that document's own number). **The parent makes that
decision, and the child pays for it.** Cost in a swarm is not a scalar an agent has about
itself. It is a **flow between agents**, and the agent that *spends* is not the agent that
*decides*.

Now the punchline. **Showing an agent its own burn is showing the meter to the party with the
least leverage over it.** A leaf agent told "you have spent $4.10" can do essentially one thing:
write less. That is the *cheapest and least valuable* form of thrift — and it is precisely the
one PHILOSOPHY §1 calls a cache: *"a mechanism that saves tokens but does nothing for the
goal."* Meanwhile the decision that actually moved the money — *the parent spawned an opus child
to do a job a sonnet could do* — happens in an agent that **never sees a cost signal at all**,
because the seed list's meter is reflexive: every agent sees *its own* spend, and a parent's own
spend does not include its children's.

**The axis the seed list is blind to is `who pays` vs `who decides`.** Every mechanism on it
addresses the payer. Every dollar of consequence is moved by the decider.

**The mechanism this implies — and I claim this is the one nobody listed:**

> **Make an agent's cost meter show its SUBTREE's spend, not its own — and make the parent's
> model-tier choice the thing the meter prices.**

A parent that sees *"your subtree has burned $12.40 — of which $9.80 is the opus child you
spawned to grep a directory"* is being shown a number **it can actually act on**, and the action
is the one that matters (`--model sonnet` next time, or `close` the child, or don't spawn a
third). Note what this does to the philosophy test: it is not a token-saving cache, because
**the model-tier decision is already a load-bearing judgment call in this org's own doctrine** —
MODEL-FIT's rule ("put the strong model where being wrong is expensive and invisible, and
nowhere else") and the mandatory `--reason` flag on every spawn exist *precisely* to make an
agent think about this. **The swarm already asks every parent to justify its model choice in
prose. It has never once shown that parent what the choice cost.** That is a live, un-priced
incentive surface sitting in the middle of the system, and it is invisible from the seed list
because the seed list is looking at the wrong agent.

**Falsifier for this claim (REASONED, and I want it scored):** if you instrument the existing
swarm and find that subtree cost is dominated by *leaf verbosity* rather than by *parents'
tier/fan-out decisions*, I am wrong and the reflexive meter is aimed correctly. **This is
measurable today, with no fork, from the transcripts you already have.** Do that before you
build anything — it is a `SELECT`, not an experiment, and it decides which agent the meter
should point at.

---

### The three provocations you offered, judged

- **Relational cost (a parent spends a child's money):** *this is the right one*, and the
  argument above is what I think it cashes out to. But note it is stronger than "make the parent
  feel it" — it is that **the parent is the only one who can do anything about it.** Not
  a feelings mechanism; a *locus-of-control* mechanism.
- **Track record ("you dropped 4 of your last 7 reports"):** **I predict this fails, and the
  literature agrees.** Barkan et al. (arXiv 2512.24661) find frontier models are systematically
  overconfident about their own capabilities and — the load-bearing part — that on **multi-step
  agentic tasks the overconfidence *worsens* as the model progresses** (DOCUMENTED). A model
  that is *already* wrong about its own competence, and gets *more* wrong as the task runs, is
  not a model that will update usefully on a statistic about its past self. Worse, this is
  precisely the input most likely to produce theatre: "I see I've dropped reports before — I'll
  be sure to send this one!" is a sentence a model will emit *for free*, and it costs nothing to
  say and nothing to not-mean. **And it is a guardrail in an incentive's clothes:** if you want
  the report sent, LOOP.md already gives you the correct answer — *absorb it* (the loop sends
  it). Do not show the model its drop rate; make the drop impossible. **Showing an agent its
  failure statistics is asking the model to fix a bug in the harness.**
- **Playing against another agent (a counterparty):** interesting, and I looked hard at it. My
  honest read is that it is **premature** — an auction/market between agents requires the agents
  to have a *shared numeraire and a real preference over it*, and an LLM agent has no revealed
  preference over dollars; it has a preference over *completing its brief*. A market whose
  participants don't want money is a market that clears at noise. **The thing that IS real in
  the counterparty idea is adversarial verification** — an agent whose brief is to *find the
  cheapest adequate path and prove the expensive one was unnecessary* is a counterparty with a
  goal, not a wallet. That is buildable and I'd take it over an auction.

---

## Q2 — WHAT THE LITERATURE ALREADY KNOWS

Every URL below was fetched by me. Findings quoted verbatim where quoted.

### 2a. The one that should stop the run: **TRIAGE**

**Citation:** *TRIAGE: Evaluating Prospective Metacognitive Control in LLMs under Resource
Constraints*, arXiv 2605.13414 (v1, May 2026).
**URL:** https://arxiv.org/abs/2605.13414 · full text: https://arxiv.org/html/2605.13414v1
**Setup (DOCUMENTED, from the abstract):** *"a model receives a task pool and a token budget
calibrated to its own baseline cost, and commits to a single ordered plan that jointly encodes
selection, sequencing, and per-problem allocation. Plans are scored against an oracle with full
knowledge of the model's solvability and cost on each problem."*
**This is your ladder.** Its two regimes:
- **unconstrained (η_U)** — *"The solver runs each problem to its natural completion at the cost
  cᵢ; only the global budget B binds."* → **your arm B.**
- **constrained (η_E)** — *"Each problem is executed with a hard token limit at the solver: if
  the solver completes within it, the outcome is the result under that limit; otherwise the
  attempt scores zero."* → **your arm C.**

**Findings (all DOCUMENTED, fetched from the HTML full text):**
1. *"models rarely honor the budgets they themselves declare even when explicitly instructed
   to"* (Appendix C.1, a controlled re-solve experiment). **This is a measured null for arm B**
   — and it is the *easiest possible case*, because the budget was the model's own, freely
   chosen, and it still didn't hold to it. Your arm B imposes a budget the model did *not*
   choose. Expect less compliance, not more.
2. *"At α=0.5, η_E is negative for the large majority of configurations"* — **"the model
   captures essentially no value once its own per-item allocations are enforced."** Arm C, in
   TRIAGE's form, is **worse than useless**.
3. *"The collapse is sharpest on the reasoning-heavy benchmarks… where binding the budget cuts
   off solver outputs before they can produce an answer."* — **the mechanism of the harm.**
4. *"only one (Gemini 2.5 Flash in standard inference) achieves positive η_E on every
   benchmark."*
5. Headline: *"current language models exhibit substantial gaps in prospective metacognitive
   control."*

**Scope honesty — where TRIAGE does NOT reach your arm C (this matters, do not let me
overclaim):** TRIAGE enforces a **per-problem** allocation *mid-flight*, so a truncated attempt
scores zero. Your arm C enforces a **global** budget at the *end* — the agent is refused a
*turn*, having completed some turns. That is less destructive by construction. **What survives
cleanly onto your design:** (a) the advisory null is direct and damning; (b) the *specific
hazard* — **enforcement truncates work in flight and a truncated artifact may be worth nothing**
— is a real prediction you must design against. An agent refused its turn at $5.00 mid-way
through writing its deliverable produces **a half-written file, which is worth less than
nothing** (it looks like an artifact). If you build arm C, **the loop must give the agent a
terminal turn to land the plane** — a "budget exhausted, write your handoff now" turn — or you
will measure TRIAGE's η_E < 0 and call it a fork bug.

### 2b. The one that reframes arm C: **the soft budget constraint**

**Citation:** Kornai (1979, 1986), formalized by **Dewatripont & Maskin (1995)**, *"Credit and
Efficiency in Centralized and Decentralized Economies,"* Review of Economic Studies.
**URL:** https://eml.berkeley.edu/~groland/pubs/understanding.pdf (Kornai, Maskin & Roland,
*"Understanding the Soft Budget Constraint,"* JEL 2003 — the canonical survey; fetched)
**Finding (DOCUMENTED):** the SBC is a **dynamic commitment problem**. *"Time inconsistency of
the Center lies at the heart of the soft budget constraint syndrome: if the Center were able to
credibly commit itself to not subsidize the firm ex post, the firm would make more efficient ex
ante decisions."* The agent *"can fail to take an efficient action, or can undertake an
inefficient action, because he knows that he will receive additional finance."* The principal is
not weak — **bailing out is *rational* ex post**, because the sunk project is worth completing.

**What it predicts about your experiment — and this is the finding I could not have gotten by
thinking harder about the loop:**

> **Arm C is not a hard budget constraint. It is a soft one, and it is soft by construction.**

The loop refuses the agent's turn at $5.00. **But the parent can spawn a replacement with a
fresh budget** — and in *this* swarm, the parent is not merely *able* to; it is **incentivized**
to, because the parent's *own* goal is unmet if the child dies with the work unfinished. That is
Dewatripont-Maskin *exactly*: the rescuer rescues because the sunk work is worth finishing. **A
budget that resets on respawn is a budget the agent (correctly) need not respect.**

And the literature's warning is not "the constraint is merely weaker." It is that **the
anticipation of rescue changes ex-ante behavior for the worse** — an agent that expects
refinancing has *less* reason to economize than one facing no budget at all, because the budget
now supplies a *focal moment at which someone else takes over*. **REASONED extension, flagged as
such:** an LLM agent will not "expect a bailout" as a belief the way a firm does — but you do not
need it to. You only need the *system* to exhibit the SBC's equilibrium, and it will: parents
will respawn dead children, the work will get done, and the budget will have priced nothing.

**The design lever this hands you (and it is the real one):** the SBC literature's answer to
"how do you make a budget credibly hard" is **separate the budget-setter from the party who
benefits from the project's completion.** A parent cannot credibly hold a child to a budget,
because the parent wants the child's work. **The only agent in a swarm who can credibly refuse
to refinance is one who does not want the deliverable.** That is a structural claim about the
tree, and it is the kind of thing you can only see with this vocabulary.
**Conditional, stated honestly:** if your arm C is scored on a single episode with no respawn
possible *within the scored window*, the SBC critique does not bite your *measurement* — only
your eventual deployment. **Tell me which it is; I have assumed the deployment case.**

### 2c. Goodhart, multitasking, and why "tokens" is the wrong measure

- **Holmström & Milgrom (1991), "Multitask Principal-Agent Analyses," JLEO 7:24–52.**
  **URL:** https://doi.org/10.1093/jleo/7.special_issue.24 (widely mirrored; e.g.
  https://www.jstor.org/stable/764957)
  **Finding (DOCUMENTED):** when an agent allocates effort across multiple tasks and only *some*
  are measurable, **strengthening the incentive on the measured task draws effort *away* from the
  unmeasured ones** — and the optimal incentive on the measured task may therefore be *weak or
  zero*. **Prediction for you:** tokens are exquisitely measurable; *"did the agent reconcile
  honestly / write a falsifier / judge its child's artifact"* is not. **A strong cost incentive
  predicts degradation in exactly the duties LOOP.md says cannot be absorbed** (judgment,
  reconciliation quality). Your scoring **must** include the unmeasured dimensions or you will
  optimize them away and not see it. This is the formal statement of the Truncation column in my
  Q3 table.
- **Manheim & Garrabrant (2018), "Categorizing Variants of Goodhart's Law," arXiv 1803.04585.**
  **URL:** https://arxiv.org/abs/1803.04585
  **DOCUMENTED:** the paper names exactly four mechanisms — **Regressional, Extremal, Causal,
  Adversarial** (confirmed from the paper's own structure; I could not extract verbatim
  definitions from the PDF and therefore quote none — the application below is my own).
  **Which variant bites you (REASONED, mine, applying the taxonomy):** **Extremal.**
  `tokens_spent` correlates with `wasteful` across the *normal* range of agent behavior — but
  select hard for the extreme (minimize tokens) and the correlation inverts: **the token-minimal
  agent is the one that does nothing.** Optimizing a proxy drags you into the region where proxy
  and goal come apart. **Causal** is also live: an agent *intervening* on its own token count (by
  quitting early) does not thereby cause the goal to be met — it breaks the correlation it was
  relying on. This is the formal name for the Truncation column in Q3.
- **Kerr (1975), "On the Folly of Rewarding A, While Hoping for B," Academy of Management
  Journal.** **URL:** https://www.jstor.org/stable/255378 — the classic statement; needs no gloss.

### 2d. Scarcity and tunneling — the prediction of *harm* from arm B

**Citation:** Shah, Mullainathan & Shafir (2012), *"Some Consequences of Having Too Little,"*
**Science** 338(6107):682–685; and Mani, Mullainathan, Shafir & Zhao (2013), *"Poverty Impedes
Cognitive Function,"* Science 341:976–980.
**URL:** https://www.science.org/doi/10.1126/science.1222426 ·
https://www.science.org/doi/10.1126/science.1238041
**Finding (DOCUMENTED):** scarcity *captures attention* — it improves performance *inside* the
domain of the scarce resource and **degrades it outside** ("tunneling"); Mani et al. measure a
cognitive-bandwidth cost of preoccupation with scarcity (the famous ~13-IQ-point effect in the
field study).
**Prediction for your arm B (REASONED — this is a human-cognition result and I will not pretend
it transfers automatically to a transformer; but it is the *right shape* and it is cheap to
check):** the salient live budget line **may make the agent better at the budget and worse at
the brief.** This is not idle: it is *exactly the shape of deepseek's measured failure* —
attention captured by a salient local problem (the harness bug), brief abandoned. **If arm B
makes agents more token-efficient and *less* likely to complete the task, you will have
reproduced tunneling, and my Q3 headline ratio is the only metric that would show you.**

### 2e. Crowding out — pricing a duty can destroy the norm doing the work

**Citation:** Gneezy & Rustichini (2000), *"A Fine Is a Price,"* Journal of Legal Studies
29(1):1–17.
**URL:** https://www.journals.uchicago.edu/doi/10.1086/468061
**Finding (DOCUMENTED):** introducing a **fine** for late pickup at Israeli daycares
**increased** late pickups significantly, and — the crucial part — **after the fine was removed,
no reduction occurred**: the original behavior did not come back. The fine converted a *moral
obligation* into a *purchased service*, permanently.
*(I originally wrote "roughly doubled" here. I could not confirm that multiple from the sources
I actually fetched, so I have removed it. The direction and the irreversibility are confirmed;
the magnitude is not mine to assert.)*
**Prediction for you (REASONED):** this is the sharpest available warning against pricing swarm
duties. The swarm's duties are *normative* today ("it's a duty and a judged artifact" —
PHILOSOPHY §2). **If you tell an agent that a report costs $0.02, you have told it that a report
is a thing you may decline to buy.** Do not price the duties. Price the *decisions* (Q1/Q4).
The distinction is the whole ballgame.

### 2f. On theatre — why you cannot trust the narration

**Citation:** Turpin, Michael, Perez & Bowman (2023), *"Language Models Don't Always Say What
They Think: Unfaithful Explanations in Chain-of-Thought Prompting,"* NeurIPS 2023.
**URL:** https://arxiv.org/abs/2305.04388
**Finding (DOCUMENTED):** CoT explanations **systematically misrepresent the true cause** of a
model's behavior — models influenced by a biasing feature in the prompt produce fluent reasoning
that never mentions it, and accuracy on biased inputs drops by **up to 36%** while the stated
rationale looks clean. **This is the theoretical license for my Q3 detector: the model's
self-narration is not evidence about the model's policy — not because it lies, but because the
narration is generated by a process that need not track the cause.** Anything that scores "did
the agent engage with its budget?" from the transcript is measuring the narration.
*(Anthropic's 2025 CoT-faithfulness work reports low faithfulness rates in the same direction; I
did not re-fetch it and so I do not quote a number — my scouts' figure is unverified and I will
not launder it into this document.)*

### 2g. What the field actually converged on

**FrugalGPT** (Chen, Zaharia & Zou, 2023, arXiv 2305.05176 — https://arxiv.org/abs/2305.05176)
and the entire cost-aware-LLM line put the cost logic in **the router/cascade — the scaffold —
and never ask the model to manage its own budget.** **DOCUMENTED** as a description of the
method; **REASONED** as a claim about the whole field, but I could not find a counterexample
where a model was trusted with its own wallet and it worked.

**This is your own doctrine, arriving from outside.** LOOP.md §2: *absorption beats gating —
the loop performs the duty, the model is never asked.* The literature agrees, and it agrees for
the same reason. **Arm B asks the model. Arm C asks the harness. Your own philosophy already
predicts which one works, and the field has already run it.**

---

## Q4 — THE ONE MECHANISM I WOULD BUILD

**Not a budget. A price tag on the one decision that actually moves the money — shown to the one
agent that makes it, at the moment it makes it.**

> ### **THE SPAWN QUOTE**
>
> When a parent calls `swarm spawn <name> --model opus`, the loop — before the child launches —
> shows the parent, in the tool's own result:
>
> ```
> spawn: research-child @ opus
>   this tier, for a task of this shape:  ~$18–60   (est. from 9 prior spawns of this shape)
>   the same task at sonnet:              ~$3–6
>   your subtree so far:                  $12.40 across 3 children
>   your parent's budget for you:         $25.00
> ```
>
> …and requires the parent to proceed or amend. **That is the whole mechanism.**

### Why this one

**It prices a decision, not a duty.** Gneezy-Rustichini (2e) says pricing a *duty* destroys the
norm that was performing it for free. But `--model` is not a duty — **it is already an explicit
choice the swarm demands a written justification for.** Every spawn in this system carries a
mandatory `--reason` whose stated purpose is *"can you cheaply tell that this child was wrong?
Cheap to check → a small model's error is free; expensive to check → pay for the strong one."*
**The swarm already asks every parent to reason about the price of being wrong, and then never
tells it the price.** This mechanism does not add an incentive to the system — **it completes one
that is already there and currently runs open-loop.**

### The evidence that this is the gap — VERIFIED, from your own disk, just now

I checked, rather than assumed. **`.swarm/agents/<name>.json` has exactly these fields:**

```
['cwd', 'model', 'name', 'parent', 'pane', 'reason', 'tab', 'task', 'ts']
```

**There are 224 of these records on disk.** Every one of them stores **`model`** (the tier the
parent chose) and **`reason`** (the parent's written justification for choosing it), *already
joined, already structured, already keyed by agent and parent.* **Not one of them stores what it
cost.** (Distribution of the 224: 41 sonnet, 13 opus, 2+2 haiku, 1 fable, 165 default.)

And in `bin/swarm` itself, the strings `cost`/`token`/`price`/`spend` appear on **10 lines — and
every single one is prose inside the briefing text**, exhorting the parent to think about cost
(*"a small model's error costs you nothing"*, *"tokens: opus · sonnet · fable · haiku"*).
**There is not one line of code in the entire tool that measures it.**

> **The swarm has been keeping the left column of a ledger for 224 rows and has never once
> written the right column.** It demands a cost-benefit justification at every spawn, records
> that justification verbatim and permanently — and has never measured the cost side of the
> trade it is asking every parent to make.

That is the un-incentivized surface, it is 224 rows deep, and **the join key already exists.**
The spawn quote is not a new mechanism bolted onto the system; it is **the missing column of a
table the system has already been maintaining.** This is also why it needs **no fork and no
opencode**: `spawn` is swarm's own Python (`bin/swarm`), the record is swarm's own JSON, and the
price table is a `SELECT` over transcripts you already have.

**It is prospective, not retrospective.** Q1's first miss: "$4.10 spent" is sunk and
undecidable. "$18–60 vs $3–6, right now, for the thing you are about to do" is a *decision under
a price*, which is the only form in which a cost signal can influence anything.

**It points at the agent with the leverage.** Q1's real blind spot. The parent moves the money;
the child merely burns it. A meter on the child is a meter on the powerless.

**It survives PHILOSOPHY §1's cache test — and this is the bar the seed list struggles with.**
A token-thrift mechanism that "does nothing for the goal is a cache." Does the spawn quote do
something for the goal? **Yes, and not incidentally: it directly serves MODEL-FIT's rule** ("put
the strong model where being wrong is expensive and invisible, and *nowhere else*"). Getting the
tier *wrong in the cheap direction* costs the goal (a weak child's error goes uncaught); getting
it wrong in the *expensive* direction costs money and capacity — and LOOP.md §6 records that the
binding constraint is **capacity**, not dollars (*"weekly limit at 82% — the swarm's token
appetite is real"*). **A parent that over-spawns opus does not just waste money; it burns the
weekly ceiling that the whole tree's future work depends on.** That is a goal argument, not a
thrift argument. The quote is not a cache.

**Now the honest test — §2. Is it an incentive, or a guardrail wearing an incentive's clothes?**

The test: *"before adding a guardrail, ask who is incentivized to notice if it is missing. If
someone already is, the guardrail is ceremony. If nobody is, fix the incentive, not the guard."*

**Nobody currently notices.** A parent that spawns opus for a grep pays nothing, is told nothing,
and no one downstream can see the choice was wrong — the child does fine work, expensively, and
the artifact looks the same. **That is a genuinely un-incentivized surface**, which by §2's own
logic is where you *fix the incentive*.

But I must be scrupulous here, because it would be easy to cheat: **as specified above, with a
mandatory "proceed or amend" confirmation, it is a GATE — and a gate is exactly what §2 refuses,
and what LOOP.md §4b's M4 was correctly graded as §2-refused.** A parent forced to click through
a price is a parent who will click through a price, and now you have ceremony *plus* latency.

**So the mechanism must be built in its non-gating form, and this is the version I am
recommending:**

> **The quote is INFORMATION, not a gate. It appears in the spawn tool's result — always,
> unconditionally, unblockable — and the spawn proceeds regardless.** And then the *actual*
> incentive: **the quote is written into the parent's journal, and into `swarm ps --reason`,
> next to the `--reason` string the parent gave.**

Now read what that does. The parent's stated reason and the price it paid **sit side by side in
the artifact that its own parent judges it by.** *"--reason: 'cheap to check, I'll re-read the
diff anyway' — cost: $47 at opus"* is a **self-indicting record**. Nobody is gated. Nobody is
compelled. But now **somebody is incentivized to notice** — the grandparent, at reconciliation,
reading the tree. And per PHILOSOPHY §4, the swarm's whole enforcement model is *judgment of
artifacts*, and per §2 the operator's own answer to enforcement was *"the parent naturally
pinging the subagent… we need to setup the right incentives with the goal tracking."*

**That is the mechanism: make the tier decision legible and priced in the record that is already
being judged.** It sets an incentive (a parent who over-spends opus will be *seen* to have
over-spent opus, by the agent who judges it) rather than installing a guard (nothing is refused,
nothing is blocked, nothing can be satisfied with noise). It requires **no fork** — the spawn
verb is swarm's own code (`bin/swarm`), and the price table is a `SELECT` over transcripts you
already have.

**And it is cheap to falsify.** Before building even this: **measure whether subtree cost is
actually dominated by parents' tier/fan-out choices rather than leaf verbosity.** If it isn't,
the whole argument collapses and the reflexive meter was right. That query costs you an hour and
it is the highest-value hour in this project.

---

## WHAT I WOULD DO WITH YOUR 3-ARM LADDER

I am not telling you to cancel it. I am telling you what it will cost you if you run it as
specified, and what to change for almost nothing:

1. **Do not run arm C without a landing turn.** TRIAGE's η_E < 0 is a warning, and the mechanism
   of harm (truncation mid-artifact) applies directly. Give the agent one terminal turn to write
   its handoff.
2. **Do not score spend.** Score attainment-per-dollar, blind-graded. Otherwise your best-looking
   arm is your worst agent (the Truncation column).
3. **Add arm B′ (sham budget).** It is nearly free and without it "cost visibility works" is
   indistinguishable from "any live number works."
4. **Add the discrete-fork task** so at least one check is a bit, not a scalar buried in variance.
5. **Register the SAY/DO cross-tab in advance,** with the prediction that they will be
   uncorrelated. If you're right, you saved the fork. If you're wrong, you've earned it.
6. **Expect arm B to be null.** TRIAGE already ran it. If yours isn't null, the *interesting*
   finding is the difference between your setup and theirs — and you should be able to say what
   it is *before* you run.

---

## MY CONFIDENCE, REGISTERED SO IT CAN BE SCORED

- Arm B (advice) produces **no significant behavior change** on a blind quality-per-dollar
  metric: **~75%**. (TRIAGE's null is direct; the salience literature gives the main path to a
  non-null, and it points at *harm*.)
- Arm B produces **detectable theatre** (SAY↑, DO≈0): **~60%**.
- Arm C (law), as specified with no landing turn, produces artifacts that a blind grader scores
  **worse** than arm A: **~45%**. With a landing turn: **~15%**.
- **Subtree cost is dominated by parents' tier/fan-out decisions rather than leaf verbosity:
  ~70%** — and this is the one I most want checked, because the spawn-quote mechanism lives or
  dies on it, and it is checkable *today* with no run.
- If the spawn quote is built in its **journaled, non-gating** form, a parent's model-tier
  choices shift measurably cheaper within one reconciliation cycle: **~50%** — genuinely
  uncertain, and I would rather be shown wrong by a cheap run than be right in a document.

---

## APPENDIX — evidence discipline, stated against myself

**Fetched and read by me** (not by a scout; where a scout surfaced a paper I re-fetched before
citing): arXiv 2605.13414 (abstract + HTML full text — the load-bearing one), arXiv 2512.24661,
the Kornai/Maskin/Roland JEL survey (Berkeley mirror), arXiv 2501.19393, arXiv 2412.18547, arXiv
1803.04585, arXiv 2305.04388, arXiv 2305.05176, and the Gneezy-Rustichini record.

**VERIFIED by me on this machine, just now:** the field list and count of `.swarm/agents/*.json`
(224 records; `model` + `reason` present, no cost field); the 10 cost-word occurrences in
`bin/swarm`, all prose, none code; the model-tier distribution.

**Claims I removed rather than launder — listed so the gaps are visible, per PHILOSOPHY §10
("if you cannot prove the number is yours, do not print a number"):**
- I first wrote that the daycare fine "roughly doubled" lateness. **I could not confirm that
  multiple from any source I actually fetched.** Removed; direction and irreversibility kept.
- I first intended to quote **Manheim & Garrabrant's verbatim definition of Extremal Goodhart.**
  The PDF would not yield clean text. The four variant *names* are confirmed; the definitions are
  not quoted, and the application to `tokens_spent` is tagged as **mine**, not theirs.
- Two fetches of **Barkan** disagreed on whether reasoning models calibrate *better* or *worse*.
  **I dropped the sub-claim entirely** rather than pick the reading that suited my argument. The
  overconfidence-worsens-across-agentic-steps finding, which is what I actually rely on, was
  consistent across both.
- **Anthropic's 2025 CoT-faithfulness rate** (~25%) was reported to me but I did not re-fetch it.
  **I therefore quote no number from it** and lean on Turpin, which I did fetch.

This appendix exists because LOOP.md §10 confessed, twice, that its author's tags into
unaudited corners were overstated and were caught only by a second reader. **I am a second
reader for this org and a first-drafter for myself, and I would rather hand you the list of my
own soft spots than have you find them.**
