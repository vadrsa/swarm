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

1. Resolve `inbox/<id>/`. If it does not exist, no-op.
2. Read every `*.json` directly under it (files in `read/` are already delivered).
3. Sort by `ts` ascending.
4. Build an injected block, explicitly framed:
   ```
   [swarm inbox] You have N new message(s) from other agents:

   --- from <sender> (<ISO time>) ---
   <body>

   These were delivered to your durable inbox; act on them as part of this turn.
   ```
   The framing is deliberate — `additionalContext` reads to the model as
   out-of-band context, and without the explicit "act on them" the model may treat
   a directive as background noise.
5. Emit the injection to stdout **first**.
6. **Then** move the surfaced files to `inbox/<id>/read/` by atomic rename.

Step 5 before step 6 is the crash-safety ordering, and the comment in the code
states the reasoning exactly: if we die between them, the message is re-injected
next turn (harmless duplicate); the reverse ordering would lose it (unrecoverable).

## Contracts and guarantees

**Guaranteed:**

- **The message is never lost.** Once `swarm send` returns 0, the message exists
  on disk in the target's inbox. A dead pane, a busy agent, a missed doorbell, a
  crashed hook — none of these can destroy it.
- The write is atomic. A concurrent `inbox-check` never reads a half-written
  message.
- A message is **never silently dropped** by the hook. If it is not injected this
  turn, it is not moved to `read/`, so it is injected next turn.
- Messages are surfaced oldest-first.
- The hook never breaks the agent's turn. Every failure mode is a silent no-op.
- The `swarm send` CLI signature is unchanged from the pre-1.0 live-typing
  version — only its contract changed.

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

There is no way for a sender to observe whether a message was surfaced. The hook
moves files to `read/`, which is a durable audit trail — but nothing reports it
upward, no verb reads it, and read-receipts were explicitly deferred. A sender's
only recourse is to read the target's pane, which the world doc permits (for
liveness) and forbids (for judging work).

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
