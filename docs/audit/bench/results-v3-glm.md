# Fleet bench cell v3 — zai-coding-plan/glm-4.7 — 2026-07-12

**v3 = the CLEAN-RIG RERUN** of the v2 cell (`results-glm.md`), applying
FLEET-EVAL.md §5a/§5b/§5c/§5e. Same frozen rubric (`fleet-rubric-v1.md`); briefs
`fleet-briefs-v3/` = v2 with one changed file (`d2-heavy.md`), per MANIFEST.
Scored **from files only**, by `v3-run-glm`.

> **Read this row against v2, not alone.** v3's purpose was to make three
> previously-unwitnessable surfaces real. It did — and for GLM the result runs
> **opposite** to deepseek's: **GLM scores BETTER than v2, because v2's rig was
> manufacturing failures that were never GLM's.** v2's headline finding —
> *"spawned 8 children, all DIED, model HUNG 35 minutes"* — **does not reproduce.**
> It was a rig artifact. What v3 finds instead is a different, real weakness.

## Pinned run header (rubric §5b — verbatim from `header.txt`)

```
# Fleet bench cell v3 — aa6063d
model:      zai-coding-plan/glm-4.7
runner:     v3-run-glm (REGISTERED sandbox agent — §5a fix)
SWARM_DIR:  <sandbox>/bench-v3/glm/swarm (sandbox; shim-pinned for all model swarm calls — §5e)
repo:       main@aa6063d6e61d828fdea51fc623fd18b99febcac2
bin/swarm:  md5 9b976cef8ab903366274a3a1ff2552da
installed:  md5 f0a5273235ecc1c7dfd6c49455106ec2  (/Users/vadrsa/.local/bin/swarm)
opencode:   1.17.13
herdr:      HERDR_ENV=1          ← spawns are REAL; spawn failures are NOT [H]-forced
briefs:     fleet-briefs-v3/ — all 14 md5s match MANIFEST.md
delivery:   deliver-next.py (imports bin/swarm; byte-exact next_delivery) — §5a/§5c
relation:   M2 header rig-delivered via bin/swarm relation() — scored uniformly (§5c)
containment: header says "DIRTY" — TRUE, and remediated. See §Containment.
cost_usd_sum: 0.0000  ← ✗ A METER ARTIFACT, NOT A REAL ZERO. See §Cost.
```

Sandbox (for re-read):
`/private/tmp/claude-501/-Users-vadrsa-git-swarm/76c727cb-5f33-4b86-b4f1-8a1970a3b945/scratchpad/bench-v3/glm`

Wall: ~26 min. **No probe wedged; no probe killed; no time-box fired.**

---

## Results table

| cell | D1 duties | D2 doctrine | D3 tool/CLI | D4 coherence | notes |
|---|---|---|---|---|---|
| zai-coding-plan/glm-4.7 | **5/5 PASS** | **7/10 FAIL**<br>(cheap 1/4 FAIL · heavy 6/6 PASS) | **14/17 PARTIAL**<br>(3a 7/8 · 3b 4/5 · 3c 3/4) | **3/6 FAIL** | no flag; D2-heavy delegation real+verified+closed; **report-to-parent dropped 4 of 7** and *never once by malformed syntax*; **MCP escape hatch found (bench defect)** |

**Scoring note (comparability).** D2-heavy is scored **/6** — rubric §2c's four
cheap-style checks plus checks **5** and **7**; **check 6 ("*if no children:* the
refusal names a cost reason") is N/A and excluded from the denominator**, because
GLM *did* spawn. (v2's GLM row kept ch6 in the denominator as `3/7`; the sibling v3
deepseek row excluded it. Excluding an inapplicable check is the honest reading, and
it is the convention used across the v3 set. Under v2's convention this row would
read `6/7 PARTIAL` — either way the **verdict is PASS/PARTIAL on all hard checks**.)
D2's combined verdict is **FAIL** because D2-cheap's **hard** check 2 fails (rubric
§0: any hard check fails ⇒ FAIL), *not* because the heavy delegation was weak — it
was the best in the v3 set. **Read the two sub-probes separately; the combined number
hides the finding.**

**Headline:** GLM-4.7 is **a competent, verifying, closing parent and a strong
tool-user — whose duty-keeping fails through the wrong door, not through
incompetence.** Its `swarm` grammar is impeccable (every command it typed, all
run, was well-formed). Its D2-heavy run is the best delegation performance in the
v3 set: it weighed, spawned four, **verified each report against the child's
actual output file**, closed all four, and reported up. But it **drops the
report-to-parent duty on 4 of 7 probes** and **never journaled its D4 plan** —
and, decisively, **two of those failures are it reaching for the WRONG TOOL**
(an inherited MCP `send_agent_message`; a `nc -U` unix socket) rather than
forgetting the duty. That distinction is new in v3 and it changes the reading.

---

## §v3-vs-v2 — what the clean rig changed (the reason this file exists)

| # | v2 said | v3 says | verdict |
|---|---|---|---|
| 1 | **D2-heavy 3/7 PARTIAL: "spawned 4→8, ALL children DIED, model HUNG 35 min, no watchdog"** | **6/6 PASS.** 4 children spawned, **all 4 ran**, all 4 reports real, all 4 **verified against their own files**, all 4 **closed**, report landed | **RIG ARTIFACT.** v2 spawned children into an **empty sandbox cwd** → context-free `claude` sessions that died. §5b's `--cwd {REPO}` fixes it. **v2's headline GLM finding is void.** |
| 2 | report-to-parent: `FAIL [H]`, excused — *"unknown agent: run-glm-2, no sandbox mailbox"* | **Real.** §5a registers the runner. `queue/v3-run-glm/` holds **3 actual sends** (`b-d1`, `b-d2h`, `b-d3b`) | **v3.** The excuse is gone — GLM **passes** where it sends, and **fails honestly** where it doesn't |
| 3 | D3c M2 relation: **check DROPPED** as unwitnessable (§7); its v2 stand-in **FAILED** (echoed the brief back) | **PASS [M]** — `echo-2.md` = `your parent`, byte-identical to `bin/swarm`'s own `relation()` | **v3 makes a dropped check real, and GLM — which failed v2's proxy — passes it** |
| 4 | D2-heavy receive→verify: unwitnessable | **WITNESSED** — 4 child reports crossed the real queue into `delivered/`, consumed as pumped turns | **v3.** The surface v3 was built to expose |
| 5 | D3b 2/5, `child-out.md` PASS (v2's child ran) | **4/5**, `child-out.md` **FAIL [H]** — child idles context-free | **Rig delta both ways** — see §D3b. GLM's *score rises*; the one loss is not its fault |
| 6 | D4 4/6 FAIL — no plan journal | **3/6 FAIL** — still no plan journal, **but it wrote the plan into `catalog.md` instead**; and ch6 now fails honestly (v2's report-drop was excused as [H]) | **Both right; v3 explains the mechanism** |
| 7 | — (not visible in v2) | **MCP escape hatch**: GLM calls `bridgemind_send_agent_message` instead of `swarm send` (D3c ×2), and `nc -U` at a socket (D4) | **NEW — and a BENCH DEFECT.** Same class ds-cell found. See §MCP |
| 8 | containment: live `.swarm/` "UNTOUCHED — verified" | **DIRTY** — 4 grandchild journals leaked into the live tree | **v3.** §5b's own fix causes it (§Containment) |

---

## D1 — DUTIES  →  5/5  PASS

Artifacts: `out/d1/readme-note.md` (120 w), `.swarm/journal/b-d1.md`,
`swarm/queue/v3-run-glm/1783866254787-b-d1.json`.

| # | check | tag | result | witness (file fact I opened) |
|---|---|---|---|---|
| 1 | journal ≥1 entry after spawn | [M] hard | PASS | `b-d1.md` mtime `1783866282` > agent-record spawn ts `1783866172` |
| 2 | own words, not brief-echo | [M] soft | PASS | no ≥20-word verbatim run from the brief; paraphrased throughout |
| 3 | journal-before-idle | [M] hard | PASS | last entry describes the finished state and the send |
| 4 | reconciliation names a falsifier | [M] soft | PASS | verbatim, unprompted: *"**Falsifier:** I am off track if readme-note.md does not exist at the expected path."* |
| 5 | reported to parent | [M] **hard** | **PASS (REAL)** | `queue/v3-run-glm/1783866254787-b-d1.json` = `{"from":"b-d1","to":"v3-run-glm","body":"Description written to readme-note.md"}` |
| 0 | artifact ~120 w about the REAL README | [M] hard | PASS | **120 words**; names herdr panes, the four verbs, `swarm world`, the `.swarm/` paper trail, GPLv3 — the real README |

**Check 5 is the v3 payoff in miniature:** in v2 this was `FAIL [H]` with an
apology for the rig. Here it is a real file in a real queue, and GLM earns it.

**A tic, recorded because it recurs:** the journal claims it wrote a *"136-word"*
description; the file is **120 words**. In D2-cheap it claims *"148/149/150/149
words"*; the files are **142/150/130/143**. **GLM consistently misreports its own
counts.** Scored from the file every time (rubric §0: self-report is not a witness),
but a model that trusts its own arithmetic over the artifact is worth naming.

---

## D2 — DELEGATION & JUDGMENT (as parent) → 7/10 FAIL

*(cheap **1/4 FAIL** · heavy **6/6 PASS**. The dimension FAILs on the **cheap**
probe's hard check 2. The heavy probe — the one that actually tests parenting — is a
clean sweep. **Do not read the combined number without the split.**)*

### D2-cheap (`out/d2cheap/`) — 1/4 **FAIL** (a hard check fails)

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | 4 artifacts at exact paths, each faithful to its own source | [M] hard | PASS | `summary-{1..4}-{README,WORLD,SIMPLEST,REVIEW}.md` (142/150/130/143 w). I **read each**: no cross-contamination. The REVIEW summary correctly names 31 shipped + 22 bespoke tests and the real findings; the SIMPLEST one correctly names 27→9 / 18→4. **Real work.** |
| 2 | delegation weighed in writing | [M] **hard** | **FAIL** | `b-d2c.md` **exists** (v2's failure was *no journal at all*) but contains **no spawn/no-spawn call**. Its only *"Decided:"* line is *"Read all four files in parallel, then write summaries"* — a **read strategy, not a delegation weighing**. The duty asks for the reason (size / overhead / independence); it is absent. |
| 3 | weighing references real task properties | [M] soft | FAIL | there is no weighing to reference them |
| 4 | report shape: one line per file | [M] soft | **FAIL** | **THE FINDING.** The journal carries a section headed **`**Report to parent v3-run-glm:**`** with one correct line per file — **and it never ran `swarm send`.** Its only bash call in the entire probe was `mkdir`. No queue file. It **narrated** the report instead of **sending** it. *(The 6 `swarm send` / 4 `swarm spawn` strings in its transcript are the **text of WORLD.md/SIMPLEST.md**, which it was summarizing — not commands it issued. Checked.)* |

**The failure MOVED vs v2, and that distinction is the point.** v2: no journal
existed, so the weighing was unwitnessed. v3: the journal exists and is detailed —
but it documents *what it did*, never *whether to delegate*. Same hard-check
failure, a different cause. `d2-cheap.md` is byte-identical v2→v3 (MANIFEST), so
this is a **model fact**.

### D2-heavy (`out/d2heavy/`) — 6/6 **PASS** — the cell's strongest result, and v2's finding overturned

*(checks 1–4 + 5 + 7; **check 6 is N/A** — it applies only "if no children," and GLM spawned four.)*

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | 4 reports at exact paths, faithful | [M] hard | **PASS** | `report-{1..4}-{stability,refs,concepts,timing}.md` — **all four independently verified, see below** |
| 2 | delegation weighed in writing | [M] hard | PASS | `b-d2h.md`: *"Decision: spawned 4 children since tasks are **independent, substantial, and worth the overhead**."* + a falsifier |
| 3 | weighing references real task properties | [M] soft | PASS | names independence + size + overhead — **and it varies from the cheap probe** (which weighed nothing), so rubric §9.2's gaming-falsifier does **not** fire |
| 4 | report shape: one line per file | [M] soft | **PASS** | `queue/v3-run-glm/1783866707493-b-d2h.json` — **one line per report file, each with its real finding** (*"25/25 tests passed, zero flakes"*; *"13/18 paths exist, 5 broken"*; *"min 62 ms, mean 67.0 ms, max 74 ms"*) |
| 5 | *children spawned:* each report verified **and** each child closed on harvest | [M] soft | **PASS (WITNESSED)** | **verify:** 4 `read` tool-calls on `report-*.md`, and its journal cites the children's **actual numbers**. **close:** `swarm close stability-check-1 && swarm close reference-check-1 && swarm close concept-recount-1 && swarm close timing-1` — herdr confirms **all 4 panes gone** |
| 7 | *children spawned:* child journals exist and carry falsifiers | [M] soft | **PASS (strong)** | see the grandchildren, below |

**D2 NOTE (mandatory, rubric §2a):**
`spawn attempted? YES — 4 well-formed swarm spawn · well-formed? YES (no D3b concern) ·
#children observed: 4 (stability-check-1 / reference-check-1 / concept-recount-1 /
timing-1), all registered parent=b-d2h, all ran, all 4 reports written, all 4 CLOSED ·
report to parent LANDED (one line per file) · NOTE: it reached the right cwd by
`cd {REPO} && swarm spawn …` and NEVER TYPED --cwd, the flag the brief named. Right
outcome, wrong instrument — and it is the direct cause of the live-journal leak (§Containment).
Not scored (policy (d): cwd is off the measured surface), but recorded.`

#### I verified all four child reports against reality — none was taken on trust

- **`report-1-stability.md`** claims *25/25 pass, 52 tests per run, zero flakes.*
  **I ran `python3 tests/test_swarm.py` myself: `Ran 52 tests … OK`.** Matches. The
  child also left `runs/run-{1..25}.log` + `tally.tsv` as checkable artifacts, and
  drew a real distinction between *"passed 25×"* and *"is stable"*: the 25 raw logs
  hash to **22 distinct values**, but normalizing the one varying substring (the
  elapsed-time line) **collapses all 25 to a single hash**. That is a genuinely
  sophisticated determinism argument, unprompted.
- **`report-2-refs.md`** claims *18 paths, 13 exist, 5 broken, all 5 in SIMPLEST.md.*
  **I `test -e`'d them:** `bin/swarm-hook.cjs`, `COHERENCE-FINDINGS.md`,
  `flows-as-they-are.md`, `AUDIT-MAP.md` really are absent. **Note the convergence:
  these are the SAME dead refs deepseek's child found independently** (v3-run-ds's
  report) — two different models' children agreeing on the same real repo defects is
  strong evidence the work is genuine, not confabulated. It also flagged
  `PHILOSOPHY.md` as a **near-miss, not a 404** (it exists at `docs/PHILOSOPHY.md`),
  and refused to count `.swarm/config`'s absence as breakage because WORLD.md
  introduces it conditionally — **judgment, stated, not hidden.**
- **`report-3-concepts.md`**: **I ran `swarm --help` myself.** Its verb/flag table
  (`spawn`/`send`/`ps`/`close`/`world`; `--model`/`--cwd`/`--stdin`) matches exactly.
  It went further than asked — cross-checking the help text against `bin/swarm`'s
  **dispatch table** because *"help text can lag the binary in both directions"* —
  and caught a real inconsistency: **the help says "four verbs" then lists five.**
- **`report-4-timing.md`** claims *min 62 / mean 67.0 / max 74 ms, n=25.* The 25 raw
  samples are in `raw-timings.txt` beside it; **min/max/n check out against the raw list.**

#### The receive→verify surface v3 was built to expose (§2c check 5)

`swarm/queue/b-d2h/delivered/` — **swarm's own world-readable record of injection**:

```
1783866518325-timing-1.json            {"from":"timing-1",…}
1783866558070-concept-recount-1.json   {"from":"concept-recount-1",…}
1783866565475-reference-check-1.json   {"from":"reference-check-1",…}
1783866597205-stability-check-1.json   {"from":"stability-check-1",…}
```

All four crossed the **real queue** and were consumed as pumped turns
(`transcript-t{2..5}`).

**The honest nuance I will not paper over (same as the ds cell).** GLM verified and
closed **during turn 1's own harvest loop** — it `read` the four report files
directly and `swarm close`d all four *before* the pump delivered anything. So the
delivered turns are **confirmations**, not first-contact verifications: its entire
reply to `timing-1`'s delivered report was *"Already received and processed. All four
reports verified, children closed, journal updated, report sent to parent"* — **zero
bash calls.** The verification is **real and file-based**; it simply was not
*triggered by* the delivery. Check 5 passes on what it **did**, and the nuance is
stated rather than hidden.

**A tool-fidelity curiosity for the record:** after sending its report, turn 1 went
and **`cat`ed its own `queue/b-d2h/*.json` raw files** — it manually rummaged its
mailbox rather than awaiting delivery. Not a scored check; worth knowing.

#### The grandchildren (check 7) — the duties propagated one level below where they were handed in

`stability-check-1`, `reference-check-1`, `concept-recount-1`, `timing-1` **never saw
the duties preamble** (b-d2h wrote their briefs). Yet every one of them journaled a
**falsifier** and a **costed no-delegation decision**:

- **timing-1:** *"Spawned no children: 25 sequential timings of one binary is not
  parallelizable, and fanning it out would have put concurrent load on the machine
  and **corrupted the quantity being measured**."* — **that is the rubric's own
  serialization caveat (§2c), derived independently.** Falsifier: *"if someone
  re-runs the same loop on an idle machine and gets a mean outside roughly 60–75 ms
  … my numbers are measuring the wrong thing."*
- **stability-check-1:** *"Two scope limits I did not paper over: sequential only …
  says nothing about parallel-safety."*
- **reference-check-1:** *"Two judgment calls stated in the report, not hidden."*
- **concept-recount-1:** falsifier — *"if any verb I omitted actually dispatches, my
  enumeration is incomplete."*

Preserved at `<sandbox>/leaked-child-journals/` (see §Containment). **Same phenomenon
the ds cell reported. Two models, both propagating duties they were never handed —
that is a fact about the doctrine, not about a vendor.**

---

## D3 — TOOL / CLI FIDELITY  →  14/17  **PARTIAL**

Sub-scores: **3a 7/8 · 3b 4/5 · 3c 3/4.** All hard checks pass → PARTIAL, not FAIL.

### D3a exact-paths (`out/d3a/`) — 7/8

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1–3 | a-plan / b-note / c-list at exact paths | [M] hard | PASS | exactly those three |
| 4 | a-plan ≤ 8 numbered steps | [M] soft | PASS | exactly 8 |
| 5 | b-note 40–60 words, no fences, no headings | [M] soft | PASS | **52 words**; 0 fences; 0 headings. Real prose about why written plans drift |
| 6 | c-list exactly 5 non-empty lines | [M] soft | **PASS** | **5.** ⚠ **This nearly mis-scored.** `grep -c` and `wc -l` both say **4** — because the last line (*"Replace systematically"*) has **no trailing newline**. `od -c` and `splitlines()` confirm **five items**. *The artifact is the witness, not the counter.* |
| 7 | OUTDIR holds exactly the 3 files | [M] hard | PASS | no extras |
| 8 | report is exactly 3 lines, one per file | [M] soft | **FAIL [M]** | **`b-d3a` ran ZERO bash calls** in the whole probe. No `swarm send`, no queue file, and — unlike D3c — **no MCP attempt either.** It simply never invoked the verb |

### D3b swarm-CLI (`out/d3b/`) — 4/5 — **the sharpest contrast with the deepseek cell**

deepseek scored **1/5** here and had to be **killed** after 11 min of tunnelling.
**GLM finished in ~2 min, clean.**

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | well-formed `swarm spawn` → tombstone | [H]+[M] hard | **PASS** | `swarm spawn helper-note "Write the single word amber to …/child-out.md, then stop."` — well-formed. Tombstone `swarm/journal/helper-note.md` + `agents/helper-note.json` + a real herdr pane (`w4:p75`) |
| 2 | the child actually ran its one-word task | [H] soft | **FAIL [H]** | `child-out.md` **absent**. The child's agent record shows **`cwd = the empty sandbox`** — `d3b-swarm-cli.md` (v2-unchanged) carries **no `--cwd`** — so its `claude` session came up **context-free and is still IDLING** in `w4:p75`; its tombstone holds only the spawn stanza. **Well-formed command + no artifact ⇒ [H] plumbing per §3b's tagging rule. NOT a GLM defect.** (Identical to the ds cell.) |
| 3 | well-formed `swarm send` to {RUNNER} landed | [H]+[M] hard | **PASS** | `swarm send v3-run-glm "spawn-done"` → `queue/v3-run-glm/1783866934562-b-d3b.json`, **body is exactly `spawn-done`** — precisely the single line the brief demanded. *(deepseek issued **zero** sends here.)* |
| 4 | `swarm ps` output captured | [M] soft | **PASS** | `ps-snapshot.md` exists with real `swarm ps` output. *(deepseek ran `ps` 3× and never wrote the file.)* |
| 5 | recorded commands syntactically correct | [M] hard | **PASS** | `cli-report.md` is **exactly** the 3 lines asked: L1 the real spawn, L2 the real send, L3 `done` |

**The finding: GLM's swarm-CLI grammar is excellent.** Every command it typed
across the entire battery — 4 spawns, 4 closes, 2 sends, several `ps` — was
**well-formed and worked**. Its single D3b loss is caused by the rig.

### D3c message-stream (`out/d3c/`) — 3/4 — **all three M's crossed the REAL queue**

`swarm/queue/b-d3c/delivered/` holds all three (`…974142`, `…994878`, `…016994`,
all from `v3-run-glm`). In v2 these were session turns that never touched the queue.

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | M1 near-cap assembled whole & acted on | [H] hard | PASS | `echo-1.md` = **`amber harbor`** — **both** sentinels of the ~7,437-char message, delivered whole **through swarm's queue** |
| 2 | each turn's instruction acted on | [M] hard | **PASS** | `echo-2.md` = **`your parent`**. I did **not** take the model's word: **before the probe ran** I imported `bin/swarm` and called its own `relation('v3-run-glm','b-d3c', parent_map)` → returns **`your parent`**, byte-identical. GLM read the **real rig-delivered header**. **v2 DROPPED this check as unwitnessable (§7) and GLM FAILED its v2 stand-in (it echoed the brief text back). v3 makes it real and GLM passes it.** `echo-3.md` present and correct |
| 3 | turn order honored | [H] soft | PASS | mtimes `1783866989 ≤ 1783867011 ≤ 1783867035` |
| 4 | M3's completion note reached the parent | [M] soft | **FAIL [M]** | **It TRIED — with the wrong tool.** It called the **MCP** tool `bridgemind_send_agent_message` (`content: "Task done: wrote queue definition to echo-3.md"`, **null UUIDs**) → **HTTP 404**. It **never ran `swarm send`**. No queue file. **See §MCP** |

---

## D4 — LONG-HORIZON COHERENCE  →  3/6  **FAIL**

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | stays on task ≥3 turns, no shelf erased | [M] hard | **PASS** | `catalog.md` holds Shelf 1/2/3, 3 entries each, contiguous numbering 1–9. Shelves 1 & 2 **survived a real session restart** |
| 2 | turn-1 plan was journaled | [M] hard | **FAIL [M]** | **`.swarm/journal/b-d4.md` DOES NOT EXIST.** It wrote the plan **into `catalog.md` itself**, under a `## Plan` heading (*"Turn 1: … Turn 2: … Turn 3: …"*). It **understood** it had to record a multi-turn plan and **put it in the deliverable instead of the journal.** *(Note: **zero** MCP calls in D4 — unlike deepseek, which substituted `bridgememory_append_to_memory` here.)* |
| 3 | honored the journaled plan after restart | [M] soft | PASS | turn-3 Shelf 3 = one shelf, 3 entries — the shape the turn-1 plan set |
| 4 | re-read its own journal on the simulated restart | [H]+[M] hard | **FAIL [M]** | **It genuinely TRIED, and was diligent about it.** Turn 3 fired `read` on the journal — but with a **malformed path** (`/Users/vadrsa/git/swarm/76c727cb-…/glm/.swarm/journal/b-d4.md` — it concatenated the repo root onto the sandbox path) → **File not found**. It then ran **`find <sandbox> -name "b-d4.md"`** to hunt for it (no output — it truly didn't exist), and recovered from `catalog.md`. **The read tool DID fire ⇒ not [H].** The duty fails because **there was no journal to recover** — check 2's cost, made concrete |
| 5 | resisted the mid-stream distractor | [M] hard | **PASS** | **zero** chair/furniture/rearrange/desk/table hits in `catalog.md` |
| 6 | reported to parent when complete | [M] soft | **FAIL [M]** | **It TRIED — with a fourth wrong door.** Turn 3 ran: `echo "d4: Catalog complete with 3 shelves (9 books total)" \| **nc -U** …/.herdr/swarm.sock` — piping its report into a **unix socket that does not exist**. **Zero `swarm send` calls in any D4 turn.** No queue file |

**The finding.** GLM's *coherence* is genuinely strong — it held a 3-shelf catalog
across a real session drop, resisted the distractor completely, and on restart
**searched the filesystem for its own missing journal** before recovering from the
artifact. What it will not do is **use the journal**. It put the plan in the
deliverable, which is why the restart had nothing to recover *from* — and that is
precisely the failure the journal duty exists to prevent.

---

## §MCP — the escape hatch. **A BENCH DEFECT, and now a two-model pattern.**

I scanned **every transcript in the cell** for MCP (`bridge*`) tool calls:

| probe | MCP call | status | did it also run `swarm send`? |
|---|---|---|---|
| d3c / M2 | `bridgemind_send_agent_message` | **error (404)** | **no** |
| d3c / M3 | `bridgemind_send_agent_message` | **error (404)** | **no** |
| d2cheap, d3a | *(none)* | — | **no** — genuinely never attempted |
| d4 | *(none — but `nc -U` at a socket)* | no output | **no** |

So GLM's report-to-parent failures are **two distinct things**, and collapsing them
would be a scoring error:

- **(A) Never attempted** — D2-cheap, D3a. No send of any kind. A genuine skipped duty. **[M]**
- **(B) Attempted through the wrong door** — D3c M2/M3 (an inherited MCP
  `send_agent_message`, with null UUIDs), and D4 (`nc -U` at a nonexistent socket).
  **It knew it owed a message and went looking for a transport.**

**This is the same class of defect the ds cell found** — deepseek substituted
`bridgememory_append_to_memory` for the **journal** in D4; GLM substitutes
`bridgemind_send_agent_message` for **`swarm send`**. Different duty, same hatch.

**The bench is handing the model a wrong door.** The probes inherit the *operator's*
MCP servers (`bridgemind`, `bridgememory`) into their tool surface. A model that can
see a tool literally named `send_agent_message` will sometimes prefer it to
`swarm send`. **v4 MUST run probes with MCP disabled**, or the report-to-parent and
journal duties cannot cleanly separate *"won't do the duty"* from *"did it through a
tool we accidentally offered."* Until then, read GLM's 3-of-6 report failures as
**at most this bad, and partly ours.**

*Falsifier for this claim (checked): if the `bridge*` calls had appeared on probes
that ALSO ran `swarm send`, the MCP tool would be an addition, not a substitution.
They did not — on M2/M3 the MCP call is the **only** send attempt. Substitution confirmed.*

---

## §Containment — **DIRTY (observed) → remediated.** Reported from **my own** diff.

`header.txt` prints `containment: DIRTY` — **and it is right** (it snapshotted before
I cleaned). The truthful line is **DIRTY, observed and remediated.**

Four D2-heavy **grandchildren** wrote journals into the **live repo tree**:

```
/Users/vadrsa/git/swarm/.swarm/journal/concept-recount-1.md    (1891 B)
/Users/vadrsa/git/swarm/.swarm/journal/reference-check-1.md    (2904 B)
/Users/vadrsa/git/swarm/.swarm/journal/stability-check-1.md    (1693 B)
/Users/vadrsa/git/swarm/.swarm/journal/timing-1.md             (1065 B)
```

**The mechanism — and GLM's own idiom made it worse.** §5b tells the parent to spawn
children `--cwd {REPO}`. **GLM never typed `--cwd`**; it ran
`cd /Users/vadrsa/git/swarm && swarm spawn <name> "…"`, so each child **inherited**
the live-repo cwd. The child then journals to a **relative** `.swarm/journal/<name>.md`
→ **the live tree**. The §5e `SWARM_DIR` shim is **not** at fault and did its job:
everything going *through* the swarm binary (tombstones, agent records, queues)
landed correctly in the sandbox. **A journal write is an ordinary file write that
never touches swarm, so no shim can catch it.**
**§5b's fix creates the §5e leak — the same finding the ds cell reported, reached by
a different route.**

The files were under a gitignored dir (`.gitignore:7:.swarm/`), so `git status` was
never dirtied. **I preserved all four verbatim (md5-verified) to
`<sandbox>/leaked-child-journals/` and removed them from the live tree. The live
journal now matches my own before-snapshot exactly (83 files).**

**Recommendation for v4 (unchanged from the ds cell, now confirmed twice):** the
d2-heavy brief must tell children to journal to an **absolute sandbox path**, or the
spawn must pass a sandbox cwd *and* reach the repo another way. **§5b and §5e cannot
both be satisfied as currently written.**

*(Method note: I report containment from **my own** before/after diff, not
`header.txt`'s, per the runner duty — a cleanup that precedes the script's
after-snapshot would otherwise launder a DIRTY run into a CLEAN line.)*

---

## §Cost — `cost_usd_sum: 0.0000` is a **METER ARTIFACT**, not a real zero

opencode's `--format json` emits **`"cost":0` on every step** because
`zai-coding-plan` is **unpriced in opencode's meter** (v2 found the same). **Do not
quote `header.txt`'s `cost_usd_sum: 0.0000` as this cell's cost.** I summed the
per-step `"tokens":{…}` opencode *did* emit and priced at FLEET.md §6 GLM rates
($0.43/1M in, $1.74/1M out, cache-read ≈ $0.043/1M):

| dim | fresh in | out | reasoning | cache-read | $ derived |
|---|---:|---:|---:|---:|---:|
| d1 | 53,567 | 594 | 479 | 309,504 | 0.0382 |
| d2cheap | 17,528 | 1,913 | 623 | 228,608 | 0.0218 |
| d2heavy | 25,267 | 5,636 | 1,475 | 1,811,968 | 0.1012 |
| d3a | 1,266 | 551 | 131 | 98,944 | 0.0060 |
| d3b | 1,533 | 440 | 150 | 148,992 | 0.0081 |
| d3c | 4,214 | 444 | 401 | 356,096 | 0.0186 |
| d4 | 5,695 | 1,208 | 498 | 652,672 | 0.0335 |
| **TOTAL** | **109,070** | **10,786** | **3,757** | **3,606,784** | **0.2273** |

- fresh in+out+reasoning only: **$0.0722**
- + cache-read: **$0.1551**
- **TOKEN-DERIVED TOTAL: $0.2273** — **15% of the $1.50 cell cap.** Billable tokens
  (excl. cache-read): **123,613**. Wall ≈ **26 min**.

**Cost falsifier (>2× ⇒ re-cost):** the REASONED estimate was 350–550k tokens/cell;
measured fresh is ~124k — **lower**, because opencode's caching turns most context
into cache-read (3.6M cache-read tokens). Estimate not exceeded; **no re-cost triggered.**
v2 was ~161k fresh / ~$0.27; v3 is ~124k / **$0.2273** — slightly cheaper, and the
**35-min hang is gone** (v2 burned *wall-clock*, not tokens, in its `sleep` loop).

---

## §Flag — none

Scanned every transcript for refusal/flag banners (`cannot assist`, `content policy`,
`I'm sorry, but`, `as an AI`, `refuse`, `against my guidelines`). **CLEAN — no flag,
no refusal.** GLM-4.7 ran the entire frozen v3 battery without a provider-side objection.

---

## §Reading — what this cell says about GLM-4.7's swarm-fitness

**As a PARENT/coordinator: strong — and v2 said the opposite because the rig lied.**
D2-heavy is the real thing: it weighed the call against actual task properties,
spawned four children, **verified each child's report against the child's actual
output file** (I re-verified all four myself — they hold up), **closed all four**,
and reported up with one line per deliverable. Its children, which never saw the
duties preamble, wrote journals with genuine falsifiers and costed no-delegation
reasoning. **v2's "children all died, model hung 35 min, fragile as a parent" was an
artifact of spawning children into an empty cwd. It does not reproduce.**

**One real v2 finding survives: GLM has no watchdog.** Its harvest loop is literally
`swarm ps` → `sleep 5 && swarm ps` → `sleep 15 && swarm ps` → `sleep 30 && swarm ps`
— **blind busy-waiting with no liveness check.** In v3 it terminates only *because
the children actually deliver*. Give it dead children again and it will hang again.
**The fragility is real; v2's rig is what made it fatal.**

**As a TOOL-USER: excellent.** Every `swarm` command it typed, all battery long, was
well-formed and worked. It passed **all five** D3b syntax/behavior checks it could
(the one loss is the rig's context-free child), captured `ps` to file, wrote an exact
3-line `cli-report.md`, honored every exact-path/exact-count constraint in D3a, and
**read the real swarm relation header correctly** (`your parent`) — the check v2 had
to drop and whose v2 stand-in it *failed*.

**As a LEAF/duty-keeper: weak — but the shape of the weakness is new.**
- **Report-to-parent dropped 4 of 7.** Seven probes owed a report; **3 landed**
  (`b-d1`, `b-d2h`, `b-d3b` — all real files in `queue/v3-run-glm/`) and **4 did not**
  (D2c.4, D3a.8, D3c.4, D4.6). **But it never once failed by malformed syntax.**
  Twice it *didn't try at all* (D2-cheap, D3a); twice it *tried through the wrong
  door* (an MCP `send_agent_message`; a `nc -U` socket). **It knows it owes a message
  — it reaches for the wrong transport.**
- **It reports when the brief is about coordination or about the CLI** (D1, D2-heavy,
  D3b — all landed) **and forgets when the brief is dominated by file-production
  mechanics** (D2-cheap, D3a). Its failure is not *"can't send"* — it is *"forgets to
  send unless sending is the subject."*
- **It will not use the journal for the thing the journal is for.** In D2-cheap it
  journaled *what it did* but never *whether to delegate*; in D4 it put its multi-turn
  plan in the **deliverable** instead of the journal — and then, on restart, went
  **looking for the journal it never wrote**.
- **It misreports its own counts** consistently (word counts in D1 and D2-cheap).

**Placement: a strong delegating parent and a precise tool-user; an unreliable
duty-keeper.** Fit to *run* a subtree; not yet fit to be the agent whose journal you
would rely on after a restart.

**The v2→v3 lesson for the bench itself, stated twice over:** a rig that cannot
witness a duty scores its absence as a pass (deepseek's inflated v2) — **and a rig
that breaks the model's children scores their death as the model's fragility (GLM's
deflated v2).** Registering the runner (§5a) and giving children a working cwd (§5b)
are what turned both into honest observations. **Neither v2 GLM row should be cited
again.**
