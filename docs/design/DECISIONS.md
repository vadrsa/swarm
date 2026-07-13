# DECISIONS — a decision engine for the operator's gate, researched against the record

**Author:** `decision-scout`, research-only, reporting to the operator. Written at
`main@834fec4`, 2026-07-10. Revised same day after adversarial review by
`red-decisions` (1 KILL, 9 WOUNDs — `.swarm/research/red-decisions-review.md`);
the revision notes at each formerly-wounded site say what changed. No code
written, no behavior changed; this document is the whole deliverable.

**The question under research (operator's brief, near-verbatim):** a decision
engine that proxies decision points bound for the operator — learns from recorded
decision history ("training"), answers on the operator's behalf at high confidence
("auto-answer on confidence"), passes through when uncertain. The brief flags its
own sensitivity: this rhymes with the buried question-detection heuristic
(SIMPLEST §2 row 16, §4) — find what is genuinely different or say nothing is.

**Evidence discipline:** **VERIFIED** (I read the line / ran the command),
**MEASURED** (instrumentation over the real corpus by my miners, method stated in
their tables), **REASONED** (judgment; falsifier named). Primary evidence: two
mined decision tables built for this research — `.swarm/research/ledger-miner-decisions.md`
(all 35 messages ever routed to the operator seat, cross-referenced against the
operator journal line-by-line) and `.swarm/research/pr-miner-decisions.md` (all 78
PRs ever merged or rejected, latency-dated, journal-corrected). Doctrine inputs
read in full: `swarm world`, PHILOSOPHY.md (§2, §5, §8, §9, §10), SIMPLEST.md,
INBOX.md, SPAN.md, HARNESS.md §1, the operator-capabilities FINAL proposal. Every
citation in this revision was re-checked after the red review found tag inflation
in the first draft (its W1/W6/W7); where a conclusion is a miner's judgment
rather than its measurement, it now says REASONED.

---

## 0. TWO HOPS, NOT ONE (read this first)

Decision points reach the human in two hops, and the record measures them
separately (VERIFIED, ledger-miner §0 — built to prevent exactly the conflation
this section guards against):

- **Hop 1, children → seat:** the 35 delivered messages. The seat — the
  `[ops-main]` hand, an agent — verifies, judges, amends, declines, adjudicates.
  This is a coordinator doing its native job under existing doctrine. **No part
  of this design governs hop 1.**
- **Hop 2, seat → human:** the desk and the merge gate. This is where the
  human's attention is spent, where pre-auth emerged, and where the engine the
  brief imagines would operate. **Everything this document recommends applies to
  hop 2 only.**

*(Revision note: the first draft narrated hop-1 seat judgments as human judgment
and sized the engine's benefit on hop-1 volume — red-decisions W4/W5. The
analysis below re-derives everything per hop.)*

## 1. WHAT THE RECORD SAYS

### 1a. Hop 1: the seat's gate is bimodal, and the split is visible ex ante

Of 35 messages ever routed to the seat, 25 carried decisions; 14 of those (56%)
were mechanical-in-hindsight — the outcome never deviated from the sender's
recommendation (MEASURED, ledger-miner §2). The split is nearly bimodal:

- **Dispatched work returning GREEN: 11/11 mechanical.** Not one hardener
  return was ever overridden, amended, or rejected — including both self-flagged
  deviations, accepted with the sender's own stated reason.
- **New questions / research deliverables / costed options: 10/14 genuine
  judgment** — but that judgment is the **seat's** (amendments, splits,
  declines, adjudications: "my call, stated to user" — VERIFIED, ledger row 19).
  It is coordinator work the seat already absorbs with no engine, and no
  conceivable authorization line covers it — you cannot pre-authorize an
  adjudication. The design must leave hop 1 alone or it *degrades* the tree
  (forcing native seat judgment to pass through would press MORE on the human).

What makes hop 1 relevant to hop 2 at all is the signal question — §1b.

### 1b. The separating signal exists before the fact, and it is participant-authored

The brief asked whether any signal separable *before the fact* distinguishes the
rubber-stamps from the genuine calls. Yes — in rank order on this corpus
(MEASURED for the correlations, ledger-miner §3.5; the rank order is the miner's
REASONED reading):

1. **Loop topology** — closes an open loop in the operator's ledger vs opens a
   new one. Closers: 14/15 mechanical. Openers: 10/11 judgment-or-open.
2. **Sender** (a proxy for dispatch shape: hardener receives fully-specified
   dispatches, so its returns can only confirm or fail spec).
3. **The sender's own decision markers** — "your call", "awaits your approval",
   "TWO DECISIONS ARE YOURS".
4. **Recommendation + measured evidence attached** → adopted, approximately
   always; costed option without a recommendation → real judgment call.
5. **Class of surface touched** — contract-class vs mechanical. The class label
   itself is written by the operator at dispatch time (VERIFIED, operator
   journal J:15, J:21; INBOX §1c found the same on its corpus prefix: "priority
   here is a property of the open loop, not of the message").

What these five share: **all are participant-authored** — written by the sender,
the dispatcher, or the operator, not stamped by any tool. Signals 1 and 5 live
in the ledger; signals 2–4 are read out of message bodies *by the seat, at read
time* (an LLM reading prose — INBOX's legitimate side of the line, not a
pattern-matcher). The first draft claimed "none is computed from message text";
that was false for three of five (red W6) and the honest statement is weaker but
sufficient: **nothing here requires the tool to detect anything, and the two
strongest hop-2-relevant signals (loop topology, declared class) never touch
message surface at all.**

On this corpus, read in hindsight, the labeling held: no genuine decision was
found hiding in an unlabeled message, and no labeled decision dissolved
(MEASURED, ledger-miner §3.2). **The caveat the first draft omitted (red W2):
there is no pre-registered marker vocabulary — the miner enumerated the judgment
messages and then located a marker in each, and one "marker" was an offhand
aside ("assuming that was you") that the seat *chose* to treat as
decision-bearing.** So the defensible claim is not "declarations are 100%
honest"; it is: *this corpus, generously read, is well-labeled, and the honesty
of declarations under growth is an open question this design must watch, not
assume* (§6 F2, with a collector this time).

### 1c. Hop 2: the human's gate is already ~fully delegated, informally, and the drift is unmeasured

The human-layer record (MEASURED where sourced, pr-miner §a–c; ledger-miner
§3.4's universal rule is the miner's REASONED conclusion and is treated as such
here):

- **As merge gate: 14/14 swarm-era PRs merged as recommended, zero rejections**
  (the 63 earlier PRs predate any gate — opened and merged in the same working
  session, 53 of them in under 60 seconds; "merging was execution, not review"
  — VERIFIED, pr-miner era note. They are excluded from every merge-rate and
  absorption claim below — #62, one of them, appears in §1d as the record's
  only rejection, a role that does not depend on gate-era statistics; the
  first draft leaned on them for volume and red W5 caught it).
- **The gate collapsed into standing authorization within a day:** #65–#68
  waited 16–17h for the human's session (then merged as a batch 26 seconds
  apart); #72/#73, contract-class, got 2.8h; #74, also contract-class, was
  merged under pre-auth in **14 seconds**; #76/#78 in 3–4s (MEASURED, pr-miner
  §c "tier drift"). The tier labels stayed; the attention behind them thinned.
- **Genuine human judgment, wherever the record shows it, is an initiation or a
  correction, never a gate answer**: rejected the overseer agent, "recon should
  shrink", R1/R2, the choice-doctrine process correction, "decision POINTS, not
  questions" (VERIFIED instances, ledger-miner §3.4; the "never" is REASONED —
  it is an absence claim over a two-day corpus).
- **The one decision that ever aged** — codex design, >18.5h open — is
  contract-class, has no recommendation to stamp, and commits future
  architecture.

This reframes the research question. "Auto-answer on confidence" already
happened: a recurring decision shape got compressed into standing pre-auth, and
answers now issue under it in seconds without per-instance human attention. The
choice is not whether to have a decision engine — the operator built one by
hand this week. **The choice is whether it keeps running as unmeasured drift or
gets what every other delegation here gets: explicit grants, an audit trail,
and falsifiers.** And the honest corollary (red W8): since the human's
mechanical-gate attention is already near zero, **the engine's product is not
absorption — that is done — it is legibility and bounds on the delegation that
already exists.** This document prices it as such (§4c).

### 1d. The strongest single datum: PR #62

One decision in the entire record was a rejection, and it is load-bearing
(MEASURED, pr-miner §b–c). PR #62 was green, verified, and built to the
operator's own prior ruling — then halted, "not because the code is wrong,"
because the operator had reinterpreted the *incident that justified the ruling*.
Three facts:

- **It was invisible at the decision surface.** Diff, tests, spec compliance —
  all clean. Any confidence model scoring decision-surface features would have
  auto-answered it wrong.
- **It was invisible in the record — until the halt.** The halt comment is
  the *first trace* of the reinterpretation anywhere in the mined record —
  both tables and the operator journal (VERIFIED for that corpus, pr-miner
  §b.1; that no earlier trace exists anywhere else is REASONED — an absence
  claim). The shift lived in the human's head. This matters
  more than the first draft allowed (red K1): no seat instruction to watch for
  "visibly moved premises" can catch a premise shift that has no record trace.
- **The save required two things, and the design must preserve both.** The
  harness permission classifier denied the agent's `gh pr merge` as
  self-approval — a dumb, scope-limited grant checker bought *delay*. The halt
  itself came from **live human attention** — the operator was actively
  re-examining ruling 1 while the escalation waited (VERIFIED sequence,
  pr-miner §c). The first draft credited the classifier alone; red K1 is right
  that this misattributes the save. The lesson, corrected: **narrow authority
  buys the time in which human attention can act; nothing replaces the
  attention.** A design that widens authority on surface confidence deletes the
  first; a design that thins human attention over ungranted classes deletes the
  second. The recommendation below is shaped by both halves: grants are narrow
  and reversibility-bounded (the classifier half), and everything ungranted
  passes through whole so the human's attention stays live exactly where
  premise shifts would land (the attention half).

### 1e. Why the approval rate cannot be trusted as training signal

The 100% stamp rate on GREEN returns is **endogenous**. Children verify before
reporting because the seat re-verifies everything ("verified 59/59 green myself"
— VERIFIED, operator journal J:8), and the seat verifies because the parent's
actual reading "is the only thing standing between the swarm and obedience
theater" (VERIFIED, SPAN §1). No GREEN in the corpus was ever false — so whether
the verification is load-bearing or ceremonial is **unfalsifiable from this
record** (ledger-miner §4). An engine trained on "operator approves 95% of X"
learns a policy whose validity depends on the reading it would remove. Delegate
the verdict on the strength of that statistic and the statistic decays
underneath you — Goodhart, in one sentence. (REASONED; falsifier: §6 F4.)

---

## 2. THE GRAVES — PLURAL — AND WHAT IS GENUINELY DIFFERENT

The brief demands this be answered, not hand-waved. The first draft answered it
against a chimera — it attributed the type field's death causes to the question
heuristic under a VERIFIED tag (red W1). There are two distinct graves, and both
constrain this design; here they are with their own epitaphs:

**Grave 1 — the question-detection heuristic** (part of SIMPLEST §2 row 16's
deleted taxonomy). Cause of death: **misclassification by design** — "a
heuristic over facts the transcript already holds; it misclassifies by design
('a hint, not ground truth')" (VERIFIED, SIMPLEST §4). It guessed decision-ness
from surface form because nothing declared it. INBOX §1c re-demonstrated the
failure live: keyword urgency detection up-ranks the least actionable mail in
the corpus and substring-matches "fail" inside "falsifier."

**Grave 2 — the `type` field** (SIMPLEST §2 row 10). Cause of death:
**wire-side and consumerless** — a hardcoded, producer-defined taxonomy in the
message record that no decision ever keyed on, whose concept cost landed on
every agent (VERIFIED, SIMPLEST §2 row 10; INBOX §2 Idea 3 draws the same line).

**What is genuinely different this time — each difference matched to the grave
it escapes:**

1. **Declaration has replaced detection** (escapes grave 1). The old heuristic
   had to guess; today the strongest signals are written down before the answer
   exists — the dispatch entry opens the loop, the class is declared at
   dispatch, the sender marks its asks — and on this corpus, read in hindsight,
   the labeling held (§1b, with §1b's stated caveat). An engine that *consumes
   declarations* contains no classifier over surface form. What it does still
   contain — the seat reading prose asks at read time — is an LLM judgment act,
   conceded openly (§3), not a stored taxonomy.
2. **Definer-is-consumer, off the wire** (escapes grave 2). The classes are
   authored by the operator at dispatch, live in the ledger and the operator's
   own standing text, are consumed by the operator's own seat, and cost no
   agent a concept. Deleting the text deletes the engine. INBOX §2 located this
   exact line for triage; this design inherits it for authority.
3. **The precedent runs and has a track record.** Tiered delegation has
   operated for a day: no merge misfire, zero reverts — and one averted
   disaster (#62) plus one measured pathology (tier drift, §1c). The question
   heuristic never had a record of its convention working; this one does,
   including exactly where it strains. PHILOSOPHY §8's bar — "an engine never,
   unless the record shows the convention failing" — is met in the only honest
   direction: the convention (informal pre-auth) is failing *at auditability*,
   and what that earns is audit structure, not answer machinery.

**And one thing is NOT different, so the design must refuse it:** any component
that infers decision-ness or confidence *from message surface* — keywords,
scores, learned classifiers over decision features — is grave 1 with a newer
shovel. #62 is the proof that the hard residual is invisible at the surface.
(§6 F2 names the observation that would show this document's own alternative
failing, and §4a now prices the one detection variant that would not rebuild
the grave, rather than pretending the space has no such corner — red's
steelman.)

---

## 3. WHAT COUNTS AS A DECISION POINT (the definition that won't rot)

> **A decision point is an open loop awaiting the operator's verdict: a
> dispatch entry without its verdict entry, a desk item, or a delivered
> message whose sender named something as the operator's to decide. It exists
> because a participant declared it, and it is enumerated by reading the
> ledger, the desk, and the operator's mail — never by a stored classification,
> a taxonomy field, or any mechanism outside the reading seat.**

Why this definition resists rot where grave 1 could not:

- **It is extensional where it can be.** Two of its three clauses are lists the
  system already keeps: F2's open loops (dispatch-without-verdict is already
  the ledger's own definition — VERIFIED, operator-capabilities F2) and F4's
  desk. Surface forms can change freely; a list mechanism does not care.
- **Its third clause is a read-time judgment, and this document says so
  plainly** (the first draft claimed "never by classifying message text" while
  including this clause — red W3 caught the contradiction). Recognizing a
  sender's ask ("your call", "awaits your approval" — or an aside like
  "assuming that was you") is the seat reading prose and exercising judgment.
  What separates this from grave 1: the judgment is made by the party who
  consumes it, at read time, leaves no stored label, keys no mechanism, and is
  auditable by re-reading the same message. It is the same act as the seat
  judging any artifact — which is the system's oldest working principle, not
  its buried one.
- **It is broader than "question" for free.** A PR sitting unmerged, an
  AskUserQuestion, a "your call" in a report, a benchmark awaiting
  authorization — each is an open loop under this definition regardless of
  grammatical shape. The operator's chosen term is satisfied without any
  taxonomy of forms.
- **Its failure mode is nameable, and now has a collector.** The definition
  under-counts only if a genuine decision exists that nobody declared and the
  seat's reading missed. Zero exist in the corpus as read (§1b, caveat owned).
  §6 F2 assigns the watch: one line per operator stint review — "did anything
  this stint turn out to have been a decision nobody surfaced?" — the P-VOL
  shape (a designed-not-run probe pattern from INBOX §5, named as such), plus
  the standing rule that any such find is journaled where it was found. The
  day one is found, declaration is insufficient, and §4a already prices the
  smallest legitimate response.
- **Its incentive is aligned.** A sender who under-declares gets a stalled
  loop; a sender who over-declares spends the operator's attention and is
  judged for it (PHILOSOPHY §9). Declaration quality is a judged artifact like
  everything else here; no mechanism polices it.

---

## 4. THE DESIGN SPACE, AND THE RECOMMENDATION

### 4a. The space (why the other corners lose, honestly this time)

Two axes: *where confidence comes from* (learned model vs declared
authorization) × *what the component does with it* (answers vs flags). Plus the
wire/seat placement question, which is settled once for all corners: anything
evaluated by the tool on the message path puts fields or rules where every
agent pays concept cost and no agent consumes them — grave 2's exact shape.
(The first draft claimed INBOX's NOT-list #2 had "already buried" declared×wire;
red W7 corrected the cite — NOT-list #2 buries delivery-time *triage filters*,
not authorization rules. The concept-cost argument stands on its own and is the
actual kill; INBOX §2 Idea 3's wire-side analysis is the precedent it leans on,
correctly this time.)

- **Learned model that answers.** Dead three ways, none rehabilitated by the
  red review's steelman pass: the training corpus is 25 decision-bearing
  messages whose observed variance is carried by participant-authored signals
  (§1b) — though note the honest form of this claim: *no evidence a model is
  needed yet*, not "settled forever" (red steelman 1; n will grow, and §6 F2/F5
  are the review triggers); the residual it must catch is surface-invisible
  (#62); and its miscalibration is the worst kind — a wrong answer issued under
  the operator's authority, exactly the "plausible wrong value" PHILOSOPHY §10
  ranks below an honest unknown.
- **Learned model that only flags** (adds pass-throughs, never answers) — the
  corner the first draft ignored and the red review built: miscalibration-safe
  by construction (a false flag costs only operator attention). It still loses
  *today*: there is nothing for it to flag that declarations don't already
  carry, and its false-positive budget spends the exact resource this whole
  design exists to protect. But it is the **pre-priced next instrument if §6
  F2 ever fires** — if genuine decisions start hiding in unlabeled mail, a
  flag-only reader (seat-side, no stored labels, no answer authority) is the
  smallest legitimate detection, and this document names it now so nobody
  builds a bigger one. (The same pre-pricing move as INBOX E3.)
- **Declared authorization, evaluated on the wire.** Killed by concept cost,
  above.
- **Declared authorization, applied at the seat.** The operator writes standing
  authorizations; the seat answers under them, citing them; everything else
  passes through whole. The only corner with a live precedent (pre-auth,
  running now), zero new concepts, and a miscalibration story that survives
  #62 — via the scope bound, not via premise clairvoyance (§4b.3, rebuilt
  after red K1). **It wins.**

### 4b. RECOMMENDATION: the standing-authorization ledger

Make the engine that already exists explicit, auditable, and falsifiable. Five
parts, all text, zero code, zero wire changes, zero new concepts:

1. **Authorization lines, with provenance.** The operator's standing
   authorizations live in the operator journal's standing-goals section —
   their words to their sessions, content not contract (the P7-kill shape,
   VERIFIED, operator-capabilities KILLED). Each line names: **scope** (which
   decision class, keyed to the dispatch-time declaration — e.g.
   "mechanical-class PR, verified green by the seat"), **grant** (what the
   seat may answer without asking), **reversibility bound** (only decisions
   cheap to reverse may be granted; and note honestly — red W9 — that
   reversal cost is *asserted* today, zero reverts having ever exercised it;
   the pilot's first overturn prices it for real), and **review trigger**
   (expiry, count, or named premise). **The provenance rule (added for red
   W9): a grant line is valid only if it quotes the human's own utterance
   verbatim, or the human wrote or edited the line themselves.** The seat
   journal is seat-authored — the existing pre-auths exist on the record only
   as the seat's paraphrase of the user ("user pre-auth", J:59). A grant the
   human never touched is a manufactured claim wearing a signature, and every
   citation of it would launder the manufacture into precedent. Quoting the
   grantor is this design's F5-claim-line move: it makes the grant witness
   its granter.
2. **The citation rule.** The seat auto-answers a hop-2 decision point
   **only** when it can cite a specific authorization line covering it, and
   the verdict entry names the line — the discipline HARNESS §1a imposes on
   harness choice ("a parent writing 'codex, because it's better at X' would
   be citing a vibe"). **Confidence is binary citability, not a score.** No
   citable line → pass through to the human, whole. This is SPAN's
   cap-as-self-test pattern applied to authority: the thing that could have
   been a stored number is instead a test anyone can run on the record (does
   the cited line exist, quote its grantor, and cover the case?). The red
   review attacked this as a possible score in disguise and reported it
   holds: binary, threshold-free, no stored number (red HOLDS list). Hop-1
   dispositions — the seat's native coordinator judgment — are explicitly
   outside the citation rule (§0, §1a; red W4).
3. **The scope bound carries #62; the premise clause is best-effort and says
   so.** *(Rebuilt after red K1, which killed the first draft's version.)*
   The design's real defense against the #62 class is structural, not
   clairvoyant: **(a)** grants are narrow and never cover contract-class or
   contract-adjacent surfaces — #62 (a send-contract change) falls outside
   any legal line's scope, which is the one mechanism that catches it *on the
   record as it stood* (red K1's honest replay: caught once, by scope, not
   twice); **(b)** everything ungranted passes through whole, which keeps
   live human attention exactly where record-invisible premise shifts land —
   the half of the #62 save that no mechanism replaces (§1d). On top of that,
   two cheap best-effort layers, honestly labeled: the seat voids any
   authorization for a decision point whose premise has moved *on the
   record* (a reopened ruling, a sender's self-flagged deviation or surprise
   — record-visible shifts exist even though #62's wasn't one); and **the
   premise sweep**: whenever the human initiates a correction or
   reinterpretation — the channel where, per §1c, their genuine judgment
   actually appears — the seat sweeps recent proxied answers for any that the
   shifted premise touches, and reopens them. This gives §6 F3 a collector:
   premise misses surface at the next human initiation, not by accident.
4. **Attribution.** A proxied answer issues in the seat's name, citing the
   authorization — never in the operator's voice. The record must always show
   who answered and under what grant (the F5 claim-line principle extended to
   verdicts — an extension, marked as such: an answer with no author is a
   manufactured claim, the same falsification the move-only queue sentence
   exists to prevent, VERIFIED, INBOX NOT-list #8 / the Task 7 narrowing). A
   wrong proxied answer is then a *bounded, attributed, revertible* event —
   categorically better than a wrong answer wearing the operator's voice,
   which is the miscalibration the brief names as the worst case.
5. **The audit loop, priced honestly** *(rebuilt after red W8)*. Two regimes:
   - **Pilot regime (§5): check everything.** ~30 proxied answers is too few
     to sample against a rate; it is few enough to review exhaustively. The
     operator (or a hand they direct) reads every proxied verdict entry of
     the stint and marks overturns. Cost: this is real re-verification work,
     not "minutes" — which is why the pilot grants only classes whose check
     is cheap (a mechanical PR's overturn check is "would I have merged
     this?", not a re-run of the suite; the seat already ran the suite, and
     *that* verification is hop-1 work the engine doesn't touch).
   - **Steady state: sampled, with a calibration constant that knows it is
     one.** Per stint: proxied count, pass-through count, sampled overturn
     check. The "~1 in 20" revocation threshold in §6 F1 is offered as
     calibration, not law — the SPAN §3a move: the operator's own judgment
     overrides the number in both directions, and the number exists so drift
     has to argue with something written down. (Red's steelman 2 noted the
     first draft smuggled a threshold back in while condemning thresholds;
     the difference — it gates *revocation of a grant*, never *issuance of
     an answer*, and it binds the human's review ritual, not a model — is
     now stated rather than assumed.)
   Tier drift — today invisible — becomes a number the record keeps either
   way: that, not absorption, is what the audit buys (§4c).

**"Training" is a promotion ritual, not a model.** When the ledger shows the
same decision shape stamped repeatedly (recurrence is already named in dispatch
entries — STRUCTURE suggestion 1, shipped and live), the seat may *propose* an
authorization line, with the record rows as evidence. The human ratifies —
and under part 1's provenance rule, ratification means the human's own words
enter the line, not the seat's summary of them. Symmetrically, the audit loop
*demotes*: an overturned answer or a fired review trigger revokes or narrows
its line, journaled like any verdict. Learning lands in operator-owned text,
where deleting a line deletes the behavior.

### 4c. What this buys, priced against the record (not oversold)

*(Rebuilt after red W5/W8: the first draft claimed ~70/78 PRs of absorption;
63 of those predate any gate, and the human's mechanical-gate attention is
already near zero under informal pre-auth. The honest ledger:)*

- **Absorption: ~nil versus the status quo.** The absorbable hop-2 corpus is
  the swarm-era mechanical tier (~9–11 PRs to date) plus whatever pre-auth
  already swallowed in seconds. The engine does not save the human meaningful
  new time. Anyone adopting this design for throughput is buying the wrong
  thing.
- **What it actually buys:** (1) **legibility** — the standing grants that
  today exist as seat paraphrase become quoted, scoped, expiring text; tier
  drift becomes a measured number instead of a 16h→14s slide nobody recorded;
  (2) **bounded miscalibration** — scope bounds, reversibility bounds,
  attribution, and the pass-through default preserve both halves of the #62
  save (§1d); (3) **a ratchet that can go backwards** — revocation is one
  journal entry, and the whole engine deletes by deleting text.
- **Its price:** one operator writing session (the lines), a per-stint audit
  line, exhaustive review during the pilot, and the premise sweep on human
  corrections. That price is paid in the exact currency the system protects —
  operator attention — and §6 F5 kills the design if the ledger shows the
  price exceeding the legibility it buys.
- **Replay checks** (REASONED — hindsight replay, with the standard caveat
  that behavior shifts under new rules): the 11 hardener GREENs stay hop-1,
  untouched. The swarm-era mechanical merges fall under one line. #62 is
  caught once, by scope (contract-adjacent — outside any legal grant), and
  the human's attention on it is preserved by pass-through, not by a clause
  pretending to read minds. The codex decision (>18.5h open, the only aged
  one) passes through untouched: contract-class, no recommendation to stamp.
  **Aging is correct behavior** — the system refusing to guess. The engine
  must not treat pass-through latency as a defect; §9's standard is *clean*,
  not *fast*.

### 4d. NOT-list

1. **No learned classifier, confidence score, or threshold over decision
   features that issues answers.** n=25 and the residual is
   surface-invisible (#62). The flag-only variant is pre-priced in §4a and
   earns consideration only if §6 F2 fires.
2. **No wire-side anything**: no decision-point or priority field in message
   records, no rules evaluated at delivery, no tool-stamped tags. Grave 2,
   plus concept cost on every agent (INBOX §2 Idea 3's line, extended here
   from triage to authority on its own argument, not on a borrowed burial).
3. **No keyword/surface detection of decision points.** Grave 1, verbatim
   (SIMPLEST §4; INBOX §1c Rule C's live demonstration).
4. **No auto-answer in the operator's voice.** Attribution or nothing.
5. **No grant without quoted human provenance and a written review trigger.**
   An unexpiring grant is tier drift with a signature; an unquoted grant is a
   forged one (§4b.1; red W9).
6. **No engine on hop 1, and none on the initiations channel.** The seat's
   coordinator judgment is native authority (§1a); direction-setting is
   constitutionally the human's, and the record shows it is the only place
   their judgment actually operates (§1c).
7. **No latency SLO on pass-throughs.** The one aged decision aged because it
   deserved to; making "open" uncomfortable rebuilds the nag.

---

## 5. A PILOT, DESIGNED AND COSTED (build nothing)

Two weeks, zero tooling, reversible by deleting text:

1. The human writes (or edits into their own words) 2–4 authorization lines
   with quoted provenance. Candidates the record already supports:
   mechanical-class PR merges (the existing informal pre-auth, finally
   written down and scoped); probe/benchmark spend under a named token budget
   (the desk's standing "benchmark smoke ~0.5M run y/n" item — VERIFIED,
   operator journal J:81 — is exactly this shape). Updater-style FYIs need no
   line; they carry no decision.
2. The seat operates the citation rule + scope bounds + premise sweep from
   the next stint. Every proxied verdict entry names its line (one clause on
   the F2 verdict-entry convention — a SKILL.md sentence, the only shippable
   text in this design, and it waits for the pilot's verdict).
3. Per stint: the audit line (proxied / passed-through / overturns), with
   **exhaustive** review of proxied answers during the pilot (§4b.5).
4. After ~2 weeks or ~30 proxied answers: read the numbers against §6.
   Adopt (the SKILL.md sentence ships), narrow, or kill — killing is
   deleting the lines; nothing else exists.

Cost: one human writing session; minutes per stint for the audit line;
real review time proportional to proxied volume (bounded by granting only
cheap-to-check classes); the premise sweep on human corrections. Risk bound:
every granted class is reversibility-bounded by construction — while owning
(red W9) that reversal has never been exercised in this repo's history, so
the first overturn is also the first real price datum on "revertible."

---

## 6. FALSIFIERS (what would show this design wrong — each with its collector)

1. **Overturn rate** (collector: the per-stint audit line). Pilot: any
   overturn at all triggers a line review — with ~30 exhaustively-checked
   answers, one overturn is signal, not noise. Steady state: more than ~1 in
   20 sampled → the lines are too coarse; narrow them. Overturns concentrated
   in one line → revoke it. An overturn that proves *expensive* to reverse →
   the reversibility bound failed where it matters most; shrink the engine's
   scope immediately and re-price every remaining grant.
2. **An undeclared decision point** (collector: one question in each stint
   review — "did anything this stint turn out to have been a decision nobody
   surfaced?" — plus journaling any such find where it happened). One
   confirmed find → declaration is insufficient on the grown corpus; the §3
   definition under-counts; the *only* legitimate next step is §4a's
   flag-only instrument, pre-priced precisely so this firing doesn't panic
   anyone into a classifier that answers.
3. **A #62 recurrence swallowed** (collector: the premise sweep, §4b.3 — every
   human-initiated correction triggers a sweep of recent proxied answers; a
   sweep that finds one → the scope bounds were drawn wrong; redraw them and
   journal the miss). Honest status (red K1): on the record as it stands,
   premise shifts can be invisible until the human speaks — which is why this
   falsifier's collector is anchored to the human's own initiations, the one
   place the record shows such shifts surfacing.
4. **Goodhart fires** (collector: pilot-regime exhaustive review, plus one
   *deep-verify* per stint — re-run one sampled proxied answer's own
   verification, because the cheap "would I have merged this?" check cannot
   see a false GREEN). Post-adoption checks start finding false GREENs or
   defects that pre-adoption seat verification would have caught (§1e
   materializing) → the reading was load-bearing; verdict delegation decays
   the pipeline that made the stamp rate high; revoke and record why.
5. **The price exceeds the product** (collector: the audit line's own
   ledger, against a stated baseline: hop-2 pass-through volume and desk size
   at pilot start). If after the promotion ritual has run for weeks the
   human's gate load is undiminished *and* the audit ritual is consuming
   stints, nothing was compressible ex ante — the mechanical share was an
   artifact of hindsight; kill the design and record that the brief's premise
   did not survive contact.
6. **Citation rot** (collector: the same sampled review, reading cited line
   against case — the F5 claim-line audit shape). Verdict entries citing
   lines that do not actually cover the case → binary citability was a score
   in disguise; the SPAN self-test pattern failed its transplant; stop.
7. **Grant provenance rot** (collector: any hand, any time — grants are
   world-readable text; added for red W9). A cited grant with no quoted human
   utterance, or whose scope text drifted across journal rewrites away from
   the quoted words → the ledger is laundering seat-authored power; freeze
   all proxying until the human re-ratifies every line.

---

## 7. SUMMARY FOR THE SEAT

The record answers the brief more sharply than expected, and twice not in the
way the first draft of this document claimed. The confidence signal a decision
engine would learn **already exists as participant-authored declarations** —
loop topology and dispatch-time class above all, which never touch message
surface — so there is nothing for a model to learn *yet*, on an n of 25 that
settles nothing forever. The one decision that ever needed catching (#62) was
invisible not just to models but to the record itself until the human spoke —
so no clause, learned or written, catches its class; what preserved it was
narrow authority buying delay plus live human attention using it, and the
design's job is to preserve both, structurally. Meanwhile the engine the brief
imagines **already runs as informal pre-auth**, its contract-class attention
collapsed 16h → 14s in a day, unrecorded.

So: don't build a classifier — and don't let the engine that already exists
keep running off the books. Write the grants down in the human's own quoted
words — scoped, reversibility-bounded, expiring, citable, provenance-checked.
Let the seat answer only what a written line covers, in its own name, on the
record. Audit exhaustively while small, by sample once grown; sweep proxied
answers whenever the human corrects a premise; and let everything ungranted
pass through whole, because pass-through is where the human's live attention —
the only #62 detector in existence — actually operates. Its yield is not saved
time; it is that the delegation already happening becomes legible, bounded,
and revocable.

**What is genuinely different this time: the buried heuristic guessed what
nobody had said; this engine repeats only what the operator has said, quotes
them saying it, and shows its work.**
