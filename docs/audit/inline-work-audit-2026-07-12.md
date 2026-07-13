# Inline operator work — a doctrine-failure audit (v2, post-red-team)

Auditor: `inline-work-audit`. Adversarial reviewer: `iwa-red` (fresh spawn) —
`docs/audit/inline-work-audit-RED.md`. **This is v2. The v1 census was materially
wrong in two ways and iwa-red killed both. Both kills are ACCEPTED and folded in;
I re-verified each against the files myself before folding.** The corrections are
recorded in §6, not hidden.

Corpus: `.swarm/journal/operator.md` (**254 lines** — grew during the audit;
v1 read a 202-line snapshot), `skill/SKILL.md` (**HEAD = 106 lines; working tree
= 134**), `skill/references/COORDINATING.md` (untracked), `git log`, `git diff`.

Evidence tags: **VERIFIED** = I ran the check or quoted the file. **REASONED** =
inference from verified facts. **CORRECTED** = v1 claimed otherwise; the red team
was right.

---

## 0. The two corrections that change the answer

### CORRECTION 1 — The edit that triggered this audit was already reverted, and already journaled.

v1's item I14 asserted the operator edited `bin/swarm` + `tests/test_swarm.py`
inline and left it unjournaled, tagged "`git diff` VERIFIED". **I never ran the
diff. I inherited the premise from my own spawn brief and stamped it verified.**

The truth, VERIFIED by me:

- `git diff --quiet HEAD -- bin/swarm tests/test_swarm.py` → **exit 0. Clean.**
  `git status --short` shows only `WORLD.md`, `install.sh`, `skill/SKILL.md`.
- `.swarm/journal/operator.md:203-207` — the operator's own entry:

  > "**Caught myself doing inline work** (added `<model>` to `swarm ps` + test,
  > ran suite) in the operator seat. **Reverted it** (`git checkout bin/swarm
  > tests/`) so the seat leaves no work-in-place. **Then delegated three streams
  > instead**" — `inline-work-audit`, `ps-model`, `model-fit`.

So the audit's *own origin event* is not an unjournaled lapse. It is the operator
noticing an inline lapse mid-flight, reverting it, and delegating it — including
delegating *this audit*. **The system, in that instance, worked.** Any report
that leads with "the operator does inline work and doesn't even journal it" is
reporting the opposite of what happened. **CORRECTED.**

This does not dissolve the finding — the operator *did* start the work inline,
and self-caught rather than never-started. But it changes the honest headline
from *"doctrine is silent and the operator drifts"* to *"doctrine is silent at
the moment of arrival, and the correction currently comes from the operator's own
vigilance after the fact — which is not a mechanism, and will not scale."*

### CORRECTION 2 — Most of the doctrine I arraigned did not exist when the lapses happened.

VERIFIED by `git show HEAD:skill/SKILL.md`:

| Clause | Text | State |
|---|---|---|
| **C1** (:10-11) "a coordinator delegates by default … **You doing the work is the failure mode**" | live since `5364f6e`, **2026-07-10 20:58** | **AT HEAD. Governs everything from 07-11 on.** |
| **C5** (doctrine 1) "If a serial chunk is more than a few minutes of work and you are **not uniquely positioned**…" | live since the same commit | **AT HEAD. Governs everything from 07-11 on.** |
| **C2** (:13-16 "manage your top-level agents"), **C3** (:21-23 "start with one"), **C4** (:24-26 **the leaf parenthetical**), **C6** (:31 "Mine before you spawn") | **UNCOMMITTED WORKING-TREE TEXT** — written 2026-07-12 by the operator's own children (`onboarding-split`, `operator-structure-scout`) | **NOT AT HEAD. Postdates every lapse in the corpus.** |

Two consequences:

1. **The 2026-07-09 and 07-10 items cannot be doctrine failures at all** — on
   day 1 (`c9ecf63`) SKILL.md was 27 lines with *zero* delegation doctrine. The
   honest doctrine-failure corpus starts **2026-07-11**.
2. **The leaf-loophole question I was asked to answer is void.** C4 is text the
   operator wrote *yesterday*, after every lapse. It could not have rationalized
   any of them. (Its reasoning is still acquittable on the merits — see §3a — but
   the question was never live.) **CORRECTED.**

---

## 1. The census, re-derived

**Counting rule** (v1's was incoherent — it summed tasks, arms, agents, and
subtrees as if they were one unit; iwa-red was right and I do not contest it):

A **work unit** = one *producible artifact* — code, doc, measurement, or a
system repair — that a child could have been briefed to produce.

**NOT work units** (the coordinator's own job, by SKILL.md:10-11 which names
them): verification by reading (~15 "verified myself / 65 OK my run" lines),
briefs, dispatch/verdict/journal entries, PR bodies, the desk page, `gh` and
`git` mechanics.

### INLINE, doctrine-live window only (2026-07-11 →)

| # | Line | What | Quote (VERIFIED) | Contested? |
|---|---|---|---|---|
| **I1** | L35 | **Authored `docs/design/SPAN.md`** — full design doc | "Wrote docs/design/SPAN.md **myself** (judgment-heavy design; delegation weighed, declined — **context all here**)" | No. Unambiguous. |
| **I2** | L41 | **Amended SPAN.md** — §3d' delegation ladder + falsifier 1' | "**Amended SPAN.md myself**: §3d' delegation ladder…" | No. |
| **I3** | L43 | **Amended SPAN.md** again (1' outcome) | "SPAN.md amended (1' outcome)" | Marginal (small). |
| **I4** | L78 | **Drafted the multi-harness choice-doctrine inline** | "I drafted choice-doctrine inline — **against my own delegation doctrine**" | No — **conceded by the operator itself, and caught by the HUMAN, not by any clause.** |
| **I5** | L33 | **Drafted v1.0.0 release notes** | "Delegation weighed and declined for release drafting (**cheap-task math**)" | Marginal. |
| **I7** | L49 | **Wrote the operator-capabilities proposal (P1–P8)**, then spawned children *only to red-team it* | "Proposal written: `.swarm/briefs/operator-capabilities-proposal.md` (P1 restore, P2 dispatch entries, …)" | No — **the sharpest item: the operator delegated the CRITICISM of its own work while keeping the WORK.** |
| **I8** | L74 | **Codex clean reinstall + surgical config rebuild** (brew reinstall, auth restore, config rebuilt) | "0.142.5 → 0.144.1 (brew cask reinstall) … Rebuilt config surgically…" | No — **remediating, by hand, the findings of an audit (`codex-audit`) it had ALREADY delegated.** |
| **I9** | L76 | **Ran 3 live hook probes** on codex 0.144.1 | "All 3 audit-checklist hook probes now VERIFIED on 0.144.1 … sentinel round-trip" | No. |
| **I10** | L114 | **Drafted the grants-entry template** | "Drafted grants-entry template (`.swarm/briefs/grants-entry-DRAFT.md`)" | Marginal (brief-adjacent). |
| **I13** | L199-200 | **Debugged the usage-limit freeze** — pane reads, doorbell experiment, 3-bug diagnosis | "**Operator asked to debug** post-usage-limit state… ROOT CAUSE (pane-read confirmed)…" | **YES — directly human-requested. See §5.** |
| **I15** | L203-206 | **Started the `<model>`-in-ps edit inline**, then **self-caught and reverted** | "Caught myself doing inline work … Reverted it … Then delegated three streams instead" | **The origin event. An inline START, a doctrine-compliant FINISH.** |

**DROPPED from v1** (iwa-red's numerator challenge, accepted): ~~I6~~ (rebase —
`git` mechanics = glue, excluded by my own §0), ~~I11~~ (workspace root-cause —
reading one function to know what to brief *is* judgment, which SKILL.md:10-11
reserves to the coordinator **by name**), ~~I12~~ (applying a delegated child's
approved edit — the merge path the operator's own PR flow mandates),
~~I14~~ (fabricated; = I15, self-corrected).

### DELEGATED, same window

Counted consistently, as **work units the operator dispatched**, not names typed:
hardener Tasks 4,5,7,8,10,11,12,13,14 (9) · field-tester probes: doctrine
before/after, flood baseline, heavy flood, reuse, two-hand, suggestion-UI,
workspace repro+verify, FLEET v3, F1/F2 root-session (9) · updater cycles (~8) ·
scout/one-shot dispatches: harness-scout, decision-scout, decision-wiring,
proxy-scout, pipeline-scout, hook-scout, patterns-contractor, inbox-scout,
structure-scout, fleet-scout, fleet-eval, onboarding-scout, onboarding-split,
operator-structure-scout, opencode-plugin-scout, org-review-scout, skill-writer,
codex-audit, trigger-scout, ps-model, model-fit, inline-work-audit (22).

**≈ 48 delegated work units.**

---

## 2. The rate — with its honest error bar

| Basis | Inline | Total | Rate |
|---|---|---|---|
| **Strict** — only the uncontested items (I1, I2, I4, I7, I8, I9) | 6 | 54 | **≈ 11 %** |
| **Central** — + the marginals (I3, I5, I10) and the self-caught start (I15) | 10 | 58 | **≈ 17 %** |
| **Inclusive** — + the human-requested debug (I13) | 11 | 59 | **≈ 19 %** |
| *v1's headline (WITHDRAWN)* | *14* | *58* | *~~24.1 %~~* |

**The honest number is a band: roughly 1 in 6 to 1 in 9 work units, the operator
did itself — call it 11–19%, not 24%.** VERIFIED where the items are quoted;
the band exists because the unit is genuinely fuzzy at the margins, and I will
not launder that into a single decimal. v1's 24.1% was an artifact of an unstable
counting unit plus one fabricated item. **CORRECTED.**

**Is it a pattern or a one-off? A PATTERN — and this survives every correction.**
Not because of the rate, but because of *what* is in the list. Four items are
unrescuable by any reading of the doctrine:

- **I1/I2** — a multi-section design document (`SPAN.md`: attention caps,
  rebalancing model, delegation ladder, falsifier register), authored **and twice
  amended** by the operator's own hand. Not glue. Not "a few minutes." Not
  requested-by-human.
- **I4** — conceded in the operator's own words as a doctrine violation, and
  **caught by the human, not by any clause**.
- **I7** — the operator wrote an 8-proposal document and then spawned children
  **only to review it**. It delegated the *judgment* and kept the *work* — the
  exact inversion of SKILL.md:10-11.
- **I8/I9** — hand-remediating an audit it had already delegated.

And it **recurred after correction**: I4 was human-caught on 2026-07-11 and
memorized ("Feedback saved to memory", L78) — and I8, I9, I10, I13, I15 all came
after. **VERIFIED. The correction did not change the behavior.** That is what
makes it a pattern and not a slip.

---

## 3. Clause attribution — only against doctrine that existed

Live at the time of every item below: **C1** (SKILL.md:10-11) and **C5**
(doctrine 1, :16-18 at HEAD / :42-44 in the working tree).

| # | Clause | The rationalization the journal actually records |
|---|---|---|
| I1, I2, I3 | **C5** | "**context all here**" → C5's `not uniquely positioned` exemption, claimed. C5 *hands this over by name.* |
| I5 | **C5** | "**cheap-task math**" → C5's `more than a few minutes` threshold, read as a permission below the line. |
| I7, I10 | **C1** | Authorship reframed as "judgment"/"glue" — C1's own reserved categories, whose boundary is undefined and therefore absorbs drafting. |
| I4 | **none** | No clause fired. The **human** fired. |
| I8, I9, I13, I15 | **none** | No rationalization is journaled. The operator simply did it. |

**The load-bearing text is C5's second sentence** —
`git show HEAD:skill/SKILL.md:16-18`:

> "If a serial chunk is **more than a few minutes of work** and you are **not
> uniquely positioned** to do it, spawn for it too."

It is **the only clause the operator ever quotes at itself while declining to
delegate**, and it is quoted in both of its exemptions ("cheap-task math",
"context all here"). VERIFIED.

### 3a. Is the leaf-loophole (SKILL.md:24-26) the culprit? **NO — and the question is void.**

Two independent reasons, either sufficient:

1. **It did not exist.** C4 is uncommitted working-tree text written 2026-07-12
   by the operator's own children. It postdates every lapse. **VERIFIED** (`git
   show HEAD:skill/SKILL.md` has no match for "independent leaves").
2. **Even if it had existed, it cannot do this work.** Read it: *"A few
   independent leaves with nothing to reconcile: **spawn them directly**, and say
   so."* **Its escape hatch is an escape INTO spawning.** It licenses skipping a
   *coordinator layer*; it cannot license skipping *delegation*. Zero of the
   inline items have that shape — none is a case of spawning leaves where a
   coordinator was warranted. **VERIFIED** by scanning the census.

The operator's hypothesis was a reasonable guess about text it had just written.
It is wrong, and the real culprit is one paragraph earlier, in the delegation
doctrine's own first item.

---

## 4. The SEAM — restated correctly after the red team

v1 said: *the doctrine is silent at task-arrives-time.* iwa-red showed that is
**imprecise in a way that matters**, and I accept the reframe:

> **It is not silence. It is a licence.**

Three facts, each VERIFIED:

1. **C1 (:10-11) — "You doing the work is the failure mode" — carries no
   time-index and no threshold.** It is a *standing predicate*, and a rule that
   always holds holds at arrival too. So the seat is not doctrinally naked at
   task-arrival. **v1 walked past its own C1 to declare a void. CORRECTED.**
2. **But C1 never converts into an operative fork.** Nothing in SKILL.md turns
   "delegation is the default" into a *question the seat must answer when a task
   lands*. The only landing-time verb in the file is `Claim mail, then act`
   (working tree :99) — and there is **no delegate-vs-do branch inside it**.
3. **And C5 affirmatively grants the exemption.** "More than a few minutes /
   uniquely positioned" is *a threshold test that a small arriving task passes
   trivially* — and it is exactly the population of tasks at issue. A small task
   landing on a warm seat is *always* under the minutes line and the seat is
   *always* "uniquely positioned" (it has the context; it's the one holding the
   file).

**So the mechanism is: an untimed stance that never becomes a test, plus an
explicit small-task exemption that the seat then cites at itself.** REASONED,
grounded in the fact that C5's two exemptions are the *only* rationalizations the
journal ever records.

### 4a. The signature — iwa-red's finding, which beats mine. VERIFIED.

v1 claimed the recurrence signature was *"every inline unit arrived already small
and already singular."* **That is false of exactly the items that survive.**
SPAN.md was not small. The P1–P8 proposal was not small. My signature described
the items I should have dropped. **CORRECTED.**

The real signature, which I verified independently after iwa-red named it:

> **The operator delegates code, measurement, research, and review. It keeps the
> writing of its own doctrine.**

VERIFIED by counting the record: **of the 12 design documents in this corpus, the
operator delegated the authoring of 11** — `DECISIONS`, `DECISION-WIRING`,
`FLEET`, `HARNESS`, `HOOK-WIRING`, `INDUSTRY-PATTERNS`, `ONBOARDING`,
`OPENCODE-PLUGIN`, `PIPELINE-WIRING`, `PROXY-WIRING`, `STRUCTURE`. It kept
**one**: `SPAN.md` (L35) — *the doctrine about its own attention* — and then
amended it by hand twice more (L41, L43). Add the two adjacent items and the set
closes: the **operator-capabilities proposal** (I7, L49 — its own seat's powers,
written inline, children spawned only to shoot at it) and the **choice-doctrine
draft** (I4, L78 — its own delegation rules, human-caught).

**Every uncontested inline item is the operator writing the rules that govern the
operator.** That is not a task-size effect. It is a subject-matter effect.

And it explains why C5's exemption is the load-bearer rather than a gap: *"context
all here"* (L35) is a **universal solvent** — it is true of anything the seat has
just been discussing, so if it licenses authoring a design doc it licenses
everything — and the seat will **always** feel uniquely positioned to author its
own doctrine. **That feeling is the failure mode, and C5 ratifies it.**

**Why the same doctrine works below the operator and fails at it** — this is the
structural half, and it is VERIFIED:

- A spawned child's duties are **re-injected into its context on every spawn and
  every restore** (`spawn_header` in `bin/swarm`; the operator itself found this,
  L175: *"doctrine reached every spawned agent (spawn_header) but skipped the
  human's root session (only sees SKILL.md)"*).
- Children consequently **do** delegate on arrival, unprompted:
  `decision-scout` spawned 4 children and ran its own red team with **"zero
  prompting"** (L90); `harness-scout` spawned 3 (L81).
- The operator reads SKILL.md **once, at trigger time.** Same model, same words,
  different **arrival surface**.

And the repo already confesses the neighborhood, in its own untracked reference
file — `skill/references/COORDINATING.md`, closing section, *"The edge this does
not cover"*:

> "All of this governs what happens **once `/swarm` has fired.** A session that
> *should* have fired it and never did … **is out of scope, and nothing in this
> repo re-evaluates it.** Stated so the next reader does not mistake it for
> solved."

That is written about the *trigger* gap, but it is the same shape one level in:
**everything the doctrine says is addressed to shaping-time. Nothing re-evaluates
at arrival-time.**

### 4b. Does doctrine need a task-arrives rule?

**A qualified yes — and the qualification is the whole finding.**

**Yes**, in that nothing in the doctrine fires when a task lands on a standing
seat: C1 is a stance that never becomes a test, and `Claim mail, then act` has no
delegate-vs-do branch in it.

**But an arrival rule alone would not have prevented a single one of the surviving
lapses**, and this is where I'd resist any gap-filling instinct:

1. **C5's exemption survives it.** "Not uniquely positioned" is the clause the
   operator actually quotes at itself. An arrival rule that says *"ask whether to
   delegate"* is answered by C5 saying *"you're uniquely positioned — proceed."*
   **The exemption needs a test, or it needs to go. The gap is downstream of the
   licence.**
2. **The surviving lapses were not arrival-shaped.** SPAN.md and P1–P8 were not
   small tasks that snuck in under a threshold; they were substantial documents
   the operator *chose* to author because they were about the operator. §4a.

So the honest diagnosis is **two findings, not one**: a *missing fork at arrival*
(real, structural, explains I5/I10/I15) and a **subject-matter capture** — the
seat keeps its own doctrine (real, explains I1/I2/I4/I7, the items that survive
every attack). Only the second explains why a human correction on 2026-07-11 did
not change the behavior.

(Fix wording is out of scope by brief. I name the constraints, not the text.)

---

## 5. The one place I REBUT iwa-red

iwa-red argues **I13** (the usage-limit debug) should not count, because
SKILL.md:13-14 says the operator is "the human's own tooling, acting on their
behalf" — so a direct human request is the seat performing its function, and to
call it a lapse I'd need to argue the operator should have *refused the human*.

**I partly reject this, and I hold I13 in the census with a flag.**

- The clause iwa-red invokes (C2, :13-14) is **uncommitted working-tree text** —
  by iwa-red's own KILL 2, it cannot be used to *excuse* an item any more than it
  could be used to *convict* one. iwa-red applied its own kill asymmetrically.
- "The human asked me to do X" and "the human asked me to *personally* do X" are
  different sentences. The operator's *entire* corpus is human-requested — every
  scout, every hardener task, every eval. **If a human request licensed inline
  work, the delegation doctrine would have no domain at all.** The whole point of
  the seat is that the human hands it goals and the seat decides the shape.
- What the operator did with I13 (pane reads, a doorbell recovery experiment, a
  three-bug diagnosis, ~2h of frozen-subtree forensics) is a **research task with
  a producible artifact** — precisely the shape it delegates to `field-tester`
  nine other times.

**But iwa-red's underlying point stands and I fold it:** the report must not
pretend every inline item is a *mistake*. So I13 is in the **Inclusive** row of
§2 and out of the **Strict** row, and the rate is a band. The reader can see
exactly what the disagreement costs: **two percentage points.**

---

## 6. What v1 got wrong (kept in the record, not scrubbed)

| v1 claim | Status |
|---|---|
| "I14: operator edited bin/swarm + tests inline, **unjournaled**, `git diff` VERIFIED" | **FALSE. Fabricated.** I never ran the diff; I inherited it from my brief and stamped it verified. The operator had reverted it and journaled it. **The single most rhetorically loaded claim in v1 was its only unchecked one.** |
| "Rate = 24.1%" | **WITHDRAWN.** Unstable unit; padded numerator. Honest band: **11–19%**. |
| "C4/the leaf loophole is not the culprit *(analysed as live doctrine)*" | **Right answer, dead question.** C4 postdates every lapse. |
| "C2/C3/C6 failed to prevent items I1–I13" | **VOID.** Those clauses did not exist on those dates. |
| "The doctrine is **silent** at task-arrives-time" | **REFRAMED:** not silent — **licensed.** C1 speaks but never becomes a test; C5 grants the exemption. |
| "§0 exclusion of verification-by-reading" | **SURVIVED.** iwa-red tried to break it and could not. |
| "The pattern is real and recurring" | **SURVIVED.** I1, I2, I4, I7, I8, I9 are unrescuable; the recurrence after human correction is VERIFIED. |

The method failure is worth naming plainly, because it is the same failure the
audit is about: **I was handed a premise by my parent and did not verify it — the
delegated-work analogue of the operator being handed a task and not delegating
it. The instinct in both cases is "I already know this; the check is not worth
the minute."** The red team was the only thing that caught it, exactly as the
human was the only thing that caught I4.
