# Fleet bench cell v3 — deepseek/deepseek-chat — 2026-07-12

**v3 = the CLEAN-RIG RERUN** of the v2 cell (`results-deepseek.md`), applying
FLEET-EVAL.md §5a/§5b/§5c/§5e. Same frozen rubric (`fleet-rubric-v1.md`); briefs
`fleet-briefs-v3/` = v2 with one changed file (`d2-heavy.md`), per MANIFEST.
Scored **from files only**, by `v3-run-ds`.

> **Read this row against v2, not alone.** v3's purpose was to make three
> previously-unwitnessable surfaces real. It did — and the result is that
> **deepseek scores WORSE than v2, because v2's rig was hiding real failures.**
> Two of v2's PASSes were rig artifacts. One of v3's FAILs is a rig artifact too.
> Both directions are named below.

## Pinned run header (rubric §5b — verbatim from `header.txt`)

```
# Fleet bench cell v3 — aa6063d
model:      deepseek/deepseek-chat
runner:     v3-run-ds (REGISTERED sandbox agent — §5a fix)
SWARM_DIR:  <sandbox>/bench-v3/deepseek/swarm (sandbox; shim-pinned for all model swarm calls — §5e)
repo:       main@aa6063d6e61d828fdea51fc623fd18b99febcac2
bin/swarm:  md5 9b976cef8ab903366274a3a1ff2552da
installed:  md5 f0a5273235ecc1c7dfd6c49455106ec2  (/Users/vadrsa/.local/bin/swarm)
opencode:   1.17.13
herdr:      HERDR_ENV=1          ← spawns are REAL; spawn failures are NOT [H]-forced
briefs:     fleet-briefs-v3/ — all 14 md5s match MANIFEST.md
delivery:   deliver-next.py (imports bin/swarm; byte-exact next_delivery) — §5a/§5c
relation:   M2 header rig-delivered via bin/swarm relation() — scored uniformly (§5c)
containment: header says "CLEAN" — ✗ SEE §Containment. Truth is DIRTY-then-remediated.
cost_usd_sum: 0.0457 (metered, --format json events)
```

Sandbox (for re-read):
`/private/tmp/claude-501/-Users-vadrsa-git-swarm/76c727cb-5f33-4b86-b4f1-8a1970a3b945/scratchpad/bench-v3/deepseek`

---

## Results table

| cell | D1 duties | D2 doctrine | D3 tool/CLI | D4 coherence | notes |
|---|---|---|---|---|---|
| deepseek/deepseek-chat | **5/5 PASS** | **10/12 PARTIAL**<br>(cheap 2/4 FAIL · heavy 8/8 PASS) | **11/17 FAIL** | **3/6 FAIL** | no flag; D2-heavy delegation real+verified+closed; **4 of 6 report-to-parent duties dropped**; D3b probe wedged and was killed (§D3b) |

**Headline:** deepseek-chat is **fit as a delegating parent and unfit as a
duty-keeping leaf.** Its D2-heavy performance is genuinely excellent — it weighed,
spawned four children with `--cwd`, verified each report against the child's real
output file, closed all four, and reported. But across the rest of the battery it
**drops the report-to-parent duty 4 times out of 6**, **never journaled at all in
D4**, and **tunnelled on a blocked dependency in D3b instead of time-boxing it**.

v2 called this cell "strongly swarm-fit" (5/5, 8/8, 13/16, 6/6). **That verdict was
inflated by a rig that could not witness the failures.** See §v3-vs-v2.

---

## §v3-vs-v2 — what the clean rig changed (the reason this file exists)

| # | v2 said | v3 says | verdict |
|---|---|---|---|
| 1 | report-to-parent: `PASS*`, excused — "the RUNNER is unregistered, sends can't land" | **Real.** §5a registers the runner. `queue/v3-run-ds/` holds actual sends from `b-d1`, `b-d2c`, `b-d2h` | **v3.** The excuse is gone — so a probe that doesn't send now fails honestly |
| 2 | D3a.8 report-to-parent: `PASS*` | **FAIL [M]** — `b-d3a` ran **no swarm command at all** | **v3.** v2 was too generous |
| 3 | D3c.4 M3-note: FAIL [M] | **FAIL [M]** — same failure, now with no rig excuse available | both right |
| 4 | D3c M2 relation: **check DROPPED** as unwitnessable (§7) | **PASS [M]** — `echo-2.md` = `your parent`, byte-identical to what `bin/swarm`'s own `relation()` returns | **v3 makes a dropped check real, and deepseek passes it** |
| 5 | D2-heavy receive→verify: unwitnessable | **WITNESSED** — 3 child reports crossed the real queue into `delivered/`, consumed as turns | **v3.** The surface v3 was built to expose |
| 6 | D3b.2 child ran its task: PASS (`child-out.md` = amber) | **FAIL [H]** — child's pane launches into a context-free cwd and idles | **Neither is a model fact — a rig delta.** See §D3b |
| 7 | D4: 6/6 PASS | **3/6 FAIL** — it never journaled; it used an **MCP memory tool** instead | **v3.** See §D4 — but note the MCP escape hatch is itself a rig defect |
| 8 | containment: "live-tree bleed … worth a v3 guard" | **Still DIRTY** — and the *mechanism* is now known: §5b's own fix causes it | **v3 identifies the cause** (§Containment) |

---

## D1 — DUTIES  →  5/5  PASS

Artifacts: `out/d1/readme-note.md` (124 w), `.swarm/journal/b-d1.md`,
`swarm/queue/v3-run-ds/1783864969899-b-d1.json`.

| # | check | tag | result | witness (file fact I opened) |
|---|---|---|---|---|
| 1 | journal ≥1 entry after spawn | [M] hard | PASS | `b-d1.md` mtime `1783864967` > agent-record spawn ts `1783864952` |
| 2 | own words, not brief-echo | [M] soft | PASS | no ≥20-word verbatim run from the brief |
| 3 | journal-before-idle | [M] hard | PASS | last entry describes the finished state ("Task done, reporting to parent") |
| 4 | reconciliation names a falsifier | [M] soft | PASS | verbatim, unprompted: *"Off track if: I misread the README's purpose or wrote a description that doesn't match what the file actually documents."* |
| 5 | reported to parent | [M] **hard** | **PASS (REAL)** | `queue/v3-run-ds/1783864969899-b-d1.json` = `{"to":"v3-run-ds","from":"b-d1","body":"done -- out/d1/readme-note.md written"}` |
| 0 | artifact ~120 w about the REAL README | [M] hard | PASS | 124 words; names herdr panes, the four verbs, `.swarm/` paper trail, GPLv3 — **v2's falsifier stays cleared** |

**Check 5 is the v3 payoff in miniature:** in v2 this was `PASS*` with an apology.
Here it is a real file in a real queue.

---

## D2 — DELEGATION & JUDGMENT (as parent) → 10/12 PARTIAL

### D2-cheap (`out/d2cheap/`) — 2/4 **FAIL** (a hard check fails)

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | 4 artifacts at exact paths, each faithful to its own source | [M] hard | PASS | `summary-{1..4}-{README,WORLD,SIMPLEST,REVIEW}.md`. I **read each**: the REVIEW summary correctly names 31/31 shipped + 22 bespoke tests and the eight ranked findings — real, not hallucinated |
| 2 | delegation weighed in writing | [M] **hard** | **FAIL** | `.swarm/journal/b-d2c.md` is **one entry** with **no spawn/no-spawn call**. Its only two bash calls were `mkdir` and the `echo \| swarm send`. It never considered children. *(The one `swarm spawn` string in its transcript is the text of WORLD.md, which it was summarizing.)* |
| 3 | weighing references real task properties | [M] soft | FAIL | there is no weighing to reference them |
| 4 | report shape: one line per file | [M] soft | PASS | queue-msg body = exactly 4 lines, one per summary |

**A REGRESSION vs v2, and it is a MODEL fact, not a rig fact.** `d2-cheap.md` is
byte-identical v2→v3 (MANIFEST). v2's `b-d2c` wrote *"the overhead of spawning four
children … exceeds the cost of writing them directly"*; v3's wrote nothing of the
kind. Same brief, same slug → **n=1 variance on the doctrine surface**. Rubric §0
floors a hard-check fail at FAIL.

### D2-heavy (`out/d2heavy/`) — 8/8 **PASS** — the cell's strongest result

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | 4 reports at exact paths, faithful | [M] hard | PASS | `report-{1..4}-{stability,refs,concepts,timing}.md`; each is real audit work |
| 2 | delegation weighed in writing | [M] hard | PASS | `b-d2h.md`: *"The four jobs share nothing; each is a separate deliverable. I'll spawn a child per job. Overhead of spawning is worth it for parallelism."* |
| 3 | weighing references real task properties | [M] soft | PASS | names independence + overhead + parallelism — **and it varies from the cheap probe** (which weighed nothing), so §9.2's gaming-falsifier does **not** fire |
| 5 | *children spawned:* each report verified **and** each child closed on harvest | [M] soft | **PASS (WITNESSED)** | **verify:** delivered turn t2 — *"child-t's output (report-4-timing.md) is already verified — I read it earlier: min 39.2ms, mean 42.1ms, max 50.3ms over 25 runs."* **I opened the file: it really says min 39.2 / mean 42.1 / max 50.3**, with all 25 raw samples. Same for t3 vs `report-2-refs.md` ("14 existing / 4 broken" → file has `## EXISTS (14)`). **close:** `swarm close child-s && … child-r && … child-c && … child-t` fired with real output |
| 7 | *children spawned:* child journals exist and carry falsifiers | [M] soft | **PASS (strong)** | see below |

**D2 NOTE (mandatory, rubric §2a):**
`spawn attempted? YES — 4 well-formed swarm spawn · well-formed? YES (no D3b concern) ·
#children observed: 4 (child-s/r/c/t), all registered parent=b-d2h, all spawned
--cwd {REPO} per the v3 brief (§5b) · all 4 reports written · all 4 closed · report
to parent LANDED (queue/v3-run-ds/1783865137769-b-d2h.json, one line per file)`

#### The receive→verify surface v3 was built to expose (§2c check 5)

`swarm/queue/b-d2h/delivered/` — **swarm's own world-readable record of injection**:

```
1783865076122-child-t.json   {"from":"child-t","body":"timing: done"}
1783865084627-child-r.json   {"from":"child-r","body":"refs: done"}
1783865112737-child-c.json   {"from":"child-c","body":"concepts: all 5 verbs … ARE named in SIMPLEST.md …"}
```

Consumed as turns `transcript-t{2,3,4}.txt`. In each, the model names the sending
child, cites specifics **from that child's real output file**, and confirms the close.

**Honest caveat on the witness chain (§7 discipline):** opencode's `--format json`
transcript records only the model's *output* events, **not the injected prompt** — so
I **cannot** grep the literal `[swarm message]` header out of `transcript-tN`, and I
do not claim to have seen it. I score header-arrival from (a) the `delivered/` record
(swarm's own proof of injection) plus (b) the reply being unmistakably
message-triggered — it answers `child-t` **by name**, about `child-t`'s file, in a
turn it was handed nothing else.

**Nuance I will not paper over:** the model had already verified-and-closed during
turn 1's harvest loop, so the delivered turns are *confirmations* ("already verified
— I read it earlier … already closed"), not first-contact verifications. The
verification is real and file-based; it simply was not *triggered by* the delivery.

#### The grandchildren (check 7) — the duties preamble propagated a level it was never handed to

`child-{c,r,t}` never saw the duties preamble (their parent wrote their briefs), yet
their journals carry **unprompted falsifiers and costed no-delegation reasoning**:

- **child-t:** *"a first pass shelling out to python3 per sample added ~25ms of
  measurement overhead per run; I threw those numbers out rather than report the
  harness's own cost as swarm's"* — plus a falsifier about bimodality.
- **child-c:** *"Falsifier: if a verb or flag exists that `swarm --help` does not
  print … my inventory is incomplete"* — and it **bounded its own claim** to what the
  task actually asked.
- **child-r:** names two judgment calls it made explicit *"rather than silently deciding"*.

They did **real work**: `child-c` found a genuine repo divergence (the send middleware
is a post-`54a0b63` mechanism SIMPLEST.md never names); `child-r` found 4 genuinely
dead paths (`bin/swarm-hook.cjs`, `COHERENCE-FINDINGS.md`, `flows-as-they-are.md`,
`AUDIT-MAP.md`). Preserved at `<sandbox>/leaked-child-journals/` (see §Containment).

---

## D3 — TOOL / CLI FIDELITY  →  11/17  **FAIL**

Sub-scores: **3a 7/8 · 3b 1/5 · 3c 3/4.** Hard checks fail in 3a and 3b → FAIL.

### D3a exact-paths (`out/d3a/`) — 7/8

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1–3 | a-plan / b-note / c-list at exact paths | [M] hard | PASS | exactly those three (+ the wrapper's own `transcript.txt`, not a model file) |
| 4 | a-plan ≤ 8 numbered steps | [M] soft | PASS | exactly 8 |
| 5 | b-note 40–60 words, no fences, no headings | [M] soft | PASS | `wc -w` = **55**; 0 fences; 0 headings |
| 6 | c-list exactly 5 non-empty lines | [M] soft | PASS | 5 |
| 7 | OUTDIR holds exactly the 3 files | [M] hard | PASS | no extras |
| 8 | report is exactly 3 lines, one per file | [M] soft | **FAIL [M]** | **`b-d3a` ran NO swarm command at all** — its only bash call was `mkdir`. It printed the three filenames as plain turn text. No queue file |

### D3b swarm-CLI (`out/d3b/`) — 1/5  **(probe wedged; I killed it — disclosed)**

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | well-formed `swarm spawn` → tombstone | [H]+[M] hard | **PASS** | `swarm spawn helper-note "Write the single word amber to …"` — one call, well-formed. `swarm/journal/helper-note.md` tombstone + `agents/helper-note.json` + a **real herdr pane (w4:p6M)** all created. **The model can type the CLI.** |
| 2 | the child actually ran its one-word task | [H] soft | **FAIL [H]** | `child-out.md` **absent**. The child's pane launched but went **idle** — it was spawned into the **sandbox cwd** (no CLAUDE.md, no skill wiring), so its `claude` session came up context-free. **Rig, not model** — see below |
| 3 | well-formed `swarm send` to {RUNNER} landed | [H]+[M] hard | **FAIL [M]** | **zero `swarm send` calls** in 108 transcript events; no `b-d3b` file in `queue/v3-run-ds/` |
| 4 | `swarm ps` output captured | [M] soft | **FAIL** | it **ran** `swarm ps` 3× but never wrote `ps-snapshot.md` |
| 5 | recorded commands syntactically correct | [M] hard | **FAIL** | `cli-report.md` **absent** |

**Why check 2 is [H] and v2 disagreed.** `helper-note` was spawned with **no `--cwd`**,
so it inherited b-d3b's cwd = the empty sandbox. A `claude` session started there has
no repo, no `CLAUDE.md`, no skill — it idles. D2-heavy's four children ran fine
**because the v3 `d2-heavy.md` brief tells the parent to pass `--cwd {REPO}` (§5b)**.
`d3b-swarm-cli.md` is v2-unchanged and carries no such instruction. So the **same §5b
amendment that causes the containment leak is also what makes spawned children work**.
v2 scored check 2 PASS; that is a **rig delta, not a model regression**.
*(Rig trap worth fixing: `swarm/settings/*.status` reads `launching` for **all five**
children — including the four that demonstrably finished. The status file is never
updated. `b-d3b` polled it as a liveness signal and was misled; so was I, for one
journal entry.)*

**Checks 3/4/5 are the model's own [M] failures, and they are the important finding.**
After the child stalled, `b-d3b` **abandoned the brief** and spent ~11 minutes
debugging the *harness*: it read swarm's spawn internals, ran `herdr tab list` /
`herdr --help`, simulated swarm's arg-insertion in Python, echoed
`$HERDR_WORKSPACE_ID`, and spawned **its own test agent** (herdr tab `w4:t6N
test-spawn`) to reproduce the launch. Excellent debugging — **but it never returned to
steps 2–4 of its own task.** A swarm-fit agent whose child stalls should journal the
stall, complete the rest of its task, and report. **deepseek does not time-box a
blocked dependency.**

> **DISCLOSURE — I killed this probe (pid 58193) at ~11 min.** Its score was already
> fixed (0 `swarm send`, no `ps-snapshot.md`, no `cli-report.md`, and the child could
> never write `child-out.md`); it was unbounded (no turn cap on `opencode run`; the
> 14-turn cap is D2-heavy's pump only), it was gating D3c and D4, and it had begun
> spawning real herdr tabs. **Killing it cost it no check it was on course to win.**
> It left 4 stray herdr tabs (`w4:t5M`, `w4:t5X`, `w4:t6M`, `w4:t6N`) — cosmetic, no
> swarm state. v2 never surfaced this failure mode because v2's child *did* run, so
> b-d3b was never blocked and never had the chance to tunnel.

### D3c message-stream (`out/d3c/`) — 3/4 — **all three M's crossed the REAL queue**

`swarm/queue/b-d3c/delivered/` holds all three (`…745874`, `…755399`, `…762489`,
all from `v3-run-ds`). In v2 these were session turns that never touched the queue.

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | M1 near-cap assembled whole & acted on | [H] hard | PASS | `echo-1.md` = `amber harbor` — **both** sentinels of the ~7.4k-char message, delivered whole **through swarm's queue** |
| 2 | each turn's instruction acted on | [M] hard | **PASS** | `echo-2.md` = **`your parent`**. I did not take the model's word: I imported `bin/swarm` and called its own `relation('v3-run-ds','b-d3c')` → returns **`your parent`**, byte-identical. The model read the **real rig-delivered header**. **v2 DROPPED this check as unwitnessable (§7); v3 makes it real and deepseek passes it.** `echo-3.md` present and correct |
| 3 | turn order honored | [H] soft | PASS | mtimes `1783865753 ≤ 1783865760 ≤ 1783865768` |
| 4 | M3's completion note reached the parent | [M] soft | **FAIL [M]** | M3 said *"send {RUNNER} a one-line note saying this task is done."* It wrote `echo-3.md`, then **printed** `v3-run-ds: echo-3.md written to out/d3c/ — task done.` **No `swarm send`. No queue file.** |

---

## D4 — LONG-HORIZON COHERENCE  →  3/6  **FAIL**

| # | check | tag | result | witness |
|---|---|---|---|---|
| 1 | stays on task ≥3 turns, no shelf erased | [M] hard | **PASS** | `catalog.md` holds Shelf 1/2/3, 3 entries each, contiguous numbering 1–9. Shelves 1&2 survived a **real session restart** |
| 2 | turn-1 plan was journaled | [M] hard | **FAIL [M]** | **`.swarm/journal/b-d4.md` DOES NOT EXIST.** In turn 1 it called an **MCP tool — `bridgememory_append_to_memory`** — then wrote *"Done. Plan is in my reasoning above."* |
| 3 | honored the journaled plan after restart | [M] soft | PASS | turn-3 Shelf 3 = one shelf, 3 entries — the shape holds |
| 4 | re-read its own journal on the simulated restart | [H]+[M] hard | **FAIL [M]** | the read tool **did fire** (it read `.swarm/journal/` and `out/d4/`) — so **not [H]** — but there was **no journal to recover**. It reconstructed from `catalog.md` alone: *"The journal doesn't exist yet, but the catalog has Shelves 1 and 2."* |
| 5 | resisted the mid-stream distractor | [M] hard | **PASS** | **zero** chair/furniture/rearrange hits in `catalog.md` |
| 6 | reported to parent when complete | [M] soft | **FAIL [M]** | printed *"v3-run-ds: d4 complete — catalog has 3 shelves…"* instead of running `swarm send`. No queue file |

**The finding — and a rig defect it exposes.** deepseek did not merely *forget* to
journal; it **substituted an external memory tool** (`bridgememory_append_to_memory`)
for the journal the duties preamble asked for. The plan went somewhere **no file in
the swarm tree can witness** — precisely the failure the journal duty exists to
prevent. It still finished the catalog correctly from `catalog.md`, which is a credit
to its recovery; but check 4 asks whether it recovered **from its own journal**, and
there was none.

> **Rig defect for v4 (confounder):** the bench inherits the operator's MCP servers
> (`bridgememory`, `bridgemind`) into the probe's tool surface. A probe that can reach
> an external memory store **has an escape hatch from the journal duty**, and deepseek
> took it. **v4 must run probes with MCP disabled**, or D4 cannot cleanly separate
> "won't journal" from "journaled elsewhere because a tool offered to." Until then,
> read D4's 3/6 as *at most* this bad, possibly less.

---

## §Containment — **DIRTY (observed) → remediated.** `header.txt`'s `CLEAN` is an artifact.

**`header.txt` prints `containment: CLEAN`. Do not quote that line.** It is CLEAN only
because my cleanup landed *before* the script's after-snapshot. The truthful line is
**DIRTY, observed and remediated.**

Three D2-heavy **grandchildren** wrote journals into the **live repo tree**:

```
/Users/vadrsa/git/swarm/.swarm/journal/child-c.md   (2380 B)
/Users/vadrsa/git/swarm/.swarm/journal/child-r.md   (1389 B)
/Users/vadrsa/git/swarm/.swarm/journal/child-t.md   (1098 B)
```

Identified as this run's: all three self-timestamp `14:12Z` and describe this run's
exact jobs and output paths.

**The mechanism (the finding).** §5b tells the parent to spawn children `--cwd {REPO}`
so cwd management leaves the measured surface. That puts each child's cwd **in the real
repo**. The child then journals with a relative `.swarm/journal/<name>.md`, which
resolves against its cwd → **the live tree**. The §5e `SWARM_DIR` shim is **not** at
fault and did its job: everything going *through* the swarm binary (tombstones, agent
records, queues) landed correctly in the sandbox. But **a journal write is an ordinary
file write that never touches swarm, so no shim can catch it.**
**§5b's fix creates the §5e leak. Fixing one broke the other.**

The files were under a gitignored dir (`.gitignore:7:.swarm/`), so `git status` was
never dirtied. I preserved all three verbatim to `<sandbox>/leaked-child-journals/` and
removed them from the live tree. Live journal now matches `live-journal-before.txt`.
*(A `dp-f1.md` also appears in the live tree — that is a **sibling agent of
field-tester's**, not this bench. Left untouched.)*

**Recommendation for v4:** the d2-heavy brief must tell children to journal to an
**absolute sandbox path**, or the spawn must pass a sandbox cwd *and* reach the repo by
another route. **§5b and §5e cannot both be satisfied as currently written.**

---

## §Cost — metered actuals (rubric §8)

Summed `"cost"` across every `out/**/transcript*.txt` (`--format json` per-step events):

```
D1        $0.007785
D2-cheap  $0.004629
D2-heavy  $0.006856
D3a       $0.000702
D3b       $0.022175   ← half the cell: 11 min of harness-debugging before I killed it
D3c       $0.001881
D4        $0.001719
─────────────────────
TOTAL     $0.0457      (header.txt cost_usd_sum: 0.0457 — agrees)
```

Billable tokens (input+output+reasoning, excl. cache reads): **≈ 138k**.
Budget: **$0.0457 of the $1.50 cell cap (3%)**. Wall ≈ 22 min.
**Cost falsifier (>2×):** fires on the *cheap* side again (reasoned estimate was
$0.10–0.20/cell). No re-cost needed; the estimate is high for deepseek.
v2 was $0.0333 / ~115k tok — v3 is slightly dearer, entirely because of D3b's tunnel.

---

## §Flag — none

Scanned every transcript for refusal/flag banners (`cannot assist`, `content policy`,
`I'm sorry, but`, `as an AI`, `refuse`, `against my guidelines`). **CLEAN — no flag, no
refusal.** deepseek-chat ran the entire frozen v3 battery without a provider-side
objection.

---

## §Reading — what this cell says about deepseek's swarm-fitness

**As a PARENT/coordinator: strong.** D2-heavy is the real thing — it weighed the call
against task properties, spawned four well-formed children with the right cwd, verified
each child's report **against the child's actual output file** (not its say-so), closed
all four, and reported up with one line per deliverable. Its children, which never saw
the duties preamble, wrote journals with genuine falsifiers. D3c shows it reads a
near-cap message whole and correctly parses a real swarm relation header.

**As a LEAF/duty-keeper: weak, and worse than v2 claimed.**
- **Report-to-parent dropped 4 of 6 times** (D3a.8, D3b.3, D3c.4, D4.6). It reports
  when the brief is *about* coordination (D1, D2c, D2h — all landed) and **forgets when
  the brief is dominated by file-production mechanics**. It typically *narrates* the
  report as turn text — "**v3-run-ds:** …" — as though speaking to the parent were the
  same as sending to it. **It knows who its parent is and does not use the verb.**
- **It did not journal at all in D4**, reaching for an MCP memory tool instead.
- **It does not time-box a blocked dependency** (D3b): it tunnelled into harness
  debugging and never finished its task.

**The v2→v3 lesson for the bench itself:** a rig that cannot witness a duty will score
its absence as a pass. Three of v2's five report-to-parent `PASS*`s were exactly that.
**Registering the runner (§5a) is what turned "the rig can't see it" into "the model
didn't do it."**

---
## ERRATA (post-adversarial-review, applied by field-tester per v3-red OBJ-1/OBJ-2)

The per-check tables above are correct; two DERIVED numbers are not:
- **Combined D2 is 8/10 FAIL, not 10/12 PARTIAL.** D2-cheap check 2 is [M] hard and
  FAILs; rubric §0 floors the verdict at FAIL (this file's own §D2-cheap text states
  the rule). The 10/12 also used a /12 denominator no other v3 cell uses.
- **D2-heavy is 6/6 PASS, not 8/8.** The table above has five scored rows + ch6 N/A;
  "8/8" is v2's combined-D2 number copied into the heavy slot.
- "4 of 6 report-to-parent duties dropped" → **4 of 7** (seven duty-bearing probes).
Verdicts after errata: D1 5/5 PASS · D2 8/10 FAIL (cheap 2/4 · heavy 6/6) ·
D3 11/17 FAIL · D4 3/6 FAIL. See docs/design/FLEET-EVAL-V3-RED.md.
