# FLEET-EVAL-RED — adversarial review of FLEET-EVAL.md

**Reviewer:** `eval-red` (fresh; did NOT run the eval). Reports to `fleet-eval`.
**Written at** `main@aa6063d`, 2026-07-11, against the sandbox artifacts under
`…/990a14af-…/scratchpad/bench-v2/{deepseek,glm,claude-base}/` (the session hash the
results files pin, not this reviewer's cwd — re-readers must use that path).

**Headline verdict: the reading STANDS on its spine but needs two CAVEATS that
materially soften it — one of which is a genuine scoring error.** The load-bearing
cross-check (deepseek's children produced real reports; GLM's did not) is TRUE at the
artifact level — I re-ran it and it holds. But (a) **deepseek's D4 was mis-scored PASS
where GLM was scored FAIL on identical behavior** — this erases the sharpest "deepseek
is more restart-capable" claim; and (b) **deepseek's parent loop was never witnessed
cleanly** — its children reported to `operator`, not to the parent, and the parent
"verified" by reading files off disk, not by receiving a report. The placement
direction survives (deepseek > GLM as a parent candidate; both above-leaf claims are
weaker than stated), but two of the reading's strongest sentences should be struck or
downgraded.

---

## Verdict per stress-test

### (1) Is "deepseek looks parent-capable" actually supported, or does the §5b wall undercut it more than §6 admits? — **UNDERCUT MORE THAN ADMITTED (CAVEAT)**

The parent loop was **never witnessed cleanly**. Evidence, all re-read:

- deepseek's 4 D2-heavy children reported to **`.swarm/queue/operator/`**, NOT to
  `queue/b-d2h/`. There is **no `queue/b-d2h/` directory at all**
  (`bench-v2/deepseek/.swarm/queue/` contains only `operator/`). So the
  *parent-receives-child-report* leg of the loop **did not happen over swarm's
  delivery** — the children rerouted to `operator`, and the parent read the report
  **files off disk**.
- The parent's "verification" (`bench-v2/deepseek/.swarm/journal/b-d2h.md`, entry 2) is
  a **file-existence check plus a restatement of each report's headline number**
  ("Harvested all outputs, verified all four report files exist: report-1: 25/25 PASS
  …"). It is **not** a recomputation or independent spot-check. Rubric D2c check 5 asks
  for "a recomputation/spot-check visible in the probe's journal"; what is visible is
  *reading and summarizing*, not recomputing.
- The `swarm close job-{stability,refcheck,concepts,timing}` calls are real (transcript,
  4 distinct closes) — that half of the loop is clean.

**So:** spawn → children run → close is genuine. **verify-via-delivery is a filesystem
side-channel**, not swarm's parent loop. FLEET-EVAL.md:126 ("**verified** and closed
them"), :277 ("verified their real output"), and the §1 phrase "**real, working
delegation**" overclaim: the delegation *ran*, but the parent never received a report
through the mechanism a real parent uses, and never re-derived a child's result. §6's
own asterisk ("report-to-parent was never witnessed *cleanly*") is correct but
**under-weighted** — it is buried as a rig footnote when it is actually the whole
receive-and-verify half of the parent loop.

**Net:** "plausible parent" survives as a *directional* read; "demonstrated the full
parent loop working end to end" (§1, §3a) does **not** — strike or downgrade it.

### (2) Is "GLM leaf-only" fair, or is the child-death a harness artifact wrongly pinned on GLM? — **PARTLY UNFAIR (CAVEAT): the child-death is downstream of a cwd choice, not a clean GLM-model fact**

The load-bearing cross-check is **TRUE**: deepseek's children produced real reports
(re-verified below), GLM's produced nothing. But **the mechanism is not a GLM model
property** — it is where each parent placed its children's cwd:

- **deepseek's parent** prepended `cd /Users/vadrsa/git/swarm && SWARM_DIR=…/deepseek/.swarm`
  to every spawn (transcript, 4×). Its children launched with **cwd = the real repo** —
  so `python3 tests/test_swarm.py`, `[ -e path ]`, `swarm world` all resolved against
  real files, and the children produced real audits.
- **GLM's parent** ran bare `swarm spawn stability` (transcript). Its children inherited
  **cwd = the empty sandbox** (`agents/stability.json` → `"cwd": "…/bench-v2/glm"`) —
  nothing to audit.
- **Both cells launch native `claude`** (`launch.sh` runs `claude --settings …`,
  `model:""` in every agent record — verified across all 8 deepseek + 9 GLM child
  records). **The child model is identical (Claude) in both cells.** So the difference
  cannot be GLM-vs-deepseek child capability.
- **It is not the trust prompt either:** `/Users/vadrsa/git/swarm` has
  `hasTrustDialogAccepted: false` in `~/.claude.json` (same as the glm sandbox), yet
  deepseek's children in that cwd ran fine. So "untrusted folder wedged the child" does
  not distinguish the cells.

**Two ways to read this, and the reading only tells one:**
- **Charitable to the reading (and I think correct):** choosing the right child cwd
  *is* a parenting competence. deepseek reasoned that children need the repo cwd; GLM
  did not. That genuinely separates them **as parents** — and supports "deepseek more
  parent-capable, GLM fragile."
- **The caveat the reading omits:** GLM's "children **died**" (FLEET-EVAL.md:48,
  results-glm.md:143 "all 8 children's claude sessions died on launch") is **not
  established**. What is established is that GLM's children had **nothing to do in an
  empty cwd**. "Died on launch" vs "launched into an empty directory and produced
  nothing" are different failure modes with different placement weight, and the
  artifacts cannot tell them apart (both `.status` files across BOTH cells say only
  "launching" — neither launcher captured a clean exit or a death). Pinning it as
  liveness-death **[H] plumbing compounded by [M] no-watchdog** is a plausible *story*,
  not a *witnessed* one. Corroboration I ran directly: deepseek's living stability child
  left a full Claude session dir (`…/ec028cad-…/scratchpad/runs/`, 50 `run-NN.{out,err}`
  files) — **no GLM child left any equivalent session dir with work products**, which is
  consistent with *either* an empty-cwd idle *or* a launch crash; the artifacts do not
  disambiguate, so "died on launch" remains unproven. (I spawned a scout,
  `eval-red-glmforensics`, to pin the exact mechanism; it went idle without producing a
  verdict and was closed — the finding stands on the launcher/cwd symmetry I verified
  myself, which does not depend on the scout.)

**Net:** "GLM leaf-only / fragile parent" **survives** — its no-watchdog hang and its
bare-spawn (no cwd management) are real and are genuine parenting weaknesses. But the
specific claim "**children died on launch**" is an inference, not an observation, and
the child-death asymmetry is **at least as much a cwd-management gap as a
child-liveness fact**. Downgrade "died" to "produced nothing (spawned into an empty
cwd, no watchdog to notice)."

### (3) Does the battery discriminate, or is it near-all-PASS? — **IT DISCRIMINATES (STANDS)**

Rubric §9 falsifier-1 does **not** fire. Dimension verdicts (excluding baseline):
- **deepseek:** D1 PASS, D2 PASS, D3 PARTIAL, D4 PASS → 3 PASS / 1 PARTIAL / 0 FAIL.
- **GLM:** D1 PARTIAL, D2-cheap FAIL, D2-heavy PARTIAL, D3 PARTIAL, D4 FAIL → **0 PASS**.

Real spread: two genuine FAILs on GLM (D2-cheap, D4), a PARTIAL gap on deepseek's D3,
and the baseline all-PASS as the anchor. The weighing check even *varies with task size*
within each model (deepseek D2c "overhead exceeds cost" vs D2h "clear win for
delegation" — re-read from `b-d2c.md`/`b-d2h.md`), so the §2c anti-gaming falsifier
holds too. **This stress-test passes clean.** (Caveat: see #4 — one of deepseek's PASSes
is mis-scored, which if corrected makes deepseek and GLM *less* separated, but the
battery still discriminates — it just discriminates less sharply than the table shows.)

### (4) Are any [H]/[M] tags mis-assigned? — **ONE HARD-CHECK SCORING ERROR + ONE ASYMMETRY (CAVEAT → partial FAIL of a cell-dimension)**

**(4a) THE HEADLINE ERROR — deepseek D4 check 2 is mis-scored PASS; on the rubric's own
witness it is a FAIL, which flips deepseek's D4 from 6/6 PASS to FAIL.**

Rubric D4 check 2 (HARD [M]): "turn-1 plan was **journaled** — a **journal entry** from
the turn-1 window describes the multi-turn plan."

- deepseek has **no `b-d4.md` journal** anywhere in its sandbox (`find … -name b-d4*`
  returns nothing; turn-3 bash literally prints `journal does not exist`).
- deepseek wrote its plan into **`out/d4/catalog.md`** (the deliverable): the
  `**Plan**: One shelf per turn…` line is at the top of the catalog, not in a journal.
- results-deepseek.md:152 scored check 2 **PASS**, citing that catalog line — but the
  witness the rubric names is a **journal** entry, not the deliverable.

**GLM was scored FAIL on the identical situation:** no `b-d4.md`, plan in `catalog.md`
→ results-glm.md:233 "**FAIL** … NO `b-d4.md` — the multi-turn plan was never written to
the journal." **Same behavior, opposite score.** Applying the rubric consistently,
**deepseek's D4 check 2 fails**, and since it is a **hard** check, deepseek's D4 verdict
drops from **6/6 PASS to FAIL** — the exact failure mode used to declare GLM leaf-only.

Both models' turn-3 recovery is *also* identical: each tried to read its (nonexistent)
`b-d4.md`, got nothing, and recovered from `catalog.md`. So FLEET-EVAL.md's repeated
claim that deepseek "**held a plan across a simulated restart by re-reading its own
journal**" (:126, :158, :277) is **factually wrong**: there was no journal; deepseek
recovered from the deliverable, exactly as GLM did. This is the single most
placement-relevant error in the document — it manufactures a deepseek>GLM gap on D4 that
the artifacts do not support.

**(4b) The D3c-M2 "relation" asymmetry — a dropped check leaks back into scoring in
opposite directions.**

Rubric §3c explicitly **drops** M2's "reply names the sender's relation" under opencode
(no swarm header exists in a `--session` turn), scoring M2 only as "did it act on this
turn." Yet:
- deepseek's `echo-2.md` = `parent` → scored PASS and cited approvingly. The transcript
  shows the runner **hand-injected** the relation into the delivered prompt ("This
  message's header shows the sender as run-deepseek-2. The relation is parent") — the
  model echoed planted text, not a real swarm header.
- GLM's `echo-2.md` = the standby brief echoed back (wrong) → scored **[M] FAIL**.

Scoring GLM's miss as a real [M] failure is **fair** (it did fail to act on the turn's
instruction). But *crediting* deepseek for naming `parent` — a check the rubric said it
dropped as unwitnessable — is **generous in the opposite direction**. The dropped check
should not add to deepseek's column while subtracting from GLM's. Low placement impact,
but it is an inconsistency in the same dimension.

**(4c) Minor: deepseek D2-heavy check 7 (child journals carry falsifiers) scored PASS.**
The child journals are 4-line spawn tombstones with **no falsifier** (re-read all four).
results-deepseek.md:92 honestly flags this ("PASS (weak)… falsifier-bearing is not
met"). It should be a soft FAIL, not a weak PASS — does not change the D2 verdict (soft
check, hard checks all pass) but the tally 8/8 is really 7/8.

### (5) Any claim in FLEET-EVAL.md NOT backed by a citable artifact? — **TWO (CAVEAT)**

- **"re-reading its own journal" (§3a:126, §6:277, results-deepseek D4:158)** — **NOT
  BACKED.** No `b-d4.md` exists; the turn-3 transcript's read of it returned empty. The
  recovery was from `catalog.md`. (See 4a.)
- **"verified their real output" / "real, working delegation" (§1:32, §1:44, §6:277)** —
  **PARTIALLY BACKED.** The output is real; the "verification" is a file-existence read,
  and no report ever reached the parent's mailbox. (See #1.)
- **Backed and re-confirmed:** the 4 deepseek reports are genuine, not fabricated —
  `report-1-stability.md` cites 50 raw `run-NN.{out,err}` files that **do exist** under
  a separate Claude child session (`…/ec028cad-…/scratchpad/runs/`, 50 files present);
  `report-4-timing.md` carries real `perf_counter` numbers. The README-note real-repo
  claim (§3a) is backed (`out/d1/readme-note.md` names swarm's four verbs, herdr,
  GPLv3). The baseline's M2 "your parent" relation-header PASS (§3c, the "rig-advantage"
  claim) is backed (`claude-base/out/d3c/echo-2.md` = "your parent"). The discrimination
  claim is backed (#3).

---

## Overclaims / errors, ranked by placement impact

1. **[FLIPS A VERDICT] deepseek D4 is mis-scored 6/6 PASS; correct score is FAIL** on
   the rubric's own hard check 2 — deepseek never journaled its plan (no `b-d4.md`; plan
   in `catalog.md`), identical to GLM which was FAILed for it. Kills the
   "deepseek re-read its own journal across a restart" claim (§1, §3a, §6). **This is the
   error most likely to change an operator's placement**: it removes the cleanest
   evidence that deepseek out-parents GLM on long-horizon coherence. After correction,
   deepseek and GLM are **tied** on the D4 journal duty (both skip it); deepseek's
   parent edge rests on D2 (real spawn/close) alone.

2. **[SOFTENS THE CORE READING] deepseek's parent loop was never witnessed cleanly** —
   children reported to `operator` not the parent (no `queue/b-d2h/`), and "verify" was
   a disk read, not a received-and-recomputed report. "real, working delegation" /
   "verified their real output" (§1, §6) overclaim; downgrade to "spawned real children
   that ran and were closed; receive-and-verify was via filesystem, not swarm delivery."

3. **[REFRAMES GLM'S FAILURE] GLM's "children died on launch" is an inference, not an
   observation** — the witnessed fact is children spawned into an **empty cwd** (a
   parent cwd-management gap) with the **same Claude launcher** as deepseek's living
   children. "Died" should be "produced nothing (empty cwd, no watchdog)." GLM's
   fragile-parent read survives; the death mechanism does not.

4. **[MINOR] D3c-M2 relation scoring is asymmetric** — a rubric-dropped check credits
   deepseek (`parent`, from runner-injected text) while penalizing GLM. Low impact.

5. **[MINOR] deepseek D2-heavy is really 7/8, not 8/8** — child-journal falsifier check
   (check 7) should be a soft FAIL (tombstone-only journals). Does not change the D2
   PASS verdict.

**None of these reverse the overall direction** (deepseek is the stronger non-Claude
parent candidate; GLM reads as a clean leaf with parenting weaknesses; Claude anchors).
But #1 and #2 together mean the document's two strongest sentences — "demonstrated the
full parent loop working end to end" and "held a plan across a restart by re-reading its
own journal" — are **not supported by the artifacts** and should be struck before the
operator relies on them. The honest post-review reading is: **deepseek's only *cleanly
witnessed* parent-grade behavior is real spawn-and-close of children it correctly chose
to give a working cwd; everything past that (receive, verify, journal-driven restart) is
either a filesystem side-channel or, in D4's case, absent — same as GLM.**

---

## What would change these verdicts (falsifiers for this review)

- If a `queue/b-d2h/` report or a recomputation appears in deepseek's sandbox that I
  missed, objection #2 weakens. (Checked: no such dir; journal shows existence-check
  only.)
- If a `b-d4.md` journal exists for deepseek anywhere, #1 collapses. (Checked:
  `find … -name b-d4*` empty; turn-3 bash prints "journal does not exist".)
- If GLM's children left a claude session dir showing a real crash (not an empty-cwd
  idle), #3's "inference not observation" softens toward the reading. (Checked: no GLM
  child left a session dir with work products, unlike deepseek's `ec028cad` child; the
  artifacts do not disambiguate crash from empty-cwd idle, so the inference stands.)
