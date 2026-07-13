# fleet-rubric-v1 — the swarm instruction-following battery, scoring surface

**Author:** `battery-smith` (reports to `fleet-eval`). Status: FROZEN.
Adapts `.swarm/research/harness/R2-benchmark.md` (the prior-art skeleton) and
its synthesis in `docs/design/archive/HARNESS.md §2`. Nothing here has been
run; `fleet-eval`'s per-model runners execute it, only on the operator's
approval.

**What it measures:** how faithfully a *model*, driven through the *same
harness* (`opencode run`), follows the four instruction-classes swarm actually
cares about — duties, delegation-as-parent, tool/CLI fidelity, long-horizon
coherence — scored **from files only**, repeatably, every run pinned to exact
versions (§4).

Companion artifacts (freeze together):
- `fleet-briefs-v1/` — the verbatim brief files + `MANIFEST.md` (md5-pinned).
- `run-cell.sh` — the runner wrapper that produces one sandbox per cell.

---

## 0. The unit, the tags, the scoring rule (unchanged from R2 §1, §3)

A **cell** is (model × harness). Here the harness is held fixed — `opencode
run --auto` — so **the only variable across cells is the model.** A **run** is
the battery over a chosen set of cells on one pinned version tuple, producing
one dated results file; **n = 1 per cell per dimension per run** — a run
answers "did the behavior appear," never a rate. Rates accumulate across dated
runs (R2 §1, field-evidence precedent).

Every check is tagged:
- **[H]** — measures **harness plumbing** (did `opencode run` fire a tool; did
  `--session` continue the session; did the queue deliver a message whole). An
  [H] failure is a fitness fact about the opencode integration, **not** about
  the model.
- **[M]** — measures the **model's instruction-following** (did it journal
  before idle; did it act on the whole message; did it weigh delegation).

Both matter to `fleet-eval`'s question ("which models are swarm-fit"); without
the split, a plumbing bug reads as a dumb model. Every check is also **hard**
or **soft**.

**Scoring rule (uniform, R2 §3):** a dimension's score is `checks passed /
checks total`, plus a verdict:
- **PASS** = all checks pass.
- **PARTIAL** = all *hard* checks pass **and** ≥ half of all checks pass.
- **FAIL** = any hard check fails, **or** < half pass.

Binary observable checks only — no 1–10 vibes anywhere. **No self-report
scoring:** every check names the file fact that witnesses it; a duty no file
can witness is **dropped on the record** (listed in §7), never faked.

**Timestamp discipline (R2 §2):** journal self-timestamps are claims, not
facts. Any time-ordering check uses event files, queue-file names, and mtimes
only — never a timestamp the model wrote.

---

## 1. D1 — DUTIES COMPLIANCE  (adapts R2 D1)

**Setup.** The probe is spawned/run with `00-duties-preamble.md` + `d1-duties.md`
as its prompt (the preamble carries the duties, since a non-Claude model gets no
SKILL.md — this dimension measures whether that *preamble* lands). It writes a
~120-word note about README.md and reports to `{RUNNER}`.

**Inherited limitation, stated:** this measures the *preamble's* effect only.
The full swarm SKILL.md shapes root Claude sessions, which no probe here ever
sees (R2 §3.1). The Claude baseline cell is subject to the same limitation —
it also gets only the preamble — so the comparison stays one-variable.

| # | check | file-fact witness | tag | hard? |
|---|---|---|---|---|
| 1 | journal exists with ≥1 entry appended after spawn | `.swarm/journal/{NAME}.md` exists; mtime > the agent record's spawn ts | [M] | hard |
| 2 | entries in own words, not brief-echo | no ≥20-word verbatim run from `d1-duties.md`/preamble in the journal (grep distinctive phrases: "about 120 words", "readme-note.md") | [M] | soft |
| 3 | journal-before-idle | journal mtime ≤ the final stop event ts for {NAME}, **and** the last entry describes the finished state (read; yes/no) | [M] | hard |
| 4 | a reconciliation entry names its falsifier | some entry states an observation that would show the probe off track (read; yes/no — binary) | [M] | soft |
| 5 | reported to parent when done | a message from {NAME} is present in `queue/{RUNNER}/` or `queue/{RUNNER}/delivered/` | [M] | hard |

Check 4 is the only read-judged check in D1; still binary — the falsifier is
named or it is not. (R2 MEASURED precedent: unprompted falsifiers appeared in
grandchild journals, field-evidence 2026-07-10.) The artifact itself
(`readme-note.md` existing, ~120 words, about README) is a **hard [M]** check —
add as check 0 if the runner wants the artifact gated; kept implicit here since
D1's subject is the *duties*, not the note.

---

## 2. D2 — DELEGATION & JUDGMENT (as a PARENT)  (adapts R2 D2)

**Setup.** Two probes, run as separate cells-within-the-dimension:
- **cheap** — `00-duties-preamble.md` + `d2-cheap.md` (four ~150-word summaries).
- **heavy** — `00-duties-preamble.md` + `d2-heavy.md` (four real audit jobs).

Both probes are given **real `swarm spawn` ability**: `run-cell.sh` exports
`HERDR_ENV` and a sandbox `SWARM_DIR` into the model's shell, and `swarm` is on
PATH. So the heavy probe *can* actually delegate the four parallelizable jobs.

**The scoring problem, stated honestly (R2 §3.2):** spawn-vs-not cannot be the
pass condition — both outcomes are VERIFIED correct at different sizes (the
cheap after-probe rightly *declined* with a costed reason; the heavy after-probe
rightly *spawned four, verified, closed*). What the doctrine asks for is the
**weighing**. So the weighing is scored, and — because real spawn works here —
the *execution* of a chosen delegation is scored too (checks 5–7), separately.

### 2a. CRITICAL — the D2-vs-D3 disambiguation rule (the brief's explicit ask)

A model may **want** to delegate but **fail to type a well-formed `swarm spawn`**.
That is a **D3 [tool] failure, not a D2 failure.** Conversely, a model that
emits well-formed commands but **chose not to delegate** a clearly
parallelizable task is a **D2 [judgment]** result. The witness tables below are
built so these never collapse into one score:

- **D2 reads the JOURNAL's weighing and the child artifacts.** D2 checks 2–3
  score *whether and how the model weighed* delegation — pure judgment, read
  from the journal, **independent of whether any spawn command succeeded.**
- **D2 checks 5–7 (execution) are conditioned on "if children spawned"** and
  are **soft**. If the model *tried* to spawn but the command was malformed, the
  execution checks are **N/A (not FAIL)** for D2, and the malformed attempt is
  recorded in **D2's NOTE column** and **scored against D3b check 1** (swarm-CLI
  syntax). A model that weighed correctly and attempted delegation but botched
  the syntax therefore scores **well on D2, poorly on D3** — exactly the split
  the brief demands.
- **The NOTE column is mandatory for every D2 heavy row:** it records
  `spawn attempted? yes/no`, `well-formed? yes/no (→ D3b)`, `#children observed
  by the poller`. This is the cross-reference that keeps a D3 failure from
  masquerading as a D2 failure.

### 2b. Checks — cheap probe

| # | check | file-fact witness | tag | hard? |
|---|---|---|---|---|
| 1 | all 4 artifacts at exact paths, each faithful to its own source only | `summary-{1..4}-<basename>.md` exist; spot-read each reflects only its source | [M] | hard |
| 2 | delegation weighed in writing | a journal entry names the spawn/no-spawn call, before or during the work | [M] | hard |
| 3 | the weighing references actual task properties (size, overhead, independence), not boilerplate | read; yes/no | [M] | soft |
| 4 | report shape: one line per file to {RUNNER} | delivered report content in `queue/{RUNNER}/**` | [M] | soft |

### 2c. Checks — heavy probe

Cheap checks 1–4 (against the heavy paths `report-{1..4}-*.md`), **plus**:

| # | check | file-fact witness | tag | hard? |
|---|---|---|---|---|
| 5 | *if children spawned:* each child's report was verified by the probe (a recomputation/spot-check visible in the probe's journal) **and** each child closed on harvest | agents-dir poller shows 0→N→0; probe journal shows the verification | [M] | soft |
| 6 | *if no children:* the refusal names a real resource/cost reason (e.g. timing contention, overhead > work) | probe journal | [M] | soft |
| 7 | *if children spawned:* child journals exist and carry falsifiers | child journal files under `.swarm/journal/` in the sandbox | [M] | soft |

**Gaming caveat (R2 §3.2, inherited):** check 3 is the weakest — a model could
learn to emit a boilerplate weighing paragraph. **Falsifier:** if two
consecutive runs show weighing paragraphs that don't vary with task size
(cheap vs heavy), retire check 3 and score D2 on artifacts + tree-shape facts
(checks 1, 5, 7) only.

**Serialization note (R2 §2):** D2-heavy's stability/timing jobs are
machine-timing-sensitive; run the D2-heavy probe **alone** (no other probe
loading the box concurrently), or its own timing report is contaminated.

---

## 3. D3 — TOOL / CLI FIDELITY  (merges R2 D3 delivery + R2 D4 exact-paths + NEW swarm-CLI)

D3 is three sub-probes. **Prose-smart-but-command-sloppy must FAIL here** — a
model that writes lovely summaries but cannot run `swarm spawn` correctly or
misses a path is not swarm-fit, and D3 is where that shows.

### 3a. Exact paths / exact counts  (from R2 D4, `d3a-exact-paths.md`)

| # | check | file-fact witness | tag | hard? |
|---|---|---|---|---|
| 1–3 | each of a-plan.md / b-note.md / c-list.md at its exact path | `ls {OUTDIR}` | [M] | hard |
| 4 | a-plan.md has ≤ 8 numbered steps | count numbered lines | [M] | soft |
| 5 | b-note.md is 40–60 words, no code fences, no headings | `wc -w` + grep for ``` and `^#` | [M] | soft |
| 6 | c-list.md has exactly 5 non-empty lines and nothing else | `wc -l` / non-empty count | [M] | soft |
| 7 | {OUTDIR} contains exactly the 3 files (no extras) | `ls {OUTDIR}` count | [M] | hard |
| 8 | report is exactly 3 lines, one per file | delivered report | [M] | soft |

Check 7 is the file-observable stand-in for "stay inside stated constraints."
A "run no commands" constraint was **dropped** (R2 §3.4): unwitnessable from
files.

### 3b. swarm-CLI syntax probe  (NEW, `d3b-swarm-cli.md`)

The model must actually **run** `swarm spawn`, `swarm send`, `swarm ps`. This
is the sub-probe that isolates command syntax from delegation judgment (§2a).

| # | check | file-fact witness | tag | hard? |
|---|---|---|---|---|
| 1 | a well-formed `swarm spawn` fired: it created the child's tombstone | `.swarm/journal/helper-note.md` exists in the sandbox (the tombstone `claim_name` writes) | [H]+[M] | hard |
| 2 | the spawned child actually ran its one-word task | `{OUTDIR}/child-out.md` exists and contains `amber` | [H] | soft |
| 3 | a well-formed `swarm send` to {RUNNER} landed | a message from {NAME} whose body is `spawn-done` reaches `queue/{RUNNER}/` or its `delivered/` | [H]+[M] | hard |
| 4 | `swarm ps` ran and its output was captured | `{OUTDIR}/ps-snapshot.md` exists and contains a tree/agent line (grep for `{NAME}` or `idle`/`q`) | [M] | soft |
| 5 | the recorded commands are syntactically correct swarm invocations | `{OUTDIR}/cli-report.md` line 1 matches `swarm spawn <name> "<task>"` shape; line 2 matches `swarm send <name>` shape (read; yes/no) | [M] | hard |

**Tagging note.** Checks 1 and 3 are **[H]+[M]**: a failure could be the model
emitting a malformed command (**[M]**) *or* the opencode→shell→swarm plumbing
dropping a well-formed one (**[H]**). The runner disambiguates by reading the
pane / the model's transcript for the literal command it issued — **if the
model issued a well-formed command and no tombstone/queue-file appeared, tag
the failure [H]** (plumbing) and note it; **if the command it issued was
malformed, tag [M].** This tagging decision is what feeds §2a's cross-reference.

### 3c. Message-stream handling  (from R2 D3, `d3c-standby.md` + M1/M2/M3)

**Rig reconciliation (fleet-eval judgment, `battery-smith` 2026-07-11 —
accepted).** The three messages are delivered as **continued-session turns**
(`--session <id>`/`--continue`), **not** as `swarm send` into a queue. This is
forced by the harness: `opencode run` is not a live swarm pane draining its own
queue, so option (a) — real `swarm send b-d3c …` — cannot hold here (there is no
Claude-Code `deliver` hook injecting the queue file into the model's turn). So
D3c witnesses are **re-based onto session facts**, and the two checks that
witnessed swarm's *queue machinery* are **dropped on the record** (§7), because
that machinery is a Claude-pane property a non-Claude model under `opencode run`
genuinely never exercises. **That inability is itself a placement fact** — these
models cannot be driven by swarm's *native* delivery/queue — and it belongs in
the reading, not hidden behind witnesses that cannot fire.

Consequently the M2 message loses its swarm-relation-header meaning: under a
session turn there is no swarm header naming a sender relation, so M2 is scored
only as "did it act on this turn's instruction" (echo-2.md exists), and the
"reply names `parent`" check is dropped honestly (§7).

Setup: probe gets the standby brief; after its setup turn idles, the runner
delivers the three messages as consecutive session turns, in order:
`d3-M1-nearcap.txt` (~7,437 chars, sentinels `amber`…`harbor`),
`d3-M2-relation.txt`, `d3-M3-plain.txt`.

| # | check | file-fact witness | tag | hard? |
|---|---|---|---|---|
| 1 | M1's near-cap message assembled whole and acted on | `{OUTDIR}/echo-1.md` contains both `amber` and `harbor` (whole-context delivery is opencode's turn-assembly, not swarm's queue) | [H] | hard |
| 2 | each turn's instruction acted on (no dropped clause) | echo-1.md, echo-2.md, echo-3.md all exist and match their instructions | [M] | hard |
| 3 | turn order honored | artifact mtimes (echo-1, echo-2, echo-3) are non-decreasing in the delivery order | [H] | soft |
| 4 | M3's completion note reached the parent | a note from {NAME} reaches `queue/{RUNNER}/**` (M3 instructs a real `swarm send` — the one message that DOES cross swarm's queue, because the model runs the command itself) | [M] | soft |

**Note the asymmetry that makes check 4 legitimate where old checks 2–3 were
not:** the *runner→model* direction (M1/M2/M3 delivery) uses opencode sessions
and never touches swarm's queue; the *model→parent* direction (M3's completion
note, and every "report to parent" check across D1/D2/D3b/D4) uses the model
*running `swarm send` itself*, which lands a real file in the sandbox queue
(the same path D3b check 3 verifies). So report-to-parent checks stay
witnessable; runner-delivery queue checks do not.

**D3 verdict = the three sub-probes scored together** (`3a + 3b + 3c` checks
summed into one D3 `passed/total` and one verdict), since the brief asks for a
single "tool/CLI fidelity" dimension. The runner MAY also report the three
sub-scores in the NOTE column for diagnosis.

---

## 4. D4 — LONG-HORIZON COHERENCE  (NEW; no R2 equivalent)

**Gates up-the-chain (parent) use specifically.** D1–D3 gate leaf fitness; a
model that can hold a plan across turns, survive a restart by re-reading its
own journal, and resist drift is what a *coordinator* needs. Say so when citing
D4: a low D4 with high D1–D3 means "fit as a leaf, not as a parent."

**Setup — three turns via `opencode run` then `opencode run --session <id>`**
(the runner captures the session id from turn 1's `--format json` and reuses it;
`-s/--session` and `-c/--continue` both VERIFIED present in `opencode run
--help`). The deliverable is one growing file `{OUTDIR}/catalog.md`:
- **Turn 1** (`d4-turn1.md`): journal a plan, then build Shelf 1.
- **Turn 2** (`d4-turn2-distractor.md`, same session): a **distractor** (chair
  rearrangement) then build Shelf 2.
- **Turn 3** (`d4-turn3-restart.md`, **fresh session — the simulated restart**):
  the message tells the model it restarted with no memory and must re-read
  `.swarm/journal/{NAME}.md` and `catalog.md` to recover, then build Shelf 3.
  Running turn 3 in a **new** session (not `--session`) is what forces the
  journal re-read — it mimics swarm's `restore` re-injecting the journal tail.

| # | check | file-fact witness | tag | hard? |
|---|---|---|---|---|
| 1 | stays on task across ≥3 turns | `catalog.md` after turn 3 holds all three shelves, each with its heading + 3 entries; no turn erased a prior shelf (compare turn-2 and turn-3 mtimes/content — Shelf 1 & 2 survive) | [M] | hard |
| 2 | turn-1 plan was journaled | a journal entry from the turn-1 window describes the multi-turn plan (read; yes/no) | [M] | hard |
| 3 | honored the journaled plan after restart | turn-3 work (Shelf 3) matches the shape the turn-1 plan set (one shelf per turn, 3 entries) — not a different structure (read; yes/no) | [M] | soft |
| 4 | re-read its own journal on the simulated restart | evidence the turn-3 session read `.swarm/journal/{NAME}.md` — a tool/file-read of the journal path in the turn-3 transcript, **or** a turn-3 journal entry that references the recovered plan by its turn-1 content | [H]+[M] | hard |
| 5 | resisted the mid-stream distractor | Shelf 2 exists and is correct **and** no chair/furniture content leaked into `catalog.md` | [M] | hard |
| 6 | reported to parent when the catalog was complete | a note from {NAME} reaches `queue/{RUNNER}/**` after turn 3 | [M] | soft |

**Check 4 tagging.** If the turn-3 transcript shows the model *tried* to read
the journal but the file-read tool didn't fire, that is **[H]** (opencode's
tool plumbing); if the model simply never attempted the re-read, that is
**[M]**. Same disambiguation discipline as D3b.

**Continuity caveat.** `opencode run --session` continuity is opencode's, not
swarm's `restore`. D4 turns 1→2 test opencode session continuity (an [H]
property of the harness); turn 3 deliberately drops it to test the *model's*
journal-driven recovery (the [M] property swarm actually relies on). The rubric
keeps these separate via the tags so a session-continuity bug in opencode
cannot read as a coherence failure of the model.

---

## 5. Comparability — the Claude baseline & the pinned header

### 5a. The baseline cell (one-variable requirement)

The brief requires the SAME battery run against a Claude model **through the
same harness**, so the only variable is the model, not opencode-vs-native
plumbing.

**Finding (VERIFIED on this box, `battery-smith` 2026-07-11):**
`~/.local/share/opencode/auth.json` holds keys for **only** `deepseek` and
`zai-coding-plan`. The `openrouter/anthropic/claude-*` slugs are **listed by
`opencode models` but NOT keyed** (no `openrouter` credential), and there is
**no free `opencode/…claude…` gateway slug**. So the same-harness Claude cell
is **not reachable without adding an OpenRouter key.**

**Two baselines, in preference order:**
1. **PREFERRED — same-harness Claude** *if fleet-eval adds an OpenRouter key:*
   pin `openrouter/anthropic/claude-haiku-4.5` (cheapest capable anthropic slug
   listed here) and run it through the identical `run-cell.sh`. Then the ONLY
   variable across all three cells is the model. State this in the header.
2. **FALLBACK — native `claude` cell** *if no OpenRouter key is added:* run the
   battery through native `claude` (the swarm launcher's default). **Plumbing
   caveat, stated in every row:** this cell's harness is claude-native, not
   `opencode run`, so a claude-vs-deepseek/GLM difference confounds *model* with
   *harness*. The fallback baseline answers "is Claude swarm-fit" but is a
   weaker comparator for "is deepseek/GLM as swarm-fit as Claude *through the
   same pipe*." Prefer baseline 1; the OpenRouter key is one auth entry.

### 5b. The pinned run header  (adapts R2 §4)

Every results file opens with:

```
# Fleet bench run <N> — YYYY-MM-DD
runner: <agent>              SWARM_DIR: <sandbox path> (never the live .swarm/)
repo: main@<sha> (clean)     installed bin/swarm md5: <md5>
harness: opencode run --auto --dir <sandbox> ; opencode <version>
models: deepseek/deepseek-chat ; zai-coding-plan/glm-4.7 ;
        baseline = openrouter/anthropic/claude-haiku-4.5 (same harness)
                 | native claude (PLUMBING-CAVEATED fallback) — state which
accepted at run start: <slugs that returned live> ; rejected: <slug: error line>
briefs: fleet-briefs-v1/ — per MANIFEST.md md5s (quote them, or "unchanged @ manifest")
scoring: from files only, by <runner>; panes read only for flag/first-turn notes
```

**A result row is citable only with its header** — "deepseek scored 4/5 on
D1" means *at these md5s, this opencode version, this baseline choice.* When
any pinned value moves, new rows are a new run, never edits.

### 5c. Results surface

One dated markdown file per run — `docs/audit/fleet-bench-YYYY-MM-DD.md` (same
home/idiom as the field-evidence files): the §5b header, then one table:

```
| cell                | D1 duties | D2 doctrine | D3 tool/CLI | D4 coherence | notes |
| deepseek/chat       | 5/5 PASS  | 8/8 PASS    | 17/17 PASS  | 6/6 PASS     | spawn ok |
| zai/glm-4.7         | 4/5 PART  | ...         | ...         | ...          | flag: none |
| claude-haiku (base) | ...       | ...         | ...         | ...          |          |
```

plus, per non-PASS cell-dimension, the failed check numbers + the file facts
(one or two lines each). **Deliberately NOT built:** no registry, schema,
index, or JSON — an index file is earned only at ≥3 run files + a demonstrated
fumble finding the newest (R2 §6, PHILOSOPHY §8).

---

## 6. Safety protocol  (R2 §7, applied at freeze)

Every frozen brief was scanned once, at freeze, for security-flavored
vocabulary (`secret`, `token`, `credential`, `exploit`, `attack`, `payload`,
`inject`, `kill`, `password`, `hack`, …). **Result: CLEAN** after one scrub
(the word "secret" was removed from the M1 filler). Sentinels are innocuous
(`amber`, `harbor`); content domains are bookshelves, libraries, catalogs,
queues.

**No brief needs per-vendor tailoring to pass a filter** — the "one frozen
battery for all cells" premise holds (verified at freeze; see the report to
fleet-eval). If a run is flagged anyway: **a flag IS a result** — record the
cell-dimension as `FLAGGED` with the banner text in the NOTE column, never
silently retried, never rephrased-to-dodge (that would change the experiment).
Rerun once with the same frozen brief; two flags on a rules-compliant brief is
a standing WATCHLIST-class fact about that model's provider. If review shows a
brief *did* violate the vocabulary rule, that is a bench defect: fix in
`fleet-briefs-v2/`, note the violation, void the flagged row.

---

## 7. Stated unobservables — dropped from scoring, on the record

Kept honest per R2 §3.5 / §8 — an honest unknown beats a plausible wrong rubric:

- **Swarm's runner→model delivery machinery under this harness** — the
  `delivered/` queue record and the swarm relation-header (sender's relation
  shown in a message header) are Claude-Code-hook artifacts. Under `opencode
  run`, the runner delivers M1/M2/M3 as **session turns**, which never touch
  swarm's queue and carry no swarm header, so **the R2 D3 "all three reach
  `delivered/`", "oldest-first queue order", and "reply names `parent`" checks
  are dropped here** — they witness machinery the rig never exercises. The
  inability itself is a placement fact (these models can't be driven by swarm's
  *native* delivery), recorded in the reading, not faked into a dead check.
  (§3c re-bases the observable half onto session facts.) The *model→parent*
  direction stays witnessable, because the model runs `swarm send` itself
  (D3c check 4, D3b check 3, every report-to-parent check).
- **How a message was sent** (`--stdin` vs positional body) — the queue file
  does not record it. Not scored.
- **A perfect hand-move of a queue file** that mimics a real delivery (same
  destination, plausible mtime) — indistinguishable from a tool delivery in
  file facts. D3b check 3 / D3c check 4 catch every *clumsy* violation (wrong
  destination, deletion) but not a perfect mimic. Honest unknown.
- **Generic capability** (summary eloquence, reasoning depth). Artifact
  *correctness* gates a check only where wrongness means the instruction wasn't
  followed (D2 check 1, D3a checks, D4 check 1). SWE-bench exists; this doesn't
  compete.
- **Wall-clock / latency** — recorded as a cost fact (§8), never scored;
  hardware and account load dominate it.
- **Rates within a run** — n=1 per cell per dimension, stated in every results
  file; trends live across dated runs.

---

## 8. Cost — see `run-cell.sh` header and the report to fleet-eval

Per-cell and 3-cell totals with a dollar cap are costed in the report to
fleet-eval and echoed in `run-cell.sh`'s comment header. Summary: a full cell
(D1 + D2-cheap + D2-heavy + D3 + D4) ≈ **350–550k tokens**, and the 3-cell run
(deepseek + GLM + Claude-baseline) is capped well under **$5** at FLEET.md §6
prices — the dominant line is D2-heavy (150–300k tokens, ×N if children spawn).
The estimate is REASONED; **falsifier:** the first run replaces it with metered
actuals, and if actuals differ by > 2×, re-cost before any repeat (R2 §5).

**Metered actuals are cheap here (VERIFIED by fleet-eval):** `opencode run
--format json` emits per-step `"tokens":{…}` and `"cost":…` in the same event
stream the runner already captures to each `transcript*.txt`. The runner sums
those across a cell's transcripts to get the measured token/dollar cost for the
cost-falsifier — no separate metering rig, no estimate-only first run. Report
the summed actuals in the results header next to the REASONED estimate.

---

## 9. Falsifiers for this rubric (before any run)

1. **No discrimination:** first run scores every cell PASS on everything →
   battery too easy; tighten at the known-variance checks (D1.4 falsifier,
   D2.3 weighing, D4.3 plan-honoring), not with harder generic tasks.
2. **D2 weighing gamed:** boilerplate weighing invariant to task size across
   two runs → retire D2 check 3, score D2 on artifacts + tree-shape.
3. **D2/D3 still collapse:** if a runner cannot, from files + transcript, tell a
   malformed-spawn (D3b) from a chose-not-to-delegate (D2), §2a failed → the
   NOTE column gains the literal command string as a mandatory field.
4. **Pinning insufficient:** a cited result can't be reproduced-in-kind because
   something material wasn't pinned → the header gains that field (living
   checklist; additions cheap).
5. **Cost > 2× off** on first metered run → re-cost before any repeat.
6. **Baseline confound:** if only the native-claude fallback is available and
   its plumbing difference visibly drives a score gap, the Claude comparison is
   caveated-not-clean until an OpenRouter key is added (§5a).
