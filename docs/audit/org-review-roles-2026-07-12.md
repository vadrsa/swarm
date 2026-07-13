# Role census — recurring roles and duplicate work in this swarm's history

**Agent:** `role-census` (child of `shape-forensics`, under `org-review-scout`)
**Date:** 2026-07-12
**Mission:** pure counting. No design, no org-shape recommendation. Numbers only.

---

## 0. Evidence base and its honest limits

| Fact | Value | Status |
|---|---|---|
| Agent records read (`.swarm/agents/*.json`) | **115** | VERIFIED |
| ...of which classified into a role | **115 / 115** (0 missing, 0 double-counted) | VERIFIED |
| Distinct names among the 115 | **115** | VERIFIED |
| **Literal name reuse (forbidden by the world)** | **ZERO** | **VERIFIED — NULL RESULT** |
| Top-level agents (`parent == operator`) | **25** | VERIFIED |
| Event records / journals | 87 / 117 | MEASURED |
| Swarm lifespan | 2026-07-09 18:40Z → 2026-07-12 16:57Z (**~70.3h, 4 UTC days**) | VERIFIED |
| Spawns per UTC day | 07-09: **5**, 07-10: **38**, 07-11: **21**, 07-12: **51** | VERIFIED |

**Correction to my own brief (MEASURED).** The brief specified 107 agents / 86 events
/ 110 journals. The true count at read time was **115 / 87 / 117**, and by the time I
finished merging it was **123** — the tree spawned 8 more agents *while I was counting
it* (my own 4 classifiers, plus `falsifier-probe`'s 4). **The census is a snapshot of a
moving population.** All counts below are the **115 records that existed at snapshot
time (2026-07-12 ~16:57Z)** — a fixed, reproducible cut. The 8 later agents are excluded
by construction, not by oversight.

**Method.** Classification was fanned out to four children (`census-c1..c4`), each given
one ~29-agent slice of the briefs plus a single pinned taxonomy, so their outputs merge
without drift. I kept taxonomy design, the merge, verification, and sections D and E.
Every class below is assigned **by what the brief asks for, not by the agent's name** —
`structure-scout` is named like a scout and *is* one (its brief says "deep design
research… Deliverable: docs/design/STRUCTURE.md"), but `structure-grave`, named like a
forensics agent, is classed **RED** because its brief says *"check whether it is a corpse
reborn… Rule honestly."*

---

## 1. HEADLINE NUMBERS

| # | Question | Answer | Status |
|---|---|---|---|
| 1 | Distinct role classes found | **9** (RED, SCOUT, FORENSICS, RUNNER, DRAFTER, BUILDER, FIXER, COORD, OTHER) | MEASURED |
| 2 | **Times the `scout → drafter → red` 3-stage shape ran, in full, with all-new names** | **4** | **VERIFIED** |
| 3 | Times the weaker `design → attack` 2-stage shape ran | **9** | VERIFIED |
| 4 | **Distinct names that held the RED role** | **25** | **VERIFIED** |
| 5 | Distinct names that held FORENSICS | **34** | VERIFIED |
| 6 | Distinct names that held SCOUT | **21** | VERIFIED |
| 7 | RED spread: distinct days / distinct parents | **3 of 4 days, 14 different parents** | VERIFIED |
| 8 | Literal name reuse anywhere in the record | **0** | VERIFIED |
| 9 | **Real duplicate work found among the 25 top-level agents** | **0 pairs** (all 5 candidates are legitimate sequels) | **REASONED — see §5** |

**The one-sentence finding.** Three roles — RED (25 names), FORENSICS (34), SCOUT (21) —
were each re-instantiated **dozens of times under a fresh name every single time**,
across **all or nearly all four days** of the swarm's life and across **many different
parents**; and **not one name was ever reused.** The recurrence is real and it is
spread, not bursty. Whether that *should* have produced standing roles is a design
question I was told not to answer — but the count is unambiguous.

---

## 2. (A) ROLE TAXONOMY — the classes, with counts

Classes were fixed **before** classification (`TAXONOMY.md`, 8 classes + OTHER) so four
parallel classifiers would produce mergeable output. Primary class only; an agent that
spans two is counted once, under its deliverable.

| Role class | N | What the brief asks for |
|---|---:|---|
| **FORENSICS** | **34** | Mine existing files/history/records for facts. Backward-looking, no design. |
| **RED** | **25** | Adversarially attack someone else's work. "KILL it, don't improve it." |
| **SCOUT** | **21** | Explore an open question, produce a design/recommendation. Forward-looking. |
| **RUNNER** | **18** | Execute one benchmark cell / probe / measurement and report the number. |
| **DRAFTER** | **8** | Write up a doc from conclusions others reached. |
| **BUILDER** | **3** | Write real code / ship a PR. |
| **OTHER** | **3** | The three SPAN load-test fixtures — briefs contain *no task* ("you will receive a stream of tasks"). |
| **FIXER** | **2** | Apply a known fix / keep something current. (`updater`, `updater-v2`) |
| **COORD** | **1** | Spawn + judge children, little first-hand work. (`warm-coord-1`) |
| | **115** | |

### Two numbers worth pausing on

- **BUILDER = 3 out of 115 (2.6%).** This swarm has spent ~97% of its agent-population on
  research, critique, evidence, and measurement, and ~3% on writing code
  (`hardener`, `skill-writer`, `battery-smith`). MEASURED, not judged.
- **COORD = 1 is an artifact of the taxonomy, not of behaviour — and the ratio is the
  finding.** Only `warm-coord-1` was briefed to *purely* coordinate. **18 other agents
  carry COORD as a secondary role**, and **12 of those 18 are top-level** — i.e. **half of
  everything the operator dispatched to (12 of 25) was a working-coordinator.**
  (VERIFIED, from the secondary column + parent field.)

  **Pure coordinators : working-coordinators = 1 : 18.** Coordination in this swarm is
  almost never a job; it is a *hat worn by a worker*.

  **This was challenged, and the challenge is what produced the number.** My classifier
  `census-c2` pushed back on exactly these rows: *"Every coordinator-shaped agent in this
  slice has a first-hand DELIVERABLE named in its brief… with 'delegate freely' as a
  permission, not the primary ask. If your rubric wants spawn-and-judge to dominate, those
  5 flip to COORD primary and SCOUT drops to 2."* I re-read all five briefs against the
  record. **c2 is right and the classification stands:** each names a first-hand artifact
  (`"Deliverable: docs/design/PIPELINE-WIRING.md — recommendation not survey"`) and appends
  **"Delegate freely"** as a *permission at the end* — never as the ask. Nobody in this
  swarm's history was ever dispatched to coordinate as their job. They were dispatched to
  *produce something*, and delegated on their own initiative while doing it.

  The 18: `field-tester`, `harness-scout`, `decision-scout`, `decision-wiring`,
  `proxy-scout`, `pipeline-scout`, `hook-scout`, `fleet-eval`, `onboarding-scout`,
  `operator-structure-scout`, `opencode-plugin-scout`, `org-review-scout` (all top-level),
  plus `wiring-surfaces`, `graveyard-check`, `oc-priorart`, `shape-forensics`,
  `structure-red2`, `deleg-heavy-after-1`.

---

## 3. (B) RECURRENCE — how many distinct names held each role

**The question is: how many times was a role re-instantiated under a NEW name?**
Because zero names were ever reused (VERIFIED), *every* instance below is a fresh name.

### RED — 25 distinct names, 0 reused (VERIFIED)

`red-simplest`, `red-operator`, `red-decisions`, `red-wiring`, `red-proxy`,
`pipeline-red`, `pipeline-redcheck`, `hook-red`, `hook-redcheck`, `eval-red`,
`onboarding-red`, `v3-red`, `v3red-mcp`, `v3red-queue`, `v3red-score`, `dp-red`,
`structure-red`, `structure-grave`, `structure-red2`, `red2-trace`, `red2-mech`,
`red2-doctrine`, `oc-red`, `structure-red3`, `grave-org`

Spawned by **14 different parents**: operator (×2), decision-scout, wiring-drafter,
proxy-scout, pipeline-drafter, pipeline-scout, hook-scout (×2), fleet-eval,
onboarding-scout, field-tester (×2), operator-structure-scout (×4), structure-red2 (×3),
opencode-plugin-scout, org-review-scout, v3-red (×3).

**The RED role was re-invented 25 times by 14 different dispatchers who never once
reached for an existing name.**

### FORENSICS — 34 distinct names (VERIFIED)
`field-tester`, `deleg-heavy-base-1`, `dh1-refs`, `dh1-concepts`, `codex-audit`,
`ledger-miner`, `pr-miner`, `wiring-surfaces`, `seat-ritual`, `ws-cli-tracer`,
`ws-hooks-scout`, `ws-gate-miner`, `eval-red-glmforensics`, `graveyard-check`,
`grave-span`, `grave-notlist`, `grave-history`, `notlist-phil`, `notlist-decs`,
`notlist-wire`, `structure-mech`, `oc-api`, `oc-priorart`, `oc-docs`, `oc-eco`,
`ledger-forensics`, `shape-forensics`, `grave-priorart`, `grave-kills`,
`falsifier-probe`, `grave-phil8`, `role-census`, `kill-audit`, `kill-nag`, `kill-metrics`
*(quota-scout counted under its primary SCOUT; the 34 above are primary-FORENSICS.)*

### SCOUT — 21 distinct names (VERIFIED)
`codex-scout`, `structure-scout`, `inbox-scout`, `harness-scout`, `bench-designer`,
`quota-scout`, `switch-scout`, `decision-scout`, `decision-wiring`, `proxy-scout`,
`pipeline-scout`, `hook-scout`, `patterns-contractor`, `fleet-scout`, `fleet-eval`,
`onboarding-scout`, `mine-probe`, `probe-designer`, `operator-structure-scout`,
`opencode-plugin-scout`, `org-review-scout`

### RUNNER — 18 distinct names (VERIFIED)
`probe-a`, `deleg-heavy-after-1`, `dh1-flake`, `dh1-latency`, `run-deepseek`, `run-glm`,
`run-claude-base`, `run-deepseek-2`, `run-glm-2`, `run-claude-base-2`, `v3-run-ds`,
`v3-run-glm`, `v3-run-cb`, `dp-f1`, `dp-f2`, `oc-probe`, `red2-trace`*, `ocr-lab`*
*(\*primary-RED/RUNNER split — see the 115-row table.)*

### DRAFTER — 8 · BUILDER — 3 · FIXER — 2 · COORD — 1
`wiring-drafter`, `proxy-drafter`, `pipeline-drafter`, `hook-drafter`, `battery-smith`,
`onboarding-split`, `deleg-base-1`, `deleg-after-1`, `warm-worker-1` (drafter-ish
fixtures) · `hardener`, `skill-writer`, `battery-smith` · `updater`, `updater-v2` ·
`warm-coord-1`

### NULL RESULT — literal name reuse
**I looked for a reused name and found none.** All 115 names are distinct
(`len(set(names)) == 115`, no filename/record mismatch). `updater` → `updater-v2` and
`structure-red` → `red2` → `red3` are **new names for a recurring shape**, which is the
opposite of reuse. The world's rule ("a name ever used is an error to reuse") **holds
perfectly in the record.** VERIFIED.

---

## 4. (C) TIME SPREAD — burst or standing?

The distinction the mission asks for: *5 instances in one hour is a burst; 5 instances
across 4 days is a standing role.* Here is the answer, measured.

| Class | N | First spawn | Last spawn | **Distinct days** | Span | Per-day histogram |
|---|---:|---|---|---:|---:|---|
| FORENSICS | 34 | 07-09 18:40 | 07-12 16:57 | **4 / 4** | 70.3h | 09:1 · 10:10 · 11:1 · 12:22 |
| RED | 25 | 07-10 15:46 | 07-12 16:55 | **3 / 4** | 49.2h | 10:5 · 11:5 · 12:15 |
| SCOUT | 21 | 07-09 23:07 | 07-12 16:53 | **4 / 4** | 65.8h | 09:1 · 10:9 · 11:5 · 12:6 |
| RUNNER | 18 | 07-09 18:44 | 07-12 16:42 | **4 / 4** | 70.0h | 09:1 · 10:4 · 11:6 · 12:7 |
| DRAFTER | 8 | 07-10 11:53 | 07-12 13:25 | **3 / 4** | 49.5h | 10:5 · 11:2 · 12:1 |
| BUILDER | 3 | 07-09 18:41 | 07-11 18:21 | 2 / 4 | 47.7h | 09:1 · 11:2 |
| FIXER | 2 | 07-09 20:37 | 07-10 17:09 | 2 / 4 | 20.5h | 09:1 · 10:1 |
| **OTHER** | 3 | 07-10 13:14 | 07-10 13:37 | **1 / 4** | **0.4h** | 10:3 |
| COORD | 1 | 07-10 16:48 | 07-10 16:48 | 1 / 4 | 0.0h | 10:1 |

**Verdict: the four big roles are SPREAD, not bursts. VERIFIED.**
RED, SCOUT, FORENSICS and RUNNER each recur on **3–4 of the swarm's 4 days**, spanning
**49–70 hours** — i.e. they reappear across *separate working sessions*, not within one.

**The control case proves the measure is not vacuous.** `OTHER` (the three SPAN load-test
fixtures) is a *textbook burst*: 3 instances inside **24 minutes**, one day, one parent.
`COORD` is a single point. The metric cleanly separates burst from standing — and RED,
SCOUT, FORENSICS, RUNNER all land firmly on the standing side.

---

## 5. (D) DUPLICATE WORK — the verdict is NULL, and I checked hard

I examined every candidate the mission named, plus the top-level list. **I found zero
pairs of real duplicate work.** Every suspicious-looking pair turns out to be a
**legitimate sequel**: the second agent's own brief *names what the first one got wrong
or didn't know*. This is a NULL RESULT and I am stating it plainly rather than inflating
it — but note the sequels are *evidence of iteration*, not of waste.

### Candidate 1: `updater` vs `updater-v2` — **LEGITIMATE SEQUEL** (VERIFIED)

- `updater` (07-09): *"keep the installed swarm tooling (~/.local/share/swarm, a git clone
  of github.com/vadrsa/swarm) current with origin/main… Watch via a run-in-background
  fetch-and-compare loop (~5 min)."*
- `updater-v2` (07-10): *"THE TOOL: /Users/vadrsa/git/swarm… Releases are git TAGS…
  INSTALL MODEL (verified): … install.sh COPIES bin/swarm into ~/.local/share/swarm…
  **So `git pull` alone does NOT change the running binary. Only `./install.sh` swaps
  it.** … You are woken once a day by a system cron."*

v2 **corrects a factually wrong model of the world** in v1 (git-pull ≠ new binary), swaps
the watch mechanism (background poll → daily cron), and re-targets the repo. Not the same
work twice; the second knew something the first could not.

### Candidate 2: `fleet-scout` vs `fleet-eval` — **LEGITIMATE SEQUEL** (VERIFIED)

- `fleet-scout`: *"how to add Chinese models… as **LEAF-ONLY** agents — the operator has
  already accepted leaf-only, so design HOW to make a good leaf, **don't re-justify the
  constraint**."*
- `fleet-eval`: *"**You succeed fleet-scout; keep FLEET.md's execution-surface findings,
  discard its leaf-only emphasis.** The operator's correction: leaf-only is a fallback…
  NOT a requirement — non-Claude models could be PARENTS."*

The brief *explicitly* says which half to keep and which to discard. **The operator
overruled its own earlier constraint** — that is a corrected premise, not a repeat.

### Candidate 3: `codex-scout` vs `codex-audit` — **NOT DUPLICATION; different objects** (VERIFIED)

- `codex-scout`: design work — *"docs/design/CODEX-DESIGN.md: the minimal integration
  design — what bin/swarm gains, what each hook maps to"* (designs **swarm's** codex support).
- `codex-audit`: *"**READ-ONLY audit of the operator's local Codex CLI setup** — version
  currency… config.toml hygiene… diagnose the observed 'MCP startup interrupted' warning."*

One designs a feature; the other audits a **machine's local install**. Different targets
entirely. The only overlap is the word "codex".

### Candidate 4: `structure-scout` vs `operator-structure-scout` — **SEQUEL across a failed test** (VERIFIED)

- `structure-scout` (07-10): *"deep design research into **where tree structure actually
  comes from**… hypotheses: (1) structure comes from REPETITION… (2) strict structure may
  belong at the OPERATOR interface only."* → shipped `STRUCTURE.md`.
- `operator-structure-scout` (07-12, **two days later**): *"Design the GENERALIZED
  doctrine that **replaces the coordinator-stance half of the shipped onboarding
  doctrine (which live F1 testing proved fails 2/2 via an operator name-collision —
  sessions flat-spawn parent=operator while citing the doctrine)**."*

The second was spawned **because field evidence falsified the first's shipped output**.
That is the research loop working, not duplicated effort.

### Candidate 5: `red-simplest` vs `red-operator` — **DELIBERATE PARALLEL DIVERSITY** (VERIFIED)

Same target (`operator-capabilities-proposal.md`), **spawned 2 seconds apart** — and given
*deliberately different lenses*:
- `red-simplest`: *"Your lens: **SIMPLICITY AND PHILOSOPHY**… hunt: resurrection of
  deleted concepts in disguise."*
- `red-operator`: *"Your lens: **THE HUMAN OPERATOR AND MULTI-SESSION REALITY**… simulate
  concretely: 3 parallel hands, one dies mid-dispatch, one is on a phone."*

This is the multi-lens pattern (two reviewers, disjoint blind spots), not accidental
double-work. The same intent is *explicit* in `hook-redcheck`: *"A first red reviewer
(hook-red) is running in parallel; **you do NOT coordinate with it — your value is
catching the blind spot you would BOTH share** if you compared notes."*

### NULL RESULTS — stated explicitly
- **No pair of agents was found doing the same work twice in ignorance of each other.**
- **No agent re-derived an artifact another had already produced** without its brief
  naming the reason (correction, overrule, or falsification).
- The nearest thing to true redundancy — the paired reviewers (`*-red` + `*-redcheck`) —
  is **intentional redundancy, briefed as such.**

---

## 6. (E) THE REPEATED PIPELINE — the mission's key hypothesis, CONFIRMED

**Hypothesis:** *"the operator repeatedly ran the same 3-stage shape — scout (design) →
red (attack) → drafter/wiring (write it up)."*

**VERIFIED. The full 3-stage shape ran 4 times. The weaker 2-stage `design → attack`
shape ran 9 times. Every instance used entirely fresh names.**

### The 4 full `SCOUT → DRAFTER → RED` pipelines

| # | Family | SCOUT (design) | DRAFTER (write) | RED (attack) | Artifact |
|---|---|---|---|---|---|
| 1 | decision-wiring | `decision-wiring` | `wiring-drafter` | `red-wiring` | DECISION-WIRING.md |
| 2 | proxy | `proxy-scout` | `proxy-drafter` | `red-proxy` | PROXY-WIRING.md |
| 3 | pipeline | `pipeline-scout` | `pipeline-drafter` | `pipeline-red` **+ `pipeline-redcheck`** | PIPELINE-WIRING.md |
| 4 | hook | `hook-scout` | `hook-drafter` | `hook-red` **+ `hook-redcheck`** | HOOK-WIRING.md |

**12 agents, 12 fresh names, 4 identical role-shapes.** Note the shape *evolved*: families
3 and 4 added a **second, independent red** — the operator learned that one reviewer
shares blind spots with the drafter that spawned it.

### The 9 `design → attack` families (the weaker, more general shape)

`decision-scout`→`red-decisions` · `decision-wiring`→`red-wiring` ·
`proxy-scout`→`red-proxy` · `pipeline-scout`→`pipeline-red`+`redcheck` ·
`hook-scout`→`hook-red`+`redcheck` · `fleet-eval`→`eval-red` ·
`onboarding-scout`→`onboarding-red` · `operator-structure-scout`→`structure-red`(+red2,red3) ·
`opencode-plugin-scout`→`oc-red`

**9 times, 9 fresh scout names, 9+ fresh red names. Not once was a warm name re-addressed.**

### The finding *behind* the finding: families 1–4 are ONE question, asked four times

The four "pipeline" families are not four topics. They are **four consecutive iterations
of a single question** — how to wire the decision engine — and each brief says so:

| Iter | Agent | The brief's own words |
|---|---|---|
| v1 | `decision-scout` | *"Research a decision engine that proxies operator-bound decision points"* |
| v1.5 | `decision-wiring` | *"**you succeed decision-scout, whose deliverable the operator RETURNED** with the verbatim reason 'the task is to understand how to wire up such an engine… not if we want to build it'"* |
| v2 | `proxy-scout` | *"whether the assumed decision engine **generalizes** from the operator mailbox to the WHOLE message plane"* |
| v3 | `pipeline-scout` | *"**third iteration** of the decision-engine wiring — the operator now asks for ONLY operator-bound escalations"* |
| v4 | `hook-scout` | *"**v4** of the decision-engine wiring — the operator **overruled the zero-tool-change constraint every predecessor assumed**"* |

**Each iteration knew something its predecessors could not** (v1.5: wrong question asked;
v2: generalize; v3: narrow again after v2 died; v4: a constraint all three had assumed was
lifted). By the D-criterion this is **iteration, not duplication** — but by the E-criterion
it is **the same organizational shape, rebuilt from scratch, five times, with 5 scouts, 4
drafters and 6 reds, none of whom shared a name with their predecessor.**

That sentence is the census's central number.

---

## 7. Testing STRUCTURE.md's claim against this data

`docs/design/STRUCTURE.md` §2b makes a **falsifiable** claim, and it is *narrower* than
"recurring shapes justify standing agents". Quoted exactly:

> *"the structural signal is not 'this kind of work keeps arriving' — it is **'I, the
> dispatcher, keep choosing to reuse this name.'**"*

and, crucially:

> *"SPAN's flood probes were repetitive (9 near-identical summarization tasks) and that
> repetition produced **zero** structure… Repetition inside a single agent's queue is just
> backlog; it never earns a new name."*

**What my data says about that claim (MEASURED; the interpretation is left to my parent):**

1. **STRUCTURE.md's descriptive claim is CONFIRMED.** Name-reuse never happened (0/115),
   and correspondingly **no standing role ever formed** for RED, SCOUT, or FORENSICS.
   The mechanism it names (reuse-a-warm-name) is indeed the only thing that produced
   standing arms, and it was never applied to these three roles.

2. **But the doctrine's own dismissal of repetition does not cover this case.** Its
   counter-example (the 9 span probes) is a *burst*: **9 tasks, one queue, one hour, one
   parent.* The RED role is the **opposite** on every axis I measured:
   **25 instances · 3 of 4 days · 49.2 hours · 14 different parents.**
   STRUCTURE.md rules out *backlog inside one queue*. It says nothing about a shape that
   **14 independent dispatchers each re-derive from scratch across three days.**

3. **NULL RESULT — the doctrine's predicted signal never fired for the big three roles.**
   By STRUCTURE.md's own test, RED/SCOUT/FORENSICS are *not* standing roles, because no
   dispatcher ever re-addressed a warm name. Whether that is the doctrine correctly
   describing reality, or the doctrine's test **failing to detect the most repeated shape
   in the swarm's history**, is a design question. **I was briefed to count, not to rule.
   The count is above; the ruling belongs to `shape-forensics` and `org-review-scout`.**

---

## 8. Appendix — the full 115-agent classification (every agent, one row)

Ordered by spawn time. **PRIMARY** = the class its brief actually asks for. **2nd** = a
secondary role it also carries. **Evidence** = the literal phrase from the brief that
decides the class. Classified by `census-c1..c4` against a pinned taxonomy; merged and
spot-audited by `role-census`.

| # | Agent | Parent | Spawn (UTC) | PRIMARY | 2nd | Evidence from its brief |
|---:|---|---|---|---|---|---|
| 1 | `field-tester` | `operator` | 07-09 18:40 | **FORENSICS** | COORD | "produce evidence for/against each docs/design/WATCHLIST.md item" |
| 2 | `hardener` | `operator` | 07-09 18:41 | **BUILDER** | FIXER | "port the 22 process-level tests rescued at .swarm/briefs/review_tests |
| 3 | `probe-a` | `field-tester` | 07-09 18:44 | **RUNNER** | - | "run the repo unit tests once with: python3 tests/test_swarm.py" |
| 4 | `updater` | `operator` | 07-09 20:37 | **FIXER** | - | "keep the installed swarm tooling (~/.local/share/swarm ...) current w |
| 5 | `codex-scout` | `operator` | 07-09 23:07 | **SCOUT** | - | "docs/design/CODEX-DESIGN.md: the minimal integration design" |
| 6 | `deleg-base-1` | `field-tester` | 07-10 11:53 | **DRAFTER** | - | "Produce four independent summaries of four unrelated documents in thi |
| 7 | `deleg-heavy-base-1` | `field-tester` | 07-10 11:57 | **RUNNER** | FORENSICS | "Four independent audit jobs on this repo, all real work" |
| 8 | `deleg-after-1` | `field-tester` | 07-10 12:03 | **DRAFTER** | - | "Produce four independent summaries of four unrelated documents in thi |
| 9 | `deleg-heavy-after-1` | `field-tester` | 07-10 12:06 | **RUNNER** | COORD | "Four independent audit jobs on this repo, all real work" |
| 10 | `dh1-flake` | `deleg-heavy-after-1` | 07-10 12:07 | **RUNNER** | - | "Run 'python3 tests/test_swarm.py' 25 times in a row. Tally passing vs |
| 11 | `dh1-refs` | `deleg-heavy-after-1` | 07-10 12:07 | **FORENSICS** | - | "For each, check whether it exists on disk" |
| 12 | `dh1-concepts` | `deleg-heavy-after-1` | 07-10 12:08 | **FORENSICS** | - | "check whether it is named in docs/design/SIMPLEST.md" |
| 13 | `dh1-latency` | `deleg-heavy-after-1` | 07-10 12:08 | **RUNNER** | - | "Run 'swarm world >/dev/null' 25 times, timing each run in millisecond |
| 14 | `span-base-1` | `field-tester` | 07-10 13:14 | **OTHER** | - | "You will receive a stream of tasks from your parent field-tester" (no |
| 15 | `span-after-1` | `field-tester` | 07-10 13:22 | **OTHER** | - | "You will receive a stream of tasks from your parent field-tester" (no |
| 16 | `span-heavy-1` | `field-tester` | 07-10 13:37 | **OTHER** | - | "These tasks are long-running and each has a mid-task checkpoint gate" |
| 17 | `structure-scout` | `operator` | 07-10 15:12 | **SCOUT** | RED | "deep design research (no code ...) into where tree structure actually |
| 18 | `red-simplest` | `operator` | 07-10 15:46 | **RED** | - | "Attack stance: try to KILL each proposal item" |
| 19 | `red-operator` | `operator` | 07-10 15:46 | **RED** | - | "Attack stance: try to BREAK each item under realistic use" |
| 20 | `inbox-scout` | `operator` | 07-10 16:47 | **SCOUT** | - | "research-only evaluation of the operator's inbox ideas" |
| 21 | `warm-coord-1` | `field-tester` | 07-10 16:48 | **COORD** | - | "spawn ONE child to do the work, verify its artifact yourself, then re |
| 22 | `warm-worker-1` | `warm-coord-1` | 07-10 16:49 | **DRAFTER** | - | "Read docs/design/REVIEW.md and write a ~100-word summary of it" |
| 23 | `updater-v2` | `operator` | 07-10 17:09 | **FIXER** | - | "a standing agent that keeps the swarm tool itself up to date" |
| 24 | `codex-audit` | `operator` | 07-10 17:10 | **FORENSICS** | - | "READ-ONLY audit of the operator's local Codex CLI setup" |
| 25 | `harness-scout` | `operator` | 07-10 17:40 | **SCOUT** | COORD | "own the multi-harness design the codex integration is missing" |
| 26 | `bench-designer` | `harness-scout` | 07-10 17:43 | **SCOUT** | - | "design (do NOT run) a repeatable swarm-specific instruction-following |
| 27 | `quota-scout` | `harness-scout` | 07-10 17:43 | **SCOUT** | FORENSICS | "discover via cheap READ-ONLY probes what usage/quota signals actually |
| 28 | `switch-scout` | `harness-scout` | 07-10 17:43 | **SCOUT** | - | "design harness switching for an existing agent given tombstones + jou |
| 29 | `decision-scout` | `operator` | 07-10 18:02 | **SCOUT** | COORD | "Research a decision engine that proxies operator-bound decision point |
| 30 | `ledger-miner` | `decision-scout` | 07-10 18:03 | **FORENSICS** | - | Build a decision table ... one row per decision point routed to the op |
| 31 | `pr-miner` | `decision-scout` | 07-10 18:03 | **FORENSICS** | - | Build a table ... one row per PR/merge decision — PR number, branch, w |
| 32 | `red-decisions` | `decision-scout` | 07-10 18:13 | **RED** | - | Your job is to BREAK it, not improve it |
| 33 | `decision-wiring` | `operator` | 07-10 19:05 | **SCOUT** | COORD | Design the WIRING end to end ... recommendation not survey, falsifiers |
| 34 | `wiring-surfaces` | `decision-wiring` | 07-10 19:08 | **FORENSICS** | COORD | Facts with file:line quotes, no design, no recommendation |
| 35 | `seat-ritual` | `decision-wiring` | 07-10 19:08 | **FORENSICS** | - | Facts and quotes only, no design |
| 36 | `ws-cli-tracer` | `wiring-surfaces` | 07-10 19:09 | **FORENSICS** | - | Facts only, no design, no recommendations. Every claim needs a file:li |
| 37 | `ws-hooks-scout` | `wiring-surfaces` | 07-10 19:09 | **FORENSICS** | - | mapping the hook/event/config surfaces of this swarm repo ... Facts on |
| 38 | `ws-gate-miner` | `wiring-surfaces` | 07-10 19:09 | **FORENSICS** | - | archaeology of how PRs physically reach the human operator ... Facts o |
| 39 | `wiring-drafter` | `decision-wiring` | 07-10 19:21 | **DRAFTER** | SCOUT | design its complete wiring into this swarm as docs/design/DECISION-WIR |
| 40 | `red-wiring` | `wiring-drafter` | 07-10 19:29 | **RED** | - | Attack the draft, do not decorate it |
| 41 | `proxy-scout` | `operator` | 07-10 21:59 | **SCOUT** | COORD | Deliverable: docs/design/PROXY-WIRING.md, recommendation not survey, p |
| 42 | `proxy-drafter` | `proxy-scout` | 07-10 22:01 | **DRAFTER** | SCOUT | Write docs/design/PROXY-WIRING.md — recommendation, not survey |
| 43 | `red-proxy` | `proxy-scout` | 07-10 22:10 | **RED** | - | Your job: attack it as hard as the record allows |
| 44 | `pipeline-scout` | `operator` | 07-11 01:02 | **SCOUT** | COORD | Deliverable: docs/design/PIPELINE-WIRING.md — recommendation not surve |
| 45 | `pipeline-drafter` | `pipeline-scout` | 07-11 01:04 | **DRAFTER** | SCOUT | Deliverable: docs/design/PIPELINE-WIRING.md — RECOMMENDATION not surve |
| 46 | `pipeline-red` | `pipeline-drafter` | 07-11 01:05 | **RED** | - | a KILL/WOUND-tagged attack on the SKETCH below |
| 47 | `pipeline-redcheck` | `pipeline-scout` | 07-11 01:18 | **RED** | - | You are an INDEPENDENT adversarial reviewer of docs/design/PIPELINE-WI |
| 48 | `hook-scout` | `operator` | 07-11 01:46 | **SCOUT** | COORD | Design the registered-engine routing hook on the operator-queue send p |
| 49 | `hook-drafter` | `hook-scout` | 07-11 01:47 | **DRAFTER** | SCOUT | Draft docs/design/HOOK-WIRING.md — v4 of the decision-engine wiring |
| 50 | `hook-red` | `hook-scout` | 07-11 02:01 | **RED** | - | You are the RED reviewer: your job is to KILL or WOUND load-bearing cl |
| 51 | `hook-redcheck` | `hook-scout` | 07-11 02:01 | **RED** | - | INDEPENDENT second-reviewer of docs/design/HOOK-WIRING.md |
| 52 | `patterns-contractor` | `operator` | 07-11 08:54 | **SCOUT** | - | project the design a senior infra engineer would build, element-by-ele |
| 53 | `skill-writer` | `operator` | 07-11 11:18 | **BUILDER** | - | PLUS wire it into install.sh ... one commit for the skill + one for in |
| 54 | `fleet-scout` | `operator` | 07-11 16:49 | **SCOUT** | - | Deliverable docs/design/FLEET.md, recommendation not survey, falsifier |
| 55 | `fleet-eval` | `operator` | 07-11 18:16 | **SCOUT** | COORD | design AND RUN (approved) a swarm-specific instruction-following eval  |
| 56 | `battery-smith` | `fleet-eval` | 07-11 18:21 | **BUILDER** | DRAFTER | Deliverables: frozen briefs dir ... rubric ... runner wrapper docs/aud |
| 57 | `run-deepseek` | `fleet-eval` | 07-11 18:36 | **RUNNER** | - | Run the frozen battery for the DeepSeek cell via: bash docs/audit/benc |
| 58 | `run-glm` | `fleet-eval` | 07-11 18:36 | **RUNNER** | - | Run the frozen battery for the GLM cell via: bash docs/audit/bench/run |
| 59 | `run-claude-base` | `fleet-eval` | 07-11 18:36 | **RUNNER** | - | SCORE per docs/audit/bench/fleet-rubric-v1.md (4 dims, [H]/[M], §2a, D |
| 60 | `run-deepseek-2` | `fleet-eval` | 07-11 18:48 | **RUNNER** | - | Run: bash docs/audit/bench/run-cell.sh deepseek/deepseek-chat ... run  |
| 61 | `run-glm-2` | `fleet-eval` | 07-11 18:48 | **RUNNER** | - | Run: bash docs/audit/bench/run-cell.sh zai-coding-plan/glm-4.7 ... The |
| 62 | `run-claude-base-2` | `fleet-eval` | 07-11 18:49 | **RUNNER** | - | Run the SAME frozen briefs ... through NATIVE claude ... SCORE per fle |
| 63 | `eval-red` | `fleet-eval` | 07-11 19:42 | **RED** | - | You are a FRESH adversarial reviewer. You did NOT run this eval — atta |
| 64 | `eval-red-glmforensics` | `eval-red` | 07-11 19:45 | **FORENSICS** | - | ONE narrow question: WHY did GLM's D2-heavy/D3b spawned children die/p |
| 65 | `onboarding-scout` | `operator` | 07-12 12:56 | **SCOUT** | COORD | Design a doctrine fix for two adoption pitfalls ... Deliverable docs/d |
| 66 | `mine-probe` | `onboarding-scout` | 07-12 12:56 | **SCOUT** | - | READ-ONLY research; produce a written artifact ... if a helper were wa |
| 67 | `graveyard-check` | `onboarding-scout` | 07-12 12:57 | **FORENSICS** | COORD | search the whole design record for prior art, collisions, and graves |
| 68 | `probe-designer` | `onboarding-scout` | 07-12 12:57 | **SCOUT** | - | EXTRACT THE EXISTING PROTOCOL ... Design a collector that actually wor |
| 69 | `grave-span` | `graveyard-check` | 07-12 12:57 | **FORENSICS** | - | Do not editorialize a verdict — I make the verdicts. Give me raw, exac |
| 70 | `grave-notlist` | `graveyard-check` | 07-12 12:58 | **FORENSICS** | - | Do not editorialize a verdict — I make the verdicts. Raw, exact, cited |
| 71 | `grave-history` | `graveyard-check` | 07-12 12:58 | **FORENSICS** | - | YOUR AXIS — the lived record: journals, audits, git history ... Raw, e |
| 72 | `notlist-phil` | `grave-notlist` | 07-12 12:58 | **FORENSICS** | - | Report EVERY passage that bears on A or B ... Raw, exact, cited materi |
| 73 | `notlist-decs` | `grave-notlist` | 07-12 12:58 | **FORENSICS** | - | the EXACT QUOTED sentence(s) (copy character-for-character, no paraphr |
| 74 | `notlist-wire` | `grave-notlist` | 07-12 12:58 | **FORENSICS** | - | does anything FORBID or CONSTRAIN the skill/hook from READING PRIOR SE |
| 75 | `onboarding-red` | `onboarding-scout` | 07-12 13:07 | **RED** | - | Your job is to try to KILL a design, not to improve it. A polite revie |
| 76 | `onboarding-split` | `operator` | 07-12 13:25 | **DRAFTER** | - | This is a REVISION, not a re-research: do not relitigate the doctrine |
| 77 | `v3-run-ds` | `field-tester` | 07-12 14:01 | **RUNNER** | - | RUN the battery: bash docs/audit/bench/run-cell-v3.sh deepseek/deepsee |
| 78 | `dp-f1` | `field-tester` | 07-12 14:17 | **RUNNER** | - | You test whether a PRISTINE root claude session ... COLLECTOR (file fa |
| 79 | `v3-run-glm` | `field-tester` | 07-12 14:22 | **RUNNER** | - | RUN the battery: bash docs/audit/bench/run-cell-v3.sh zai-coding-plan/ |
| 80 | `dp-f2` | `field-tester` | 07-12 14:42 | **RUNNER** | - | n=2 runs, SEQUENTIAL ... COLLECTORS (file facts, verbatim) ... verdict |
| 81 | `v3-run-cb` | `field-tester` | 07-12 14:49 | **RUNNER** | - | runner for the FLEET v3 NATIVE-CLAUDE BASELINE cell ... SCORE from fil |
| 82 | `v3-red` | `field-tester` | 07-12 15:21 | **RED** | - | Your job: try to BREAK the synthesis at docs/design/FLEET-EVAL-V3.md a |
| 83 | `v3red-mcp` | `v3-red` | 07-12 15:23 | **RED** | FORENSICS | You are an ADVERSARIAL FACT-CHECKER for a bench-eval synthesis. Judge  |
| 84 | `v3red-queue` | `v3-red` | 07-12 15:23 | **RED** | FORENSICS | ADVERSARIAL FACT-CHECKER ... for each claim, ARTIFACT-PROVEN / UNPROVE |
| 85 | `v3red-score` | `v3-red` | 07-12 15:24 | **RED** | FORENSICS | ADVERSARIAL SCORING AUDITOR ... find SCORING INCONSISTENCIES BETWEEN C |
| 86 | `dp-red` | `field-tester` | 07-12 15:49 | **RED** | - | fresh adversarial reviewer ... Try to BREAK it against the primary art |
| 87 | `operator-structure-scout` | `operator` | 07-12 15:59 | **SCOUT** | COORD | Design the GENERALIZED doctrine ... Deliverable docs/design/OPERATOR-S |
| 88 | `structure-red` | `operator-structure-scout` | 07-12 16:01 | **RED** | - | Your job is to try hard to KILL the proposal; a red team that agrees i |
| 89 | `structure-grave` | `operator-structure-scout` | 07-12 16:01 | **RED** | FORENSICS | before adding anything, check whether it is a corpse reborn ... Rule h |
| 90 | `structure-mech` | `operator-structure-scout` | 07-12 16:01 | **FORENSICS** | - | MECHANICS PROBE — read code and files, report facts, no design opinion |
| 91 | `opencode-plugin-scout` | `operator` | 07-12 16:02 | **SCOUT** | COORD | Deliverable docs/design/OPENCODE-PLUGIN.md, recommendation not survey  |
| 92 | `oc-api` | `opencode-plugin-scout` | 07-12 16:03 | **FORENSICS** | - | NO shipped product code; you produce a FACTS doc only: docs/audit/open |
| 93 | `oc-priorart` | `opencode-plugin-scout` | 07-12 16:03 | **FORENSICS** | COORD | Your job — find what ALREADY EXISTS, so we extend rather than reinvent |
| 94 | `oc-probe` | `opencode-plugin-scout` | 07-12 16:04 | **RUNNER** | BUILDER | Build a THROWAWAY PROBE PLUGIN for opencode v1.17.13 and run it LIVE |
| 95 | `oc-docs` | `oc-priorart` | 07-12 16:04 | **FORENSICS** | - | Read the OFFICIAL DOCS and write down exactly what they CLAIM |
| 96 | `oc-eco` | `oc-priorart` | 07-12 16:05 | **FORENSICS** | - | Your job: find what ALREADY EXISTS in the wild |
| 97 | `structure-red2` | `operator-structure-scout` | 07-12 16:22 | **RED** | COORD | FRESH ADVERSARIAL REVIEW — you are the mandatory skeptic on a finished |
| 98 | `red2-trace` | `structure-red2` | 07-12 16:24 | **RED** | RUNNER | ATTACK A + the relation() bug — the highest-value attack in an adversa |
| 99 | `red2-mech` | `structure-red2` | 07-12 16:25 | **RED** | RUNNER | ATTACKS B + C + reproduction, in an adversarial review of a proposed f |
| 100 | `red2-doctrine` | `structure-red2` | 07-12 16:26 | **RED** | - | ATTACKS D + E + F, in an adversarial review of docs/design/OPERATOR-ST |
| 101 | `oc-red` | `opencode-plugin-scout` | 07-12 16:41 | **RED** | - | ADVERSARIAL REVIEW. Attack docs/design/OPENCODE-PLUGIN.md ... Your job |
| 102 | `ocr-lab` | `oc-red` | 07-12 16:42 | **RUNNER** | RED | RE-RUN, HOSTILELY, the four experiments that docs/design/OPENCODE-PLUG |
| 103 | `structure-red3` | `operator-structure-scout` | 07-12 16:45 | **RED** | - | FRESH ADVERSARIAL REVIEW of a REFRAMED design. You are the mandatory s |
| 104 | `org-review-scout` | `operator` | 07-12 16:53 | **SCOUT** | COORD | Deliverable docs/design/ORG-REVIEW.md: instrument recommendation + ful |
| 105 | `ledger-forensics` | `org-review-scout` | 07-12 16:54 | **FORENSICS** | - | MISSION: Mine the OPERATOR LEDGER as EVIDENCE. Produce a data artifact |
| 106 | `shape-forensics` | `org-review-scout` | 07-12 16:55 | **FORENSICS** | COORD | MISSION: Mine the TREE SHAPE + TOP-LEVEL AGENTS' JOURNALS as EVIDENCE |
| 107 | `grave-org` | `org-review-scout` | 07-12 16:55 | **RED** | FORENSICS | find out whether this repo has ALREADY KILLED THIS IDEA ... I want the |
| 108 | `grave-priorart` | `grave-org` | 07-12 16:56 | **FORENSICS** | - | YOUR JOB — THE LIVING PRIOR ART. Read these files FULLY, top to bottom |
| 109 | `grave-kills` | `grave-org` | 07-12 16:56 | **FORENSICS** | - | YOUR JOB — EXHUME THE THREE KILLS ... Quote, never paraphrase kills |
| 110 | `falsifier-probe` | `shape-forensics` | 07-12 16:56 | **FORENSICS** | - | MISSION: answer ONE hard empirical question, honestly, with a real cha |
| 111 | `grave-phil8` | `grave-org` | 07-12 16:56 | **FORENSICS** | RED | §8's test is EMPIRICAL: does the convention already exist, WORKING IN  |
| 112 | `role-census` | `shape-forensics` | 07-12 16:56 | **FORENSICS** | - | MISSION: pure counting. Produce TRUE NUMBERS about RECURRING ROLES and |
| 113 | `kill-audit` | `grave-kills` | 07-12 16:56 | **FORENSICS** | - | YOUR SINGLE JOB — EXHUME THE KILLED 'AUDIT' AGENT ... Quote, never par |
| 114 | `kill-nag` | `grave-kills` | 07-12 16:57 | **FORENSICS** | - | YOUR SINGLE JOB — THE NAG, KILLED TWICE. Find BOTH kills ... verbatim  |
| 115 | `kill-metrics` | `grave-kills` | 07-12 16:57 | **FORENSICS** | - | YOUR SINGLE JOB — THE METRICS ENGINE. Did this repo kill a metrics / d |
---

## 9. Provenance and reproducibility

- **Source of truth:** `.swarm/agents/*.json` (115 records at snapshot), read in full.
  The `task` field — the complete spawn brief — is the evidence for every classification.
- **Method:** briefs dumped and split into 4 slices; four children (`census-c1`…`c4`)
  classified them in parallel against one pinned taxonomy; `role-census` merged (115/115,
  0 gaps, 0 doubles), then personally re-read the ~30 edge cases and all top-level briefs
  for §5 and §6.
- **Claim tags:** VERIFIED = counted mechanically from files. MEASURED = derived from
  those counts. REASONED = my judgment over quoted briefs (only §5's sequel/duplication
  verdicts, each with both briefs quoted so the reader can overrule me).

### Why RED = 25 is trustworthy: two independent checks it survived

**1. Convergent validity on the hardest boundary (VERIFIED).** The grave-hunting agents are
the census's hardest call — they *look* adversarial but many are briefed not to be. Two
classifiers (`census-c3`, `census-c4`) held **disjoint slices**, never saw each other's
work, and **independently drew the identical line**:

| Briefed to… | Class | Agents | The deciding words in their briefs |
|---|---|---|---|
| **RULE / prosecute** | **RED** | `structure-grave`, `grave-org` | *"check whether it is a corpse reborn… **Rule honestly**"* · *"I want the **PROSECUTION case**"* |
| **QUOTE / not decide** | **FORENSICS** | `grave-span`, `grave-notlist`, `grave-history`, `notlist-phil/decs/wire`, `grave-priorart`, `grave-kills`, `kill-audit`, `kill-nag`, `kill-metrics` | *"**Do not editorialize a verdict — I make the verdicts.**"* · *"**Quote, never paraphrase.**"* |

Two independent readers, disjoint evidence, same axis. The boundary is a property of the
briefs, not of a classifier's mood.

**2. The count is a FLOOR, not a ceiling (VERIFIED).** My classifiers repeatedly *declined
to inflate RED when a name invited it*. `eval-red-glmforensics` — which literally has "red"
in its name — is **FORENSICS**, because its brief asks *"ONE narrow question: WHY did GLM's
spawned children die"*. The ten quoter-agents above all hunt for corpses and *look* like
attackers. Waving those eleven in on name or vibe would have taken **RED from 25 → 32, a
28% inflation of this document's headline.** They were excluded because the briefs forbid
them. **If these recurrence numbers err, they err low.**
- **Known limit:** the population grew from 115 → 123 *during* the census. The 8 newest
  agents (4 of them mine) are excluded. Re-running this on the full 123 would change
  FORENSICS (+5) and add my own classifiers; it would not change §5 or §6.
