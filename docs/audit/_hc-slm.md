# Small function-calling models: verification and prior art (evidence only)

Prepared by agent hc-slm (with children hc-slm-cactus, hc-slm-class, hc-slm-priorart) for harness-contractor. Bounded factual research per brief — no design or placement rulings; those belong to the parent. Every claim in the three parts below is tagged DOCUMENTED (with URL) or KNOWLEDGE (training memory, may be stale).

## 10-line summary

1. Cactus and Needle are both real: Cactus Compute, Inc. makes "Cactus," an on-device/edge inference engine (mobile/wearable, OpenAI-compatible local HTTP server, custom tiered-free proprietary license); "Needle" is their 26M-param function-calling model built for it (MIT license, JSON-schema tool I/O).
2. But "a tree-of-agents system" is **not** a supported characterization of Cactus/Needle — no source describes multi-agent orchestration in either project; that framing appears unsourced and should not be inherited as fact.
3. Needle's context window is undocumented anywhere checked; several numeric claims (star counts, "Gemini 3.1" distillation source) are flagged low-confidence rather than asserted.
4. The broader small-function-calling-model class is real and active: Gorilla/OpenFunctions, Salesforce xLAM (1B–70B ladder), Hammer (0.5B–7B), Octopus-v2 (2B), Phi-4-mini (not Phi-3), small Qwen2.5/Qwen3, Gemini Nano (I/O 2026), and Apple's ~3B on-device model with "constrained tool calling" all document real function-calling support.
5. Reliability numbers exist but are scattered and largely vendor/paper-self-reported (e.g. Octopus-v2 99.5% on its own narrow Android benchmark; xLAM-7b 88.24% on BFCL-v1-era scoring); the primary BFCL leaderboard table itself was not directly fetchable this session.
6. Failure modes are well-documented across the class: hallucinated function names, syntactically-valid-but-semantically-wrong JSON args, and — with actual quantified numbers — over-triggering (Qwen3-8B: 38.2% unnecessary calls) and under-triggering (Llama-3.2-3B: 39.0% missed calls) from the same 2026 benchmark.
7. Tool-use judgment (knowing when *not* to call) does not scale monotonically with parameter count in at least one documented case (Qwen2.5:1.5B outperformed Qwen2.5:3B on this specifically).
8. Major agent frameworks (LangGraph, OpenAI Agents SDK, CrewAI, AutoGen) all have documented LLM-based router/triage/manager patterns, but none of their official docs mandate a *small* model for that role — model size is left to the developer, and CrewAI's own community guidance warns small models suffice only for simple delegation.
9. Quantified routing-accuracy evidence exists only on the cascade/router-research side (FrugalGPT: up to 98% cost reduction/4% accuracy gain; RouteLLM: up to 85% cost reduction at 95% GPT-4 performance via a tunable threshold) — and a dedicated study (arXiv 2606.07587, "Routing Plateau") finds routers structurally plateau below oracle accuracy, with failures concentrated on the hardest queries.
10. Anthropic's own strongest documented small-model number (Opus 4.5 + Haiku 4.5 subagents, 87.0% vs 74.8%) is a **worker** result, not a routing/triage result — no primary Anthropic doc found describing a small-model router/guard pattern in Claude Code/Agent SDK.


---

# PART 1 — Does "Cactus Needle" exist? (factual research)

**Scope note:** The source brief for this doc characterized "cactus needle" as "a tree-of-agents system... as an example of a small function-calling model." That characterization was UNVERIFIED going in. It does **not** match what was found. See verdict below before reading further.

## Verdict, plainly

- **Cactus** is a real, actively-developed project: an on-device/edge AI inference engine for mobile and wearable devices. It exists.
- **Needle** is a real, related project: a 26-million-parameter small language model built by the same organization (Cactus Compute) specifically for function/tool calling, designed to run on Cactus's runtime on small devices.
- **Cactus is not "a tree-of-agents system."** It is an inference engine/SDK (comparable in category to llama.cpp / MLC-LLM / ONNX Runtime Mobile, but mobile-first with OpenAI-compatible APIs). Nothing found describes Cactus or Needle as implementing multi-agent orchestration, a tree of agents, or anything resembling the swarm/agent-tree architecture this design doc is presumably about.
- So: "Cactus" and "Needle" are correctly related to each other (Needle is Cactus Compute's small model, built to run on the Cactus engine), but the **"tree-of-agents system" framing is not supported by any source found** and should not be inherited into the design doc as if verified. If PART 1 is meant to source an analogy for a multi-agent architecture, that analogy does not come from Cactus/Needle's actual design — it would need to be constructed and labeled as the doc author's own metaphor, not attributed to the project.

---

## Cactus (the engine)

- **What it is**: An edge/on-device AI inference engine for mobile devices and wearables, providing local (and optionally cloud-handoff) inference for LLMs, VLMs, and speech recognition. DOCUMENTED: [github.com/cactus-compute/cactus](https://github.com/cactus-compute/cactus), [cactuscompute.com](https://cactuscompute.com/)
- **Architecture** (per repo docs), four layers: DOCUMENTED — [github.com/cactus-compute/cactus](https://github.com/cactus-compute/cactus)
  - *Cactus Engine* — OpenAI-compatible APIs for text, speech, vision
  - *Cactus Graph* — zero-copy computation graph for tensor ops
  - *Cactus Kernels* — ARM NEON SIMD kernels tuned per-vendor (Apple, Snapdragon, Google, Exynos, MediaTek)
  - *Cactus Quants* — custom rotation-based quantization, 1–4 bit
- **Platforms**: macOS, iOS, iPadOS, visionOS, Android (iPhone 15 Pro+ and newer Pixel/Samsung devices called out specifically). DOCUMENTED — [github.com/cactus-compute/cactus](https://github.com/cactus-compute/cactus)
- **Language bindings**: Swift, Kotlin, Flutter, React Native, Python, Rust; a separate Kotlin Multiplatform library also exists. DOCUMENTED — [github.com/cactus-compute/cactus](https://github.com/cactus-compute/cactus), [github.com/cactus-compute/cactus-kotlin](https://github.com/cactus-compute/cactus-kotlin)
- **Function-calling / API interface**: Exposes an **OpenAI-compatible local HTTP server** (i.e., the /chat/completions-style tool-calling contract), plus tool calling and RAG support built into the Engine layer. DOCUMENTED — [github.com/cactus-compute/cactus](https://github.com/cactus-compute/cactus)
- **Latency claim**: sub-50ms time-to-first-token for on-device inference (Cactus's own marketing claim, not independently verified here). DOCUMENTED (claim, unverified by third party) — [huggingface.co/blog/rshemet/cactus-on-device-inference](https://huggingface.co/blog/rshemet/cactus-on-device-inference)
- **License**: **Custom proprietary license with a tiered free-use carve-out**, not a standard OSS license despite being source-available on GitHub. Free for: individuals (personal/educational/research/non-commercial use), organizations under $2M in both funding and annual revenue, educational institutions, and 501(c)(3) nonprofits. Larger/commercial organizations must obtain a separate paid commercial license. There is an auto-termination clause: if a qualifying small org later exceeds either $2M threshold, the free grant terminates and a commercial license is required within 30 days. DOCUMENTED — [github.com/cactus-compute/cactus/blob/main/LICENSE](https://github.com/cactus-compute/cactus/blob/main/LICENSE)
- **Maturity / maintainer**: Maintained by **Cactus Compute, Inc.**, founder/lead named as Henry Ndubuaku in repo metadata. Active development signals: 19 releases, latest reported as v2.0.1 (July 2026), tens of open issues and PRs. GitHub star count could not be pinned to a single reliable number — different fetch passes returned different figures (5.5k in one pass), so treat any specific star count as approximate/unverified rather than citing a precise number. DOCUMENTED (activity signals) — [github.com/cactus-compute/cactus](https://github.com/cactus-compute/cactus); star count NOT reliably confirmed, flagged rather than reported as fact.
- **Cost**: No pricing was found published for the commercial license tier; free tier is scoped as above. DOCUMENTED (absence of published pricing) — [github.com/cactus-compute/cactus/blob/main/LICENSE](https://github.com/cactus-compute/cactus/blob/main/LICENSE)

## Needle (the model)

- **What it is**: A 26-million-parameter model distilled from Google's Gemini (one source says "Gemini 3.1," specific enough to flag as possibly imprecise/unverifiable — see caveat below) for **single-shot function/tool calling** on very small/consumer devices (phones, watches, glasses). Built by Cactus Compute, designed to run on the Cactus runtime. DOCUMENTED — [github.com/cactus-compute/needle](https://github.com/cactus-compute/needle), [cactuscompute.com/blog/needle](https://cactuscompute.com/blog/needle), [huggingface.co/Cactus-Compute/needle](https://huggingface.co/Cactus-Compute/needle)
- **Architecture**: Cactus calls this a "Simple Attention Network" (SAN) — an encoder-decoder transformer variant with **no feed-forward/MLP layers**, only attention + gating. 12 encoder layers (no FFN) + 8 decoder layers (masked self-attention + cross-attention). Hidden dim 512, 8 attention heads / 4 KV heads (grouped-query attention), RoPE positional encoding, 8,192-entry BPE vocabulary. DOCUMENTED — [github.com/cactus-compute/needle/blob/main/docs/simple_attention_networks.md](https://github.com/cactus-compute/needle/blob/main/docs/simple_attention_networks.md), [github.com/cactus-compute/needle](https://github.com/cactus-compute/needle)
- **Model size**: 26M parameters, single size (no family of sizes found — e.g. no 26M/70M/200M tiers were mentioned anywhere). DOCUMENTED — all sources above.
- **Context window**: **Not documented anywhere found.** Multiple direct look-ups (GitHub repo, HF model card, targeted web search) came back empty on this specific figure. One secondary source (DeepWiki, an AI-generated wiki, so lower-confidence) states "in-context learning is not currently supported but is on the roadmap," implying the current context handling is limited/non-standard, but no numeric context length is documented. **Flagging as an open gap, not filling it with a guess.**
- **Quantization**: Quantizes down to a 14 MB footprint at INT4 (per one summarized source); not independently confirmed against a primary spec sheet. DOCUMENTED, lower confidence — [github.com/cactus-compute/needle](https://github.com/cactus-compute/needle) (via secondary summary)
- **Speed claims**: "6000 tokens/sec prefill and 1200 decode" — stated as measured on Cactus's own runtime/hardware, not tied to a specific device model in what was fetched. This is a vendor performance claim, not independently benchmarked here. DOCUMENTED (claim) — [cactuscompute.com/blog/needle](https://cactuscompute.com/blog/needle), [github.com/cactus-compute/needle](https://github.com/cactus-compute/needle)
- **Training**: Pretrained on 200B tokens using 16× TPU v6e over 27 hours; post-trained (function-calling specialization) on 2B tokens over 45 minutes, using a synthesized dataset generated via Gemini across 15 tool categories. DOCUMENTED — [cactuscompute.com/blog/needle](https://cactuscompute.com/blog/needle)
- **Function-calling interface**: Takes **JSON-schema-style tool definitions** (name, description, parameters) and emits a **JSON array of function calls**, e.g. `[{"name":"get_weather","arguments":{"location":"San Francisco"}}]`. This is compatible in spirit with the OpenAI tools/function-calling JSON shape, though nothing found states Needle directly implements the OpenAI tool-calling wire protocol itself (that OpenAI-compatibility claim is made for the **Cactus engine**, not explicitly for Needle's raw model I/O). Treat "Needle speaks OpenAI tools format" as an inference, not a confirmed fact. DOCUMENTED (JSON shape) — [cactuscompute.com/blog/needle](https://cactuscompute.com/blog/needle)
- **Benchmarks claimed**: Said to outperform FunctionGemma-270M, Qwen-0.6B, Granite-350M, and LFM2.5-350M on single-shot function-calling tasks. This is a self-reported vendor benchmark; no independent/third-party benchmark confirming this was found. DOCUMENTED (vendor claim, not independently verified) — [cactuscompute.com/blog/needle](https://cactuscompute.com/blog/needle)
- **License**: **MIT** (this is distinct from and more permissive than the parent Cactus engine's proprietary tiered license — do not conflate the two). DOCUMENTED — [huggingface.co/Cactus-Compute/needle](https://huggingface.co/Cactus-Compute/needle), [github.com/cactus-compute/needle](https://github.com/cactus-compute/needle)
- **Maturity**: GitHub activity figures returned inconsistently across fetch passes (one pass reported ~3,000 stars / 212 forks / 12 open issues for the Needle repo specifically); given the inconsistency seen on the Cactus repo's star count too, treat any specific Needle star count as approximate and secondary, not load-bearing. Hugging Face model card shows modest usage (235 downloads in the most recent month observed) — small but real adoption, consistent with a recently-released niche model rather than a widely-adopted production dependency. DOCUMENTED, flagged confidence — [huggingface.co/Cactus-Compute/needle](https://huggingface.co/Cactus-Compute/needle)
- **Deployment / usage**: `needle playground` CLI command launches a local web UI (localhost:7860) for testing/finetuning; also offers a Python API and CLI. Repo is majority Python (~93%). DOCUMENTED — [github.com/cactus-compute/needle](https://github.com/cactus-compute/needle)
- **Cost**: No pricing found — MIT-licensed, weights open on Hugging Face, no paid tier mentioned for the model itself (unlike the Cactus engine, which has a commercial license tier). DOCUMENTED (absence of pricing) — [huggingface.co/Cactus-Compute/needle](https://huggingface.co/Cactus-Compute/needle)

## Explicit caveats / gaps

1. **Context window length is not documented** in any source checked (repo, HF card, targeted search). This is a real gap, not an oversight in this research — do not backfill it with a plausible-sounding number in the design doc.
2. **"Gemini 3.1" as the distillation source** — this specific version string appeared in one secondary source only; it was not independently cross-confirmed against a primary Cactus source in the fetches performed. KNOWLEDGE caveat: as of this agent's training data, no "Gemini 3.1" had been publicly named by Google — this may be a real forward-dated release (current date in this session is stated as 2026-07-13, well past this agent's knowledge cutoff) or may be an error/marketing imprecision in the secondary source. Flagging rather than asserting either way.
3. **GitHub star/fork counts are unstable across fetches** for both repos — likely because WebFetch summarization is lossy on numeric tables/badges rather than the underlying pages actually disagreeing. Do not cite a specific star count as precise in the downstream doc; "actively maintained, multiple releases, real but modest community size" is the defensible summary.
4. **No "tree-of-agents" or multi-agent orchestration capability was found** in either project. If the broader design doc wants to use Cactus/Needle as "an example of a small function-calling model," that specific, narrower claim (small model, does function calling, runs on-device) **is supported**. The "tree-of-agents system" framing is not — it appears to be either a misunderstanding, a conflation with something else, or an intended metaphor that was never labeled as such. This should be corrected or explicitly labeled as the design doc's own metaphor before PART 1 is spliced in.

## Source list

- [github.com/cactus-compute/cactus](https://github.com/cactus-compute/cactus) — Cactus engine repo
- [github.com/cactus-compute/cactus-kotlin](https://github.com/cactus-compute/cactus-kotlin) — Kotlin Multiplatform bindings
- [github.com/cactus-compute/cactus/blob/main/LICENSE](https://github.com/cactus-compute/cactus/blob/main/LICENSE) — Cactus license text
- [cactuscompute.com](https://cactuscompute.com/) — product site
- [huggingface.co/blog/rshemet/cactus-on-device-inference](https://huggingface.co/blog/rshemet/cactus-on-device-inference) — Cactus overview/latency claims
- [huggingface.co/Cactus-Compute](https://huggingface.co/Cactus-Compute) — org page
- [github.com/cactus-compute/needle](https://github.com/cactus-compute/needle) — Needle model repo
- [github.com/cactus-compute/needle/blob/main/docs/simple_attention_networks.md](https://github.com/cactus-compute/needle/blob/main/docs/simple_attention_networks.md) — SAN architecture doc
- [cactuscompute.com/blog/needle](https://cactuscompute.com/blog/needle) — Needle announcement/spec blog post (primary vendor source for most Needle numbers)
- [huggingface.co/Cactus-Compute/needle](https://huggingface.co/Cactus-Compute/needle) — Needle model card
- Secondary/lower-confidence, used only where flagged: [rits.shanghai.nyu.edu](https://rits.shanghai.nyu.edu/ai/cactus-releases-needle-a-26m-distilled-model-for-on-device-tool-calling/), [deepwiki.com/cactus-compute/needle](https://deepwiki.com/cactus-compute/needle) (AI-generated wiki, not a primary source)

---

# PART 2 — Landscape of Small Function-Calling / Tool-Use Language Models (2025–2026)

Scope: factual survey only, independent of any specific product or use case. No recommendations. Every claim tagged **DOCUMENTED** (with URL) or **KNOWLEDGE** (training-memory recall, not independently verified this session — flagged for staleness since this space moves fast, roughly monthly new releases/benchmarks).

---

## 1. Model-by-model survey

### 1.1 Gorilla / OpenFunctions (UC Berkeley)

- Gorilla OpenFunctions-v2 is presented as an open-source function-calling LLM claimed on-par with GPT-4 on function calling. **DOCUMENTED** — [Gorilla OpenFunctions v2 blog](https://gorilla.cs.berkeley.edu/blogs/7_open_functions_v2.html), [HF model card](https://huggingface.co/gorilla-llm/gorilla-openfunctions-v2)
- Exact parameter count for OpenFunctions-v2 was not confirmed from the pages fetched this session (search results discussed capability claims, not size). OpenFunctions-v1/v2 are fine-tunes of existing open base models (historically reported as ~7B class, e.g. a CodeLlama/Llama derivative) — **KNOWLEDGE**, unverified this session, flag for staleness/accuracy.
- Berkeley also maintains the **Berkeley Function-Calling Leaderboard (BFCL)**, now at v4, described as evaluating "the LLM's ability to call functions (aka tools) accurately," spanning AST-based single-turn evaluation, live (real-world/enterprise-contributed) queries, multi-turn interaction, and (per version history) relevance/irrelevance detection. **DOCUMENTED** — [BFCL leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html), [BFCL GitHub](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard), [BFCL paper (MLR Press)](https://proceedings.mlr.press/v267/patil25a.html)
- BFCL version history: V1 (Feb 2024, single-turn AST), V2 (Aug 2024, live enterprise-contributed data), V3 (Sep 2024, multi-turn), V4 (Jul 2025, "holistic agentic evaluation"). **DOCUMENTED** — same leaderboard page/search summary above.
- As of a June 29, 2026 snapshot cited by a third-party tracker, top BFCL v3 scores were led by GLM 4.5 (76.7%), Claude Opus 4.7 (76.6%), Gemini 3.1 Flash Lite Preview (76.5%) — none of these are small models; included only to calibrate the scale small-model scores (below) sit against. **DOCUMENTED**, third-party aggregator, not the primary leaderboard page — [pricepertoken.com BFCL v3](https://pricepertoken.com/leaderboards/benchmark/bfcl-v3). Treat as lower-confidence secondary source; primary leaderboard table itself did not render in a fetchable form this session.

### 1.2 Salesforce xLAM ("Large Action Models")

- Family explicitly built for function calling, reasoning, and planning; marketed under "Large Action Models" branding. **DOCUMENTED** — [Salesforce xLAM GitHub](https://github.com/SalesforceAIResearch/xLAM), [Salesforce blog: Introducing xLAM](https://www.salesforce.com/blog/xlam-large-action-models/)
- Sizes: original family released July–August 2024 included **xLAM-1b-fc-r** (1B, "Tiny Giant," on-device target) and **xLAM-7b-fc-r** (7B, for GPU-constrained academic use). **DOCUMENTED** — [HF xLAM-1b-fc-r](https://huggingface.co/Salesforce/xLAM-1b-fc-r), [HF xLAM-7b-fc-r](https://huggingface.co/Salesforce/xLAM-7b-fc-r)
- 2025 update ("xLAM-2" series) adds multi-turn support and a wider size ladder: **xLAM-2-1B-r** (on-device), **xLAM-2-3B-r**, **xLAM-2-8B-r** (academic), **xLAM-2-32B-r** (industrial), **xLAM-2-70B-r** (best research-grade). **DOCUMENTED** — [Salesforce blog: xLAM v2](https://www.salesforce.com/blog/xlam-large-action-models-v2/)
- Reported accuracy: xLAM-7b-fc-r 88.24% overall on BFCL (original v1 leaderboard cut); xLAM-1b-fc-r 78.94%, reported as beating GPT-3.5-Turbo despite 1B size. **DOCUMENTED** (via search synthesis of Salesforce/HF pages — recommend re-verifying exact figure against current leaderboard page since BFCL versions and scoring have since changed; original ranking was BFCL v1-era, #3 and #25 respectively). Flag: these are old (mid-2024) BFCL-v1-era numbers, likely stale relative to BFCL v3/v4 scoring methodology.
- More recent (2025/2026-era) BFCL-style academic re-evaluation: **xLAM-2-3b-fc-r (FC)** reported as the strongest among evaluated small/medium models in one paper's comparison table, at 65.74% overall accuracy (81.03% live execution, 88.22% non-live AST, 55.62% multi-turn). **DOCUMENTED** — surfaced via WebSearch summary referencing a 2025/2026 arXiv paper (likely "TinyLLM: Evaluation and Optimization of Small Language Models for Agentic Tasks on Edge Devices," https://arxiv.org/pdf/2511.22138, or a closely related one — exact source arXiv ID not independently confirmed by direct fetch this session, so treat citation as approximate pending direct verification).

### 1.3 Hammer (MadeAgents)

- Explicitly positioned as "Robust Function-Calling for On-Device Language Models via Function Masking." **DOCUMENTED** — [arXiv paper](https://arxiv.org/pdf/2410.04587), [GitHub](https://github.com/MadeAgents/Hammer)
- Sizes: Hammer 2.0 family ships at **0.5B, 1.5B, 3B, 7B**. **DOCUMENTED** — [HF Hammer-1.5b](https://huggingface.co/MadeAgents/Hammer-1.5b), [HF Hammer-7b](https://huggingface.co/MadeAgents/Hammer-7b)
- Training data: APIGen function-calling dataset (60K samples) plus an added "xlam-irrelevance-7.5k" set specifically to teach irrelevance/no-call detection. **DOCUMENTED** — [Hammer GitHub README](https://github.com/MadeAgents/Hammer/blob/main/README.md)
- Reported performance: Hammer-7B ranks "second only to the proprietary GPT-4" on BFCL among the scales tested, per the paper's own framing; the paper's stated motivation is that other function-calling models were found to be overfit to specific naming conventions ("misled by naming conventions"), i.e., a documented brittleness finding for the class as a whole, not just Hammer's predecessors. **DOCUMENTED** — [arXiv 2410.04587](https://arxiv.org/pdf/2410.04587)

### 1.4 Octopus-series (Nexa AI, on-device)

- Octopus-V2-2B: 2B-parameter model, explicitly targeted at on-device Android API function calling. **DOCUMENTED** — [HF NexaAI/Octopus-v2](https://huggingface.co/NexaAI/Octopus-v2), [arXiv paper](https://arxiv.org/html/2404.01744v5)
- Key technique: "functional tokens" — each supported function is mapped to a single new token (e.g. `<func_1>`) added to the tokenizer/vocabulary, so function-name selection becomes single-token classification rather than multi-token generation. This is stated by the authors as the mechanism that eliminates a category of function-name hallucination (multi-token misgeneration of names). **DOCUMENTED** — [arXiv 2404.01744v5](https://arxiv.org/html/2404.01744v5)
- Reported accuracy (paper's own benchmark, Android function-calling task, ground truth manually labeled with Gemini assistance): Octopus v2 (2B) 99.524%, GPT-4 98.571%, GPT-3.5 97.143% (no RAG)/98.095% (with RAG), Llama-7B+RAG 68.095%. Latency reported as 0.38s average, ~35x faster than the Llama-7B+RAG baseline, with ~95% context-length reduction versus RAG-based approaches. **DOCUMENTED** — [arXiv 2404.01744v5](https://arxiv.org/html/2404.01744v5). Caveat: this is a single-paper, author-run benchmark on a narrow Android-API task set, not BFCL; treat the head-to-head "beats GPT-4" framing as coming from the model's own paper, not an independent third-party leaderboard.
- Paper explicitly names failure modes observed in baselines: "incorrect function name selection and erroneous parameter generation" as the two primary error categories for non-Octopus baselines on this task. **DOCUMENTED** — same source.

### 1.5 Microsoft Phi-family

- **Phi-3 / Phi-3.5**: not documented to officially support function/tool calling. Community reports exist of ad hoc success getting JSON-like output via prompting, but this is not a first-class supported feature. **DOCUMENTED** (absence of support) — [HF Phi-3.5-mini-instruct discussion](https://huggingface.co/microsoft/Phi-3.5-mini-instruct/discussions/7), [HF Phi-3-mini-128k-instruct discussion](https://huggingface.co/microsoft/Phi-3-mini-128k-instruct/discussions/18)
- **Phi-4-mini** and **Phi-4-multimodal**: DO officially support function calling as of their release; Microsoft frames this as a new capability versus Phi-3. Function calling is scoped to the Phi-4-mini-based line specifically — other Phi-4 variants (e.g. Phi-4-reasoning-plus) are reported as not supporting it. **DOCUMENTED** — [Microsoft Tech Community: Phi-4-mini & Phi-4-multimodal](https://techcommunity.microsoft.com/blog/educatordeveloperblog/welcome-to-the-new-phi-4-models---microsoft-phi-4-mini--phi-4-multimodal/4386037), [PhiCookBook function calling guide](https://github.com/microsoft/PhiCookBook/blob/main/md/02.Application/07.FunctionCalling/Phi4/FunctionCallingBasic/README.md)
- Microsoft explicitly markets Phi-4-mini function calling for edge/on-device agent scenarios (e.g. via Ollama). **DOCUMENTED** — [Building AI Agents on edge devices using Ollama + Phi-4-mini](https://techcommunity.microsoft.com/blog/educatordeveloperblog/building-ai-agents-on-edge-devices-using-ollama--phi-4-mini-function-calling/4391029)
- Phi-4-mini parameter size: **KNOWLEDGE** (commonly cited as ~3.8B) — not independently re-confirmed via a fetched primary source this session; flag for verification if precision matters.
- No BFCL-specific score for any Phi model was surfaced in this session's searches — absence noted, not confirmed absence of any score anywhere.

### 1.6 Small Qwen variants (Qwen2.5 / Qwen2.5-Coder / Qwen3 small)

- Qwen2.5 and Qwen3 small variants (0.5B–3B range) are documented as supporting tool/function calling via a Hermes-style `<tool_call>` prompt format; Qwen2.5-**Coder** variants specifically diverge and instead reliably use a `<tools>` tag format (not Hermes-style) when given few-shot prompting — a documented format inconsistency within the same model family. **DOCUMENTED** — [Qwen function-calling docs](https://qwen.readthedocs.io/en/latest/framework/function_call.html), [vLLM Qwen2.5-Coder tool parser](https://github.com/hanXen/vllm-qwen2.5-coder-tool-parser), [GitHub issue: does qwen2.5-coder support function calling](https://github.com/QwenLM/Qwen3-Coder/issues/180)
- A user-reported hallucination issue exists specifically for Qwen2.5-Coder-7B-Instruct function calling ("Model Hallucination in Function Call") — DOCUMENTED as a reported issue thread, not a systematic study. **DOCUMENTED** — [HF discussion](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct/discussions/22)
- Academic evaluation across Qwen-series models 0.5B–14B on five function-calling benchmarks (BFCL-v3, Mobile Actions, SealTools, OpenFunction, ToolAlpaca) found: 1.5B and 0.5B models show only slight improvement from function-calling-specific training, while 3B and 7B gain substantially — suggesting personalized/complex tool invocation is scale-dependent below a certain threshold. **DOCUMENTED** — [arXiv 2505.04072](https://arxiv.org/pdf/2505.04072)
- A separate real-world ("in the wild") tool-use benchmark found a **non-monotonic** relationship between size and agent quality when judgment (knowing when NOT to call) is measured: qwen2.5:1.5b outperformed qwen2.5:3b by declining uncertain prompts rather than guessing wrong. **DOCUMENTED** — [Local Agent Bench: 21 open-weight models](https://mikeveerman.be/blog/github-2026-02-06-tool-calling-benchmark/), corroborating [GitHub tool-calling-benchmark](https://github.com/MikeVeerman/tool-calling-benchmark)

### 1.7 Google Gemini Nano (on-device, Android/AICore)

- Google expanded Gemini Nano on-device capability at I/O 2026 specifically to add function calling and structured JSON output for offline-capable Android agents, accessed via AICore. **DOCUMENTED** — [Android Developers: Gemini Nano](https://developer.android.com/ai/gemini-nano), [Gemini Nano on-device function calling writeup](https://mvpfactory.io/blog/gemini-nano-on-device-function-calling-for-android-structured-output-token/)
- Documented technical constraint: ~32K token on-device budget must cover system prompt + tool schemas + history + response; reported first-token latency 80–200ms on-device vs. 300–800ms for cloud Gemini Flash, but on-device explicitly "degrades with schema complexity" while cloud remains "stable [with] complex schemas" — a documented reliability-vs-schema-size tradeoff specific to the small on-device model. **DOCUMENTED** — [mvpfactory.io writeup](https://mvpfactory.io/blog/gemini-nano-on-device-function-calling-for-android-structured-output-token/) (secondary/practitioner source, not a Google primary benchmark page — treat performance figures as practitioner-reported, not vendor-certified).
- Documented failure modes specific to Gemini Nano tool calling per the same source: schemas over ~1,200 tokens can silently overflow the context budget and produce incoherent output with no error; the model frequently wraps valid JSON in explanatory text or markdown code fences (requiring stripping before parse); the model can hallucinate parameter names not present in the registered schema. **DOCUMENTED** — same source. Flag: single practitioner source, not independently cross-checked against a second writeup this session.

### 1.8 Apple Intelligence / Apple on-device Foundation Models

- Apple's on-device foundation model (as of the 2025 generation) is ~3B parameters, using KV-cache sharing and 2-bit quantization-aware training for on-Apple-silicon efficiency. A separate, larger server-side model uses a Parallel-Track Mixture-of-Experts (PT-MoE) architecture. **DOCUMENTED** — [Apple ML Research: 2025 foundation model updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates), [Apple Intelligence Foundation Language Models Tech Report 2025](https://machinelearning.apple.com/research/apple-foundation-models-tech-report-2025), [arXiv tech report](https://arxiv.org/pdf/2507.13575)
- Apple's Foundation Models framework (introduced WWDC 2025) explicitly exposes "constrained tool calling" alongside guided generation and LoRA adapter fine-tuning, as a first-class, developer-facing Swift API against the ~3B on-device model. **DOCUMENTED** — [Apple Newsroom: Foundation Models framework](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/), [WWDC25 session: Meet the Foundation Models framework](https://developer.apple.com/videos/play/wwdc2025/286/), [WWDC25 deep dive session](https://developer.apple.com/videos/play/wwdc2025/301/)
- "Constrained" tool calling implies grammar/schema-constrained decoding is used to keep tool-call output well-formed by construction, though the tech report content on failure rates/accuracy specific to tool calling was not directly quoted in the pages retrieved this session — the fact of constrained decoding is documented; quantitative tool-call accuracy/error-rate numbers were not found in this session's searches (absence noted, not confirmed absent from the tech report itself, which is long and was not fully read).
- No BFCL or third-party tool-calling benchmark placement for Apple's on-device model was found — Apple has not (per this session's searches) submitted it to BFCL or similar open leaderboards. **KNOWLEDGE**/absence-of-evidence — flag as a gap, not a confirmed non-participation.

---

## 2. Documented failure modes for small function-calling models (cross-cutting)

These are drawn from literature/blogs/papers across the above models and general small-model tool-use studies, not limited to one vendor.

1. **Hallucinated function/tool names.** The model emits a call to a tool name that doesn't exist in the provided schema (or in the dispatcher's registry). Directly named as a failure mode across multiple sources; Octopus v2's single-token function-name design was built specifically to structurally eliminate this category for its supported function set. **DOCUMENTED** — [arXiv 2404.01744v5](https://arxiv.org/html/2404.01744v5); general framing: [LLM Function-Calling Pitfalls](https://medium.com/@2nick2patel2/llm-function-calling-pitfalls-nobody-mentions-a0a0575888b1); Gemini Nano-specific: [mvpfactory.io](https://mvpfactory.io/blog/gemini-nano-on-device-function-calling-for-android-structured-output-token/); Qwen2.5-Coder-7B-specific user report: [HF discussion](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct/discussions/22)

2. **Malformed / invalid JSON arguments.** Even with schema-constrained decoding guaranteeing syntactic JSON validity, models (especially small ones) still populate wrong types, omit required fields, or hallucinate plausible-looking but incorrect field values — described as "JSON mode is a syntax guarantee, not a schema guarantee." Small models are specifically called out as forming valid-shaped-but-wrong-content calls more often. **DOCUMENTED** — search synthesis citing multiple 2026 practitioner sources: [futureagi.com](https://futureagi.com/blog/llm-function-calling-2025/), [tensoria.fr](https://tensoria.fr/en/blog/structured-outputs-llm-production), [vLLM RFC on tool-call parsing](https://github.com/vllm-project/vllm/issues/39848)

3. **Over-triggering (calling a tool when none is needed).** Directly quantified in at least one 2026 benchmark: across evaluated models, "no-call accuracy" (correctly declining to call a tool) was consistently much lower than "call accuracy," pulling overall accuracy down to a 55–70% range. One named example: **Qwen3-8B** called a tool on 38.2% of queries it could have answered directly (over-triggering), while only 3.5% of queries that genuinely needed a tool went uncalled. **DOCUMENTED** — [When2Tool-related arXiv paper on over-calling bias](https://arxiv.org/pdf/2605.18882), [Local Agent Bench](https://mikeveerman.be/blog/github-2026-02-06-tool-calling-benchmark/)

4. **Under-triggering (failing to call a tool when needed).** Same source family reports the opposite failure in a different model: **Llama-3.2-3B-Instruct** failed to call a tool on 39.0% of queries that actually needed one. General mismatch rates in this study ranged 26.5–54.0% (arithmetic tasks) and 30.8–41.8% (factual QA) across the tested small local models. **DOCUMENTED** — [Local Agent Bench](https://mikeveerman.be/blog/github-2026-02-06-tool-calling-benchmark/), [GitHub tool-calling-benchmark repo](https://github.com/MikeVeerman/tool-calling-benchmark)

5. **Schema drift.** Not small-model-specific, but relevant as a systemic failure category: when a tool's schema is updated (e.g. a new required field) but the model's prompt/instructions aren't regenerated in lockstep, the model keeps emitting the old parameter shape, since "the toolset is in code, the prompt is in code, they are not the same code." This is framed as one of the highest-impact and easiest-to-miss bugs in production tool-calling systems generally. **DOCUMENTED** — [Tool Definition Drift](https://dev.to/gabrielanhaia/tool-definition-drift-when-your-agents-toolset-outgrows-its-prompt-k32)

6. **Naming-convention overfitting / benchmark brittleness.** The Hammer paper's own stated motivation: prior function-calling models' benchmark performance was found to vary significantly depending on function/parameter naming conventions used at eval time, implying models were partly pattern-matching on naming style rather than robustly understanding schemas — a form of narrow generalization failure specifically flagged in small on-device function-calling model research. **DOCUMENTED** — [Hammer arXiv paper](https://arxiv.org/pdf/2410.04587)

7. **Context/schema-size-induced degradation on-device.** Documented specifically for Gemini Nano: schemas above ~1,200 tokens risk silently consuming the ~32K on-device token budget, causing incoherent responses with no explicit error signal — a failure mode tied directly to the constrained context budgets small on-device models operate under (as opposed to cloud models). **DOCUMENTED** — [mvpfactory.io](https://mvpfactory.io/blog/gemini-nano-on-device-function-calling-for-android-structured-output-token/)

8. **Output wrapped in extraneous text/markdown.** Documented for Gemini Nano: model frequently wraps a valid JSON tool call in explanatory prose or markdown code fences, breaking naive parsers expecting raw JSON — a formatting-discipline failure distinct from JSON validity itself. **DOCUMENTED** — same source.

9. **Non-monotonic scaling for judgment/relevance-detection specifically.** Multiple sources converge on: raw parameter count does not monotonically predict tool-use *judgment* quality (when to call vs. not), even though it more reliably predicts raw *formatting* competence. Qwen2.5:1.5B outperforming Qwen2.5:3B on a real-world benchmark by being more willing to decline uncertain calls is the cited concrete example. **DOCUMENTED** — [Local Agent Bench](https://mikeveerman.be/blog/github-2026-02-06-tool-calling-benchmark/); scale-dependence for complex/personalized invocation: [arXiv 2505.04072](https://arxiv.org/pdf/2505.04072)

---

## 3. Staleness / confidence flags (explicit)

- This is an actively moving space: multiple cited sources are dated within the last few months of the current date (2026-07-13) — e.g. Gemini Nano's function-calling expansion was announced at "I/O 2026," and the Local Agent Bench post is dated 2026-02-06. Any of these could already be superseded by newer releases not surfaced in this session's searches.
- The primary BFCL leaderboard table (gorilla.cs.berkeley.edu/leaderboard.html) did not render usable tabular data via WebFetch this session; all BFCL numeric scores above were obtained via WebSearch summaries or secondary aggregator sites (pricepertoken.com) or academic papers citing BFCL-style numbers, not a direct read of Berkeley's own current table. Anyone needing exact current BFCL rank/score for a specific small model should re-fetch the leaderboard directly (it may require JS rendering).
- Gorilla OpenFunctions-v2's exact parameter count and xLAM-1B/7B's original BFCL rank numbers rely partly on **KNOWLEDGE** or lightly-sourced search summaries rather than a directly fetched primary page — flagged inline above where this applies.
- Apple's on-device tool-calling accuracy/error-rate numbers (as opposed to the fact that constrained tool calling exists) were not found — this is a gap in this session's research, not a confirmed absence of published numbers.

---

*End of PART 2. Prepared by agent hc-slm-class for splicing into a larger audit document.*

---

# PART 3 — Do production agent frameworks use small models for routing/triage/guard roles?

Scope: whether small/cheap models are documented as performing routing, triage/classification, or guard/filter roles specifically (as distinct from just being cheap general-purpose workers). Every claim tagged DOCUMENTED (source URL) or KNOWLEDGE (model training memory, may be stale/unverifiable).

## Framework-by-framework findings

### LangGraph
- DOCUMENTED: LangGraph's documented "routing pattern" uses conditional edges where a node — commonly an LLM call — inspects the query/state and returns a string/`Command()` naming the next node. The official pattern does not mandate a *small* model; it's model-agnostic routing logic. (https://docs.langchain.com/oss/python/langgraph/graph-api, https://medium.com/@huzaifaali4013399/the-routing-pattern-build-smart-multi-agent-ai-workflows-with-langgraph-44f177aadf7a)
- DOCUMENTED: A community example project (`johnsosoka/langgraph-model-router`) explicitly demonstrates an LLM-based router that routes a query to either a "simple model" or an "advanced model" depending on assessed query complexity — i.e., a small/cheap model classifying complexity to select the downstream model. This is a community example, not core LangChain-maintained documentation. (https://github.com/johnsosoka/langgraph-model-router)
- No reported misrouting/accuracy numbers found for LangGraph's own router pattern — it's presented as an architecture, not benchmarked.

### OpenAI Agents SDK
- DOCUMENTED: The SDK's core multi-agent pattern is "handoffs": a **triage agent** classifies an incoming request and hands off (transfers full conversation) to a specialized agent. Official guidance: "make the handoff's purpose explicit... and tell triage to route, not answer." Handoffs can carry small structured metadata (`input_type`, e.g. reason/priority/summary) generated by the triage agent. (https://openai.github.io/openai-agents-python/handoffs/, https://developers.openai.com/api/docs/guides/agents/orchestration, https://openai.github.io/openai-agents-python/multi_agent/)
- The docs do not mandate the triage agent be a small/cheap model specifically — model choice per agent is left to the developer — but the pattern ("cheap triage agent classifies... transfers to the right specialist") is commonly described that way in secondary sources. No reported misclassification-rate numbers found in OpenAI's own docs.

### CrewAI
- DOCUMENTED: CrewAI's "hierarchical process" uses a manager agent/LLM (`manager_llm`) to decide task delegation among worker agents — a routing/orchestration role, filled by an LLM call per delegation decision. (https://docs.crewai.com/en/learn/hierarchical-process)
- DOCUMENTED (community guidance, not official benchmark): commentary states the manager "needs strong instruction-following and tool-use capability... GPT-4o-mini works for simple crews. For complex delegation, use GPT-4o or Claude 3.5 Sonnet" — i.e. practitioners explicitly warn that small models are only adequate for simple delegation and larger models are needed as complexity grows. (https://activewizards.com/blog/hierarchical-ai-agents-a-guide-to-crewai-delegation/)
- DOCUMENTED: multiple bug reports/community posts describe the hierarchical manager **misdelegating tasks to the wrong agent** or failing to selectively delegate at all, causing incorrect invocation and inflated token usage — a real-world documented failure mode of LLM-based task routing, independent of model size. (https://github.com/crewAIInc/crewAI/issues/4783, https://community.crewai.com/t/manager-agent-delegates-task-to-wrong-agent-in-a-hierarchical-process/3179, https://towardsdatascience.com/why-crewais-manager-worker-architecture-fails-and-how-to-fix-it/)
- No quantified misrouting rate (%) found, only qualitative bug reports.

### AutoGen / AG2
- DOCUMENTED: `GroupChatManager` performs speaker selection — deciding which agent acts next — via an LLM call when using the `"auto"` selection strategy (`llm_config` set on the manager). This is a documented LLM-as-router role. (https://docs.ag2.ai/latest/docs/user-guide/advanced-concepts/groupchat/groupchat/, https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/selector-group-chat.html)
- DOCUMENTED: AG2 docs/notebooks show groupchats can mix agents on different models (including differently-sized models) within one chat, with the manager (router) itself configurable independently of the participant agents' models — but no official doc explicitly recommends a *small* model for the manager/router role specifically. (https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat_customized/)
- DOCUMENTED: GitHub issue #3462 ("GroupChat doesn't work well") documents real quality problems with LLM-based speaker selection in practice. No quantified accuracy numbers found.

### Claude Code / Claude Agent SDK
- DOCUMENTED: Anthropic's Claude Opus 4.5 system card reports that pairing Claude Opus 4.5 (orchestrator) with Claude Haiku 4.5 subagents scored 87.0% vs. 74.8% for Opus 4.5 alone on a (search-task) benchmark — a 12.2-point gain from an orchestrator+small-worker architecture. (https://www.anthropic.com/claude-opus-4-5-system-card)
  - Note: this figure documents small models as **cheap parallel workers**, not specifically as routers/classifiers/guards — it is evidence for the "small model as worker" pattern, which the task explicitly asked to distinguish from routing/triage/guard use. Flagging this distinction rather than overstating it.
- DOCUMENTED (secondary/community source, not an Anthropic primary doc): guidance describing a policy of "let research and search agents run on a small fast model... set CLAUDE_CODE_SUBAGENT_MODEL when you need a hard ceiling," framing Haiku-class models as suited to "routing, classification, and research" — but this framing itself comes from a third-party blog (CallSphere), not confirmed as official Anthropic documentation language. Treat as KNOWLEDGE/secondary-sourced, not a primary Anthropic claim. (https://callsphere.ai/blog/td30-anth-haiku45-subagent — secondary source, could not confirm this exact framing exists in Anthropic's own docs)
- KNOWLEDGE: I could not find, via search, a primary Anthropic doc explicitly describing a small-model "router" or "guard" node pattern in Claude Agent SDK's own architecture docs (e.g. code.claude.com/docs). The subagent docs describe subagents as isolated-context parallel workers, not as a routing/classification layer ahead of a bigger model.

## Broader ecosystem: cascade/routing research

### FrugalGPT (arXiv 2305.05176, Chen et al.)
- DOCUMENTED: Proposes three cost-reduction strategies: prompt adaptation, LLM approximation, and **LLM cascade** (query smaller/cheaper LLMs first; escalate to GPT-4-class models only when needed). This is a scoring/confidence-based escalation cascade, not a single upfront classifier. (https://arxiv.org/abs/2305.05176)
- DOCUMENTED reported numbers: "can match the performance of the best individual LLM (e.g., GPT-4) with up to 98% cost reduction, or improve accuracy over GPT-4 by up to 4% at the same cost." Overall reported cost savings range 50–98%. (https://arxiv.org/abs/2305.05176, https://ar5iv.labs.arxiv.org/html/2305.05176)
- Mitigation documented: the cascade itself IS the mitigation — cheap models handle queries a scoring function judges "answerable," harder/uncertain queries escalate to GPT-4-class models. This is the fallback-to-bigger-model pattern in its purest documented form.

### RouteLLM (arXiv 2406.18665, lmsys/lm-sys, ICLR 2025)
- DOCUMENTED: Trains a binary router (several variants: similarity-weighted ranking, matching/matrix-factorization, BERT classifier) to route each query to either a "strong" model (e.g. GPT-4 Turbo) or "weak" model (e.g. Mixtral-8x7B) based on predicted win-rate/quality need, using human preference data (Chatbot Arena) for training. (https://arxiv.org/abs/2406.18665, https://github.com/lm-sys/RouteLLM)
- DOCUMENTED reported numbers (GitHub README): "reduce costs by up to 85% while maintaining 95% of GPT-4's performance"; "same performance as commercial routing offerings while being >40% cheaper." (https://github.com/lm-sys/RouteLLM)
- DOCUMENTED reported numbers (paper, via secondary summary): using GPT-4 Turbo (strong) + Mixtral-8x7B (weak), RouteLLM cuts costs by up to 3.66× vs. random routing at equivalent quality, and 75% cost savings vs. random routing at matched performance. (https://zilliz.com/learn/routellm-open-source-framework-for-navigate-cost-quality-trade-offs-in-llm-deployment) — secondary source paraphrasing the paper; treat headline multiplier with some caution pending direct read of the paper's tables.
- DOCUMENTED mitigation mechanism: a tunable **cost threshold** (α) is the explicit control lever — README gives a concrete calibration example: threshold = 0.11593 routes 50% of Chatbot Arena queries to the strong model. This is the "confidence threshold" mitigation, explicit and user-tunable, not automatic.
- DOCUMENTED (third-party blog, citing what it frames as a router fine-tuning result — could not independently verify against the primary paper/README in the time available): "fine-tuning the router's embedding model with ~805 training examples... pushes routing accuracy from 80.39% to 98.53% — reducing misrouting from 1-in-5 to 1-in-70 requests." Flagging this as a claim from a secondary source (Medium-style writeup), not confirmed directly in the RouteLLM GitHub README or arXiv abstract during this research pass. (via search snippet, https://medium.com/@michael.hannecke/implementing-llm-model-routing-a-practical-guide-with-ollama-and-litellm-b62c1562f50f — unverified primary attribution)
- No documented fallback/human-in-loop step beyond the threshold mechanism itself; misrouted queries simply receive weak-model-quality answers with no stated recovery step in the README.

### The Routing Plateau (arXiv 2606.07587, Rice University + Amazon)
- DOCUMENTED: Systematic study of 21 routing methods across 5 benchmarks finds a "routing plateau" — most methods (including kNN-based routers) converge to a narrow, similar accuracy band well below an oracle router's ceiling. (https://arxiv.org/pdf/2606.07587)
- DOCUMENTED root-cause claim: routers mostly learn "global averaged model-performance trends" rather than per-query routing signals, so they succeed on overlapping "easy" queries but collectively fail on queries that need instance-specific routing judgment (i.e., routers are systematically weaker exactly where routing quality matters most).
- DOCUMENTED mitigation directions proposed by the paper: larger training datasets, stronger encoders, end-to-end fine-tuning — all reduce-the-plateau strategies, not full solutions; the paper frames the plateau as a persistent ceiling, not something the field has already solved.
- This paper is the strongest evidence found in this pass that **LLM/embedding-based routing has a structural accuracy ceiling**, independent of implementation quality — directly relevant to any wrong-routing risk assessment.

### semantic-router (aurelio-labs)
- DOCUMENTED: This library is **not LLM-based routing** — it is embedding-based. Utterances are pre-defined per route, embedded, and incoming queries are classified by nearest-neighbor semantic similarity to those route embeddings — no LLM call, no prompt, in the routing decision itself. Supports OpenAI/Cohere/HuggingFace/TF-IDF encoders. (https://github.com/aurelio-labs/semantic-router, https://docs.aurelio.ai/semantic-router/get-started/introduction)
- This directly answers the brief's question ("is it embedding-based or LLM-based") — it's embedding-based, positioned explicitly as faster/cheaper than "waiting for slow LLM generations to make routing decisions."
- DOCUMENTED misrouting evidence, but for a *related* production system (vLLM Semantic Router, a different project inspired by/using similar embedding-classification ideas, not aurelio-labs' library itself — flagging this distinction): a practitioner analysis reports "at a 20% misrouting rate, semantic routing is difficult to justify," and a specific failure mode where longer/more-detailed prompts are misclassified as higher-complexity than they are, because the embedding classifier reads surface semantic similarity, not task complexity. Also reports "8.2% of queries unnecessarily routed to slow reasoning" in one study, split into "factual queries with misleading complexity signals (3.1%)" and "well-established domain knowledge misclassified as cross-domain (2.8%)." (https://vllm-semantic-router.com/docs/v0.1/training/training-overview/, https://developers.redhat.com/articles/2026/06/02/improve-vllm-semantic-router-accuracy-fine-tuning) — IMPORTANT CAVEAT: these numbers are about vLLM Semantic Router (a CNCF/Red Hat-adjacent project), not confirmed to be the aurelio-labs `semantic-router` package the brief named. Do not conflate the two when citing.
- DOCUMENTED mitigation pattern described for production intent-routing generally: an ensemble — fast heuristics (length/keywords) → lightweight classifier (BERT-class) → safety/PII checks → confidence scoring to decide whether to escalate — i.e., layered fallback rather than a single-shot classifier decision. (https://www.getmaxim.ai/articles/top-5-llm-routing-techniques/)

## Cross-cutting observations (evidence only, no recommendation)

1. Every routing/cascade system found with reported numbers (FrugalGPT, RouteLLM) documents its savings/accuracy jointly — none report a "small model routes with 0% error." All frame routing as a tunable cost/quality tradeoff via an explicit threshold, not a solved classification problem.
2. The one paper specifically about routing *accuracy* as a research question (Routing Plateau) reports that routers systematically underperform an oracle and that the failure concentrates on exactly the harder/ambiguous queries — i.e., routing error is not uniformly distributed, it clusters where the routing decision is hardest and most consequential.
3. Where frameworks document LLM-as-router failure in the wild (CrewAI hierarchical delegation, AutoGen GroupChat speaker selection), the documentation is bug reports and community troubleshooting threads, not benchmarked accuracy figures — i.e., production frameworks acknowledge routing failures qualitatively far more often than they quantify them.
4. The strongest quantified "small model as worker" (not router) result is Anthropic's own Opus 4.5 + Haiku 4.5 subagent number (87.0% vs 74.8%) — worth keeping distinct from routing/triage claims per the task's framing, since it is a different role (parallel worker under a fixed orchestrator, not a classifier deciding where to send work).
5. No source in this pass documents a small model used purely as a **guard/filter** (e.g., pre-screening for safety/policy before a bigger model acts) as a named, benchmarked pattern — the closest analogues found were the "PII detection / safety checks" step mentioned generically in one routing-techniques writeup (not tied to a specific framework) and RouteLLM's threshold mechanism (which filters by predicted quality-need, not by safety).

## Sources consulted (deduplicated)
- https://docs.langchain.com/oss/python/langgraph/graph-api
- https://github.com/johnsosoka/langgraph-model-router
- https://medium.com/@huzaifaali4013399/the-routing-pattern-build-smart-multi-agent-ai-workflows-with-langgraph-44f177aadf7a
- https://openai.github.io/openai-agents-python/handoffs/
- https://developers.openai.com/api/docs/guides/agents/orchestration
- https://openai.github.io/openai-agents-python/multi_agent/
- https://docs.crewai.com/en/learn/hierarchical-process
- https://activewizards.com/blog/hierarchical-ai-agents-a-guide-to-crewai-delegation/
- https://github.com/crewAIInc/crewAI/issues/4783
- https://community.crewai.com/t/manager-agent-delegates-task-to-wrong-agent-in-a-hierarchical-process/3179
- https://towardsdatascience.com/why-crewais-manager-worker-architecture-fails-and-how-to-fix-it/
- https://docs.ag2.ai/latest/docs/user-guide/advanced-concepts/groupchat/groupchat/
- https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/selector-group-chat.html
- https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat_customized/
- https://github.com/microsoft/autogen/issues/3462
- https://www.anthropic.com/claude-opus-4-5-system-card
- https://callsphere.ai/blog/td30-anth-haiku45-subagent (secondary, framing not confirmed against primary Anthropic docs)
- https://arxiv.org/abs/2305.05176 (FrugalGPT)
- https://ar5iv.labs.arxiv.org/html/2305.05176
- https://arxiv.org/abs/2406.18665 (RouteLLM)
- https://github.com/lm-sys/RouteLLM
- https://zilliz.com/learn/routellm-open-source-framework-for-navigate-cost-quality-trade-offs-in-llm-deployment (secondary)
- https://medium.com/@michael.hannecke/implementing-llm-model-routing-a-practical-guide-with-ollama-and-litellm-b62c1562f50f (secondary, unverified attribution)
- https://arxiv.org/pdf/2606.07587 (Routing Plateau)
- https://github.com/aurelio-labs/semantic-router
- https://docs.aurelio.ai/semantic-router/get-started/introduction
- https://vllm-semantic-router.com/docs/v0.1/training/training-overview/ (different project from aurelio-labs — see caveat above)
- https://developers.redhat.com/articles/2026/06/02/improve-vllm-semantic-router-accuracy-fine-tuning
- https://www.getmaxim.ai/articles/top-5-llm-routing-techniques/
