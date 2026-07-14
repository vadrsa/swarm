# PROXY-WIRING — does the decision engine generalize to the whole message plane?

> SUPERSEDED by HOOK-WIRING.md §13, which answers PROXY-WIRING's own question ("does it generalize to the whole plane") oppositely (yes, via admission control) to what PROXY-WIRING recommended (observe-only); kept for the record (the interposition-safety asymmetry analysis and measured plane volume).

**Author:** `proxy-drafter`, for `proxy-scout`. Written at `main@834fec4`,
2026-07-11; revised same day after adversarial review by `red-proxy`
(0 KILL, 7 WOUND, 7 minor citation findings —
`.swarm/research/red-proxy-review.md`); the revision notes at repaired
sites say what changed. Answers the operator's ask (verbatim in §0a) of whether a
proxy can intercept **every** message — agent-to-agent and operator-bound —
predict whether the operator would want it surfaced, and attach a predicted
decision. The two prediction engines (surfacing predictor, response
predictor) are ASSUMED to exist per the brief; whether to build them is not
this document's question. This document decides the WIRING: the interposed
form the ask describes, versus an observational form that reads the message
plane after the fact. It inherits DECISION-WIRING's invariants and rituals
(cited as `DW §n`) rather than reinventing them.

**Evidence discipline:** every load-bearing claim cites
`.swarm/research/wiring-surfaces.md` (`SURF §n`), `docs/design/DECISIONS.md`
(`DEC §n`), `docs/design/DECISION-WIRING.md` (`DW §n`),
`.swarm/research/ledger-miner-decisions.md` (`LM §n`), `WORLD.md` line refs
(`W:n`), `docs/PHILOSOPHY.md` (`PHIL §n`), or a `bin/swarm:line` at main.
Volume numbers were measured by this author over `.swarm/queue/*/delivered/`
on 2026-07-11 and are marked MEASURED; the method is stated where used.

**The recommendation in one paragraph.** **Observational, decided.** Messages
flow exactly as today — zero bytes, zero hops, zero latency added to any
wire. The operator-bound direction is already wired: DECISION-WIRING's
engine-hand IS the response predictor for the operator mailbox, unchanged
here (DW §1–§4). This document adds exactly one thing: a read-only
**observer duty** — run during the pilot as a per-stint batch read, zero
standing cost; a standing `plane-observer` agent only if the pilot's
numbers earn it (§3b) — that reads the world-readable message record
(`queue/*/delivered/`, journals — W:17-25, W:26-29) after delivery, runs the
surfacing predictor over agent-to-agent traffic, and appends `SURFACED`
entries — each carrying a predicted decision as a draft — to its ledger,
which the seat reads at stint time and routes by ordinary seat judgment.
Nothing pushes to the human (W:58); no draft ever touches a message or the
wire (DW §4's invariant, kept); the observer answers no one and delays
nothing, which is tighter than DW's grant ledger and §6 says why. The
interposed form the ask describes is killed in §2 on grounds the maps force:
the two message directions are structurally asymmetric — the operator
mailbox has no delivery code for a hand to be added beside (bin/swarm:610-611,
SURF §1c), while every agent queue has live delivery code running today
(bin/swarm:331-339, SURF §1b) — so an interposed proxy on the plane must
either edit the delivery path (CONTRACT-CLASS on "delivered means delivered"
for every message in the system, W:51-53) or re-deliver under its own or a
forged identity, erasing the true sender's relation and turn-record from
the contracted surfaces (§1c). The
observational form delivers every outcome the ask names except one — holding
delivery until the operator looks — and §2d argues from the record that the
operator does not use and doctrine forbids that one. CONTRACT-CLASS bill for
the recommended form: **zero new items** (§8 carries DW's one inherited
amendment, unchanged, scoped to the operator mailbox only).

---

## 0a. The operator's ask, verbatim

*(Added after red-proxy W2 — the preamble promised this section and the
first draft omitted it. Every "the ask's own words" argument below (§2, §2d,
§6) is checkable against this text without leaving the document. Canonical
source: the brief carried in `.swarm/settings/proxy-drafter.task`, re-read
verbatim by red-proxy.)*

> "Can we intercept any message written from and to anyone, in separate
> places, where a proxy takes, proxies, and passes through the message? For
> an agent-to-agent message, first predict: would the operator want this
> message surfaced to them? If no, send it on to the recipient. If yes,
> surface it, and also predict how the operator would respond — what
> decision they would make. Same for messages to the operator."

Read for §2d before it is argued: the no-branch says "send it on" —
verbatim; the yes-branch says *surface*, not *hold*.

---

## 1. The asymmetry, verified (the hypothesis test the brief demanded)

The parent's hypothesis: the two directions are not symmetric, because
DW's hand-shape worked only where no delivery code exists, and every
agent-to-agent queue already has live delivery code. I verified this against
SURF §6.1, §6.2, §6.6, §6.9 as instructed. **Verdict: confirmed in
substance, refined in one place — and the refinement is reported, not
buried.**

### 1a. Why the engine-hand shape worked at the operator mailbox

DW's proxy is byte-identical-to-absent on pass-through (DW §8 I3) because of
one mechanical fact: **the tool never delivers to the operator queue.**
`cmd_deliver` exits immediately for the operator (bin/swarm:610-611, verified
live by this author; SURF §1c), and the only code that ever moves a file into
`delivered/` is `deliver_once`, unreachable for that queue (bin/swarm:336-337,
SURF §1c). A message to the operator is a durable file that sits **unclaimed,
indefinitely**, until a reader's hand moves it (W:57-61). A hand added to
that mailbox is purely additive: it claims what it covers and its absence
changes nothing.

### 1b. No such idle file exists anywhere else on the plane

For every other recipient, delivery is live code running today with no engine:
`deliver_once` injects exactly one message per turn, oldest first, and moves
the file to `delivered/` only after the bytes drained (bin/swarm:331-339,
SURF §1b; W:51-53). The window between `queue_put` and delivery is the gap
before the recipient's next turn — the doorbell rings it immediately
(bin/swarm:922-925, SURF §1a). There is no unclaimed file waiting for a hand;
there is a file already owned by the delivery path, in flight.

### 1c. The four candidate surfaces, checked one by one

- **SURF §6.1 (inside `cmd_send`):** attaches only by editing bin/swarm's
  send path or by a PATH-shadowing wrapper that is "per-seat and invisible to
  the repo" (SURF §6.1 ATTACHES). Editing the path puts engine code between
  every sender and `queue_put` — engine failure becomes send failure, the
  degradation DW §1b already called the dirtiest possible. Redirecting `to`
  toward a proxy means the true recipient's `delivered/` never records the
  sender's message consuming a turn (W:17-25, concept 4) and the proxy's
  re-send arrives under the proxy's name and relation, not the sender's
  (relation is computed structurally, bin/swarm:147-163, SURF §1d) — unless
  the proxy forges `SWARM_AGENT_ID`, which the appendix of SURF names for
  what it is. **Requires editing the delivery path or forging identity.
  Hypothesis holds here.**
- **SURF §6.2 (directory watcher):** on the operator queue this was DW's
  winning shape. On an agent queue it races live `deliver_once`: to interpose
  it must move files out of a queue the tool owns, and W:20-22 is explicit —
  "Never move your own queue files — delivery is the tool's job, and a file
  moved by hand makes that record claim a turn that never happened."
  (Stated precisely, per red-proxy's minor sweep: the quoted letter bans
  moving your *own* queue files, and an interposing watcher moves *another
  agent's* — a case the letter does not literally reach; what covers it is
  the sentence's own rationale clause, true of any mover, plus the general
  rule that for agent queues delivery is the tool's job.) The
  operator queue is the contract's *stated exception* (W:59-61, SURF §1c);
  agent queues have no exception. And the race is unwinnable by design: the
  watcher cannot guarantee it beats the doorbell-triggered delivery, so
  interposition-by-watcher is not even reliable interception. **Observational
  reading of `delivered/` is legal here (that is this design); interposition
  is not. Hypothesis holds here.**
- **SURF §6.6 (sender-side hooks):** the map's own words — the wired hook
  events "cannot intercept `swarm send` itself on these four events (send is
  a CLI call mid-turn, not a hook)" (SURF §6.6). Observation of transcripts,
  yes; interception, no. **Hypothesis holds here.**
- **SURF §6.9 (PreToolUse / PermissionRequest):** **here the hypothesis's
  strong form is technically false, and I am saying so as instructed.** A
  PreToolUse hook via user-level `~/.claude/settings.local.json` reaches every
  session with zero bin/swarm edits (SURF §2a, §6.9 ATTACHES) and can block
  the literal `swarm send <agent> …` before the CLI runs. A send-side
  interception point for agent-to-agent mail that does not edit the delivery
  path therefore EXISTS. But follow it one step further and no interposed
  *proxy* survives it. The map witnesses two hook verbs (SURF §2b —
  exhaustiveness over the harness's hook API is not verified; any third
  verb, rewrite or redirect, lands in 6.1's kills): **allow** — in which
  case nothing was intercepted — or **deny**, followed by the proxy
  forwarding the message itself. *(Rewritten after red-proxy W3: the first
  draft killed the deny branch on silent-drop grounds — "a denied send has
  no file at all" — and that leg is defeatable: a denying hook runs with
  the sender's own pane env (SURF §2b), so it can `swarm send` a durable
  buffer file as the true sender before exiting 2, and the crash ordering
  is fail-safe — crash before the buffer and the original send proceeds;
  crash after and the result is a visible duplicate, never a silent drop.
  The kill does not need that leg.)* What actually kills deny-then-forward,
  each leg independently sufficient: **(i)** the forward arrives under the
  proxy's name and relation, or under a forged `SWARM_AGENT_ID` — identity
  laundering as a steady-state mechanism (SURF appendix); **(ii)** the true
  recipient's `delivered/` never records the sender's message consuming a
  turn — the world-readable record concept 4 promises (W:17-25) goes false
  for every proxied message; **(iii)** the wiring lives in the user's
  personal settings file, outside the repo's own record — the objection DW
  §1b already used to kill 6.3; and on top, every sender's send now ends in
  a tool denial it must interpret. **Refined finding: an interception point
  exists; an interposed proxy does not survive it — every 6.9 variant
  either degenerates to observation or launders identity and falsifies the
  delivered-record.**

### 1d. The asymmetry, stated as the finding

**Confirmed:** there is no geometry on this plane where an interposed proxy
gets what DW's engine-hand got at the operator mailbox — a durable,
unclaimed, pre-delivery file that a hand can claim additively. Agent-to-agent
mail offers only: a file already owned by live delivery code (6.1/6.2), a
pre-CLI gate whose only interposition path launders identity and falsifies
the delivered-record (6.9), or the file after delivery (6.8 — observation).
The first two each break promises made for **every message in the system**;
the third is this design. DW priced its one
contract touch against one sentence-pair about one mailbox (DW §9); an
interposed plane proxy re-prices "delivered means delivered" itself. That is
not a bigger version of the same decision — it is a different and worse one,
and it is the central reason the recommendation is observational.

---

## 2. The interposed form, killed honestly (and what of the ask survives)

The ask's outcomes (§0a), enumerated: (a) irrelevant agent-to-agent mail flows
untouched; (b) mail the operator would want to see reaches them, with a
predicted decision attached; (c) operator-bound mail is answered as the
operator would answer, or surfaced with a draft. The interposed form buys
(a)–(c) plus one thing the observational form cannot: **withholding delivery
until the operator has looked.** Price the whole package:

### 2a. Turn economics (MEASURED)

Method: counted `*.json` under `.swarm/queue/*/delivered/` excluding
`operator/`, on 2026-07-11; timestamps span 1783622783005 → 1783713285681 ms.

- **133 plane-wide delivered messages over ~25.1h ≈ 127/day** — the number
  interposition must be priced on, since the ask (§0a) covers every message.
  *(Label corrected after red-proxy W1, which independently reproduced the
  arithmetic:)* of the 133, **21 are operator-authored seat dispatches and
  112 are true agent-to-agent** — the observer's actual read corpus, since
  §3a exempts operator-authored mail from both predictors. Against 37
  lifetime operator-bound (35 at LM's corpus close, LM §1): the plane is
  **~3.6× the operator mailbox, the observer's corpus ~3.0×**, and both
  ratios grow with tree size: plane volume scales with agent count,
  operator volume with one human.
- Delivery is one message per turn (W:17-19). An interposed hop converts
  every message into **two** messages (sender→proxy, proxy→recipient) —
  doubling the delivered/ record — and inserts a proxy turn into every
  delivery: ring latency plus a full model turn, per message, ~127 times a
  day at today's volume.
- Worse than the added latency is the **serialization**: all plane traffic
  funnels through one proxy queue, delivered to the proxy one-per-turn,
  oldest first (bin/swarm:184-190 via SURF §1b). Concurrent conversations
  between disjoint agent pairs — parallel today — queue behind each other
  inside the proxy. The swarm's message plane is parallel by construction;
  the interposed proxy makes it serial.

### 2b. The single point of failure

DW §8's guarantee is "the engine can only ever subtract itself." An
interposed plane proxy inverts it: proxy wedged = **every message in the
system stops**, and the doorbell note's own warning applies to the whole
plane at once — mail to a closed or dead proxy "will never be delivered"
(bin/swarm:926-930, SURF §1a). No falsifier collects fast enough to make
that acceptable; the failure is the outage.

### 2c. Relations and identity

Every re-sent message arrives headed `from <proxy> — sibling` instead of the
true sender and relation (bin/swarm:147-163, 210-212; SURF §1b, §1d).
The tree's authority structure — parent/child/sibling/OPERATOR headers —
is how recipients weigh messages (W:17-19). The proxy either erases that
structure on every message or forges `SWARM_AGENT_ID` per message (SURF
appendix) — identity laundering as a steady-state mechanism.

### 2d. The one capability lost, priced against the record

Withholding delivery until the operator looks is a **veto gate on the
tree's internal mail**. The record says the operator does not operate that
way: their genuine judgment appears as initiations and corrections after
reading, never as gate-answers (LM §3.4, DEC §1c); the one decision that
aged, aged correctly (DEC §4c). A veto gate presses operator attention into
the hot path of every conversation — the exact inversion of PHIL §9, the
operator's second instruction in the entire project: keep the operator's
channel clean of work the tree can do. And the ask's own words (§0a) do not
demand it: "if no, send it on" — and
if yes, *surface* it; surfacing does not require holding. Reading the ask as
copy-on-surface rather than hold-on-surface honors every stated outcome and
is the only reading that survives the contract. If the operator does want a
hold, that is a new contract negotiation (W:51-56 rewritten for every
message), and this document's honest advice is: do not.

### 2e. Verdict

Interposed dies on §1's structural ground before its economics are even
reached; §2a–§2c are what it would cost even if it didn't. Killed.

---

## 3. The recommended wiring: observational, two components

### 3a. Component 1 — operator-bound direction: DECISION-WIRING, unchanged

The response predictor for operator-bound mail **is** DW's engine-hand:
grant-gated auto-answers in its own wire name, pass-through as absence,
byte-identical to engine-absent (DW §2c, §3, §4, §8). Nothing here amends
it. The surfacing predictor is moot for this direction: a message addressed
to `operator` was surfaced *by its sender* — the addressing is the
declaration (DEC §3). What this document adds for this direction is one
formalization DW already sanctioned: for pass-throughs, the engine MAY write
a **draft entry in its own journal** — DW §4 killed the dossier on the
human's surface but said in the same section that "anything worth saying
about a near-miss belongs in the engine's own journal, which is
world-readable anyway and costs the human nothing unless sought" (DW §4
reason iii). §4 below gives that entry a standard grep-able shape so the
seat can find it when the human wants a one-word ratification. Prioritizing
or triaging the operator's mailbox is explicitly NOT reopened — the inbox
problem was researched and found not to exist yet (inbox-scout's verdict,
delivered at LM §1 row 25 and carried in INBOX.md; attribution corrected
per red-proxy's minor sweep); nothing here ranks the human's mail.

Messages **from** the operator need no proxy stage in either direction:
they are the human's own words — surfacing them to their author is circular,
and predicting the author's response to their own message is meaningless.
They enter this design only as training history for both predictors (§7).

### 3b. Component 2 — agent-to-agent direction: the observer duty

*(Rewritten after red-proxy W6: the first draft opened with "one new
standing agent," asserted rather than argued. DW earned its standing hand
on latency — answering the mechanical share while the human is away (DW
§1a.4) — and that argument does not transplant: this observer answers no
one, delays no one, and its output is consumed only at stint time; nothing
reads it between stints and nothing pushes (W:58). And PHIL §8's standing
bias — "prompt-level convention first, a visibility verb second, an engine
never — unless the record shows the convention failing" — cuts against a
warm pane no convention has yet earned.)*

The observer is a **duty, not (yet) an agent**: a per-stint batch read.
During the pilot it runs as one step of the seat's stint, under the
charter's authority alone (the DW step-12 pattern: doctrine text ships at
adoption) — zero standing pane, zero standing tokens, and the identical
`SURFACED` output at the identical consumption moment. Its ledger during
the pilot is the operator journal, entries tagged `[observer]` — the
one-journal discipline DW step 3 enforced for seat-visible breadcrumbs. A
standing `plane-observer` agent (spawned like any agent, with pane, journal,
doorbell — SURF §3, §4; its own journal then becomes the ledger) is the
**post-pilot option the numbers must earn**: the one fact that would
justify a warm pane is evidence that surfaced items are time-sensitive
between stints, and the pilot's ledger will show that or it won't. In
either form the observer is **not a hand on any seat** — it claims nothing,
moves nothing, drains nothing. The duty cycle, per stint:

1. **Read** — new files under `queue/*/delivered/` since the last watermark
   (a line in the ledger) — **excluding `queue/operator/` (DW's surface,
   not this duty's) and `from=operator` files (the seat's own dispatches,
   exempted by §3a; scoping per red-proxy W1)** — plus journals for
   context. All world-readable today (W:17-25 concept 4, W:26-29 concept 5;
   SURF §6.8); reading is zero new exposure — the brief's tension 5, first
   half, resolved by the contract as it stands.
2. **Predict** — run the surfacing predictor per message: would the operator
   want this surfaced? Below threshold: **write nothing**. No entry, no
   count, no "considered and passed" line — the pass-through-is-absence
   invariant (DW §8 I3) applied to the observer's own ledger, so that its
   output stays proportional to what the operator would actually read.
   (What this costs in auditability, P-F8's sampled miss-audit pays back —
   §9.)
3. **Surface** — above threshold: append one `SURFACED` entry to the ledger
   (shape in §4), running the response predictor to attach the predicted
   decision as a draft.
4. **Batch note** — one watermark line closing the stint (files-read range),
   so staleness is an observable fact (W:26-29).

The economics of this shape are the mirror image of §2a: a file reader is
not bound by one-message-per-turn — that is a *delivery* constraint, not a
read constraint. The observer reads a day's plane traffic in a handful of
turns (during the pilot, inside a stint the seat is running anyway), in
parallel with everything, adding zero latency to any message.

**How surfaced items reach the human — pull, never push (W:58):** the seat's
stint ritual gains one line (the SKILL bullet, §8): grep the observer
ledger for `SURFACED` entries since the last stint, and route them by
ordinary seat judgment — desk, dispatch, dismissal, or escalation. The
observer duty sends nothing to anyone — during the pilot it is a stint step
with no wire identity of its own; a promoted standing observer sends
unsolicited mail to **no one** (the falsifier P-F1 makes that a kill
condition), may answer mail addressed to it (it has a queue like any
agent), and is harvested like any child.

**The answering engine and the surfacing observer stay separate — separate
briefs, and if the observer is ever promoted, separate agents.** The duties
differ in authority (grants vs none), kill semantics (§7), and failure
blast radius, and separation makes the observer's no-answer-authority bound
*structural* — its brief and stint step simply contain no answer ritual, so
scope creep requires a re-brief, not a drift. That is DEC §1d's lesson
applied to agent shape: narrow authority is what buys the delay in which
attention can act. *(Citation swapped after red-proxy W7 — the first draft
cited PHIL §5 here, whose recorded instances all delete distinctions rather
than preserve them; the substance stands on DEC §1d.)* `decision-engine`
never runs the surfacing duty, and nothing that runs the surfacing duty
holds a grant.

---

## 4. Where the drafts live (the pass-through collision, resolved)

The collision: DW §4's invariant — pass-through byte-identical to
engine-absent — versus the ask's "surfaced messages carry a predicted
decision." Resolution: **the message never carries anything; the draft is a
parallel ledger entry keyed to the message's queue filename.** Queue
filenames are `{ts}-{from}.json`, unique within a queue by O_EXCL
construction (bin/swarm:265-275, SURF §0), so the global key is
`<recipient>/<filename>`. The entry shapes, grep-able like claim lines:

```
## <date> — SURFACED: queue/<recipient>/delivered/<ts>-<from>.json
why: <one line — what the operator would want to see in it>
predicted decision: <the draft the human can ratify with one word>
confidence: <c> (informational; authority is a human word, never this number)
status: OPEN
```

in the observer ledger for agent-to-agent mail (§3b: the operator journal,
`[observer]`-tagged, during the pilot; the standing observer's own journal
if promoted), and

```
## <date> — [hand:engine] DRAFT: <queue filename> (passed through)
predicted decision: <draft>
confidence: <c>
```

in `decision-engine`'s journal for operator-bound pass-throughs (the DW §4
journal note, given a standard shape — an extension of DW, marked as such).

Rules, inherited and hard:

- **Never on the message, never on the wire, never on the desk.** The
  message file stays byte-identical to engine-absent (DW §8 I3, W-F4's
  collector applies verbatim). The desk stays seat-owned (DW §4).
- **A draft is prose, not authority.** The human ratifies with their own
  word to the seat; the seat executes **citing the human's utterance**
  (provenance rule, DEC §4b.1), never citing the draft. A verdict entry that
  cites a draft as its authority is falsifier P-F4 firing.
- Confidence appears only as engine-authored prose, never a field any tool
  reads (DW §2c storage honesty, inherited).

This gives the operator exactly what they asked for — "predict how the
operator would respond" (§0a), a draft the human can ratify with one word —
with zero bytes on any contracted surface.

**Known gap, flagged not fixed** *(red-proxy minor sweep)*: no inherited
open-loop rule covers `SURFACED` entries — C17's vocabulary is dispatch
entries — so an item surfaced but never routed ages `OPEN` with no owner
and no alarm. P-F7 bounds the volume; nothing yet collects the staleness.
If the pilot shows aged-OPEN accumulation, the adopt-gate decision must
either extend C17's adoption rule to the observer ledger (an extension, to
be marked as such) or drop the `status` field.

---

## 5. The surfacing predictor vs the question-detection grave (argued both ways)

The brief demands honesty here, and the honest answer has a residual.

**The case that the grave stays closed.** Grave 1 died of "misclassification
by design" — a wire-adjacent heuristic guessing decision-ness from surface
because nothing declared it, feeding a mechanism (DEC §2). The surfacing
predictor differs on every axis DEC §2 named as load-bearing: it is
**flag-only** — it never answers, never gates, never delays; messages flow
identically whether it is right, wrong, or dead (miscalibration-safe by
construction, DEC §4a's own words for this corner). It is
**definer-is-consumer in its endpoints**: trained on the operator's recorded
surfacing/dismissal choices, its output read by the operator's own seat,
killable by deleting text — no agent pays a concept, nothing
lands on the wire (DEC §2.2) — though the resolution below owns how far
that claim stretches. And it is **auditable**: every prediction is
a ledger entry whose hit/dismissal outcome the record collects (§9 P-F2),
where the old heuristic's misranking was invisible until someone tripped
on it.

**The case that it reopens the grave, taken seriously.** DEC §4a pre-priced
the flag-only learned reader and still rejected it *today*, on two grounds:
"there is nothing for it to flag that declarations don't already carry,"
and its false-positive budget spends operator attention — the protected
resource. It was to be reached for **only if DEC §6 F2 fires** (a genuine
decision found hiding undeclared). F2 has not fired. Deploying the surfacer
on the plane is therefore **DEC's pre-priced instrument deployed before its
trigger — a marked deviation from DEC's letter**, and universalizing
per-message classification to ~127 messages/day is a much larger surface for
false flags than the operator mailbox ever was.

**The resolution, with its honest limit** *(rewritten after red-proxy W4,
which broke the first draft's distinguisher)*. First, owning what a hostile
reader would otherwise find. The first draft claimed the plane is
"undeclared by definition"; that is false as stated — **sender escalation
IS a plane declaration mechanism** (any agent holding something the
operator would want can `swarm send operator`, and P-F3's own text lists it
first among the channels a justifying hit must beat). So the honest
description of the surfacer is grave 1's opening act: classify from surface
what nobody declared — a net under the escalation channel. And the observer
sits on the wrong side of DEC §3's own read-time-judgment criteria: its
judgment IS a stored label (the `SURFACED` entry), it DOES key a mechanism
(the seat's stint grep, §3b), and the judge is a third party, not the
consumer. What saves the design is therefore not DEC §3's criteria — it is
DEC §4a's already-adjudicated corner: grave 1's recorded cause of death is
misclassification *feeding a mechanism that acts on the guess* (ranking,
answering, gating — DEC §2), and a flag-only reader that feeds nothing but
a journal the seat may grep was named by DEC itself "miscalibration-safe by
construction" and "the smallest legitimate detection" — that, plus
falsifiability (§9), is the whole defense. The deviation that remains is
timing: DEC said deploy it only when F2 fires, and F2 has not fired. The
argument for deviating early is the one that is actually true: **DEC's
wait-for-F2 policy cannot transplant to the plane, because F2's collector
does not exist there.** F2 works at the operator mailbox because the human
eventually reads that mail — an undeclared decision WILL cross live
attention at some stint. Nobody ever reads the plane; a plane F2-analog has
no collector, and its trigger could only fire post-hoc, after harm surfaces
through some other channel. Waiting on a trigger nothing collects is not a
policy. **The pilot IS the F2-collection experiment for the plane, run
under a kill condition:** P-F2 kills on false flags (the DEC F5
price-exceeds-product shape), P-F3 kills on zero utility, and P-F8's
sampled miss-audit measures the recall neither can see. **If the pilot ends
with zero P-F3 hits, the observer dies — and the recorded datum is "this
instrument, under this charter, surfaced nothing the operator used," NEVER
"there was nothing to surface"** *(per red-proxy W5: a blind observer over
a gap-riddled plane produces the same zero as an empty plane; conflating
the instrument-datum with the world-datum would poison exactly the future
decision DEC §4a reserved that datum for)*. The interposed variant of this
predictor — where misclassification would delay or divert delivery —
reopens the grave with delivery authority attached, and is already dead in
§2 for independent reasons.

---

## 6. Authority bounds: tighter than the grant ledger, and why

DW's engine holds the maximum authority this system has ever granted a
machine: answering mail addressed TO the operator, under quoted grants
(DW §3a). The plane needs **less**, and this design grants less:

- **The observer answers no one.** Not under grants, not above any
  confidence, not ever. A grant ledger for plane-answers is not "the same
  shape but wider" — it is categorically new authority: DW's engine answers
  askers who *chose to address the operator's side*, so its answer arrives
  from the seat they knocked on; a proxy answering sibling mail injects the
  operator's predicted voice into conversations nobody routed to the
  operator. No legal grant can carry that: hop-1-and-below traffic is the
  tree's native judgment ("no engine on hop 1", DEC NOT-list 6 — extended
  here from the seat's hop to the whole plane, an extension marked as such),
  and "you cannot pre-authorize an adjudication" (DEC §1a) applies to
  approximately everything siblings say to each other. Why tighter than the
  grant ledger, in one sentence: **grants scope authority the operator
  already had (their own mailbox); the plane was never the operator's to
  answer, so there is nothing to grant.** One precision, so that sentence
  is not misread *(owed per red-proxy's verification of this section)*: the
  operator lacks no plane *authority* — the root reads anything, messages
  anyone under the OPERATOR header, closes anyone. What does not exist is a
  standing *answer role* on the plane to delegate: the record shows the
  operator's plane-judgment as initiations and corrections only (LM §3.4),
  which are DEC §1a's unpre-authorizable class — every intervention right,
  ungranted because ungrantable.
- **The observer delays no one.** Structurally guaranteed, not briefed: it
  sits beside no delivery path (§1), so there is no mechanism by which its
  judgment, latency, or death touches a message's transit. "Promptness is
  best-effort" (W:54-56) keeps exactly today's meaning.
- **The observer's one output is its ledger (§3b).** Writing anywhere else —
  a queue, the desk, the wire — is P-F1, a kill condition.
- **The one grant it does need:** the STANDING GOALS surfacing charter
  (§8 #1) — the operator's own quoted words on what classes of plane traffic
  they want surfaced, with a review trigger. This inherits DEC §4b.1's
  provenance rule whole: no quoted human words, no charter, no observer.
  It bounds *what the observer reads for* — never what it may do, because
  what it may do is fixed at "append journal entries" by construction.

---

## 7. Kill switch, override, degraded modes (inheriting DW §7/§8)

**Kill — two layers, per DW §7, both cheaper here:**

- **Soft kill:** one STANDING GOALS entry freezing the surfacing charter.
  Same cooperation-dependence DW §7 states honestly — it stops a compliant
  observer. But note what non-cooperation costs here versus there: a rogue
  decision-engine issues answers; a rogue observer writes ledger entries
  nobody is obliged to read. The blast radius of the worst case is one
  polluted journal.
- **Hard kill:** during the pilot, the duty exists only as charter text plus
  a stint step — the hard kill is dropping the step (the charter deleted,
  nothing else exists). If a standing `plane-observer` was later earned
  (§3b): `swarm close plane-observer` — pane dies, files stay (W:32), name
  burns (W:14-16). Additionally, the seat-side half of the wiring has its
  own independent off-switch: the seat stops grepping the observer ledger.
  Either side alone fully disconnects the human from the observer's output.

**Override:** a surfaced item the human judges noise gets a one-word
dismissal to the seat; the seat marks the entry's `status: DISMISSED` in a
stint note. During the pilot both live in the same ledger (the operator
journal, §3b) — the status note lands beside the entry; if a standing
observer is promoted, the seat's note stays in the operator journal (never
editing the observer's append-only journal) and the observer mirrors status
on its next read. Dismissals are top-weight negative labels (DW §5's ritual,
inherited: batch retrain per stint plus event-triggered on dismissal;
manifests to `.swarm/engine/observer-manifest-<date>.md` — DW's existing
directory, no new one; the self-training exclusion applies verbatim —
observer-authored entries never train except through a human
ratification/dismissal, DW §5, W-F6's collector extended to these
manifests). A ratified draft is a top-weight positive for the response
predictor, keyed to the human's actual wording so divergence between draft
and ratification is itself a label.

**Degraded modes — DW §8's invariants, applied:**

- **I1 (wire untouched):** stronger here than in DW — the observer has no
  claim ritual at all; there is no file it may move anywhere in the system.
- **I2 (no exclusive holds):** it holds nothing but its watermark; a crash
  mid-stint means some `delivered/` files get read next stint. Nothing waits
  on it.
- **I3 (pass-through is absence):** doubled — messages it declines to
  surface leave no trace on the plane *or in its ledger* (§3b step 2).
- **I4 (authority is text):** the charter is world-readable journal text
  valid with the observer dead; the seat's ritual gains one optional read
  and no dependency — with the observer absent, the seat's stint is today's
  stint exactly.

| failure | invariants | observed result |
|---|---|---|
| duty never run / step dropped / standing observer closed | I1+I3 | today, exactly: the plane never knew it existed |
| wedged / stale | I2 | watermark staleness visible in the ledger (W:26-29); zero messages affected; seat reads an empty grep |
| surfaces garbage | I4 + §7 override | human dismisses; P-F2 counts toward kill; no message was touched |
| drafts leak into authority | §4 rules | P-F4's grep catches a verdict citing a draft without a human's word — freeze the charter |
| goes rogue (sends mail, moves files — standing form) | §7 hard kill | P-F1: any unsolicited send or non-ledger write ⇒ close; the damage is enumerable — its journal and sends are wire-attributed like anyone's |

---

## 8. Exactly what changes

### The priced list

| # | change | size | class |
|---|---|---|---|
| 1 | STANDING GOALS **surfacing charter** in the operator journal: the classes of plane traffic the operator wants surfaced, in their quoted words, plus dismissal-rate calibration line and review trigger (DEC §4b.1 provenance rule) | ~6 lines, human-authored | operator-owned text; zero code |
| 2 | `.swarm/briefs/plane-observer.md` — the duty's brief, whoever runs it (pilot: the seat's stint step; post-pilot: a standing agent): read-only duty cycle (§3b), **read scope excluding `queue/operator/` and `from=operator` files (red-proxy W1)**, entry shapes (§4), the no-send / no-move / ledger-only hard bounds (§6), retrain + manifest ritual (§7), kill semantics | ~100 lines, new file | convention |
| 3 | The observer stint step, run by the seat under the charter (pilot form, §3b); `swarm spawn plane-observer` only post-adoption, if the pilot's numbers earn a standing pane | 0 commands during pilot | none — seat ritual under charter text |
| 4 | skill/SKILL.md, operator-seat section: one bullet — the stint grep of `SURFACED` entries and the route/dismiss ritual; drafts are prose, ratification is the human's word | ~5 lines, 1 file | convention, contract-adjacent (names a seat-ritual step); ships at the adopt gate like DW step 12 |
| 5 | `decision-engine` brief amendment: the standard `DRAFT:` entry shape for pass-throughs (§4) — formalizing what DW §4 already permits | ~5 lines in DW's #3 brief | convention |
| 6 | `.swarm/engine/observer-manifest-<date>.md` — retrain manifests | files in DW's existing dir | convention; world-readable |
| 7 | **Standing cost** *(re-priced after red-proxy W6)*: during the pilot, **zero** — the duty runs inside stints the seat runs anyway (batched reading: a handful of turns per day, not per message). A warm `plane-observer` pane and its tokens (DW §9 #6's honesty) become a cost only if the pilot's evidence — surfaced items proving time-sensitive between stints — earns the promotion | pilot: none; post-pilot: recurring, bounded by `swarm close` = 1 command | the price of plane coverage, deferred until earned |
| 8 | WORLD.md | **zero changes** | — |
| 9 | bin/swarm | **zero lines** | — |
| 10 | hooks (both layers) | **zero changes** | — |

### CONTRACT-CLASS items, in one pass

**This design's own bill: zero.** The observer reads surfaces the contract
already declares world-readable (W:17-25, W:26-29; SURF §6.8), moves
nothing, delivers nothing, answers nothing, pushes nothing to the human
(W:58). No sentence of WORLD.md gains a new reader-role, exception, or
strain. **Inherited, unchanged:** DW's one CONTRACT-CLASS item — the
two-clause mailbox amendment (W:57-61) — belongs to the operator-mailbox
engine-hand and ships at DW's adopt gate (DW §9 step 12); nothing here
widens or depends on it. **Flagged for completeness:** the interposed form
this document rejects would have carried, at minimum, re-pricing W:51-53
(delivered means delivered / no silent drop) and W:17-25 (one-per-turn,
relation headers, delivered-as-record) for **every message in the system**,
plus SURF §6.1/§6.9's flags — that bill, itemized in §1–§2, is the
recommendation's strongest single argument and is stated here so no reader
mistakes "zero" for "nothing was at stake."

### Implementation sketch (ordered; each step with its verification)

| # | actor | step | verify |
|---|---|---|---|
| 1 | human | Write the surfacing charter (#1) — quoted words, calibration, review trigger. **Blocking: nothing runs before this** (DW step 1's gate, inherited) | entry exists; every line quotes or was typed by the human (DEC §6 F7 check, once, by hand) |
| 2 | hardener | Write `.swarm/briefs/plane-observer.md` (#2) | parent reads it against this doc; no-send/no-move/journal-only bounds and both entry shapes verbatim |
| 3 | seat | First observer stint step under the charter (#3 — no spawn; §3b) | first `[observer]`-tagged watermark entry appears in the operator journal |
| 4 | seat (observer step) | **Retro-shadow stint** over the existing **~112-message agent-to-agent corpus — excluding `queue/operator/` and `from=operator` files (red-proxy W1)**: full read, `SURFACED` entries for history | every entry's key resolves to a real file; entry count is a first false-flag estimate the human reads before going live |
| 5 | human + outside hand | Human reads the retro list against their own recollection, **plus the first P-F8 miss-audit: a hand outside the observer/drafter lineage (or the human) draws K random messages from the unsurfaced remainder and judges "would the operator have wanted this?" (red-proxy W5)** | any confirmed miss → charter or predictor gap, journaled; dismissal rate + first recall estimate recorded as the pilot baseline |
| 6 | seat (observer step) | First live stint | byte-identical check: plane files untouched (W-F4's method); watermark line present |
| 7 | seat | First routing: grep, route one surfaced item, dismiss one | routed item reaches the human by existing channels only; dismissal produces the status note + manifest label |
| 8 | human+seat | Ratification drill: human ratifies one draft with one word | the executing verdict entry cites the human's utterance, not the draft (P-F4's grep run once) |
| 9 | seat | Kill drills: soft (charter freeze ⇒ next stint surfaces nothing), hard (drop the stint step ⇒ plane identical, seat grep empty; `swarm close` drill applies only if a standing observer was spawned) | §7 table observations |
| 10 | adopt gate | ~2 weeks (DW step 12's shape): human reads P-F2/P-F3 numbers and P-F8 recall estimates; adopt (SKILL bullet #4 ships, one human-approved PR; promote to a standing agent ONLY on between-stint time-sensitivity evidence, §3b), narrow the charter, or kill | on kill: delete the charter, drop the step — nothing else exists; the recorded datum is instrument-relative (§5) |

---

## 9. Falsifiers — each with its collector

DW's W-F1–W-F8 remain in force for the decision-engine, untouched. DEC §6
F1–F7 remain inherited law. The plane wiring adds:

1. **P-F1 — the observer acts beyond its ledger.** Any unsolicited send,
   any file moved, any write outside the observer ledger (§3b) and
   its manifests. Collector: any hand — sends are wire-attributed in
   recipients' `delivered/` (W:17-25), moves violate reconcile greps, and
   (in the standing form) `ps` shows its pane. One instance ⇒ hard kill; the
   no-authority bound is this design's spine.
2. **P-F2 — false flags dominate.** Dismissal rate on surfaced items
   exceeding the charter's calibration line (a written constant the human's
   judgment overrides in both directions — the SPAN-shape DEC §4b.5 uses).
   Collector: the seat's per-stint routed/dismissed count. Fires ⇒ narrow
   the charter or kill; the observer exists to spend fewer operator-attention
   units, not more (the DEC F5 shape).
3. **P-F3 — the justifying hit (the inverse falsifier, run honestly).** A
   surfaced item the operator acted on that no existing channel (sender
   escalation, seat judgment, desk) would have carried to them. Collector:
   the stint review question, extended from DEC §6 F2's wording. **If the
   pilot ends with zero P-F3 hits, the observer's premise failed — kill,
   and record the zero as instrument-relative: "this instrument, under this
   charter, surfaced nothing the operator used," never "there was nothing
   to surface"** *(red-proxy W5 — a blind observer and an empty plane
   produce the same zero; only P-F8's miss-audit can tell them apart, and
   the record must not pre-judge which it was)*.
4. **P-F4 — a draft becomes authority.** Any verdict entry citing a
   `SURFACED`/`DRAFT` entry without quoting a human ratification. Collector:
   any hand; both are world-readable text (DEC §6 F7's collector shape).
   One instance ⇒ freeze the charter pending re-ratification.
5. **P-F5 — plane bytes differ from observer-absent.** Any observer byte on
   any queue file, wire, desk, or `ps` (W-F4 extended from the operator
   surface to the plane). Collector: the seat, diffing a sampled message
   file against its send-time shape (`{"to","from","ts","body"}` is
   deterministic, SURF §0). Fires ⇒ I1/I3 void; kill and investigate.
6. **P-F6 — behavioral interposition.** Agents begin *waiting* on surfacing
   verdicts before acting — the observational proxy becoming a de-facto gate
   through convention drift. Collector: journal reads at reconcile (any
   "pending plane-observer" language); the observer's brief states it owes
   nobody anything. Fires ⇒ re-brief the waiting agent; if systemic, the
   design has failed its own premise — kill.
7. **P-F7 — surfacing volume presses the operator's span.** Surfaced items
   per stint exceeding what the human declared (C20/C21 via DW W-F7's
   shape). Collector: the human, who owns the number; the seat counts.
   Fires ⇒ narrow the charter — same remedy, same reason as W-F7.
8. **P-F8 — recall, measured by sampled miss-audit** *(added after
   red-proxy W5: P-F2 measures precision, P-F3 utility, P-F7 volume — false
   negatives were measured nowhere, and §3b step 2's write-nothing rule
   means a passed-over message leaves no per-message trace to audit)*. At
   the retro (step 4) and once per pilot stint, a hand OUTSIDE the
   observer/drafter lineage — or the human — draws K random messages from
   the UNSURFACED remainder and judges: would the operator have wanted
   this? Collector: that hand's journal entry naming the K refs and
   verdicts. One confirmed miss ⇒ charter or predictor gap, journaled where
   found (DEC §6 F2's rule); repeated misses ⇒ the surfacer under-covers —
   retrain or kill. The audit is also what makes the retro (step 4)
   something other than the observer grading its own coverage, and what
   licenses P-F3's zero to be read at all.

---

## Summary for proxy-scout

The operator's ask generalizes — but the *wiring* that honored it at the
operator mailbox does not, and the maps say why with one mechanical fact:
DW's engine-hand was additive because the tool never delivers to the
operator queue (bin/swarm:610-611); everywhere else, delivery is live code
(bin/swarm:331-339), so an interposed plane proxy must either edit the
delivery path, race it, or re-deliver under laundered identity that
falsifies the delivered-record — each breaking promises made for every
message in the system (§1, verified against SURF §6.1/6.2/6.6/6.9,
including the one honest refinement: 6.9 is a real interception point that
no interposed proxy survives). The interposed form also serializes a
parallel message plane through one queue at ~127 plane messages/day — 112
of them true agent-to-agent, ~3.0× the operator mailbox; 3.6× counting the
seat's own dispatches (MEASURED) — doubles the delivered record, launders
relations, and inverts "the engine can only ever subtract itself" into a
plane-wide single point of failure (§2). The observational form delivers
every outcome the ask names except pre-delivery veto — which the record
shows the operator never exercising and doctrine forbidding (§2d) — at a
cost of one read-only stint duty (a standing agent only if the pilot earns
it, §3b), two ledger-entry shapes, one human-authored charter, one SKILL
bullet at the adopt gate, and zero WORLD.md changes (§8). Drafts live
beside the plane, never on it (§4); the surfacing predictor is the
flag-only instrument DEC pre-priced, deployed early because F2's collector
does not exist on the plane, and wired to die on its own numbers — with
its zero recorded as instrument-relative and its recall sampled by an
outside hand (§5, P-F2/P-F3/P-F8); and the observer holds authority
tighter than DW's engine because the plane was never the operator's to
answer, so there is nothing to grant (§6). Everything it could break, it
can only break inside its ledger; for every message in the system it is,
by construction, indistinguishable from absent.
