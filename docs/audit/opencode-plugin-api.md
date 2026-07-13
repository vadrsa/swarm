# opencode v1.17.13 — plugin API: FACTS

Source-spelunk of the **installed** opencode, not the docs. Ground truth read on disk:

- `/Users/vadrsa/.opencode/node_modules/@opencode-ai/plugin/dist/**` (= `~/.config/opencode/node_modules/@opencode-ai/plugin/dist/**`; identical, `@opencode-ai/plugin@1.17.13`)
- `/Users/vadrsa/.opencode/node_modules/@opencode-ai/sdk/dist/v2/gen/types.gen.d.ts`
- `~/.config/opencode/plugins/bridgespace-notify.js` (installed working plugin)
- `/Users/vadrsa/.opencode/bin/opencode` — 130 MB Bun single-file executable, Mach-O arm64. The bundled JS is **plain text inside it** and greppable with `grep -a`. All "binary" citations below are real grep hits.

Every claim is tagged **VERIFIED** (I read the installed source), **DOCUMENTED** (only the official docs say so), or **REASONED** (inferred).

---

## 0. The one-line answer

**This is not "event hooks only". opencode genuinely lets a plugin edit the agent loop.**

Two independent APIs ship in this build:

- **v1 `Hooks`** — every hook is `(input, output) => Promise<void>`. The return value is structurally ignored; the hook's *only* power is to **mutate the `output` object in place**, and opencode reads that object back after awaiting. A v1 plugin can rewrite the message array sent to the model, rewrite the system prompt, rewrite tool args, rewrite tool descriptions the model sees, rewrite model params/headers, rewrite the assistant's output text, and add new tools. **VERIFIED.**
- **v2 `PluginContext`** (`@opencode-ai/plugin/v2/promise` and `/v2/effect`) — undocumented on the plugins page but **fully wired**: opencode's own provider integrations are written with it. Its `aisdk.language` hook hands you the `LanguageModelV3` instance and lets you **replace it**, so a plugin can wrap the model and intercept every single LLM call. **VERIFIED end-to-end.**

The one thing that is **shallower than the types promise**: `permission.ask` is declared in the `.d.ts` but **never dispatched anywhere in the binary**. It is dead surface in 1.17.13. See §4.

---

## 1. The v1 plugin shape

`@opencode-ai/plugin/dist/index.d.ts:36-56` — **VERIFIED**:

```ts
export type PluginInput = {
    client: ReturnType<typeof createOpencodeClient>;
    project: Project;
    directory: string;
    worktree: string;
    experimental_workspace: { register(type: string, adapter: WorkspaceAdapter): void };
    serverUrl: URL;
    $: BunShell;
};
export type PluginOptions = Record<string, unknown>;
export type Plugin = (input: PluginInput, options?: PluginOptions) => Promise<Hooks>;
```

The installed prior art matches (`~/.config/opencode/plugins/bridgespace-notify.js`) — an async function taking `{ $ }` and returning a hooks object:

```js
export const BridgeSpaceNotifyPlugin = async ({ $ }) => {
  return {
    event: async ({ event }) => {
      if ((event?.type ?? "") === "session.idle") {
        await $`node ${helper} --agent opencode --event stop`.quiet();
      }
    },
  };
};
```

**Loading — VERIFIED** (binary, the `config-plugin` effect). Plugins come from two places:
1. the config `plugin` / `plugins` array — bare npm spec, `file://…`, or `./relative` path (`Config.plugin?: Array<string | [string, PluginOptions]>`, `index.d.ts:48-50`);
2. a directory scan: `glob("{plugin,plugins}/*.{ts,js}", { cwd: <config dir>, ... })`, sorted — i.e. `~/.config/opencode/plugin*/…` and project-local `plugin*/…`.

---

## 2. The mutation contract (this is the whole ballgame)

`index.d.ts:173-322` declares **every** hook as `(input, output) => Promise<void>`. `Promise<void>` means **a returned value is thrown away**. So the API is: *opencode builds an `output` object, hands it to you, and reads it back after you await.*

The dispatcher — **VERIFIED**, grepped from the binary:

```js
X = v.fn("Plugin.trigger")(function*(W, K, B) {   // W = hook name, K = input, B = output
  if (!W) return B;
  let U = yield* p0.get(Y);
  for (let z of U.hooks) {
    let M = z[W];
    if (!M) continue;
    yield* v.promise(async () => M(K, B));        // await hook(input, output); return value discarded
  }
  return B                                        // same object reference handed back to the caller
})
```

Two consumption patterns at the call sites, and **the difference matters to plugin authors**:

- **return-value sites** — the caller does `let k = yield* trigger(...)` and reads `k.foo`. Here both *in-place mutation* and *wholesale reassignment* (`output.foo = newThing`) are honored.
- **outer-variable sites** — the caller passes an existing object/array (`trigger("...", input, { args: g })`) and afterwards reads **`g`**, not `output.args`. Here **only in-place mutation is honored**; `output.args = {…}` is silently dropped.

> **Practical rule for a plugin author: always mutate in place** (`output.messages.push(…)`, `Object.assign(output.args, …)`, `output.system[0] = …`). Never reassign the top-level property unless you have checked which pattern that specific hook uses. The table below marks it.

**Blocking is by exception, not by return value — VERIFIED.** `Plugin.trigger` has no try/catch of its own, and the `tool.execute.before` call site does not catch either, so a hook that **throws** short-circuits the Effect chain and `tool.execute(...)` is never reached; the failure surfaces as `session.next.tool.failed` / `ToolStateError` on that one tool call. The session is not killed. That throw is opencode's real BLOCK primitive.

Lifecycle hooks (`config`, `dispose`) *are* wrapped — `tryPromise(...).pipe(tapError(logError("plugin config hook failed")), ignore)` — so those log-and-continue. **VERIFIED.**

---

## 3. THE TABLE

Mutation power legend: **OBSERVE** = fire-and-forget · **MUTATE-CONTEXT** = changes what the model sees this turn · **MUTATE-PARAMS** = changes model params/headers/model choice · **INTERCEPT-TOOL** = changes tool dispatch or its result · **ADD-TOOL** = registers new callable tools · **BLOCK** = can prevent the operation · **REPLACE-MODEL** = swaps the LanguageModel object itself.

### v1 `Hooks` — `@opencode-ai/plugin/dist/index.d.ts:173-322`

| hook | when it fires | args (`input` → `output`) | power | mutation semantics | citation |
|---|---|---|---|---|---|
| `event` | on every event on the bus (incl. `session.idle`, `session.error`, message/part updates) | `{ event: Event }` — **no `output`** | **OBSERVE** | Nothing to mutate. Fired via `for (let M of K) M.event?.({event:{id,type,properties}})` inside `bus.listen`. This is the only true fire-and-forget hook. Covers **turn-end / idle (g)**. | `.d.ts:175-177`; binary `$.listen((N)=>{...M.event?.(...)})` — **VERIFIED** |
| `config` | once at plugin load, with the resolved config | `(input: Config)` — **no `output`** | **MUTATE-PARAMS** (config object is passed by reference) | Called directly as `N.config?.(w)`, errors caught + logged + ignored. Mutating the passed config object is the documented way to inject config. Covers **session start (f)** only in the "process start" sense — see §5. | `.d.ts:178`; binary `tryPromise({try:()=>Promise.resolve(N.config?.(w))})` — **VERIFIED** |
| `dispose` | at shutdown (Effect finalizer) | `()` | **OBSERVE** | Cleanup only. Errors logged + ignored. | `.d.ts:174`; binary `addFinalizer(...N.dispose?.()...)` — **VERIFIED** |
| `tool` | at load — it is a **map**, not a function | `{ [name: string]: ToolDefinition }` | **ADD-TOOL** ✅ | A plugin declares new tools the model can call: `tool({ description, args: zodShape, execute(args, ctx) })`. `ToolContext` gives `sessionID, messageID, agent, directory, worktree, abort, metadata(), ask()`. `ask()` is how a custom tool requests permission. | `.d.ts:179-181`, `tool.d.ts:1-56` — **VERIFIED** (type); dispatch site not independently located in the binary — **REASONED** that it is read at load like `auth`/`provider` |
| `auth` | at load / on `opencode auth login` | `AuthHook { provider, loader?, methods[] }` | **ADD-AUTH** (out of loop scope) | Registers OAuth/API-key auth flows for a provider. Not an agent-loop hook. | `.d.ts:62-125,182` — **VERIFIED** (type only) |
| `provider` | at load | `ProviderHook { id, models?(provider, ctx) }` | **MUTATE-PARAMS** | Contributes/overrides the model catalog for a provider. | `.d.ts:167-170,183` — **VERIFIED** (type only) |
| `chat.message` | a new user message is received, before it is processed | `{ sessionID, agent?, model?, messageID?, variant? }` → `{ message: UserMessage, parts: Part[] }` | **MUTATE-CONTEXT** ✅ | **Outer-variable pattern.** Binary: `trigger("chat.message", {...}, {message:O, parts:fe}); let z = yield* s.forEach(fe, ...)` — `fe` (the parts array) is read afterward. **Mutate `output.parts` in place** (push a part → you have injected content into this turn's user message). Reassignment dropped. This is capability **(a)**. | `.d.ts:187-199`; binary trigger site — **VERIFIED** |
| `chat.params` | before the model call, per turn | `{ sessionID, agent, model, provider, message }` → `{ temperature, topP, topK, maxOutputTokens, options }` | **MUTATE-PARAMS** ✅ | **Return-value pattern.** Binary: `k = yield* trigger("chat.params", …)` → returned as `params:k` → consumed at the model call as `temperature:i.params.temperature, topP:…, topK:…, maxOutputTokens:…, providerOptions:i.params.options`. Both mutation and reassignment honored. `options` → provider options passthrough. Capability **(b)**. | `.d.ts:203-215`; binary — **VERIFIED** |
| `chat.headers` | before the model call, per turn | `{ sessionID, agent, model, provider, message }` → `{ headers: Record<string,string> }` | **MUTATE-PARAMS** ✅ | Return-value pattern: `{headers:f} = yield* trigger("chat.headers", …, {headers:{}})`, `f` used as the request headers. Lets you inject arbitrary HTTP headers on the LLM request. | `.d.ts:216-224`; binary — **VERIFIED** (destructure seen; exact fetch consumption not traced → HIGH but not absolute) |
| `permission.ask` | **NEVER — dead in this build** | `(input: Permission, output: { status: "ask"\|"deny"\|"allow" })` | **⚠️ NONE (declared, never dispatched)** | **Zero `.trigger("permission.ask")` call sites, and the bare string `permission.ask` does not occur in the 130 MB binary at all** — every `permission.ask*` hit is `"permission.asked"` / `"permission.replied"`, a *separate* event-bus permission subsystem unrelated to `Plugin.trigger`. The type promises BLOCK; the runtime does not deliver it. **Do not build a gate on this hook.** | `.d.ts:225-227` (type exists); binary: **absence proven by exhaustive grep, re-run independently** — **VERIFIED (negative)** |
| `command.execute.before` | a slash-command is about to run | `{ command, sessionID, arguments }` → `{ parts: Part[] }` | **MUTATE-CONTEXT** ✅ + **BLOCK** (by throw) | Outer-variable: `trigger("command.execute.before", …, {parts:Ye}); let B = yield* we({sessionID, parts:Ye, …})` — `Ye` is what the prompt executor receives. Mutate in place to rewrite what a command expands into. | `.d.ts:228-234`; binary — **VERIFIED** |
| `tool.execute.before` | immediately before a tool executes | `{ tool, sessionID, callID }` → `{ args: any }` | **INTERCEPT-TOOL** ✅ + **BLOCK** ✅ | Outer-variable: `trigger("tool.execute.before", {tool:y.id, …}, {args:g}); let W = yield* y.execute(g, c)` — the tool runs with **`g`**. So `Object.assign(output.args, …)` / `delete output.args.x` **is honored**; `output.args = {…}` is **dropped**. **Throwing here blocks the tool call** (Effect short-circuits; `y.execute` never runs; surfaces as `ToolStateError` on that call, session survives). Capabilities **(c)** and **(d)** — d only via throw. | `.d.ts:235-241`; binary — **VERIFIED** |
| `tool.execute.after` | after a tool returns, before the result reaches the model | `{ tool, sessionID, callID, args }` → `{ title, output, metadata }` | **INTERCEPT-TOOL** ✅ | Outer-variable: `trigger("tool.execute.after", {…}, i); return i` — `i` is the result object, returned as-is. **Mutate `output.output` in place to rewrite what the model sees as the tool's result.** Reassigning the whole object is dropped. | `.d.ts:249-258`; binary — **VERIFIED** |
| `shell.env` | before spawning a shell (bash tool etc.) | `{ cwd, sessionID?, callID? }` → `{ env: Record<string,string> }` | **INTERCEPT-TOOL** ✅ | Return-value: `Y = yield* trigger("shell.env", …, {env:{}})` then `env: {...Y.env, TERM:"dumb"}` spread into the spawned process. Inject env vars into every shell the agent runs. | `.d.ts:242-248`; binary — **VERIFIED** |
| `experimental.chat.messages.transform` | before the message list is converted to model messages | `{}` → `{ messages: { info: Message; parts: Part[] }[] }` | **MUTATE-CONTEXT** ✅✅ **the big one** | Outer-variable: `trigger("experimental.chat.messages.transform", {}, {messages: C}); … toModelMessagesEffect(C, z)` — `C` **is the array sent to the model**. Push/splice/edit in place → you have rewritten the entire conversation the model sees this turn (inject context, redact, reorder, drop). Also runs on the compaction path (`{messages: Ze}`). `output.messages = newArray` is **dropped** — splice in place instead. Capability **(a)**, in full. | `.d.ts:259-264`; binary (2 call sites) — **VERIFIED** |
| `experimental.chat.system.transform` | before the system prompt is assembled | `{ sessionID?, model }` → `{ system: string[] }` | **MUTATE-CONTEXT** ✅✅ | Outer-variable: `trigger(…, {system:l})` then `l` is what builds the request (`d.instructions = l.join(…)`). **Mutate the array in place → you own the system prompt.** Capability **(b)**. | `.d.ts:265-270`; binary — **VERIFIED** |
| `tool.definition` | when tool definitions are built for the LLM | `{ toolID }` → `{ description: string, parameters: any }` (runtime also carries `jsonSchema`) | **MUTATE-CONTEXT / INTERCEPT-TOOL** ✅ | Cleanest proof in the codebase — a fresh object is built *for the hook* and then read back: `let j = {description:Q.description, parameters:Q.parameters, jsonSchema:Q.jsonSchema}; yield* trigger("tool.definition", {toolID:Q.id}, j); … return {id:Q.id, description:[j.description,…].join(…), parameters:j.parameters, jsonSchema:ro, …}`. It even branches on whether `j.jsonSchema` changed. **Rewrite any built-in tool's description/schema as the model sees it.** Capability **(e′)** — reshape existing tools. | `.d.ts:316-321`; binary — **VERIFIED** |
| `experimental.provider.small_model` | when resolving the "small/cheap" model | `{ provider }` → `{ model?: ModelV2 }` | **MUTATE-PARAMS** ✅ | Return-value: `M = yield* trigger(…, {model: void 0}); if (M.model) return {...M.model, …}` — short-circuits the built-in heuristic. | `.d.ts:271-275`; binary — **VERIFIED** |
| `experimental.session.compacting` | before compaction runs | `{ sessionID }` → `{ context: string[], prompt?: string }` | **MUTATE-CONTEXT** ✅ | Return-value: `Ve = yield* trigger(…); je = Ve.prompt ?? ui({previousSummary:M, context:Ve.context})`. Set `prompt` to **replace the compaction prompt entirely**; push to `context` to append. | `.d.ts:283-288`; binary — **VERIFIED** |
| `experimental.compaction.autocontinue` | after compaction, before the synthetic "continue" turn | `{ sessionID, agent, model, provider, message, overflow }` → `{ enabled: boolean }` | **BLOCK** ✅ | Return-value, read straight into an `if`: `if ((yield* trigger(…, {enabled:!0})).enabled) { … }`. Set `false` → no synthetic continue turn. | `.d.ts:296-305`; binary — **VERIFIED** |
| `experimental.text.complete` | when an assistant text part completes | `{ sessionID, messageID, partID }` → `{ text: string }` | **MUTATE-CONTEXT** ✅ (output side) | Return-value, assigned straight back: `i.currentText.text = (yield* trigger("experimental.text.complete", …, {text: i.currentText.text})).text`. **Rewrite the assistant's own output text** before it is persisted/streamed. | `.d.ts:306-312`; binary — **VERIFIED** |

**Undeclared hooks: none. VERIFIED (negative).** A sweep of every `.trigger("` call site in the binary yields exactly the 14 dispatched names above — no hidden ones. (`.trigger("file.open")` / `.trigger("tab.new")` hits are a same-named **TUI command bus**, unrelated to `Plugin.trigger`. False positives, confirmed by context.)

### v2 `PluginContext` — `@opencode-ai/plugin/dist/v2/{promise,effect}/*.d.ts`

Not on the plugins docs page, but **wired and in production use by opencode itself**.

| hook | when it fires | args | power | semantics | citation |
|---|---|---|---|---|---|
| `aisdk.language` | when the `LanguageModelV3` for a model is resolved (before each generation, memoized per `provider/model/variant`) | `{ readonly model: ModelV2Info; readonly sdk: any; readonly options: Record<string,any>; language?: LanguageModelV3 }` | **REPLACE-MODEL** ✅✅✅ | **The deepest hook in the system.** Callbacks are folded over one accumulator object; then: `y = k.language ?? m.languageModel(a.api.id)`. **If you set `input.language`, your object is what opencode calls generate/stream on.** Set it to a `wrapLanguageModel(input.language ?? default, …)` and you intercept **every LLM call** — messages in, stream out. Consumed at `Agent.generate` → `q = yield* C.getLanguage(b)`. | `v2/promise/aisdk.d.ts`; binary `AISDK.language` resolver + `Agent.generate` — **VERIFIED end-to-end** |
| `aisdk.sdk` | when the provider SDK object is constructed | `{ model, package, options, sdk?: any }` | **MUTATE-PARAMS / REPLACE-SDK** | Same fold; set `input.sdk` to supply/replace the provider SDK. **This is how opencode ships its own providers** — e.g. `cohere`: `o.aisdk.sdk(function*(e){ if (e.package !== "@ai-sdk/cohere") return; e.sdk = r.createCohere(e.options) })`. Proof the v2 API is not dead. | binary — **VERIFIED** |
| `agent.transform` | at agent-catalog load / reload | `AgentDraft { list(), get(id), default(id), update(id, fn), remove(id) }` over `AgentV2Info` | **MUTATE-CONTEXT / MUTATE-PARAMS** ✅ | `AgentV2Info = { id, model?: ModelRef, request: ProviderRequest, system?: string, description?, mode, hidden, color?, steps?, permissions: PermissionV2Ruleset }`. So a plugin can **rewrite any agent's system prompt, swap its model, change its permission ruleset, change its step budget**, add/remove agents, set the default. Note: **no `tools` field** — tool availability is not mutable through this record. | `v2/effect/agent.d.ts`; `sdk/dist/v2/gen/types.gen.d.ts` (`AgentV2Info`) — **VERIFIED** |
| `catalog.transform` | at model-catalog load | `CatalogDraft` — provider `list/get/update/remove`, model `get/update/remove`, `model.default.get/set` | **MUTATE-PARAMS** | Rewrite the model catalog; set the default model. | `v2/effect/catalog.d.ts` — **VERIFIED** (type) |
| `command.transform` | at command load | `CommandDraft { list, get, update, remove }` over `CommandV2Info { name, template, description?, agent?, model?, subtask? }` | **MUTATE-CONTEXT** | Rewrite slash-command templates. | `v2/effect/command.d.ts`; `types.gen.d.ts` — **VERIFIED** (type) |
| `skill.transform` | at skill load | `SkillDraft { source(SkillV2Source), list() }` | **ADD-CONTEXT** | Register skill sources: `{type:"directory",path}` / `{type:"url",url}` / `{type:"embedded",skill:{name,description,slash,location,content}}`. **Inject skills programmatically.** | `v2/effect/skill.d.ts`; `types.gen.d.ts` — **VERIFIED** (type) |
| `reference.transform` | at reference load | `ReferenceDraft { add(name, ReferenceLocalSource\|ReferenceGitSource), remove, list }` | **ADD-CONTEXT** | Register reference sources. | `v2/effect/reference.d.ts` — **VERIFIED** (type) |
| `integration.transform` + `integration.connection` | integration/credential load | `IntegrationDraft` + `connection.active(id)` / `connection.resolve(conn)` | **ADD-AUTH** | OAuth/key/env credential methods. Out of agent-loop scope. | `v2/effect/integration.d.ts` — **VERIFIED** (type) |
| `plugin.add` / `plugin.remove` | any time | `PluginDomain.add(plugin)` / `.remove(id)` | **META** | A plugin can register/unregister other plugins at runtime. | `v2/effect/plugin.d.ts` — **VERIFIED** (type) |

**v2 shape and loading — VERIFIED (binary).** The loader schema-decodes a module's **default export** against a union:

```js
var fs = i.Struct({ default: i.Union([
  i.Struct({ id: i.String, effect: i.declare((o)=>typeof o==="function") }),   // Effect flavor
  i.Struct({ id: i.String, setup:  i.declare((o)=>typeof o==="function") })    // Promise flavor
])})
```
…then `f = "effect" in c ? c : oo.fromPromise(c)` and `o.plugin.add({ id: f.id, effect: (u)=>f.effect({...u, options}) })`.

Promise flavor (`v2/promise/plugin.d.ts`, **VERIFIED**) — note the field is **`setup`**, not `effect`:

```ts
export interface Plugin { readonly id: string; readonly setup: (context: PluginContext) => Promise<void> | void }
export declare function define(plugin: Plugin): Plugin;     // identity fn, for type inference only
export type Hooks<Spec> = { readonly [Name in keyof Spec]:
   (callback: (input: Spec[Name]) => Promise<void> | void) => Promise<Registration> };
```

Minimal v2 plugin that wraps every LLM call:

```ts
import { define } from "@opencode-ai/plugin/v2/promise";

export default define({
  id: "my-plugin",
  async setup(ctx) {
    await ctx.aisdk.language(async (input) => {
      const original = input.language ?? input.sdk.languageModel(input.model.api.id);
      input.language = wrapLanguageModel(original, myMiddleware);   // mutate in place
    });
    await ctx.agent.transform((draft) => {
      for (const a of draft.list()) draft.update(a.id, (info) => { info.system = (info.system ?? "") + "\n…"; });
    });
  },
});
```

---

## 4. What is shallower than hoped — say it plainly

1. **`permission.ask` does not exist at runtime.** It is in the `.d.ts` with a `status: "ask"|"deny"|"allow"` output that reads exactly like a policy gate, and it is **never dispatched**. If a design leans on "we'll approve/deny tool calls via `permission.ask`", that design is built on a type that lies. Blocking must be done by **throwing inside `tool.execute.before`** instead. **VERIFIED (negative — exhaustive grep of the binary).**
2. **No session-start / session-resume hook.** Nothing in the hook list fires "a session began" or "a session was resumed". The nearest things are: `config` (fires once at *process* load, not per session), and the `event` hook, through which you can *observe* session lifecycle events on the bus but not act inside the turn. To inject at the top of a session you must do it in `experimental.chat.messages.transform` / `chat.message` and detect first-turn yourself. Capability **(f)** is **NOT** directly served. **VERIFIED.**
3. **Turn-end is observe-only.** `session.idle` arrives through `event` — fire-and-forget, no `output`, no way to say "actually, keep going". (`experimental.compaction.autocontinue` can *suppress* a continue turn but cannot *add* one.) Capability **(g)** = OBSERVE only. **VERIFIED.**
4. **Reassignment vs in-place is an unmarked trap.** Half the hooks read their `output` back from the trigger's return value; half read an outer variable they passed in by reference. `output.args = {...}` in `tool.execute.before` — the most natural thing an author writes — is **silently ignored**. No type, doc, or runtime warning tells you this. **VERIFIED.**
5. **Errors in per-turn hooks are not sandboxed.** `Plugin.trigger` has no try/catch; a throw propagates into the operation (which is what makes blocking work, but also means an *accidental* throw in, say, `chat.params` will break the turn). Only `config` and `dispose` are explicitly caught-and-ignored. **VERIFIED.**
6. **v2 is undocumented.** The `aisdk.language` / `agent.transform` power is real and wired, but it is not on `opencode.ai/docs/plugins`, ships under a `v2/` subpath, and the two flavors disagree on the field name (`effect` vs `setup`). It is production-grade for opencode's own use; for a third party it is an unstable-by-omission surface. **VERIFIED** (wired) / **REASONED** (stability judgment).

## 5. Capability checklist (the question as asked)

| capability | served? | by what |
|---|---|---|
| (a) inject/modify the message or context the model sees THIS turn | **YES, fully** | `experimental.chat.messages.transform` (mutate the array in place = own the whole conversation), `chat.message` (mutate `parts`) |
| (b) alter model params / system prompt | **YES, fully** | `chat.params`, `chat.headers`, `experimental.chat.system.transform`, `experimental.provider.small_model`; v2 `agent.transform` (`system`, `model`), `catalog.transform` |
| (c) intercept or replace TOOL dispatch | **YES** | `tool.execute.before` (rewrite args in place), `tool.execute.after` (rewrite the result the model sees), `shell.env`, `tool.definition` (rewrite the schema/description the model sees) |
| (d) block / allow | **PARTLY — by throwing, not by returning** | throw in `tool.execute.before` → tool never runs (`ToolStateError`). `experimental.compaction.autocontinue` → `enabled:false`. **`permission.ask` is dead.** |
| (e) add new tools | **YES** | the `tool` hook — a map of `ToolDefinition` (zod args + `execute`), with a `ToolContext` that includes `ask()` for permission |
| (f) fire on session start / resume | **NO** | no such hook. `config` = process load; `event` = observe-only |
| (g) fire on turn end / idle | **OBSERVE ONLY** | `event` → `session.idle` (exactly what the installed `bridgespace-notify.js` plugin uses) |
| **bonus: intercept the model call itself** | **YES (v2)** | `aisdk.language` → replace the `LanguageModelV3`; wrap it and you see every request/response |

## 6. Verdict

**opencode's plugin API genuinely lets a plugin edit the agent loop.** It is materially deeper than Claude Code's hooks: those are out-of-process shell callbacks that communicate by exit code and stdout JSON, whereas opencode loads your JavaScript **in-process** and hands you the actual live objects — the message array, the system-prompt array, the tool args, the tool result, the tool schemas, the sampling params, and (v2) the language-model object itself — with the contract "mutate this and I will use what you leave behind."

The honest caveats, in the order they will bite:
- **No session-start hook** and **turn-end is observe-only**. If a design needs "on session start, inject X" or "on idle, decide whether to continue", the API does not offer a first-class seat; you must synthesize it from `event` + a first-turn check inside `experimental.chat.messages.transform`.
- **`permission.ask` is a declared-but-dead type.** Block by throwing in `tool.execute.before`.
- **In-place mutation only** for roughly half the hooks, with no signal telling you which half.
- The deepest capability (**replace the model object**) is in the **undocumented v2 API** — real and load-bearing for opencode's own providers, but unversioned in the docs.

So: not "shallower than hoped" in *power* — it is deeper than Claude Code's hooks by a wide margin, and the `experimental.chat.messages.transform` + `aisdk.language` pair is enough to build essentially any middleware over the loop. It **is** shallower than hoped in *lifecycle coverage* (no session start; idle is observe-only) and in *honesty of the type surface* (`permission.ask`).
