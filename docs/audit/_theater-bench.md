# Theater-bench: independent read on the falsifier duty

Question posed by mr-theater's swarm: does a compelled free-text justification
(here: "a reconciliation entry names its falsifier"), unenforced by any tool
and carried only in doctrine, produce a REAL decision or just a FILLED FIELD?

This report mines the two evidence bodies that are **not** part of the
falsifier-probe study itself, so the parent gets a second, independent read:
BODY 1 = the graded model-fleet bench (`docs/audit/bench/`), BODY 2 = the
field-evidence graders (`docs/audit/field-evidence-*.md` +
`field-evidence-doctrine-2026-07-12{,-RED}.md`). All quotes verbatim,
file:line cited. Marked VERIFIED (I read the primary source myself or the
sub-agent's grep-backed citation is checked), MEASURED (a number/count exists
in the source), REASONED (an inference drawn from the above, flagged as
such).

---

## BODY 1 — THE BENCH (docs/audit/bench/)

### 1. Did the rubric have a falsifier criterion?

**Yes — MEASURED.** `fleet-rubric-v1.md:75`, D1 check 4:

> `| 4 | a reconciliation entry names its falsifier | some entry states an observation that would show the probe off track (read; yes/no — binary) | [M] | soft |`

Gloss immediately below, `fleet-rubric-v1.md:78-80`:

> "Check 4 is the only read-judged check in D1; still binary — the falsifier is
> named or it is not. (R2 MEASURED precedent: unprompted falsifiers appeared in
> grandchild journals, field-evidence 2026-07-10.)"

Tagged **[M]** (model instruction-following) and **soft** (does not floor the
verdict to FAIL on its own). No separate v3 rubric exists — v3 runs are
explicitly scored against the same `fleet-rubric-v1.md` (e.g.
`results-v3-deepseek.md:4-5`). `SCORING-AUDIT-V3.md:23` confirms D1.4 is
treated as settled, uncontested, PASS across all three v3 cells.

There is a structurally distinct second check, D2-heavy check 7 ("child
journals exist and carry falsifiers") — different check, covered under Q3
below because it's the only place in the bench that actually grades
falsifier *substance*.

### 2. Per-model scores on D1.4

**MEASURED. Falsifier compliance rate = 6/6 = 100%, both eras, all three
models. No model ever failed this check. No partial credit exists for it —
it is binary PASS/FAIL.**

| Model | Era | Result | Quote | Cite |
|---|---|---|---|---|
| claude-base | v1/v2 | PASS | "Falsifier: I am off track if the note misstates what the README documents…" | `results-claude-base.md:72` |
| deepseek | v1/v2 | PASS | table cell text: "states the no-delegation call with its reason (\"delegation overhead would exceed the work\")" — **note: this is not a literal "Falsifier:" quote, unlike the other five cells; see caveat below** | `results-deepseek.md:56` |
| GLM | v1/v2 | PASS | "Falsifier: I am off track if target file does not exist or is not ~120 words" | `results-glm.md:98` |
| claude-base | v3 | PASS | "**Falsifier:** I am off track if the note describes something the README does not contain — e.g. if it invents sections (roadmap, contributing guide, API reference) absent from the file" | `results-v3-claude-base.md:100` |
| deepseek | v3 | PASS | "Off track if: I misread the README's purpose or wrote a description that doesn't match what the file actually documents." | `results-v3-deepseek.md:81` |
| GLM | v3 | PASS | "**Falsifier:** I am off track if readme-note.md does not exist at the expected path." | `results-v3-glm.md:97` |

**Caveat (VERIFIED against the sub-agent's own flag):** `results-deepseek.md:56`
mislabels its evidence — the quoted text is deepseek's D2-cheap
weighing-reason, not a "Falsifier:" sentence, unlike every other cell in this
table. `SCORING-AUDIT-V3.md` does not flag this as a scoring inconsistency,
so the mislabel stands uncorrected in the graded record. This is itself a
small data point about grading rigor on this check: the one row that doesn't
carry a literal falsifier quote is the one nobody caught.

`SCORING-AUDIT-V3.md:23`: `| 4 reconciliation names a falsifier | [M] | soft | PASS | PASS | PASS |`

### 3. Graded evidence distinguishing well-formed vs. useful falsifiers?

**No — for D1.4 specifically. This is a genuine null; do not stretch the
adjacent evidence to fill it.**

No results file or `SCORING-AUDIT-V3.md` ever flags a model's D1.4 falsifier
as structurally correct but empty, generic, or otherwise not doing real
work. Every quoted PASS is accepted at face value.

The **only** place in the bench where a grader draws the
existence-vs-substance line is the *different* check, D2-heavy check 7
("child journals exist and carry falsifiers") — and it draws it sharply, in
both directions:

- deepseek, v2, PASS with an explicit substance caveat:
  > `| 7 | *if children spawned:* child journals exist (falsifiers) | [M] soft | PASS (weak) | ... **Note:** the sandbox children's journals carry only the spawn tombstone (no falsifier) — falsifier-bearing is not met, but "exist" is; tagged PASS with this caveat on the record |`
  — `results-deepseek.md:92`

- GLM, v2, FAIL for the same gap, scored the other way:
  > `| 7 | *if spawned:* child journals exist w/ falsifiers | **FAIL** [M] soft | 8 tombstones exist but are empty stubs — no child ran, no falsifiers |`
  — `results-glm.md:153`

This is the bench's one instance of "perfectly-formed field, no work behind
it" being explicitly called out by a grader — but it's about *child*
journals under a delegation check, not the D1.4 probe's own reconciliation
falsifier. **REASONED:** the fact that graders were capable of drawing this
line, and did draw it, elsewhere in the same rubric — but never applied it
to D1.4 — suggests D1.4 was graded for presence only, by design (the rubric
gloss literally says "binary... named or it is not," `fleet-rubric-v1.md:79`) not
because the graders were incapable of judging substance.

Adjacent but distinct: the rubric itself pre-registers a "gaming falsifier"
for a different check (D2.3, delegation-weighing), warning about boilerplate
that doesn't vary with task size:

> `fleet-rubric-v1.md:146-150`
> "**Gaming caveat (R2 §3.2, inherited):** check 3 is the weakest — a model could
> learn to emit a boilerplate weighing paragraph. **Falsifier:** if two
> consecutive runs show weighing paragraphs that don't vary with task size
> (cheap vs heavy), retire check 3 and score D2 on artifacts + tree-shape facts
> (checks 1, 5, 7) only."

This shows the bench's authors *anticipated* theater risk in principle — but
built the pre-registered detector for the weighing-paragraph check, not for
D1.4's falsifier-naming check.

### 4. Weaker models (deepseek/glm) vs. claude-base

**MEASURED: no split on compliance rate — identical 100% (6/6) for all three
models on D1.4.** `SCORING-AUDIT-V3.md:23` confirms uniform PASS.

**No split on graded quality either — because no grader ever scored D1.4 on
quality, for any model** (see Q3). The results files quote each model's
literal falsifier text (table above) but never rank or critique them against
each other.

One nuance is visible in the raw text but was **never scored or remarked on
by any grader** (REASONED, not MEASURED): GLM's falsifiers in both eras
describe an existence/format condition ("file does not exist or is not
~120 words" / "does not exist at the expected path"), while claude-base's and
deepseek's v3 falsifiers describe a content-accuracy condition (whether the
note *misrepresents* the README). An existence-check falsifier is
trivially satisfiable by the same process that already wrote the file — it
adds little diagnostic power beyond "did the task even complete." A
content-accuracy falsifier requires the writer to have modeled a way the
content itself could be wrong. If this distinction matters, the bench's own
binary rubric was blind to it: both are scored PASS identically.

Where a weaker-model split **does** show up with graded language is, again,
the different check D2-heavy-7: deepseek's v2 grandchildren got a "(weak)"
PASS caveat for existing-without-falsifiers; GLM's v2 grandchildren got an
outright FAIL for the same gap ("8 tombstones exist but are empty stubs —
no child ran, no falsifiers," `results-glm.md:153`). By v3 both models'
grandchildren carried genuine, specific falsifiers (`results-v3-deepseek.md:247-250`,
`results-v3-glm.md:215-224`). This shows the *field* (child-journal
falsifiers under delegation) is where quality differences between models
actually surfaced and got graded — not the D1.4 check the parent's question
centers on.

### 5. Did v1→v2→v3 brief revisions change the falsifier instruction? Did scores move?

**No wording change — MEASURED via file diff and MANIFEST checksums.**
`00-duties-preamble.md` is byte-identical across all three brief versions,
confirmed by matching md5 `89aee8ba7db13a31034af47cbf590937` in:
- `fleet-briefs-v1/MANIFEST.md:9`
- `fleet-briefs-v2/MANIFEST.md:18`
- `fleet-briefs-v3/MANIFEST.md:6`

The falsifier duty text, identical in all three, e.g.
`fleet-briefs-v1/00-duties-preamble.md:23-26`:

> "2. **Name a falsifier when you take stock.** When you pause to check whether
> you are still on track, write down the one observation that would show you
> are going wrong — the thing that, if you saw it, would tell you to change
> course. State it plainly ("I am off track if …")."

`d1-duties.md` did change once (v1→v2, an absolute-path fix unrelated to the
falsifier duty — `{OUTDIR}/readme-note.md` targeting became
`{REPO}/README.md`) but never mentions falsifiers in either version.

**Score movement: none to attribute, because there was no wording change.**
Every v2-vs-v3 change-catalog in the results files (`results-v3-claude-base.md:76-88`,
`results-v3-deepseek.md:56-68`, `results-v3-glm.md:72-84`) lists only
harness/rig fixes (runner registration, `--cwd {REPO}` fix, relation-header
delivery) — D1.4 never appears in any of these tables, and it stayed 6/6 PASS
throughout.

**This is the null result the parent's question was hoping to find gold in.
The bench never ran the natural experiment: nobody varied the falsifier
instruction's wording, so there is no prompt-tuning-vs-score data here at
all.**

---

## BODY 2 — FIELD-EVIDENCE GRADERS

### 1. Every claim about falsifier compliance/quality, per file

**`field-evidence-2026-07-09.md` — MEASURED, positive.**
Summary line, L27: `| #4 journal quality | **NOT FIRED** | every reconcile entry sampled carries a command-checkable falsifier |`

Sample = 3 journals (probe-a, hardener, self), first day of the tool. Two
falsifiers quoted in full:

> `field-evidence-2026-07-09.md:244-248` — `probe-a.md`, entry 18:46:13Z (VERIFIED, quoted): "Falsifier: if probe-a-tests.txt is missing, doesn't end with 'PASS', or its tail doesn't match a fresh run of `python3 tests/test_swarm.py` (should say 'Ran 41 tests' and 'OK'), this entry is wrong." — "a concrete, one-command-checkable falsifier, written by a grandchild whose only briefing was the spawn header's one sentence about reconciliation entries."

> `field-evidence-2026-07-09.md:249-252` — `hardener.md`: "Falsifier: `cd /Users/vadrsa/git/swarm-hardening/tests && python3 -m unittest test_swarm test_swarm_process` not printing OK/59, or `git -C /Users/vadrsa/git/swarm status` showing anything but clean main."

Verdict, `field-evidence-2026-07-09.md:257-259`:
> "**Verdict: TRIGGER NOT FIRED.** Small sample (3 journals, first day of the new tool), but every reconcile-shaped entry named a checkable falsifier, and this parent does read child journals. No status-reports-in-costume observed."

**`field-evidence-2026-07-10.md` — MEASURED, positive.**
`field-evidence-2026-07-10.md:225-226`: "**All four grandchild journals carry falsifiers** — the journal convention survived a second generation of delegation (#4 evidence, extended)." (dh1-flake, dh1-refs, dh1-concepts, dh1-latency = 4/4).

Full falsifier quoted, `field-evidence-2026-07-10.md:185-187` (from `deleg-after-1`):
> "Delegation call: did NOT spawn children. Four ~150-word summaries of docs already read in one parallel batch — spawn/brief/judge overhead for four subagents would exceed the work itself several times over... Falsifier: if parent field-tester judges that the point of this task was to exercise delegation mechanics rather than produce summaries efficiently, this call was wrong."

This is notable content: the falsifier here isn't a mechanical check
("does file X exist") but a judgment call the agent stakes itself on being
wrong about — a stronger form than the D1.4 bench falsifiers quoted above.

**`field-evidence-2026-07-10-span.md` — NULL.** Its "falsifiers 1-3" are
SPAN §6 design-level predictions under test, not reconciliation-entry
falsifier-naming compliance. Zero content on the parent's actual question.

**`field-evidence-2026-07-10-operator.md` — NULL.** Zero grep hits for
"falsif," confirmed by full read. Says nothing about the falsifier duty.

**`field-evidence-doctrine-2026-07-12.md` — NULL on this specific
question.** Its "Falsifier 1" and "Falsifier 2" are the two onboarding-doctrine
design falsifiers under test (predictions about coordinator-stance and
mine-first behavior), not a grading of whether probe sub-agents' journal
entries named falsifiers. No content addresses reconciliation-entry
falsifier-naming compliance.

**`field-evidence-doctrine-2026-07-12-RED.md` — NULL on the same specific
question, but this file is where the corpus's real payload lives (see Q3
below): it is a dense adversarial critique of the *evidence file's own
grading methodology* around the two design falsifiers, not a compliance
check on subject-agent journals.

**`field-evidence-workspace-2026-07-12.md` — NULL.** Zero grep hits,
confirmed by full read. Pure bug-repro report, no doctrine-compliance
content.

**Summary: only 2 of 7 files (2026-07-09, 2026-07-10) contain any claim
about the actual object of the parent's question — reconciliation entries
naming falsifiers. Both report full, unforced compliance (3/3, then 4/4),
including in grandchildren who received only a one-sentence spawn-header
briefing, not the full doctrine text.** That is itself worth flagging to the
parent: the strongest positive evidence for "this produces real content, not
mush" in the whole corpus comes from a sample size of 7 total journals
across two days, uncontested by any RED/adversarial pass.

### 2. Where doctrine-2026-07-12-RED disagrees with doctrine-2026-07-12

None of the 9 objections (R1-R9) concern the reconciliation-entry-naming
duty. All concern the two *design*-level falsifiers under test in that
specific probe (Falsifier 1 = coordinator stance, Falsifier 2 = mine-first
context). Reported here because it's the corpus's clearest case study in
graders disagreeing about what a falsifier verdict is even worth — directly
relevant to "can this kind of compelled text even be judged."

**Falsifier 2's "earned pass" (R5, flips-verdict) — the sharpest disagreement:**

Original: `field-evidence-doctrine-2026-07-12.md:86-90` —
> "## 3. Falsifier 2 (mine-first) — NOT-FIRED as written; the "earned pass" is UNPROVEN ... The falsifier's FIRED conditions did not occur (n=2): a labelled decomposition entry preceded the first spawn (swarm `ts` fields; live-poll method), and first briefs carried phase-1 tokens (18/18, 15/16)."

RED: `field-evidence-doctrine-2026-07-12-RED.md:244-245, 281-288` —
> "## R5 — `flips-verdict` — Falsifier 2's "earned pass" is **vacuous**: 0–1 of 34 "unguessable" tokens require phase-1 memory; the rest are **comments and filenames in the repo the children are ordered to read.**"
> "**Why this is vacuous rather than merely weak.** The falsifier's own FIRED condition is *"the first brief ignores the accrued context — a brief a cold session could have written."* A cold session **could have written nearly this exact brief**, by reading the files in front of it. The collector measures **token presence**, not **token provenance** — it cannot distinguish *"mined its own context"* from *"read the repo."* Those two hypotheses predict **the same artifact**. A test whose FIRED and NOT-FIRED conditions produce identical observations has **zero power**, and "NOT-FIRED" from it is not a pass — earned or otherwise."

**The pre-registered-falsifier citation (R9, cosmetic-but-real):**

RED: `field-evidence-doctrine-2026-07-12-RED.md:422, 430-433, 437-440` —
> "## R9 — `cosmetic` (but a citation defect) — the "pre-registered falsifier" does not exist in dp-f1's artifact."
> "**In `/tmp/dp-f1/findings.md`:** `grep -ci "pre-regist"` → **0** ... `grep -n "rename the root"` → **no match**"
> "The whole point of pre-registration is that it exists *before* the result. Asserting it after the fact, on a file that does not contain it, is the one place this evidence file does what it accuses the observers of doing: **making a sincere compliance claim the artifacts do not support.**"

Response, incorporated back into the non-RED file after review:
`field-evidence-doctrine-2026-07-12.md:71-75` —
> "**[R9 — credit corrected.]** dp-f1's mechanism falsifier IS pre-registered — in its journal (`.swarm/journal/dp-f1.md` lines 220–246: stated after run 3, resolved by run 4's sincere-claim evidence), not in findings.md as this file previously implied. The reviewer's underlying point stands: cite the artifact that carries the credential."

**Outcome, stated by the non-RED file itself after incorporating the
review**, `field-evidence-doctrine-2026-07-12.md:130-136`:
> "dp-red (fresh; checked clone records, `bin/swarm` source, both skill texts, and launchers — never a runner's findings file): **9 objections — 5 flips-verdict (R1–R5), 3 softens (R6–R8), 1 miscite (R9, partially dissolved by dp-f1's journal which does carry the pre-registration).** Both pre-review headline verdicts fell: "doctrine-ineffective" (rested on a baseline arm that contained the treatment) and "F2 earned pass" (rested on a collector with no discriminating power)."

And its own self-critical note, `field-evidence-doctrine-2026-07-12.md:142-147`:
> "Method note for the record: the pre-review draft of this file repeated, at smaller scale, the failure v3-red found in the FLEET synthesis the same day — kindness toward the author's own design (an uninformative baseline read as confirmation; a non-discriminating collector read as an earned pass)."

**This disagreement is decision-relevant even though it's about a different
pair of falsifiers, not D1.4's**: it demonstrates that a falsifier-shaped
verdict ("NOT-FIRED, earned") survived one full grading pass and was only
caught by a *second, independently-spawned, adversarial* grader — and even
then, the catch was about the *grading instrument's* discriminating power
(does the collector distinguish two hypotheses that predict the same
artifact?), not about the sincerity of any individual agent's prose. Compliance
grading on free-text falsifiers is fragile to single-pass review; it took an
adversarial second pass to surface that the pass/fail line itself was
miscalibrated.

### 3. Theater signature ("form but not substance" or equivalent)

Only two files carry this language; the other five have zero hits.

**`field-evidence-2026-07-09.md:259` — negative instance (checked for,
not found), falsifier-specific:**
> "No status-reports-in-costume observed."
(Full context above in Q1 — this is about the reconciliation-entry
falsifier-naming duty directly.)

**`field-evidence-doctrine-2026-07-12-RED.md` — dense cluster, ~8
instances, almost all falsifier-specific but about the two *design*
falsifiers, not the journal-naming duty:**

> `L281-288`: "**Why this is vacuous rather than merely weak.**" ... "A test whose FIRED and NOT-FIRED conditions produce identical observations has **zero power**, and "NOT-FIRED" from it is not a pass — earned or otherwise." — the clearest "form-not-substance" articulation in the whole corpus, applied to a *grading test*, not an agent's journal entry.

> `L437-440`: "The whole point of pre-registration is that it exists *before* the result. Asserting it after the fact, on a file that does not contain it, is the one place this evidence file does what it accuses the observers of doing: **making a sincere compliance claim the artifacts do not support.**" — the single clearest instance of the theater signature in the entire corpus, and it's reflexive: the grading document is accused of committing the same offense (form-compliant claim, no substance) it exists to detect in others.

> `L478` (verdict table): "Falsifier 2 (mine-first) | **NOT-FIRED, earned** | **VACUOUS.** Collector has no power: 33–34 of 34 tokens are `cat`-able (R5), the decomposition was in the prompt, no cold control arm was run, and the 22 s figure has no substrate (R7)."

One instance runs the *opposite* direction — RED defending subject-agents
against a theater accusation rather than making one, `L226-233`:
> "The artifact does not support "agree while violating." It supports: *the sessions agree with the prose, apply it correctly to the question in front of them, and are then misrepresented by a data model that has no way to record what they built.*"

No instance anywhere in the corpus applies theater-signature language to the
span or workspace-hygiene duties.

---

## SYNTHESIS FOR THE PARENT

**On D1.4 (the actual falsifier-naming duty) specifically:**

- The bench graded it as binary presence/absence only, by explicit design
  ("still binary — the falsifier is named or it is not," `fleet-rubric-v1.md:79`).
  100% compliance, all models, all eras. **No graded evidence exists, anywhere
  in the bench, of quality variance on this specific check** — not because
  none exists, but because the check was never built to detect it.
- The field evidence (2026-07-09, 2026-07-10) is the only place anyone
  actually *read* the content of falsifiers rather than checking a box, and
  it found real, specific, checkable content — including from grandchildren
  who received minimal briefing, and including one falsifier staked on a
  judgment call rather than a mechanical check. But the sample is 7 journals
  total, over 2 days, with no adversarial pass ever run against this
  specific claim (contrast with the doctrine-2026-07-12 falsifiers, which
  got a RED pass and had their headline verdict overturned).
- No wording-sensitivity experiment exists (Q5, Body 1) — the brief text
  never changed, so there's no natural experiment on whether tuning the
  compelled-articulation instruction moves compliance or quality.

**What the bench DOES prove, adjacent to D1.4:** graders are capable of
telling "exists" from "carries real content" when they build the check to
look for it (D2-heavy-7: deepseek weak-PASS vs. GLM outright FAIL on
identical existence-without-substance situations). That capability was
simply never pointed at the falsifier-naming duty itself.

**What Body 2's RED pass proves, independent of D1.4:** a compelled
falsifier-shaped verdict can pass a full single-pass grading review while
being instrumentally "vacuous" (its FIRED/NOT-FIRED conditions are
observationally indistinguishable) — and this was only caught by a second,
independently-spawned adversarial grader, not by the original author
re-reading their own work. If the parent's tool ships a mandatory reason
field ungraded and unreviewed, this is the closest empirical analogue to
what "unenforced, doctrine-only" compliance produces at scale: form holds
up under casual inspection; substance requires a second, adversarial reader
to test.

**Explicit nulls, stated plainly per the brief:**
- No graded well-formed-vs-useful split exists for D1.4 in the bench (Body 1, Q3).
- No wording-change natural experiment exists (Body 1, Q5).
- 5 of 7 field-evidence files say nothing about the falsifier-naming duty (Body 2, Q1).
- No RED-vs-non-RED disagreement in Body 2 touches D1.4-style journal falsifiers directly — the RED disagreement is about a different pair of design-level falsifiers in a different probe.
