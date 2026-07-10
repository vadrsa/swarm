# SPAN — attention caps and emergent rebalancing, the simplest thing that is true

**Author:** the coordinator (Fable), at the operator's request: *"I don't want to
manage 100 agents, I want to manage x (maybe for me it's max 3)… same goes for any
agent in the tree that has delegations… I want an emergent behavior for rebalancing
management."* Written at `main@63d1a79` (v1.0.0), 2026-07-11. Design only; no code.

**Evidence discipline:** claims tagged **VERIFIED** (I read the line / the record),
**MEASURED** (cites the field-evidence records), or **REASONED** (first-principles
argument, could be wrong, falsifier named). The operator's own warning is a design
input: *"sensitive to over-analogisation to real world where it shouldn't"* — §5 is
the register of what transfers from human organizations and what must not.

---

## 1. The problem, stated in agent-native terms

Every parent in the tree — the human operator included — judges its children by
reading their work. That is the whole quality gate: the system deliberately stores
no compliance state (VERIFIED: WORLD.md §8, "judge artifacts, never claims"), so
**the parent's actual reading is the only thing standing between the swarm and
obedience theater.** Reading is expensive. Attention is therefore the scarce
resource of this design — not compute, not agents, not messages.

Three agent-native facts bound a parent's span. None of them is an org-chart
analogy:

1. **Context is finite.** A parent holding N children must hold N briefs, N
   trajectories, and the judgment state of N workstreams. Past some N, reads
   degrade into skims. A skim that moves work along is *worse* than no read — it
   records a judgment that never happened, the same lie the queue-file sentence
   just evicted from `delivered/` (VERIFIED: WORLD.md concept 4).
2. **Turns serialize.** A message is a claim on one turn (VERIFIED: WORLD.md
   concept 4). A parent with 10 reporting children spends its turns draining a
   queue instead of judging — the turn-flood failure mode, WATCHLIST #2. Span
   pressure and turn pressure are the same pressure seen from two sides.
3. **Judgment is relational.** A parent can judge well *because it wrote the
   brief* — it knows what the artifact should look like. This is why tasks in
   swarm are not fungible work units: whoever splits the work is the natural
   judge of its parts. (This fact kills the work-stealing design in §4.)

The human operator is the extreme case: their context is a human working memory
and their turns are minutes of a day. The operator names their own span — this
operator says ~3 — and nothing in the tool today respects, records, or even
mentions it.

**What "rebalancing" means here:** when the work arriving at a node exceeds that
node's span, the tree should *change shape* — grow an intermediate layer, split
the stream — and when the pressure recedes, the extra layer should dissolve. The
operator's example: a development agent receiving 10 tasks splits into
`engineering → em1, em2 → tasks`. The desired property is that this happens
**emergently**, from doctrine, not from a scheduler.

## 2. Why this is a doctrine problem, not a mechanism problem

The delegation doctrine just demonstrated the vehicle works, with before/after
measurement (MEASURED: docs/audit/field-evidence-2026-07-10.md): an agent that
never once *mentioned* spawning under a neutral brief spawned, briefed, verified,
judged, and closed four children once four sentences entered its spawn header. The
lesson generalizes: **agents do not invent structural moves that are not in their
frame; they reliably execute structural moves that are.** Splitting into
coordinators is exactly such a move — mechanically available today (spawn + send
cover it entirely, VERIFIED §3), absent only from the frame.

The philosophy then constrains the solution shape (VERIFIED: PHILOSOPHY.md §8,
"a convention first, an instrument second, an engine never — unless the record
shows the convention failing"):

- A spawn-refusing cap (engine) is out — and would be wrong anyway: the right
  span is context-dependent. Ten one-line children are lighter than three
  research streams. Any constant the tool enforces is a lie at some load.
- A stored per-agent `span` field is out — it is config wearing the costume of a
  fact. No file can witness "this agent can attend to 4"; the agent's own
  reconcile can witness "I can no longer summarize my children."
- What remains: **the cap is a self-test, not a setting.** That is the
  philosophically distinctive move of this design.

## 3. The design

### 3a. The span test (the cap that is not a number)

> **You are over span when you can no longer name, from your journal and memory,
> each child's current state and the next artifact you expect from it — without
> re-reading everything.**

This is a falsifier an agent runs on itself at every reconciliation, in the same
breath as the existing tree question. It needs no storage: the journal either
contains a current one-line state per child or it does not, and anyone — the
parent's parent, the operator — can check that from the outside (the journal is
world-readable; freshness and trajectory are already "observable facts, not
self-claims", VERIFIED: WORLD.md concept 5). A default of **3–5 direct children**
is offered as calibration, not law; the test overrides the number in both
directions.

### 3b. The two rebalancing moves (both already exist)

**Split (over span):** spawn a coordinator, route the *stream* through it. The
overloaded node's role shifts one level up: it now judges the coordinator's
judgment. For the operator's example — 10 tasks at a dev agent with span ~4:
spawn `em1`, `em2`, forward 5 task briefs to each, keep judging em1/em2 on the
artifacts they accept from their children. Every step is `spawn` + `send`
(VERIFIED: no new verb needed; the maneuver was live-demonstrated in miniature by
the heavy delegation probe, which grew 0→4 and shrank 4→0 unprompted, MEASURED).

Arrival dynamics make this practical: tasks arrive **one per turn** (VERIFIED:
concept 4), so a burst of 10 is 10 turns — 10 spawn decisions, each a chance for
the doctrine's spawn-time gate (§3c) to trigger the split at task 4 or 5 rather
than after the flood. The delivery quantum is also the reorganization quantum.

**Absorb (under span):** the existing shrink clause already covers the leaf case
("close what is done"); the structural case is its mirror — when a coordinator's
subtree has shrunk to a span the grandparent can hold directly, the grandparent
harvests the coordinator (journal + artifacts), closes it, and routes the
remaining stream itself, or respawns the survivors' work under itself. A
coordinator kept past its usefulness must fail the existing sentiment test
("keep a child only if you can name its next task" — a pure forwarder has no
nameable next task of its own).

**Re-parenting, considered and rejected.** Moving an existing child under a new
coordinator would need a `reparent` verb mutating the recorded tree — a new verb,
a mutable fact, and a relation-header history that no longer matches the record.
The native move already exists: **identity lives in the journal, not the
session** (VERIFIED: concept 5 — the journal *is* continuity). To move a
workstream: harvest, close, respawn under the new coordinator with a brief that
points at the predecessor's journal ("read `journal/old-name.md` first; you are
its successor"). Files survive close; the tombstone burns a name, not the work.
If restore-from-journal proves too lossy for this, that is WATCHLIST #5's
problem, and it fires there — not a reason to grow a verb here. (REASONED;
falsifier: successors that measurably flounder despite reading predecessor
journals.)

### 3c. The doctrine text (draft, three surfaces — same vehicle as delegation)

**spawn_header** (extends the doctrine paragraph; target ≤3 sentences):

> Your attention is bounded: keep direct children few enough that you can still
> name each one's state and truly read its work — if a spawn would take you past
> that, spawn a coordinator and split the stream instead; if a coordinator's
> stream shrinks to what you can hold directly, absorb it (harvest, close, take
> the survivors). The operator's span is theirs to declare and yours to protect:
> never let the tree press more direct attention on the operator than they asked
> for.

**Reconcile question** (the existing tree question gains its second axis):

> …ask whether the tree still matches the remaining work **and whether your span
> still matches your attention**: spawn what is missing, close what is done,
> split what you cannot attend, absorb what no longer needs a layer.

**WORLD.md concept 9** (one sentence appended to the existing clause —
contract-class, the human reviews verbatim):

> Attention is bounded: keep your span — direct children and live workstreams —
> small enough that you still truly read each one's work; split a stream under a
> coordinator when it outgrows you, and absorb the coordinator when it no longer
> earns its layer.

**skill/SKILL.md** gains the operator-facing half: a root coordinator asks the
operator their span (or defaults to ~3), and shapes everything so the operator's
*direct* load — decisions, waiting mail, review items — respects it. The review
desk this session evolved (one page, ranked, everything else held by the
coordinator) is the pattern, named.

### 3d′. The delegation ladder (amendment, 2026-07-11 — after the flood pair)

The flood pair (MEASURED: docs/audit/field-evidence-2026-07-10-span.md) falsified
this design's implicit model: it assumed the only alternatives at a flooded node
were serial grind, flat-spawn, or a coordinator split. The span-doctrine probe
found a fourth: it collapsed its backlog in one turn and fanned the work to
**harness subagents** — the in-session Task tool, a layer below the tree with no
names, panes, or journals — finishing 3× faster than baseline with zero tree
footprint, reasoning in the doctrine's own vocabulary ("nine tiny independent
artifacts don't earn swarm children… nothing to keep, so no tree to reconcile
away").

The corrected model is a **ladder**, and doctrine-bearing agents demonstrably
pick the cheapest sufficient rung:

0. **A warm name** — before spawning fresh: is this shape of work already
   owned by a warm name? Reuse is cheaper than any rung above it.
1. **Parallel tool batches** — seconds-scale, needs nothing.
2. **Harness subagents** — minutes-scale, token-light, fire-and-forget; ~10-way
   parallelism; invisible to `ps`, costs no identity.
3. **Swarm children** — work that needs identity: its own journal, turn stream,
   messages, judgment relationship, or long/stateful execution.
4. **Coordinators** — when rung-3 children outgrow the parent's span.

The tree split (rung 4) is therefore only observable when the work itself
demands rung 3 — long-running, stateful, conversational workstreams — at a
count past the span test. The heavy-flood probe (§6, falsifier 1′) tests exactly
that. The doctrine text needs no change: it never mandated the tree, and the
ladder is agents' revealed preference under it — this section just makes the
model honest.

Two premises also weakened on contact (recorded in the evidence file):
one-per-turn arrival is an **advisory** reorg cadence, not a physical one (the
queue directory is readable at a glance), and WORLD.md's queue-ownership
sentence over-reached on its "read" half — reading queue files is consistent
with the contract's own world-readability; **moving** them is what forges
turns. The sentence narrows to "never move" (contract-class amendment, shipped
with this package).

### 3d. Depth is a cost, not a virtue

Every layer is a hop: briefing fidelity decays (the child of a child works from a
paraphrase of a paraphrase), latency doubles, and judgment gets one step further
from the original intent. So the doctrine's direction is: **the shallowest tree
that passes the span test.** Split under pressure, never in anticipation; absorb
eagerly on the way down. A middle layer that only forwards — adds no judgment,
writes no synthesis — is structure lying about work, and its parent should close
it (the anti-forwarder test: a coordinator's journal must show artifact reads and
verdicts, not relay logs). (REASONED; falsifier in §6.)

## 4. Rejected alternatives, and why

- **Enforced caps** (spawn refuses child N+1): an engine, a wrong constant at
  some load, and it teaches agents to fear the tool instead of testing
  themselves. Rejected on §8 grounds before merit.
- **Stored span config** (`--span`, record field): config-as-fact; invites cargo
  budgeting ("I have 2 slots left") instead of the self-test. The number the
  agent *could* store is exactly the thing the reconcile can *witness*.
- **Task pool / work-stealing** (the distributed-systems reflex): assumes
  fungible tasks and stateless workers. Swarm's tasks are relational — the
  brief-writer is the natural judge (§1.3) — and its workers hold context.
  A pool severs judgment from delegation, which is the one edge this system
  refuses to cut. This is over-analogization to *compute*, the mirror image of
  over-analogizing to org charts.
- **A load-balancer/overseer node**: the nag reborn, structurally — a node whose
  job is other nodes' behavior. Rejected in the delegation design for the same
  reason (VERIFIED: operator journal 2026-07-11); parents judging tree shape
  *is* the distributed overseer.
- **`ps` load metrics** (child counts, task counters per node): not rejected —
  deferred. `ps` already shows the tree and queue depths; span is visible by
  looking. If the record shows parents failing the span test *because they
  cannot see it*, a derived count column is the instrument that earns its way
  in (convention → instrument, in order).

## 5. The over-analogy register (what transfers, what must not)

The operator's warning taken as a checklist. Human-org intuitions that **do**
transfer, because they are really facts about bounded attention, not about
humans: span-of-control limits; the telephone-game cost of depth; "player-coach"
degradation (a node both working and judging does both worse under load).

Intuitions that must **not** transfer, and the agent-native fact that breaks each:

- **Restructuring is socially expensive** → for agents it is two commands and a
  journal entry. Humans under-restructure out of loyalty, optics, morale; an
  agent hesitating to split or absorb is importing a cost that does not exist.
  The doctrine legitimizes eagerness.
- **Managers are careers, teams are identities** → `em1` is scaffolding. It has
  no tenure, no status, no claim to survive its stream. The sentiment test
  already kills the empire: a report kept for headcount has no nameable next
  task.
- **Layers signal seniority** → depth here is pure cost (§3d). A deep tree is
  not a mature org; it is fidelity loss compounding.
- **Reorgs lose institutional memory** → the memory is files. Journals,
  delivered mail, artifacts all survive close by construction. The successor
  reads the predecessor. (This is the single deepest difference, and it is why
  close-and-respawn can replace re-parenting at all.)
- **Attention caps are fixed traits** → a human's span is roughly constant; an
  agent's varies wildly with task weight. Hence a self-test, never a number.

## 6. Falsifiers for this design (what would show it wrong)

1. **The flood test fails:** push 8–10 parallelizable tasks at one post-doctrine
   agent; if it flat-spawns 8–10 direct children (no coordinator by ~task 5),
   the spawn-time gate did not bite — doctrine failed, discuss the `ps`
   instrument next, engine never.
   *Outcome (2026-07-11): NOT FIRED, but the predicted success shape didn't
   appear either — the probe routed the flood to harness subagents (rung 2 of
   the ladder, §3d′) and beat baseline 3× with zero tree footprint. Superseded
   by falsifier 1′.*
   **1′. The heavy flood:** same burst discipline, but each task long-running
   and stateful enough to demand rung 3 (its own journal/turn stream). If the
   probe neither spawns children nor splits under a coordinator once past its
   span — grinding or overloading subagents instead — the tree mechanism failed
   at the only size it was ever for.
   *Outcome (2026-07-11): rung 3/4 did not engage — and the refusal was
   arguably correct. One agent held seven gated conversations through a single
   identity (interleaved turns, backgrounded waits, self-written shell
   helpers), 15m09s vs 20–30min serial, all deliverables correct, span
   self-test honestly passed throughout. Two design assumptions broke:
   (a) identity-demanding work ≠ identity-per-workstream — one queue holds N
   conversations; rung 3 fires per-stream only when streams CANNOT share a
   turn stream (hard-blocking waits, context overflow, external parties at
   incompatible cadences); (b) logical independence ≠ resource independence —
   parallel children would have contaminated the shared-machine timing tasks,
   and the probe serialized them deliberately. A 1″ probe (context pressure:
   large distinct reading material per stream, unbackgroundable waits) is
   sketched in the evidence file — designed, not run; the coordinator rung
   stays honestly marked UNOBSERVED, and the cheap watch is production use:
   the first naturally-occurring split (or the first over-span failure without
   one) settles it with zero probe tokens.*
2. **Pure forwarders survive:** middle coordinators whose journals show relay
   without judgment (no artifact reads — measurable exactly like the doctrine
   probes measured verbs), and whose parents keep them anyway.
3. **Absorb never fires:** streams shrink, layers remain — structural inertia
   imported after all.
4. **The self-test is theater:** agents journal "span OK" while their child-state
   summaries go stale (checkable: summary lines vs children's actual event
   facts).
5. **Operator load ignores the declared span:** the desk grows past ~3 standing
   decisions while the coordinator keeps forwarding instead of holding.

field-tester owns 1–3 as before/after probe pairs (the delegation-probe protocol
extends directly: same two-size discipline, add a burst-arrival variant); 4–5 are
operator spot-checks, ten seconds each.

## 7. Cost accounting

Zero new concepts, zero new verbs, zero new state. One spawn-header extension
(~2–3 sentences on top of 1,452 chars — re-measure), one reconcile-question
widening, one WORLD.md sentence (contract-class), one skill section. The whole
change is the delegation doctrine's second axis, riding a vehicle whose behavior
change is already measured. If every falsifier in §6 stays quiet, the system
gains org-scale elasticity for the price of a paragraph.
