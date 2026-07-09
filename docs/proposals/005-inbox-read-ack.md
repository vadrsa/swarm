# Proposal 005 — Notify-and-pull for the inbox: adopt, but not for the reason proposed, and not for agents

**STATUS:** proposed · **From:** product · **Date:** 2026-07-09
**Requested by:** the operator, who asked explicitly for criticism rather than agreement

---

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
> **G17**, a message over ~64 KB is destroyed by the *agent* delivery hook, silently, with a
> success exit code. (The operator's own mailbox is spared, because it is read by Python
> rather than Node — an accident, not a design, and one that unification would undo. See
> the cost of unification below.) Product asserted a defect from reading; engineering
> disproved it by executing; executing then found a worse one. That sequence is the argument
> for the method, and it is why this correction is printed here rather than edited away.

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
4. **Fix G17 first, ahead of all of this.** A message over ~64 KB sent to an *agent* is
   destroyed on delivery. It is unrelated to the redesign, it is one line in the hook, and
   no decision about read/ack semantics matters while the agent channel loses large
   messages outright. It is also a reason not to unify: the operator's mailbox is the one
   inbox G17 cannot reach, and unification would hand it the bug.

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

**Cumulative ack does close one real hole**, and this is the proposal's best argument.
Today, "which messages did the agent actually see?" is answered by a side effect of a
character count. If the agent's turn dies after injection but before the renames complete,
`injectedCount` messages were shown and some subset were moved — the loop is not atomic
across files. Explicit ack replaces that with a single monotonic watermark the agent
controls. That is strictly better *bookkeeping*.

But it is better bookkeeping for a problem the operator's mailbox has and agents do not.

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
  Fix G17 first (decision 0), and then unify only if a reason survives that isn't
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

Four separable yes/no answers. **The first is not part of your redesign and outranks all
of it.**

0. **Fix G17 now** — do not `process.exit()` before stdout drains; add a size guard to
   `send`; truncate an oversized injection with a pointer to the file rather than emitting
   it whole. Yes/no. *(Product recommends yes, immediately. Every message over ~64 KB sent
   **to an agent** is currently destroyed — including one you send. Your own mailbox is
   spared only because it is read by Python, which unification would change. No read/ack
   semantics matter while that is true.)*
1. **Operator mailbox: make acknowledgement explicit and cumulative** (`swarm updates`
   becomes non-destructive; add `swarm inbox ack <id>`). Yes/no.
2. **Agents: keep injecting message bodies** rather than switching to notify-and-pull.
   Yes/no. (Product recommends yes — keep injection.)
3. **Add `swarm inbox read`/`ack` as verbs available to both**, governing only what the
   injection cap leaves behind. Yes/no. *(The header line is a separate copy nit; do not
   bundle it.)*

If you want one answer rather than four: **fix the message loss, adopt the acknowledgement
model, reject the notification model.**

**IF NO** — i.e. you adopt the redesign wholesale

Product will document the new guarantee honestly, which means rewriting `WORLD.md`'s
delivery language from *"a message is always delivered"* to something like *"a message is
always **queued**; an agent that does not read its inbox does not receive it."* That is a
materially weaker promise than the one the durable-inbox work was built to make, and the
gap register will carry it as a known limitation rather than a defect, because it will have
been chosen. I will also record that this was decided against product's recommendation, so
the record shows where the disagreement was.

---

## The one thing to fix today regardless of this decision

Not the header. **G17.**

A message over ~64 KB never reaches the agent. The hook writes it to a pipe, Node buffers
the overflow, `process.exit(0)` throws the buffer away, the harness parses truncated JSON
and injects nothing, and the message — already renamed into `read/` — is gone. Exit code 0.
No error anywhere. The cliff is exact: 65,265 bytes of body is delivered; 65,266 is
destroyed.

This is independent of everything above, it is one line in the hook, and it falsifies the
sentence `WORLD.md` uses to describe the whole feature: *"the message is surfaced into the
agent's context on its next turn — even if the agent was busy or the doorbell was missed."*

**How it was found is the argument for how product should work.** I filed a defect
(the header's acknowledgement is silent) that I had reasoned out from reading the source.
`cos` did not accept it from a sibling who had been right three times running; it ran the
fixture, found the `…and N more` line I had myself quoted two paragraphs earlier in
[PRD 02](../prd/02-inbox-messaging.md), and told me. Chasing *why* I had been wrong is what
put me back in front of the hook with a synthetic inbox — and that is where G17 was.

The system already does implicit cumulative acknowledgement, and announces it. Making it
explicit is right. Making it *pull-based* is the part that costs a guarantee. And none of
it matters until the channel stops eating large messages.
