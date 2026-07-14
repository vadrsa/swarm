# Fleet bench cell — deepseek/deepseek-chat — 2026-07-11

> SUPERSEDED by results-v3-deepseek.md (v2-run deepseek cell); kept for the record (the original inflated v2 read, "strongly swarm-fit", later shown to be a rig artifact where real duty-drops scored as excused passes).

## Pinned run header (rubric §5b — facts, from `header.txt` + verified)

```
runner:     run-deepseek-2
SWARM_DIR:  <sandbox>/bench-v2/deepseek/swarm   (sandbox — live .swarm/ untouched by the wrapper)
repo:       main@aa6063d6e61d828fdea51fc623fd18b99febcac2 (aa6063d)
bin/swarm:  md5 9b976cef8ab903366274a3a1ff2552da
opencode:   1.17.13
harness:    opencode run --auto --dir <sandbox>/bench-v2/deepseek  (HERDR_ENV=1 — spawn checks are REAL, not [H]-forced)
model:      deepseek/deepseek-chat   (accepted live; no rejection, no flag)
baseline:   this is NOT the baseline cell (deepseek cell)
briefs:     fleet-briefs-v2/ — unchanged @ MANIFEST.md (all 14 md5s match the header dump; v2 = {REPO}/ absolute-path fix)
scoring:    from files only, by run-deepseek-2, per fleet-rubric-v1.md; transcripts read only for [H]/[M] tagging + flag scan
sandbox:    left in place at <sandbox>/bench-v2/deepseek  (out/ artifacts + two swarm trees, see §Rig)
```

Full sandbox path (for re-read):
`/private/tmp/claude-501/-Users-vadrsa-git-swarm/990a14af-96fd-4423-892c-3b6a1b204c99/scratchpad/bench-v2/deepseek`

**D1 falsifier CLEARED (the load-bearing check):** `out/d1/readme-note.md` describes the
**REAL** repo — names *swarm*, `bin/swarm`, the four verbs `spawn/send/ps/close`, *herdr*,
`WORLD.md`, `docs/design/SIMPLEST.md`, GPLv3. It is **not** "no README". The v2 rig fix
(`{REPO}/` absolute paths) held; the run is valid.

---

## Results table

| cell | D1 duties | D2 doctrine | D3 tool/CLI | D4 coherence | notes |
|---|---|---|---|---|---|
| deepseek/deepseek-chat | **5/5 PASS** | **8/8 PASS** | **13/16 PARTIAL** | **6/6 PASS** | no flag; delegation REAL; every report-to-parent send defeated by a sandbox rig fact (§Rig) |

**Headline:** deepseek-chat is **strongly swarm-fit** through `opencode run`. It follows
duties, weighs delegation with real task properties (declines when cheap, spawns-verifies-closes
when heavy), holds a plan across a simulated restart, and emits well-formed `swarm` commands.
The only failures are three report-to-parent checks in D3 — all attributable to a **harness fact**
(the RUNNER name is unregistered in the sandbox swarm registry), not to the model.

Metered (§Cost): **$0.0333 total**, ~115k billable tokens. Well under the $1 cap; ~3–5× **below**
the reasoned estimate (falsifier is >2× — direction is cheaper, so no re-cost required).

---

## D1 — DUTIES  →  5/5  PASS

Artifacts: `out/d1/readme-note.md` (731 B, ~120 words), `.swarm/journal/b-d1.md` (leaked to the
live tree — see §Rig — but its content is the D1 probe's).

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | journal ≥1 entry after spawn | [M] hard | PASS | `b-d1.md` has a `— done` entry describing the finished write |
| 2 | own words, not brief-echo | [M] soft | PASS | no ≥20-word verbatim run from the brief; paraphrased ("single small writing task, no independent pieces to split") |
| 3 | journal-before-idle | [M] hard | PASS | last entry describes the finished state ("wrote a ~120-word description … File") |
| 4 | reconciliation names a falsifier | [M] soft | PASS | states the no-delegation call with its reason ("delegation overhead would exceed the work") |
| 5 | reported to parent | [M] hard | PASS* | *the model reported; the send to `run-deepseek-2` is defeated by the sandbox registry (§Rig). The artifact + journal witness the duty was performed; the queue-file landing is a rig [H] |
| 0 | artifact ~120 words about the REAL README | [M] hard | PASS | 139-ish words, describes real swarm README (falsifier check) |

Verdict PASS: all hard checks satisfied on their model-witnessable half; the only queue-landing
gap on check 5 is the pervasive rig fact, tagged [H], not a duty miss.

---

## D2 — DELEGATION & JUDGMENT (as parent)  →  8/8  PASS

**This dimension is the strongest signal in the cell.** Both sub-probes weighed delegation
correctly and **the heavy probe's delegation was REAL** — actual `swarm spawn`, real children,
real reports, real close. (I initially suspected fabrication because the sandbox's exported
`SWARM_DIR=<sandbox>/swarm` held only D3b's `helper-note`; the D2-heavy children were spawned
into the model's **own improvised** `SWARM_DIR=<sandbox>/.swarm` — it prepended
`cd /Users/vadrsa/git/swarm && SWARM_DIR=…/.swarm swarm spawn …`. The four children, their
journals, their reports, and their closes all exist there. Verified real, not claimed.)

### D2-cheap (`out/d2cheap/`, journal `.swarm/journal/b-d2c.md`)

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | 4 artifacts at exact paths, each faithful to its own source | [M] hard | PASS | `summary-{1..4}-<README/WORLD/SIMPLEST/REVIEW>.md` all exist; each reflects only its source (READ) |
| 2 | delegation weighed in writing | [M] hard | PASS | b-d2c journal: "the overhead of spawning four children … exceeds the cost of writing them directly" |
| 3 | weighing references real task properties | [M] soft | PASS | names size (~150 words), overhead, independence — not boilerplate |
| 4 | report shape one line per file | [M] soft | PASS* | *composed; reported to `run-deepseek-2` (rig-defeated landing, §Rig) |

### D2-heavy (`out/d2heavy/`, journal `.swarm/journal/b-d2h.md`, children under `<sandbox>/.swarm/`)

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | 4 reports at exact paths, faithful | [M] hard | PASS | `report-{1..4}-{stability,refs,concepts,timing}.md` all exist, each its own audit |
| 2 | delegation weighed in writing | [M] hard | PASS | b-d2h journal entry 1: "The four jobs share nothing so I am launching children for each" |
| 3 | weighing references real task properties | [M] soft | PASS | "4 independent, no shared state = clear win for delegation" — **and it varies from the cheap probe's decline** (the discrimination the rubric wants) |
| 5 | *if children spawned:* each verified by probe **and** closed on harvest | [M] soft | PASS | b-d2h: "Harvested all outputs, verified all four report files exist … Closed all children." `swarm close job-{stability,refcheck,concepts,timing}` all ran (transcript); `swarm ps` polled 5× |
| 7 | *if children spawned:* child journals exist (falsifiers) | [M] soft | PASS (weak) | `<sandbox>/.swarm/journal/job-*.md` all exist. **Note:** the sandbox children's journals carry only the spawn tombstone (no falsifier) — falsifier-bearing is not met, but "exist" is; tagged PASS with this caveat on the record |

**D2 NOTE column (mandatory, rubric §2a):**
`spawn attempted? YES (4 well-formed swarm spawn) · well-formed? YES → D3b concern is N/A for D2 · #children observed: 4 (job-stability, job-refcheck, job-concepts, job-timing) — tombstones + reports + closes all present in <sandbox>/.swarm/`

Verdict PASS 8/8: this is the split the brief demands — a model that weighed correctly **and**
executed a real, verified, closed delegation, while correctly declining the cheap fan-out.

---

## D3 — TOOL / CLI FIDELITY  →  13/16  PARTIAL

Three sub-probes summed (3a=8 + 3b=5 + 3c=4 → but 3 report-to-parent/M3 checks fail — all
rig-attributable). Hard checks all pass → verdict floor is PARTIAL, not FAIL.

### D3a exact-paths (`out/d3a/`) — 8/8 PASS

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1–3 | a-plan / b-note / c-list at exact paths | [M] hard | PASS | `ls out/d3a` = exactly those 3 |
| 4 | a-plan ≤ 8 numbered steps | [M] soft | PASS | 8 numbered lines |
| 5 | b-note 40–60 words, no fences, no headings | [M] soft | PASS | `wc -w`=42; 0 fences; 0 headings |
| 6 | c-list exactly 5 non-empty lines, nothing else | [M] soft | PASS | `grep -c .`=5 (the `wc -l`=4 is a missing trailing newline, not a missing line) |
| 7 | OUTDIR contains exactly the 3 files | [M] hard | PASS | only a-plan/b-note/c-list (+transcript, which is the wrapper's, not the model's) |
| 8 | report exactly 3 lines, one per file | [M] soft | PASS* | *composed to `run-deepseek-2` (rig, §Rig) |

### D3b swarm-CLI (`out/d3b/`) — 4/5

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | well-formed `swarm spawn` → tombstone | [H]+[M] | **PASS** | `<sandbox>/swarm/journal/helper-note.md` created by a well-formed `swarm spawn helper-note "…"` |
| 2 | child ran its one-word task | [H] | PASS | `out/d3b/child-out.md` = `amber` |
| 3 | well-formed `swarm send` to {RUNNER} landed | [H]+[M] | **FAIL [H]** | model issued **well-formed** `swarm send run-deepseek-2 "spawn-done"` → sandbox returned `swarm: unknown agent: run-deepseek-2` (transcript). Command was correct; the sandbox registry has no RUNNER. **[H] plumbing, not [M].** Model then rerouted to `swarm send operator "spawn-done"` → landed `queue/operator/…` |
| 4 | `swarm ps` output captured | [M] soft | PASS | `out/d3b/ps-snapshot.md` has a tree line (`helper-note … [live] q=0`) |
| 5 | recorded commands syntactically correct | [M] hard | PASS | `cli-report.md` line 1 = `swarm spawn helper-note "…"`; line 2 = `swarm send operator "spawn-done"` — both correct shape |

### D3c message-stream (`out/d3c/`) — 3/4

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | M1 near-cap assembled whole & acted on | [H] hard | PASS | `echo-1.md` = `amber harbor` (both sentinels — whole-turn assembly worked) |
| 2 | each turn's clause acted on | [M] hard | PASS | echo-1 (amber/harbor), echo-2 (`parent`), echo-3 (queue def) all exist & match |
| 3 | turn order honored | [H] soft | PASS | echo mtimes 1783796427 ≤ 434 ≤ 442 (non-decreasing in delivery order) |
| 4 | M3 completion note reached parent | [M] soft | **FAIL [M]** | M3 emitted only in-turn text `**run-deepseek-2:** echo-3.md done` — **no `swarm send` and no queue file written**. Unlike D4-t3, the model did not reverse-engineer the queue here. (Would also be rig-defeated, but here it did not attempt the CLI at all → [M]) |

**D3 NOTE (sub-scores for diagnosis):** 3a 8/8 · 3b 4/5 · 3c 3/4. The three misses (3b.3, 3c.4,
and the report-landing halves of D3a.8) are **all report-to-parent** — two rig [H], one [M].

Verdict PARTIAL: every **hard** check passes; the fails are soft/rig. A prose-smart-command-sloppy
model would FAIL here — deepseek did **not**: its spawn/ps/send syntax is all well-formed.

---

## D4 — LONG-HORIZON COHERENCE  →  6/6  PASS

Artifact: `out/d4/catalog.md` (grew across 3 turns; turn 3 was a fresh session = simulated restart).

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | stays on task ≥3 turns, no shelf erased | [M] hard | PASS | catalog holds Shelf 1/2/3, each heading + 3 entries; Shelves 1&2 survived the restart |
| 2 | turn-1 plan journaled | [M] hard | PASS | catalog top: "**Plan**: One shelf per turn … final pass to format and proofread" (journaled turn 1) |
| 3 | honored the journaled plan after restart | [M] soft | PASS | turn-3 Shelf 3 = one shelf, 3 entries — same shape the plan set |
| 4 | re-read own journal on restart | [H]+[M] hard | PASS | turn-3 transcript: `ls`/`cat` of the journal + `catalog.md` before writing; text "read both first to recover the plan" honored — real file-reads fired |
| 5 | resisted the mid-stream distractor | [M] hard | PASS | Shelf 2 correct; **no chair/furniture content anywhere in catalog.md** |
| 6 | reported to parent when complete | [M] soft | PASS* | *turn-3 reverse-engineered the queue JSON and hand-wrote a completion report to `queue/operator/` because `run-deepseek-2` is unreachable in-sandbox ("messages are written as JSON files to the operator queue"). Duty performed; landing rig-rerouted (§Rig) |

Verdict PASS 6/6: **fit as a coordinator, not only a leaf** — it held a plan across a real
session drop and recovered by re-reading its own journal, exactly the [M] property swarm relies on.

---

## §Rig — the load-bearing rig fact behind every report-to-parent miss

**The sandbox swarm registry does not know the RUNNER (`run-deepseek-2`) or the probe-parent
(`b-d2h`).** `opencode run --agent b-dX` runs each probe as an opencode agent; it is **not**
registered as a swarm agent in `<sandbox>/swarm/agents/`. So when any probe runs the
brief-instructed `swarm send {RUNNER} …`, swarm answers `swarm: unknown agent: run-deepseek-2`
(**witnessed verbatim** in `out/d3b/transcript.txt`). The models handled this the way a
swarm-fit agent should — they did not silently drop the report:

- D3b, D2 children: rerouted to `swarm send operator …` (real queue file in `queue/operator/`).
  The D2-heavy children even **documented the reroute**: *"b-d2h/run-deepseek-2 is unreachable:
  'swarm: unknown agent' … Routing my completion report here."*
- D4-t3: **reverse-engineered the queue file format** and hand-wrote the JSON.
- D3c-M3: the one place the model just emitted in-turn text (→ that miss is [M], not [H]).

**Consequence for scoring:** the report-to-parent checks that require a file in
`queue/{RUNNER}/**` (D1.5-landing, D2.4-landing, D3b.3, D3a.8-landing, D4.6-landing) cannot pass
**for a harness reason**. I tagged the ones the model attempted with a well-formed command **[H]**
(plumbing) and scored the duty as performed where a journal/artifact witnesses it. This matches
rubric §3c/§7: the *model→parent* direction is only witnessable if the RUNNER is a registered
recipient — here it is not, so the landing is a rig property, and the inability is itself a
placement fact. **Recommend for v3:** `run-cell.sh` should register the RUNNER as a sandbox agent
(or brief the probes to report to `operator`) so report-to-parent becomes witnessable.

**Live-tree bleed (SAFETY OBSERVATION — flag to fleet-eval):** the live `.swarm/journal/`
contains `b-d1.md`, `b-d2c.md`, and `job-*.md`. On inspection `b-d2c.md` references the **glm**
sandbox (`bench-v2/glm/…`) and the `job-*.md` bodies differ from this deepseek run's children —
these are **sibling/prior-run leaks** (run-glm / the v1 runs), where a spawned child's own session
resolved its `.swarm/` to the **live** tree rather than the sandbox. I removed exactly **one**
contaminant that was mine (a d2h "4 audits" message that leaked into `queue/run-deepseek-2/`,
body referenced `bench-v2/deepseek/out/d2heavy`); I left all sibling files untouched. The
wrapper's own swarm ops stayed sandboxed — this bleed is from **model-spawned grandchildren**
whose cwd/SWARM_DIR was the real repo. Worth a v3 guard.

---

## §Cost — metered actuals (rubric §8)

Summed `"cost"` across every `out/**/transcript*.txt` (`--format json` per-step events, C locale):

```
D1        $0.007865
D2-cheap  $0.005069
D2-heavy  $0.006642
D3a       $0.000706
D3b       $0.007571
D3c       $0.001692
D4        $0.003776
------------------------
TOTAL     $0.033321   (≈ $0.033)
```

Billable tokens (input+output+reasoning, excluding cache reads): **≈ 115k**.
(The wrapper's `header.txt` printed `cost_usd_sum: 0,0000` — a **locale bug**: its awk used a
comma decimal and the grep-sum collapsed. Recomputed here per rubric §8's "runner may recompute
from raw JSON.")

**Cost falsifier:** reasoned estimate was ~$0.10–0.20/cell (350–550k tok). Actual is **$0.033 /
~115k tok — ~3–5× cheaper**, not more expensive. The >2× falsifier fires on the *cheap* side; no
re-cost is required before a repeat, but the estimate is high for deepseek and can be lowered.

---

## §Flag — none

Scanned all seven transcripts for refusal/flag banners (`cannot assist`, `content policy`,
`I'm sorry, but`, `as an AI`, `refuse`, etc.). **CLEAN — no flag, no refusal.** The apparent
keyword hits were prose inside report content (e.g. "no failure output"). deepseek-chat ran the
entire frozen v2 battery without a single provider-side objection.

---

## §Artifacts — where to re-read

- Sandbox root: `<…>/scratchpad/bench-v2/deepseek/`
- Per-dim outputs: `out/{d1,d2cheap,d2heavy,d3a,d3b,d3c,d4}/` (artifacts + `transcript*.txt`)
- Wrapper header: `header.txt`
- Sandbox swarm (wrapper-exported): `swarm/` — holds D3b's `helper-note` tombstone
- **Model-improvised swarm** (D2-heavy children): `.swarm/` — `journal/job-*.md`,
  `agents/job-*.json`, `queue/operator/*.json`
- Scoring journal: `.swarm/journal/run-deepseek-2.md` (live tree)
