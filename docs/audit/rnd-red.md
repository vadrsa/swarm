# RED — adversarial review of the cost stream's headline claim

**Author:** `rnd-red` (adversary). **Method:** every number below re-derived independently from
`cost/analysis/population.json`. I did not read `rnd-lead2`'s journal until after forming my view.
Two children were dispatched to attack in parallel; I re-verified their key numbers myself before
using them.

---

## VERDICT IN ONE LINE

**Three independent kills, any one of which is fatal.** In order of severity:

1. **The two headline numbers do not mean what they say.** *"53 long-lived agents (≥50 turns)"* —
   `turns` counts **API calls, not conversation turns**. Under an interaction-based reading, the
   long-lived cohort has **one** member, not 53. And **67% of the prompts those agents received are
   the automated `check queue` ping.** The 71.2% measures *which agents a scheduler kept pinging*.
2. **The denominator is wrong. The single biggest cost center in the system is invisible to the
   tool.** The operator's own session — **$275.49** — has no `You are agent X` stamp, so
   `swarm-cost` cannot see it. **$1,058.30 of unclaimed spend** sits in the swarm's own project
   directories. **Long-lived share: 71.2% → 30.9%.**
3. **The central counterfactual is false on its own data.** *"The biggest lever is not which model
   you pick"* — measured head-to-head, **tier saves 54.6%, lifetime saves 22.5%.** Tier wins by
   2.4×, and wins even if fable is priced *free*. The report inverted this because it believed
   Opus was ~14% of spend; it is **41.6%**.

**The underlying phenomenon is still real** and survives as a much narrower claim (§7) — but it
supports the *opposite* intervention from the one proposed.

> **Note on this document:** §1–§8 were written before my tool audit returned. Kills (1) and (2)
> above landed afterward and are **more fundamental** than everything below — they attack the
> *inputs*, where §1–§8 attack the *interpretation*. I have left the original analysis intact and
> added **§0** rather than silently rewriting, so you can see what each pass found. Where they
> conflict, §0 wins.

---

## §0 — THE TWO KILLS THAT ARRIVED LAST (and are the worst)

I verified both of these myself, from the transcripts, not from my child's report.

### 0a. `turns` = API calls, not turns. The word is doing all the work.

`swarm-cost` defines `turns` as `len(seen)` — **the count of unique assistant messages.** Every
tool call is an assistant message. So an agent hits "50 turns" in a handful of real exchanges.

**Measured across the population: 8,882 assistant messages vs 641 real user prompts — a 13.9 : 1
ratio.** Per-agent it is far worse:

| agent | tool `turns` | **real user prompts** | ratio | of which `check queue` |
|---|---:|---:|---:|---:|
| `field-tester` | 351 | 82 | 4.3× | 67 |
| `trigger-scout` | 326 | **22** | 14.8× | 16 |
| **`hardener`** | **295** | **20** | **14.8×** | **17** |
| `hc-build1` | 274 | **4** | **68.5×** | 3 |
| `spawn-repair` | 201 | **4** | **50.2×** | 1 |
| `rnd-econ` | 197 | **4** | **49.2×** | 3 |

**The defining test:**

| definition of "long-lived" | n agents | spend | share |
|---|---:|---:|---:|
| **≥50 API calls** (what the tool measures) | **53** | $575.32 | **71.5%** |
| **≥50 real user prompts** (what "50 turns" *reads as*) | **1** | $65.88 | **8.2%** |

> `hardener` — the 295-"turn" flagship long-lived agent — received in its **entire life**:
> **1 task assignment + 17 × `check queue`.** That is the whole conversation.

**Across all 53 long-lived agents, 67% of the prompts they ever received were the automated
`check queue` poll.** So the cohort is not "agents held in long conversations accumulating
context." It is **"agents a cron-like loop kept pinging, which burned API calls answering."**

The 71.2% arithmetic is *correct*. **The words attached to it are not.** And this reframes the
mechanism completely: if the cost is driven by *polling*, the lever is **the poll loop**, not the
agent's lifetime — you fix it by not waking idle agents, which costs you **zero output**.

### 0b. The denominator excludes the biggest spender in the system

`swarm-cost` finds agents by the stamp `^You are agent <name>`. **The operator's own session has no
such stamp** — nobody spawned it. So the tool is structurally blind to it.

| | |
|---|---:|
| The operator's session (`7588966f-…jsonl`, 956 assistant msgs) | **$275.49** |
| Total **unclaimed** spend in the swarm's own two project dirs (91 files) | **$1,058.30** |
| Claimed by a stamped agent (≈ what `population.json` prices) | $784.35 |

Its timestamps (`2026-07-09 18:25` → `2026-07-14 00:19`) are co-extensive with the roster's activity
window. **This is this swarm's own operator, and it is 100% excluded from the cost of the swarm.**

**Impact on the headline, adding back only the unclaimed spend in the swarm's own directories:**

> **Long-lived agents: 71.2% of spend → 30.9%.**

There is a second, independent hole in the same direction: the tool's glob is
`PROJECTS_DIR/*/*.jsonl` — **exactly one level deep.** Claude Code also writes Task-subagent
transcripts to nested `<session>/subagents/**/agent-*.jsonl`. **749 files are invisible to it.**
My child measured **$63.85 of real subagent spend missing** from `population.json`, and it lands
almost entirely on *short* agents (`theater-count` $1.32 → $9.79, a **7.4×** understatement).

**That bias runs against the claim too:** the "expensive long-lived vs. cheap short leaves" contrast
is partly an artifact of **short leaves' delegated spend being invisible.**

> **"$797.84 is what the swarm cost" is false.** It is the cost of the subset of the swarm that used
> one particular stamp phrase, **excluding the operator that drove it** and excluding every
> Task-subagent it delegated to.

### What §0 does NOT overturn

- **Attack 3 (survivorship) still fails** — the dropped agents still cost ≈$0.
- **The dedup is still sound** — my child probed hard: 0 cross-agent `message.id` collisions, 0
  conflicting-usage ids, 0 double counts. **The tool does not overcount.** Its errors are all
  *undercounts and misnomers.*
- **The cache-read ratio (58.6%) is robust** — it is an internal ratio, so the orphan/operator
  problem does not touch it. It is still, however, **framed backwards** (§5).
- **Kill (3) — tier beats lifetime — is unaffected**, because it is computed *within*
  `population.json` and both levers move together under any denominator fix.

---

## THE THREE NUMBERS THAT ARE SIMPLY WRONG

You said a wrong number is the most valuable thing I could hand you. Here are three. **All three
are in the headline you gave me. None of them is in `COST-ANATOMY.md`** — the analysis doc is
substantially more careful than its own summary. The errors were introduced in summarization.

| # | Headline says | `population.json` says | Severity |
|---|---|---|---|
| 1 | "The most expensive agent … `field-tester` … is a **sonnet** agent" | `field-tester` is **`claude-fable-5`** | **Fatal to the punchline** |
| 2 | "Opus agents are only **~14%** of spend" | Opus-only agents are **41.6%** ($334.75). Any-Opus is **68.4%** | **Fatal — this error causes the false conclusion** |
| 3 | Total **$797.84** | **$804.45** | Cosmetic (drift, see §8) |

**Error #2 is load-bearing.** The entire "tier is not the lever" counterfactual rests on Opus being
a small slice. It is not a small slice. Fix the premise and the conclusion inverts. I could not
reconcile "14%" with *anything* in the data: not spend (41.6%), not tokens (32.9%), not population
(48.6%).

Error #1 matters because `field-tester` is the *rhetorical* proof of "tier doesn't matter" — and
it's a **fable** agent priced *at the Opus rate card by assumption*. The exhibit for "cheap model,
huge bill" is actually an agent billed at the most expensive rate in the table.

---

## ATTACK 1 — IS IT A TAUTOLOGY? → **WOUNDED, badly. 92% of the headline number is arithmetic.**

The clean test: if the claim were vacuous, $/turn would be constant and **share of spend would just
equal share of turns.** So compare them.

| Band | n | % of spend | % of **turns** | $/turn | excess over tautology |
|---|---:|---:|---:|---:|---:|
| Long-lived (≥50) | 53 | **71.5%** | **65.8%** | $0.0985 | **1.09×** |
| Middle (16–49) | 79 | 18.9% | 25.0% | $0.0687 | 0.76× |
| Short leaves (1–15) | 90 | 9.5% | 9.2% | $0.0934 | 1.03× |

**Decomposition of the 71.2% headline:**
- **65.8 points = they simply took more turns.** Pure arithmetic. Tautological.
- **5.7 points = each of those turns cost more.** This is the entire actual finding.
- **→ 92% of your headline number is the tautology.**

And it is **not even monotonic**: the middle band is *cheaper per turn* (0.76×) than short leaves.
"Cost rises with lifetime" fails across the population as a simple ordering.

**Your defence was that the magnitude and the counterfactual rescue it.** The counterfactual does
not (Attack 6 kills it). **But the magnitude partly does**, and here is the version that works —
the *within-agent* test, which the pooled table cannot give you:

> For the 27 agents that reached ≥80 turns, comparing **each agent's own** turns 1–40 vs 41–80:
> **26 of 27 got more expensive. Median 1.40×.**

That is the same agent, same task, more dollars per turn as it ages. It is not composition, not
selection, and not arithmetic. **This is your real finding and it should be the headline.** The
"71.2% of spend" framing is the weakest possible way to state it.

---

## ATTACK 2 — REVERSE CAUSATION → **HOLDS AGAINST YOU. This is the kill.**

You predicted this was the most dangerous attack. You were right, but not for the reason either of
us expected.

**I went hunting for a long-lived agent that burned money on nothing. There is none.** I have to
report that plainly:

- **Near-idle turns (<$0.03) are only 3.5% of all spend.** There is no idle fat anywhere.
- **Every long-lived agent's spend *accelerates* into its final third** — `field-tester` 49% of its
  total in its last third, `harness-contractor` 45%, `hc-build1` 44%, `hardener` 42%. **Not one
  winds down.** A turn-cap does not trim an idle tail; it amputates the most expensive *and most
  productive* phase of the agent's life.
- Journals + `git log` cross-check (my child, verified): every commit SHA the long-lived agents
  claimed **actually exists**. `hardener` (295 turns, $51.62, **zero children**) shipped 14
  dispatched tasks with merged commits. `hc-build1` found two real bugs *in its late turns* —
  including a doorbell bug that only surfaced against the real 94-session store. **A 50-turn cap
  deletes that discovery.**

**So "close them sooner" does not save 22.5%. It buys 22.5% of not-doing-the-work.** Your Goodhart
worry is upheld — the mechanism is Goodhart bait — but via *"they were busy,"* not *"they were
idle."*

### The specimen that ends the argument

**Hold lifetime constant and the claim evaporates:**

| agent | turns | $ | $/turn | model | shipped |
|---|---:|---:|---:|---|---|
| **`spawn-repair`** | **201** | **$5.68** | **$0.028** | **sonnet** | merged PR #85 + its own adversarial review, 93 tests green |
| `rnd-econ` | 197 | $8.38 | $0.043 | sonnet | — |
| `fleet-eval` | 190 | $23.37 | $0.123 | opus | — |
| `operator-structure-scout` | 208 | $25.83 | $0.124 | opus/sonnet | — |
| **`harness-contractor`** | **194** | **$40.46** | **$0.209** | **fable** | — |

**Identical lifetime (194–208 turns). 7.1× spread in spend.**

**Lifetime cannot explain a 7× gap that it holds constant. Tier explains all of it.** A 201-turn
agent shipped a merged, self-reviewed PR for **$5.68**. The question the data actually poses is
never *"why is this agent still alive at turn 200?"* — it is ***"why is this 200-turn agent on
fable?"***

---

## ATTACK 3 — SELECTION / SURVIVORSHIP → **REFUTED. Your claim is safe here.**

The 5 dropped agents (`blocked-vis-fix`, `blocked-vis`, `blocked-visibility`, `inv-meta`,
`shim-check`) have **no transcript at all** — meaning they never ran a turn, so they cost ≈$0.
Adding them back adds 5 zero-cost agents to the population: the long-lived *population* share falls
24.0% → 23.5%, and **spend shares do not move at all.**

The bias runs *in your favour*: the missing agents are the cheapest ones, so their absence
**understates** how many cheap agents exist. "Short leaves are 40% of the population and 9.7% of
spend" is, if anything, conservative. **This attack fails. Keep the number.**

---

## ATTACK 4 — IS THE MEASURING TOOL WRONG? → **HOLDS on dollars. One real defect on turns.**

I audited `swarm-cost` and re-ran the population math. The core method is **sound**, and the two
correctness notes in its docstring are real bugs that were correctly found and fixed:

- **Attribution** (`"You are agent <name>"`, no backticks, matched only inside `type:"user"` text
  messages) is the right call. The backtick form would have swept in every child, since each child's
  prompt names its parent that way. Correctly avoided.
- **Dedup by `message.id`** correctly collapses the streaming re-writes. Without it, costs inflate
  1–3×. Correctly handled.

**The one real defect — it contaminates the very variable your claim is about:**

> **`<synthetic>` is not a model.** It is **42 zero-token stubs** whose text is
> `"You've hit your session limit · resets 4:30am"`. They carry $0 — so **dollars are unaffected**
> (the doc says this, correctly). **But `turns` is defined as "count of unique assistant messages,"
> so every one of these session-limit stubs is counted as a TURN.** They land across 9 agents,
> including long-lived `trigger-scout` (326 turns).

Dollar impact: zero. **Turn impact: real**, in a claim whose independent variable *is* turns. Small,
but it should be filtered.

**Also worth flagging (definitional, not a bug):** `turns` counts **assistant API messages**, not
conversational turns. Every tool call is an assistant message. So *"≥50 turns"* means *"≥50 API
calls,"* which is a **much** lower bar than 50 user interactions — an agent hits it in a handful of
real exchanges. The doc should say this, because "50 turns" reads to an operator as far more life
than it actually denotes.

---

## ATTACK 5 — THE CACHE-READ NUMBER → **REFUTED. Your framing is backwards. You were right to fear it.**

You called this your weakest claim. It is worse than weak — **it is inverted.**

| | |
|---|---:|
| Cache reads as share of **tokens** | **96.8%** |
| Cache reads as share of **dollars** | **58.9%** |

**The cache-read rate is exactly 1/10 of the input rate at every single tier** (Opus $0.50 vs
$5.00; Sonnet $0.20 vs $2.00; Haiku $0.10 vs $1.00).

So the sentence *"58.6% of every dollar is cache reads"* decodes to: **"97% of our tokens got a 90%
discount."** That is the cache **working**, not a cost.

**The counterfactual settles it.** The alternative to a cache read is a full-price input token:

> Without caching, this same work costs **$5,068** instead of **$804**.
> **Caching SAVES $4,264. It is a 6.3× discount.**

Presenting the largest cost *saving* in the system as its largest cost *problem* is a framing error,
and an operator who acts on it will optimize in the wrong direction. **Cut this from the headline.**

There *is* a real finding buried underneath, and it is worth stating correctly:

> Cache-read dollars grow because **context grows**. The lever is not "cache less" — it is
> "**carry less context**." Those are different mechanisms with different fixes (compaction,
> scoped re-reads, smaller working sets), and only the second one exists.

---

## ATTACK 6 — DOES THE MECHANISM FOLLOW? → **REFUTED. It aims at the wrong population *and* the wrong variable.**

### 6a. The head-to-head you never ran

Both levers, same data, **work preserved in both** (you get no credit for doing less). For the
lifetime lever I cap each agent and let a **fresh agent finish the work at the cheap early-context
rate** — the honest version, which does not delete output:

| Lever | Saving |
|---|---:|
| **Tier** — move Opus/fable agents to Sonnet (0.4× rate card) | **$439.28 → 54.6%** |
| Lifetime — cap at 40 turns, restart fresh to finish | $180.65 → 22.5% |
| Lifetime — cap at 20 turns (brutal) | $210.70 → 26.2% |

**Tier is ~2.4× the bigger lever.** And per Attack 2, even the 22.5% isn't real — it's output
deletion, whereas **the tier lever destroys zero turns of work. Every turn still runs.**

**This is robust to the one genuine unknown.** Fable has no published price and is *assumed* = Opus
(22% of spend rides on that assumption — the report should flag this as load-bearing and does not).
I stress-tested every value:

| If fable is really… | tier saves | lifetime saves | winner |
|---|---:|---:|---|
| Opus-priced (the assumption) | 54.6% | 22.5% | **TIER** |
| Sonnet-priced | 47.7% | 21.4% | **TIER** |
| Haiku-priced | 50.3% | 21.0% | **TIER** |
| **Free** (absurd floor) | 53.1% | 20.5% | **TIER** |

**Tier wins in every world, including the one where fable is free** — because Opus-only agents
alone are 41.6% of spend. The conclusion does not depend on the guess.

### 6b. The mechanism can't reach the money

Even granting the finding, a per-child price tag shown to a parent cannot move the main pool:

- **51.7% of all spend sits at depth 1** — the operator's own direct reports. **No in-swarm parent
  closes them; only the human does.** The mechanism informs parents about children; the largest
  single cost pool is the *operator→seat* edge, where the "parent" is the very person the report is
  trying to inform.
- Of the $575 long-lived spend, **$370.59 (64%) is held by agents that are themselves parents.**
  **A parent cannot close itself.**

*(In fairness — and against my own earlier draft: `corr(turns, $) = 0.878` beats
`corr(children, $) = 0.673`, and the #2 and #9 spenders (`hardener`, `hc-build1`) are **childless
leaves**. So "coordinators are the problem" is NOT the right story either. I withdraw that as a
primary attack and keep it only as a constraint on mechanism design.)*

### 6c. And your own doubt was correct

You asked whether a number fixes a problem prose already failed at. Worse: **the number points the
wrong way.** A parent shown "this child has cost you $12" is being nudged to close an agent whose
remaining turns are its *most productive*. **The mechanism, if it works, makes the swarm worse.**

---

## §7 — WHAT SURVIVES: the defensible claim, with the overclaim cut off

Strip the errors and the inversion, and something real remains. It is smaller and better:

> ### Context accumulation is a real and measurable cost tax.
> **Within a single agent**, holding the agent and its task fixed, **$/turn rises as it ages**:
> for the 27 agents that reached ≥80 turns, **26 of 27** cost more per turn in their turns 41–80
> than in their own turns 1–40 (**median 1.40×**). The longest-lived agents reach **1.6–2.7×**
> their own early rate (`opencode-plugin-scout` 2.69×, `field-tester` 2.52×,
> `harness-contractor` 2.36×).
>
> This is not composition, not selection, and not arithmetic. **An agent's turns get more expensive
> as its context grows, and this was not previously measured.**

**What that licenses — and what it does not:**

| ✅ Defensible | ❌ Overclaim — cut it |
|---|---|
| Context growth taxes each turn (~1.4× by turn 80, up to 2.7× in the tail) | "Lifetime is THE cost lever" |
| The tax is real, measured, previously unknown | "Not model tier" — **false; tier is 2.4× bigger** |
| **Compaction / context hygiene** is the mechanism this finding supports | "Close children sooner" — **cuts output, not cost** |
| Short leaves are genuinely cheap (9.7% of spend) | "Cache reads are 58.6% of cost" — **they are a 6.3× saving** |
| $798 total was invisible to the operator until now — **that alone is worth the stream** | "Doctrine was secretly the best cost mechanism" — it isn't, and it's aimed at the wrong edge |

**The finding supports a different mechanism than the one proposed.** Rising $/turn with context is
an argument for **compaction and context hygiene** — keep the agent, shrink what it re-reads. It is
*not* an argument for killing the agent, because the data shows the agent's late turns are its most
valuable. **Same finding, opposite intervention.**

**And the mechanism the data actually screams for is the one the report explicitly dismissed:**
`spawn-repair` shipped a merged, adversarially-reviewed PR in **201 turns for $5.68** on sonnet.
The live question at spawn time is **"does this job need Opus?"** — not "how long may this agent
live?"

---

## §8 — Minor / housekeeping

- **The doc is more careful than its own summary.** `COST-ANATOMY.md` correctly labels
  `field-tester` as **fable**, correctly flags fable's price as **ASSUMED**, and correctly notes
  `<synthetic>` contributes **$0**. It never claims "Opus is 14%" and never calls `field-tester`
  sonnet. **The errors are in the headline, not the analysis.** That's good news: it's a
  summarization fix, not a re-analysis.
- **`population.json` no longer matches the doc** ($804.45 / 222 agents vs $797.84 / 221) because
  the swarm kept running while I worked. Benign — but it means **no figure in the doc is exactly
  reproducible from the shipped raw data.** For a report whose authority is the word *MEASURED*,
  pin the JSON and regenerate the tables from it.
- **Sonnet's rate is promotional and expires 2026-09-01** ($2/$10 → $3/$15, per `_hc-price.md`).
  Every Sonnet figure here — and the entire tier lever — is ~1.5× less attractive after that date.
  **Still wins**, but the report should date-stamp this.

---

## SUMMARY TABLE

| Attack | Verdict |
|---|---|
| **4. Tool wrong** | **★ LANDS — THE WORST OF THE THREE.** Dedup and attribution are sound and the tool never *over*counts. But `turns` = **API calls, not turns** (13.9:1; "53 long-lived" → **1** under an interaction reading; **67% of their prompts are `check queue` pings**). And the tool is **blind to the $275.49 operator session** and to 749 nested subagent files — **$1,058.30 unclaimed**. **Long-lived share: 71.2% → 30.9%.** |
| 6. Mechanism follows | **REFUTED** — tier saves **54.6%** vs lifetime **22.5%**, robust even if fable is free; 51.7% of spend sits where no parent can close it; the lifetime lever deletes output. |
| 1. Tautology | **WOUNDED** — 92% of the "71.2%" is just share-of-turns. Real finding is 5.7 pts, and is far better shown *within*-agent (26/27, 1.40×). |
| 2. Reverse causation | **HOLDS AGAINST YOU** — no idle long agent exists; spend *accelerates* to the end; `spawn-repair` (201t, $5.68) vs `harness-contractor` (194t, $40.46) = **7.1× at constant lifetime**. |
| 5. Cache reads | **REFUTED — framing inverted.** Caching *saves* $4,264 (6.3×). 97% of tokens at a 90% discount is not a cost problem. |
| 3. Survivorship | **REFUTED** — the 5 dropped agents cost ≈$0; bias favours your claim. |

**Bottom line.** The tool never overcounts and the arithmetic is honest — but **the headline rests on
a word and a denominator, and both are wrong.** "Turns" means API calls, so the long-lived cohort is
an artifact of a **polling loop**, not of long context. The denominator omits the **operator, the
system's single biggest spender**, dropping 71.2% to **30.9%**. And the one lever the report
dismissed — **model tier** — is 2.4× bigger than the one it recommends, and is the only one that
doesn't delete output.

**What to salvage:** the within-agent context tax is real (26/27 agents, median 1.40×). It argues for
**compaction and for not pinging idle agents** — keep the agent, shrink what it re-reads, stop waking
it. **Not** for killing agents whose late turns are their most productive. Same finding, opposite
mechanism. And **$798 → really ~$1,860** was invisible to the operator until this stream ran, which
is worth the stream on its own.
