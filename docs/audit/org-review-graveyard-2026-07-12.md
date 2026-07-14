# THE GRAVEYARD CHECK — the top-level-structure-review instrument

> SUPERSEDED by the final ORG-REVIEW.md design and its RED review; kept for the record (the specific kill/clear verdicts — overseer kill, nag kill, offer kill — synthesized from the phil8/priorart docs).

**Prosecutor:** `grave-org`, child of `org-review-scout`. **Date:** 2026-07-12. **Base:** `main@aa6063d`.
**Subject:** an INSTRUMENT that reviews the swarm's TOP-LEVEL structure and SUGGESTS improvements to
the human — advisory only, invoked as a named skill/command, plus a rare evidence-warranted OFFER
from the coordinator (*"your top layer looks worth reviewing"*).

**Method.** Three independent evidence hunts, delegated and then verified by me at source
(`grave-priorart` → living prior art; `grave-kills` → the three alleged kills; `grave-phil8` → the §8
empirical test). I re-read every decisive line myself. Where a child's finding contradicted my own
leading theory, the child won and I say so.

**Evidence discipline.** **VERIFIED** = I read the line and quote it. **MEASURED** = a count someone
ran. **REASONED** = argument, with its falsifier named.

**Standard of proof.** I was asked for the prosecution case. I have brought it. Where the charge in my
own brief was **false**, I report that too — a prosecutor who indicts on a phantom corpse loses the
real case. One of the three alleged kills does not exist.

---

# THE VERDICTS

| # | The thing | Verdict |
|---|---|---|
| 1 | **The whole idea** (any instrument reviewing the top layer, in any form) | **MUST-SATISFY — and today it does not.** Not a corpse. But §8's precondition is **unmet**: the convention it would tool **has never once been performed by the human**. |
| 2 | **Separate skill** (explicitly invoked, named command) | **MUST-SATISFY.** The *lawful form*, and the only survivor. Cleared of the overseer kill (invoked ≠ standing). Blocked by §8 until the convention exists. |
| 3 | **Coordinator duty** (a briefed sentence, no new surface) | **CLEARED — and it is the recommended form.** This is what §8's ladder mandates and what the record's own closest precedent (`PROXY-WIRING`) already ruled. |
| 4 | **Report artifact** (a written structure review the human reads) | **CLEARED-CONDITIONAL.** Legal *if and only if* a human reader actually reads it — the exact condition on which the last dashboard died. |
| 5 | **Periodic prompt** (recurring reminder / cadence) | **KILLED-BEFORE. Dead three times. Do not resurrect.** The nag. |
| 6 | **Offer-mechanism** (unsolicited "your top layer looks worth reviewing") | **KILLED-BEFORE — killed TODAY, twice, on MEASURED grounds.** The strongest kill in the file. |

**The one-sentence verdict:** *the instrument is not a corpse, but it is a tool for a convention that
does not yet exist — and its two moving parts (the offer, the cadence) are corpses. What survives is a
sentence of doctrine, not an instrument.*

---

# THE SINGLE STRONGEST ARGUMENT AGAINST BUILDING THIS AT ALL

> **The human has never once reviewed their top-level structure by hand, has never once said it hurt,
> and — TODAY, one workstream over — ruled that the shape must be *emergent, never prescribed*.
> §8 forbids tooling a convention that does not exist. Building this would be guessing at a workflow
> and calling it an instrument.**

The corollary is the load-bearing text, and it must be read **exactly** (`docs/PHILOSOPHY.md:262-266`,
VERIFIED):

> *"**prompt-level convention first, a visibility verb second, an engine never** — unless the record
> shows the convention **failing**."*
>
> *"**The test this gives you:** if you cannot point to the convention working in practice, you are not
> building tooling, you are guessing at a workflow."*

Two conditions gate the escape hatch, and **both** are required: (1) a convention **exists**; (2) the
record shows it **failing**. The record here shows **neither**. **Silence is not failure — silence is
the absence of the convention**, which is condition (1) unmet. The hatch does not open.

---

# COUNT 1 — THE KILLED 'AUDIT' AGENT: **THERE ISN'T ONE. THE CHARGE IS FALSE.**

My brief asserted an 'audit' agent was killed. **I could not find it, because it does not exist.**
`grave-kills`/`kill-audit` and I searched the corpus, all 117 journals, and git history
(`log -S'audit'`, `--diff-filter=D`). **NULL RESULT.**

The only audit-named agent ever to exist, `codex-audit`, was **closed on harvest — a normal, successful
completion.** And the operator's own note on closing it is the **opposite of a kill**
(`.swarm/journal/operator.md:86`, VERIFIED):

> *"closed codex-audit on harvest (**re-audits are fresh spawns by design — audit independence**)"*

Read what that actually says. It is a **shipped doctrine endorsing invoked, one-shot, freshly-spawned
audits** — and giving the *reason*: independence from the author-adjacent context. The dispatch that
created it says the same (`operator.md:71`, VERIFIED): *"Fresh name… audit is a different shape… and
**independence from the design's author-adjacent context is a mild plus**."*

**This is the instrument's strongest affirmative precedent, and my brief had it exactly backwards.**

### Arguing both sides, as instructed

**FOR the prosecution (the org-reviewer IS the corpse):** the *real* corpse is not called "audit," it
is called **the overseer**, and the org-reviewer sits at its definitional center. See Count 2 — that
argument is real and I make it in full there.

**FOR the defense (genuinely different):** `codex-audit` is a **live, blessed, repeated precedent** for
precisely the proposed shape: a read-only, one-shot, explicitly-dispatched agent that reads evidence,
writes a ranked artifact, reports, and **dies**. It held no standing pane. It watched nobody. It was
spawned *because a human asked a question* and closed when it answered. **If the org-review instrument
is built in that shape, it is not a new thing — it is `codex-audit` pointed at a different subject,
and the operator has already run that play and written down why it works.**

**VERDICT on Count 1: NO SUCH KILL. Charge dismissed — and it converts into precedent FOR the invoked
form.**

---

# COUNT 2 — THE OVERSEER: **ONE CORPSE, STATED FOUR TIMES, WITH A TRIPWIRE ON IT**

This is the kill my brief was reaching for. It is real, it is repeated, and it is the deadliest thing
in the record for **the standing form** of this instrument.

1. **`.swarm/journal/operator.md:23`** (VERIFIED) — the operator's own dispatch, the one that shipped
   the delegation doctrine: **"Rejected: overseer agent (nag reborn)."**
2. **`docs/design/SPAN.md:231-234`** (VERIFIED):
   > *"**A load-balancer/overseer node**: the nag reborn, structurally — **a node whose job is other
   > nodes' behavior**. Rejected in the delegation design for the same reason (VERIFIED: operator
   > journal 2026-07-11); **parents judging tree shape *is* the distributed overseer**."*
3. **`docs/design/archive/HARNESS.md:511-514`** (VERIFIED) — this is the "killed twice," and it is
   explicit about the count *and* names the rhyme:
   > *"**The nag / overseer** (**rejected twice**: delegation design, SPAN §4) — rhymes: **a health
   > monitor watching for dead children instead of parents judging them**."*
4. **`docs/design/ONBOARDING.md:248`** (VERIFIED, this week): *"**NOT an overseer/load-balancer node.**
   SPAN §4 killed it as *'the nag reborn'*."*

### Why this is *worse* for the org-reviewer than for anything previously cleared

`graveyard-check` (the prior graveyard agent, `.swarm/journal/graveyard-check.md:43`) **narrowed** this
kill to save the coordinator-in-place: a coordinator's job is **the goal** — it briefs, judges
artifacts, synthesizes — so it is not *"a node whose job is other nodes' behavior."* That narrowing was
right, and **it rescues the coordinator by convicting this instrument.**

**An org-review instrument judges no artifact, advances no goal, and produces no work. Its entire job
is the shape of other nodes.** It is not at the periphery of the killed class — **it is the
definitional center of it.** And HARNESS.md's stated rhyme is the instrument with two nouns swapped:
*"a health monitor watching for dead children **instead of parents judging them**"* → *a shape monitor
watching the top layer instead of the operator judging it*.

The same sentence that kills it names **what already occupies its function**: *"parents judging tree
shape **is** the distributed overseer."* The design did not leave this job unfilled. It deliberately
**distributed** it into every parent's briefed duty and then **refused the centralized node**. The
instrument is not filling a hole — **it is re-centralizing a function the design consciously spread
out.** And per PHILOSOPHY §3 (`:106-109`, VERIFIED), the standing version of that role was *already
formally denied*:

> *"**Universal, not privileged.** Every agent reconciles, at every depth. **There is no reconciler
> role.** (ASK #35 later offered "a dedicated standing reconciler agent" as an option; the
> recommendation was "Every parent, recursively," and the whole question was **denied**.)"*

*"Does my tree still match my work — do I need more agents or fewer?"* **is the reconciliation question,
verbatim.** An instrument that answers it *for* the operator is a reconciler role for the top layer.

### THE LIVE TRIPWIRE

This repo does not merely remember this kill — **it patrols it.** `docs/design/SELF-AUDIT.md:34`
(VERIFIED) maintains a standing grep-based corpse-check table, and one row is literally:

| Deleted | Grep | Hits |
|---|---|---|
| the nag | `grep -ci 'nag' swarm` | 0 |

And `docs/design/WATCHLIST.md:28` (VERIFIED) carries the standing order: *"**do NOT reintroduce the
nag**; the nag was tried and its absence read as compliance."*

### THE DISTINCTION THAT DECIDES IT — and it is the one the four kills never had to draw

**Every corpse above is STANDING.** A *node*. An *agent*. A *monitor*. A *warm pane* whose job is to
watch. **None of the four kills addresses a thing that is invoked, runs once, and dies** — because
nobody had proposed one. The kills are all of *standing surveillance*, and their stated reason is
always the same: a thing whose job is watching, that runs whether or not anyone asked, and whose output
nobody consumes.

**An explicitly-invoked skill is not that.** It has no pane, no cadence, no standing existence; it runs
because a human asked a question, and it dies when it answers. That is `codex-audit` (Count 1), and the
operator blessed it.

**And the record already ruled on exactly this distinction, in the closest analogue it has.**
`docs/design/PROXY-WIRING.md:296-321` (VERIFIED) — a read-only reviewer of world-readable evidence,
asked precisely "should this be a standing agent?":

> *(Rewritten after red-proxy W6: **the first draft opened with "one new standing agent," asserted
> rather than argued.** … And **PHIL §8's standing bias** — "prompt-level convention first, a
> visibility verb second, an engine never — unless the record shows the convention failing" — **cuts
> against a warm pane no convention has yet earned**.)*
>
> *"The observer is a **duty, not (yet) an agent**: a per-stint batch read… **zero standing pane, zero
> standing tokens**… A standing `plane-observer` agent … is the **post-pilot option the numbers must
> earn**."*

**That is the template, and it was written after a red-teamer caught the exact error being made here.**
The repo has already published the correction to this proposal.

**VERDICT on Count 2: the STANDING form is KILLED-BEFORE (it would die as "the nag reborn," a node
whose job is other nodes). The INVOKED form is CLEARED of this kill — but it is thereby pushed onto
§8's ladder, where it fails at rung 1 (Count 5).**

---

# COUNT 3 — THE NAG, KILLED TWICE (AND A THIRD TIME TODAY)

**Kill 1 — the recipient-side reminder.** `docs/design/SIMPLEST.md:177` (VERIFIED):

> *"The reminder was tried and **its own builder priced it**: it **carries strictly less information
> than the ignored body**, is **cleared by a command that proves nothing**, and **its absence reads as
> compliance**. The party incentivized to check — the sender — now has eyes… **Losing the
> recipient-side reminder is losing a guardrail the philosophy condemns anyway**."*

**Kill 2 — the wire-side ping cadence.** `docs/design/INBOX.md:172-173` (VERIFIED):

> *"**A configurable ping cadence is the nag reborn with a settings page** — the nag died because it
> **carried strictly less information than the mail it nagged about**."*

**Kill 3 — THE ONE THE PROPOSAL ACTUALLY RESEMBLES: the nag aimed at the HUMAN.**
`docs/design/DECISIONS.md:494-495` (VERIFIED):

> *"7. **No latency SLO on pass-throughs.** The one aged decision aged because it deserved to;
> **making "open" uncomfortable rebuilds the nag**."*

`kill-nag` (grandchild, via `grave-kills`) found this independently and is right that it is the
sharpest of the three: **kills 1 and 2 are nags aimed at *agents*. This one is a nag aimed at the
human — and it is the only one that indicts the OFFER directly.** Parse the corpse precisely: it is
not "a reminder to an agent," it is **anything that makes the human's non-response uncomfortable.**
An unsolicited *"your top layer looks worth reviewing"* that the human keeps declining is exactly a
mechanism that makes not-acting uncomfortable.

### THE NECESSARY CONDITIONS — derived strictly from the stated kill reasons

*(I derived N1–N5 from the primary kills myself; `kill-nag` derived a nine-condition list
independently from the same quotes and its conditions 1/2/3 match N1/N2/N3 predicate-for-predicate.
Two separate derivations from the same kill text converged — that is the corroboration worth
having, and it is why I state these as hard conditions rather than suggestions.)*

Both primary kills turn on **the same predicate**, stated in nearly the same words. Every condition
below traces to a quoted kill reason; none is invented from first principles.

**N1 — INFORMATION-POSITIVE.** *"carries strictly less information than the ignored body"* (SIMPLEST:177);
*"strictly less information than the mail it nagged about"* (INBOX:173).
**⇒ The prompt must BE the finding, not a pointer to one.** *"Your top layer looks worth reviewing"* is
a pointer — **it is strictly less information than the evidence that triggered it, and it dies on this
condition alone.** The only surviving form: the message **names the file fact** ("`ledger-forensics` and
`shape-forensics` have both been idle 3h with q=0 and no report — 2 of your 6 direct children"). Reading
the message must *be* reading the evidence. **If the human must go look to find out what you meant, you
built the nag.**

**The operational test** (`kill-nag`'s sharpening, and it is the right one): *if the content is
derivable by the human running `swarm ps` and looking, it is the nag.* The instrument must state **a
fact the human cannot see by looking** — a recurrence, a decay, a cross-journal pattern — **never
"you have a tree, consider reviewing it."** This is a high bar and the proposed offer does not clear
it.

**N2 — NO CLEARING RITUAL.** *"is cleared by a command that proves nothing"* (SIMPLEST:177).
**⇒ No ack, no dismiss, no snooze, no "reviewed" state.** Nothing may record that the human saw it.

**N3 — ABSENCE MUST NOT READ AS COMPLIANCE.** *"its absence reads as compliance"* (SIMPLEST:177);
WATCHLIST:28 restates it as standing order.
**⇒ Silence from the instrument must not be evidence the top layer is healthy.** An instrument that
stays quiet when the tree is fine teaches the human that quiet = fine — and then its own failure
(never firing, misreading, being wrong) is **indistinguishable from good news**. This is the condition
the offer-mechanism can least satisfy.

**N4 — NO CADENCE, EVER.** *"A configurable ping cadence is the nag reborn **with a settings page**"*
(INBOX:172); PHILOSOPHY §5 (`:174-176`): *"a field you set is machinery"*.
**⇒ A periodic prompt is dead on arrival, and a *configurable* one is dead twice.**

**N5 — DO NOT MAKE THE OPEN LOOP UNCOMFORTABLE.** *"making 'open' uncomfortable rebuilds the nag"*
(DECISIONS:495).
**⇒ The instrument may not escalate, repeat, or apply any pressure for not being acted on.** Said once,
or not at all.

**VERDICT on Count 3: the PERIODIC PROMPT is KILLED-BEFORE (N4 — dead three times, no defense
available). Any resurrected prompt-or-offer MUST-SATISFY N1–N5. The proposed offer as worded
("*your top layer looks worth reviewing*") **fails N1 and N3** and must be either rewritten as the
finding itself or dropped.**

---

# COUNT 4 — THE METRICS ENGINE: KILLED, AND THE KILL CITES §8 *INSIDE THE KILL*

`docs/design/SIMPLEST.md:178` (VERIFIED), the deletion table, in full:

| Deleted | What is lost, concretely | Why acceptable |
|---|---|---|
| The checkpoint schema (tasks[], status enums, delegated_to[], blockers, seq, open_threads, work_cache) | Machine-readable status; **any future dashboard over task states**. | **No code ever read the machine-readable parts (VERIFIED).** The fields that were read by humans (mission, progress) survive as journal prose. **A dashboard can be built over journals *when something reads it* — conventions earn tooling (§8).** |

Read the kill **precisely**, because it is the most misread line in the corpus. The dashboard was **not
forbidden**. It was **deferred until a reader exists.** The thing that died was **a schema nothing
consumed** — machinery emitting structure into the void.

### Does an evidence-reading structure reviewer = the metrics engine reborn?

**FOR (it is the corpse):** the moment the reviewer emits **scores, health grades, span numbers, or a
structural dashboard**, it is the checkpoint schema with a nicer name — *machine-readable status about
the tree, produced on a cadence, consumed by nobody*. And PHILOSOPHY §10 (`:325-326`, VERIFIED) —
*"**if you cannot prove the number is yours, do not print a number**"* — bites hard: a "span health
score" for a human's org is a number the instrument cannot prove. Note also that the operator's own
brief to `structure-scout` pre-emptively forbade this (`operator.md:45`, VERIFIED): *"Off-track if: it
ships theory without mining the record, or **proposes counters/metrics engines**."*

**AGAINST (it is categorically different):** the checkpoint schema died of **"no code ever read the
machine-readable parts."** A one-shot, human-invoked reviewer is **the reader arriving.** It emits **prose
citing file facts**, to a **human who asked for it**, and then **ceases to exist**. It stores no state,
maintains no schema, and runs no cadence. On the kill's own stated terms — *"a dashboard can be built
over journals **when something reads it**"* — **a human who typed the command IS the something that
reads it.**

**MY JUDGMENT:** the *reviewer* is not the corpse; the *dashboard* is. The kill is **conditional and the
condition is satisfiable**. But the condition is load-bearing and narrow, so it becomes a hard bound.

**And `kill-metrics` (grandchild, via `grave-kills`) found the mechanism that makes the bound precise
— it cuts the proposal exactly in half, and its test is better than mine.** The checkpoint schema died
not merely because nothing read it, but because its fields (`SIMPLEST.md:139-140`) *"were all
**SELF-CLAIMS with ZERO PARENT VERDICTS**."* Apply that to the two possible outputs:

- **A prose finding citing file facts** — *re-derived from scratch at each invocation, and it **is** a
  reconcile.* Nothing durable survives it to be contradicted. **PASSES.**
- **A structural score / health grade / span number** — *a **durable self-description** that outlives
  the reconcile that should overturn it* ("my tree scored well"). That is verbatim SPAN's **"cargo
  budgeting"** (`SPAN.md:222-224`) and verbatim the checkpoint's cause of death. **FAILS.**

**The line is exact: the instrument may say what it read. It may never say how the tree scored.**

**VERDICT on Count 4: CLEARED-CONDITIONAL — MUST-SATISFY: (i) output is PROSE CITING FILE FACTS, never
scores/grades/counters/dashboards (§10 + the operator's own standing "no metrics engines" instruction);
(ii) it STORES NOTHING — no state file, no schema, no history dir (the checkpoint corpse); (iii) it
runs ONLY when a human asks, so that "something reads it" is true BY CONSTRUCTION and not by hope.**

---

# COUNT 5 — SELF-AUDIT / REVIEW / WATCHLIST, AND THE §8 VERDICT

## (a) The three files are NOT prior art. Their names mislead.

`grave-priorart` read all three top to bottom and grepped every shipped surface (`bin/swarm`,
`skill/SKILL.md`, `WORLD.md`, `README.md`, `install.sh`, `.claude/`).

- **`SELF-AUDIT.md`** — its own first line (`:1`): *"# SELF-AUDIT — **simplest/swarm vs the SIMPLEST
  spec**"*. It is a **one-shot conformance audit of `bin/swarm` against its own design doc**, written
  once on 2026-07-09. It is about **the tool's code**, not the operator's org. A dead letter.
- **`REVIEW.md`** — an adversarial review of that same rewrite. Dead letter.
- **`WATCHLIST.md`** — **alive**, but as a **design ledger of tripwires for the tool**, cited only by
  other design docs.

**No shipped surface references any of them.** (MEASURED.)

## (b) THE KILLER QUESTION — is the operator ALREADY getting this?

**NO. NULL RESULT — and this is the honest answer, not the convenient one.** The operator has **never,
once, received a top-layer structure review from any shipped mechanism.** The closest shipped thing —
**the review desk** (`skill/SKILL.md:47-49`) — is a **ranked *decisions* page**: it hands the human
*what to decide*, never *how their top layer is shaped*. **The instrument does not exist today and never
has. Nobody has ever proposed one, and nothing has ever killed one.**

*(This is the finding that could have killed my own deliverable. It did not. I report it as it fell.)*

## (c) ★ THE §8 VERDICT — **NO. DO NOT BUILD THE INSTRUMENT.**

§8's test is **empirical**: *"if you cannot point to the convention working in practice…"* So: **has the
human ever done this by hand?**

**COUNT: ZERO.** And the methodological fact that establishes it — which corrected my own first reading
and is the single most important discovery in this audit:

> **`.swarm/journal/operator.md` is NOT the human's ledger. It is an AGENT's ledger.**

Every entry from 2026-07-11 on is tagged **`[ops-main]`** — a **hand on the operator seat**, a Claude
session (`skill/SKILL.md:51-59`, the seat doctrine; `bin/swarm:1037`: *"operator is a mailbox, not a
node: no pane, no doorbell"*). **The human writes nothing into `.swarm/`.** They appear **only as
reported speech**: *"User approved…"*, *"Operator parked…"*, *"User corrected my framing…"*

So every entry that *looks* like the human reviewing their tree — *"Tree: 4 arms"*, *"tree pruned per
doctrine"*, *"Closed red-operator, red-simplest, structure-scout"* — is **an agent executing the
already-shipped reconcile duty.** `grave-phil8` read **all 45** `*-operator.json` delivered messages:
**all 45 are the seat dispatching to children. Not one is the human.** (MEASURED.)

**That inverts the meaning of the evidence.** Those entries are not a human convention awaiting tooling
— **they are proof the convention already works WITHOUT an instrument**, performed by the briefed
reconcile duty that PHILOSOPHY §3 made universal.

**And the pain?** A grep of the entire ledger and every brief for *too many agents | lost track | hard
to see | hard to manage | overwhelm | confus | don't know what | messy tree | out of control* returns
**ZERO hits** (MEASURED). **The pain this instrument would relieve has never been expressed by the
person it would relieve. It is 100% hypothesized by agents on the human's behalf.**

**Therefore, by §8's own test, stated plainly, as my brief demanded:**

> **There is NO convention of top-level structure review working in practice in this repo. The human
> has never performed it, and has never named its absence as pain. §8 says: DO NOT BUILD THE
> INSTRUMENT. Do it by hand a few times first, and let the record show it working — or failing.**

## (d) THE KEYSTONE — the operator pre-killed the instrument's OUTPUT CLASS today

`.swarm/journal/operator.md:194` (VERIFIED), dated **TODAY**, from the operator's own reframe in the
*immediately adjacent* workstream (`operator-structure-scout`):

> *"**NO prescribed org shapes** — teach the stance + selection rule ("what you'd confirm yourself goes
> under you"), **structure EMERGES unsteered; prescribed = anticipatory = SPAN violation**."*

And `operator.md:184` (VERIFIED): *"**primary act before any task = design top layer**"* — written in the
**imperative future**. The human is *adopting* this practice. They have **not yet performed it**.

**An org-review instrument's entire deliverable is a prescribed org shape, produced by something other
than the person whose stance it is.** The operator ruled that class of output out **today**, one
workstream over, without knowing they were doing it. That is not a graveyard rhyme — **it is a live
standing ruling, and it is the most current thing in the record.**

## (e) §9 AND THE OFFER — **KILLED TODAY, TWICE, ON MEASURED GROUNDS**

The offer is *"a message into `queue/operator/` that asks the human to engage."* Both of today's docs
killed exactly that shape.

**The MEASURED datum** (`docs/design/DECISIONS.md:120-127`, VERIFIED, quoted in `OPERATOR-STRUCTURE-GRAVE.md:258-279`):

> *"**The gate collapsed into standing authorization within a day:** #65–#68 waited **16–17h**…; #74 was
> merged under pre-auth in **14 seconds**; #76/#78 in **3–4s** (MEASURED). **The tier labels stayed; the
> attention behind them thinned.**"*

**The structural fact** (`DECISIONS.md:130-134`, VERIFIED) — **the deadliest sentence in the corpus for
the offer:**

> *"**Genuine human judgment, wherever the record shows it, is an initiation or a correction, never a
> gate answer**: rejected the overseer agent, "recon should shrink", R1/R2, the choice-doctrine process
> correction, "decision POINTS, not questions"."*

**An offer asks the human to answer a gate. This human, measured across the whole record, never answers
gates — he initiates and he corrects.** The offer will be answered "sure" in three seconds without
being read, and the instrument will have purchased a ritual. That is not speculation: **it is what this
repo measured happening to its last gate, within a day.**

**And §9's own test** (`PHILOSOPHY.md:300-302`, VERIFIED): *"anything reaching the operator must be
readable by someone who has not been in the room."* An offer that says *"your top layer looks worth
reviewing"* — without the finding in it — **is not readable by someone who has not been in the room. It
fails §9's test on its face**, and independently fails N1.

**The shipped alternative the repo already uses** (`ONBOARDING.md:180-183`, VERIFIED): **announce, don't
ask** — *"the session says so plainly once rather than nagging."*

**VERDICT on the offer-mechanism: KILLED-BEFORE. Drop it, or convert it into an announcement that IS
the finding (satisfying N1/N3/§9) and is said exactly once, with no gate, no ack, and no repeat.**

---

# WHAT SURVIVES

The instrument, as proposed, does not survive. **One sentence of doctrine does**, and it is what §8's
ladder mandates and what the record's closest precedent already ruled (`PROXY-WIRING.md:308`): *"a
**duty, not (yet) an agent**."*

**The recommended form — rung 1 of §8's ladder, the only rung the evidence has earned:**

> **A briefed sentence** in the operator-seat doctrine: *when you reconcile, judge your own top layer
> the way you judge a child's — is each direct arm one you can name the next artifact for?* Zero new
> surface, zero new concept, zero standing cost. It is what the seat **already does** (`operator.md:53`,
> *"tree pruned per doctrine"*) — **written down, so it is a convention that can be observed working,
> or observed failing.**

**And then §8's ladder tells you exactly what to do next, and it is the honest path:**

1. **Ship the sentence.** Let the human (or the seat) do this by hand.
2. **Watch the record.** If the convention *works*, the instrument is unnecessary. If it **fails** —
   and the record *shows* it failing — **then and only then** does the corollary's escape hatch open,
   and the invoked skill (Count 1's `codex-audit` shape: one-shot, read-only, prose, dies on report)
   becomes **earned**, not guessed.
3. **The offer never returns.** N1–N5 and the MEASURED gate-decay foreclose it in every form except
   *announce-once-with-the-finding-in-it*.

**The falsifier for this entire audit:** if the human states, in their own words, that they cannot see
or manage their top layer and that this is costing them — **that is the convention's failure entering
the record**, §8's hatch opens, and the invoked skill is earned the same day. **Nothing in the record
says that today.** It is one sentence from the human away from being true, and **that sentence is the
only thing that should unlock this build.**

---

## Provenance

- `docs/audit/org-review-phil8-2026-07-12.md` — `grave-phil8` (the §8 empirical test; the `[ops-main]`
  discovery; the zero-count). The finding that inverted this audit.
- `docs/audit/org-review-priorart-2026-07-12.md` — `grave-priorart` (the living prior art; the NULL
  result; the OPERATOR-STRUCTURE-GRAVE kills).
- `grave-kills` (+ `kill-audit`, `kill-nag`, `kill-metrics`) — the three kills; its detail confirms the
  quotes I verified independently at source above.
- Harvested from prior graveyard work: `.swarm/journal/graveyard-check.md`, `grave-span.md`,
  `grave-history.md`, `structure-grave.md`.
