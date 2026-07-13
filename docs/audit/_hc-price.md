# Cost measurement — status quo, foreign prices, comparison

**Author:** `hc-price`. Numbers with sources, no design. Every figure tagged
**MEASURED** (I computed it from files on this machine), **DOCUMENTED** (a
named external source states it), or **ASSUMED** (I chose it; falsifiable,
stated explicitly).

**Method (Part 1):** Claude Code writes one `.jsonl` transcript per session
under `~/.claude/projects/-Users-vadrsa-git-swarm/`, one line per turn, with a
`usage` object on each assistant message (`input_tokens`, `output_tokens`,
`cache_creation_input_tokens`, `cache_read_input_tokens`) and a `timestamp`.
Agent name → transcript file is not recorded anywhere in `.swarm/` — I
recovered it by grepping each `.jsonl` for the literal spawn-prompt phrase
`agent \`<name>\`` (the phrasing `swarm spawn` stamps into the first system
message). Several agents resumed across multiple transcript files (context
compaction / restore) — I summed tokens across **all** matching files per
agent, matched via the exact spawn-phrase grep, confirmed by hand for one
agent (`hc-price`, this file, is its own transcript
`315f7c41-0f19-40a0-b3a9-0baa82968f77.jsonl`).

**Wall-clock has two different honest meanings here, and they differ by
10–20×.** *Calendar span* (last timestamp − first timestamp) includes hours
an agent sat idle waiting on a child or a parent's mailbox — herdr panes are
long-lived and cheap to leave open, so most of a "session" is silence, not
tokens. *Active time* (sum of inter-message gaps, each capped at 120s to
exclude idle waiting) is what a turn actually cost in wall-clock. I report
both; **$/active-hour is the meaningful unit for "what does compute cost,"
$/calendar-hour is the meaningful unit for "what does a pane cost to leave
open."** Neither is more "real" than the other — they answer different
questions.

---

## PART 1 — The status quo, measured

### Anthropic API prices used (DOCUMENTED, `platform.claude.com/docs/en/about-claude/pricing`, fetched 2026-07-13)

| Model | Input $/1M | Output $/1M | Cache write (5m) | Cache read |
|---|---|---|---|---|
| Claude Opus 4.8 (`claude-opus-4-8`) | $5.00 | $25.00 | $6.25 | $0.50 |
| Claude Sonnet 5 (`claude-sonnet-5`) — **promo thru 2026-08-31** | $2.00 | $10.00 | $2.50 | $0.20 |
| Claude Sonnet 5 — standard from 2026-09-01 | $3.00 | $15.00 | $3.75 | $0.30 |
| Claude Haiku 4.5 | $1.00 | $5.00 | $1.25 | $0.10 |

Sonnet pricing is **promotional and expires 2026-09-01** — any projection past
that date should use $3/$15, not $2/$10. All dollar figures below use the
current promo rate since that's what's actually billing today.

`claude-fable-5` (used by `harness-contractor`, this tree's operator) has
**no published per-token price** on Anthropic's public pricing page — it does
not appear as a priced SKU. I could not find a rate card. Any Fable $/hour
figure below is **ASSUMED = same rate as Opus 4.8** (Fable is the newest,
presumably-largest tier, so this is a floor, not a guess at its real price —
flagged, not measured).

### Measured sessions, this swarm, today (2026-07-13) and yesterday

Grep-matched by exact spawn phrase across all resumed transcript files per
agent name (MEASURED):

| Agent | Model | Total tokens (in+out+cache) | Active min | API-equiv $ | $/active-hr | $/calendar-hr |
|---|---|---:|---:|---:|---:|---:|
| hc-price (self) | Sonnet 5 | 1,274,436 | 2.1 | $0.62 | **$17.62** | $20.56 |
| hc-eval | Sonnet 5† | 850,051 | 5.8 | $0.84 | $8.72 | $7.66 |
| hc-field | Sonnet 5 | 3,098,922 | 5.2 | $1.54 | $17.78 | $15.41 |
| hc-industry | Sonnet 5 | 3,904,858 | 10.8 | $1.86 | $10.33 | $9.29 |
| hc-mech | Sonnet 5 | 2,810,018 | 5.7 | $1.11 | $11.66 | $10.07 |
| hc-slm | Sonnet 5 | 8,908,440 | 6.1 | $4.02 | $39.58 | $40.24 |
| hc-red | Opus 4.8 | 22,570,884 | 19.3 | $26.38 | **$82.00** | $79.93 |
| trigger-scout | Sonnet 5 | 175,790,501 | 112.2 | $49.30 | $26.36 | $2.48 |
| model-fit | Opus 4.8‡ | 30,839,823 | 51.3 | $32.17 | $37.63 | $1.87 |

† hc-eval's transcript mixes `claude-haiku-4-5` and `claude-sonnet-5` messages;
priced entirely at Sonnet rate (the dominant model by message count) — a
minor overstatement.
‡ model-fit's transcript mixes Opus and Sonnet across its 5 resumed files;
priced entirely at Opus rate (worst case, overstatement) since I did not
split token counts by model per-message for this one.

**Blended average, all 9 sampled agents:**
- **Sonnet leaves/scouts: $18.86/active-hour** (mean of 7 samples, range
  $8.72–$39.58 — nearly 5× spread depending on how output-heavy the task was)
- **Opus seats: $59.81/active-hour** (mean of 2 samples, range $37.63–$82.00)

The spread is real and driven by output-token intensity (`hc-red` and
`hc-slm` both wrote long documents; `hc-eval` and `hc-industry` did lighter,
more read-heavy work) — there is no single "true" per-model rate, only a
task-dependent one. Treat $18.86 and $59.81 as this sample's central
tendency, not a physical constant.

**Idle time dwarfs active time.** `trigger-scout` and `model-fit` each show
~17–20 hours of *calendar* span but only 51–112 *active* minutes — under 10%
duty cycle. This means: (a) leaving a swarm's panes open overnight costs
essentially nothing beyond the occasional Stop-hook re-check, and (b)
"cost per agent-hour" is meaningless without specifying which hour you mean.
A 10-agent tree running 1 active-hour each but left open for a full calendar
day costs the same in tokens as a tree that closes the moment work stops —
the token bill is driven by active minutes, not pane-open duration.

### Per-agent-hour and 10-agent-tree headline numbers

Using the blended averages above, for **1 active hour of real work**:

- Sonnet leaf: **$18.86/hour** (MEASURED, blended)
- Opus seat: **$59.81/hour** (MEASURED, blended)

For a **10-agent tree, 1 active hour each, all-Claude, all seats billing
simultaneously** (ASSUMED shape: 1 Opus operator + 3 Opus seats + 6 Sonnet
leaves — matches this swarm's actual proportions roughly, see `swarm ps` in
the session: 1 fable coordinator, several sonnet leaves, occasional opus for
`hc-red`/`model-fit`-style review work):

**10-agent tree, 1 active-hour each ≈ $352/hour** (MEASURED rates × ASSUMED
tree shape: 4 × $59.81 + 6 × $18.86 = $239.24 + $113.16 = $352.40)

This is a **ceiling**, not a typical bill: it assumes every one of the 10
agents is in its active-burst minute simultaneously, which the measured duty
cycle (well under 10% for long-lived scouts) shows rarely happens in
practice. A more realistic multi-hour tree, given the observed ~10% duty
cycle for scout-tier agents, would cost something closer to **$35–50 for a
full calendar hour** of a 10-agent tree left open — but that number depends
entirely on how synchronized the agents' bursts are, which I have not
modeled; flagged as **ASSUMED**, not measured.

### Subscription vs. API — the number that actually binds today

This swarm does **not** pay per-token API prices. It runs on a Claude
subscription with a **weekly usage limit**. From the operator's own journal
(`.swarm/journal/operator.md:200`, dated 2026-07-12, MEASURED — direct quote):

> "Also: weekly limit at 82% — the swarm's token appetite is real."

That entry also documents a **concrete failure mode this pricing model
creates that pure API billing would not**: a session mid-turn hit a
*session*-level limit ("session limit resets 11:10pm"), the Stop hook never
fired, no event fact was written, queued mail sat undelivered for ~2 hours,
and the pane froze until manually double-doorbelled back to life. Under
metered API billing this would just be a bigger invoice; under a
subscription with hard limits it is an **outage** — the swarm stops
producing, silently, with no automatic recovery. This is a structural
consequence of subscription pricing, not a bug in any one number above.

**So: the API-equivalent dollar figures in this document ($18.86/hr Sonnet,
$59.81/hr Opus, ~$352/hr for a synchronized 10-agent burst) are what the
same token consumption would cost if metered.** What actually happened this
week is: the swarm burned enough tokens to put the operator's account at
82% of its weekly cap (DOCUMENTED, operator's own words) — i.e., the
subscription is the binding constraint, not dollars, and the two units
(dollars vs. %-of-weekly-cap) currently have no published conversion rate
between them (Anthropic does not document how many API-equivalent dollars a
Claude subscription's weekly cap represents) — flagged as an **open
unknown**, not guessed at.

---

## PART 2 — Foreign model prices, verified current

Verified via WebSearch against vendor pricing pages, 2026-07-13
(DOCUMENTED). All figures per 1M tokens.

| Model | Input $/1M | Output $/1M | Cache notes | Source |
|---|---|---|---|---|
| DeepSeek V4 Flash | $0.14 | $0.28 | Cache hit $0.0028 (98% off) | api-docs.deepseek.com/quick_start/pricing |
| DeepSeek V4 Pro | $0.435 | $0.87 | Cache hit $0.003625 | same |
| GLM-4.6 (pay-as-you-go) | $0.60 | $2.20 | — | docs.z.ai/guides/overview/pricing |
| GLM-5 (current flagship PAYG) | $1.00 | $3.20 | — | same |
| GLM-5.1 (newest PAYG) | $1.40 | $4.40 | — | same |
| GLM Coding Plan — Lite | $18/mo ($12.60 promo) | — | ~80 prompts/5h, ~400/wk | z.ai/subscribe |
| GLM Coding Plan — Pro | $72/mo ($50.40 promo) | — | ~400 prompts/5h, ~2000/wk | same |
| GLM Coding Plan — Max | $160/mo ($112 promo) | — | ~1600 prompts/5h, ~8000/wk | same |
| Qwen3.7-Plus (current "Plus" flagship) | $0.40 | $1.60 | 20% promo live | alibabacloud.com/help/en/model-studio/model-pricing |
| Qwen-Max (top flagship) | $1.60 | $6.40 | 50% batch discount | same |
| Kimi K2.7 Code (current flagship) | $0.95 | $4.00 | Cached $0.19 | platform.kimi.ai/docs/pricing/chat-k27-code |
| Kimi K2.7 Code — HighSpeed | $1.90 | $8.00 | Cached $0.38 | same |
| MiniMax-M3 (≤512K input) | $0.30 | $1.20 | Cache read $0.06 | platform.minimax.io/docs/guides/pricing-paygo |
| MiniMax-M3 (>512K input) | $0.60 | $2.40 | Cache read $0.12 | same |

**DeepSeek chat/reasoner naming note:** the legacy `deepseek-chat` /
`deepseek-reasoner` aliases are retiring 2026-07-24 (this week, per vendor
docs) and route to V4 Flash non-thinking/thinking modes respectively — so
"deepseek chat + reasoner" pricing today **is** the V4 Flash row above, not a
separate SKU.

### Drift vs. `docs/design/FLEET.md:325-330` (written 2026-07-11, "re-verify at build")

| Model | FLEET.md figure | Current verified | Drift |
|---|---|---|---|
| DeepSeek V4 Flash | $0.14 / $0.28 | $0.14 / $0.28 | **none** |
| MiniMax M2 | $0.26 / $1.02 | M3 (successor) $0.30 / $1.20 | **model superseded**, price ~+15%/+18% for the new flagship |
| GLM-4.6 | $0.43 / $1.74 | $0.60 / $2.20 | **+40% / +26%**, and GLM-5/5.1 now exist above it |
| Qwen Plus | $0.40 / $1.60 | $0.40 / $1.60 | **none** (20% promo currently layered on top, not reflected in list price) |
| Kimi K2.6 | $0.95 / $4.00 | K2.7 Code $0.95 / $4.00 | **model version advanced, headline price held** |

Also worth flagging: FLEET.md's own Opus anchor line ("~$15/$75") is **itself
now stale** — current Opus 4.8 is $5/$25 (see Part 1 table above), a ~3×
drop. Two years of "re-verify at build" comments compound; this document is
itself subject to the same decay and should be re-verified before being
treated as current beyond its write date.

### Multiplier vs. Opus and vs. Sonnet (MEASURED, computed from tables above)

Using DeepSeek V4 Flash as the cheapest foreign anchor:

| Comparison | Input multiplier | Output multiplier |
|---|---:|---:|
| Sonnet 5 vs. DeepSeek V4 Flash | 14.3× | 35.7× |
| Opus 4.8 vs. DeepSeek V4 Flash | 35.7× | 89.3× |

Using GLM-4.6 (a more realistic "similarly-capable coding model" anchor,
per operator's own prior reachability note that GLM is already keyed in
opencode):

| Comparison | Input multiplier | Output multiplier |
|---|---:|---:|
| Sonnet 5 vs. GLM-4.6 | 3.3× | 4.5× |
| Opus 4.8 vs. GLM-4.6 | 8.3× | 11.4× |

---

## PART 3 — The comparison that matters

**Same 10-agent tree shape as Part 1** (1 operator + 3 seats + 6 leaves),
**1 active-hour of real work per agent**, three configs. Claude-side rates
are MEASURED (Part 1 blended averages); foreign-side rates are DOCUMENTED
(Part 2) but **applied to an ASSUMED token volume** — see caveat below, this
is the load-bearing unknown of this whole part.

| Config | Operator | Seats (×3) | Leaves (×6) | $/hour |
|---|---|---|---|---:|
| **All-Claude** | Opus 4.8 ($59.81/hr) | Opus 4.8 ($59.81/hr each) | Sonnet 5 ($18.86/hr each) | **$352.40** |
| **Mixed** | Fable (ASSUMED = Opus rate, $59.81/hr) | Opus or foreign, ASSUMED Opus for seats (judgment/coordination role) | Foreign (GLM-4.6, DOCUMENTED price, ASSUMED same token volume as measured Sonnet leaves) | see caveat below |
| **All-foreign-below-operator** | Fable (ASSUMED = Opus rate, $59.81/hr) | Foreign (GLM-4.6) | Foreign (GLM-4.6) | see caveat below |

**Mixed and all-foreign numbers, computed under the stated assumption**
(foreign models consume the **same token volume per task** as the measured
Sonnet/Opus sessions above — i.e., repricing `hc-industry`'s actual measured
token stream at foreign per-token rates rather than assuming a different
volume):

- `hc-industry` (a representative measured Sonnet leaf) consumed tokens at a
  rate that cost $10.33/hr at Sonnet prices. Repricing that **same token
  stream** at GLM-4.6 rates: **$3.02/hr**. At DeepSeek V4 Flash rates:
  **$0.69/hr**.
- Mixed config (Fable operator + Opus seats + GLM leaves, same-volume
  assumption): $59.81 + 3×$59.81 + 6×$3.02 ≈ **$257.5/hour**
- All-foreign-below-operator (Fable operator, GLM seats + GLM leaves, same
  assumption): $59.81 + 9×$3.02 ≈ **$87.0/hour**

### The caveat that matters more than any number above

**Foreign-model token consumption per task is NOT measured in this
document — it is assumed equal to Claude's, and that assumption is very
likely wrong, in an unknown direction.** Different model families tokenize
differently, use different amounts of chain-of-thought/reasoning tokens for
the same task (DeepSeek-reasoner and Kimi's "thinking" variants are
explicitly priced as heavier-output modes), and may need more turns (more
tool-call round-trips, more retries on a weaker model) to reach the same
result — every extra turn multiplies both input and output tokens, not just
adds a constant. A weaker or less steerable model could easily burn 2–5×
the tokens of Sonnet to do the same job, which would erase most or all of
the sticker-price advantage shown above. **I did not run any foreign model
against this swarm's actual tasks, so I have no measured token-volume ratio
to correct with — do not treat the $3.02/hr or $87/hr figures above as
predictions of real cost; treat them only as "what the discount would be
if token consumption were equal," which is the one clean, honest thing
that can be said without a real trial.**

---

## Summary of headline numbers (for the report to harness-contractor)

1. **All-Claude status quo, measured:** Sonnet leaves cost **$18.86/active-hour**
   (blended, MEASURED, 7 samples), Opus seats cost **$59.81/active-hour**
   (blended, MEASURED, 2 samples) — active-hour, not calendar-hour; duty
   cycle in this swarm ran under 10% for long-lived scouts.
2. **10-agent tree ceiling (all bursting simultaneously, all-Claude):**
   **$352/hour**, MEASURED rates × ASSUMED synchronized-tree shape.
3. **Foreign-model discount, same-token-volume assumption (NOT a real-world
   prediction — flagged):** the same 10-agent tree with GLM-4.6 below a
   Fable/Opus operator drops to **~$88–258/hour** depending on how much of
   the seat layer stays on Claude — but this could be wrong by several
   multiples in either direction because foreign token-consumption-per-task
   is unmeasured.
4. **The number that actually constrains this swarm today isn't dollars:**
   operator's own journal, 2026-07-12, `.swarm/journal/operator.md:200`:
   *"weekly limit at 82% — the swarm's token appetite is real."* No
   published conversion exists between subscription-%-used and
   API-equivalent dollars.
