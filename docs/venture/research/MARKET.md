# The agent-orchestration market, mid-2026

Research date: 2026-07-14. Every claim tagged VERIFIED (fetched primary source directly), DOCUMENTED (credible secondary reporting, primary not independently fetched), or REASONED (inference/synthesis, explicitly labeled). Spot-check note: 4 of the highest-leverage claims below (LangSmith Plus pricing, Cognition's May 2026 raise, the arXiv 2604.02460 paper, Temporal's Series D) were independently re-fetched from source during synthesis and matched exactly.

---

## 1. Who charges what, for what

**Headline finding: nobody sells orchestration logic itself. Every pure-orchestration framework in this list (LangChain/LangGraph, CrewAI's core, AutoGen, Microsoft Agent Framework, the OpenAI Agents SDK) is free and open-source (MIT or equivalent). The money is in three other layers: model tokens, managed hosting/runtime, and observability/ops tooling. Coding-agent products (Devin, Factory, Claude Code) sell a bundled subscription + compute-credit *experience*, not a licensable orchestration algorithm.**

### LangChain / LangGraph / LangSmith
- LangChain and LangGraph (the orchestration libraries) are free OSS; money flows through LangSmith (observability/deployment platform) — REASONED — https://www.langchain.com/pricing
- LangSmith tiers: Developer $0/seat/mo (1 seat, 5k traces/mo free), Plus $39/seat/mo (10k traces/mo free), Enterprise custom — VERIFIED — https://www.langchain.com/pricing
- Trace pricing billed separately from seats: base traces (14-day retention) $2.50/1k, extended traces (400-day) $5.00/1k — VERIFIED — https://www.langchain.com/pricing
- LangSmith "Engine" (automated trace-analysis/agent-ops product) metered in LCUs at $1.50/LCU — VERIFIED — https://www.langchain.com/pricing
- LangGraph Platform (hosted deployment) bills per deployment run ($0.005/run) plus per-minute compute ($0.0036/min prod, $0.0007/min dev); ~1M nodes executed on Plus ≈ $1,000 — VERIFIED/DOCUMENTED — https://www.langchain.com/pricing, https://www.zenml.io/blog/langgraph-pricing
- "Unlimited agents" stated on every LangGraph Platform tier — no multi-agent surcharge, except that separately-deployed agents calling each other bill to the called deployment — VERIFIED — https://www.langchain.com/pricing-langgraph-platform

### CrewAI (incl. Enterprise)
- Core framework (open-source Python) free; CrewAI charges via hosted platform CrewAI AMP / CrewAI Enterprise — REASONED — https://crewai.com/pricing
- Two published tiers: Basic ($0/mo, 50 workflow executions/mo) and Enterprise (custom, contact sales) — VERIFIED — https://crewai.com/pricing
- Enterprise adds hosted-or-private infra, VPC/NAT, security certs (SAM, FedRAMP High), 50 dev-hours/mo, SSO/RBAC — VERIFIED — https://crewai.com/pricing
- Third-party estimate: Enterprise contracts run ~$60K–$120K/year (no official rate card) — DOCUMENTED — https://techjacksolutions.com/ai-tools/crewai/crewai-pricing/
- CrewAI requires customers to bring their own LLM API keys — token cost is pass-through, not metered by CrewAI — DOCUMENTED — https://www.lindy.ai/blog/crew-ai-pricing
- No differentiation by agent/crew count in pricing — REASONED — https://crewai.com/pricing

### Temporal Cloud
- Open-source Temporal server/SDKs (durable-execution orchestration) are free; Temporal Cloud is a paid, consumption-based managed service — VERIFIED — https://temporal.io/pricing
- Billed on two metrics: Actions and Storage. Essentials: greater of $100/mo or 5% of usage spend, incl. 1M Actions. Business: $500/mo floor, 2.5M Actions, SAML SSO. Enterprise/Mission Critical: custom, 10M Actions, 24/7 <30min or <15min SLA — VERIFIED — https://docs.temporal.io/cloud/pricing
- No separate "observability" SKU — bundled into Actions+Storage+support — REASONED — https://docs.temporal.io/cloud/pricing
- Not agent-orchestration-native by origin, but reframed as "the plumbing beneath every agent" by 2026 press and its own Series D language — DOCUMENTED — https://theagenttimes.com/articles/temporal-raises-300m-series-d-the-plumbing-beneath-every-agent-just-got-a-5b-price-tag

### OpenAI (Agents SDK / AgentKit)
- Agents SDK is open-source, free; AgentKit tools (Agent Builder, ChatKit, Connector Registry, Evals) are "included with standard API model pricing" — no separate platform fee — VERIFIED — https://openai.com/index/introducing-agentkit/
- Money is 100% token consumption + hosted-tool metering: Code Interpreter $0.03–$1.92/20-min session by container size; File Search $0.10/GB/day + $2.50/1k calls; Web Search $10–$25/1k calls — VERIFIED — https://developers.openai.com/api/docs/pricing
- OpenAI announced deprecation of Agent Builder and Evals, both leaving the platform 2026-11-30 — DOCUMENTED — https://mcp.directory/blog/openai-agentkit-deprecation-2026
- No orchestration-logic charge (handoffs, guardrails, tracing UI) — monetized entirely via tokens/tools — REASONED — https://openai.com/index/introducing-agentkit/

### Anthropic (Claude Code, subagents, Agent SDK)
- Subscription plans (Free/Pro $20mo/Max $100+/Team/Enterprise) AND pay-per-token API access, stackable — VERIFIED — https://claude.com/pricing
- No separate charge for "subagents" as a feature — billed only via underlying token/session usage of whichever plan runs it — REASONED (no subagent SKU found) — https://claude.com/pricing
- Claude Agent SDK (the library) carries no separate license fee — ordinary API/subscription consumption — REASONED — https://platform.claude.com/docs/en/about-claude/pricing
- "Claude Managed Agents" hosted product bills tokens PLUS session runtime at $0.08/session-hour — VERIFIED — https://platform.claude.com/docs/en/about-claude/pricing
- Anthropic proposed (then paused, not implemented as of research date) carving Agent SDK/headless usage into a separate credit pool from subscriptions, June 2026 — DOCUMENTED — https://thenewstack.io/anthropic-agent-sdk-credits/, https://devops.com/anthropic-hits-pause-on-claude-agent-sdk-billing-change-for-now/

### Microsoft (AutoGen / Agent Framework)
- AutoGen (MIT) and its successor Microsoft Agent Framework (MIT, unifies AutoGen + Semantic Kernel, ~Oct 2025) are both free OSS — VERIFIED — https://github.com/microsoft/autogen, https://github.com/microsoft/agent-framework
- Microsoft earns no direct license revenue from the frameworks — REASONED — https://github.com/microsoft/agent-framework
- Money is (1) underlying LLM API calls, (2) optional Microsoft Foundry Agent Service hosted-agent infra (Azure-managed, scaling/persistence/observability), pricing deferred to a separate doc as of mid-2026 — REASONED/VERIFIED(feature) — https://learn.microsoft.com/en-us/agent-framework/hosting/foundry-hosted-agent
- Foundry Agent Service pricing "remains based on consumption of underlying services rather than on the number of agents deployed," despite marketing multi-agent as a headline use case — DOCUMENTED — https://azure.microsoft.com/en-us/pricing/details/foundry-agent-service/
- Multi-agent debate/reflection loop patterns can multiply token spend 3–5x vs single-agent calls if rounds aren't capped — DOCUMENTED (practitioner estimate) — https://www.secondtalent.com/resources/how-enterprises-are-using-autogen/

### Devin / Cognition
- Charges subscription + usage-based ACU (Agent Compute Unit) consumption — not free — VERIFIED — https://devin.ai/pricing
- Individual: Free $0, Pro $20/mo, Max $200/mo. Teams: $80/mo base + $40/mo per full seat. Enterprise: custom, ACU rate "set in their order form" — VERIFIED — https://devin.ai/pricing, https://docs.devin.ai/admin/billing
- 1 ACU ≈ ~15 min of active autonomous work (concept corroborated by multiple secondary sources, exact wording not on an official page) — DOCUMENTED — https://www.eesel.ai/blog/cognition-ai-pricing
- April 2025: Cognition cut self-serve pricing from a $500/mo-minimum enterprise-only model to $20/mo pay-as-you-go with $2.25/ACU — DOCUMENTED — https://venturebeat.com/programming-development/devin-2-0-is-here-cognition-slashes-price-of-ai-software-engineer-to-20-per-month-from-500
- Devin charges for the agent product itself (subscription + metered agent sessions), not a separate hosting/observability SKU — REASONED — https://devin.ai/pricing
- Architecturally single-agent — excluded from multi-agent pricing comparisons — REASONED — https://docs.devin.ai/admin/billing

### Factory (factory.ai / Droid)
- Charges subscription (Pro $20, Plus $100, Max $200/mo) plus optional prepaid usage credits — not free — VERIFIED — https://factory.ai/pricing
- Plus tier adds "Droid Computers" (Factory-managed cloud compute for remote/background agents) — a distinct compute-hosting layer billed alongside the subscription — VERIFIED — https://factory.ai/pricing
- Sessions consume "Factory Standard Credits" (model usage) plus separate Droid Computers compute charges — both an agent-usage layer and a hosting-passthrough layer are billed — VERIFIED — https://docs.factory.ai/pricing
- Business/Enterprise add SSO, ZDR, on-prem deployment, dedicated compute — VERIFIED — https://docs.factory.ai/pricing

### Answer to the analytical question
No one successfully charges for orchestration logic as such. Every pure-orchestration framework (LangChain, LangGraph, CrewAI core, AutoGen, MS Agent Framework, OpenAI Agents SDK) is free/OSS, explicit that the graph/workflow-definition layer carries no license fee. Money clusters in: (1) **model tokens** — sold directly (Anthropic, OpenAI) or passed through (CrewAI, LangGraph Platform, Temporal customers' own LLM bills); (2) **managed hosting/runtime at scale** — LangGraph Platform's per-run/per-minute fees, Temporal Cloud's Actions+Storage, Foundry Agent Service, Factory's Droid Computers, Devin's ACU-metered sessions — structurally identical to any cloud-compute business, and the clearest real recurring-revenue layer; (3) **observability/ops tooling** — LangSmith is the one case reading as genuine software margin rather than compute resale, though still priced on trace volume, not "the orchestration" per se. Coding-agent products (Devin, Factory, Claude Code) blur categories deliberately: flat subscription + usage credits, selling the *agent product experience* (autonomy, UI, support), not a licensable orchestration algorithm.

---

## 2. Funding, 2024–2026

### Pure orchestration/infra layer
- **LangChain**: $10M seed (Benchmark, Apr 2023) → $25M Series A (Sequoia, Feb 2024, ~$200M valuation) → **$125M Series B (IVP, Oct 2025, $1.25B valuation)**. Series B growth stats: 35% of Fortune 500 use it, trace volume up 12x YoY — VERIFIED — https://www.langchain.com/blog/series-b
- **CrewAI**: $2M inception (boldstart) + Series A → **$18M combined (Insight Partners, Oct 2024)**. Insight's thesis: "AI multi-agent platforms" are the catalyst for enterprise LLM ROI. 10M+ agents executed/month claimed — VERIFIED — https://www.insightpartners.com/ideas/crewai-launches-multi-agentic-platform-to-deliver-on-the-promise-of-generative-ai-for-enterprise/
- **Temporal**: $100M Series B (Index, 2022, $1.5B) → $75M Series B-Prime (Greenoaks, 2023) → **$146M Series C (Tiger Global, Mar 2025, $1.72B)**, explicitly "to Fuel Durable, Production Agentic Workloads" → $105M secondary (GIC, Oct 2025, $2.5B) → **$300M Series D (a16z, Feb 2026, $5B)** — VERIFIED — https://temporal.io/blog/temporal-raises-usd300m-series-d-at-a-usd5b-valuation
- **/dev/agents**: $56M seed (Index/CapitalG, Nov 2024, $500M valuation) — ex-Stripe/Android leadership team, thesis: "OS for trusted AI agents," monetization via transaction fees/subscriptions — DOCUMENTED — https://techcrunch.com/2024/11/28/ai-agent-startup-dev-agents-has-raised-a-massive-56m-seed-round-at-a-500m-valuation/

### Coding agents
- **Cognition (Devin)**: $21M Series A (Founders Fund, Mar 2024, $350M) → $175M (Apr 2024, $2B) → "hundreds of millions" (8VC, Mar 2025, $4B) → $400M (Founders Fund, Sep 2025, $10.2B; ARR $73M Jun 2025, up from $1M Sep 2024) → **>$1B (Lux/General Catalyst/8VC, May 2026, $25B pre-money); $492M annualized revenue run-rate cited, customers Mercedes-Benz/NASA/Goldman Sachs/Santander** — DOCUMENTED — https://techcrunch.com/2026/05/27/ai-coding-startup-cognition-raises-1b-at-25b-pre-money-valuation/
- **Factory**: $5M seed (Sequoia/Lux, Nov 2023) → $15M Series A ($120M, Jun 2024) → $50M Series B (NEA/Sequoia/JPM/Nvidia, Sep 2025, $300M) → **$150M Series C (Khosla, Apr 2026, $1.5B)** — VERIFIED — https://techcrunch.com/2026/04/16/factory-hits-1-5b-valuation-to-build-ai-coding-for-enterprises/

### Vertical agent products (customer support etc.)
- **Sierra** (Bret Taylor): $110M (Sequoia/Benchmark, Feb 2024, ~$1B) → $175M (Greenoaks, Oct 2024, $4.5B) → $350M (Greenoaks, Sep 2025, $10B) → **$950M Series E (Tiger Global/GV, May 2026, >$15B); $150M ARR by Feb 2026, 40%+ of Fortune 50 as customers** — VERIFIED — https://techcrunch.com/2026/05/04/sierras-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/
- **Decagon**: $5M seed + $30M Series A (Accel, Jun 2024, $35M combined) → $65M Series B (Bain, Oct 2024, $650M, $100M total) → $131M Series C (Accel/a16z, Jun 2025, $1.5B) → **$250M Series D (Coatue/Index, Jan 2026, $4.5B — tripled in <6 months)** — VERIFIED — https://decagon.ai/blog/series-d-announcement
- **Parahelp**: $3.2M seed + $18M Series A (Jack Altman/Alt Capital, Sep 2025, $21.2M combined) — customers Perplexity, Replit, HeyGen, "0% churn" claimed — VERIFIED — https://parahelp.com/blog/announcing-our-series-a-and-seed

### Agent tooling/observability adjacents
- **Arize AI**: $70M Series C (Adams Street, Feb 2025) — "largest-ever investment in AI observability," $131M total — VERIFIED — https://arize.com/blog/arize-ai-raises-70m-series-c-to-build-the-gold-standard-for-ai-evaluation-observability/
- **Braintrust**: $36M Series A (a16z, Oct 2024, $150M) → **$80M Series B (ICONIQ, Feb 2026, $800M)** — VERIFIED — https://www.braintrust.dev/blog/announcing-series-b
- **Galileo AI**: $45M Series B (Scale VP, Oct 2024, $68M total), 834% revenue growth cited — VERIFIED — https://galileo.ai/blog/announcing-our-series-b
- **Langfuse**: $4M seed (Lightspeed, Nov 2023) — no Series A found; **acquired by ClickHouse, Jan 2026** — VERIFIED/DOCUMENTED — https://langfuse.com/blog/announcing-our-seed-round, https://langfuse.com/press/press
- **Browserbase**: $6.5M seed (2024) → $21M Series A → $40M Series B (Notable, Jun 2025, ~$300M, $67.5M total) — DOCUMENTED — https://siliconangle.com/2025/06/17/browserbase-reels-40m-browser-automation-tools/
- **E2B**: $11.5M seed (Oct 2024) → $21M Series A (Insight, Jul 2025, $32-35M total) — "88% of Fortune 100 already signed up" claimed — VERIFIED — https://e2b.dev/blog/series-a

### Failed/absorbed before reaching maturity (see graveyard for detail)
- **Adept**: $65M Series A (2022) → $350M Series B (Mar 2023, ~$1B, $415M total) → Amazon reverse-acquihire Jun 2024 — DOCUMENTED — https://techcrunch.com/2023/03/15/adept-a-startup-training-ai-to-use-existing-software-and-apis-raises-350m/
- **MultiOn**: undisclosed seed → $20M Series A (Jun 2024, $100M) — did not die, pivoted twice (Windows agent → web agent → consumer mobile "AGI-0") — DOCUMENTED — https://synthedia.substack.com/p/multions-nine-figure-valuation-highlights
- **Imbue**: $200M+ Series B (Astera/Nvidia, Sep 2023, >$1B) — still independent as of Apr 2026 — VERIFIED — https://imbue.com/blog/introducing-imbue

### The thesis pattern across all rounds
Every 2025-2026 round in this list, regardless of layer, cites the same underlying justification in its own words: agents are easy to demo, hard to run reliably/durably/observably in production, and the round funds closing that gap — "durability" (Temporal), "trace volume/production trust" (LangChain, Braintrust, Galileo, Arize), "scaled enterprise reliability" (Sierra, Decagon, Cognition). This is REASONED synthesis across the VERIFIED thesis quotes above, not a single source.

---

## 3. The graveyard: who died, pivoted, or got absorbed, and why

- **Adept AI**: $415M raised, ~$1B valuation (Mar 2023) → June 2024 Amazon hired CEO David Luan + most co-founders/researchers ("reverse acquihire") and licensed the tech; investors bought out (~$25M routed through licensing); FTC opened informal inquiry into whether this dodged merger review — DOCUMENTED — https://www.cnbc.com/2024/06/28/amazon-hires-execs-from-ai-startup-adept-and-licenses-its-technology.html, https://www.semafor.com/article/08/02/2024/investors-in-adept-ai-will-be-paid-back-after-amazon-hires-startups-top-talent
  - Luan's own reasoning: continuing to build frontier foundation models AND an enterprise agent product would force Adept into an endless compute-fundraising treadmill it couldn't win standalone — DOCUMENTED — https://www.thetwentyminutevc.com/david-luan
  - By 2026: ~4 people left at Adept per LinkedIn; Luan himself left Amazon's AGI Lab Feb 2026; 4 of 5 co-founders who joined Amazon have since left entirely — DOCUMENTED — https://www.geekwire.com/2026/head-of-amazons-agi-lab-is-leaving-in-latest-exit-from-high-profile-adept-deal/

- **MultiOn**: did NOT die — pivoted from web-automation agent to consumer mobile app "AGI-0," its second pivot (originally a Windows desktop agent) — DOCUMENTED — https://aiindigo.com/blog/multion-2026-review-the-agi-0-mobile-app-redefines-personal-automation

- **AutoGPT**: went viral 2023 (100K+ GitHub stars), but a 2023 Amazon benchmark found it completed only ~24% of shopping tasks, with a recurring circular-tool-call failure mode — DOCUMENTED — https://www.bairesdev.com/blog/the-rise-of-autonomous-agents-autogpt-agentgpt-and-babyagi/, https://github.com/vectara/awesome-agent-failures/blob/main/docs/case-studies/autogpt-planning-failures.md
  - The project did NOT die: rewrote into a visual-workflow-builder commercial platform (autogpt.net), ~185K stars, still shipping (v0.6.59, May 2026) — but the original "fully local, fully autonomous" mode is unmaintained/broken by 2026, and AutoGen/CrewAI have "largely eclipsed" its original autonomous-loop use case — DOCUMENTED — https://vibeagentmaking.com/blog/autogpt-got-100k-stars-and-then-what/, https://www.promptquorum.com/power-local-llm/autonomous-local-agents-actually-work

- **BabyAGI**: original <200-line script (Mar 2023) inspired AutoGPT/AgentGPT/AutoGen — but the repo was frozen and moved to a `babyagi_archive` repo, Sept 2024; author Nakajima explicitly says it was "not meant for production use" and moved on to smaller successor experiments — DOCUMENTED/VERIFIED — https://github.com/yoheinakajima/babyagi_archive

- **AgentGPT / Reworkd**: launched Apr 2023 (YC S23), feature development stopped Nov 2023; raised $4M Jul 2024 and explicitly pivoted from general autonomous agents to structured web-scraping, reasoning "general AI agents was too broad" — DOCUMENTED — (search synthesis, corroborated across outlets). Repo archived 2026-01-28, 130+ unanswered issues — DOCUMENTED — https://github.com/reworkd/AgentGPT

- **Inflection AI**: raised $1.3B+ for consumer chatbot Pi → March 2024 Microsoft hired most staff incl. co-founders Suleyman/Simonyan via $650M licensing deal (not acquisition); Suleyman told Bloomberg Inflection "had not found an effective business model" for Pi — DOCUMENTED — https://finance.yahoo.com/news/inflection-ai-plans-pivot-most-214440697.html, https://www.forbes.com/sites/alexkonrad/2024/03/19/inflection-abandons-chatgpt-challenger-ceo-suleyman-joins-microsoft/

- **Same reverse-acquihire pattern, non-agent-framework but structurally identical**: Character.AI/Google ($2.7B licensing, Aug 2024, DOJ scrutiny) and Windsurf/Google ($2.4B licensing, Jul 2025, derailed a prior $3B OpenAI acquisition; the remaining Windsurf entity then bought outright by Cognition) — DOCUMENTED — https://www.pymnts.com/artificial-intelligence-2/2024/google-reportedly-spent-2-7-billion-to-rehire-character-ai-founder/, https://www.cnbc.com/2025/07/11/google-windsurf-ceo-varun-mohan-latest-ai-talent-deal-.html

- **SuperAGI**: open-source framework stalled (no releases since Jan 2024, unaddressed vulnerabilities) while the company pivoted from "marketing platform" to broader enterprise "agentic AI platform," Jul 2025 — DOCUMENTED (search synthesis)

- **Hardware-agent adjacents** (execution failures, not agent-tech failures): Humane AI Pin — panned on launch, HP bought assets for $116M (down from ~$1B rumored valuation), servers killed Feb 28, 2025 — VERIFIED — https://techcrunch.com/2025/02/18/humanes-ai-pin-is-dead-as-hp-buys-startups-assets-for-116m/. Rabbit r1 — sold ~100K units, mass returns, employees unpaid since Jul 2025, not formally dead as of research but "zombie" status — DOCUMENTED — https://www.tomsguide.com/ai/whats-next-for-rabbit-employees-say-they-havent-been-paid-for-months-while-company-teases-new-ai-hardware

- **Aggregate**: ~3,800 AI startups shut down in 2025 (methodology unclear, directional only), another ~1,800 in early 2026 — DOCUMENTED — https://techstartups.com/2025/12/09/top-ai-startups-that-shut-down-in-2025-what-founders-can-learn/. Reverse-acquihire (licensing fee + key-talent hire, no formal M&A) became the standard exit shape for agent/model startups specifically to avoid FTC/DOJ merger review — DOCUMENTED (pattern across Adept, Inflection, Character.AI, Windsurf) — https://www.heavybit.com/library/article/the-acqui-hire-is-no-longer-a-distress-sale

### Synthesis: common causes of death/pivot (REASONED)
1. **Foundation-model absorption** — once frontier labs shipped native agentic/computer-use capability, startups betting on "we build the agent model" (Adept) lost their standalone reason to exist; the capability got commoditized into the base model layer.
2. **Hype without a business model** — AutoGPT/BabyAGI/AgentGPT achieved massive attention in 2023 with no paying-customer product behind the autonomous loop; real-world benchmarks (24% task success) exposed the gap, and each either archived, pivoted to a narrower commercial wrapper, or was outpaced by newer frameworks.
3. **Compute-cost asymmetry forced consolidation** — the reverse-acquihire (licensing fee + talent hire, no/minimal equity) became standard because continuing to compete on frontier compute was unaffordable standalone, while it let big labs acquire talent/tech while sidestepping formal antitrust review.
4. **Consumer-hardware "agent in a device" bets failed on execution, not agent-tech** — Humane and Rabbit's failures were reliability/latency/battery/demo-vs-reality problems, not evidence against the underlying agent loop.
5. **Narrow vertical framing survives; general-purpose framing dies** — the survivors (Sierra, Cognition, Decagon) each picked one high-value enterprise workflow and sold it as SaaS with clear ROI; "general autonomous agent" framing correlates with death, narrow vertical-agent framing correlates with survival and continued fundraising.

---

## 4. Multi-agent: premium product or bundled feature?

**Verdict: bundled feature, not a premium product, as of mid-2026.**

### Pricing evidence
- Across 11 major platforms checked (LangGraph Platform, CrewAI, Microsoft Foundry Agent Service, AWS Bedrock Agents/AgentCore, OpenAI Agents SDK, Google Vertex AI Agent Builder/ADK, Salesforce Agentforce, Relevance AI, n8n, Dust.tt, Devin), only **one** — Dust.tt — structurally prices multi-agent higher, via cumulative sub-agent credit stacking — VERIFIED — https://docs.dust.tt/docs/credits
- The other 10 price on agent-count-agnostic consumption units (tokens, executions, vCPU-hours, conversations): LangGraph states "unlimited agents" on every tier — VERIFIED — https://www.langchain.com/pricing-langgraph-platform; AWS Bedrock's multi-agent collaboration docs contain zero pricing language — VERIFIED — https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html; Microsoft Foundry explicitly states pricing is based on "consumption of underlying services rather than on the number of agents deployed" despite marketing multi-agent as a headline use case — DOCUMENTED — https://azure.microsoft.com/en-us/pricing/details/foundry-agent-service/

### Case-study evidence
- Zero named CIO/buyer quotes found, across LangGraph/CrewAI/Azure/Bedrock/Agentforce/Anthropic/OpenAI case studies, stating they *selected or paid for* a vendor specifically because of multi-agent coordination — what exists is deployment/outcome testimony, not procurement rationale — REASONED (synthesis) 
- Two positive counter-signals: JM Family Enterprises credits "multi-agent architecture" for productivity gains (60% QA time saved) on Azure — VERIFIED — https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/building-a-digital-workforce-with-multi-agents-in-azure-ai-foundry-agent-service/4414671; Netcore Cloud calls multi-agent architecture "a key differentiator" on AWS — VERIFIED — https://aws.amazon.com/solutions/case-studies/netcore-bedrock-case-study/. Both are deployment testimonials, not purchase-decision statements.
- CrewAI's own 2026 buyer survey — the leading dedicated multi-agent vendor's own market research — ranks security/governance (34%), integration ease (30%), and reliability (24%) above multi-agent coordination as enterprise selection criteria — DOCUMENTED — https://www.digitalcommerce360.com/2026/02/11/survey-enterprises-ai-agents-crewai-report/
- The widely-cited OpenAI/Klarna "700 agents" story describes a single AI assistant, not multi-agent architecture, in OpenAI's own telling — DOCUMENTED (negative finding) — https://openai.com/index/klarna/

### Adoption/analyst evidence
- Gartner: 89% of AI agent pilots fail to reach production; surviving 11% deliver 171% ROI (no single-vs-multi breakout) — DOCUMENTED — https://www.beri.net/article/ai-agent-adoption-enterprise-2026-gartner-idc
- Gartner: only ~130 of "thousands" of vendors marketing agentic AI are genuinely agentic — rest is "agent-washing" — DOCUMENTED — https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025
- McKinsey: ~2/3 of enterprises have experimented with agents, fewer than 10% have scaled any to deliver tangible value — DOCUMENTED — https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/tech-forward/state-of-ai-trust-in-2026-shifting-to-the-agentic-era
- "22% of production deployments now coordinate three or more agents" — repeated across secondary aggregators (attributed to Forrester/BCG), primary not directly located — DOCUMENTED — https://www.digitalapplied.com/blog/ai-agent-adoption-2026-enterprise-data-points
- **Anthropic's own engineering blog**: their multi-agent Research system beat single-agent Opus 4 by 90.2% but consumed ~15x the tokens; multi-agent economics "only work for high-value research" — a vendor-side admission that multi-agent is a narrow tool, not a general product — VERIFIED — https://www.anthropic.com/engineering/multi-agent-research-system
- **Stanford/Contextual AI, arXiv 2604.02460 (Apr 2026, independently re-verified during this research)**: under equal reasoning-token budgets, single-agent systems consistently match or outperform multi-agent systems on multi-hop reasoning; many reported multi-agent advantages trace to uncontrolled extra compute (specifically flagged artifacts in Gemini 2.5 budget control) rather than architectural benefit — VERIFIED — https://arxiv.org/abs/2604.02460
- Countervailing data point: AORCHESTRA (arXiv 2602.03786) reports +16.28% improvement over the strongest single-agent baseline on GAIA/SWE-Bench/Terminal-Bench with an orchestrator+subagent topology — multi-agent can win on specific agentic-tool-use benchmarks — DOCUMENTED — https://arxiv.org/abs/2602.03786
- Industry has converged on orchestrator + ephemeral isolated-subagent topology (Anthropic, OpenAI, Cognition, Microsoft/AutoGen, LangChain), not peer-to-peer multi-agent collaboration; five competing topologies (fan-out, pipeline, debate, supervisor, swarm) still coexist with no dominant standard — DOCUMENTED — https://www.flowhunt.io/blog/multi-agent-ai-system/, https://www.totalum.app/blog/ai-agent-orchestrator-totalum-2026

### Verdict, stated plainly (REASONED)
Multi-agent is not a separately monetizable product category as of mid-2026 — it's an architectural choice made inside a platform that is priced the same regardless. Where real pricing premiums *do* attach in this market, they're on governance, observability, and compliance tooling layered on top of agent platforms — not on the number of agents coordinating. The one vendor most invested in the multi-agent thesis (CrewAI) finds in its own survey data that its customers rank security and reliability above multi-agent capability. The strongest technical evidence (Anthropic's own cost admission, the Stanford/Contextual paper) says multi-agent buys real capability only at 10-15x token cost, for a narrow set of high-value, high-complexity workloads — which is consistent with "feature for specific hard problems," not "product with its own demand curve."

---

## Sources and methodology note
Research conducted 2026-07-14 by four parallel research agents (mkt-pricing, mkt-funding, mkt-graveyard, mkt-multiagent), each further subdividing into parallel sub-research threads. Synthesizer (vent-market) independently re-fetched 4 load-bearing claims (LangSmith Plus pricing, Cognition's May 2026 raise/ARR, arXiv 2604.02460's existence and claims, Temporal's Series D) and found exact agreement with the source material — no corrections were needed to the underlying research.
