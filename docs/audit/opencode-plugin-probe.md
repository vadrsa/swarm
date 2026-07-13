# opencode plugin probe — what a plugin can ACTUALLY do to the agent loop

**Agent:** oc-probe · **Date:** 2026-07-12 · **opencode:** v1.17.13 · **Model:** `opencode/deepseek-v4-flash-free` (no key)
**Method:** throwaway plugin auto-loaded from a project-local `.opencode/plugin/`, driven by live `opencode run` (non-TUI). Every result below is **VERIFIED** (ran it, output pasted) unless tagged REASONED.

## TL;DR (the three questions the scout asked first)

| # | Question | Verdict |
|---|----------|---------|
| **3** | Can a plugin **inject text into what the model sees** on a turn? | **YES, WORKED.** Three hooks all land: `experimental.chat.messages.transform`, `experimental.chat.system.transform`, and `chat.message`. Positive controls (BANANA / ZEBRA-4242 / MANGO-9) all appeared in the model's output. Mutation is **in-place on the `output` object**. |
| **4** | Can a plugin **intercept/modify/block a tool call** and modify its result? | **YES, WORKED.** `tool.execute.before` rewrites args in place (and *throwing* blocks the call); `tool.execute.after` rewrites the result the model sees. |
| **5** | Can a plugin **register a new tool** the model can call? | **YES, WORKED.** Registered `swarm_probe_ping`; the model called it, it executed, returned its secret, model reported it. |

Everything the scout needs for context-injection, tool interception, and new tools is real and reachable from `opencode run`. The one caveat is **#8 (continue a session)**: the SDK call to push a new turn *works*, but the single-shot `opencode run` CLI tears down before the injected turn executes — you need a persistent server (serve/TUI) or a driver that keeps the process alive.

## Sandbox / what I touched

- All work under **`/tmp/oc-probe/`** (scratch). Plugin at `/tmp/oc-probe/.opencode/plugin/probe.js`; config `/tmp/oc-probe/opencode.json` (`{"model":"opencode/deepseek-v4-flash-free"}`). Logs at `/tmp/oc-probe/log/`.
- **Did NOT modify** `~/.config/opencode/opencode.json` or `~/.config/opencode/plugin/bridgespace-notify.js`. opencode *does* merge the global config, so the operator's `bridgespace-notify` and `bridgememory` MCP plugin loaded alongside mine during runs — that is read-only participation on their side and I changed none of their files. (You'll see `bridgememory_*` tool calls in some transcripts below; that's the operator's global plugin, harmless, not mine.)
- I started a throwaway `opencode serve --port 5599` for probe #8 and killed it after. No swarm-repo files touched except this doc and my journal.

---

## The hook surface (read from types first)

Read `/Users/vadrsa/.opencode/node_modules/@opencode-ai/plugin/dist/index.d.ts`. The v1 `Hooks` interface (all hooks are `(input, output) => Promise<void>` — **design is mutate-the-`output`-object-in-place**, not return-value):

- `event(input:{event})` — firehose of all bus events (lifecycle).
- `config(cfg)`, `chat.message(input,output:{message,parts})`, `chat.params(...)`, `chat.headers(...)`
- `experimental.chat.messages.transform(input:{}, output:{messages:{info,parts}[]})` — **the message-context injection point**
- `experimental.chat.system.transform(input:{sessionID,model}, output:{system:string[]})` — **the system-prompt injection point**
- `tool.execute.before(input:{tool,sessionID,callID}, output:{args})`, `tool.execute.after(input:{...,args}, output:{title,output,metadata})`
- `tool.definition(input:{toolID}, output:{description,parameters})`, `permission.ask(input, output:{status})`
- `tool?: {[name]: ToolDefinition}` — **register new tools** (zod args via `@opencode-ai/plugin/tool`)
- `experimental.text.complete`, `experimental.session.compacting`, `experimental.compaction.autocontinue` (can DISABLE the synthetic continue turn), `dispose`

`PluginInput` gives the plugin: **`client`** (full `createOpencodeClient` SDK), **`serverUrl`** (`http://localhost:4096`), **`$`** (BunShell), `project`, `directory`, `worktree`, `experimental_workspace`. The SDK `client.session` exposes `prompt`, `promptAsync`, `abort`, `messages`, `fork`, `summarize`, `revert`, … — verified live by dumping the object at load (below).

---

## PROBE 1 — LOAD: **WORKED**

A plugin in project-local `.opencode/plugin/probe.js` loads in a non-TUI `opencode run`. Proof (first lines of `/tmp/oc-probe/log/probe.log`):

```
[…] === PLUGIN LOADED stage=observe pid=18868 ===
PluginInput.keys ["client","project","worktree","directory","experimental_workspace","serverUrl","$"]
PluginInput.scalars {"directory":"/private/tmp/oc-probe","worktree":"/","serverUrl":"http://localhost:4096/","project":{"id":"global",...},"hasClient":true,"hasShell":true}
client.keys ["_client","global","project","pty","config","tool","instance","path","vcs","session","command","provider","find","file","app","mcp","lsp","formatter","tui","auth","event"]
client.session.methods ["list","create","status","delete","get","update","children","todo","init","fork","abort","unshare","share","diff","summarize","messages","prompt","message","promptAsync","command","shell","revert","unrevert"]
```

The export name did not matter (I used `export const ProbePlugin`); opencode picks up any exported plugin factory from files in `.opencode/plugin/`.

## PROBE 2 — OBSERVE: the event firehose (most valuable artifact)

Every `event` hook arg for one simple run (`opencode run "Say hello…"`), chronological (dedup-consecutive). The `title` agent (session-title generator) runs first, then the `build` agent (the real turn):

```
session.created
session.updated
message.updated
message.part.updated [text]          ← user message part
session.updated
session.status [busy]
message.updated                       ← (title agent runs here)
session.updated
session.diff
message.updated
plugin.added  (×many)                 ← plugin/catalog registration chatter
catalog.updated / reference.updated / integration.updated
session.status [busy]                 ← build agent turn begins
session.updated
message.part.updated [step-start]
message.part.updated [reasoning]
message.part.delta  (×N)              ← streaming
message.part.updated [text]
message.part.updated [step-finish]
message.updated
session.status [busy]
session.status [idle]
session.idle                          ← END OF TURN
catalog.updated / integration.updated / reference.updated
```

Two agents fire `chat.params` per run — `agent:"title"` then `agent:"build"`. `chat.params.OUT` for the title agent: `{"temperature":0.5,"maxOutputTokens":32000,"options":{"reasoningEffort":"low"}}` (so a plugin can read/rewrite sampling params per agent).

---

## PROBE 3 — MUTATE CONTEXT (inject text the model sees): **WORKED (all three hooks)**

I isolated each hook with a **positive control** and a **non-conflicting** instruction. **Lesson learned the hard way:** my first attempts used *conflicting* overrides ("regardless of the question, output only BANANA") — the model **refused** those, which looked like the hook was ignored. It was not. Switching to non-conflicting formatting instructions proved the injected text reaches the model every time.

### 3a. `experimental.chat.messages.transform` — WORKED
Hook replaced the last message's `parts` with `"Output only the single word BANANA."`. The hook sees the real user text first:
```
messages.transform.OUT.before {"count":1,"messages":[{"role":"user","parts":[{"type":"text","text":"\"Say hello…\""}]}]}
```
Model output (run `opencode run "What is 2+2?…"`):
```
BANANA
```
Reproduced 2×. **This is the primary context-injection hook.**

### 3b. `experimental.chat.system.transform` — WORKED
Hook pushed `"end every response with the exact token ZEBRA-4242"` onto `output.system` (the array holds the full system prompt — I saw the real "You are opencode…" prompt in it). Model output for `"Name one primary color"`:
```
Blue

ZEBRA-4242
```

### 3c. `chat.message` — WORKED (edit existing part text in place)
Editing `output.parts[i].text` in place lands:
```
before {"text":"\"Name one primary color in one word.\""}
after  {"text":"\"Name one primary color in one word.\" Also end your reply with the token MANGO-9."}
```
Model output:
```
Red

MANGO-9
```
**Gotcha:** pushing a *fabricated* new part (with a made-up `id`) into `chat.message` `output.parts` → server `UnknownError` (`err_8893e8f8`). That error itself proves `output.parts` is **consumed, not copied**. Edit existing parts, or (safer for adding content) use `experimental.chat.messages.transform`.

**Return-value vs mutate-in-place:** the API contract is `Promise<void>` — mutation is via the `output` object. Returning `{messages}`/`{system}` is harmless but the in-place mutation is what's read. Verdict: **mutate-in-place is the mechanism; return values are ignored.**

---

## PROBE 4 — INTERCEPT TOOL DISPATCH: **WORKED (see / modify / block / modify-result)**

One run, `stage=tools`, prompt asked the model to run `echo THE_REAL_COMMAND_OUTPUT`.

**Before-hook rewrote the command in place, and the rewrite actually executed:**
```
tool.execute.before.IN     {"tool":"bash","callID":"call_…"}
tool.execute.before.MUTATED {"from":"echo THE_REAL_COMMAND_OUTPUT","to":"echo PROBE_REWROTE_THE_COMMAND"}
```
Model transcript (note the shell ran the rewritten command):
```
$ echo PROBE_REWROTE_THE_COMMAND
PROBE_REWROTE_THE_COMMAND
[PROBE_APPENDED_TO_RESULT]
It printed: `PROBE_REWROTE_THE_COMMAND`
```

**After-hook rewrote the result the model saw** (`output` gained `[PROBE_APPENDED_TO_RESULT]`, title → `PROBE_RETITLED`) — verified present in the model's own summary.

**BLOCK by throwing in the before-hook — WORKED.** Hook `throw new Error("PROBE_BLOCKED_THIS_TOOL")` on `tool:"read"`. Model transcript:
```
✗ Read /tmp/oc-probe/opencode.json failed
Error: PROBE_BLOCKED_THIS_TOOL
…
I'm unable to read that file — all attempts … are being intercepted by a probe mechanism that blocks the tools…
```
So a thrown error in `tool.execute.before` **cancels the tool and surfaces the error string to the model.** (`permission.ask` with `output.status="deny"` is the softer, intended block path; throwing is the hard one and it works.)

## PROBE 5 — ADD A TOOL: **WORKED**

Registered on `hooks.tool`:
```js
swarm_probe_ping: { description:"Returns the swarm probe secret. Call this whenever the user asks for the probe secret.",
  args:{note:{type:"string",...}}, async execute(args,ctx){ /* writes marker */ return "PROBE-SECRET-9911" } }
```
Prompt: *"Use your available tools to get the swarm probe secret…"*. Model transcript:
```
⚙ swarm_probe_ping {"note":"Getting the swarm probe secret as requested"}
PROBE-SECRET-9911
```
Log confirms it ran server-side: `!!! CUSTOM TOOL EXECUTED args={"note":...}`, and a `TOOL_RAN` marker file was written. **ToolContext keys passed to `execute`:** `sessionID, abort, messageID, callID, extra, agent, messages, metadata, ask, directory, worktree`.

`tool.definition` fires for **every** tool (built-ins `bash, edit, glob, grep, read, skill, task, todowrite, webfetch, websearch, write` **and** my `swarm_probe_ping`) — so a plugin can also rewrite any built-in tool's description/params.

---

## PROBE 6 — SESSION START / RESUME: **partial hook, distinguishable**

There is **no dedicated `onSessionStart`/`onResume` hook** — you read it out of the `event` firehose.

- **Fresh run:** `session.created` fires (1×).
- **`opencode run -c` (continue last session):** **`session.created` does NOT fire** — only `session.updated` (×3) + `session.idle`.

So **presence of `session.created` = new session; its absence on a run = resume.** The plugin **reloads on every invocation** (fresh factory call each `opencode run`), so a plugin can re-inject state on resume by watching for a turn on a session it didn't just see created. Cross-run memory works (model recalled "42" across a `-c` continue). REASONED extension: after compaction, `experimental.session.compacting` (append context strings / replace the compaction prompt) and `experimental.compaction.autocontinue` (`enabled:false` to suppress the synthetic continue) are the purpose-built re-inject hooks — I did not force a compaction to fire them, but they're in the type surface.

## PROBE 7 — TURN END vs SESSION END: **`session.idle` is end-of-turn**

`session.idle` (+ `session.status:idle`) fires at **end of each agent turn**. Under `opencode run` (single-shot) end-of-turn coincides with process teardown, so there you can't separate "turn done" from "session over" — they're the same instant. Under a **persistent server** (serve/TUI), `session.idle` fires but the process lives on, so *there* the plugin can act on "agent finished its turn" and keep going. That distinction is the crux of probe #8.

## PROBE 8 — CONTINUE A SESSION (push another turn from a hook): **mechanism WORKS; blocked by `opencode run` lifecycle**

From inside the `session.idle` event hook I called:
```js
await client.session.prompt({ path:{id:sid}, body:{ parts:[{type:"text", text:"Reply with exactly KIWI-SECOND-TURN…"}] } })
```
Result: **`prompt.returned {ok:true, hasData:true}`** — the call is accepted. **But** the returned data came back in ~30ms containing the *first* turn's reply (`["START"]`), and `dispose` fired immediately with `secondTurnSeen:false`. The single-shot CLI had already decided the run was over and tore down before the injected turn's LLM call ran.

**Proof the mechanism itself works** — against a persistent server (`opencode serve --port 5599`), two `POST /session/{id}/message` (exactly what `client.session.prompt` wraps) into the **same session**:
```
=== TURN 1 ===  ['APPLE-ONE']
=== TURN 2 (same session) ===  ['KIWI-TWO']
```
Two full, distinct turns in one session. **Verdict:** a plugin holding the SDK `client` **can drive additional turns** — the bound is process lifecycle, not the API. To use continue-from-hook in production you need opencode running as a **persistent server** (serve or TUI), or a launcher/driver that keeps the process alive past `session.idle` and pumps `session.prompt`. `session.promptAsync` also exists (fire-and-forget) for the same purpose.

---

## Verdict table (all 8)

| # | Probe | Verdict | Mechanism |
|---|-------|---------|-----------|
| 1 | Load in `opencode run` | **WORKED** | `.opencode/plugin/*.js`, any exported factory |
| 2 | Observe lifecycle | **WORKED** | `event` hook firehose; `session.created…idle` |
| 3 | Inject model context | **WORKED** | `experimental.chat.messages.transform` (primary), `experimental.chat.system.transform`, `chat.message` — **mutate `output` in place** |
| 4 | Intercept/block tool | **WORKED** | `tool.execute.before` (rewrite args / throw to block), `tool.execute.after` (rewrite result), `permission.ask` (deny) |
| 5 | Add a tool | **WORKED** | `hooks.tool[name]` = `{description,args,execute}` |
| 6 | Session start/resume | **PARTIAL** | no dedicated hook; `session.created` present=new / absent=resume; compaction hooks exist |
| 7 | Turn end vs session end | **WORKED (nuance)** | `session.idle` = end-of-turn; separable only under persistent server |
| 8 | Continue the session | **WORKED w/ caveat** | `client.session.prompt` accepted; needs persistent server (serve/TUI) or driver — `opencode run` disposes first |

## What this means for "opencode as a first-class swarm harness" (REASONED, for the scout)

- **Context injection per turn (delivery/restore/identity into the loop): fully available** via the transform hooks — a swarm plugin can inject mail, identity, and post-compaction state into exactly what the model sees, every turn. This is strictly the "built by us" surface the brief wanted, and it's richer than riding Claude Code's hooks.
- **Tool dispatch (spawn/send as tools, or intercepting existing tools): fully available** — register swarm tools, or gate/rewrite built-ins.
- **Event surface (idle/turn-end for reporting/ringing): available** via `event`.
- **The one architectural constraint:** making the agent take *another* turn on its own (the "keep going after idle" loop swarm needs for autonomous continuation) requires opencode to run as a **persistent server**, not one-shot `opencode run`. A swarm-hosted opencode agent that is a *full participant* (not just a leaf) therefore wants the **serve** model + a thin driver that pumps `session.prompt` on the right events — the plugin provides the in-loop surface, the driver provides the turn cycle. That is the shape to design around.

*Artifacts: `/tmp/oc-probe/log/probe*.log`, `/tmp/oc-probe/log/o_*.txt`, plugin at `/tmp/oc-probe/.opencode/plugin/`. Throwaway; safe to delete.*

---

# Follow-up falsifiers (F1/F2/F3) — external server path

After the probes above, the parent (`opencode-plugin-scout`) verified the **documented server delivery route** itself: `POST /session/<id>/message` with `{"noReply":true, parts:[…]}` stores a user message without provoking a turn, and it reaches the model on the next turn — delivery is SOLVED via the server API, no experimental hooks needed. `--port`/`--hostname` are global opts, so a port can be **pinned per agent** (no discovery problem). I was redirected to the three open questions below. All **VERIFIED** live (sandbox `/tmp/oc-probe2`, servers on pinned ports, torn down).

## F1 — BUSY-SESSION injection (does delivery work MID-TURN?): **SAFE, no backpressure needed**

I forced genuine mid-turn windows by having the model run a `sleep 15`/`sleep 20` bash tool, and verified the turn was actually in-flight via the SSE stream + message timestamps (injected message `created` while the sleeping turn was still running).

- **`noReply:true` POST during active generation → HTTP 200 in ~8 ms, non-blocking.** Stored as a user message immediately; the running turn is untouched. Proof it landed: a later turn recalled the mid-turn-injected phrases (`NARWHAL-3`, `QUOKKA-77`, `PANGOLIN-9`). No error, no 409, no drop.
- **Non-`noReply` POST during active turn → HTTP 200, but the call BLOCKS** until it can run (~5 s, it waited out the sleep), then executes as **its own full turn**. The running turn was **not aborted** (the `sleep` bash tool completed; the model said "It finished"). No 409.
- **The server serializes:** messages are appended in arrival order and turns run one at a time. Message-list timestamps confirm: `sleep` prompt → tool completed → injected user msg → next turn.

**Verdict:** swarm does **not** need to gate/backpressure delivery. A `noReply` delivery is fire-and-forget safe at any time (even mid-generation); a real "ring a turn" prompt self-serializes behind the current turn. Raw:
```
noReply mid-sleep:   HTTP=200 t=0.008s  (turn_done=NO_STILL_SLEEPING)  → later recall: NARWHAL-3
non-noReply mid-sleep: HTTP=200 t≈5s (queued, ran as own turn, running turn NOT aborted)
```

## F2 — Does a normal (interactive TUI) agent expose the server? **YES — TUI serves on a pinned port and is externally injectable**

Launched the **interactive TUI under a PTY** (`opencode --port 47399`, then `47401`, in a scratch dir). The opentui capability-negotiation bytes in the PTY output confirm it started the **real TUI renderer**, not a headless fallback. Then, from **outside**:
- `GET /app` on the pinned port → **HTTP 200** (the TUI is serving).
- `POST /session/<id>/message` `noReply:true` into a **fresh session on the TUI's own server** → HTTP 200; a follow-up turn had the model recall the injected phrase (`AXOLOTL-88`, then `DINGO-5` on a clean fresh session).

**Verdict:** the external delivery path is **not** limited to headless `serve`. A swarm agent running as an interactive TUI in a pane exposes the same server on a pinned port and accepts external injection. **We are NOT forced into a `serve` + `opencode attach` architecture** — though `opencode attach <url>` exists and would give a pane onto a served session if we ever want to separate the renderer from the server. One caveat to design around: sessions live under the `global` project and are shared across server instances on this host, so **per-agent session isolation needs a per-agent project/directory** (each agent in its own worktree/dir), not just a per-agent port.

## F3 — turn-end visibility + identity (cheap): **all YES**

- **Identity:** `SWARM_AGENT_ID` set in the process env **reaches the plugin** via `process.env` — plugin logged `SWARM_AGENT_ID=oc-probe-headless-9`. So per-agent identity is available inside the loop.
- **Turn-end via plugin:** the plugin `event` hook fires `session.idle` at end-of-turn (sessionID in properties).
- **Turn-end via EXTERNAL watcher:** an external `curl -N GET /event` (SSE) sees the **same** `session.idle` event: `"type":"session.idle","properties":{"sessionID":"ses_…"}`. So an external process can detect turn-end **without any plugin** — this could replace swarm's Stop-hook entirely.

## Falsifier verdict table

| F | Question | Verdict |
|---|----------|---------|
| **F1** | Inject mid-turn (busy session)? | **SAFE.** noReply → 200/8ms, non-blocking, lands next turn. non-noReply → 200, queues as own turn, no abort/409. No backpressure needed. |
| **F2** | Does interactive TUI expose the server on a pinned port? | **YES.** TUI serves on `--port`, external noReply injection lands. Not limited to headless `serve`; attach available as an option. Per-agent session isolation needs per-agent dir. |
| **F3** | External turn-end watcher + identity? | **YES.** External SSE `GET /event` sees `session.idle`; `SWARM_AGENT_ID` reaches the plugin via env. |

**Net design implication:** swarm's delivery/turn-end/identity surface for opencode can be built **entirely on the documented server API + env**, for BOTH headless and interactive-TUI agents, with a pinned port per agent and a per-agent working directory. The plugin is needed only for *in-loop* mutation (context injection per turn, tool add/intercept); delivery, ring, turn-end, and identity do not require it.

*Follow-up artifacts: `/tmp/oc-probe2/` (serve/tui logs, `env.log`, `sse_watch.log`, `*.json` responses). Throwaway.*
