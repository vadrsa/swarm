# opencode as a fork target — what forking buys beyond the plugin API

Scope: this document does NOT re-measure the plugin surface (v1 Hooks / v2
PluginContext) — that is exhaustively covered by `docs/audit/opencode-plugin-api.md`,
`docs/audit/opencode-plugin-probe.md`, `docs/design/OPENCODE-PLUGIN.md`,
`docs/design/OPENCODE-PLUGIN-RED.md`. This document answers only: what does a
full source fork add on top of that plugin surface. Evidence only, no
recommendation.

Method: `gh api` against the live GitHub repo (README describes it, `gh auth
status` confirmed authenticated), plus one `curl` against the public
models.dev API. Every fact below is tagged **DOCUMENTED** (I ran the command/
read the file, output shown or summarized faithfully) or **KNOWLEDGE**
(asserted without a fresh check — flagged explicitly, none used for load-
bearing claims below).

---

## 1. Repo identity & license

**The name has changed underneath the URL you'd guess.** `github.com/sst/opencode`
returns an HTTP 301 redirect to `github.com/anomalyco/opencode` — this is a
GitHub org rename/transfer, not a fork-of-a-fork or an unrelated project.
**DOCUMENTED**:
```
$ curl -sI https://github.com/sst/opencode | head -5
HTTP/2 301
location: https://github.com/anomalyco/opencode
```
`gh api repos/sst/opencode` resolves to `"full_name":"anomalyco/opencode"` —
same repo ID (`975734319`), same content, just renamed. **DOCUMENTED**.

**Repo facts** (`gh api repos/anomalyco/opencode`), **DOCUMENTED**:
- Full name: `anomalyco/opencode`, created 2025-04-30, default branch `dev`.
- Description: "The open source coding agent." Homepage `https://opencode.ai`.
- Not a fork itself (`"fork":false`, `"parent":null`).
- 185,378 stargazers, 23,163 forks, 4,678 open issues, 711 subscribers.
- Language: TypeScript. Size: 383,461 KB (repo blob size, not LOC).

**License: MIT.** `gh api repos/anomalyco/opencode/contents/LICENSE` (base64-
decoded), **DOCUMENTED**:
```
MIT License
Copyright (c) 2025 opencode
Permission is hereby granted, free of charge, to any person obtaining a copy...
```
Standard MIT, no additional restriction clauses in the LICENSE file text
itself. `gh repo view` also reports `licenseInfo: {key: "mit", name: "MIT
License"}`. MIT is OSI-approved and permits forking, modifying, relicensing
derivative works, and commercial use, with the sole condition of preserving
the copyright/permission notice. **DOCUMENTED**.

**No CLA bot / CLA requirement found.** Checked `.github/` contents for a CLA
workflow — none present (`CODEOWNERS`, `ISSUE_TEMPLATE`, `TEAM_MEMBERS`,
`actions`, `publish-python-sdk.yml`, `pull_request_template.md`, `workflows`
— no `cla.yml` or similar). A repo-wide code search for "CLA" inside the repo
turned up no CLA-process files (hits were unrelated: doc mentions of "Claude",
a glossary entry, etc.). `CONTRIBUTING.md` describes contribution categories
and a design-review requirement for "any UI or core product feature" but says
nothing about a CLA or IP assignment. **DOCUMENTED** — absence of evidence,
not proof of absence; a fork's counsel should still not assume this is
exhaustive, but nothing in the repo's own contributor-facing docs asserts one.

**No trademark/naming policy file found.** No `TRADEMARK.md`, `BRAND.md`, or
naming-restriction clause anywhere in the repo root listing or README.
**DOCUMENTED** that no such file exists in-repo; this does NOT mean SST/
Anomaly has no trademark claim on "opencode" as a name under general trademark
law (MIT license covers copyright/code, not trademarks — that's a standard
legal distinction, **KNOWLEDGE**, not verified against any opencode-specific
statement because none exists to verify). The org itself quietly renamed from
(likely) `sst` to `anomalyco` with no in-repo announcement of why — the
README has zero hits for "trademark," "rename," "formerly," or "SST."
**DOCUMENTED** (grep against README.md returned empty).

**No dual-licensing wrinkle found** — single LICENSE file, MIT, applies
repo-wide as far as the root LICENSE file's scope goes. Did not check every
subpackage individually (there are ~28 packages under `packages/`) for a
package-local override; this is a gap, not a finding either way.

---

## 2. Upstream velocity

**Release cadence — sharpened, not just corroborated.** Pulled the last 100
releases via `gh api repos/anomalyco/opencode/releases`. **DOCUMENTED**:
```
v1.17.18   2026-07-09T18:51:45Z
v1.17.17   2026-07-09T15:03:12Z
v1.17.16   2026-07-09T06:36:00Z
v1.17.15   2026-07-07T15:31:38Z
v1.17.14   2026-07-06T18:50:53Z
v1.17.13   2026-07-01T15:19:06Z
v1.17.12   2026-06-30T19:48:04Z
...
v1.17.0    2026-06-10T03:12:35Z
v1.16.2    2026-06-05T15:58:51Z
v1.16.0    2026-06-05T03:08:15Z
```
This sharpens the plugin investigation's observation: v1.17.13 (2026-07-01)
to v1.17.18 (2026-07-09) is **5 patch releases over 8 days** — confirms the
binary drifted *during* that investigation, and shows the drift wasn't a
fluke: the v1.17.x line alone shipped 19 releases (1.17.0 → 1.17.18) in 29
days (2026-06-10 → 2026-07-09), i.e. roughly one release every 1.5 days.
Some days saw 3 releases (2026-07-09 shipped .16, .17, .18 the same day).

**Tag volume**: 1,065 total tags in the repo (`gh api repos/anomalyco/opencode/tags
--paginate | wc -l`). **DOCUMENTED**. This is consistent with sub-2-day
release cadence sustained over a long period, not a recent spike.

**Commit velocity**: `gh api repos/anomalyco/opencode/stats/commit_activity`
(GitHub's 52-week weekly commit histogram). **DOCUMENTED**. Sample of recent
weeks (unix week-start timestamp → commit count):
```
1779580800  255
1780185600  312
1780790400  209
1781395200   65
1782000000  381
1782604800  262
1783209600  142
1783814400   41
```
Range across the visible recent weeks: **41 to 381 commits/week**, i.e.
roughly 6–55 commits/day, highly variable week to week but never near zero.
Earlier-in-window weeks (about a year back from now) ran ~85–212/week — so
velocity has been sustained, arguably increased, not tapering.

**Contributor count & company concentration**: `gh api
repos/anomalyco/opencode/contributors --paginate` returns **455 unique
contributor logins** (DOCUMENTED — raw count of the API response). But commit
concentration is heavily top-loaded — top contributors by commit count:
```
2246  thdxr
2000  adamdotdevin
1404  rekram1-node
1357  opencode-agent[bot]
1080  kitlangton
 981  actions-user
 567  iamdavidhill
 385  fwang
 364  Brendonovich
 355  jayair
```
Cross-referenced against `.github/TEAM_MEMBERS` (a flat text file listing 20
names: adamdotdevin, arvsrn, Brendonovich, fwang, Hona, iamdavidhill, jayair,
jlongster, kitlangton, kommander, ludvigrask, MrMushrooooom, nexxeln, R44VC0RP,
rekram1-node, thdxr, simonklee, Slickstef11, usrnk1, vimtor, starptech) —
**every one of the top human contributors (thdxr, adamdotdevin, rekram1-node,
kitlangton, iamdavidhill, fwang, Brendonovich, jayair) is a listed team
member**, and `gh api users/<login>` shows explicit company affiliation for
several: adamdotdevin → `"company":"@anomalyco"`, rekram1-node →
`"company":"@Anomalyco"`, kitlangton → `"company":"Anomaly"`. thdxr (top
committer, 2246 commits) has `"company":null` on the GitHub profile but is
on TEAM_MEMBERS. **DOCUMENTED**. Conclusion evidence (not stated as
conclusion, just the shape of the data): the top ~5-8 committers, who
dominate commit count, are the same ~20-person org roster; the 455-strong
"contributor" tail is presumably long-tail one-off PRs. Two bot accounts
(`opencode-agent[bot]`, `actions-user`) are themselves in the top 6 by commit
count — automated commits (likely CI-driven changesets/version bumps) are a
non-trivial share of raw commit volume, which inflates the raw commit/week
number above relative to "human-authored feature work."

**Core-loop-specific churn**: did not diff commit history scoped to
`packages/opencode/src/session/*` specifically (would require walking
`git log --follow` per file or the GraphQL commit-history-by-path API, not
done in this pass — **gap**, not a finding). What IS established: the
session-loop files exist as identifiably separate, actively-referenced
modules within the same fast-moving package (`packages/opencode/src/session/`)
that ships on the same ~1.5-day release cadence as everything else — there is
no evidence of a slower-moving "stable core" vs "fast-moving plugin surface"
split. Given release cadence applies repo-wide (single versioned package,
`packages/opencode`), the reasonable inference (not verified per-file) is
that core-loop files churn on the same overall cadence as the rest of the
package. Flagging this as **KNOWLEDGE/inference**, not confirmed by a
per-file blame history.

---

## 3. Loop stages the plugin API does NOT expose

Found the actual TypeScript source tree via `gh api
repos/anomalyco/opencode/contents/packages/opencode/src` — **DOCUMENTED**,
this is source, not a built binary or docs page. Top-level dirs include:
`account, acp, agent, auth, background, bus, cli, command, config,
control-plane, effect, env, event-manifest.ts, event-v2-bridge.ts, format,
git, id, ide, image, index.ts, installation, lsp, markdown.d.ts, mcp, node.ts,
patch, permission, plugin, project, provider, question, server, session,
share, skill, snapshot, sql.d.ts, storage, sync, temporary.ts, tool, util,
worktree`.

The `session/` directory is the loop itself. Listing (**DOCUMENTED**,
`gh api .../src/session`):
```
compaction.ts     instruction.ts   llm.ts        llm/
message-error.ts  message-v2.ts    message.ts    overflow.ts
processor.ts      prompt.ts        prompt/       reminders.ts
retry.ts          revert.ts        run-state.ts  schema.ts
session.ts        status.ts        summary.ts    system.ts
todo.ts           tools.ts
```
Read the actual file heads/imports of four of these (base64-decoded via `gh
api .../contents/<path>`), **DOCUMENTED**:

- **`session/llm.ts`** (404 lines) — the direct call site of `streamText`
  from Vercel's `ai` SDK (`import { streamText, wrapLanguageModel, ... } from
  "ai"`). Defines `StreamInput`/`StreamRequest` types carrying `model`,
  `agent`, `permission`, `system`, `messages`, `tools`, `toolChoice`,
  `retries`. Wires through `ProviderTransform`, `Plugin`, `Permission`,
  `EventV2Bridge`, and imports `LLMAISDK`, `LLMNativeRuntime`,
  `LLMRequestPrep` from a `./llm/` subdirectory. This is the exact model-
  invocation stage — no plugin hook (v1 or v2) intercepts at this level of
  detail (request assembly + streaming + tool-schema wiring in one place);
  hooks only see already-assembled inputs/outputs at coarser boundaries per
  the sibling plugin-surface docs.
- **`session/processor.ts`** (720 lines) — imports `Session`, `LLM`,
  `MessageV2`, `isOverflow` from `./overflow`, plus `Agent`, `Config`,
  `Permission`, `Plugin`, `Snapshot`, `Image`. This is the largest file in
  the directory and is the plausible tool-call-loop driver (turn-by-turn
  orchestration: call model → get tool calls → execute → append → repeat).
  Not fully read line-by-line (720 lines, only imports + structure
  confirmed) — the *existence and centrality* of this file is DOCUMENTED,
  its full internal control flow is not.
- **`session/compaction.ts`** (566 lines) — imports `Session`, `Provider`,
  `MessageV2`, `Token` (from `@/util/token`), `SessionProcessor`, `Agent`,
  `Plugin`, `Config`. This is the context-compaction/summarization logic —
  entirely internal; the plugin docs (per the sibling investigation) expose
  no compaction hook.
- **`session/overflow.ts`** (34 lines, small) — computes usable context
  budget: `usable({cfg, model, outputTokenMax})` reads `model.limit.context`,
  subtracts a `COMPACTION_BUFFER` of 20,000 tokens and a configurable
  reserved amount. This is the token-budget policy that decides *when*
  compaction fires — a pure internal policy function, not touchable via any
  hook.
- **`session/retry.ts`** (201 lines) — defines `RetryReason` including
  `"free_tier_limit" | "account_rate_limit"`, a `GO_UPSELL_MESSAGE` /
  `GO_UPSELL_URL` pointing at `opencode.ai/go` (evidence of a commercial
  upsell path embedded directly in retry/error-handling logic, source-level,
  not plugin-visible).
- **`session/llm/` subdirectory** (**DOCUMENTED**, listed via `gh api`):
  `ai-sdk.ts`, `native-request.ts`, `native-runtime.ts`, `request.ts`, plus
  an `AGENTS.md`. `ai-sdk.ts` is the direct source-level confirmation of
  where the plugin docs' `aisdk.language` hook name comes from — it lives
  next to (not instead of) a parallel `native-request.ts`/`native-runtime.ts`
  pair, implying opencode has *two* code paths for issuing model requests
  (an AI-SDK-mediated path and a "native" path) — a distinction invisible
  from the plugin surface alone.

**Provider abstraction source** (relevant to both Q3 and Q4, so cited once
here): `packages/opencode/src/provider/` contains `auth.ts` (229 lines),
`error.ts`, `model-status.ts`, `provider.ts`, `transform.ts`. `provider/
auth.ts` defines schema-level `Method` (oauth | api), `Prompt` (text |
select, with conditional `when` clauses), and `Authorization` (url + method
"auto"|"code" + instructions) types — i.e., a declarative, provider-agnostic
auth-flow description format, not one-off per-provider glue. **DOCUMENTED**
(read file content directly).

Everything in this section is source-file-existence-and-import-graph level
evidence: I confirmed these files exist, their rough size, and their import
lists, which establishes they are real, separate, substantial loop-internal
stages. I did NOT trace full control flow through `processor.ts` or
`compaction.ts` (too large for this pass) — labeling the *existence and
location* of these stages DOCUMENTED, and any claim about their exact
internal algorithm would be KNOWLEDGE/inference (none made above).

---

## 4. The provider layer — what a fork inherits for free

Two distinct layers exist, confirmed from source (**DOCUMENTED** throughout
this section unless noted):

**(a) Hand-written wire-protocol adapters** — `packages/llm/src/providers/`
(a separate workspace package, `@opencode-ai/llm`, own `package.json`,
`DESIGN.md`, `README.md`, `test/`). Listing:
```
amazon-bedrock.ts  anthropic.ts   azure.ts       cloudflare.ts
github-copilot.ts  google.ts      index.ts       openai-compatible-profile.ts
openai-compatible.ts  openai-options.ts  openai.ts  openrouter.ts  xai.ts
```
**13 files = 11 named-vendor adapters + 1 generic `openai-compatible` adapter
+ index.** Sibling directory `packages/llm/src/protocols/`:
```
anthropic-messages.ts   bedrock-converse.ts      bedrock-event-stream.ts
gemini.ts               openai-chat.ts           openai-compatible-chat.ts
openai-responses.ts     shared.ts                utils/
```
**6 distinct wire-protocol implementations** (Anthropic Messages, Bedrock
Converse, Bedrock EventStream, Gemini, OpenAI Chat, OpenAI Responses, plus an
OpenAI-compatible-chat variant) — i.e. opencode has hand-rolled request/
response translation for each major vendor wire format itself, rather than
depending entirely on `@ai-sdk` provider packages for wire-level work. The
`packages/llm/package.json` dependencies are minimal and low-level: `@smithy/
eventstream-codec`, `@smithy/util-utf8`, `aws4fetch`, `effect` — i.e. this
package implements AWS SigV4/eventstream handling itself rather than
depending on the AWS SDK, and depends on `effect` (Effect-TS) as its
structuring library, not on `@ai-sdk/*` packages at this layer.

**(b) A live external model registry (`models.dev`)** — `packages/core/src/
models-dev.ts` fetches model/pricing/context-limit metadata from an external
source at runtime (imports `ModelsDev` schema from `@opencode-ai/schema/
models-dev`, uses `FetchHttpClient`/`HttpClient`, has cache/flock/hash
utilities suggesting it downloads and locally caches a catalog rather than
bundling one statically). `anomalyco/models.dev` is itself a separate GitHub
repo (`gh api repos/anomalyco/models.dev`: "An open-source database of AI
models," 5,872 stars). Queried its live public API directly:
```
$ curl -s https://models.dev/api.json | python3 -c "...len(d)..."
providers: 166
```
**166 providers registered** in the models.dev catalog as of this check
(**DOCUMENTED**, live API call, timestamp implicit in "now" = 2026-07-13).
This is model/pricing *metadata* (what models exist, context limits, cost
tiers — confirmed by `CostTier` schema in `models-dev.ts`: input/output/
cache_read/cache_write pricing + context-size tier), not 166 wire-protocol
implementations — a model available via models.dev still needs one of the
~7 protocol implementations above (or the generic OpenAI-compatible path) to
actually be called. CONTRIBUTING.md states directly: "New providers
shouldn't require many if ANY code changes... if you want to add support for
a new provider first make a PR to: https://github.com/anomalyco/models.dev" —
confirming the registry/protocol split is intentional and documented by the
maintainers themselves.

**(c) A third layer: built-in provider "plugins" bundled in the main repo.**
`packages/opencode/src/plugin/` (distinct from `packages/opencode/src/
session/llm/`) contains: `azure.ts`, `cloudflare.ts`, `digitalocean.ts`,
`github-copilot/` (subdir), `index.ts`, `install.ts`, `loader.ts`, `meta.ts`,
`openai/` (subdir, containing at least `codex.ts` per code search),
`pty-environment.ts`, `shared.ts`, `snowflake-cortex.ts`, `tui/`, `xai.ts`.
This shows opencode ships several vendor-specific *integrations* (not just
wire protocols) as first-party bundled plugins — e.g. GitHub Copilot and
OpenAI Codex get dedicated subdirectories, suggesting more than simple
API-key auth (likely their own OAuth/device-flow or session-token schemes).
Not fully read (would need per-file inspection to characterize each), but
their existence and naming is **DOCUMENTED** via directory listing and one
code search (`gh api search/code -f q='oauth repo:anomalyco/opencode
extension:ts path:packages/opencode/src'`) which surfaced `mcp/oauth-
callback.ts`, `mcp/oauth-provider.ts`, `provider/auth.ts`, `plugin/
digitalocean.ts`, `plugin/openai/codex.ts`, `plugin/github-copilot/
copilot.ts`, `plugin/xai.ts`, `account/account.ts`, `core/src/oauth/page.ts`
— i.e. OAuth-flow code is spread across at least 9 distinct files, not one
central shim.

**Auth-flow characterization**: `provider/auth.ts` (229 lines, read in full)
defines a declarative auth-method schema — `Method{type: "oauth"|"api",
label, prompts}`, `Prompt` as `TextPrompt | SelectPrompt` (with conditional
`when` clauses keyed on other prompt values), and `Authorization{url, method:
"auto"|"code", instructions}`. This is provider-agnostic scaffolding meant to
describe arbitrary auth flows (not just Anthropic/OpenAI) declaratively; the
per-vendor specifics (e.g. actual OAuth client IDs/endpoints for Copilot or
Codex) live in the `plugin/` subtree files named above. `core/src/auth/` /
`packages/opencode/src/auth/index.ts` (97 lines, read in full) is a thin
storage schema (`Oauth | Api | WellKnown` discriminated union) for persisting
credentials — not the flow logic itself.

**Summary quantification** (for the parent's weighing, not a recommendation):
a fork inherits, without rebuilding: **11 named hand-written vendor wire
adapters + 1 generic OpenAI-compatible adapter** (`llm/src/providers/`), **7
wire-protocol implementations** covering the major request/response formats
in use industry-wide (`llm/src/protocols/`), **a live-fetched external
catalog of 166 providers'** worth of model/pricing/context metadata
(`models.dev`, itself a separate maintained OSS project under the same org),
**at least 9 files' worth of OAuth/auth-flow plumbing** spanning a
provider-agnostic declarative schema plus per-vendor implementations for at
least GitHub Copilot, OpenAI Codex, Azure, Cloudflare, DigitalOcean, xAI, and
Snowflake Cortex, and **a low-level AWS SigV4/eventstream implementation**
(`@smithy/eventstream-codec`, `aws4fetch`) for Bedrock rather than a
dependency on the full AWS SDK. None of this is reachable or reconstructable
via the plugin API alone per the sibling investigation's findings — the
plugin surface consumes already-resolved providers/models, it does not let a
plugin add a new wire protocol or OAuth flow from outside the source tree
(unconfirmed against the sibling doc's exact wording — flagged as
**KNOWLEDGE** pending cross-check by the reader against `docs/audit/
opencode-plugin-api.md` directly, since re-deriving that was explicitly out
of scope here).

---

## Gaps / not done in this pass

- Did not diff `git log` scoped to `session/*` paths specifically for
  churn-rate-of-core-vs-rest (flagged in §2).
- Did not read `session/processor.ts` or `session/compaction.ts` line-by-line
  (720 and 566 lines respectively) — existence/imports confirmed, full
  control-flow not traced.
- Did not verify whether any subpackage under `packages/` carries a
  different license than the root MIT LICENSE file.
- Did not attempt to legally verify absence of a CLA beyond checking for a
  CLA-bot workflow file and searching in-repo docs — a CLA could in
  principle be enforced out-of-band (e.g. a first-PR bot comment) without a
  committed config file; this was not checked against a live PR.
