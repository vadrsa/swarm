# FALSIFIERS — the consolidated live list

Every falsifier named across the design corpus, in one place. Previously scattered across
`SPAN.md §6`, `HARNESS.md §9`, `LOOP.md §9`, `OPERATOR-STRUCTURE*.md §5/§7`, `MODEL-FIT.md`,
`DECISION-WIRING.md`/`PIPELINE-WIRING.md`/`PROXY-WIRING.md`/`HOOK-WIRING.md`, `TRIGGER.md`,
`ORG-REVIEW.md`, `SIMPLEST.md §6`/`WATCHLIST.md`, `OPENCODE-PLUGIN.md`, `INBOX.md`,
`ONBOARDING.md`, `INDUSTRY-PATTERNS.md`, and `PHILOSOPHY.md §7`.

Built by `repo-cleanup` (2026-07-15) from a full extraction of the design corpus
(`docs/_scout-falsifiers.md`, superseded by this file). Classification rule: **RETIRED** if the
source doc states it answered/fired/refuted, or if the doc/mechanism it gates is itself
superseded with no successor carrying the question forward. **STILL LIVE** if open and the
gating doc is current. **STALE** if open but the work it gates no longer exists.

**Running these live falsifiers is exactly what the Counterfactual Toolset (M10,
`swarm-rnd/POWERS-tools.md`) was designed for** — it runs a step twice, once with the full
toolset and once narrowed, and lets the operator read what the agent *would have done* in the
world not taken. SPAN.md itself named this gap: *"§6 is a GRAVEYARD of falsifiers named and
never cheaply run."* M10 is the first instrument built to close it; it hasn't been applied to
the list below yet.

---

## STILL LIVE — consolidated (the real open list)

### Span, delegation, coordination shape
- **SPAN.md #2 — pure forwarders survive**: middle coordinators whose journals show relay
  without judgment, whose parents keep them anyway. Untested.
- **SPAN.md #3 — absorb never fires**: streams shrink but layers remain (a coordinator whose
  span has shrunk to what its parent could hold directly, kept anyway). Untested.
- **SPAN.md #4 — the self-test is theater**: agents journal "span OK" while child-state
  summaries go stale. Untested.
- **SPAN.md #5 — operator load ignores declared span**: desk grows past ~3 standing decisions
  while a coordinator keeps forwarding rather than absorbing. Untested, spot-check not yet
  performed.
- **SPAN.md #1′ coordinator rung, deeper context-pressure variant** — the original flood probes
  ran and did not fire as predicted (see RETIRED below), but a sharper variant (sustained,
  stateful load specifically meant to force rung-3/4 engagement) was sketched and never run.
  Marked UNOBSERVED, not answered.
- **OPERATOR-STRUCTURE.md F-DOCTRINE**: a session handed a multi-part goal stands up top-level
  agents owning subtrees, not a row of workers it holds itself. Not yet run, collector cold.
- **OPERATOR-STRUCTURE.md F-MIDDLEWARE, grandchild arm**: the corrected operator-span
  middleware passed once after a misconfigured fail-open version leaked mail — the live,
  pane-backed grandchild arm is still untested.
- **OPERATOR-STRUCTURE-RED.md attack A**: a root session holding a tree across compaction from
  a self-maintained journal, without a swarm-managed identity. Not run.
- **OPERATOR-STRUCTURE-RED.md attack B**: a root session proposes a top layer, human confirms,
  a collector diffs proposed-vs-built shape. Not run; author predicts 100% divergence.
- **OPERATOR-STRUCTURE-RED.md attack D3**: a coordinator in the record whose journal shows
  verdicts (judgment) rather than relay. None found as of last check — open, re-checkable
  against the current record at any time.
- **OPERATOR-STRUCTURE-GRAVE.md falsifier 3**: a human confirm that does not decay — the
  operator answers pre-task shape proposals with substantive corrections over ≥5 tasks.
  Untested.
- **OPERATOR-STRUCTURE-GRAVE.md falsifier 4**: a coordinator pane whose journal shows verdicts,
  not relay logs — notes its own parent swarm as the cheapest live test.
- **ONBOARDING.md Claim 1 (coordinator stance)**: falsified if an after-onboarding operator ends
  up with ≥3 direct children and no intermediate node. Not yet collected.
- **ONBOARDING.md Claim 2 (mine-first)**: falsified if dismissal/ritual/generic-spawn pitfalls
  fire in production. Not yet collected, spot-check pending.
- **ONBOARDING.md recommendation-earning falsifier**: a real session produces a bad delegation
  map traceable to missing recall, not bad judgment. Never tried.
- **WATCHLIST.md #5 — post-compaction floundering**: restored agents re-ask/redo work. Open, no
  doc reports this yet.
- **WATCHLIST.md #6 — operator-bound questions stay malformed**. Open.
- **WATCHLIST.md #7 — scope creep in the rewrite**: any addition with no fired-trigger
  justification. Open/ongoing self-check — actively invoked by ORG-REVIEW.md when justifying its
  own new `review` verb, so this one is a live working discipline, not just a claim.
- **WATCHLIST.md #8 — shared-tree hazard**: a third lost-work incident (two shapes already
  recorded). Open.
- **SIMPLEST.md §6.2 / WATCHLIST.md #2 — turn floods**: queue-drain turns become the majority of
  an agent's turns. Open, unmeasured.
- **SIMPLEST.md §6.3 / WATCHLIST.md #3 — re-ring reliability**: self-ring proves unreliable,
  messages stall. Bounded but still open, not retired: a real ~3-minute stall was observed
  2026-07-10 (WATCHLIST.md §3, "delayed, never lost"), but the source docs themselves say
  live-pane reliability "remains untested" — same shape as OPERATOR-STRUCTURE.md's F-MIDDLEWARE
  grandchild arm (kept STILL LIVE above for the same reason: a partial pass on one arm doesn't
  close the untested arm). Corrects an earlier draft of this file that retired this one
  inconsistently with F-MIDDLEWARE (cleanup-red review).
- **SIMPLEST.md §6.5 — post-compaction floundering** (same as WATCHLIST #5 above — duplicate
  entry point, one open question).

### Harness / model-loop mechanics
- **HARNESS.md §9.1 — remodel-identity ruling**: remodeled agents flounder worse than fresh
  spawns from the same journal; a reader misattributes journal work across the remodel
  partition line. Collector named, not yet run.
- **HARNESS.md §9.3 — priority line / static reason**: spawn reasons never cite declared
  priority in the first 50 mandated spawns (dead text), or static-default reasons converge to
  one frozen string (theater). Mandate not yet built/enforced at the scale needed to check this.
- **HARNESS.md §9.4 / HARNESS-RED.md — survivability gate**: run an Opus-pinned child into the
  same first-touch permission wall. Explicitly never run — the single most-repeated "still not
  run" item across two docs.
- **HARNESS.md §9.5 — SLM leaf**: a small-model artifact fails parent spot-checks at a rate
  consuming the parallelism gained, or fails in the omission direction. Open.
- **HARNESS.md §9.6 — foreign-seat play**: a deepseek/GLM seat drops work despite constraints,
  or a clean run suggests the constraints are too tight. Open.
- **HARNESS.md §9.7 — limit-remodel caveat**: whether a within-Anthropic remodel escapes a hit
  usage limit. Unmeasured.
- **HARNESS.md §9.8 — no-router ruling**: contingent — re-argue only if swarm grows a labeled
  evaluation surface making wrong routes scorable in-loop. Open but contingent, not urgent.
- **HARNESS.md §9.9 / LOOP.md §8 — structural leaf denial**: any foreign-row leaf producing a
  descendant means the swarm-verb denial failed. Named live risk in two docs, still unbuilt.
- **HARNESS.md §9.10 — duplicate-directive collector**: an operator directive duplicating an
  already-queued unread report should earn annotate-never-drop middleware. Open.
- **LOOP.md §9.1 — absorption prediction**: a duty-loop re-run reaches 7/7 delivered reports,
  zero journal hard-fails. Open as a full claim.
- **LOOP.md §9.2 — judgment layer**: with protocol absorbed, foreign models still sink the
  delegation battery on judgment alone. Open, pending Build 2.
- **LOOP.md §9.3 — digest signal quality**: loud misfire (parents reopen pane-reading) vs. quiet
  misfire (digests become unread formality). Sharpened per LOOP-RED3 but not yet run.
- **LOOP.md §9.4 — pinned-stock bet**: an opencode release breaks the pinned plugin surface
  twice, or a duty needs turn-end gating. Fork trigger not yet fired.
- **LOOP.md §9.6 — cost premise**: measured foreign-model token consumption per task erodes the
  per-token cost advantage. Unmeasured.
- **LOOP.md §9.7 — the registered prior**: §4b.4's probabilities, self-falsifying by
  construction, scored against future Build 2/2.5/2.6 runs. Not yet scored.
- **LOOP-RED3.md repair 5**: two missing rubric rows were prerequisitized into §4b.3's text but
  never actually authored. Still open in substance, not just disposition.
- **OPENCODE-PLUGIN.md F1**: pump's `noReply` write not visible to the next turn across a
  compaction. "Still genuinely untested," priority 3.
- **OPENCODE-PLUGIN.md F4**: pump strands or duplicates mail under load (50 sends to a busy
  agent). "The most valuable unrun experiment," priority 2.
- **OPENCODE-PLUGIN.md F5**: an opencode upgrade breaks `experimental.session.compacting`,
  silently degrading restore. Open.
- **OPENCODE-PLUGIN.md — pump inside a live TUI**: oc-red's exact prediction test. Priority 1,
  "the first experiment an implementer should do."
- **OPENCODE-PLUGIN-RED.md closing falsifier**: run the *corrected* §3.1 pump (not the original
  reviewed/broken one) against a live TUI — composition still untested.
- **FLEET-EVAL-V3.md — D2-cheap stability**: weighing is unstable run-to-run; a same-brief ×3
  stability probe is needed before treating it as a model property. Deferred to "v4 rubric gap,"
  still open.
- **FLEET.md — report-without-cooperation**: the report can't leave the pane without the model's
  cooperation (opencode `run` can't emit a parent-readable artifact except via the leaf itself).
  Named UNOBSERVED at time of writing; no later doc confirms this was actually exercised
  (cleanup-red review found no supporting grep hit in FLEET-EVAL.md). Still open.
- **FLEET.md — noisy `session.idle`**: fires so often mid-task that a done-signal can't gate
  cleanly off it. Same status as above — UNOBSERVED, not confirmed exercised by any successor.
  Still open.
- **FLEET.md — silent soft-kill**: a mid-flight refusal leaves nothing in the pane, no artifact,
  only a timeout. UNOBSERVED, not confirmed exercised — still open.

### Model selection / delegation doctrine
- **MODEL-FIT.md — Rung 3 seat behavior**: a cheap-model leaf's artifact is fine but its seat
  behavior fails (narrates instead of `swarm send`, never journals, doesn't terminate). Doc
  itself calls this "the single thing most worth watching on the next cheap spawn."
- **MODEL-FIT.md §4 — over-delegation ruling**: a Haiku child that at the judgment wall spawns
  children to escape it. Not yet observed.
- **MODEL-FIT.md — Rung 1 (seats must be Opus)**: a Sonnet coordinator runs a real subtree with
  no protocol drops — would demote Rung 1 if observed. Open.
- **MODEL-FIT.md §4 — "strong model is more, not better, on mechanical work"**: an Opus census
  turns out tighter than a Haiku census on the same question. Unfired.
- **MODEL-FIT-MANDATE.md — `--why` quality at scale**: read the next 30 spawns' reason clauses;
  wrong if ≥1/3 is vacuous mush. Not yet run at full scale (a small sample was checked during
  the mandate PR review, but not this full-scale version).
- **TRIGGER.md falsifier 2**: some SKILL.md-only change fires ≥3/3 on a big goal under shipped
  conditions. Open/live risk, untested beyond the three variants already tried.
- **TRIGGER.md falsifier 3**: a clean, higher-n total-denial arm shows the skill firing reliably
  once every built-in is gone. Doc's own words: "weakest evidence in this document, first thing
  worth re-running."

### Wiring layer (decision engine / pipeline / proxy / hook)
These four docs (DECISION-WIRING, PIPELINE-WIRING, PROXY-WIRING, HOOK-WIRING) form one lineage —
HOOK-WIRING §13's universal send-middleware is what actually shipped, so falsifiers below are
live **as questions about the shipped middleware**, even though the docs that originally posed
some of them are themselves superseded-but-historical.
- **HOOK-WIRING.md H-F1**: an operator message is dropped. Would void the never-drop guarantee
  if it ever fires. Open — the highest-stakes item in this cluster.
- **HOOK-WIRING.md H-F2**: fail-open is not byte-identical to the no-middleware baseline. Open.
- **HOOK-WIRING.md H-F3**: a reply/claim gets mis-attributed — tied to the identity-injection
  fix. Open.
- **HOOK-WIRING.md H-F4**: a branch fires off the operator path. Open.
- **HOOK-WIRING.md H-F5**: the send path acquires an unbounded block. Open.
- **HOOK-WIRING.md H-F6**: timeouts dominate (expected to be modal, not tail) — predicted, not
  yet measured in production.
- **HOOK-WIRING.md H-F7**: an orphan appears in `delivered/` with no claim line, from a
  SIGKILL-mid-claim. Explicitly "not auto-recovered." Open.
- **DECISION-WIRING.md W-F1 through W-F8**: standing, none reported fired — an answer without
  covering grant; a delivered file with no claim line; auto-answer under the OPERATOR header;
  pass-through surface differing from absent; engine-down increasing human load; a self-training
  leak; the engine pressing the operator's span; a claim-race double-act. Kept as one bundle —
  these describe the general failure surface any engine/middleware in this lineage must avoid,
  and HOOK-WIRING's shipped middleware hasn't been checked against all eight.
- **PIPELINE-WIRING.md PIPE-F1**: barrier bites — engine-down increases human load. Open, the
  falsifier the doc's own recommendation hinges on.
- **PIPELINE-WIRING.md PIPE-F3**: DRAFT trace presses the operator's span, becomes a second
  inbox. Open.
- **PROXY-WIRING.md P-F1 through P-F8**: observer acts beyond the ledger; false flags dominate;
  the "justifying hit" test; draft becomes authority; plane bytes differ from absent; behavioral
  interposition/drift; volume presses span; recall via sampled miss-audit. All open,
  pilot-dependent — kept as one bundle for the same reason as W-F1–8.

### Review-cadence / org-review instrument
- **ORG-REVIEW.md F1**: the verb is run once at ship and never again (confirm-but-never-read
  decay). Open/unrun — author's own most-expected-to-fire.
- **ORG-REVIEW.md F2**: the page produces no decision across 3 consecutive invocations. Open.
- **ORG-REVIEW.md F3**: it grows an opinion (score/health/rating language starts appearing in
  output). Open.
- **ORG-REVIEW.md F5**: the coordinator "offer" comes back (unsolicited surfacing, the exact
  pattern SPAN/GRAVE killed once already). Open.
- **ORG-REVIEW.md F6**: classifications rot — a printed classification can't be re-derived from
  its citation. Open.
- **ORG-REVIEW.md §3.2′ — duplicate-work / serial re-issue**: explicitly left as an unmeasured,
  named hole ("I will not print a number I cannot prove is mine").

### Misc standing
- **INDUSTRY-PATTERNS.md §9**: whether the org will accept a standing consumer (Conflict 1) —
  open, explicitly "the org's call," not an empirical falsifier.
- **INBOX.md P-CLAIM-AUDIT**: an exercise check of the claim-line mechanism over the next 20
  operator messages. Designed, not run.
- **INBOX.md P-VOL**: volume-threshold probe gating E2 (the seat-triage paragraph). Designed,
  not run.
- **INBOX.md P-TRIAGE**: one-stint triage-paragraph trial — contingent on P-VOL firing first.
  Designed, not run.
- **INBOX.md Idea 1 verdict falsifier**: a real corruption/misclaim incident in the operator
  queue that the claim-line audit fails to catch. Open/unfired.
- **ORG-REVIEW.md F4**: session latency presented as human latency. Open/unrun — the doc already
  found and self-corrected one near-miss instance of exactly this (§3.5/§4c′), which makes this
  the ORG-REVIEW falsifier closest to firing for real; worth watching first among that cluster.
- **PHILOSOPHY.md §7**: internal tension between the `--major` version guard and the standing
  policy of never incrementing major (an inert guard). Explicitly named as unresolved — "the
  tooling has not caught up to it." Not a probe-and-measure falsifier, but a live doctrine
  contradiction worth tracking until resolved one way or the other.

---

## RETIRED — answered, refuted, or the gated mechanism is gone

- **FLEET.md's keyed-provider falsifier** (deepseek/zai-coding-plan keys don't authorize a live
  call) — RETIRED: exercised by FLEET-EVAL.md's actual keyed runs. Confirmed — this is the one
  of FLEET.md's four build-step falsifiers with a real successor exercise; corrects an earlier
  draft of this file that claimed all four were exercised (cleanup-red review: `grep -i
  soft-kill docs/design/FLEET-EVAL.md` returns zero hits, so the soft-kill path specifically was
  never actually run).
- **FLEET-EVAL.md falsifier-1 (battery doesn't discriminate)** — RETIRED, answered: does not
  fire, real PASS/PARTIAL/FAIL spread observed.
- **FLEET-EVAL.md cost falsifier** — RETIRED, answered: does not fire, actuals came in 3–5×
  under estimate.
- **FLEET-EVAL-RED.md's 3 evidence-check falsifiers** (missing report dir, missing journal,
  missing crash-session dir) — RETIRED: all checked, none overturn the reviewed verdicts.
- **FLEET-EVAL-V3.md MCP-off recovery falsifier** — RETIRED, refuted by V3-RED's OBJ-6 (the
  write itself errored; MCP-off would not have helped).
- **FLEET-EVAL-V3.md cost falsifier** — RETIRED, answered: fires only on the cheap side, native
  cell was unmetered as run.
- **FLEET-EVAL-V3-RED.md's 6 OBJ falsifiers** (OBJ-1, 2, 3, 5, 6, CLEARED-1) — RETIRED: all
  checked against source/logs, none die/collapse/reverse as their alternate condition specified.
- **HARNESS-RED.md's `--model default` reason-theater attack** — RETIRED: became HARNESS.md
  §9.3 (still open, tracked above under that name — not a duplicate, the original attack-framing
  is closed and folded into the standing falsifier).
- **HARNESS.md §9.2 — plays-as-convention** — RETIRED as originally framed: HARNESS-RED's
  citation for this was later found to be a retired v2 finding, walking back its evidentiary
  basis. The underlying question ("does a briefed parent ever earn `--play`") isn't worth
  re-listing as live without a fresh citation.
- **LOOP.md §9.5 — pump composition** — RETIRED, resolved 2026-07-13 (per `_hc-build1-verify.md`
  cited in the corpus): both named unrun compositions were run against real opencode 1.17.18 and
  verified. Did not fire.
- **LOOP-RED.md's 2 findings** (falsifier-3 sharpening, GLM-hang citation) — RETIRED: both
  folded into LOOP.md §10 (item 7 and item 1 respectively).
- **LOOP-RED3.md repairs 1, 3, 4, 7** — RETIRED: quiescence predicate rebuilt, M1b added, M1
  split, branch asymmetry noted — all folded per LOOP.md §10.
- **LOOP-RED3.md repair 6 ("per model generation" trigger)** — RETIRED: the scout that extracted
  this flagged it as possibly still open, but a direct check against `LOOP.md` §4b.3 (around
  line 361) shows "per model generation" reopening is explicitly defined there. Resolved, not
  open — corrects the raw extraction in `docs/_scout-falsifiers.md`.
- **OPERATOR-STRUCTURE.md F-SPAN** — RETIRED as a bounded result: run, not fired (0 of 61
  messages from depth ≥2). Doesn't prove the tree never floods, but the probe ran and the
  doctrine held under it — treat as answered-for-now, re-open only if a flood is later observed.
- **OPERATOR-STRUCTURE.md F-MODEL** — RETIRED, run and held: ps/send work with HERDR_ENV unset,
  only spawn is gated.
- **OPERATOR-STRUCTURE-FIX.md's parent-naming prediction** — RETIRED: discharged, §7h's
  end-to-end run matched the prediction exactly. (The FIX mechanism itself was later retracted
  wholesale by OPERATOR-STRUCTURE.md — the falsifier was answered even though the design it
  validated didn't ship.)
- **OPERATOR-STRUCTURE-RED.md attack C** — RETIRED: checked, confirmed impossible, kills claim C
  outright.
- **OPERATOR-STRUCTURE-GRAVE.md falsifier 1** (`COORDINATING.md` exists) — RETIRED: checked,
  does not exist.
- **OPERATOR-STRUCTURE-GRAVE.md falsifier 2** (`bin/swarm` gains a root-session name) — RETIRED:
  this was the recommendation itself; it fired via the FIX, then the FIX was retracted. Closed
  either way — the mechanism it predicted no longer exists to re-test.
- **OPERATOR-STRUCTURE-GRAVE.md Part II §9d** (behavioral constraint with no compliant path) —
  RETIRED: checked and discharged, no such constraint found.
- **OPERATOR-STRUCTURE-RED2.md D.1** (pane recycling) — RETIRED: tested against real herdr, did
  not fire, pane ids confirmed monotonic/persisted.
- **OPERATOR-STRUCTURE-RED2.md §3 phantom-root attack** — RETIRED as bounded: could not
  manufacture from stock herdr; treated as closed pending a stock-herdr change that would reopen
  it (none reported).
- **SPAN.md #1 flood test** — RETIRED: run, not fired as predicted, but superseded in place by
  #1′ (see below) — the original probe's predicted shape (flat 8–10 direct children) didn't
  appear either; the probe routed the flood to harness subagents instead. The question mutated
  rather than closed clean, so it's retired as a probe, with #1′ carrying the live remainder
  (see STILL LIVE above).
- **SPAN.md #1′ heavy flood, rung 3/4 engagement** — RETIRED for the base case: run, rung 3/4
  did not engage (arguably correctly). The coordinator rung result (marked UNOBSERVED — never
  actually run, not "ran and didn't fire") and the sharper context-pressure variant remain open
  — carried forward under STILL LIVE.
- **MODEL-FIT.md — "unpinned child inherits its parent's model"** — RETIRED: fired, folded in.
  Confirmed FALSE — no such inheritance exists in the shipped code.
- **MODEL-FIT.md — "a leaf stays a leaf"** — RETIRED: fired, folded in. Confirmed FALSE — 18/115
  agents grew coordinator roles unbriefed. (This finding is exactly why MODEL-FIT.md's Rung 3
  seat-behavior falsifier, above, stays live — the failure mode is known to occur, just not yet
  observed on a *cheap-model* leaf specifically.)
- **TRIGGER.md falsifier 1** — RETIRED: reproduced/answered, replicated across 12 runs on two
  rigs; doc itself says "no longer the cheapest open check."
- **HOOK-WIRING.md §12 "Condition 1"** — RETIRED as VOID: structural certainty requirement
  declared impossible to satisfy by any operator sentence — the substrate cannot order the human
  relative to the hook. Closed by declaration, not measurement, but closed.
- **OPENCODE-PLUGIN.md F2** (`session.idle` fires once per turn) — RETIRED: measured, false as a
  worry — confirms it fires once per turn as needed.
- **OPENCODE-PLUGIN.md F3** (session-store collision across agents) — RETIRED as FIRED: 93
  sessions from other directories observed. This is a confirmed-real hazard, not an open
  question — if the mitigation for it isn't already load-bearing in the shipped plugin design,
  that's worth a fresh look, but the falsifier itself is answered.
- **OPENCODE-PLUGIN-RED.md's closing falsifier, original framing** — RETIRED: confirmed true
  against the reviewed (broken) pump. The *corrected* pump's version of this question is carried
  forward under STILL LIVE.
- **SIMPLEST.md §6.1 / WATCHLIST.md #1 (senders don't look)** — RETIRED: informed by ORG-REVIEW's
  probe finding, FIRED→IGNORED: 0 of 135. Answered for the sampled period.
- **SIMPLEST.md §6.4 / WATCHLIST.md #4 (journals rot into mush)** — RETIRED as FIRED: confirmed
  explicitly by ORG-REVIEW.md §6c″ using this doc's own trigger definition. This is a confirmed
  real failure mode, not a hypothesis — if nothing has shipped to address it, that's a gap worth
  a human decision, but it's not an unanswered falsifier anymore.
## STALE — gated work no longer exists

- **OPERATOR-STRUCTURE-RED3.md §H central falsifier** — STALE, not live: explicitly never run by
  its own author, AND its target (the operator-span middleware) has since been partially
  exercised via OPERATOR-STRUCTURE.md's own F-MIDDLEWARE (see STILL LIVE — grandchild arm still
  open). Superseded by the more specific, still-tracked F-MIDDLEWARE item; not worth double
  listing. (Filed here, not under RETIRED, since nothing about §H itself was answered — the
  question just moved to a better-specified successor. Filing corrected per cleanup-red review.)
- **archive/CODEX-DESIGN.md §8's open items** — STALE: the doc's own conclusion doesn't transfer
  to opencode per OPENCODE-PLUGIN.md §9 — the harness choice these falsifiers gated (codex) is
  no longer the live path. Not worth carrying forward; OPENCODE-PLUGIN.md's own falsifiers
  (carried above under STILL LIVE) are the live version of this question now. (Filing corrected
  per cleanup-red review — was previously misfiled under RETIRED despite being labeled STALE in
  its own text.)
- **DECISIONS.md F1–F7** — STALE: DECISIONS.md is superseded as an implementation guide by
  DECISION-WIRING and ultimately HOOK-WIRING §13's shipped universal middleware. F1–F7 were
  written for a bespoke decision-engine mechanism that was never built in that form — the
  shipped middleware is a different mechanism, and its open questions are the W-F1–8 /
  H-F1–7 falsifiers already carried forward under STILL LIVE. Re-litigating F1–F7 against a
  mechanism that doesn't exist adds nothing.
- **PIPELINE-WIRING.md PIPE-F2** (on-disk tracking state rots with no consumer) — STALE: the
  doc's own recommendation (a tracked pipeline) was not what shipped — HOOK-WIRING §13's
  middleware isn't a tracked pipeline at all, so there's no on-disk tracking state for this to
  apply to.
- **archive/CODEX-CAPABILITIES.md** — not applicable, no falsifiers were ever formally named
  here (VERIFIED/DOCUMENTED/SUSPECT tags only) — nothing to retire or carry forward.

---

## Summary

| Status | Count |
|---|---|
| STILL LIVE (consolidated above, duplicates merged) | 78 |
| RETIRED | 33 |
| STALE | 5 |

Counts are exact (recounted by heading after the cleanup-red review below), not approximate —
an earlier draft's ~65/~35/~10 wasn't reproducible from the file because two STALE-labeled
entries were mis-filed under the RETIRED heading; both are now filed under the heading their own
text asserts.

**Reviewed by `cleanup-red` (opus) on 2026-07-15.** The reviewer spot-checked ~10 entries across
clusters against source docs and found the consolidation sound overall, with three specific
fixes applied here as a result: (1) three falsifiers silently dropped from the original
extraction — INBOX.md P-VOL, INBOX.md P-TRIAGE, ORG-REVIEW.md F4 — restored under STILL LIVE;
(2) FLEET.md's three unexercised build-step falsifiers (report-cooperation, noisy
`session.idle`, silent soft-kill) were incorrectly bundled as RETIRED alongside the one
(keyed-provider) that actually was exercised — split out and restored to STILL LIVE; (3)
SIMPLEST.md §6.3/WATCHLIST.md #3 (re-ring reliability) was retired despite the source docs
stating the live-pane arm "remains untested" — moved to STILL LIVE for consistency with how
OPERATOR-STRUCTURE.md's F-MIDDLEWARE (same bounded-but-partially-untested shape) is treated.

The raw per-doc extraction this was built from is `docs/_scout-falsifiers.md` — that file is
proposed for deletion now that this doc's coverage is confirmed complete against it, since
everything in it worth keeping is folded in here with judgment applied; nothing here restates
status a source doc already states more precisely for a specific reader who wants to check
original context (each entry above is findable by doc name and section, so the primary docs
remain the citation of record).
