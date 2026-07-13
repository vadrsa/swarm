# DECISION-WIRING — wiring the assumed decision engine into this swarm

**Author:** `wiring-drafter`, for `decision-wiring`. Written at `main@834fec4`,
2026-07-10; revised same day after adversarial review by `red-wiring`
(3 KILL, 10 WOUND, 13 citation findings — `.swarm/research/red-wiring-review.md`);
the revision notes at formerly-broken sites say what changed. The engine is
ASSUMED to exist per the operator's returned brief:
a black box, trained on the operator's recorded decisions, that receives
operator-bound decision points and either auto-answers (confidence above
threshold) or passes through. Whether to build it is not this document's
question. This document is the complete integration design — everything on
either side of the engine's interface — as a recommendation, not a survey.

**Evidence discipline:** every load-bearing claim cites `.swarm/research/wiring-surfaces.md`
(`SURF §n`), `.swarm/research/seat-ritual.md` (`SEAT §n` / contract items
`C1–C21`), `docs/design/DECISIONS.md` (`DEC §n`), or a file:line at main.
DECISIONS' authority constraints are inherited law here; **two** collisions
with the assumed engine exist — both confidence-shaped — and are resolved
loudly in §2c, not dropped. (The first draft flagged only one; red-wiring K1
found the second hiding under a false "verbatim.")

**The recommendation in one paragraph.** Spawn the engine as a real agent
(`swarm spawn decision-engine …`) and seat it as a **hand** on the operator
seat by convention. It watches `queue/operator/` like the seat's existing
Monitor does, and for each waiting item it can cover it performs the ordinary
hand claim ritual — move, claim line, act — answering the asker **in its own
wire name** with a grant citation and an explicit "the human has not read
this" marker, and writing a hand-tagged verdict entry in the operator ledger.
Everything it cannot cover it does not touch: pass-through is the *absence of
action*, byte-identical to the engine never having existed. Its authority is
not its confidence score but the standing-authorization grant lines DECISIONS
§4b defined, quoted in the human's own words in the operator journal; its
config **is** those lines. Kill is one journal entry (soft — effective
against a compliant engine) or `swarm close` (hard — effective against
anything). The shippable text: one SKILL.md bullet, one operator-journal
entry, and **one recommended two-clause WORLD.md amendment — the single
CONTRACT-CLASS item, flagged in §9**. The design can run without the
amendment under an interpretation the human may ratify instead, but the maps
say the contract sentence strains (SURF §6.2), and this document carries
that rather than hiding it.

---

## 1. Interception point: a standing engine-hand on the mailbox

### 1a. The choice, argued from the maps

The parent's addendum named the fork: (A) standing engine-hand with its own
spawned identity, (B) seat-step engine run inside the human/ops-main ritual,
(C) wire/watcher/addressee variants. **A wins.** I confirm the parent's lean,
on grounds the maps force:

1. **The category already exists.** C13 (skill/SKILL.md:53-55): "A session
   acting for the human at the root — reading the operator mailbox,
   dispatching, judging — is a **hand** on the operator seat." An engine that
   reads and answers operator mail is not a new kind of thing; it is a hand,
   and the hand kit comes free: hand-tagged claim lines (C15), the
   delivered-without-claim-line crash alarm — proven live (SEAT §1g, EV:78) —
   journal-as-audit-trace, and seat-owned open loops (C17). The wiring's
   crash-safety does not need to be invented; it shipped in PR #74.

2. **The wire solves the voice problem only for a named agent.** There is no
   `--as` flag and no proxy path (SEAT §5: `cmd_send`'s only flag is
   `--stdin`, bin/swarm:887-890); anything sending from a seat environment
   speaks as `from operator — the OPERATOR (the human at the root)`
   (bin/swarm:154-155, 210-212) — maximum structural authority, colliding
   with inherited law (DEC NOT-list 4: "No auto-answer in the operator's
   voice. Attribution or nothing."). Identity is `SWARM_AGENT_ID`
   (bin/swarm:52-53); a spawned agent's sends carry its own name on every
   delivered file and in every relation header. A body-line disclaimer under
   the OPERATOR header (option B's best case) is attribution the recipient
   must notice; a distinct wire name is attribution the recipient cannot
   miss. For a machine answering in the human's stead, the stronger form is
   the only defensible one.

3. **Only the hand shape degrades clean.** Mail always lands in
   `queue/operator/` (no re-addressing, no send-path change); the engine
   claims what it answers and leaves the rest; engine absent = today exactly
   (§8). Every C variant degrades dirty or breaks contract (§1b).

4. **Latency, priced honestly.** Option B answers nothing while no seat hand
   runs; the engine's whole assumed value is answering the mechanical share
   while the human is away. Inherited law says pass-through latency is not a
   defect (DEC NOT-list 7) — so the standing hand is chosen not to meet an
   SLO but because a seat-step engine simply fails the brief's premise
   ("receives operator-bound decision points" — not "receives them when a
   stint happens to run"). B also entangles engine failures with the
   ops-main hand's own stint context; A isolates them to their own pane,
   world-readable (W:10; `swarm ps` "the one view", WORLD.md:30-31).

### 1b. The losing corners, killed with citations

- **6.1 wire-side, inside `cmd_send`** (SURF §6.1): declining to queue
  violates "nothing ever refuses a message to the operator" (WORLD.md:58-59,
  C3) — CONTRACT-CLASS, verbatim in the map. Redirecting *strains* "`ps`
  shows them waiting" (WORLD.md:57-58, C2) — the map's flag is conditional,
  "CONTRACT-CLASS unless the engine's own queue is surfaced equivalently"
  (wiring-surfaces.md:268-272); this design declines the escape hatch
  because an equivalently-surfaced second queue buys nothing the hand shape
  lacks and still costs a bin/swarm edit. And code on the send path makes
  engine failure a send failure — the dirtiest possible degradation. Dead.
- **6.2 non-hand watcher daemon** (SURF §6.2): performs exactly the
  engine-hand's acts but nameless — no journal, no claim lines, invisible in
  `ps` (my characterization of namelessness, not the map's words). The map's
  actual flag is heavier and broader: moving operator mail to `delivered/`
  makes it "stop meaning 'the human looked'" and "WORLD.md:60-61's
  drain-by-reader sentence would need rewording to name the engine as (part
  of) the reader's side — CONTRACT-CLASS" (wiring-surfaces.md:289-293).
  That flag attaches to ANY engine that moves operator mail — the
  recommended hand included; §9 carries it as this design's one
  CONTRACT-CLASS item instead of burying it on this corpse. The map's second
  hazard — answering *without* moving leaves `ps` showing the mail waiting,
  a double-answer hazard when the human later drains — resurfaces as §7's
  fourth interruption state. The non-hand dies because it takes the contract
  exposure *without* the audit kit; §1a is its rehabilitation. Dead as a
  non-hand.
- **6.5 dedicated addressee** (`send decider` instead of `send operator`,
  SURF §6.5): the map states the adoption cost and the silent bypass
  (wiring-surfaces.md:351-356) and — noted honestly — flags NO WORLD.md
  sentence: this is the one candidate with zero contract strain. It dies on
  degradation, and that leg is the parent's construction plus my inference,
  not the map's: a dead or wedged addressee is a jammed mailbox in front of
  the human (parent's addendum point 3; mechanism bin/swarm:926-930 — "if
  <to> is closed … it will never be delivered"), which fails §8's I3 in a
  way the hand shape structurally cannot. "Fatal" is my word for
  adoption-cost-plus-jam together. Dead.
- **6.9 blocking PreToolUse on `swarm send operator`** (SURF §6.9): a
  refusal (C3, CONTRACT-CLASS) that additionally leaves *no durable record
  the attempt happened* — worse than 6.1. Dead. (Observe-only 6.9 is legal
  and is NOT recommended either — §5's feed does not need it; it is
  pre-priced there as the one legitimate expansion if training wants
  sender-context capture later.)
- **6.3 operator-session hooks** (SURF §6.3): injecting mail into the
  human's session is a push (C3) unless gated on the human's own submit; it
  also edits the human's personal `~/.claude/settings.local.json` — wiring
  outside the repo's own record. Nothing the hand shape doesn't already
  provide. Dead.
- **B, seat-step engine** (SURF §6.4): loses on voice (point 2 above) and on
  coverage (point 4). Note what B *is*, though: it is exactly today's
  practice — the seat answering under informal pre-auth (SEAT §1d), in the
  operator's voice (SEAT §5). B survives as the system's degraded mode, not its
  design: when the engine is down or killed, the seat may still do what it
  does today. The engine adds to that baseline; it never replaces it.

### 1c. Spawn shape

`swarm spawn decision-engine "<brief>"` executed from the seat environment
(no `SWARM_AGENT_ID` ⇒ parent recorded as `operator`, bin/swarm:52-53,
843-845). The name is chosen, not derived (WORLD.md:14-16); `decision-engine`
is recommended and, like any name, burns on close. The engine gets the
standard four hooks, a pane, a journal (SURF §3), and doorbell service for
its own queue (SURF §4, §1a) — meaning the human can `swarm send decision-engine …` and it
answers promptly, unlike the operator mailbox. It keeps a standing watch on
`queue/operator/` from inside its own pane — the F6 Monitor precedent, the
seat's one owned instrument (SEAT §2, F:59-63), now duplicated by a second
hand. Two watchers on one mailbox is contemplated by C14 ("hands come and
go, in sequence or in parallel") — but the race safety must be stated for
what it is: **a convention this design imposes, not a mechanism the maps
witness** *(rewritten after red-wiring K2, which caught the first draft
citing F5/C15/C16 for a race they never discuss)*. The facts: the claim move
is "plain `mv`; the tool offers no verb for it and verifies nothing"
(seat-ritual.md:264-266), and the only code that ever moves a file into
`delivered/` is the deliver path, unreachable for the operator queue
(bin/swarm:336-337, 610-611) — so nothing mechanical adjudicates two
simultaneous claimants. What makes the race safe is POSIX rename
exclusivity — one same-filesystem `mv` of the same source succeeds, the
loser exits non-zero — IF every hand (a) moves with `mv`, never copies, and
(b) aborts the claim on a failed move. This design writes that rule into
the engine's brief as a hard duty (§9 change #3), drills the race
(implementation step 7), and names its falsifier (W-F8: two claim lines for
one file, or one asker holding two answers to one decision point). The
EV:78 alarm covers a *sequential* crash, not this race.

---

## 2. Decision-point shape and routing

### 2a. What the engine enumerates (routing)

Inherited definition, unchanged (DEC §3): a decision point is an open loop
awaiting the operator's verdict — **(i)** a dispatch entry without its
verdict entry, **(ii)** a desk item, **(iii)** a delivered message whose
sender named something as the operator's to decide — enumerated *by reading*,
never by a stored classification. The engine therefore reads exactly three
surfaces, all of which already exist:

- `queue/operator/*.json` — waiting mail (clause iii at its birth);
- `.swarm/journal/operator.md` via the grep idiom (C-adjacent, S:61-63) —
  open loops and declared classes (clauses i, ii's source);
- the desk is **not** read — a marked deviation from DEC §3's letter, which
  enumerates "the ledger, the desk, and the operator's mail"
  (DECISIONS.md:256-261). The argument for deviating: the desk is declared
  derived and never load-bearing (C19, F4), regenerable from the two
  surfaces above at any time — so reading those surfaces reads the desk's
  sources, and reading the Artifact itself would make load-bearing a surface
  the contract says must never be one.

Nothing routes *to* the engine. Senders keep addressing `operator`; the wire,
the record shape `{"to","from","ts","body"}` (bin/swarm:912), and the send
path are untouched. This honors grave 2 / NOT-list 2 (no wire-side anything)
by construction rather than by discipline.

### 2b. The assembled record (shape)

Per decision point, the engine assembles **at read time, in its own memory or
journal — never on the message** (parent's H2, confirmed):

| field | source |
|---|---|
| `source_ref` | queue filename (e.g. `1783702294235-hardener.json`) or ledger entry ref |
| `sender`, `ts`, `body` verbatim | the queue record itself (bin/swarm:912) |
| `relation` | computed — the function is pure and importable (bin/swarm:147-163; SURF §1d) |
| `loop_ref` | the matching dispatch entry, if this closes a loop (DEC §1b signal 1) |
| `declared_class` | operator-authored class from the dispatch entry (DEC §1b signal 5) |
| `candidate_grant` | the standing-authorization line that would cover it, if any (§3a) |

The two strongest **hop-2-relevant** signals (loop topology, declared class —
the qualifier is DEC §1b's own, DECISIONS.md:97-99) never touch message
surface — the engine's routing does not resurrect grave 1.

### 2c. The collisions with inherited law — two, both confidence-shaped, resolved loudly

*(Rewritten after red-wiring K1/W5: the first draft flagged one collision and
argued it against the law's friendliest formulation; there are two, and the
resolution sentence was overdrawn. Both repaired here.)*

**Collision 1 — the score.** DECISIONS NOT-list 1 forbids "a learned
classifier, confidence score, or threshold over decision features **that
issues answers**" (the qualifier is verbatim, DECISIONS.md:476-477). The
broader formulations must be faced too: DEC §2 says any component inferring
confidence *from message surface* "is grave 1 with a newer shovel"
(DECISIONS.md:243-246), and DEC §4a kills even the flag-only learned model
*today*. The assumed engine's confidence is computed over records that
include the body verbatim (§2b) — it IS a score over decision features, and
no routing argument launders that. Those sentences argued against *building*
such a thing; the operator's returned brief assumes it built, which settles
the build question and leaves the wiring exactly one duty: **the score must
never be the authority.** Resolution by composition:

> The engine may auto-answer a decision point **only when BOTH hold**:
> **(a)** a standing-authorization grant line with quoted human provenance
> covers it (binary citability — DEC §4b.2, the hard gate), AND
> **(b)** the engine's confidence clears its threshold.
> Confidence below threshold inside a granted scope ⇒ pass through.
> Confidence above threshold outside any grant ⇒ pass through, **always** —
> no score, however high, widens authority by one millimeter.

Stated precisely (the first draft's "the score never issues; it only
withholds" overdrew — within a granted scope, above-threshold confidence is
a necessary conjunct of every issued answer, the deciding bit): what the
composition guarantees is narrower, and is the thing the law actually
protects — **the score never expands authority beyond a grant.** It can only
shrink the answered set within one. NOT-list 1's target (surface confidence
issuing answers no human authorized — the #62 failure shape, DEC §1d)
remains structurally impossible: #62-class items are contract-adjacent,
outside any legal grant's scope (DEC §4b.3a), and pass through whole to the
live human attention that is "the only #62 detector in existence" (DEC §7).
Flag for the human's one-pass read: if any future change lets confidence
answer where no grant covers, this document's design is void.

**Collision 2 — the threshold.** DEC §4b.2: "Confidence is binary
citability, not a score … binary, threshold-free, no stored number"
(DECISIONS.md:371-377). The assumed engine's interface carries a threshold,
and this wiring stores it — one human-authored line in the grants entry
(§3a). That is a stored number, and it is flagged here with the same
loudness as collision 1. Resolution: DEC §4b.2's rule governs the
*authority mechanism*, and that stays intact — citability remains binary
and threshold-free; no number ever decides whether a grant covers a case.
The stored threshold configures only the engine's conservatism *inside*
covered scope (collision 1's composition), it is the human's own written
words like every other line in the entry, and deleting it deletes nothing
but caution. **Residual, accepted in writing:** threshold observance is
unauditable — the confidence number exists only as engine-authored prose
(below), so an engine answering below its stated threshold inside a granted
scope violates nothing any §10 collector can see. The harm is bounded
because the grant still gates; the residual is real, and no falsifier
catches it.

Storage honesty (C9/C10): the confidence number appears only in prose the
engine authors — its answer body and its ledger entry, an agent's own words,
facts a file can witness ("the engine said 0.93"). It is never a field in any
record the tool reads, never on the wire, never tool state.

---

## 3. Auto-answer path

### 3a. Authority: the engine's config IS the grant ledger

Reused from DEC §4b (the brief's instruction: reuse, don't parallel) with
one engine-specific addition that DEC §4b does not contain, flagged as
collision 2 in §2c. The grants live as `STANDING GOALS` entries in the
operator journal (S:78-86 — the shipped convention; C18's
out-of-band-doesn't-exist rule was written for goals and is extended here to
grants — same principle, marked as an extension), each line carrying
**scope, grant, reversibility bound, review trigger, and quoted human
provenance** (DEC §4b.1; NOT-list 5). The engine has **no other config
file**. The threshold lives in the same entry as one more human-authored
line (e.g. "engine threshold: answer only above 0.9") — the stored number
§2c flags and prices. Consequences, all inherited for free:

- deleting a line deletes the behavior (DEC §4c, "ratchet that can go
  backwards");
- authority changes are instant text, independent of any retraining (§5);
- grant-provenance rot has a collector already defined (DEC §6 F7: any hand,
  any time — grants are world-readable text).

### 3b. The answer ritual, step by step

For each covered, above-threshold item, in one turn:

1. **Claim** — move the queue file to `queue/operator/delivered/` and append
   the hand-tagged claim line (C15):
   `## <date> — [hand:engine] CLAIM: <file> (auto-answer, grant <ref>)`.
2. **Answer** — `swarm send <asker>` from the engine's own environment. Wire
   header the asker sees (bin/swarm:210-212): `[swarm message] from
   decision-engine — <relation> — sent <ts>` — never the OPERATOR header.
   Body template (must fit TURN_CAP 8000, bin/swarm:32; long rationale goes
   in a file, path sent, per WORLD.md:24-25):

   ```
   AUTO-ANSWER — the human has NOT read your message.
   re: <your message <queue-filename> / loop <ledger ref>>
   answer: <the answer>
   under grant: "<verbatim quoted grant line>" (operator journal, STANDING
     GOALS <date>)
   confidence: <c> (informational; authority is the grant, not this number)
   to contest: send operator citing this message; an override freezes the
     grant pending the human's re-ratification.
   ```
3. **Record** — append the ledger verdict entry (the audit trace):
   `## <date> — [hand:engine] AUTO-ANSWER: <source_ref> → <asker>` with:
   decision point in one line; grant cited (entry + quoted words); the
   answer; confidence; training-basis refs (the manifest row, §5); `human
   pre-read: NO`; reversal pointer ("journal an OVERRIDE naming this
   entry"). This is DEC §4b.4's attribution rule executed with a stronger
   wire identity than DECISIONS could assume.

**Citable, reversible, in whose name:** the answer issues in the engine's
name in the header (wire fact), in the body (first line), and in the ledger
(hand tag). Every answered decision is citable by its queue filename +
ledger entry — a guarantee with one crash window (the turn dying between
answer and record), closed by §7's fourth-state recovery rule — and
reversible by the override ritual (§6) — grants are
reversibility-bounded by construction (DEC §4b.1), so nothing the engine may
answer is expensive to reverse *by declared bound* (owning DEC's caveat that
this bound is asserted until the first real overturn prices it, red W9).

**What the asking agent sees:** one ordinary message claiming one ordinary
turn (C5), from a sender visibly not the human, telling it so twice, with the
contest path inline. No new concepts land on any agent — an agent that has
never heard of the engine can still act correctly on this message (grave-2
discipline, DEC §2.2).

---

## 4. Pass-through path: untouched, unenriched

Anything out of scope, below threshold, hop-1-shaped, or arriving while the
engine errs: **the engine does not touch it.** No move, no annotation, no
side dossier, no desk write. The file waits in `queue/operator/`; `ps` shows
it at the top (bin/swarm:429-435, 942-943); the human's ritual is SEAT §3
verbatim.

This overturns parent's H4 (side dossier "the human can open"). Killed for
three reasons: (i) the strongest degraded-mode invariant available is
*pass-through output is byte-identical to engine-absent* (§8 I3) — a dossier
breaks it and makes engine-down observable at the human's surface; (ii) the
dossier's read-cost lands on exactly the attention the design protects, for
items the engine already judged un-answerable — my reading of INBOX's
enrichment findings, offered as gloss, not citation (what DEC §2 cites INBOX
§1c for is keyword *misclassification*, a different failure); (iii) anything
worth saying about a near-miss belongs in the engine's own journal, which is
world-readable anyway (WORLD.md:28-29) and costs the human nothing unless
sought. **The desk stays seat-owned** (parent's open question 4): the engine
never writes the Artifact; because desk content is regenerated from journal +
repo (C19, SEAT §1f), engine-answered items fall off the next desk
regeneration automatically — via the ledger, not via desk access.

**Hop-1 reconciliation** (parent's open question 3, stated plainly): the
operator's description says the engine "receives operator-bound decision
points." In this wiring it *receives* everything that reaches the operator
surface — the one mailbox plus the ledger, which is where all three clauses
of DEC §3 are born — and *acts* only on the granted hop-2 subset. Hop-1
material (dispatched work returning for seat judgment, adjudications,
amendments) passes through untouched: not because the engine cannot read it,
but because no legal grant can cover it — "you cannot pre-authorize an
adjudication" (DEC §1a), and NOT-list 6 is inherited law. The description is
honored as receive-all, answer-granted, touch-nothing-else. Where hop-1 mail
goes: where it always went — the seat.

---

## 5. Training-data feed

**What it reads (paths, all read-only, all existing):**

| source | yields |
|---|---|
| `.swarm/journal/operator.md` | dispatch/verdict pairs = labeled decisions; claim lines; STANDING GOALS grants; OVERRIDE/ratification entries (the labels that matter most) |
| `queue/operator/delivered/*.json` | the full decision-point corpus with sender + ts — "the single richest training corpus" (SURF §6.8) |
| `gh pr list` / `gh pr view` | merge verdicts + latency (read-only gh "agents already run unblocked", SURF §6.7; the usage record SURF §5) |
| other journals, `queue/*/delivered/` | context only (SURF §6.8) |

No new capture surface. Specifically NOT wired: PreToolUse/PostToolUse
observation (SURF §6.9) — delivered/ plus journals already witness every
decision point and every outcome; hook capture is the pre-priced expansion if
the black box someday demonstrably needs sender-side context, and it lands as
a settings change for future spawns only (bin/swarm:812-817), observe-only.

**When:** batch, at the close of each engine stint, journaled as a
`## <date> — [hand:engine] RETRAIN` entry (parent's H5, confirmed) — plus
**event-triggered on any OVERRIDE entry**, because overrides are the
highest-weight labels and must not wait a stint. Note the separation that
makes this safe: *authority* changes instantly with text (§3a) — a frozen
grant stops answers before any retrain; *learning* merely catches up.

**How labels enter:** a human override/reversal entry = top-weight negative;
a human ratification = positive — where "ratification" means an explicit
entry, or an item the pilot-regime exhaustive review read and did not
overturn (DEC §4b.5's marks are *overturn* marks; counting the un-overturned
as positives is this design's extension, marked as such); an unreviewed
auto-answer = **no label at all**.

**The self-training exclusion:** every retrain writes a manifest row per
source entry to `.swarm/engine/manifest-<date>.md` (the one new directory
this design adds; world-readable). Entries authored under `[hand:engine]`
are EXCLUDED from the training set unless a later human entry ratified or
reversed them — in which case the *human's entry* is the label. Sourcing,
stated honestly: DEC §1e is a REASONED diagnosis of the Goodhart hazard
(DECISIONS.md:184-194); the exclusion-plus-manifest mechanism is this
design's own discharge of it, not an inherited rule. And §1e's endogeneity
worry reaches further than the exclusion does — the human stamp rate itself
is endogenous to seat verification — which no manifest fixes; the inherited
collector for that residual is DEC §6 F4's per-stint deep-verify. The
manifest is the collector for the narrower leak: any hand can grep it for
`[hand:engine]`-authored rows lacking a human ratification ref (falsifier
W-F6, §10).

---

## 6. Override: the human reverses an auto-answer

The ritual, end to end — one journal entry triggers everything:

1. **The human writes the override** (or dictates it; provenance rule
   applies): `## <date> — OVERRIDE: <engine verdict-entry ref>` with the
   corrected answer and, if visible, why the engine was wrong. Out-of-band
   reversal does not exist until written (extending C18's rule — written for
   goals — to reversals; same principle, marked as an extension).
2. **The asker is told** — a correcting `swarm send <asker>` naming the
   overridden message; sent by the human's own hand (legitimately `from
   operator` — this is the human speaking) or by the seat on their behalf.
3. **The cited grant freezes automatically.** Convention: an override entry
   names the grant its target answered under; that grant is void until the
   human re-ratifies or narrows it in a superseding STANDING GOALS entry
   (restatements cite what they supersede — S:79-82). The engine re-reads
   grant state before *every* answer (the citation rule is a live read, DEC
   §4b.2), so the freeze takes effect on the next decision point with no
   engine restart — noting plainly that the re-read is a briefed duty, so
   this works on a compliant engine; the non-cooperative case belongs to
   §7's hard kill. Chosen over "mandatory review of everything" because it
   is targeted, instant, and text-only; chosen over "automatic numeric
   narrowing" because scope is the human's words and only the human's words
   (NOT-list 5).
4. **The label enters training** at top weight, event-triggered (§5).
5. **The engine is nudged** — `swarm send decision-engine` pointing at the
   override entry (a prompt, not the authority; the journal is the
   authority). Its next journal entry must acknowledge the freeze.
6. **Scale response** is inherited: pilot regime, any overturn triggers line
   review; an overturn that proves expensive to reverse shrinks the engine's
   scope immediately and re-prices every remaining grant (DEC §6 F1).

---

## 7. Kill-switch

Two layers, both mid-flight safe:

- **Soft kill (pause) — one journal entry:** `## <date> — STANDING GOALS:
  all engine grants frozen (supersedes <ref>)`. Because authority is a live
  text read (§3a, §6.3), the engine answers nothing from its next item on —
  clean pass-through with the pane still warm, resumable by re-ratifying.
  Cost: one entry. Stated honestly *(rewritten after red-wiring K3)*: the
  freeze's *effect* rides on the engine's own briefed re-read duty — it
  stops a compliant engine, including one whose judgment has gone bad, but
  it is cooperation-dependent by construction; nothing mechanical gates an
  agent's sends (this design itself killed the one gate that could, 6.9
  blocking, §1b). This replaces parent's H6 presence-file: a
  `settings/engine-enabled` file would be new tool-adjacent state with a new
  meaning, when the grant ledger already IS the enable switch — and C14
  says seat mechanics are "convention in that journal, not tool state" —
  and a presence file would be exactly as cooperation-dependent, so it buys
  no rogue coverage either.
- **Against non-cooperation, the hard kill is the only kill.** A rogue
  engine — one not honoring its brief — is stopped by `swarm close`, which
  removes the pane, and by nothing softer.
- **Hard kill — `swarm close decision-engine`:** pane dies, files stay
  (WORLD.md:32), name burns (WORLD.md:15-16) — a restart is a new name and
  a new spawn, which is the record working as designed. Cost: one command.

**In-flight items under either kill:** the engine holds nothing across
turns — each item is claim→answer→record within one turn (§3b). The **four**
possible interruption states *(the first draft listed three; red-wiring W2
found the fourth, and it is the worst one)*:

1. **File untouched** ⇒ ordinary waiting mail; nothing happened.
2. **Moved, no claim line** ⇒ the C16 alarm at the next seat reconcile
   (proven live, EV:78).
3. **Claimed, no answer** ⇒ a seat-owned open loop any hand may adopt —
   extending C17, whose verbatim rule speaks of *dispatch entries*, to claim
   lines: this design's extension, marked as such and written into the
   SKILL bullet (§9 #2), not an inherited rule.
4. **Answer sent, verdict entry unwritten** ⇒ the asker holds a live
   AUTO-ANSWER that appears in no ledger — §3b's every-answer-citable
   guarantee is false in this window, W-F1's ledger grep cannot see the
   answer, and a hand adopting the state-3-lookalike loop could send a
   second, contradictory answer (the double-answer hazard SURF §6.2 named).
   **The recovery rule, a hard duty in the engine brief and the SKILL
   bullet: any hand adopting a claimed-but-unverdicted item MUST first
   check the asker's queue and `delivered/` for a `decision-engine` send
   referencing the source file** — the sent answer is world-readable
   evidence (`"from": "decision-engine"` in the delivered record). If
   found: write the missing verdict entry from the send's own content; do
   not re-answer. W-F1's collector gains the matching inverse sweep (§10).

Answers already sent remain attributed and reversible (§6) — a kill never
un-sends, and never needs to.

---

## 8. Degraded modes: the engine can only ever subtract itself

Parent's H7 invariants, **amended — not confirmed** *(red-wiring W6: the
first draft said "confirmed" while breaking H7's first clause)*. H7 said the
engine "never moves queue files"; this design's engine-hand moves them — the
claim, §3b step 1 — trading H7's letter for the hand kit's alarms and
carrying the resulting contract exposure openly as §9's flagged amendment.
The amended invariants:

- **I1 — the wire is untouched.** Nothing sits between `swarm send` and
  `queue_put`; no hook, no field, no redirect (§1b kills; §2a routing). Mail
  durability is exactly `queue_put`'s O_EXCL/ts-bump mechanics
  (bin/swarm:252-275; call site 912-919), engine or no engine — and the tool
  provably never delivers to the operator queue at all (bin/swarm:610-611),
  so the engine cannot sit on the wire even by accident.
- **I2 — no exclusive holds.** The engine never possesses the only copy of
  anything and never holds an item across turns (§3b); every intermediate
  state maps to an existing alarm or ownership rule (C16, C17 — §7).
- **I3 — pass-through is absence.** Zero engine bytes on unanswered mail,
  the desk, or `ps` (§4). An observer of the pass-through surface cannot
  distinguish engine-down from engine-choosing-not-to-answer.
- **I4 — authority is text, not process.** Grants are world-readable journal
  lines valid without the engine running (§3a); freezing the *text* requires
  no engine cooperation, while the freeze's *effect* rides on the engine's
  briefed re-read duty — the distinction §7 states and the rogue row below
  applies. The seat's own ritual (SEAT §3) never acquires an engine
  dependency: no step of SKILL.md's seat section is modified, only appended
  to (§9).

Every failure mode traces to them:

| failure | invariants | observed result |
|---|---|---|
| engine never spawned / closed / crashed while idle | I1+I3 | today, exactly: mail waits, `ps` shows it, human ritual unchanged (SEAT §3) |
| crashed between move and claim line | I2 | C16 alarm fires at seat reconcile (proven collector, EV:78) |
| crashed between claim and answer | I2 | seat-owned open loop, any hand adopts (§7 state 3 — the C17 extension) |
| crashed between answer and record | I2 | §7 state 4: the adopter's check-the-asker's-queue rule recovers the verdict entry; no double answer |
| slow / wedged | I1+I3 | mail waits; a human or ops-main hand may claim first — resolved by the claim-race convention, drilled and falsified (§1c, W-F8); latency of pass-through is not a defect (DEC NOT-list 7) |
| answers wrongly | I4 + §6 | bounded (scope), attributed (name on the wire), revertible (grant's reversibility bound); falsifier W-F7 counts it |
| hallucinates authority (cites a non-covering or nonexistent grant) | I4 | world-readable text vs world-readable ledger entry: W-F1's check — any hand can run it (that any-hand property is DEC §6 F7's collector shape; F6's own collector is the sampled review) |
| goes rogue / floods | §7 hard kill | the soft kill is useless here by definition — it works through the engine's own re-read duty, and a rogue engine is one not honoring its duties; `swarm close` removes the pane, and the record (every send wire-attributed) makes the damage enumerable and reversible (§6) |

The engine adds capability only on the answered subset and adds *nothing* —
no step, no dependency, no artifact — anywhere else. That is the guarantee
"engine down = clean pass-through," stated as invariants a probe can attack
rather than as intent.

---

## 9. Exactly what changes

### The priced list

| # | change | size | class |
|---|---|---|---|
| 1 | STANDING GOALS entry in `.swarm/journal/operator.md`: DEC §5 pilot step 1's 2–4 grant lines with quoted human provenance, **plus two engine-specific lines that are NOT in DEC §5** — the threshold (collision 2, §2c) and the enable statement *(the first draft called this "DEC §5 verbatim"; red-wiring K1 — it is DEC §5 plus additions, priced as such)* | ~12 lines, human-authored | operator-owned text; zero code |
| 2 | skill/SKILL.md, operator-seat section: one new bullet naming the engine-hand — an autonomous hand may claim and answer operator mail only under quoted grant lines; answers issue in its own wire name carrying the auto-answer marker and grant citation; its verdicts are ledger entries like any hand's; a claim line with no verdict entry is a seat-owned open loop (the C17 extension, §7); an adopter of such a loop checks the asker's queue before answering (the §7 state-4 rule) | ~10 lines, 1 file | **convention, contract-adjacent** — SKILL.md not WORLD.md, but it names a new autonomous actor on the seat: PR gate with the human's explicit approval. (Precedent, stated accurately per red-wiring W7: the F-package landed human-approved, seat-merged under pre-auth — J:51, SEAT §1d; whether the human merges this one themselves or pre-authorizes is theirs.) |
| 3 | `.swarm/briefs/decision-engine.md` — the engine-hand's brief: duties, citation rule (§2c composition, verbatim), answer/claim/verdict templates (§3b), **hard duties: `mv`-and-abort-on-failure claiming (§1c), grant re-read before every answer (§6.3), the state-4 adopter check (§7)**, retrain ritual + manifest format (§5), override acknowledgment (§6), kill semantics (§7) | ~150 lines, new file | convention |
| 4 | `swarm spawn decision-engine "<brief path>"` | 1 command | none — existing verb |
| 5 | `.swarm/engine/` — retrain manifests (the Goodhart-exclusion audit surface) | new dir, engine-written | convention; world-readable |
| 6 | **Standing cost of the standing hand** *(unpriced in the first draft; red-wiring W10 — the fork's own price axis, wiring-sketch.md:184-185: B has "zero standing cost")*: one permanently warm pane running a Claude session on a mailbox watch — its tokens, and one live node in `ps`, for as long as the engine is seated | recurring, not lines; bounded by the soft/hard kill costing one entry / one command | the price A pays for coverage while the human is away; B remains the zero-standing-cost fallback |
| 7 | WORLD.md | **one recommended two-clause amendment — see the flagged list below** | **CONTRACT-CLASS** |
| 8 | bin/swarm | **zero lines** | — |
| 9 | hooks (both layers) | **zero changes** | — |
| 10 | `ps` engine-answered counts (parent's H8 option) | **killed**: a CLI change with no consumer — `ps` already shows the engine's pane, liveness, and last words; the ledger is the count | — |

### CONTRACT-CLASS items, in one pass

**One recommended WORLD.md amendment — the honest default.** *(Rewritten
after red-wiring W1, which broke two of the first draft's three legs for
"zero WORLD.md changes." The repaired reasoning:)* The maps themselves say
the sentence strains. SURF §6.2 attaches CONTRACT-CLASS to the
move-to-`delivered/` by ANY engine — "WORLD.md:60-61's drain-by-reader
sentence would need rewording to name the engine as (part of) the reader's
side" (wiring-surfaces.md:289-293) — and that flag does not care that the
mover is seated as a hand. And the neighbor clause the first draft never
confronted — "Messages to `operator` wait **until the human looks**"
(WORLD.md:57-58, C2) — is falsified for the answered subset by any standing
auto-answerer. What survives of the interpretation argument is real but
thinner than claimed: C13 is verbatim ("a session … reading the operator
mailbox … is a hand"), F5's own text says "a session claims operator mail"
(F:47-57), and the current stint's `[ops-main]` claim lines (J:55-57) show a
*hand* draining — though whether that hand was an agent or the human's own
session the record does not establish (C11's open question, SEAT §4), so it
witnesses hands-may-drain, not autonomy-may-drain.

**The recommendation: amend the mailbox paragraph (WORLD.md:57-61), two
clauses, one edit, human-approved merge:**

> "Messages to `operator` wait until **the human's side** looks; …" and
> "… the human's side — **the human, or a hand they have seated in
> writing** — moves the mail to `delivered/` and journals the claim before
> acting on it."

**CONTRACT-CLASS: one sentence-pair. This is the design's only mandatory
contract touch, and it ships at the adopt gate (implementation step 12),
not before.** The cheaper path — ship nothing on WORLD.md and treat the
hand reading as interpretation ratified by the human's approval of the
SKILL bullet — remains available and functional; but it leaves two contract
clauses reading contrary to running practice, which is exactly the
off-books condition DECISIONS §1c documents as the failure this whole
design exists to end. Recommendation: take the amendment.

**One optional harness-config item, default OFF:** a permission grant letting
the engine execute `gh pr merge` for mechanical-tier PRs. Not part of this
design's v1 — the merge gate keeps its current shape (seat merges under
pre-auth; the classifier's per-object denial stays as the delay-buying layer
DEC §1d credits). Listed because it is the one place the engine's scope could
later grow into an *action* rather than an answer, and it must arrive as an
explicit human-added permission rule plus a grant line, never as drift.

### Implementation sketch (ordered; each task with its verification)

*(Reordered after red-wiring W4: the first draft shipped the SKILL bullet at
step 3, silently inverting DEC §5's adopt-gate — "the SKILL.md sentence …
waits for the pilot's verdict" (DECISIONS.md:512-517). The pilot runs on
operator-journal text alone, which is the authority anyway (§3a); doctrine
text ships at adoption.)*

1. **[human]** Write the STANDING GOALS grants entry (#1) — quoted
   provenance, scope, reversibility bound, review trigger, threshold,
   enable. *Verify:* entry exists; every grant line quotes the human
   verbatim or was typed by them (DEC §6 F7 check run once, by hand).
   **Blocking: nothing runs before this.**
2. **[hardener]** Write `.swarm/briefs/decision-engine.md` (#3) from §§2c,
   3b, 5, 6, 7 of this document. *Verify:* parent reads it against this doc;
   every template present; the composition rule (§2c) and the three hard
   duties (mv-abort claim, grant re-read, state-4 adopter check) stated
   verbatim.
3. **[seat]** `swarm spawn decision-engine` (#4). *Verify:* `ps` shows it;
   a seat-take entry tagged `[hand:engine]` appears **in the operator
   journal** (S:59-61; C14's one-journal rule — the first draft put this
   breadcrumb in the engine's own journal, where no seat grep would ever
   see it; red-wiring W8).
4. **[engine]** Shadow stint — enumerate decision points and journal what it
   *would* answer, claiming and answering nothing. *Verify:* seat compares
   the shadow list against its own mailbox read; zero file moves occurred
   (`queue/operator/` untouched).
5. **[engine]** First live answer on one granted item. *Verify the full
   chain:* file in `delivered/` + claim line + asker's delivered file reads
   `"from": "decision-engine"` + body carries marker/grant/contest lines +
   ledger AUTO-ANSWER entry cites the grant.
6. **[seat]** Crash drill: kill the engine pane between move and claim line
   (replay the EV:78 probe). *Verify:* reconcile fires the
   delivered-without-claim-line alarm; the seat adopts the item.
7. **[seat+engine]** Race drill (new; red-wiring K2): two hands claim the
   same queue file simultaneously (scripted `mv` race). *Verify:* exactly
   one claim line lands; the loser's `mv` exited non-zero and it aborted;
   the asker received exactly one answer (W-F8's collector exercised once).
8. **[seat]** Fourth-state drill (new; red-wiring W2): kill the engine
   between answer send and verdict entry. *Verify:* the adopting hand's
   check finds the `decision-engine` send in the asker's `delivered/`,
   writes the missing verdict entry from it, and does not re-answer.
9. **[human+seat]** Override drill on a sacrificial answer. *Verify:*
   correcting send received; grant frozen (engine's next candidate under
   that line passes through); next manifest carries the override at top
   weight.
10. **[engine]** First retrain event. *Verify:* manifest exists under
    `.swarm/engine/`; grep shows zero `[hand:engine]`-authored rows without
    a human ratification ref (§5 exclusion).
11. **[seat]** Kill drills: soft (freeze-all entry ⇒ next items pass
    through, pane alive), then hard (`swarm close decision-engine` ⇒ mail
    waits, ritual unchanged, files stay). *Verify:* I1–I4 observations per
    the §8 table.
12. **[adopt gate]** After ~2 weeks or ~30 proxied answers (DEC §5.4), the
    human reads the audit numbers against §10 and adopts, narrows, or
    kills. **On adopt only:** hardener ships the SKILL bullet (#2) and the
    WORLD.md amendment (#7) in one human-approved PR. On kill: delete the
    grants entry and close the engine — nothing else exists.

---

## 10. Falsifiers — each with its collector

Inherited falsifiers DEC §6 F1–F7 remain in force (overturn rate, undeclared
decision points, #62 recurrence via the premise sweep — which stays a SEAT
duty on human-initiated corrections, not an engine duty — Goodhart
deep-verify, price-exceeds-product, citation rot, provenance rot). Wiring
adds its own:

1. **W-F1 — an answer without a covering grant.** Collector: any hand;
   verdict entries and grant lines are both world-readable text — read the
   cited line against the case (DEC §6 F6's check shape; note F6's own
   collector is the sampled review — the any-hand property here follows
   F7's). Plus the inverse sweep for answers the ledger grep cannot see:
   grep askers' `delivered/` for `decision-engine` sends with no matching
   AUTO-ANSWER entry (§7 state 4's collector). One confirmed instance ⇒
   freeze all grants (§7 soft kill) pending re-ratification.
2. **W-F2 — a delivered operator-mail file with no claim line.** Collector:
   the seat's post-restore reconcile (skill/SKILL.md:65-66); alarm proven
   live (EV:78).
   Fires ⇒ a hand died mid-claim; if it recurs under the engine, the
   engine's turn discipline (§3b) is broken.
3. **W-F3 — an auto-answer arriving under the OPERATOR header.** Collector:
   the recipient (the marker line and the header would contradict), plus
   implementation step 5's chain check; structurally this requires the
   engine to shed its `SWARM_AGENT_ID` — one instance ⇒ hard kill and
   redesign, the attribution invariant is the design's spine.
4. **W-F4 — pass-through surface differs from engine-absent.** Any engine
   byte on unanswered mail, the desk Artifact, or `ps` output. Collector:
   the seat, comparing a passed-through file against its send record
   (`{"to","from","ts","body"}` is deterministic); I3 is void if this fires.
5. **W-F5 — engine-down increases human load.** Anything jammed, held, or
   requiring engine revival to proceed. Collector: the stint review against
   the §8 table; one instance ⇒ an invariant was violated somewhere — find
   which before restarting the engine.
6. **W-F6 — self-training leak.** A manifest row training on an
   `[hand:engine]`-authored entry with no human ratification/override ref.
   Collector: any hand, grep over `.swarm/engine/manifest-*.md` (§5).
7. **W-F7 — the engine presses the operator's span.** Escalations,
   clarifying questions, or desk items *originated by the engine* exceeding
   what the human declared (C20, C21). Collector: the human, who owns the
   number; the seat counts engine-originated items per stint. Fires ⇒ narrow
   grants or kill — the engine exists to spend fewer of exactly these units.
8. **W-F8 — a claim-race double-act.** Two claim lines naming one queue
   file, or one asker holding two answers to one decision point. Collector:
   the seat's reconcile (grep claim lines by filename) and any asker (both
   sends sit in its own `delivered/`). Fires ⇒ the §1c convention
   (mv-and-abort) was violated by some hand; re-drill implementation step 7,
   and if the violator was the engine, hard kill — its turn discipline is
   the design's load-bearing assumption.

---

## Summary for decision-wiring

The maps make the shape nearly forced: the contract already contains the
category (hand, C13), the crash alarm (C15/C16, proven), the audit medium
(the ledger), and the identity mechanism (`SWARM_AGENT_ID`) this engine
needs — so the wiring is one spawn, one SKILL bullet, one journal entry, one
brief file, one recommended two-clause WORLD.md amendment (the single
CONTRACT-CLASS item, flagged in §9, shipped only at the adopt gate), and
zero changes to bin/swarm or any hook. Parent's lean A is confirmed with two
amendments (no dossier on pass-through; grant freeze replaces the presence
file) and all four open questions are answered (§9 contract call — resolved
against the first draft, toward the amendment; §3b answer body; §4 hop-1
statement; §4 desk untouched). The two real tensions — a confidence score
and a stored threshold under a law that forbids both — are resolved by
composition: grants gate, scores and thresholds only shrink within them.
The red review (red-wiring, 3 KILL / 10 WOUND, all repaired in place) is
part of this document's provenance: what it killed was overdrawn sourcing
and one wrong safety claim, not the shape — the shape survived adversarial
reading intact. Everything the engine could break, it can only break for
items it answered, in its own name, on a record any hand can audit; for
everything else it is, by construction, indistinguishable from absent —
except against outright non-cooperation, where the honest answer is
`swarm close`, and the design says so.
