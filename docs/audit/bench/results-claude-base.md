# Fleet bench run — Claude baseline cell (native-claude, PLUMBING-CAVEATED) — 2026-07-11

> SUPERSEDED by results-v3-claude-base.md (v2-run baseline); kept for the record (the first "is Claude swarm-fit" measurement — 38/38 clean sweep — under a harness where the runner was unregistered, later shown by v3 to hide a real containment distinction).

runner: run-claude-base-2   SWARM_DIR: /private/tmp/claude-501/-Users-vadrsa-git-swarm/990a14af-96fd-4423-892c-3b6a1b204c99/scratchpad/bench-v2/claude-base/swarm  (sandbox — never the live .swarm/)
repo: main@aa6063d (clean)   installed bin/swarm md5: 9b976cef8ab903366274a3a1ff2552da
**harness: claude-native** — `swarm spawn` under sandbox SWARM_DIR, one real
  `claude` session per probe (claude 2.1.207), turns delivered as REAL `swarm send`
  into the probe's pane. **NOT `opencode run`.** (rubric §5a option 2, native fallback.)
models: baseline = **native claude** (claude 2.1.207) — the swarm launcher's default.
briefs: **fleet-briefs-v2/** — unchanged @ MANIFEST.md md5s (v2 = the {REPO}/-absolute
  fix over v1; d1-duties + d2-cheap md5s changed vs v1, all others byte-identical).
scoring: from files only, by run-claude-base-2; panes read only for the D3c/D4
  delivery-order + journal-re-read notes and the one trust-prompt unblock.
accepted at run start: native `claude` (live, no auth error). rejected: n/a (no opencode/OpenRouter slug used).

---

## ⚠ THE PLUMBING CAVEAT (carried in every row below — this cell's honesty)

This baseline is a **same-BATTERY** Claude anchor, **not** a same-HARNESS one. The
deepseek/GLM cells run through `opencode run`; this cell runs through **native
claude** driven by real `swarm spawn`/`swarm send`. So **a Claude-vs-deepseek/GLM
score gap here confounds MODEL with HARNESS.** The caveat cuts **both ways**:

1. **More-capable harness, not just a different model.** Native claude + real swarm
   spawn *exercises swarm's actual delivery/queue/restore machinery* — tombstones,
   the `deliver` hook injecting queue files as turns, the relation header, the
   SessionStart `restore` re-inject. The opencode cells **structurally cannot touch
   any of that** (rubric §3c, §7): their turns are `--session` continuations, not
   swarm messages. Two rubric checks the opencode rig had to DROP are **witnessable
   and PASS here** (see D3c note). That inability is itself a placement fact for the
   Chinese cells — and its *absence* here inflates this cell relative to a true
   same-pipe comparison.
2. **This answers "is Claude swarm-fit?" cleanly** (yes, on every dimension) but is
   a **weaker comparator** for "is deepseek/GLM as swarm-fit as Claude *through the
   same pipe*." Prefer the same-harness baseline (rubric §5a option 1) once an
   OpenRouter key is added; until then this row is **caveated-not-clean** (rubric
   §9 falsifier 6).

**Spend:** Anthropic pool (the runner's own account — this cell is FREE, not billed
against the deepseek/GLM dollar cap). Estimated ~350–500k tokens across the cell
(9 probe sessions + 1 grandchild + ~6 delivered turns), in line with rubric §8's
350–550k estimate. Native claude does not emit the per-step `--format json`
`tokens`/`cost` stream the opencode rig sums, so this is REASONED, not metered;
falsifier (rubric §8): a metered rerun >2× off re-costs before repeat.

---

## Results table

| cell | D1 duties | D2 doctrine | D3 tool/CLI | D4 coherence | notes |
|---|---|---|---|---|---|
| **claude-native (base)** | **5/5 PASS** | **8/8 PASS** (cheap 4/4 + heavy 4/4; heavy ch5&7 N/A) | **17/17 PASS** (3a 8/8 · 3b 5/5 · 3c 4/4) | **6/6 PASS** | native-harness (confounds model×harness); every probe declined-or-spawned correctly; 0 flags; self-journals leak to live (rig, cleaned) |

**n = 1 per dimension** (rubric §0). Every row is citable **only with the header
above** — at these md5s, this native harness, this baseline choice.

---

## D1 — DUTIES COMPLIANCE — 5/5 PASS  [all [M]]

Probe `b1-duties` (preamble + d1-duties.md, {REPO}/README.md absolute). Artifact
`out/d1/readme-note.md` = 123 words, grounded in the REAL README (names swarm's four
verbs, herdr panes, `.swarm/` state, WORLD.md, GPL-3.0). **v2 fix VALIDATED: the
probe read the real repo README, not an empty-sandbox miss** — this is the check the
runner was told to verify before trusting the battery.

| # | check | verdict | file fact |
|---|---|---|---|
| 1 | journal ≥1 entry after spawn | PASS | live `.swarm/journal/b1-duties.md`, 2 entries, mtime 23:00 > spawn 22:54 (see rig note on the live-journal location) |
| 2 | own words, not brief-echo | PASS | no verbatim ≥20-word run of "about 120 words"/"readme-note.md" in journal |
| 3 | journal-before-idle, last entry finished | PASS | last entry describes the finished state ("Artifact confirmed at out/d1/readme-note.md. Work done; going idle.") |
| 4 | reconcile names a falsifier | PASS | "Falsifier: I am off track if the note misstates what the README documents…" |
| 5 | reported to parent | PASS [H] | message from b1-duties in sandbox `queue/operator/…-b1-duties.json` (see rig note: parent name unroutable in the sandbox tree → operator is its effective parent-mailbox) |

---

## D2 — DELEGATION & JUDGMENT — 8/8 PASS  [all [M]]

### 2b — cheap probe `bv2-d2c` — 4/4 PASS

Four summaries at exact paths, spot-read each faithful to ONLY its source
(README→swarm overview; WORLD→9-concepts/4-verbs contract; SIMPLEST→27→9 clean-slate
design; REVIEW→execution-based PASS review). Words 142/143/145/143 (~150 target).

| # | check | verdict | file fact |
|---|---|---|---|
| 1 | 4 artifacts, each faithful to own source | PASS | `out/d2cheap/summary-{1..4}-<basename>.md` exist; no cross-source contamination on read |
| 2 | delegation weighed in writing | PASS | journal: "Decided NOT to delegate: reading was already done in my context… too small to earn delegation overhead" |
| 3 | weighing references real task properties | PASS | names size, overhead, independence explicitly |
| 4 | report one line per file | PASS | delivered report in `queue/operator/…-bv2-d2c.json`, one line per summary |

**NOTE (mandatory):** spawn attempted? **no** · well-formed? **n/a** · #children **0**.
Correct DECLINE at cheap size (rubric §2 — declining small independent jobs is
VERIFIED-correct), not a D3 failure.

### 2c — heavy probe `bv2-d2h` — 4/4 applicable PASS (ch5, ch7 N/A)

Four real audit jobs, all correct: report-1 test_swarm.py **25/25 PASS**; report-2
7 existing paths + 4 genuinely-broken refs (all in SIMPLEST's "Inputs read in full"
audit list) + CLAUDE.md/PHILOSOPHY.md nuance; report-3 all 5 verbs + 3 flags from
`swarm --help` named in SIMPLEST (word-boundary, not substring); report-4 `swarm
world` ×25 min/mean/max 41.5/45.2/52.0 ms (cold first-run noted).

| # | check | verdict | file fact |
|---|---|---|---|
| 1 | 4 reports faithful | PASS | `out/d2heavy/report-{1..4}-*.md` exist, correct, real work |
| 2 | delegation weighed | PASS | journal: "Overhead of spawning 4 children likely exceeds doing them directly, and I must read every child's output anyway" |
| 3 | weighing references real properties | PASS | names overhead, must-verify-outputs, size, determinism |
| 4 | report one line per file | PASS | `queue/operator/…-bv2-d2h.json`, one line per report |
| 5 | *if children:* verified + closed | N/A | no children spawned |
| 6 | *if no children:* refusal names real cost | PASS | the ch2/ch3 weighing IS a costed refusal |
| 7 | *if children:* child journals + falsifiers | N/A | no children spawned |

**NOTE (mandatory):** spawn attempted? **no** · well-formed? **n/a** · #children **0**.
A correct SOLO decision at this deterministic scale. **Ran alone** (rubric §2c
serialization) — no concurrent probe of MINE; sibling runners' box load is noted as
a caveat on report-4's absolute timing values (rubric does not score the ms, only
that the report carries min/mean/max — it does).

**D2 gaming-caveat check (rubric §2c falsifier):** the weighing DID vary with task
size — cheap said "reading already in context, too small"; heavy said "must read
every child's output anyway, deterministic." Not invariant boilerplate → check 3
stands this run.

---

## D3 — TOOL / CLI FIDELITY — 17/17 PASS  (3a 8/8 · 3b 5/5 · 3c 4/4)

### 3a — exact paths / exact counts `bv2-d3a` — 8/8 PASS

| # | check | verdict | file fact |
|---|---|---|---|
| 1–3 | a-plan.md / b-note.md / c-list.md at exact paths | PASS | `ls out/d3a` = exactly these 3 |
| 4 | a-plan ≤ 8 numbered steps | PASS | 8 numbered lines |
| 5 | b-note 40–60 words, no fences, no headings | PASS | 56 words; 0 ``` ; 0 `^#` |
| 6 | c-list exactly 5 non-empty lines, nothing else | PASS | 5 total lines, 5 non-empty |
| 7 | {OUTDIR} exactly the 3 files | PASS | `ls out/d3a` count = 3 |
| 8 | report exactly 3 lines, one per file | PASS | `queue/operator/…-bv2-d3a.json` body = 3 content lines |

### 3b — swarm-CLI syntax `bv2-d3b` — 5/5 PASS

Spawned grandchild `helper-note`, sent `spawn-done`, ran `swarm ps`, wrote cli-report.

| # | check | verdict | file fact |
|---|---|---|---|
| 1 | well-formed `swarm spawn` fired (tombstone) | PASS [H]+[M] | sandbox `.swarm/journal/helper-note.md` exists |
| 2 | child ran its one-word task | PASS [H] | `out/d3b/child-out.md` == `amber` |
| 3 | well-formed `swarm send` landed | PASS [H]+[M] | `spawn-done` body in `queue/operator/…-bv2-d3b.json` |
| 4 | `swarm ps` output captured | PASS | `out/d3b/ps-snapshot.md` shows the sandbox tree (bv2-d3b, helper-note, q= lines) |
| 5 | recorded commands are well-formed swarm invocations | PASS | cli-report line1 `swarm spawn helper-note "…"`; line2 `printf 'spawn-done\n' \| swarm send operator --stdin` |

The grandchild was spawned, wrote `amber`, and was verified+closed — the full spawn
cycle, exercising swarm's real plumbing.

### 3c — message-stream handling `bv2-d3c` — 4/4 PASS

M1/M2/M3 delivered as **real `swarm send` turns** (the child's `deliver` hook injected
each queue file as a UserPromptSubmit turn — swarm's native machinery, NOT an
opencode `--session` continuation). Delivered in order, each awaited before the next.

| # | check | verdict | file fact |
|---|---|---|---|
| 1 | M1 near-cap assembled whole & acted on | PASS [H] | M1 body 7553 chars delivered whole; `echo-1.md` = `amber harbor` (correct first+last words) |
| 2 | each turn acted on, no dropped clause | PASS [M] | echo-1 (amber harbor), echo-2 (your parent), echo-3 (correct 1-sentence queue def) all exist & match |
| 3 | turn order honored | PASS [H] | echo mtimes 23:12:54 ≤ 23:14:52 ≤ 23:15:21, non-decreasing in delivery order |
| 4 | M3 completion note reached parent | PASS [M] | note from bv2-d3c in `queue/operator/` after M3 |

**RIG-ADVANTAGE FINDING (native-only) — the M2 relation check the opencode rig DROPS,
PASSES here.** Rubric §3c/§7 dropped M2's "reply names the sender's relation"
check as unwitnessable under opencode (a `--session` turn carries no swarm header).
Under this native rig the `deliver` hook DID inject `[swarm message] from
run-claude-base-2 — your parent — sent …` (swarm's `relation()` returns "your parent"
because bv2-d3c's recorded parent == the sender), and the probe **echoed "your
parent" faithfully** (`echo-2.md`). So this cell witnesses a check the Chinese cells
structurally cannot — recorded here per the caveat, since the machinery is exactly
what those cells never exercise (rubric §7 "the inability is a placement fact").

**Dropped-here-too (honest, rubric §7):** none of §7's *runner→model queue* checks
apply — the model→parent direction (all report checks) stays witnessable because the
probe runs `swarm send` itself.

**D3 = 3a + 3b + 3c summed = 17/17 PASS.**

---

## D4 — LONG-HORIZON COHERENCE — 6/6 PASS

Probe `bv2-d4`. Turns 1&2 via `swarm send` into the same pane (session continuity);
**turn 3 = a GENUINE fresh session** — the runner `/quit` the turn-1/2 claude and
launched a NEW `claude --settings bv2-d4.json` session, firing swarm's SessionStart
`restore` hook (re-injects the journal tail) — the REAL restart mechanism, not a
simulation. `out/d4/catalog.md` = 3 shelves, 3 entries each, 9 books.

| # | check | verdict | file fact |
|---|---|---|---|
| 1 | stays on task ≥3 turns, all shelves survive | PASS | catalog.md holds Shelf 1/2/3 each with heading + 3 entries; Shelves 1&2 intact after restart |
| 2 | turn-1 plan journaled | PASS | journal: "Turn 1: plan+Shelf1 / Turn 2: Shelf2 / Turn 3: Shelf3 / Final pass" |
| 3 | honored the journaled plan after restart | PASS | one shelf/turn, 3 entries — matches the turn-1 shape |
| 4 | re-read own journal on restart | PASS [H]+[M] | turn-3 journal "Restarted with no in-context memory; recovered state by reading journal + catalog.md"; pane transcript shows "Read 1 file" recovery |
| 5 | resisted mid-stream distractor | PASS | NO chair/furniture content in catalog.md; the chair aside answered in ONE journal line only |
| 6 | reported to parent after completion | PASS | note from bv2-d4 in `queue/operator/` after turn 3 |

**D4 reading (rubric §4):** high D4 with high D1–D3 → **fit as a coordinator, not
only as a leaf** — this model held a 3-turn plan across a real session restart and
recovered it from its own journal.

---

## Rig honesty — what the native harness does to the witnesses

1. **`swarm spawn` control-plane is correctly sandboxed.** Tombstones, agent
   records, queues, and events for every probe (and the grandchild) landed in the
   sandbox SWARM_DIR, never live — verified after every batch (`swarm ps` in the
   probes did NOT see them as live agents in the live tree; reports landed in the
   SANDBOX queue). **Falsifier held: no control-plane record and no absolute-path
   artifact ever reached the live tree.**
2. **Self-authored journals leak to live.** A native claude probe, obeying its duty
   text's relative `.swarm/journal/{NAME}.md`, resolves it to the live tree for
   *some* probes (b-d1, b1-duties, bv2-d2c, bv2-d2h) and to the sandbox for others
   (bv2-d3a, bv2-d3b, bv2-d3c, bv2-d4) — a native-claude path nondeterminism. It
   does NOT affect any score (the journal content is identical wherever it lands and
   is fully scorable) and does NOT touch the swarm control-plane. The four live
   leaks were snapshotted against a pre-run baseline and **removed after scoring**,
   returning the live tree to baseline.
3. **report-to-parent is [H]-shaped.** The runner (`run-claude-base-2`) is NOT a
   registered agent in the sandbox tree, so a probe's `swarm send run-claude-base-2`
   hits swarm's `die(unknown agent)` guard and the probe correctly falls back to
   `swarm send operator` (the sandbox's effective parent-mailbox). Every report DID
   land; the model reported correctly — only the address space differs. Tagged [H]
   on every report check.
4. **One-time trust ack.** The fresh sandbox cwd triggered claude's "trust this
   folder?" prompt on the first spawn; acked once (persisted in `~/.claude.json`),
   so no later probe blocked. A rig-setup fact, not model behavior — excluded from
   every [M] score.
5. **Minor path-literalism (D3c only).** bv2-d3c wrote its echo files at the
   cwd-relative `out/d3c/` (still inside the sandbox via the cwd dir) rather than the
   brief's absolute `{OUTDIR}` — content all correct; not a leak, noted for honesty.

## Artifact paths (for a fresh reviewer to re-read)

- Sandbox root: `/private/tmp/claude-501/-Users-vadrsa-git-swarm/990a14af-96fd-4423-892c-3b6a1b204c99/scratchpad/bench-v2/claude-base/`
  - `swarm/` — the sandbox SWARM_DIR (journals/agents/queue/event/settings)
  - `out/d1 … out/d4` (+ `cwd/out/d3c`) — probe artifacts
  - `rendered/` — the exact rendered prompts fed to each probe
  - `live-journal-baseline.txt` — the pre-run live-journal set (cleanup basis)
- Runner journal: `.swarm/journal/run-claude-base-2.md` (full rig diagnosis + per-dim scoring).
