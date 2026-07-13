# LOOP-RED — adversarial review of LOOP.md

**Reviewer:** `hc-red2`, fresh eyes, no access to the author's reasoning process.
My mandate was to refute, not repair. Where a claim survives, I say so and name the
strongest attack that still stands against it. Every citation below was checked
against the artifact it claims to cite, not against the author's paraphrase of it.

**Scope:** LOOP.md in full, cross-checked against HARNESS.md §1-3/§8/§10,
`_hc-ocloop.md`, `_hc-claudeval.md`, `_hc-price.md`, `OPENCODE-PLUGIN.md`, and
`FLEET-EVAL-V3.md`/`FLEET-EVAL.md`/`FLEET-EVAL-V3-RED.md` (the eval sources LOOP.md's
central prediction depends on, which the operator's brief did not name but which
turned out to be load-bearing for surface (i) and (v)).

---

## VERDICT SUMMARY

| Surface | Verdict | One line |
|---|---|---|
| (i) Seat-capability claim | **WOUNDED** | The absorption argument for *protocol* is sound; the judgment half is contaminated by a citation of a **retired v2 finding** (GLM's 35-min hang) presented as a live counterweight, and falsifier 3 is honest but the doc's own prose undercuts it in §4. |
| (ii) Fork-vs-build ruling | **HOLDS**, barely | The trigger design is coherent and the "mostly verified" framing is *mostly* honest (§5 does disclose the gaps), but LOOP.md's own §1/§3 oversell the pump as "VERIFIED: self-ring, two-phase `delivered/`" in a way §5 itself contradicts. |
| (iii) Cost section | **HOLDS** | `_hc-price.md` is faithfully represented; the "capacity buy" framing is the source's own words, not spin invented by LOOP.md. |
| (iv) Affordability-as-goal (§6) | **WOUNDED** | Legitimate as argued, but the doc supplies no limiting principle — nothing in the text stops "the goal requires it to be affordable" from being invoked for the next cost-cutting proposal too. |
| (v) Evidence integrity | **REFUTED as a discipline claim** | Multiple tags misstate their sources, including one that cites a finding the source document explicitly retracted ("No v2 GLM D2 row should be cited again") and one VERIFIED-flavored claim ("verified: self-ring, two-phase delivered/") that its own source tags REASONED/unrun. |

---

## (i) THE SEAT-CAPABILITY CLAIM

### Is the absorption argument circular?

No, not on the protocol half. The move is real: the loop reads `last_words` +
artifact paths and sends them without the model doing anything. That is not
"redefining report down to notification" in the pejorative sense — a
model-authored account was never a duty the *harness* could enforce; what the
harness *can* enforce is that the account, whatever its authorship, reaches the
parent. LOOP.md's own table (§3) is honest about the resulting boundary:
"Model-authored reports remain welcome and better; the floor is no longer zero."
That is a defensible, narrow claim. The attack that it "quietly redefines report
down to notification" lands weakly here — LOOP.md does not claim the auto-digest
*replaces* judgment-bearing reports, only that it replaces silence.

### Is "last words + artifact paths" judgeable, or noise?

This is where the doc is most honest and most exposed simultaneously.
**Falsifier 3 (§9)** is not a fig leaf — it is stated in a form that can actually
fire ("if parents of duty-loop agents measurably re-open pane-reading... absorption
failed its purpose"). Crediting the doc: most self-critical designs bury this kind
of falsifier in a way that can never be observed; this one names a concrete,
collectible signal (parent journals).

But the falsifier's *honesty* does not make the underlying risk small. A digest of
"last assistant words" is exactly what a model produces when it is mid-thought,
not when it is done thinking about how to report — that's precisely the failure
mode the original duty existed to prevent (the eval's own finding: "it knows who
its parent is and does not use the verb," i.e., models *narrate* instead of
*filing*). An auto-captured narration is not obviously better-formed than a
model-authored one; it is just guaranteed to arrive. The doc never argues the
*content* quality of the digest improves — only that its *delivery* becomes
certain. Those are different axes, and LOOP.md's own Build 2 prediction
("D4 journal hard-fails vanish... judgment... is what remains") assumes away the
question of whether a forced-delivery digest of unstructured last-words is legible
enough for a parent to *judge* rather than merely *receive*. That is the strongest
surviving attack even though the surface as a whole is not refuted: **the design
has built certainty of delivery without evidence of legibility**, and conflates
the two under "report."

### Does absorption atrophy the model's incentive to think about reporting?

The doc addresses this only glancingly. PHILOSOPHY §2's incentives-over-guardrails
logic cuts against building a mechanical crutch for a habit models should be
forming — and there is a real risk that once the loop always sends *something*,
a model that could have been trained/prompted into good reporting discipline never
develops it, because the visible symptom (silence) is gone. LOOP.md's own
distinction between protocol and judgment actually makes this worse, not better:
it explicitly says "the loop only bounds [judgment], it does not supply it" for
things like reconciliation — but it does not ask the symmetric question for report
quality itself. If a model that *could* have learned to file real reports never
has to, because the floor is now non-zero, the design has traded a visible failure
(3/7 drops) for an invisible one (7/7 delivered, but declining information content
over time as models learn there's no cost to not trying). This is a plausible,
not measured, failure mode — the doc doesn't measure it and its own falsifier 3
would only catch it if a parent explicitly notices reopening pane-reads, not if
the digest quietly settles into being technically-delivered noise nobody re-opens
panes over because there's nothing to gain by doing so (a parent who stops reading
digests because they're never useful is a silent failure the falsifier as written
would miss).

### Does the protocol/judgment split stay clean, or does judgment contaminate the "protocol seats open" conclusion?

This is where I find the sharpest, evidence-backed problem, detailed fully under
(v) below: **the judgment failures LOOP.md cites as the surviving, unabsorbed
half are themselves unreliable citations.** The GLM `ps`-misread + 4-retry-hang
claim (§2, §4, HARNESS.md §3 citing V3:98-100) is **the v2 finding that
FLEET-EVAL-V3 explicitly retired**: "v2's 'children all died, model hung 35 min,
fragile parent' does NOT reproduce and is retired. It was the rig's empty cwd... No
v2 GLM D2 row should be cited again" (`FLEET-EVAL-V3.md:107-108, 123-124`). LOOP.md
cites this stale finding as a *currently standing* judgment weakness surviving
absorption (§4: "GLM still fails the dead-children case unless the parent watchdog
... catches it" — a prediction built on the retired hang, not on V3's actual
finding, which is "no watchdog... [but] terminated only because its children
delivered" — a different, milder claim: unexercised risk, not a demonstrated
failure). This is a genuine contamination: the "protocol seats open, judgment
seats stay Claude" conclusion leans on a piece of judgment evidence that the
project's own evaluation history disowns. It does not sink the whole claim
(deepseek's 11-minute brief-abandonment is real, at V3:82-83, and the "does not
time-box" judgment gap is genuinely V3-sourced) — but it means the doc's
judgment-side evidence is weaker than presented, at exactly the seam the operator
asked to have attacked hardest.

**Verdict: WOUNDED.** The protocol-absorption logic holds. The judgment-boundary
claim is contaminated by a stale citation that the project's own record says
should not be cited again, and the "judgeable vs. noise" question is asserted
resolved by falsifier 3's existence rather than actually resolved.

---

## (ii) THE FORK-VS-BUILD RULING

### Is "pin and wait for two breaks" viable against ~1 release/1.5 days?

Viable, conditionally, and the doc is honest about the condition: it explicitly
says *"tracking unpinned stock at that velocity is untenable (the pin is not
optional)"* (§5) — i.e., the plan only works because it commits to never
following upstream HEAD, only a frozen point. That is coherent. What is thinner:
the "fork when the pinned surface breaks twice" trigger measures **plugin-surface
breakage**, not **security/CVE pressure** on a version that will age for however
long "twice" takes to accumulate at a ~1.5-day cadence. A pinned version frozen
for months while upstream ships hundreds of commits/week is also frozen against
any security fixes in the *core* (session store, HTTP server) that `_hc-ocloop.md`
§0 already flags as unauthenticated-by-default and world-readable. The doc never
weighs security-patch lag as a cost of pinning — only feature/API drift. That's a
real gap in the trigger design, not fatal to it.

### Is the pinned version re-installable long-term (binary availability)?

LOOP.md does not address this at all, and it should — `_hc-ocloop.md` §2.1 confirms
MIT/no-CLA (so a fork is *legally* re-buildable from source at any point), but
nothing in either document establishes that the specific pinned **binary release**
stays downloadable from whatever distribution channel opencode uses once newer
releases supersede it (a common failure mode for fast-moving OSS: old release
artifacts get pruned, package managers point only at latest, or a version is
yanked). If the pin is a source pin (build from a tagged commit), re-installability
is fine — MIT and a public git history guarantee that. If the pin is a binary/npm
pin, it depends on registry retention that neither document checks. This is an
unflagged gap, not a refutation: the ruling survives IF the pin is understood as
"build from tag," which the doc's own §5 language ("a fork *today* would buy...")
implies but never states outright.

### Does the two-phase pump's own doc admit unrun compositions?

Yes, and LOOP.md **discloses this correctly in one place and misrepresents it in
another** — see (v) below for the exact contradiction between LOOP.md §1/§3's
"VERIFIED: self-ring, two-phase `delivered/`" and OPENCODE-PLUGIN.md's own
"the two-phase pump as one program is REASONED — run it first (F4)" /
"pump-inside-a-live-TUI... is unrun." Falsifier 5 (§9) is honest and correctly
scoped ("the Claude backend... is unaffected and ships anyway"). So the
*falsifier* is honest even where the *body text* overclaims — which makes this a
genuine internal inconsistency in the document, not merely an aggressive
gloss: §9's falsifier language ("fail in practice") presupposes exactly the
unrun-composition status that §1/§3 elides.

**Is "mostly verified" therefore an overclaim?** Partially. The individual
mechanisms genuinely are VERIFIED (self-ring causes a turn, `noReply` fires no
idle, `tool.execute.before` blocks) — that part is not overclaimed. What is
overclaimed is compressing "every component verified, composition unrun" into
"VERIFIED: self-ring, two-phase delivered/" as a parenthetical in §1's build plan,
which reads to anyone who hasn't read OPENCODE-PLUGIN.md as a settled fact rather
than an assembled-but-untested claim.

### Is refusing build-own sound given the fork inherits HARD rows from a moving base?

This is the sharpest version of the attack and it partly lands. `_hc-claudeval.md`'s
three HARD rows (agentic loop, session persistence/compaction, maintenance-as-
standing-cost-center) are graded HARD *because Anthropic's engineering investment
sits behind Claude Code and keeps moving with it*. A **frozen fork** of opencode
gets a snapshot of that same engineering, but frozen — it does not keep receiving
upstream's compaction/loop improvements once pinned, and re-syncing periodically
against a base moving at ~1.5-day cadence, with `session/processor.ts` (720 lines,
not fully traced — `_hc-ocloop.md` §2.3 admits this) as the file a turn-end gate
would eventually need to touch, **is itself a maintenance-cost-center**, just a
smaller one than build-own. LOOP.md's own §5 half-admits this ("a fork frozen at
the pin slowly decays against a moving provider world") but only defends the
*provider* layer's decay (mitigated by the fact the provider layer is
metadata-driven and inherited). It does **not** make the equivalent argument for
the *loop* layer's decay — the very rows `_hc-claudeval.md` scored HARD. The
honest cost of "fork on trigger" is: you get the HARD rows once, for free, at the
pin — but every subsequent pin-bump to absorb a fork-worthy break re-imports some
fraction of build-own's maintenance burden, proportional to how far the fork has
drifted from the tip by then. The doc doesn't quantify this, so "refused: build
your own" is sound for **day 1**, but the document oversells how cleanly the fork
option avoids becoming its own standing cost center over multiple pin-cycles.

**Verdict: HOLDS, barely.** The trigger logic is coherent and legally grounded.
Strongest surviving attack: the doc treats "inherits the HARD rows" as a one-time
gift rather than a decaying asset, and doesn't price re-sync cost across multiple
fork-trigger cycles — which is exactly the maintenance-cost-center argument it
uses to refuse build-own, only partially applied to itself.

---

## (iii) THE COST SECTION

Spot-checked `_hc-price.md` line-by-line against LOOP.md §6's claims.

- **"$18.86/active-hour" Sonnet, "$59.81/active-hour" Opus** — LOOP.md §6 quotes
  these correctly, and correctly as *blended* MEASURED averages
  (`_hc-price.md`: "Sonnet leaves/scouts: $18.86/active-hour (mean of 7 samples...)").
  Accurate.
- **"$352/hour" ceiling** — accurate, and LOOP.md correctly carries the source's
  own caveat ("a ceiling, not a typical draw").
- **"$88-258/hour" mixed range** — accurate range from `_hc-price.md`'s Part 3
  ($87.0 all-foreign-below-operator, $257.5 mixed with Opus seats retained).
  LOOP.md's own framing ("ASSUMPTION-FLAGGED... *if* foreign token volume per
  task equals Claude's, which is unmeasured") **correctly reproduces** the
  source's loudest caveat verbatim in spirit ("do not treat the $3.02/hr or $87/hr
  figures above as predictions of real cost").
- **Is the mixed range doing rhetorical work its flag can't carry?** Marginally,
  yes, but the doc mitigates it: presenting a *specific* two-number range
  ("$88-258") reads more authoritative than the source's own hedged framing, even
  with the ASSUMPTION flag attached — ranges anchor perception more than the
  flag disclaims, a known rhetorical effect independent of the author's honesty.
  But this is a mild overclaim of precision, not a fabrication: both endpoints are
  traceable to real `_hc-price.md` computations, and the flag is present and
  correctly worded, immediately adjacent to the number, not buried.
- **"82%-weekly-limit framing" / "capacity buy" language** — checked directly:
  `_hc-price.md` itself says *"the mixed tree is a capacity buy at least as much
  as a cost cut, and that may be the more honest headline"* — this is the
  **source's own words**, not LOOP.md's invention. LOOP.md quotes this framing
  faithfully (§6: "the mixed tree is a capacity buy at least as much as a cost
  cut, and that may be the more honest headline" — verbatim match). Not spin
  introduced by LOOP.md; if it's spin, it's the child artifact's spin, faithfully
  inherited.
- **Method spot-check (active-hour normalization, 9-transcript sample):** accurate
  representation of `_hc-price.md`'s stated method (120s-capped inter-message gap
  sum), and LOOP.md does not misstate the sample size or overstate its
  representativeness beyond what the source itself claims (9 real transcripts,
  explicitly not claimed to be a statistically rigorous sample by the source
  either).

**Verdict: HOLDS.** LOOP.md's cost section is a faithful, appropriately-hedged
digest of `_hc-price.md`. Strongest surviving attack: presenting the mixed range
as a clean two-number bracket still does more rhetorical anchoring work than the
adjacent ASSUMPTION flag can fully cancel, even though every individual number and
caveat traces correctly to its source.

---

## (iv) THE AFFORDABILITY-AS-GOAL ARGUMENT (§6)

LOOP.md's argument: PHILOSOPHY §1 refuses *token-thrift mechanisms inside the
contract*; "the all-Claude architecture is too expensive to exist at the scale the
goal requires" is a different claim — a system that cannot run doesn't serve the
goal frugally, it doesn't serve it at all.

This is a legitimate distinction in the abstract — there is a real difference
between "cache responses to save tokens" (a mechanism inside the contract,
refused by §1) and "an all-frontier-model tree cannot be run at the scale the
goal needs" (a claim about feasibility, not thrift). But the argument as written
supplies **no limiting principle** for where "cannot exist at the scale the goal
requires" stops being a scale claim and starts being an ordinary cost argument
wearing a goal-argument's clothes. Any future proposal that wants to cut cost can
make the identical move: assert the current approach "cannot exist at the scale
the goal requires" and thereby exit PHILOSOPHY §1's refusal zone by definitional
fiat, without needing to show the scale claim is actually true (LOOP.md's own
scale claim rests on a *ceiling* number — $352/hr for a synchronized 10-agent
burst that the source itself says "rarely happens in practice" — not on a
demonstrated inability to run at the fleet's actual, measured, sub-10%-duty-cycle
cost). If a ceiling that the fleet's own measured duty cycle shows is not
representative counts as "cannot exist at the scale the goal requires," the bar
for invoking the affordability-is-a-goal exception is set low enough to
readmit nearly any cost-driven proposal PHILOSOPHY §1 was written to block.

The fit-rule tie-in (MODEL-FIT §6, "strong model where being wrong is expensive
and invisible, nowhere else") is the actual load-bearing argument here, and it is
sound on its own terms — but it does not need the "affordability is the goal"
framing to work; the fit rule alone would justify the mixed tree without touching
§1 at all. The affordability-as-goal move is therefore doing rhetorical work it
doesn't need to do, and that's exactly what makes it risky as precedent: it's an
unnecessary door LOOP.md opens on the way to a conclusion the fit rule reaches
without it.

**Verdict: WOUNDED.** The distinction is real but the document supplies no test
for when a cost claim qualifies as a "cannot exist at scale" claim versus an
ordinary cost-thrift claim wearing that framing — which means the argument, as
written, is reusable by any future token-thrift proposal that wants to claim the
same exemption.

---

## (v) EVIDENCE INTEGRITY — spot-checked tags

The operator named this the author's known weakness (HARNESS.md §10: "citation
quality tracking distance from the source... decorative into his own children's
artifacts"). I checked more than six tags; findings below, worst first.

### 1. "VERIFIED: self-ring, two-phase `delivered/`" — MISREPRESENTED

**LOOP.md §1:** *"the pump from OPENCODE-PLUGIN.md §3.1 (verified: self-ring,
two-phase `delivered/`)"*

**LOOP.md §5:** *"the pump (delivery, self-ring, two-phase `delivered/` —
VERIFIED end-to-end minus the final TUI composition, which is the named first
run-it check)"*

**Source, `OPENCODE-PLUGIN.md` §3.7:** *"components all VERIFIED... The
**two-phase pump as one program is REASONED** — run it first (F4)."* And: *"Scope
honesty on the delivery row. Every mechanism it rests on has been run — but
**not the final composition**... The two-phase `delivered/`... is a small
argued-for correction layered on the pump I ran with one-phase marking."*

**Gap:** The source explicitly refuses to call the two-phase `delivered/`
mechanism VERIFIED — it is REASONED, argued-for, unrun as a whole. LOOP.md's §1
parenthetical drops the qualifier entirely ("verified: self-ring, two-phase
delivered/"), and even §5's more careful phrasing ("VERIFIED end-to-end minus the
final TUI composition") still overclaims: the source names **two** gaps
(pump-inside-TUI *and* two-phase `delivered/` itself, run one-phase), and §5
folds both into a single "minus the TUI composition" carve-out, silently
absorbing the two-phase gap into "VERIFIED." This is the exact "decorative into
his own children's artifacts" pattern HARNESS.md §10 was warned about, recurring
in the reopened document.

### 2. GLM ps-misread + 4-retry hang cited as live judgment evidence — CONTRADICTS SOURCE'S OWN RETRACTION

**LOOP.md §2:** *"the eval's *other* failure class (GLM's `ps` misread + 4-retry
hang; deepseek's 11-minute harness detour)"*

**LOOP.md §4:** *"GLM still fails the dead-children case unless the parent
watchdog... catches it"* (stated as a prediction for Build 2, implying this is
still-live behavior).

**Source, `FLEET-EVAL-V3.md:107-108`:** *"v2's 'children all died, model hung 35
min, fragile parent' does NOT reproduce and is retired. It was the rig's empty
cwd."*

**Source, `FLEET-EVAL-V3.md:123-124`:** *"GLM's v2 was deflated (rig-killed
children scored as model fragility)... **No v2 GLM D2 row should be cited
again.**"*

**Gap:** This is the most serious integrity finding. The "ps misread + 4-retry
hang" citation traces only to `FLEET-EVAL.md` (v2), and the project's own v3
synthesis explicitly retracts it and instructs that it not be cited again. LOOP.md
(and HARNESS.md §3 before it, uncorrected) cites it anyway, as part of the
evidentiary basis for "judgment seats stay Claude" — precisely the claim the
operator asked to have checked for contamination. V3's *actual* live GLM finding
is milder: "no watchdog... terminated only because its children delivered" — an
unexercised risk, not a demonstrated hang. LOOP.md's Build 2 prediction ("GLM
still fails the dead-children case") is stated as though restating a known
failure mode; it is actually re-asserting a retired one.

### 3. "deepseek's 11-minute harness detour" — imprecise but traceable (minor, already flagged once)

**LOOP.md §2:** *"deepseek's 11-minute harness detour"* (no line cite given here,
unlike HARNESS.md §3's "V3:84-86").

**Source, `FLEET-EVAL-V3.md:82-83`:** *"deepseek **abandoned the brief and spent
11 min debugging the harness**"* — confirmed real, verbatim.

**Gap:** Minor and already self-corrected once in this project's history —
`_hcr-evidence.md` and `_hcrev-eval.md` both document that HARNESS.md's original
citation of this fact used an off-by-2 line range (`V3:84-86` instead of
`V3:82-83`). LOOP.md drops the line-cite here rather than repeating the wrong
range — net neutral, but worth noting the fix was to omit the pincite rather than
correct it, which is a regression in traceability even though it avoids repeating
the specific error.

### 4. "166-provider catalog" — ACCURATE

**LOOP.md §5:** *"11+ wire adapters, a live 166-provider catalog, OAuth
plumbing"*

**Source, `_hc-ocloop.md` §2.4:** *"**166 providers** registered as of this check
(live `curl` against `models.dev/api.json`)"* and *"11+1 hand-written wire
adapters."* Matches. Clean.

### 5. "one documented-but-dead type already found (permission.ask)" — ACCURATE

**LOOP.md §5:** *"`permission.ask` is already a documented-but-dead type"*

**Source, `_hc-ocloop.md` §0:** *"`permission.ask` is **dead code** — declared in
the `.d.ts`, never dispatched, the bare string does not occur in the 130MB binary
... Re-confirmed independently by `ocr-lab`."* Matches. Clean.

### 6. "the binary already drifted 1.17.13→1.17.18 during this repo's own investigation" — ACCURATE

**LOOP.md §1:** *"the binary already drifted 1.17.13→1.17.18 *during this repo's
own investigation* (VERIFIED, `_hc-ocloop.md` §0)"*

**Source, `_hc-ocloop.md` §0:** *"Target across all of them: opencode
**v1.17.13 → v1.17.18** (the binary drifted *during* the original
investigation...)"* and later, §2.2: *"sharpens... the plugin investigation's own
observation that its target binary drifted from 1.17.13 to 1.17.18 during that
investigation (2026-07-01 → 2026-07-09, 5 patch releases in 8 days)."* Matches,
correctly tagged VERIFIED. Clean.

### 7. "opencode can't gate turn-end at all... no `decision:block` analog" — ACCURATE

**LOOP.md §2:** *"no hook at any documented depth can refuse to let a turn end...
there is no `decision:block` analog (VERIFIED — `_hc-ocloop.md` §1, all seven duty
rows and the pattern section)"*

**Source, `_hc-ocloop.md` §1 pattern section:** *"No v1 hook can gate on 'the turn
is ending'... no analog to Claude Code's `Stop` hook returning
`{'decision':'block'}`."* Matches. Clean.

### 8. "~1 release per 1.5 days" — ACCURATE

**LOOP.md §5:** *"upstream ships **~1 release per 1.5 days** from a core of ~8
company-affiliated committers"*

**Source, `_hc-ocloop.md` §2.2:** *"19 releases on the 1.17.x line alone across 29
days... roughly **one release every 1.5 days**"* and *"the top commit counts are
dominated by ~8 individuals who are all listed in `.github/TEAM_MEMBERS`."*
Matches. Clean.

### Summary of the evidence-integrity spot-check

Of 8 tags checked, **6 clean, 1 seriously misrepresented (self-ring/two-phase
delivered/), 1 built on a source that explicitly disowns it (GLM hang)**. The
2/8 failure rate concentrates on exactly the two claims the document's central
predictions depend on most (the pump's readiness, and the judgment-side evidence
for "judgment seats stay Claude"). This is not a high overall error rate, but it
is not randomly distributed — it clusters on load-bearing claims, which is worse
than a uniform error rate would be, and reproduces the exact "decorative into
children's artifacts" pattern HARNESS.md §10 flagged as the author's own
strongest-named defect, in the very document reopening that same author's design.

**Verdict: REFUTED as a discipline claim.** LOOP.md states its evidence discipline
as continuous with HARNESS.md's ("VERIFIED / MEASURED / DOCUMENTED / REASONED...
with the same post-review humility"). The self-ring/two-phase-delivered tag and
the GLM-hang citation both fail that standard in the same way HARNESS.md's first
draft did before its own review — meaning the "same discipline" claim does not
hold uniformly across this document's most consequential claims.

---

## §8's "STANDS" LIST — does anything actually contradict the new design?

Checked each STANDS item against LOOP.md's own body text for self-contradiction:

- **"the SLM rulings (§7 — the SLM forced-call runner is untouched)"** —
  confirmed accurate against HARNESS.md §7 itself (§7a-e rulings are not
  discussed or altered anywhere in LOOP.md). No contradiction.
- **"the survivability gate as repaired post-review"** — HARNESS.md §2.4's gate
  depends on `cmd_spawn` writing a `permissions` block, listed in HARNESS.md §8
  as **unbuilt**. LOOP.md's Build 0 ("prerequisite, already owed") correctly
  restates this as a dependency rather than contradicting it — consistent.
- **The one genuine tension, not flagged as a contradiction by LOOP.md but worth
  naming:** HARNESS.md §8 also lists **the structural leaf-cannot-spawn change**
  as unbuilt and explicitly warns "a *Claude* cheap leaf's 'I will not become a
  parent' remains an unenforced promise, and this design knowingly ships on top
  of that." LOOP.md's Build 3 ("open the seats... foreign tokens stop being
  leaf-only") widens exactly the population of non-Claude-family agents holding
  mid-tree seats, while this structural gap (for Claude-family leaves) is
  untouched and unmentioned in LOOP.md at all. This is not a logical
  contradiction — LOOP.md's own §2.2-inherited foreign-row denial via
  `tool.execute.before` is a different, already-built mechanism for the
  *foreign* rows specifically — but LOOP.md's STANDS list cites "everything
  else" as standing without flagging that one of the things standing is a
  **known, named, unbuilt safety gap** in the very leaf-tier the design is about
  to make more populous and more capable. A reader relying on the STANDS list
  alone would not learn that this gap exists; they'd have to independently
  cross-reference HARNESS.md §8's last bullet.

No item in the STANDS list actively contradicts LOOP.md's new design in the sense
of being logically incompatible with it. The gap above is an omission, not a
contradiction — but in a document reopening prior work specifically to widen the
foreign-model seat population, silently standing on an unbuilt safety gap for the
adjacent (Claude-family) leaf tier without a cross-reference is worth flagging as
a completeness defect in §8.

---

## RANKED REPAIR LIST

1. **Fix the GLM-hang citation (highest priority).** Strike "GLM's `ps` misread +
   4-retry hang" from §2 and the "GLM still fails the dead-children case" framing
   from §4's registered prediction. Replace with V3's actual, live finding: GLM's
   harvest loop has no watchdog and would hang on a genuinely dead child, but this
   is an *unexercised* risk (v3: "terminated only because its children
   delivered"), not a demonstrated failure. This directly affects the
   judgment-seats-stay-Claude conclusion's evidentiary weight for surface (i),
   which the operator specifically asked to have checked for contamination.

2. **Fix the self-ring/two-phase-delivered tag.** In §1 and §5, replace "VERIFIED:
   self-ring, two-phase `delivered/`" with the source's own framing: components
   verified individually; the two-phase mechanism and the pump-inside-TUI
   composition are both unrun, per `OPENCODE-PLUGIN.md` §3.7's own scope-honesty
   paragraph. This affects the "mostly verified" framing under surface (ii) and
   is a direct instance of the evidence-integrity failure the operator asked to
   have checked under (v).

3. **Add a limiting principle to §6's affordability argument**, or drop the
   "affordability is the goal, not thrift" framing and rest the mixed-tree case
   on the fit rule alone (MODEL-FIT §6), which reaches the same conclusion
   without opening the "cannot exist at scale" exemption to reuse by future
   proposals that haven't earned it.

4. **State the fork's decay cost for the loop layer, not just the provider
   layer**, in §5 — the "inherits the HARD rows" framing should acknowledge that
   a frozen fork re-imports a fraction of build-own's maintenance burden at every
   pin-bump cycle, proportional to drift since the pin, rather than treating the
   inheritance as a one-time, non-decaying gift.

5. **Cross-reference the unbuilt structural leaf-cannot-spawn gap** (HARNESS.md
   §8's last bullet) from LOOP.md's §8 STANDS list or Build 3, since Build 3
   widens the foreign-seat population while this Claude-family-leaf gap remains
   unaddressed and currently unmentioned in LOOP.md.

6. **Restore the line-pincite for "deepseek's 11-minute harness detour"** in §2
   (correctly this time — `V3:82-83`, not the `V3:84-86` HARNESS.md originally
   used) rather than omitting the cite entirely, to avoid the regression in
   traceability noted in the evidence-integrity section.

7. **Sharpen falsifier 3 (digest signal quality)** to also catch the quieter
   failure mode: a parent that stops reading digests because they're
   low-information, rather than only the loud failure mode (a parent that
   reopens pane-reading). As written, the falsifier only catches the case where
   parents visibly revert to old habits, not the case where the digest quietly
   becomes a rubber-stamped, unread formality — which is arguably the more likely
   failure and the one the "loop-crutch atrophies reporting discipline" concern
   (surface i, PHILOSOPHY §2) predicts.
