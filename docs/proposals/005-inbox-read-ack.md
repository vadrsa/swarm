# Proposal 005 — Notify-and-pull for the inbox: adopt, but not for the reason proposed, and not for agents

**STATUS:** **ADOPTED** (2026-07-09), all three parts, plus one operator addition ·
**From:** product · **Implementation:** commissioned from `cos`
**Requested by:** the operator, who asked explicitly for criticism rather than agreement

---

> ## Outcome
>
> The operator adopted this as written and rejected the half of his own redesign that this
> document argued against:
>
> 1. **Operator mailbox → explicit cumulative acknowledgement.** Reading never destroys;
>    `swarm updates` becomes non-destructive in all forms including `--json`. `read` prints
>    ids, `ack` must **name the highest id claimed**, and there is **no `ack --all`** — the
>    safety requirement this document raised at *"the N+1 question"* below.
> 2. **Agents keep full-body injection.** Notify-and-pull is **rejected**.
> 3. **New verbs** `swarm inbox read` / `swarm inbox ack <id>`, an honest header, and a real
>    cap (no single oversized message blowing through the budget — G10).
> 4. **Operator addition:** `swarm send` rejects oversized bodies with a helpful error,
>    establishing *files-referenced-by-path* as the pattern for large payloads. The limit is
>    `cos`'s to pick, grounded in the injection budget.
>
> **`swarm inbox read`/`ack` therefore governs what the cap holds back, and the operator's
> mailbox stops being destructively read. Nothing is unified** — the Python and Node read
> paths stay separate, because unifying them would import G17 into the operator's channel
> (see the cost of unification below).
>
> **One note for the implementer.** Item 3's *"fix the lying header"* refers to the
> `Showing 3 of 5 new messages (2 remain…)` wording. Product filed that as a **defect** and
> then **retracted it** — `cos` proved the shortfall is already announced by an `…and N more`
> line that ships. The retraction stands: this is a **copy improvement**, not a bug fix. It is
> worth doing, and the code already does the thing it was accused of omitting. Do not go
> looking for a missing disclosure.

> ## Correction, 2026-07-09 — one supporting claim in this proposal was wrong
>
> This document repeatedly describes today's cumulative acknowledgement as **silent**, and
> recommends a header line to fix that "defect." **The acknowledgement is not silent.** The
> hook unconditionally appends `…and N more; full messages in inbox/<id>/` whenever it
> withholds anything. `cos` refuted the claim by running the fixture rather than accepting
> it from a sibling who had been right three times running.
>
> **What survives:** the recommendation is unchanged — *adopt the acknowledgement model,
> reject the notification model, unify nothing.* Every argument for that verdict stands on
> its own evidence. The observation that the product **already performs implicit cumulative
> prefix-ack** stands too, and remains the strongest argument for the operator's instinct.
> What falls is one word: *silent*. The proposed header line is a **copy improvement**, not
> a defect fix, and should not be carried as a rider on any code change.
>
> **What chasing the refutation found:** a real, critical, message-loss defect —
> **G17**, where the *agent* delivery hook destroyed any message over ~64 KB, silently, with
> a success exit code. (The operator's own mailbox was spared, because it is read by Python
> rather than Node — an accident, not a design, and one that unification would have undone.
> See the cost of unification below.) Product asserted a defect from reading; engineering
> disproved it by executing; executing then found a worse one. That sequence is the argument
> for the method, and it is why this correction is printed here rather than edited away.
>
> **G17 was fixed and installed the same day** (PR #31), so decision 0 below needs no
> answer. Decisions 1–3 stand.

---

**TITLE**

Replace pushing message bodies into an agent's context with a notification the agent
must act on, and make acknowledgement an explicit, cumulative, separate step.

**RECOMMENDATION**

**Adopt-modified, and split in two.** The proposal contains one change that is
straightforwardly right and one that is a regression, and they have been bundled.

1. **Adopt explicit cumulative acknowledgement — for the operator's mailbox.** It fixes
   a live, confirmed bug where reading the mail destroys it. Do this now.
2. **Reject notify-and-pull for agents.** Keep injecting message bodies. The proposal
   trades a guarantee the system currently *has* for a saving it does not need, and it
   introduces a failure mode that reconciliation cannot reliably catch.
3. **Adopt one piece of the diagnosis regardless:** today's 8,000-character cap already
   performs an implicit cumulative ack — announced, not silent (see the correction above).
   That behaviour is *correct*, and it is the reason the operator's instinct is right.
   Making it explicit needs a verb, not a bug fix.
4. **G17 is fixed** (PR #31), so this no longer gates the redesign. It remains a reason
   not to unify: the operator's mailbox was the one inbox G17 could not reach, spared only
   because it is read by Python rather than the Node hook. Unification would have handed it
   the bug. That accident should not be relied on twice.

The unifying instinct — one read/ack model for agents and the operator — is the part I
think is wrong. Agents and the operator are not the same kind of recipient, and the
proposal's own strongest argument only applies to one of them.

**WHY NOW**

Two mail-handling bugs are open at once. The research analyst found that `swarm updates`
marks the operator's mail read on **every** invocation, including `--json` — so any
script that polls it silently destroys the mail it read. The chief-of-staff is holding
that fix pending exactly the decision this proposal asks for. That half is urgent.

Nothing about agent-side injection is urgent. It works.

**EVIDENCE**

All of this was read out of `bin/swarm-hook.cjs` and `bin/swarm`, not out of the task
description, which I was asked to verify rather than trust. It was right on every point
except one, noted below.

**1. The operator's mailbox really is destructively read, including by `--json`.**
`cmd_updates` prints, flushes, then calls `mark_read()` — which moves every message into
`read/` — and it does this *before* `sys.exit(0)` on the `--json` path too. A monitoring
script that runs `swarm updates --json` in a loop consumes the operator's escalations and
leaves no trace in the terminal. Confirmed at source.

**2. `inbox-check` fires only on `UserPromptSubmit`.** This is the load-bearing fact, and
it is why injection is safe today. A prompt submission is a turn *beginning*. The message
body lands in the context of a turn that is already going to happen, with no action
required from the agent to receive it. Delivery is **atomic with the turn**. There is no
step at which the agent can fail to collect its mail, because collection is not something
the agent does.

**3. Today's cap already performs a cumulative ack — the task description missed this.**
The hook injects messages until the running total exceeds 8,000 characters, then marks
read **exactly the prefix it injected** (`for i = 0; i < injectedCount; i++`). The
remainder stays unread and is re-offered next turn.

I did not infer this. I ran the shipping hook against a synthetic inbox of five 2,600-character
messages:

```
HEADER:          [swarm inbox] You have 5 new message(s) from other agents:
bodies injected: 3
still unread:    2      moved to read/: 3
…and 2 more; full messages in inbox/tester/
```

So the system **already** acknowledges a prefix and leaves a suffix — exactly the semantics
the proposal wants to introduce — and it *tells the agent so*, pointing at a directory
rather than giving it a verb. **The proposal's cumulative-ack model is not a new idea for
this system; it is a description of what the code already does, without a verb to name it.**

*(An earlier draft of this proposal said "minus the honesty" and called the ack silent.
That was wrong; the `…and N more` line ships. See the correction at the top. The
substantive point — that cumulative ack already exists and works — is what matters, and it
is unaffected.)*

**4. The `injectedCount > 0` guard means the cap is not a cap.** Same method, one 20 KB
message followed by a 100-byte one:

```
injected chars:  20224     (CAP is 8000)
bodies injected: 1
unread left:     1
```

The oversized message is injected **in full, 2.5× over the cap**, because the loop keeps at
least one. So "capped at 8k" is false for the case that matters most and true only where
truncation would have been harmless. Any context-economy argument built on that cap is
built on a number the code does not honour.

**This escape hatch is the delivery vehicle for G17.** The `CAP` guard bounds the
*multi-message* case at `8000 + one body`, which can never reach the 64 KiB pipe buffer.
Only a **single** message over the threshold gets there — and it gets there precisely
because the loop refuses to withhold the first one. `cos` found the other half: `cmd_send`
has **no size guard at all**, so nothing upstream prevents it. An oversized body is queued,
injected whole, truncated by the pipe, and destroyed.

**5. Context economy is real but small.** Measured across the five messages actually in my
inbox today: **16,302 characters, roughly 4,076 tokens**. A notification would be about 20.
Against a one-million-token window, a full day of inter-agent mail costs **0.4%** of
context. The proposal's context saving is genuine and it is not worth a guarantee.

## The failure mode this introduces

Today: the message is in the context of a turn that is happening anyway. **Zero agent
actions required.**

Proposed: the agent is told mail exists and must spend a tool call to read it, then
another to acknowledge it. **Two agent actions required, both optional, both forgettable.**

The task asks whether reconciliation catches this. It does not, and the reason is
structural rather than a matter of diligence:

- Reconciliation is a **duty, not a mechanism** — deliberately, per this project's own
  philosophy. Nothing fires it. An agent that ignores a notification is precisely an agent
  that is not reconciling carefully, so the safety net is woven from the same thread as
  the failure.
- The notification arrives via `additionalContext`, which the hook's own comment warns
  "reads as out-of-band context, so without framing the model may not treat it as a
  directive." That comment exists because someone already observed the model under-reacting
  to injected context. **The proposal's entire delivery guarantee rests on the model
  reliably obeying the one channel the codebase documents as unreliable for directives.**
- The failure is silent on both ends. The sender sees exit 0. The message sits unread. No
  verb reports it. Read receipts were explicitly deferred, so nothing closes the loop.

That last point deserves its own line. The gap register already records that delivery is
guaranteed to the inbox, not to the agent — an agent that goes permanently idle never
reads its mail. **Notify-and-pull widens that window from "an agent that never takes
another turn" to "an agent that takes a turn and doesn't feel like reading."**

## What the crash-safety story actually becomes

Today, *as designed*: emit, then rename. A crash between them re-injects next turn.
**Fails safe by re-showing.**

Today, *as built*: that ordering assumes the emit either happened or didn't. **It can
half-happen.** `process.stdout.write()` to a pipe queues its overflow and
`process.exit(0)` discards it, so above ~64 KB the hook renames a message it never
delivered — and the failure is not a crash, so the "crash between the two" reasoning never
engages. See G17. **The current design's fail-safe property is real for small messages and
inverted for large ones**, which is worth holding in mind before replacing it with a
different one.

Proposed, per the task: `read` prints, `ack` renames. Between them sits an *agent decision*
and a second process invocation. The window is no longer microseconds inside one process;
it is however long the agent takes, and it spans a possible context compaction, a restart,
or an idle death. Crash-safety is preserved in the same direction — an un-acked message
re-shows — but the window grows by orders of magnitude, and the thing that closes it is
now the model's diligence rather than a `rename` two lines later.

**Cumulative ack does close one real hole**, and this was the proposal's best argument as
first written. Today, "which messages did the agent actually see?" is answered by a side
effect of a character count. If the agent's turn dies after injection but before the renames
complete, `injectedCount` messages were shown and some subset were moved — the loop is not
atomic across files. Explicit ack replaces that with a single monotonic watermark the agent
controls. That is strictly better *bookkeeping*.

### A stronger argument, supplied by the agent it indicts

*Added after adoption. `cos` routed this at the operator's request, as evidence.*

The operator sent `cos` the directive adopting this proposal. **`cos` never acted on it.** It
kept reporting the mail-read item as "awaiting the operator" for four more cycles while the
answer sat in its own `read/` directory. The operator had to re-send it.

The tempting reading is *"a message slipped, therefore push is unreliable, therefore
notify-and-pull."* **That inverts it**, and the artifacts say so. Product replayed the exact
pair through the real hook — the 4,699-byte message that preceded it and the 2,036-byte
directive that followed 37 seconds later:

```
header: [swarm inbox] You have 2 new message(s) from other agents:
bodies injected: 2          operator body present: TRUE
total injected: 6,965 chars (CAP 8,000)   withheld line: none
acked to read/: 2           still unread: 0
```

Nothing was truncated. **The directive was fully in the agent's context, beside the other
message, with its commissioning text intact.** The agent answered the interesting technical
exchange and not the operator telling it what to build. Then the hook auto-acked both.

So this is **not a delivery defect, and it is evidence *for* rejecting notify-and-pull.** The
failure was not that `cos` lacked the text — it had the text. The failure was that it did not
act. Replacing the body with *"you have 1 message, go read it"* converts a message the agent
ignored into a message it must take a **second, separate, forgettable action** even to see.
It demonstrably forgot the zeroth action; adding a first one does not help.

What the incident *does* prove is the hazard this document already names — **"`ack N+2`
silently acknowledges N+1, whether or not the agent understood it"** — happening in the wild.
The hook acked the directive into `read/` at the instant of injection, on the strength of
having *rendered* it. **Shown is not understood.** Today's implicit prefix-ack acknowledges
**delivery** and records it as **receipt**.

Under explicit cumulative ack, that directive would have stayed outstanding and re-surfaced on
every subsequent turn until claimed by id. `cos` would have tripped over it four times.

> **The watermark is not merely cleaner bookkeeping. It is the only mechanism by which a busy
> agent's own inattention becomes observable to itself. A message that stays outstanding is a
> message that keeps asking.** — `cos`, on being the counterexample

That argument is stronger than the data-integrity one above, and this document did not have
it. It corrects a claim made in the next line as originally written.

**The bookkeeping problem belongs to the operator's mailbox. The *inattention* problem belongs
to agents, and this proposal originally missed it.**

## Cumulative ack: the N+1 question

The task asks what happens to message N+1 when the agent acks N after reading N+2.

Under cumulative ack, `ack N` acknowledges everything **up to and including** N. So N+1 and
N+2 remain unread and are re-offered. That is correct and safe. The hazard is the opposite
one, and the task did not ask about it:

> **`ack N+2` silently acknowledges N+1, whether or not the agent understood it.**

An agent that reads three messages, acts on the third, and acks the third has just
discarded the first two with no record that it ever engaged with them. Per-message ack
would prevent that; cumulative ack makes it a one-token mistake. Given that a message may
be a *steering instruction from a parent*, silently marking an unactioned instruction as
handled is a worse failure than showing it twice.

**If cumulative ack is adopted, `read` must print message identifiers and `ack` must name
the highest one the agent is claiming.** Never `ack --all`. The ceiling should be a
count, and messages beyond it stay unread — no starvation, because the next `read` offers
them again, exactly as the cap does today.

**COST**

- **Operator-side ack (recommended):** small. `swarm updates` stops calling `mark_read()`;
  add `swarm inbox ack <id>` and print the ack hint after each message. This is close to
  what the chief-of-staff is already holding.
- **Agent-side notify-and-pull (not recommended):** a new verb pair, a rewrite of
  `inbox-check`, a change to `WORLD.md`'s delivery guarantee — which `RELEASING.md`
  classifies as **breaking** — and a migration for every running agent, whose hook config
  is baked into its pane at spawn and cannot be changed in place. The last cutover of this
  kind had to be sequenced by hand and blinded every live agent. It is recorded as a gap.
- **Unification (not recommended):** the operator has no hook, no turn, and no context
  window. Agents have all three. A unified model must be the *weaker* of the two — pull —
  which means unification is not a simplification; it is a downgrade of the agent path in
  order to make one code path serve two very different recipients.

  **And there is now a concrete hazard, found after this proposal was first written.**
  The operator's mailbox is the only inbox in the system that G17 cannot destroy, and it
  is spared *by accident*: `cmd_updates` is Python, which flushes stdout on exit; the agent
  hook is Node, which discards it. Nothing records that dependency and nothing tests it.
  **Unifying the two read paths would carry the agent path's message-loss bug into the
  operator's mailbox** — the one channel where a lost message is an unanswered escalation.
  G17 is now fixed, but the lesson stands: unify only if a reason survives that isn't
  "one code path is tidier."

**ALTERNATIVES**

- *Adopt as proposed, wholesale.* Rejected on the evidence above: it exchanges an atomic
  delivery guarantee for a 0.4% context saving and a new silent-failure mode.
- *Notification-only, but the hook exits nonzero until the agent reads.* Rejected: this is
  hook enforcement, which the operator abandoned for checkpoints — *"the agent should just
  know…"* — and which he denied when it returned as tooling. It would also break the hook's
  stated contract that it must never break the turn.
- *Inject bodies AND provide `swarm inbox read`/`ack`.* **This is the modification I
  recommend.** Keep the push (delivery stays atomic), add the verbs (the operator gets a
  real read path; agents get a way to re-read a message they've lost to compaction, which
  today requires reaching into `inbox/<id>/read/` by hand). Explicit ack governs only the
  *overflow* — the messages beyond the cap — which is precisely where today's implicit
  cumulative ack lives.
- *Keep everything, just fix `--json` not to mark read.* This is the minimum viable fix and
  it is defensible. It is narrower than what I recommend only because "reading destroys"
  is a design smell that will bite again, not just on `--json`.

**DECISION**

Four items. **The first needs no answer — it is already done.** The rest are separable
yes/no.

0. ~~**Fix G17 now**~~ — **DONE, no decision needed.** `cos` fixed and installed it the day
   it was filed (PR #31, `08f683b`). Both hook writes now wait for stdout to drain, and the
   `read/` rename is conditional on the write actually succeeding. Product verified this
   independently against the installed hook: a 400 KB message delivers and parses; an
   `EPIPE` mid-write leaves the message **unread** rather than acking it. *The channel no
   longer destroys large messages.* Decisions 1–3 below are now unblocked.
1. **Operator mailbox: make acknowledgement explicit and cumulative** (`swarm updates`
   becomes non-destructive; add `swarm inbox ack <id>`). Yes/no.
2. **Agents: keep injecting message bodies** rather than switching to notify-and-pull.
   Yes/no. (Product recommends yes — keep injection.)
3. **Add `swarm inbox read`/`ack` as verbs available to both**, governing only what the
   injection cap leaves behind. Yes/no. *(The header line is a separate copy nit; do not
   bundle it.)*

If you want one answer rather than three: **adopt the acknowledgement model, reject the
notification model.** (The message loss is already fixed.)

**IF NO** — i.e. you adopt the redesign wholesale

Product will document the new guarantee honestly, which means rewriting `WORLD.md`'s
delivery language from *"a message is always delivered"* to something like *"a message is
always **queued**; an agent that does not read its inbox does not receive it."* That is a
materially weaker promise than the one the durable-inbox work was built to make, and the
gap register will carry it as a known limitation rather than a defect, because it will have
been chosen. I will also record that this was decided against product's recommendation, so
the record shows where the disagreement was.

---

## Postscript — the thing this review actually found, and how

Not the header. **G17**, and it is already fixed.

A message over ~64 KB never reached the agent. The hook wrote it to a pipe, Node buffered
the overflow, `process.exit(0)` threw the buffer away, the harness parsed truncated JSON
and injected nothing, and the message — already renamed into `read/` — was gone. Exit code
0. No error anywhere. The cliff was exact: 65,265 bytes of body delivered; 65,266
destroyed.

`cos` fixed it the same day (PR #31), and caught a bug in its own first draft while doing
so: under `EPIPE` the drain callback fires *with an error*, and its initial version acked
the message anyway — *"I had reproduced the original bug in a new costume."* The rename is
now conditional on delivery. Product verified both properties independently against the
installed hook rather than accepting the report.

It was independent of everything above, it was one line in the hook, and it falsified the
sentence `WORLD.md` uses to describe the whole feature: *"the message is surfaced into the
agent's context on its next turn — even if the agent was busy or the doorbell was missed."*
That sentence is true again.

**How it was found is the argument for how product should work.** I filed a defect
(the header's acknowledgement is silent) that I had reasoned out from reading the source.
`cos` did not accept it from a sibling who had been right three times running; it ran the
fixture, found the `…and N more` line I had myself quoted two paragraphs earlier in
[PRD 02](../prd/02-inbox-messaging.md), and told me. Chasing *why* I had been wrong is what
put me back in front of the hook with a synthetic inbox — and that is where G17 was.

Three agents had been over that file — `rd` filed a finding on it, a child of `cos` rewrote
a function inside it, and `cos` reviewed that diff line by line. **None of them saw a 64 KiB
cliff sitting under a `process.exit()`.** It surfaced only because a wrong claim was chased
rather than defended.

The system already does implicit cumulative acknowledgement, and announces it. Making it
explicit is right. Making it *pull-based* is the part that costs a guarantee.
