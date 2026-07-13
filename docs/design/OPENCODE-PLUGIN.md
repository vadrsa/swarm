# OPENCODE-PLUGIN — can opencode be a first-class swarm harness?

**Author:** `opencode-plugin-scout`, at the operator's request, with four children
(`oc-api` — the installed plugin API, source-traced to binary dispatch sites;
`oc-probe` — a throwaway probe plugin, 8 probes + 3 falsifiers; `oc-priorart` —
docs, server, ecosystem, itself split into `oc-docs` + `oc-eco`; **`oc-red`** — the
adversarial review, with `ocr-lab` doing bench work). Evidence:
`docs/audit/opencode-plugin-api.md`, `docs/audit/opencode-plugin-probe.md`,
`docs/audit/opencode-plugin-priorart.md`, `docs/audit/opencode-priorart-docs.md`,
and the review itself at **`docs/design/OPENCODE-PLUGIN-RED.md`**.
Target: **opencode v1.17.18**, the binary installed on this machine.

⚠️ **The binary moved under this investigation.** Early probes ran against
**1.17.13** (and their pasted outputs say so, verbatim — I have not rewritten
them); by the end `opencode --version` reported **1.17.18**. All four
load-bearing experiments were re-run on 1.17.18 by `ocr-lab` and **survive the
bump**. But the fact that a version drifted *during a single investigation* is
itself evidence for §6.3: **pin the version, and re-run the probes on every
bump.** I state this rather than quietly normalizing the numbers, because a doc
that told you to pin a version while being wrong about which version it probed
would have earned no trust.

**The review changed this document materially** — it landed three attacks, two of
which are corrections to the delivery mechanism itself (§3.1, §3.1.1, §3.1.3), and
it proved the design's central pivot (§2.2) at a resolution I had not reached. The
errors it caught are recorded where they happened rather than tidied away; a design
doc that hides its own corrections teaches nobody.

Every claim is tagged **VERIFIED** (someone ran it; the run is in the record),
**DOCUMENTED** (official docs, not exercised), or **REASONED** (inference, named
as such). All probe sandboxes were torn down; no product code was written.

---

## 0. The answer, in one breath

**Yes — and the operator's hypothesis is confirmed, but the winning design is not
the one the hypothesis pointed at.**

An opencode plugin *can* genuinely edit the harness loop. It is loaded
**in-process** and handed the live objects — the message array, the system-prompt
array, tool args, tool results, tool schemas, sampling params, even the language
model itself — with the contract *"mutate this and I will use what you leave
behind."* That is materially **deeper than Claude Code's hooks**, which are
out-of-process shell callbacks that talk through exit codes and stdout JSON
(VERIFIED — `docs/audit/opencode-plugin-api.md` §2, traced to binary dispatch
sites; I confirmed it live: a plugin of mine pushed a string into the system
prompt and into the message array, and the model obeyed both).

But swarm should **not** deliver mail through that power, and the reason is a
negative result I went looking for and found:

> **`experimental.chat.messages.transform` mutates the model's *view*, not the
> session.** The model sees your injected message on that turn — and the session
> never records it. Next turn it is gone. (VERIFIED, §2.2.)

An agent given its mail that way **forgets it the instant the turn ends**. So the
deepest hook in the API is the wrong tool for delivery, and a reader who saw only
the positive result would have built the broken thing.

The design that works uses only **documented** surface, preserves swarm's
contract byte-for-byte, and is *better than what swarm has against Claude Code
today*:

> **`swarm send` keeps writing its durable queue file and rings a best-effort
> wake-up over HTTP. The recipient's own plugin — *the pump* — wakes on
> `session.idle`, pops exactly one message, writes it into its own session with
> `noReply:true` (which persists), and **rings its own next turn**. The file moves
> to `delivered/` only at the *following* idle, once a turn has provably run with
> the message in context.**

One message, one turn, durable, contract intact. **The doorbell becomes an HTTP
POST with a status code instead of the herdr `send-text` + bracketed-paste +
settle-loop + `❯`-heuristic screen scrape that swarm's own source calls "THE ONE
UNPROVEN MECHANISM."** (bin/swarm:699-735.)

The two details that make it correct rather than merely plausible — **the pump
must supply its own turns**, and **`delivered/` must lag the turn that reads the
mail** — were both found by this document's adversarial review (`oc-red`, with
`ocr-lab`) *after* an earlier draft got them wrong. They are in §3.1, §3.1.1, and
§3.1.3, and the record of the error is kept in §8 rather than tidied away.

**Recommendation: build it — a third `--agent` kind, `opencode`, in the frame
`HARNESS.md` already designed.** And, contra the archived doctrine's "prefer
codex for *leaf* work," an opencode agent built this way is a **full
participant** — it receives mail, reports, restores, and spawns — not a leaf.
That is the claim that earns this document.

---

## 1. What a swarm harness must provide

From the archived codex work (`docs/design/archive/CODEX-CAPABILITIES.md`) and
`bin/swarm` itself, the surface is six items. This is the checklist; §3 answers
each.

| # | Surface | What Claude Code gives swarm | Where |
|---|---|---|---|
| 1 | **delivery** | `UserPromptSubmit` hook; stdout `additionalContext` is injected into *this* turn; the queue file moves to `delivered/` **only after** the hook's stdout drains | `cmd_deliver`, bin/swarm:685 |
| 2 | **event** | `Stop` hook; payload carries `transcript_path` → last assistant words | `cmd_event`, bin/swarm:699 |
| 3 | **doorbell** | `Stop` hook re-rings its own pane (herdr send-text + Enter) so the queue keeps draining while idle | `ring_doorbell_once`, bin/swarm:662 |
| 4 | **restore** | `SessionStart` hook (startup/resume/compact) → re-inject task + journal tail | `cmd_restore`, bin/swarm:737 |
| 5 | **identity** | `SWARM_AGENT_ID` in the process env, inherited by hook processes | `my_name`, bin/swarm:63 |
| 6 | **spawn / pane** | the agent runs the `swarm` CLI as a shell command, in a herdr pane | `cmd_spawn`, bin/swarm:844 |

The two invariants these serve, which any harness must not break:

- **A message is a claim on ONE turn.** One queued message per turn, oldest
  first.
- **Delivered means delivered.** The file moves to `delivered/` only because a
  turn *consumed* it — never because a sender *sent* it. bin/swarm's header is
  explicit: nothing on disk "stores a claim about attention, compliance, or
  intent."

---

## 2. What the opencode plugin API actually is

### 2.1 It is real loop-editing, not event hooks (VERIFIED)

Every v1 hook is `(input, output) => Promise<void>`. The return value is
**discarded**; the dispatcher hands the *same* `output` reference back to the
caller (`for (let M of K) await M(K,B); return B`). Your power is to **mutate
`output` in place** — and it is a big one (VERIFIED, `oc-api`, traced to the
binary).

I ran a throwaway plugin (`/tmp/oc-hookprobe`, torn down) in a plain
`opencode run`. It loaded from a project-local `.opencode/plugin/*.js` — **no
install, no registry, no global config edit** — and these fired live:

```
[load] plugin loaded. serverUrl=http://localhost:4096/ SWARM_AGENT_ID=hookprobe
[chat.message] FIRED
[system.transform] FIRED. system[] len=1 → pushed → now len=2
[messages.transform] FIRED. messages=1 → pushed → now=2
[tool.execute.before] ...
[event] session.idle
```

Then I asked the model for the two codewords I had injected — one via the system
prompt, one as a synthetic user message. It answered:

```
PELICAN-9      ← from experimental.chat.system.transform
MANATEE-5      ← from experimental.chat.messages.transform
```

**Both mutations reached the model.** (VERIFIED.) The operator's hypothesis —
"we could write something that edits the harness's loop" — is true.

The useful hooks, in swarm's terms:

| Hook | Power | Swarm use |
|---|---|---|
| `experimental.chat.messages.transform` | rewrite **the whole conversation** the model sees this turn | see §2.2 — **not** delivery |
| `experimental.chat.system.transform` | own **the system prompt**, per turn | **identity / contract injection** ✅ |
| `event` → `session.idle` | observe turn-end | **the pump trigger** ✅ |
| `tool` (a map) | **register new tools** the model can call | native `swarm_send` / `swarm_spawn` ✅ |
| `tool.execute.before` / `.after` | rewrite tool args / rewrite the result the model sees | policy, worktree rewriting |
| `shell.env` | inject env into **every shell** the agent runs | ambient `SWARM_AGENT_ID` ✅ |
| `experimental.session.compacting` | shape the compaction prompt | **restore by construction** ✅ |

### 2.2 The negative result that decides the design (VERIFIED)

`experimental.chat.messages.transform` is a **per-model-call view transform, not
a session write.**

The experiment (`/tmp/oc-persist`, torn down). A plugin injects
`"your codeword is OTTER-77"` into the message array **exactly once** (guarded by
a marker file — simulating swarm popping one message from the queue), then never
again:

- **Turn 1** (fresh session): plugin logs `INJECTING ONCE`. Model replies normally.
- **Turn 2** (`opencode run --continue`, *same session*): plugin logs
  `already popped, no inject`. I ask: *"What is your codeword?"*
- **Model answers: `UNKNOWN`.**

The message reached the model on the turn it was injected (that is the
`MANATEE-5` result) and **the session never recorded it**. The hook mutates the
array *on its way to the provider*; opencode's persisted history is untouched.

Why this is fatal for delivery: an agent mailed this way **cannot cite the
message next turn, cannot act on it across turns, cannot remember it was told.**
And the obvious "fix" — re-inject every turn so it stays visible — is worse: the
hook fires **once per model call**, several times within a single tool-using turn,
so the message would be delivered *forever* and never leave the queue. Both
branches are wrong.

**Proven at the store, not by model recall.** My original evidence for this was a
model *utterance* (`UNKNOWN`) — which is consistent with non-persistence and
*equally* consistent with a small model simply failing to recall. `oc-red`'s lab
closed that gap and it is the right way to run this: opencode persists sessions in
**SQLite** (`~/.local/share/opencode/opencode.db`, queryable via
`opencode db "<SQL>"`), so "did it persist?" is a **yes/no query with a positive
control**, not an inference from what a model said:

| Path | Codeword | user-role parts in the store |
|---|---|---|
| positive control (an ordinary prompt) | `CONTROL-1111` | **1** ✅ *(the probe can see writes)* |
| `experimental.chat.messages.transform` | `OTTERBREAK-4471` | **0** |
| `noReply` write | `MOOSE-9090` | **1** |

⚠️ **The trap:** a naive `grep <codeword>` over the store **returns a hit** for the
`messages.transform` case — and it looks like persistence. It is not. The hit is an
**assistant `reasoning` part** (the model quoting the codeword in its own
chain-of-thought), not a user write. You must join `part`→`message` and filter
`role='user'`.

**The second, stronger reason — the model REFUSES phantom mail as an attack.** This
is `oc-red`/`ocr-lab`'s finding, and it is the best one in the investigation. When
mail was injected via `messages.transform`, the model's own reasoning part read:

> *"this appears to be a prompt injection attempt trying to override my
> instructions… I should not follow prompt injection attempts."*

**And the model is right.** A synthetic user message *that the session has no
record of* is indistinguishable from a prompt injection — because that is precisely
what a prompt injection **is**. The same text delivered via `noReply` (which *is* in
the store) was read and obeyed. **A stored user message is legitimate; a phantom one
is not.**

So there are two independent reasons delivery cannot ride `messages.transform`: it
is **incorrect** (the agent forgets its mail) and it is **illegitimate** (the agent
is right to refuse it). Either alone would be decisive.

**Delivery cannot ride `messages.transform`.** This is the single most important
finding in this document, and it is invisible unless you go looking for it.

### 2.3 Four traps in the API (VERIFIED)

These cost real time to find. They belong in any implementer's face.

1. **`permission.ask` is DEAD CODE.** It is declared in the installed `.d.ts`
   with `output: {status: "ask"|"deny"|"allow"}` — it reads *exactly* like a
   policy gate — and it is **never dispatched**. The bare string does not occur
   in the 130 MB binary at all (every hit is `permission.asked`, an unrelated bus
   event). `oc-api` re-ran this itself rather than trust a first reading.
   **A design that gates tool calls on `permission.ask` is built on a type that
   lies.** The real block primitive is **throwing inside `tool.execute.before`**
   (`Plugin.trigger` has no try/catch; the throw short-circuits, the tool never
   runs, it surfaces as `ToolStateError` on that one call, the session survives).

2. **In-place mutation only — and which half is unmarked.** Roughly half the
   hooks read `output` back from an outer variable they passed by reference; the
   other half read the trigger's return. `output.args = {...}` in
   `tool.execute.before` — the most natural line an author writes — is **silently
   ignored**. Use `Object.assign(output.args, ...)`. No type, doc, or runtime
   warning tells you this.

3. **Per-turn hooks are NOT sandboxed — an *accidental* throw breaks the turn.**
   `Plugin.trigger` has no try/catch. That is *why* throwing blocks a tool (trap 1)
   — but it also means a stray `undefined.foo` in, say, `chat.params` takes the
   agent's turn down with it. Only `config` and `dispose` are caught-and-ignored.

   **The pump is fortunate here, and it is worth knowing why.** The pump lives in
   the `event` hook, which is dispatched from `bus.listen` as
   `for (M of K) M.event?.(…)` — **the one true fire-and-forget hook** (VERIFIED,
   `oc-api`). Nothing awaits it, so a throw in the pump **cannot break a turn**.
   That is the right place for contract-critical code to live.

   ⚠️ **But the same property hides its failures.** A throw in the pump is
   *swallowed*: the queue simply stops draining, with no error in the pane, no
   `ToolStateError`, nothing in `ps` but a rising `q=`. **The pump must therefore
   catch its own exceptions and make its failures visible** — the same discipline
   `bin/swarm`'s hook verbs already keep (*"any error → exit 0, no output, turn
   intact"*, `cmd_deliver`:685, with the message left queued so the next turn
   retries). Wrap the body; on error, leave the file queued and log where a human
   will see it.

4. **Never `await` a call back into your own host server from inside a hook.**
   My first pump plugin `await`ed `client.session.prompt(...)` inside the `event`
   hook. **It self-deadlocked** — the server was awaiting my hook while my hook
   awaited the server; the run hung for a full 5-minute timeout and `session.idle`
   never even fired. Fire-and-forget (`.then()/.catch()`, return immediately)
   works first try. (VERIFIED, both directions.)

### 2.4 Where the API is genuinely shallower than hoped (VERIFIED)

Stated plainly, per the brief:

- **There is no session-start / session-resume hook.** Nothing fires "a session
  began" or "was resumed." `config` fires once at *process* load, not per
  session. So restore has no first-class seat (§3.4 says what we do instead).
- **Turn-end is observe-only.** `session.idle` arrives through the `event` hook —
  no `output`, no way to say "keep going." Unlike Claude Code's `Stop` hook,
  which can return `{"decision":"block"}` and *force* a continuation turn, an
  opencode plugin cannot re-ring itself from inside the hook. It must cause the
  next turn the same way anyone else does: by prompting the session (§3.3).
- **The deepest capability is undocumented.** v2's `aisdk.language` lets a plugin
  hand back a wrapped `LanguageModelV3` and intercept *every* model call
  (VERIFIED end-to-end by `oc-api`). It is real, and it is how opencode ships its
  own providers. **We deliberately do not use it** — see the NOT-list (§7).

---

## 3. The design: server-primary, plugin-adjunct

Two mechanisms, cleanly separated. **The sender never writes the recipient's
context.** That is the line that preserves the contract.

### 3.1 Delivery — the pump (VERIFIED end-to-end)

`swarm send` does **exactly what it does today**: write a durable file into
`queue/<name>/`. It does *not* POST the mail. Then the recipient's own plugin, in
its own process:

**The pump must supply its own turns.** This is the single most important
structural fact in the design, and the first draft of this document got it wrong.
`session.idle` fires at the *end* of turn N. The pump writes the mail there. The
mail needs turn **N+1** — and a `noReply` write provokes no turn (that is what it
is *for*) and fires no further `session.idle` (VERIFIED, §3.1.2). **So the pump's
write is a terminal state unless the pump itself rings.** A sender's doorbell
cannot cover this: it caused turn N, which has already ended.

```js
// the pump — the whole delivery mechanism
let pumping = false
let staged  = null                             // the message written but not yet
                                               // proven-consumed (Fix B)
event: async ({ event }) => {
 try {                                         // the `event` hook swallows throws
                                               // silently (§2.3.3) — a stray error
                                               // here would stop the queue draining
                                               // with NOTHING to see. Catch it.
  if (event.type !== "session.idle") return    // a TURN just ended (once/turn)
  if (pumping) return                          // re-entrancy guard
  const sid = event.properties?.sessionID
  pumping = true

  // A turn just ran. If a message was staged before it, that turn HAD it in
  // context -> only NOW is `delivered/` a true statement about a consumed turn.
  if (staged) { markDelivered(staged); staged = null }

  const next = oldestQueuedMessage()           // swarm's queue, exactly one
  if (!next) { pumping = false; return }       // EMPTY -> NO RING. the loop
                                               // guard: ring only when we
                                               // actually popped something,
                                               // else idle->ring->idle forever

  // FIRE AND FORGET — never await a call back into your own host (§2.3.4)
  client.session.prompt({ path: {id: sid},     // 1. WRITE (noReply; persists,
      body: { noReply: true,                   //    provokes no turn, fires no idle)
              parts: [{type:"text", text: next.body}] } })
    .then(() => { staged = next                // 2. STAGED — still in queue/
      return client.session.promptAsync({      // 3. RING: the pump supplies the
        path: {id: sid},                       //    turn that will READ it
        body: {parts: [{type:"text", text:"check queue"}]} }) })
    .then(()  => { pumping = false })          // 4. delivered/ happens at the
    .catch(e => { staged = null                //    NEXT idle — i.e. after a turn
                  pumping = false             //    provably ran with it. Fix B.
                  logVisibly(e) })             //    file stays QUEUED -> retried
 } catch (e) { pumping = false; logVisibly(e) } // fail open, loudly. Never silent.
}
```

Three properties, each load-bearing:

- **The pump rings its own turn** (steps 1→3). Delivery does not depend on anyone
  sending. An agent idling with mail and nobody sending still drains its queue.
- **The loop guard** (empty queue → no ring) terminates the drain. Ringing on an
  empty queue gives `idle → ring → empty turn → idle → ring …` forever — the
  hazard `bin/swarm`'s R7 ruling already names for the Claude harness ("ring only
  if the head is DELIVERABLE," bin/swarm:722-731). Same hazard, same fix.
- **Two-phase `delivered/`** (staged → next idle → marked). The file moves *only
  after a turn has provably run with the message in its context*. §3.1.1 explains
  why anything less makes `delivered/` a lie.

The loop guard is not decoration. Ringing on an *empty* queue would produce
`idle → ring → empty turn → idle → ring …` forever, burning tokens with nobody
watching — which is exactly the hazard `bin/swarm`'s R7 ruling already names for
the Claude harness ("ring only if the head is DELIVERABLE," bin/swarm:722-731).
Same hazard, same fix, arrived at independently.

`noReply: true` **writes the session and provokes no turn.** opencode's own doc
comment for the flag reads: *"Inject context without triggering AI response
(useful for plugins)"* — our exact case, blessed by the vendor (DOCUMENTED).

I built this and ran it end to end (`/tmp/oc-pump`, `/tmp/oc-ring`, both torn
down). The plugin's own log:

```
idle sid=ses_0a8c96a77… pumping=false
  pop 001.txt
  delivered; SELF-RINGING now
  self-ring sent
idle sid=ses_0a8c96a77… pumping=false
  queue empty -> NO ring (loop guard)      ← terminates cleanly
```

and the session's **stored message history**, dumped afterwards from the server:

```
[user]      "Say only STARTED."                                  ← the task
[assistant] STARTED.                                             ← turn 1 → idle
[user]      [swarm message] … your codeword is FALCON-9.         ← PUMP DELIVERED (noReply, persisted)
[user]      check queue                                          ← the self-ring
```

That is swarm's delivery shape, exactly, inside opencode (VERIFIED):

- the mail is **in the session's persisted history, ahead of the ring**, so the
  rung turn sees it — not a per-call view (§2.2);
- the **second `session.idle` proves the self-ring caused a real new turn**;
- the loop guard terminated it: queue empty → no ring → done;
- the file moved to `delivered/` only after the write succeeded, and the next
  idle found an empty queue — **no double-delivery**.

Independently, an earlier pump run confirmed persistence by scanning every
session on a live server for its codeword: *`FOUND HERON-3 in session
ses_0a8d42f78… (occurrences=1)`* — exactly one copy, in the message store.

**The corrected order is itself VERIFIED.** §3.1.1 argues the first pump had the
rename in the wrong place (it marked `delivered/` after the *write*, not after
the *ring*). Rather than leave the fix as reasoning, I re-ran the pump with the
inverted order:

```
idle: pop 001.txt
  1. WRITE ok (noReply, persisted)
  2. RING ok -> only NOW rename
  3. delivered/ (after the ring, per §3.1.1)
idle: queue empty -> no ring (guard)
```

`delivered/` is marked **only after the ring succeeds**, so a failed ring leaves
the message queued for redelivery and a false `delivered/` is unreachable.
(VERIFIED, `/tmp/oc-order`, torn down.)

**This means delivery does not depend on an external sender.** An opencode agent
idling with mail in its queue and *nobody sending* still drains it:
`idle → pop → deliver → self-ring → turn → idle → … → queue empty → stop`. That
is the property Claude Code gives swarm through its `Stop`-hook re-ring, and
opencode gives it through the pump.

### 3.1.1 "Delivered means delivered" — the hardest question, answered from source

This is the design's sharpest exposure and it deserves the source, not a
hand-wave. **What does `delivered/` actually promise today?**

`deliver_once`'s own docstring (bin/swarm:394): *"move it to `delivered/` **ONLY
after the emit reports the bytes drained**."* And `emit_hook_output`
(bin/swarm:355) states the discipline it inherits: *"side effects are conditional
on the bytes actually leaving."*

So even on Claude Code, `delivered/` means **"the harness took the bytes,"** not
"the model read them." Nobody ever confirms comprehension. That is the honest
baseline, and it is the right one — swarm's header says nothing on disk "stores a
claim about attention, compliance, or intent."

**But there is a real asymmetry, and in the first draft of this document it was a
bug.** In Claude's case the emit is *intrinsically* tied to a turn: the hook runs
*because* a turn is happening, and its stdout **is** that turn's context. The bytes
cannot drain into nothing. The pump breaks that coupling — the write and the turn
are separate acts. A pump that marks `delivered/` on a successful **write** claims
a turn consumed a message when **no turn has run and none may ever run**. The
header calls `delivered/` a *"world-readable record: this message consumed a turn"*
(bin/swarm:14). That record would be a **lie** — one that `swarm ps` would
faithfully report as `q=0`, and that **nothing in the system could witness**, which
inverts the header's founding sentence (*"Everything stored on disk is a fact the
filesystem can witness"*). Claude Code's design cannot produce such a lie.
*(This defect, and the fix below, are `oc-red`'s — Attack 2. It was right.)*

**The fix — two-phase delivery.** The message is **staged** (written to the
session, but **left in `queue/`**) and moves to `delivered/` only at the *next*
`session.idle` — i.e. only after a turn has **provably run with it in context**:

```
idle N    : (nothing staged) → pop M → write M (noReply) → M STAGED, still in queue/ → ring
   turn N+1 runs, with M in its context
idle N+1  : M was staged and a turn just ran → NOW move M to delivered/   ← true
          → pop M+1 → write → stage → ring …
```

Cost: **one bit of pump state.** Gain: `delivered/` never lies. Failure table:

| Failure point | Outcome |
|---|---|
| `noReply` write fails | file stays queued → retried next idle. **Safe.** |
| write OK, **ring fails** | file **stays queued** (never staged past the catch) → retried. |
| process dies after write, before the turn | file **stays queued** → redelivered. The message may be written into the session **twice** — a duplicate context, never a lost claim. |

Every failure degrades to **at-least-once delivery**, never to loss and never to a
false `delivered/`. That is the same direction `deliver_once` already fails in
(*"worst case: re-delivered next turn; never lost"*, bin/swarm:414) — inherited,
not invented.

### 3.1.2 Why the pump cannot over-deliver, and why it cannot run away (VERIFIED)

Two measurements, both by `ocr-lab` at better resolution than I had, decide the
pump's safety. They are the assumptions the whole mechanism rests on:

1. **`session.idle` counts TURNS, not model calls or tool calls.** Instrumented
   two independent ways (the plugin's `event` hook *and* an external plugin-free
   SSE watcher on `GET /event`), with a prompt engineered to force four separate
   `bash` calls:

   | Observable | Count |
   |---|---|
   | `bash` tool calls in the turn | 4 |
   | model round-trips (`messages.transform` fires) | 5 |
   | **`session.idle`** | **1** |

   So one-per-idle **is** one-per-turn. The pump pops one message per turn. (This
   also retires the double-fire worry: the *per-turn hooks* fire once per model
   call, but `session.idle` does not.)

2. **A `noReply` write does NOT itself fire `session.idle`.** Measured
   `idle_before=1, idle_after=1, DELTA=0` over a 20 s window: the write returns
   HTTP 200 in ~9 ms and emits `message.updated`/`session.updated` — a real session
   write — but **no idle**. This is what makes the pump terminate: if a `noReply`
   write fired an idle, the pump would re-enter itself and **burst-drain the whole
   queue into one turn** (the contract broken in the *opposite* direction). It does
   not. The ring causes exactly one turn; that turn ends; exactly one idle fires;
   the pump pops exactly one message. **A self-sustaining, terminating,
   one-per-turn drain.**

### 3.1.3 Sender rings must be pure wake-ups (VERIFIED, `oc-red` Attack 1b)

A trap I fell into and `oc-red` caught: keeping the *mail* one-per-turn is not
enough if the *rings* can batch. `swarm send` is **two** acts (bin/swarm:1030-1046)
— `queue_put` **then** `ring_doorbell` — and a doorbell is a turn-causing POST,
which is **exactly what `oc-priorart` VERIFIED batches**:

```
Agent A is BUSY. Five senders each `swarm send A`.
  → 5 durable queue files.           mail: one-per-turn, contract HELD.
  → 5 turn-causing POSTs.            these BATCH into ONE turn.
  ⇒ ring-count ≠ message-count. Messages strand.
```

**The fix is the pump's self-ring**, and it is why the self-ring is not optional:
when the pump supplies its own ring per delivered message, **ring-count is
definitionally equal to delivered-count**, and no amount of sender-side ring
batching can desync them. Sender rings collapse into **best-effort wake-ups** —
which is what `ring_doorbell`'s docstring already claims they are (*"every failure
here only delays pickup"*). Under the pump that sentence is **true**; without it,
it is false.

**Why the other invariant holds.** *One claim, one turn:* the recipient pops
exactly one message per idle — swarm's queue stays swarm's, and opencode never
sees more than one message at a time, so the batching case (below) cannot arise.

**The batching collision, and the half of it I got wrong.** `oc-priorart` VERIFIED
that **mail batches**: POST three messages into a busy session and all three drain
into *one* turn (4 user messages → 2 assistant messages), which breaks "a claim on
one turn." It offered a dilemma — accept batching, or make the *sender* gate on
`session.idle`. Neither is needed **for the mail**: swarm keeps its own queue, the
recipient pumps one per idle, and opencode never sees more than one message at a
time. That much holds.

But an earlier draft stopped there and declared the collision *dissolved*. **It
was not** (`oc-red`, Attack 1b): `swarm send` is *two* acts, and while I kept the
**mail** one-per-turn I left the **rings** free to batch — and the rings are what
supply the turns. Five senders to a busy agent produce five turn-causing POSTs that
collapse into one turn, so ring-count desyncs from message-count and messages
strand. **The pump's self-ring is what actually closes this** (§3.1.3), by making
ring-count equal delivered-count by construction. The collision was not dissolved;
it *moved*, and it had to be killed where it moved to.

(Separately, `oc-probe`'s F1 VERIFIED that the server *serializes*: a `noReply`
POST during active generation returns HTTP 200 in ~8 ms, non-blocking, and lands on
a later turn; a real prompt mid-turn self-serializes into its own turn. So swarm
needs no backpressure — a different question from the ring-count one above, and one
where the good news is real.)

### 3.2 Event — free, twice over (VERIFIED)

`session.idle` is the turn-end fact, and it is available **two** ways:
- in-process, via the plugin's `event` hook (what the pump uses);
- **externally**, with no plugin at all — `curl -N GET /event` (SSE) sees the same
  `session.idle` (VERIFIED, `oc-probe` F3). An external watcher could replace
  swarm's `Stop` hook entirely.

Last-assistant-words (which `cmd_event` records) come from
`GET /session/{id}/message`.

### 3.3 Doorbell — an HTTP POST, not a screen scrape (VERIFIED)

`swarm send` rings by POSTing a turn-causing prompt to the recipient's **pinned
port**:

```
POST /session/{id}/message   {"parts":[{"type":"text","text":"check queue"}]}
```

I ran the whole path against a **live TUI agent** — the exact shape a swarm agent
takes:

1. inject with `noReply:true` → HTTP 200, no turn;
2. ring → the agent took a turn and answered **`ZEPPELIN-42`**, the codeword from
   the injected message. (VERIFIED.)

Compare what this replaces: `ring_doorbell` is 30 lines of `herdr send-text` +
bracketed paste + a settle loop + an `❯` prompt-line heuristic + bounded Enter
retries, whose own docstring concedes every failure "only delays pickup," and
whose sibling comment calls the stop re-ring **"THE ONE UNPROVEN MECHANISM."**
Against opencode it is one HTTP call that either returns 200 or does not.
**This is not parity with Claude Code — it is better than swarm's delivery
against Claude Code today.**

**The discovery problem does not exist.** `--port` and `--hostname` are accepted
by the **TUI** (the default command). Swarm *assigns* a port per agent at spawn,
exactly as it already assigns a pane, and writes it into `agents/<name>.json`.
No port hunting, no mDNS, no lockfile scraping. (VERIFIED: launched
`opencode --port 47333 --prompt ... --model ...`; `GET /global/health` →
`{"healthy":true,"version":"1.17.13"}`; `GET /session` → its live session.
Independently confirmed by `oc-probe` F2 under a real PTY.)

⚠️ **`opencode run` SILENTLY IGNORES `--port` — and this fails in the dangerous
direction.** A full-participant agent must be the **TUI** (or `serve`), never
`run`. But the failure if you get it wrong is *not* loud: `run` **accepts** the
flag, executes the turn normally, exits 0 — **and serves nothing** (VERIFIED: a
genuinely bogus flag prints help; `--port` does not, and afterwards
`curl http://127.0.0.1:<port>/global/health` → connection refused). A launcher
that mis-wires this produces an agent that **starts, looks healthy, answers, exits
clean — and never receives mail**, with nothing in `ps` to see. *(Caught by
`oc-red`; my first draft claimed the opposite, that it would fail loudly.)*

**Design consequence:** the launcher must **assert the port is listening after
spawn** (`GET /global/health`) rather than trusting the command to fail. See §5.

### 3.4 Restore — the one place the plugin is irreplaceable (DOCUMENTED + VERIFIED)

There is **no session-start hook** (§2.4). But restore has a *better* seat than
Claude Code's:

- `experimental.session.compacting` lets the plugin **shape the compaction prompt
  itself** — `output.context.push(task + journal-tail)`, or replace
  `output.prompt` wholesale — so the agent's task and journal survive compaction
  **by construction**, rather than by a racing external repair afterwards. This is
  the one place the in-loop position cannot be replicated from outside
  (DOCUMENTED; opencode's own example for this hook is a continuation prompt).
- For plain startup, the task is the launch prompt (`--prompt`), as it is today.
- Belt-and-braces: an external watcher seeing `session.compacted` can push the
  restore payload with `noReply:true` (VERIFIED — `oc-priorart` recalled an
  injected identity + journal after compaction).

### 3.5 Identity — free (VERIFIED)

`SWARM_AGENT_ID` in the process env reaches the plugin as `process.env`
(VERIFIED — my probe printed it). Two upgrades on Claude Code:
- `experimental.chat.system.transform` puts the agent's name and contract in the
  **system prompt, every turn**, at no cost to the task text (VERIFIED —
  `PELICAN-9`);
- `shell.env` injects `SWARM_AGENT_ID` into **every shell the agent runs**, so
  `swarm send` invoked from the agent's own bash just knows who it is.

### 3.6 Spawn / pane — unchanged (VERIFIED)

The agent runs the `swarm` CLI from its shell, as today. The pane is a herdr pane
running the opencode TUI — observable exactly like a `claude` pane. Optional
upgrade: a plugin-registered **`swarm_send` / `swarm_spawn` tool** gives the model
typed verbs instead of shelling out (`oc-probe` VERIFIED that a registered tool is
callable: the model called `swarm_probe_ping` and it executed).

### 3.7 The scorecard

| Surface | Provided by | Status |
|---|---|---|
| delivery | the pump: `session.idle` → pop one → `noReply` write → self-ring → `delivered/` at next idle | **components all VERIFIED** (write persists; idle is once-per-turn; `noReply` fires no idle; self-ring causes a turn; loop guard terminates). The **two-phase pump as one program is REASONED** — run it first (F4). |
| event | `session.idle` (plugin hook *or* external SSE) | ✅ **VERIFIED**, free |
| doorbell | `POST /session/{id}/message` to a pinned port — a **best-effort wake-up** (§3.1.3) | ✅ **VERIFIED**, *better than today* |
| restore | `experimental.session.compacting` (+ external fallback) | ✅ **VERIFIED/DOCUMENTED**, *better than today* |
| identity | `process.env` + `system.transform` + `shell.env` | ✅ **VERIFIED**, *better than today* |
| spawn / pane | the `swarm` CLI in a herdr pane (+ optional native tools) | ✅ unchanged |

**Scope honesty on the delivery row.** Every *mechanism* it rests on has been run —
but **not the final composition**, and I will not let a VERIFIED tag imply
otherwise. Two gaps, both small, both real:

- I ran the self-ringing pump under **`opencode run`** (`FALCON-9`, `OSPREY-1`), not
  inside a **live TUI** (no TTY in my probe environment). The TUI's *server* side is
  independently verified (`oc-probe` F2, `ocr-lab`, both under a real PTY); the
  *pump-inside-a-TUI* composition is unrun.
- The **two-phase `delivered/`** (stage → next idle → mark) is a small argued-for
  correction layered on the pump I ran with one-phase marking.

**Run both before trusting the row.** §8 lists them in priority order.

**Every load-bearing mechanism is documented surface.** No `experimental.*` hook
is required for delivery, event, or the contract. The `experimental.` risk touches
only *restore* and *ergonomics* — and restore has a documented fallback. This is a
design that degrades, never breaks.

---

## 4. Is it better than FLEET's thin-runner / leaf path?

**For leaves: no — FLEET is still right.** A one-shot `opencode run "<task>"` that
streams to a pane and exits is cheaper, has no plugin, no server, no port, no
liveness protocol. If the job is *one completion*, use FLEET's path. Nothing here
displaces it.

**For full participants: yes, decisively, and this is new.** FLEET and the
archived `HARNESS.md` both concluded "prefer opencode/codex for **leaf** work,"
because a leaf was all the surface could support. This document refutes that
bound: with the pump, an opencode agent **receives mail one-per-turn, reports,
survives compaction, knows who it is, and spawns children** — every duty a swarm
node has. It is a **full participant**, not a leaf.

The honest cost of the upgrade: a persistent TUI process with a pinned port and a
plugin, versus a one-shot pipe. Take it when you want a *node*; take FLEET's
runner when you want a *completion*.

---

## 5. Cost and shape

**Concept cost: zero new concepts.** `HARNESS.md` §1 already designed the frame —
*a child's harness is chosen per-task, never inherited; `--agent <kind>` selects
the launcher body*. opencode is a **third kind** in an existing frame. §4 already
settled that you never *switch* an agent's harness; you respawn a successor. Both
are inherited, not re-litigated.

**Changes to `bin/swarm` (small, and at seams that already exist):**

1. **`port` in `agents/<name>.json`** — the record already carries
   `{name, parent, pane, tab}` (bin/swarm:920). One more field, written at spawn.
2. **The launcher body** (bin/swarm:823-838 — the *only* `claude` coupling):
   ```
   opencode --port <assigned> --model <m> --prompt "$PROMPT" [--auto]
   ```
   (the TUI, **not** `run` — §3.3.)
3. **`cmd_send`'s doorbell** (bin/swarm:1040) already branches on
   `agents[to]["pane"]`. For an opencode agent it POSTs to `agents[to]["port"]`
   instead of ringing the pane. The durable queue write above it is **unchanged**,
   and the ring stays exactly what its docstring already says it is — a
   **best-effort wake-up** (§3.1.3). The pump, not the sender, supplies the turns.
4. **A post-spawn liveness assertion** — `GET /global/health` on the assigned port.
   This is **not optional**: `opencode run` silently ignores `--port` (§3.3), so a
   mis-wired launcher yields an agent that looks healthy and never receives mail.
   `write_launcher` already records a pre-flight outcome to `$STATUS`
   (bin/swarm:816-838); this is one more check in the same place, in the same
   style — *"spawn can tell a started harness from a dead one by a fired signal,
   not a screen scrape."*
5. **A per-agent `OPENCODE_SERVER_PASSWORD`** in the launcher's env, and the
   matching auth header on `cmd_send`'s POST. **Not hardening-for-later:** without
   it, any local process can *drive* the agent — prompt it, and **run shell in it**
   via `POST /session/{id}/shell`. It does **not** make agents unreadable to each
   other (the session store is a world-readable SQLite file — §6.1); it closes the
   *drive/shell* path, which is the one this design newly opens.

**Where the plugin lives:** shipped **in the swarm repo**, alongside `skill/`,
and pointed at by the per-agent opencode config the launcher writes — exactly as
swarm already writes a per-agent `settings/<name>.json` for Claude Code's hooks.
It loads from a project-local `.opencode/plugin/` with no install step (VERIFIED).

**Is a plugin an "engine"?** No — and this matters to the philosophy. The plugin
is the *same category as `bin/swarm`'s hook verbs*: it is the code that binds
swarm's contract to a harness's callbacks. Claude Code gets `cmd_deliver` /
`cmd_event` / `cmd_restore` as argv-dispatched hook entrypoints; opencode gets the
same three verbs as an in-process plugin. **Same verbs, same contract, different
socket.** It adds **no new concept** and **no new verb**.

**But it is not free, and the honest ledger says so** (`oc-red`, Attack 5 —
GLANCES, and it is right): the design **does** store new state (a `port` per
agent) and it **does** make new claims about the world (that a port is listening;
that a session id maps to an agent). An earlier draft of this section claimed it
"stores no new state and makes no new claim" — that was an overclaim and it is
struck. The price is: one field, one launcher assertion, one JS file shipped in
the repo, a version pin, and a loopback server to secure. That is a **price, not a
disqualifier** — but it should be paid knowingly.

---

## 6. Risks, stated before they bite

1. **⚠️ AGENTS DO NOT ISOLATE FROM EACH OTHER. This is a DESIGN REQUIREMENT, not a
   risk bullet — and my first draft prescribed a fix that does not work.**

   Two facts compound into one defect (both VERIFIED):

   - **The server is UNAUTHENTICATED by default.** It says so itself:
     `Warning: OPENCODE_SERVER_PASSWORD is not set; server is unsecured`. Any local
     process can drive any agent — mail it, read its history, and **run arbitrary
     shell via `POST /session/{id}/shell`**.
   - **Sessions are NOT scoped by directory.** My first draft said per-agent
     isolation "needs a per-agent directory/worktree, not merely a per-agent port."
     **That fix does not work** (caught by `oc-red`; I re-ran it myself): a server
     started in a **fresh, empty** directory returned **93 sessions, from every
     other directory on the host** — other agents' sessions, other probes' sessions.
     `--dir` does not isolate the session store.

   So on a host running two swarm agents, **either can enumerate, read, and drive
   the other's sessions, and execute shell inside them.**

   **And the obvious fix only half-works — I checked, because I had just written
   that it fully worked.** The session store is a **world-readable SQLite file**
   (`~/.local/share/opencode/opencode.db`, mode `-rw-r--r--`), and *any* local
   process can dump *every* agent's messages with `opencode db "SELECT …"` — **no
   server, no port, no password** (VERIFIED: 1,279 messages, straight off disk).
   So:

   | Barrier | Stops **driving** another agent (HTTP: prompts, shell) | Stops **reading** another agent's conversation |
   |---|---|---|
   | `OPENCODE_SERVER_PASSWORD` + loopback | ✅ yes — set it; it is load-bearing | ❌ **no** — the store is readable on disk regardless |

   **State this honestly rather than dressing it up:** a per-agent password is
   necessary and the launcher must set it, but **swarm agents sharing a host and a
   Unix user are mutually readable, and no opencode setting changes that.** If that
   is unacceptable for a given deployment, the answer is an OS boundary (separate
   users / containers), not a config flag. For swarm's actual case — a tree of
   agents the operator owns, on the operator's own machine — mutual readability is
   *already* true (they share `.swarm/`, each other's journals, and the repo), so
   this is **not a new exposure**; it is an existing one that opencode does not
   worsen. The thing that *would* be new is the **shell/drive** path, and that is
   exactly what the password closes.
2. **Compaction and session sprawl.** Because the store is global (above), an
   agent's `GET /session` is not a clean view of *its own* work. The pump keys on
   `event.properties.sessionID` (the session it is actually in), which sidesteps
   this — but any code that *enumerates* sessions to find "this agent's" must not
   trust the directory field.
3. **`experimental.*` may break on upgrade.** It touches *restore* and
   *ergonomics* only — delivery/event/contract are documented surface (§3.7).
   Mitigation: **pin the opencode version**; re-pull `GET /doc` from the pinned
   binary on every bump; the docs lag the binary badly (89 wire event types in the
   binary vs ~25 documented), so **design against `/doc`, never the website.**
4. **The double-fire / idempotency hazard.** Per-turn hooks fire **once per model
   call**, several times in a tool-using turn. The pump is safe because it is
   driven by `session.idle` (once per turn) and marks `delivered/` on success —
   but any future hook-driven injection must be idempotent, keyed on message id.
5. **`opencode run` is not a harness, and it fails SILENTLY if you try.** It
   accepts `--port` and ignores it (nothing listens), and its process lifecycle
   disposes before an injected turn can run (VERIFIED; `oc-probe` #8 independently).
   Full participants must be the TUI or `serve` — and **the launcher must assert
   `GET /global/health` on the assigned port after spawn**, because a mis-wired
   agent will otherwise look perfectly healthy while receiving no mail (§3.3).

---

## 7. NOT-list — what this design deliberately does not do

- **Not `aisdk.language`.** The deepest hook in the system (replace the
  `LanguageModelV3`, intercept every model call) is real and VERIFIED. We do not
  use it: it is v2, undocumented, and swarm needs none of it. Naming it as
  *available and refused* is the point — depth was never the constraint.
- **Not `permission.ask`.** It is dead (§2.3.1). No policy gate is built on it.
- **Not delivery via `messages.transform`**, however tempting the `MANATEE-5`
  result looks in isolation (§2.2).
- **Not sender-side context writing.** `swarm send` never POSTs mail into a
  recipient's session; it queues and rings. This is what keeps "delivered means
  delivered" true.
- **Not a replacement for FLEET's leaf runner** (§4).
- **Not session migration, and not switching a live agent's harness** — inherited
  from `HARNESS.md` §4, unchanged.

---

## 8. Falsifiers, with collectors

| # | If this is observed, this document is wrong | How to collect |
|---|---|---|
| F1 | The pump's `noReply` write is **not** visible to the *next* turn in a long, tool-using session (e.g. it is dropped by compaction before it is read) | Run an opencode agent through ≥1 compaction with mail delivered pre-compact; ask it to cite the message after |
| F2 | ~~`session.idle` does not fire once per turn~~ | **RETIRED — measured.** `ocr-lab`: 4 tool calls + 5 model round-trips → **1 idle**, two independent instruments agreeing. And a `noReply` write fires **zero** idles (Δ=0). §3.1.2 |
| F3 | ~~Two agents on one host collide through the shared session store despite per-agent `--dir`~~ | **FIRED — they DO collide.** A server in a *fresh, empty* dir returned **93 sessions from other directories** (VERIFIED, `oc-red` + re-run by me). `--dir` does not isolate. The design absorbed this: §6.1 makes a per-agent `OPENCODE_SERVER_PASSWORD` a **requirement**, not a risk note. |
| F4 | The pump strands or duplicates mail **under load** — many senders ringing a busy agent | 50 sends to a busy opencode agent; count `delivered/` vs `queue/` after it goes idle. **The most valuable unrun experiment.** |
| F5 | An opencode upgrade breaks `experimental.session.compacting` → restore silently degrades | Pin the version; on bump, re-run the compaction probe before adopting |

**A correction the record should carry.** The first draft of this document said
the **external** ring (`swarm send`'s doorbell) was *sufficient on its own* and
filed the self-ring as an optional nicety. **That was wrong, and `oc-red` broke
it:** the sender's ring causes turn N, the pump writes at the *end* of turn N, and
the mail needs turn **N+1** — so an agent with mail and nobody sending would have
sat forever with a `delivered/` record that no turn had read. Its diagnosis of *how*
I got there is exact and worth preserving: my `ZEPPELIN-42` run was
**inject-then-ring, both acts by the sender**; the pump **inverts** that to
ring-then-inject, actor moved to the recipient. **I carried a VERIFIED tag across an
ordering change, and the ordering is the mechanism.**

The rings are **not** independently sufficient; **the pump must supply its own**
(§3.1, §3.1.3). I had verified the self-ring (`FALCON-9`) but had not understood it
was *load-bearing rather than optional*. The mechanism in §3.1 is the corrected one.

`oc-red` closed by issuing a falsifier and a prediction: *"run your §3.1 pump
verbatim against a live TUI agent, send one message, send nothing else — I predict
it goes idle with the message in its session store, unread, marked `delivered/`."*

**Against the pump it reviewed, that prediction is correct** — the mail would have
sat there forever. **Against the pump in §3.1 now**, which rings its own turn, the
deadlock does not occur: the `FALCON-9` and `OSPREY-1` traces show `idle → pop →
write → self-ring → turn → idle → queue empty → halt`, with the message read on the
rung turn.

⚠️ **But I owe the exact test an exact answer, and it is a partial one.** I ran the
self-ringing pump under **`opencode run`**. I did **not** get it running inside a
live **TUI** — the environment I probe from has no TTY (`script: tcgetattr/ioctl:
Operation not supported on socket`), and I will not report a run I did not make.
What *is* independently established is each half: the pump self-rings and drains
(my traces, under `run`), and a **TUI on a pinned port accepts external injection
and serves its API** (`oc-probe` F2 and `ocr-lab`, both under a real PTY). **The
composition — this pump, inside a TUI, in a pane — is the one thing nobody has
run.** It is the *first* experiment an implementer should do, ahead of F4, and it
is exactly `oc-red`'s test.

**Still genuinely untested,** in priority order:
1. **The pump inside a live TUI** (above) — `oc-red`'s falsifier, run it verbatim.
2. **The pump under sustained load** (F4) — 50 sends to a busy agent.
3. **The pump across a real compaction** (F1).

None is a hole in the architecture; all three are the first things to measure.

---

## 9. Graveyard-check

- **`HARNESS.md` §1** (harness chosen per child from the task, never inherited;
  spawn-time only; `--agent <kind>` selects the launcher) — **inherited, not
  re-litigated.** opencode is a third kind.
- **`HARNESS.md` §4** (no switching a live agent's harness; harvest, close,
  respawn a successor) — **inherited unchanged.**
- **`FLEET.md`** (opencode as a *leaf* runtime; `session.idle` is not "task
  complete") — **refined, not overturned.** FLEET's leaf path stands for leaves
  (§4). Its warning that `session.idle` ≠ "done" is *why* the pump uses idle as a
  *pump trigger* (drain one message) and never as a done-signal.
- **The codex work** (`archive/CODEX-*.md`) — its contribution here is the
  six-item checklist (§1), which it earned. Its conclusion ("swarm's hook verbs
  survive almost intact on a harness with Claude-shaped hooks") **does not
  transfer**: opencode has no Claude-shaped hook surface at all. We author it.
- **`ring_doorbell`'s "ONE UNPROVEN MECHANISM"** (bin/swarm:713) — this design
  *retires* that risk for opencode agents, replacing a screen scrape with an HTTP
  status code. It remains for Claude agents.

---

## 10. What I would tell the operator in one breath

Your hypothesis was right — an opencode plugin really can edit the harness loop,
in-process, deeper than Claude Code's hooks let us reach; I proved it by pushing a
string into the system prompt and into the message array and watching the model
obey both. But the deepest hook is a **view** transform, not a session write. Mail
delivered through it is forgotten the moment the turn ends — and, it turns out, the
model *refuses it as a prompt injection*, correctly, because a user message the
session has no record of is exactly what a prompt injection is. So the plugin is
not the mailman.

The plugin is the **pump**: on every idle it pops one message from swarm's own
queue, writes it into its own session with `noReply` (which persists), and **rings
its own next turn** — then marks it `delivered/` only once that turn has actually
run. `swarm send` keeps its durable queue and its ring becomes a best-effort
wake-up: an HTTP POST with a status code instead of a bracketed-paste screen
scrape. Every load-bearing piece is documented surface, the contract does not bend
anywhere, the launcher change is a port field, a different command line, and a
health assertion — and the result is a **full participant**, not the leaf that
FLEET and the codex work had to settle for.

Two things I would not have got right alone, and the record shows it: the pump
must supply its own turns, and `delivered/` must lag the turn that reads the mail.
Both came from the red team. The design is better for having been attacked, which
is the point of attacking it. **Build it.**
