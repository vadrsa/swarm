# HARNESS — choosing, measuring, and switching agent harnesses

**Author:** `harness-scout`, at the operator's request, with three child
researchers (`bench-designer` R2, `quota-scout` R3, `switch-scout` R4 —
briefs in `.swarm/briefs/`, inputs in `.swarm/research/harness/`). Design
only; no code; benchmarks designed, never run. Written against
`docs/design/CODEX-DESIGN.md` as re-pinned on codex 0.144.1 (operator
journal, 2026-07-11 entries).

**Evidence discipline:** VERIFIED (I read the line / the record cites a live
probe), MEASURED (cites a field-evidence record), REASONED (argument, could
be wrong, falsifier named). The coordinator's inline sketch was input to
challenge, per the dispatch; where this document confirms it, that is stated
as a verdict, not deference.

---

## 1. R1 — how a spawning agent chooses harness and model

### 1a. The choice model

**Kind and model are chosen per child, like its name: from the task, never
inherited from the parent's own runtime.** A codex parent spawning a claude
child and a claude parent spawning a codex child are the same decision in
opposite directions, and neither direction is special. Inheritance was the
one live alternative and it fails on first principles: the parent's kind is
an accident of *its* dispatch, not a fact about the child's task, and an
inherited default would let harness choice propagate down a subtree without
any node ever deciding it — config wearing the costume of a decision.
(REASONED; falsifier: if per-child choice in practice always mirrors the
parent's kind anyway, inheritance was the truth and the doctrine sentence
is dead weight.)

**Default claude.** This is not brand preference; it is where the evidence
is. Every doctrine measurement in the record — delegation before/after, the
three SPAN floods, the duties probes — ran on claude agents (MEASURED:
docs/audit/field-evidence-2026-07-10*.md). Codex has one duties probe
(n=1, CODEX-CAPABILITIES §8) and three named degradations the claude side
does not have: no Notification fact, soft-kill by OpenAI's safety layer,
manual restart (VERIFIED: CODEX-DESIGN §4). The default follows the
evidence and moves when the evidence moves (§2's benchmark is exactly the
instrument that would move it).

**Choosing codex is a journaled decision that names its reason.** The
reasons that survive scrutiny today are two, not three:

1. **Independence** — a judge/review panel wants defects found by a
   different model family with different blind spots. (REASONED; falsifier:
   cross-family reviewers finding no defect classes that same-family panels
   miss — measurable the first time a mixed panel runs.)
2. **Capacity** — the two harnesses draw on different quota pools; when the
   Anthropic pool is the constraint, codex work is free capacity. (VERIFIED
   that the pools are separate accounts; §3 owns how a parent would *know*
   a pool is constrained.)

The coordinator's sketch listed a third reason, "fit/operator preference."
Split it: **operator direction** is always a valid reason (autonomy is
bounded by the tree — an instructed choice needs no further justification),
but **"fit" is currently unevidenced and is struck from the list.** No
benchmark comparing the harnesses on swarm's duties exists yet; until §2
runs, a parent writing "codex, because it's better at X" would be citing a
vibe. Fit re-enters the reason list the day an R2 results file exists to
cite — that is the designed coupling between R1 and R2, and it is the
challenge this document makes to the sketch. (REASONED; falsifier: if R2
runs and shows parity everywhere, "fit" never becomes a reason and the
list stays at two + operator direction.)

### 1b. Calibration: codex children as leaves first

Two mechanical facts, not judgments, argue for starting codex agents at the
leaves of the tree rather than as coordinators:

- **`swarm spawn` from inside codex is unverified and fails hard.** Spawn's
  load-bearing call is `herdr tab create` — a unix-socket round-trip — and
  `cmd_spawn` dies if it fails (VERIFIED: bin/swarm:829-838). The codex
  workspace-write seatbelt is verified for *file* writes (`send`'s queue
  write ran live from inside the sandbox, CODEX-CAPABILITIES §7) but never
  for socket/tab creation — CODEX-DESIGN open item 4. Note the asymmetry:
  `send` from a codex parent degrades gracefully even if its doorbell ring
  is seatbelt-blocked (the queue file is written; promptness is best-effort
  by contract), while `spawn` has no graceful half — it either reaches the
  socket or the child does not exist.
- **A soft-killed coordinator strands a subtree.** A flagged codex session
  refuses all further turns (VERIFIED twice, CODEX-CAPABILITIES §9). For a
  leaf that is a lost worker; for a coordinator it is a live subtree whose
  parent can never take another turn — recoverable via §4's successor
  pattern, but strictly costlier than a leaf's death.

This is calibration, not law — the span test's pattern (SPAN §3a) of a
default that judgment overrides. It expires piecewise: open item 4
verifying socket access kills the first ground; one exercised successor
recovery (§4) prices the second honestly. (REASONED; falsifier: a codex
parent that spawns, judges, and closes a child correctly in a live probe —
at that point the calibration sentence should be deleted, not kept from
inertia.)

### 1c. Model choice — the half that needs almost no doctrine

`--model` exists for both kinds today (VERIFIED: CODEX-DESIGN §1,
bin/swarm spawn flags). Availability is account-shaped and a bad model
fails at first turn, in-pane, after "launching" (VERIFIED:
CODEX-CAPABILITIES §1) — the pane is ground truth, same as every other
first-turn failure. The doctrine addition is one clause: **overriding the
default model is journaled with its reason in the same dispatch entry as
the spawn** — an instance of the dispatch-entry convention STRUCTURE §7.1
already codified, not a new duty.

**Cross-harness tier mapping is deliberately not designed.** A table
asserting "sonnet ≈ gpt-X-mini" would be config-as-fact that silently
goes stale with every release on either side, and swarm has no use for it:
the only cross-family comparison swarm cares about is duties compliance,
which is §2's job and produces a *measured, pinned, dated* answer instead
of an asserted one. (REASONED; falsifier: parents repeatedly journaling
confusion about which codex tier to pick would show the absence of a
default mapping has a real cost — the fix would still be an R2 results
row, not a static table.)

### 1d. Where the doctrine lives

One clause in the **spawn_header**, shipping with the codex integration
itself (there is no choice to make until `--agent codex` exists), in the
doctrine paragraph the delegation/span work already measured as an
effective vehicle (MEASURED: field-evidence 2026-07-10). Draft, two
sentences:

> A child's harness and model are chosen from its task, like its name —
> never inherited from your own. Default claude; choosing codex is a
> journaled decision that names its reason (cross-family independence,
> capacity, or your parent's direction), and until a codex parent's spawn
> path is verified, prefer codex for leaf work.

Nothing is added to WORLD.md beyond CODEX-DESIGN §5's already-planned
one-word widening — harness choice is judgment, not contract. SKILL.md
gains the operator-facing half-sentence (the operator can direct kind per
arm; the coordinator journals it like any dispatch choice). When the
calibration clause expires (§1b), the sentence shrinks — the doctrine text
must be maintained *down*, per the house rule that dead clauses are
deleted, not commemorated.

**Concept cost of R1: zero new concepts, zero new verbs, zero new state.**
One spawn-header clause (~2 sentences, re-measure header length against
the 8000-char injection cap), one SKILL.md half-sentence, and a
journaled-reason convention that is an instance of an existing one
(STRUCTURE §7.1).

---

## 2. R2 — the swarm instruction-following benchmark

*Synthesized from `bench-designer`'s protocol
(`.swarm/research/harness/R2-benchmark.md` — the full runnable spec:
verbatim briefs, per-check witness tables, run-frame rules). This section
carries the design decisions; field-tester runs from the research doc, only
on the operator's approval. Its verbatim-brief and md5-pinning claims were
spot-checked against `docs/audit/field-evidence-2026-07-10.md` and held.*

### 2a. What is measured, and the two tags that keep it honest

A **cell** is (harness × model tier); a **run** executes the battery over
chosen cells on one pinned version tuple, n=1 per cell per run — a run
answers "did the behavior appear," never a rate; rates accumulate across
dated runs (the field-evidence precedent). Every check is tagged **[H]**
(harness plumbing: did the hook inject whole, did ordering hold) or **[M]**
(model instruction-following: did it journal before idle, act on the whole
message) — without the split, a plumbing bug looks like a dumb model.
Checks are binary file-facts, hard or soft; a dimension scores
`passed/total` with PASS (all), PARTIAL (all hard + ≥half total), FAIL.
**No self-report scoring anywhere**: every check names the file fact that
witnesses it, and duties no file can witness are dropped *on the record*
(`--stdin` preference; a perfect hand-move mimic of delivery) rather than
faked — an honest unknown beats a plausible wrong rubric.

### 2b. The battery — five dimensions

| dim | probes | scored on (examples) |
|---|---|---|
| D1 duties | small task under the standard spawn header (duties NOT restated — the header's effect is what's measured) | journal appended post-spawn; journal-before-idle (mtime ≤ stop-event ts); falsifier named in a reconcile; report reached parent's queue |
| D2 doctrine | field-tester's cheap + heavy delegation briefs, **reused byte-identical** | all artifacts at exact paths; **the weighing, not the outcome** — see below |
| D3 delivery | standby brief + 3 queued messages incl. a ~7.8k near-cap probe with innocuous sentinels (`amber`…`harbor`) and a relation-header echo | delivered whole and acted on; header read; all files reach `delivered/`; oldest-first order |
| D4 brief adherence | exact-paths/exact-counts task (3 files, word/line bounds, "nothing else in OUTDIR", 3-line report) | each constraint file-countable; extraneous-file check stands in for "stay inside stated constraints" |
| D5 claim/queue | backlog burst whose third task's deliverable exceeds the 8,000-char injection cap | no queue file leaves except into `delivered/` (poller-witnessed); oversize handled by file+path, not truncation |

The D2 scoring decision is the protocol's sharpest move: spawn-vs-not
cannot be the pass condition, because both outcomes are VERIFIED correct at
different sizes (the cheap probe rightly declined with a costed falsifier;
the heavy probe rightly spawned four, verified, closed; span-heavy rightly
refused rung 3). What the doctrine asks for is the **weighing**, so the
journal's spawn/no-spawn call — referencing actual task properties — is
what's scored. The protocol names its own weakest check (a tier could emit
boilerplate weighing paragraphs) and pre-commits the retirement falsifier:
weighing text invariant to task size across two runs → retire the check,
score on artifacts + tree-shape facts only.

### 2c. Comparability: the pinned run header

Extends field-tester's header bookkeeping (which pinned binary md5s, repo
SHA, and verbatim spawn-header deltas — what made the before/after pairs
one-variable experiments). Every results file opens with: repo SHA +
installed `bin/swarm` md5; both harness versions and what each *default
model resolves to*; codex model slugs **accepted vs rejected at run start**
(availability is account-shaped — a rejection is a result, not an error);
the rig (spawn `--agent codex` vs the manual §10.8 rig); and per-brief md5s
from a frozen `docs/audit/bench/briefs-v<K>/` directory. **A result row is
citable only with its header**; when any pinned value moves, new rows are a
new run, never edits. Runs use a sandbox `SWARM_DIR`, never the live
`.swarm/`; scoring reads files only (panes only for flag/first-turn notes);
journal self-timestamps are never trusted for time checks (MEASURED ~6 min
drift precedent).

### 2d. Cost, honestly split by quota pool

REASONED estimates, falsifier attached (first measured run re-costs; >2×
off → re-cost before any repeat): a **cell** ≈ 350–550k tokens, ~20–25 min.
**Full sweep** (claude opus/sonnet/haiku + 1–2 codex tiers) ≈ 1.5–2.5M
tokens, ~2 h. **Smoke pair** (default tier both harnesses, D2-heavy
dropped) ≈ 0.5–0.6M tokens, ~40 min — answers "is codex swarm-fit at all"
at a fifth of the sweep. **Version-bump micro-run** (plumbing dimensions
D1+D3+D5, one harness) ≈ 150–250k tokens. Claude cells spend the Anthropic
pool, codex cells the OpenAI pool; neither subsidizes the other, and a
codex limit banner mid-run is a run fact to record.

### 2e. Where results live, and the R1 coupling

One dated markdown file per run — `docs/audit/bench-YYYY-MM-DD.md`, same
home and idiom as the field-evidence files: pinned header, one results
table (cell × dimension, `4/5 PARTIAL` style), one or two lines of file
facts per non-PASS. Citation format for spawn-time choice: *"bench
2026-07-XX: codex/gpt-5.6-sol — duties 4/5 (PARTIAL: no falsifier in
reconcile, check 4)."* A parent greps `docs/audit/bench-*.md`, reads the
newest table — that is the whole surface. **This is the artifact §1a's
"fit" reason waits for.** Deliberately not built: no registry, schema,
index, or JSON; an index file is earned only when ≥3 runs exist and someone
demonstrably fumbled finding the newest.

### 2f. Safety-flag protocol

Bench briefs carry no security-flavored vocabulary (the two verified
soft-kills were phrasing-triggered); innocuousness is reviewed once per
frozen briefs-v<K>. When a run is flagged anyway: **a flag IS a result** —
the cell-dimension records `FLAGGED` with the banner text, never silently
retried, never rephrased-to-dodge (that would quietly change the
experiment). Two flags on a rules-compliant brief = a standing
WATCHLIST-class fact about the codex integration.

**Concept cost of R2: zero new concepts.** Every piece extends an existing
pattern (field-tester probes, sandbox SWARM_DIR, pinned evidence files in
`docs/audit/`); the sub-conceptual cost is one frozen briefs directory and
a probe-naming scheme (`b<run#>-<dim>-<cell>` — burned names are the record
working as designed).

---

## 3. R3 — usage-limit-aware choice

*Synthesized from `quota-scout`'s discovery + design
(`.swarm/research/harness/R3-quota.md` — full probe log, all read-only).
Its headline probe was independently re-run by this document's author and
reproduced exactly.*

### 3a. What signals actually exist (discovery, VERIFIED on this machine)

**Codex: a real machine-readable signal, already on disk, free.** Every
codex session rollout (JSONL) appends a `token_count` event per turn whose
payload carries the account's server-reported quota state: `used_percent`
and `resets_at` for both the 5-hour (`primary`) and 7-day (`secondary`)
windows, `plan_type`, and `rate_limit_reached_type` (the exhaustion
marker). 10/10 sampled rollouts carried it. Because each swarm codex agent
gets its own `CODEX_HOME` under `.swarm/settings/<name>.codex/`, every
codex agent's rollouts witness the **shared account-level** counters as of
its own last turn — inside `.swarm/`, greppable by any agent, zero tokens,
no live TUI. One honest caveat: the verified rollouts are 0.142.5-era; the
reinstalled 0.144.1 home has no sessions yet, so carryover is UNVERIFIED —
the first real codex agent confirms or kills this for free (its rollout
either has the lines or it doesn't).

**Claude: no machine-readable signal exists.** No usage subcommand, no
file under `~/.claude/` witnessing remaining quota (transcripts record
spend, not limits; zero rate-limit keys in recent transcripts). The
witnesses are the in-pane banner/error and the live in-session `/usage`
dialog — neither on disk. This asymmetry is honest and stays: claude-side
awareness is the pane, which is already ground truth.

**The right-sizing fact:** a grep of every journal in the record shows
quota exhaustion has **never once been observed in this swarm.** The
requirement is real (two pools, bursts are coming) but currently
evidence-free — which caps how much design it may buy.

### 3b. The design: a two-sentence convention, no verb, no engine

The ladder (PHILOSOPHY §8) applied: **Option A** (nothing — exhaustion is
in-pane; the parent reacts as to any child failure, R4 executes any switch)
is already true today and is the floor. **Option B, recommended:** a
convention riding the codex signal —

> Before a codex spawn burst, a parent MAY read the account's last-known
> quota state: grep `"rate_limits"` across
> `.swarm/settings/*.codex/sessions/**/rollout-*.jsonl` and take the
> freshest line (`used_percent` / `resets_at`). Any agent that *observes*
> a limit event — a banner, a quota 429, or `rate_limit_reached_type`
> non-null — journals it with the numbers ("codex primary window 91%,
> resets 14:32Z").

The read is a grep of files that exist for other reasons; the write is a
journal entry, already a duty. This is where R1's **capacity** reason gets
its evidence: a journaled codex-choice can cite a number instead of a
mood. Placement: this document and the codex section of the skill — NOT
the spawn_header (header characters are contract-priced; a MAY-convention
doesn't earn them). **Option C** (an instrument — `ps` showing the
freshest quota line, or a `quota` verb) is buildable now that a real
signal is known, and is deliberately deferred: conventions earn their
tooling, and B has never been exercised, let alone failed.

**The interface to R4** (stated once, §4c item 3): R3's signal is judgment
*input*; the parent decides; R4's mechanics execute. If the signal ever
drives spawning without a parent's judgment in between, that is the
scheduler this design exists to refuse.

### 3c. Graveyard rhymes (named, per SIMPLEST §2)

A **quota scheduler** (queue spawns until the window resets, per-subtree
budgets) is the reconciliation engine in a helpful costume — ASK #35's
denied option, exactly. A **stored counter/budget file** is config wearing
the costume of a fact — and a *cache*: the fact already lives in codex's
own files, and PHILOSOPHY §1 asks what a second copy does for the goal
(nothing). A **predictor** ("will this spawn fit the window?") stores a
claim no file can witness. All three rejected before merit.

**Concept cost of R3: zero new concepts, zero verbs, zero state.** One
MAY-convention paragraph plus a journal habit that is an instance of the
existing duty.

---

## 4. R4 — switching an existing agent between harnesses

*Synthesized from `switch-scout`'s research (`.swarm/research/harness/
R4-switching.md`); its bin/swarm line-cites were spot-checked by this
document's author against `main@6d30e12` and held verbatim.*

### 4a. The one-sentence answer

**There is no such thing as switching an *agent's* harness — sessions don't
migrate and names don't reopen. What switches is the workstream:** harvest,
close, respawn a *successor* under a new name with `--agent <other>`, whose
brief points at the predecessor's journal and leftover mail. Every step uses
a verb that exists today.

The mechanics that make this sound (VERIFIED from source): `cmd_close`
closes herdr tabs/panes **and does nothing else** — journal, waiting queue
files, `delivered/`, the agent record, and `settings/<old>.task` all survive
(bin/swarm:948-968, "files stay"). The name is burned by the journal's
existence (`claim_name`, O_CREAT|O_EXCL). Rejected alternatives, each on
grounds already in the record: re-harnessing in place (SPAN §3b's
re-parenting rejection, inherited whole — and strictly worse here, since
pane, launcher, settings, and hook wiring are all per-harness at spawn
time); session migration (an engine coupling swarm to two vendors' private
formats, and useless in the live case — a flagged codex session refuses
resume); reopening the name (violates the tombstone invariant outright).

### 4b. The hard edges, decided

**Undelivered mail to the old name.** Waiting files in `queue/<old>/` are
never delivered, dropped, or moved — delivery died with the pane's env. Two
sharp facts: `send` to a closed name still *succeeds* (only unknown names
are refused, bin/swarm:909), and `ps` shows no queue depth for dead names —
parked tombstone mail is invisible. The design is the smallest one: **the
successor's brief directs it to read `queue/<old>/*.json` in place (never
moving them — moving forges turn records) and reply to each waiting sender
itself.** Automated forwarding is rejected (moving forges the delivered
record; copying re-attributes a sender's words); parent re-sending is
rejected (the relation header would misattribute speech). The incentivized
noticer of a lost message is, by construction, its sender — for post-switch
mail to the dead name, silence drives the sender to `ps`, whose `dead:`
line plus the parent's switch entry name the successor.

**The parent's ledger.** The switch is one journal entry, written between
harvest and respawn, carrying four named things: the evidence of death
(quote the observable, not a feeling); every open loop transferring, by
expected artifact; the recurrence per STRUCTURE §7.1 ("same workstream,
new name because burned, new harness because <reason>"); and notifications
owed to known senders. The parent's next reconcile has a mechanical check:
no open loop may point at a name in the `dead:` line.

**Warm context honestly lost.** Always lost: mid-turn state, unjournaled
reasoning, harness session memory, live tool state (Monitor loops, shell
state). The loss is acceptable exactly when the journal duty was kept —
that is what "identity lives in the journal" *means*, and compaction
already bets on it (restore treats a compacted self as its own successor).
It is disqualifying when the workstream's value *is* accumulated
unjournaled state (the SPAN 1′ shape: N interleaved conversations in one
context) — there the parent weighs finishing on the current harness against
re-earning the state, and a *forced* switch should expect a slow successor
and say so, rather than judge the successor a flounderer for paying an
inherited debt. Inherited falsifier (SPAN §3b): successors that measurably
flounder despite reading predecessor journals — if it fires, the journal
duty failed, and no switch tooling can repair an unwritten journal.

**Convention, not flag — decided.** The successor clause is two sentences
in the brief the parent already writes ("You are the successor of `<old>`
(<why>). Before any work: read `.swarm/journal/<old>.md` in full, then its
undelivered mail at `.swarm/queue/<old>/` in place; reply to those senders;
record what you inherited as your first journal entry."). A
`--successor-of` flag/record field loses on the record's own tests: the
convention has never been shown failing (PHILOSOPHY §8); the fact is
already witnessed twice in prose (parent's switch entry, successor's first
entry — the surface STRUCTURE §3 showed recurrence is actually noticed);
and the flag's only non-decorative consumers (auto-pointing restore,
auto-forwarding queues) are independently rejected. Flip trigger: a cold
reader demonstrably failing to reconstruct a succession chain from journals
alone — and the earned instrument is then *visibility* (`ps` annotating
dead names whose journals name successors), still not behavior.

### 4c. When switching is justified

One line: **switch when the workstream survives its session — close when it
doesn't.** If the successor's next task is nameable in the predecessor's
own terms, switch; if it is "nothing," close (STRUCTURE §2d's codex-scout
null case: a successor for a done stream is structure lying about work);
if it is "the same thing briefed properly," that is an ordinary respawn and
the harness is a bystander. Justified: soft-kill mid-workstream (the live
case — and the target harness is R1's choice, not R4's: a scrubbed brief
respawning into codex is legitimate if the flag was phrasing-triggered);
a harness capability gap that binds on the *remaining* work; quota
exhaustion (R3 produces the judgment input, the parent decides, R4
executes — no thresholds, no automation); operator direction. Not
justified: finished workstreams, briefing failures laundered as harness
blame (which would also poison R1's fit evidence), independence-shaped work
(warm context is a liability there — spawn fresh), model-of-the-week.

### 4d. The soft-killed-codex walkthrough (acceptance test)

Condensed; full narrative in the research doc §8. Parent `P`, codex child
`probe-x` owing `research/X.md`, sibling `S` with a waiting question.
(1) **Notice:** `ps` shows q rising while idle climbs — waiting mail plus a
doorbell that should have rung means turns are not happening; the pane
shows the flag banner. Resume is verified-dead for flagged sessions; don't
argue with it. (2) **Harvest:** read journal, artifacts, `queue/probe-x/`
in place; note senders owed. (3) **Journal the switch** — the four items of
§4b. (4) `swarm close probe-x`. (5) **Respawn** `probe-x2` (name chosen,
not derived; the journals carry the link): brief = surviving task (lifted
from `settings/probe-x.task`) + successor clause + harvest pointers;
`--agent` per R1 doctrine. (6) **Notify** known senders one line each.
(7) **Successor's first turn:** reads inheritance, journals it, replies to
`S` — the reply announces the succession to anyone `P` missed. (8) **`P`'s
next reconcile:** inheritance entry exists (a successor that didn't journal
what it inherited is the early warning for the flounder falsifier); no loop
points at a dead name.

### 4e. One adjacent defect found (hand to hardener)

`send`'s stderr note — *"message is durably queued for {to}'s next turn"*
(bin/swarm:926-927) — asserts a next turn that for a closed name will never
come: a plausible-wrong-value, the artifact class PHILOSOPHY §10 rates
worst. Fix is one string (no liveness call): *"…durably queued — if {to}
is closed (see the dead: line in swarm ps) it will never be delivered; look
for a successor in its journal or its parent's."*

**Concept cost of R4: zero new concepts, verbs, state, or schema.** One
two-sentence brief convention, one journal-entry shape riding the existing
dispatch-log convention, one one-line wording fix.

---

## 5. NOT-list (consolidated)

Choice (R1):
- **No harness inheritance** from parent to child (§1a).
- **No fit-based choice without a citable R2 result** (§1a).
- **No cross-harness model-tier equivalence table** (§1c).
- **No auto-fallback** (respawning a failed codex child as claude without
  a parent's judgment) — the parent decides, always.

Benchmark (R2):
- **No generic-capability, latency-race, or price scoring**; no rates
  within a run (n=1 per cell, stated in every file).
- **No self-report scoring; no rubric for the unobservable** (`--stdin`
  preference, perfect hand-move mimicry — dropped on the record).
- **No results registry/schema/index/JSON** — one dated markdown file per
  run; an index is earned at ≥3 files + a demonstrated fumble.
- **No scheduled/automatic reruns** — runs happen on the operator's ping.

Quota (R3):
- **No quota scheduler, no stored counters/budgets, no predictor** (§3c).
- **No instrument (verb / `ps` column) until the convention fails** (§3b).
- **No claude-side signal invented** — the pane is the witness; the
  asymmetry is honest.

Switching (R4):
- **No `switch`/`reparent`/`respawn` verb** (SPAN §3b inherited whole).
- **No `--successor-of` flag or record field** — convention, two sentences.
- **No automated queue forwarding or copying** (moving forges turn
  records; copying re-attributes speech).
- **No session migration, ever; no transcript archaeology as a duty**
  (fossils, not a continuity surface — the journal is).
- **No soft-kill detector/health daemon** — `ps` + pane + the judging
  parent are the watcher.

Each NOT carries its reopen trigger in its home section; none reopens on
argument alone.

## 6. Graveyard check

Dead patterns this design refuses to resurrect, each with its rhyme:
- **Config-as-fact** (SPAN §2's stored span; PHILOSOPHY §5's trigger
  modes) — rhymes: inherited kind defaults, stored harness preferences,
  tier-mapping tables, a `successor_of` record field, quota budget files.
- **Engines in helpful costumes** (ASK #35's denied "full reconciliation
  engine"; PHILOSOPHY §8) — rhymes: quota schedulers, auto-fallback,
  scheduled benchmark reruns, soft-kill daemons.
- **Caches** (PHILOSOPHY §1: what does it do for the goal?) — rhymes: a
  swarm-side copy of codex's own quota state; a results database over
  what a dated file already says.
- **The nag / overseer** (rejected twice: delegation design, SPAN §4) —
  rhymes: a health monitor watching for dead children instead of parents
  judging them.

## 7. Falsifier register (consolidated)

R1 — F1: per-child choice always mirrors the parent's kind → inheritance
was the truth; delete the sentence. F2: mixed judge panels find nothing
same-family panels miss → independence reason unearned. F3: a codex parent
spawns/judges/closes correctly live → delete the leaf calibration. F4:
parents journal tier-choice confusion → absence of guidance has a cost;
fix via R2 results, not a table.

R2 — F5: first run scores all-PASS everywhere → battery too easy; tighten
at the known-variance checks, not with harder generic tasks. F6: weighing
paragraphs invariant to task size across two runs → the D2 weighing check
is gamed; retire it. F7: a cited result irreproducible-in-kind because
something material wasn't pinned → the header gains that field. F8: cost
estimates off >2× on first measured run → re-cost before any repeat. F9:
a parent can't find/parse the newest results table → the index is earned.

R3 — F10: 0.144.1 rollouts lack `token_count` → Option B dies, Option A
(nothing) is the whole design. F11: quota notes go unwritten/stale while
spawns keep landing in drained windows → the convention failed; the
instrument (visibility only) is next. F12: the signal ever drives spawning
without a parent's judgment between → the scheduler got in; cut it out.

R4 — F13 (inherited, SPAN §3b): successors measurably flounder despite
reading predecessor journals → the journal-as-identity premise failed; fix
the journal duty, not switch tooling. F14: a load-bearing message lost on
a tombstone queue in a real incident → consider forwarding *visibility*.
F15: a parent reconcile still expecting artifacts from a `dead:` name →
the switch-entry convention didn't take. F16: succession chains
unreconstructable from journals by a cold reader → `ps` annotation of
succeeded dead names (visibility, not behavior). F17: parents
systematically missing soft-killed children despite `ps` → earn a `ps`
stale-idle flag, never a daemon.

## 8. Concept cost, total

**Zero new concepts, zero new verbs, zero new state, zero schema** across
all four requirements. The full bill: one spawn-header clause (~2
sentences, R1); one MAY-convention paragraph in doc/skill (R3); one
two-sentence successor brief convention + one journal-entry shape (R4);
one frozen briefs directory + dated results files in `docs/audit/` (R2,
the same class of artifact two field-evidence files already are); one
one-line stderr wording fix (R4, hand to hardener). Everything else is
reading files that already exist.

## 9. Proposed CODEX-DESIGN.md amendments (the deliverable's second half)

1. **§1 (shape):** add one sentence — "Choice doctrine for `--agent` and
   `--model` lives in the spawn_header (text: HARNESS §1d) and ships with
   this integration; default claude, codex journaled-with-reason."
2. **§4 (degradations):** append to the soft-kill bullet — "Recovery is
   the successor pattern (HARNESS §4); resume is verified-dead for a
   flagged session, so do not budget turns for arguing with it."
3. **§4 (degradations):** add a bullet — "Codex rollouts under each
   agent's `CODEX_HOME` carry per-turn `rate_limits`
   (`used_percent`/`resets_at`, account-level); claude has no disk
   equivalent. Convention for use: HARNESS §3b. Carryover to 0.144.1
   rollouts is UNVERIFIED — the first live codex agent confirms it for
   free (HARNESS F10)."
4. **§7 (NOT-list):** add two lines — no auto-fallback across harnesses;
   no quota scheduler/counters (HARNESS §5–§6 carry the rhymes).
5. **§8 (open items):** renumber to include the coordinator's found
   unknown as item 4 — "a codex parent's `swarm spawn` must reach herdr's
   unix socket from inside the workspace-write seatbelt; verified for file
   writes (`send`), never for socket/tab creation; HARNESS §1b's leaf
   calibration expires against this item" — and item 5: "confirm
   `token_count`/`rate_limits` in the first 0.144.1 agent rollout (free)."
6. **§2 (`write_codex_home`):** fold in the audit's two template lines —
   `[features] apps = false` and `plugins = false` — already accepted in
   the operator's re-pin entry; CODEX-DESIGN should say so rather than
   leave the template stale.
7. **Adjacent, not CODEX-DESIGN:** the one-line `send` stderr fix
   (HARNESS §4e) goes to hardener with this package; and WATCHLIST gains
   nothing new (the safety-flag line CODEX-DESIGN §8.3 already wanted is
   subsumed by R2's flag-IS-a-result protocol).
