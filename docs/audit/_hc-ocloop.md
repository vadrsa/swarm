# hc-ocloop — what can be CONTROLLED in opencode's agent loop, at three depths

**Agent:** `hc-ocloop` (parent: `harness-contractor`), with one child, `hc-ocloop-fork`
(fork-depth external research: license, upstream velocity, provider layer,
loop-stages-invisible-to-plugins). Evidence only — the ruling is the parent's.

**Method.** Depths 1-2 are a re-read and re-organization of this repo's existing
opencode prior art, cited file:line/section throughout — no new probes were run,
because the prior art already measured everything askable at those two depths
(see §0 for the inventory). Depth 3 (fork) required fresh external research,
delegated to `hc-ocloop-fork`, whose findings are folded in under §4-§6 and
tagged DOCUMENTED/KNOWLEDGE by that child.

Every claim below carries its origin tag, inherited from the source docs:
**VERIFIED** (someone ran it, against the binary or a live server), **DOCUMENTED**
(official docs, not independently exercised), **REASONED** (inference, named as
such). Depth-3 material additionally uses **KNOWLEDGE** (asserted from training
data, not freshly checked) per this task's instruction.

---

## 0. What prior art already measured (the inventory this doc builds on)

Read in full, this session: `docs/design/OPENCODE-PLUGIN.md` (949 ln),
`docs/design/OPENCODE-PLUGIN-RED.md` (736 ln), `docs/audit/opencode-plugin-api.md`,
`docs/audit/opencode-plugin-probe.md`, `docs/audit/opencode-plugin-priorart.md`,
`docs/audit/opencode-priorart-docs.md`, `docs/audit/oc-red-relab.md`,
`docs/audit/oc-report-digest.md`. Target across all of them: opencode
**v1.17.13 → v1.17.18** (the binary drifted *during* the original investigation;
`ocr-lab`'s hostile re-run redid all four load-bearing experiments on 1.17.18 and
they survive).

### Confirmed against the brief's three named facts

| Claimed fact | Status | Citation |
|---|---|---|
| `tool.execute.before` can rewrite args and throwing blocks the call | **VERIFIED**, exactly as stated | `opencode-plugin-api.md` §2 ("Blocking is by exception, not by return value — VERIFIED... a hook that throws short-circuits... surfaces as ToolStateError on that one tool call. The session is not killed."); table row `tool.execute.before`, `opencode-plugin-api.md` §3 |
| `session.idle` counts turns | **VERIFIED**, and re-verified hostilely | `oc-red-relab.md` E3-A: 4 bash tool calls + 5 model round-trips → **1** `session.idle`, measured two independent ways (plugin hook + external SSE) |
| A `noReply` write fires zero idles | **VERIFIED**, and this is the load-bearing safety fact for any pump/driver design | `oc-red-relab.md` E3-B: `idle_before=1, idle_after=1, DELTA=0` over a 20s window after a `noReply` POST that itself returned HTTP 200 in 9ms and produced a real session write |

### Everything else measured (full list, so nothing is silently omitted)

**v1 `Hooks` (the documented plugin surface), one row per dispatched hook —** all
14 are enumerated with mutation semantics in `opencode-plugin-api.md` §3: `event`,
`config`, `dispose`, `tool` (map), `auth`, `provider`, `chat.message`,
`chat.params`, `chat.headers`, `permission.ask` (dead — see below),
`command.execute.before`, `tool.execute.before`, `tool.execute.after`,
`shell.env`, `experimental.chat.messages.transform`,
`experimental.chat.system.transform`, `tool.definition`,
`experimental.provider.small_model`, `experimental.session.compacting`,
`experimental.compaction.autocontinue`, `experimental.text.complete`. A sweep of
every `.trigger("...")` call site in the binary found exactly these — **VERIFIED
(negative)**, no hidden hooks (`opencode-plugin-api.md` §3, "Undeclared hooks:
none").

**v2 `PluginContext` (undocumented, but wired)** — `aisdk.language` (replace the
`LanguageModelV3` object, intercept every LLM call — **VERIFIED end-to-end**),
`aisdk.sdk`, `agent.transform` (rewrite any agent's system prompt / model /
permission ruleset / step budget), `catalog.transform`, `command.transform`,
`skill.transform`, `reference.transform`, `integration.transform` /
`integration.connection`, `plugin.add`/`plugin.remove` — all VERIFIED as types,
`aisdk.language` and `aisdk.sdk` additionally VERIFIED as live/wired (opencode's
own providers are built on them). `opencode-plugin-api.md` §3.

**Four traps, all VERIFIED** (`opencode-plugin-api.md` §2.3, cross-cited in
`OPENCODE-PLUGIN.md` §2.3):
1. `permission.ask` is **dead code** — declared in the `.d.ts`, never dispatched,
   the bare string does not occur in the 130MB binary (every hit is the unrelated
   `permission.asked` event). Re-confirmed independently by `ocr-lab`.
2. In-place mutation only for roughly half the hooks (outer-variable pattern);
   `output.args = {...}` is silently dropped in those — must
   `Object.assign(output.args, ...)`. No type/doc/runtime signal distinguishes
   which half.
3. Per-turn hooks are **not** sandboxed — `Plugin.trigger` has no try/catch, so an
   accidental throw in, e.g., `chat.params` breaks the turn. Only `config` and
   `dispose` are caught-and-ignored. The `event` hook is the one true
   fire-and-forget dispatch (`for (M of K) M.event?.(...)` inside `bus.listen`,
   nothing awaits it) — the only hook where a throw cannot break a turn, but
   also where a throw is **silently swallowed** (queue just stops draining, no
   visible error).
4. Never `await` a call back into the host server from inside a hook — measured
   self-deadlock (5-minute timeout, `session.idle` never even fired) when a pump
   plugin awaited `client.session.prompt(...)` from inside the `event` hook.
   Fire-and-forget (`.then()/.catch()`) works.

**Server/HTTP surface (a heavier, non-plugin config-level control point) —**
`opencode-plugin-priorart.md` VERIFIED that 5 of swarm's 6 primitives are
servable with **zero plugin code**, purely over HTTP: delivery
(`POST /session/{id}/prompt_async`, including mid-turn — queues, does not drop
or corrupt the running turn), event (`GET /event` SSE, same `session.idle`),
restore (`noReply:true` silent context push), spawn (`POST /session` with
`parentID`, native parent/child session trees), identity (per-call `system`
string). Also VERIFIED: mail sent to a *busy* session **batches** — 3 concurrent
sends drained into **1** next turn (4 user messages → 2 assistant messages),
which breaks "a message is a claim on one turn" unless swarm's own queue stays
authoritative and drains it one-per-turn (`opencode-plugin-priorart.md` §6.4).

**Security facts, both VERIFIED and independently re-run:** the server is
**unauthenticated by default** (own warning:
`OPENCODE_SERVER_PASSWORD is not set; server is unsecured` — any local process
can prompt/read/`POST /session/{id}/shell` any agent); sessions are **not**
scoped by directory (a per-agent `--dir` does not isolate `GET /session` — 92-93
sessions returned from other directories on two independent runs); the session
store is a **world-readable SQLite file**
(`~/.local/share/opencode/opencode.db`, mode `-rw-r--r--`) queryable with no
server/port/password at all (`opencode db "SELECT..."` dumped 1,279 messages
straight off disk in one run). A per-agent `OPENCODE_SERVER_PASSWORD` closes the
drive/shell path only; it does not and cannot close the read path.

**The red-team's landed corrections (now folded into the design, not into what a
plugin/server *can* do, but into how you must sequence it):** the delivery
mechanism must self-ring (the recipient's own next turn, not the sender's, must
be what reads injected mail — `OPENCODE-PLUGIN-RED.md` Attack 1); ring-batching
means "delivered ⇒ read" requires the pump's ring-count to equal its
delivered-count, achieved only by the self-ring (Attack 1b); `delivered/` must
be two-phase — staged at write, moved only at the *next* idle once a turn
provably ran with it in context (Attack 2). These are sequencing/contract facts
about how a plugin+server combination must be *used*, not new capability facts,
and they do not change any YES/NO/PARTIAL verdict below — they change how the
YES is implemented.

**The version-drift fact:** the binary itself moved (1.17.13 → 1.17.18) *during*
this repo's own investigation of it — direct, self-demonstrating evidence for
§6's "pin the version" concern, independent of anything hc-ocloop-fork reports
on release cadence.

---

## 1. Per-duty enforcement table — PLUGIN surface (depths 1 + 2)

Reading: **YES** = the plugin surface can make the turn structurally incapable
of completing without the duty being satisfied (an enforced gate, not a request
the agent could ignore). **PARTIAL** = some real structural leverage exists but
it is either bypassable, degrades to observe-only, or requires accepting the
"heavier config/agent-level" depth (v2 `PluginContext`, `agent.transform`, or the
HTTP server) rather than a pure v1 hook. **NO** = nothing in the surface can
enforce it; at most it can be requested/observed.

| # | Swarm duty | Verdict | Hook + measured semantics |
|---|---|---|---|
| 1 | **Report-to-parent** | **NO** | No hook fires on "assistant produced its final text" in a way that can block completion pending a report. `experimental.text.complete` (`opencode-plugin-api.md` §3) can **rewrite** the assistant's own output text before it's persisted/streamed — so a plugin could, e.g., append "report sent: true/false" cosmetically, or even append the report text itself — but it cannot verify a `swarm send` actually happened, cannot re-open a completed turn, and cannot force another turn from inside that hook (turn-end is observe-only, §2.4 of `OPENCODE-PLUGIN.md`: "an opencode plugin cannot re-ring itself from inside the hook"). A plugin can *notice* the turn ended without a report (via `event`→`session.idle`) and *cause* a follow-up turn nagging for one (self-ring, exactly the pump mechanism) — but the original turn already completed uncontrolled. That is detection-and-followup, not turn-gating. |
| 2 | **Journal/checkpoint write** | **PARTIAL** | Same shape as #1: nothing gates *this* turn's completion on a journal write happening first. But `tool.execute.before` (**VERIFIED** block primitive: throwing prevents the tool from running, `ToolStateError`, session survives — `opencode-plugin-api.md` §2) could in principle refuse to let certain tools (e.g. a `swarm` CLI invocation, or a designated "turn complete" signal) execute unless a journal-write marker was set earlier in the same turn — this is buildable but is a policy *you* construct on top of the hook, not something the hook gives you natively. `experimental.session.compacting` (**DOCUMENTED+VERIFIED**, `OPENCODE-PLUGIN.md` §3.4) is the one place a plugin can force journal-equivalent content (task+journal tail) into context **by construction** rather than by request — but only at compaction, not every turn. |
| 3 | **Reconcile prompt** | **NO** | No hook can inject a "have you reconciled?" gate that blocks turn completion. The nearest lever is `experimental.chat.system.transform` (**VERIFIED**, `PELICAN-9` result) which can put "you must reconcile every N turns" into the system prompt every turn — a standing instruction, not an enforced gate. The model can ignore it; nothing in the API structurally prevents the turn from ending without compliance. |
| 4 | **Time-box/watchdog** | **PARTIAL** | A plugin cannot set a hard wall-clock kill from *inside* the v1 Hooks surface — there's no "abort this turn after N seconds" hook. But the **server** (heavier depth-2 surface, no plugin needed) exposes `POST /session/{id}/abort` (**DOCUMENTED**, `opencode-priorart-docs.md` §4) — an *external* watcher (the swarm CLI itself, or a plugin's own `event`-driven timer using `client.session.abort`) can enforce a wall-clock cap by calling this from outside the turn. That is real enforcement — the turn is structurally terminated — but it is server-level control exercised by an external process, not something a v1 hook enforces from within the loop itself. |
| 5 | **Done-signal** | **PARTIAL** | `experimental.compaction.autocontinue` (**VERIFIED**, `opencode-plugin-api.md` §3) can return `{enabled:false}` to **suppress** the synthetic continue-turn after compaction — a real, structural block on continuation. But that's the *opposite* control: it can prevent a turn from happening, not require one. There's no hook that says "you may not stop until you emit X" — the closest analog to Claude's `Stop` hook returning `{"decision":"block"}` to force continuation does not exist for opencode (`OPENCODE-PLUGIN.md` §2.4: "Unlike Claude Code's `Stop` hook, which can return `{"decision":"block"}` and *force* a continuation turn, an opencode plugin cannot re-ring itself from inside the hook"). A plugin CAN cause another turn from *outside* the hook (fire-and-forget `client.session.prompt` after the `event` hook returns — this is the pump mechanism) which functionally re-opens the loop until a done-signal appears, but it is a driver bolted alongside the loop, not the loop enforcing it on itself. |
| 6 | **Spawn-with-model-and-reason** | **PARTIAL/YES for the *model* half** | `agent.transform` (v2, **VERIFIED** wired, `opencode-plugin-api.md` §3: `AgentDraft.update(id, fn)` over `AgentV2Info{model, request, permissions, steps,...}`) lets a plugin rewrite **any agent's model** and step budget at the catalog level — this is a structural, enforced gate: an agent literally cannot be instantiated with a model the plugin's `agent.transform` didn't allow, because the catalog is rewritten before any session uses it. But it operates on the **agent-definition catalog**, not on a specific spawn call's stated "reason" — there is no hook that inspects a spawn request's rationale and blocks the spawn if unreasoned. `tool.execute.before` on a custom `swarm_spawn` tool (**VERIFIED buildable**, `opencode-plugin-probe.md` PROBE 5: a custom tool registered and callable) could require a `reason` arg and throw if absent — same "policy you construct on the block primitive" shape as #2. So: model choice is enforceable at the catalog level (YES); reason-attachment is enforceable only if you build a custom spawn tool with a required arg and gate it via `tool.execute.before` (PARTIAL, buildable not native). |
| 7 | **Context restore after crash/compaction** | **YES** (the one duty with the strongest native seat) | `experimental.session.compacting` (**DOCUMENTED**, `opencode-priorart-docs.md` §1, and **VERIFIED**, `OPENCODE-PLUGIN.md` §3.4): `output.prompt` **replaces the compaction prompt entirely**, or `output.context.push(...)` appends to it — this is structural: the compaction call cannot proceed without running through this hook, and setting `output.prompt` wholesale means the plugin's task+journal content is definitionally what survives, not a request layered on top of a default. Opencode's own shipped docs example for this exact hook is verbatim a multi-agent swarm continuation prompt (`opencode-priorart-docs.md` §1: *"You are generating a continuation prompt for a multi-agent swarm session..."*) — the vendor built this hook for precisely this duty. Caveat: there is **no session-start/resume hook** (`opencode-plugin-api.md` §4: "`config` fires once at *process* load, not per session") — so *crash*-restart restore (a fresh process, not a compaction) has no first-class plugin seat; it falls back to the launch prompt (`--prompt`) or an external watcher pushing a `noReply` restore payload after detecting `session.compacted`/process-restart on the bus (`OPENCODE-PLUGIN.md` §3.4, "Belt-and-braces"). So: compaction-restore is YES; crash-restore is PARTIAL (external/launch-prompt fallback, not hook-enforced). |

### The pattern across all seven rows

No v1 hook can gate on **"the turn is ending"** — because turn-end
(`session.idle`, via `event`) is observe-only and fire-and-forget: no `output`
argument exists to say "not yet" (`opencode-plugin-api.md` §4: "Turn-end is
observe-only... no way to say 'keep going'"). Every duty that is naturally
"before you're allowed to stop, do X" (report, reconcile, done-signal) therefore
lands at NO or PARTIAL, because opencode's plugin API has no analog to Claude
Code's `Stop` hook returning `{"decision":"block"}`. The duties that land at
YES/PARTIAL-strong (spawn's model half, compaction-restore) do so because they
sit on hooks that fire **before an operation the loop cannot skip**
(catalog resolution before instantiation; the compaction call itself) rather
than at the ambiguous "turn is over" boundary.

The **heavier, config/agent-level surface** (depth 2) adds real leverage in
exactly two places: `agent.transform`'s catalog-level rewrite (duty 6, model
half) and the server's `POST /session/{id}/abort` for external time-boxing
(duty 4) — both genuinely structural, neither available from a pure v1 Hooks
plugin. Depth 2 does **not** add a done-signal or reconcile-prompt gate; those
remain NO/PARTIAL even with the full server + v2 surface, because the missing
primitive (a loop stage that can refuse to end the turn) does not exist at any
documented depth.

---

## 2. Depth 3 — what a FORK adds beyond the plugin surface

Full detail: `docs/audit/_hc-ocloop-fork.md` (`hc-ocloop-fork`). Method there:
`gh api` against the live repo (source-tree reads, release/commit history) plus
one `curl` against the public `models.dev` API. Tags preserved from that doc.

### 2.1 Repo identity & license

- **Repo:** `github.com/anomalyco/opencode` — `sst/opencode` 301-redirects here;
  same repo ID (`975734319`), an org rename, not a fork-of-a-fork.
  **DOCUMENTED.** Created 2025-04-30, default branch `dev`, not itself a fork
  (`"fork":false`). 185,378 stargazers, 23,163 forks, 4,678 open issues.
- **License: MIT**, standard text, no added restriction clauses; OSI-approved,
  permits forking/modifying/relicensing/commercial use, sole condition is
  preserving the copyright notice. **DOCUMENTED** (LICENSE file read directly).
- **No CLA workflow found** in `.github/` and no CLA mention in
  `CONTRIBUTING.md`. **DOCUMENTED** as absence-of-evidence, explicitly not
  proof of absence (a CLA could be enforced out-of-band, e.g. a first-PR bot
  comment, which was not checked against a live PR).
- **No trademark/naming-policy file** (`TRADEMARK.md`, `BRAND.md`, etc.) found
  in-repo, and zero README hits for "trademark"/"rename"/"formerly"/"SST."
  **DOCUMENTED** that no such file exists; does **not** mean no trademark claim
  exists on the name "opencode" under general trademark law — MIT covers
  copyright/code, not trademarks, a standard legal distinction the child flags
  as **KNOWLEDGE** since no opencode-specific statement exists to verify it
  against.
- **No dual-licensing wrinkle found** at the root; ~28 subpackages under
  `packages/` were **not** individually checked for a package-local override —
  stated as a gap, not a finding either way.

**Bottom line: legally forkable** on the evidence gathered — MIT, no found CLA
gate, no found trademark restriction on use of the code (name-reuse is a
separate, unverified question).

### 2.2 Upstream velocity

- **Release cadence:** 19 releases on the 1.17.x line alone across 29 days
  (2026-06-10 → 2026-07-09) — roughly **one release every 1.5 days**, some days
  shipping 3 releases. **DOCUMENTED**, `gh api .../releases`. This sharpens
  (does not merely corroborate) the plugin investigation's own observation that
  its target binary drifted from 1.17.13 to 1.17.18 *during* that
  investigation (2026-07-01 → 2026-07-09, 5 patch releases in 8 days) — the
  drift was not a fluke, it is the steady-state cadence.
- **Tag volume:** 1,065 total tags — consistent with sub-2-day cadence
  sustained over a long period. **DOCUMENTED.**
- **Commit velocity:** 41–381 commits/week over recently-visible weeks
  (roughly 6–55/day), variable but never near zero; earlier-window weeks ran
  ~85–212/week — velocity sustained or increasing, not tapering.
  **DOCUMENTED** (`gh api .../stats/commit_activity`).
- **Contributor concentration:** 455 unique contributor logins, but the top
  commit counts are dominated by ~8 individuals who are *all* listed in
  `.github/TEAM_MEMBERS` (a 20-name roster) and several explicitly show
  company affiliation `@anomalyco`/`Anomaly` on their GitHub profiles.
  **DOCUMENTED.** Two bot accounts (`opencode-agent[bot]`, `actions-user`) are
  themselves in the top 6 by commit count, meaning a non-trivial share of raw
  commit volume is automated (CI-driven version bumps), inflating the raw
  commit/week figure relative to human-authored feature work.
- **Core-loop-specific churn:** **not measured** — the child did not diff
  `git log` scoped to `session/*` paths. What is established: the session-loop
  files ship inside the same single versioned package
  (`packages/opencode`) on the same repo-wide ~1.5-day cadence; there is no
  evidence of a slower-moving "stable core" split from a faster "plugin
  surface." The inference that core-loop churn matches overall package churn
  is flagged **KNOWLEDGE**, not confirmed per-file.

**Bottom line: a fast-moving upstream.** A fork tracking this repo is pricing
in near-daily release activity and double-digit-to-hundreds of weekly commits,
concentrated in a small company-affiliated core team — not a slow, stable
dependency.

### 2.3 Loop stages a fork reaches that no hook (v1 or v2) reaches

Source tree confirmed directly (not the binary, not docs):
`packages/opencode/src/session/` is the loop. Files read/characterized
(**DOCUMENTED** — existence, size, imports; full control-flow not traced for
the two largest):

| File | Size | What it is | Plugin-reachable? |
|---|---|---|---|
| `session/llm.ts` | 404 ln | The direct call site of `streamText` (Vercel `ai` SDK) — assembles `model, agent, permission, system, messages, tools, toolChoice, retries` and wires `ProviderTransform`/`Plugin`/`Permission`/`EventV2Bridge` in one place. | **No** — hooks see already-assembled inputs/outputs at coarser boundaries; this exact request-assembly-plus-streaming union is invisible to any hook. |
| `session/processor.ts` | 720 ln (largest in dir) | The plausible tool-call-loop driver — turn-by-turn orchestration (call model → get tool calls → execute → append → repeat). Imports `Session, LLM, MessageV2, isOverflow, Agent, Config, Permission, Plugin, Snapshot, Image`. | **No** — existence/centrality DOCUMENTED, full internal control flow not traced (a gap the child names explicitly). |
| `session/compaction.ts` | 566 ln | Context-compaction/summarization logic. Imports `Session, Provider, MessageV2, Token, SessionProcessor, Agent, Plugin, Config`. | **Partially** via `experimental.session.compacting` (§1 duty 7) — but that hook only shapes the *prompt*, not the compaction *policy/algorithm* implemented here. |
| `session/overflow.ts` | 34 ln | Token-budget policy: `usable({cfg, model, outputTokenMax})` subtracts a 20,000-token `COMPACTION_BUFFER` plus a configurable reserve from `model.limit.context` — decides **when** compaction fires. | **No** — pure internal policy function, no hook touches it. |
| `session/retry.ts` | 201 ln | Retry-reason taxonomy including `free_tier_limit`/`account_rate_limit`, plus a `GO_UPSELL_MESSAGE`/URL pointing at `opencode.ai/go` — a commercial upsell path embedded in error-handling logic. | **No** — source-level only, not plugin-visible. |
| `session/llm/` subdir | `ai-sdk.ts`, `native-request.ts`, `native-runtime.ts`, `request.ts` | Two parallel code paths for issuing model requests: an AI-SDK-mediated path (where `aisdk.language` hooks in) and a separate **"native" path**. | The native path's existence alongside the AI-SDK path is itself invisible from the plugin surface — a hook that only knows `aisdk.language` cannot tell if it's on the AI-SDK path or being bypassed by the native one. |

**The pattern:** a fork buys touch access to request-assembly-and-tool-loop
orchestration (`llm.ts` + `processor.ts` combined — no hook sees these as one
unit), the compaction *algorithm* (not just its prompt), the token-budget
policy that decides *when* to compact, retry/upsell logic, and the
choice-of-code-path between AI-SDK-mediated and native model invocation. None
of this is reachable via v1 Hooks or the undocumented v2 `PluginContext`
(including `aisdk.language`) per the sibling plugin-surface investigation — a
plugin consumes what these stages hand it; a fork can rewrite the stages
themselves.

### 2.4 The provider layer — what a fork inherits for free

Three layers, confirmed from source, quantified for weighing (not as a
recommendation):

1. **Hand-written wire adapters** — `packages/llm/src/providers/`: **11 named
   vendor adapters** (Amazon Bedrock, Anthropic, Azure, Cloudflare, GitHub
   Copilot, Google, OpenAI, OpenRouter, xAI, plus two OpenAI-compatible
   variants) **+ 1 generic OpenAI-compatible adapter**. Sibling
   `packages/llm/src/protocols/`: **7 distinct wire-protocol implementations**
   (Anthropic Messages, Bedrock Converse, Bedrock EventStream, Gemini, OpenAI
   Chat, OpenAI Responses, OpenAI-compatible-chat) — hand-rolled per-vendor
   request/response translation, not a blanket dependency on `@ai-sdk`
   provider packages; Bedrock's AWS SigV4/eventstream handling is
   self-implemented (`@smithy/eventstream-codec`, `aws4fetch`) rather than
   pulled from the full AWS SDK.
2. **A live external model registry** — `models.dev`
   (`anomalyco/models.dev`, a separate maintained OSS repo, 5,872 stars),
   fetched at runtime for model/pricing/context-limit metadata. **166
   providers** registered as of this check (live `curl` against
   `models.dev/api.json`). `CONTRIBUTING.md` states new-provider PRs should go
   to the `models.dev` repo, not require opencode code changes — confirming
   the registry/protocol split is intentional and maintainer-documented. This
   is metadata (what exists, pricing, context limits), not wire
   implementations — a models.dev entry still needs one of the 7 protocols (or
   the generic OpenAI-compatible path) to actually be callable.
3. **Bundled provider-integration "plugins"** —
   `packages/opencode/src/plugin/`: dedicated code for Azure, Cloudflare,
   DigitalOcean, GitHub Copilot (own subdir), OpenAI Codex (own subdir),
   Snowflake Cortex, xAI. OAuth-flow code is spread across **at least 9
   distinct files** (`mcp/oauth-callback.ts`, `mcp/oauth-provider.ts`,
   `provider/auth.ts`, `plugin/digitalocean.ts`, `plugin/openai/codex.ts`,
   `plugin/github-copilot/copilot.ts`, `plugin/xai.ts`, `account/account.ts`,
   `core/src/oauth/page.ts`), not one central shim. `provider/auth.ts` (229
   lines, read in full) defines a **declarative, provider-agnostic auth-flow
   schema** (`Method{oauth|api}`, conditional `Prompt`s, `Authorization{url,
   method: auto|code}`) — substantial, reusable scaffolding, not one-off glue.

**Quantified summary, for weighing against fork-maintenance cost:** a fork
inherits, without rebuilding, 11+1 hand-written wire adapters, 7 wire-protocol
implementations, a live-fetched 166-provider metadata catalog maintained by a
separate project under the same org, 9+ files of OAuth/auth plumbing across at
least 7 named vendor integrations, and a self-implemented AWS SigV4/eventstream
layer for Bedrock. None of this is reachable or reconstructable via the plugin
API alone — the plugin surface consumes already-resolved providers/models, it
does not let a plugin add a new wire protocol or OAuth flow from outside the
source tree (this last clause is the child's own inference from the shape of
the plugin surface, flagged **KNOWLEDGE**, not re-derived against
`opencode-plugin-api.md`'s exact wording in that pass).

### 2.5 Gaps in the depth-3 research (named by the child, preserved here)

- Core-loop-vs-rest churn rate not measured per-file (§2.2).
- `session/processor.ts` (720 ln) and `session/compaction.ts` (566 ln) not
  read line-by-line — existence/imports confirmed, full control flow not
  traced.
- Whether any of the ~28 subpackages under `packages/` carries a license
  different from the root MIT file — not checked.
- CLA absence checked only via committed-workflow-file search, not against
  live PR behavior (an out-of-band CLA bot would not show up this way).

---

## 3. Falsifiers

| # | If observed, this document is wrong | How to collect |
|---|---|---|
| F1 | A v1 hook exists that DOES gate turn-completion (return value honored to block/delay `session.idle`) | Re-grep the binary's `Plugin.trigger` call sites for any `event`-hook variant that reads a return value; none found in `opencode-plugin-api.md`'s exhaustive sweep, but re-verify on whatever version is current at read-time |
| F2 | `agent.transform`'s catalog rewrite is bypassable per-session (e.g. a session pins a model before the transform runs) | Instantiate a session immediately after changing `agent.transform`'s model output; check which model actually served the turn |
| F3 | opencode ships (in a version newer than 1.17.18) a documented session-start/resume hook, closing the crash-restore gap in duty 7 | Re-pull `GET /doc` and the plugins page on any version bump; diff hook list against `opencode-plugin-api.md` §3's 14-hook enumeration |
| F4 | Core-loop files (`session/*`) churn slower than the repo-wide ~1.5-day release cadence (i.e. a fork could track a stable subset while ignoring fast-moving plugin/provider churn) | `git log --follow` (or the GraphQL commit-history-by-path API) scoped to `packages/opencode/src/session/*` specifically, compared against repo-wide commit frequency — not done in this pass, per `hc-ocloop-fork`'s own named gap |
| F5 | A CLA is enforced out-of-band (e.g. a bot comment on first PR) despite no committed CLA workflow file | Open a real first-time PR against `anomalyco/opencode` and observe whether any bot/maintainer response demands CLA agreement |
