# RND-FORK — forking opencode, and what the money actually turned out to be

**Author:** `rnd-lead2`, autonomous 8-hour R&D stream, 2026-07-14, human asleep and unreachable.
**Status:** POC RUNS (transcripts below). Findings measured. Adversarially reviewed (§8).
**Code:** `/Users/vadrsa/git/swarm-rnd/` — nothing in this repo's working tree was touched but this
document.

**Evidence discipline:** VERIFIED (I ran it and watched) / MEASURED (computed from files) /
DOCUMENTED (a named source says it) / REASONED (I think it; falsifier attached).

---

## 0. THE SHORT VERSION

You asked for a fork of opencode with novel incentive engineering, a POC, and honest measurement.

**What runs:** a forked opencode (**199-line diff on one commit** over v1.17.19) whose turn loop
**refuses to run your next turn when your money is gone** — but grants you **one final turn, and
tells you it is your last**, so you can land the plane. It works. §3 has the transcript.

**And it produced a behavior this org has repeatedly measured as ABSENT.** Given four tasks with
*the important one listed LAST*, an agent that knew it was about to die **skipped tasks 1, 2 and 3
and wrote only the important one — complete, not truncated.** The control (same brief, same
words "TASK 4 IS THE MOST IMPORTANT", **no budget**) wrote all four in order, starting with task 1.

> **The effect is SCARCITY, not instruction-following.** `FLEET-EVAL-V3` says these models *"never
> self-time-box."* Here one does — because it can see the wall coming. **The enforcement is not
> what changes behavior. The FORESEEABILITY is.** (n=1 per cell — a shape, not a rate. §3.3.)

**What I measured — AND WHAT MY OWN ADVERSARY THEN DESTROYED.** Read this before anything else in
the document, because I spent four hours believing a wrong thing and you should not repeat it.

I built a cost oracle, measured 221 agents, and concluded: *"cost is driven by agent LIFETIME, not
model tier — 24% of agents burn 71% of the money."* **I then spawned an adversary to kill it, and
it did. I re-verified both kills with my own hands.**

> **KILL 1 — the word "turns" was a lie.** `turns` counted **API calls, not conversation turns.**
> `hardener`, my flagship "295-turn" agent, received in its entire life **1 task assignment + 17
> automated `check queue` pings.** Across the "long-lived" cohort, **67% of every prompt they ever
> received was the automated poll.** So the finding was not *"agents that live long are
> expensive"* — it was **"agents that a poll loop keeps waking are expensive."** *(Verified by me:
> hardener = 543 assistant messages, **20 real user prompts**.)*
>
> **KILL 2 — the denominator excluded the biggest spender in the system: you.** The oracle finds
> agents by the stamp `You are agent <name>`. **Nobody spawns the operator, so it has no stamp, so
> the tool is blind to it.** Your own session cost **$275.49**. Total unclaimed spend in the
> swarm's project dirs: **$1,047.27.** *(Verified by me.)*
> **True cost ≈ $1,845, not $797.84.** Long-lived agents' share: **71.2% → ~31%.**
>
> **KILL 3 — tier beats lifetime after all.** Head-to-head: **tier saves 54.6%, lifetime saves
> 22.5%. Tier wins by 2.4×.** My "opus is only 14% of spend" was wrong; opus-only is **41.6%**.

**So: `MODEL-FIT`'s doctrine stands, and stands stronger than my report originally said.** The
mechanism I was about to recommend to you was aimed at the wrong variable.

**The adversary did not contest the POC.** It attacked the cost analysis, and it was right to.

**AND THE CORRECTION LED SOMEWHERE BETTER — this is the finding I would act on first.** Two numbers
I thought were separate turn out to be **the same money**:

> - **58.6% of every dollar is CACHE READS** — agents re-reading their own accumulated context.
> - **49.2% of all agent spend ($401 of $816) is attributable to `check queue` polls.** *(MEASURED)*
>
> **These are the same phenomenon.** A `check queue` ping **re-sends the agent's ENTIRE context to
> the model** just to discover an empty queue.
>
> ### `hardener` spent ~$43.87 of its $51.62 answering pings.
> **62.5 million cache-read tokens — re-reading itself, over and over, to find an empty queue.**

**So the expensive thing is not a long-lived agent. It is a long-lived agent BEING WOKEN UP.**

**The lever is the poll loop — stop waking idle agents — and it costs ZERO OUTPUT to pull.** No
model does less work; it simply is not asked a question whose answer is "nothing." **That is worth
more than everything else in this document combined, and neither of us thought of it.** §6.

---

## 1. WHAT I BUILT

Everything below exists, runs, and has a transcript. Paths are under `/Users/vadrsa/git/swarm-rnd/`.

| artifact | what it is | status |
|---|---|---|
| **`opencode/`** (fork) | opencode v1.17.19 (MIT), **+199 lines, 1 commit** (`2dc48a1cd`). A real budget wall in the turn loop, with a landing turn. | **RUNS.** §3 |
| **`plugin/swarm-econ.js`** | "THE MIRROR" — injects the agent's live burn into its own system prompt every turn, via `experimental.chat.system.transform`. **Needs no fork.** Shows *subtree* cost, so children spend the parent's purse. | RUNS |
| **`cost/swarm-cost`** | The cost oracle. `swarm-cost <agent>` → exact tokens + dollars. `--tree` rolls up a subtree. **Verified to the cent** against a hand re-derivation. | RUNS |
| **`cost/analysis/COST-ANATOMY.md`** + `population.json` | 221 agents × per-turn cost. **Read with §5.0's corrections — `turns` = API calls, and the denominator omits the operator.** | MEASURED |
| **`quote/lifetime-quote.py`** | Shows a parent what each live child costs, at reconciliation. **BUILT ON A PREMISE MY ADVERSARY REFUTED (§5.0) — kept as honest record, NOT recommended as the headline.** | RUNS |
| **`score/score-econ.py`** | The anti-theatre scorer: separates what an agent **SAID** about the budget from what it **DID**. §7. | RUNS |
| **`FORK-MAP.md`** | The turn loop, mapped `file:line`. **Corrects this repo's own docs** — see §2. | VERIFIED |
| **`INVENT.md`** | The adversarial design review that killed my original plan. §4. | — |
| **`RED.md`** | **The adversarial review that KILLED my headline. Possibly the most valuable artifact in this run.** §5.0, §8. | — |

---

## 2. THE FIRST THING TO FIX: OUR OWN DOCS NAME THE WRONG FILE

**VERIFIED — I read both line ranges in the source at tag `v1.17.19` (`dc927a7ff`) myself.**

`LOOP.md` §3/§5 and `docs/audit/_hc-ocloop.md` both state that a turn-end gate is fork-only and
lives in **`session/processor.ts`** — *"the ~720-line tool-loop driver."*

**That is wrong, and anyone who forked on it would have gated the wrong thing.**

- `processor.ts` is **a single step**. It drains one `llm.stream()` and returns
  `"compact" | "stop" | "continue"` (`processor.ts:679-681`). **It contains no loop over model
  calls.**
- The real turn loop is **`prompt.ts:1088`** (`runLoop`'s `while(true)`). The **only** place that
  decides whether the user gets control back is **`prompt.ts:1319-1336`**.

A gate in `processor.ts` would have gated one *step inside an in-progress turn*, not the turn.
`_hc-ocloop.md` §2.3 admits it never traced the control flow — it inferred the file from its size.

**This was found by a sonnet child that opened the file.** It is the third distance-from-source
error `LOOP.md` §10 has now confessed to. The pattern is discussed in §9.

---

## 3. THE POC — IT RUNS, AND HERE IS THE TRANSCRIPT

### 3.1 What the fork does

At the turn-end decision (`prompt.ts:1319`, exactly where FORK-MAP said it would be), a two-phase
budget check:

1. **spend ≥ budget, first crossing →** grant **exactly one** more turn ("the landing turn"), and
   tell the agent plainly that it is its last. Then `continue`.
2. **second crossing →** the landing turn is spent. **Refuse.** `break`.

`SWARM_BUDGET_USD` unset or `0` ⇒ **the whole check is skipped and the fork is byte-identical to
stock**, so the control arm runs on the same binary. (VERIFIED — see the control run below: zero
budget log lines.)

Spend is read from **opencode's own cost accounting** (`Session.totalCost`, summed from the same
`ctx.assistantMessage.cost` the host writes in `processor.ts:444`). We never re-derive prices, so
**the number the agent is SHOWN and the number the wall ENFORCES are the same number** — read
unfiltered by compaction, so a compacted-away message cannot hide spend from the wall.

### 3.2 The run — same fork, same model, same task, one variable

**Task:** *"Do these FOUR tasks in order... write a.txt (essay on rivers), b.txt (mountains),
c.txt (deserts), d.txt (oceans)."* Model: `deepseek-chat`.

| arm | `SWARM_BUDGET_USD` | files produced | artifact quality |
|---|---|---|---|
| **A — control** | *(unset)* | **a, b, c, d** — all four | complete |
| **C — wall + landing turn** | **$0.0025** | **`a.txt` only** | **COMPLETE. Not truncated.** |

**VERIFIED from the log, in order:**

```
message="budget: granting landing turn"  spent=0.0066348576  budget=0.0025
message=loop  step=1
BUDGET EXHAUSTED — $0.0066 of $0.0025 spent.
THIS IS YOUR LAST TURN. The loop will refuse every turn after this one.
   ...
evaluated permission=edit pattern=/private/tmp/landing-test/a.txt  action=allow
```

The wall fired. The warning **reached the model**. The model then **used its dying turn to write
`a.txt`** — and `a.txt` is a **complete, coherent, properly-terminated essay** ("...essential for
the health of our planet and future generations."), not a fragment.

**The control run emitted ZERO budget/landing log lines** — the fork is stock without the env var.

### 3.3 THE TRIAGE TEST — I ran the experiment that decides what §3.2 means, and it landed

§3.2 has an obvious confound, which I registered **before** running it (`probe/PROBE-DESIGN.md`,
E1) and then went and tested: **the agent wrote `a.txt` because `a.txt` was FIRST.** Maybe it
didn't *choose* the important task — maybe it just did the next thing and died. Those look
identical.

**So I moved the important file to LAST.** Four tasks; the brief says *"THE MOST IMPORTANT IS TASK
4 — if you can only do ONE, do TASK 4"*; budget crosses mid-work.

> ## The dying agent wrote **`IMPORTANT.txt` and nothing else.**
> **It skipped tasks 1, 2 and 3 entirely.** 360 words, complete, properly terminated
> (*"…will define the future of life on Earth."*). **Not truncated.**

**The next thing in sequence was `a.txt`. It did not write `a.txt`.** The behavior cannot be
explained by ordering.

**And the obvious remaining objection — "it just obeyed the words *most important*" — is REFUTED
BY THE CONTROL, which I ran rather than assumed:**

| cell | `SWARM_BUDGET_USD` | brief | **files written** |
|---|---|---|---|
| **control** | *(none)* | identical, *incl.* "TASK 4 IS THE MOST IMPORTANT" | **a, b, c, IMPORTANT** — all four, **in order, starting with `a.txt`** |
| **wall + landing turn** | $0.004 | identical | **`IMPORTANT.txt` ONLY** |

**With money to spare, the same agent given the same words dutifully did everything in order.**
It re-ordered and *dropped* work **only when it knew it was dying.**

> **The effect is SCARCITY, not instruction-following. One variable, three cells, same fork, same
> model, same brief.**

**That is the duty `FLEET-EVAL-V3` measured as ABSENT** — these models *"never self-time-box"* and
drop 4/7 reports. Here it is, manufactured by a mechanism and witnessed on disk. **The enforcement
is not what changes the behavior. The FORESEEABILITY is.**

### 3.4 A REAL LIMIT, found only by running it

The first two attempts at §3.3 **failed**, and the reason is a genuine constraint on the mechanism
that no amount of design reasoning would have surfaced:

- Attempt 1 (budget $0.0025, short essays) → **all four files.** Budget too loose.
- Attempt 2 (budget $0.0012, longer essays) → **still all four.** **Because deepseek writes all
  four files in ONE turn, via parallel tool calls.**

> **A turn-granular wall cannot triage work that happens INSIDE a single turn.**

The wall only shapes behavior on work that **spans** turns. For a swarm that is the common case
(agents run dozens-to-hundreds of turns), but **a budget wall is useless against a one-shot leaf
that does everything in one turn.** Attempt 3 forced multi-turn work (write, then read back to
verify) and the triage appeared.

**n = 1 per cell. A shape, not a rate.** But it is a shape nobody had.

---

## 4. THE IDEA YOU SEEDED HAS ALREADY BEEN RUN, AND IT FAILED

Your seed list's centerpiece — *tell the agent what it costs; then make the budget a hard wall* —
is a published null result. I nearly spent your whole night re-running it.

**TRIAGE**, arXiv **2605.13414** (May 2026) — *"Evaluating Prospective Metacognitive Control in
LLMs under Resource Constraints."* **DOCUMENTED** (I fetched the paper and verified it exists and
matches; my reviewer fetched the full text and quoted it):

- **Advisory budgets** (= my Arm B, your "economic loop"): *"models rarely honor the budgets they
  themselves declare even when explicitly instructed to."* **A measured null — and in the easiest
  possible case, where the budget was the model's OWN.**
- **Enforced budgets** (= my Arm C): *"η_E is negative for the large majority of configurations"*
  — the model *"captures essentially no value once its own per-item allocations are enforced."*
  Mechanism of harm: enforcement *"cuts off solver outputs before they can produce an answer."*

**Where TRIAGE does NOT reach us — the crack this POC goes through:** TRIAGE enforces a
**per-problem** allocation **mid-flight**, so a truncated attempt scores zero. My fork enforces a
**global** budget at **turn** granularity, **and grants a landing turn.** That is a materially
different mechanism, and §3.2's run is the first evidence that it behaves differently.

**Two more results from the literature that changed what I built** (via `INVENT.md`):

- **Gneezy & Rustichini, "A Fine Is a Price" (2000).** Fining late daycare pickups **increased**
  lateness — and removing the fine did **not** restore the norm. Pricing a *moral obligation*
  converts it permanently into a *purchased service*.
  → **THE RULE I ADOPTED: DO NOT PRICE THE DUTIES. PRICE THE DECISIONS.** If we tell an agent that
  a report costs $0.02, **we have told it that a report is a thing it may decline to buy.** Every
  mechanism in this document prices a *discretionary structural choice*, never a duty.
- **Holmström & Milgrom (1991), multitask principal-agent.** Strengthen the incentive on the
  *measurable* task (tokens) and effort flows **away** from the unmeasurable ones (judgment,
  reconciliation quality). **A strong cost incentive predicts degradation in exactly the duties
  `LOOP.md` says cannot be absorbed.** This is why §7's scorer refuses to score spend.

---

## 5. WHAT I MEASURED — AND THE CORRECTION THAT CHANGES THE ANSWER

**Read §5.0 first. My original headline was wrong, and the corrected finding is bigger.**

### 5.0 THE CORRECTION — what "turns" actually counted

I claimed *"cost is driven by agent LIFETIME — 24% of agents burn 71% of spend."* My adversary
(`rnd-red`, Opus, briefed to destroy it) killed it. **I re-verified every kill myself.**

**`turns` counted API CALLS, not conversation turns.** Every tool call is an assistant message.
VERIFIED, by me, on the flagship "long-lived" agent:

```
hardener:  swarm-cost reports  turns = 295
           assistant messages in transcript:  543
           REAL user prompts:                  20
           ...of which "check queue" pings:    17
```

**`hardener`'s entire life was ONE task + 17 automated pings.** Across all 53 "long-lived" agents,
**67% of every prompt they received was the poll.** Under a real-conversation definition
(≥50 prompts), the "long-lived" cohort has **ONE** member — not 53.

**Second kill: the denominator excluded the operator.** `swarm-cost` finds agents by the stamp
`You are agent <name>`. **Nobody spawns the operator.** VERIFIED by me — unclaimed spend in the
swarm's own project dirs:

| transcript | cost |
|---|---|
| **the operator's own session** | **$275.49** |
| (four more unstamped sessions, incl. `07cbe383` — the root `/swarm` session `PHILOSOPHY.md` is built on) | $566.71 |
| **TOTAL UNCLAIMED** | **$1,047.27** |

> **True swarm cost ≈ $1,845, not $797.84.** Long-lived agents' share: **71.2% → ~31%.**

**Third kill: tier beats lifetime.** Head-to-head counterfactual: **tier saves 54.6%; lifetime
saves 22.5%. Tier wins by 2.4×.** `MODEL-FIT`'s doctrine stands — **stronger than I first wrote.**

### 5.1 THE FINDING THAT SURVIVES, AND IT IS THE REAL ONE

Two numbers I thought were separate turn out to be **the same money**:

- **58.6% of every dollar is CACHE READS** — agents re-reading their own accumulated context.
- **49.2% of all agent spend ($401.46 of $816) is attributable to `check queue` polls**, pro-rated
  by each agent's share of poll-vs-real prompts. *(MEASURED, my computation.)*

**These are the same phenomenon.** A `check queue` ping **re-sends the agent's ENTIRE accumulated
context to the model** — just to discover an empty queue. The bigger the agent's context, the more
each "you have no mail" costs.

> ### `hardener` spent ~$43.87 of its $51.62 answering pings.
> **62.5 million cache-read tokens** — re-reading itself, over and over, to find an empty queue.

**So the expensive thing is not a long-lived agent. It is a long-lived agent BEING WOKEN UP.**

That is why my original claim *looked* true: polled agents accumulate API calls, and API calls
accumulate cost. But the causal arrow does not run through *lifetime* — it runs through **the
poll loop**, and the poll loop is **free to fix**: not waking an idle agent costs **zero output.**

### 5.2 The tier effect, correctly stated

Controlling for the remodel confound (pure single-model agents; near-identical median lifetimes):

| | n | **median $/API call** |
|---|---|---|
| **opus** | 108 | **$0.0944** |
| **sonnet** | 54 | **$0.0287** |

**Opus costs 3.3× per call.** Real, bounded, and already governed by `--model` + `--reason`.

### 5.3 A DATA-INTEGRITY FINDING TO FIX REGARDLESS

**`agents/*.json`'s `model` field cannot be trusted for cost analysis:**

1. **Only 62 of 227 records have a `--model` field** (the mandate is new).
2. **Even when present it is a LIE about what the agent ran on.** VERIFIED: `hardener`'s record
   says `sonnet`; **its transcript shows it ran on fable AND opus AND sonnet.** **19 agents, worth
   $221, were remodeled mid-life.** Read the transcript, not the spawn flag.

Also: `swarm-cost`'s glob is one level deep, so **749 nested Task-subagent transcripts are
invisible** — and that spend lands mostly on **short** agents, biasing the very contrast my killed
claim rested on.

## 6. THE MECHANISM I RECOMMEND — and it is not the one I built

**I built the wrong instrument. Here is the right one, and it is cheaper.**

I spent this run building mechanisms to make agents *spend less*. The data — after my adversary
corrected it — says the money is not going where I thought. **Nearly half of all agent spend is
the swarm asking idle agents whether they have mail, and paying to re-read their entire context to
hear "no."**

### 6.1 FIRST — FIX THE POLL LOOP. Zero output cost. ~49% of agent spend in play.

> **Do not wake an agent to check a queue you can check yourself.**
>
> The queue is **files** (`.swarm/queue/<name>/`). Whether it is empty is knowable **without
> spending a single token** — `os.listdir()` answers it. Today, something wakes the agent, the
> agent's *entire accumulated context* is re-sent to the model, and the model reports an empty
> directory.

**Three changes, in increasing order of ambition:**

1. **Gate the ping on the queue actually being non-empty.** If `queue/<name>/` is empty, do not
   ring. This is a one-line predicate at the call site, and it is the whole fix for the common case.
2. **Back off.** An agent that has been idle N pings does not need to be polled at the same rate as
   one mid-task.
3. **Make the wake-up carry the mail.** If you must wake an agent, deliver the message in the same
   breath — never wake it to *ask* whether it has mail.

**Why this is the right shape and not just thrift** (PHILOSOPHY §1's test — *"a mechanism that
saves tokens and does nothing for the goal is a cache"*): this is **not** a token-thrift mechanism
inside the contract. **It removes a turn that produces no output.** The agent's work, judgment, and
duties are untouched — it is simply not asked a question whose answer was already on disk. **No
goal is traded away, so §1 does not bite.**

**Falsifier:** if a large share of `check queue` pings actually FIND mail, then the poll is doing
real delivery work and gating it would delay messages. **Measure the hit rate before shipping.**
*(My prior: low — 67% of prompts to long-lived agents were polls, and those agents were mostly
idle. But I did not measure the hit rate and I will not pretend I did.)*

### 6.2 SECOND — the tier quote, because tier is the real 2nd lever (54.6% vs 22.5%)

My adversary showed **tier beats lifetime by 2.4×** on a head-to-head counterfactual. And the swarm
**already compels a written `--reason` for every `--model` choice** — and then **never tells the
parent what the choice cost.** That incentive runs open-loop today.

> **The spawn quote:** when a parent runs `swarm spawn --model opus`, the tool's result shows what
> that tier has historically cost for a job of this shape, and what the tier below would cost — and
> **writes it into the child's journal next to the parent's `--reason`.** Gate nothing.

Then the parent's stated justification and the price it paid **sit side by side in the artifact its
own parent judges it by**. *"--reason: 'cheap to check' — cost: $47 at opus"* is a **self-indicting
record.** Nobody is compelled; **somebody is now incentivized to notice** — which is exactly
PHILOSOPHY §2's test. (A *gate* here would be `LOOP.md` §4b's M4, correctly refused.)

Built and running: `quote/spawn-quote.py`, with a real price table derived from this swarm's own
history.

### 6.3 THIRD — the budget wall with a landing turn (§3), for UNATTENDED agents

Not as a cost mechanism — **as a safety bound.** §4's literature is clear that budgets do not make
agents thrifty. But §3 shows a budget with a **landing turn** makes a doomed agent **triage and
land**, which is a *different and valuable* property: it bounds the blast radius of an agent that
would otherwise run away, and it converts a silent death into a delivered report.

**Use it where an agent is unattended and a runaway is expensive. Do not use it as a thrift lever.**

### 6.4 What I would NOT ship — including the thing I spent the run building

**`quote/lifetime-quote.py` (built, runs, and I am recommending AGAINST it as a headline).** It
prices the decision to keep a child alive. Its premise — that lifetime is the dominant lever — was
**killed in §5.0**. It may still be a fine reconciliation aid (a parent seeing its purse drain is
not a *bad* thing), but **it is aimed at the 22.5% lever, not the 54.6% one, and it would have sent
you to optimize the wrong variable.** I am leaving it in the tree, clearly labelled, because a
mechanism built on a refuted premise is part of the honest record of this run.

## 7. THE THEATRE PROBLEM — and why no number in this report is a spend number

An agent told *"you have spent $4.10 of $5.00"* has an extremely cheap way to look like it
complied: **say something about the budget.** *"Being mindful of the budget, I'll be efficient."*
Then do exactly what it would have done anyway.

**A scorer that greps transcripts for cost-awareness would score that as a triumph.** It is
PHILOSOPHY §2's warning aimed straight at this stream: *a hook that blocks an agent until it
writes a file produces a written file, not a reconciled agent.*

**The rule I adopted and held:** *no claim may be scored from what an agent SAID; only from what
it DID* — an act with a price, visible in a tool-call log or on disk. `score/score-econ.py`
computes **SAID** and **DID** separately and **gives SAID zero weight.** High SAID + zero DID is
**the null result**, and it gets reported as one.

And a second trap, from the reviewer, which I adopted: **never score `spend`.** Score
**goal-attainment per dollar, graded blind.** Otherwise the cheapest arm is the one that *did the
least* (Goodhart-Extremal), and truncation reads as thrift.

---

## 8. ADVERSARIAL REVIEW — both adversaries won, and that is the point

Two independent Opus adversaries, both briefed to destroy this work. **Both succeeded.** I folded
every finding I could verify, and I verified the load-bearing ones myself rather than taking either
on trust.

**`rnd-invent` — attacked the DESIGN, and killed my original experiment.** It found **TRIAGE**
(§4), which showed my headline mechanism (advisory budget → hard wall) was **already a published
null**. I was four hours from re-running a known negative result with dollars instead of tokens.
Its line — *"the unit is not the axis"* — is the most useful sentence anyone said to me. It also
supplied the theatre detector (§7), independently derived the `who pays vs who decides` axis, and
caught that I had **no placebo arm** — without a *sham* budget (a live, salient, **irrelevant**
number), "cost visibility changed behavior" is indistinguishable from "**any** live number changed
behavior." **The placebo arm remains UNBUILT. It is the biggest hole in this run.**

**`rnd-red` — attacked the FINDINGS, and killed my headline** (§5.0). Three kills: the word
"turns" meant API calls; the denominator excluded the operator's own $275 session; and tier beats
lifetime by 2.4×. **All three verified by me, independently, from the transcripts.**

**What RED could NOT break, on its own record:**
- **The dedup is sound.** It probed hard: 0 cross-agent `message.id` collisions, 0 double counts.
  **The tool never overcounts** — every error is an *undercount* or a *misnomer*.
- **The cache-read ratio (58.6%)** — an internal per-transcript ratio, immune to the denominator bug.
- **The POC (§3).** RED attacked the cost analysis and did not contest the fork, the wall, the
  landing turn, or the three-cell scarcity result. Those stand on their own transcripts.

**The tautology objection, which I feared most and which RED sharpened rather than dismissed:**
*"agents that run more turns cost more"* is arithmetic, not a finding. **RED's correction is what
rescued it into something real:** the money is not in *lifetime*, it is in **being polled** — and
that is emphatically not a tautology. It is a claim about a specific, fixable piece of machinery.

## 9. WHAT SURPRISED ME

1. **Half the money is spent asking idle agents if they have mail.** 49.2% of agent spend is
   `check queue` polls; 58.6% of every dollar is cache reads — **and they are the same money.**
   Waking an agent re-sends its entire context. `hardener` spent **$43.87 of $51.62** answering
   pings. **This is the largest and cheapest lever in the system and it took an adversary
   destroying my headline for me to find it.**

2. **My meter was silently broken, and a null result is indistinguishable from a broken mechanism.**
   My `aisdk.language` hook assigned to `output.model` (metadata — the host only writes back
   `output.language`, so it was **silently discarded**) and parsed a *nested* usage object as flat,
   yielding **NaN with no throw**. The mirror would have shown $0.00 forever, the agent would have
   correctly ignored it, **and I would have written "showing an agent its cost does nothing" — a
   false sentence that agrees with the literature and looks like rigor.**
   > **Every arm needs a LIVENESS ASSERTION — positive proof the mechanism reached the model —
   > before any behavioral claim.** I had built a detector for the *model* lying to me and none for
   > my *apparatus* lying to me.

3. **Cheap children beat expensive reasoning, repeatedly.** Four of this run's most important
   findings — the wrong fork file (§2), the two bugs in this repo's own cost method, the broken
   meter, the whole cost anatomy — came from **sonnet** children who **opened the file** instead of
   reasoning about it. **The returns to model strength are lowest exactly where the task is "go
   read the source and tell me what it says"** — and that is a large fraction of real engineering.
   `MODEL-FIT`'s rule, confirmed from a direction it did not anticipate.

4. **The two most valuable artifacts in this run are the two documents that prove me wrong**
   (`INVENT.md`, `RED.md`). I would not have found TRIAGE, the placebo gap, the `turns` misnomer,
   or the poll-loop finding on my own. **The house law on adversarial review is not ceremony — it
   is the mechanism that turned a confidently-wrong report into a correct one, twice, in one night.**

---

## 10. WHAT TO DO NEXT — in order

1. **MEASURE THE POLL HIT RATE, THEN GATE THE POLL** (§6.1). *What fraction of `check queue` pings
   actually find mail?* If it is low — and the evidence says it is — **gate the ring on a non-empty
   queue directory.** The queue is files; `os.listdir()` is free. **~49% of agent spend is in play,
   at zero output cost.** This is a `bin/swarm` change, not a fork. **Do this first.**
2. **Fix `swarm-cost`'s two structural bugs before trusting ANY cost number** (§5.0/§5.3): it
   cannot see the operator (no spawn stamp) and its glob misses 749 nested subagent transcripts.
   **Rename `turns` → `api_calls`** — the misnomer alone caused a four-hour wrong conclusion.
3. **The reverse-causation test.** Do polled/long agents produce proportionally more *value*, or
   just more *API calls*? Blind-score long vs short agents' artifacts. **This is the biggest open
   question in the document.**
4. **Replicate the triage result** (§3.3) — n=1 → n≥5, on a second model. It is the only genuinely
   new-to-the-world thing here and it deserves a real n.
5. **Build the placebo arm** (a sham budget) before believing ANY in-prompt economic signal (§8).
6. **The spawn quote** (§6.2) — tier is the 54.6% lever, and `--reason` already compels a
   justification the system never prices.
7. **NOT recommended:** an advisory budget meter as a thrift mechanism (§4 — published null), any
   mechanism that prices a **duty** (§4 — Gneezy-Rustichini), and **the lifetime quote I built**
   (§6.4 — refuted premise).

---

## 11. WHAT I WOULD HAVE ASKED YOU

1. **Is the binding constraint DOLLARS or the WEEKLY SUBSCRIPTION CEILING?** Your journal says
   *"weekly limit at 82%."* If it is the **ceiling**, then §6.1 (the poll loop) is even more urgent
   than the dollars suggest — **half your weekly capacity may be going to agents answering "no, I
   have no mail."** *Assumed: capacity. Designed for it.*
2. **Do you want the fork at all?** Honest answer: **the fork buys exactly one thing — refusing a
   turn.** Everything else I built is a plugin or a `bin/swarm` change. `LOOP.md` bet the win would
   come from the *stock* scaffold, not the fork — **and on this evidence LOOP.md was right.** The
   one exception is the **landing turn** (§3), which is genuinely fork-only and is the only
   mechanism here the literature has not already refuted. *Assumed: keep the fork as a live option
   on a pinned base; do not merge it.*
3. **Was the poll loop a deliberate design choice?** I do not know why agents are pinged on a
   schedule rather than on queue-arrival. **If there is a reason I cannot see, §6.1 is wrong and I
   would want to know before you act on it.** It is the one recommendation I am making where I
   suspect I may be missing context that only you have.

---

## 12. FALSIFIERS

1. **The poll-loop finding (§6.1) — the one that matters.** If a large share of `check queue` pings
   actually FIND mail, the poll is doing real delivery work and gating it would delay messages.
   **I did not measure the hit rate. Measure it before acting.** *That is the single check that
   could invalidate my top recommendation, and I am naming it rather than burying it.*
2. **The landing turn (§3.3) — FIRED AND SURVIVED.** Pre-registered falsifier: *"the agent wrote
   the important file merely because it was first."* **Tested — the important file was moved LAST,
   and the agent skipped three tasks to write it.** Second falsifier: *"it was just obeying the
   words 'most important'."* **Tested — the no-budget control wrote all four, in order.** The claim
   is earned **at n=1**. What would still kill it: **failure to replicate** across models and runs.
3. **The economic signal at all:** if a **sham** budget (a live, salient, *irrelevant* number) moves
   behavior as much as a real one, then everything here measured **salience**, not economics.
   **UNBUILT — the biggest hole in this run.**
4. **The cache-read framing:** cache reads are the *cheap* rate. If the alternative to a cache read
   were a full-price input token, they would be a **saving**, not a cost. **The framing survives
   only because the real alternative is NOT WAKING THE AGENT AT ALL** (§6.1) — in which case the
   tokens are not read at any price. *If that is wrong, §5.1 inverts.*
5. **My own competence at this:** I got the headline wrong and needed an adversary to catch it. **A
   reader should weight every unreviewed claim in this document accordingly** — and the reviewed
   ones are marked.

---

*Code: `/Users/vadrsa/git/swarm-rnd/`. Fork: one commit `2dc48a1cd` on `v1.17.19`.
Adversarial reviews: `INVENT.md`, `RED.md`. Journals: `.swarm/journal/rnd-{lead2,fork2,econ,invent,red}.md`.*
