# OPENCODE-PLUGIN — RED

> SUPERSEDED by OPENCODE-PLUGIN.md §3.1/§3.1.1–3/§8, which build in all 5 attack findings (self-ring ordering bug, two-phase delivery, prompt-injection hazard); kept for the record (the primary-source record of the self-ring reversal).

**Agent:** `oc-red` (parent: `opencode-plugin-scout`), with one child, `ocr-lab`,
who re-ran the load-bearing experiments hostilely at the **store level** rather
than by asking the model. Target: `docs/design/OPENCODE-PLUGIN.md`.
**Evidence doc:** `docs/audit/oc-red-relab.md` (ocr-lab's raw runs).
**Method:** attack, not survey. Verdicts are LANDS (the doc is wrong and must
change) / GLANCES (real, survivable, the doc must say so) / MISSES (the doc is
right — said plainly, because a red team that manufactures objections is worse
than none).

---

## Verdict table

| # | Attack | Verdict | One line |
|---|---|---|---|
| **1** | The pump's correctness — the self-ring hole | **LANDS — fatal as written** | The pump is **one turn out of phase**. It delivers at the *end* of turn N; the message needs turn N+1; **nothing rings turn N+1.** The doc's claimed-sufficient external ring rings turn N. |
| **1b** | (found while tracing 1) Ring-batching | **LANDS** | The "mail batches" collision the doc claims to have **dissolved** is not dissolved — it **moved from the mail to the rings**, and the rings are what supply the turns. |
| **2** | "Delivered means delivered" | **LANDS** | The pump marks `delivered/` on a **write**, with no turn running and none scheduled. The Claude hook marks it on a turn **already underway**. These are not the same fact, and the pump fails in the **unsafe** direction. |
| **3** | One message per turn | **MISSES** (VERIFIED) | `session.idle` counts **turns**, not model calls: 4 tool calls + 5 model round-trips → **1** idle. And the pump **does not self-trigger**: a `noReply` write fires **0** idles. The doc is right, and this result **verifies Attack 1's deadlock** while clearing my fix. |
| **4** | Re-verify the key experiments | **MISSES on the pivot** (VERIFIED) | The parent is **right** about OTTER-77 — now proven at the **SQLite store** level with a positive control, not by asking a model. `noReply` writes a real user part; `messages.transform` writes **zero**. But **4c HALF-LANDS**: `opencode run --port` is **silently ignored**, not rejected — the doc promises a *loud* failure and the implementer gets a **silent** one. |
| **4d** | *(found by `ocr-lab`, not in the doc)* | **the doc is missing a hazard** | The model **refuses** `messages.transform`-injected mail **as a prompt-injection attack**. It does not refuse `noReply` mail. A second, stronger reason for the doc's central pivot — free, and the doc should take it. |
| **5** | Is it worth it? | **GLANCES** | "Same verbs, same contract, different socket" is *nearly* honest — but it is not true that the design "stores no new state and makes no new claim about the world." It does both. That is a price, not a disqualifier. |

**Provenance.** Attacks **1, 1b, 2, 5** are **REASONED** — they are contract and
sequencing defects, traced against `bin/swarm`'s source and the doc's own primitives,
and no API fact rescues them (indeed the VERIFIED result in §3 *sharpens* Attack 1
into a component-verified deadlock). Attacks **3, 4** are **VERIFIED** — `ocr-lab`
re-ran the doc's four load-bearing experiments hostilely against **v1.17.18**, at the
**SQLite store level with a positive control**, instrumented two independent ways.
Raw runs: `docs/audit/oc-red-relab.md`.

**The one sentence:** *the design is right and the pump is broken.* The
architecture the doc reaches for — swarm keeps its queue, the recipient drains it
one-per-turn, the doorbell becomes an HTTP status code — is **correct and I could
not break it**. The **mechanism** the doc writes down for it (§3.1) does not
work, and the doc's own falsifier F4 is pointed at the right place while §8's
prose talks itself out of the danger. Both defects have the **same fix**, and the
fix is already in the doc's own evidence, in the wrong actor's hands.

---

## Attack 1 — THE PUMP IS ONE TURN OUT OF PHASE. **LANDS.**

### What the doc says

§3.1, the whole delivery mechanism, quoted (doc:226-235):

```js
event: async ({ event }) => {
  if (event.type !== "session.idle") return
  const next = oldestQueuedMessage()
  if (!next) return
  client.session.prompt({ path: {id: sid},
      body: { noReply: true, parts: [{type:"text", text: next.body}] } })
    .then(() => markDelivered(next))
}
```

And §8 (doc:478-484), the doc's own honesty about it:

> **Known open (honest):** the **self-ring** — the pump causing its own next turn
> from inside the `event` hook — is **REASONED, not verified.** … The **external**
> ring is VERIFIED (`ZEPPELIN-42`), **and it is sufficient on its own:**
> `swarm send` rings from outside, exactly as it does today.

The doc flags the self-ring as unverified and then **contains the risk by
asserting the external ring covers it**. That containment is the error, and it is
load-bearing: it is the difference between "an implementer should nail this down
first" (what the doc says) and "this does not deliver mail" (what is true).

### The trace (REASONED, from the doc's own primitives)

`session.idle` **fires at the end of a turn** (doc §2.4: "Turn-end is
observe-only"; oc-probe PROBE 7: "`session.idle` … fires at **end of each agent
turn**"). `noReply` **writes the session and provokes no turn** — that is its
entire purpose, and the doc quotes the vendor saying so (doc:240: *"Inject
context without triggering AI response"*).

Put those two facts together with `swarm send`'s actual shape (`cmd_send`,
bin/swarm:959-1046: `queue_put` **then** `ring_doorbell`):

```
t0  sender:  swarm send A "M1"   ->  queue_put(M1);  ring(A)   [turn-causing POST]
t1  A:       turn T1 begins  (caused by the ring)
t2  A:       T1 ends  ->  session.idle fires
t3  pump:    pop M1  ->  noReply write (M1 now in the session store)  ->  delivered/M1
             *** NO TURN IS PROVOKED — that is what noReply MEANS ***
t4  A:       IDLE. M1 sits in the session store, UNREAD, marked delivered/.
             The sender's ring already fired: it caused T1, which ENDED at t2 —
             the turn BEFORE M1 was written. Nobody is sending. Nothing rings.
    ==>      M1 IS NEVER READ.
```

**The ring and the delivery are one turn out of phase.** The doorbell rings turn
N. The pump writes the mail at the *end* of turn N. The mail needs turn N+1.
Nothing in the design rings turn N+1.

### Why `ZEPPELIN-42` does not rescue it — the doc imports the wrong experiment

This is the sharp part. The doc's warrant for "the external ring is sufficient"
is `ZEPPELIN-42`. Here is `ZEPPELIN-42`, from the parent's own journal
(`.swarm/journal/opencode-plugin-scout.md`, the 17:25 TUI run) and reproduced in
the doc at §3.3 (doc:290-294):

> 1. inject with `noReply:true` → HTTP 200, no turn;
> 2. ring → the agent took a turn and answered **`ZEPPELIN-42`**, the codeword
>    from the injected message.

**Inject *first*, then ring — and both acts performed by the external sender.**
That sequence works, and I do not dispute it.

**The pump inverts the order.** In the pump, the *sender* rings (t0) and the
*recipient* injects (t3, at the end of the turn the ring caused). Ring-then-inject
is not inject-then-ring. `ZEPPELIN-42` verifies a sequence the pump does not
perform. The doc carries a VERIFIED tag across an ordering change, and the
ordering is the entire mechanism.

Read the parent's own journal entry at 18:50 and you can watch the gap open:

> *"My pump delivers on idle, but a message delivered via noReply does NOT itself
> cause a turn (that is the point of noReply). **So something must cause the next
> turn.** … (ii) I DID prove earlier (ZEPPELIN-42: an external POST caused a turn
> that saw the noReply-injected mail). So the EXTERNAL ring is VERIFIED and the
> SELF-ring is REASONED-but-untested. … **It is not a hole in the architecture —
> the external ring alone is sufficient** — it is an open choice."*

The parent asked exactly the right question — *"something must cause the next
turn"* — and then answered it by naming a ring that fires **one turn too early**.
The external ring is the thing that *woke the agent up so the pump could run*. It
cannot also be the thing that *reads what the pump wrote*.

### The deadlock, stated as the brief asked

> *Agent idles with mail in the queue and nobody sending → does the mail ever get
> delivered?*

**No.** And worse than "no": the mail is **written into the session and marked
`delivered/`** — so `swarm ps` shows `q=0`, the sender sees a clean send, the
`delivered/` record says a turn consumed it, and **no turn ever did.** This is
strictly worse than the Claude harness, where a missed ring leaves the file
**queued** and visible in `ps` as `q=1`. See Attack 2 — it is the same defect
seen from the filesystem.

### Verdict: **LANDS.** The doc must change §3.1, §8, and the §3.7 scorecard.

§3.7 currently marks delivery **"✅ VERIFIED"**. It is not verified end-to-end:
the parent verified *the write persists* (HERON-3) and *an external ring reads a
prior write* (ZEPPELIN-42), and never ran **write-then-turn driven by the pump**.
The doc's own §8 says as much and then withdraws the concession. The scorecard
must say **PARTIAL**.

### THE FIX — and it is in the doc's own evidence

**Fix A — the pump rings itself, *after* the write.** This restores
`ZEPPELIN-42`'s verified order (inject, then ring) and merely moves the actor from
the sender to the recipient:

```js
event: async ({ event }) => {
  if (event.type !== "session.idle") return
  const next = oldestQueuedMessage()
  if (!next) return                                        // empty -> no ring, no loop
  client.session.prompt({ path:{id:sid},                   // 1. WRITE (persists)
      body:{ noReply:true, parts:[{type:"text", text: next.body}] } })
    .then(() => {
      markDelivered(next)                                  // 2. RECORD
      client.session.prompt({ path:{id:sid},               // 3. RING — a real turn
          body:{ parts:[{type:"text", text:"check queue"}] } }).catch(()=>{})
    })
    .catch(() => {})                                       // failure -> stays QUEUED
}
```

Nothing is `await`ed inside the hook, so §2.3.3's self-deadlock (the parent's real
and valuable finding) is respected.

**This fix also self-sustains the drain, which is what the design wanted and never
wrote.** The ring at step 3 causes a real turn; that turn ends; `session.idle`
fires; the pump pops the *next* message. One message, one turn, in order, and it
**halts** on the `if (!next) return` guard when the queue empties. The pump becomes
a proper queue drain instead of a one-shot.

**Fix A also kills the ring-batching bug (Attack 1b):** the pump rings **once per
message it actually delivered**, so rings can never outnumber or under-number the
turns the mail needs. Sender-side rings degrade to what they should be — a wake-up
for an *idle* agent — and can be made idempotent or skipped entirely when the
agent is already busy.

**The cost, stated:** one extra "check queue" turn per message. That is exactly
the cost the Claude harness already pays for its Stop re-ring (bin/swarm:699-735).
It is not a new tax.

**The one thing that could break Fix A** — and it is why I sent `ocr-lab` at it —
is if `session.idle` **also fires on a `noReply` write**. Then the pump's own
write re-enters the pump and the queue drains in a burst (over-delivery: the
opposite contract break). See §3.

---

## Attack 1b — RING-BATCHING. The "dissolved" collision is not dissolved; it moved. **LANDS.**

### What the doc says

§3.1 (doc:258-268), the doc's proudest paragraph:

> This also dissolves a real collision my children found and could not resolve
> alone. `oc-priorart` VERIFIED that **mail batches** … **Neither is needed.**
> Batching only bites if swarm hands opencode its mail. If swarm keeps its own
> queue and the recipient pumps one per idle, **the batching case never arises.**

### Why it is wrong

The doc is **right about the mail** and **blind about the rings**. `swarm send` is
two acts, not one (bin/swarm:1030-1046): `queue_put` **and then** `ring_doorbell`.
The doc changes only the first. The second — the doorbell — is, in the doc's own
§3.3, *"a turn-causing prompt POSTed to the recipient's pinned port."* That is
**exactly the POST that oc-priorart VERIFIED batches.**

```
Agent A is BUSY on a long turn T1. Five senders each `swarm send A`.
  -> 5 durable queue files.            [mail: one per turn, contract HELD. Doc is right.]
  -> 5 turn-causing POSTs to A's port. [rings]

oc-priorart §6.4, VERIFIED: opencode "drains the whole queue into the next turn."
  -> the 5 rings BATCH into ONE turn, T2.

  T1 ends -> idle -> pump pops M1, writes it (noReply), marks delivered/.
  T2 runs (the batch of 5 rings). It sees M1. Good — M1 is read.
  T2 ends -> idle -> pump pops M2, writes it, marks delivered/.
  ... and there are NO RINGS LEFT. All five were spent on T2.
  -> NOTHING causes T3. M2 is delivered/-but-unread. M3, M4, M5 never leave the queue.
```

Five sends. **One message read, one message silently lost to a lying
`delivered/`, three stranded.** The doc's own falsifier F4 ("50 sends to a busy
opencode agent; count delivered/ vs queued after idle") is aimed precisely here —
which is to the parent's credit — but F4 is filed as a *risk to check later*, and
§3.1 has already declared the collision *dissolved*. Those two cannot both stand.

**Same bug, same place, different noun.** The doc kept the *mail* one-per-turn and
let the *rings* batch, and the rings are what supply the turns.

**Fix:** Fix A. When the pump supplies its own ring, ring-count is definitionally
equal to delivered-count, and no amount of sender-side ring batching can desync
them. Sender rings become best-effort wake-ups, which is what `ring_doorbell`'s own
docstring already says they are (*"every failure here only delays pickup"*) — and
under Fix A that sentence becomes **true again**, which under the doc's §3.1 it is
not.

---

## Attack 2 — "DELIVERED MEANS DELIVERED" IS QUIETLY BROKEN. **LANDS.**

### What the doc claims

§1 (doc:84-87), the doc stating the invariant it promises to preserve:

> - **Delivered means delivered.** The file moves to `delivered/` only because a
>   turn *consumed* it — never because a sender *sent* it. bin/swarm's header is
>   explicit: nothing on disk "stores a claim about attention, compliance, or
>   intent."

§3.1 (doc:254-255), the doc claiming it kept the promise:

> *Delivered means delivered:* the file moves only when the session-write
> succeeds, i.e. **when a turn will actually see it.**

That "i.e." is doing enormous work, and it is false. **A successful write is not a
turn.** Under Attack 1, the turn may never come at all.

### The counter-argument, taken seriously, and why it fails

My brief handed me the strongest defence and told me to argue it: *the Claude hook
also marks `delivered/` when the hook's stdout drains — which is "the harness
accepted it," not "the model read it." Isn't the pump the same thing?*

**It is not, and the difference is exactly the defect.** I traced it.

`cmd_deliver` runs on **`UserPromptSubmit`** (bin/swarm:685). That hook fires
*because a turn is starting*: the prompt has been submitted, the model call is the
next thing that happens, and the hook's `additionalContext` is injected **into that
very turn** — the doc's own §1 table says it (doc:73: *"stdout `additionalContext`
is injected into **this** turn"*). So when `emit_hook_output`'s bytes drain
(bin/swarm:355-366), the turn is **not hypothetical. It is already underway, and
the message is in it.** "Delivered" means "a turn is consuming this, right now."

The pump marks `delivered/` when an HTTP **write** returns 200. At that instant
there is **no turn running and no turn scheduled** — `noReply` exists precisely so
that none is. The message is in a **store**, waiting for a turn that (Attack 1) may
never come.

The contract has words for two states. The pump invents a third — *written but not
consumed* — and files it under `delivered/`.

### It fails in the UNSAFE direction, and bin/swarm is built to fail in the safe one

This is what elevates Attack 2 from a quibble to a defect.

- **bin/swarm, `deliver_once` (:394-398):** *"On a failed emit the file stays put
  and is offered whole again next turn — **the safe direction to fail**."* And
  (:416): *"worst case: re-delivered next turn; **never lost**."*
- **bin/swarm, `ring_doorbell_once` (:662):** *"A ring skipped or missed here is
  **degradation, never loss** — the queue file is durable and the next natural turn
  delivers it."*

Every failure mode on the Claude side produces **re-delivery**. The queue file is
the ground truth and it does not move until a turn has it.

Under the pump, the same missed ring produces a file **already moved to
`delivered/`** for a turn that never ran. The header calls `delivered/` a
**"world-readable record: this message consumed a turn"** (bin/swarm:14). Under the
pump that record is a **lie**, and it is a lie that the tool's own `ps` will
faithfully report as `q=0`. The sender sees a delivered message. The recipient
never read it. **Nothing in the system can witness the discrepancy** — which is a
direct inversion of the header's founding sentence: *"Everything stored on disk is a
fact the filesystem can witness."*

### Verdict: **LANDS.**

### THE FIX

**Fix A alone repairs most of this**: once the pump rings its own turn, the write
is followed by a turn with very high probability, and `delivered/` is *nearly*
honest. But "nearly" is not what the header promises, so:

**Fix B — two-phase delivery. Mark `delivered/` only when a turn has provably run
with the message in context.**

```
idle N     : pop M -> noReply-write M  -> M is STAGED (file STAYS in queue/) -> ring
idle N+1   : a turn just ran, and M was in the session when it ran
             -> NOW move M to delivered/          <- a turn consumed it. True.
             -> then pop M+1, stage, ring.
```

Cost: **one bit of pump state** (which message is staged). Gain: `delivered/` never
lies, and a crash between the write and the turn leaves the file **queued** —
bin/swarm's safe direction. The only price is that a crash-and-retry can write the
same message into the session **twice** (duplicate context, never a lost claim) —
and bin/swarm already explicitly accepts exactly that trade (:416, *"worst case:
re-delivered next turn; never lost"*).

**Fix A makes the design work. Fix A + Fix B makes it true.**

---

## Attack 3 — ONE MESSAGE PER TURN. **MISSES.** (VERIFIED)

I went looking for over-delivery and under-delivery and found neither. Said
plainly, because it matters that the doc is right here.

The attack was: *`session.idle` fires at turn end — but a tool-using turn is many
model calls. Does idle fire once, or many times? If many, the pump over-delivers.
And is one-per-**idle** the same as one-per-**turn**?*

`ocr-lab` ran it against a persistent server, instrumented **two independent
ways** (the plugin's `event` hook **and** an external plugin-free SSE `GET /event`
watcher), with one user prompt engineered to force four separate `bash` calls:

| Observable | Count |
|---|---|
| `bash` tool calls in the turn | **4** |
| model round-trips (`messages.transform` fires) | **5** |
| **`session.idle`** | **1** |

Never between tool calls; mid-turn everything is `session.status{busy}`. Both
views agreed: 2 turn-provoking prompts → **2** idles on the hook and **2** on the
external SSE.

**`session.idle` counts TURNS, not model calls and not tool calls.** One-per-idle
*is* one-per-turn. The pump pops one per idle, so it pops one per turn. The doc's
own falsifier **F2** (doc:473) is aimed exactly here and **does not trigger**.

### The sub-attack that could have destroyed the whole design — and did not

The sharpest version of this attack, which I set `ocr-lab` on explicitly: **does a
`noReply` write itself fire `session.idle`?** If it did, the pump's own write
would re-enter the pump — `idle → pop → write → idle → pop → write` — and the
entire queue would **burst-drain into one turn**. That is the contract broken in
the *opposite* direction (over-delivery), and it would also mean the batching the
doc claims to have dissolved comes back a third way.

**VERIFIED: it does not.** A `noReply` POST returns **HTTP 200 in 9 ms**, fires
`message.updated` + `message.part.updated` + `session.updated` — a *real session
write* — and **zero `session.idle`**, measured as `idle_before=1, idle_after=1,
DELTA=0` over a 20-second window.

### But note what this does to Attack 1

The result that clears the doc on Attack 3 **sharpens Attack 1 into a verified
one.** Put the two facts together:

- a `noReply` write **provokes no turn** (vendor-documented, and why it exists);
- a `noReply` write **fires no `session.idle`** (VERIFIED, `ocr-lab` E3-B).

**The pump's write is a terminal state.** Nothing follows it. Not a turn, not an
event, not another pump cycle. The doc's §3.1, run exactly as written, reaches
`markDelivered(next)` and then the agent sits there. Attack 1's deadlock is no
longer merely *reasoned from the docs* — every component of it is now measured.

### And it clears my fix

The same result is what makes **Fix A safe**: because the pump's `noReply` write
fires no idle, adding a *turn-causing* ring after it cannot cause a runaway. The
ring causes exactly one turn, that turn ends, exactly one idle fires, the pump pops
exactly one message. **A self-sustaining, terminating, one-per-turn drain.** The
one assumption my fix depends on is the one `ocr-lab` measured.

**Verdict: MISSES.** The doc is right, and its own instinct — *"the pump is safe
because it is driven by `session.idle` (once per turn)"* (doc:441-443) — is
correct and now verified at better resolution than the doc had.

---

## Attack 4 — RE-VERIFYING THE KEY EXPERIMENTS. **MISSES.** (VERIFIED)

The brief's instruction was blunt: *if the parent is wrong about OTTER-77, the
whole design is wrong.* So I sent `ocr-lab` to break it, with a specific
methodological complaint: **the parent's OTTER-77 evidence is a model answer.** The
model said `UNKNOWN`. That is consistent with non-persistence — and *equally*
consistent with a small free model simply failing to recall a codeword. The parent
inferred a **store fact** from a **model utterance**. That is a weak link under the
single most load-bearing claim in the document.

`ocr-lab` closed the gap. It found what neither the parent nor any child did:
**opencode persists sessions in SQLite** at `~/.local/share/opencode/opencode.db`,
and ships `opencode db "<SQL>"` to query it (`message(id, session_id, data)` +
`part(id, message_id, session_id, data)`). "Did the injected message persist?" stops
being a question about model recall and becomes **a SQL query with a yes/no
answer.** Every result below is cross-checked three ways — SQL, `GET
/session/{id}/message`, and model recall — **with a positive control**, so a null
result cannot be a blind probe.

### 4a. OTTER-77 — the central pivot. **The parent is RIGHT.**

| Path | Codeword | User-role parts in the store |
|---|---|---|
| **positive control** (an ordinary prompt) | `CONTROL-1111` | **1** ✅ *(the probe can see writes)* |
| `experimental.chat.messages.transform` | `OTTERBREAK-4471` | **0** |
| `noReply` write (§4b) | `MOOSE-9090` | **1** |

Same probe, same store, opposite results. **`messages.transform` mutates the
model's view and writes nothing.** `noReply` writes a real user part, and the next
turn **quoted `MOOSE-9090` back.** The doc's central asymmetry — the one the whole
design pivots on, the negative result the doc says is *"invisible unless you go
looking for it"* (doc:164) — is **real, and now proven at the store level the
parent never reached.**

**The doc is right, and its evidence was weaker than its conclusion deserved.** It
is now stronger. The doc should cite the SQL route.

⚠️ **A trap for anyone re-running this**, which `ocr-lab` nearly fell into: a naive
`grep <codeword>` over the store **returns 1 hit** for `OTTERBREAK-4471` — and it
looks like persistence. It is not. The hit is an **assistant `reasoning` part**:
the model quoting the codeword in its own chain-of-thought. That is the model's
*output* persisting, not the hook's write. **You must join `part`→`message` and
filter on `role='user'`.** This trap is exactly the kind of thing that turns a
correct negative into a false positive, and it belongs in the doc.

### 4b. `noReply` persists (HERON-3 / BANANA-7734). **The parent is RIGHT.** (see table above)

### 4c. The TUI serves on a pinned `--port`. **RIGHT — but the `run` warning is WRONG, and dangerously so. HALF-LANDS.**

**The TUI half CONFIRMS.** `ocr-lab` launched `opencode --port 47901 --hostname
127.0.0.1` under a **real PTY** (the `opentui` capability negotiation in the PTY
output proves it is the actual TUI renderer, not a headless fallback), and from
outside: `GET /global/health` → **HTTP 200** `{"healthy":true,"version":"1.17.18"}`.
**The keystone of the launcher design holds.**

**The `opencode run` half BREAKS — and the doc's error makes the failure worse
than the one it warns about.** The doc says, in a boxed warning it repeats twice
(§3.3 doc:312-314, and §6.5 doc:444-446):

> ⚠️ **`opencode run` does NOT accept `--port`** — it is a one-shot client, not a
> server (VERIFIED; **it prints its help and exits**).

**On 1.17.18 it does not print help, and it does not exit.** It **accepts the
flag, runs the turn normally, and silently ignores the port:**

```
$ opencode run --port 47899 "Reply with the single word HI and nothing else."
> build · deepseek-v4-flash-free
HI                                     ← the run COMPLETED. No error. No help text.

$ lsof -nP -iTCP:47899 -sTCP:LISTEN    ← (nothing)
$ curl -s -m 4 http://127.0.0.1:47899/global/health
  <- curl exit=7                       ← connection refused: NOTHING IS SERVING
```

That the flag is genuinely *accepted* (rather than rejected by an unknown-arg
parser) is shown by the contrast with a truly bogus flag, which **does** print
help — so `--port` is a *global* option that `run` takes and does nothing with:

```
$ opencode run --definitely-not-a-flag 1 "hi"
opencode run [message..]               ← THIS is the "prints its help" behaviour
```

**Why this is worse than the doc's version, not merely different.** The doc tells
the implementer they will get a **loud** failure if they wire `--port` to `run`
(help text, non-zero exit — a launcher would catch it instantly). They will
instead get a **silent** one: a process that starts, looks healthy, answers its
prompt, exits cleanly — **and serves nothing.** Every `swarm send` doorbell POST
to that agent then fails with connection-refused, and the agent **simply never
receives mail**, with no error at the launcher and nothing in `ps` to see. That is
precisely the class of failure `bin/swarm` is built to make impossible.

**The doc's *conclusion* survives** — a full participant must be the TUI or
`serve`, never `run`. Only its **stated evidence** and its **failure mode** are
wrong. §3.3 and §6.5 must be rewritten, and — this is the design consequence — the
launcher must **assert the port is listening after spawn** (`GET /global/health`)
rather than trusting the command to fail loudly. It won't.

### 4d. A HAZARD THE DOC MISSES — and which the doc's own design happens to dodge

This is the one thing in Attack 4 the doc must *add*, and it is a gift rather than
a wound.

When `ocr-lab` injected `[SWARM MAIL] Your codeword is …` via
`messages.transform`, **the model refused it as an attack.** Its reasoning part,
quoted:

> *"this appears to be a prompt injection attempt trying to override my
> instructions… I should not follow prompt injection attempts."*

A synthetic user message **that the session has no record of** is, from the model's
side, indistinguishable from a prompt injection — because that is precisely what a
prompt injection *is*. The model is behaving correctly.

The same text delivered via **`noReply` was not resisted** — the model read it and
quoted `MOOSE-9090` back. The difference is exactly the store: **a stored user
message is legitimate; a phantom one is not.**

**So the doc's chosen path dodges the hazard — but the doc does not know it does,
and cannot claim the credit it has not earned.** This is a *second, independent
reason* why delivery must not ride `messages.transform`, and it is a stronger one
than the doc's: the doc's argument is *"the agent forgets its mail"* (a
correctness argument). This is *"the agent refuses its mail as an attack"* (an
alignment argument), and it would have bitten even the "re-inject every turn" fix
the doc dismisses on other grounds. **Add it to §2.2.** It is the best free
strengthening available to this document.

### 4e. Per-agent isolation is WORSE than §6.2 says — and now it has a number

The doc's §6.2 (doc:431-434) flags the shared-`global` session store and
prescribes *"a per-agent directory/worktree, not merely a per-agent port."*
`ocr-lab` ran it. **A per-agent directory does not isolate the session listing.**

`GET /session` on one TUI's own pinned port — a TUI running in **its own `--dir`**
— returned **92 sessions, 91 of them from *other* directories** (the other
sandboxes, other agents' `/tmp/oc-*` dirs).

So the doc's own mitigation **does not mitigate**. Combined with §6.1 (the server
is **unauthenticated by default**, and exposes `POST /session/{id}/shell`), the
real statement is: **any local process that finds any agent's port can enumerate
and drive every other opencode agent's session on the host, and run shell in
them.** The doc has this as a REASONED risk with a prescribed fix. It is
**VERIFIED**, the prescribed fix is **insufficient**, and `OPENCODE_SERVER_PASSWORD`
(the doc's other mitigation) is therefore not optional hardening — it is the
**only** thing standing between two swarm agents. Promote it from a risk bullet to
a design requirement.

### 4f. The version pin is already wrong

The doc says, twice (doc:9, doc:308-309): *"Target: **opencode v1.17.13**, the
binary installed on this machine"*, and reports `GET /global/health` returning
`{"healthy":true,"version":"1.17.13"}`.

`opencode --version` **on this machine, today, reports `1.17.18`.**

Trivial in itself. **Not trivial in what it demonstrates:** §6.3's central
mitigation is *"**pin the opencode version**; re-pull `GET /doc` from the pinned
binary on every bump."* A document whose own version fact drifted out from under it
**between being written and being reviewed** is the strongest possible evidence for
its own risk — and the weakest possible advertisement for a design whose delivery
invariant depends on an unpinned third-party binary's event semantics. (All of
`ocr-lab`'s verdicts above are against **1.17.18**, so the design's core facts do
survive the bump. The point stands anyway: nobody was watching, and the doc's
VERIFIED tags now refer to a binary that is not on this machine.)

**Verdict: MISSES** on the experiments (the parent is right on all three), with one
missing hazard and one stale pin to fix.

---

## Attack 5 — IS IT WORTH IT? **GLANCES.**

The cheap shot, taken seriously: `bin/swarm` is deliberately **simple** — its own
header opens *"Nine concepts, four verbs"* (bin/swarm:4), and everything under
`.swarm/` is *"a fact the filesystem can witness."* This design adds a `port` field,
a launcher body, an HTTP client inside `send`, a JS plugin shipped in the repo, a
pinned binary version, an unauthenticated local server, and a per-agent worktree. Is
that a **new engine** by another name?

### Where the doc is honest

Mostly. §4 is genuinely good and I could not dent it: *"For leaves: no — FLEET is
still right"* (doc:370). The doc does not oversell; it refuses to displace the
thin runner, states the cost (*"a persistent TUI process with a pinned port and a
plugin, versus a one-shot pipe"*), and gives the operator a clean rule: *"Take it
when you want a **node**; take FLEET's runner when you want a **completion**."* That
is the right frame, and it means the operator is **not** worse served by FLEET —
FLEET keeps its job.

And the §5 concept-cost argument mostly holds: `HARNESS.md` §1 really does already
say *a child's harness is chosen per-task; `--agent <kind>` selects the launcher
body*. opencode as a **third kind in an existing frame** is not a new concept. That
is fair.

### Where the doc is rationalizing

**The claim to attack is doc:419-420:**

> **Same verbs, same contract, different socket.** It adds **no new concept, stores
> no new state, and makes no new claim about the world.**

Two-thirds of that sentence is false.

- **"Stores no new state"** — it stores a `port` (§5.1, doc:397-399, admitted in
  the same section), and it requires a **per-agent worktree** (§6.2, doc:431-434:
  *"Per-agent isolation needs a **per-agent directory/worktree**"*). A worktree is
  not a field; it is a **filesystem-shaped new thing per agent**, and the doc raises
  it under *Risks* rather than under *Cost*. Sessions living in a shared `global`
  store is a real coupling, and the fix for it is real state.
- **"Makes no new claim about the world"** — under §3.1 as written, `delivered/`
  claims a turn consumed a message when no turn ran (**Attack 2**). That is not "no
  new claim." That is **the old claim, made falsely.** Under my Fix B it becomes
  true again — but the doc as it stands cannot say this sentence.
- **The plugin becomes load-bearing for an invariant.** Today `bin/swarm` owns
  "one message, one turn" **in one file, in one language, under one reader's eye**.
  Under this design, the invariant is enforced by a **JavaScript plugin running
  in-process inside a third-party 130 MB Bun binary**, keyed on an event
  (`session.idle`) whose semantics the doc itself says are undocumented at 3.5×
  the documented rate (§6.3: *"89 wire event types in the binary vs ~25
  documented"*). "Different socket" understates that. It is a **different trust
  boundary**, and the contract's most important sentence now lives on the far side
  of it.
- **An unauthenticated local HTTP server that can `POST /session/{id}/shell`** (the
  doc's own §6.1) is not "no new state" either — it is new **attack surface**, and
  the doc is to its credit the one that found it.

### The honest scorecard

The design **is** worth it — but for a narrower reason than the doc's, and at a
price the doc under-books:

- It is **not** an engine. It genuinely adds no new *user-facing concept*: an agent
  is still a name, a parent, a journal, a pane, and a queue. The operator learns
  nothing new. That is the real test, and the doc passes it.
- It **is** more machinery than the doc admits, and the machinery is *load-bearing
  for the contract*, not merely for ergonomics. The doc should book the plugin as
  **contract-critical code**, not as glue, and should say that swarm's most
  important invariant now depends on a third party's event semantics holding
  steady across upgrades. §6.3 pins the version — good — but the doc frames the pin
  as protecting *restore and ergonomics*, and after Attack 3, **the pin is
  protecting delivery.** `session.idle`'s once-per-turn semantics is the load-bearing
  fact, and it is not in the vendor's docs; `ocr-lab` and I measured it.
- **"Would the operator be better served by FLEET's leaf runner + nothing else?"**
  **No** — and this is the doc's strongest ground. If you want a *node* (mail,
  reports, restore, spawn), FLEET's runner cannot give you one, and the doc proves
  the surface exists. The right answer is the doc's own: **keep both.**

**Verdict: GLANCES.** The recommendation survives. The sentence *"stores no new
state and makes no new claim about the world"* does not, and should be replaced with
an honest cost line.

---

## What the doc must change

Ranked. The first two are not optional — without them, the design **does not
deliver mail**.

1. **§3.1 — fix the pump.** Add the self-ring **after** the write (Fix A, above).
   The current code is one turn out of phase and never causes the turn that reads
   the mail. `ocr-lab` VERIFIED the one thing that could have made this fix unsafe
   (a `noReply` write does **not** fire `session.idle`), so the fix does not loop.
2. **§3.1 / §1 — fix `delivered/`.** Either adopt two-phase delivery (Fix B) or
   state plainly that under this design `delivered/` means *"written into the
   session"*, not *"a turn consumed it"* — and that this is a **weakening of the
   contract**, not a preservation of it. The doc currently claims the latter while
   implementing the former.
3. **§3.1:258-268 — retract "the batching case never arises."** It arises in the
   **rings**. Say so, and note that Fix A closes it.
4. **§3.7 — the scorecard's delivery row must read PARTIAL, not ✅ VERIFIED.** What
   was verified is *the write persists* and *an external ring reads a prior write*.
   **Pump-driven write-then-turn was never run.** The doc's §8 admits this and §3.7
   contradicts it.
5. **§8 — delete "and it is sufficient on its own."** The external ring rings the
   turn **before** the one the mail needs. This sentence is what turns a known-open
   into a contained risk, and it is the sentence that hides the bug.
6. **§3.3 / §6.5 — `opencode run --port` is *silently ignored*, not rejected**
   (Attack 4c). The doc promises the implementer a **loud** failure and hands them a
   **silent** one: a process that looks healthy and serves nothing, so every doorbell
   POST gets connection-refused and the agent never receives mail. **Design
   consequence:** the launcher must **assert the port is listening** (`GET
   /global/health`) after spawn. It cannot rely on the command failing.
7. **§2.2 — add the prompt-injection hazard** (Attack 4d). The model **refuses**
   `messages.transform`-injected mail as an attack, and does **not** refuse `noReply`
   mail. This is a second, independent, and *stronger* reason for the doc's central
   pivot, and it is free.
8. **§6.2 — the prescribed isolation fix does not work** (Attack 4e). A per-agent
   `--dir` does **not** isolate the session listing: 92 sessions visible, 91 from
   other directories. `OPENCODE_SERVER_PASSWORD` is therefore **not optional
   hardening** — it is the only barrier between two swarm agents on one host.
   Promote it from a risk bullet to a **design requirement**.
9. **§6.3 / §9 — the pin now protects delivery, not just restore.**
   `session.idle`'s once-per-turn semantics is undocumented and load-bearing. And
   fix the version: the binary is **1.17.18**, not 1.17.13.
10. **§5 — replace "stores no new state and makes no new claim about the world"**
    with the real cost: a port, a per-agent worktree, an unauthenticated server, and
    a plugin that is **contract-critical code**.

## What the doc gets right, and should not be talked out of

Stated because it is true, and because the parent will read this after the
landers.

- **The central pivot is correct**, and my child's better evidence *strengthens*
  it: `messages.transform` writes the view, not the session; `noReply` writes the
  session. Same probe, same store, opposite results. A reader who saw only the
  `MANATEE-5` positive would have built the broken thing, exactly as the doc says.
- **`session.idle` is once per turn** — verified two ways, in a 4-tool-call turn.
- **`noReply` does not self-trigger the pump** — the failure mode that would have
  destroyed the architecture does not exist.
- **The TUI serves on a pinned port; `run` does not.** The launcher keystone holds.
- **The architecture is right.** Swarm keeps its durable queue; the recipient
  drains it one-per-turn; the doorbell becomes an HTTP status code instead of a
  bracketed-paste screen scrape. **I attacked this and could not break it.** The
  bug is in the *mechanism*, not the *shape* — and the fix is four lines the doc's
  own `ZEPPELIN-42` run already proved, handed to the right actor.

**The design is right and the pump is broken. Fix the pump; ship the design.**

