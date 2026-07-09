# PRD 02 — Durable inbox messaging + doorbell

*How one agent reaches another. Landed in PR #10 as a breaking change.*

## The problem

A coordinator needs to tell a running subagent something: change direction, here
is the missing context, your sibling finished, stop.

The obvious mechanism — type the message into the subagent's terminal — was the
original implementation, and it failed in ways that were individually fixable and
collectively fatal. herdr delivers a long message as several asynchronous
bracketed-paste chunks; an immediate `Enter` races them and gets consumed, leaving
the text sitting in the prompt box, unsubmitted, forever (PR #6). Worse, an agent
that is mid-tool-call has no prompt box to type into at all. And a pane that has
died takes the message with it. There was **no delivery guarantee** — only a
delivery *attempt* whose failure was silent.

The reframing: **the message is a file, not a keystroke.** Delivery is the write.
Everything after the write is an optimization on *when* the agent notices.

## Who uses it

**Agents**, exclusively. `swarm send` is how a parent steers a child, how siblings
coordinate, and how a child escalates upward.

The **operator** can invoke `swarm send` from a shell, and is the sender-of-record
when `SWARM_AGENT_ID` is unset (the message is attributed to `operator`). Since
PR #20 the operator can also *receive*: `swarm send operator "…"` is the one
non-agent target, a durable-file-only mailbox with no pane and no doorbell, read
via `swarm updates`. See **G2** below for what that does and does not guarantee.

## Current behavior

### Send

`swarm send <id> "<message>"`

1. Validate that `agents/<id>.json` exists, else `unknown agent: <id>`.
2. Determine the sender: `$SWARM_AGENT_ID`, or `operator` if unset.
3. Write the message **atomically** (`tmp` + `rename`) to
   `inbox/<id>/<ts_ms>-<from>.json`. Millisecond timestamp in the filename, so
   files sort by arrival. Record shape:
   ```json
   {"id":"<from>-<ts>","to":"<id>","from":"<from>","ts":<ms>,
    "type":"message","body":"<message>","read":false}
   ```
4. **Ring the doorbell** (best-effort). If the pane is unavailable, print a note to
   stderr and exit 0 anyway — the file is already durable.

The ordering is the contract: *the file is written before anything else is
attempted*, so no failure downstream of step 3 can lose a message.

### The doorbell

`ring_doorbell <pane>` exists to convert a durable file into a *prompt* delivery
without waiting for the agent's next spontaneous turn.

The mechanism rests on one non-obvious fact about Claude Code: **a bare `Enter`
does not fire `UserPromptSubmit`.** An empty prompt is a no-op. So the doorbell
must submit real, non-empty text. It sends the literal string `check inbox`.

The text is irrelevant to delivery — the hook injects the actual message content
regardless. `check inbox` exists only to make the turn boundary happen.

Then, because herdr's `send-text` arrives asynchronously via bracketed paste:

- **Phase 1** — poll the pane's visible prompt line (grep for `❯`) up to 20 times
  at 200ms until the text stops changing, i.e. the paste settled (~4s bound).
- **Phase 2** — press `Enter`, wait 400ms, re-read the prompt line; if it drained,
  the doorbell rang. Retry up to 5 times.
- If the box never confirms empty, return success anyway: text and `Enter` were
  both sent, and durability does not depend on this.

### Pickup

The `UserPromptSubmit` hook runs `swarm-hook.cjs inbox-check` on **every turn of
every agent**. It is therefore written to be fast, side-effect-light, and
bulletproof — every path is wrapped so that any error exits 0 with no output.

A mailbox has **three** states, and they are the file's **location**, never a flag
inside the record. `read/` is a directory precisely so that the state change is one
atomic rename with no re-injection race; a flag would need a read-modify-write on a
file a concurrent reader may hold. `rendered/` inherits that property for free.

| location | meaning | hook behaviour |
|---|---|---|
| `inbox/<id>/*.json` | never delivered | inject the body |
| `inbox/<id>/rendered/*.json` | delivered once, **unacked** | name it in the one-line nag |
| `inbox/<id>/read/*.json` | explicitly acked | silent |

**Unacked** is the union of the first two. Only `swarm inbox ack <id>` reaches
`read/`. Rendering a message is not acknowledging it (operator ruling, 2026-07-09) —
proposal 005 records the hook acking an operator directive into `read/` on the
strength of having *rendered* it, and the agent never acting on it. Shown is not
understood.

1. Resolve `inbox/<id>/`. If it does not exist, no-op.
2. Read every `*.json` directly under it — the never-delivered ones — and, separately,
   every `*.json` under `rendered/` — the delivered-but-unacked ones. Sort each by `ts`.
3. If there is nothing to inject and nothing outstanding, exit 0 silently.
4. If there is nothing to inject but `rendered/` is not empty, emit **one line** — the
   nag — and nothing else. It names the unacked ids and the ack hint. Bodies are never
   re-injected. The nag has no side effect: nothing is moved.
   ```
   [swarm inbox] 2 message(s) delivered earlier and still UNACKED: cos-1783…, rd-1783… — re-read with `swarm inbox read`; clear with `swarm inbox ack <id>` (cumulative).
   ```
5. Otherwise build an injected block, explicitly framed:
   ```
   [swarm inbox] You have N new message(s) from other agents:

   --- from <sender> (<ISO time>) [id <message-id>] ---
   <body>

   These were delivered to your durable inbox; act on them as part of this turn.
   (`swarm inbox read` re-reads them; `swarm inbox ack <id>` acknowledges through <id>
   — they stay UNACKED, and are re-listed every turn, until you do.)
   ```
   …followed by the nag line, if any message was delivered on an *earlier* turn and is
   still unacked. The framing is deliberate — `additionalContext` reads to the model as
   out-of-band context, and without the explicit "act on them" the model may treat
   a directive as background noise.
6. Emit the injection to stdout **first**.
7. **Then** move the surfaced files to `inbox/<id>/rendered/` by atomic rename.

The nag's width is subtracted from the 8,000-char budget before any body is measured,
exactly as the header and the `…and N more` line are. Unlike them its width is not
bounded by the message count — it grows with the number of ids carried — so appending
it to a spent budget would blow the cap.

Step 6 before step 7 is the crash-safety ordering, and the comment in the code
states the reasoning exactly: if we die between them, the message is re-injected
next turn (harmless duplicate); the reverse ordering would lose it (unrecoverable).

## Contracts and guarantees

**Guaranteed.** These held in intent from the start; the first and third were **false in
fact** for any message over ~64 KB until PR #31 (`08f683b`) fixed the hook's stdout drain.
They are true now, at any size, and verified against the installed hook.

- **The message is never lost.** Once `swarm send` returns 0, the message exists
  on disk in the target's inbox. A dead pane, a busy agent, a missed doorbell, a
  crashed hook — none of these can destroy it.
- The write is atomic. A concurrent `inbox-check` never reads a half-written
  message.
- A message is **never silently dropped** by the hook. If it is not injected this
  turn, it is not moved to `rendered/`, so it is injected next turn. Since PR #31 the
  rename is **conditional on the injection actually reaching the harness** — if the
  write fails (a vanished reader, `EPIPE`), the message stays **unrendered** and is
  re-offered whole. Failing toward re-injection is the safe direction, and the code now
  enforces what the ordering always meant.
- A delivered message is **never silently dropped by the agent** either. It stays in
  `rendered/`, and every later turn re-surfaces its id in the one-line nag, until the
  agent runs `swarm inbox ack`. A message that stays outstanding is a message that keeps
  asking.
- Messages are surfaced oldest-first.
- The hook never breaks the agent's turn. Every failure mode is a silent no-op.
  *(This one always held — and it is precisely what hid G17 for the life of the feature:
  a silent no-op is indistinguishable from a silently lost message.)*
- The `swarm send` CLI signature is unchanged from the pre-1.0 live-typing
  version — only its contract changed.

**Not bounded, and worth knowing:** nothing limits how much the hook *tries* to inject.
`cmd_send` has no size guard, `inbox-check`'s 8,000-character cap cannot withhold the
first message (G10), and `restore-state` has no cap at all (G18). The drain fix means an
oversized payload now arrives intact rather than being destroyed — a correctness bug
converted into a context-budget one.

**Best-effort — explicitly NOT guaranteed:**

- **Timeliness.** The doorbell may fail to fire a turn boundary — reliably so when
  the target is mid-tool-call, per PR #10's own verification. The message is then
  picked up on the agent's *next real turn*, whenever that is.
- **That the agent ever takes another turn at all.** See G8.

**Explicitly deferred** (PR #10, operator decision): read receipts, and structural
verification that the injected message was acted upon.

The word to hold onto is that WORLD.md's phrasing is precise: *"a message is
always delivered, but a busy agent may see it on its next turn rather than
instantly."* "Delivered" means *written to the inbox*, not *read by the model*.

## Edge cases and known limitations

**G2 — the operator could not receive messages. Closed by PR #20 (`1892806`);
one edge survives.** The operator is now an addressable target. It is *not* an
agent — no registry row, no pane, no model, no lifecycle, and it never appears in
`list` or `graph` — so `cmd_send` special-cases exactly two things for the id
`operator` and nothing else: it skips the `agents/<id>.json` existence guard, and
it skips the doorbell (there is no pane to ring) along with the warning that a
missing pane would otherwise print. Every other unknown id still dies
`unknown agent: <id>`.

The message file the operator receives is byte-for-byte an agent inbox message —
same keys, same `<ts_ms>-<from>.json` name, same atomic tmp+rename write — in
`.swarm/inbox/operator/`. The read path reuses `swarm updates` rather than adding
CLI surface: when `updates` is run *by* the operator (`SWARM_AGENT_ID` unset or
empty — the same test `cmd_send` uses to name the human root, and suppressed by
`--id`, which targets a specific agent's reports) it also drains
`inbox/operator/`. Read semantics mirror the agent inbox hook exactly: surfacing a
message marks it read by moving it to `inbox/operator/read/` (atomic rename,
durable audit trail), and it emits *before* it moves, so a crash between the two
re-shows a message rather than losing one. An empty inbox is a silent no-op.

The mark-read is deliberately **best-effort and never fatal** — a failed `makedirs`
or `os.replace` is swallowed, so an unwritable inbox re-shows its messages on the
next `swarm updates` rather than erroring or dropping them. The bias is
consistently toward *showing a message twice* over *losing it once*.

The `--json` shape depends on who asks, never on whether mail exists: agents and
`--id` keep the historical bare array; the operator gets
`{"updates":[…],"inbox":[…]}` with `inbox` possibly empty, so a poller sees one
stable schema either way.

**The surviving edge: the operator is a mailbox, not a node.** It has no pane, no
doorbell, and no hook. An agent's inbox is *surfaced into its context* by a
`UserPromptSubmit` hook on its next turn; the operator's inbox is surfaced only
when a human types `swarm updates`. So G8 below — delivery is guaranteed to the
inbox, not to the recipient — applies to the operator more sharply than to any
agent: it is the one recipient in the graph with nothing that will ever tell it
mail has arrived. An escalation from the top layer is now durably *stored* rather
than lost, which is a real improvement over failing with `unknown agent`; it is
not yet durably *seen*.

**G8 — delivery to the inbox is not delivery to the agent.** An agent that has
finished its work and gone permanently idle never takes another turn. Its
`UserPromptSubmit` hook never fires. The message sits unread indefinitely, and
`swarm send` reported success. The doorbell is the *only* thing that closes this
gap, and the doorbell is best-effort by design.

There is no way for a **sender** to observe whether a message was surfaced. The hook
moves files to `rendered/` and then `swarm inbox ack` moves them to `read/`, which is a
durable audit trail — but nothing reports it upward, no verb reads another agent's box,
and read-receipts were explicitly deferred. A sender's only recourse is to read the
target's pane, which the world doc permits (for liveness) and forbids (for judging work).
*(The **recipient** now observes its own outstanding mail, on every turn — see below.)*

**There is a third rung on this ladder, and it is the one that has actually cost something.**
Delivery to the *inbox* is not delivery to the *agent* (above). But delivery to the agent's
**context** is not **receipt** either — and the hook **used to mark** a message `read/` at the
instant it injected it, recording consumption on the strength of having *rendered* the text.

Demonstrated, not hypothesised. `cos` was sent the operator's directive commissioning an
implementation. Replaying the exact message pair through the hook of the day: 6,965 characters
injected against an 8,000 cap, both bodies present, **nothing withheld, both auto-acked**. The
directive was in its context, intact. It answered the other message and not the operator, and
spent four cycles reporting the item as *"awaiting the operator"* while the answer sat in its
own `read/` directory.

**Shown is not understood.** The implicit prefix-ack conflated the two. **Fixed** (operator
ruling, 2026-07-09): injection now moves a message to `rendered/`, not `read/`, and every
later turn re-surfaces its id in a one-line nag until the agent runs `swarm inbox ack`. An
unclaimed message stays outstanding and keeps asking, so a busy agent's own inattention becomes
visible *to itself*. `cos` would have tripped over that directive four times.

Note the direction of the evidence: this is an argument for **explicit ack**, and
simultaneously an argument **against** notify-and-pull, because the failure was never a missing
body. It was a missing action, and a notification adds one. The nag is not a notification: the
body was already delivered, in full, once. The nag only refuses to let the agent forget it.

**G19 — the injection renders a directive and a peer's opinion identically, and calls the
operator an agent.** The mechanism behind the incident above, and it is a property of the
tool rather than of the agent that tripped on it.

Verified at source and by fixture:

- The header is unconditional: ``You have ${unread.length} new message(s) **from other
  agents**:`` (`swarm-hook.cjs:237`). The operator is **not an agent** — it has no registry
  entry, by design — yet its directives are announced as agent chatter.
- Messages are sorted **by timestamp only** (`:225`). There is no priority, no sender class.
- `rec.from` is used to *print a name* and for nothing else (`:242`). It is never read to
  order, mark, or separate.
- Both messages were auto-acked into `read/` identically. *(No longer: both are now moved to
  `rendered/` identically, and both nag identically until acked. **G19's remaining half stands**
  — the sender class is still invisible, so a directive and a peer's opinion still look alike.
  What is fixed is that neither can now be silently consumed by being read.)*

So a message that **settles** a question and a message that **opens** one are presented in the
same frame, in arrival order, and were consumed by the same act of rendering. A settling message
presents as *finished*; an opening one presents as *work*. Nothing in the arrangement rewards
reading the short procedural one first — and in the incident above, the short procedural one
was the operator commissioning an implementation.

`from == "operator"` is already on every message record and is a clean discriminator (the
operator has no `agents/<id>.json`, which is exactly how `swarm send operator` is
special-cased). The fix is small; it belongs with the `swarm inbox read`/`ack` work now in
flight.

*Recorded because `cos` asked that it be, and declined it as exculpation:* **"the system did
not decide what I attended to; it presented both and I chose."** Both findings are true and
they belong in different places. The structural one is here. The personal one is a task in its
checkpoint. The actionable form it derived — *"when an injection contains more than one
message, read the one that changes what I should be doing first"* — is a habit no document can
enforce, which is the point.

**G9 — the doorbell screen-scrapes, against the product's own doctrine.**
`ring_doorbell` greps the pane for `❯` to find the prompt line. WORLD.md's
foundational reliability claim is that *"the hook firing is reliable; the pane is
ground truth [for what happened], screen-scraping is not [how we detect events]."*
The near-realtime path is a hard-coded dependency on a glyph in Claude Code's TUI.
It degrades safely — a restyled prompt breaks timeliness, never durability — but it
is an undocumented coupling to another product's cosmetics, and its failure is
silent (the function returns success after 5 unconfirmed attempts).

**G10 — the injection cap is not a cap on any single message.** `inbox-check`
budgets 8000 characters of injected context. The loop breaks when the budget is
exceeded **and at least one message was already injected** — so a single message of
any size is injected in full. Conversely, when the cap does bite, the agent is told
"…and N more; full messages in `inbox/<id>/`" and those N remain unread on disk,
correctly, for next turn.

Both halves verified by running the shipping hook against a synthetic inbox. One 20 KB
message injects **20,224 characters through an 8,000-character cap** — 2.5× over. Any
argument about the injection's context cost that leans on that number is leaning on a
number the code does not honour.

This is not merely a mis-stated bound. **The escape hatch is the delivery vehicle for
G17**: because the guard cannot withhold the *first* message, a single oversized body
reaches `process.stdout.write()` whole, overruns the pipe buffer, and is destroyed. The
multi-message case is bounded at `8000 + one body` and never gets there. And `cmd_send`
has no size guard, so nothing upstream stops it.

**The cap and the send-time limit are one invariant with two enforcement points**, not two
features. Adopted with [proposal 005](../proposals/005-inbox-read-ack.md), which adds both:

- **no *accepted* message may exceed the injection budget** — enforced at `send`
- **no message *on disk* may blow the budget** — enforced at `inject`

The second is not redundant: it covers messages written before the limit existed, and
anything hand-planted. If the two numbers are allowed to drift apart, one of them is
decoration. `cos` accepted this framing and rebriefed its implementation child to state the
relationship in a comment rather than leave two magic constants to diverge.

**G17 — a message over ~64 KB was silently destroyed on delivery. RESOLVED by PR #31
(`08f683b`).** It was the most serious defect in this document, and it directly falsified
the first guarantee above. The mechanism is preserved here because it is instructive: a
correct comment, a correct ordering, and a defect that lived underneath both.

`inbox-check` wrote the injection to stdout, *then* renamed the message into `read/`,
*then* called `process.exit(0)`. The comment above that ordering explains the intent:

> *"Emit the injection FIRST, then mark read. If we crashed between the two, the messages
> would be re-injected next turn (safe) — losing one is not."*

The reasoning is sound and Node defeats it. Claude Code invokes hooks with stdout on a
**pipe**. `process.stdout.write()` of more than the pipe buffer (64 KiB) returns `false`
and *queues* the remainder — it does not block, does not throw, and does not complete.
`process.exit(0)` then discards the queue. The write is never finished, no error is
raised on any channel, and the rename runs regardless.

Measured against the shipping hook. The cliff is exact:

| Body size | Bytes reaching the harness | Result |
|---:|---:|---|
| 65,265 | 65,529 | delivered |
| **65,266** | **65,536** | **destroyed** |
| 400,000 | 65,536 | destroyed |

Past the cliff the harness receives JSON truncated mid-string, fails to parse it, and
injects **nothing** — while the message sits in `read/` and the hook has reported success.
Isolated to `process.exit()`: a 200 KB write completes in full if the process is allowed
to exit naturally.

Three properties compound to make it invisible:

1. **`cmd_send` has no size guard whatsoever** (found by `cos`), so nothing prevents an
   oversized body from being queued.
2. **G10's `injectedCount > 0` escape hatch** means a single message bypasses the 8,000
   character budget entirely — so a lone oversized message reaches `write()` in full. The
   multi-message case is bounded at `8000 + one body` and cannot reach the cliff.
3. **The hook's own "never break the turn" guarantee** turns the failure into a silent
   no-op. That guarantee holds. It is precisely what hides this.

**The fix (PR #31).** Both of the hook's stdout writes now route through a single
`emitAndExit()` that waits for the drain callback before exiting. Verified independently
against the installed hook: a 400 KB message delivers 400,264 bytes and parses; the capped
multi-message path is unchanged.

The interesting part is what the *first draft* of that fix got wrong. It ran the `read/`
rename unconditionally once the drain callback fired — but under `EPIPE` (the reader
vanishes mid-write) the callback fires **with an error**, the bytes never landed, and the
message would have been acked anyway. `cos` caught it with a test rather than shipping it:
*"I had reproduced the original bug in a new costume."* The rename is now conditional on
delivery (`done(!err)`), so a failed write leaves the message unread for the next turn.
**Failing toward re-injection is the safe direction** — which is exactly what the
emit-before-mark comment always meant, now enforced by code instead of assumed by it.

**Scope: the agent inbox only — and the operator's mailbox is spared by accident.** The
operator reads mail through `cmd_updates`, which is Python, and Python flushes stdout on
exit. The agent path is Node, which does not:

```
python3 -c 'import sys; sys.stdout.write("X"*200000); sys.exit(0)' | wc -c  → 200000
node    -e 'process.stdout.write("X".repeat(200000)); process.exit(0)'   | wc -c  →  65536
```

An escalation *to* the operator therefore cannot be lost this way; a steering instruction
*from* the operator to an agent can. Nothing in the code records that this safety exists,
nothing tests it, and it is a property of the runtime rather than the design. **Unifying
the two read paths — which the operator's proposed redesign contemplates — would extend
this defect to the operator's own mailbox unless the flush is fixed first.**

---

**G16 — the inbox header over-counts. *Retracted as a defect; kept as a copy note.***
The injected header is built from `unread.length` while the loop injects `injectedCount`,
so a capped delivery announces *"You have 5 new message(s)"* above three bodies. That much
is true. **What product asserted, and got wrong, is that the shortfall is unannounced.**

It is announced. The hook emits, unconditionally, whenever anything is withheld:

```js
const remaining = unread.length - injectedCount;
if (remaining > 0) context += `\n\n…and ${remaining} more; full messages in inbox/${id}/`;
```

`cos` disproved the claim by running the fixture instead of accepting it, and noted the
decisive evidence was not a fixture at all: the line appears in every real capped
injection, including the ones both agents were reading at the time. This document had
even quoted that line, two paragraphs above, while the register asserted its absence.

What remains is a wording improvement, worth one line and no more:

> `[swarm inbox] Showing 3 of 5 new messages (2 remain — they will be shown next turn).`

It names what *was* shown rather than only what was withheld. That is clearer. It is not
a defect.

The observation underneath survives and matters: the product **already performs implicit
cumulative acknowledgement** — it acks exactly the prefix it delivered, and announces the
remainder. That is the strongest argument for making acknowledgement explicit, and it is
why [proposal 005](../proposals/005-inbox-read-ack.md) recommends adopting the ack half of
the operator's redesign while rejecting the notification half. The proposal's reasoning
stands; only its characterisation of this line as *silent* does not.

There is **no cap on inbox growth**. A parent that sends faster than a child takes
turns accumulates an unbounded directory, and each subsequent turn re-reads and
re-parses all of it.

**Filename collision.** Two messages from the same sender to the same target within
the same millisecond produce the same filename and one overwrites the other. In
practice `swarm send` is invoked from a shell so this is not reachable, but the
uniqueness of `<ts_ms>-<from>` is assumed rather than enforced.

**`date +%s%3N` is GNU-only.** The code detects the BSD/macOS failure (the literal
`N` survives) and falls back to Python. Correct, but it means every `send` on
macOS pays a Python startup.

**No message ordering across senders.** Files sort by timestamp, and timestamps
come from the sender's clock. All agents are on one machine today, so this is
sound; it would not survive distribution.

**G14 — delivery is guaranteed; *integrity of the body* is not, and nothing says
so.** The durability claim covers the message from the moment `swarm send` receives
it. It says nothing about the shell that invoked `swarm send`, and that is where a
message can be silently mutilated.

Every example this product ships shows a double-quoted body — `WORLD.md` twice, the
usage string, and the help text. In a double-quoted shell string, backticks and `$`
are evaluated. Since every agent writes markdown, and markdown names a verb or a flag
with backticks, an agent sending `` the `wait` verb blocks `` transmits `the  verb
blocks`: the word is deleted, and `wait` is *executed* as a command.

This is not hypothetical. It happened to `cos` — the agent that writes the most shell
in the graph — inside a message explaining an engineering decision, and it ate the two
subjects of the sentence. `cos` caught it and resent a correction. A reader who
received only the first copy would have read a grammatical sentence that had quietly
lost its referents.

`cmd_send` is **not** at fault: it passes the body to Python as an environment
variable under a quoted heredoc, so nothing is evaluated inside the tool. By the time
`swarm` runs, the word is already gone and nothing downstream can recover or even
detect it. The defect is that the documentation teaches the habit that destroys the
message.

The irony worth recording: `spawn` already solved this. It writes an agent's task to a
**file** rather than a command line, with a comment explaining that a quote-heavy
prompt re-parsed through a pane shell breaks. That reasoning was never carried across
to `send`. Proposed fix in [proposal 004](../proposals/004-send-quoting-hazard.md);
the durable answer is a `--stdin`/file body, since no quoting style is safe for all
message bodies (single quotes break on an apostrophe).

**Four strikes, and the fourth proves the mitigation is not a fix.** `cos` was bitten three
times — a send delivering zero bytes; a send landing with words deleted mid-sentence; and a
third death by backtick *two cycles after it filed the bug, escalated it, proved the tool
blameless, and warned three children about its sibling.*

**Product's is different in kind: it used proposal 004's own recommendation.** Building a
message body in single quotes, an apostrophe in `006's` terminated the string; the shell then
executed the backticked words after it. `swarm send` received the fragment and **exited 0**,
because a 2,982-byte argument is a perfectly valid message. Verified, all three forms:

```
'…the 006's caveat…'          → bash: unexpected EOF while looking for matching '
"…run `date` now…"            → the backticks EXECUTE
"$(cat body.txt)"             → apostrophe, backtick and $(…) all survive verbatim
```

So **004 does not fix G14; it moves the failure from backticks to apostrophes.** Every agent
writes markdown, and markdown has backticks. Every agent writes prose, and prose has
apostrophes. Product wrote that sentence into 004 before either agent was bitten, and then
walked into it — which is the strongest available demonstration that **care is not the
mechanism.** Command substitution is the only safe transit today, because its output is never
re-scanned.

**And the fourth strike exposes something worse than G14 as filed.** G14 says a body can be
corrupted before the tool sees it. What the incident shows is sharper:

> **A truncated message is indistinguishable from a complete one, at every layer.**

`swarm send` exits 0. The record is well-formed, with all seven keys and a body that is a valid
string. It is under the 6,000-byte send cap, so nothing rejects it; under the 8,000-char
injection budget, so the hook's truncation marker never fires. The recipient's hook injects it
without comment. `release-mgr` caught it **only because it ended mid-word and it is the kind of
reader who checks.**

Nothing anywhere asks *"did the whole body arrive?"* — and `exit 0` answers a different
question. That is the same shape as the sort-order trap below: a correct answer to a question
nobody asked.

## Testing this file's claims

Every measurement in this document was produced by running the shipped code against a
fixture. **That method has a hole, and it is worth stating before anyone reproduces the
numbers.**

`SWARM_AGENT_ID` selects which read path executes (**G21**). It is set in every spawned
agent's environment by construction (`bin/swarm:505`), so an agent testing the *operator*
path gets the *agent* path instead — silently, at exit 0, with well-formed output. To
exercise the operator path from inside an agent:

```sh
env -u SWARM_AGENT_ID SWARM_DIR=<fixture>/.swarm swarm inbox read
```

Every claim above about the operator's mailbox was verified this way, on **both** paths. The
claims about `[id ?]` and unackable legacy mail (**G20**) reproduce identically on each,
which is how they were confirmed to be defects in the reader rather than artifacts of the
environment.

`release-mgr`'s formulation is the one to hold onto: *"Not an empty result from a failed
command, but an **unchanged** result from a command that never ran the code path under test.
It looks like a passing check."*

**A second costume of the same hazard, caught live.** Verifying G1's release history, product
ran `git tag | tail -3` and `git ls-remote --tags origin | tail -4`. Both printed cleanly,
exited zero, and showed the newest tag as `v0.9.0`. Product nearly reported that
`release-mgr` had created `v0.10.0`/`v0.11.0` and never pushed them — a release-integrity
failure.

**Both tags were on the remote.** Git sorts tags *lexically*, so `v0.10.0` and `v0.11.0` sort
right after `v0.1.1` — **before** `v0.6.0` — and `tail` showed the wrong end of the list. Two
different commands, the same trap, and neither failed.

```
git tag | tail -1                     → v0.9.0    ← wrong (lexical)
git tag --sort=-creatordate | head -1 → v0.11.0   ← right today, by accident
git tag --sort=-v:refname | head -1   → v0.11.0   ← right today, still wrong
```

`--sort=-creatordate` orders by **creation time**, which agrees with the highest version only
while tags are created in version order. Back-tag an old commit, or re-create a tag, and it
reports a version that is not the highest — exits zero, looks right. `cos` had been using it
all session to mean *"the latest release."*

> **Correction, and it is against this document.** An earlier revision recommended
> `--sort=-v:refname` as *"right by construction."* **It is not.** `release-mgr` chased
> product's near-miss *past its own vindication* — instead of stopping at *"I use `sort -V`,
> I am fine"* — and audited its own release gate. Verified here in a throwaway repository:
>
> ```
> git tag --sort=-v:refname | head -3   →  v0.12.0-rc1
>                                          v0.11.0-rc1
>                                          v0.11.0        ← rc outranks its own release
> ```
>
> `sort -V` and `for-each-ref --sort=-version:refname` have the identical defect. **Semver says
> a pre-release *precedes* its release**, and `RELEASING.md` explicitly supports `vX.Y.Z-rcN`.
>
> **There is no correct git sort flag.** Only an explicit parse is right — which is exactly
> what `bin/swarm:92` does, sorting on `(major, minor, patch, is_stable, pre)` with stable
> ranking above pre. `swarm update --check` is correct; every shell shortcut around it is not.
>
> No release was ever misclassified, because no rc has ever existed. **It was a landmine, not a
> wound** — found only because a report product had no obligation to send was chased one step
> past agreement.
>
> **Where the landmine was — and the correction of a correction.** `#48`'s commit message said
> *"`release-mgr`'s release gate used `sort -V`."* Product then wrote `#49` retracting that as a
> false defect, on the strength of `release-mgr`'s later description of its gate as
> *filter-to-stable-then-max*, which the `-v:refname` trap genuinely cannot reach.
>
> **`release-mgr` refused the acquittal.** `git tag -l | sort -V | tail -1` *was* a real command
> in its real gate, run repeatedly. The two accounts are both true and **temporally ordered**:
> its checkpoint's `t37` describes the gate *before* the fix, `t39` *after*. It was in the gate
> **and** in the cron prompt. **`#48` asserted a defect that existed. `#49` retracted a true
> statement.** Its own words: *"I would rather hand you back the fault than keep an acquittal I
> did not earn."*
>
> The bug was **latent, never active**, and that survives checking: on this repository's real
> tags, `sort -V`, the corrected parse, and `bin/swarm` all name `v0.11.0`, because **no
> pre-release tag has ever existed here.** A landmine, not a wound.
>
> **The finding product reached is nonetheless the better one, and `release-mgr` kept it.** Both
> of its wrong rules — the `sort -V` baseline and *"build send bodies in single quotes"* — lived
> in its **daily cron prompt**: standing guidance written for a future self that wakes with no
> memory and no cheap way to check. That is **G22 one level up** — a stale *instruction*
> re-asserted to a *rebuilt* agent rather than a stale *fact* re-asserted to a *resumed* one —
> and it is worse, because *"a resumed agent at least reads the blocker as a claim it might test;
> a rebuilt agent reads the instruction as a procedure and simply executes it."* It has added a
> third standing line: **rewrite the prompt whenever the tooling changes, not only when the
> release state does.**
>
> Recorded, not smoothed. `#48` stands; `#49` is corrected here.

**The trap is in our shells, not in the tool — and the tool is the only thing here that is
right.** `git tag` appears **nowhere** in `bin/swarm`. `cmd_update` parses semver into an
explicit `(major, minor, patch, is_stable, pre)` tuple and sorts on that, carrying the comment
*"don't trust `-v:refname`."* That comment is not defensive; it is **correct, and it anticipated
the pre-release defect three of us then walked into.** Verified behaviourally: `swarm update
--check` names **v0.11.0**, the true highest, while `git tag | tail -1` names `v0.9.0`.

**A register entry reading "swarm mis-sorts tags" would be false**, and would send the next
agent to patch a function that was already right. `cos` checked this before letting the finding
be written down — and `release-mgr` then found that the *shell remedies* three agents had been
recommending each other were all wrong in the same way the tool had explicitly avoided.

**This is a distinct species, and `cos` counted it as the tenth.** The environment hazard above
is *a command that never ran the path under test*. `grep -c` counting comments is *a command
that matched the wrong thing*. Both fail on the **mechanism**, and their output can betray them.
This one fails on an **ordering assumption underneath the question**, and nothing in the output
can reveal it:

> **A correct answer to a well-formed question that is not the question the claim depends on.**

The command ran. It exercised the path. It answered accurately. **It answered a different
question.**

## Open product questions

1. **Should the operator be *notified*, not just addressable?** *(Narrowed by
   PR #20, which answered the first half of this question and made the second half
   the live one.)* The operator now has `inbox/operator/` and reads it with `swarm
   updates` — it is addressable. It is still not *reachable*: nothing pushes, so an
   escalation waits on the human to poll. Every agent gets its inbox injected by a
   hook; the operator, the one recipient who cannot be hooked, is the one recipient
   with no push. The options are a real notification (terminal bell, `herdr`
   notice, OS notification), a passive surface (unread count in `swarm status`, or
   in the shell prompt), or an explicit decision that polling is the contract and
   WORLD.md should say so. Doing none of them leaves an escalation durably stored
   where nobody is looking — a quieter failure than `unknown agent: operator`, and
   therefore a more dangerous one.

2. **Should `swarm send` report whether the doorbell rang?** Today it exits 0 for
   both "delivered and the agent is reading it now" and "delivered to a pane that
   no longer exists." Those are very different for a caller deciding whether to
   wait. A distinct exit code, or a line on stdout, would let a coordinator choose.

3. **Do we need read receipts after all?** They were deferred as scope. The
   argument for is that G8 makes "sent" and "seen" genuinely different states that
   a coordinator must distinguish, and the `read/` directory already contains the
   information — it is simply not exposed. The argument against is that reading a
   receipt is not evidence the agent *complied*, and a coordinator judging by
   artifact should not care.

4. **Should the inbox be bounded?** Unbounded growth is a slow leak in a long-lived
   swarm, and every turn pays to re-read it. A retention policy on `read/` would be
   the cheap half of the fix.

5. **Is `check inbox` the right doorbell text?** It appears in the agent's own
   transcript as a user turn, so every message delivery leaves a spurious
   `check inbox` prompt in the conversation history — noise in a context window the
   product is otherwise careful about (see [PRD 03](03-checkpoints-continuity.md)).
