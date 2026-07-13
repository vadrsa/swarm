# opencode-as-swarm-harness — synthesized digest

Read in full: `OPENCODE-PLUGIN.md` (949 ln), `OPENCODE-PLUGIN-RED.md` (736 ln), `opencode-plugin-api.md`, `opencode-plugin-priorart.md`, `opencode-plugin-probe.md`, `opencode-priorart-docs.md`, `oc-red-relab.md`. This is distillation only — no new opinions added.

---

## 1. The question, precisely

Can a custom **opencode plugin** make opencode a first-class swarm harness by injecting swarm's six primitives — delivery, event, doorbell, restore, identity, spawn/pane — into opencode's agent loop, matching or beating what Claude Code's hooks give swarm today?

The six-item checklist swarm needs (from `bin/swarm` + `HARNESS.md`, OPENCODE-PLUGIN.md §1): delivery (`cmd_deliver`), event (`cmd_event`), doorbell (`ring_doorbell_once`), restore (`cmd_restore`), identity (`SWARM_AGENT_ID` env), spawn/pane (herdr pane running the CLI). Two invariants any harness must preserve: **"a message is a claim on ONE turn"** and **"delivered means delivered"** — the file moves to `delivered/` only because a turn *consumed* it, never because a sender *sent* it.

## 2. What opencode is + its plugin/extension model

opencode ships a **server** (every instance, TUI included, is a client of its own HTTP server) plus an **in-process plugin API**. Two APIs coexist (`opencode-plugin-api.md` §0, §3):

- **v1 `Hooks`**: every hook is `(input, output) => Promise<void>`. Return value is discarded (`Plugin.trigger`, traced to binary: `for (let M of K) await M(K,B); return B`) — the only power is **mutating `output` in place**. ~14 dispatched hook names, verified by exhaustive grep of the binary (no hidden ones).
- **v2 `PluginContext`** (`aisdk.language`, `agent.transform`, etc.) — undocumented, but fully wired; lets a plugin **replace the `LanguageModelV3` object itself** and intercept every model call. Real, verified end-to-end, but the design explicitly does NOT use it (§7 NOT-list).

Key hooks and their power (api doc §3, cross-verified live by `oc-probe`):
- `experimental.chat.messages.transform` — rewrites the **whole conversation the model sees this turn**. The "big one," but per-call view only.
- `experimental.chat.system.transform` — owns the system prompt every turn.
- `event` → `session.idle` — the only true fire-and-forget hook (nothing awaits it); turn-end signal.
- `tool` (map) — register new model-callable tools (verified: registered `swarm_probe_ping`, model called it).
- `tool.execute.before/.after` — rewrite args/results; **throwing** in `.before` blocks the tool (surfaces as `ToolStateError`, session survives).
- `shell.env` — inject env into every shell the agent runs.
- `experimental.session.compacting` — shape the compaction prompt; **the one hook opencode's own docs example is literally a multi-agent swarm continuation prompt.**

**What a plugin cannot do:**
- **No session-start/resume hook.** `config` fires once per *process*, not per session.
- **Turn-end is observe-only.** `session.idle` carries no `output` — a plugin cannot force a continuation from inside the hook; it must prompt the session like anyone else.
- **`permission.ask` is DEAD CODE.** Declared in the `.d.ts` with `output:{status:"ask"|"deny"|"allow"}`, reads exactly like a policy gate, and the string never occurs in the 130MB binary (every hit is the unrelated `permission.asked` event). Verified negative by exhaustive grep, independently re-confirmed by `ocr-lab`.
- **In-place mutation only, unmarked which half.** Roughly half the hooks read `output` back from an outer variable (mutate-in-place only, `output.args={...}` silently dropped); half read the trigger's return (either works). No type/doc/runtime signal distinguishes them.
- **Per-turn hooks are unsandboxed** — `Plugin.trigger` has no try/catch, so an accidental throw in e.g. `chat.params` kills the turn. Only `config`/`dispose` are caught-and-ignored.

**A parallel finding that reframes everything (`opencode-plugin-priorart.md`):** the **HTTP server itself**, driven externally with zero plugin code, already gives 5 of 6 primitives — delivery via `POST /session/{id}/prompt_async` (queues mid-turn, doesn't drop/interrupt), event via `GET /event` SSE, restore via `noReply:true` silent context push, spawn via `POST /session` with `parentID` (native parent/child session trees), identity via per-call `system` string. The plugin's real, narrow job becomes: (1) `experimental.session.compacting` for restore-by-construction, (2) a custom `swarm_send`/`swarm_spawn` tool, (3) `shell.env` for ambient identity. **"Server-primary, plugin-adjunct."**

## 3. The verdict: buildable?

**Yes — build it.** Direct quote, OPENCODE-PLUGIN.md §0: *"Yes — and the operator's hypothesis is confirmed, but the winning design is not the one the hypothesis pointed at."* And its closing line (§10): *"Build it."*

Recommendation: a **third `--agent` kind, `opencode`**, inside the existing `HARNESS.md` frame (no new concepts — `--agent <kind>` already selects the launcher body). Unlike FLEET/archived `HARNESS.md` doctrine ("prefer opencode for leaf work"), this design claims an opencode agent built this way is a **full participant** — receives mail, reports, restores, spawns — not a leaf. For one-shot completions, FLEET's thin `opencode run` path remains correct and cheaper (§4: "For leaves: no — FLEET is still right").

**The mechanism (the "pump"):** `swarm send` keeps writing its durable queue file exactly as today; it does NOT POST mail directly. The recipient's own plugin wakes on `session.idle`, pops one message, writes it via `noReply:true` (persists, provokes no turn), then **rings its own next turn** (self-ring), and marks `delivered/` only at the *following* idle once a turn has provably run with the message in context (two-phase delivery). This replaces `ring_doorbell_once`'s "THE ONE UNPROVEN MECHANISM" (bin/swarm:699-735, a herdr send-text + bracketed paste + settle-loop + prompt-heuristic screen scrape) with one HTTP POST returning a status code.

**Important: the mechanism as originally drafted was WRONG and had to be corrected by the red team** — see §5 below. The corrected version is what "buildable" refers to.

## 4. The security caveat (load-bearing)

Two compounding facts, both VERIFIED independently by the parent, `oc-priorart`, and re-run hostilely by `ocr-lab` on the current binary (1.17.18):

- **The server is unauthenticated by default.** It prints its own warning: `"Warning: OPENCODE_SERVER_PASSWORD is not set; server is unsecured"`. Any local process can drive any agent — prompt it, and run arbitrary shell via `POST /session/{id}/shell`.
- **Sessions are NOT scoped by directory.** A per-agent `--dir` does **not** isolate the session listing. Numbers, from two independent runs:
  - `oc-red`'s original probe (a fresh, empty directory): **93 sessions**, from every other directory on the host.
  - `ocr-lab`'s independent re-run (TUI on its own pinned port, own `--dir`): **92 sessions returned, 91 from other directories.**
  - All sessions live under a shared `global` project regardless of `--dir`.
- **The obvious fix (password) only half-works.** The session store is a **world-readable SQLite file** (`~/.local/share/opencode/opencode.db`, mode `-rw-r--r--`). Any local process can dump every agent's messages with `opencode db "SELECT …"` — no server, no port, no password needed. Verified: **1,279 messages, straight off disk.**

The resulting table (OPENCODE-PLUGIN.md §6.1):

| Barrier | Stops driving another agent (HTTP: prompts, shell)? | Stops reading another agent's conversation? |
|---|---|---|
| `OPENCODE_SERVER_PASSWORD` + loopback | yes — load-bearing | **no** — the store is readable on disk regardless |

Framing (doc's own words): for swarm's actual deployment shape — a tree of agents the operator owns, on the operator's own machine, already sharing `.swarm/`, journals, and the repo — mutual **readability** is *already true* and not a new exposure. What **is** newly opened is the **drive/shell** path, and a per-agent `OPENCODE_SERVER_PASSWORD` is what closes that — stated as a **design requirement**, not optional hardening (elevated from a risk bullet to a requirement specifically because of these numbers).

## 5. What the red team challenged — landed vs. missed

`oc-red` (with child `ocr-lab`, who re-ran experiments at the SQLite-store level with positive controls rather than trusting model recall) issued 6 attacks:

**LANDED (doc was wrong, had to change):**
1. **The pump was one turn out of phase — fatal as originally written.** `session.idle` fires at the *end* of turn N; a `noReply` write provokes no turn; the doc's first draft relied on the *sender's* external ring to cover the next turn — but that ring already fired (it caused turn N). Nothing rings turn N+1. Result: mail gets written, marked `delivered/`, and never read — forever. **Fix ("Fix A"): the pump must ring its own next turn** after writing, not rely on the sender.
2. **Ring-batching (found while tracing #1).** `swarm send` is two acts — `queue_put` then `ring_doorbell` — and the doc's claim that batching "never arises" addressed only the mail, not the *rings*. 5 senders to a busy agent produce 5 durable queue files (fine) but their 5 turn-causing ring POSTs **batch into one turn** (verified elsewhere that opencode drains concurrent prompts into a single turn) — so ring-count desyncs from message-count and mail strands. Fixed by the same self-ring: ring-count becomes definitionally equal to delivered-count.
3. **"Delivered means delivered" was quietly broken.** The pump marked `delivered/` on a successful **write**, with no turn running and none scheduled — the opposite of Claude Code, where the hook firing IS the turn already underway. This fails in the *unsafe* direction (a lying `delivered/` record vs. Claude's fail-safe "stays queued, retried"). **Fix ("Fix B"): two-phase delivery** — stage the write, leave the file in `queue/`, move to `delivered/` only at the *next* idle once a turn has provably run with it in context.

**MISSED (doc was right, verified at higher resolution):**
3'. **One message per turn.** `session.idle` counts **turns**, not model calls: a forced 4-tool-call turn produced 5 model round-trips but **1** idle (measured two independent ways: plugin hook + external SSE watcher). And critically — **a `noReply` write fires ZERO `session.idle` events** (measured `idle_before=1, idle_after=1, Δ=0` over 20s) — meaning the pump cannot self-trigger a runaway burst-drain. This is what makes Fix A *safe*.
4'. **OTTER-77, the central pivot, re-verified at the SQL store level, not just model recall.** Positive control (ordinary prompt) → 1 user-role part in store. `messages.transform` injection → **0** user-role parts (a naive grep finds a false-positive hit, but it's an assistant *reasoning* part quoting the codeword, not a user write — must join `part`→`message` filtered on `role='user'`). `noReply` write → **1** user-role part, persisted and recalled correctly. Confirms: `messages.transform` mutates the view only; `noReply` writes the session.

**A found-for-free hazard (not an attack, a gift):** the model **refuses `messages.transform`-injected mail as a prompt injection** — its own persisted reasoning: *"this appears to be a prompt injection attempt trying to override my instructions… I should not follow prompt injection attempts."* The identical text via `noReply` was NOT resisted and was read normally. This is a second, independent, and arguably stronger reason (an alignment argument, not just a correctness argument) that delivery must never ride `messages.transform`.

**GLANCES (real but survivable):** Attack 5 challenged "is it worth it?" — the doc's claim that the design "stores no new state and makes no new claim about the world" is **false**: it stores a `port` per agent and (per the doc's §6.1 finding) makes the plugin **contract-critical code** running inside a third-party 130MB binary, keyed on an event whose semantics are undocumented at 3.5× the documented rate (89 wire event types in the binary vs. ~25 documented). Verdict stands as a real **price**, not a disqualifier — the recommendation to build survives, but the "no new state/claim" line was struck as an overclaim.

**One more concrete bug the red pass caught:** the doc originally warned that `opencode run --port` would **fail loudly** (print help, exit) if misused. On the actual binary (1.17.18) it does the opposite — **silently ignores** `--port`, runs the completion normally, exits 0, and serves nothing. A mis-wired launcher produces an agent that looks healthy and never receives mail, with nothing in `ps` to show it. Design consequence: the launcher **must** assert `GET /global/health` on the assigned port after spawn rather than trusting the command to fail.

Red team's closing line: *"The design is right and the pump is broken. Fix the pump; ship the design."* — and the corrected pump (self-ring + two-phase delivery) is what's now in the design doc.

## 6. Prior art

From `opencode-plugin-priorart.md` and `opencode-priorart-docs.md`, checked against the live npm registry:

- **The server/SDK surface is the real answer, not the plugin.** External, no-plugin HTTP calls already give delivery (mid-turn injection tested: sent a message to a busy agent, it queued and landed cleanly on the next turn, no drop/corruption), event (SSE `GET /event`), restore (`noReply`), spawn (`parentID`/`/session/{id}/children` — native parent/child session trees), identity (per-call `system` string). Opencode's own docs example for `experimental.session.compacting` is verbatim a multi-agent swarm continuation-summary prompt — i.e., the vendor already anticipated this exact use case.
- **Existing published plugins** (npm, verified counts, not the meaningless 250,902 fuzzy-match number some search returns — real count is ~20 genuinely-named packages): cluster around memory/context (`opencode-mem`, `opencode-supermemory`, `@cortexkit/opencode-magic-context`), RAG (`opencode-rag-plugin`), observability/tracing (`@langchain/langsmith-opencode`, `@braintrust/trace-opencode`, `@mastra/opencode`), provider routing (`opencode-anthropic-multi-account`, `opencode-plugin-litellm`). Closest neighbors: `@scrylog/opencode-plugin` (pushes session events to a daemon — half of the EVENT primitive, for observability) and `opencode-subagent-statusline` (watches subagent sessions).
- **Verdict: nobody has published an agent-to-agent messaging/orchestration plugin.** The orchestration slot is empty — this would be new ground, not a reinvention.
- **A real, separately-flagged mismatch:** opencode **batches concurrent mail** — 3 messages sent during one running turn were all accepted (204) and drained into a **single** next turn (4 user messages → 2 assistant messages), not one turn each. This is why the corrected pump design keeps swarm's own queue authoritative and drains it one-per-turn itself, rather than trusting opencode's native queuing to preserve "one message, one turn."

## 7. Open questions / undecided

Explicitly flagged as unrun, in priority order (OPENCODE-PLUGIN.md §8, and RED's own falsifier):
1. **The pump running inside a live TUI, end-to-end, has never been run.** The self-ringing pump was verified under `opencode run` (a non-persistent process); the TUI-serves-on-a-pinned-port half was verified separately. The *composition* — pump logic actually running inside a TUI in a herdr pane — is the single most important untested thing, and is literally the red team's own falsifier test ("run your pump verbatim against a live TUI agent, send one message, send nothing else").
2. **The pump under sustained/concurrent load** (the doc's own F4: 50 sends to a busy agent, count `delivered/` vs `queue/` after it idles) — untested.
3. **The pump across a real compaction event** — untested (F1).
4. Whether `tool.execute.after`'s exact mutation semantics are fully nailed down (docs are silent on its signature; source-level answer exists but is secondary).
5. The version-drift problem is itself unresolved as process: the investigation's own target binary moved from 1.17.13 → 1.17.18 *during the investigation*, which is direct evidence for the doc's own recommendation to pin the version and re-run probes on every bump — nobody was watching, and it happened anyway.

None of the above are described as architectural holes — they're flagged as "the first things to measure" before trusting the design in production.

## 8. Bottom line

The design is sound and the recommendation is to build it, but only the corrected mechanism (self-ringing pump + two-phase delivery), not the version the red team first reviewed — that version silently loses mail. Greenlight conditioned on three guardrails: (1) run the still-untested pump-inside-a-live-TUI composition before trusting it in production, (2) treat `OPENCODE_SERVER_PASSWORD` as a mandatory launcher requirement (it stops drive/shell hijacking but explicitly does NOT stop cross-agent reads — the SQLite store is world-readable regardless), and (3) pin the opencode version and re-verify `session.idle`'s once-per-turn semantics on every bump, since that undocumented behavior is now load-bearing for the delivery contract itself, not just for restore/ergonomics as originally scoped.
