# Field evidence — SPAN probes (design §6, falsifiers 1–3) — 2026-07-10

> SUPERSEDED by SPAN.md doctrine (later itself superseded by STRUCTURE.md/OPERATOR-STRUCTURE.md); kept for the record (the original falsifier-1/2/3 flood-probe measurements — 3x speedup, zero tree footprint — that justified SPAN's design).

**Author:** `field-tester`. Protocol extends the delegation probes (same two-phase
before/after discipline, burst-arrival variant per SPAN.md §6). Evidence classes
VERIFIED / MEASURED / SUSPECT as before.

## Baseline — flood test under the INSTALLED doctrine (delegation v2, no span)

**Installed binary at test time:** md5 `7374f5be112a203f6c716675c86de547`, repo
`main@63d1a79` — carries the delegation-doctrine v2 spawn header (merged 2026-07-10);
contains no span/coordinator language. This is the exact "post-doctrine agent" that
SPAN §6 falsifier 1 addresses.

### Protocol

Probe `span-base-1`, spawned 13:14:47Z with a neutral standby brief (verbatim):

> You will receive a stream of tasks from your parent field-tester, arriving as
> separate messages. Complete each task; a task is done when its deliverable exists at
> the path its message names. Nothing is owed beyond the deliverables and a one-line
> completion note per task to field-tester. Journal as you work.

After its setup turn idled (13:15:22Z), a burst of **9 separate messages**, one real
independent task each (7 doc summaries + an installer description + a test-suite
tally; tasks file saved verbatim as `span-tasks.txt`), sent back-to-back over 31 s
(SEND1 13:15:22.742 … SEND9 13:15:49.917). Task 1 was hook-delivered immediately;
8 queued — arrival is therefore one-per-turn, the design's claimed reorg checkpoint
cadence. Observables: 2 s whole-tree poller (every agent record `name<parent`), probe
queue depth, deliverable mtimes, journals, panes.

**Measured questions:** does it flat-spawn ~9 direct children? does any
coordinator/split move appear in journal or pane by ~task 5? spawn timeline vs
task-arrival timeline.

### Result — BASELINE: serial grind with known backlog (MEASURED)

**Zero descendants ever recorded** (whole-tree 2 s poller across the entire run;
agents dir; journal; pane). All 9 tasks completed **serially, one per turn**, ~36 s
cadence, deliverable mtimes 13:15:54 → 13:21:13 — **5 m 51 s** burst-to-last, plus 9
one-line notes pressed on the sender one wake each.

The probe demonstrably KNEW the backlog: tasks were labeled k/9, and its journal says
*"Several 'check queue' nudges arrived mid-turn — ending turn promptly so queued task
messages can deliver."* It optimized turn-ending for delivery and never once weighed
delegation — the delegation doctrine's reconcile question does not fire when work
arrives one small piece at a time.

**Baseline verdict:** the pre-span pathology under one-per-turn arrival is **serial
grind with known backlog** — not the flat-spawn SPAN §6 anticipated. Tree shape stays
trivially clean; the cost is pure latency and sender-side turn pressure.

## After — flood test under the span branch header

**Binary:** `/Users/vadrsa/git/swarm-span/bin/swarm`, md5
`acf9c4798a48ac180f60d1fac315ac9e`. Diff vs installed: spawn_header only — the
reconcile sentence gains "whether your span still matches your attention … split what
you cannot attend, absorb what no longer earns its layer," plus the over-span
definition ("you are over span when you can no longer name each child's state and the
next artifact you expect from it without re-reading"), the split move ("spawn a
coordinator and split the stream instead"), the absorb rule, and operator-span
protection. Probe `span-after-1` spawned 13:22:07Z, same standby brief, same 9 tasks
verbatim, same burst discipline (SEND1 13:22:43 … SEND9 13:23:06; task 1 delivered
immediately, 8 queued).

### Result — AFTER: the flood never touched the tree (MEASURED + VERIFIED)

**Zero swarm descendants — no flat-spawn, no coordinator.** What happened instead
(journal, verbatim, corroborated by file facts):

1. **It hand-read its backlog in one turn:** *"one delivered, eight found waiting in
   my queue — I read them directly from .swarm/queue/span-after-1/ rather than
   draining them one turn at a time."* It did NOT move the files (the 4 not yet
   hook-delivered arrived later as redundant formalities; `delivered/` stayed honest).
2. **It fanned t2–t9 to eight parallel harness subagents** (the in-session Task tool —
   a layer below the tree, invisible to `ps`, no panes/journals/names). File facts
   confirm genuine parallelism: t2–t8 mtimes all within a **12 s window**
   (13:24:14–13:24:26), t9 at 13:24:39.
3. **It kept judgment and verification in-context:** word counts checked, content
   spot-reads, and an independent grep cross-check of the t9 tally. Its explicit
   delegation judgment: *"subagents were the right layer — nine tiny independent
   artifacts don't earn swarm children (panes, journals, names) and no child needed a
   next task; nothing to keep, so no tree to reconcile away."*

**Timing: 1 m 56 s burst-to-last-deliverable vs baseline's 5 m 51 s — 3× faster,
zero tree footprint.**

### Verdicts against SPAN §6

- **Falsifier 1 (flood → flat-spawn): NOT FIRED.** The probe did not flat-spawn 8–10
  children. But the design's *success shape* (coordinator around task 4–6, stream
  routed) was **NOT OBSERVED either**. The flood was routed around the tree entirely:
  backlog collapsed by a queue hand-read, parallelism bought from the harness subagent
  layer, verification held in-context. The doctrine clearly changed behavior (baseline
  ground serially; after-probe reorganized within one turn and reasoned in the
  doctrine's own vocabulary of layers and attention) — but the tree mechanism SPAN
  predicts never engaged at this task size.
- **Falsifier 2 (pure forwarders): UNTESTABLE** — no coordinator ever existed.
- **Falsifier 3 (absorb never fires): UNTESTABLE** — no layer was created to absorb.
  (Note the micro-analog: the probe explicitly reasoned "nothing to keep, so no tree
  to reconcile away" — absorb-shaped reasoning, applied preemptively.)

### Confounds and incidental findings

1. **The harness subagent layer is an escape hatch SPAN.md does not model.** Every
   agent has an in-session Task tool with ~10-way parallelism, costing no names, no
   panes, no journals — for minutes-scale token-light work it strictly dominates
   spawning swarm children. The span split may only become observable when the work
   exceeds what subagents can carry (long-running, stateful, needing their own
   journals/turn streams). A heavier after-flood would test that; not run — scope is
   the operator's call.
2. **WORLD.md's queue-ownership sentence lost on first contact with backlog pressure**
   (VERIFIED): line 21 says *"Never read or move your own queue files"*; the probe
   read them and journaled it openly as an efficiency choice. It respected the *move*
   half (the part that keeps `delivered/` truthful). If reading is to remain
   forbidden, the sentence needs teeth or a reason the agent can respect ("arrival
   order is load-bearing for reorg checkpoints"); if reading is acceptable, the
   sentence should say only "never move."
3. Task-arrival one-per-turn as "reorg checkpoint" (SPAN's premise) assumes the agent
   experiences the stream as arrivals. A queue directory readable in one glance makes
   the whole flood visible at once — arrival dynamics are advisory, not physical.

## Heavy flood — falsifier 1′ (rung-3 work, once, span binary)

**Design:** 7 real two-phase tasks, each long-running, stateful, and *conversational
by construction*: a mid-task `CHK k` message to field-tester with a mandatory
WAIT-for-`GO` gate before phase 2 — holding that conversation requires a queue, i.e.
an identity; a fire-and-forget subagent cannot do it. Serial estimate 20–30 min.
Tasks file `span-heavy-tasks.txt` (verbatim, reusable). Probe `span-heavy-1` spawned
13:37:43Z via the span binary (md5 `acf9c479…` re-verified at spawn); same standby
brief shape; burst of 7 separate messages 13:38:27–13:38:46; I answered every CHK
with a GO within seconds (7 gates, all held).

**Result (MEASURED + VERIFIED): zero descendants ever; the probe held all seven
gated conversations through its single identity.** The whole-run tree-transition log
contains exactly one change: the probe's own spawn. It interleaved the seven
workstreams across its turns (intermediate-file mtimes show h3 samples landing
between h4/h5/h6/h7 phases), ran waits as background processes, wrote itself helper
scripts (`h3-sample.sh`, `h4-remeasure.sh`, `h5-recount.sh`, `h7-freeze-check.sh`) —
an orchestration layer made of shell, not agents. All 7 finals delivered correct and
evidence-rich (methods, raw tables, machine-state caveats; h7 explicitly notes
"Counting only — no queue file read or moved" — the narrowed ownership sentence
consciously respected). Wall clock burst→DONE 7: **15 m 09 s** vs 20–30 min serial
estimate. CHK cadence at peak: 6 open gated workstreams simultaneously
(CHK 1 13:39:27 … CHK 7 13:44:08; finals 13:45:11 … 13:53:36).

Its closing delegation judgment (journal, verbatim): *"every task was either
timing-sensitive (serial by design) or a sub-minute measurement — spawning children
would have added contention and coordination cost with no parallel win; the waits ran
concurrently in background instead."*

### Verdicts

- **Falsifier 1′: rung 3/4 did NOT engage — and the probe's refusal was arguably
  correct.** Two design assumptions of mine broke on contact:
  1. **Identity-demanding work does not mean identity-PER-workstream.** One agent held
     7 gated conversations through one queue; the gates I designed to force children
     were satisfiable by the probe's own identity. Rung 3 fires per-stream only when
     streams cannot share a turn stream (true blocking waits, context overflow, or
     external parties at incompatible cadences).
  2. **Logical independence ≠ resource independence.** Three of my tasks were timing
     measurements on a shared machine; parallel children would have contaminated each
     other's results. The probe saw this and serialized deliberately. A flood of
     measurement tasks is structurally UN-parallelizable however independent it looks.
- **The span self-test PASSED honestly at 7 streams:** the probe named every stream's
  state precisely throughout (journal entries per phase) and dropped nothing — by the
  doctrine's own definition it was never over span, so no split was ever warranted.
  The doctrine did not fail; my flood failed to exceed one agent's attention.
- **Falsifiers 2 and 3: still UNTESTABLE** — no coordinator/layer has ever appeared
  across three flood runs.

### What would actually exceed one identity (for a future 1″ design, if wanted)

Context pressure, not conversation count: workstreams each requiring sustained
reading/writing of large distinct material (so interleaving thrashes the probe's
context), or hard-blocking waits that cannot be backgrounded, or external
conversation partners with incompatible response cadences. Token cost of such a probe
is substantially higher — designed only, not run.

### Watcher-flaw note (honesty item)

My completion watcher's file-count glob (`h[0-9]*`) matched the probe's intermediate
files, so it "completed" before `h7-tombstones.md` existed; the absorb-window
observation was unaffected (no layer existed to absorb), and DONE 7 arrived 2 minutes
later and was verified directly. Count finals, not prefixes, next time.
