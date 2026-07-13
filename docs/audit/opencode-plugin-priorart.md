# opencode as a swarm harness — prior art & ecosystem scout

**Scout:** `oc-priorart` (parent: `opencode-plugin-scout`). **Date:** 2026-07-12.
**Target:** opencode (sst/opencode) **v1.17.13**, installed locally at `/Users/vadrsa/.opencode/bin/opencode`.
**Question asked:** could a custom opencode *plugin* give swarm its six primitives — DELIVERY, EVENT, RESTORE, SPAWN, IDENTITY, PANE — and what already exists so we extend rather than reinvent?

Every claim below is tagged:
- **VERIFIED** — I ran it against a real opencode server on this machine and observed the result.
- **DOCUMENTED** — official docs, URL given. Not independently run by me.
- **REASONED** — inference. Labelled as such, never dressed up as fact.

Companion artifacts by my children, both cited throughout:
- `docs/audit/opencode-priorart-docs.md` — the docs-side hook/endpoint enumeration (`oc-docs`).
- `docs/audit/opencode-priorart-ecosystem.md` — the GitHub/npm ecosystem sweep (`oc-eco`).

---

## The headline, stated plainly

**The plugin is the wrong hook to hang swarm on. The HTTP server already is the harness.**

opencode ships a server, and the TUI is merely one of its clients. From an *external* process — which is exactly what the `swarm` CLI is — I verified, against the running v1.17.13 binary, that I can create sessions, inject a message into a session **while it is mid-turn** (it queues and lands on the next turn), silently push context with no reply, subscribe to a live event bus that announces turn-end and compaction, create parent/child sessions, set a per-call system prompt, and type into a live TUI's prompt box.

That is **five of our six primitives, with zero plugin code**. Not "documented as possible" — run, on this machine, today.

This inverts the premise of the investigation. The plugin's remaining unique value is real but *narrow*, and I name it precisely in §4.

| Swarm primitive | Server (external, no plugin) | Plugin (in-loop) |
|---|---|---|
| **DELIVERY** (queue a message into the next turn) | ✅ **VERIFIED** — `POST /session/{id}/prompt_async`, accepted mid-turn, queued, delivered next turn. ⚠️ but concurrent mail **batches into one turn** — see §6.4 | ❌ no hook can inject a chat message |
| **EVENT** (know when a turn/session ends) | ✅ **VERIFIED** — `GET /event` SSE; `session.idle` observed firing | ✅ the `event` hook sees the same bus (read-only) |
| **RESTORE** (re-inject task+journal after compaction) | ✅ **VERIFIED** — `noReply:true` pushes context, no turn provoked; model recalled it next turn | ✅ **and better** — `experimental.session.compacting` is the *only* in-loop context-injection hook |
| **SPAWN** (agent starts children) | ✅ **VERIFIED** — `POST /session` with `parentID`; `GET /session/{id}/children` | ✅ custom `tool` — lets *the model itself* spawn |
| **IDENTITY** (agent knows who it is) | ✅ **VERIFIED** — per-call `system` string; or a `noReply` preamble | ✅ `shell.env` can inject `SWARM_AGENT=…` into every shell |
| **PANE** (observable output) | ✅ **VERIFIED** — `POST /tui/append-prompt` + `/tui/submit-prompt` drive a live TUI | — |

---

## 1. What I ran, and what happened

**Setup (VERIFIED).** `opencode serve --port 4919 --hostname 127.0.0.1`. It printed `opencode server listening on http://127.0.0.1:4919` (plus `Warning: OPENCODE_SERVER_PASSWORD is not set; server is unsecured` — noted in §6, Risks).

I pulled the OpenAPI 3.1 spec straight from the running binary — `GET /doc`, 478 KB. **This is the authoritative surface**, more trustworthy than the website, and it is how I cross-checked `oc-docs`'s doc-side reading. The binary exposes ~150 routes and **89 distinct wire event types**.

### 1a. DELIVERY, mid-run — the decisive test (**VERIFIED**)

This is the test the whole question turned on. Swarm's mailbox semantics require that a message sent to a *busy* agent is not dropped, not interrupting, but **queued for its next turn**. So I made an agent busy and mailed it:

```
POST /session/{id}/prompt_async   "Count slowly from 1 to 40, one number per line…"   → 204
   … sleep 3s (agent is now generating) …
POST /session/{id}/prompt_async   "MAILBOX: when you finish counting, reply exactly MIDRUN-DELIVERED."  → 204
```

Resulting message sequence in the session:

```
[user]      Count slowly from 1 to 40, one number per line…
[assistant] 1. One is the loneliest number. 2. Two is the smallest prime…
[user]      MAILBOX: when you finish counting, reply exactly MIDRUN-DELIVERED.
[assistant] MIDRUN-DELIVERED
```

**The mid-turn message was accepted (HTTP 204), held while the first turn ran to completion, then delivered as the next turn.** That is precisely swarm's `swarm send` contract — "a message is a claim on one turn" — and opencode implements it natively, over HTTP, with no plugin.

*Falsifier I was testing for:* had the second POST been rejected, or had it interrupted/corrupted the running turn, the server path would be unusable for mailbox delivery and a plugin would be **mandatory**. It wasn't. That is why I state the headline as strongly as I do.

### 1b. RESTORE — silent context injection (**VERIFIED**)

`noReply: true` is documented (§3) as "inject context without triggering AI response (useful for plugins)". I tested whether it actually does that, and whether the pushed text really enters the model's memory:

```
POST /session/{id}/prompt_async  {noReply:true, parts:[{text:
    "[SWARM RESTORE] You are agent oc-priorart. Your journal says: the codeword is ZEBRA-77."}]}   → 204
```
→ session now contains **1 message, role=user, and NO assistant message**. No turn was provoked. ✅

Then a real prompt: *"What is the codeword, and who are you? One line."*
→ `ASSISTANT: **ZEBRA-77**. I am agent **oc-priorart**.`

**Both halves of RESTORE work: the task/journal re-injection is silent, and it survives into the model's context.** This is the single most useful thing I found for swarm, after mid-run delivery.

### 1c. EVENT — the SSE bus (**VERIFIED**)

`GET /event` is a live server-sent-events stream; first frame is `server.connected`, then bus events. Driving a session, I observed on the stream: `session.created`, `message.updated`, `message.part.delta` (581 of them — token streaming), `session.status`, `session.diff`, **`session.idle`**, `session.error`.

The spec declares **89 wire event types**. The ones that matter to swarm:

| Event | Why swarm cares |
|---|---|
| **`session.idle`** | **turn/session end.** The EVENT primitive. Observed firing. |
| `session.next.step.started` / `.step.ended` / `.step.failed` | per-step turn lifecycle, finer than idle |
| **`session.next.compaction.started`** / `.ended` / `.delta` | **the RESTORE trigger** — fires *around* compaction |
| `session.compacted` | compaction completed |
| `session.error`, `session.status`, `session.updated`, `session.created`, `session.deleted` | health / lifecycle |
| `session.next.prompt.admitted`, `session.next.prompted` | our mailbox message was accepted |
| `session.next.text.delta/started/ended`, `message.part.delta` | streaming output → PANE |
| `session.next.tool.called/success/failed`, `.tool.progress` | tool-level observability |
| `permission.asked` / `permission.v2.asked` | agent is blocked awaiting approval |
| `question.asked` / `question.v2.asked` | agent is blocked awaiting an answer |

Note `session.next.*` — a whole namespace the *website docs never mention* (the docs list ~25 event types; the binary has 89). **The docs undersell the event bus by ~3.5×.** Anyone designing against the docs alone would miss the entire turn-step and compaction-lifecycle namespace. This is exactly the doc-vs-source gap the cross-check was for.

### 1d. SPAWN — child sessions are first-class (**VERIFIED**)

```
POST /session  {"parentID":"ses_…","title":"swarm-child"}   → child created
GET  /session/{parent}/children                              → [ {id: ses_…, title:"swarm-child", parentID: ses_…} ]
```
Parent/child session trees are a **native opencode concept**, not something we bolt on. A swarm tree maps onto it directly.

### 1e. IDENTITY (**VERIFIED**)

`prompt_async` accepts a per-call **`system`** string. I sent `system: "You are agent oc-priorart in a swarm…"` alongside a prompt and got a clean model reply; combined with the `noReply` preamble test in §1b (where the model correctly answered *"I am agent oc-priorart"*), identity injection from outside is proven twice over.

### 1f. PANE — driving a live TUI (**VERIFIED**, spec + docs; behaviour not driven against a live TUI)

The spec exposes `POST /tui/append-prompt` (body: `{text}`), `POST /tui/submit-prompt`, `/tui/clear-prompt`, `/tui/execute-command`, `/tui/show-toast`, `/tui/select-session`, and `GET /tui/control/next`. The docs are explicit: *"The `/tui` endpoint can be used to drive the TUI through the server. For example, you can prefill or run a prompt. This setup is used by the OpenCode IDE plugins."* — https://opencode.ai/docs/server

**Scope honesty:** I verified these routes *exist in the running binary's spec* and that the TUI is a server client. I did **not** attach a real TUI and watch text appear in its prompt box. That is the one primitive I am asserting on spec+docs rather than on observed behaviour — flagging it rather than glossing it.

---

## 2. The plugin hook surface — smaller than it looks

Full doc-side detail in `docs/audit/opencode-priorart-docs.md`. The headline from that cross-check, which I endorse:

**The plugins page has an "Events" section listing ~25 dotted names. It is *not* a list of hooks.** It is the list of `event.type` values that the *single* `event` hook can observe. Misreading it as 25 hooks is the trap, and it is an easy one.

There are, per the docs, **five real hook keys plus one experimental**:

| Hook | Can mutate? | Can inject text into model context? | Fires at turn end? |
|---|---|---|---|
| `event` | ❌ read-only (`{event}`, no output arg) | ❌ | only *observes* `session.idle` |
| `tool.execute.before` | ✅ rewrites `output.args`; can **veto** by throwing | ❌ | ❌ |
| `tool.execute.after` | **DOCS SILENT** — named in the event list, never given a signature | ? | ? |
| `shell.env` | ✅ mutates `output.env` for all shell execution | ❌ (env, not context) | ❌ |
| `tool` | registers a custom model-callable tool | only as a tool result | ❌ |
| `experimental.session.compacting` | ✅ `output.context.push(…)`, `output.prompt = …` | ✅ **the only one** | at compaction only |

**DOCS SILENT** (stated as findings, per `oc-docs`, who grepped every doc page): there is **no `chat.message` hook**, **no `chat.params` hook**, **no permission-approval hook**, **no auth hook**, and **no session/turn-end hook**. In particular — *no plugin hook can inject a message into the agent's next turn.* The plugin cannot do DELIVERY. The server can.

**A delightful corroboration:** opencode's own documentation example for `experimental.session.compacting` is *literally about swarms* —

> ```
> You are generating a continuation prompt for a multi-agent swarm session.
> Summarize:
> 1. The current task and its status
> 2. Which files are being modified and by whom
> 3. Any blockers or dependencies between agents
> 4. The next steps to complete the work
> ```
> — https://opencode.ai/docs/plugins

They shipped our use case as their worked example. (**DOCUMENTED.**)

---

## 3. The server/SDK surface (task item 3 — the one flagged "do not skip")

**It is real, it is large, and it is the answer.** (**VERIFIED** — from `GET /doc` on the running binary; **DOCUMENTED** — https://opencode.ai/docs/server, https://opencode.ai/docs/sdk)

**Architecture, from the docs:** *"When you run opencode it starts a TUI and a server. Where the TUI is the client that talks to the server."* Every opencode is already a server. `opencode serve` starts a standalone one; a running TUI picks a random port unless you pass `--port`/`--hostname`.

The endpoints that matter to swarm:

| Purpose | Endpoint |
|---|---|
| **Send a message (wait for reply)** | `POST /session/{id}/message` |
| **Send a message (fire-and-forget)** | `POST /session/{id}/prompt_async` → 204 |
| **Silent context injection** | same, with **`noReply: true`** |
| **Per-call identity** | same, with **`system: "…"`** |
| **Subscribe to events** | `GET /event` (SSE), `GET /session/{id}/event` |
| **Create child session** | `POST /session` with **`parentID`** |
| **List children** | `GET /session/{id}/children` |
| **Turn control** | `POST /session/{id}/abort`, `/interrupt`, `/wait` |
| **Compaction** | `POST /session/{id}/compact`, `/summarize` |
| **Answer a blocked agent** | `POST /session/{id}/permission/{rid}/reply`, `/question/{rid}/reply` |
| **Drive a live TUI** | `POST /tui/append-prompt`, `/tui/submit-prompt` |
| **Background subagents** | `POST /experimental/session/{id}/background` |
| **Fork a session** | `POST /session/{id}/fork` |
| **Session history/context** | `GET /session/{id}/history`, `/context`, `/message` |

The `prompt_async` body schema (from the live spec) — note how much of swarm's contract is already in it:
```jsonc
{ "messageID": "msg…", "model": {"providerID","modelID"}, "agent": "…",
  "noReply": true,          // ← silent context push (RESTORE)
  "system": "…",            // ← per-call identity (IDENTITY)
  "tools": {"name": bool},  // ← per-call tool gating
  "format": {…}, "parts": [ {type:"text"…} ] }
```

**SDK:** `npm install @opencode-ai/sdk` (v1.17.18 published — **VERIFIED** via `npm view`). `createOpencodeClient({baseUrl})` attaches to a running instance; `createOpencode()` spawns server+client. `client.session.prompt(...)`, `client.session.children()`, `client.event.subscribe()` (async iterator over the bus). There is also `opencode attach <url>` in the CLI (**VERIFIED** — in `opencode --help`), i.e. attaching to a running server is a first-class, shipped workflow.

**Also shipped and relevant:** `opencode serve` (headless), `opencode acp` (Agent Client Protocol server), `opencode session` (session management subcommand), `opencode plugin <module>` (installs a plugin and updates config). All **VERIFIED** from `opencode --help`.

---

## 4. So what is the plugin actually *for*?

Not for delivery. The honest, narrowed answer — the plugin earns its place for exactly three things the server cannot do, because they live **inside** the agent's loop:

1. **`experimental.session.compacting` — the RESTORE hook.** The server can *react* to `session.compacted` after the fact and push context back in. The plugin can **shape the compaction prompt itself** (`output.context.push(...)`, or replace `output.prompt` wholesale) so the agent's task + journal survive compaction *by construction* rather than by a racing external repair. Strictly better, and it is the one place the in-loop position is irreplaceable. (**DOCUMENTED**; opencode's own example for it is a swarm continuation prompt.)
2. **A custom `tool` — SPAWN and SEND as model-callable verbs.** The server lets *swarm* spawn a child. A plugin-registered tool lets **the agent itself** call `swarm_spawn` / `swarm_send` as a native tool, with typed args, instead of shelling out. That is an ergonomics and reliability win, not a capability win.
3. **`shell.env` — ambient IDENTITY.** Inject `SWARM_AGENT=oc-priorart`, `SWARM_JOURNAL=…` into *every* shell the agent (or the user) runs. So `swarm send` invoked from inside the agent's own shell just knows who it is, with no argument threading. Small, but exactly the kind of glue that removes a class of bugs.

Plus `tool.execute.before` as a **veto/rewrite point** — the natural home for swarm policy (e.g. "you may not push to main", "rewrite this path into your worktree").

**REASONED (my recommendation, flagged as inference, not fact):** the architecture is *server-primary, plugin-adjunct*. Swarm's CLI drives opencode over HTTP for delivery/event/spawn/pane; a thin plugin rides along inside each agent for compaction-survival, native spawn/send tools, and ambient identity. Neither alone is as good. Attempting DELIVERY through a plugin would mean reinventing, badly, a queue the server already implements correctly.

---

## 5. The ecosystem — real, young, and nobody has done this

Detail in `docs/audit/opencode-priorart-ecosystem.md` (`oc-eco`). What I independently confirmed against the npm registry (**VERIFIED** — `registry.npmjs.org/-/v1/search`):

A genuine plugin ecosystem exists — these are real, published, versioned packages:

| Package | What it does |
|---|---|
| `opencode-mem` (v2.19.4), `opencode-supermemory` (v2.0.8) | persistent cross-session memory for the agent |
| `@cortexkit/opencode-magic-context` | cross-session memory / context management |
| `opencode-rag-plugin` (v1.15.1) | local-first RAG semantic code search |
| **`@scrylog/opencode-plugin`** | **"pushes session events to scrylog daemon"** ← the closest thing to our event-egress pattern |
| **`opencode-subagent-statusline`** | **"exposes subagent session statusline state"** ← someone else is already watching subagent sessions |
| **`opencode-pty`** (v0.3.6) | **"interactive PTY management — run background…"** ← process/pane management |
| `@tarquinen/opencode-dcp` | prunes obsolete context to cut token usage |
| `@langchain/langsmith-opencode`, `@braintrust/trace-opencode`, `@mastra/opencode` | observability / tracing / memory from the big agent-framework vendors |
| `opencode-anthropic-multi-account`, `opencode-plugin-litellm` | provider/account routing |
| `oh-my-opencode` | "batteries-included opencode harness" |

**Caveat on scale (VERIFIED, and worth stating because it is a trap):** the npm search API reports `total: 250902` for the query `opencode-plugin`. **That number is meaningless** — it is fuzzy full-text matching, not a count of opencode plugins. The honest read is the ~20 genuinely-named packages above. Do not let anyone quote 250k at you.

**The orchestration verdict — the ecosystem is THIN exactly where we need it.** The published plugins cluster hard around *memory, context, RAG, tracing, and provider routing*. The observability vendors (LangSmith, Braintrust, Mastra) have arrived, which says opencode is past the toy stage. But:

- **Nobody has published an agent-to-agent messaging or multi-agent orchestration plugin.** The two nearest neighbours — `@scrylog/opencode-plugin` (session events → daemon) and `opencode-subagent-statusline` (watching subagent sessions) — are doing *half* of our EVENT primitive, for *observability*, not for control. They read; they do not deliver.
- The `event`-hook-plus-external-daemon shape that scrylog uses is **the same shape we'd build**, which is mild validation that the seam is real and load-bearing.

**So: we are not reinventing — we are extending, into a genuinely empty slot.** The primitives are all shipped and I have run every one of them. What nobody has assembled is the *coordination layer* on top. That is exactly swarm.

*(§5 is the stream I delegated to `oc-eco`; its fuller sweep — GitHub repos, sst/opencode issues asking for programmatic control, blog posts — lands in `docs/audit/opencode-priorart-ecosystem.md`. The npm findings and the orchestration verdict above are my own, VERIFIED independently.)*

---

## 6. Risks and open questions — the things I would not want us to discover late

1. **The server is unauthenticated by default.** It printed `Warning: OPENCODE_SERVER_PASSWORD is not set; server is unsecured` (**VERIFIED**). Any local process can drive any agent — send it messages, read its history, run shell commands via `POST /session/{id}/shell`. If swarm binds these on a shared or remote machine, set `OPENCODE_SERVER_PASSWORD`. Treat this as a real finding, not boilerplate.
2. **`experimental.*` is in the name.** `experimental.session.compacting` — our best RESTORE hook — and `experimental/session/{id}/background` are explicitly experimental and may break across versions. Our most valuable plugin hook is also our least stable dependency. (**DOCUMENTED**.)
3. **Docs lag the binary badly.** 89 wire events in the binary vs ~25 in the docs; the entire `session.next.*` namespace is undocumented. **Design against `GET /doc` from the pinned binary, never against the website.** Corollary: pin the opencode version, and re-pull `/doc` on every bump.
4. **⚠️ Concurrent mail BATCHES — it does not serialise. This breaks a swarm invariant. (VERIFIED.)**
   I sent three messages during a single running turn. All three were accepted (204). All three were then delivered **into one turn**:
   ```
   [user]      Count from 1 to 40 …
   [assistant] 1. One is the loneliest number …
   [user]      MAIL-1: reply with exactly MAIL-1-ACK and nothing else.
   [user]      MAIL-2: reply with exactly MAIL-2-ACK and nothing else.
   [user]      MAIL-3: reply with exactly MAIL-3-ACK and nothing else.
   [assistant] MAIL-1-ACK MAIL-2-ACK MAIL-3-ACK          ← ONE assistant turn, not three
   ```
   → 4 user messages, **2** assistant messages. opencode drains the whole queue into the next turn.

   **Swarm's contract says "a message is a claim on one turn."** opencode gives you *one turn for all mail that piled up*. For swarm this is a **semantic mismatch, not a bug** — and it is arguably *better* for throughput (an agent with three queued messages answers them in one pass instead of three). But any swarm logic that assumes *N sends ⇒ N turns* — turn accounting, one-task-per-turn dispatch, backpressure — **will be wrong on opencode**.

   Two ways out (**REASONED**): either (a) accept batching and make swarm's dispatcher idempotent w.r.t. turn count, or (b) enforce one-message-per-turn in the swarm CLI by gating on `session.idle` — hold mail, release exactly one, wait for idle, release the next. (b) preserves the contract at the cost of latency. **This is a design decision for the parent, and it is the sharpest thing I found.**
5. **`tool.execute.after` is undefined territory** — named in the event list, no signature in the docs. If we want to observe/rewrite tool results, someone must read the source.

---

## 7. What I'd tell the parent in one breath

The premise ("can a plugin make opencode a swarm harness?") had the wrong subject. **opencode's HTTP server is already a swarm harness** — I created sessions, mailed a busy agent and watched the message queue and land on its next turn, silently restored identity+journal into a session's context, subscribed to a bus that announces turn-end and compaction, and built a parent/child session tree, all from outside, all today, all on v1.17.13, with no plugin. The plugin is still worth writing, but for a *narrow and specific* reason: it owns compaction-survival (`experimental.session.compacting`), it can give the model native `swarm_spawn`/`swarm_send` tools, and it can put the agent's identity into every shell's env. Build server-primary, plugin-adjunct. The ecosystem has memory/RAG/tracing plugins and two that watch sessions for observability — but the orchestration slot is **empty**, so we extend into open ground rather than reinvent.

The one sharp edge, which I *did* probe: **mail batches.** Three messages arriving during one turn are drained into a *single* next turn, not three — so swarm's "a message is a claim on one turn" does not hold on opencode unless the swarm CLI enforces it by gating sends on `session.idle`. That's a design decision, not a blocker, and it's §6.4.
