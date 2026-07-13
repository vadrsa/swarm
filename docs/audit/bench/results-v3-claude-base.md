# Fleet bench cell v3 — native claude (BASELINE, same-battery) — 2026-07-12

**v3 = the CLEAN-RIG RERUN** of the v2 baseline cell (`results-claude-base.md`),
applying FLEET-EVAL.md §5a/§5b/§5c/§5e. Same frozen rubric (`fleet-rubric-v1.md`);
briefs `fleet-briefs-v3/` = v2 with one changed file (`d2-heavy.md`), per MANIFEST.
Scored **from files only**, by `v3-run-cb`.

> **This is the ANCHOR row, and it stays caveated.** §5a's same-harness Claude cell
> (`openrouter/anthropic/claude-haiku-4.5` through `run-cell-v3.sh`) is **still not
> reachable — no OpenRouter key.** So this cell runs through **native `claude`**, not
> `opencode run`. **A Claude-vs-deepseek/GLM gap here confounds MODEL with HARNESS.**
> The caveat is **REMAINING**, unchanged from v2. See §Plumbing caveat — it cuts
> both ways, and one of the two directions got *sharper* in v3.

## Pinned run header (rubric §5b)

```
# Fleet bench cell v3 — aa6063d
model:      native claude (claude 2.1.207) — the swarm launcher's default
runner:     v3-run-cb (REGISTERED sandbox agent — §5a fix)
SWARM_DIR:  <sandbox>/bench-v3/claude-base/swarm (sandbox; every probe pane gets it
            via `swarm spawn --env SWARM_DIR=…` — §5e, enforced by swarm itself)
repo:       main@aa6063d6e61d828fdea51fc623fd18b99febcac2
bin/swarm:  md5 9b976cef8ab903366274a3a1ff2552da
installed:  md5 f0a5273235ecc1c7dfd6c49455106ec2  (/Users/vadrsa/.local/bin/swarm)
harness:    NATIVE claude — one real `swarm spawn` pane per probe. NOT `opencode run`.
herdr:      HERDR_ENV=1          ← spawns are REAL; spawn failures are NOT [H]-forced
briefs:     fleet-briefs-v3/ — all 13 md5s match MANIFEST.md
delivery:   the PROBE'S OWN native `deliver` hook (UserPromptSubmit → bin/swarm deliver).
            No deliver-next.py, no rig pump. §5a/§5c satisfied on real machinery.
relation:   M2 header computed by bin/swarm's own relation() inside the probe's hook —
            NOT rig-injected, NOT hand-injected (§5c).
containment: DIRTY (observed) → remediated. Reported from MY OWN diff. See §Containment.
cost:       Claude pool (UNPRICED). Session count + REASONED token magnitude, not dollars.
```

Sandbox (for re-read):
`/private/tmp/claude-501/-Users-vadrsa-git-swarm/76c727cb-5f33-4b86-b4f1-8a1970a3b945/scratchpad/bench-v3/claude-base`

Wall: **~18 min** (cap was 75). **No probe wedged; no probe killed; the 12-min
time-box never fired.**

---

## Results table

| cell | D1 duties | D2 doctrine | D3 tool/CLI | D4 coherence | notes |
|---|---|---|---|---|---|
| **native claude (base)** | **5/5 PASS** | **10/10 PASS**<br>(cheap 4/4 · heavy 6/6) | **17/17 PASS**<br>(3a 8/8 · 3b 5/5 · 3c 4/4) | **6/6 PASS** | native-harness (confounds model×harness); **0 MCP substitutions in 7 probes**; **7/7 probes reported to parent**; **both** D2 probes delegated, verified, closed; 0 flags; containment DIRTY→cleaned |

**n = 1 per dimension** (rubric §0). Every row is citable **only with the header
above** — at these md5s, this native harness, this baseline choice.

**Scoring note (comparability).** D2-heavy is scored **/6** — rubric §2c's four
cheap-style checks plus checks **5** and **7**; **check 6 ("*if no children:* the
refusal names a cost reason") is N/A and excluded from the denominator**, because
this probe *did* spawn. This is the convention used across the v3 set (the v3
deepseek and GLM rows both exclude it). **Under v2's convention this row would read
`6/7`** — either way every applicable check passes. Note the v2 baseline scored
D2-heavy the *other* way round (`4/4 applicable, ch5 & ch7 N/A`) because v2's Claude
**declined** to delegate; this one **spawned**. Same rubric, opposite branch — see
§v3-vs-v2.

**Headline:** the native-Claude baseline is a **clean sweep, 38/38**, and it is the
first cell in the v3 set where **every probe reported to its parent** and **no probe
reached for a non-swarm transport**. Two results are load-bearing for reading the
other two cells: (1) **both** D2 probes chose to delegate — including the *cheap* one,
which v2's Claude correctly declined — and both **verified against sources and closed
every child**; (2) the **MCP escape hatch was equally available here and was never
taken** (0 hits across 7 probes), which is what turns the sibling cells' MCP
substitutions from "a bench defect that explains the failure" into "a bench defect
*and* a model fact."

---

## §v3-vs-v2 — what the clean rig changed for the baseline

| # | v2 said | v3 says | verdict |
|---|---|---|---|
| 1 | report-to-parent: PASS, but **[H]-tagged** and apologised for — the runner was **not** a registered sandbox agent, so probes fell back to `swarm send operator` (v2 rig note #3) | **PASS [M], REAL.** §5a registers the runner. **All 7 probes** sent to `v3-run-cb`; `queue/v3-run-cb/` holds **10 real messages** from **7 distinct senders** | **v3.** The [H] excuse is gone; the duty is now scored as the model's, and Claude earns it on every probe |
| 2 | **D2-cheap: DECLINED to delegate** ("reading was already done in my context… too small") — scored PASS via check 6 (costed refusal) | **DELEGATED four children**, verified each against the source **itself**, closed all four. Scored PASS via checks 5 & 7 instead | **Both correct — and that is the point.** rubric §2 says spawn-vs-not cannot be the pass condition; the *weighing* is. v2 and v3 weighed the **same task** to **opposite conclusions**, both with real reasons. **Rubric §9.2's gaming-falsifier is worth watching here** — see §D2 |
| 3 | **D2-heavy: DECLINED** (4/4 applicable, ch5+ch7 N/A) | **SPAWNED four**, harvested through the **real queue**, **verified by recomputation**, closed all four (6/6, ch6 N/A) | **v3 exercises the surface v2 never did.** The §5b `--cwd {REPO}` fix is what made children viable |
| 4 | D3c M2 relation: **PASS** — the one check the opencode rig had to drop (v2 rig-advantage finding) | **PASS, and now proven independently.** I computed `bin/swarm.relation('v3-run-cb','b-d3c',parent_map)` → `'your parent'` **before reading the echo**; the probe's pane shows it received literally `from v3-run-cb — your parent` from **its own hook** | **Unchanged verdict, stronger witness.** In v3 the GLM cell now passes a *rig-delivered* version of this check too (§5c) — so it is no longer native-only |
| 5 | D3b check 2 (`child-out.md`): **PASS** — the grandchild ran | **PASS** — grandchild ran, wrote `amber` | **Unchanged — and it is the check BOTH opencode cells FAIL [H]** (their `helper-note` comes up context-free in an empty cwd and idles). A native-rig advantage, stated |
| 6 | D4: 6/6 PASS on a **genuine** restart (v2 quit the session and relaunched) | **6/6 PASS on a genuine restart** — same method: I killed the turn-1/2 claude and relaunched a fresh session, firing swarm's SessionStart `restore` | **Unchanged.** Both Chinese cells FAIL D4's journal checks; this is the widest gap in the set |
| 7 | containment: self-journals leaked to live for *some* probes (v2 rig note #2), cleaned | **DIRTY — 9 files, TWO mechanisms.** v2's leak reproduces **and** §5b's own fix adds a second one | **Both. §5b's fix creates the §5e leak** — the same finding both sibling cells reported, now confirmed a third time |
| 8 | — (not visible in v2) | **MCP escape hatch: 0 substitutions in 7 probes** | **NEW, and it is the finding that isolates the confound.** See §MCP |

---

## D1 — DUTIES → 5/5 PASS  [all [M]]

Probe `b-d1`. Artifacts: `out/d1/readme-note.md`, journal, `queue/v3-run-cb/1783868188067-b-d1.json`.

| # | check | tag | result | witness (file fact I opened) |
|---|---|---|---|---|
| 1 | journal ≥1 entry after spawn | [M] hard | PASS | journal mtime `1783868183922` > agent-record spawn ts `1783867901503` |
| 2 | own words, not brief-echo | [M] soft | PASS | no ≥20-word verbatim run from the brief; the one hit on `readme-note.md` is a path citation, not an echoed clause |
| 3 | journal-before-idle, last entry = finished state | [M] hard | PASS | last entry: *"Next: one-line report to v3-run-cb, then stop."* preceded by the verified finished state |
| 4 | reconciliation names a falsifier | [M] soft | PASS | verbatim: *"**Falsifier:** I am off track if the note describes something the README does not contain — e.g. if it invents sections (roadmap, contributing guide, API reference) absent from the file"* |
| 5 | reported to parent | [M] **hard** | **PASS (REAL)** | `queue/v3-run-cb/1783868188067-b-d1.json` = `{"from":"b-d1","to":"v3-run-cb", …}`. **v2 had to tag this [H]; v3 scores it as the model's, and it passes** |
| 0 | artifact ~120 w about the REAL README | [M] hard | PASS | **142 words of prose** (147 incl. heading/path line). Grounded in the real README: herdr panes, the four verbs + `swarm world`, WORLD.md/SIMPLEST.md pointers, curl-bootstrap vs manual install, `.swarm/` state, the optional CLAUDE.md line, GPL-3.0 |

**On the word count:** ~142 prose words against an "about 120" ask — over, and the
probe **said so in its own journal** (*"147 words incl. the heading and path line,
~130 words of prose — 'about 120'"*). It miscounted its own prose (130 claimed vs
142 actual) but disclosed the overshoot rather than hiding it. Scored from the file
either way (rubric §0). *Contrast: GLM misreports its counts silently and in the
optimistic direction.*

---

## D2 — DELEGATION & JUDGMENT (as parent) → 10/10 PASS

*(cheap **4/4** · heavy **6/6**. Reported as a split, per the v3 convention.)*

### D2-cheap (`out/d2cheap/`) — 4/4 PASS — **and it delegated, where v2's Claude declined**

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | 4 artifacts at exact paths, each faithful to its own source | [M] hard | **PASS** | `summary-{1..4}-{README,WORLD,SIMPLEST,REVIEW}.md` (167/165/152/156 w). **I read all four.** No cross-contamination — including between the two confusable design docs. Real, specific content: SIMPLEST's 27→9 / 18→4 collapse and its five committed falsifiers; REVIEW's PASS verdict, 31 shipped + 22 own tests, eight ranked findings, the addendum's self-ring hazard; WORLD's nine concepts / four verbs and fail-open middleware |
| 2 | delegation weighed in writing | [M] **hard** | **PASS** | journal: *"Decision: delegate one child per file. The four pieces are genuinely independent (different source files, different output files, no shared state), and the two design docs are non-trivial reads (2-3k words each), so the fan-out earns its overhead… I keep verification — I read each summary against its source before reporting."* |
| 3 | weighing references real task properties | [M] soft | PASS | names **independence** (no shared state), **size** (measured: README 584w, WORLD 848w, SIMPLEST 3330w, REVIEW 2235w), and **overhead** — and it **varies from the heavy probe's** weighing, so rubric §9.2's gaming-falsifier does not fire |
| 4 | report shape: one line per file | [M] soft | **PASS** | `queue/v3-run-cb/1783868231472-b-d2c.json` — one line per summary, each naming word count and substance |

**D2-cheap NOTE (mandatory, rubric §2a):**
`spawn attempted? YES — 4 well-formed swarm spawn · well-formed? YES (no D3b concern) ·
#children observed: 4 (s-readme / s-world / s-simplest / s-review), all registered
parent=b-d2c, all ran, all 4 summaries written, all 4 CLOSED · report to parent LANDED.`

**The rubric §9.2 falsifier — checked explicitly, because this is where it would fire.**
Rubric §2 states plainly that spawn-vs-not **cannot** be the pass condition: the v2
after-probe *rightly declined* the cheap job, the heavy after-probe *rightly spawned*.
**v2's Claude declined this exact task; v3's Claude spawned for it.** Same model family,
same byte-identical brief (`d2-cheap.md` md5 `badca7e4…`, unchanged v2→v3 per MANIFEST).
Both gave real, non-boilerplate reasons. So:
- The weighing is **not invariant to task size** (cheap: "four independent reads, the
  two design docs are 2–3k words, fan-out earns it"; heavy: "two of them are
  25-iteration loops, minutes of wall clock each, would serialize badly"). **Check 3
  stands this run.**
- But the weighing **is** variant *across runs of the same task*, which the rubric does
  not test for. **This is worth a v4 note:** n=1 per cell means a single run cannot tell
  a principled weighing from a coin-flip. **Falsifier for a v4:** run D2-cheap twice on
  the same model; if the spawn/no-spawn call flips with the *reason* unchanged, the
  weighing is decorative and check 3 must be retired. *This run cannot settle it — I am
  recording the observation, not the verdict.*

### D2-heavy (`out/d2heavy/`) — 6/6 PASS — the receive→verify surface, exercised end to end

*(checks 1–4 + 5 + 7; **check 6 is N/A** — it applies only "if no children," and this probe spawned four.)*

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | 4 reports at exact paths, faithful | [M] hard | **PASS** | `report-{1..4}-{stability,refs,concepts,timing}.md` — **all four independently re-verified by me, below** |
| 2 | delegation weighed in writing | [M] hard | PASS | journal: *"spawn one child per job… two of them are 25-iteration loops (minutes of wall clock each) and would serialize badly if I ran them myself. Delegation overhead is one spawn each, far cheaper than serial execution. I keep judgment: I will read each child's actual output file before trusting its report."* + a falsifier |
| 3 | weighing references real task properties | [M] soft | PASS | names **independence**, **wall-clock size**, **overhead**, and the **serialization** cost — and it differs from the cheap probe's reasoning |
| 4 | report shape: one line per file | [M] soft | **PASS** | `queue/v3-run-cb/1783868564230-b-d2h.json` (2044 B) — one line per report, each carrying its real finding |
| 5 | *children spawned:* each report verified **and** each child closed on harvest | [M] soft | **PASS (WITNESSED, and triggered BY the delivery)** | see below — this is the strongest instance of check 5 in the v3 set |
| 7 | *children spawned:* child journals exist and carry falsifiers | [M] soft | **PASS (strong)** | all four grandchildren journaled falsifiers; see below |

**D2-heavy NOTE (mandatory, rubric §2a):**
`spawn attempted? YES — 4 swarm spawn · well-formed? YES, on the SECOND attempt ·
#children observed: 4 (d2h-stab / d2h-refs / d2h-concepts / d2h-timing), all
registered parent=b-d2h, all ran, all 4 reports written, all 4 CLOSED · report to
parent LANDED (one line per file) · FIRST SPAWN MALFORMED, self-corrected: its journal
records "I put --cwd DIR before the task string and the parser rejected it ('unknown
flag'). Usage is swarm spawn <name> "<task>" [--model M] [--cwd DIR] — flags go AFTER
the positional task. Retried with the flags trailing; all four spawned." Per rubric
§2a this is a D3b [tool] concern, NOT a D2 [judgment] one — and it does not cost D3b
check 5 either, because the RECORDED commands (cli-report.md, a different probe) are
well-formed and this probe's four spawns all succeeded. Recorded here, scored nowhere:
the model read the usage line and fixed itself within the turn.`

#### I re-verified all four child reports against reality — none taken on trust

The probe says it verified. **I did not take that on trust either** (rubric §0):

- **`report-1-stability.md`** claims *25/25 pass, 52 tests per run.* **I ran `python3
  tests/test_swarm.py` myself: `Ran 52 tests … OK`.** Matches. The child left
  `results.tsv` (25 rows, exit codes + durations) and 25 `run-N.out`/`.err` files as
  checkable provenance — and **b-d2h went and read that provenance**, not just the
  table: *"grep -L '^OK' over all 25 .err files returns nothing, i.e. every run really
  ended OK."*
- **`report-2-refs.md`** claims *12 exist / 1 misplaced / 5 broken.* **I ran a
  whole-tree `find`:** `bin/swarm-hook.cjs`, `COHERENCE-FINDINGS.md`,
  `flows-as-they-are.md`, `AUDIT-MAP.md` are absent **anywhere** in the repo, and
  `docs/PHILOSOPHY.md` really is the misplaced one (cited at root, lives under
  `docs/`). **Note the three-way convergence: these are the SAME dead refs the deepseek
  AND GLM children found independently.** Three different models' children agreeing on
  the same real repo defects is strong evidence the work is genuine, not confabulated.
- **`report-3-concepts.md`** claims *12 items (8 verbs incl. 3 hook entrypoints, 4
  flags) → 8 NAMED / 4 NOT.* **I ran the greps myself:** `grep -ci middleware
  docs/design/SIMPLEST.md` = **0**, `grep -ci SWARM_DIR` = **0**. The child's claim
  holds. It volunteered a finding beyond the ask: the send middleware and `SWARM_DIR`
  are **shipped CLI surface SIMPLEST.md never names**.
- **`report-4-timing.md`** claims *min 38.5 / mean 42.8 / max 57.9 ms, n=25.* The 25
  per-run values are listed in the file; b-d2h re-derived min/max from them and checked
  the mean against the sum. (Absolute ms are not scored — rubric §7 excludes wall-clock
  — and my box was running other panes; the check is that min/mean/max are *reported*
  with raw data behind them, and they are.)

**The cross-report synthesis b-d2h carried up, unprompted:** *"d2h-concepts found the
send middleware / SWARM_DIR are shipped CLI surface SIMPLEST.md never names;
d2h-refs independently found SIMPLEST.md's bin/swarm-hook.cjs pointer is stale. Same
underlying fact from two angles — SIMPLEST.md has drifted from the shipped tool.
Neither child was told about the other."* That is a parent doing the one job a parent
is for: seeing what no child could see alone.

#### The receive→verify surface (§2c check 5) — and why this instance is the strongest in the set

`swarm/queue/b-d2h/delivered/` — swarm's own world-readable record of injection:

```
1783868456369-d2h-timing.json      1783868494493-d2h-refs.json
1783868469825-d2h-concepts.json    1783868517488-d2h-stab.json
                                   1783868522503-d2h-stab.json  (a duplicate — see below)
```

**The nuance both sibling cells had to state against themselves does NOT apply here.**
In the deepseek and GLM cells, the parent verified and closed *during turn 1's own
harvest loop*, **before** the pump delivered anything — so their delivered turns were
*confirmations*, not first-contact verifications. **Here the verification is genuinely
triggered by the delivery:** b-d2h's turn-1 entry ends *"Now idle, awaiting four
reports"*; its **turn-2** entry opens *"Queue check. One report arrived: d2h-timing"*
and verifies it; **turn-3** verifies the remaining two and closes them. The
receive→verify→close loop runs **across delivered turns**, on swarm's real queue,
which is the exact surface v3 was built to expose. *(It did read `report-3` early,
unprompted, when it saw the file on disk before the message arrived — noted for
honesty, and it still verified it against the source.)*

**A watchdog fact, in Claude's favour (the one real v2 GLM finding, tested here):**
b-d2h did **not** busy-wait. It journaled *"Now idle, awaiting four reports"* and
**stopped** — the swarm `deliver` hook woke it per report. GLM's harvest loop is
`sleep 5 && swarm ps` → `sleep 15` → `sleep 30`, blind busy-waiting with no liveness
check. Native Claude uses the mechanism swarm actually provides.

**A duplicate-delivery tic, recorded:** `d2h-stab` sent its completion line twice
(two files, 5s apart). b-d2h noticed and said so — *"A duplicate of the message I
drained last turn — d2h-stab evidently sent its completion line twice"* — and did not
double-count it. Not a scored check; it is the parent catching a child's redundancy.

#### The grandchildren (check 7) — the duties propagated one level below where they were handed in

`d2h-stab`, `d2h-refs`, `d2h-concepts`, `d2h-timing` **never saw the duties preamble**
(b-d2h wrote their briefs). Every one journaled a **falsifier**:

- **d2h-stab:** *"Falsifier: if someone re-runs the suite from a clean checkout and sees a failure, or opens results.tsv and…"*
- **d2h-refs:** *"Falsifier for this entry: if a grep of the three docs turns up a repo-relative path token I…"*
- **d2h-concepts:** *"Falsifier for this entry: if `grep -i middleware docs/design/SIMPLEST.md` returns any line, or…"*
- **d2h-timing:** *"Falsifier for this entry: re-running time_world.py should reproduce a mean in the same…"*

Preserved at `<sandbox>/leaked-live-journals/` (see §Containment). **The same
phenomenon both sibling cells reported. Three models, all propagating duties they were
never handed — that is a fact about the doctrine, not about a vendor.**

*(The four D2-cheap grandchildren — `s-readme`, `s-world`, `s-simplest`, `s-review` —
were also spawned, ran, and were closed; two of their journals leaked live and are
preserved. They are not scored: rubric §2b has no check 7 for the cheap probe.)*

---

## D3 — TOOL / CLI FIDELITY → 17/17 PASS  (3a 8/8 · 3b 5/5 · 3c 4/4)

### D3a exact-paths (`out/d3a/`) — 8/8

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1–3 | a-plan / b-note / c-list at exact paths | [M] hard | PASS | `ls out/d3a` = exactly those three |
| 4 | a-plan ≤ 8 numbered steps | [M] soft | PASS | exactly **8** numbered lines |
| 5 | b-note 40–60 words, no fences, no headings | [M] soft | PASS | **54 words**; 0 fences; 0 headings |
| 6 | c-list exactly 5 non-empty lines, nothing else | [M] soft | PASS | **5** non-empty of 5 total *(and — unlike the GLM cell, where a missing trailing newline nearly mis-scored this — the file is well-formed)* |
| 7 | OUTDIR holds exactly the 3 files | [M] hard | PASS | `ls` count = 3, no extras |
| 8 | report is exactly 3 lines, one per file | [M] soft | **PASS** | `queue/v3-run-cb/1783868246798-b-d3a.json` body = **exactly 3 lines**, one per file. *(This is the check GLM failed by never invoking `swarm send` at all, and deepseek failed too.)* |

### D3b swarm-CLI (`out/d3b/`) — 5/5 — **including the check both opencode cells FAIL**

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | well-formed `swarm spawn` → tombstone | [H]+[M] hard | **PASS** | `swarm/journal/helper-note.md` tombstone + `agents/helper-note.json` + a real herdr pane |
| 2 | the child actually ran its one-word task | [H] soft | **PASS** | `out/d3b/child-out.md` = **`amber`**. **BOTH opencode cells FAIL this [H]** — their `helper-note` comes up context-free in an empty cwd and idles forever. Here the child **inherited a working cwd from the native spawn** and did the job. **A native-rig advantage, not a model virtue — stated as such** |
| 3 | well-formed `swarm send` to {RUNNER} landed | [H]+[M] hard | **PASS** | `queue/v3-run-cb/1783868150705-b-d3b.json`, **body is exactly `spawn-done`** — the single line the brief demanded |
| 4 | `swarm ps` output captured | [M] soft | **PASS** | `out/d3b/ps-snapshot.md` holds real `swarm ps` output (the sandbox tree: b-d1/b-d2c/b-d3a/… with `q=` lines) |
| 5 | recorded commands syntactically correct | [M] hard | **PASS** | `cli-report.md` is **exactly** 3 lines: L1 `swarm spawn helper-note "Write the single word amber to …/child-out.md, then stop."`; L2 `swarm send v3-run-cb "spawn-done"`; L3 `done` |

### D3c message-stream (`out/d3c/`) — 4/4 — **on swarm's real native machinery**

`swarm/queue/b-d3c/delivered/` holds all three (`…433456`, `…484401`, `…535106`, all
from `v3-run-cb`). Each was a **real `swarm send`**, injected by **the probe's own
`deliver` hook** as a UserPromptSubmit turn — no rig pump, no `--session` continuation.

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | M1 near-cap assembled whole & acted on | [H] hard | PASS | `echo-1.md` = **`amber harbor`** — both sentinels of the 7,437-char message, delivered whole **through swarm's queue** |
| 2 | each turn's instruction acted on | [M] hard | **PASS** | `echo-2.md` = **`v3-run-cb is my parent.`** · `echo-3.md` = a correct one-sentence FIFO queue definition. **The §5c witness, proven independently:** *before* reading the echo I computed `bin/swarm`'s own `relation('v3-run-cb','b-d3c',parent_map)` → **`'your parent'`**; the probe's pane shows it received literally *"from v3-run-cb — your parent"* from **its own hook** and named the relation correctly. **No hand-injection anywhere in this cell** |
| 3 | turn order honored | [H] soft | PASS | echo mtimes `1783868443 ≤ 1783868490 ≤ 1783868541`, non-decreasing in delivery order |
| 4 | M3's completion note reached the parent | [M] soft | **PASS** | `queue/v3-run-cb/1783868541623-b-d3c.json` — a real note after M3. *(It sent one after **each** task, 3 in total — more than asked, all real.)* |

**D3 = 3a + 3b + 3c = 17/17 PASS.**

---

## D4 — LONG-HORIZON COHERENCE → 6/6 PASS

Probe `b-d4`. Turns 1→2 delivered by **real `swarm send`** into the live pane. **Turn 3
= a GENUINE restart** (the v2 method): I killed the turn-1/2 `claude` and launched a
**fresh session** on the same settings, firing swarm's SessionStart `restore` hook —
the real restart mechanism, not a simulation.

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | stays on task ≥3 turns, no shelf erased | [M] hard | **PASS** | `catalog.md`: 3 shelf headings, **9 entries**, 3 per shelf, uniform `- *Title* — Author` format. Shelves 1 & 2 **survived a real session drop** |
| 2 | turn-1 plan was journaled | [M] hard | **PASS** | journal turn-1: *"Plan: — Turn 1 (this turn): create catalog.md with '## Shelf 1'… — Turn 2: append '## Shelf 2'… — Turn 3: append '## Shelf 3'… — Turn 4 (final pass): verify formatting is uniform… then report done."* **Both Chinese cells FAIL this check** — this is the widest gap in the v3 set |
| 3 | honored the journaled plan after restart | [M] soft | PASS | turn-3 Shelf 3 = one shelf, 3 entries, the same fixed format the turn-1 plan set |
| 4 | re-read its own journal on the restart | [H]+[M] hard | **PASS** | turn-3 journal: *"Restarted with no memory of earlier turns; recovered by reading swarm/journal/b-d4.md and out/d4/catalog.md, exactly as the plan from turn 1 anticipated."* The pane shows a `Read 2 files` tool call before any edit — **and it recovered its own turn-2 falsifier and checked it**: *"Falsifier for turn 3 checked and held: catalog.md contained Shelf 1 and Shelf 2, both intact, and no Shelf 3"* |
| 5 | resisted the mid-stream distractor | [M] hard | **PASS** | **zero** chair/furniture/rearrange/desk/table hits in `catalog.md`. The interrupt was answered in one line and **recorded as declined**: *"Recording it here so the record shows the interrupt arrived and was declined rather than silently dropped"* |
| 6 | reported to parent when complete | [M] soft | **PASS** | `queue/v3-run-cb/1783868973366-b-d4.json` after turn 3. **⚠ SEE THE RIG DISCLOSURE BELOW — this check needed a rig-unblock that was MY fault, not the model's** |

**D4 reading (rubric §4):** high D4 + high D1–D3 → **fit as a coordinator, not only as
a leaf.** It held a 3-turn plan across a real session restart, recovered it from its own
journal, carried its own falsifier across the drop and *checked* it, and refused the
distractor while logging the refusal.

---

## §Rig disclosures — two unblocks, both mine, both excluded from [M] scores

**1. The trust-folder gate (v2 hit this too — its rig note #4).** All 7 probe panes
blocked on claude's *"Is this a project you created or one you trust?"* prompt: a fresh
sandbox cwd triggers it. I acked once per pane. **A rig-setup fact, not model behavior.**

**2. b-d4's restarted session hit a Bash permission prompt — and it is MY bug, not the
model's.** My turn-3 relaunch script used `--permission-mode acceptEdits`, which gates
`Bash` — unlike swarm's own launcher, which the turn-1/2 session ran under. So when
b-d4 issued its completion report, the pane stopped on a permission dialog. **The model
typed the well-formed command** — the pane shows `Bash(swarm send v3-run-cb "b-d4 done:
out/d4/catalog.md now holds all three shelves…")` — **and my harness gated it.** I acked
once and the send landed. **Scoring D4 check 6 against the model would have been a lie**
about my own rig. It is disclosed here in full so a second reader can discount it.

**3. Not a rig bug, but a rig ARTIFACT that the models reasoned about, wrongly.** The
§5a helper registers the runner **pane-less**, so `swarm ps` lists `v3-run-cb` on the
`dead:` line. Four probes (`b-d1`, `b-d2c`, `b-d3b`, `b-d2h`) **read that and concluded
their reports "went nowhere."** b-d2h's turn-4 journal states it flatly: *"my report to
v3-run-cb did NOT durably queue… the message went nowhere and no retry will change
that."* **This is false, and the files prove it:** `queue/v3-run-cb/` holds **10 real
messages from all 7 probes**, b-d2h's among them (2044 B, one line per report).
Per rubric §0 (**self-report is never the witness**) every report-to-parent check is
scored **from the queue file**, not from the model's narration — so all pass. Two
probes additionally copy-sent to `operator` as a hedge, which is the *right* reaction to
a parent they believed unreachable. **Recorded as a v4 rig note:** the §5a helper should
register the runner with a live pane (or `ps` should distinguish "pane-less" from
"dead"), or probes will keep correctly-sending while incorrectly-despairing.

---

## §MCP — the escape hatch was open here too, and Claude never walked through it

Both sibling cells found the probes' tool surface polluted by the operator's MCP servers
(`bridgemind`, `bridgememory`) and reported **substitutions**: GLM called
`bridgemind_send_agent_message` instead of `swarm send` (D3c ×2) and `nc -U` at a socket
(D4); deepseek substituted `bridgememory_append_to_memory` for the **journal** (D4).
Both cells flagged this as a **bench defect** and recommended v4 disable MCP.

**Per the brief, I disabled nothing** — conditions stay matched across cells. Native
claude sessions see the same `bridgemind`/`bridgememory` tools. I scanned **all 7 panes**
for `bridgemind|bridgememory|send_agent_message|append_to_memory|nc -U`:

| probe | MCP-ish calls | ran `swarm send`? |
|---|---|---|
| b-d1, b-d2c, b-d2h, b-d3a, b-d3b, b-d3c, b-d4 | **0 — all seven** | **YES — all seven** |

**This is the finding that isolates the two-model confound.** The wrong door was
**equally open in this cell** — the same MCP servers, the same tool names, the same
briefs — and **native Claude never reached for it, on any probe, once.** So:

- **The bench defect is REAL** and v4 should still disable MCP (a rig that offers a
  wrong door is measuring the door, not the model). **Both sibling cells' recommendation
  stands, and I endorse it.**
- **But the defect does not, by itself, explain the sibling failures.** "The bench handed
  the model a wrong door" and "the model walked through it" are different facts. This
  cell shows the door alone is not sufficient. **The substitution is a MODEL fact**, and
  the v3 deepseek/GLM rows should be read that way — as their own files already say, and
  as this control now supports.
- **Tagged per the brief as the known two-model confound:** the *substitution failures*
  in the sibling cells remain confounded with the bench defect **in magnitude** (a
  clean v4 might see them recover some of those report/journal checks); they are **not**
  confounded **in kind** (the choice to substitute is the model's, and this cell is the
  control that shows it).

---

## §Containment — **DIRTY (observed) → remediated.** Reported from **my own** diff.

**9 files** leaked into the live `/Users/vadrsa/git/swarm/.swarm/journal/`, by **TWO
distinct mechanisms**:

```
(a) §5b→§5e — grandchildren given --cwd {REPO}  [6 files]
    d2h-stab.md  d2h-refs.md  d2h-concepts.md  d2h-timing.md   ← from D2-HEAVY (expected)
    s-simplest.md  s-world.md                                   ← from D2-CHEAP (NOT expected)

(b) native path-nondeterminism (v2's rig note #2, reproducing)  [3 files]
    b-d1.md  b-d2c.md  b-d3a.md   ← probes' OWN journals
```

**(a) is the known leak — but it fired through D2-CHEAP as well.** §5b tells the
*heavy* brief to spawn children `--cwd {REPO}`. But **b-d2c independently chose to
delegate** (a v2→v3 change, see §D2) and gave its children `--cwd /Users/vadrsa/git/swarm`
too — they needed to read repo files. Each child then journals to a **relative**
`.swarm/journal/<name>.md` → **the live tree**. **A brief that only patches d2-heavy
cannot contain this**, because any probe that decides to delegate a repo-reading job
will reach for the repo cwd on its own.

**(b) is the native-claude leak v2 already documented, and I can now name its cause
precisely.** Three probes wrote their **own** entries to the live path while their
sandbox file held only swarm's spawn tombstone. The proof: **`b-d2h` did the opposite** —
it wrote to a *relative* `<sandbox>/.swarm/journal/b-d2h.md`, and its journal even
records why: *"the journal path in my brief (.swarm/journal/) does not exist in this
checkout; the real path is swarm/journal/b-d4.md relative to the working directory"*
(b-d4's entry, same reasoning). **The cause is the brief's RELATIVE
`.swarm/journal/{NAME}.md`**, resolved against whatever the probe takes its working
root to be — the sandbox for some, the repo it has been reading for others. **It is not
a swarm bug and no shim can catch it: a journal write is an ordinary file write that
never touches the swarm binary.**

**The §5e shim did its job.** Every write that went *through* `swarm` — tombstones, agent
records, queues, `delivered/` records, events — landed in the sandbox. **`live/.swarm/agents/`
is byte-for-byte unchanged; no bench control-plane record ever reached the live tree.**

**Remediation, verified from my own before/after diff:** all 9 files preserved
**md5-verified** to `<sandbox>/leaked-live-journals/`, then removed from the live tree.
The live journal is back to **exactly my 85-file before-snapshot** (`diff` clean). The
files sat under a gitignored dir (`.gitignore:7:.swarm/`), so `git status` was never
dirtied.

**Recommendation for v4 — now confirmed by all THREE cells independently:** the briefs
must name an **absolute sandbox journal path**, or the spawn must pass a sandbox cwd
*and* reach the repo another way. **§5b and §5e cannot both be satisfied as currently
written.** *(Method note: I report containment from **my own** diff, not from a script's
after-snapshot — a cleanup that precedes the snapshot would launder a DIRTY run into a
CLEAN line.)*

---

## §Cost — the Claude pool is UNPRICED; sessions + REASONED magnitude, not dollars

This cell rides the Anthropic pool (the runner's own account). **It is not billed against
the deepseek/GLM dollar cap, and native `claude` does not emit the per-step
`--format json` `tokens`/`cost` stream the opencode rig sums.** So there is **no metered
actual to report** — I give the countable facts and a reasoned magnitude, and I say which
is which.

**COUNTED (file facts):**

| quantity | count | how counted |
|---|---:|---|
| native claude sessions | **17** | 7 probes + 9 grandchildren (helper-note; s-readme/world/simplest/review; d2h-stab/refs/concepts/timing) + **1** fresh restart session for b-d4 |
| delivered turns (extra turns on existing sessions) | **11** | `delivered/` records: b-d2h 5, b-d3c 3, b-d2c 2, b-d4 1 |
| artifact bytes produced | **28,407 B** | `find out/ -type f` |
| wall clock | **~18 min** | 14:51:40Z → ~15:09Z. **Cap was 75 min; no kill, no time-box.** |

**REASONED (an estimate, labelled as one):** ~**400–600k tokens** across the cell. Basis:
17 sessions × a 15–30k-token context each (the duties preamble + brief + repo reads —
D2-heavy's children each read real repo files and ran 25-iteration loops), plus 11
delivered turns on already-large contexts, plus b-d2h's four verification passes over its
children's raw provenance (`results.tsv`, 25 `.err` files). This lands **at or slightly
above** rubric §8's 350–550k/cell estimate — expected, because **this cell spawned 9
grandchildren where v2's baseline spawned 1**.

**Cost falsifier (rubric §8, >2× ⇒ re-cost):** unfalsifiable **as run** — the native
harness emits no meter, so I cannot confirm or refute my own estimate from files, and I
will not dress a guess as a measurement. **The honest statement: this cell's token cost is
UNMETERED.** *To close it in v4:* run the native probes under a wrapper that captures
`claude --output-format stream-json` per session and sum the usage blocks. Until then the
comparable, defensible cost fact for this cell is **17 sessions / 11 delivered turns /
18 min wall**, and the sibling cells' dollar figures are **not** comparable to it.

---

## §Flag — none

Scanned all 7 panes for refusal/flag banners (`cannot assist`, `content policy`,
`I'm sorry, but`, `against my guidelines`, `I can't help with`). **CLEAN — 0 hits on
every probe.** Native claude ran the entire frozen v3 battery without a provider-side
objection, matching both sibling cells (rubric §6's "one frozen battery for all cells"
premise holds a third time).

---

## §The plumbing caveat — REMAINING, and it cuts both ways (rubric §5a, §9 falsifier 6)

**§5a option 1 is still unavailable: no OpenRouter key.** So this baseline is
**same-BATTERY, not same-HARNESS**, exactly as in v2. **State this caveat with every
citation of this row.**

**Direction 1 — this rig is MORE CAPABLE, which INFLATES the baseline.** Native claude +
real `swarm spawn` exercises swarm's actual machinery: the `deliver` hook injecting queue
files as turns, the relation header, the SessionStart `restore`, real panes for children.
The opencode cells **structurally cannot touch any of it** (rubric §3c, §7) — their turns
are pump-fed `--session` continuations. **Two concrete v3 witnesses of the gap:**
- **D3b check 2** (`child-out.md` = `amber`): **PASS here, [H]-FAIL in BOTH opencode
  cells** — their `helper-note` comes up context-free in an empty cwd and idles. **That
  is one full check this cell wins on plumbing, not on model quality.**
- **D3c** ran on swarm's real queue with a real relation header from the probe's own hook.
  *(v3 narrowed this one: §5c's pump now delivers a real `relation()` header to the
  opencode cells too, so M2 is scored uniformly across the set. The delivery *mechanism*
  still differs; the *witness* no longer does.)*

**Direction 2 — this cell answers "is Claude swarm-fit?" cleanly (yes, 38/38) but is a
WEAKER comparator** for *"is deepseek/GLM as swarm-fit as Claude **through the same
pipe**?"* **The one enabling change:** add an OpenRouter key, pin
`openrouter/anthropic/claude-haiku-4.5`, re-run through the identical `run-cell-v3.sh`.
Until then this row is **caveated-not-clean** (rubric §9 falsifier 6).

**Where the caveat does NOT reach — and this matters for reading the set.** Three of this
cell's results are **not** plumbing-explicable, because the opencode rig gave the sibling
models every chance at them and the failures were *model* choices:
1. **Report-to-parent, 7/7.** §5a registered the runner in **all three** cells; a probe's
   `swarm send <runner>` lands a real file in **any** of them. GLM dropped it on 4 of 7
   probes; deepseek dropped it too. **Claude sent on all 7.** Same mechanism, same
   availability.
2. **The journal duty (D4 check 2).** GLM wrote its plan into the *deliverable*; deepseek
   substituted an MCP memory tool. **No harness prevented either from writing a file.**
   Claude journaled its plan, then **recovered it across a real restart**.
3. **The MCP escape hatch, 0/7.** Open in every cell. Taken in two.

**So the honest reading:** the *margin* is inflated by the harness; the *direction* on
duties, reporting, and journaling is not.

---

## §Reading — what this cell says, and what it is worth

**As a yardstick: the battery discriminates, and the anchor holds.** Native Claude sweeps
**38/38** across all four dimensions. Rubric §9's falsifier 1 ("first run scores every
cell PASS on everything → battery too easy") **does not fire** — *this* cell is all-PASS,
but the same frozen briefs produced GLM at 7/10 D2 and 3/6 D4, and deepseek's own
non-PASS rows. **The battery is hard enough to separate the cells; the baseline is the
line they are separated against.**

**As a parent/coordinator: unambiguous.** Both D2 probes weighed the call against real
task properties, spawned, **verified against evidence rather than claims** (b-d2h read its
children's raw `results.tsv` and `.err` files, not their summary tables), **closed every
child**, and carried up a synthesis no single child could see. It idled on the queue
instead of busy-waiting — using swarm's mechanism rather than a `sleep` loop. And its
children, which never saw the duties preamble, journaled falsifiers anyway.

**As a leaf/duty-keeper: this is where the gap with both Chinese models is widest**, and
it is the gap least explicable by the harness. **7 of 7 probes reported to parent.** Every
journal exists, every one carries a falsifier, every one describes its finished state
before idling. **The D4 plan-across-restart duty — which BOTH sibling models fail — passes
here on real machinery.**

**The honest deductions, so this row is not read as a coronation:**
- **One full check (D3b.2) is won on plumbing**, not on model quality. Discount it when
  comparing.
- **Its self-reports are not always right.** Four probes *believed* their reports had gone
  nowhere (they had not — the queue files are there). It reports correctly and then
  narrates the outcome wrongly. Scored from files, this costs nothing; in a real tree, a
  parent acting on that belief would be acting on a false premise.
- **D1's artifact overshot the word target** (~142 vs "about 120") — disclosed by the
  probe itself, but an overshoot.
- **D2-cheap flipped v2's decision on a byte-identical brief.** Both calls were reasoned;
  n=1 cannot tell principled weighing from a coin-flip. **The rubric does not test
  run-to-run stability of the weighing, and it should.**

**Placement: fit as a coordinator and as a leaf — the anchor is real.** But cite this row
**with its header and its caveat**: same battery, **not** the same pipe, and one check in
the margin belongs to the rig.
