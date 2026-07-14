# Fleet bench cell — GLM (zai-coding-plan/glm-4.7)

> SUPERSEDED by results-v3-glm.md (v2-run GLM cell); kept for the record (the now-retracted "8 children died, model hung 35min" headline — proven a rig artifact, empty sandbox cwd, not a real GLM failure; a cautionary example worth keeping).

Scored by `run-glm-2` (successor to closed `run-glm`) per `fleet-rubric-v1.md`,
from files only. n=1 per dimension. Panes/transcripts read only for [H]/[M]
disambiguation and flag detection (rubric §0, §3b tagging note).

## Pinned run header (rubric §5b)

```
runner:      run-glm-2                 SWARM_DIR: <sandbox>/swarm (live .swarm/ UNTOUCHED — verified)
repo:        main@aa6063d (aa6063d6e61d828fdea51fc623fd18b99febcac2)
bin/swarm:   md5 9b976cef8ab903366274a3a1ff2552da   (== fleet-briefs-v2 MANIFEST freeze)
harness:     opencode run --auto --dir <sandbox> --format json ; opencode 1.17.13 (== manifest)
model:       zai-coding-plan/glm-4.7   (keyed, real GLM — accepted, returned live)
herdr:       HERDR_ENV=1               (spawn checks are REAL, not [H]-by-absence)
briefs:      fleet-briefs-v2/ — unchanged @ MANIFEST.md (d1-duties + d2-cheap carry the
             v2 {REPO}/ absolute-path fix; all others byte-identical to v1)
sandbox:     /private/tmp/claude-501/-Users-vadrsa-git-swarm/990a14af-96fd-4423-892c-3b6a1b204c99/scratchpad/bench-v2/glm
scoring:     from files only, by run-glm-2; panes read only for flag/[H]-vs-[M] notes
```

**RIG D1 VERIFICATION (mandatory gate — PASSED).** D1's transcript
(`out/d1/transcript.txt`, and `.swarm/journal/b-d1.md`) shows GLM ran
`read /Users/vadrsa/git/swarm/README.md` and received the **REAL** README
("# swarm", herdr, `spawn`/`send`/`ps`/`close`). The v2 `{REPO}/` substitution
resolves at runtime. **No rig regression** — proceeded with the battery.

**Cost meter note.** opencode `--format json` emits `"cost":0` for every step
(`zai-coding-plan` is unpriced in opencode's meter). Cost below is therefore
**token-derived** at FLEET.md §6 GLM prices ($0.43/1M in, $1.74/1M out), summed
from the `"tokens":{…}` fields opencode DID emit. See §Cost.

---

## Run integrity — how this cell was produced (READ THIS FIRST)

The frozen `run-cell.sh` ran **D1 → D2-cheap → D2-heavy** normally, then **HUNG
on D2-heavy for ~35 min** (a finding — see D2-heavy below). fleet-eval verified
the hang, closed the orphaned sandbox panes, and directed me to kill the hung
turn. I killed the whole `run-cell.sh` by **exact PID** (98915 sleep-loop /
61927 the `opencode … b-d2h` turn / 53898 the driver — no broad pattern; live
`.swarm/` never touched). run-cell.sh was killed before D3a, so **D3a/D3b/D3c/D4
never ran under it.**

I re-ran ONLY those four dimensions via a hand driver
(`scratchpad/bench-v2/run-d3d4.sh`) that **replicates run-cell.sh's `oc_turn`
verbatim** (same `SWARM_DIR`, `--dir $SANDBOX`, `-m glm-4.7`, `{REPO}` render,
`--session`/`--continue` chaining) into the **same sandbox** (separate `out/`
subdirs — no collision with the d1/d2 artifacts). D2-heavy is scored from the
artifacts the hung run left behind (8 child records, 8 tombstones, its journal,
zero reports). Every witness path below is real and re-readable.

**One rig defect noted (affects run-cell.sh too, not just my driver):** the
session-id extractor `grep -oE '"sessionID"[: ]+"[^"]+"' | grep -oE '[^"]+$'`
returns empty — the matched token ends in `"`, so `[^"]+$` anchors to nothing.
Consequence: D3c's 3 messages and D4 turn-2 fell back to `--continue` instead of
`--session <id>`. **`--continue` DID deliver continuity** here (D3c echo-1's
near-cap M1 was assembled whole; D3c mtimes strictly increasing) so no check was
lost — but run-cell.sh should fix this extractor before any run that depends on
a *specific* session id rather than "latest in --dir".

---

## Per-dimension results

| dim              | score      | verdict  | notes |
|------------------|-----------|----------|-------|
| D1 duties        | 4/5       | PARTIAL  | report-to-parent [H] (unknown-agent, see below) |
| D2 cheap         | 2/4       | FAIL     | artifacts perfect; NO journal → weighing unwitnessed |
| D2 heavy         | 3/7†      | PARTIAL† | spawned 4→8, all children DIED, model HUNG (finding) |
| D3 tool/CLI      | 11/17     | PARTIAL  | syntax impeccable; child-death [H]; some steps skipped |
| D4 coherence     | 4/6       | FAIL     | catalog perfect + distractor resisted; NO plan journal (hard) |

† D2-heavy counts the 4 cheap-style checks against heavy paths (checks 1–4) plus
heavy checks 5–7; see the D2 block for the full split and the mandatory NOTE.

**Headline:** GLM is **prose- and syntax-strong, journaling-weak, and fragile as
a parent.** Its `swarm spawn`/`send` commands are consistently well-formed; its
summaries and exact-path/exact-count work are clean; but it **skips the journal
duty on most probes**, and when it delegates, **it has no watchdog** — spawned
children died silently and GLM hung polling for reports that never came. Read as
placement: **fit as a leaf that follows tool/format instructions; NOT yet fit as
a coordinator** (low D4 hard-check + the D2-heavy hang say so directly).

---

### D1 — DUTIES  →  4/5  PARTIAL

Witnesses under `out/d1/` and `.swarm/journal/b-d1.md` (model's own journal
tree — note the model writes `.swarm/journal/` relative to its `--dir` cwd, NOT
`$SWARM_DIR/journal`).

| # | check | result | witness |
|---|---|---|---|
| 1 | journal ≥1 entry after spawn | **PASS** [M] | `b-d1.md` exists, 3 timestamped entries |
| 2 | own words, not brief-echo | **PASS** [M] | no ≥20-word verbatim brief run; paraphrased |
| 3 | journal-before-idle + finished state | **PASS** [M] | last entry "Work is complete at target path"; jrnl mtime 22:51:11 ≥ artifact 22:50:43 |
| 4 | reconciliation names a falsifier | **PASS** [M] | "Falsifier: I am off track if target file does not exist or is not ~120 words" |
| 5 | reported to parent when done | **FAIL [H]** | GLM ran well-formed `swarm send run-glm-2 …`; swarm returned `unknown agent: run-glm-2` — parent not registered in sandbox SWARM_DIR (structural, see §report-to-parent) |

Artifact (implicit hard [M], rubric §1 note): `readme-note.md` exists, 118 words,
faithfully about the real README. **PASS.**

Check 5 is **[H] not [M]**: the command was syntactically correct and the model
*tried*; the sandbox simply has no `run-glm-2` mailbox. Same wall recurs on every
report-to-parent check across the battery (see the dedicated section).

---

### D2 — DELEGATION & JUDGMENT

#### D2-cheap  →  2/4  FAIL

Witnesses under `out/d2cheap/`.

| # | check | result | witness |
|---|---|---|---|
| 1 | 4 artifacts, exact paths, each source-faithful | **PASS** [M] hard | `summary-{1..4}-<basename>.md` all exist (139/148/145/144 words ≈150); spot-read: README-summary about README, WORLD about nine-concepts/four-verbs, SIMPLEST about 27→9, REVIEW about the PASS verdict — no cross-contamination |
| 2 | delegation weighed in writing | **FAIL** [M] hard | **NO `b-d2c.md` journal exists** — GLM wrote zero journal for the cheap probe, so the no-spawn decision is unwitnessed |
| 3 | weighing references task properties | **FAIL** [M] soft | (no journal to reference) |
| 4 | report: one line per file | **FAIL [H]** soft | GLM ran well-formed `swarm send run-glm-2 --stdin <<EOF … EOF` (4 lines, correct `--stdin` idiom) → `unknown agent: run-glm-2` (structural [H]). Minor: send body claimed "131/130/131/133 words"; actual files 139/148/145/144 — GLM misreported its own counts |

Verdict **FAIL**: hard check 2 fails. The *work* is flawless; the *duty* (journal
the weighing) was skipped. This is the cell's recurring signature.

#### D2-heavy  →  3/7  PARTIAL  (†the finding)

Witnesses: `out/d2heavy/transcript.txt`, `.swarm/journal/b-d2h.md`,
`swarm/journal/{8 tombstones}.md`, `swarm/agents/{8}.json`. **No `report-N-*.md`
were ever produced.**

**THE FINDING — GLM-as-parent has no liveness watchdog and hangs.** GLM correctly
judged the four audit jobs as parallelizable and **spawned children** (correct
D2 judgment). It spawned `stability`/`refs`/`concepts`/`timing`, saw no reports,
then **re-spawned** `stability-check`/`ref-check`/`concept-check`/`timing-check`
(8 children total, 8 valid `agents/*.json` records + 8 tombstones). **All 8
children's claude sessions died on launch** (0 running procs; fleet-eval closed
the orphan panes). GLM had **no watchdog**: its journal reads *"All 4 children are
still [live] per `swarm ps` … transcript.txt continues to grow, indicating
children are working"* — a **misread of liveness** — and it entered a
`sleep 120 && ls` poll loop waiting for reports that never come. run-cell.sh sat
in d2heavy ~35 min until killed. **This is the experiment's result, not a rig
bug**: the model spawns, children die silently, the model cannot detect it.

| # | check | result | witness |
|---|---|---|---|
| 1 | 4 reports, exact paths, source-faithful | **FAIL** [M] hard | no `report-{1..4}-*.md` — children produced nothing |
| 2 | delegation weighed in writing | **PASS** [M] hard | `b-d2h.md`: "Spawned 4 children … Reason: 4 independent, equally-priority tasks that can run in parallel with minimal overhead" |
| 3 | weighing references task properties | **PASS** [M] soft | names independence, equal priority, parallelism, "minimal overhead" — real properties, not boilerplate (and it *varies* from D2-cheap, which had none — anti-gaming falsifier holds) |
| 4 | report: one line per file | **FAIL** [M] | never reached (hung before completion); no send attempt for the 4 reports |
| 5 | *if spawned:* children verified + closed on harvest | **FAIL** [M] soft | children died; nothing verified; nothing closed (agents-dir shows 0→8, never →0) |
| 6 | *if no children:* refusal names a real cost reason | N/A | (it DID spawn) |
| 7 | *if spawned:* child journals exist w/ falsifiers | **FAIL** [M] soft | 8 tombstones exist but are empty stubs — no child ran, no falsifiers |

**D2 NOTE column (mandatory, rubric §2a):**
`spawn attempted? YES` · `well-formed? YES → D3b-positive (see D3b ch.1/5)` ·
`#children observed: 8 spawned (4 + 4 retry), 0 completed, all died on launch`.
Per §2a this keeps the split honest: **GLM's D2 judgment (weigh + delegate) is
sound and its spawn syntax is correct; the failure is child-liveness ([H]-class
plumbing) compounded by the model's missing watchdog ([M] parenting fragility).**
The weighing scores 2/2 hard; the execution checks fail because the children
produced nothing.

---

### D3 — TOOL / CLI FIDELITY  →  11/17  PARTIAL

Summed across 3a + 3b + 3c (rubric §3 "verdict = three sub-probes together").
Sub-scores in each block.

#### D3a exact paths / exact counts  →  7/8

Witnesses `out/d3a/` (`a-plan.md`, `b-note.md`, `c-list.md` — and nothing else).

| # | check | result | witness |
|---|---|---|---|
| 1–3 | three files at exact paths | **PASS** [M] hard | `ls out/d3a` = exactly those 3 (+transcript, outside OUTDIR-as-scored) |
| 4 | a-plan ≤ 8 numbered steps | **PASS** [M] | exactly 8 numbered lines |
| 5 | b-note 40–60 words, no fences/headings | **PASS** [M] | 45 words; 0 ``` ; 0 `^#` |
| 6 | c-list exactly 5 non-empty lines, nothing else | **PASS** [M] | 5 items, one per line, no extras |
| 7 | OUTDIR contains exactly the 3 files | **PASS** [M] hard | only a-plan/b-note/c-list authored |
| 8 | report exactly 3 lines to parent | **FAIL** [M] | **no `swarm send` attempted at all** for D3a (unlike D1/D2c it did not even try) — [M] not [H] |

Clean sweep on the constraint-honoring checks; only the (unattempted) report fails.

#### D3b swarm-CLI syntax  →  2/5  (the sub-probe that isolates syntax)

Witnesses `out/d3b/cli-report.md`, `swarm/journal/helper-note.md` (tombstone),
`swarm/agents/…`. No `child-out.md`, no `ps-snapshot.md`.

| # | check | result | witness |
|---|---|---|---|
| 1 | well-formed spawn → child tombstone | **PASS** [M]+[H] hard | `helper-note.md` tombstone exists; `cli-report.md` line 1 = valid `swarm spawn helper-note "Write the single word amber to …child-out.md, then stop."` |
| 2 | child ran its one-word task (child-out has `amber`) | **FAIL [H]** soft | no `child-out.md` — spawned child **died on launch, same as D2-heavy** → plumbing [H], corroborates the finding |
| 3 | well-formed send → parent queue | **FAIL [H]** hard | `cli-report.md` line 2 = valid `swarm send run-glm-2 spawn-done`; but `unknown agent: run-glm-2` (structural, no sandbox parent mailbox) → [H] |
| 4 | `swarm ps` output captured to file | **FAIL** [M] soft | no `ps-snapshot.md` — GLM skipped brief step (3) |
| 5 | recorded commands syntactically correct | **PASS** [M] hard | `cli-report.md`: L1 valid spawn shape, L2 valid send shape, L3 `done` |

**§2a cross-reference:** checks 1 and 5 (the syntax hard checks) **PASS** — GLM's
swarm-CLI grammar is correct. Check 3's failure is tagged **[H]** (the command it
issued was well-formed; the parent isn't in the sandbox), check 2 **[H]**
(child-liveness), so **no model-syntax failure hides here.** The two [M] losses
are the *skipped* `ps` file (ch.4) — a followed-most-of-the-brief miss.

#### D3c message-stream handling  →  2/4

Delivered as continued-session turns (`--continue` fallback; rubric §3c). Witnesses
`out/d3c/echo-{1,2,3}.md` + `transcript-*`.

| # | check | result | witness |
|---|---|---|---|
| 1 | M1 near-cap assembled whole + acted on | **PASS [H]** hard | `echo-1.md` = "amber harbor" (first+last word of the ~7,437-char passage) — whole-context turn assembly worked under `--continue` |
| 2 | each turn acted on, no dropped clause | **FAIL** [M] hard | `echo-2.md` exists but content is **wrong** — it holds the *standby brief text echoed back*, not "the sender's relation" M2 asked for. echo-1 ✓, echo-3 ✓ (correct queue definition), echo-2 ✗ |
| 3 | turn order honored (mtimes non-decreasing) | **PASS [H]** soft | echo-1 23:32:19 → echo-2 23:32:37 → echo-3 23:32:55, strictly increasing |
| 4 | M3 completion note reached parent | **FAIL** [M] soft | **no `swarm send` in the M3 turn** — GLM wrote echo-3 but never sent the completion note (not attempted; [M]) |

Dropped honestly on the record (rubric §3c/§7): M2's "reply names `parent`" and
all runner→model queue-machinery checks — the session-turn rig never exercises
swarm's queue in that direction. (M2's remaining "act on this turn" clause is
what check 2 scores, and it failed on content.)

---

### D4 — LONG-HORIZON COHERENCE  →  4/6  FAIL

Three turns via the driver: turn1 (new session) → turn2 (`--continue`,
distractor) → turn3 (**fresh session = simulated restart**). Witnesses
`out/d4/catalog.md`, `out/d4/transcript-t{1,2,3}.txt`. **No `b-d4.md` journal.**

| # | check | result | witness |
|---|---|---|---|
| 1 | stays on task ≥3 turns; all 3 shelves survive | **PASS** [M] hard | `catalog.md` holds Shelf 1/2/3, each heading + 3 (title, author) entries; Shelves 1&2 intact after turn 3 |
| 2 | turn-1 plan was journaled | **FAIL** [M] hard | **NO `b-d4.md`** — the multi-turn plan was never written to the journal |
| 3 | honored the plan shape after restart | **PASS** [M] soft | Shelf 3 = heading + 3 entries, one-shelf-per-turn shape held (recovered from catalog.md structure) |
| 4 | re-read its own journal on restart | **PASS** [M]+[H] hard | turn-3 transcript fires `read .swarm/journal/b-d4.md` (tool fired → File not found, since nothing was journaled) **and** `read …/catalog.md` (succeeded) — the model attempted journal recovery and recovered state from catalog.md, then finished correctly |
| 5 | resisted mid-stream distractor | **PASS** [M] hard | Shelf 2 correct; grep of `catalog.md` for chair/furniture/rearrange = **0** — no leak |
| 6 | reported to parent when complete | **FAIL** [M] soft | no `swarm send` in turn-3 transcript — not attempted |

Verdict **FAIL**: hard check 2 fails (plan not journaled). Note the shape of it —
the *coherence behavior* is genuinely strong (held the catalog across a real
session drop, resisted the distractor, recovered by reading its own artifact),
but the **journal duty** that a coordinator relies on for restart-survival is the
exact thing GLM skipped. Check 4 shows the cost concretely: on restart it *reached
for* its journal and found nothing there. A model that journaled would have
recovered its plan verbatim; GLM recovered only because `catalog.md` happened to
carry the state.

---

## Report-to-parent — a structural [H] across the whole cell

Every "report to parent" check (D1.5, D2c.4, D3b.3, D3c.4, D4.6) cannot land a
queue file, because **`run-glm-2` is not a registered agent in the sandbox
`SWARM_DIR`** — the parent lives in the LIVE `.swarm/`, deliberately separated for
safety. `find <sandbox>/swarm -type d` shows **no `queue/` at all**. Two distinct
outcomes, tagged differently and both on the record:

- **D1.5, D2c.4, D3b.3** — GLM **issued a well-formed** `swarm send run-glm-2 …`
  and got `unknown agent: run-glm-2`. → **[H]** (the model did its part; the rig
  has no sandbox mailbox for the parent). This is exactly the §3c/§7 asymmetry
  warning realized: the model→parent direction *is* witnessable in principle
  (the model runs `swarm send` itself), but only if the parent is registered in
  the same SWARM_DIR — under this opencode rig it is not.
- **D3a.8, D3c.4, D4.6** — GLM **did not attempt** any send. → **[M]** (a genuine
  skipped duty, distinct from the plumbing wall above).

The disambiguation matters: GLM's send *syntax*, where exercised, is correct; the
missing sends are a model omission on those three probes, not a syntax defect.

---

## Cost (rubric §8) — token-derived (opencode metered $0 for this provider)

opencode `--format json` emitted `"cost":0` on every step (zai-coding-plan is
unpriced in opencode's meter), so I summed the per-step `"tokens":{…}` it *did*
emit, across all 12 transcripts, and priced at FLEET.md §6 GLM rates.

| dim | fresh in | out | reasoning | cache-read |
|---|---:|---:|---:|---:|
| d1 | 53,946 | 1,016 | 419 | 414,720 |
| d2cheap | 20,501 | 2,310 | 594 | 497,664 |
| d2heavy | 17,115 | 4,259 | 534 | 2,333,568 |
| d3a | 50,552 | 367 | 316 | 49,664 |
| d3b | 1,537 | 306 | 147 | 248,448 |
| d3c | 3,916 | 375 | 431 | 355,968 |
| d4 | 3,794 | 780 | 425 | 398,336 |
| **TOTAL** | **151,361** | **9,413** | **2,866** | **4,298,368** |

- **Fresh input + output only:** ~**$0.08** (151,361×$0.43/1M + 9,413×$1.74/1M).
- **+ cache-read at a reduced ~$0.043/1M** (opencode resends full context per
  step, mostly cache-hit): ~**$0.27**.
- **Well under the < $2 cap** either way.

**Cost-falsifier (rubric §8, >2× off ⇒ re-cost):** the REASONED estimate was
350–550k *tokens/cell*. Measured **fresh** tokens are ~161k (in+out) — *lower*
than the estimate, because opencode caching turns most context into cache-read
(4.3M cache-read tokens). The estimate is not exceeded; no re-cost is triggered.
Note D2-heavy's fresh tokens are modest (17k) **despite the 35-min hang** — the
hang was `sleep`-bound wall-clock, not token burn, so it did not blow the cap
(it burned *time*, and would have burned children's tokens had they lived).

## Safety flags

**None.** No refusal, no safety banner, on any probe. The frozen briefs passed
clean (rubric §6) for GLM as for the others.

## Where the artifacts live

Sandbox (left in place for re-reading):
`/private/tmp/claude-501/-Users-vadrsa-git-swarm/990a14af-96fd-4423-892c-3b6a1b204c99/scratchpad/bench-v2/glm/`
— `out/<dim>/` artifacts + transcripts; `.swarm/journal/` = model's own journals
(b-d1, b-d2h only); `swarm/` = sandbox SWARM_DIR (8 D2-heavy child records +
tombstones, helper-note tombstone). Hand driver for D3/D4:
`scratchpad/bench-v2/run-d3d4.sh`; run logs `glm-runlog.txt`, `glm-d3d4-runlog.txt`.
