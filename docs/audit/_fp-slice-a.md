# fp-slice-a — falsifier forensics: field-tester, hardener, updater

Auditor: fp-slice-a (child of falsifier-probe). Rubric: docs/audit/_falsifier-rubric.md.
Source journals read READ-ONLY and IN FULL (not just grep hits) — the forward-hunt for
class-(a) statements requires later entries. No journal file was modified.

Every `file:line` below is real and was read (VERIFIED). Counts are MEASURED. Inferences are
marked REASONED.

---

## field-tester.md

125 lines, 37 entries (MEASURED: `grep -c "^## "`), 38 grep-hits on "falsif". The grep-hit count is NOT the statement
count: several lines carry a MENTION (a report about another agent's falsifiers, or the *name*
of a SPAN test) alongside — or instead of — a statement of the agent's own.

### Statements table

| # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence |
|---|-----------|-----------------------------------------------|-------|---------|---------|----------|
| 1 | .swarm/journal/field-tester.md:7 | "Falsifier for this entry: if a prior evidence file or grandchild artifacts exist somewhere I didn't look, I'm redoing finished work." | (a) | a-independent | NOT-FIRED | Same line, VERIFIED: "journal had only the spawn entry, docs/audit/ empty, no grandchildren yet — so no work is lost". The witness is the repo dir + .swarm/agents/, not prose. |
| 2 | .swarm/journal/field-tester.md:10 | "Falsifier for this entry: if probe-a never reaches idle (no stop event within ~5 min), my instrument is broken, not the mechanism under test." | (a) | a-independent | NOT-FIRED | field-tester.md:13 VERIFIED: "3a: send→delivered ≤1s to idle probe-a (VERIFIED, poller)" — probe-a reached idle; the `.swarm/event/` stop fact named in :10 is the independent witness. |
| 3 | .swarm/journal/field-tester.md:13 | "Falsifier: if probe-a hand-reads the queue again despite instruction, 3c is contaminated and I need a different isolation." | (a) | a-independent | NOT-FIRED (for 3c; superseded) | field-tester.md:16 VERIFIED: "3c failed to isolate (probe-a backgrounded the sleep — turn ended early, payload hit idle pane…)". 3c died of a DIFFERENT cause than the falsifier named; the agent replaced it with 3d and re-registered the same falsifier (row 4). REASONED: the named observation (hand-read) did not occur; the test failed anyway. |
| 4 | .swarm/journal/field-tester.md:16 | "Falsifier for 3d: if probe-a's queue drains BEFORE its stop event, it hand-read the queue again and 3d is contaminated." | (a) | a-independent | NOT-FIRED | field-tester.md:19 VERIFIED: "#3 NOT FIRED (re-ring proven twice: 3.5s and 4s stop→delivery…)" — a measured stop→delivery gap is exactly the observation that the queue did NOT drain before the stop event. Witnesses named: queue/probe-a/delivered/*, .swarm/event/*. |
| 5 | .swarm/journal/field-tester.md:20 | "Falsifier for this reconciliation: any timestamp or quote in the evidence file failing to match the underlying files (.swarm/queue/probe-a/delivered/*, .swarm/event/*, poller log in session scratchpad, probe-a journal) — every claim there names its source." | (a) | a-independent | CANNOT-TELL | The journal never returns to re-audit the evidence file against those files. docs/audit/field-evidence-2026-07-09.md exists (VERIFIED, 15786 bytes) but no later entry or artifact settles the cross-check. NOTE: partly (b) — "poller log in session scratchpad" is not a repo file — but the queue/ and event/ witnesses are in-repo, so it is (a)-independent overall. |
| 6 | .swarm/journal/field-tester.md:24 | "Falsifier: \`ls .swarm/queue/field-tester/\` showing any non-delivered file after this timestamp without a corresponding new wake." | (a) | a-independent | NOT-FIRED | VERIFIED by me, 2026-07-12: `.swarm/queue/field-tester/` contains only `delivered/` (67 files). Zero non-delivered files. The falsifier is discharged by direct inspection — the cleanest (a)-independent in the whole slice. |
| 7 | .swarm/journal/field-tester.md:27 | "Falsifier: if the poller misses a child that spawned-and-closed within 3s, or the probe writes summaries out of OUTDIR, my accounting is wrong — cross-check its journal and pane at harvest." | (a) | a-independent | NOT-FIRED | field-tester.md:30 VERIFIED: "deleg-base-1: zero children (poller + agents-dir, corroborated by journal and pane)" — the named cross-check was performed and agreed. `.swarm/agents/deleg-base-1.json` exists (VERIFIED). |
| 8 | .swarm/journal/field-tester.md:31 | "Falsifier: if the after-run is executed with a materially different brief, model, or repo state, the comparison I promised is invalid — the protocol section in the evidence file is the checklist." | (a) | a-independent | NOT-FIRED | field-tester.md:37 VERIFIED: "Verified by diff: the branch differs from installed ONLY in spawn_header"; :40 "doctrine header confirmed present in its .task file"; :46 "header v1/v2 bookkeeping". The one-variable claim was actively re-checked, and the .task files are independent witnesses. |
| 9 | .swarm/journal/field-tester.md:34 | "Falsifier: same as cheap probe — poller missing a fast spawn-and-close child would corrupt the count; cross-check journal+pane at harvest." | (a) | a-independent | NOT-FIRED | field-tester.md:40 VERIFIED: "Heavy baseline verdict: zero children, 1 turn, 4m36s" with the harvest cross-check performed (journal detail about background shell jobs = pane/journal read). `.swarm/agents/deleg-heavy-base-1.json` exists. |
| 10 | .swarm/journal/field-tester.md:37 | "Falsifier: if the branch binary drifts (new commits) between now and the after-runs, re-diff before spawning or the one-variable claim is false." | (a) | a-independent | NOT-FIRED | field-tester.md:40 VERIFIED: "deleg-after-1 spawned 12:03:59Z via the branch binary (md5 ea5a148a...)"; :43 "header v2 (amended…; md5 2f46a901 recorded)". The md5s were taken at spawn time — drift was checked-for and the change (v1→v2) was DETECTED and bookkept rather than ignored. |
| 11 | .swarm/journal/field-tester.md:40 | "Falsifier: if deleg-after-1's task file lacked the doctrine sentences the after-run would be measuring nothing — checked, grep found them." | (a) | a-independent | NOT-FIRED | Same line, VERIFIED: "checked, grep found them." Discharged in the same breath as it was raised; the .task file is the independent witness. |
| 12 | .swarm/journal/field-tester.md:43 | "Falsifier: if the heavy after-probe's kids never appear in agents/ but its journal claims delegation, my poller method is broken, not the probe." | (a) | a-independent | NOT-FIRED | field-tester.md:46 VERIFIED: "FULL delegation under header v2 — 4 children (one per job, ~15s spawn cadence)". Children DID appear in agents/ — VERIFIED by me: `.swarm/agents/dh1-flake.json`, `dh1-refs.json`, `dh1-concepts.json`, `dh1-latency.json` all exist. Journal and agents/ agree; poller method sound. |
| 13 | .swarm/journal/field-tester.md:47 | "Falsifier for the whole measurement: any cell of the comparison table contradicted by the underlying agent records, poller logs, report mtimes, or queue files — every number in the evidence doc traces to one of those." | (a) | a-independent | CANNOT-TELL | The journal never re-audits the comparison table against agent records. docs/audit/field-evidence-2026-07-10.md exists (VERIFIED) but nothing later settles the cell-by-cell check. Honest CANNOT-TELL. |
| 14 | .swarm/journal/field-tester.md:53 | "Falsifier: if the probe finishes tasks without its completion notes reaching me AND without deliverables at the named paths, my watcher's done-condition is measuring the wrong thing." | (a) | a-independent | NOT-FIRED | field-tester.md:56 VERIFIED: "Baseline verdict (span-base-1…): 9/9 done SERIALLY, ~36s cadence" — deliverables landed and were counted; the done-condition fired correctly. |
| 15 | .swarm/journal/field-tester.md:56 | "Falsifier for the pair: different task set, brief, or arrival cadence between runs — both used span-tasks.txt verbatim, same standby brief, same burst discipline." | (a) | a-independent | NOT-FIRED | field-tester.md:62 VERIFIED: "Falsifier for the pair's validity: any difference between runs beyond the header (same tasks file verbatim, same brief, same burst discipline, same repo — all checked; binaries differ in spawn_header only, both diffs quoted in evidence)" — the agent re-checked and re-affirmed at harvest. |
| 16 | .swarm/journal/field-tester.md:59 | "Falsifier for this entry: if the subagent claim is false (no parallel execution), deliverable mtimes will show serial spacing — check at harvest." | (a) | a-independent | NOT-FIRED | field-tester.md:62 VERIFIED, explicitly and by name: "t2-t8 in a 12s mtime window (parallel subagent claim VERIFIED — my previous entry's falsifier resolved)". The model case of a pre-registered falsifier with an mtime witness, discharged at harvest. |
| 17 | .swarm/journal/field-tester.md:62 | "Falsifier for the pair's validity: any difference between runs beyond the header (same tasks file verbatim, same brief, same burst discipline, same repo — all checked; binaries differ in spawn_header only, both diffs quoted in evidence)." | (a) | a-independent | NOT-FIRED | Same line, VERIFIED: "all checked". Discharged in-entry against the tasks file, briefs, and binary diffs (all file-observable). |
| 18 | .swarm/journal/field-tester.md:65 | "Falsifier for the design: if the GO-gate is satisfiable without identity (e.g. a subagent polling for a GO file), rung 3 wasn't actually forced — check HOW gates were held at harvest." | (a) | a-independent | NOT-FIRED | field-tester.md:68 VERIFIED: "one identity held 7 gated conversations (peak 6 open)" — the harvest check named in the falsifier was performed; the gate WAS held by identity, not by file-polling. |
| 19 | .swarm/journal/field-tester.md:69 | "Falsifier for the verdict: if span-heavy-1's journal or artifacts show a dropped/confused stream state I missed (I spot-checked h1 and h7 in full, others by DONE-line + mtime), \"passed the span test honestly\" overstates." | (a) | a-independent | CANNOT-TELL | The agent itself flags the gap ("spot-checked h1 and h7 in full, others by DONE-line + mtime"). No later entry returns to complete the check; span-heavy-1's journal is not re-read. Honest CANNOT-TELL — the witness exists in principle (the journal is a file) but the journal never settles it. |
| 20 | .swarm/journal/field-tester.md:73 | "Falsifier for PR-B's verdicts: if hand-B's pane actually wrote its claim line somewhere I didn't look before the kill (checked: journal has no [hand-B] CLAIM qa line; desk/qa-status.txt absent), the alarm demonstration is staged rather than real." | (a) | a-independent | NOT-FIRED | Same line, VERIFIED: "(checked: journal has no [hand-B] CLAIM qa line; desk/qa-status.txt absent)". Discharged in-entry against two independent file witnesses (a journal grep and a file's absence). |
| 21 | .swarm/journal/field-tester.md:77 | "Falsifier: single-trial null — if a future harness version co-submits, the recheck recipe in the addendum exposes it in 30s." | (b) | — | — | OBSERVABLE-ELSEWHERE: the firing condition is a FUTURE harness version's behaviour in a live pane. No repo file records it; the recipe would have to be re-run by a human. The rubric's own example ("if a future harness version co-submits") is this line. |
| 22 | .swarm/journal/field-tester.md:81 | "Falsifier: if the child record's tab prefix were w4 despite focus on w9, there is no bug and the report's root cause is wrong — the record says w9, so the bug stands." | (a) | a-independent | NOT-FIRED | Same line, VERIFIED: "the record says w9, so the bug stands". The agent record (`.swarm/agents/<child>.json`) is the independent witness, quoted verbatim into docs/audit/field-evidence-workspace-2026-07-12.md (VERIFIED, file exists). |
| 23 | .swarm/journal/field-tester.md:85 | "Falsifier: if HERDR_WORKSPACE_ID were unset in real panes the fix would silently no-op — checked my own pane (w4) and the fix's fallback branch is explicit in the diff." | (a) | a-independent | NOT-FIRED | Same line, VERIFIED: "checked my own pane (w4) and the fix's fallback branch is explicit in the diff." The diff is a git artifact; corroborated independently by hardener.md:296-298 ("graceful-fallback via fake herdr argv log"). |
| 24 | .swarm/journal/field-tester.md:89 | "Falsifier for the rig: if the pump's injected text differs by one byte from what deliver_once would emit (header shape, truncation, oldest-first), the \"via swarm delivery\" claim is false — smoke test includes a byte-compare against build_delivery output." | (a) | a-independent | NOT-FIRED | field-tester.md:92 VERIFIED, by name: "Smoke: pump output BYTE-IDENTICAL to bin/swarm build_delivery (rig falsifier discharged)". Pre-registered, then discharged by a mechanical byte-compare. Textbook. |
| 25 | .swarm/journal/field-tester.md:92 | "Falsifier: if v3-run-ds's cell shows probes' sends attributed to v3-run-ds instead of b-* names, the identity pin didn't take and D-scores involving sends are contaminated." | (a) | a-independent | NOT-FIRED | field-tester.md:99 VERIFIED: "D2-heavy's receive→verify is now WITNESSED through the real queue (3 reports crossed delivered/, verified against artifacts, children closed)" — sends were attributed correctly enough to be witnessed per-child through the sandbox queue. REASONED: a failed identity pin would have collapsed those reports onto v3-run-ds; the entry instead reports per-child crossings. |
| 26 | .swarm/journal/field-tester.md:96 | "Falsifier for dp-f1's design: if an observer pane shows the swarm skill loading at session START (not on trigger) or any swarm vocabulary reached its prompt, that run measures contamination, not doctrine — the pristineness proof in findings.md is the check." | (a) | a-independent | NOT-FIRED | field-tester.md:102 VERIFIED: "the swarm skill never loaded despite every documented trigger condition" — the opposite of contamination; the pristineness held (indeed too well: it produced the trigger-gap finding). The named witness (findings.md pristineness proof) is a file. |
| 27 | .swarm/journal/field-tester.md:99 | "Falsifier: if glm's cell shows different briefs md5s than ds's header, comparability is broken and the synthesis must say so." | (a) | a-independent | CANNOT-TELL | field-tester.md:108 reports the GLM cell in detail but never states the briefs-md5 comparison. :111 does say "D2-cheap FLIPPED vs v2 on a byte-identical brief" — but that is a v2-vs-v3 brief identity, not the ds-vs-glm md5 check this falsifier names. The journal never returns to it. Honest CANNOT-TELL. |
| 28 | .swarm/journal/field-tester.md:102 | "Falsifier for my (a) call: if the trigger phrase itself is judged coaching by the adversarial reviewer, runs 3/4 measure phrase-compliance, not doctrine — mitigated by the phrase saying nothing about tree shape." | (a) | a-self-report | NOT-FIRED | The witness is the adversarial reviewer's (dp-red's) judgment — which WAS in fact recorded: field-tester.md:121 VERIFIED, "dp-red spawned with six specific attack lines including baseline validity and trigger-phrase coaching", and :124 lists dp-red's verdicts — the trigger-gap finding was PROMOTED ("trigger gap leads"), not struck as coaching. Flagged a-self-report because the reviewer's verdict reaches the repo only via field-tester's own narration of it (dp-red's journal exists but the falsifier does not name it). |
| 29 | .swarm/journal/field-tester.md:105 | "Falsifier for the F2 design: if phase-1 momentum is too thin (tool trivially known from the goal text alone), the context-token grep can't distinguish mined briefs from cold ones — the fixture quirks and flag decisions are the deliberately unguessable tokens." | (a) | a-independent | NOT-FIRED | field-tester.md:114 VERIFIED: "briefs carry unguessable phase-1 tokens 18/18 and 15/16" — the grep discriminated, so momentum was not too thin. The .task files are the independent witness. (See row 30 for the twist: the reviewer later attacked the PROVENANCE of this, not the token count.) |
| 30 | .swarm/journal/field-tester.md:108 | "Falsifier for the cross-cell comparison: if cb's briefs md5s or scoring conventions differ from the two v3 results files, the anchor is off-battery and the synthesis must not treat it as comparable." | (a) | a-independent | NOT-FIRED | field-tester.md:111 VERIFIED: "claude-base 38/38 clean sweep… same battery"; :117 "37/37+1 restated" after review corrections — the results files were re-audited by v3-red against the battery, and the synthesis DID adjust (ds D2 flipped to 8/10 FAIL) rather than assert comparability blindly. Witnesses: results-v3-*.md. |
| 31 | .swarm/journal/field-tester.md:111 | "Falsifier for the synthesis: any §1 row not derivable from its results file's per-check table by the rubric's own verdict rule — exactly what v3-red is briefed to hunt." | (a) | a-independent | **FIRED-CHANGED** | See Notable §A. FIRING: field-tester.md:117 VERIFIED — "Review corrections folded (ds D2 flipped to 8/10 FAIL — LEVEL with GLM…)". A §1 row WAS non-derivable and v3-red found it. CHANGE: same line — corrections folded, "Errata appended to results-v3-deepseek.md", "§8 records v3-red's meta-finding verbatim". Course demonstrably changed. |
| 32 | .swarm/journal/field-tester.md:114 | "Falsifier for the baseline: if the restore lands before either observer's skill load, that observer read the DOCTRINE text and its run is void — the watcher's condition (agents/ non-empty = skill already loaded and acted) prevents exactly this ordering." | (a) | a-independent | NOT-FIRED — but the CLAIM it protected was later retracted for an unrelated reason | field-tester.md:121 VERIFIED: "Baseline recovered from the trust-gate stall (both observers had never started — zero contamination…)". The ORDERING hazard this falsifier names did not fire. NOTE (REASONED): the baseline arm was nonetheless retracted at :124 — "my 'pre-doctrine' text contained the treatment — I diffed for two paragraphs and never read the rest" — a DIFFERENT flaw the falsifier did not cover. Precision-of-the-wrong-thing, not a firing. |
| 33 | .swarm/journal/field-tester.md:118 | "Falsifier: if the operator's read of results-v3-* finds another cross-cell inconsistency v3-red missed, my verification pass was too shallow — the per-check tables are the audit surface." | (b) | — | — | OBSERVABLE-ELSEWHERE: fires on **the operator's private read**. Nothing in the repo records whether the operator found another inconsistency. The per-check tables are files, but the FIRING EVENT (operator noticing) is not. |
| 34 | .swarm/journal/field-tester.md:121 | "Falsifier for the whole file: any of the four flat-spawn collector outputs not reproducible from the clones' agents/ records — dp-red is briefed to recount them from the raw trees." | (a) | a-independent | **FIRED-CHANGED** | See Notable §B. FIRING: field-tester.md:124 VERIFIED — "F1's flat rows are a TOOL fact — my_name() hard-codes root spawns to parent=operator". The flat rows were NOT what the collector claimed they measured; dp-red recounted from the raw trees exactly as briefed. CHANGE: same line — "baseline arm retracted", "the corrected file is the record", both headlines flipped. |
| 35 | .swarm/journal/field-tester.md:125 | "Falsifier for this reconciliation: any claim in the corrected evidence file still resting on a runner's findings text where the underlying clone/journal/code artifact disagrees — dp-red's method (never read the findings file first) is the audit procedure." | (a) | a-independent | CANNOT-TELL | Final entry of the journal. Nothing follows it; the agent goes idle. The witness (clones, journals, code) exists in principle, but no later entry or artifact settles it. Honest CANNOT-TELL — and the expected shape for a journal's last falsifier. |

### MENTIONS (not statements) — field-tester

VERIFIED, each read in place:
- `:16` — "#4 NOT FIRED (probe-a + hardener journals both carry command-checkable falsifiers, quoted in evidence file)" — a report ABOUT OTHERS' falsifiers (this is field-tester's WATCHLIST-#4 verdict, i.e. the same audit I am doing). Mention.
- `:19` — "#4 NOT FIRED (all sampled entries carry checkable falsifiers)" — same, a verdict about others' falsifiers. Mention.
- `:53` — "Operator assigned SPAN.md §6 falsifiers 1-3" — names of tests in a design doc. Mention.
- `:56` — "Watcher includes a 20s post-drain window to catch absorb moves (falsifier 3)." — names SPAN test 3. Mention.
- `:59` — "SPAN falsifier 1: the flood forced NO tree response at this size" AND "Falsifiers 2/3: UNTESTABLE (no coordinator/layer existed)." — names of SPAN §6 tests, reported on. Mentions (2). The entry's OWN statement is row 16.
- `:64` — heading "## 2026-07-10 13:39Z — heavy flood launched (SPAN falsifier 1')" — test name in a heading. Mention.
- `:65` — "Watcher has a 90s post-drain absorb window (falsifier 3)." — SPAN test name. Mention.
- `:68` — "F2/F3 still untestable after three floods." — SPAN test names (no "falsif" string, so not in the grep, but the same class). Not counted in the 8 below.
- `:95` — "onboarding-doctrine falsifiers 1 (coordinator stance) + 2 (mine-first)" — names of doctrine tests being run. Mention. (This entry's OWN statement is row 26 at :96.)
- `:102` — "Falsifier 1 NOT-FIRED twice but vacuously" — a verdict on the DOCTRINE's test F1, not on field-tester's own trajectory. Mention. (Own statement is row 28, same line.)
- `:105` — "Interim FIRED report sent… with pre-registered falsifier survived" and "dp-f2 spawned: mine-first falsifier" — reports about the doctrine test. Mentions.
- `:114` — "F2: NOT-FIRED n=2" — doctrine-test verdict. Mention.

**Statement count reconciled against entry boundaries (MEASURED).** `grep -c "^## "` → **37 entries**.
Of those, **35 carry exactly one falsifier statement** (rows 1–35 above, one per entry, in order).
The two that carry none are:
- `:3-4` — the spawn entry (task text only).
- `:49-50` — the 2026-07-10 12:18Z closed-sender entry (ends "Idle."; no falsifier).

37 − 2 = 35, matching the 35 rows exactly. The gap between 38 grep-lines and 35 statements is
accounted for by the 12 MENTION clauses listed above, several of which share a line with a
statement (e.g. `:59` carries one statement and two mentions). VERIFIED.

### Counts — field-tester

- MENTIONS (not statements): **12** (MEASURED; listed above)
- STATEMENTS: **35**
  - (a)-independent: **32**
  - (a)-self-report: **1** (row 28)
  - (b): **2** (rows 21, 33)
  - (c): **0**
- OUTCOMES for (a) only (n=33):
  - FIRED-CHANGED: **2** (rows 31, 34)
  - FIRED-IGNORED: **0**
  - NOT-FIRED: **26**
  - CANNOT-TELL: **5** (rows 5, 13, 19, 27, 35)

### Notable — field-tester

**§A. FIRED-CHANGED (row 31) — the synthesis falsifier fired and flipped a headline.**
Registered at `field-tester.md:111` (2026-07-12 15:28Z):
> "Falsifier for the synthesis: any §1 row not derivable from its results file's per-check table
> by the rubric's own verdict rule — exactly what v3-red is briefed to hunt."

Fired at `field-tester.md:117` (15:50Z) — VERIFIED:
> "Review corrections folded (ds D2 flipped to 8/10 FAIL — LEVEL with GLM; pump-writes-delivered/
> disclosed with transcripts as the real witness; harvest-loop caveat restored; evidence claims
> scoped; 37/37+1 restated; bridgememory attempt was an unnoticed ERROR)."

The change of course is in the same sentence, and is structural, not cosmetic: "Errata appended
to results-v3-deepseek.md rather than editing the runner's tables silently", and §8 of
FLEET-EVAL-V3.md "records v3-red's meta-finding verbatim: where the draft was kind, it was kind
to the rig its author built." The agent registered a falsifier aimed at its own authorship bias,
paid an adversary to hunt it, the adversary found it, and the artifact changed. This is the
doctrine working exactly as designed.

**§B. FIRED-CHANGED (row 34) — the collector falsifier fired and RETRACTED a whole arm.**
Registered at `field-tester.md:121` (16:12Z):
> "Falsifier for the whole file: any of the four flat-spawn collector outputs not reproducible
> from the clones' agents/ records — dp-red is briefed to recount them from the raw trees."

Fired at `field-tester.md:124` (16:35Z) — VERIFIED:
> "(2) F1's flat rows are a TOOL fact — my_name() hard-codes root spawns to parent=operator,
> contradicting WORLD.md's operator-is-a-mailbox; baseline arm retracted (my 'pre-doctrine' text
> contained the treatment — I diffed for two paragraphs and never read the rest)"

The change: "dp-red flipped both my headlines and the corrected file is the record". The agent
also wrote the self-indicting line — "two independent reds caught the same author-bias direction
in my drafts today — the fresh-reviewer convention is load-bearing and I am not exempt from the
failure mode I measure in others" (`:124`, VERIFIED).

**§C. FIRED-IGNORED: ZERO.** MEASURED. I looked specifically for the pathology — a named
observation that demonstrably occurred with no course change — and did not find one in this
journal. The closest candidate is row 32 (`:114`), where the baseline arm the falsifier guarded
was later retracted (`:124`). But the falsifier's NAMED observation (restore landing before skill
load) did not occur; the arm died of a flaw the falsifier never covered. That is a
**falsifier aimed at the wrong hazard**, not a falsifier ignored. I record it as such rather
than inflate it into a pathology. (REASONED, stated as reasoning.)

### Reconciliation pairing — field-tester

- Entries the journal itself calls a reconciliation: **6** (MEASURED, VERIFIED by heading text)
  — `:18` "evidence file complete; reconciliation", `:45` "after-measurement complete; reconciliation",
  `:61` "SPAN pair complete; reconciliation", `:67` "heavy flood complete; reconciliation",
  `:71` "PR-A and PR-B complete; reconciliation", `:123` "doctrine probe shipped post-review; day's reconciliation".
- Of those, how many name a falsifier IN THE SAME ENTRY: **6 of 6** (100%). VERIFIED: :20, :47, :62, :69, :73, :125.
- Does it name falsifiers but then go idle / never reconcile again? **Partly — yes at the end.**
  The final entry (`:123-125`) is a reconciliation naming a falsifier that nothing ever returns to
  (row 35, CANNOT-TELL), and the journal ends there. That is the terminal-CANNOT-TELL shape and is
  structurally unavoidable for a last entry. Mid-journal, the pattern is the opposite of idle: this
  agent repeatedly returns to a prior entry's falsifier BY NAME (`:62` "my previous entry's falsifier
  resolved"; `:92` "rig falsifier discharged"). It is the strongest discharge discipline in my slice.

---

## hardener.md

299 lines, 20 entries (MEASURED: `grep -c "^## "`), 21 grep-hits on "falsif".

### Statements table

| # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence |
|---|-----------|-----------------------------------------------|-------|---------|---------|----------|
| 1 | .swarm/journal/hardener.md:14-15 | "Falsifier: full suite (test_swarm + test_swarm_process) not green from the worktree against the worktree's bin/swarm." | (a) | a-independent | NOT-FIRED | hardener.md:21-22 VERIFIED: "Full suite: 59 tests OK in ~11s, warning-free." The suite is a runnable, re-runnable artifact — an independent witness (anyone can re-run it). |
| 2 | .swarm/journal/hardener.md:24-27 | "Falsifier: \`cd /Users/vadrsa/git/swarm-hardening/tests && python3 -m unittest test_swarm test_swarm_process\` not printing OK/59, or \`git -C /Users/vadrsa/git/swarm status\` showing anything but clean main." | (a) | a-independent | CANNOT-TELL | The command is fully specified and independently runnable — the ideal (a)-independent form. But the journal never re-runs it; the worktree /Users/vadrsa/git/swarm-hardening no longer exists as a live check in any later entry. NOT-FIRED cannot be asserted from the journal alone. Honest CANNOT-TELL. NOTE: the second clause (clean main) was later contradicted-but-explained at :42-44 — see Notable §D. |
| 3 | .swarm/journal/hardener.md:41-44 | "Falsifier: \`cd /Users/vadrsa/git/swarm-naming/tests && python3 -m unittest test_swarm\` not OK/46; or main checkout dirtied (it shows only a sibling's untracked docs/audit/, not mine); or the operator/field-tester reproducing either defect against ae16ab3." | (a) | a-independent | NOT-FIRED (in part) / CANNOT-TELL (in part) | Clause 2 discharged IN-LINE, VERIFIED: "(it shows only a sibling's untracked docs/audit/, not mine)" — the agent checked git status and correctly attributed the dirt to field-tester. Clauses 1 and 3 are never revisited. I score the STATEMENT as NOT-FIRED on the strength of the in-line discharge of the only clause the agent could observe, and flag the residue honestly. |
| 4 | .swarm/journal/hardener.md:59-62 | "Falsifier: \`git -C /Users/vadrsa/git/swarm-world diff main --stat\` touching anything but WORLD.md, or the sentence not sitting immediately after the delivered/-record sentence in concept 4, or probe-a-class agents still hand-draining queues after this lands in a live tree." | (a) | a-independent | NOT-FIRED (clauses 1-2) | Clause 2 is checkable against the repo TODAY and I checked it: WORLD.md concept 4 (VERIFIED via `swarm world`) reads "…is the world-readable record that it consumed a turn. Never move your own queue files — delivery is the tool's job…" — the sentence sits immediately after the delivered/-record sentence, exactly as promised. Clause 3 ("probe-a-class agents still hand-draining queues") DID later fire elsewhere — field-tester.md:59 VERIFIED: "hand-READ its 8 undelivered queue files in one turn (WORLD.md's 'never read or move' sentence violated on the read half)". See Notable §E: hardener never learns this, and the fix was to NARROW the sentence (Task 7), not to treat it as a firing. |
| 5 | .swarm/journal/hardener.md:77-81 | "Falsifier: \`git -C /Users/vadrsa/git/swarm-delegation diff eac88e2 --stat\` touching anything beyond README.md/WORLD.md/bin/swarm(spawn_header string)/skill/SKILL.md, or spawn_header('example-agent','parent-agent') rendering over 8000 chars, or field-tester's after-probe showing agents briefed with this header still grinding parallelizable work serially." | (a) | a-independent | **FIRED-CHANGED** (clause 3) | See Notable §F. Clause 3 is a cross-agent falsifier and it FIRED: field-tester.md:43 VERIFIED — "deleg-after-1 (header v1): zero children, 1 turn, 83s" on a task field-tester itself called parallelizable. The header did NOT stop serial grinding. CHANGE: hardener.md:84-95 — "Task 4 amendment GREEN, branch rebuilt… Bidirectional reconcile (grow AND shrink) folded in", header 1364→1452 chars. The doctrine text was amended. (The causal chain runs operator→hardener, not field-tester→hardener directly; hardener's journal does not name the probe. REASONED.) |
| 6 | .swarm/journal/hardener.md:92-94 | "Falsifier: old commit ids (bfd6395..934d828) still reachable from the branch head, or spawn_header not containing \"keep a child only if you can name its next task\", or WORLD.md concept 9 missing the second sentence." | (a) | a-independent | NOT-FIRED | Clause 2 VERIFIED by me against the LIVE installed header — my own spawn task text (this session) contains verbatim: "keep a child only if you can name its next task". Clause 3 VERIFIED against `swarm world` concept 9: the shrink sentence is present ("The tree should match the remaining work: spawn what is missing, close what is done — keep a child only if you can name its next task."). Both discharged by independent inspection of shipped artifacts. |
| 7 | .swarm/journal/hardener.md:106-108 | "Falsifier: the new test passing against eac88e2's bin/swarm, or \`event stop\` observed blocking >~10s in a live tree with the fix, or any pane-read call appearing on the stop path." | (a) | a-independent | NOT-FIRED (clause 1 in-line) | Clause 1 discharged IN-ENTRY, VERIFIED at :104-105: "Regression test proven to bite: against pre-fix bin/swarm it dies at a 60s timeout; with the fix, <10s bound + zero-pane-read assertions pass." Clause 2 (live-tree blocking) is corroborated independently by field-tester.md:53 VERIFIED — "noted my stop-hook-stall finding already fixed on main (37cb2fa, re-ring single-attempt)". Cross-journal discharge. |
| 8 | .swarm/journal/hardener.md:124-127 | "Falsifier: header not containing \"over span when you can no longer name\", or skill missing the review-desk pattern, or diff touching anything beyond bin/swarm(spawn_header)/WORLD.md/skill/SKILL.md, or SPAN §6's flood test (falsifier 1) failing against agents briefed with this header." | (a) | a-independent | Clause 1 NOT-FIRED; clause 4 CANNOT-TELL-as-written | Clause 1 VERIFIED by me against the live header — my own task text contains "You are over span when you can no longer name each child's state and the next artifact you expect from it without re-reading." Clause 4 is the interesting one: field-tester.md:62 VERIFIED reports "F1 NOT FIRED / success-shape NOT OBSERVED (flood routed around the tree via queue hand-read + harness subagents)" — i.e. the flood test neither passed nor failed in the sense hardener meant; the probe evaded via harness subagents. hardener never learns this. I score the STATEMENT NOT-FIRED (clause 1 is decisive and checkable) and record the residue. |
| 9 | .swarm/journal/hardener.md:139-141 | "Falsifier: WORLD.md concept 4 still containing \"read or move\", or the reason clause differing from the pre-narrowing text, or §3d' naming a doctrine-text change I failed to apply." | (a) | a-independent | NOT-FIRED | Clauses 1-2 VERIFIED by me against the shipped contract (`swarm world`, concept 4): the sentence reads "Never move your own queue files — delivery is the tool's job, and a file moved by hand makes that record claim a turn that never happened." — "read or" is GONE, and the reason clause is byte-identical to the pre-narrowing text. Discharged by direct inspection of a git-tracked doc. |
| 10 | .swarm/journal/hardener.md:156-158 | "Falsifier: any diff outside the four named files, or the WORLD sentence deviating from the quote above, or the skill section missing one of F1/F2/F4/F5's named elements (checkable against the spec's SHIP list)." | (a) | a-independent | NOT-FIRED (clause 2) | Clause 2 VERIFIED by me against `swarm world`: "The operator queue alone is drained by its reader: the tool never delivers there — the human's side moves the mail to `delivered/` and journals the claim before acting on it." — byte-identical to the quote at :152-154. Clauses 1 and 3 are never revisited in the journal (git-checkable in principle). |
| 11 | .swarm/journal/hardener.md:171-173 | "Falsifier: skill bullet missing any of the five dispatch elements, or diff touching files beyond skill/SKILL.md + docs/design/SPAN.md, or the branch not containing fe0c8c6." | (a) | a-independent | CANNOT-TELL | Fully file-checkable in principle (skill text, git diff, branch ancestry) but the journal never returns to it, and no later entry or artifact settles it. Honest CANNOT-TELL. |
| 12 | .swarm/journal/hardener.md:183-184 | "Falsifier: bin/swarm still containing \"next turn\" in the doorbell note, or the process send test failing on the unchanged prefix." | (a) | a-independent | CANNOT-TELL | Both clauses are grep/test checkable against a git artifact — the ideal form — but the journal never re-checks, and no later entry settles it. Honest CANNOT-TELL. |
| 13 | .swarm/journal/hardener.md:201-204 | "Falsifier: any H-F1/H-F2/H-F3 test failing; a passed message re-authored; a reply from OPERATOR/asker; the hook invoked off the operator path; or the verb claiming before size-checking (checkable by reading cmd_engine_hook's order: decide -> size-check -> mv -> claim line -> reply)." | (a) | a-independent | SUPERSEDED → I score CANNOT-TELL | The entire surface this falsifier guards (the engine verb, H-F1/2/3 tests, cmd_engine_hook) was DELETED two entries later by operator directive — hardener.md:219-234 VERIFIED: "verb + grants + model call + decision prompt deleted from bin/swarm". The falsifier was never discharged; it was made moot. Not a firing, not a discharge. REASONED: CANNOT-TELL is the honest cell; "superseded" is the true story and I say so rather than round it to NOT-FIRED. |
| 14 | .swarm/journal/hardener.md:216-217 | "Falsifier: resuming without re-reading this entry, or committing before the suite is green again." | (a) | a-self-report | NOT-FIRED | This is a falsifier about the agent's OWN future conduct — its only witness is the agent's own later prose. And it was honoured, VERIFIED: :219-233 shows the resume DID re-read (the entry is a direct continuation, "Task 12 correction executed") and the commit was withheld until green — :232-233 "HELD: commits… Suite 76 OK". Textbook a-self-report, and a rare one that was actually kept. |
| 15 | .swarm/journal/hardener.md:231-233 | "Falsifier: any \"engine\" string surviving in bin/swarm/tests/WORLD-amendment (grep, excluding WORLD's pre-existing \"rule engine\" line), or a commit landing before the operator's spec, or the suite not OK/76." | (a) | a-independent | NOT-FIRED | hardener.md:250 VERIFIED: "grep: zero \"engine\" in bin/swarm, tests, WORLD amendment." Discharged by a mechanical grep — an independent, non-narrative witness. Clause 2 also honoured (:236 "built and committed" only after "the operator's final spec"). |
| 16 | .swarm/journal/hardener.md:254-256 | "Falsifier: suite not OK/77 from the worktree; or \"PASS\" sentinel logic queueing on dirty exit / not queueing on PASS (checkable in TestSendMiddleware); or the waiting message contradicting what I committed." | (a) | a-independent | **FIRED-CHANGED** (clause 3) | See Notable §G. The agent pre-registered "the waiting message contradicting what I committed" and then DELIBERATELY HELD ITS REPORT to check (:251-253 VERIFIED: "REPORT TO OPERATOR IS HELD until I read the waiting message next turn (it may amend; a stale report would waste an operator turn)"). It fired: the next entry (:258-274) is "Task 12 COMPLETE (final spec + **config amendment**)" — the branch was REBUILT AGAIN for a TOML `[middleware]` config section that the held commits did not have. Course changed. |
| 17 | .swarm/journal/hardener.md:271-273 | "Falsifier: registered_middleware not returning None on a config missing command; or a PASS line with dirty exit being queued as \"handled\"; or any middleware-named surface still reading .swarm/hook; or suite not OK/79." | (a) | a-independent | SUPERSEDED (PASS-sentinel clause) → NOT-FIRED overall | hardener.md:276-285 VERIFIED: the very next entry replaces the stdout PASS sentinel with an exit-code contract ("Exit-code contract replaced the stdout sentinel… stdout never read"), so clause 2 became moot by design change, not by firing. Clause 4 discharged in-line at :267 ("Suite 79 OK"). REASONED: NOT-FIRED, with the sentinel clause noted as superseded. |
| 18 | .swarm/journal/hardener.md:284-285 | "Falsifier: any code path reading middleware stdout; or exit 1 being treated as HANDLED; or suite not OK/80." | (a) | a-independent | NOT-FIRED | Discharged IN-ENTRY, VERIFIED at :281-283: "stdout never read. New test pins stdout-is-never-parsed. Suite 80 OK twice." Independently corroborated by the SHIPPED CONTRACT — `swarm world` (VERIFIED, read this session) now says "Its exit code is the whole verdict: 0 passes the message through… 100 means the middleware handled it… any other exit… passes the message through unchanged". Clause 2 is contract-level true. |
| 19 | .swarm/journal/hardener.md:296-298 | "Falsifier: a spawn with HERDR_WORKSPACE_ID=wX whose fake-herdr log lacks \"--workspace wX\"; or any diff beyond bin/swarm:905-917 + the two tests + the clean-room line." | (a) | a-independent | NOT-FIRED | Clause 1 discharged by hardener's own test (:293-294 "Tests: pins-to-w4 + graceful-fallback via fake herdr argv log") AND independently corroborated cross-journal — field-tester.md:84 VERIFIED: "Branch f0a52732 (one-site diff: --workspace from HERDR_WORKSPACE_ID): Test A (wA focused -> w4:t50), Test B… Test C… All PASS". The live verification hardener's entry says it is awaiting (:299 "Idle, awaiting field-tester verification") DID happen and PASSED — hardener just never journals learning it. |

### MENTIONS (not statements) — hardener

VERIFIED:
- `:127` — "SPAN §6's flood test (falsifier 1) failing against agents briefed with this header" — the phrase "(falsifier 1)" is the NAME of a SPAN test. It is embedded inside a genuine falsifier statement (row 8), so it is a mention riding inside a statement; counted once as a mention.
- `:164` — "(STANDING GOALS entry w/ falsifiers; restatement MUST cite superseded entry;…)" — this is a description of the DOCTRINE TEXT hardener is shipping (the skill bullet tells other agents to write falsifiers). Doctrine restatement, not hardener's own falsifier. Mention.

MEASURED: 21 grep-lines → **19 STATEMENTS + 2 MENTIONS**.

### Counts — hardener

- MENTIONS (not statements): **2**
- STATEMENTS: **19**
  - (a)-independent: **18**
  - (a)-self-report: **1** (row 14)
  - (b): **0**
  - (c): **0**
- OUTCOMES for (a) only (n=19):
  - FIRED-CHANGED: **2** (rows 5, 16)
  - FIRED-IGNORED: **0**
  - NOT-FIRED: **13** (rows 1, 3, 4, 6, 7, 8, 9, 10, 14, 15, 17, 18, 19)
  - CANNOT-TELL: **4** (rows 2, 11, 12, 13)

MEASURED, checksum: 2 + 13 + 4 = **19** = the statement count. ✓

### Notable — hardener

**§D. The clean-main clause (row 2) — a falsifier whose observation ALMOST fired, and the agent
noticed.** At `:26` hardener names "`git -C /Users/vadrsa/git/swarm status` showing anything but
clean main" as disconfirming. In the NEXT task's falsifier (`:42-43`) it writes: "or main checkout
dirtied (**it shows only a sibling's untracked docs/audit/, not mine**)". VERIFIED. The observation
LOOKED like it fired, the agent checked, and correctly attributed the dirt to field-tester rather
than silently ignoring it or falsely claiming clean. This is a falsifier being *used*.

**§E. The cross-agent residue on row 4 (queue-ownership).** hardener's Task-3 falsifier includes
"or probe-a-class agents still hand-draining queues after this lands in a live tree" (`:61-62`).
That clause DID fire — in another agent's journal: `field-tester.md:59` VERIFIED, span-after-1
"hand-READ its 8 undelivered queue files in one turn (WORLD.md's 'never read or move' sentence
violated on the read half, journaled openly)". hardener never learns it. What happened instead is
subtler and, I think, better: the contract was **narrowed to move-only** in Task 7 (`:130-141`) —
the read half was withdrawn precisely because agents kept reading. So the world responded to the
firing; hardener's *journal* just never books it as a firing. I record this as a **cross-journal
firing with an in-world course change but no in-journal booking** — not FIRED-IGNORED (the course
DID change), but the honest shape is worth naming: falsifiers that fire in someone else's journal
are structurally invisible to their author.

**§F. FIRED-CHANGED (row 5) — the delegation-header falsifier fired in field-tester's probe.**
Registered `hardener.md:77-81`: "…or field-tester's after-probe showing agents briefed with this
header **still grinding parallelizable work serially**." Fired: `field-tester.md:43` VERIFIED —
"deleg-after-1 (header v1): zero children, 1 turn, 83s". Change: `hardener.md:84-95` — the header
was amended (v1→v2, bidirectional reconcile, "keep a child only if you can name its next task"),
branch rebuilt. The falsifier named the exact observation; the observation occurred; the text
changed. That the change came via the operator rather than by hardener reading field-tester's
journal is a routing detail, not a failure — the loop closed.

**§G. FIRED-CHANGED (row 16) — the agent pre-registered "the waiting message contradicts me" and
then WAITED FOR IT.** `hardener.md:254-256`, VERIFIED. The mid-turn doorbell rang while it was
building; instead of reporting and letting the operator correct it later, it wrote:
> "A second mid-turn doorbell rang while building — REPORT TO OPERATOR IS HELD until I read the
> waiting message next turn (it may amend; a stale report would waste an operator turn)."
and named the contradiction as a falsifier. The message DID amend: the next entry (`:258`) is
"Task 12 COMPLETE (final spec + **config amendment**)" — the branch was rebuilt again for a TOML
`[middleware]` config section. This is the only case in my slice where an agent **built a wait
into its own loop because a falsifier might fire**.

**§H. FIRED-IGNORED: ZERO.** MEASURED. hardener's falsifiers are dominated by exact,
mechanically-runnable commands (`git diff --stat`, `grep`, `python3 -m unittest`, exact string
checks). They are the most rigorous FORM in my slice — and the largest source of CANNOT-TELL,
because a command that is never re-run settles nothing. Rigour of form ≠ discharge.

### Reconciliation pairing — hardener

- Entries the journal itself calls a reconciliation: **0**. VERIFIED — hardener uses no
  "reconciliation" heading anywhere in 299 lines (`grep -c reconcil` → 0 in headings; the word
  appears only inside doctrine text it is *shipping*, e.g. `:88` "reconcile sentence now
  tree-matches-remaining-work", `:116` "reconcile widened to second axis"). Its unit is the TASK,
  not the reconciliation: 14 entries, each "Task N GREEN, reported", each ending with a falsifier
  and "Idle, awaiting…".
- Of those, how many name a falsifier IN THE SAME ENTRY: **N/A (0 of 0)**.
- Does it name falsifiers but then go idle / never reconcile again? **Yes — structurally, by design.**
  17 of 17 entries end with "Idle, awaiting review / next dispatch" (VERIFIED at :27, :45, :63, :82,
  :95, :109, :128, :142, :159, :174, :185, :205, :234, :274, :286, :299). Every falsifier is named at
  the moment of going idle and the agent then WAITS. It is a **dispatch-driven worker, not a
  self-directed investigator** — its falsifiers are handoff assertions ("here is how to prove me
  wrong") rather than course-correction instruments. That is a legitimate and honest use of the
  form, and it explains both the zero FIRED-IGNORED and the high CANNOT-TELL: nobody, including
  hardener, ever re-runs the commands it so carefully specified.

---

## updater.md

139 lines, 18 entries (MEASURED: `grep -c "^## "`), 18 grep-hits on "falsif".

### Statements table

| # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence |
|---|-----------|-----------------------------------------------|-------|---------|---------|----------|
| 1 | .swarm/journal/updater.md:11-12 | "Falsifier: if \`git -C ~/.local/share/swarm rev-parse origin/main\` on GitHub's main differs from eac88e2 right now, my \"up to date\" verdict is wrong." | (b) | — | — | OBSERVABLE-ELSEWHERE: the witness is **GitHub's origin/main at that moment** — a remote, time-indexed state that no repo file records. The install clone is at ~/.local/share/swarm, outside this repo. Firing is real and checkable in principle, but not from repo files. |
| 2 | .swarm/journal/updater.md:15-16 | "Falsifier: watcher output file shows the loop died without origin/main having moved." | (b) | — | — | OBSERVABLE-ELSEWHERE: the witness is a **background-task output buffer** (task bnr4w029b) in the harness session — the rubric's named example of an "ephemeral poller log". Not a repo file. |
| 3 | .swarm/journal/updater.md:22-23 | "Falsifier: bh42q12xx output shows death without origin/main moving, or origin/main on GitHub differs from eac88e2 now." | (b) | — | — | OBSERVABLE-ELSEWHERE (same two witnesses). NOTE: this falsifier DID fire in the world — `:25` VERIFIED, "Watcher bh42q12xx killed externally, empty output" — but it fired against an EPHEMERAL witness; nothing in the repo records it. See Notable §I. |
| 4 | .swarm/journal/updater.md:30 | "Falsifier: b2hb2rlhx dies without origin/main moving." | (b) | — | — | OBSERVABLE-ELSEWHERE. Also fired in-world (`:33` VERIFIED, "b2hb2rlhx killed externally like the two before") with an ephemeral witness. See §I. |
| 5 | .swarm/journal/updater.md:39-40 | "Falsifier: an origin/main move that goes unnoticed for hours would show the kill-restart chain is NOT providing coverage." | (b) | — | — | OBSERVABLE-ELSEWHERE: fires on a NON-EVENT (a move nobody noticed) whose witness is GitHub's timeline vs. the agent's wake times. Not recorded in any repo file. |
| 6 | .swarm/journal/updater.md:49-50 | "Falsifier: bf8w7rckc dies or goes silent while origin/main has actually moved." | (b) | — | — | OBSERVABLE-ELSEWHERE: Monitor task liveness + remote state. Never in the repo. Corroborating NOTE (VERIFIED, :53): the Monitor DID work — "Monitor bf8w7rckc fired (first real trigger — the persistent Monitor works where bash watchers were killed)". |
| 7 | .swarm/journal/updater.md:64-65 | "Falsifier: origin/main on GitHub != 85776d4 right now, or the suite I ran was not the new tree's (worktree was at origin/main per git output)." | (b) | — | — | OBSERVABLE-ELSEWHERE: GitHub's remote HEAD at a past instant; the scratch worktree was removed (`:63` "scratch worktrees removed") so the second clause's witness is gone too. |
| 8 | .swarm/journal/updater.md:71 | "Falsifier: origin/main on GitHub differing from 85776d4." | (b) | — | — | OBSERVABLE-ELSEWHERE. |
| 9 | .swarm/journal/updater.md:76-77 | "Falsifier: origin/main != 63d1a79 now, or installed HEAD != 63d1a79." | (b) | — | — | OBSERVABLE-ELSEWHERE: both witnesses (GitHub remote; the install clone at ~/.local/share/swarm) live OUTSIDE this repo. |
| 10 | .swarm/journal/updater.md:82-83 | "Falsifier: origin/main != 9402f94 now, or installed HEAD != 9402f94." | (b) | — | — | OBSERVABLE-ELSEWHERE (same). |
| 11 | .swarm/journal/updater.md:88-89 | "Falsifier: origin/main != ef72109 now, or installed HEAD != ef72109." | (b) | — | — | OBSERVABLE-ELSEWHERE (same). |
| 12 | .swarm/journal/updater.md:95 | "Falsifier: origin/main != 7e5a644 now, or installed HEAD != 7e5a644." | (b) | — | — | OBSERVABLE-ELSEWHERE (same). |
| 13 | .swarm/journal/updater.md:100-101 | "Falsifier: origin/main != 6d30e12 now, or installed HEAD != 6d30e12." | (b) | — | — | OBSERVABLE-ELSEWHERE (same). |
| 14 | .swarm/journal/updater.md:106-107 | "Falsifier: origin/main != 834fec4 now, or installed HEAD != 834fec4." | (b) | — | — | OBSERVABLE-ELSEWHERE (same). |
| 15 | .swarm/journal/updater.md:117-118 | "Falsifier: origin/main != aa6063d, installed HEAD != aa6063d, or either skill symlink dangling." | (b) | — | — | OBSERVABLE-ELSEWHERE: all three witnesses (GitHub, the install clone, ~/.claude/skills symlinks) are outside the repo. |
| 16 | .swarm/journal/updater.md:123 | "Falsifier: any of the three hashes differing." | (b) | — | — | OBSERVABLE-ELSEWHERE: "the three hashes" = HEAD, origin/main, v1.2.0^{commit} — the first two on the install clone / GitHub. Borderline (c) for terseness, but the antecedent sentence (`:121-122`) names them exactly, so the observation IS stated. Scored (b), not (c). |
| 17 | .swarm/journal/updater.md:130 | "Falsifier: origin/main != 1e254e4 now, or installed HEAD != 1e254e4." | (b) | — | — | OBSERVABLE-ELSEWHERE (same). |
| 18 | .swarm/journal/updater.md:138-139 | "Falsifier: origin/main != b94fa9e, HEAD != b94fa9e, or COORDINATING.md unreachable through the symlink." | (b) | — | — | OBSERVABLE-ELSEWHERE (same; the symlink is a filesystem fact outside the repo). |

### MENTIONS (not statements) — updater

**0.** VERIFIED: all 18 grep-hits are the agent's own falsifier statements. updater never quotes,
names, or reports on anyone else's falsifier.

### Counts — updater

- MENTIONS (not statements): **0**
- STATEMENTS: **18**
  - (a)-independent: **0**
  - (a)-self-report: **0**
  - (b): **18**
  - (c): **0**
- OUTCOMES for (a) only (n=0): FIRED-CHANGED 0 | FIRED-IGNORED 0 | NOT-FIRED 0 | CANNOT-TELL 0
  — **no forward-hunt was possible: this journal contains ZERO class-(a) falsifiers.**

### Notable — updater

**§I. The finding of this journal is its CLASS, not its outcomes.** MEASURED: 18 of 18 falsifier
statements are class (b) — every one names an observation whose witness lives OUTSIDE the
repository: GitHub's `origin/main` at a past instant, the install clone at `~/.local/share/swarm`,
a harness background-task output buffer, a `~/.claude/skills` symlink. **Not one falsifier in
updater's entire journal could be checked by a later reader with only this repo.** That is a
clean, publishable structural result and it is not a criticism of updater: its *job* is entirely
outside the repo (keep the INSTALL current), so its honest falsifiers necessarily point outward.
The lesson is about the doctrine, not the agent: **a falsifier's checkability is a property of the
agent's task surface, not of the agent's discipline.**

**§J. Falsifiers 3 and 4 DID fire — and were handled exemplarily — but the repo cannot see it.**
`:22-23` names "bh42q12xx output shows death without origin/main moving". It fired: `:25` VERIFIED,
"Watcher bh42q12xx killed externally, empty output. Re-checked: HEAD = origin/main = eac88e2, still
up to date." The agent then did exactly what a fired falsifier demands — it counted
("Consecutive deaths: 2 — one more and I report to operator per brief"), fired again (`:33`), hit
its pre-declared threshold, **reported to the operator**, and then **changed the mechanism entirely**
(`:42-50`: bash watcher → persistent Monitor, on operator prescription). Three firings, an
escalation rule declared IN ADVANCE, and a mechanism replacement. Under the rubric this cannot be
scored FIRED-CHANGED, because the outcome column is (a)-only and the witness (a background-task
buffer) is ephemeral. **I flag this explicitly for falsifier-probe: the rubric's (a)/(b) split will
systematically hide the single best-executed falsifier loop in my slice.** That is a finding about
the *instrument*, and I would rather say it than let the count imply updater did nothing.

**§K. FIRED-IGNORED: ZERO** (vacuously — no (a) statements exist to hunt).

**§L. The pattern is a template, and templates are cheap.** Rows 9–18 are the same sentence with
a different SHA: "Falsifier: origin/main != X now, or installed HEAD != X." VERIFIED across 10
entries. It is a genuine, checkable-at-the-time assertion (not (c) — the observation is stated
precisely), and it is trivially satisfied at the moment of writing, since the agent has *just*
verified both hashes. REASONED: this is a falsifier as **receipt**, not as **risk** — it restates
the check just performed rather than naming a hazard the agent has not yet ruled out. Formally
sound; epistemically near-free. Contrast field-tester.md:59 ("if the subagent claim is false,
deliverable mtimes will show serial spacing — **check at harvest**"), which names a hazard the
agent could not yet rule out and then goes and checks it.

### Reconciliation pairing — updater

- Entries the journal itself calls a reconciliation: **0**. VERIFIED — the word "reconcil" does not
  appear in updater.md at all (`grep -ci reconcil` → 0).
- Of those, how many name a falsifier IN THE SAME ENTRY: **N/A (0 of 0)**.
- Does it name falsifiers but then go idle / never reconcile again? **It names a falsifier in
  EVERY entry (18 statements / 15 entries; three entries carry two) and goes idle after each one —
  but it is a watcher, and it genuinely wakes and re-checks.** The falsifiers are per-cycle receipts,
  discharged-on-arrival by construction. So: it never *reconciles* in the doctrine's sense, and it
  never needed to.

---

## SLICE TOTALS (MEASURED)

| | field-tester | hardener | updater | **TOTAL** |
|---|---|---|---|---|
| grep-lines on "falsif" | 38 | 21 | 18 | 77 |
| MENTIONS (not statements) | 12 | 2 | 0 | **14** |
| **STATEMENTS** | 35 | 19 | 18 | **72** |
| (a)-independent | 32 | 18 | 0 | **50** |
| (a)-self-report | 1 | 1 | 0 | **2** |
| (b) | 2 | 0 | 18 | **20** |
| (c) | 0 | 0 | 0 | **0** |
| — (a) forward-hunt, n= | 33 | 19 | 0 | **52** |
| FIRED-CHANGED | 2 | 2 | 0 | **4** |
| **FIRED-IGNORED** | **0** | **0** | **0** | **0** |
| NOT-FIRED | 26 | 13 | 0 | **39** |
| CANNOT-TELL | 5 | 4 | 0 | **9** |

### Headline findings

1. **FIRED-IGNORED = 0 across 52 class-(a) statements.** I hunted for the pathology and it is not
   here. I decline to manufacture one. The nearest miss (field-tester row 32) is a falsifier that
   guarded the *wrong hazard* — the claim it protected was retracted, but for a flaw the falsifier
   never named. That is a different disease and I have named it as such.

2. **(c) UNFALSIFIABLE-AS-WRITTEN = 0 across all 72 statements.** Not one vague "if I'm off base"
   in three journals. Whatever else is true, these agents write falsifiers with a stated observation.

3. **NOT-FIRED (39) dwarfs CANNOT-TELL (9) — the OPPOSITE of the rubric's expectation.** The rubric
   predicted CANNOT-TELL would be "the largest bucket". In my slice it is not, and the reason is
   specific: field-tester and hardener overwhelmingly **discharge their falsifier inside the same
   entry that raises it** ("checked, grep found them"; "grep: zero 'engine'"; "(checked: journal has
   no [hand-B] CLAIM qa line)"). That is a real discipline — but it also means many of these
   falsifiers are **receipts for a check already performed**, not live risks carried forward.
   The 9 genuine CANNOT-TELLs are the ones that named a *future* check nobody ever ran.

4. **The 4 FIRED-CHANGED cases are the doctrine actually working**, and all four share one shape:
   the falsifier named an **external adversary or an incoming message** as the witness
   (v3-red's review ×2, field-tester's probe, the waiting operator mail). **No falsifier in my slice
   fired against its own author's unaided later observation.** REASONED, and I think it is the most
   load-bearing thing in this file: a falsifier appears to need a *second party* to fire.

5. **Class is task-shaped, not discipline-shaped** (updater, §I): 18/18 (b) not because updater is
   sloppy — its falsifiers are precise and it handled three real firings exemplarily (§J) — but
   because its work lives outside the repo. Any doctrine that grades agents on falsifier-checkability
   is grading their job description.

---
*fp-slice-a. Every file:line above was read this session and is real. Journals were opened
read-only; none was modified.*
