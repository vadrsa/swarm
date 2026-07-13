# opencode prior art — what the OFFICIAL DOCS claim

Scout: `oc-docs`. Parent: `oc-priorart`. Target: opencode (sst/opencode), docs as of pages stamped **"Last updated: Jul 10, 2026"**, read 2026-07-12.

**Method / scope discipline.** Everything below was read off the live doc pages listed. I did **not** read installed source — a sibling does that, and the point of this file is to be the doc side of a doc-vs-source cross-check. Every claim is tagged with the URL it came from. Where the docs are *silent*, I say so explicitly and mark it **DOCS SILENT** — those are first-class findings, not gaps in my reading. I did not fill anything in from training data.

**The one-line headline:** the docs describe **five** plugin hook keys with real signatures — `event`, `tool.execute.before`, `tool.execute.after`, `shell.env`, `tool`, plus experimental `experimental.session.compacting`. The long bulleted "Events" list on the plugins page is **not** a list of hooks; it is the list of `event.type` string values the single `event` hook can observe. And yes — **an external message-injection endpoint into an existing session is documented**, twice over (`POST /session/:id/message`, `POST /session/:id/prompt_async`), plus a documented "inject context without triggering a reply" flag.

---

## 0. The most load-bearing distinction on the plugins page

The plugins page has a section headed **"Events"** that reads, verbatim:

> "Plugins can subscribe to events as seen below in the Examples section. Here is a list of the different events available."
> — https://opencode.ai/docs/plugins

It then lists ~25 dotted names (`session.idle`, `permission.asked`, `tool.execute.after`, …). It is very easy to misread that list as "here are 25 plugin hooks." **It is not.** The only example the page gives of consuming them is via the single `event` hook, switching on `event.type`:

```js
export const NotificationPlugin = async ({ project, client, $, directory, worktree }) => {
  return {
    event: async ({ event }) => {
      // Send notification on session completion
      if (event.type === "session.idle") {
        await $`osascript -e 'display notification "Session completed!" with title "opencode"'`
      }
    },
  }
}
```
— https://opencode.ai/docs/plugins

So `session.idle` and `permission.asked` are **event *types*, observed after the fact**, not hooks with a mutable `output` argument. Two names — `tool.execute.before` and `tool.execute.after` — appear in *both* roles: in the bus-event list, and (for `.before`) as a genuine mutating hook key in code. **The docs never show `tool.execute.after` used as a hook, never give its signature, and never say whether it can mutate.** That ambiguity is the single most important thing for the sibling to resolve against source.

---

## 1. Plugin hooks — every hook the docs actually NAME with a signature

Source for all of §1: **https://opencode.ai/docs/plugins**

| Hook key | Signature as shown in docs | Stated firing point | MUTATE input? | INJECT text into model context / next turn? | Fires at session/turn END? |
|---|---|---|---|---|---|
| `event` | `event: async ({ event }) => {}` | Docs say only "Plugins can subscribe to events". No firing-point prose beyond that. | **No** — receives `{ event }`, no `output` arg shown. Read-only in every example. | **No** — no documented return/output channel. | **Indirectly** — it can *observe* `session.idle`, which the doc example comments as "Send notification on session completion". That is the closest documented thing to a turn/session-end signal. |
| `tool.execute.before` | `"tool.execute.before": async (input, output) => {}` — `input.tool` is the tool name; `output.args` is the tool's arguments object | Before a tool executes | **YES.** Both doc examples mutate: `output.args.command = escape(output.args.command)`, and the `.env` example *aborts* by `throw new Error("Do not read .env files")`. | Not shown. It rewrites tool args; the docs show no path from here into the prompt. | No |
| `tool.execute.after` | **NOT SHOWN.** Named only in the bus-event list. | **DOCS SILENT** | **DOCS SILENT** | **DOCS SILENT** | **DOCS SILENT** |
| `shell.env` | `"shell.env": async (input, output) => {}` — `input.cwd`; `output.env` is a mutable env map | Docs: "Inject environment variables into all shell execution (AI tools and user terminals)" | **YES.** Example: `output.env.MY_API_KEY = "secret"`, `output.env.PROJECT_ROOT = input.cwd` | No — env vars, not model context | No |
| `tool` | `tool: { mytool: tool({ description, args, async execute(args, context) {} }) }` | Registers a custom tool callable by the model. `execute`'s `context` destructures to `{ directory, worktree }`. | N/A (it *is* a tool) | Only in the ordinary sense that a tool's return string goes back to the model as a tool result. | No |
| `experimental.session.compacting` | `"experimental.session.compacting": async (input, output) => {}` — `output.context` is a **pushable array**; `output.prompt` is a **settable string** | Verbatim: *"The `experimental.session.compacting` hook fires before the LLM generates a continuation summary."* | **YES** | **YES — this is the ONLY documented text-injection-into-model-context hook.** `output.context.push("## Custom Context …")` injects into the compaction prompt. Setting `output.prompt` **replaces the compaction prompt entirely**; docs: *"When `output.prompt` is set, it completely replaces the default compaction prompt. The `output.context` array is ignored in this case."* | **Only at compaction**, which is not the same as turn end or session end. |

Note the compaction example the docs themselves ship is *literally about swarms* — verbatim:

> ```
> You are generating a continuation prompt for a multi-agent swarm session.
> Summarize:
> 1. The current task and its status
> 2. Which files are being modified and by whom
> 3. Any blockers or dependencies between agents
> 4. The next steps to complete the work
> ```
> — https://opencode.ai/docs/plugins

### The full "Events" list (event.type values for the `event` hook)
Verbatim from https://opencode.ai/docs/plugins, grouped as the page groups them:

- **Command:** `command.executed`
- **File:** `file.edited`, `file.watcher.updated`
- **Installation:** `installation.updated`
- **LSP:** `lsp.client.diagnostics`, `lsp.updated`
- **Message:** `message.part.removed`, `message.part.updated`, `message.removed`, `message.updated`
- **Permission:** `permission.asked`, `permission.replied`
- **Server:** `server.connected`
- **Session:** `session.created`, `session.compacted`, `session.deleted`, `session.diff`, `session.error`, `session.idle`, `session.status`, `session.updated`
- **Todo:** `todo.updated`
- **Shell:** `shell.env`
- **Tool:** `tool.execute.after`, `tool.execute.before`
- **TUI:** `tui.prompt.append`, `tui.command.execute`, `tui.toast.show`
- **Experimental:** `experimental.session.compacting` *(listed under Examples/prose, and it is a real hook — see table)*

### DOCS SILENT — things the task asked about that the docs do NOT contain
I grepped all five doc pages for each of these. Stating these plainly because "the docs don't say" is the finding:

- **`chat.message` — DOCS SILENT.** The string does not appear on any opencode doc page. There is **no documented hook that intercepts or mutates a user/assistant chat message.**
- **`chat.params` — DOCS SILENT.** Does not appear anywhere. **No documented hook to alter model params (temperature, system prompt) per-request.**
- **A permission hook — DOCS SILENT.** `permission.asked` / `permission.replied` exist only as **observable event types**. The docs show **no hook that can approve/deny a permission from a plugin.** (Permission *policy* is configured declaratively — see §5 — and there is a *server* endpoint to answer one, see §3.)
- **An auth hook — DOCS SILENT.** No `auth` hook on the plugins page. "auth" appears in the docs only as the server route `PUT /auth/:id` and the SDK's `client.auth.set()` (§3), i.e. credential *setting*, not a plugin hook.
- **A session/turn-END hook — DOCS SILENT.** No `session.end`, no `message.received`, no turn-completion hook key. The nearest documented thing is *observing* the `session.idle` event via the `event` hook.
- **`tool.execute.after` as a usable hook — DOCS SILENT** on its signature, its mutability, and whether it can rewrite a tool result.

---

## 2. The plugin authoring model
Source: **https://opencode.ai/docs/plugins** (and https://opencode.ai/docs/config for the `plugin` key)

**How a plugin is loaded — two documented ways ("There are two ways to load plugins"):**

1. **From local files.** "Place JavaScript or TypeScript files in the plugin directory."
   - `.opencode/plugins/` — project-level
   - `~/.config/opencode/plugins/` — global
   - "Files in these directories are automatically loaded at startup."
   - *(Note the plural `plugins/`. The config page adds: "The `.opencode` and `~/.config/opencode` directories use plural names for subdirectories: `agents/`, `commands/`, `modes/`, `plugins/`, `skills/`, `tools/`, and `themes/`. Singular names (e.g. `agent/`) are also supported for backwards compatibility." — https://opencode.ai/docs/config)*
2. **From npm**, via the `plugin` config key:
   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "plugin": ["opencode-helicone-session", "opencode-wakatime", "@my-org/custom-plugin"]
   }
   ```
   "Both regular and scoped npm packages are supported."

**Install mechanics (verbatim):** "npm plugins are installed automatically using Bun at startup. Packages and their dependencies are cached in `~/.cache/opencode/node_modules/`." Local plugins that need external packages require a `package.json` in the config dir (`.opencode/package.json`); "OpenCode runs `bun install` at startup to install these."

**Load order (verbatim):** "Plugins are loaded from all sources and all hooks run in sequence. The load order is:" global config → project config → global plugin directory → project plugin directory. Plus: "Duplicate npm packages with the same name and version are loaded once. However, a local plugin and an npm plugin with similar names are both loaded separately."

**The Plugin function signature.** "A plugin is a JavaScript/TypeScript module that exports one or more plugin functions. Each function receives a context object and returns a hooks object."

```js
export const MyPlugin = async ({ project, client, $, directory, worktree }) => {
  console.log("Plugin initialized!")
  return {
    // Hook implementations go here
  }
}
```

**What the plugin function receives** (verbatim bullets):
- `project`: The current project information.
- `directory`: The current working directory.
- `worktree`: The git worktree path.
- `client`: An opencode SDK client for interacting with the AI.
- `$`: Bun's shell API for executing commands.

**What `@opencode-ai/plugin` exports** — the docs demonstrate exactly two importable names:
- `Plugin` — the TS type: `import type { Plugin } from "@opencode-ai/plugin"`
- `tool` — the custom-tool helper, with `tool.schema` as a Zod schema builder: `import { type Plugin, tool } from "@opencode-ai/plugin"`, used as `tool({ description, args: { foo: tool.schema.string() }, async execute(args, context) {} })`.
- The docs do **not** enumerate a complete export list for the package. Anything beyond `Plugin` and `tool` is **DOCS SILENT**.

**Logging:** "Use `client.app.log()` instead of `console.log` for structured logging" — `client.app.log({ body: { service, level, message, extra } })`; "Levels: debug, info, warn, error."

**Tool-name collision (verbatim):** "If a plugin tool uses the same name as a built-in tool, the plugin tool takes precedence."

---

## 3. The HTTP server + SDK — **YES, external message injection into an existing session is DOCUMENTED**
Sources: **https://opencode.ai/docs/server** and **https://opencode.ai/docs/sdk**

### Starting it
`opencode serve [--port <number>] [--hostname <string>] [--cors <origin>]` — https://opencode.ai/docs/server

| Flag | Description | Default |
|---|---|---|
| `--port` | Port to listen on | `4096` |
| `--hostname` | Hostname to listen on | `127.0.0.1` |
| `--mdns` | Enable mDNS discovery | `false` |
| `--mdns-domain` | Custom domain name for mDNS service | `opencode.local` |
| `--cors` | Additional browser origins to allow | `[]` (repeatable) |

- **Auth:** "Set `OPENCODE_SERVER_PASSWORD` to protect the server with HTTP basic auth. The username defaults to `opencode`, or set `OPENCODE_SERVER_USERNAME` to override it."
- **Architecture (verbatim):** "When you run opencode it starts a TUI and a server. Where the TUI is the client that talks to the server." And: "You can run `opencode serve` to start a standalone server. If you have the opencode TUI running, `opencode serve` will start a new server."
- **Discovery of a running TUI's server:** "When you start the TUI it randomly assigns a port and hostname. You can instead pass in the `--hostname` and `--port` flags. Then use this to connect to its server."
- **Spec:** OpenAPI 3.1 at `GET /doc`, e.g. `http://localhost:4096/doc`.

### THE ANSWER TO THE KEY QUESTION — inject a message into an EXISTING session

**Yes. Documented, with exact paths** (https://opencode.ai/docs/server, "Messages" table):

| Method | Path | Docs' own description | Body (verbatim) |
|---|---|---|---|
| `POST` | **`/session/:id/message`** | **"Send a message and wait for response"** | `{ messageID?, model?, agent?, noReply?, system?, tools?, parts }` → returns `{ info: Message, parts: Part[] }` |
| `POST` | **`/session/:id/prompt_async`** | **"Send a message asynchronously (no wait)"** | "same as `/session/:id/message`", returns **204 No Content** |
| `POST` | `/session/:id/command` | "Execute a slash command" | `{ messageID?, agent?, model?, command, arguments }` |
| `POST` | `/session/:id/shell` | "Run a shell command" | `{ agent, model?, command }` |
| `GET` | `/session/:id/message` | "List messages in a session" | query `limit?` |
| `GET` | `/session/:id/message/:messageID` | "Get message details" | — |

**And a documented *silent* context-injection flag.** The SDK page shows `noReply` explicitly, with this comment in opencode's own example code:

```js
// Inject context without triggering AI response (useful for plugins)
await client.session.prompt({
  path: { id: session.id },
  body: {
    noReply: true,
    parts: [{ type: "text", text: "You are a helpful assistant." }],
  },
})
```
— https://opencode.ai/docs/sdk

The SDK table restates it: `session.prompt({ path, body })` — "`body.noReply: true` returns UserMessage (context only). Default returns AssistantMessage with AI response." So: **text can be pushed into a live session's context from outside, without provoking a turn.** That is the capability worth flagging upstream. The server page also lists `system?` and `tools?` in the same POST body — the docs do not further explain either. **DOCS SILENT** on what `system` does there.

### SSE / event stream — YES

| Method | Path | Docs' description |
|---|---|---|
| `GET` | **`/event`** | **"Server-sent events stream. First event is `server.connected`, then bus events"** |
| `GET` | `/global/event` | "Get global events (SSE stream)" |

SDK equivalent — `event.subscribe()`, https://opencode.ai/docs/sdk:
```js
const events = await client.event.subscribe()
for await (const event of events.stream) {
  console.log("Event:", event.type, event.properties)
}
```
So an SSE event has at least `.type` and `.properties`. **The server page names exactly ONE event type: `server.connected`.** It does not enumerate the bus events — for that list you must go to the plugins page's Events section (§1), and the docs never state that the two lists are the same set. **DOCS SILENT** on whether the SSE bus emits exactly the plugin `event` types.

### Rest of the endpoint list (verbatim paths, https://opencode.ai/docs/server)
- **Global:** `GET /global/health` → `{ healthy: true, version: string }`; `GET /global/event`
- **Project:** `GET /project`, `GET /project/current`
- **Path & VCS:** `GET /path`, `GET /vcs`
- **Instance:** `POST /instance/dispose`
- **Config:** `GET /config`, `PATCH /config`, `GET /config/providers`
- **Provider:** `GET /provider`, `GET /provider/auth`, `POST /provider/{id}/oauth/authorize`, `POST /provider/{id}/oauth/callback`
- **Sessions:** see §4
- **Commands:** `GET /command`
- **Files:** `GET /find?pattern=`, `GET /find/file?query=`, `GET /find/symbol?query=`, `GET /file?path=`, `GET /file/content?path=`, `GET /file/status`
- **Tools (Experimental):** `GET /experimental/tool/ids`, `GET /experimental/tool?provider=&model=`
- **LSP/Formatter/MCP:** `GET /lsp`, `GET /formatter`, `GET /mcp`, `POST /mcp` (add MCP server dynamically, body `{ name, config }`)
- **Agents:** `GET /agent` → `Agent[]`
- **Logging:** `POST /log`, body `{ service, level, message, extra? }`
- **TUI:** `POST /tui/append-prompt`, `/tui/submit-prompt`, `/tui/clear-prompt`, `/tui/execute-command`, `/tui/show-toast`, `/tui/open-help`, `/tui/open-sessions`, `/tui/open-themes`, `/tui/open-models`, `GET /tui/control/next`, `POST /tui/control/response`. Server page: *"The `/tui` endpoint can be used to drive the TUI through the server. For example, you can prefill or run a prompt. This setup is used by the OpenCode IDE plugins."*
- **Auth:** `PUT /auth/:id` — "Set authentication credentials. Body must match provider schema"
- **Docs:** `GET /doc`

### SDK client construction (https://opencode.ai/docs/sdk)
- `npm install @opencode-ai/sdk`
- `createOpencode()` — "This starts both a server and a client". Options: `hostname` (`127.0.0.1`), `port` (`4096`), `signal`, `timeout` (`5000`), `config`.
- `createOpencodeClient({ baseUrl: "http://localhost:4096" })` — "If you already have a running instance of opencode, you can create a client instance to connect to it". Options: `baseUrl`, `fetch`, `parseAs`, `responseStyle` (`fields`), `throwOnError` (`false`).
- Structured output is documented: `body.format = { type: "json_schema", schema, retryCount? }`, read back at `result.data.info.structured_output`; failure surfaces as `error.name === "StructuredOutputError"`. *(Minor doc inconsistency worth noting: the Sessions table calls this `body.outputFormat`, while the worked example and the "JSON Schema Format" table call it `format`. The docs contradict themselves here.)*

---

## 4. Sessions and Agents

### Session endpoints — child sessions and sharing are BOTH documented
https://opencode.ai/docs/server:

| Method | Path | Description | Notes (verbatim) |
|---|---|---|---|
| `GET` | `/session` | List all sessions | Returns `Session[]` |
| `POST` | `/session` | Create a new session | **body: `{ parentID?, title? }`** ← **child/sub-session creation is documented via `parentID`** |
| `GET` | `/session/status` | Get session status for all sessions | `{ [sessionID: string]: SessionStatus }` |
| `GET` | `/session/:id` | Get session details | |
| `DELETE` | `/session/:id` | Delete a session and all its data | |
| `PATCH` | `/session/:id` | Update session properties | body `{ title? }` |
| **`GET`** | **`/session/:id/children`** | **"Get a session's child sessions"** | Returns `Session[]` |
| `GET` | `/session/:id/todo` | Get the todo list for a session | `Todo[]` |
| `POST` | `/session/:id/init` | **"Analyze app and create AGENTS.md"** | body `{ messageID, providerID, modelID }` |
| `POST` | `/session/:id/fork` | "Fork an existing session at a message" | body `{ messageID? }` |
| `POST` | `/session/:id/abort` | Abort a running session | |
| `POST` | `/session/:id/share` | Share a session | Returns `Session` |
| `DELETE` | `/session/:id/share` | Unshare a session | Returns `Session` |
| `GET` | `/session/:id/diff` | Get the diff for this session | query `messageID?` |
| `POST` | `/session/:id/summarize` | Summarize the session | body `{ providerID, modelID }` |
| `POST` | `/session/:id/revert` | Revert a message | body `{ messageID, partID? }` |
| `POST` | `/session/:id/unrevert` | Restore all reverted messages | |
| `POST` | `/session/:id/permissions/:permissionID` | **"Respond to a permission request"** | body `{ response, remember? }` ← permission answering exists **as an HTTP endpoint**, not as a plugin hook |

SDK mirrors these (https://opencode.ai/docs/sdk): `session.list()`, `session.get()`, **`session.children()` — "List child sessions"**, `session.create()`, `session.delete()`, `session.update()`, `session.init()`, `session.abort()`, `session.share()`, `session.unshare()`, `session.summarize()`, `session.messages()`, `session.message()`, `session.prompt()`, `session.command()`, `session.shell()`, `session.revert()`, `session.unrevert()`, `postSessionByIdPermissionsByPermissionId()`.

`share` also exists as a **config key** with values manual / auto / disabled (https://opencode.ai/docs/config).

### Agents — https://opencode.ai/docs/agents

Two kinds (verbatim): "There are two types of agents in OpenCode; primary agents and subagents."
- **Primary:** "the main assistants you interact with directly. You can cycle through them using the Tab key, or your configured `switch_agent` keybind."
- **Subagents:** "specialized assistants that primary agents can invoke for specific tasks. You can also manually invoke them by @ mentioning them in your messages."

**Built-ins:** primary — **Build** ("all tools enabled"), **Plan** ("restricted… file edits and bash commands set to ask"). Subagents — **General** ("A general-purpose agent for researching complex questions and executing multi-step tasks. Has full tool access (except todo)… Use this to run multiple units of work in parallel."), **Explore** (read-only, codebase), **Scout** (read-only, external docs/deps). Plus two **hidden system agents**: one that "generates short session titles" and one that "creates session summaries" — both "run automatically and [are] not selectable in the UI."

**Invocation (verbatim):** "Subagents can be invoked: Automatically by primary agents for specialized tasks based on their descriptions. Manually by @ mentioning a subagent in your message. For example. `@general help me search for this function`"

**The `task` tool.** The docs do **not** give a task-tool schema. What they *do* say is that `task` is a **permission key**, and: *"The `permission.task` setting controls which subagents a primary agent can invoke… When set to `deny`, the subagent is removed from the Task tool description entirely, so the model won't attempt to invoke it."* — https://opencode.ai/docs/agents. So the Task tool is confirmed to exist and to be how subagents get invoked, but **its parameters/signature are DOCS SILENT.**

**Subagents create child sessions — stated plainly** (verbatim): *"Navigation between sessions: When subagents create child sessions, use `session_child_first` (default: `<Leader>+Down`) to enter the first child session from the parent."* Then `session_child_cycle` (Right) / `session_child_cycle_reverse` (Left) to cycle, `session_parent` (Up) to return. This is the doc-level confirmation that **opencode's subagent model is literally a parent/child *session* tree**, matching the `parentID` / `/session/:id/children` API.

**Agent config keys** (https://opencode.ai/docs/agents): `description` (required for subagents), `mode` (`primary` | `subagent` | `all`), `model`, `prompt`, `temperature`, `steps`, `permission`, `tools` (**deprecated** — "Prefer the agent's `permission` field"), `disable`.
- `model`: "If you don't specify a model, primary agents use the model globally configured while subagents will use the model of the primary agent that invoked the subagent."
- `steps`: "Maximum agentic iterations before text-only response… When the limit is reached, the agent receives a special system prompt instructing it to respond with a summarization of its work and recommended remaining tasks." If unset, "the agent will continue to iterate until the model chooses to stop or the user interrupts the session."

**Two ways to define an agent** — JSON under the `agent` key in `opencode.json`:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "You are a code reviewer. Focus on security, performance, and maintainability.",
      "permission": { "edit": "deny" }
    }
  }
}
```
…or **Markdown files** with YAML frontmatter in `~/.config/opencode/agents/` (global) or `.opencode/agents/` (per-project); the filename becomes the agent id (`review.md` → `review`).

---

## 5. Config keys
Source: **https://opencode.ai/docs/config** (+ https://opencode.ai/docs/rules for AGENTS.md)

**`plugin`** — array of npm package names. "Place plugin files in `.opencode/plugins/` or `~/.config/opencode/plugins/`. You can also load plugins from npm through the `plugin` option."
```json
{ "$schema": "https://opencode.ai/config.json", "plugin": ["opencode-helicone-session", "@my-org/custom-plugin"] }
```

**`agent`** — map of agent-id → agent config (see §4). **`default_agent`** — "specifies which agent runs when none is explicitly selected", e.g. `"default_agent": "plan"`.

**`instructions`** — "You can configure the instructions for the model you're using through the `instructions` option… This takes an array of paths and glob patterns to instruction files."
```json
{ "$schema": "https://opencode.ai/config.json", "instructions": ["CONTRIBUTING.md", "docs/guidelines.md", ".cursor/rules/*.md"] }
```

**`permission`** — top-level, and overridable per agent. Each key takes `"allow" | "ask" | "deny"`. Documented keys include `edit`, `bash`, `read`, `glob`, `grep`, `list`, **`task`**, `external_directory`, `lsp`, `skill`, `webfetch`. Verbatim: *"`read`, `edit`, `glob`, `grep`, `list`, `bash`, `task`, `external_directory`, `lsp`, and `skill` accept either a shorthand action ("allow" | "ask" | "deny") or an object of glob/pattern → action for fine-grained control."* And: *"Permission keys are matched as wildcard patterns against the underlying tool name, so the same syntax works for built-ins, custom tools, and MCP tools — for example `"mymcp_*": "deny"` denies every tool from an MCP server."*

**Other top-level keys the config page lists:** `model`, `small_model`, `provider`, `server`, `shell`, `tools`, `command`, `share`, `attachment`, `formatter`, `lsp`, `theme`/`keybinds` (in `tui.json`), `snapshot`, `autoupdate`, `compaction`, `watcher`, `mcp`, `disabled_providers`/`enabled_providers`, `experimental`. On `experimental`: "The `experimental` key contains options that are under active development… Experimental options are not stable. They may change or be removed without notice." (`experimental.policies` currently gates which providers may be used.)

**AGENTS.md loading** — https://opencode.ai/docs/rules:
- Project rules: **`AGENTS.md`** in the project root. "You can provide custom instructions to opencode by creating an AGENTS.md file… It contains instructions that will be included in the LLM's context." Created/updated by the **`/init`** command; `/init` "will improve it in place instead of blindly replacing it."
- Global rules: **`~/.config/opencode/AGENTS.md`** — "This gets applied across all opencode sessions."
- **Claude Code compatibility is explicit:** "Project rules: `CLAUDE.md` in your project directory (used if no AGENTS.md exists). Global rules: `~/.claude/CLAUDE.md` (used if no `~/.config/opencode/AGENTS.md` exists)."
- **Precedence (verbatim):** "Local files by traversing up from the current directory (AGENTS.md, CLAUDE.md); Global file at `~/.config/opencode/AGENTS.md`. The first matching file wins in each category. For example, if you have both AGENTS.md and CLAUDE.md, only AGENTS.md is used."
- The `POST /session/:id/init` endpoint is described as "Analyze app and create AGENTS.md" — i.e. `/init` is reachable over HTTP.

---

## 6. What the sibling should cross-check against source

Ranked by how much the answer changes a design that builds on opencode:

1. **Is `tool.execute.after` a real hook with `(input, output)`, and can it rewrite the tool *result*?** Docs name it in the event list but never as a hook. If it can mutate a tool result, that is a text-injection channel the docs never advertise.
2. **Do `chat.message` / `chat.params`-style hooks exist in source?** The docs contain neither string. If source has them, the docs materially understate what a plugin can do (and vice versa: if source lacks them, there is genuinely **no** documented or undocumented way to mutate a prompt from a plugin, and `noReply` + the compaction hook are the only injection paths).
3. **Is there any hook firing at turn/session END** (post-assistant-message), or is observing `session.idle` on the `event` bus really the only option?
4. **Can a plugin answer a permission request?** Docs give an *endpoint* (`POST /session/:id/permissions/:permissionID`) and *events* (`permission.asked`/`permission.replied`), but no hook. A plugin holds a `client`, so it could in principle answer via the client — the docs never say so.
5. **Does the `/event` SSE bus emit exactly the plugins-page event list?** Docs never assert the two sets are equal.
6. **`session.prompt` `format` vs `outputFormat`** — the SDK page contradicts itself; source settles it.
7. **The `system` and `tools` fields in the POST message body** — listed, never explained.

## 7. Pages read
- https://opencode.ai/docs/plugins
- https://opencode.ai/docs/server
- https://opencode.ai/docs/sdk
- https://opencode.ai/docs/agents
- https://opencode.ai/docs/config
- https://opencode.ai/docs/rules

All stamped "Last updated: Jul 10, 2026", fetched 2026-07-12. Docs are unversioned — **they carry no "v1.17.13" marker anywhere**, so the mapping from these pages to the pinned version is itself an assumption the source-reader should confirm.
