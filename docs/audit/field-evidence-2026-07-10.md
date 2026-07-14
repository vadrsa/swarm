# Field evidence — 2026-07-10

> SUPERSEDED by the shipped delegation doctrine in bin/swarm's spawn_header; kept for the record (the founding before/after measurement — "doctrine flipped the default").

**Author:** `field-tester`. Continuation of `field-evidence-2026-07-09.md`; same method
and evidence discipline (VERIFIED / MEASURED / SUSPECT).

## Delegation baseline (before the doctrine change)

**Question (operator's):** does a swarm agent given an obviously parallelizable task
spawn children under the CURRENT doctrine, or grind serially?

### Protocol (designed to be repeated verbatim as the after-measurement)

Spawn one probe with this task, byte-identical except the probe name and OUTDIR
(saved at `deleg-probe-brief.txt` in the session scratchpad):

> Produce four independent summaries of four unrelated documents in this repo:
> (1) README.md (2) WORLD.md (3) docs/design/SIMPLEST.md (4) docs/design/REVIEW.md.
> For each, write a ~150-word summary to OUTDIR/summary-N-\<basename\>.md (N = 1..4).
> The four are separate deliverables of equal priority; each summary must reflect only
> its own source document. When all four files exist, report to your parent
> field-tester with one line per file, then go idle. Journal as you work.

Properties: 4 genuinely independent parts; wording stresses independence ("separate",
"equal priority", "only its own source") without mentioning children, spawning, or
delegation in either direction — the only delegation exposure is the standard spawn
header (which names `swarm spawn` as available) and `swarm world` if the probe reads
it. Observables: a 3 s poller on `.swarm/agents/*.json` (any record with
`parent == <probe>` = a child, caught even if closed quickly), OUTDIR file mtimes
(serialization order), the probe's journal and pane (turn accounting).

Comparability requirements for the after-run: same parent (field-tester), same model
(default), same four docs (repo state noted below), fresh probe name (`deleg-after-…`)
and fresh OUTDIR; run it after hardener's doctrine change lands, on the operator's ping.

- Baseline run: probe `deleg-base-1`, spawned 2026-07-10 11:53:50Z (ts 1783684430187),
  repo HEAD at spawn: `eac88e2`.

### Result — BASELINE: NO DELEGATION; strictly serial, one turn (MEASURED)

- **Children spawned: zero.** The 3 s poller on `.swarm/agents/` saw `kids=[]` at every
  tick of the run, and no agent record with `"parent": "deleg-base-1"` ever existed.
  Its journal and pane confirm: it read all four docs itself and wrote all four
  summaries itself.
- **Serialization order = task order**, one summary every ~6 s after a ~25 s read phase
  (file mtimes, seconds after spawn at 11:53:50Z):

```
+25s  summary-1-README.md      (mtime 1783684455)
+31s  summary-2-WORLD.md       (1783684461)
+37s  summary-3-SIMPLEST.md    (1783684467)
+42s  summary-4-REVIEW.md      (1783684472)
+71s  report received by field-tester (11:55:01Z)
+74s  final Stop (event ts 1783684504690)
```

- **Turn accounting: 1 turn total** (its pane shows a single prompt — the spawn task;
  no message-headed or self-rung turns). Work quality was fine: all four summaries
  accurate to their sources (spot-checked; probe's own falsifier invited the check).

**Verdict (baseline): under current doctrine, an agent given a 4-way-parallelizable
task grinds serially and never considers spawning** — nothing in its journal or pane
even mentions the possibility, despite the spawn header naming `swarm spawn` first in
its tool list.

**Caveat for the comparison, stated up front:** this task is cheap enough (~42 s of
writing) that serial execution is arguably the *rational* choice — spawn overhead is
~30–60 s per child. The probe therefore measures whether doctrine *changes the
default*, not whether delegation would have been efficient here. If the after-run
delegates, that shows doctrine-following (possibly over-following — four spawns for a
71 s task would be slower); if it stays serial, the doctrine either didn't reach the
agent or correctly yielded to size judgment. Interpret jointly with timing.

Two incidental observations, consistent with yesterday's file: the probe wrote
"Resumed after restore" at its initial spawn (the spawn/restart indistinguishability,
again), and its last words show it briefly reached for a non-swarm `SendMessage` tool
before correcting to the `swarm` CLI — harness tool-surface bleed-through, harmless
here but worth remembering when reading probe behavior.

## Delegation baseline — HEAVY variant (before the doctrine change)

**Why a second size** (operator's rationale, recorded): the doctrine in progress
includes sizing heuristics, so the after-measurement must distinguish (a) default
flipped where it should (heavy → spawns), (b) default rationally unflipped (cheap →
serial, but with the option visibly weighed), (c) over-delegation churn (cheap →
pointless spawning). Both sizes therefore get before/after pairs.

### Protocol (repeat verbatim for the after-run; brief saved at
`deleg-heavy-brief.txt` in the session scratchpad)

> Four independent audit jobs on this repo, all real work: (1) FLAKE CHECK: run
> `python3 tests/test_swarm.py` 25 times in a row; write a tally of passing/failing
> runs plus any failure output to OUTDIR/report-1-flake.md. (2) REFERENCE CHECK: find
> every repo-relative file path mentioned in README.md, WORLD.md, and
> docs/design/SIMPLEST.md; check each exists on disk; write the existing/broken lists
> to OUTDIR/report-2-refs.md. (3) CONCEPT RECOUNT: list every verb and flag shown by
> `swarm --help`; check each is named in docs/design/SIMPLEST.md; write the comparison
> (named / not named) to OUTDIR/report-3-concepts.md. (4) LATENCY: run
> `swarm world >/dev/null` 25 times, timing each run; write min/mean/max milliseconds
> to OUTDIR/report-4-latency.md. The four jobs are separate deliverables of equal
> priority and share nothing with each other. When all four reports exist, report to
> your parent field-tester with one line per file, then go idle. Journal as you work.

Sizing: each job is minutes-scale but token-cheap (job 1 alone is ~2.5 min of wall
time at ~5.4 s per suite run); serial total is estimated 8–12 min vs. ~3–4 min
parallel including spawn overhead — at this size delegation is rational, unlike the
cheap probe. Same observables as the cheap variant (3 s agents-dir poller, OUTDIR
mtimes, journal, pane).

- Heavy baseline run: probe `deleg-heavy-base-1`, spawned 2026-07-10 11:57:56Z
  (ts 1783684676222), repo HEAD `eac88e2`, parent field-tester, default model.

### Result — HEAVY BASELINE: NO DELEGATION, but deliberate intra-turn parallelism (MEASURED)

- **Children spawned: zero** (poller `kids=[]` at every tick; no parent records ever;
  journal and pane corroborate). **1 turn total.** Spawn→report 4 m 36 s
  (11:57:56Z → 12:02:32Z).
- **But not a naive serial grind.** File mtimes (seconds after spawn):

```
+0:41  flake-failures.txt        <- flake loop STARTED as a background shell
+2:08  report-2-refs.md          <- refs done while flake loop still running
+2:24  report-3-concepts.md      <- concepts too
+3:42  report-1-flake.md         <- flake report written when the loop finished
+4:08  report-4-latency.md       <- latency deliberately sequenced after test load
+4:36  report to field-tester
```

  Its journal states the plan explicitly: shell loops in the background for jobs 1/4,
  reading work in the foreground for jobs 2/3, and latency *deferred* so the flake load
  wouldn't skew timings. The work products were correct and genuinely useful (5 broken
  doc refs found in SIMPLEST.md; hook entrypoints unnamed in the design; `swarm world`
  mean 69.8 ms).

**Verdict (heavy baseline): the agent plainly recognized the parallelism and exploited
it — with background shells inside its own single turn, never with children.** Spawning
is not weighed anywhere in its journal or pane. So the current-doctrine default at both
sizes is: all work stays in one context; parallelism, when seen, is expressed as
intra-agent concurrency. The after-measurement should therefore watch whether doctrine
*redirects* this existing parallelism instinct toward children, not whether it creates
the instinct.

### After-measurement setup (one variable, verified)

Per the operator: after-probes are spawned with the branch binary
`/Users/vadrsa/git/swarm-delegation/bin/swarm`. I diffed it against the installed
binary at 12:04Z: **the only difference is four doctrine sentences appended to
`spawn_header`** ("Delegate by default: keep judgment, verification, and glue; spawn
children for the work itself… each reconciliation, ask: could my remaining work be
parallelized or delegated — and if yes, why am I not spawning?…"). Everything else —
delivery, hooks, ps, close — is byte-identical, so the before/after pairs differ in
exactly one variable: those sentences in the probe's first prompt.

**Recorded limitation:** the doctrine also lands in SKILL.md, which shapes ROOT
sessions (operator-side spawning habits), not spawned agents — a spawned probe never
sees it. These probes therefore measure the header's effect only; SKILL.md's effect on
root-session behavior is untested by this experiment.

## After-runs (branch doctrine header)

**Header versions (the branch was amended mid-experiment; both quoted, per operator):**

- **v1** (binary md5 `ea5a148ae5d803d064cb070bf6c4c845`), seen by `deleg-after-1`:
  sentence 1 "Delegate by default: keep judgment, verification, and glue; spawn
  children for the work itself — doing parallelizable work serially yourself is
  off-track." + reconcile sentence "Each reconciliation, ask: could my remaining work
  be parallelized or delegated — and if yes, why am I not spawning?"
- **v2** (md5 `2f46a9019188dab7a3e4bc04cf745cab`), seen by `deleg-heavy-after-1`:
  same sentence 1; reconcile sentence now bidirectional — "Each reconciliation, ask
  whether the tree still matches the remaining work: spawn what is missing, and close
  harvested children whose workstream is done — keep a child only if you can name its
  next task." Both versions end with the same judge-delegation and
  reshape-is-normal sentences. Sentence 1 — the delegate-by-default bet — is identical
  across v1/v2; only the reconcile sentence's form differs (spawn-only question vs.
  bidirectional tree-shape question).

### Cheap after-run — `deleg-after-1` (header v1), spawned 12:03:59Z

**Result: NO children, 1 turn, 83 s spawn→report — but the delegation question was
asked and answered, in writing (outcome (b) of the operator's frame).** Journal,
verbatim:

> *"Delegation call: did NOT spawn children. Four ~150-word summaries of docs already
> read in one parallel batch — spawn/brief/judge overhead for four subagents would
> exceed the work itself several times over. Parallelism was achieved via parallel
> tool calls (all reads in one block, all writes in one block). Falsifier: if parent
> field-tester judges that the point of this task was to exercise delegation mechanics
> rather than produce summaries efficiently, this call was wrong."*

Its report to me carried the same unprompted "Delegation note." Execution also
sharpened vs. baseline: all four summaries written **within an 8 s window** (parallel
tool batches; mtimes +45 s…+53 s after spawn) against the baseline's one-every-6-s
serial sequence. Summary quality: equivalent to baseline (spot-checked).

**Cheap pair verdict: the doctrine asks the question without mandating the answer —
exactly the designed behavior.** Baseline never mentioned delegation; after-run weighed
it, priced it, declined it with a stated falsifier, and still got faster.

### Heavy after-run — `deleg-heavy-after-1` (header v2), spawned 12:06:32Z

**Result: FULL DELEGATION with verification and self-initiated tree shrink (VERIFIED +
MEASURED).** Timeline (all from file facts — agent records, report mtimes, queue
files; the probe's own journal timestamps drifted ahead of wall clock, see note):

```
12:06:32  probe spawned (ts 1783685192621)
12:07:37  dh1-flake spawned     (agent rec 1783685257757)   <- one child per job,
12:07:52  dh1-refs spawned      (1783685272826)                spawned back-to-back,
12:08:04  dh1-concepts spawned  (1783685284297)                ~15 s apart
12:08:17  dh1-latency spawned   (1783685297995)
12:08:42  report-4-latency.md   (child artifact mtimes)
12:09:13  report-3-concepts.md
12:09:39  report-2-refs.md
12:11:03  report-1-flake.md     (flake loop is the critical path)
12:12:07  probe's final summary sent to field-tester (queue file ts 1783685527835)
```

- **Division of labor matched the doctrine's words:** the probe kept "judgment,
  verification, and glue" — each child got the exact commands, the exact report path,
  and an explicit raw-evidence requirement; the probe then *verified* each report on
  arrival (recomputed the latency mean from the 25 raw rows; byte-compared the child's
  `--help` transcript; spot-checked 6 existing + 4 broken paths), judged each child's
  delegation ("judge its delegation too" — its words appear in the journal), and
  **closed each child upon harvest with the v2 close-rule cited** ("no next task
  nameable"). The poller watched the tree grow 0→4 and shrink 4→0 with no prompting.
- **All four grandchild journals carry falsifiers** — the journal convention survived
  a second generation of delegation (#4 evidence, extended).
- **Cost accounting:** spawn→summary 5 m 35 s vs. heavy baseline's 4 m 36 s — ≈+1 min
  for 4 spawns (~15 s each) plus per-report verification turns the baseline never did.
  The critical path (the 25-run flake loop) dominated both runs; delegation bought
  independent verification, not wall-clock speed, at this size.
- Work quality: equal or better than baseline (same findings, plus raw evidence
  attached per child and one bonus finding — SWARM_DIR unnamed in SIMPLEST.md).

### Incidental findings from the heavy after-run (not delegation verdicts)

1. **A Stop hook blocked for ~3 minutes** (VERIFIED live in the probe's pane:
   `running stop hook · 2m 58s`), during which two deliverable child messages sat
   queued and the agent could not take its next turn — the re-ring inside `event stop`
   is synchronous, and its pane-settle loop can spin up to ~20 × 10 s-timeout herdr
   reads under load (5 live panes here). The mechanism meant to hasten delivery
   delayed it. Degradation-not-loss held (everything drained after), but this is a
   measured latency wart in the exact direction WATCHLIST #3's fix note anticipates
   ("the retry belongs in herdr"). Mechanism attribution beyond the pane observation:
   SUSPECT (herdr slowness under concurrent pane load is inferred, not traced).
2. **Journal self-timestamps are claims, not facts** (MEASURED): the probe's journal
   entries dated "12:15Z"/"12:18Z" described states I directly observed at wall-clock
   12:12:35Z (its clock claims ran ~6 min ahead). Event files, queue-file names, and
   mtimes are the trustworthy timeline; journals narrate honestly but timestamp
   unreliably.
3. The probe handled the two child "done" messages that arrived after it had already
   read the reports gracefully — final delivery consumed them as formalities ("already
   read and acted on"), no rework, no confusion.

## Overall delegation verdicts (both pairs)

| probe | doctrine | children | shape |
|---|---|---|---|
| cheap baseline | none | 0 | serial grind; delegation never mentioned |
| heavy baseline | none | 0 | background-shell parallelism; delegation never mentioned |
| cheap after (v1) | header | 0 | **weighed delegation in writing, declined on cost, parallel tool batches** |
| heavy after (v2) | header | 4 | **spawned per job, verified each report, closed each child on harvest** |

**The doctrine flipped the default exactly where it should and only where it should**
— operator's outcome (a) on the heavy pair, outcome (b) on the cheap pair, and no
outcome (c) (no pointless spawning) observed. The four header sentences alone did
this; the probes saw no SKILL.md, no other doctrine surface. Sample size: one run per
cell — sufficient for "the trigger fired / didn't", not for rates.
