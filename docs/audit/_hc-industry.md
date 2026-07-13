# Industry survey: per-agent model choice, named model combinations, and failover

Bounded evidence survey for the design doc on per-agent model choice, named model-combination
patterns, and on-the-fly model failover. **Evidence only — no recommendation for swarm.**

Every claim is labeled **DOCUMENTED** (with source) or **KNOWLEDGE** (training data, may be
stale, not verified against a live source at research time). Research was fanned out across four
parallel agents, each with WebSearch/WebFetch; sources actually fetched are listed at the end of
each section.

---

## 1. LangGraph (LangChain)

**(a) Model-per-node/agent UX surface — DOCUMENTED**
No dedicated "per-node model" abstraction. A node in the low-level `StateGraph` API is just a
Python callable added via `add_node("call_llm", call_llm)`; the model is whatever chat-model
object that function closes over. At the prebuilt-agent layer, `create_react_agent(model=...)`
and `create_supervisor([agents...], model=...)` take a `model` constructor argument — either a
string (`"openai:gpt-4.1"`) or a pre-instantiated chat-model object:
```python
model = ChatOpenAI(model="gpt-4o")
math_agent = create_react_agent(model=model, tools=[add, multiply], name="math_expert")
research_agent = create_react_agent(model=model, tools=[web_search], name="research_expert")
workflow = create_supervisor([research_agent, math_agent], model=model, prompt=...)
```
(Source: github.com/langchain-ai/langgraph-supervisor-py)

**(b) Named presets / combination patterns — DOCUMENTED (topologies) / not found (model tiers)**
LangGraph documents *orchestration* topologies — "supervisor," "network," "hierarchical teams"
(langgraph-supervisor-py, `hierarchical_agent_teams.ipynb`) — which are agent-graph shapes, not
model-tiering conventions. No named "cheap/expensive" model-combo preset was found as a
first-class concept; per-agent model choice is left entirely to the user.

**(c) Automatic failover — DOCUMENTED, two separate uncomposed mechanisms**
1. **Node-level retry (same model)**: `RetryPolicy` NamedTuple — `initial_interval=0.5`,
   `backoff_factor=2.0`, `max_interval=128.0`, `max_attempts=3`, `jitter=True`,
   `retry_on=default_retry_on`, attached via `add_node("call_llm", call_llm, retry=RetryPolicy(...))`.
   (Source: github.com/langchain-ai/langgraph `libs/langgraph/langgraph/types.py`, fetched directly.)
2. **Model-level fallback (switch model/provider)**: LangChain-core's `.with_fallbacks()` —
   a separate library layer, not LangGraph-specific:
   ```python
   model = ChatAnthropic(model="claude-sonnet-4-6").with_fallbacks(
       [ChatOpenAI(model="gpt-5.4-mini")]
   )
   ```
   "Fallbacks are tried in order until one succeeds or all fail." (Source:
   reference.langchain.com RunnableWithFallbacks; langchain-ai/langchain `how_to/fallbacks.ipynb`.)

These two are **not unified** — "retry same model N times, then fall back to a different model"
requires manually composing both, or hand-rolling state via conditional edges.

**(d) Conceptual cost — DOCUMENTED (synthesized from above)**
~4-5 distinct concepts spanning two libraries (langgraph + langchain-core): the
node-is-just-a-callable model (no dedicated field), `create_react_agent`/`create_supervisor`
constructor args, `RetryPolicy` (6 fields), and `RunnableWithFallbacks`/`.with_fallbacks()` — with
no single unified "failover" abstraction tying retry and fallback together.

Sources fetched: github.com/langchain-ai/langgraph-supervisor-py; langgraph `types.py` (raw);
reference.langchain.com/python/langgraph/types/RetryPolicy; langchain.com/blog/fault-tolerance-in-langgraph;
docs.langchain.com/oss/python/langchain/{overview,models}; reference.langchain.com RunnableWithFallbacks.

---

## 2. OpenAI Agents SDK (and predecessor OpenAI Swarm)

**(a) Model-per-agent UX surface — DOCUMENTED**
`model` is a constructor argument on the `Agent` dataclass — a string or a concrete `Model`
implementation:
```python
spanish_agent = Agent(name="Spanish agent", instructions="You only speak Spanish.", model="gpt-5-mini")
english_agent = Agent(name="English agent", instructions="...",
    model=OpenAIChatCompletionsModel(model="gpt-5-nano", openai_client=AsyncOpenAI()))
triage_agent = Agent(name="Triage agent", handoffs=[spanish_agent, english_agent], model="gpt-5.6-sol")
```
Three precedence layers: `OPENAI_DEFAULT_MODEL` env var → per-run `RunConfig(model=...)` →
per-agent `model=` (highest precedence). No CLI flag or config file — all Python
constructor/dataclass arguments. (Source: openai.github.io/openai-agents-python `docs/models/index.md`,
fetched directly via GitHub API.)

**Predecessor, OpenAI Swarm — DOCUMENTED**: `Agent.model: str` field, default `"gpt-4o"`.
`client.run(..., model_override="...")` overrides the model for a single call without editing the
Agent definition. (Source: github.com/openai/swarm README.)

**(b) Named presets / combination patterns — DOCUMENTED (prose guidance, not an API)**
The docs explicitly name the pattern in prose under "Mixing models in one workflow": "you could
use a smaller, faster model for triage, while using a larger, more capable model for complex
tasks" — with a code example (cheap triage → expensive specialist). This is guidance + example,
not a distinct named API/decorator/preset. Caveat also documented: mixing `OpenAIResponsesModel`
and `OpenAIChatCompletionsModel` shapes is discouraged unless all used features are supported on
both. Separately, `docs/multi_agent.md` names two control-flow topologies — "Agents as tools"
(`Agent.as_tool()`) and "Handoffs" — not model-tiering presets.

**(c) Automatic failover — DOCUMENTED, opt-in, same-model-only, no cross-model fallback exists**
`ModelSettings(retry=ModelRetrySettings(...))`, **off by default**:
```python
from agents import Agent, ModelRetrySettings, ModelSettings, retry_policies

agent = Agent(name="Assistant", model="gpt-5.6-sol",
    model_settings=ModelSettings(retry=ModelRetrySettings(
        max_retries=4,
        backoff={"initial_delay": 0.5, "max_delay": 5.0, "multiplier": 2.0, "jitter": True},
        policy=retry_policies.any(
            retry_policies.provider_suggested(), retry_policies.retry_after(),
            retry_policies.network_error(), retry_policies.http_status([408,409,429,500,502,503,504]),
        ))))
```
`retry_policies` ships composable named helpers: `.never()`, `.provider_suggested()`,
`.network_error()`, `.retry_after()`, `.http_status([...])`, `.any(...)`, `.all(...)`. (Source:
confirmed directly against `src/agents/retry.py` and `src/agents/model_settings.py`.)

**Confirmed limitation (source-level, not just docs)**: this retries the *same* model call with
backoff. There is **no fallback-to-a-different-model list** anywhere in the SDK (unlike
LangChain's `.with_fallbacks()`). A user wanting model-switch-on-failure must catch the exception
after retries are exhausted and manually invoke a different `Agent` themselves.

**Swarm predecessor**: no retry/rate-limit handling at all; only generic tool-call error recovery
via chat history (agent-level conversational recovery, not network/model retry).

**(d) Conceptual cost — DOCUMENTED (synthesized)**
Base model selection is one concept (`model=` string). Full retry subsystem adds ~5-6 new types
(`ModelSettings`, `ModelRetrySettings`, `ModelRetryBackoffSettings`, `retry_policies` namespace
with 7 helpers, `RetryPolicyContext`, `RetryDecision`) — comparable in size to LangGraph's
`RetryPolicy` — with **no built-in fallback-model concept at all**, so cross-model failover must
be hand-designed and hand-coded by the user.

Sources fetched: openai.github.io/openai-agents-python/{agents,models,ref/model_settings}; GitHub
raw fetches of `README.md`, `src/agents/model_settings.py`, `src/agents/retry.py`,
`docs/multi_agent.md` (repo `openai/openai-agents-python`); github.com/openai/swarm README.

---

## 3. CrewAI

**(a) Model-per-agent UX surface — DOCUMENTED**
Two surfaces. YAML/JSONC config (`agents.yaml`), the recommended approach:
```jsonc
{
  "role": "{topic} Senior Data Researcher",
  "goal": "Uncover cutting-edge developments in {topic}",
  "backstory": "You find the most relevant information and present it clearly.",
  "llm": "openai/gpt-4o",
  "tools": ["SerperDevTool"]
}
```
Or direct Python: `Agent(role=..., llm="gpt-4")` (default `OPENAI_MODEL_NAME` or `"gpt-4"`). A
separate `function_calling_llm` field lets tool-calling route to a cheaper model while reasoning
uses a stronger one. Model strings follow LiteLLM's `provider/model` convention — CrewAI supports
"any model available through LiteLLM," including local Ollama. (Source: docs.crewai.com/en/concepts/agents.)

**(b) Named presets / combination patterns — DOCUMENTED (mechanism) + KNOWLEDGE (specific advice)**
`Process.hierarchical` + a `manager_llm` (or full `manager_agent`) parameter on `Crew` is a
first-class manager/worker split, separate from worker-agent LLMs — the closest thing to a named
manager/worker model pattern found in this survey. (Source: docs.crewai.com/en/learn/hierarchical-process.)
Community guidance recommending specific models per role (e.g. GPT-4o-mini for simple crews) is
**KNOWLEDGE** — found via secondary blog/community sources, not the official doc page. A
Towards-Data-Science piece and community threads report hierarchical-mode manager delegation is
unreliable in practice (tasks run sequentially regardless of intended routing) — **KNOWLEDGE**,
flagged as a real-world caveat, not an official claim.

**(c) Automatic failover — DOCUMENTED, native retry is same-model only; cross-model delegated out**
CrewAI's `LLM` class exposes `timeout`/`max_retries` against the *same* model/provider:
```python
llm = LLM(model="openai/gpt-4o", timeout=60.0, max_retries=3)
```
No native `fallback_models` list was found. For actual cross-model failover, CrewAI's docs point
to LiteLLM underneath (non-natively-integrated providers route through it) and to third-party
gateway integration (Portkey) — failover is delegated to an external layer, not first-party.
(Source: docs.crewai.com/en/concepts/llms; docs.crewai.com/en/observability/portkey.) A live
GitHub issue (crewAIInc/crewAI#4262) documents a real bug where LiteLLM fallback breaks with
Groq-hosted OpenAI-compatible models — evidence this integration point is immature.

**(d) Conceptual cost**
Basic per-agent model: 1 concept (`llm` field). Manager/worker split: +2
(`Process.hierarchical`, `manager_llm`/`manager_agent`) + `allow_delegation` discipline. Retries:
+2 flags, same-model only. True cross-model fallback: exit CrewAI's vocabulary entirely and learn
a second system (LiteLLM Router or a third-party gateway) — the failover feature is not "free"
inside CrewAI's own abstractions.

Sources fetched: docs.crewai.com/en/{concepts/agents,concepts/llms,learn/hierarchical-process,
observability/portkey}; github.com/crewAIInc/crewAI/issues/4262 (via search).

---

## 4. AutoGen / AG2 (note the fork)

**Fork context — KNOWLEDGE (corroborated across multiple independent secondary sources, no
single official page)**: In Nov 2024, AutoGen's original creators left Microsoft and forked the
0.2 codebase as **AG2** (`ag2ai/ag2`), keeping the `autogen` PyPI package name and Discord.
Microsoft rewrote its own repo (`microsoft/autogen`) from scratch as **v0.4** — an actor-model,
event-driven architecture unrelated in API shape to 0.2/AG2. In Oct 2025 Microsoft folded AutoGen
into "Microsoft Agent Framework" (merged with Semantic Kernel); classic AutoGen entered
maintenance mode. Net effect: **AG2 = continuation of AutoGen 0.2's API**; **microsoft/autogen
0.4+/Agent Framework = a different, incompatible API** despite similar branding.

### AG2 (continuation of AutoGen 0.2 API)

**(a) Model-per-agent UX — DOCUMENTED**
`llm_config` on the agent constructor:
```python
llm_config = LLMConfig({"api_type": "openai", "model": "gpt-5", "api_key": os.environ["OPENAI_API_KEY"]})
my_agent = ConversableAgent(name="helpful_agent", system_message="...", llm_config=llm_config)
```
(Source: docs.ag2.ai/latest/docs/user-guide/basic-concepts/llm-configuration/.)

**(b) Named presets — DOCUMENTED (mechanism) / not found (named pattern)**
`LLMConfig` supports multiple config dicts + a `.where(model=...)` filter to scope configs per
agent from a shared pool. No officially named preset combo (no manager/worker naming convention
analogous to CrewAI's) was found — confirmed by direct fetch of the advanced-concepts deep-dive
page, which gives no role-based example code.

**(c) Automatic failover — DOCUMENTED, built-in ordered fallback list, "for free"**
This is AG2's most distinctive feature vs. every other framework surveyed: a **built-in,
in-order model fallback list**, no external router needed:
```python
llm_config = LLMConfig(
    {"api_type": "openai", "model": "gpt-5-nano", "api_key": os.environ["OPENAI_API_KEY"]},
    {"api_type": "openai", "model": "gpt-5", "api_key": os.environ["OPENAI_API_KEY"]},
)
```
Documented behavior: "An agent uses the very first model configuration... If the model fails
(e.g., API throttling) the agent will retry the request against the 2nd configuration and so on
until prompt completion is received (or throws an error if none of the models successfully
completes the request)." (Source: docs.ag2.ai/latest/.../llm-configuration/, matching language on
the legacy 0.2 docs, confirming lineage.) `timeout` is documented; a `max_retries` param is
referenced only in secondary community text — **KNOWLEDGE**, not directly confirmed in fetched pages.

**(d) Conceptual cost**
Low: one object (`LLMConfig`/`config_list`), one behavior (order = priority, first-success-wins,
exhausted list = hard error), plus optional `.where()` filtering. No separate fallback
keyword/decorator to learn — fallback is "add more dicts to the list." Trade-off: failure
classification (which exceptions count as "fails") is not spelled out in the fetched pages.

### Microsoft AutoGen (current, 0.4+ / "Agent Framework")

**(a) Model-per-agent UX — DOCUMENTED**
Explicit `model_client` object, not a config dict:
```python
model_client = OpenAIChatCompletionClient(model="gpt-4o")
agent = AssistantAgent(name="assistant", model_client=model_client, tools=[...])
```
Provider-specific client classes exist (`OpenAIChatCompletionClient`,
`AzureOpenAIChatCompletionClient`, `AzureAIChatCompletionClient`, `OllamaChatCompletionClient`
(experimental), `AnthropicChatCompletionClient` (experimental), a Semantic Kernel adapter). This is
structurally different from AG2's dict-based config — object instantiation, not declarative
config. (Source: microsoft.github.io/autogen/stable/.../model-clients.html.)

**(c) Automatic failover — DOCUMENTED (limited) / gap explicitly documented**
No sequential model-fallback-list analogous to AG2's `config_list` was found at the model-client
layer. Resilience instead lives in the separate Microsoft Agent Framework layer as middleware:
`RetryPolicy` with exponential backoff (agent-level or per-invocation override), and
`AgentMiddleware` to intercept/retry/degrade around invocations. Explicitly documented gap:
"individual tool call failures surface as exceptions from RunAsync, with no RetryPolicy,
automatic backoff, or fallback routing — retry logic must be implemented via middleware or
try/catch patterns." (Source: learn.microsoft.com/en-us/agent-framework/agents/middleware/exception-handling;
github.com/microsoft/agent-framework issue #2687.)

**(d) Conceptual cost**
Noticeably higher than AG2: `RetryPolicy` for retries, hand-written `AgentMiddleware` for
cross-model failover, a separate Durable Extension concept for checkpointed recovery. No
one-line "add a second dict" primitive — failover is DIY middleware, not a config feature.

### Summary contrast (CrewAI / AG2 / MS AutoGen)

| | CrewAI | AG2 | MS AutoGen (0.4+/Agent Framework) |
|---|---|---|---|
| Model-per-agent surface | `llm` field (YAML/JSONC or `Agent(llm=...)`) | `llm_config`/`LLMConfig` dict(s) | `model_client` object instance |
| Manager/worker naming | Yes — `manager_llm`/`manager_agent` + `Process.hierarchical` | No named pattern | No named pattern |
| Built-in cross-model fallback | No (native retry same-model only; cross-model via LiteLLM/Portkey, external) | Yes — ordered `LLMConfig` list, first-success-wins | No — hand-build via `AgentMiddleware`/`RetryPolicy` |
| New concepts for failover | External system (LiteLLM Router or Portkey) | ~0 (reuse the list you already built) | Middleware pattern + RetryPolicy (+ Durable Extension) |

Sources fetched: docs.ag2.ai/latest/docs/user-guide/{basic-concepts/llm-configuration,
advanced-concepts/llm-configuration-deep-dive}/; microsoft.github.io/autogen/0.2/docs/topics/llm_configuration/;
microsoft.github.io/autogen/stable/.../model-clients.html; github.com/microsoft/agent-framework
issue #2687; learn.microsoft.com/en-us/agent-framework/agents/middleware/exception-handling;
dev.to/maximsaplin and gettingstarted.ai/autogen-vs-ag2 (secondary, fork history).

---

## 5. Claude Code subagents

**(a) Model-per-agent UX surface — DOCUMENTED**
The `model:` field in YAML frontmatter of a `.claude/agents/*.md` file:
```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---
```
Accepted values (quoted): "**Model alias**: `sonnet`, `opus`, `haiku`, or `fable`" /
"**Full model ID**: e.g. `claude-opus-4-8` or `claude-sonnet-5`" / "**inherit**: same model as the
main conversation" / "**Omitted**: defaults to `inherit`." Resolution order: (1)
`CLAUDE_CODE_SUBAGENT_MODEL` env var, (2) a per-invocation `model` param Claude can pass when
spawning, (3) the subagent's frontmatter `model`, (4) the main conversation's model. Resolved
values are checked against an org `availableModels` allowlist; excluded values fall back to the
inherited model. Also settable via `--agents` CLI JSON (session-scoped, ephemeral), same `model`
key. (Source: code.claude.com/docs/en/sub-agents.)

**(b) Named presets — DOCUMENTED (built-in defaults) / no named triad**
No named pattern like aider's triad. Built-in subagents have individual hardcoded/capped
defaults: `Explore` inherits the main conversation's model "capped at Opus on the Claude API";
`Plan` and `general-purpose` inherit directly; `statusline-setup` is hardcoded to Sonnet;
`claude-code-guide` is hardcoded to Haiku. These are per-agent defaults, not a named
multi-model vocabulary.

**(c) Automatic failover — DOCUMENTED, two separate mechanisms, neither is per-subagent**
1. **Session-level fallback**: `--fallback-model` flag / `fallbackModel` settings array. "When the
   primary model is overloaded, unavailable, or returns another non-retryable server error,
   Claude Code can switch to a fallback model instead of failing the request... Chains are capped
   at three models after duplicate removal... The switch lasts for the current turn only."
   Explicitly: "Authentication, billing, rate-limit, request-size, and transport errors never
   trigger a switch." (Source: code.claude.com/docs/en/model-config.) So classic 429 rate-limiting
   does **not** trigger this fallback — only overload/unavailability/non-retryable server errors do.
2. **Exponential-backoff retry**: 529/500/timeouts/dropped connections/some 429s retried up to
   `CLAUDE_CODE_MAX_RETRIES` (default 10, capped 15); `CLAUDE_CODE_RETRY_WATCHDOG=1` retries
   429/529 indefinitely for unattended sessions. (Source: code.claude.com/docs/en/errors.)

There is **no `fallbackModel` in subagent frontmatter** — it's session/CLI-wide, not per-agent. A
subagent whose call fails terminally after retries reports "Agent terminated early due to an API
error" back to the parent rather than silently switching models. (Source: sub-agents.md, "API
errors in subagents" section.) A separate, unrelated "fallback" concept exists for Fable 5 safety
classifiers rerouting to Opus — not evidence for the rate-limit/overload failover pattern surveyed.

**(d) Conceptual cost**
~5-6 concepts spread across two docs pages: `model` field + 4 value forms; the 4-level resolution
order; the session-scoped `--fallback-model`/`fallbackModel` (distinct mechanism, distinct
trigger conditions excluding rate limits); retry env vars
(`CLAUDE_CODE_MAX_RETRIES`, `CLAUDE_CODE_RETRY_WATCHDOG`, `API_TIMEOUT_MS`); built-in agents'
individual hardcoded defaults. Per-agent model and fallback are unrelated, non-composable mechanisms.

Sources fetched: code.claude.com/docs/en/{sub-agents,errors,model-config,cli-reference}.

---

## 6. aider

**(a) Model-per-role UX surface — DOCUMENTED**
CLI flags (env var + YAML key equivalents for each): `--model MODEL` (main chat model),
`--editor-model EDITOR_MODEL` (editor tasks, default depends on `--model`), `--weak-model
WEAK_MODEL` (commit messages + chat-history summarization, default depends on `--model`),
`--editor-edit-format EDITOR_EDIT_FORMAT`. YAML (`.aider.conf.yml`) uses the same keys without
`--`. A separate, more advanced per-model-metadata file (`.aider.model.settings.yml`) lets a model
entry declare its own paired weak/editor models:
```yaml
- name: anthropic/claude-3-5-sonnet-20241022
  edit_format: diff
  weak_model_name: anthropic/claude-3-5-haiku-20241022
  editor_model_name: anthropic/claude-3-5-sonnet-20241022
  editor_edit_format: editor-diff
```
(Source: aider.chat/docs/config/{options,aider_conf,adv-model-settings}.html.)

**(b) Named presets — DOCUMENTED, the clearest named triad found in this survey**
Aider documents "up to three models simultaneously to optimize cost and performance": **main**
model (complex code generation), **editor** model (executes edits — used specifically in
Architect mode, where the main/"architect" model proposes and the editor model turns the proposal
into concrete edits), and **weak** model (lightweight tasks: commit messages, history
summarization). This triad is aider's own named architecture, referenced in docs as a deliberate
mode. (Source: aider.chat/docs/{config/adv-model-settings,usage/modes}.html.)

**(c) Automatic failover — not documented; none found**
No automatic-switch-to-another-model behavior on rate limit or error across any of the three
fetched config pages. Only related control is `--timeout` (per-call timeout). One doc explicitly
states aider "never *enforces* token limits, it only *reports* token limit errors from the API
provider" — errors surface, they aren't worked around. (A GitHub feature request, #3383, asks for
`/editor-model`/`/weak-model` in-chat commands — evidence of ongoing parameterization work, not
failover.)

**(d) Conceptual cost**
Three named roles × 3 surfaces each (CLI flag + env var + YAML key) = 9 permutations of the same 3
concepts, plus an optional advanced per-model settings file, plus `--editor-edit-format` as a 4th,
more obscure axis. No fallback vocabulary exists.

Sources fetched: aider.chat/docs/config/{adv-model-settings,options,aider_conf}.html.

---

## 7. opencode

Note on repo identity — **KNOWLEDGE** (not directly confirmed via a fetched page): `sst/opencode`
appears to be the repo behind opencode.ai's docs; a same-named but unrelated older project exists
at `opencode-ai/opencode` (Go-based TUI). This survey uses opencode.ai's own docs.

**(a) Model-per-agent UX surface — DOCUMENTED**
Per-agent `model` field, format `provider/model-id`, settable in JSON config or markdown
frontmatter:
```json
{ "agent": { "plan": { "model": "anthropic/claude-haiku-4-20250514" } } }
```
```yaml
---
model: anthropic/claude-sonnet-4-20250514
---
```
Resolution rule (quoted): "If you don't specify a model, primary agents use the model globally
configured while subagents will use the model of the primary agent that invoked the subagent."
Frontmatter also supports `mode` (`primary`/`subagent`/`all`), `temperature`, `maxSteps`, tool
enable/disable, permissions; unrecognized keys pass through directly to the provider (e.g.
`reasoningEffort`, `textVerbosity`). A global `small_model` key is used for lightweight tasks
(title generation): "By default, OpenCode tries to use a cheaper model if one is available from
your provider, otherwise it falls back to your main model" — a cost-routing default, not an
error-triggered fallback. (Source: opencode.ai/docs/{agents,config,models}/.)

**(b) Named presets — weaker than aider's; no editor-model equivalent**
A `default_agent` config concept and two built-in agent names (`build`, `plan`) ship as defaults,
plus the main-model/`small_model` two-tier split (analogous to but less elaborated than aider's
main/weak split). No named multi-model pattern comparable to aider's triad is documented.

**(c) Automatic failover — not confirmed as first-party; community gap widely reported**
The three fetched opencode.ai pages (config, agents, models) describe model selection/priority
only, no retry/circuit-breaker/failover language. WebSearch surfaced multiple open GitHub
feature-request issues in this space ("[FEATURE]: Native Model Fallback / Failover Support,"
"fallback models for (sub) agents") plus at least one third-party plugin
(`opencode-model-fallback`) built to patch the gap by redirecting to a healthy model on
rate-limit/5xx/timeout — **KNOWLEDGE/weakly-sourced** (could not fully confirm these issues are
against the exact `sst/opencode` repo from search snippets alone). Net assessment: **no confirmed
first-party automatic failover** in opencode's own docs at research time.

**(d) Conceptual cost**
~5 concepts: `provider/model-id` string format; per-agent `model` override (JSON or frontmatter);
`mode` as a separate axis from model; `default_agent`; `small_model` as a second cost-oriented
tier; open-ended provider-specific passthrough options. No fallback vocabulary since none is
first-party-documented.

Sources fetched: opencode.ai/docs/{agents,config,models}/.

### Cross-tool comparison (Claude Code / aider / opencode)

| | Per-agent model surface | Named combo pattern | First-party rate-limit/error failover | Concept count |
|---|---|---|---|---|
| Claude Code | frontmatter `model:` (4 value forms) + resolution order | none named; built-ins have individual hardcoded defaults | Yes, but session-scoped, turn-only, excludes rate-limit errors; separate from per-agent model | ~5-6, split across 2 mechanisms |
| aider | `--model`/`--editor-model`/`--weak-model` (+ YAML + per-model-settings file) | Yes — explicit main/editor/weak triad, tied to Architect mode | Not documented | ~3 named roles + 1 optional file format |
| opencode | per-agent `model` (provider/model-id) + `small_model` | Weak — main/small_model split only | Not documented first-party; community requests + 3rd-party plugin | ~5, with open-ended passthrough options |

---

## 8. LiteLLM (Router)

**(a) Model-per-call UX surface — DOCUMENTED**
`model_list`: a list of dicts, each mapping a logical `model_name` alias to concrete
`litellm_params` (actual provider/model + credentials). Multiple entries can share one
`model_name` to represent multiple deployments/providers behind an alias:
```python
model_list = [{
    "model_name": "gpt-3.5-turbo",
    "litellm_params": {"model": "azure/chatgpt-v-2", "api_key": ..., "api_base": ...}
}]
```
Deployment priority within one `model_name` uses an `order` field (order=1 tried first).
(Source: docs.litellm.ai/docs/routing.)

**(b) Named routing strategies — DOCUMENTED**
`routing_strategy` string passed to `Router(...)`: `"simple-shuffle"` (default, random weighted
shuffle), `"least-busy"`, `"usage-based-routing"`/`"usage-based-routing-v2"` (v2 requires Redis
for shared state), `"latency-based-routing"` (lowest observed latency), `"cost-based-routing"`
(name only confirmed, parameters not shown on fetched page). (Source: docs.litellm.ai/docs/routing.)

**(c) Automatic failover — DOCUMENTED, the deepest failover DSL found in this survey**
Three distinct, composable mechanisms:
- **Fallbacks**: explicit ordered map from a primary `model_name` to fallback `model_name`(s):
  ```yaml
  router_settings:
    fallbacks: [{"gpt-3.5-turbo": ["gpt-4"]}]
  ```
  Variants fire on different error classes: `context_window_fallbacks` (context-length errors),
  `content_policy_fallbacks` (content-policy refusals), `default_fallbacks` (catch-all when no
  model-specific fallback matches). "Fallbacks are done in-order."
- **Retries**: global `num_retries`, or a granular `RetryPolicy` keyed by exception type:
  ```python
  retry_policy = RetryPolicy(ContentPolicyViolationErrorRetries=3, AuthenticationErrorRetries=0,
      BadRequestErrorRetries=1, TimeoutErrorRetries=2, RateLimitErrorRetries=3)
  ```
- **Cooldowns**: after `allowed_fails` failures in a rolling window, a deployment is pulled from
  rotation for `cooldown_time` seconds (`Router(..., allowed_fails=1, cooldown_time=100)`);
  disableable via `disable_cooldowns=True`.
(Source: docs.litellm.ai/docs/routing; docs.litellm.ai/docs/proxy/reliability.)

**(d) Conceptual cost — DOCUMENTED (synthesized)**
Large surface area, essentially a full traffic-management DSL: `model_name` (alias) vs.
`litellm_params.model` (concrete) split; `order`; four separate fallback lists keyed by different
error classes; a 5-value routing-strategy enum (one requiring Redis); a per-error-type
`RetryPolicy` distinct from simpler `num_retries`; a cooldown/`allowed_fails` window concept
distinct from retries.

Sources fetched: docs.litellm.ai/docs/routing; docs.litellm.ai/docs/proxy/reliability.

---

## 9. OpenRouter

**(a) Model-per-call UX surface — DOCUMENTED**
A `models` array in the request body, tried sequentially in priority order:
```json
{ "models": ["~anthropic/claude-sonnet-latest", "gryphe/mythomax-l2-13b"],
  "messages": [{ "role": "user", "content": "..." }] }
```
Billing follows whichever model actually served the request (indicated in the response's `model`
field). A separate, orthogonal `provider` object controls which *upstream provider* serves a
chosen model (not model choice itself):
```json
{ "provider": { "order": ["openai", "together"], "allow_fallbacks": false } }
```
(Source: openrouter.ai/docs/guides/routing/{model-fallbacks,provider-selection}.)

**(b) Named presets — DOCUMENTED**
`provider.sort`: `"price"`, `"throughput"`, or `"latency"` (or structured `{by, partition}` form).
Model-name suffix shortcuts: `:floor` (cheapest-price routing) and `:nitro` (fastest-throughput
routing). Separately, an "Auto Router" exposes a `cost_quality_tradeoff` (0-10 scale, default 7)
plugin parameter for blending cost vs. quality when picking a model automatically — a different
feature from both the `models`-array fallback and the `:floor`/`:nitro` suffixes. (Source:
openrouter.ai/docs/{features/model-routing,guides/routing/provider-selection}.)

**(c) Automatic failover — DOCUMENTED**
Triggers on rate-limiting, provider downtime, context-length validation errors, and
moderation/content-policy refusals. Strictly sequential: if model[0] errors, try model[1], etc.;
if all fail, the last error is returned. `provider.allow_fallbacks` (default `true`) separately
controls whether OpenRouter may silently substitute a backup *provider* for the same model —
distinct from the `models`-array fallback. (Source: openrouter.ai/docs/guides/routing/model-fallbacks.)

**(d) Conceptual cost**
Two independent axes easy to conflate: `models` (array, model-level fallback) vs. `provider`
(object, provider-level routing for a fixed model). Plus: `sort` enum + `:floor`/`:nitro`
suffixes, `allow_fallbacks`, `require_parameters`, `data_collection`, `ignore`/`only` lists, and
the Auto Router's `cost_quality_tradeoff`. Flatter than LiteLLM overall — no retry-policy-by-
error-type, no cooldown/allowed-fails window, no Redis-backed strategy (OpenRouter is a hosted
single request-response API, not a client-side load balancer).

Sources fetched: openrouter.ai/docs/{features/model-routing,guides/routing/model-fallbacks,
guides/routing/provider-selection}.

---

## 10. Temporal (analogy only — worker/task retry, not LLM-specific)

- Retry policy fields (documented defaults): `InitialInterval` (1s), `BackoffCoefficient` (2.0,
  exponential), `MaximumInterval` (100x initial, caps growth), `MaximumAttempts` (default
  unlimited), `NonRetryableErrorTypes` (empty by default). (Source: docs.temporal.io/encyclopedia/retry-policies.)
- Activities monitored via **Heartbeats**: a periodic worker→server ping; missing a
  `HeartbeatTimeout` window marks the activity failed and reschedulable. Other timeout types:
  Schedule-To-Close, Start-To-Close, Schedule-To-Start. (Source:
  docs.temporal.io/encyclopedia/detecting-activity-failures.)
- Worker failover: the server doesn't directly detect a crashed worker — it relies on
  Start-To-Close timeout expiry or missed heartbeats, after which the task is rescheduled onto the
  task queue and **any** available worker can pick it up. A new worker replays the event history
  to reconstruct state (sticky-queue mechanism, 5s default stickiness-disable window). (Source:
  docs.temporal.io/sticky-execution.)

Sources fetched: docs.temporal.io/{encyclopedia/retry-policies,encyclopedia/detecting-activity-failures,
develop/python/activities/timeouts,sticky-execution}.

---

## 11. Ray (analogy only — actor/task retry, not LLM-specific)

- `max_restarts` on an actor: max restarts of a crashed actor; default 0 (no restart); `-1` =
  unlimited. `max_task_retries`: if an in-flight call fails, Ray retries the task up to this many
  times, bounded jointly by `max_restarts` (e.g. `max_task_retries=5` + `max_restarts=2` → up to 6
  total attempts across 2 crashes). `retry_exceptions=True` additionally retries on user-raised
  exceptions (recommended only for idempotent methods). (Source: docs.ray.io/en/latest/ray-core/fault_tolerance/actors.html.)
- Ray Serve: if a node hosting a replica crashes, Ray restarts that actor on another node; other
  healthy replicas keep serving during recovery. (Source: docs.ray.io/.../serve/production-guide/fault-tolerance.html.)
- Ray Train: on worker/node failure, Train shuts down all workers, provisions replacements if
  needed, restarts the full worker group, and resumes each worker from the latest checkpoint.
  (Source: docs.ray.io/.../train/user-guides/fault-tolerance.html.)

Sources fetched: docs.ray.io/en/latest/{ray-core/fault_tolerance/actors,serve/production-guide/fault-tolerance,
train/user-guides/fault-tolerance}.html.

---

## Cross-cutting findings

1. **Retry (same model, backoff) and failover (switch model/provider) are treated as two
   separate primitives almost everywhere, and only LiteLLM, AG2, and OpenRouter unify them into
   one first-class list.** LangGraph splits them across two libraries (`RetryPolicy` in
   langgraph vs. `.with_fallbacks()` in langchain-core); OpenAI Agents SDK has a rich retry
   subsystem (`ModelRetrySettings`, 7 named policy helpers) but **no fallback-to-different-model
   concept at all**, confirmed at the source level; CrewAI's native retry is same-model-only,
   with cross-model failover pushed out to LiteLLM or a third-party gateway; Claude Code's
   `--fallback-model` and its retry-with-backoff are two distinct mechanisms with different
   trigger conditions (fallback explicitly excludes rate-limit errors, retry handles them).

2. **"Different model per role" is near-universal as a raw capability (a string or object field
   on the agent), but a *named*, multi-model pattern with its own vocabulary is rare.** Only
   aider (main/editor/weak triad, tied to Architect mode) and CrewAI (`manager_llm` +
   `Process.hierarchical`) have an officially named pattern. LangGraph and OpenAI Agents SDK
   document the "cheap triage model + expensive specialist model" idea only as prose
   guidance/example code, not as an API-level abstraction with its own name. AG2, Microsoft
   AutoGen, Claude Code, and opencode have no named combination pattern at all — just a
   per-agent field.

3. **Router/gateway layers (LiteLLM, OpenRouter) carry by far the most-developed failover
   vocabulary of anything surveyed, and multiple frameworks explicitly delegate cross-model
   failover to them rather than building it natively** (CrewAI → LiteLLM/Portkey; implicitly,
   any framework whose model string is a LiteLLM-style `provider/model` identifier inherits
   LiteLLM's routing options if the user chooses to run it through LiteLLM's Router/proxy). This
   suggests the industry pattern is: agent framework owns *which agent gets which model
   assignment*, router layer owns *what happens when a model call fails*.

4. **Where a fallback list exists, "first item, in order, until one succeeds" is the dominant
   shape** (AG2's `LLMConfig` list, LiteLLM's `fallbacks` map, OpenRouter's `models` array,
   Claude Code's `fallbackModel` chain capped at 3). The variation is in what triggers a step to
   the next item: LiteLLM and OpenRouter allow error-class-specific fallback lists (context-window
   vs. content-policy vs. general); Claude Code explicitly excludes whole classes of error
   (rate-limit, auth, billing) from triggering its fallback chain; AG2's trigger condition
   ("if the model fails") is not specified down to exception type in the fetched docs.

5. **Conceptual cost to enable full model-choice + failover is consistently multi-concept and
   rarely singular, but the size varies by an order of magnitude.** Cheapest observed: AG2's
   fallback (reuse the same list object you already built for per-agent config — ~0 marginal
   concepts). Most expensive observed: LiteLLM's full DSL (alias/concrete split, `order`, 4
   separate fallback-list types, 5-value routing-strategy enum with a Redis-dependent option, a
   per-exception-type `RetryPolicy`, and a separate cooldown/`allowed_fails` window) and OpenAI
   Agents SDK's retry-only subsystem (~5-6 new types for retry alone, with zero fallback
   capability delivered for that cost). Frameworks with a CLI/config-file surface (aider, Claude
   Code, opencode) tend toward flatter, fewer-concept surfaces than pure-Python
   library/router layers (LangGraph, OpenAI Agents SDK, LiteLLM).

---

### All sources (deduplicated)

LangGraph: github.com/langchain-ai/langgraph-supervisor-py; langgraph `types.py` (raw);
reference.langchain.com/python/langgraph/types/RetryPolicy; langchain.com/blog/fault-tolerance-in-langgraph;
docs.langchain.com/oss/python/langchain/{overview,models}; reference.langchain.com RunnableWithFallbacks;
langchain-ai/langchain `how_to/fallbacks.ipynb`.

OpenAI Agents SDK/Swarm: openai.github.io/openai-agents-python/{agents,models,ref/model_settings};
GitHub raw `README.md`, `src/agents/model_settings.py`, `src/agents/retry.py`, `docs/multi_agent.md`
(openai/openai-agents-python); github.com/openai/swarm README.

CrewAI: docs.crewai.com/en/{concepts/agents,concepts/llms,learn/hierarchical-process,
observability/portkey}; github.com/crewAIInc/crewAI/issues/4262.

AG2/AutoGen: docs.ag2.ai/latest/docs/user-guide/{basic-concepts/llm-configuration,
advanced-concepts/llm-configuration-deep-dive}/; microsoft.github.io/autogen/0.2/docs/topics/llm_configuration/;
microsoft.github.io/autogen/stable/.../model-clients.html; github.com/microsoft/agent-framework#2687;
learn.microsoft.com/en-us/agent-framework/agents/middleware/exception-handling; dev.to/maximsaplin;
gettingstarted.ai/autogen-vs-ag2.

Claude Code: code.claude.com/docs/en/{sub-agents,errors,model-config,cli-reference}.

aider: aider.chat/docs/config/{adv-model-settings,options,aider_conf}.html.

opencode: opencode.ai/docs/{agents,config,models}/.

LiteLLM: docs.litellm.ai/docs/{routing,proxy/reliability}.

OpenRouter: openrouter.ai/docs/{features/model-routing,guides/routing/model-fallbacks,
guides/routing/provider-selection}.

Temporal: docs.temporal.io/{encyclopedia/retry-policies,encyclopedia/detecting-activity-failures,
develop/python/activities/timeouts,sticky-execution}.

Ray: docs.ray.io/en/latest/{ray-core/fault_tolerance/actors,serve/production-guide/fault-tolerance,
train/user-guides/fault-tolerance}.html.
