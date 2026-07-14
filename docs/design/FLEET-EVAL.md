# FLEET-EVAL — a swarm instruction-following eval on real Chinese models

> SUPERSEDED by FLEET-EVAL-V3.md; kept for the record (the first measured run — the caught rig bug §4 and the adversarial-correction discipline §9, flipped D4 verdict, that recurred in V3-RED).

**Author:** `fleet-eval` (successor to `fleet-scout`), reporting to the operator.
**Written at** `main@aa6063d`, 2026-07-11. **Status:** RUN — designed, executed
(operator-approved), verified, adversarially reviewed, **and corrected against the
review** (`eval-red`, `docs/design/FLEET-EVAL-RED.md`). The review flipped one
verdict and softened two claims; every correction is folded below and logged in §9.

**What this is.** The operator kept `fleet-scout`'s execution-surface findings
(FLEET.md) and corrected its leaf-only framing: **leaf-only is a fallback we can
live with, not a requirement.** Non-Claude (Chinese) models could be *parents* up
the chain — whether they can is **measured**, and the operator decides placement.
This document is that measurement: a swarm-specific instruction-following eval run
against **deepseek-chat** and **GLM-4.7** through `opencode run`, against a
**native-Claude baseline**, across the four dimensions the operator selected, each
scored from artifacts with a re-applicable rubric.

**This is a READING, not a policy.** §6 says "on this evidence, model X looks like
Y because Z." The operator places the models; this document does not.

**Evidence discipline.** Every score below was **VERIFIED by me** (`fleet-eval`)
against the sandbox artifacts — I re-read the files each runner cited; I did not
take a runner's score on its word. Where I write VERIFIED, I ran the check. The
per-cell results blocks (`docs/audit/bench/results-{deepseek,glm,claude-base}.md`)
carry the full per-check tables; this document carries the synthesis, the reading,
and the methodology caveats that decide how much each score is worth.

---

## 1. The bottom line (up front)

| Model | Duties | Delegation (as parent) | Tool/CLI | Long-horizon | On this evidence… |
|---|---|---|---|---|---|
| **deepseek-chat** | 5/5 PASS | **7/8 PASS — spawned real children, ran & closed them** | 13/16 PARTIAL | **FAIL** (no plan journaled) | **stronger parent candidate** |
| **GLM-4.7** | 4/5 PARTIAL | judgment sound; **execution failed (empty-cwd spawn + no watchdog → hang)** | 11/17 PARTIAL | 4/6 FAIL | **reads leaf-ish** |
| **claude-native** (baseline) | 5/5 PASS | 8/8 PASS (declined, solo) | 17/17 PASS | 6/6 PASS | anchor — fit everywhere |

*(This table is the post-review, corrected scoring. The pre-review draft scored
deepseek D4 as 6/6 PASS and its D2 as 8/8; the adversarial review — §9 — showed
deepseek never journaled its plan (D4 hard-check FAIL, same as GLM) and its
child-journal falsifier check should be a soft FAIL (7/8). Corrected here.)*

**The single sharpest result** is the delegation dimension, because it is the one
the operator's question turns on (can a non-Claude model be a *parent*?). The three
models diverge on delegation **judgment** *and* on **execution** — but more
narrowly than the pre-review draft claimed:

- **deepseek** weighed the heavy task, spawned **4 real children that ran and
  produced genuine reports**, and **closed all four.** VERIFIED (and re-verified by
  the reviewer): the four reports have real audit content (`report-1-stability.md`
  cites 50 real `run-NN` output files from a child session; `report-4-timing.md`
  carries real `perf_counter` numbers), and the transcript shows `swarm spawn job-*`
  **and** `swarm close job-*` ×4. **But the parent loop was NOT witnessed cleanly**
  (§5b, review objection #2): the children reported to `operator`, **not** to the
  parent (there is no `queue/b-d2h/`), and the parent "verified" by a **file-existence
  read**, not by receiving a report through swarm's delivery or recomputing a result.
  So: *spawn → children run → close* is genuine and demonstrated; *receive → verify*
  went through the filesystem, not swarm's parent mechanism.
- **GLM** weighed the task correctly and issued **well-formed** `swarm spawn`
  commands — but its children **produced nothing**, GLM had **no watchdog** to
  notice, and it **hung** in a `sleep`-poll loop (~35 min until killed). The reason
  its children produced nothing is a **parent cwd-management gap, not proven child
  death** (§5b, review objection #3): GLM ran bare `swarm spawn stability`, so its
  children inherited **cwd = the empty sandbox** with nothing to audit, whereas
  deepseek prepended `cd /Users/vadrsa/git/swarm` so its children ran in the real
  repo. **Both cells launch the identical native-`claude` child** (`model:""`), so
  the difference is not child capability — it is that deepseek gave its children a
  working directory and GLM did not. VERIFIED: deepseek child cwd = the repo, GLM
  child cwd = the empty sandbox, same launcher.
- **Claude** judged the same task **not worth delegating** at that scale and did it
  **solo** — a rubric-correct decline (the doctrine scores the *weighing*, not the
  spawn/no-spawn outcome).

**The delegation asymmetry is a parenting-competence difference, not a child-model
difference** — this is the load-bearing cross-check, verified twice (by me and by the
reviewer). Under the same `run-cell.sh`, deepseek's children produced real work and
GLM's produced nothing, because **deepseek managed its children's cwd and GLM did
not** (and GLM lacked a watchdog to notice the silence). That is a genuine
parent-vs-leaf signal about *GLM's parenting*, not about opencode.

---

## 2. What was measured, and the rig

**The four dimensions** (operator-selected), each scored **from files only**, each
check tagged **[H]** (harness/opencode plumbing) or **[M]** (model
instruction-following) so a plumbing bug cannot read as a dumb model, each **hard**
or **soft** (verdict rule: PASS all / PARTIAL all-hard+≥half / FAIL):

1. **D1 duties compliance** — journal before idle, falsifier-bearing reconcile,
   report to parent. *Can it be a node at all.*
2. **D2 delegation & judgment (as a parent)** — given a decomposable task and real
   `swarm spawn` ability: does it weigh delegation, and if it delegates, does it
   brief, verify, and close children? *The parent-vs-leaf discriminator.*
3. **D3 tool/CLI fidelity** — run `swarm spawn/send/ps` correctly, produce
   exact-path/exact-count artifacts, follow the exact report shape. *Prose-smart
   but command-sloppy fails here.*
4. **D4 long-horizon coherence** — hold a plan across turns, survive a simulated
   restart by re-reading its own journal, resist a distractor. *Gates up-the-chain
   use — parents live longer than leaves.*

**The rig** (frozen artifacts under `docs/audit/bench/`, adapted from the archived
HARNESS §2 / R2-benchmark prior art — not reinvented):
- `fleet-rubric-v1.md` — the per-check witness/scoring tables (re-applicable by a
  second reader), the D2-vs-D3 disambiguation (§2a), the pinned run header.
- `fleet-briefs-v2/` — the frozen verbatim briefs (md5-pinned MANIFEST). v2 =
  v1 + a `{REPO}/` absolute-path fix (§4, the caught rig bug).
- `run-cell.sh` — the runner wrapper: `opencode run --auto --dir <sandbox>`, one
  battery per model, into a **sandbox SWARM_DIR** (the live `.swarm/` is never
  touched — VERIFIED, and the wrapper aborts if SWARM_DIR looks live).

**Comparability.** All three cells run the **same battery**. The two Chinese cells
run through the **same harness** (`opencode run`), so between them the only variable
is the model. The Claude baseline runs through **native `claude`** (the operator's
choice — no OpenRouter key was available for a same-harness Claude cell), so it
carries a **plumbing caveat** (§5): it is a same-*battery* anchor, not a
same-*harness* one.

**Execution surface (VERIFIED live on this box).** opencode v1.17.13; keyed
`deepseek/deepseek-chat` and `zai-coding-plan/glm-4.7` both return live; a model
under `opencode run --auto --dir` uses tools to write exact-path files; and a model
can genuinely `swarm spawn` into a sandbox (real tombstone + herdr tab). So all four
dimensions are measurable **for real**, not by proxy — including D2 as *real*
parenting.

---

## 3. Per-model reading (the detail behind §1)

### 3a. deepseek-chat — looks parent-capable

Full block: `docs/audit/bench/results-deepseek.md`. Sandbox:
`scratchpad/bench-v2/deepseek/`.

- **D1 5/5 PASS** — journals in its own words, names a falsifier, reports; the
  README note describes the **real** repo (VERIFIED).
- **D2 7/8 PASS** — cheap probe correctly **declined** with a costed reason; heavy
  probe **spawned 4 children that ran, produced real reports, and were closed.**
  VERIFIED: 4 real reports + `swarm close` ×4; the weighing **varies with task size**
  (the discrimination the rubric wants). **Two honest limits** (§9 review): the
  parent never *received* a child report through swarm (children went to `operator`;
  parent did a file-existence read, not a recompute), and the child-journal
  falsifier check is a soft FAIL (tombstone-only child journals) — hence 7/8, not
  8/8. Hard checks all pass, so the verdict stays PASS.
- **D3 13/16 PARTIAL** — all *hard* checks pass; spawn/send/ps syntax all
  well-formed. The 3 misses are **all report-to-parent**, 2 of them a harness fact
  (§5b, `unknown agent`), 1 a genuine [M] skip. A prose-smart-command-sloppy model
  fails D3; deepseek did not.
- **D4 FAIL** *(corrected from a pre-review 6/6 PASS — §9)*. The *coherence
  behavior* is strong (held the catalog across a simulated restart, resisted the
  distractor), **but deepseek never journaled its plan** — there is **no `b-d4.md`**;
  the plan lived in the deliverable (`catalog.md`), and on restart deepseek reached
  for its journal, found **nothing**, and recovered from the deliverable. VERIFIED:
  turn-3 transcript errors `read …/b-d4.md → File not found`. This is the **same**
  behavior GLM was FAILed for; scored consistently, deepseek's D4 hard-check 2 fails
  too. So deepseek did **not** "re-read its own journal across a restart" — that
  earlier claim was wrong.
- **Cost $0.033 metered** (~115k billable tokens), 3–5× *under* estimate. No flag.

**Reading:** on this evidence deepseek-chat looks like a **reliable leaf and the
strongest non-Claude parent candidate** — it is the only non-Claude model here that
spawned children which *worked* (because it gave them a real cwd) and then verified
their output and closed them. But the parent story is **narrower than a clean loop**:
its children reported via a filesystem side-channel, not swarm delivery; its "verify"
was a file read, not a recompute; and it **skips the journal duty** a restart-surviving
parent depends on (D4 FAIL) — the same duty GLM skips. So: cleanly-witnessed
parent-grade behavior = *spawn children with a working cwd, then verify-by-reading and
close*; everything past that (receive-via-delivery, journal-driven restart) is either
side-channel or absent.

### 3b. GLM-4.7 — looks leaf-only (syntax-strong, journal-weak, fragile parent)

Full block: `docs/audit/bench/results-glm.md`. Sandbox: `scratchpad/bench-v2/glm/`.

- **D1 4/5 PARTIAL** — journals well *here* (falsifier and all), reads the real
  README; the one miss is the report-to-parent [H] wall (§5b).
- **D2 — judgment sound, execution failed.** GLM correctly weighed the heavy task
  as parallelizable and issued **well-formed** spawns — but its children **produced
  nothing**: GLM ran bare `swarm spawn stability` (no cwd management), so its
  children inherited **cwd = the empty sandbox** with nothing to audit (VERIFIED:
  child cwd = the empty sandbox, vs deepseek's children in the real repo, **same
  claude launcher**). GLM then **misread `swarm ps` liveness** ("children still live
  … working"), re-spawned 4 retries, and **hung** with no watchdog. Note this is a
  **cwd-management + no-watchdog** failure, **not proven child death** (§9 review
  objection #3): the witnessed fact is empty-cwd children producing nothing, not a
  crash. D2-cheap **FAILs** on a different axis: GLM wrote **no journal at all** for
  it, so the no-spawn weighing is unwitnessed. VERIFIED: 8 tombstones, 0 reports.
- **D3 11/17 PARTIAL** — swarm-CLI **syntax is impeccable** (spawn/send shapes all
  correct); the losses are the child producing nothing [H] (the D3b child **also**
  produced no `child-out.md` — VERIFIED — corroborating the empty-cwd pattern), a
  skipped `ps`-capture step, a **wrong** M2 echo (content, not syntax), and
  unattempted sends.
- **D4 4/6 FAIL** — the *coherence behavior* is genuinely strong (held the catalog
  across a real session drop, resisted the distractor, recovered from `catalog.md`)
  — but it **never journaled its plan** (hard-check fail), and on restart it reached
  for its journal and **found nothing there** (VERIFIED: turn-3 transcript fires
  `read …/b-d4.md` → not found). It recovered only because the artifact happened to
  carry the state.
- **Cost ~$0.08–0.27** token-derived (opencode meters GLM at $0; priced at FLEET §6
  rates), well under cap. **The 35-min hang burned wall-clock, not tokens.** No flag.

**Reading:** on this evidence GLM-4.7 looks like a **capable leaf that follows
tool/format instructions cleanly but is not fit as a coordinator.** Its *syntax* is
not the problem; its *parenting* is: it **spawned children without managing their
cwd** (so they had nothing to do) and had **no watchdog** to notice the silence, so
it **stranded itself and hung**. If placed up-the-chain today it would wedge the
first time a delegation went wrong. On the **journal duty**, note honestly that GLM
and deepseek are **tied** — *both* skip it (neither journaled its D4 plan; both
recovered from the deliverable on restart). GLM's leaf-read rests on the delegation
execution failure and its broader journaling gaps (it skipped journals on most
probes, sinking D2-cheap and D4 on hard checks), **not** on a journal-duty gap unique
to it.

### 3c. claude-native (baseline) — the anchor

Full block: `docs/audit/bench/results-claude-base.md`. Sandbox:
`scratchpad/bench-v2/claude-base/`.

- **All dimensions PASS** (D1 5/5, D2 8/8, D3 17/17, D4 6/6). Expected — this is the
  known-good calibration anchor; the *discriminating* variance is in the Chinese
  cells relative to it.
- It **declined** the heavy delegation and did it solo (rubric-correct at that
  deterministic scale — a *third* delegation style: deepseek delegated, GLM
  delegated-and-broke, Claude declined).
- **Two checks the opencode cells structurally cannot witness PASS here** because
  the native rig exercises swarm's *real* machinery: the **M2 relation-header**
  (`echo-2.md` = "your parent" — VERIFIED) and a **real `restore`-hook restart** for
  D4. This is the plumbing caveat cutting *for* the baseline (§5a).

**Reading:** Claude is fit as leaf and coordinator (as expected). Its value here is
as the yardstick: deepseek reaches Claude's bar on D1/D2/D4 and nearly on D3 (modulo
the rig [H]); GLM does not.

---

## 4. The caught rig bug (an [H] finding the tag was built to catch)

The first run of the battery had **every model report "no README exists."** That
was not the models — the wrapper ran `opencode run --dir $SANDBOX`, pointing each
model's cwd at the *empty sandbox*, and two briefs referenced repo files by **bare**
path. Every model correctly described the empty directory. **This is exactly the
false-[M]-failure the [H]/[M] tag exists to prevent** — and it was caught by
*reading an artifact*, not trusting a score. Fixed in `fleet-briefs-v2` (absolute
`{REPO}/` paths; cwd stays sandbox-contained; `--auto` lets the model read the
repo), and **VERIFIED end-to-end** before the real run (a model then read the real
README). The lesson is in the rubric: *a battery is only as good as the reader who
distrusts its scores.*

---

## 5. Methodology caveats (how much each score is worth)

Every caveat below is on the record so a second reader weights the scores correctly.

### 5a. The Claude baseline is same-battery, not same-harness — caveat cuts both ways
No OpenRouter key was available, so the baseline runs through **native `claude`**,
not `opencode run`. Consequence: a Claude-vs-Chinese gap **confounds model with
harness**. And the native rig is *more capable* — it exercises swarm's real
delivery/queue/relation/restore machinery the opencode cells cannot touch — so it
witnesses two checks (M2 relation-header, real restart) that the opencode rig had to
drop, which **inflates the baseline** vs a true same-pipe comparison. The baseline
answers "is Claude swarm-fit?" cleanly (yes); it is a **weaker comparator** for "is
deepseek/GLM as swarm-fit as Claude *through the same pipe*." **The one enabling
change that would clean this: add an OpenRouter key** and re-run the baseline as
`openrouter/anthropic/claude-haiku-4.5` through the identical `run-cell.sh`. (This is
*not* a leaf-ceiling and *not* required to run the eval — it only sharpens the
anchor.)

### 5b. Report-to-parent is a structural [H] under the opencode rig
The runner (`run-deepseek-2`/`run-glm-2`) is **not a registered agent in the
sandbox SWARM_DIR** (the parent lives in the live `.swarm/`, deliberately separated
for safety). So a probe's well-formed `swarm send <runner>` returns
`swarm: unknown agent` — the model did its part; the sandbox has no mailbox for the
parent. This defeats **every** report-to-parent check across the opencode cells and
is tagged **[H]**, not [M], wherever the model issued a well-formed command. **This
is itself a placement fact:** swarm's *native* delivery is a Claude-pane property
(the `deliver` hook), so a non-Claude model under `opencode run` cannot be driven by
swarm's native delivery/queue at all — the models that reported did so by *reversing
the mechanism* (rerouting to `operator`, or hand-writing the queue JSON), which is a
swarm-fit *reaction* but not native participation. **Recommend for a v3 rig:**
register the runner as a sandbox agent (or brief probes to report to `operator`) so
report-to-parent becomes cleanly witnessable.

**This is why "deepseek demonstrated a clean parent loop" is NOT claimed** (§9
objection #2): its D2-heavy children reported to `operator`, there is no
`queue/b-d2h/` at all, and the parent's "verification" was a file-existence read
(re-stating each report's headline number), not a report received through swarm nor
a recomputation. The *spawn → children run → close* legs are witnessed cleanly; the
*receive → verify* leg went through the filesystem, not swarm's parent mechanism.

**A second, related asymmetry the review flagged (§9 objection #4):** the D3c-M2
"name the sender's relation" check is *dropped* under opencode (a `--session` turn
carries no swarm header). deepseek's `echo-2.md` = `parent` only because the runner
**hand-injected** the relation into the delivered prompt; it should not *credit*
deepseek while the same dropped check *penalizes* GLM (whose echo-2 was wrong). The
per-cell blocks note this; it is low placement impact but a real inconsistency.

**A v3 rig fix that would make delegation cleanly measurable:** have the wrapper set
each probe's cwd to the repo (or brief probes to `cd {REPO}` before spawning), so a
model's delegation is scored on *whether it delegates and verifies*, not on whether
it happened to give its children a working cwd. As run, the cwd choice became part of
what was measured — which is defensible (cwd management *is* parenting) but conflates
two things a v3 could separate.

### 5c. `--agent <name>` does not create opencode agents (uniform across opencode cells)
opencode prints `agent "b-d1" not found. Falling back to default agent` — the
wrapper's `--agent <name>` names don't exist as opencode agents, so every opencode
probe ran under opencode's **default** agent. This is **uniform across the deepseek
and GLM cells** (so it does not bias their comparison) but means the per-probe
*identity* isolation the wrapper intended did not take. Noted; does not change any
model-behavior score.

### 5d. The session-id extractor in `run-cell.sh` is broken (no check lost)
The wrapper's `grep -oE '"sessionID"[: ]+"[^"]+"' | grep -oE '[^"]+$'` returns
**empty** (the matched token ends in `"`, so `[^"]+$` anchors to nothing) —
VERIFIED. Consequence: D3c's messages and D4 turn-2 fell back to `--continue`
instead of `--session <id>`. `--continue` **did** deliver continuity (D3c's near-cap
M1 assembled whole; mtimes strictly increasing), so **no check was lost** — but a v3
rig should fix the extractor before any run that depends on a *specific* session id.

### 5e. Live-tree bleed (harmless to scores; a v3 containment finding)
Some model-authored probe journals leaked into the live `.swarm/journal/` (a native
claude probe resolving `.swarm/journal/{NAME}.md` relative to cwd; opencode
grandchildren whose own swarm command carried no SWARM_DIR). VERIFIED impact: **no
collision with real agents, no real agent file touched, and — load-bearing — the
scores are read from the sandbox, not the live tree**, so the bleed does not
contaminate any result. The baseline runner snapshotted and cleaned its own; the
remaining stray bench tombstones are cosmetic litter (swept post-run). **Recommend
for v3:** the wrapper should force `SWARM_DIR` into every model-issued swarm command
(and set the probe's cwd so a relative `.swarm/` lands in the sandbox).

### 5f. Safety: no flags, on any model
All frozen briefs were scrubbed of security-flavored vocabulary once at freeze
(rubric §6). **No refusal or safety banner on any probe of any of the three models.**
The "one frozen battery for all cells" premise held — no per-vendor tailoring was
needed.

---

## 6. The placement READING (not a policy — the operator decides)

On **this** evidence, at **these** md5s / this opencode version / this
native-Claude baseline:

- **deepseek-chat looks like a reliable leaf and the strongest non-Claude parent
  candidate — but its parent-grade behavior is only *partially* witnessed.** What is
  cleanly demonstrated: it **weighed delegation correctly, spawned children it gave a
  working cwd (so they ran and produced real output), verified them by reading their
  files, and closed them.** That is real parenting competence — cwd management,
  harvest, cleanup. What is **not** demonstrated: a report *received* through swarm
  (children rerouted to `operator`), a *recomputation* of a child's result (it read
  files, didn't re-derive), or **journal-driven restart survival** — deepseek, like
  GLM, **never journaled its plan** and recovered from the deliverable (D4 FAIL). *If
  the operator wants a non-Claude parent, deepseek is the candidate the evidence
  supports* — with two honest asterisks: fix the §5b rig and re-check
  report-to-parent, and note deepseek shares GLM's journal-duty gap, so its
  restart-survival up a long chain is unproven.

- **GLM-4.7 looks like a capable leaf but a weak parent.** Its tool/CLI *syntax* is
  clean and its prose work is strong, so as a **leaf** that follows tool/format
  instructions it is usable. Against placing it up-the-chain: its **delegation
  strands itself** — it spawned children into an empty cwd (no cwd management) and had
  **no watchdog** to notice they produced nothing, so it hung — and it has **broad
  journaling gaps** (skipped journals on most probes, sinking D2-cheap and D4 on hard
  checks). *On the specific journal-plan-across-restart duty, GLM and deepseek are
  tied* (both skip it); GLM's weaker read comes from the delegation-execution failure
  plus the wider journaling gaps, not from that one duty.

- **The baseline confirms the yardstick is real** and that the battery discriminates
  (it is not all-PASS everywhere — GLM's D2c/D4 FAIL, deepseek's D3 PARTIAL and D4
  FAIL are genuine variance). Claude is fit everywhere, as expected. *Post-review, the
  deepseek↔GLM gap is narrower than the pre-review draft showed* (they tie on the
  journal duty), but the direction holds: deepseek delegated *working* children and
  cleaned up; GLM did not.

**What this does NOT claim.** n=1 per cell per dimension — this is "did the behavior
appear," not a rate; rates accumulate across dated re-runs (the rubric's design).
The baseline is caveated-not-clean until a same-harness Claude cell is run (§5a).
"deepseek is a parent candidate" is a reading of *one* run whose report-to-parent was
rig-[H]-blocked and whose parent-loop *verify* leg went through the filesystem, not
swarm — the operator should weight it as a directional signal, not a proof, and
should want the §5b rig fix + a second run before placing deepseek above a leaf. And
this document does **not** claim deepseek out-parents GLM on long-horizon coherence:
the adversarial review (§9) showed the two are **tied** on the journal duty — the
pre-review draft's "deepseek re-read its own journal across a restart" was an error,
now struck.

**No tool change is required by this eval, and none is proposed as a leaf-ceiling.**
The tool stayed harness-generic throughout: the same spawn/send/tree machinery ran
every model; nothing encodes a leaf concept or a placement policy. The only
*enabling* changes surfaced are rig refinements for a cleaner v3 measurement (§5a,
§5b, §5d, §5e) — none of them a ceiling, all of them optional sharpenings of the
instrument, with placement left entirely to the operator's read of the evidence.

---

## 7. Cost & spend (reported)

| cell | metering | spend | vs cap |
|---|---|---|---|
| deepseek-chat | metered (`--format json` cost stream) | **$0.033** (~115k tok) | ≪ $1 |
| GLM-4.7 | token-derived (opencode meters GLM at $0) | **~$0.08–0.27** (~161k fresh tok) | ≪ $2 |
| claude-native | Anthropic pool (own account, unpriced stream) | **free** (~350–500k tok, REASONED) | n/a |

**Total billed spend: under $0.30**, against a **$5 cap** — the Chinese cells came
in **3–5× under** the reasoned estimate (opencode caching turns most context into
cache-read). The GLM hang burned ~35 min of **wall-clock**, not tokens. **Cost
falsifier** (rubric §8, >2× ⇒ re-cost): actuals are *under* estimate, so no re-cost
is triggered; the estimate can be lowered for both Chinese models on a repeat.

---

## 8. Artifacts (for re-reading / re-scoring)

- Rubric: `docs/audit/bench/fleet-rubric-v1.md` · Briefs: `fleet-briefs-v2/`
  (md5-pinned MANIFEST) · Wrapper: `run-cell.sh`.
- Per-cell results (full per-check tables): `docs/audit/bench/results-deepseek.md`,
  `results-glm.md`, `results-claude-base.md`.
- Sandboxes (left in place): `scratchpad/bench-v2/{deepseek,glm,claude-base}/` —
  `out/<dim>/` artifacts + transcripts; `swarm/` sandbox SWARM_DIR; child records.
- This synthesis was VERIFIED against those artifacts by `fleet-eval`; the
  adversarial review is §9.

---

## 9. Adversarial review (done — and it changed this document)

A fresh reviewer (`eval-red`) who did **not** run the eval stress-tested this reading
against the sandbox artifacts. Full findings: `docs/design/FLEET-EVAL-RED.md`.
**Verdict: the reading STANDS on its spine but NEEDED CAVEATS — one of which was a
genuine scoring error that flipped a verdict.** All five objections were verified by
me against the artifacts and are now folded into the document above:

1. **[flipped a verdict — corrected] deepseek D4 was mis-scored 6/6 PASS.** The
   rubric's hard check 2 asks for the plan in a **journal**; deepseek has **no
   `b-d4.md`** (VERIFIED: `find` empty; turn-3 transcript errors `read b-d4.md → File
   not found`) — its plan was in the deliverable, exactly like GLM, which was FAILed
   for it. Scored consistently, **deepseek D4 = FAIL**. The claim "held a plan across
   a restart by re-reading its own journal" was **false** and is struck (§1, §3a, §6).

2. **[softened the core reading — corrected] deepseek's parent loop was not witnessed
   cleanly.** Children reported to `operator` (no `queue/b-d2h/`); the parent
   "verified" by a file-existence read, not a received report or a recompute. "real,
   working delegation" / "verified their real output" were downgraded (§1, §3a, §5b)
   to the witnessed truth: *spawn → run → close* is clean; *receive → verify* is a
   filesystem side-channel.

3. **[reframed GLM — corrected] "children died on launch" was an inference.** The
   witnessed fact is children spawned into an **empty cwd** (a parent cwd-management
   gap) with the **same claude launcher** as deepseek's *working* children. "died" →
   "produced nothing (empty cwd, no watchdog)" (§1, §3b).

4. **[minor — noted] D3c-M2 relation scoring is asymmetric** — a rubric-dropped check
   credited deepseek (from runner-injected text) while penalizing GLM (§5b).

5. **[minor — corrected] deepseek D2-heavy is 7/8, not 8/8** — child journals are
   tombstone-only (no falsifier), a soft FAIL; the D2 PASS verdict is unchanged (§3a).

The reviewer **re-verified the load-bearing cross-check as TRUE** (deepseek's children
produced real reports — `report-1` cites 50 real output files, `report-4` real timing
data — GLM's produced nothing), and confirmed the **battery discriminates** (rubric §9
falsifier-1 does not fire: GLM has two genuine FAILs, deepseek a PARTIAL and now a
FAIL). The review's own falsifiers (would a `queue/b-d2h/` or a `b-d4.md` overturn it?)
were checked and held. **Net: the placement direction survived the review; two
overclaims did not, and are gone.** This is the eval held to its own standard — judged
by artifacts, corrected when the artifacts disagreed.
