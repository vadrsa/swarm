# LOOP-RED3 — adversarial review of LOOP.md §4b, the third fork trigger, and the Build 1 quiescence rule

**Reviewer:** `hc-red3`, fresh eyes, no access to the author's reasoning process, no
access to `hc-red2`'s prior review while forming my own reads (checked against
`LOOP-RED.md` only afterward, to avoid duplicate filing — noted where our findings
overlap and where mine goes further).

**Scope, exactly as briefed:** LOOP.md §4b (the Build 2-FAIL branch), the third fork
trigger named in §5, and §1's Build 1 Claude-backend quiescence rule. Cross-read:
`_hc-ocloop.md` §1 (per-duty hook semantics), `OPENCODE-PLUGIN.md` §2 (what hooks
actually receive), `FLEET-EVAL-V3.md` §3b-§4 (F-A/F-B/F-C's source data),
`fleet-rubric-v1.md` (what the "three checks" in §4b.3 actually are), `bin/swarm`
(what the quiescence rule's code today actually does).

**Operator's charge:** is the mechanism list real, or is it hope with a fork attached?

---

## VERDICT SUMMARY

| Surface | Verdict | Strongest surviving attack |
|---|---|---|
| M1 "operating frame" mechanism | **WOUNDED** | The children-liveness table is real and cheap to compute (closed-enum data, per-turn-fresh by construction of `system.transform` firing every model call). But the doc's own words for M1 — "the standing rule... blocked >N min... → journal BLOCKED and return to the brief" — is exactly a prompt-hope for the F-A half; only the *data* (clock, liveness) is a new-in-kind mechanism, the *instruction* is not. LOOP.md conflates the two under one mechanism number. |
| Inputs-vs-inference decomposition | **WOUNDED** | Not unfalsifiable in principle — §4b.4 commits numbers before data exists, which is the right discipline — but the one piece of supporting evidence offered (GLM's 6/6 verification-with-data) is doing more work than it can bear: it is harvest-time file-checking, not the liveness-*monitoring-while-blocked* capability F-B actually needs, and the doc's own hedge word ("plausibly") admits this without following through on how much weaker that makes the F-B prior. |
| Stopping-rule numbers (§4b.3) | **WOUNDED** | The three checks are named in §4b.3's "Pass, defined per-arm" line but do not exist as scoreable rows in `fleet-rubric-v1.md` today — two of the three ("deliberately-exercised dead-child row," a distinct "time-box row") require **new rubric rows that are not yet written**, and the third (D2-heavy verification) is real but currently a single 6/6 aggregate, not a bit that "flips." "3 battery runs + 1 week" is a real, checkable cap in isolation, but "a model property for this model generation" is an open-ended re-entry clause with no stated trigger for when a "new generation" has arrived — it reopens on the author's say-so, not on a measurement. |
| The prior (§4b.4) | **HOLDS, barely** | The probabilities are pre-registered before data, which is the discipline the doc claims and the one thing that makes them scoreable at all — this is real, not decoration. But "operator wins but via stock" is close to unfalsifiable as *the operator's* win: the operator bet on the fork; a stock-only win scores as the author right twice (see §4b.4's own last line) and the operator's chosen instrument wrong, which means almost every non-STOP outcome reads as "I was right," a structurally favorable framing for the reviewer's own prior. |
| M4/M5 honesty / fork steelman | **REFUTED as complete** | The mechanism list is demonstrably incomplete. `experimental.chat.messages.transform` — read in full in `OPENCODE-PLUGIN.md` §2.2, cited elsewhere in this same document (§3's duty table) — is a stock, no-fork hook that can **rewrite the entire conversation the model sees, per model call**, i.e. real context-window curation: pruning an 11-minute harness-debugging detour out of view before the next call, or replacing it with "you were debugging the harness; stop; return to the brief." LOOP.md never proposes this for F-A. It is strictly stronger than M1 (which only *appends* a rule) and requires no fork — a missed **stock** mechanism, not just a missed fork one, which the operator's framing didn't anticipate but the finding is worse for the doc precisely because of that. |
| Quiescence rule (§1, Claude backend) | **REFUTED as currently specified** | Two independent problems, one of them fatal today: (a) the rule as designed **is not implemented** — `bin/swarm`'s actual `cmd_event` (bin/swarm:878-908) only records the event and re-rings on a non-empty queue; there is no cooldown file, no digest send, no quiescence check anywhere in the codebase. §1 describes a mechanism that does not exist yet, stated in the present/future tense as though it were a design decision away from being true, not flagging "unbuilt" the way Build 0 is flagged. (b) even as *designed*, the rule misfires on at least three common shapes named concretely below: multi-turn-work digest-spam, children-waiting digest-spam, and restart-cooldown-loss causing an immediate re-digest storm. |

---

## 1. M1 — "the per-turn operating frame": real data, prompt-hope instruction

### What the hook actually receives (checked against source)

`_hc-ocloop.md` §0 and §1 are unambiguous: `experimental.chat.system.transform`
fires **every model call** within a turn (not once per turn — `OPENCODE-PLUGIN.md`
§3.1.2's own measurement shows `messages.transform`-class hooks firing 5 times
against 1 `session.idle` in a single 4-bash-call turn; `system.transform` is the
same per-call dispatch shape). So "per-turn-fresh" understates it — the frame is
**per-model-call-fresh**, strictly fresher than the doc claims it needs to be.

Can the plugin cheaply compute a children-liveness table from inside the hook?
Yes, on the evidence already in this repo's own artifacts: `.swarm/` is a plain
file tree (`agents/*.json`, `queue/*`, `journal/*`) and herdr's `agent_status` is
the same closed-enum data HARNESS.md §2.3 already ships to Claude-side agents via
`swarm ps`. A `system.transform` hook runs in the same process as the plugin that
already reads these files for the pump (`OPENCODE-PLUGIN.md` §3.1) — there is no
new I/O surface being invented, just a read of files already read elsewhere in
this design. **Staleness/race:** the hook fires synchronously before the model
call is issued (it is a request-assembly-time hook, not an async one — see
`_hc-ocloop.md` §2.3's characterization of `llm.ts` as the assembly site that
`system.transform`'s output feeds into), so the table is as fresh as the
filesystem at call time — no worse than `swarm ps`'s own staleness today, and
better than any Stop-hook-cadence digest, which only updates once per Claude turn.
**This half of M1 is real and does not need to be taken on faith.**

### Where M1 quietly becomes M1-instruction, not M1-data

§4b.2 bundles two different things under one mechanism number:

1. A **data supply**: clock, liveness table — this is what a loop can do that a
   briefing cannot, because the loop computes it and injects it as fact, not as
   an ask.
2. A **standing rule**: *"blocked >N min on infrastructure → journal BLOCKED and
   return to the brief."*

Item 2 is not different in kind from the duty preamble that already failed the
V3 battery. It is text in the system prompt asking the model to behave a certain
way when a condition holds — exactly the shape of "duties compliance" (D1) that
`fleet-rubric-v1.md` §1 exists to measure, and which the doc's own §3 concedes is
**PROMPTED, not absorbed**, for reconciliation. LOOP.md's own duty table (§3) is
explicit that a standing instruction in the system prompt is the PROMPTED
category — "the model can ignore it; nothing in the API structurally prevents the
turn from ending without compliance" (quoting `_hc-ocloop.md` §1 duty 3, which
LOOP.md itself relies on elsewhere). M1's instruction half is that same category,
applied to F-A instead of reconciliation, without saying so.

**What would make M1 different in kind, and isn't proposed:** if the *data* (a
computed "you have burned N minutes on non-brief tool calls" counter, itself
loop-computed, not self-reported) were paired with a **structural** consequence —
M2's perseveration guard (`tool.execute.before` refusing the N+1th near-identical
command) is exactly this, and is listed separately. M1 alone, stripped of M2, is:
better information plus a nicer-worded nag. The nag is not new leverage; only the
information is. The doc should score these as two different confidence levels,
not one bullet with one confidence.

**Verdict: WOUNDED.** The data half of M1 is a genuine, cheap, fresh, real
mechanism — this is not hope. The instruction half is a renamed prompt-hope,
and the doc's own §3 duty table already contains the concept needed to say so
but does not apply it to M1.

---

## 2. Inputs-vs-inference: real discipline, one overloaded evidence citation

The decomposition itself is not unfalsifiable in the way the charge worries about.
An unfalsifiable version would say "any failure that persists must have been
inference" with no independent test of which is which — but §4b.4 does not do
this: it states per-mechanism percentages **before Build 2.5 runs**, which means
a specific, dated, checkable claim exists to be wrong against. That is real
falsifier discipline, not post-hoc sorting — crediting the doc.

Where it goes soft is the one piece of evidence recruited to support "F-B is
inputs-shaped": GLM's V3 D2-heavy 6/6, described in §4b.1 as *"GLM verified each
child's report against the child's actual output file when it had the data."*
Checked directly against `FLEET-EVAL-V3.md:94-97`: this is **harvest-time**
verification — GLM re-derived test counts and timing samples from finished
children's output files, after they had already delivered. It says nothing about
whether GLM could or would **poll liveness of a still-running, silent child**
and decide "dead vs. slow" — the actual F-B risk (§3b: *"no watchdog... blind
sleep-escalation... terminated only because its children delivered"*). Those are
different competencies: reading a completed artifact correctly (demonstrated,
6/6) versus judging an unfinished, silent process's state from indirect signals
(never exercised in v3 — the doc's own §4 says so: "an *unexercised* risk").

The doc hedges this correctly in prose ("plausibly," "is direct supporting
evidence" — not "proves") but then carries a specific number, **~70%**, forward
in §4b.4 as though the hedge had been resolved rather than merely stated. A
70% figure implies a base rate has been estimated from *something*; the something
here is one adjacent, not-quite-matching data point. The number is not
decoration — it will get compared against a real Build 2.5 result and can be
wrong — but its input is thinner than its precision suggests.

**Verdict: WOUNDED.** The decomposition is doing real work as a falsifiable
framework. The F-B-specific prior leans on evidence that measures a related but
distinct capability, and the doc's confidence number doesn't carry the same
hedge its prose does.

---

## 3. The stopping rule — do the "three checks" exist to flip?

§4b.3's "Pass, defined per-arm" line names: *"the D2-heavy verification rows, the
deliberately-exercised dead-child row, the time-box row."* I checked each against
`fleet-rubric-v1.md`, the frozen rubric the whole battery runs against:

- **D2-heavy verification rows** — these exist today: §2c checks 5/6/7 (verify
  + close, refusal-reason, child-journal-falsifiers). Real, scoreable, already
  in the frozen rubric. **This one is well-defined.**
- **The deliberately-exercised dead-child row** — does **not exist** in
  `fleet-rubric-v1.md` as written. §4's own text admits this is new: *"the
  re-run should exercise it deliberately (kill a child mid-battery) to convert
  the unexercised risk into a measured row."* A row that must be *invented* for
  Build 2 is not yet a row that can be read off "as it actually scores," which
  is exactly the operator's suspicion. Until this row is drafted (what file
  fact witnesses "correctly judged a child dead," what counts as pass/fail,
  hard or soft), "flips" for this check is undefined — it will require a
  judgment call by whoever drafts it, and that judgment call is exactly the
  "vibe" the rubric's own §0 was built to keep out ("Binary observable checks
  only — no 1–10 vibes anywhere").
- **The time-box row** — also not present as such. D3/D4 have no "self-imposed
  time-box observed" check; the closest existing material is F-C's *behavioral*
  observation (deepseek tunneled 11 minutes) rather than a scored rubric row.
  Like the dead-child row, this needs to be authored, and its authoring is
  exactly where "flip" becomes a judgment call rather than a lookup.

So: **one of three named checks is well-defined against the existing rubric;
two require new rows not yet drafted.** This does not mean the stopping rule is
fake — new rows can be drafted with the same binary-observable discipline the
rubric already uses elsewhere (§4b's own dead-child exercise plan sketches what
the row would witness: did the parent correctly identify and act on a truly
dead child, from files). But "flips zero/≥2 of 3" as currently written is not
yet a lookup against a frozen document; it is a promise to write two more rows
in the same style, and the stopping rule's numeric precision (zero vs. one vs.
two) outruns what exists to measure it by 2/3.

### "3 battery runs + 1 week" vs. "per model generation"

The **spend cap** — 3 battery runs + 1 week of fork work — is a real, checkable
number: whoever runs Build 2.5/2.6 can count runs and calendar days against it,
and it does bound "try harder" the way the doc claims.

The **re-entry clause** is where the cap's teeth come out: *"a new model
generation is a new experiment... not a resumption of 'try harder.'"* No
criterion is given for what counts as a new generation — a GLM point release?
A named next-gen model from the same vendor? Any model at all released after
the STOP date? Without that criterion, the cap only binds the *current* attempt;
it does not prevent an indefinite sequence of "this is technically a new
generation" re-openings, each individually capped at 3 runs + 1 week but with no
ceiling on how many such re-openings occur. The cap is real for one cycle and
silent on the thing the operator's charge specifically worried about — reopening
indefinitely.

**Verdict: WOUNDED.** The per-cycle cap is real. Two of three stopping-rule
checks need to be authored before "flips" is measurable rather than judged, and
the "per model generation" re-entry has no stated trigger, which is exactly the
shape of an indefinitely reopenable clause.

---

## 4. The prior (§4b.4) — scoreable, but structurally comfortable for the author

The numbers are pre-registered before Build 2 data exists, which is the
falsifiable discipline the doc claims (§9's falsifier 7 explicitly says the
prior will be scored against the runs "in the doc, not quietly forgotten") —
this is not decoration; a specific F-B~70%/F-A~50%/F-C~80% set of numbers can
turn out wrong, and the doc says what would make them wrong.

The soft spot is the net line: *"the operator's 'try harder' bet succeeds with
meaningful probability (~40–45%) — but if it succeeds, I expect the win to come
from the STOCK scaffold, not the fork."* Walk the outcome space:

- **STOP fires (zero or ≥2-of-3 fail):** author's original "judgment is a model
  property, seats stay Claude" position vindicated.
- **2.5 alone clears the bar:** operator's *direction* (try harder) vindicated,
  but the author's specific prediction ("if it succeeds, via stock, not fork")
  is also vindicated — author right twice, per the doc's own words in §4b.4's
  last line.
- **2.6 (the fork) is what flips the last check:** the one outcome where the
  author says plainly "I was wrong twice." This is the *only* branch of the
  outcome tree that costs the author anything.

That is three branches, two of which read as author-vindicated and one of which
the author has pre-conceded. This is not proof the numbers are gamed — a real
technical prediction can legitimately have an asymmetric outcome space — but it
means "operator wins but via stock" is not a hedge that makes the prior
*unscoreable* (the charge's exact word); it is a hedge that makes the prior
**scoreable in a way that is favorable to the author's starting position in
2 of 3 branches.** The prior is falsifiable; it is not neutral. That distinction
is worth naming exactly because the doc's own text (§10) already owns a pattern
of the author's citations landing favorably to his own reasoning — this is the
same shape one level up, in a probability rather than a citation.

**Verdict: HOLDS, barely.** The numbers are real and pre-registered, which is
the discipline that matters most. The branch structure they're attached to is
tilted, and the doc doesn't flag the tilt the way it flags other self-known
weaknesses elsewhere (§10's confession pattern is a strength this section
doesn't extend to itself).

---

## 5. M4/M5 — the fork steelman the doc didn't run, and a stock mechanism it missed entirely

The brief asked me to steelman FORK harder than the doc did, specifically
checking for a context-window-curation mechanism for F-A that the doc might
have missed. It exists, and it is stronger than a fork case — **it needs no
fork at all**, which makes this a completeness defect in the *stock* mechanism
list (§4b.2's "Stock opencode — no fork" bullet group), not merely a
fork-steelman gap.

### The mechanism: `experimental.chat.messages.transform`

`OPENCODE-PLUGIN.md` §2.2, read in full for this review, documents this hook at
length — and LOOP.md itself cites the *sibling* hook (`system.transform`) from
the same table (`OPENCODE-PLUGIN.md` §2.1's hook table) as M1's basis. The two
hooks are adjacent rows in that same table:

| Hook | Power (per `OPENCODE-PLUGIN.md` §2.1) |
|---|---|
| `experimental.chat.system.transform` | own the system prompt, per turn — **used by LOOP.md as M1** |
| `experimental.chat.messages.transform` | rewrite **the whole conversation** the model sees this turn — **not used by LOOP.md anywhere in §4b** |

`messages.transform` is documented as unfit for **delivery** (§2.2's central,
correctly-emphasized finding: a message injected this way is a per-call view
mutation, never written to the session store, so the model can't recall it next
turn, and — the sharper reason — the model is *right* to treat unstored mail as
a prompt injection and refuse it). LOOP.md correctly avoids using it for
delivery (§7: "Not delivery via `messages.transform`... however tempting the
`MANATEE-5` result").

But **curation is a different operation from delivery, and the property that
disqualifies it for delivery (non-persistence) is irrelevant or even helpful for
curation.** Delivery needs the model to *remember* being told something across
turns — that's what non-persistence breaks. Curation needs the model to **not
see** something *this* call — that's what non-persistence trivially achieves,
because the hook fires fresh before every model call and rewrites the array
handed to the provider, not the store. The exact mechanism the doc rules out for
one job is close to ideal for a different job it never considers:

- **F-A's measured shape** (`FLEET-EVAL-V3.md:81-86`): deepseek spent 11 minutes
  reading spawn internals, simulating arg-insertion, spawning a test tab — a
  self-generated tail of harness-debugging turns that, left in context, is
  exactly the kind of material that keeps a model anchored to the detour rather
  than the brief (each new call sees its own prior detour and continues it).
- **A `messages.transform` hook could, on the same trigger M2 uses** (N
  near-identical failing/exploratory commands), **rewrite the messages array
  the model is about to see**: drop or collapse the harness-debug tail, and
  splice in a single synthetic line — *"you spent N turns debugging the
  harness; that is resolved; return to the brief: <brief text>."* This is not a
  request layered on top of the model's own view of its detour (which is what
  M1's instruction-half is); it **removes the detour from view** and replaces
  it with the re-anchor. The model cannot "ignore" a rule about a context it no
  longer sees the same way it can ignore a standing instruction sitting beside
  the thing it's currently doing.

This is stronger than M1 for F-A specifically (M1 only adds text; this changes
what competes for the model's attention) and marginal-but-real over M2 (M2 only
blocks the *next* tool call; it doesn't clean up the turns of context already
accumulated, which keep exerting pull on later calls within the same turn or a
continued session). It requires **no fork** — it is one more row in the same
"Stock opencode — no fork" bullet list M1-M3 already occupy.

### Why the doc missed it, on its own evidence

Not carelessness in a vacuum — `OPENCODE-PLUGIN.md` §2.2 spends its longest
passage making the case that `messages.transform` is **wrong for delivery**, and
that passage's rhetorical weight ("the single most important finding in this
document") plausibly anchored LOOP.md's later author away from revisiting the
hook for anything else. That's a real, nameable failure mode (a strong negative
result about one use crowding out consideration of a different use of the same
primitive) rather than a citation error — worth naming because it's the kind of
gap a second fresh reader is supposed to catch and the first review
(`hc-red2`) also did not catch it (LOOP-RED.md's evidence-integrity section
checks tag *accuracy*, not mechanism-list *completeness* — a different axis of
attack, which is exactly why the operator spawned a third reviewer with a
narrower brief).

### M4/M5 as stated — are they at least honest about what they are?

Yes, on inspection. M4 (hard turn-end gate) is correctly graded §2-refused for
judgment predicates — this matches `_hc-ocloop.md` §1's own pattern finding
(no v1 or v2 hook can gate turn-end at all; PHILOSOPHY §2's refusal of compelled
form is a separate, additional reason even where a gate *could* exist). M5
(harvest interlock) is honestly graded as "marginal over M1" and the doc is
right that acknowledgment-of-death is a one-bit act, harder to fake than prose —
that reasoning holds up against `_hc-ocloop.md`'s tool-blocking primitive
(`tool.execute.before`, VERIFIED). Both gradings survive scrutiny **as far as
they go** — the defect is not in what's said about M4/M5, it's in the list
being incomplete one row up, at the stock-mechanism layer that precedes any
fork discussion.

**Verdict: REFUTED as complete.** The mechanism list is missing a real, stock,
no-fork mechanism for F-A that is documented in this project's own prior art
and cited elsewhere in this same document for a different purpose. This is a
finding in the sense the operator's charge anticipated ("if yes, the mechanism
list was incomplete") — and it cuts in the operator's favor more than the
doc's: it strengthens the **stock** case (§4b.4's own prediction that "if it
succeeds, I expect the win to come from the STOCK scaffold" gets *more* support
from this finding, not less), which the doc should register as raising its own
Build 2.5 confidence numbers, not just as an omission to patch.

---

## 6. The quiescence rule — designed, but not built, and misfires on named shapes even as designed

### It does not exist in the code today

§1's Claude-backend bullet describes the rule in a mix of present and future
tense — *"the digest fires on quiescence... at Stop, if the inbound queue is
empty AND no send-to-parent has happened within the last T minutes... the hook
sends the parent one digest... and arms the cooldown"* — worded as a completed
design decision, distinguishable from Build 0's explicit "prerequisite, already
owed" framing (which correctly flags itself as **not yet built**). I checked
`bin/swarm`'s actual `cmd_event` (the named hook target, `bin/swarm:878`):

```python
def cmd_event(kind):
    # Stop/Notification. Record the fact; on Stop with a non-empty queue,
    # re-ring our own doorbell so the queue keeps draining while we idle.
    ...
    record_event(root, name, kind, last_assistant_text(...), now_ms())
    ...
    # ring only if queue head is deliverable
```

This is exactly what the doc's own §1 says it *extends* — but the extension
(cooldown file, quiescence check, digest-to-parent send) is **not present**.
`grep -n "cooldown\|quiescen" bin/swarm` returns nothing. There is no cooldown
file format defined anywhere in the repo, no digest-send call, no quiescence
predicate. The mechanism named as Build 1's Claude-backend core — "the core of
this design" per §1's own header — is prose describing a hook extension that
has not been written, and §1 does not flag it as unbuilt the way it flags Build
0. This matters because §4's central falsifiable prediction ("Build 2's re-run,
predicted 3/7→7/7") is a claim about a mechanism's *effect*, stated as though the
mechanism already exists to be re-run against — it doesn't yet, and the gap
between "designed" and "built" is exactly where the operator's "hope with a fork
attached" charge bites hardest on this specific surface.

### Even as designed, three concrete misfire shapes

**(a) Multi-turn-work digest-spam (false positive on "quiescence").** The rule's
predicate is "inbound queue empty AND no send-to-parent within T." An agent deep
in a long, single-threaded task (e.g., writing a large document across many
Stop/continue cycles, self-triggered by its own tool use rather than by inbound
mail) has an empty inbound queue for its entire working session — it isn't
waiting on anyone, it simply hasn't finished. Under the stated predicate, **every
Stop event during that work, once T minutes have elapsed since the last
send-to-parent, re-arms and fires a digest** — not once, but repeatedly, every
time the cooldown re-expires, for as long as the work continues without a
send. This is not a rare edge case; it's the *default* shape of focused,
uninterrupted work, which is presumably the behavior the whole reporting duty
wants to reward, not spam. The rule conflates "not talking to me" with "possibly
stuck," when the far more common cause of silence is "correctly absorbed in
work."

**(b) Children-waiting digest-spam (same false positive, different cause).** An
agent that has spawned children and is genuinely waiting — correctly, per its
own duty — for their reports has an empty inbound queue (nothing has arrived
yet) and, by design, is *not* sending to its own parent because it has nothing
new to report until a child delivers. This is exactly the state the design
elsewhere calls correct behavior (§3's table: "Done-signal... artifact-exists
convention + idle"). Under the quiescence rule as stated, this correct waiting
state is indistinguishable from a stuck one and will generate a digest every T
minutes regardless — "last assistant words" for an agent that is idling on its
queue will read as something like "waiting for child X" repeated verbatim
across digests, which is exactly the "unread formality" failure mode
`LOOP-RED.md`'s falsifier-3 discussion already names for a different reason (a
parent that stops reading digests because they carry no new information) — this
review adds the concrete *mechanical* cause of that flavor of noise.

**(c) Cooldown-file survival across restarts.** §1 does not state whether the
per-agent cooldown file is expected to survive a process/machine restart. Two
readings, both bad in a different direction:
  - **If the cooldown file is ephemeral** (e.g., tied to a directory that a
    restart clears, or reset on every fresh session start), an agent restarted
    after a long-lived cooldown had already suppressed several digest cycles
    comes back with a **cold cooldown** — the very next Stop, however soon after
    restart, satisfies "no send within T" trivially (T minutes have "passed"
    relative to a clock reset to zero) and fires a digest immediately, even if
    the agent is mid-recovery and has nothing yet worth reporting. This produces
    a burst of restart-triggered digests exactly at the moment a parent is
    least equipped to distinguish "restarted and fine" from "restarted and
    struggling" from the digest content alone (last words at that point are
    likely restore-boilerplate, not task content).
  - **If the cooldown file is meant to persist** (a plain file under `.swarm/`,
    consistent with the rest of the design's file-based philosophy), the doc
    never states this, and it is the kind of implementation detail whose
    absence is exactly what makes surface (a)/(b) above hard to rule out from
    the text alone — a persistent cooldown *mitigates* (a)/(b)'s spam rate
    (fewer re-arms) but does not eliminate the underlying false-positive
    predicate; it only changes how often it fires.

None of these three are exotic — (a) and (b) are the *modal* shapes of a
working, healthy agent tree, not adversarial or unlikely inputs. A rule whose
false-positive cases are the common case, not the exception, needs either a
smarter predicate (e.g., distinguish "quiet because blocked" from "quiet because
working" from "quiet because waiting on children" using something other than
elapsed time — such as whether the agent's own children have open, undelivered
items, which is exactly the liveness data M1 already proposes computing for the
opencode side and could equally be read on the Claude side) or an explicit
acceptance that the design trades false-positive digest volume for guaranteed
non-silence, stated as a tradeoff rather than left implicit.

**Verdict: REFUTED as currently specified.** Unbuilt today, and the design as
written — not merely as implemented — misfires on the two most common healthy-
agent shapes (heads-down work, waiting on children) by conflating "no message
sent" with "possibly stuck," and leaves cooldown persistence across restarts
unstated in a way that produces a bad outcome under either plausible reading.

---

## RANKED REPAIRS

1. **Build the quiescence mechanism, or flag it unbuilt.** Either implement the
   cooldown file + digest-send extension to `cmd_event` before treating §4's
   7/7 prediction as re-runnable, or relabel §1's Claude-backend bullet the way
   Build 0 is labeled ("prerequisite, already owed") so a reader doesn't mistake
   design prose for shipped mechanism. This is the highest-priority repair
   because it affects whether Build 2 can even run as described.

2. **Fix the quiescence predicate before building it.** Add a liveness/waiting
   signal (e.g., "agent has undelivered sends to children" or "agent's last N
   tool calls touched artifacts within the task scope") so that heads-down work
   and children-waiting states are distinguished from genuinely stuck silence,
   rather than firing a digest on elapsed time alone. State explicitly whether
   the cooldown file persists across restarts, and if so, where (a `.swarm/`
   path, consistent with the rest of the design).

3. **Add `experimental.chat.messages.transform`-based context curation as a
   named stock mechanism** (call it M0 or fold into M1/M2) targeting F-A: on
   the same perseveration trigger M2 uses, rewrite the messages array to
   collapse/replace the harness-debug tail with a re-anchoring line, rather
   than only appending a rule beside it. This is stronger than M1's instruction
   half, needs no fork, and should raise (not lower) the doc's Build 2.5
   confidence numbers in §4b.4, since it adds another stock lever to the side
   the doc already predicts will win.

4. **Split M1 into its data half and its instruction half**, and grade them at
   different confidence: the computed clock/liveness table is a real,
   loop-supplied input (high confidence, no fork, cheap); the standing
   "blocked >N min → journal BLOCKED" rule is a PROMPTED duty in the same sense
   §3's own duty table already uses that word elsewhere in this document, and
   should be graded there, not folded into the same mechanism number as the
   data supply.

5. **Author the two missing rubric rows** (deliberately-exercised dead-child
   row; self-imposed time-box row) before Build 2.5, in the same
   file-fact-witnessed, binary style as `fleet-rubric-v1.md`'s existing checks,
   so "flips zero/≥2 of 3" is a lookup at re-run time rather than a judgment
   call made in the moment — which is the exact vibe-reintroduction risk the
   operator's charge named.

6. **Give "per model generation" a stated trigger.** Define what distinguishes
   a "new model generation" (e.g., a named next major version from a vendor
   already in the battery, or any model release after the STOP date, whichever
   is more conservative) so the re-entry clause cannot be invoked on the
   author's judgment alone after a STOP.

7. **Flag the branch asymmetry in §4b.4's prior.** Note explicitly that 2 of the
   3 outcome branches (STOP; 2.5-alone-succeeds) read as author-vindicated and
   only 1 (2.6/fork-succeeds) is conceded as author-wrong-twice, the same way
   the doc's §10 already names its own citation-integrity pattern — this keeps
   the prior's self-awareness consistent across the document rather than
   applying it to citations but not to the probabilities built on them.

8. **Recompute F-B's ~70% figure with its evidence gap stated inline**, not
   only in prose above it — e.g., "~70% (evidence: harvest-time file-verification
   6/6; untested: live-liveness-while-blocked judgment, the actual F-B
   mechanism)" — so the number's precision doesn't outrun what it's built on
   when read on its own, out of the surrounding hedge.
