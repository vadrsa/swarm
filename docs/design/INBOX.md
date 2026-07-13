# INBOX — an evaluation of the operator's mailbox ideas

**Author:** `inbox-scout`, research-only, reporting to the operator. **Written at**
`main@9402f94`, 2026-07-10. No code written, no behavior changed; this document is
the whole deliverable.

**The ideas under evaluation (operator's words, near-verbatim):** (1) the operator
inbox could be "of different structure and harder to read and write to without the
swarm tooling"; (2) the operator wants to "set up how and in what structure it
wants to be pinged"; (3) "be able to categorise and prioritise messages
automatically based on defined rules. Think Gmail."

**Evidence discipline:** **VERIFIED** (I read the line / ran the command),
**MEASURED** (my own instrumentation over the real corpus, method stated),
**REASONED** (my judgment; falsifier named). Inputs read in full: `swarm world`,
PHILOSOPHY.md, SIMPLEST.md, the operator-capabilities FINAL proposal + both red
reviews, STRUCTURE.md §5–6, the operator ledger (54 lines, every entry), and **all
22 messages in `.swarm/queue/operator/delivered/`** — every message the operator
has ever received under this system.

**A dating caveat, owned up front:** ledger entries from `2026-07-11` onward carry
a known journal-timestamp drift (operator ledger entry "doctrine measured & PR'd"
records it as an evidence caveat). Dates below are as-labeled in their sources.

---

## 1. THE CORPUS

Method (MEASURED, reproducible): `python3` over `queue/operator/delivered/*.json`
— parse `from`/`ts`/`body`, count, size, classify by hand-reading every body in
full. 22 files, zero parse failures.

### 1a. The numbers

- **22 messages** across ~21 hours of active operation (2026-07-09 18:47Z →
  2026-07-10 15:55Z), i.e. **~11–16 per active day** at current tree size
  (4–7 live arms). Peak arrival: 13 messages in the 3h49m window 12:06–15:55
  on 07-10.
- **7 senders**, all operator-spawned children: hardener (8), field-tester (6),
  updater (4), codex-scout / structure-scout / red-operator / red-simplest (1
  each).
- Sizes 403–3,210 bytes; median ~1.6KB. Every message fits its turn with >50%
  headroom. Nothing was ever refused, split, or file-indirected.
- **Waiting backlog right now: zero.** `queue/operator/` contains only
  `delivered/` (VERIFIED by listing).

### 1b. Natural categories — what the mail actually is

Classified by reading all 22 bodies (MEASURED; the classification itself is
judgment, so REASONED at the margins):

| Category | Count | Members |
|---|---|---|
| **Work-complete report awaiting operator verdict** ("Task N GREEN", "deliverable ready", "review DONE", probe verdicts) | **18** | all 8 hardener, all 6 field-tester, codex-scout, structure-scout, both reds |
| **Routine confirmation, no action needed** ("update applied ✅") | **3** | updater |
| **Anomaly FYI, explicitly no action needed** (watcher killed 3×, self-healed, "No action needed unless…") | **1** | updater |
| Questions | **0** | — |
| Escalations / urgent interrupts | **0** | — |

Three facts fall out of this table:

1. **The corpus is monocultural.** 18 of 22 messages are the same speech act: a
   child closing a loop the operator opened. Every one of the 18 answers a
   dispatch entry that already existed in the operator ledger (VERIFIED: I
   matched each against ledger entries — Task 1–7, the probe assignments, the
   two red reviews, structure-scout's brief). The inbox is not an inbox of
   strangers; it is the return path of the operator's own dispatch loop.
2. **The variance Gmail exists to manage is absent.** Gmail's rules earn their
   keep against uncontrolled, heterogeneous, unsolicited senders. Here the
   operator authored every sender's brief, and the brief visibly controls the
   report shape: updater's uniform "update applied ✅ <sha>→<sha>" format is its
   brief's verify-before-apply contract speaking (VERIFIED against
   `.swarm/briefs/updater.md` reference in ledger); hardener's uniform "Task N
   GREEN" mirrors the operator's own numbered-task dispatch style.
3. **Zero questions is not luck; it is the escalation history repeating.** The
   predecessor system's audit found 4 of 51 operator-bound messages ever used
   the structured escalation format (SIMPLEST §4, VERIFIED row). The mail that
   actually flows to this operator is reports, and reports don't need routing —
   they need judging, which is the desk's job.

### 1c. Counterfactual rule runs — what would Gmail-style rules have done?

I wrote the plausible day-one rules an operator might define and ran them by hand
over all 22 bodies (MEASURED — the matches; REASONED — the usefulness verdicts):

- **Rule A, "needs my verdict":** body matches `GREEN|deliverable ready|COMPLETE|
  DONE|complete`. Hits 18/22 — exactly the work-report category. **Useful signal,
  zero new information:** all 18 were already open loops in the operator's own
  ledger; the desk (F4) and dispatch/verdict discipline (F2) already carry this
  distinction, defined at dispatch time by the person who will consume it.
- **Rule B, "routine, deprioritize":** `from:updater AND "update applied"`. Hits
  3/22 correctly. This is the one rule with real (tiny) value — and its correct
  home is shown in §3, extraction E1: the operator controls updater's brief, so
  the "routine:" marking can be emitted at the *sender*, where it costs one
  sentence of brief text and zero mechanism.
- **Rule C, "anomaly, escalate":** body matches `instab|killed|error|fail`.
  **Misfires on both sides.** It up-ranks the single *least* actionable message
  in the corpus — updater's watcher-instability FYI, whose own body says "No
  action needed unless you want a different watch mechanism" — and `fail` also
  substring-matches "falsifier", which appears throughout field-tester's
  entirely-routine probe reports. A keyword heuristic misclassifying by design
  is not a hypothetical: it is the exact epitaph of the graveyard's
  question-detection heuristic ("a hint, not ground truth" — SIMPLEST §4).
- **The rule nobody can write:** the corpus's real priority axis was
  *contract-class vs mechanical* — Task 3's one-sentence WORLD.md change needed
  the human personally; Task 1's 22 ported tests did not. That distinction
  appears nowhere in message text. It lives in the operator's dispatch entries
  (VERIFIED: ledger marks "contract-class: human reviews personally" at dispatch
  time). **Priority here is a property of the open loop, not of the message** —
  and the open loop is already recorded, by its definer, at the moment it opens.

### 1d. Mis-prioritization incidents: the ledger search

The brief asked: has the operator ever suffered urgent-mail-behind-routine-mail?
I read the full ledger looking for any incident of ordering damage
(MEASURED-by-exhaustive-read): **none exists.** The attention incidents in the
whole record are (a) the predecessor's co-injection drops (F4 — two messages
sharing one turn), fixed structurally by one-message-per-turn, and (b) the
red-operator Race 1 claim-then-die hazard, fixed by F5 claim lines before any
inbox idea was raised. The operator has processed every batch to date via the
desk, including the 13-message peak window, with no journaled complaint about
order. 22 messages, zero misorderings, zero backlogs: **there is no recorded
failure for prioritization to fix.**

---

## 2. VERDICTS

### Idea 1 — "different structure, harder to read/write without the tooling"

**Verdict: UNSUPPORTED (the opacity itself), and its strongest sub-need already
shipped last cycle as F5.**

- The mailbox is *already* structured: every message is a JSON record
  (`from/to/ts/body`), written only by `swarm send` (VERIFIED by parsing all
  22). The only genuinely new content in this idea is making it *harder to
  read* — and readability was deliberately **re-legalized yesterday**: hardener
  Task 7 (commit `e3d06db`) narrowed the queue-ownership sentence to move-only
  precisely because "world-readability is already the contract's stated posture
  (concepts 1, 4, 5)" (VERIFIED, the delivered report quotes the drafting
  choice). An opaque operator queue would reverse a decision the record made,
  with reasons, this week.
- Ask what failure the idea points at. Candidates from the brief: *accidental
  corruption by hand-edits* — zero recorded incidents (the one hand-touch in
  the record, span-after-1 hand-READING its queue, was openly journaled, moved
  nothing, and led to reading being legalized, not restricted); *enforcement of
  claim discipline* — F5 (move + hand-tagged claim line) shipped in the FINAL
  proposal and has been live since the operator's `[ops-main]` entries; its
  falsifier ("a delivered operator-mail file with no claiming journal entry")
  has never fired — it has also barely been exercised, so the honest posture is
  *wait for F5's falsifier*, not *add hardening on top of an untested
  discipline*; *a canonical access idiom* — F1's seat-take convention already
  names one (ps → journal grep → mailbox).
- Making the queue harder to *write* is worse than unsupported — it collides
  with a contract promise: "nothing ever refuses a message to the operator"
  (`swarm world`, VERIFIED). Any write barrier is a refusal with extra steps.
- REASONED, falsifier for this verdict: a real corruption or misclaim incident
  in the operator queue that F5's claim-line audit fails to catch. If that
  fires, the pre-priced next step is a *permissions* instrument (e.g. the
  delivered/ dir writable only via a `claim` verb), not format opacity.

### Idea 2 — "set up how and in what structure it wants to be pinged"

**Verdict: split. Wire-side ping machinery RHYMES WITH THE GRAVEYARD (the nag /
doorbell escalations). Presentation-side and sender-side structure HOLDS — and
most of it already exists as F1/F4 plus a practice the operator is already
doing unbriefed.**

- "Pinged" on the wire cannot mean push: "the operator is a mailbox, not a
  node… nothing pushes to the human" (`swarm world`, VERIFIED), and SIMPLEST F8
  assigns push-to-human to the multiplexer (a herdr tab badge), not the CLI.
  A configurable ping cadence is the nag reborn with a settings page — the nag
  died because it carried strictly less information than the mail it nagged
  about (SIMPLEST §4, VERIFIED row).
- What the operator can legitimately configure is **what the seat does when the
  human looks**: reading order, presentation shape, what gets surfaced first.
  That is F4's desk ("one ranked decisions page for the human, never the raw
  stream") plus F1's seat-take ritual — both just approved, both text, both
  operator-owned. The residual ask — *my* preferred structure — is exactly the
  shape the P7 kill preserved: the human's own standing words to their own
  sessions, "content, not contract" (FINAL, KILLED section, VERIFIED).
- The genuinely under-named part: **report shape is configurable at the
  sender**, and the operator already does it. Updater's telegraphic ✅ format
  and hardener's Task-N-GREEN format are brief-induced (§1b). No mechanism in
  the system knows this is happening; it costs one sentence per brief.
  Extraction E1 names it.

### Idea 3 — "categorise and prioritise automatically based on defined rules. Think Gmail."

**Verdict: the engine form RHYMES WITH THE GRAVEYARD (the `type` field, the
question-detection heuristic — both named corpses). The read-time convention
form is legitimate in principle — definer-is-consumer really does defeat the
§5 objection — but UNSUPPORTED today: the corpus gives rules nothing to do and
shows naive rules doing harm (§1c). Earnable; earning conditions and a probe
are specified.**

The exact line the brief asked me to locate:

- **Graveyard side of the line:** the *tool* stamping category/priority onto
  messages on the wire — a `priority` field in the message record, a rules file
  the hook evaluates at delivery, sender-visible tags. This is the `type` field
  with a config page. The type field died because it was a hardcoded taxonomy
  nobody consumed (SIMPLEST §2 row 10, §4); Philosophy §8's bias is "an engine
  never — unless the record shows conventions failing," and §1d shows no
  convention failing. Worse, message-record fields are contract-class: every
  agent must understand them (concept-count cost lands on all 9 concepts'
  users, not just the operator).
- **Acceptable side of the line:** the operator's own seat session, at READ
  time, applying triage text the operator wrote, to plain world-readable files,
  producing a presentation (the desk) — and the *reader is an LLM session, not
  a regex engine*, so "rules" are a paragraph of standing prose, not a
  pattern-matcher that up-ranks "No action needed" mail because it contains
  the word "killed" (§1c Rule C). Nothing on the wire changes; senders can't
  see it; other humans configure differently at zero cost; deleting the
  paragraph deletes the feature. This is Gmail's actual architecture lesson —
  client-side, at presentation, configured by the recipient — imported
  *without* Gmail's mechanism.
- **Does definer-is-consumer flip the §5 verdict?** Argued both ways, as the
  brief requires. *For:* the type field's fatal defect was producer-defined
  taxonomy with no consumer; an operator-authored triage paragraph read by the
  operator's own seat has definer = consumer by construction, so that specific
  death does not apply. *Against:* §5's deeper test is "delete the distinction
  before you configure it" — and §1c shows the corpus currently has only one
  real distinction (needs-verdict vs routine), which the dispatch/verdict
  discipline (F2) already records at higher fidelity than any message-text
  rule could recover. A rule system with one rule that duplicates an existing
  record is a config field for a distinction that already has a home. **Both
  arguments land in the same place: legitimate form, no present need.**
- What would create the need: mail volume or heterogeneity the desk ritual
  can't absorb in one seat-take. Probe P-VOL (§5) defines the threshold
  observation instead of guessing.

---

## 3. RANKED EXTRACTIONS

What survives, ranked. Each: smallest implementation, concept cost, falsifier,
and the evidence that would earn the next rung. Ladder discipline throughout:
convention → instrument → never engine.

**E1. Sender-side report shape, named as a practice.** *(extract now — it is
already true, just unnamed)*
- Smallest implementation: one sentence in the operator seat section of
  SKILL.md: "You control every sender's brief: when a report category exists
  (routine confirmations, FYI-no-action), have the brief say so in the
  message's first line — shape mail at the sender, not the mailbox."
- Concept cost: 0 (briefs already carry report instructions; this names an
  existing habit, the same move STRUCTURE.md made for warm-name reuse).
- Falsifier: a brief-specified first-line marker that senders drift off of
  within a week (would show briefs can't hold format discipline, and the
  marker needs to move… nowhere — it dies; markers are not load-bearing).
- Earns next rung: nothing. This is terminal; it never becomes an instrument.

**E2. The seat triage paragraph — operator-authored reading order, applied at
read time by the seat session.** *(extract as a slot, fill only on evidence)*
- Smallest implementation: an optional, operator-written paragraph in the seat
  skill (or the operator's own journal preamble — their words to their
  sessions): e.g. "at seat-take, surface in this order: anything matching an
  open contract-class loop; then work-complete reports oldest-first; routine
  ✅ confirmations last, one line each." The seat session reads it like any
  other standing instruction. No file format, no evaluator, no tags.
- Concept cost: 0 contract concepts; one paragraph of seat text. (It composes
  with F1's seat-take and F4's desk — it *is* a desk-rendering preference.)
- Falsifier: two consecutive stints where the seat demonstrably ignores the
  paragraph (desk order contradicts it) — would show prose preferences don't
  survive contact and only then justifies discussing an instrument.
- Earning condition (do NOT add today): P-VOL fires — a seat-take where
  waiting mail exceeds what one reading pass absorbs, journaled as such by the
  operator. Until then this slot stays empty; 22 messages in 21 hours with
  zero backlog earns nothing (§1a, §1d).

**E3. Pre-priced instrument, named so nobody invents a bigger one:
`ps` sender-grouping or `--from` filter for the operator's waiting-mail view.**
*(do not build)*
- Smallest implementation *if ever earned*: a read-only rendering option on
  the one existing view. No new state, no message-record change.
- Concept cost: ~0.5 (a flag on an existing verb — still a §5 smell; that is
  why it needs a fired falsifier first).
- Falsifier-to-earn (must fire first): E2's paragraph exists AND a stint's
  journal shows the seat mis-ordering because the flat oldest-first listing
  buried structure that grouping would have shown. No such observation exists
  or is close to existing.

Ranking rationale: E1 is free and already true; E2 is the entire legitimate
content of ideas 2+3 compressed to its convention form; E3 exists only to cap
the instrument conversation with the smallest possible pre-priced answer.

---

## 4. NOT-LIST

Explicitly rejected, each with its corpse or contradiction:

1. **No `priority`/`category`/`type` field in the message record.** The type
   field is a named grave (SIMPLEST §2 row 10); definer-is-consumer does not
   apply on the wire, because every agent pays the concept cost and no agent
   consumes the field.
2. **No rules engine, rules file, or hook-evaluated filters at delivery.**
   Philosophy §8: engine never, absent a recorded convention failure; §1d
   shows none. Rule C (§1c) shows mechanical matching actively mis-ranking
   this corpus.
3. **No keyword urgency detection anywhere.** The question-detection
   heuristic's grave, plus a live demonstration: `fail` matches "falsifier"
   in 6/22 messages; "killed" flags the least urgent mail in the corpus.
4. **No opaque or binary mailbox format; no read barrier.** Contradicts
   world-readability (world concepts 1/4/5) and reverses the move-only
   narrowing decision (`e3d06db`) made with stated reasons this week.
5. **No write barrier on the operator queue.** "Nothing ever refuses a
   message to the operator" is contract text; a write barrier is a refusal.
6. **No read/unread/ack state, no nag, no re-ping cadence.** The three-state
   inbox machine, ack semantics, and the nag are all named graves (SIMPLEST
   §2 rows 13–15, §4); "configurable ping structure" on the wire is the nag
   with preferences.
7. **No push-to-human machinery in swarm.** F8's boundary: push is the
   multiplexer's job (tab badge), and the one live watcher instrument is
   already owned and accounted (F6); it is a seat arrangement, not a system
   surface.
8. **No auto-archive / auto-move of operator mail by any rule.** Only a claim
   (move + journaled claim line, F5) may move operator mail; an automatic
   mover would manufacture claims with no claimant — exactly the record-
   falsification the move-only sentence exists to prevent.
9. **No second inbox, folder taxonomy, or per-category queues.** Folders are
   the three-state machine with more states; the delivered/ split plus the
   ledger's open loops already partition the world into the only two sets
   the record uses (claimed / not yet claimed).

---

## 5. DESIGNED-NOT-RUN PROBES

**P-VOL — the volume threshold probe** (gates E2's earning condition).
- Design: zero new tooling. For the next 10 operator seat-takes, the seat's
  existing F1 ritual already touches the mailbox; add one measured line to the
  seat-take journal entry: waiting-count at seat-take, count actually read
  this stint, and a yes/no "did anything wait past a stint it should not
  have" (operator's own judgment, one word). 10 entries = the dataset.
- Fires (earning E2's paragraph) if: any entry records unread-carryover the
  operator calls wrong, or waiting-count at seat-take exceeds the operator's
  declared span number (~3, per SPAN §3c's desk sketch) times three.
- Cost: one journal line per stint, ~2 minutes total across the whole probe.
  Risk: none — it is observation of a ritual that already runs.

**P-TRIAGE — one-stint triage-paragraph trial** (runs only if P-VOL fires).
- Design: operator writes the E2 paragraph in their own words; one seat stint
  runs with it; the artifact judged is the desk that stint produces, diffed by
  the operator against what they actually wanted first. One stint, then a
  keep/kill verdict journaled.
- Fires (kills E2) if: the desk with the paragraph is judged no better than
  the desk without it — in which case the paragraph is deleted and this
  document's E2 slot is closed with that evidence.
- Cost: one paragraph of writing + one ordinary stint. No tool changes.

**P-CLAIM-AUDIT — F5 exercise check** (guards the Idea-1 verdict).
- Design: after the next 20 operator messages are claimed, one grep pass:
  every `delivered/` file newer than F5's adoption has a matching hand-tagged
  claim line in the operator journal (the F5 falsifier, actually checked once
  rather than assumed).
- Fires if: any claimed file lacks a claim line — reopening Idea 1's
  *enforcement* sub-need with real evidence, and pointing at the pre-priced
  permissions instrument (§2, Idea 1) rather than opacity.
- Cost: one grep + ten minutes, by whoever holds the seat.

---

## 6. SUMMARY FOR THE SEAT

The corpus says the operator's inbox problem does not exist yet: 22 messages,
one speech act dominating 18 of them, zero questions, zero urgencies, zero
backlogs, zero misorderings — and every priority distinction that mattered was
already recorded by the operator at dispatch time, where it belongs. The
legitimate kernel inside all three ideas is the same small thing: **the
operator may write down, in their own standing words, how their own seat reads
their own mail** — that is E2, it costs a paragraph, and even it is not earned
until volume says so (P-VOL). Everything mechanical — fields, rules, engines,
opacity, pings — has a named grave or a named contradiction waiting for it.

Shape mail at the sender (you write the briefs). Rank at the desk (you own the
seat). Put nothing on the wire.
