# Who actually pays money to run coding/work agents — mid-2026

Compiled by `vent-buyer` from five parallel research passes (`buy-claude`, `buy-agents`, `buy-agencies`, `buy-orchestration`, `buy-fleets`), each of which further fanned out to sub-scouts and independently spot-checked its own children's highest-stakes claims. Full per-thread detail with additional quotes and sourcing lives in the sibling scratch files (paths noted per section); this file is the synthesis.

**Tagging** (carried through from every source scout): **VERIFIED** = a primary source was personally loaded (by a scout or by me) and the claim is directly readable on it. **DOCUMENTED** = a secondary/traceable source cites it with a link, but the primary was not independently loaded. **REASONED** = inference, explicitly labeled, never presented as fact. Several scouts also used **UNVERIFIED/COULD NOT TRACE** for claims that recur widely but couldn't be pinned to an original source — those are flagged, not used as evidence.

---

## The one-paragraph answer

Real money is moving in five distinct places, and they are not the same market. Individuals and companies pay **Anthropic/vendor subscriptions** ($20–$200/mo per seat) and blow through **enterprise budgets** in months (Uber, Microsoft) chasing productivity, and the dominant complaint is **rate-limit drain and cost unpredictability**, not model quality. A parallel market pays **$20–$200/mo per seat** for autonomous-agent *products* (Devin, Factory, Cursor, Replit, Copilot) with genuinely strong named-customer evidence for some (Devin, Factory, Replit) and vendor-only evidence for others (Cursor). A third market — **agencies selling agent-delivered work to clients** — is real but **essentially unpriced in public**: exactly one firm (Globant) has changed the unit of sale (token-metered subscriptions) and even it won't disclose a number; one firm (LG CNS) has a full case study with scope, timeline, and a cost *ratio*. A fourth market — **agent reliability/orchestration tooling** — is genuinely real and growing fast (Temporal's $300M raise, Braintrust's 5.3x valuation step-up), metered as a separate line item from raw model cost, bought specifically to solve debugging/retry/compliance problems raw API access doesn't touch. And the sharpest finding of the whole research set: practitioners running **fleets of parallel agents** hit a human-attention ceiling at **2–5 actively-supervised agents**, not the 20+ the premise assumed — the unsolved pain is semantic/architectural collision and losing track of which agent needs you, not file conflicts, and it's a real, nameable, quotable population.

---

## 1. Heavy Claude Code users: subscriptions, real spend, real complaints

*Full detail: `buy-claude` → scratchpad `claude-users.md`*

**Pricing (VERIFIED, claude.com/pricing + Anthropic's own Agent SDK billing support article, both directly loaded):**

| Plan | Price | 
|---|---|
| Pro | $17/mo annual, $20/mo monthly |
| Max 5x | $100/mo |
| Max 20x | $200/mo |
| Team Standard / Premium | $25 / $125 per seat/mo (DOCUMENTED, not independently re-verified against a live team pricing page) |

**Company-scale spend (DOCUMENTED via TechCrunch, directly fetched; corroborated by Forbes/Fortune):**
- **Uber**: burned its **entire 2026 AI budget in 4 months** running Claude Code across ~5,000 engineers. $150–$250/engineer/month average; power users $500–$2,000/month. One executive spent **$1,200 in a two-hour demo**. Uber then capped spend at **$1,500/employee/month**. COO Andrew Macdonald: *"it's very hard to draw a line"* between AI usage and new feature spend. Uber's internal leaderboards ranking engineers by usage reportedly incentivized burning more tokens.
- **Microsoft**: cancelled Claude Code for ~5,000 engineers (Experiences and Devices division) after costs hit up to **$2,000/engineer/month** — DOCUMENTED only via aggregators, original Windows Central piece not independently reached.
- Anthropic's own stated aggregate: **~$13/developer/active day**, **$150–$250/developer/month** enterprise-wide, 90% of users under $30/day — DOCUMENTED, original Anthropic source not located, repeated consistently across secondary sources.

**Individual self-reports — VERIFIED:**
- **Simon Willison**: personal Max subscription = **$200/month**. Wrote he'd consider switching to Codex over a jump from $20→$100+ during Anthropic's brief (~2% test cohort) pricing-confusion incident in April 2026.
- **GitHub issue #38335** (karenrebecag, named, dated): 5-hour Claude Code sessions cut to 1–2 hours; tasks that used 20–30% of quota now hit 80–100% in one go, same workload.
- **dev.to (gonewx)**: lost 4 hours of context on an auth refactor to silent compaction: *"It happens silently. No warning. You're deep in flow and suddenly you're talking to a Claude that doesn't know your codebase anymore."*

**Flagged as suspect, explicitly NOT used**: a "10B tokens / $15k API-equivalent vs $800 Max bill" story repeated across ~8 SEO blogs with no traceable original author; a GreekReporter claim of a company "accidentally" spending $500M in one month (couldn't fetch, 2–3 orders of magnitude off every other figure — smells fabricated).

**The pain, in their own words**: rate-limit/quota drain (March 2026 incident — Reddit threads at 300+ comments reported by secondary coverage, not independently verified), cost unpredictability (Uber's COO quote above; Anthropic itself paused a planned June 15 billing split after apparent pushback), and context loss (gonewx's quote above).

**Weakest coverage**: individual X/Reddit self-reports with real handles and dollar figures — Reddit fetch was blocked for this scout's pass (resolved better by `buy-fleets`, see §5).

---

## 2. Devin/Factory/Cursor-style autonomous agent products

*Full detail: `buy-agents` → scratchpad `agent-products.md`*

**Pricing (VERIFIED, all fetched directly, and independently spot-checked a second time by the parent scout — matched exactly):**

| Product | Entry | Mid | Max/Ceiling | Team |
|---|---|---|---|---|
| Devin | Free | $20/mo Pro | $200/mo Max | $80/mo base + $40/seat |
| Factory.ai | — | $20/mo Pro | $200/mo Max | Custom (Business/Enterprise) |
| Cursor | Free (Hobby) | $20/mo Individual | ~$60/~$200 Pro+/Ultra (DOCUMENTED only, not on Cursor's own page) | $40/seat |
| GitHub Copilot | Free | $10/mo Pro | $100/mo Max | $19/seat (Business), $39 (Enterprise) |
| Replit Agent | Free | $20/mo Core (annual) | $95/mo Pro (annual) | Custom |

Entry-level pricing has **converged around $20/mo** with **$200/mo as a common "Max" ceiling** across four of five products. Devin has no public per-ACU rate — a "$500/mo, $2/ACU" figure still circulating traces to a stale April 2025 TechCrunch article.

**Named customers, ranked by evidence strength:**
- **Devin (strongest)** — Nubank (PM: 8–12x efficiency, 20x cost savings, 100k+ data class migrations), Itaú (CTO), Goldman Sachs (CIO Marco Argenti, on record: *"Devin is going to be like our new employee"*) — all VERIFIED via direct fetch.
- **Factory.ai (strongest evidence tier of anything found across all research)** — 5 full case studies with name+title+quote+ROI: Groq (Head of Agents: 3–5x faster dev), Empower, Nav, You.com, Chainguard — all VERIFIED.
- **Replit** — 5 named case studies (Zinus: $140k saved; Firecrown Media: $1.2M/yr savings; SaaStr: $200k/yr savings) — VERIFIED, plus an unprompted honest flag: **SaaStr's Jason Lemkin is also the named victim of Replit Agent's 2025 production-database-deletion incident** — both true and public, reported together, not cherry-picked.
- **Cursor** — ~19 named individuals with titles (Stripe/Collison, Brex/Reggio, Coinbase/Armstrong) but every quote traces only to Cursor's own site, no independent corroboration of the specific stats.
- **GitHub Copilot coding agent** — only 2 verified named customers (Carvana, EY), thin. A broader customer roster was spot-checked (Trimble) and correctly excluded — it's autocomplete-only, not agent-relevant.

**Discipline note**: every sub-scout independently caught and rejected something rather than passing it through — stale pricing, fabricated SEO stats ("31x faster" with no primary source), an incident it could have hidden, an irrelevant roster entry.

---

## 3. Agencies selling agent-delivered work to clients

*Full detail: `buy-agencies` → scratchpad `agencies.md`*

**This is the sharpest negative finding in the whole research set.** Across 25+ named firms and four independent research lanes, the count of firms publishing **both a named client and a price** for agent-delivered work is **essentially zero**.

The category collapses into three buckets that are constantly conflated:
- **(a) Agency delivers to a client** — the actual question. Real firms exist (Sphere Partners: ~8 named client execs; Made By Agents: 4 named clients, verified pricing quotes but no dollar figure; KIBO Studios; Thoughtworks × Mechanical Orchard, $148M raised) — **none publish a price.**
- **(b) Company uses agents on its own codebase** — Klarna, Cisco, Nubank, Ramp. This is where almost all the impressive published numbers live. **It is not the question.**
- **(c) System integrator resells/enables a vendor's agent** — ~$250M in vendor partner money (Anthropic's $100M Claude Partner Network, OpenAI's $150M Partner Network, cohorts including Accenture/BCG/McKinsey/PwC). **Enablement, not delivery.**

**The two exceptions that carry the whole answer:**
- **⭐⭐ Anthropic × LG CNS (VERIFIED, claude.com/customers/lg-cns)** — the single best artifact: a Korean IT services firm modernized a third-party client's 20-year-old system — **2,888 of 2,913 APIs converted (99.1%), 1,340 screens migrated, 7 months, at ~50% the cost of a conventional rebuild** — now productized as "LG CNS Build Factory." This case survived a challenge-and-verify loop (the scout initially couldn't corroborate it, challenged its own child to produce the URL or retract, then verified every figure directly) — the strongest single fact in the report came within one search of being wrongly discarded.
- **⭐ Globant "AI Pods" (VERIFIED, PR Newswire)** — the one firm that changed the *unit of sale*: a token-metered monthly subscription explicitly replacing effort-based billing, named client **YPF** (46 agents). CEO Martin Migoya: *"a radical departure from what anyone else in our industry is offering"* — read carefully, an admission the rest of the industry hasn't followed. **Even this discloses no dollar figure.**

**Real transacting prices exist only in tooling, never delivery**: Greptile ($30/seat + $1/review), CodeRabbit ($24–48/user/mo), Devin ($2.25/ACU, ~$9/agent-hour — the only true agent-time billing found anywhere).

**Evidence that cuts against an "agencies charge a premium" thesis** (given real weight, not buried):
- A peer-reviewed CHI 2026 study: freelancers actively **conceal** AI use from clients to protect their rates — *if it commanded a premium, they'd advertise it.*
- The METR RCT: experienced developers were **19% slower** with AI tools while believing they were 20% faster (though METR itself now calls this result historical/dated).
- Greptile's attempt to charge per-review (because agents multiplied PR volume) triggered a **customer revolt** — a developer logging 571 PRs/month saw his bill jump from $30 to $500+; the market wants agent output but refuses to pay in proportion to it.
- Client price pressure runs toward **discounts**, not premiums (50–70% cut demands, 20–30% actual concessions).

**Bottom line**: agent-delivered agency work is real, not vaporware — but the market prices it by quietly absorbing agent efficiency into existing margins, not by publishing a new, lower, agent-specific rate.

---

## 4. Teams paying for agent reliability/orchestration (not just model access)

*Full detail: `buy-orchestration` → scratchpad `orchestration.md`*

**Yes — real, multi-vendor evidence.** Every vendor researched (LangSmith, Temporal, Braintrust, Langfuse, Helicone, Arize, W&B Weave, AgentOps.ai) meters tracing/evals/orchestration as a **distinct billed line item on top of raw model cost** — a structural signal this is a genuinely separate spend category, independent of any customer quote.

**Standout data point**: **Temporal's $300M Series D at a $5B valuation** (Feb 2026, a16z-led — independently re-verified via GeekWire, Yahoo Finance, TechFundingNews, a16z's own tweet, not just Temporal's site). OpenAI's own VP of App Infrastructure, quoted directly in the raise: *"Durable Execution is a core requirement for modern AI systems."* **1.86 trillion of 9.1 trillion lifetime billed Actions** (Temporal's literal billing unit) are attributed to "AI-native companies" — ties agent workloads to real metered revenue, not just logos.

**Named customers with attributed quotes on WHY** (not vague personas), recurring pattern across unrelated companies/vendors:
- **Debugging rare agent failures via searchable traces**: Notion/Braintrust (AI Lead Sarah Sachs, independently corroborated via podcast/LinkedIn/YouTube), Podium/LangSmith.
- **Retry-isolation and state persistence for long-running agents**: Gradient Labs/Temporal (CTO Neal Lathia), Gorgias/Temporal, Replit/Temporal (*"It's a pretty bad user experience to have the agent get super far into something and then hit a catastrophic error, and you lose everything"*).
- **Evals at scale replacing manual spot-checks**: Canva/Langfuse.
- **Compliance/auditability**: Merck/Langfuse (Chief Data & AI Officer: *"turning black-box models into auditable, optimizable assets"*), SumUp/Langfuse.

**Honest negative flags, not padded**:
- LangSmith's 3 opened case studies (Klarna, Podium, Cisco) have **zero directly-attributed named-person quotes** on reliability specifically — the "why" is vendor third-person copy.
- **No vendor discloses a clean ARR figure** sizeable enough to size the category bottom-up.
- **AgentOps.ai** — the vendor most literally branded "agent reliability" — has essentially no real customer evidence: pricing page 404s, no case-study page exists at all.
- **W&B Weave is a genuine disconfirming data point**: only ~2% of W&B's $50M ARR (Dec 2024) came from Weave specifically, per The Information — even inside a company built for this, the agent-specific product can lag far behind legacy revenue.
- Consolidation is happening fast: 3 of 6 agent-ops vendors researched (Langfuse, Helicone, W&B Weave) have already been acquired — real value, but "independent agent-ops vendor" as a standalone bet is narrowing.

---

## 5. Fleet/swarm runners — the sharpest question, in their own words

*Full detail: `buy-fleets` → scratchpad `fleet-runners.md`, ~190 verbatim quotes cross-checked against raw sources (HN Algolia API, GitHub REST API, PullPush Reddit archive) after WebFetch's own summarizer was independently caught inventing attributions*

**The brief's premise (5–20+ agents) is largely wrong, and that's the finding.** Three independent channels (HN, personal blogs, a roundup of 7 professional fleet-operators) converged **unprompted** on the same number: the practitioner ceiling for **actively supervised** agents is **2–5**, occasionally 8. Above that, people shift to fire-and-forget background work whose only interface is a PR — not hands-on fleet management. People claiming higher numbers are disproportionately tool authors with a motivated interest in the number sounding big (flagged explicitly, not laundered as neutral).

**The wall is human review/attention, not tooling, compute, or file conflicts.** File-level collision (what every orchestrator product sells against — worktrees, Conductor, Claude Squad, Amux) was solved years ago. The unsolved problems: (1) knowing which of N agents needs you *right now*, (2) **semantic/architectural collision that survives clean file merges** (worktrees solve file conflicts; nobody solves two agents independently renaming the same type differently), (3) losing track of where work physically lives.

**Real named practitioners, quoted directly:**

- **Prateek Karnal** (@agent_wrapper, Composio, AI infra engineer) — richest single source, 20+ agents:
  > *"I've been running 20+ Claude Code agents simultaneously across multiple codebases, orchestrated by a parent agent in my home directory."*
  > *"With 15+ agents running, I kept finding sessions that had finished work 20 minutes ago sitting idle."*
  > *"Agents are unreliable narrators."*
  Budgets explicitly: target **$2–5/PR**, flags **$15–30/PR** as the undisciplined failure mode.

- **Scott Chacon** (GitHub co-founder) — the deepest failure account:
  > *"One of a group of parallel agents broke a fundamental part of the testing harness and it looked like a massive regression... I gave up on it almost entirely for a time."*
  Spent **$10–15k**, ~45B tokens, on a months-long project. **At fleet scale you can lose the oracle that tells you whether the fleet is even working** — this is arguably the single deepest finding in the corpus.

- **Peter Steinberger** (PSPDFKit founder) — the anti-worktree dissent:
  > *"I currently have 4 OpenAI subs and 1 Anthropic sub, so my overall costs are around 1k/month for basically unlimited tokens."*
  > *"I experimented with worktrees, PRs but always revert back to [one folder] as it gets stuff done the fastest."* Runtime isolation (dev servers, ports), not file conflicts, was the real cost of worktrees for him — an important counter-signal for anyone building a worktree-based product.

- **Simon Willison** (Django co-creator) — named the review bottleneck first:
  > *"Reached the stage of parallel agent psychosis where I've lost a whole feature."*
  > *"AI-generated code needs to be reviewed, which means the natural bottleneck on all of this is how fast I can review the results."*

- **Dave Schumaker** — quantified the monorepo tax: 750,000+ `node_modules` files make a new worktree take **10+ minutes** for a 5-minute task; built a hand-rolled 6-slot warm-worktree pool CLI, and reports colleagues **independently built the same tool** — the strongest "everyone hand-rolls the same missing thing" signal in the corpus.

- **xinhat** (author, Centurion scheduler): built a resource scheduler after Anthropic closed his feature request as NOT_PLANNED — *"Claude Code has zero cross-session resource awareness... Spawn five parallel sessions on a 16 GB Mac Mini and you get OOM kills."*

- **Geoffrey Huntley** (Ralph technique): *"Cost of a $50k USD contract, delivered, MVP, tested + reviewed with [Ralph]: $297 USD."* — extreme low end of the cost distribution.

**Dollar costs, more first-person figures**: bakies (HN) — *"$40-$60 [per conversation], the long ones with multiple compactions get to $100+"*; solenoid0937 (HN) — *"$1k in tokens every day is easy to hit"*; Khadin Akbar (Indie Hackers) — *"I used $30,983 of AI tokens last month in Claude Code on $200/mo plan"*; Andrew Shu — forced to consider running **2+ Max 20x subscriptions simultaneously** once parallel agents pushed his utilization from 16% to 45%+.

**What they wish existed**: *"The full stack — agent orchestration, window management, and resource isolation in a single integrated product — doesn't exist."* (Alex Lavaee, "nobody owns the full stack"). Beefin (Amux author): wants agents treated like `htop` processes — visible resource usage, kill/restart the expensive ones.

**Honest gaps stated plainly**: Reddit unreachable live in this harness; its only working archive (PullPush) stops 2025-05-19, so Reddit quotes are real and verbatim but dated 2024-09→2025-05, not mid-2026 — stated rather than faked. X/Twitter almost entirely unloadable; most X-handle quotes actually trace to the person's own blog, flagged inline.

---

## Cross-cutting reads

1. **The pain that people already pay to solve, ranked by evidence strength**: (1) cost unpredictability/rate-limit drain at the subscription layer (Uber, Microsoft, the March 2026 incident) — companies are already capping spend rather than solving the underlying problem; (2) reliability/debugging at the orchestration layer (Temporal, Braintrust, Langfuse) — a real, separately-metered, fast-growing spend category; (3) human-attention exhaustion at the fleet layer (Karnal, Chacon, Steinberger) — real, quotable, currently solved with hand-rolled bash scripts and tmux, not a product.

2. **"Nobody owns the full stack" is a claim made independently in two different research threads** — once by an orchestration-tooling researcher (agent-ops vendors solve tracing/evals but not fleet-level supervision) and once, verbatim, by a fleet practitioner (Alex Lavaee: agent orchestration + window management + resource isolation in one product doesn't exist). This convergence, from two unrelated angles, is the strongest single signal for where a gap might be.

3. **Worktrees are both the default answer and a documented irritant** — solving file collision but breaking dev servers, hot-reload, `.env` files, and submodules, and doing nothing for semantic/architectural collision. At least one serious practitioner (Steinberger) rejected them entirely. Any product betting purely on worktree isolation is betting on a partially-solved, partially-rejected mechanism.

4. **The concealment finding (agencies hiding AI use from clients) and the fleet-scale finding (2–5 is the real ceiling) both puncture parts of the popular narrative** — this research set was structured to let scouts report negative/thin findings rather than pad them, and in both cases the negative finding is more informative than a positive one would have been.

5. **Confidence is uneven across sections, by design of the tagging discipline**: §1 and §5 lean on VERIFIED first-person quotes; §2 is strong on Devin/Factory/Replit and weaker on Cursor/Copilot; §3's central finding is a verified *absence*; §4 is strong on pricing structure and named customers but has no vendor-disclosed ARR anywhere. Treat confidence per-claim via its tag, not per-section.
