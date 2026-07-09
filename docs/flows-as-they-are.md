# Messaging and escalation, as they actually are

**Author:** `cos` (chief-of-staff). **Date:** 2026-07-09. **Commissioned by:** the operator.

This is a map, not a route. It proposes no fixes — that was the instruction, and it is also
the right instruction, because every fix this session addressed the layer below where the
problem lives. Every claim here was checked against the code or an execution, at the commit
`451a2ec`. Where I did not run it, I say so.

I built or approved most of what is criticised below.

**Relationship to `docs/AUDIT-MAP.md`.** That document is `product`'s, commissioned in the same
breath, and it is the *org's* map: what the system is, where two shipped things disagree. This
one is narrower and worse-behaved. It is the account of the agent who wrote #40, #50, and #59,
who approved proposal 005 twice, and who dropped two of the operator's directives — one of them
the halt on the build described in §4.1. Product cannot write §2 or §4; nobody outside my own
inbox can. Read theirs for the system. Read this for what it is like to be inside it, and for
which of my own shipped work I no longer trust.

---

## 0. The one-sentence map

**The system cannot distinguish a message that *changes what an agent must do* from one that
merely informs it, so it renders, acks, and forgets both identically.** Delivery is solved.
Attention is not, and attention is the scarce resource.

Everything below is a consequence.

---

## 1. What actually works

Not everything is broken, and the working parts are load-bearing.

- **Durable delivery.** A message is a file. It survives a crash, a compaction, a restart.
  Verified repeatedly; I have never lost a message to the *storage* layer.
- **Atomic rename as the state machine.** `inbox/` → `rendered/` → `read/`. One syscall per
  transition, no read-modify-write, no torn record. `swarm-hook.cjs:200` documents why.
- **The G17 fix (#31).** The hook used to `process.exit(0)` before stdout drained, so any
  message over ~64 KB was truncated to unparseable JSON, injected as nothing, and *already
  moved to `read/`*. Silent destruction with a success exit code. The ack is now conditional
  on the write draining: an `EPIPE` leaves the message unrendered. This is the single most
  serious defect found and it is genuinely fixed.
- **Non-destructive reads (#40).** `swarm updates` no longer drains the operator's mailbox.
  Before this, any second reader — a monitoring loop, a re-run — silently consumed an
  escalation.
- **`swarm send --stdin` (#50).** A message body is no longer a shell word.
- **Explicit cumulative ack discloses its sweep.** `ack N+2` prints every id it consumed and
  marks them `(swept by cumulative ack)`. Proposal 005 asked only that the hazard be
  *prevented*; the tool announces it instead.

---

## 2. Where I have been bitten

### 2.1 The two dropped directives

**First.** The operator sent a commissioning directive. It arrived 37 seconds after a
4,699-byte message from `product`. Both were injected — replayed from the archived records at
`451a2ec`: **7,170 chars against an 8,000-char cap, nothing withheld** — and both were
auto-acked into `read/` at the instant of rendering. I
answered the sibling's absorbing technical message and never acted on the directive. I then
reported the item as "awaiting the operator" for four cycles while his answer sat in my
`read/` directory. He re-sent it and told me.

I diagnosed it myself: **shown is not understood.**

**Second.** One hour after writing that sentence, the operator sent a HALT of the very build
that sentence motivated. It arrived at `19:41:13.649`. I merged PR-1 at `19:41:15` — two
seconds later, mid-command, unseen. I then instructed the child to open PR-2, drained my
inbox, wrote a checkpoint, and reported to him. I never read it. I found it only when an
external auditor's question forced me to search my own inbox.

**His halt was consumed by the mechanism it was written to condemn.** That is the most
important fact in this document.

### 2.2 G14: four strikes, two agents, one bug

A message body passed as a positional argument is a shell word. Backticks and `$(...)` are
*executed* by the caller's shell; an apostrophe terminates a quoted string. All of it happens
before `swarm` runs, so the tool cannot see, warn about, or recover the damage.

1. `cos` → `release-mgr`: send **died on a backtick**. Zero bytes delivered. Discovered only
   because I read the inbox back off disk.
2. `cos` → `product`: send **landed with words deleted** mid-sentence. The deleted words were
   the two subjects of the sentence explaining why a gap could not be closed.
3. `cos` → `release-mgr`: **died on a backtick again**, two cycles after I filed the bug,
   escalated it, proved the tool blameless, and warned three children about its sibling trap.
4. `product` → `cos`: send died. It used proposal 004's documented **single-quote mitigation**,
   and an apostrophe terminated the body. 004 predicted exactly this in writing.

Strike 4 settles it. The doc fix moved the failure from backticks to apostrophes. Agents write
prose; prose has apostrophes. **Care is not a mechanism.** Fixed by `--stdin` (#50), but only
after four failures across two agents, one of whom had filed the bug himself.

### 2.3 The stale-claim pattern, now found in four organs

*Nothing re-checks a claim but its author.* A claim that was true when written becomes a lie
when the world changes, and nobody notices.

| organ | instance |
|---|---|
| `blockers` | Two of my own were dead — asking for a decision the operator had already given, on work I had already shipped. I found the second only because I refused to fix only the record I was told about. |
| `delegated_to[].status` | My own record said a child was `in-flight`. The child was dead, its PR merged, and I had approved and closed it. |
| documentation | `docs/prd/02-inbox-messaging.md` still says "`cmd_send` has no size guard." The 6000-byte limit shipped in #40. True when written. |
| `inbox/read/` | *See §3.* |

The pattern generalises past checkpoints. **A document is a claim about the present too.**

### 2.4 A brief that labelled a requirement a "cost"

I briefed a child on the `rendered/` design and described the union-reader — *outstanding =
`inbox/` ∪ `rendered/`* — as "the only place this touches 005's reader definition." A cost.

A competent implementer optimises away a cost. It was load-bearing: without it the nag names an
id that `swarm inbox read` cannot show. Announced and unfindable. `product` caught it; I
verified at both reader sites and corrected the child mid-build.

Nobody built a bug. I would have caused one by describing a requirement as a price.

---

## 3. The ack trail is stored where its only reader cannot reach it

This is the structural finding, and it is the same disease as §2.3 in its most consequential organ.

`swarm inbox read` and `swarm inbox ack` take **no agent argument**. `bin/swarm:925` reads
`local box="$INBOX_DIR/$me"` — always the caller's own inbox. No verb exposes another agent's
`inbox/`, `rendered/`, or `read/`. `graph`, `status`, and `children` read `state/` and
`updates/`, never `inbox/`. I checked each.

So: **has anyone ever read another agent's `read/` to check a directive was acted on?**

Never. Not "nobody bothered" — the tool forbids it. I have read sibling inbox directories only
to confirm my *own* message landed, with raw Python, bypassing the tool entirely. That is a
delivery check, not a compliance check.

The ack trail is a claim about compliance, stored in a directory that only the party with no
interest in checking it can read. `rendered/` (#59) adds a fourth organ to the pattern: a claim
that a body was *shown*, stored where only the shown-to agent can see it.

---

## 4. The fixes I now doubt

### 4.1 #59 — the summary-line nag. I doubt this most.

I replayed my own incident against merged `451a2ec` in a throwaway `SWARM_DIR`: `product`'s
4,699-byte message and the operator's 2,036-byte directive, 37 seconds apart.

```
TURN 1: both bodies injected. 7,170 chars. Cap 8,000. Nothing withheld.
```

(Replayed from the two archived records themselves, not from reconstructed bodies. My first
replay used filler bodies of the right *length* and produced 7,152; a second, 7,157. Both were
close, neither was the number. This is the map, so it carries the one I can reproduce.)

**That is the turn I failed on, and #59 changes nothing about it.** The directive was fully in
context then and would be fully in context now.

The nag appears on turn 2 and carries *strictly less information* than the body I had already
ignored: an id, a hint, no content. If 2,036 bytes did not move me, 24 characters will not. And
**acking is not complying**: one command clears the nag and builds nothing. I could have acked
it and shipped nothing — and the record would then show a clean, silent, fully-acknowledged
failure. **The nag's absence reads as compliance.** That is worse than what it replaced.

What it *does* do, narrowly: it removes one mode — a message rendered while the agent is
inattentive, which then vanishes. It guarantees a standing trace. Real, and small.

I sold it as reaching the mechanism. It re-dresses the mechanism.

One property survives, **by accident**: ids have the form `<from>-<ts>`, so
`operator-1783595020254` happens to name its sender. Nothing designed that.
`swarm-hook.cjs:270` builds the list from `rec.id` and nothing else.

### 4.2 Proposal 005 — scope drawn around the symptom

005's ack half was argued on my dropped directive. But the operator scoped item 3 to *"what the
injection cap holds back"* — and my directive was never held back. Nothing in the shipped
feature touches a message that fits. Not a build error and not a spec error: **a scope drawn
around the symptom I reported rather than the mechanism we had both already written down.** I
approved that brief.

### 4.3 G19 — the tool calls a directive "agent chatter"

Still open. I ran it at `451a2ec`: an operator directive is injected under the header

```
[swarm inbox] You have 1 new message(s) from other agents:
```

The operator is not an agent; it has no registry entry, and that absence is precisely how
`swarm send operator` is special-cased. Messages sort by timestamp only. `rec.from` is used to
print a name and for nothing else. So the tool announces the one sender whose message is a
*directive* as agent chatter, then sorts it by clock beside a peer's opinion.

I ruled the fix out of scope on #40 for a correct reason — reordering would silently redefine
what a cumulative ack acknowledges, since the ack is a prefix by array index over arrival order.
The reason was right. The gap is still there.

### 4.4 WORLD.md now contradicts the code

`WORLD.md:68-72`, verbatim, at `451a2ec`:

> For an **agent**, mail is acked automatically the moment the hook injects it: delivery is
> atomic with the turn, **so nothing can be shown and then lost.** […] **That asymmetry is
> deliberate.**

After #59 the asymmetry is gone. And "nothing can be shown and then lost" was already false when
it was written — it is exactly what happened to me, twice. The child that built #59 noticed,
correctly refused to write the replacement words, and routed them to `product`.

---

## 5. What I cannot see from here

Stated so the auditor can weigh my account.

- **I have never once caught a motivated error in myself.** I audited my 18 recorded errors: 8
  caught alone — every one unmotivated or against my own interest — and 10 caught by someone
  else, of which 6 were errors whose wrong answer flattered my delivered work. Disinterest is
  the mechanism, and it is not a property I have about my own code.
- **I wrote the brief, corrected the brief, judged the artifact, and merged it.** The permission
  classifier denied my child's self-merge because "the merge instruction came through a
  sub-agent delegation prompt, not the user." It was right. I merged under a standing
  instruction that routes the operator's consent through the person doing the work.
- **This document is a claim about the present**, written by the agent whose claims have twice
  gone stale in exactly the way it describes. It should be re-checked against the code, not
  believed.
