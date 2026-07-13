# STRUCTURE — where tree shape actually comes from

**Author:** `structure-scout`, at the operator's request after three SPAN flood
probes failed to summon structure from load. Design only; no code; no
agent-spawning probes — this document is desk research over the swarm's own
recorded history plus the doctrine documents that shaped it. Written at
`main@63d1a79`, 2026-07-10, from a solo desk seat (no children — see §6).

**Evidence discipline**, as in SPAN.md: **VERIFIED** (I read the line / the
file), **MEASURED** (cites a field-evidence record with numbers), **REASONED**
(first-principles argument, could be wrong, falsifier named). Where the record
contradicts the operator's hypotheses or SPAN.md, that contradiction is named,
not smoothed.

---

## 0. The question, restated

Three flood probes (SPAN.md §6, `docs/audit/field-evidence-2026-07-10-span.md`)
tried to make a tree grow a coordinator layer under load, and none did — twice
the flood was absorbed by a rung below the tree (harness subagents), once by
one identity holding seven conversations. **Structure never grew from load in
any of the three trials.** Meanwhile, structure that nobody designed *did*
grow: `swarm ps` right now shows four standing arms — `field-tester`,
`hardener`, `updater`, `codex-scout` — next to twelve names in the `dead:`
line, every one of them a flood probe or its grandchild, closed within the
hour it was born. The operator's question: if not load, then what — and where,
in a system that stores only journals and tombstones, would that "what" leave
a mark anyone could read?

This document's method is to take the standing-vs-dead split as ground truth
and ask what actually separates the two columns, rather than asking which
theory sounds right first.

---

## 1. The dataset, exactly as it stands

**VERIFIED** — `swarm ps`, run at the start of this research:

```
operator — no waiting mail
├─ codex-scout [live] q=0 idle 15h
├─ field-tester [live] q=0 idle 1h
├─ hardener [live] q=0 idle 1h
├─ structure-scout (you) [live] q=0 idle ?
└─ updater [live] q=0 idle 2h
dead: deleg-after-1, deleg-base-1, deleg-heavy-after-1, deleg-heavy-base-1,
      dh1-concepts, dh1-flake, dh1-latency, dh1-refs, probe-a, span-after-1,
      span-base-1, span-heavy-1
```

**VERIFIED** — from `.swarm/journal/operator.md` (the coordinator's own
running record, 2026-07-09 through 2026-07-11) and the four standing agents'
journals, the dispatch history per arm:

| agent | spawned for | # of distinct dispatches after spawn | span |
|---|---|---|---|
| `field-tester` | dogfood WATCHLIST triggers | baseline+3 WATCHLIST tests (2026-07-09), delegation baseline+heavy (2 probes), delegation after ×2, SPAN baseline/after/heavy (3 more flood cycles) — **9 distinct measurement assignments**, each independently dispatched by the operator's journal | 2 days |
| `hardener` | port review tests | Task 1 (port tests) → Task 2 (naming defects) → Task 3 (queue-ownership sentence) → Task 4 (delegation doctrine) → Task 4 amendment → Task 5 (re-ring bound) → Task 6 (span doctrine) → Task 7 (queue narrowing) — **7 numbered Tasks**, sequentially dispatched | 2 days |
| `updater` | keep the install current | one initial brief ("keep current with origin/main, forever") → autonomous cycles triggered by its own Monitor, not by fresh operator dispatch | 2 days, ongoing |
| `codex-scout` | codex integration research | one brief, two probe rounds, two deliverables — **workstream is finished**; idle 15h awaiting the operator's decision on whether to build it | spawned once, never re-dispatched |
| 12 dead probes | one artifact each (a summary, a report, a flood measurement) | **1 dispatch each** — spawned, worked, reported, closed same session | under an hour |

**MEASURED** (`docs/audit/field-evidence-2026-07-10.md`,
`field-evidence-2026-07-10-span.md`) — every one of the 12 dead names was
itself an *instrument in an experiment*: a probe built to answer one
measurement question, whose entire reason for existing was to be closed the
moment its report file existed. `deleg-heavy-after-1` is the sharpest case: it
is a probe that itself spawned four grandchildren (`dh1-flake`,
`dh1-refs`, `dh1-concepts`, `dh1-latency`), verified each on harvest, and
closed all four *and itself* inside one session — the shortest full
grow-and-shrink cycle in the record, VERIFIED in its own journal tail
(`.swarm/journal/deleg-heavy-after-1.md`, 5 entries, all dated 2026-07-10
12:07Z–12:26Z).

---

## 2. Where structure actually comes from — three candidate explanations,
   tested against the table above

### 2a. Load (SPAN's bet) — REJECTED by the record

SPAN.md §1 argued attention-pressure at a node should force a coordinator
split. **MEASURED, three times, zero for three:** the flood always resolved
below the tree (harness subagents) or within one identity (interleaved
conversations), never by growing a coordinator (`field-evidence-2026-07-10-span.md`,
verdicts on falsifiers 1 and 1′, both "NOT FIRED" / "success shape NOT
OBSERVED"). Nothing in the standing-arm table above is explained by load
either: `hardener` never had more than one open Task at a time: each dispatch
in its journal begins "Idle, awaiting review or next dispatch" and ends with
the next Task landing only after the operator read the prior one — sequential,
not concurrent, load (VERIFIED, `.swarm/journal/hardener.md`, every entry ends
with an idle line before the next Task entry begins). **Structure in this
swarm has never once come from momentary attention pressure.** SPAN's
falsification stands; this document does not need to re-argue it, only note
that the standing-arm data independently confirms it from the opposite
direction — the arms that *do* stand were never under load either.

### 2b. Repetition of task SHAPE, addressed to a stable NAME — SUPPORTED,
   with a precise mechanism

The operator's hypothesis was repetition. The record supports a narrower
version of it: **it is not the count of tasks that makes an arm stand — it is
that the operator kept addressing the same open question to the same name
before that name's prior task was done being useful.** Concretely:

- `hardener` stood because the operator's own workflow generates a recurring
  *shape* of need — "a proven fix exists, someone must implement it in a
  worktree, off main" — and the cheapest way to get Task 2 done was to hand it
  to the agent that already knew the codebase's conventions from Task 1,
  rather than pay a fresh spawn's onboarding cost. This is VERIFIED directly
  in the operator's own words: Task 2's dispatch note reads "Dispatched to
  hardener (Task 2): defect 1…" — addressed by name, not spawned fresh
  (`.swarm/journal/operator.md`, 2026-07-09 entry two). The same pattern
  repeats for every one of hardener's 7 Tasks.
- `field-tester` stood on the identical mechanism for the measurement shape:
  "a doctrine change needs a before/after field measurement" recurred five
  times (WATCHLIST triggers, delegation cheap+heavy, SPAN cheap+heavy+flood),
  and every single time the operator dispatched to the *existing* name rather
  than spawning `field-tester-2`.
- The 12 dead probes never got this treatment because **they were never
  addressed twice.** Each was spawned by `field-tester` (their parent, not the
  operator) as a single-use instrument for one specific measurement, and
  `field-tester`'s own journal closes each one in the same reconciliation
  entry that reports its result. There was structurally no second dispatch
  coming — the shape of the task ("run this one flood and report") is
  complete in one round by construction.

**REASONED, with a falsifier already available in the record:** this is not
"repetition of work" in the abstract — SPAN's flood probes *were* repetitive
(9 near-identical summarization tasks in `span-base-1`) and that repetition
produced **zero** structure, because all 9 were addressed to one already-open
name in one burst, not addressed *across* separate closings-and-reopenings.
Repetition inside a single agent's queue is just backlog; it never earns a
new name. What earns persistence is repetition **across dispatches that could
each have gone to a fresh name but didn't**, because the operator (or a
parent) judged that re-addressing the standing name was cheaper than paying
onboarding again. This reframes the operator's hypothesis precisely: **the
structural signal is not "this kind of work keeps arriving" — it is "I, the
dispatcher, keep choosing to reuse this name."** That choice is the fact a
file can witness (§3).

### 2c. Standing triggers / watches (updater's shape) — SUPPORTED as a
   third, distinct mechanism

`updater` does not fit 2b at all: the operator dispatched to it **once**
(VERIFIED, `.swarm/journal/updater.md` entry 1, "Task from operator:… keep
the installed swarm tooling current… Watch via a run-in-background
fetch-and-compare loop"). Every subsequent action in its journal is
self-triggered by its own Monitor firing, not by a fresh operator message.
This is a different species of persistence from `hardener`/`field-tester`:
those two stand because a *dispatcher* keeps choosing them; `updater` stands
because its *brief itself* names an unbounded watch with no terminal state —
"keep current with origin/main" has no notion of "done." A probe cannot
accidentally acquire this shape; it must be spawned with it. This is the one
case in the record where standing structure was **designed in from the
brief**, not discovered by repetition after the fact.

### 2d. The null case that breaks a clean story: `codex-scout`

`codex-scout` is live at idle 15h with a **finished** workstream — both
deliverables written, reconciliation entry filed, "Going idle after
reporting to operator" (VERIFIED, `.swarm/journal/codex-scout.md`, final
entry). It was never re-dispatched (2b does not apply) and it was never
briefed as a watch (2c does not apply). It stands purely because **closing
costs an action nobody has taken yet** — the operator's own journal names
this explicitly: *"codex-scout close pends codex decision"*
(`.swarm/journal/operator.md`, 2026-07-11 entry "all six merged"). This is
important evidence against a naive reading of either hypothesis: **standing
is not always earned; sometimes it is just unclaimed idle time before a
close that hasn't happened.** Any design that infers "this name is
structurally important" from liveness alone will be fooled by this case. The
correct read of `codex-scout` is: a finished child with a decision pending
*on its output*, not a standing role. The distinguishing test (already latent
in the existing doctrine, WORLD concept 9 / SKILL.md point 2) is exactly
"can you name its next task" — and for `codex-scout` today, the honest
answer is no; its own report already said "going idle" — it is not the
operator's decision that keeps it, it is that nobody has run the harvest+close
step. **This is a small operational finding, not a theory point:**
`codex-scout` is a close overdue, not a fourth structural pattern.

---

## 3. Where would repetition be remembered? — the minimal surface

The brief asks for the smallest place "this work-shape has arrived N times"
could become noticeable, without counters, schemas, or a metrics engine. Three
candidates were offered; here is how each fares against §2's actual mechanism
(re-addressing a name, not raw task count):

**Candidate: a convention — "name the shape of the work you just routed," in
the parent's own reconcile entry.** This is not hypothetical: it is *already
the pattern operator.md exhibits*, unprompted, in every dispatch entry —
"Task 2 (naming defects)", "Task 5: re-ring bound", "SPAN test cycle
dispatched (Task 6)". The operator has been running exactly this convention
by hand for two days, without anyone naming it as a convention. **The
smallest fix is not a new mechanism — it is naming the existing habit as a
duty**, so it survives beyond this operator's personal style: *when
dispatching to a name you've dispatched to before, say so, and say what
recurred.* This is one sentence added where the reconcile duty already lives
(spawn_header / WORLD concept 9), costs zero new concepts, and the falsifier
is cheap: read ten consecutive dispatch entries in any coordinator's journal
and check whether a re-addressed name is ever dispatched to *without* a
"Task N" — style marker naming the recurrence. Today (VERIFIED): it never is,
in this swarm's whole record — the pattern already holds without being
required. That is unusually strong evidence *for* codifying it (§8: earn the
tooling only after the convention proves out — it already has, for two days,
unbriefed).

**Candidate: the tombstone record as a fossil record of shapes.** REASONED,
partially supported: `dead:` in `swarm ps` already lists every closed name,
and each has a journal (files survive close, VERIFIED WORLD.md concept 7).
In principle a reader could grep those twelve journals and notice "four of
these are named `dh1-*`, spawned in one burst by one parent, each doing a
qualitatively different single job" and reconstruct that a flood happened.
But this is expensive — it requires reading N journals to notice a pattern
that a two-line dispatch-log convention (above) would have made visible for
free, prospectively, in one file. The fossil record is real and worth
keeping (it already is kept, by construction), but it is a *forensic*
resource, not a *noticing* one: nobody reads twelve tombstones looking for a
pattern unless they already suspect one. **REASONED — rejected as the
primary surface, kept as corroboration.** Falsifier: if a future researcher
(like this document) needs to reconstruct a repetition pattern, measure
whether the dispatch-log convention (once adopted) makes that reconstruction
faster than tombstone-mining did here. (It did, for this very research — §1's
table came from one file, `operator.md`, in minutes; cross-referencing twelve
dead journals for the same picture took longer and would not have found the
`codex-scout` null case at all.)

**Candidate: the operator's desk.** REASONED: the desk (per SPAN §3c's
sketched skill section) is where *decisions* accumulate, not where *dispatch
shape* accumulates — its job is bounding what reaches the human (Philosophy
§9), not remembering what kind of work keeps recurring underneath. Repetition
of task shape happens one or two levels below the desk (`operator.md` is the
coordinator's journal, one hop down from the human operator's actual
attention); putting the noticing mechanism at the desk itself would put it
one layer too high to see the pattern before it has already produced 7 Tasks.
**Rejected as the primary surface** — the desk consumes the *output* of
noticing (a named recurring arm to address), it should not be where the
noticing first happens.

**Verdict on Q2:** the minimal surface is the **dispatcher's own reconcile
entry, at the moment of choosing to re-address an existing name** — which
this swarm has already been doing, unbriefed, for two days. The fix is not a
new place to remember; it is naming the remembering that is already
happening as a duty, so it is not this operator's personal habit but the
system's convention. Zero new files, zero new state, one sentence.

---

## 4. The two-regime hypothesis — operator-stable, sub-tree-fluid

**The record supports a version of this, but not for the reason the
hypothesis states.** The operator's framing was "a human needs standing
roles... because it wants a different structure than an agent harness." Read
literally, this is an over-analogy the record does not actually support:
`updater`'s standing-ness has nothing to do with being addressed by a human —
it stands because of its *brief's shape* (§2c), and it would stand exactly
the same way if its parent were another agent instead of the operator. Two
of the four standing arms (`hardener`, `field-tester`) are children *of the
operator*, but the mechanism that keeps them standing (§2b, re-addressing a
name) is not operator-specific either — `deleg-heavy-after-1`, a plain
agent, ran the identical spawn→verify→harvest→close cycle on its own
grandchildren with zero operator involvement, and did it *correctly and
eagerly* (closed all four the same session, VERIFIED §1). **Nothing in the
record shows agents needing MORE structure to run this loop than the human
operator does; if anything the agent ran it faster and more completely than
the human-facing arms have (which are still open, evidence of the human's
own slower reconciliation cadence, not the agent's).**

What the record *does* support, narrowly: the **cost of re-briefing** is
asymmetric between a human and an agent, and that asymmetry is real, not
cosplay (see §5). A human re-reading a stranger's journal to reconstruct
context pays in wall-clock minutes of scarce attention (Philosophy §9: "the
operator's attention is treated as the scarcest resource in the system —
scarcer than tokens"); an agent re-reading the same journal pays in tokens,
which this project has explicitly refused to optimize for (Philosophy §1:
"save the goal, not the context... context efficiency is a side effect,
never a thing it optimizes for"). So a human dispatcher has a *sharper*
incentive to reuse a warm name than an agent dispatcher does — not a
different *mechanism*, a different *slope on the same cost*. This is worth
stating precisely because it lets the answer to Q3 be smaller and more
honest than "two regimes":

**There is one mechanism (§2b: reuse a warm name when re-addressing a
recurring shape), and the operator sits at the steep end of its cost curve.**
No doctrine text needs to say "the operator is special" — it already isn't,
mechanically. What could usefully be said, if anything, is the numeric
default already offered in SPAN §3c ("ask the operator their span, default
~3") — which is about *bounding the human's simultaneous load*, a genuinely
different concern from *whether names persist*. Persistence-of-names and
bounded-span are two different knobs; SPAN already owns the second one
correctly-scoped; this document should not duplicate it under a
"two-regime" banner that implies a bigger split than the evidence shows.

**Smallest expression, if the operator still wants something written down
after reading this:** not a new regime, but a one-clause tightening of the
convention from §3 — *when a dispatcher is the human operator, the
name-reuse convention is not optional; a human should never be asked to
re-learn an agent's context they already paid for once.* That is a
half-sentence added to the SKILL.md coordinator doctrine's point 2
(reconciliation), not a new WORLD.md concept, not a new file. If the record
later shows agents ALSO suffering real harm from name-churn (a successor
agent measurably floundering despite reading a predecessor's journal — the
exact falsifier SPAN §3b already named for re-parenting), the clause
generalizes to everyone and the "two-regime" framing turns out to have been
right after all, just for a different reason than "humans are special": it
would be about relearning cost, universally, with the operator simply
hitting the threshold first because their reading is slowest. **REASONED;
falsifier: an agent successor's measurably degraded performance after a
close+respawn, vs. an equivalent-context warm reuse — untested, not run,
this document does not run agent probes.**

## 4b. Challenging SPAN.md directly

SPAN.md's model (§1) treated "attention bounded" as the single organizing
force and built a whole ladder (§3d′) to explain why load alone didn't
produce trees. The standing-arm data in this document shows a **structural
force SPAN never modeled at all: dispatcher-side name reuse**, which is
active in the record right now, growing real (if shallow) persistence, with
no flood, no span pressure, and no coordinator anywhere in sight. SPAN's
falsifiers 2 and 3 (forwarder coordinators, absorb-never-fires) stayed
UNTESTABLE after three floods because **SPAN was probing for a coordinator
layer that this swarm's actual structure-forming mechanism never needed** —
none of the four standing arms is a coordinator; all four are leaves the
operator or a peer kept re-addressing directly. SPAN is not wrong about what
it measured (load does not produce coordinators — confirmed independently
here), but its ladder implicitly treated "no coordinator" as "no
structure," when the record shows persistent flat structure forming by a
completely different mechanism the ladder doesn't have a rung for. **A
fifth rung belongs in the §3d′ ladder, cheaper than "swarm children" and
orthogonal to it: rung 0, *name reuse* — before any spawn decision, "is this
shape of work already owned by a warm name I should re-address instead of
spawning fresh?"** This is REASONED, not measured (no probe was run to
confirm agents actually make this check today versus defaulting to fresh
spawns) — see §7 suggestion 1 for the falsifier.

---

## 5. What does the human actually need that an agent doesn't? — unsentimental

Working through the brief's list against the record:

- **Continuity of names ("tell hardener…").** REAL, not cosplay. VERIFIED
  mechanically: `hardener`'s 7 Tasks were dispatched *by name* in
  `operator.md` every time — "Dispatched to hardener (Task 2)…" — because
  the operator (a human) cannot hold "which of my children already knows
  the naming-conventions codebase" as cheaply as re-reading a journal to
  find out. An agent dispatcher, shown in `deleg-heavy-after-1`, made the
  identical choice (reuse `dh1-flake`'s... no — actually it spawned *fresh*
  grandchildren every time, because each grandchild's job was a single
  closed-form measurement with no expectation of a second round). The
  difference is not that the agent doesn't value continuity — it's that
  **none of its dispatches were actually the recurring-shape case**; it
  never got the chance to demonstrate the preference either way. This
  weakens (not strengthens) the human-vs-agent framing: the record shows
  *task shape* driving the choice, and the operator's tasks happened to be
  the recurring ones. **REASONED — genuinely unresolved**, falsifier
  named in §4b.
- **Predictable mailbox rhythm.** REAL. Philosophy §9 quotes the operator
  demanding a clean channel — this is verified doctrine, not this
  document's inference, and it predates SPAN/STRUCTURE entirely. Nothing
  here adds to it; SPAN §3c's desk sketch already owns this correctly.
- **A desk that never exceeds declared span.** This is SPAN's territory
  (§3c), already correctly scoped there as a human-specific number ("this
  operator says ~3"). This document does not re-derive it; it is a
  genuinely different mechanism from name-persistence (§4) and should stay
  in SPAN, not migrate here.
- **Roles addressable without re-briefing.** This collapses into
  "continuity of names" above — same mechanism, same evidence.

**Unsentimental summary:** the record supports exactly one human-specific
fact — humans pay more per re-briefing than agents do, because their
attention (Philosophy §9) is scarcer than an agent's tokens (Philosophy §1)
— and one genuinely orthogonal, already-solved fact (bounded simultaneous
span, SPAN §3c). It does **not** support "operators need standing roles"
as a category distinct from "whoever keeps re-addressing a name benefits
from that name staying warm," because the one clean agent-dispatcher
example in the record (`deleg-heavy-after-1`) never repeated a name, so it
never tested the alternative. The honest state: **partially confirmed,
partially untested, no evidence of a categorical human/agent split** — only
a slope difference on one shared curve.

---

## 6. A note on this document's own span (the brief asked for this)

The brief said: "if you find yourself wanting children, that fact itself is
data for question 1." I did not. This task was one continuous read-and-write
workstream with no independently-progressable parts — the journals had to be
read in a specific order to build the table in §1 before §2's analysis could
be written, and the analysis itself is one argument, not N parallel ones. That
is exactly the "cheapest sufficient rung" the ladder (§3d′) predicts:
rung 1 (my own reads, done directly) sufficed because nothing here was
identity-demanding, long-running, or independently choosable. This is a
non-event, but the brief asked for it honestly: no want, no gap.

---

## 7. Suggestions, ranked

Each: smallest implementation, concept-count cost, falsifier, evidence that
would earn it. Per Philosophy §8, none of these should ship on this document
alone — they are convention-first proposals, instrument only where the
convention is shown (here) already working unbriefed.

### 1. Name the recurrence in the dispatch entry (codify existing habit)

**Smallest implementation:** one sentence added to the reconcile duty
(spawn_header and/or WORLD concept 9): *"When you dispatch to a name you have
dispatched to before, say what recurred, in the same entry — this is how
repeated shapes of work become visible to anyone reading your journal."*
**Concept-count cost:** zero new concepts, zero new files, zero new state —
this is a phrasing addition to an existing duty (journaling), the cheapest
class of change the design vocabulary has.
**Falsifier:** read ten consecutive dispatch entries from any coordinator's
journal after this ships; if a re-addressed name is dispatched to without
naming what recurred, the convention didn't take and should not be pushed
further (no instrument, no schema — just note the failure).
**Evidence that would earn it:** already present, per §3 — the operator has
been doing this unprompted, in writing, for two days, across two different
standing arms, without being told to. This is the strongest case in the
whole document: the convention already works; this suggestion is *naming*
it, not inventing it.

### 2. Add "name reuse" as rung 0 of the SPAN §3d′ ladder

**Smallest implementation:** one clause in SPAN.md §3d′ (once merged):
*"0. Before spawning fresh, ask: is this shape of work already owned by a
warm name I should re-address? Reuse is cheaper than any rung above it —
zero onboarding cost, an existing journal already primed."* No doctrine-text
change elsewhere; SPAN.md is unmerged, this is a same-document amendment.
**Concept-count cost:** zero — SPAN's ladder is prose, not a mechanism; this
adds one bullet to prose that already exists.
**Falsifier:** the next flood or repeated-shape probe field-tester runs
should show whether agents actually check for a reusable name before
spawning fresh, versus defaulting to fresh names out of habit — **this has
never been measured**, because every probe run so far (delegation, span ×3)
gave probes single-shot briefs with no prior warm name to reuse. Design a
probe where the SAME shape of task is dispatched twice to a fresh coordinator
that has a live, idle prior child capable of doing it — does it reuse or
respawn?
**Evidence that would earn it:** the falsifier probe above; not run by this
document (no agent-spawning probes, per brief). This is the single most
useful next measurement in this research thread.

### 3. Close `codex-scout` (operational, not structural — do now, costs nothing)

**Smallest implementation:** none — this is not a design change, it is an
overdue action. `codex-scout`'s own final journal entry already says "going
idle after reporting"; its workstream is finished; its only obstacle is a
pending operator decision on the design it delivered, not any further work
FROM codex-scout. Harvest (already done, by the operator reading its report)
and close.
**Concept-count cost:** zero.
**Falsifier:** if `codex-scout` is closed and the operator later wants a
follow-up on the CODEX design, that follow-up would need fresh context
anyway (the decision is the operator's, not codex-scout's continuing state)
— re-spawning costs nothing extra versus keeping it idle.
**Evidence that would earn it:** already complete; this is a correction to
this session's own tree, offered because judging a child's work means
judging whether it should still be a child (WORLD duties clause).

### 4. Do NOT build a repetition counter, schema, or metrics engine

**Smallest implementation:** none — explicitly reject this class of fix.
**Concept-count cost:** would be substantial (a stored count per task-shape,
a classifier for "is this the same shape as that," a place to persist it) —
exactly the "config wearing the costume of a fact" pattern SPAN §2 already
rejected for span numbers, and Philosophy §5 rejected for trigger-mode
fields. The dispatcher's own journal entry (#1 above) is strictly cheaper
and requires no shape-matching machinery at all — a human or agent reading
"Task 2 (naming defects)… Task 3…" already sees the count without anyone
having counted anything.
**Falsifier:** if suggestion #1's convention is tried and STILL fails to
make recurring shapes visible to a new reader (i.e., a future scout doing
this same research can't reconstruct §1's table from journals alone), that
is the trigger to reconsider — not before.
**Evidence that would earn it:** none exists; none should be sought until
#1's falsifier fires.

### 5. Do NOT adopt a categorical "operator regime vs. sub-tree regime" split

**Smallest implementation:** none — the record does not support a second
regime distinct from the one mechanism in §3/§4b. If the operator still
wants this in writing, the smallest true version is the half-sentence in
§4 ("a human should never be asked to re-learn context they already paid
for"), added to SKILL.md point 2 — NOT a new WORLD.md concept, NOT a
schema distinguishing "operator-children" from "other children."
**Concept-count cost:** zero for the minimal version; a full second regime
would cost at minimum one new classification (which nodes are
"operator-interface" vs not) that the record gives no clean way to draw
(`hardener` and `field-tester` are two hops from the human in some
dispatches, direct in others — the boundary is not the tree edge, it's
"who is doing the re-addressing," which is §3's mechanism, not a tree
position).
**Falsifier:** an agent-to-agent dispatcher demonstrably suffering from
name churn the way a human would (§4b's untested falsifier) would justify
promoting the half-sentence to a universal one — which would then dissolve
the "two regimes" framing entirely rather than confirm it, since the fix
would apply everywhere.
**Evidence that would earn it:** the same probe as suggestion #2 would
also settle this — one measurement answers both questions.

---

## 8. Summary of verdicts

1. **Where does structure come from?** Not load (SPAN's bet, independently
   re-falsified here). Not a designed mechanism at all, in this record —
   **dispatcher-side reuse of a warm name**, driven by re-briefing cost, is
   the only mechanism actually observed producing the standing/dead split,
   plus one distinct second mechanism (a brief with a built-in, terminus-free
   watch, `updater`'s shape). One name (`codex-scout`) is standing for
   neither reason — it is an uncompleted close, not structure.
2. **Where would repetition be remembered?** In the dispatcher's own
   reconcile/dispatch journal entry, at the moment of choosing to re-address
   a name — which this swarm has already been doing, unbriefed, for two
   days. The fix is naming a habit, not building a memory.
3. **Two-regime hypothesis?** Not supported as a categorical split. Supported
   as a slope difference on one shared cost curve (re-briefing cost), on
   which the human operator sits at the steep end because attention is
   scarcer than tokens (Philosophy §1, §9) — already-established doctrine,
   not new. If written down at all, one half-sentence, not a new regime.
4. **What does the human need that an agent doesn't?** One confirmed fact
   (steeper re-briefing cost), one already-solved orthogonal fact (bounded
   span, owned by SPAN), and no confirmed categorical need beyond those two.
5. **Suggestions:** name the recurrence (do it), add rung 0 to SPAN's ladder
   (do it, cheap), close codex-scout (do it, free), do not build a counter,
   do not build a second regime.

**What would most cheaply move any of this from REASONED to MEASURED:** one
field-tester probe, not run here — dispatch the same task shape twice to a
fresh coordinator holding one idle prior child capable of doing it, and watch
whether it reuses the name or spawns fresh. That single probe settles
suggestion #2, and by extension gives real evidence for or against §4b and
§4's slope-not-regime claim, for the price of one probe pair — cheaper than
any of the three SPAN floods, because it does not need a burst at all, only
a second dispatch.
