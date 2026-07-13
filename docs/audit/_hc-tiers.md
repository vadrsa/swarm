# Cheap-tier roster for Build 2b

Live verification task, run 2026-07-13. Every row below was fetched today by
a child agent from the vendor's own docs (or, where noted, corroborated by a
secondary aggregator because the primary page didn't carry that field).
Access date for every citation in this document is **2026-07-13** unless
stated otherwise. Do not treat any of this as stable beyond today — see each
row's falsifier.

This roster exists to pick 2-3 CHEAP arms for a follow-on eval (Build 2b) of
the fleet experiment in this repo. Requirement, non-negotiable: **tool/function
calling support**, since Build 2b agents must drive tools. Reachability via
opencode (checked against models.dev, since opencode's own docs don't publish
a static provider list) is a strong preference, not yet confirmed a hard gate.

---

## Part 1 — verified rows

### DeepSeek

| Model ID | Input $/1M | Output $/1M | Cache hit | Context | Tool calling | opencode/models.dev |
|---|---|---|---|---|---|---|
| `deepseek-v4-flash` (cheap/non-thinking tier) | $0.14 | $0.28 | $0.0028 (98% off) | 1,000,000 in / 384K max out | **Yes** | Listed on models.dev as `deepseek-v4-flash`, `tool_call: true` |
| `deepseek-v4-pro` (for reference, not cheap tier) | $0.435 | $0.87 | $0.003625 | same family | Yes | Listed |

Source: `api-docs.deepseek.com` pricing page, fetched twice independently by
`hc-tiers-deepseek`, consistent both times. **Confirms `_hc-price.md`'s
existing DeepSeek V4 Flash row — no drift.**

Note: the legacy `deepseek-chat` / `deepseek-reasoner` aliases are still live
today but scheduled to retire **2026-07-24 15:59 UTC** (11 days from today),
after which they route to `deepseek-v4-flash`'s non-thinking/thinking modes.
This matches the prior audit's finding — confirmed still accurate, not stale.
models.dev lists both the new IDs and the legacy aliases side by side right
now.

Discarded as untrustworthy: several WebSearch hits on SEO-farm domains
(haimaker.ai, aimadetools.com, bswen.com, devtk.ai, pi.dev) made
opencode-integration claims about `deepseek-v4-flash` — not cited, content-mill
pattern, no vendor or maintainer authority.

Falsifier: re-fetch `api-docs.deepseek.com` pricing and models.dev's DeepSeek
provider entry any time after 2026-07-24 — the alias retirement crosses that
date inside Build 2b's likely runway.

---

### Qwen (Alibaba Cloud Model Studio)

| Model ID | Input $/1M | Output $/1M | Context | Tool calling | opencode/models.dev |
|---|---|---|---|---|---|
| `qwen3-coder-flash` (snapshot `qwen3-coder-flash-2025-07-28`) | $0.30 (0-32K) – $0.50 (32K-128K) | $1.50 (0-32K) – $2.50 (32K-128K) | UNVERIFIED on vendor page (see below) | UNVERIFIED on vendor page | Listed as `alibaba/qwen3-coder-flash`, context **1,000,000**, `tool_call: true`, price shown as **$0.20/$0.97** |

Source: `alibabacloud.com/help/en/model-studio/model-pricing`, fetched
directly by `hc-tiers-qwen`. This is the cheapest *coder-branded* current
Qwen tier — legacy `qwen-coder-turbo` ($0.287/$0.861) is superseded and not
cheaper on a like-for-like basis; plain (non-coder) `qwen-flash` is cheaper
still but isn't the coder tier Build 2b would want for agentic coding tasks.

**Discrepancy, not reconciled:** models.dev's price for `qwen3-coder-flash`
($0.20/$0.97) does not match Alibaba's own tiered pricing page ($0.30-0.50 /
$1.50-2.50). Treat Alibaba's own page as authoritative for pricing since it's
the primary source; models.dev's number may reflect a different region,
discount tier, or stale scrape — **flagged, not silently averaged.**

UNVERIFIED (child could not confirm via direct fetch, page likely
JS-rendered/paginated beyond WebFetch's reach):
- Exact context window for `qwen3-coder-flash` specifically (models.dev claims
  1M; Alibaba's model-family page suggests "256K native / 1M extendable" at
  the family level, not confirmed per-snapshot).
- Explicit "Yes" for tool-calling on Alibaba's own capability page for this
  specific snapshot (models.dev says yes; not independently confirmed on
  vendor docs).

Falsifier: a successful direct fetch of `alibabacloud.com/help/en/model-studio/models`
that surfaces `qwen3-coder-flash`'s row and contradicts the context/tool-call
claims above would supersede this entry.

---

### Kimi (Moonshot AI)

| Model ID | Input $/1M | Output $/1M | Cache hit | Context | Tool calling |
|---|---|---|---|---|---|
| `kimi-k2.5` | **$0.60** | **$3.00** | $0.10 | 262,144 | Yes |
| `kimi-k2.7-code` | $0.95 | $4.00 | $0.19 | 262,144 | Yes |
| `kimi-k2.6` | $0.95 | $4.00 | $0.16 | 262,144 | Yes |
| `kimi-k2.7-code-highspeed` | $1.90 | $8.00 | ~$0.38 (secondary-source only) | 262,144 (assumed same family) | Yes |

Source: `platform.kimi.ai/docs/pricing` index + per-model sub-pages, fetched
directly by `hc-tiers-kimi` (not aggregators, for the k2.5/k2.6/k2.7 rows).

**This is a correction to the roster, not just a confirmation:** the prior
audit (`_hc-price.md`) only priced `kimi-k2.7-code` ($0.95/$4.00) as "Kimi's
current flagship." That's real but **not the cheapest Kimi tier** — `kimi-k2.5`
at $0.60/$3.00 (37% cheaper on both legs) is a distinct, currently-live,
tool-calling-capable tier that the prior audit didn't surface. This is the
Kimi row Build 2b should use if picking Kimi.

The `HighSpeed` variant's exact price could not be primary-source-confirmed
(guessed URL path 404'd); the $1.90/$8.00 figure is **secondary-source-confirmed**
(OpenRouter + aggregators converging on the same number), not vendor-primary.
Legacy `moonshot-v1-{8k,32k,128k}` line is smaller-context, tool-calling
undocumented on the pricing page — not a Build 2b candidate.

models.dev lists `moonshotai/*` including `kimi-k2.7-code-highspeed`,
`kimi-k2.6`, `kimi-k2.5`, `kimi-k2-thinking(-turbo)` — registry presence
confirmed for opencode reachability, **but pricing fields on models.dev show
$0.00/$0.00 for several of these rows** (a data-population gap on models.dev's
side, not real free pricing — official Kimi docs used as source of truth for
price instead).

Falsifier: re-fetch `platform.kimi.ai/docs/pricing/chat-k25.md` if a new
lite/flash Kimi tier is announced, or if HighSpeed's price needs
primary-source confirmation before relying on it for a cost model.

---

### GLM (Zhipu / Z.ai)

| Model ID | Input $/1M | Output $/1M | Cache | Context | Tool calling |
|---|---|---|---|---|---|
| `glm-4.7-flashx` | $0.06–$0.07 (page shows minor variance between fetches, likely rounding) | $0.40 | $0.01 cached | ~200K (third-party corroborated, not on primary pricing page) | Yes (third-party corroborated — agentic/coding-focused model) |
| `glm-4.7-flash` / `glm-4.5-flash` | **free** | **free** | — | ~200K | Yes (third-party corroborated) |
| GLM-4.6 (PAYG, flagship, for reference) | $0.60 | $2.20 | — | — | Yes |

Source: `docs.z.ai/guides/overview/pricing`, fetched twice by
`hc-tiers-glm-minimax` (once for the full table, once targeted at the
Flash/FlashX rows specifically) — the two fetches showed $0.06 vs $0.07 for
FlashX input, flagged as likely page rounding/formatting noise rather than
a real price change. Context window and tool-calling for FlashX/Flash are
**not stated on the primary pricing page** — corroborated via WebSearch
against OpenRouter/pricepertoken/artificialanalysis, so treat those two
fields as secondary-source, not primary-verified.

**This is new information vs. `_hc-price.md`:** the prior audit only priced
GLM-4.6/5/5.1 flagship PAYG tiers ($0.60+/1M and up). It did not know a
GLM-4.7-FlashX tier exists at **~$0.06-0.07/$0.40 per 1M** — an order of
magnitude cheaper than the GLM-4.6 row that document's cost model leaned on.
If GLM-4.7-FlashX holds up under a real eval, it's a materially cheaper anchor
than the GLM-4.6 figure used throughout `_hc-price.md`'s Part 2 cost tables.

Falsifier: re-fetch `docs.z.ai/guides/overview/pricing` and resolve the
$0.06/$0.07 discrepancy; independently confirm context window and tool-calling
on a Zhipu-owned page (not just third-party) before betting a cost model on it.

---

### MiniMax

| Model ID | Input $/1M | Output $/1M | Cache read | Context | Tool calling |
|---|---|---|---|---|---|
| `MiniMax-M3` (≤512K input) | $0.30 | $1.20 | $0.06 | 1,048,576 (512K billing breakpoint) | Yes (+ vision, third-party corroborated) |
| `MiniMax-M3` (>512K input) | $0.60 | $2.40 | $0.12 | same | Yes |

Source: `platform.minimax.io/docs/guides/pricing-paygo`, fetched twice by
`hc-tiers-glm-minimax`. **Confirms `_hc-price.md`'s existing MiniMax-M3 row
exactly — no drift.** Explicitly checked for anything cheaper than M3 (a
"lite"/"flash" MiniMax tier) — **none exists**; M3 is MiniMax's price floor
today. models.dev's list-price framing (~50% promo off $0.60/$2.40) is
consistent with this.

Falsifier: re-check `platform.minimax.io/docs/guides/pricing-paygo` if
MiniMax announces a new tier below M3.

---

## Part 2 — cross-check vs. `docs/audit/_hc-price.md` Part 2

| Row in `_hc-price.md` | Prior figure | Live figure (today) | Verdict |
|---|---|---|---|
| DeepSeek V4 Flash | $0.14 / $0.28 | $0.14 / $0.28 | **No drift, confirmed.** |
| MiniMax-M3 (≤512K / >512K) | $0.30/$1.20, $0.60/$2.40 | $0.30/$1.20, $0.60/$2.40 | **No drift, confirmed.** |
| GLM-4.6 (PAYG) | $0.60 / $2.20 | $0.60 / $2.20 | **No drift, confirmed** — but see below: not the cheap tier. |
| GLM-5 / GLM-5.1 | $1.00/$3.20, $1.40/$4.40 | not re-checked (out of scope — flagships, not cheap tier) | Not re-verified this pass. |
| Qwen3.7-Plus | $0.40 / $1.60 | not re-checked (task targeted the cheap coder tier, not Plus) | Not re-verified this pass. |
| Kimi K2.7 Code | $0.95 / $4.00, cached $0.19 | $0.95 / $4.00, cached $0.19 | **No drift, confirmed** — but see below: not the cheapest Kimi tier. |
| Kimi K2.7 Code HighSpeed | $1.90 / $8.00, cached $0.38 | $1.90 / $8.00, cached ~$0.38 (secondary-source only this pass) | Consistent, but downgraded to secondary-source confidence today. |

**Corrections to note, not drift but gaps:**
1. `_hc-price.md` used GLM-4.6 ($0.60/$2.20) as its "cheap foreign anchor" for
   coding-capable models. A **GLM-4.7-FlashX** tier exists today at roughly
   **$0.06-0.07/$0.40** per 1M — 8-9× cheaper on input, 5.5× cheaper on
   output than the anchor that document's cost tables used. Any cost model
   built on `_hc-price.md`'s GLM-4.6 figures understates the achievable
   foreign-model discount if FlashX is viable for the workload.
2. `_hc-price.md` priced Kimi only at the K2.7 Code tier. **Kimi K2.5** exists
   today at $0.60/$3.00 (tool-calling capable) — 37% cheaper than the row that
   document used, and not previously in the roster at all.

---

## Part 3 — UNVERIFIED (explicit, not guessed)

- Qwen3-coder-flash exact context window and primary-source tool-calling
  confirmation (Alibaba's own capability page didn't surface this snapshot).
- GLM-4.7-FlashX / GLM-4.7-Flash / GLM-4.5-Flash context window and
  tool-calling — corroborated only by third-party aggregators, not a
  Zhipu-owned capability page.
- Kimi HighSpeed variant's exact price — secondary-source-confirmed
  (OpenRouter + aggregators), not primary-vendor-confirmed (guessed doc URL
  404'd).
- GLM-5 / GLM-5.1 and Qwen3.7-Plus prices — not re-verified this pass (out of
  scope for a *cheap-tier* roster; carried forward unchanged from
  `_hc-price.md` without a fresh fetch).
- opencode's own docs (not models.dev) were not independently checked for any
  vendor — all "opencode reachability" claims in this document are inferred
  from **models.dev registry presence**, which is a reasonable but indirect
  proxy (opencode is known to consume models.dev's registry, but this pass
  did not fetch opencode's own provider config to confirm live routing).
- models.dev's own pricing fields are unreliable for several rows in this
  audit (multiple $0.00/$0.00 placeholder entries for Kimi tiers, and a
  discrepancy vs. Alibaba's own Qwen pricing) — registry **presence** is
  usable as a reachability signal, registry **price** is not trustworthy and
  vendor docs were used as source of truth throughout.

---

## Part 4 — REASONED recommendation: 2-3 arms for Build 2b

Ranked by cheapest-per-capability among tool-calling-capable, models.dev-listed
(opencode-reachable) candidates:

**1. `deepseek-v4-flash` — $0.14 / $0.28 per 1M, 1M context, tool-calling: yes.**
   Cheapest fully-primary-verified, no-caveat row in this entire roster.
   Confirmed twice independently, matches the prior audit exactly, and is the
   only candidate with zero open UNVERIFIED flags on price/context/tools.
   **Top pick — lowest risk, lowest price, largest context.**

**2. `kimi-k2.5` — $0.60 / $3.00 per 1M (cache hit $0.10), 262K context,
   tool-calling: yes.** Materially cheaper than the K2.7 Code tier this
   swarm has already been discussing, fully primary-source-verified today,
   and gives Build 2b a second model *family* (not just a second DeepSeek
   price point) — useful if the eval wants to separate "cheap tier" effects
   from "DeepSeek specifically" effects.

**3. `glm-4.7-flashx` — ~$0.06-0.07 / $0.40 per 1M — conditional pick.**
   Would be the outright cheapest arm by a wide margin if its context window
   and tool-calling are confirmed on a Zhipu-primary page (currently only
   third-party corroborated — see UNVERIFIED above). Recommend a cheap
   one-turn smoke test (a single tool-calling round-trip against the live
   API) before committing it as a full Build 2b arm, rather than either
   trusting third-party corroboration blindly or discarding a genuinely
   attractive price point.

**Not recommended for Build 2b:** Qwen3-coder-flash — real price is likely
competitive but has two open UNVERIFIED fields (context, tool-calling) on the
one thing Build 2b cannot compromise on (tool use), and a live discrepancy
between vendor and models.dev pricing that wasn't resolved this pass. Worth
revisiting once the vendor's own capability page can be directly confirmed,
not worth staking an eval arm on today.

---

## Sources (all fetched 2026-07-13 by child agents, this pass)

- `api-docs.deepseek.com` (pricing page) — via `hc-tiers-deepseek`
- `models.dev` — via all four children, cross-checked
- `alibabacloud.com/help/en/model-studio/model-pricing` — via `hc-tiers-qwen`
- `platform.kimi.ai/docs/pricing` + per-model sub-pages — via `hc-tiers-kimi`
- `docs.z.ai/guides/overview/pricing` — via `hc-tiers-glm-minimax`
- `platform.minimax.io/docs/guides/pricing-paygo` — via `hc-tiers-glm-minimax`
- Secondary/corroborating only (never sole source for a verified row):
  OpenRouter, pricepertoken, artificialanalysis
