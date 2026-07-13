# PIPELINE-WIRING — a sequential, tracked pipeline for operator-bound escalations

**Author:** `pipeline-drafter`, for `pipeline-scout`. Written at `main@834fec4`,
2026-07-11. Third iteration of the decision-engine wiring, scoped down by the
operator to **only operator-bound escalations**: the engine reads each one
FIRST (as a guarantee), then either AUTO-ANSWERS (grant-covered,
confidence-cleared) or PASSES TO THE HUMAN with its trace attached. Prediction
engines are ASSUMED to exist; whether to build them is settled elsewhere (DEC).
This document AMENDS `docs/design/DECISION-WIRING.md` (`DW §n`); it does not
supersede it. It is a recommendation, not a survey — and on the operator's
central word ("sequential, as a guarantee") it recommends **against the hard
form and toward plain races-allowed — the engine reading first as a tendency of
its standing watch, never as an enforced or audited guarantee**, for reasons the
maps force.

**Evidence discipline:** every load-bearing claim cites `DW §n`
(`docs/design/DECISION-WIRING.md`), `PROXY §n` (`docs/design/PROXY-WIRING.md`),
`INBOX §n` / `INBOX NOT-n` (`docs/design/INBOX.md`), `SIMPLEST §n`
(`docs/design/SIMPLEST.md`), `WORLD:n` (`WORLD.md` line), or a `bin/swarm:line`
at main. **All `bin/swarm:` line numbers were re-derived against `main@834fec4`
after `pipeline-redcheck` found the first draft's operator-exit cite had rotted
to unrelated plumbing (Finding C); a skeptical reader opening those lines finds
the real code.** Two adversarial reviews are part of this document's provenance:
`pipeline-red` (`.swarm/research/pipeline-red-review.md`, the drafter's own
child) and the independent `pipeline-redcheck`
(`.swarm/research/pipeline-redcheck.md`, spawned by the parent to catch the
shared blind spot — 1 KILL / 2 WOUND / 3 CONFIRM, all repaired in place, none
changing the recommendation). Repaired sites say what changed.

---

## The recommendation in one paragraph

**Adopt the pipeline as DW-plus-one-refinement, and drop "engine-first as a
guarantee" for what the substrate can actually give: races-allowed, where the
engine wins because it never sleeps.** The sequence the operator wants — engine
reads first, auto-answers or passes with a trace — is DW's engine-hand already
(DW §1–§4). "Reads first" is delivered not by a mechanism that orders the two
hands but by the engine's **standing watch**: it holds a Monitor on
`queue/operator/` and answers within a turn (DW §1c, DW:153-154), so it *tends*
to reach a new item before a human stint does — a tendency of always-being-awake,
never a guarantee the record enforces. The one refinement over DW is a **trace
that is entirely derived** — the engine's ledger verdict entry (DW §3b step 3),
its hand-tagged claim line (DW §3b step 1), its world-readable journal, and
`ps` — with **no new state-bearing record and zero bytes on the message file**
(DW §8 I3 preserved). A HARD engine-first guarantee — one a human must satisfy
before draining, or one the record can *audit* as "engine read this before the
human could" — is **recommended against, in the strong sense PROXY-WIRING used
for the veto-hold: do not.** It cannot be built on this substrate without (a) a
jam in front of the human when the engine is down (the exact failure DW §1b
killed the dedicated-addressee corner on), (b) a new rule the human must
remember under stress (a lock, a staleness timer, or a liveness-gated drain —
each modifies, not appends to, the seat ritual, breaking DW:558-559), or (c)
recording the deliberation interval "engine has read, not yet ruled" — a state
that is a named grave three ways over (§4). All three are the same crack: **the
tool never delivers to the operator queue (bin/swarm:610-611), so there is no
delivery path to order two hands, which is the very fact that makes DW's hand
additive — and equally makes a hard barrier impossible.** The value the operator
wants (the engine reading the mechanical share before a human spends attention)
is delivered by the always-awake watch at zero contract cost; the *guarantee*
they asked for cannot be, and §5 proves why. The grave stays shut because
**every pipeline state maps to a consumer DW already defined, and the one state
the guarantee would force onto the wire — "engine reading, not yet ruled"
(S1.5) — is kept off the wire by the engine's briefed discipline** (§4; this is a
discipline-bounded residual, not a code guarantee — the honest register, and a
private in-memory read-marker is an accepted, uncollectable residual like DW
§2c's unauditable threshold). CONTRACT-CLASS bill: **DW's one inherited
amendment, unchanged** — the soft/races-allowed form needs no further WORLD.md
touch; the hard form would break "Promptness is best-effort" (§8), which is one
more reason it is rejected. This document changes DW in two small places (§9)
and adds no new grave.

---

## 1. What "sequential" and "tracked" actually name — read against the maps

The operator's two words are the whole novelty over DW. Taken at face value
they reopen exactly what the two prior docs closed, so they must be read
precisely before they are designed.

- **"Sequential" = engine reads first, as a guarantee.** DW's engine has **no
  priority**: "hands come and go, in sequence or in parallel" (DW §1c, quoting
  C14), and the design's whole additivity rests on **races-allowed** — "the
  engine claims what it answers and leaves the rest; engine absent = today
  exactly" (DW §1a.3), with a claim-race convention (mv-and-abort, DW §1c) as
  the only ordering discipline, and that convention exists precisely because
  **nothing mechanical adjudicates two claimants** (DW §1c, citing
  `seat-ritual.md:264-266`). "Engine reads first, guaranteed" asks for the one
  thing DW deliberately does not provide: an ordering guarantee on the operator
  mailbox. That is HAZARD 1, the barrier (§5).

- **"Tracked" = per-escalation state the operator can see.** A tracked
  sequential pipeline with per-item states is the closest any of the three
  iterations has come to **SIMPLEST §2 row 13** — "inbox three-state machine:
  `inbox/` → `rendered/` → `read/`" — a DELETED concept whose cause of death
  (INBOX NOT-6, NOT-8, NOT-9) is precise: states that lived on the wire and
  nobody consumed, and "an automatic mover would manufacture claims with no
  claimant — exactly the record-falsification the move-only sentence exists to
  prevent" (INBOX NOT-8). That is HAZARD 2, the grave (§4).

The rest of this document is these two hazards, designed out or declared
un-designable-out, and the small set of changes to DW that the honest design
implies.

---

## 2. The pipeline spec, per operator-bound escalation, in order

Scope, stated once and enforced by construction: **only messages addressed to
`operator`.** No agent-to-agent traffic (that is PROXY-WIRING's plane; killed
as interposition there, PROXY §2). No hop-1 seat-judgment material — the engine
may *read* it but no legal grant can *cover* it (DW §4, "you cannot
pre-authorize an adjudication", DEC §1a). "Escalation" is not a new message
class the engine detects — that would be the question-detection grave (INBOX
NOT-3, SIMPLEST §2 row 16); it is simply **an item waiting in
`queue/operator/`**, which is where DEC §3's clause-iii decision points are
born (DW §2a).

The stages, with a latency budget each. "Budget" here is a *design bound*, not
an SLO — DW establishes that pass-through latency is not a defect (DW §1a.4,
DEC NOT-list 7); the budgets exist so it is explicit that the engine's read adds
no *required* latency to any hand (nothing waits on it, §5) and so the barrier's
cost, were it built, would be visible.

| # | stage | what happens | latency budget | fail-open at this stage |
|---|---|---|---|---|
| S0 | **arrival** | sender does `swarm send operator`; file lands in `queue/operator/` via `queue_put` (bin/swarm:917). Wire untouched; no routing; the engine is not on the send path (bin/swarm:910-917). | 0 (unchanged from today) | n/a — nothing can fail here that isn't failing today |
| S1 | **engine reads first (by always being awake, not by a lock)** | the engine's standing Monitor on `queue/operator/` (DW §1c, DW:153-154) sees the item and answers within a turn; it tends to reach the item before a human stint does. **No hand is prevented from acting; nothing defers by duration.** | ≤ one engine turn (a tendency, not a bound) | **the fail-open is the substrate itself** — see §5. The item is ordinary waiting mail the whole time; any hand may claim it at any moment (DW §1c races-allowed). The engine "wins" only by usually getting there first; if it doesn't, the human just drains it — that IS today. |
| S2 | **verdict** | grant-covered AND confidence-cleared (the DW §2c composition) ⇒ **auto-answer** (S3a); else ⇒ **pass** (S3b). | ≤ one engine turn | verdict never reached ⇒ item is a pass by default (S3b): the absence of an auto-answer IS a pass-through (DW §4). |
| S3a | **auto-answer** | claim (move + hand-tagged claim line), answer the asker in the engine's own wire name with the AUTO-ANSWER marker + grant citation, write the ledger verdict entry. DW §3b verbatim. | ≤ one engine turn | crash mid-ritual ⇒ DW §7's four interruption states + recovery rules, unchanged. |
| S3b | **pass-to-human-with-trace** | **the engine does nothing to the message.** The item waits in `queue/operator/`; `ps` shows it (bin/swarm:429-432); the human's ritual is SEAT §3 verbatim (DW §4). The "trace" is the engine's own journal note (DW §4 reason iii, PROXY §4's `DRAFT:` shape), NOT a byte on the message. | 0 added | this stage IS the fail-open state — indistinguishable from engine-absent (DW §8 I3). |
| S4 | **human action** | the human (or a seated hand) drains, reading auto-answers as already-claimed and passes as ordinary waiting mail. | best-effort (WORLD:54) | n/a |
| S5 | **record closes** | no explicit close: an auto-answer's ledger entry IS its closed record; a pass's close is the human's own claim line when they drain it (WORLD:60-61). | — | §4 proves no state is left open with no consumer. |

**Nothing in this table is new relative to DW.** There is no window, no timer,
no deferral, no lock. "Sequential" is delivered entirely by S1's standing watch
— the engine reads first by being awake first, not by any mechanism that orders
the hands. Every stage is DW executing; the only additions this document makes
are the *derived trace* (§3, §4) and the standardized pass-path journal note
(§9). If the engine is absent, slow, or wedged at any stage, the item is
ordinary waiting mail and the human drains it exactly as today — there is no
pipeline rule that becomes active or inactive, because the pipeline is nothing
but "what a live, always-watching hand does," and a dead hand does nothing.

---

## 3. What "tracked" buys the operator, concretely — and where they SEE it

The operator's word is "tracked." The honest question is: *tracked where, and
who reads the track?* The answer must not invent a new view (INBOX E3 prices
even a `--from` flag as unearned; a new tracking surface is heavier). Every
place the operator can see the pipeline **already exists**:

- **`ps`** (WORLD:30, "the one view"): shows the engine's pane and liveness
  (is the pipeline *running*?), the operator's waiting mail at the top (what is
  *in* the pipeline, un-auto-answered), and the engine's last words (what it
  last did). An operator glancing at `ps` sees the pipeline's state without any
  new surface.
- **The operator ledger** (`.swarm/journal/operator.md`): every auto-answer is
  a `[hand:engine] AUTO-ANSWER:` verdict entry (DW §3b step 3) — the closed
  half of the pipeline, grep-able. Every human drain is a claim line (WORLD:61)
  — the other closed half.
- **The engine's own journal** (world-readable, WORLD:28): pass-through drafts
  (DW §4 reason iii; the `DRAFT:` shape PROXY §4 standardized) — the
  "considered and passed, here's what I'd have said" trace, costing the human
  nothing unless sought.
- **The asker's `delivered/`**: an auto-answered decision point shows
  `"from": "decision-engine"` in the asker's delivered record (DW §7 state-4
  recovery relies on this) — the answer is world-readable evidence.

**What "tracked" does NOT buy, and must not:** a per-escalation status field, a
`rendered/`/`read/` folder, a `pipeline-state.json`, or any record whose states
a mover advances. That is the grave (§4). The operator sees the pipeline the
way they see everything else in this system — by reading world-readable files
and `ps`, never by consulting a state machine. If the operator, after the
pilot, finds this insufficient, the pre-priced next rung is INBOX E2 (a
seat-authored triage paragraph, read at stint time) — NOT a tracking record.

---

## 4. HAZARD 2 — the grave: every state has a named consumer, message files byte-untouched

The design decision, made loudly: **the tracking record does not exist as a new
artifact. The pipeline's states are DERIVED from records DW already writes, and
the message file is byte-identical to engine-absent (DW §8 I3).** This is
option (a) in the brief's fork — named consumer per state, files untouched —
and it is chosen over option (b) (knowing state-on-the-wire) because option (b)
cannot address INBOX NOT-8: any state a mover advances on the operator queue
manufactures a claim with no claimant, and DW's own move-only discipline exists
to forbid exactly that.

Here is every pipeline state, its **derivation** (where it is legible — never a
stored field), its **consumer** (who acts on it), and its **collector** (who
notices if it rots). If any row had a state with no consumer, the grave would
be reopening; none does.

| state | how it is legible (derived, never stored on the wire) | consumer | collector (notices rot) |
|---|---|---|---|
| **arrival** | the file's presence in `queue/operator/` + `ps` (bin/swarm:429-432) | the engine's Monitor; any draining hand | `ps` itself — a waiting file is visible; nothing to rot |
| **engine-reading, not yet ruled (S1.5)** | **KEPT OFF THE WIRE by the engine's briefed discipline — no on-disk record, no marker, no hold.** The engine reads in its own memory; the file is byte-identical to waiting mail throughout. | **none — and that is the point.** Nothing consumes "the engine is thinking," because nothing may depend on it. | PIPE-F2 fires if any *on-disk* record of S1.5 appears; a *private in-memory* read-marker is neither code-prevented nor PIPE-F2-caught — a discipline-bounded residual, §4a (like DW §2c's unauditable threshold) |
| **verdict: auto-answer** | the `[hand:engine] AUTO-ANSWER:` ledger entry + the hand-tagged claim line + the asker's `delivered/` record (DW §3b) | the asker (receives the answer); the seat (reads it as claimed) | DW W-F1 (answer without covering grant) + the inverse sweep (DW §7 state 4) — both already defined |
| **verdict: pass-to-human** | **the absence of any engine action** — the file still in `queue/operator/`, no claim line, no ledger entry (DW §4) | the human, who drains it as ordinary waiting mail (SEAT §3) | none needed — a pass is indistinguishable from engine-absent, so "rot" means "an item waited," which is today's normal and not a failure (INBOX §1d: zero misorderings in the whole corpus) |
| **human-action** | the human's own claim line when they drain (WORLD:61) | the record itself (the claim line IS the action) | DW W-F2 (delivered file with no claim line) — the C16 alarm, proven live (DW, EV:78) |
| **record-closes** | no explicit close: an auto-answer's ledger entry is terminal; a pass closes when the human's claim line lands | whoever later greps the ledger / the mailbox | the same W-F2 / W-F1 collectors; there is no "closing" state to advance and therefore none to rot |

**The message file, byte-untouched — the proof.** The engine only ever touches
a message file in the auto-answer path, and only by the DW claim move (`mv` to
`delivered/`, DW §3b step 1) — the *same* move a human hand makes when it
drains (WORLD:61), producing the *same* claim-line record. On the pass path it
touches nothing (DW §4). So there is **no state a mover advances that a
claimant does not author**: every move is a claim with a claimant, and INBOX
NOT-8's failure ("a mover manufacturing claims with no claimant") is
structurally impossible. There is no `rendered/`, no `read/`, no third folder
(INBOX NOT-9), no status field (INBOX NOT-1). The "pipeline" is a *reading* of
existing records, not a *machine* that moves files through states.

### 4a. S1.5 — the state the word "guarantee" would force onto the wire

The dangerous state is S1.5: **"the engine has READ this item and is deciding,
but has not yet ruled."** DW's design does not have this state — the engine
reads, and then either it *claims* (moves the file, S3a) or it *does nothing*
(S3b); "considering" leaves no trace, which is exactly why pass-through is
absence (DW §8 I3). But the operator's word **"guarantee"** puts pressure on
S1.5 to become observable, because *"the engine reads first, always" is only
auditable if the record can show the engine read before the human could.* The
moment S1.5 gets a record, the grave reopens — three ways, each already
autopsied elsewhere:

1. **as a "considered / passed" marker** — which PROXY-WIRING explicitly
   forbade even for the observer's own private ledger: "write nothing… No entry,
   no count, no 'considered and passed' line — the pass-through-is-absence
   invariant (DW §8 I3) applied to the observer's own ledger" (PROXY §3b, PW
   step 2). A per-item "engine has read this" stamp is the same line, one layer
   earlier;
2. **as a read/unread/seen state** on operator mail — INBOX NOT-6, "No
   read/unread/ack state… the three-state inbox machine"; "engine-read →
   engine-ruling → human-may-drain" is SIMPLEST §2 row 13 wearing a pipeline
   costume;
3. **as a HOLD** — the engine moving the file to reserve it during
   deliberation, to *guarantee* it reads before a human can grab it. This is
   INBOX NOT-8 verbatim (an automatic mover manufacturing a claim with no
   claimant) AND it destroys I3 — engine-down now leaves items *held* (moved)
   with no answer, observably NOT engine-absent. It promotes DW §7's state-3
   crash accident into the steady-state mechanism.

**The design's answer: S1.5 is kept off the wire by the engine's briefed
discipline — and the honest register for that is "discipline-bounded," NOT
"structural."** *(This paragraph was over-claimed in the first draft and is
downgraded here after `pipeline-redcheck` Finding A — the KILL. What changed:
"structurally unstateable" became "unstateable on the wire by briefed
discipline," and the PIPE-F2 blind spot below is now stated plainly.)* Because
engine-first is a races-allowed *tendency* of the standing watch, not a
guarantee, there is no obligation to make S1.5 observable — and the engine's
brief forbids recording it. Concretely: **the engine reads in its own memory;
its brief instructs it to write no record that it read, hold nothing during
deliberation, and leave no marker on unanswered mail. An item the engine is
mid-deliberation on is byte-identical to waiting mail; a human who drains it
during that interval simply wins the race (DW §1c), and the engine's failed `mv`
aborts its claim (DW §1c, DW:167-172).**

**The precise honesty — read against I1, this design's one genuinely structural
guarantee.** I1 (the wire is untouched) is *structural*: `bin/swarm` **cannot**
deliver to the operator queue (the operator-exit, bin/swarm:610-611), so no
amount of engine misbehavior can put a byte on that path — the code forecloses
it. S1.5's off-the-wire-ness is **not** of that kind. Nothing in `bin/swarm`
stops the engine session from writing `.swarm/engine/read-markers/<id>` or a
`read:` line in a status file, or — the case no collector can see — simply
**noting privately in its own reasoning** "I have read item X." The only thing
keeping S1.5 off the wire is a sentence in the brief, which is a *convention the
engine is asked to honor*, exactly like DW §2c collision 2's unauditable
threshold (which this section already cited as "the same shape"). So the twin
must wear the same word: **S1.5 is unstateable by briefed DISCIPLINE, not by
CODE.**

**The residual, stated where the operator can see it — the KILL's substance,
not just its wording.** Two limits follow, and neither changes the
recommendation:

- **PIPE-F2 is blind to the in-memory case.** Its collector (§11) sees only
  files on disk — `git status`, reconcile greps, accumulating traces. A private,
  in-context read-marker (the engine noting to itself "I read X, so I'll time my
  claim to win the race") leaves no file, no git delta, no grep hit. **PIPE-F2
  catches an *on-disk* S1.5 record; it cannot catch an *in-memory* one.** §11
  now says this in the falsifier itself rather than implying total coverage.
- **What that permits, bounded.** An engine keeping a private read-ledger could
  condition its claim timing on a state only it can see — manufacturing a *soft*
  version of the ordering this document says the wire cannot carry, without
  touching the wire. Nothing detects it directly. What bounds the harm: it can
  only ever produce the *effects* the engine already may produce legitimately (it
  claims grant-covered items and passes the rest); the private timing changes
  *which hand wins a race*, never *what gets answered or by what authority*
  (grants still gate, DW §3a) — so the blast radius is "the engine won a race it
  might have lost," which costs the human nothing and is exactly today's
  races-allowed outcome when the always-awake hand wins. It is a discipline
  residual, accepted in writing here, precisely as DW accepts the unauditable
  threshold.

**The consequence, restated honestly:** the pipeline cannot prove, after the
fact, that the engine read a given passed-through item before the human did; it
can only prove what the engine *did* (the ledger), and it cannot prove the
engine kept no private read-marker. That un-provability is the price of keeping
the grave shut — and it is the right price, because the alternative (an on-disk
"engine read this" record) is exactly the consumed-by-nobody state that killed
the three-state machine. This is also the record-side face of §5's mechanical
argument: the only way to *audit* "reads first as a guarantee" is to record
S1.5, and there is no way to record S1.5 on the wire that is not a grave — so
"reads first" can be a tendency the record never stores, or a guarantee the
record cannot keep, but not both.

---

## 5. HAZARD 1 — the barrier: the fail-open, and why engine-first must be a tendency, not a guarantee

This is the load-bearing section. The operator wants engine-first **as a
guarantee.** DW's prime invariant is **"the engine can only ever subtract
itself"** (DW §8). These two are in direct tension, and the tension must be
resolved in the open, not papered over. The resolution: engine-first is
delivered as a *tendency* of the always-awake standing watch, and any mechanism
that would upgrade it to a *guarantee* breaks the invariant — this section
enumerates every such mechanism and shows there is no exception.

### 5a. The test, stated first

From the brief, verbatim in intent: *can a human, engine-down, drain the
mailbox exactly as they do today (SEAT §3) WITHOUT remembering any pipeline
rule?* If yes, the barrier is designed out. If the human must remember "check
the engine first" or "wait for the window" or "run the drain command not the
`mv`," the barrier is NOT designed out — engine-down has added human load, and
DW §8 I3 ("pass-through is absence; an observer cannot distinguish engine-down
from engine-choosing-not-to-answer") is false.

### 5b. Why a HARD guarantee fails the test — the durable reason first, then the mechanism sweep

**The durable reason, which holds regardless of any code detail** *(led with
first after `pipeline-redcheck` Finding B — the first draft leaned on the
current-code fact and subordinated this; the order is reversed here because this
is the argument that survives even a future `bin/swarm` change).* A hard
engine-first guarantee makes the engine a **mandatory reader that every operator
message must pass through before the human may act.** That is, by definition, a
**single point of failure on the operator's own mailbox** — a wedged engine
holds the mail from the human, converting the contract's "delayed, never lost"
into "blocked until the engine reads." This breaks **"Promptness is
best-effort"** (WORLD:54), which promises no component is a hard dependency for a
message making progress; it is PROXY §2b's plane-wide SPOF inversion ("proxy
wedged = every message stops… the failure is the outage") scoped to one mailbox.
**This reason is about the invariant, not the code: it stands even if someone
later added an operator-delivery path to `bin/swarm`.** It is the spine.

**The current-code fact, as corroboration.** On today's substrate the guarantee
is not merely unwise but *unbuildable*, and the fact that makes it so is the same
one that makes DW's hand additive: the tool **never delivers to the operator
queue** (`cmd_deliver` exits for the operator, bin/swarm:610-611), so there is no
delivery path on which order could be enforced at all. Every remaining mechanism
is shared consulted state — and each fails independently. The sweep:

A *hard* guarantee means the record can enforce, or at least audit, that the
engine read an item before any human hand acted on it. Ordering two independent
hands on one mailbox requires a mechanism that makes hand B (the human) *wait
for or consult* hand A (the engine). Enumerate every such mechanism this
substrate offers:

1. **Tool code on the delivery path** — the only place order could be enforced
   mechanically. **It does not exist for this queue:** `cmd_deliver` exits
   immediately for the operator (bin/swarm:610-611), the tool *never* delivers
   to `queue/operator/`, and the only code that moves a file to `delivered/` is
   unreachable for it (DW §8 I1; PROXY §1a). There is no delivery path to gate.
   This absence is the very fact that makes DW's hand *additive* — and it
   equally forecloses a hard barrier. No mechanism here.

2. **A lock or presence-file the human must consult** ("don't drain until the
   engine has stamped this item"). This is new tool-adjacent state DW already
   killed (DW:490-494). To fail open, the human must know *when the lock is
   stale* — must remember "if the engine is down, ignore the lock." **That
   remembered rule falsifies DW §8 I3 and the prime invariant.** And a lock the
   engine never clears (because it died) is a jam in front of the human — the
   dedicated-addressee failure DW §1b killed: "a dead or wedged addressee is a
   jammed mailbox in front of the human." **Fails both halves of the test.**

3. **A staleness timer** ("item older than X with no verdict is free"). A new
   number every draining hand must remember and evaluate (what is X? has it
   elapsed?). This is the ack/re-ping cadence machine SIMPLEST buried — "the nag
   with preferences" (INBOX NOT-6) — an ack-timer read before every drain.
   **A new remembered rule. Grave-adjacent. Fails the test.**

4. **A liveness-gated drain** ("drain only if no verdict OR engine not live in
   `ps`"). The closest to honest — but read the drain rule it produces: it is
   **not today's rule.** Today's rule (SEAT §3, WORLD:57-64) is "no claim on the
   item ⇒ I may claim it." The moment the human must *also* check the engine's
   `ps` liveness before draining, a pipeline rule has been added — and DW is
   explicit that "no step of SKILL.md's seat section is modified, only appended
   to" (DW:558-559). A liveness-gated drain **modifies** the drain step; it does
   not append. **I3 falsified.**

5. **Recording S1.5** so the guarantee is at least *auditable after the fact*
   ("the record shows the engine read before the human"). Every recording of
   S1.5 is a named grave (§4a). **Reopens the grave.**

There is no sixth mechanism: ordering two hands needs either code on a path
(none exists, #1) or shared consulted state (a lock/timer/flag/record — #2–#5,
each a remembered rule or a grave). **The hard guarantee has no mechanism that
is not fatal, so it is recommended against in the strong sense: do not build
it.** This is the same verdict PROXY-WIRING reached about the veto-hold (PROXY
§2d) and for the same kind of reason — the ask names a capability the substrate
cannot carry without breaking a load-bearing promise.

### 5c. The recommended form — races-allowed; the engine wins because it never sleeps

Drop "as a guarantee." Engine-first is delivered by the **standing watch**, not
by any ordering mechanism:

- The engine holds a Monitor on `queue/operator/` and answers within a turn (DW
  §1c, DW:153-154). Because it is **always awake**, it *tends* to reach a new
  item before a human stint does. That is the whole delivery of "reads first" —
  a tendency of always-being-awake, not a promise the record enforces.
- **No hand is ever prevented from acting.** The item is ordinary waiting mail
  from arrival onward; any hand may claim it at any moment (DW §1c
  races-allowed). If a human drains an item while the engine is mid-deliberation,
  the human simply wins the race, and the engine's failed `mv` aborts its claim
  (DW §1c, DW:167-172). The drilled falsifier for a double-claim is DW's own
  W-F8 (two claim lines for one file) — inherited, not new.
- **There is no window, no timer, no deferral, no lock.** "The engine reads
  first" and "the human may drain whenever they like" are both true at once,
  because the first is a statistical tendency and the second is the standing
  contract. Nothing consults the engine's state; nothing waits on it.

### 5d. Passing the test explicitly

*Can a human, engine-down, drain exactly as today with no remembered rule?*
**Yes — trivially, because there is no rule to suspend.** The drain rule is
unchanged from SEAT §3: "no claim on the item ⇒ I may claim it." Engine-down,
engine-slow, engine-wedged, engine-choosing-not-to-answer all present the human
with the *same* surface — an unclaimed file in `queue/operator/` — and the same
action. The human never checks the engine's liveness, never consults a timer,
never invokes a drain verb. DW §8 I3 survives whole: a passed-through item under
any engine state is byte-identical to engine-absent. **The fail-open is not a
mechanism the design adds; it is the substrate the design refused to modify.**

### 5e. The honest residual

The races-allowed form gives the operator **less than the literal ask.** "Engine
reads first, guaranteed" becomes "the engine, being always awake, usually reads
first — but nothing guarantees it and nothing waits on it." The word
"guaranteed" is downgraded to "reliably, because it never sleeps." This is a
real gap between the ask and the design, stated rather than hidden: **the
guarantee the operator asked for cannot be built without breaking the invariant
that makes the whole engine safe (§5b) and reopening the grave (§4a).** The
standing watch delivers the *value* of engine-first — the engine reads the
mechanical share before a human spends attention on it, for as long as it is
alive — without the *hazard* (a live dependency on the operator's own mailbox).
The one honest question left for the operator is in §12: **was "guarantee"
load-bearing, or was it loose for "reliably handles these because always
watching"?** If the former, the answer is *do not*; if the latter, this design
already delivers it, soundly, at zero contract cost.

---

## 6. Override / kill — inherited from DW, unchanged

Override (DW §6) and kill (DW §7) are **inherited verbatim.** The pipeline adds
no new authority (auto-answers are still grant-gated, DW §3a), no new held state
(each item is claim→answer→record within one turn, DW §3b; there is no window
and no deferral, so there is nothing to hold), and no new actor beyond DW's
engine-hand. Specifically:

- **Soft kill** (freeze grants, one journal entry, DW §7): the engine
  auto-answers nothing from its next item and passes everything through. There
  is no window to suspend and nothing else to say — a frozen engine on a
  races-allowed mailbox is just a hand that claims nothing, which changes
  nothing for the human. One entry.
- **Hard kill** (`swarm close decision-engine`, DW §7): pane dies ⇒ engine not
  live in `ps` ⇒ the standing watch stops ⇒ today's ritual, unchanged, because
  the mailbox was races-allowed the whole time. Nothing "opens" on kill because
  nothing was ever gated closed.

The four interruption states (DW §7) and their recovery rules (the C16 alarm,
the seat-owned open loop, the state-4 adopter check) are unchanged — and the
pipeline introduces **no fifth state on the wire**, because S1.5 ("engine
reading, not yet ruled") is kept off the wire by the engine's brief (§4a): a
crash during deliberation leaves the item byte-identical to waiting mail,
indistinguishable from the engine simply not having gotten to it, which is
exactly DW's state-1 ("file untouched ⇒ ordinary waiting mail"), not a new
state. (The one thing a crash cannot clean up — a private in-memory read-marker
— vanishes with the crashed session anyway; §4a's residual is about a *live*
engine, not a crashed one.)

---

## 7. Degraded-mode invariants — the engine can only ever subtract itself, under the barrier

DW §8's invariants I1–I4, re-checked under the sequential/races-allowed
semantics. **All four survive; the races-allowed form is chosen specifically so
they do.**

- **I1 — the wire is untouched.** Unchanged from DW: nothing between `swarm
  send` and `queue_put`; the engine is not on the send path (bin/swarm:910-917).
  There is no window, timer, or gate — nothing is added to any path.
- **I2 — no exclusive holds.** Stronger than in DW's own framing, because there
  is no window to even appear to hold anything. The file sits in
  `queue/operator/` from arrival exactly as it would with no engine; any hand
  may take it at any moment (races-allowed, DW §1c). A crash at any point
  strands no item — the file is always just waiting mail.
- **I3 — pass-through is absence.** The load-bearing one, and the reason the
  guarantee is refused. Under the races-allowed form, a passed-through item —
  and an item the engine is mid-deliberation on — under any engine state (down,
  slow, wedged, choosing-not-to-answer) is byte-identical to engine-absent and
  the human's ritual is SEAT §3 verbatim. **Under a hard guarantee this
  invariant would be FALSE** (engine-down would jam the mailbox or force a
  remembered rule; auditing "reads first" would require recording S1.5); that is
  the core reason the hard form is rejected (§5b, §4a).
- **I4 — authority is text, not process.** Unchanged: grants are world-readable
  journal lines valid without the engine (DW §3a). The design adds no window and
  no new authority — races-allowed grants no one anything; the engine's only
  power is the grant-gated auto-answer it already had in DW.

### The failure table, under the pipeline

| failure | invariants | observed result |
|---|---|---|
| engine never spawned / closed / crashed while idle | I1+I3 | today, exactly: mail waits, `ps` shows it, human ritual SEAT §3; **no rule is active, so none needs to be remembered or suspended** |
| slow / wedged (live in `ps`, not acting) | I2+I3 | the item is ordinary waiting mail; any hand claims it whenever it likes (races-allowed). **No jam, no wait** — nothing was ever deferring |
| crashed mid-deliberation (S1.5) | I3 | byte-identical to waiting mail; = DW state-1 (file untouched); a human draining it just wins the race |
| crashed mid-auto-answer | I2 | DW §7's four interruption states + recovery, unchanged |
| answers wrongly | I4 + §6 | DW-bounded: scope-limited, wire-attributed, revertible; DW W-F7 counts it |
| goes rogue / floods | §7 hard kill | `swarm close`; the standing watch stops; the mailbox was races-allowed throughout, so nothing changes for the human but the loss of auto-answers |
| **engine-down INCREASES human load** | — | **cannot occur by construction** (I3 + §5d): engine-down presents the human the same surface and the same action as today; if it ever does increase load, PIPE-F1 (§11) has fired and the barrier was not designed out — the design is void |

The last row is the prime-invariant guarantee restated as a probe target: the
races-allowed form makes engine-down strictly ≤ today's load, and PIPE-F1 fires
if it ever exceeds it.

---

## 8. CONTRACT-CLASS — the WORLD.md sentence-pair, re-checked under barrier semantics

DW already carries **one** CONTRACT-CLASS item: the mailbox paragraph
amendment (DW §9), because a standing auto-answerer falsifies "Messages to
`operator` wait until **the human looks**" (WORLD:57) for the answered subset,
and moving mail to `delivered/` strains "the human's side moves the mail"
(WORLD:60-61). DW's recommended wording:

> "Messages to `operator` wait until **the human's side** looks; …" and
> "… the human's side — **the human, or a hand they have seated in writing** —
> moves the mail to `delivered/` and journals the claim before acting on it."

**Does this still cover the sequential pipeline? Re-checked under both readings
of "sequential," and the answer splits cleanly on the word "guarantee":**

**Under the recommended races-allowed form: NO additional strain beyond DW's —
add nothing.** The engine does not look *first, always*; it looks first *as a
tendency* of always being awake (§5c), and any hand may look and drain before it
(races-allowed). So the mail still "waits until the human's side looks," and
whether the engine-hand or the human's own attention looks first, both are the
human's side (DW's amendment already says exactly that). The item is idle until
*a* reader on the human's side chooses to look; nothing routes it through a
mandatory first reader. **DW's one CONTRACT-CLASS amendment covers the
sequential form unchanged, and no new WORLD.md wording is warranted** — adding
pipeline language to a contract that INBOX/SIMPLEST fought to keep at nine
concepts would itself be an unearned cost.

**Under the HARD guarantee the ask literally requests — the reading this
document rejects — it strains past DW's amendment, at two clauses:**

1. **"Messages wait until the human's side looks"** describes mail idle until a
   reader *chooses* to look. A hard barrier makes the engine a **mandatory first
   reader that always looks before the human can** — the mail is no longer
   merely waiting; it is *routed through a required stage*. DW's amendment names
   *who may look* (human or seated hand); it does not license a *mandatory
   ordering* of who looks first. The hard reading strains a clause DW's
   amendment does not reach.
2. **"Promptness is best-effort" (WORLD:54)** — the cleanest kill. The contract
   promises no component is a hard dependency for a message making progress:
   "delayed, never lost." A hard engine-first barrier makes the engine exactly
   that hard dependency — a wedged engine that has not yet "read first" would,
   under a true guarantee, *hold the item from the human*, converting "delayed,
   never lost" into "blocked until the engine reads." That is PROXY §2b's
   single-point-of-failure inversion ("proxy wedged = every message stops… the
   failure is the outage"), scoped to one mailbox. **A hard barrier falsifies
   "promptness is best-effort" for operator mail.** The races-allowed form does
   not touch it: an engine that never reads changes nothing, because the human
   drains as today (the item is delayed at most until the human's next stint,
   never by the engine, WORLD:52-53).

**CONTRACT-CLASS verdict:** for the recommended form, **one inherited item (DW's
mailbox amendment, unchanged) and zero new mandatory contract touches.** The
engine-first *tendency* — worth describing so a reader is not surprised — belongs
in the engine's brief (`.swarm/briefs/decision-engine.md`), as content, not in
WORLD.md, as contract (the INBOX P7-kill distinction, INBOX:180-181): "the
engine holds a standing watch and therefore usually reaches operator mail before
a human stint does; this is a tendency, not a guarantee, and nothing waits on
it." The hard form would add at least one contract touch (WORLD:54 reworded) and
arguably a rewrite of WORLD:57 to name the engine's first-look as load-bearing —
which is one more reason it is rejected.

---

## 9. Does this supersede or amend DECISION-WIRING? — AMEND, two changes

**Amend. DW stands; this document changes it in two small places.** The pipeline
is DW's engine-hand with a standardized trace and one sentence of framing — not a
new design. Superseding would burn DW's adversarial provenance (the red-wiring
review) for no gain.

The amendment list:

| # | DW section | change |
|---|---|---|
| 1 | **DW §4** (pass-through) | STANDARDIZE the pass-through journal note as a `[hand:engine] DRAFT:` entry (PROXY §4's shape, already an accepted DW extension), so "tracked" has a concrete grep-able trace on the pass path without a byte on the message. This is the only structural change; everything else is framing. |
| 2 | **the engine brief** (`.swarm/briefs/decision-engine.md`, DW §9 #3 — a brief, not a DW section) | ADD the engine-first *tendency* sentence as CONTENT, not contract: "the engine holds a standing watch and therefore usually reaches operator mail before a human stint does; this is a tendency, not a guarantee, and nothing waits on it." NO deferral duty, NO window — the engine holds no ordering obligation and imposes none on any hand. |

**The DRAFT trace is a "considered and passed" line — named out loud, and why it
is permitted here.** *(Added after `pipeline-redcheck` Finding D — the doc builds
at §9 #1 the exact record it quotes a prohibition against at §4a.)* The
`[hand:engine] DRAFT:` entry (#1) is, precisely, the "considered and passed" line
PROXY §3b forbade for the observer's own ledger. The two are not in contradiction,
but the distinction is load-bearing and must be stated rather than left for the
reader to reconcile: PROXY §3b forbids such a line **as a per-item stamp implying
the reader OWES a look** (a push that manufactures obligation); §9 #1's DRAFT is
**pull-not-push** — it sits in the engine's world-readable journal, costs the
human nothing unless sought (DW §4 reason iii), and is guarded by **PIPE-F3
(§11)**, which fires the instant it starts pressing the operator's span (becoming
a second inbox). The permission is entirely carried by that pull-not-push
property plus PIPE-F3's collector; if either fails, the DRAFT trace *is* the grave
it resembles, and PIPE-F3 is the collector that catches it.

**Explicitly NOT changed:** DW §1c stays exactly as written — races-allowed, no
window, no priority. This document adds no courtesy window, no staleness timer,
and no seat-side deferral rule; §5 explains why (all three are barrier mechanisms
that fail the no-rule-to-remember test). And **WORLD.md is not touched** beyond
DW's single inherited amendment (§8). §2 (routing), §3 (auto-answer ritual), §5
(training), §6 (override), §7 (kill), §8 (invariants), §10 (falsifiers) are
inherited whole; this document's §4/§5/§7/§11 re-derive them under the pipeline
framing and confirm they hold.

---

## 10. Priced implementation sketch — ordered, each step with its verification

Built on DW §9's sketch; the pipeline adds only the standardized DRAFT shape and
three drills that *prove the barrier is not present* (that engine-down, -slow,
and -wedged all leave the human's ritual identical to today). There is no
courtesy-window step because there is no courtesy window. Steps 1–5 and 9–12 are
DW's, unchanged; the new/changed steps are marked **[PIPE]**.

| # | actor | step | verify |
|---|---|---|---|
| 1 | **[human]** | Write the STANDING GOALS grants entry (DW §9 #1) — scope, provenance, threshold, enable. **Blocking.** | entry exists; every line quoted or human-typed (DEC §6 F7, once) |
| 2 | **[hardener]** | Write `.swarm/briefs/decision-engine.md` (DW §9 #3) **[PIPE]: plus the engine-first *tendency* sentence (§9 #2 — content, not a duty; the engine holds no window and imposes no deferral), the standardized `DRAFT:` entry shape (§9 #1), and the hard rule that the engine NEVER records S1.5 (no read-marker, no hold during deliberation — §4a)** | parent reads it against DW + this doc; the tendency sentence, the DRAFT shape, and the never-record-S1.5 rule all present; NO deferral/window duty present |
| 3 | **[seat]** | `swarm spawn decision-engine` (DW §9 #4); seat-take entry in the operator journal | `ps` shows it; `[hand:engine]` seat entry in operator journal |
| 4 | **[engine]** | Shadow stint — enumerate + journal would-answers, touch nothing | seat compares shadow list to its mailbox read; `queue/operator/` untouched; **no S1.5 marker written anywhere (§4a)** |
| 5 | **[engine]** | First live auto-answer on one granted item | DW §9 step 5 chain check (delivered + claim line + asker record + marker/grant + ledger entry) |
| 6 | **[seat]** **[PIPE]** | **No-barrier drill (engine LIVE): an item arrives; the human drains it *immediately*, without checking the engine.** | the human's drain succeeds with no deferral, no check, no wait; if the engine had begun a claim, its `mv` aborts (DW §1c) and exactly one claim line lands (W-F8's collector); **proves the item was never gated** |
| 7 | **[seat]** **[PIPE]** | **Fail-open drill: kill the engine pane, then an item arrives.** | seat drains exactly as SEAT §3 (engine not live ⇒ no rule active); **PIPE-F1 collector run once — human load NOT increased, no rule remembered** |
| 8 | **[seat]** **[PIPE]** | **Wedged drill: engine live in `ps` but not acting; item arrives.** | seat drains immediately; the item was never held or delayed by the engine (races-allowed); no jam, no timer consulted |
| 9 | **[seat]** | DW crash/race/fourth-state drills (DW §9 steps 6–8) | unchanged from DW |
| 10 | **[human+seat]** | Override drill (DW §9 step 9) | unchanged from DW |
| 11 | **[engine]** | First retrain + manifest (DW §9 step 10) | unchanged from DW |
| 12 | **[adopt gate]** | After ~2 weeks / ~30 answers (DEC §5.4): human reads §11 numbers, adopts / narrows / kills. **On adopt:** hardener ships the DW SKILL bullet + WORLD amendment (DW §9 #2/#7), unchanged — **no pipeline-specific SKILL line, because the seat ritual is not modified (there is no deferral rule to add).** On kill: delete grants, close engine — nothing else exists. | I1–I4 per §7 table; the pipeline adds no doctrine to SKILL.md beyond DW's own bullet |

The pipeline adds **three drill steps** (6, 7, 8) over DW — all of which *prove
the absence* of a barrier — and **zero SKILL lines** beyond DW's. Everything else
is DW.

---

## 11. Falsifiers — each with a named collector

DW's W-F1–W-F8 and DEC's F1–F7 remain in force, unchanged. The pipeline adds
two, aimed squarely at the two hazards the operator named:

1. **PIPE-F1 — the barrier bites: engine-down INCREASES human load.** ANY of:
   an operator item that a human could not drain by SEAT §3 because the engine
   was down/slow/wedged; a human who had to remember or invoke a pipeline rule
   (check liveness, consult a timer, wait a window, use a drain verb) to drain;
   a jam, lock, hold, or gate in front of the mailbox attributable to the engine.
   **Collector:** the seat's per-stint review against the §7 failure table, plus
   the human (who owns the load). **Fires ⇒ the prime invariant (DW §8) is
   violated — a barrier mechanism has crept in. Remove it and revert to pure
   races-allowed (DW §1c, which this design never left) before restoring the
   engine.** This is the falsifier the brief demanded: it fires the instant any
   ordering mechanism has appeared on the operator mailbox.

2. **PIPE-F2 — an ON-DISK tracking state rots with no consumer: the grave
   reopens.** ANY of: a per-item status field, a `rendered/`/`read/` folder, a
   `pipeline-state.json` or equivalent, an on-disk S1.5 read-marker, or any
   record whose states a mover advances on the operator queue; OR a pipeline
   state (§4) observed with no consumer acting on it (e.g. a "pass" trace nobody
   ever reads that accumulates). **Collector:** any hand — the §4 state table is
   world-readable, and any such file shows up in `git status` / a reconcile grep;
   the seat notices accumulating unread traces at stint review. **Fires ⇒
   SIMPLEST §2 row 13 / INBOX NOT-8 is reopening — delete the state-bearing
   record; the trace must be derived from existing records (ledger, `ps`,
   journals) or not exist.** This is the grave-reopening falsifier the brief
   demanded — **for on-disk records.**
   **Stated blind spot (the `pipeline-redcheck` KILL): PIPE-F2 sees only files.
   It CANNOT catch a private in-memory read-marker** — the engine noting to
   itself "I read item X" and timing its claim on that private state. That leaks
   no file, no git delta, no grep hit, and PIPE-F1 sees it only if it distorts
   *human load*. This is the one S1.5 record no collector detects; §4a accepts it
   as a discipline-bounded residual (bounded because the private timing changes
   only which hand wins a race, never what is answered or under what authority —
   grants still gate). Do not read this falsifier as total coverage of S1.5; it
   covers the on-disk case only, and the doc says so rather than implying more.

3. **PIPE-F3 — the DRAFT trace presses the operator's span.** The standardized
   `[hand:engine] DRAFT:` pass-through entries (§9 #1) accumulate into something
   the human feels obliged to read — the trace becoming a second inbox rather
   than a costs-nothing-unless-sought journal note (DW §4 reason iii). **This is
   the one place "tracked" could quietly re-grow the operator's load.**
   **Collector:** the human, who owns the span (C20/C21, DW W-F7's shape); the
   seat notices if it starts routing DRAFT entries to the human's attention
   rather than leaving them in the engine's world-readable journal. **Fires ⇒
   the trace has stopped being derived-and-optional and become a surface the
   human must process — stop emitting it, or confirm (per INBOX E2) that the
   human explicitly wants it; the trace exists to be there when sought, never to
   be pushed.** (Note this is the pass-path analog of DW W-F7 and PROXY P-F7 —
   the engine pressing the span it exists to relieve.)

---

## 12. The one decision only the operator can make

Everything above turns on one word in the ask: **"guarantee."** It has two
readings, they are genuinely different asks, and the design cannot decide between
them for the operator. Here they are priced **symmetrically** — each with what it
delivers and what it costs — with no thumb on the scale; the recommendation
comes *after*, as its own line, so the operator sees the choice before they see
the lean. *(Reframed after `pipeline-redcheck` Finding B, which caught the first
draft presenting one reading as "do not" and the other as "already delivers,
soundly" — a fork the doc had already picked. The prices below are stated
even-handedly; the durable argument, not the perishable code fact, carries the
weight.)*

- **Reading 1 — "guarantee" = HARD ordering:** the engine provably reads each
  operator item before any human hand can act, auditable after the fact.
  *Delivers:* the operator never has to wonder whether the engine considered an
  item — it is structurally certain it did. *Costs:* the engine becomes a
  mandatory reader on the operator's own mailbox — a single point of failure that
  breaks "Promptness is best-effort" (WORLD:54) when it wedges (the durable
  reason, §5b; true regardless of code). On today's substrate it is additionally
  *unbuildable*: no delivery path exists to order two hands (bin/swarm:610-611),
  so every mechanism reduces to a lock, a timer, a liveness-gated drain, or a
  recorded S1.5 — each a rule the human must remember under stress, a jam when the
  engine dies, or a reopened grave (§5b, §4a). The record also shows no demand
  for the ordering it buys (INBOX §1d: zero misorderings, zero backlogs in the
  entire operator corpus).

- **Reading 2 — "guarantee" = "reliably handles these because always watching":**
  the always-awake engine reads the mechanical share first as a tendency, and the
  human never waits on it. *Delivers:* the engine reads the mechanical share
  before a human spends attention on it, for as long as it is alive; the trace is
  the ledger, `ps`, and the engine's journal the operator already has. *Costs:*
  "usually," not "always" — the engine can lose a race (a human draining first)
  and, when down, does nothing; the operator gets no structural certainty that a
  given item was engine-considered before they saw it (§5e's residual). This is
  DW's engine-hand, and it is buildable today at zero new contract cost.

**Why the operator may keep asking — engaged, not dismissed.** This is the
*third* time the operator has asked for something stronger on this axis
(DECISION-WIRING → PROXY-WIRING → this), each time scoped down further — from "the
whole message plane" to "just operator escalations." That pattern is a signal
worth taking seriously: the operator is circling a real want, and the honest
name for it is probably **"I don't want to have to think about whether the engine
did its job."** Reading 2 answers that *partly* — the DRAFT trace (§9 #1) is
present for every passed item, so the operator *can* confirm at a glance that the
engine considered something and chose to pass — but it answers it by *pull* (the
trace is there when sought), never by the *structural certainty* Reading 1 names.
If what the operator wants is that certainty, this document's answer is that the
substrate cannot give it without becoming a barrier — and that is the thing to
decide, eyes open, not to route around.

**The recommendation, stated as its own line and separable from the fork above:**
absent a signal that Reading 1's structural certainty is what the operator
requires, **take Reading 2** — it survives the maps, it is the only one buildable
without breaking a load-bearing promise, and its residual (no structural
certainty) is the one the record shows costs the operator nothing today. If the
operator reads the fork and says "no, I meant the certainty" — then the answer is
the PROXY §2d answer: *do not*, and here is exactly why (§5b, §8). The fork is
real; my lean is Reading 2; the choice is the operator's.

---

## Summary for pipeline-scout

The operator's third iteration — a sequential, tracked pipeline for
operator-bound escalations — is **DW's engine-hand, delivered as races-allowed
with the engine winning because it never sleeps, plus a standardized derived
trace**, and it AMENDS DW in two small places (§9) rather than superseding it.
On the operator's central word, **"guarantee," the recommendation is AGAINST the
literal ask** — for a durable reason and a corroborating one. The durable reason
(true regardless of any code detail): a hard engine-first guarantee makes the
engine a single point of failure on the operator's own mailbox, breaking
"Promptness is best-effort" (WORLD:54) when it wedges — PROXY §2b's SPOF scoped to
one mailbox. The corroborating fact (true on today's substrate): the tool never
delivers to the operator queue (bin/swarm:610-611), so there is no path to order
two hands at all — every ordering mechanism is a lock, a staleness timer, a
liveness-gated drain, or a recorded deliberation state, each of which either jams
the mailbox when the engine dies, forces the human to remember a rule under
stress, or reopens the grave; and the one honest fail-open
(free-for-all on any staleness/liveness signal) *dissolves* the hard guarantee
into plain races-allowed. So the design delivers engine-first's **value** (the
always-awake engine reads the mechanical share first) without a courtesy window,
timer, or any deferral mechanism — because those are themselves barrier
mechanisms that fail the "no rule to remember" test — and it passes that test
trivially: engine-down presents the human the same surface and the same action
as today, with no rule to suspend (§5). The GRAVE stays shut: every pipeline
state maps to a consumer DW already defined, and the one state the guarantee
would force onto the wire — "engine reading, not yet ruled" (S1.5) — is kept off
the wire by the engine's briefed discipline, so the trace is entirely derived
from the ledger / `ps` / journals and the message file is byte-untouched — no
`rendered/`/`read/`, no status field, no on-disk read-marker, no hold, no mover
manufacturing claims (§4, against INBOX NOT-8 / SIMPLEST row 13). **The one
honest residual, stated plainly (the `pipeline-redcheck` KILL): S1.5's
off-the-wire-ness is a discipline, not a code guarantee like I1 — a private
in-memory read-marker is neither prevented by code nor caught by PIPE-F2, and is
accepted in writing as a bounded residual (§4a), exactly as DW §2c lives with
its unauditable threshold.** CONTRACT-CLASS: DW's one inherited
mailbox amendment covers the races-allowed form **unchanged, with zero new
mandatory contract touches**; the hard form would strain "wait until looked at"
and break "Promptness is best-effort" (WORLD:54) into a lie — a decisive
asymmetry (§8); the engine-first *tendency* is described in the engine brief as
content, never in WORLD.md as contract. Two new falsifiers fire on exactly the
two hazards: PIPE-F1 if engine-down (or any crept-in ordering mechanism) ever
increases human load (the barrier biting), PIPE-F2 if any tracking state rots
with no consumer (the grave reopening); PIPE-F3 guards the one place "tracked"
could re-grow the span — the DRAFT trace. **Where I recommend against the
operator's framing:** the word "guarantee" — engine-first is a tendency of the
standing watch, not a guarantee, and §5e/§12 state the gap and the operator's
one decision in the open. This document survived two adversarial
passes, both part of its provenance: `pipeline-red` (the drafter's own child, 2
WOUND / 1 CONFIRM — the courtesy window I first drafted was itself a barrier
mechanism, struck) and the independent `pipeline-redcheck` (spawned by the parent
to catch the shared blind spot, 1 KILL / 2 WOUND / 3 CONFIRM — it downgraded
"S1.5 is *structurally* unstateable" to the honest "discipline-bounded, and
PIPE-F2 is blind to the in-memory case," corrected a rotted bin/swarm cite that
both earlier reviewers had copied, and made §12 a symmetric fork with a
separable recommendation). Neither pass changed the recommendation; both made the
doc honest where it had over-claimed. Everything the engine can break, it can
only break for items it answered, in its own name, on a record any hand can
audit; for the operator's own mailbox, engine-down is byte-identical to
engine-absent, by construction — which is the whole point. The one residual the
operator should hear plainly: "reads first" is kept off the wire by the engine's
discipline, not by code — a private in-memory read-marker is uncollectable, and
this document accepts that as a bounded residual rather than dress it in a
stronger word.
