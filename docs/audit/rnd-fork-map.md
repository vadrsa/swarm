# FORK-MAP — opencode v1.17.19 turn loop

Target: `sst/opencode`, tag `v1.17.19`, commit `dc927a7ff071741537cb0bdac7e09b5667ed568d`,
cloned into `/Users/vadrsa/git/swarm-rnd/opencode`. All citations below are
`file:line` against that exact commit — grep them, don't trust prose.

Two files, two layers:
- `packages/opencode/src/session/prompt.ts` — the OUTER loop (`runLoop`, `while(true)`
  at line 1088). Decides whether to run another step at all, assembles the system
  prompt, and decides when the whole multi-step turn ends and control returns to
  the user/caller.
- `packages/opencode/src/session/processor.ts` — the INNER step (`Service.process`,
  line 627). One model-call-plus-tool-round-trip. Returns `"compact" | "stop" |
  "continue"` back to the outer loop.

The earlier audit doc (`docs/audit/_hc-ocloop.md` §2.3) correctly identified
`processor.ts` as the tool-loop driver but explicitly had NOT traced its control
flow line-by-line, and did not know about `prompt.ts`'s `runLoop` at all. This doc
closes both gaps.

---

## a. Where does one turn iterate?

Two nested loops, not one:

**Outer loop — one iteration = one assistant-message step** (handles tool-call
round trips that need a fresh model call, compaction, subtasks):
`packages/opencode/src/session/prompt.ts:1088`

```ts
1088	        while (true) {
1089	          yield* status.set(sessionID, { type: "busy" })
1090	          yield* Effect.logInfo("loop", { "session.id": sessionID, step })
1091	
1092	          let msgs = yield* MessageV2.filterCompactedEffect(sessionID).pipe(
1093	            Effect.provideService(Database.Service, database),
1094	          )
```

The decision to go around the outer loop again vs. break lives at
`packages/opencode/src/session/prompt.ts:1319-1336`:

```ts
1319	            if (result === "stop") return "break" as const
1320	            if (result === "compact") {
1321	              yield* compaction.create({
1322	                sessionID,
1323	                agent: lastUser.agent,
1324	                model: lastUser.model,
1325	                auto: true,
1326	                overflow: !handle.message.finish,
1327	              })
1328	            }
1329	            return "continue" as const
1330	          }).pipe(
...
1334	          if (outcome === "break") break
1335	          continue
1336	        }
```

`result` here is the return value of `handle.process(...)` — the inner loop.

**Inner "loop" — actually a single step, not a loop over multiple model calls.**
It is called ONCE per outer-loop iteration. The actual model call + streamed
tool-call events happen inside `Service.process`:
`packages/opencode/src/session/processor.ts:627-646`

```ts
627	      const process = Effect.fn("SessionProcessor.process")(function* (streamInput: LLM.StreamInput) {
628	        yield* Effect.logInfo("[RND-FORK BUILD] processor.process turn start", {
629	          "session.id": input.sessionID,
630	          messageID: input.assistantMessage.id,
631	        })
632	        ctx.needsCompaction = false
633	        ctx.shouldBreak = (yield* config.get()).experimental?.continue_loop_on_deny !== true
...
640	            const stream = llm.stream(streamInput)
641	
642	            yield* stream.pipe(
643	              Stream.tap((event) => handleEvent(event)),
644	              Stream.takeUntil(() => ctx.needsCompaction),
645	              Stream.runDrain,
646	            )
```

Correction to the map's own framing: "the tool-loop" as commonly described (model
calls itself repeatedly until it stops requesting tools) is actually implemented
as the OUTER `while(true)` in `prompt.ts` calling the INNER single-shot
`processor.process` once per pass. `processor.ts` itself has no loop over
multiple model calls — it drains ONE `llm.stream()` (which internally may cover
several AI-SDK "steps"/tool-round-trips within one HTTP stream — see `step-start`/
`step-finish` events at `processor.ts:424-484` — but that's the provider's
multi-step tool-calling within a single stream, not opencode re-calling the model).
Whether to call the model AGAIN (a fresh `handle.process`) is entirely the outer
loop's decision, made after inspecting `result`.

(Line note: `processor.ts:628` shows the `[RND-FORK BUILD]` marker added for the
smoke test — see `smoke-test.txt`; the un-instrumented text was `"process"`.)

---

## b. Where is the system prompt assembled, per turn?

Immediately before each call to `handle.process`, inside the outer loop, at
`packages/opencode/src/session/prompt.ts:1255-1271`:

```ts
1255	            yield* plugin.trigger("experimental.chat.messages.transform", {}, { messages: msgs })
1256	
1257	            const [skills, env, instructions, mcpInstructions, modelMsgs] = yield* Effect.all([
1258	              sys.skills(agent),
1259	              sys.environment(model),
1260	              instruction.system().pipe(Effect.orDie),
1261	              sys.mcp(agent, session.permission),
1262	              MessageV2.toModelMessagesEffect(msgs, model),
1263	            ])
1264	            const system = [
1265	              ...env,
1266	              ...instructions,
1267	              ...(mcpInstructions ? [mcpInstructions] : []),
1268	              ...(skills ? [skills] : []),
1269	            ]
1270	            const format = lastUser.format ?? { type: "text" as const }
1271	            if (format.type === "json_schema") system.push(STRUCTURED_OUTPUT_SYSTEM_PROMPT)
```

`system` (an array of strings, in this exact order: environment block →
instruction files → MCP-server instructions → skills) is then handed straight
into the `process` call as the `system` field:
`packages/opencode/src/session/prompt.ts:1272-1286`

```ts
1272	            const result = yield* handle.process({
1273	              user: lastUser,
1274	              agent,
1275	              permission: session.permission,
1276	              sessionID,
1277	              parentSessionID: session.parentID,
1278	              system,
1279	              messages: [
1280	                ...modelMsgs,
1281	                ...(isLastStep ? [{ role: "assistant" as const, content: MAX_STEPS_PROMPT }] : []),
1282	              ],
1283	              tools,
1284	              model,
1285	              toolChoice: format.type === "json_schema" ? "required" : undefined,
1286	            })
```

Note this is reassembled from scratch on EVERY outer-loop pass (every step),
not cached across steps of the same turn — `sys.skills`, `sys.environment`,
`instruction.system()`, `sys.mcp()` are all re-invoked at line 1257-1262 each
time the `while(true)` loops around. This is the one plugin-visible seat named
in the audit doc (`experimental.chat.system.transform`) but note that hook is
NOT visible in this exact assembly block — grep confirms it fires deeper inside
`sys.environment`/`instruction.system`, not here; this block is where the pieces
get concatenated into the final `system` array actually sent to the model.

---

## c. Where does token usage / cost become available?

Type: `Usage`, defined in `packages/llm/src/schema/events.ts:51-74`:

```ts
51	export class Usage extends Schema.Class<Usage>("LLM.Usage")({
52	  inputTokens: Schema.optional(Schema.Number),
53	  outputTokens: Schema.optional(Schema.Number),
54	  nonCachedInputTokens: Schema.optional(Schema.Number),
55	  cacheReadInputTokens: Schema.optional(Schema.Number),
56	  cacheWriteInputTokens: Schema.optional(Schema.Number),
57	  reasoningTokens: Schema.optional(Schema.Number),
58	  totalTokens: Schema.optional(Schema.Number),
59	  providerMetadata: Schema.optional(ProviderMetadata),
60	}) {
```

That's the RAW provider-reported usage (one per AI-SDK `step-finish` event).
It becomes the session-level tracked struct via `Session.getUsage`,
`packages/opencode/src/session/session.ts:338-395` (field-normalization +
cost calc; excerpt of the shape that's actually stored):

```ts
338	export const getUsage = (input: { model: Provider.Model; usage: Usage; metadata?: ProviderMetadata }) => {
...
370	  const tokens = {
371	    total,
372	    input: adjustedInputTokens,
373	    output: safe(outputTokens - reasoningTokens),
374	    reasoning: reasoningTokens,
375	    cache: {
376	      write: cacheWriteInputTokens,
377	      read: cacheReadInputTokens,
378	    },
379	  }
...
390	  return {
391	    cost:
392	      typeof totalNanoAiu === "number" && Number.isFinite(totalNanoAiu) && totalNanoAiu >= 0
393	        ? new Decimal(totalNanoAiu).div(100_000_000_000).toNumber()
```

(cost calc continues past line 393 into tier-based `costInfo` — the `cost`/`tokens`
pair is the full return value of `getUsage`.)

It gets POPULATED — i.e. this is the exact point per-step usage is folded onto
the persisted assistant message — inside `processor.ts`'s `step-finish` handler,
`packages/opencode/src/session/processor.ts:435-446`:

```ts
435	          case "step-finish": {
436	            const completedSnapshot = yield* snapshot.track()
437	            yield* Effect.forEach(Object.keys(ctx.reasoningMap), finishReasoning)
438	            const usage = Session.getUsage({
439	              model: ctx.model,
440	              usage: value.usage ?? new Usage({}),
441	              metadata: value.providerMetadata,
442	            })
443	            ctx.assistantMessage.finish = value.reason
444	            ctx.assistantMessage.cost += usage.cost
445	            ctx.assistantMessage.tokens = usage.tokens
```

`ctx.assistantMessage.tokens` (type `SessionV1.Assistant["tokens"]`, shape
`{ total, input, output, reasoning, cache: { read, write } }` — matches the
`tokens` object built at `session.ts:370-379` above) and `.cost` (a running
float accumulator, note `+=` at line 444 — cost accumulates across multiple
`step-finish` events within one stream, e.g. multi-step tool calls inside a
single `llm.stream()`) are what the outer loop and the rest of the app read.
Confirmed live in the smoke test log: session-creation line shows the zeroed
shape before any turn (`tokens.input=0 tokens.output=0 tokens.reasoning=0
tokens.cache.read=0 tokens.cache.write=0`, see `smoke-test.txt`).

---

## d. Where does a turn END?

Two distinct "end" points, matching the two loops in (a):

**Step end (inner):** `processor.process` returns one of three `Result` values,
decided at `packages/opencode/src/session/processor.ts:679-681`:

```ts
679	          if (ctx.needsCompaction) return "compact"
680	          if (ctx.blocked || ctx.assistantMessage.error) return "stop"
681	          return "continue"
```

**Turn end (outer, user-visible):** the outer `while(true)` in `prompt.ts` decides
whether to `break` (hand control back to the caller/user) or loop again. There
are two break points:

1. Normal "model is done, no more tool calls to resolve" exit — checked BEFORE
   even calling the model again, at the top of the next pass, by inspecting the
   previous assistant message's `finish` reason and whether unresolved tool
   calls remain: `packages/opencode/src/session/prompt.ts:1111-1130`

```ts
1111	          if (
1112	            lastAssistant?.finish &&
1113	            !["tool-calls"].includes(lastAssistant.finish) &&
1114	            !hasToolCalls &&
1115	            lastUser.id < lastAssistant.id
1116	          ) {
...
1128	            yield* Effect.logInfo("exiting loop", { "session.id": sessionID })
1129	            break
1130	          }
```

(Confirmed live in the smoke test: `message="exiting loop" session.id=ses_...`
is the literal last log line before the process exits — `smoke-test.txt`.)

2. After a step completes, based on the inner `Result` returned by
   `handle.process`, at `packages/opencode/src/session/prompt.ts:1319-1336`
   (quoted in full under (a) above) — `"stop"` → `break` immediately;
   `"compact"` → schedule a compaction task then loop again; `"continue"` (or
   falling through) → loop again to build the next step.

Once the outer loop `break`s, `runLoop` does one more thing — prunes old
compaction artifacts and returns the final assistant message — at
`packages/opencode/src/session/prompt.ts:1338-1339`:

```ts
1338	        yield* compaction.prune({ sessionID }).pipe(Effect.ignore, Effect.forkIn(scope))
1339	        return yield* lastAssistant(sessionID)
```

That's the true end of a turn as opencode itself defines it — this is the
function (`runLoop`, `prompt.ts:1081`) that the outer HTTP/CLI/TUI layer awaits.

---

## Fork-depth note (extends `docs/audit/_hc-ocloop.md` §2.3)

The prior audit doc treated `processor.ts` as if it alone were "the tool-loop
driver" and had not traced its control flow. Having now read both files in
full: the real turn-end decision point — the ONLY place that decides whether
the user gets control back — is `prompt.ts:1088-1336` (`runLoop`), not
`processor.ts`. A fork wanting a turn-end gate (the audit doc's NO/PARTIAL
verdict on duties #1, #3, #5 — report-to-parent, reconcile-prompt, done-signal)
should hook the `outcome === "break"` decision at `prompt.ts:1334`, or the
pre-loop early-exit at `prompt.ts:1111-1130` — NOT inside `processor.ts`,
which only ever decides whether to run one more STEP within an
already-in-progress turn, not whether the turn itself ends.
