# Contract changes — send/inbox (operator rulings 1 and 2)

*The words for the mechanism `send-inbox` is building. Product owns these; `cos` and its child
own the code. Written against **PR #59's diff**, not against a description of it.*

**Status:** drafted for `send-inbox`. Ask 1 lands on PR-1; Ask 2 lands with PR-2; the migration
note routes to `release-mgr`, who owns `RELEASING.md`.

---

## One correction, because it changes the paragraph

`send-inbox` reported that *"the asymmetry is GONE."* **Half of it is.**

What died is the **acking** asymmetry — nothing but an explicit `ack` reaches `read/`, for agent
or operator alike. What survives is a **mechanical** difference, and PR #59's own comment says
so: *"the operator has no hook, so `rendered/` is normally empty in its box — but the definition
of outstanding is one definition."*

Agents get a `rendered/` state because agents have a hook that renders. The operator does not.
**Same rule, different mechanics.** The replacement paragraph must say that, or the next reader
will wonder why the operator has an empty directory.

## Ask 1(a) — replace `WORLD.md` lines 68–72

*(the "For an **agent**… That asymmetry is deliberate." paragraph)*
  Mail is **never acked by being shown**. A message is injected into an agent's context in
  full exactly once; from then on the hook only *nags* — one line naming the unacked ids —
  and the message stays outstanding until an explicit `swarm inbox ack`. The same rule holds
  for the operator, who has no hook and therefore is never shown anything automatically.
  Rendering is not acknowledging: **only `ack` consumes**, for everyone.

  A message therefore has three states, and its state is where the file lives:
  `inbox/<id>/` (never delivered), `inbox/<id>/rendered/` (delivered once, still unacked),
  `inbox/<id>/read/` (acked). **Outstanding = unacked = the first two.** An agent's
  `rendered/` fills as the hook delivers; the operator's stays empty, because nothing
  delivers to it — but the definition of outstanding is one definition.

## Ask 1(b) — replace `WORLD.md` line 60
Current: "`swarm inbox read [--json]` → your unread messages, each with its **message id**."

Replace with:
  `swarm inbox read [--json]` → your **outstanding** messages — everything unacked, whether
  or not it has already been delivered to your context — each with its **message id** and a
  note of which it is. Non-destructive; safe to run repeatedly.

Reason: "unread" is now false and strictly too small. A message delivered to your context an
hour ago is still outstanding, and `read` shows it — which is the entire point of the change,
and the thing that makes the nag's instruction ("re-read with `swarm inbox read`") true.

## Ask 2(a) — replace the delivery guarantee (`WORLD.md` lines 37 and 41)
Line 37, currently: "Delivery is guaranteed by the file: the message is surfaced into the
agent's context (via a UserPromptSubmit hook) on its next turn — even if the agent was busy or
the doorbell was missed."

Replace with:
  Delivery is guaranteed **once the message is accepted**: it is written to the target's
  inbox before anything else, and it is surfaced into the agent's context on its next turn
  even if the agent was busy or the doorbell was missed. **Acceptance is not guaranteed** —
  see backpressure below.

Line 41, currently: "a message is *always delivered*, but a busy agent may see it on its next
turn rather than instantly."

Replace with:
  an **accepted** message is always delivered, though a busy agent may see it on its next
  turn rather than instantly. A message that `swarm send` **rejects** was never accepted and
  was never queued: the sender holds it, and knows.

## Ask 2(b) — the backpressure contract (new bullet, under `swarm send`)
  **Backpressure.** An agent holding **50 or more unacked messages** stops accepting mail.
  `swarm send` to it **exits non-zero** with `agent busy, N unacked, try again later`, and
  **nothing is queued** — the message does not exist anywhere. This applies to the
  `operator` target too: a full operator inbox is a real signal, not an exemption.

  A refused sender must **reason about the refusal, not retry it**. Proceed if you can
  continue without the reply; **escalate** if you cannot. Retrying a full inbox is spinning;
  the inbox drains only when its owner acks.

  **You can always dig yourself out.** `swarm inbox ack` reads your *own* inbox and needs no
  incoming message, and the nag reaches you on your own turn through the hook — a different
  path from the send cap. A capped agent always sees its unacked ids and can always ack. The
  only agent that stays full is one that has stopped taking turns, and that is precisely the
  signal the refused sender is meant to act on.

## Ask 2(c) — where the migration note goes
RELEASING.md, as a migration note in the tagged tree. Not WORLD.md, not a PRD, not a proposal.

The reason is a standing operator ruling, and it is load-bearing: G1 is CLOSED-accepted, and
its closure entry states that across a breaking minor **the RELEASING.md migration notes are
the ONLY user-facing warning** — the `--major` guard is deliberately inert through 0.x. So a
contract change that removes an unconditional guarantee MUST land its note inside the tagged
tree, or a user crosses it with no warning at all. That is exactly the dependency G1's closure
names.

Text for the note (release-mgr owns the version heading and the standard warning block; this is
the body):

  **Delivery is no longer unconditionally guaranteed.** `swarm send` now refuses mail to an
  agent holding 50 or more unacked messages, exiting non-zero and queueing nothing. Scripts
  that assumed `swarm send` always succeeds must check its exit status. A refusal is not a
  transient error to retry — it means the recipient is not draining its inbox, and the
  sender should proceed without the reply or escalate.

  Relatedly, **rendering a message no longer acknowledges it.** Mail delivered into an
  agent's context stays outstanding until an explicit `swarm inbox ack`. Agents that never
  ack will accumulate unacked mail and eventually refuse new messages. `swarm inbox read`
  now lists everything unacked, delivered or not.

## One thing product will not write
Nothing above softens the refusal into a queue, a retry, or an exemption. The operator ruled the
refusal is **intended**; `cos`'s self-lockout analysis shows it is **escapable, not a deadlock**;
and the escape is written into the contract so nobody "fixes" it later. If a
future reader thinks the cap is a bug, the paragraph tells them why it is not.

Land 1(a) and 1(b) on PR-1. Land 2(a)/(b) with PR-2, and route 2(c) to release-mgr, who owns
RELEASING.md and the version heading.
