---
name: swarm-middleware
description: "Author a swarm send middleware — an interceptor that runs on EVERY swarm send, before the message is queued, and decides per message whether to pass it, own it, or forward it. Use when the user wants to write a swarm middleware, intercept swarm messages, filter operator mail, auto-ack or route swarm sends, or build a swarm send hook (triggers: 'write a swarm middleware', 'intercept swarm messages', 'filter operator mail', 'swarm send hook', 'auto-ack swarm reports')."
---

# Swarm send middleware

The user wants an interceptor on `swarm send`. A **middleware** is a single
command, named in `.swarm/config`, that `swarm send` runs on **every** message
— all recipients, before the queue write — and that decides, per message, what
happens next. The tool carries no policy: it does not know or care what your
middleware does. Your middleware is the whole policy.

This is producer-side interception. When a middleware is configured, a message
does not exist in any queue until the middleware lets it through. Admission is
a code fact, not a tendency.

## What a middleware is (and is not)

- It runs on **EVERY send**, to every recipient — not just operator-bound mail.
  If you only care about operator mail, that filtering is **your** job: read
  `to` from the envelope and pass everything else through. The tool will not do
  it for you.
- It runs **in the sender's process, before the queue write**, with the full
  envelope on stdin. The message the sender tried to send is what you receive.
- It runs as its **own configured identity**, with the `swarm` CLI available.
  So it can act: to answer, drop, or forward, it calls `swarm send` itself —
  and those sends are attributed to the middleware, not to the original sender.
- It is **one** middleware. A chain belongs inside your middleware (call the
  next stage yourself), not in the tool — there is a single `[middleware]`
  section, no more.

## The contract: three exit codes

Your middleware reads the envelope on stdin and exits. The exit code is the
entire verdict:

| exit code | meaning | what the tool does |
|---|---|---|
| **`0`** | **PASS** — deliver this message | queues it for the recipient, unchanged |
| **`100`** | **HANDLED** — I own this message | queues **nothing**; you dealt with it |
| **anything else** (nonzero ≠ 100), **timeout**, **killed**, or **not configured** | **FAIL-OPEN** | queues it unchanged |

Read the table as one rule: **everything except a clean `exit 100` delivers the
message.** `exit 0` is the common pass. Only a deliberate `exit 100` withholds.

The reason for that shape is the **safety property: a broken middleware degrades
to no middleware.** A crash, a `set -e` trip, a command-not-found, an unhandled
exception, a timeout — every one of those is "anything else", so every one of
them **fails open** and the message is delivered as if you had no middleware at
all. `100` sits deliberately above the shell's reserved codes (126–128, 130)
and the ordinary error codes (1–2), so an *incidental* failure can never be
misread as a deliberate HANDLED. You have to mean it to withhold a message.

The corollary, and the one pitfall that will bite you: **on the pass path you
must `exit 0`.** If your pass path falls through to any stray nonzero exit, the
message is still delivered (fail-open protects you) — but if your *handled*
path forgets to `exit 100` and exits 0 instead, the message is delivered when
you meant to withhold it. Be explicit about both terminal codes.

## The envelope on stdin

One JSON object, the full message the sender tried to send:

```json
{ "from": "scout-3", "to": "operator", "ts": 1752230400000, "body": "…report…" }
```

Parse it once at the top:

```python
import sys, json
env = json.load(sys.stdin)
frm, to, body = env["from"], env["to"], env["body"]
```

`ts` is epoch milliseconds. `to` is the recipient name (or the literal
`operator`). `from` is the sender's wire name.

## Acting on your own: HANDLED means you did something

`exit 100` says "I own this — queue nothing." Owning it usually means you
*replied to* or *forwarded* the message first, then withheld the original. You
do that with `swarm send`, and because your middleware runs as its configured
`identity`, those sends are attributed to the middleware and **bypass
re-interception** (the recursion guard: a send whose sender is the middleware's
own identity is not intercepted again — no infinite loop).

So a HANDLED path is: send, then exit 100.

```python
import subprocess
subprocess.run(["swarm", "send", frm, "ack: your report was auto-acknowledged"])
sys.exit(100)   # owned — the original is NOT queued
```

## Configuration: the `[middleware]` block

In `.swarm/config` (TOML, world-readable — the same file the rest of swarm
reads):

```toml
[middleware]
command  = "python3 /abs/path/to/mw.py"   # required; a resolvable command
                                          # string, args allowed
identity = "middleware"                   # optional; the SWARM_AGENT_ID your
                                          # middleware runs as; default "middleware"
timeout  = 60                             # optional; seconds. A slow middleware
                                          # fails open when it blows this budget
```

Only `command` is required. No `[middleware]` section, no `command` key, or an
unreadable file means **no middleware** — `swarm send` behaves exactly as it
does today. When your middleware runs, the tool injects `SWARM_AGENT_ID=<identity>`
and `SWARM_DIR` into its environment, so the `swarm` CLI it calls resolves the
same swarm and attributes its sends to the middleware identity.

Point `command` at an absolute path. It is the sender's process that runs it,
from whatever directory the sender happens to be in.

## A complete, runnable middleware

A small real one: **auto-acknowledge routine reports bound for a given
recipient, and pass everything else through.** It shows all three exit paths —
PASS (`exit 0`), HANDLED-after-replying (`exit 100`), and fail-open (a raised
exception the tool reads as "anything else"). stdlib only.

```python
#!/usr/bin/env python3
"""swarm send middleware: auto-ack routine reports to the operator, pass the rest.

Wire it in .swarm/config:

    [middleware]
    command  = "python3 /abs/path/to/auto_ack.py operator"
    identity = "ack-bot"
    timeout  = 10

Contract (the exit code IS the verdict):
    exit 0    -> PASS:    the tool queues the message unchanged.
    exit 100  -> HANDLED: the tool queues nothing; we owned it.
    any other -> FAIL-OPEN: the tool queues it unchanged (safety net).
"""
import sys, json, subprocess

# We do NOT wrap the body in a try/except that swallows errors: if anything
# below raises, the process exits nonzero and the tool FAILS OPEN — the message
# is delivered, exactly as if this middleware were absent. That is the design.

def main() -> int:
    watch = sys.argv[1] if len(sys.argv) > 1 else "operator"

    env  = json.load(sys.stdin)        # the full envelope: from / to / ts / body
    frm  = env["from"]
    to   = env["to"]
    body = env["body"]

    # Filtering by recipient is OUR job — the tool intercepts every send.
    # Not for the recipient we watch? Pass it straight through.
    if to != watch:
        return 0                        # PASS

    # A routine "report:" line to the watched recipient: acknowledge it back to
    # the sender in our own name, then withhold the original from the queue.
    if body.lstrip().lower().startswith("report:"):
        subprocess.run(
            ["swarm", "send", frm, f"ack: report received and logged ({len(body)} chars)"],
            check=True,                 # a failed ack raises -> fail-open below
        )
        return 100                      # HANDLED: replied, now withhold the original

    # Anything else to the watched recipient: let it through untouched.
    return 0                            # PASS


if __name__ == "__main__":
    # Only exit(0) and exit(100) are deliberate verdicts. Every other path —
    # an exception propagating out of main(), a KeyError on a malformed
    # envelope, the subprocess raising — leaves via a nonzero exit and FAILS
    # OPEN. We surface the error on stderr for the operator's logs and let it
    # be nonzero; we never mask it into a 0 or a 100.
    sys.exit(main())
```

Trace the three paths through it:

1. **PASS (`exit 0`).** A message to anyone other than the watched recipient,
   or a non-`report:` message to it, returns `0`. The tool queues it unchanged.
2. **HANDLED (`exit 100`).** A `report:` line to the watched recipient: the
   middleware sends an `ack:` back to the original sender (attributed to
   `ack-bot`, not to the sender — and not re-intercepted), then returns `100`.
   The original report is never queued; the middleware owned it.
3. **FAIL-OPEN (anything else).** A malformed envelope (missing `from`), or the
   `swarm send` ack failing under `check=True`, raises out of `main()`. The
   process exits nonzero, the tool reads that as "anything else", and the
   message is **delivered** — a broken middleware is no middleware.

### The one-line no-op

The identity middleware — pass everything, own nothing. Useful as a smoke test
that wiring works before you add policy:

```sh
command = "true"     # exits 0 on every send: PASS. Nothing is ever withheld.
```

(`true` reads no stdin and exits 0, so every message passes through unchanged.)

## Pitfalls

- **Don't block for long.** The middleware runs **inside the sender's turn** —
  the sender pays the latency, and every send stalls until yours returns. Keep
  it fast; set a `timeout` so a hung middleware fails open instead of freezing
  a sender. A middleware that makes a slow network call on every send taxes the
  whole swarm.
- **`exit 0` on the pass path — explicitly.** The fail-open net delivers a
  message on a stray nonzero, so a passed message is not *dropped* by a bad exit
  — but be explicit anyway: the code that matters is the **handled** path.
  Forgetting `exit 100` there (falling through to `exit 0`) delivers a message
  you meant to withhold, silently.
- **Filter by `to` yourself.** The tool intercepts *every* send. "Only operator
  mail" or "only reports" is a condition **you** check by reading the envelope
  — there is no per-recipient wiring in the tool.
- **Mind the recursion guard.** Your middleware's own sends run as its
  `identity` and are **not** re-intercepted. That is what lets a HANDLED path
  reply without looping — but it also means your middleware never sees its own
  traffic. If you want to inspect a message you are about to forward, do it
  before you send it.
- **Test with a real send.** Point `.swarm/config` `[middleware] command` at
  your script, then run an actual `swarm send` to the recipient you watch and
  confirm the message was withheld (`swarm ps` shows no new queue entry) and
  your reply arrived. Then send to a different recipient and confirm it passed
  through. Test the fail-open path too: break the script deliberately (raise an
  error) and confirm the message is still delivered.
