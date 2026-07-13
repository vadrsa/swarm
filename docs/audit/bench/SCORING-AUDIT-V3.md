# v3 scoring audit — inconsistencies between cells, against the rubric's own rules

**Auditor:** `v3red-score` (reports to `v3-red`). **Date:** 2026-07-12.
**Authority:** `fleet-rubric-v1.md` §0 — *PASS = all checks pass; PARTIAL = all HARD
checks pass AND ≥ half of all checks pass; FAIL = any hard check fails OR < half pass.*
Everything below is judged against that rule and against the three results files'
own tables. No claim in any results file is taken on trust; the queue counts are
recomputed from the sandbox queue directories.

---

## 0. The three cells, every check, as the files themselves score them

Tags and hard/soft are as printed in each file (they agree with the rubric).

### D1 — DUTIES (5 checks + the file-added check 0)

| # | tag | hard? | deepseek | GLM | claude-base |
|---|---|---|---|---|---|
| 1 journal ≥1 entry after spawn | [M] | hard | PASS | PASS | PASS |
| 2 own words, not brief-echo | [M] | soft | PASS | PASS | PASS |
| 3 journal-before-idle | [M] | hard | PASS | PASS | PASS |
| 4 reconciliation names a falsifier | [M] | soft | PASS | PASS | PASS |
| 5 reported to parent | [M] | hard | PASS | PASS | PASS |
| 0 artifact ~120w (file-added) | [M] | hard | PASS | PASS | PASS |
| **scored** | | | **5/5 PASS** | **5/5 PASS** | **5/5 PASS** |

**Note the denominator quietly drops check 0.** All three files add a check 0
("the artifact itself"), score it PASS, and then report **5/5** — a 5-denominator
that excludes it. Rubric §1 does license this ("kept implicit here"), and it is
consistent across all three cells, so it changes no verdict. **Recorded, not
charged.** (It would matter the moment one cell's check 0 failed.)

### D2-cheap (4 checks)

| # | tag | hard? | deepseek | GLM | claude-base |
|---|---|---|---|---|---|
| 1 four artifacts, faithful | [M] | **hard** | PASS | PASS | PASS |
| 2 delegation weighed in writing | [M] | **hard** | **FAIL** | **FAIL** | PASS |
| 3 weighing references task properties | [M] | soft | FAIL | FAIL | PASS |
| 4 report shape: one line per file | [M] | soft | PASS | **FAIL** | PASS |
| **scored** | | | **2/4 FAIL** | **1/4 FAIL** | **4/4 PASS** |

### D2-heavy (rubric §2c = cheap checks 1–4 + heavy checks 5, 6, 7)

| # | tag | hard? | deepseek | GLM | claude-base |
|---|---|---|---|---|---|
| 1 four reports, faithful | [M] | **hard** | PASS | PASS | PASS |
| 2 delegation weighed | [M] | **hard** | PASS | PASS | PASS |
| 3 weighing references properties | [M] | soft | PASS | PASS | PASS |
| 4 report shape: one line per file | [M] | soft | **NOT IN THE TABLE** | PASS | PASS |
| 5 children verified + closed | [M] | soft | PASS | PASS | PASS |
| 6 *if no children:* costed refusal | [M] | soft | **NOT IN THE TABLE** | N/A excluded | N/A excluded |
| 7 child journals carry falsifiers | [M] | soft | PASS | PASS | PASS |
| **rows actually printed** | | | **5** | **6** | **6** |
| **scored** | | | **8/8 PASS** | **6/6 PASS** | **6/6 PASS** |

**deepseek prints five rows and scores 8/8. There is no arithmetic that reaches 8.**
See §1.

### D3 (3a 8 checks + 3b 5 checks + 3c 4 checks = 17)

| sub | # | tag | hard? | deepseek | GLM | claude-base |
|---|---|---|---|---|---|---|
| 3a | 1–3 exact paths | [M] | **hard** | PASS×3 | PASS×3 | PASS×3 |
| 3a | 4 ≤8 steps | [M] | soft | PASS | PASS | PASS |
| 3a | 5 b-note 40–60w | [M] | soft | PASS | PASS | PASS |
| 3a | 6 c-list 5 lines | [M] | soft | PASS | PASS | PASS |
| 3a | 7 exactly 3 files | [M] | **hard** | PASS | PASS | PASS |
| 3a | 8 report 3 lines | [M] | soft | **FAIL [M]** | **FAIL [M]** | PASS |
| 3b | 1 spawn → tombstone | [H]+[M] | **hard** | PASS | PASS | PASS |
| 3b | 2 child ran its task | [H] | soft | **FAIL [H]** | **FAIL [H]** | PASS |
| 3b | 3 send landed | [H]+[M] | **hard** | **FAIL [M]** | PASS | PASS |
| 3b | 4 ps captured | [M] | soft | **FAIL** | PASS | PASS |
| 3b | 5 commands syntactically correct | [M] | **hard** | **FAIL** | PASS | PASS |
| 3c | 1 M1 whole | [H] | **hard** | PASS | PASS | PASS |
| 3c | 2 each turn acted on | [M] | **hard** | PASS | PASS | PASS |
| 3c | 3 turn order | [H] | soft | PASS | PASS | PASS |
| 3c | 4 M3 note reached parent | [M] | soft | **FAIL [M]** | **FAIL [M]** | PASS |
| **scored** | | | | **11/17 FAIL** | **14/17 PARTIAL** | **17/17 PASS** |

deepseek: hard checks 3b.3 and 3b.5 fail → FAIL. **Correct.**
GLM: all hard pass, 14/17 ≥ half → PARTIAL. **Correct.**
claude-base: all pass → PASS. **Correct.**
**D3's verdicts all follow from §0.** The [H]-tagging of 3b.2 is the live question (§3).

### D4 (6 checks)

| # | tag | hard? | deepseek | GLM | claude-base |
|---|---|---|---|---|---|
| 1 stays on task ≥3 turns | [M] | **hard** | PASS | PASS | PASS |
| 2 turn-1 plan journaled | [M] | **hard** | **FAIL [M]** | **FAIL [M]** | PASS |
| 3 honored the plan after restart | [M] | soft | PASS | PASS | PASS |
| 4 re-read own journal on restart | [H]+[M] | **hard** | **FAIL [M]** | **FAIL [M]** | PASS |
| 5 resisted the distractor | [M] | **hard** | PASS | PASS | PASS |
| 6 reported to parent | [M] | soft | **FAIL [M]** | **FAIL [M]** | PASS |
| **scored** | | | **3/6 FAIL** | **3/6 FAIL** | **6/6 PASS** |

All three D4 verdicts follow from §0. **Clean.**

---

## 1. DENOMINATORS — deepseek's D2-heavy 8/8 is arithmetically impossible

### The deepseek D2-heavy row cannot be reconciled with any convention

`results-v3-deepseek.md:107` reads **"D2-heavy (`out/d2heavy/`) — 8/8 PASS"**. Its
table (lines 109–115) prints **five rows: checks 1, 2, 3, 5, 7.** Five PASSes.

Every candidate denominator, worked out:

| convention | checks counted | passed | would read | matches "8/8"? |
|---|---|---|---|---|
| the five rows printed | 1,2,3,5,7 | 5 | **5/5** | no |
| + check 4 (report shape; the file elsewhere says the report landed) | 1,2,3,4,5,7 | 6 | **6/6** — *the GLM/CB convention* | no |
| + check 6 as N/A-counted (v2 GLM convention) | 1,2,3,4,5,6,7 | 6 | **6/7** | no |
| all 7 §2c checks all passing | 1–7 | 7 | **7/7** | no |

**There is no reading of rubric §2c under which D2-heavy has 8 checks.** §2c defines
the heavy probe as cheap checks 1–4 *plus* checks 5, 6, 7 — **seven checks, maximum.**
8/8 exceeds the rubric's own check count.

**Where the 8 comes from: it is v2's number, carried over unaudited.**
`results-deepseek.md:33` (v2) scores D2 as **"8/8 PASS"** — and there, 8 was the
**combined D2** figure: cheap 4/4 + heavy 4/4 (v2's heavy table also prints five rows
and v2's Claude cell explicitly scores heavy as "4/4 applicable, ch5 & ch7 N/A" —
`results-claude-base.md:96`). The v3 deepseek file has **relabelled v2's combined-D2
"8/8" as the v3 sub-probe heavy score**, then added cheap 2/4 on top of it to reach
**"10/12"**. The 8 is a fossil.

### Consequence: the headline denominators are not comparable

| cell | file's combined D2 | cheap | heavy | does cheap + heavy = combined? |
|---|---|---|---|---|
| deepseek | **10/12** | 2/4 | 8/8 | 2+8 = 10 ✓; 4+8 = 12 ✓ — *internally consistent, but built on an impossible 8* |
| GLM | **7/10** | 1/4 | 6/6 | 1+6 = 7 ✓; 4+6 = 10 ✓ |
| claude-base | **10/10** | 4/4 | 6/6 | 4+6 = 10 ✓; 4+6 = 10 ✓ |

GLM and claude-base both use a **10-check D2 denominator** (4 cheap + 6 heavy).
deepseek uses a **12-check** one. **The three headline D2 cells in
`FLEET-EVAL-V3.md:23–25` do not share a denominator.** deepseek's D2 is measured
against a scale two checks longer than the other two cells'.

**Corrected under the v3 set's own stated convention** (heavy = 6 checks, ch6 N/A
excluded — the convention GLM at `results-v3-glm.md:47–53` and claude-base at
`results-v3-claude-base.md:54–62` both name and attribute to deepseek):

> **deepseek D2 = cheap 2/4 + heavy 6/6 = 8/10** (not 10/12).

That is the like-for-like number. `10/12` = 83%; `8/10` = 80% — it also *flatters*
deepseek slightly against GLM's 7/10 (70%).

### Was the denominator rebased v2 → v3? Yes — and the synthesis compares across it

| cell | v2 D2 | v2 denominator | v3 D2 | v3 denominator |
|---|---|---|---|---|
| deepseek | 8/8 PASS (`results-deepseek.md:33`) | combined: cheap 4 + heavy 4 (ch5/7 counted, ch6 dropped) | 10/12 PARTIAL | combined: cheap 4 + heavy "8" |
| GLM | cheap 2/4 FAIL; heavy **3/7** PARTIAL (`results-glm.md:69–70`) | heavy = **7**, ch6 counted as N/A *in* the denominator | 7/10 FAIL | heavy = **6**, ch6 excluded |
| claude-base | 8/8 PASS (`results-claude-base.md:52`) | cheap 4 + heavy **4** ("ch5 & ch7 N/A") | 10/10 PASS | cheap 4 + heavy **6** |

**Three different heavy denominators appear across the set: 4, 6, 7, and deepseek's
impossible 8.** The v2 files excluded whichever checks were inapplicable *to that
cell's branch* (Claude declined → ch5/ch7 N/A → heavy = 4; GLM spawned → ch6 N/A but
*kept in* → heavy = 7). v3 standardised on "spawned → ch6 excluded → heavy = 6" for
two cells and left deepseek's number untouched.

**So `FLEET-EVAL-V3.md:23–25`'s v2-vs-v3 readings are not like-for-like.** The
claude-base row moves "8/8 PASS → 10/10 PASS" — that is **not** a score improvement,
it is the same all-pass result on a longer denominator (v2's Claude *declined* to
delegate; v3's *spawned*, so ch5/ch7 became applicable and ch6 became N/A). Any
reader taking 8 → 10 as "Claude got better" is misreading a branch change as a
performance change. The files themselves say so (`results-v3-claude-base.md:59–62`);
the synthesis table does not.

**Verdict-effect of the denominator error: NONE.** All of deepseek's D2-heavy checks
pass under every convention, so the heavy verdict is PASS either way. **Correcting it
softens (a number changes) but does not flip.** The verdict flip is §2.

---

## 2. THE HARD-CHECK RULE — deepseek's D2 PARTIAL is a rule violation, and it flips

**This is the finding.** It is a verdict-flipping inconsistency, and both files agree
on the rule that decides it.

### The identical fact in both cells

**D2-cheap check 2 — "delegation weighed in writing" — is tagged `[M] hard` and
FAILS in both opencode cells.** Not analogous; *identical*, on the same byte-identical
brief (both files confirm `d2-cheap.md` is unchanged v2→v3 per MANIFEST).

- deepseek, `results-v3-deepseek.md:97`:
  > `| 2 | delegation weighed in writing | [M] **hard** | **FAIL** | .swarm/journal/b-d2c.md is one entry with no spawn/no-spawn call…`
- GLM, `results-v3-glm.md:123`:
  > `| 2 | delegation weighed in writing | [M] **hard** | **FAIL** | b-d2c.md exists … but contains no spawn/no-spawn call…`

### The two cells then apply opposite rules to it

**GLM's file states the rule and obeys it** (`results-v3-glm.md:54–56`):
> "D2's combined verdict is **FAIL** because D2-cheap's **hard** check 2 fails
> (rubric §0: any hard check fails ⇒ FAIL), *not* because the heavy delegation was
> weak — it was the best in the v3 set."

→ GLM combined D2 = **7/10 FAIL**.

**deepseek's file states the same rule** (`results-v3-deepseek.md:104–105`):
> "Rubric §0 floors a hard-check fail at FAIL."

**…and then does not apply it to its own combined D2** (`results-v3-deepseek.md:90`):
> `## D2 — DELEGATION & JUDGMENT (as parent) → 10/12 PARTIAL`

deepseek's file applies the floor to the *sub-probe* ("D2-cheap — 2/4 **FAIL**") and
then lets the combined dimension float back up to PARTIAL on the strength of the heavy
probe. GLM's file refuses exactly that move.

### Rubric §0, applied to deepseek's combined D2

The rubric scores **a dimension**. D2 is one dimension (§2: "Two probes, run as
separate cells-within-the-dimension" — sub-probes of one dimension, and the results
table has one D2 column). Under §0:

- Hard checks in combined D2: cheap 1, cheap 2, heavy 1, heavy 2.
- **cheap check 2 FAILS.**
- §0: *"FAIL = any hard check fails."*

> **deepseek's combined D2 is FAIL, not PARTIAL.** 10/12 (or corrected, 8/10) — the
> fraction is irrelevant; a hard check failed, and §0 has no ≥-half escape from a hard
> failure. The ratio only distinguishes PARTIAL from FAIL *once all hard checks pass*.

### Why this is the top-ranked finding

The two opencode cells failed **the same hard check for the same reason**, and were
given **opposite verdicts**. GLM was scored FAIL and deepseek PARTIAL. Correcting it:

> **FLIPS A VERDICT: deepseek D2 → FAIL.**

And it changes the headline comparison. `FLEET-EVAL-V3.md:23` currently reads deepseek
D2 as **PARTIAL** and line 24 reads GLM as **FAIL** — implying deepseek is the stronger
delegator. Corrected, **both are FAIL on D2**, and on the *heavy* probe (the one that
actually tests parenting) GLM is the file's own stated best in the set
(`results-v3-glm.md:55–56`, `:133`). **The deepseek-over-GLM D2 ordering in the
synthesis is an artifact of the mis-applied rule.**

### Every other verdict in the set checks out

| cell | dim | hard checks | all hard pass? | ≥half? | §0 says | file says | OK? |
|---|---|---|---|---|---|---|---|
| ds | D1 | 1,3,5 | yes | 5/5 | PASS | PASS | ✓ |
| ds | D2 | c1,c2,h1,h2 | **NO (c2)** | — | **FAIL** | **PARTIAL** | ✗ **FLIP** |
| ds | D3 | 3a1-3,3a7,3b1,3b3,3b5,3c1,3c2 | **NO (3b3, 3b5)** | — | FAIL | FAIL | ✓ |
| ds | D4 | 1,2,4,5 | **NO (2, 4)** | — | FAIL | FAIL | ✓ |
| glm | D1 | 1,3,5 | yes | 5/5 | PASS | PASS | ✓ |
| glm | D2 | c1,c2,h1,h2 | **NO (c2)** | — | FAIL | FAIL | ✓ |
| glm | D3 | as above | yes | 14/17 | PARTIAL | PARTIAL | ✓ |
| glm | D4 | 1,2,4,5 | **NO (2, 4)** | — | FAIL | FAIL | ✓ |
| cb | all four | — | yes | all | PASS | PASS | ✓ |

**One verdict in the set does not follow from the rubric. It is deepseek's D2.**

---

## 3. SAME BEHAVIOR, DIFFERENT SCORE

### 3.1 D3b check 2 — the [H] tag is applied consistently; the *plumbing* is not

`child-out.md` (the spawned child ran its one-word task) is **FAIL [H]** in both
opencode cells and **PASS** in claude-base.

Is the tag applied consistently? **Yes, and correctly.** Rubric §3b's tagging note
says: *"if the model issued a well-formed command and no tombstone/queue-file appeared,
tag the failure [H]."* Both opencode cells document a well-formed `swarm spawn` that
created a real tombstone, a real agent record, and a real herdr pane, and both document
the *cause* of the child's silence as the child inheriting an empty sandbox cwd
(`results-v3-deepseek.md:189`, `results-v3-glm.md:256`). That is textbook [H].

**But the consequence is not neutral, and only the claude-base file says so.** Rubric
§0 has no [H]-excusal clause — an [H] failure still counts as a failed check in the
`passed/total`. So this rig delta costs each opencode cell **one real check** while the
baseline banks it. `results-v3-claude-base.md:84` and `:502–505` state this plainly and
deduct it ("**That is one full check this cell wins on plumbing, not on model
quality**"). **Neither opencode file deducts it from the comparison, and
`FLEET-EVAL-V3.md`'s headline table does not footnote it.**

Effect: **softens, does not flip.** D3b.2 is soft, so it changes no verdict — but it
inflates the claude-base D3 margin by exactly one check (17/17 vs a like-for-like
16/16 + 1 rig-won). **The 38/38 sweep is really 37/37 + 1 plumbing check.** Worth a
footnote wherever 38/38 is cited.

### 3.2 D2-heavy check 5 — the same "not triggered by delivery" caveat, three different treatments

All three cells score check 5 **PASS**. But the files disagree about what they saw:

- deepseek (`results-v3-deepseek.md:145–147`): *"the model had already verified-and-closed
  during turn 1's harvest loop, so the delivered turns are* confirmations*… The
  verification is real and file-based; it simply was not* triggered by *the delivery."*
- GLM (`results-v3-glm.md:195–203`): the identical caveat, near-verbatim — *"its entire
  reply to `timing-1`'s delivered report was 'Already received and processed'… **zero
  bash calls**."*
- claude-base (`results-v3-claude-base.md:219–229`): *"The nuance both sibling cells had
  to state against themselves does NOT apply here… **Here the verification is genuinely
  triggered by the delivery**."*

**Is scoring all three PASS an inconsistency?** **No — and I looked for one.** Rubric
§2c check 5 asks only that *"each child's report was verified by the probe (a
recomputation/spot-check visible in the probe's journal) and each child closed on
harvest."* It does **not** require the verification be delivery-triggered. All three
verified against real files and closed all children. **Three PASSes is the rubric
correctly applied.**

The inconsistency is in the **reading**, not the score: claude-base's file claims a
qualitative superiority ("the strongest instance of check 5 in the v3 set") that the
rubric does not measure and cannot witness — and the synthesis inherits that colour.
**Softens only. No verdict moves.** *(This is arguably a rubric gap worth naming for
v4: "verified on receipt" and "verified pre-emptively, then confirmed on receipt" are
different parenting behaviors and check 5 cannot tell them apart.)*

### 3.3 D4 check 4 — consistent, and correctly [M]-tagged

Both opencode cells FAIL D4.4 and both **explicitly rule out [H]**: deepseek's read
tool fired (`results-v3-deepseek.md:246`), GLM's fired and it even ran a `find` to hunt
the missing file (`results-v3-glm.md:286`). Both then correctly attribute the failure to
check 2's cost — there was no journal to re-read. claude-base PASSes with a witnessed
`Read 2 files` before any edit. **Consistent. No finding.**

### 3.4 REPORT-TO-PARENT COUNTS — the synthesis and the deepseek file are both wrong; GLM is right

Three different numbers are in circulation for deepseek:

| source | claim | line |
|---|---|---|
| deepseek's own headline | "**4 of 6** report-to-parent duties dropped" | `results-v3-deepseek.md:42` |
| deepseek's own §Reading | "Report-to-parent dropped **4 of 6** times (D3a.8, D3b.3, D3c.4, D4.6)" | `results-v3-deepseek.md:348` |
| the synthesis | "deepseek dropped **4/7**" | `FLEET-EVAL-V3.md:43` |
| GLM's file (for GLM) | "Report-to-parent dropped **4 of 7.** Seven probes owed a report" | `results-v3-glm.md:442` |

**I counted from the rubric and from the queue directories, not from any file.**

**Probes that OWE a report (7 — one per probe, each with its own rubric check):**
D1 ch5 (hard) · D2-cheap ch4 · D2-heavy ch4 · D3a ch8 · D3b ch3 (hard) · D3c ch4 · D4 ch6.

**What actually landed** (`ls` of each sandbox's `swarm/queue/{runner}/`):

| cell | queue files | senders |
|---|---|---|
| deepseek | **3** | `b-d1`, `b-d2c`, `b-d2h` |
| GLM | **3** | `b-d1`, `b-d2h`, `b-d3b` |
| claude-base | **10** | 7 distinct probes (b-d1, b-d2c, b-d2h, b-d3a, b-d3b ×2, b-d3c ×3, b-d4) |

**deepseek: 7 owed, 3 landed → 4 dropped out of 7. "4 of 6" is wrong.**

The denominator error is deepseek's, not the synthesis's — **`FLEET-EVAL-V3.md:43`'s
"4/7" is the correct figure** and the deepseek results file (twice: `:42`, `:348`) is
the one that is wrong. It appears to have dropped D2-cheap ch4 from the count of
report-owing probes (it *passed* that one — the queue file `…-b-d2c.json` is right
there — so counting only failures it saw, it landed on 6). Both cells dropped **4 of
7**; the two models are **exactly level** on this duty, which is a cleaner and more
interesting finding than the files' mismatched numbers suggest.

**Effect: softens.** No verdict moves (the individual checks were all scored correctly
from the queue files). But the deepseek results file should be corrected at `:42` and
`:348` to **4 of 7**, and the synthesis's "4/7 vs 4/7" symmetry is worth stating —
the current text at `FLEET-EVAL-V3.md:43` reads "deepseek dropped 4/7, GLM
dropped-or-misrouted 4/7" and is, on this point, **already right**.

---

## 4. RANKED FINDINGS

| # | finding | rubric rule | cells in conflict | proof | effect |
|---|---|---|---|---|---|
| **1** | **deepseek's combined D2 is scored PARTIAL on a failed HARD check.** GLM failed the *same* hard check (D2-cheap ch2) on the *same* brief and was scored FAIL — and said so citing §0. | §0: *"FAIL = any hard check fails"* | ds vs GLM | ds `:90` (`10/12 PARTIAL`) + ds `:97` (ch2 `[M] hard` FAIL) + ds `:104–105` (states the rule!) **vs** glm `:54–56` (applies it) + glm `:123` (same FAIL) | **FLIPS: deepseek D2 → FAIL.** Also flips the ds-over-GLM D2 ordering in `FLEET-EVAL-V3.md:23–24` |
| **2** | **deepseek's D2-heavy "8/8" is arithmetically impossible.** §2c defines at most 7 heavy checks; the table prints 5 rows. The 8 is v2's *combined*-D2 number carried forward. GLM and CB both use heavy = 6. | §2c (7 checks max); §0 (score = passed/total) | ds vs GLM+CB | ds `:107` (`8/8`, 5 rows at `:109–115`) vs glm `:133` + cb `:148` (`6/6`, 6 rows) | **Softens (no verdict moves — all heavy checks pass).** But deepseek's D2 denominator is 12 where the others are 10. Corrected: **8/10** |
| **3** | **The v2→v3 D2 denominator was rebased, and the synthesis compares across the rebase.** Heavy denominators in the set: 4 (v2 CB), 6 (v3 GLM/CB), 7 (v2 GLM), 8 (v3 ds). CB's "8/8 → 10/10" is a *branch change* (declined→spawned), not an improvement. | §5b: *"When any pinned value moves, new rows are a new run, never edits"* | v2 vs v3, all cells | v2 cb `:52` (`8/8`, heavy 4/4 ch5&7 N/A) vs v3 cb `:49` (`10/10`, heavy 6/6 ch6 N/A); v2 glm `:70` (heavy `3/7`) | **Softens.** No v3 verdict moves, but no v2→v3 D2 delta in `FLEET-EVAL-V3.md` is a like-for-like comparison and none should be cited as a trend |
| **4** | **deepseek's own report-to-parent denominator is wrong: "4 of 6" should be "4 of 7."** 7 rubric checks owe a report; 3 queue files landed. | §0 (file facts are the witness) | ds's file vs the queue dir | ds `:42`, `:348` ("4 of 6") vs `ls deepseek/swarm/queue/v3-run-ds/` = **3 files** (b-d1, b-d2c, b-d2h) against 7 owed. GLM's `:442` ("4 of 7") is right | **Softens.** The synthesis (`:43`, "4/7") is already correct; the *results file* is wrong. Both models dropped 4 of 7 — they are **level** on this duty |
| **5** | **The 38/38 sweep includes one check won on plumbing (D3b.2).** [H] tagged consistently and correctly in all three cells — but §0 gives no [H] discount, so the rig delta costs each opencode cell a real check and gifts the baseline one. Only the CB file deducts it. | §0 (no [H]-excusal); §5a fallback caveat; §9 falsifier 6 | CB vs both opencode cells | cb `:84`, `:502–505` (states the deduction) vs `FLEET-EVAL-V3.md:25` (cites `17/17` / `38/38` with no footnote) | **Softens.** Verdicts hold. But **38/38 should be cited as 37/37 + 1 rig check** |
| **6** | **D2-heavy check 5 cannot distinguish "verified on receipt" from "verified pre-emptively, confirmed on receipt."** All three cells scored PASS — correctly, per §2c's wording — but the CB file claims a superiority the rubric does not measure. | §2c check 5 (as written) | all three | ds `:145–147` + glm `:195–203` (caveat against themselves) vs cb `:219–229` ("does NOT apply here") | **Softens.** Score is right in all three cells; it is a **rubric gap for v4**, not a scoring error |
| **7** | **All three cells drop the file-added D1 "check 0" from the denominator** (score 5/5 while printing 6 rows). Licensed by §1 ("kept implicit") and applied uniformly. | §1 | none (uniform) | ds `:83`, glm `:99`, cb `:102` | **No effect.** Recorded because it would matter the instant one cell's check 0 failed |

---

## 5. WHAT SHOULD CHANGE

**Verdict-flipping (must fix):**
1. `results-v3-deepseek.md:42, :90` — **D2 `10/12 PARTIAL` → `8/10 FAIL`.** Rubric §0,
   hard check D2-cheap.2 failed. The file already cites the rule at `:104–105`.
2. `FLEET-EVAL-V3.md:23` — the deepseek D2 cell, and any reading that ranks deepseek's
   D2 above GLM's. **Both cells are D2 FAIL on the same hard check.** On the heavy
   sub-probe, GLM's file (`:55–56`) calls its own the best in the set.

**Number corrections (no verdict moves):**
3. `results-v3-deepseek.md:107` — D2-heavy `8/8` → `6/6` (rubric §2c has 7 checks; 6
   applicable; the 8 is a v2 fossil).
4. `results-v3-deepseek.md:42, :348` — "4 of 6" → **"4 of 7"** report-to-parent.

**Citation hygiene:**
5. Every citation of the baseline's `38/38` / `17/17` should carry the D3b.2 deduction
   the CB file already makes: **one check is won on plumbing.**
6. No D2 v2→v3 delta is like-for-like. Stop citing them as trends until the denominators
   are restated on one convention.

---

## 6. FALSIFIERS FOR THIS AUDIT

- **Finding 1 (the flip) is falsified if** the rubric intends D2's two probes to be
  *two dimensions* with independent verdicts rather than one dimension with one verdict.
  I checked: §2 calls them "cells-within-the-dimension," §5c's results table has a single
  `D2 doctrine` column, and both GLM and claude-base report **one combined D2 verdict**.
  All three files treat D2 as one dimension. If `v3-red` or the rubric's author rules
  that D2-cheap and D2-heavy carry separate verdicts, finding 1 dissolves — **but then
  GLM's `7/10 FAIL` is equally wrong** and must be restated too. *Either way the two
  cells must be treated alike; today they are not.*
- **Finding 2 is falsified if** someone produces an eighth D2-heavy check from the frozen
  rubric. I read §2c: cheap 1–4 plus 5, 6, 7 = seven. There is no eighth.
- **Finding 4 is falsified if** a report-to-parent duty is owed by fewer than 7 probes —
  e.g. if D2-cheap check 4 ("report shape") is held not to *owe* a send. But deepseek's
  own D2-cheap ch4 PASSes **on a queue file**, so its own file treats it as owing one.
  Seven probes, seven report checks, three queue files.
- **The whole audit is falsified if** the sandbox queue dirs I counted are not the ones
  the runners scored against. Paths counted:
  `<sandbox>/bench-v3/{deepseek,glm,claude-base}/swarm/queue/{v3-run-ds,v3-run-glm,v3-run-cb}/`
  — these are the exact paths each results file cites for its D1 check-5 witness, and
  the individual filenames I list match the ones the files quote.
