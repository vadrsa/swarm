# INDEX — the map

Every doc under `docs/` (plus root `README.md`/`WORLD.md`), classified, one line each. This is
the ground truth for "where do I look" — read this before searching the tree.

**Classes:**
- **CURRENT** — live, referenced, load-bearing.
- **SUPERSEDED-BUT-HISTORICAL** — replaced by a newer doc, but records a real decision,
  reversal, or measured finding; has a `> SUPERSEDED by ...` header at the top pointing to the
  successor and naming what it's kept for.
- **RED/REVIEW** — an adversarial review; noted whether it's still live or fully folded (folded
  ones are also headered SUPERSEDED-BUT-HISTORICAL).

**Full classification detail and reasoning:** `docs/CLEANUP-PROPOSAL.md` (what was proposed,
what the reviewer vetoed, why). **The consolidated live falsifier list:** `docs/design/FALSIFIERS.md`.

Produced by `repo-cleanup` from `audit-scout` + `design-scout` (sonnet inventory) and
`cleanup-red` (opus review). 153 docs classified: 60 CURRENT, 93 SUPERSEDED-BUT-HISTORICAL,
0 deleted (the reviewer vetoed all 4 original deletion proposals — see CLEANUP-PROPOSAL.md).

---

## Top level

| Doc | Class | What it is |
|---|---|---|
| `README.md` | CURRENT | User-facing entry point; matches the shipped `bin/swarm`/`WORLD.md` contract. |
| `WORLD.md` | CURRENT | The living contract itself — `swarm world` prints it; successor to `SIMPLEST.md`. |
| `docs/PHILOSOPHY.md` | CURRENT | Top-level maintained doctrine; cited as live law across the design corpus. |
| `docs/INDEX.md` | — | This file. |
| `docs/CLEANUP-PROPOSAL.md` | — | The full record of this cleanup: proposed deletions, reviewer verdict, header list. |

## docs/design/ — the core design corpus (43 docs: 18 CURRENT, 25 SUPERSEDED-BUT-HISTORICAL)

**Start here for live doctrine:**

| Doc | Class | What it is |
|---|---|---|
| `SPAN.md` | CURRENT | Foundational attention-span design — self-test, delegation ladder, falsifier graveyard (now consolidated in `FALSIFIERS.md`). |
| `STRUCTURE.md` | CURRENT | Independent investigation into where tree structure/persistence comes from. |
| `OPERATOR-STRUCTURE.md` | CURRENT | Terminal synthesis: operator is outside the swarm, doctrine + send-middleware is the answer. |
| `HOOK-WIRING.md` | CURRENT | §13 "ADOPTED" — the universal send-middleware that actually shipped. |
| `HARNESS.md` | CURRENT | Live launcher-body/model-token seam design; base doc `LOOP.md` builds on. |
| `LOOP.md` | CURRENT | Live design for running non-Claude models in a controlled loop; Build 1 shipped. |
| `MODEL-FIT.md` | CURRENT | Model-selection doctrine at spawn (3-rung ladder); §5 amended for the operator's `--reason`-mandate overrule. |
| `MODEL-FIT-RED.md` | CURRENT (review) | Live, not-fully-folded critique of `MODEL-FIT.md`. |
| `TRIGGER.md` | CURRENT | Why the swarm skill doesn't auto-fire; shipped fix, one open follow-up (§6b). |
| `FLEET-EVAL-V3.md` | CURRENT | Latest, most-corrected measurement of Chinese-model swarm-fitness. |
| `OPENCODE-PLUGIN.md` | CURRENT | Recommendation to build a third `--agent` kind (opencode); red-team-corrected. |
| `INBOX.md` | CURRENT | Research verdict on operator-mailbox ideas ("no build; extract E1/E2/E3"). |
| `INDUSTRY-PATTERNS.md` | CURRENT | Outside-view analysis of a later operator-mailbox proposal. |
| `ONBOARDING.md` | CURRENT | Recommendation with a drafted, not-yet-applied SKILL.md diff. |
| `ORG-REVIEW.md` | CURRENT | Live recommendation ("ship `swarm ps` un-collapse first"); companion to `OPERATOR-STRUCTURE.md`. |

**Superseded but kept for the record** (each file carries its own `> SUPERSEDED by ...` header
with full detail — this is a index-level summary):

| Doc | Superseded by | Kept for |
|---|---|---|
| `FLEET.md` | `FLEET-EVAL.md` | launcher-override architecture, leaf-contract, leaf-liveness protocol, concept-cost accounting |
| `FLEET-EVAL.md` | `FLEET-EVAL-V3.md` | first measured run; caught rig bug; adversarial-correction discipline |
| `FLEET-EVAL-RED.md` | `FLEET-EVAL.md` §9 (folded) | raw review-process record |
| `FLEET-EVAL-V3-RED.md` | — (still-live) | unresolved line-level corrections not yet applied |
| `HARNESS-RED.md` | `HARNESS.md` §10 (folded) | citation-integrity pattern recurring in `LOOP.md` |
| `archive/HARNESS.md` | (different topic — codex-vs-claude choice, not a stale draft) | benchmark protocol, quota-signal asymmetry finding, harness-switching pattern |
| `LOOP-RED.md` | `LOOP.md` §10 (folded) | measured GLM-hang citation-quality finding |
| `LOOP-RED3.md` | `LOOP.md` §10 (mostly folded; repair #6 confirmed resolved, see `FALSIFIERS.md`) | quiescence predicate rebuild, M1b addition |
| `DECISION-WIRING.md` | `HOOK-WIRING.md` §13 | grant/claim/attribution ritual design PIPE/PROXY/HOOK inherit |
| `DECISIONS.md` | `HOOK-WIRING.md` §13 (via DECISION-WIRING) | cited evidentiary base — PR #62 case study, falsifier-corpus audit |
| `PIPELINE-WIRING.md` | `HOOK-WIRING.md` §13 | barrier-vs-tendency ordering-guarantee analysis |
| `PROXY-WIRING.md` | `HOOK-WIRING.md` §13 | interposition-safety asymmetry analysis |
| `MODEL-FIT-MANDATE.md` | `MODEL-FIT.md` §5 (overruled) | falsifier-audit evidence (0/135, 17 fired), blast-radius measurement |
| `OPERATOR-STRUCTURE-FIX.md` | `OPERATOR-STRUCTURE.md` (retracted wholesale) | clearest real-reversal case in the corpus — built, tested 79/80 green, then abandoned |
| `OPERATOR-STRUCTURE-GRAVE.md` | `OPERATOR-STRUCTURE.md` | graveyard-check rulings; WORLD.md concept diagnosis |
| `OPERATOR-STRUCTURE-RED.md` | `OPERATOR-STRUCTURE.md` §1 (folded) | decisive kill of claim C |
| `OPERATOR-STRUCTURE-RED2.md` | `OPERATOR-STRUCTURE.md` (folded) | finding that caused the pivot to doctrine+middleware |
| `OPERATOR-STRUCTURE-RED3.md` | `OPERATOR-STRUCTURE.md` §2/§4e (folded) | mechanism discovery, authority/agent-graph distinction |
| `OPENCODE-PLUGIN-RED.md` | `OPENCODE-PLUGIN.md` §3.1/§8 (folded) | self-ring ordering-bug reversal record |
| `REVIEW.md` | (absorbed into shipped `bin/swarm`) | evidentiary trail behind `SELF-AUDIT.md`'s R1–R6 fixes |
| `SELF-AUDIT.md` | (absorbed into shipped `bin/swarm`) | 27→9 concept traceability table, R1–R7 amendment ledger |
| `SIMPLEST.md` | `WORLD.md` | founding 27→9 concept-deletion argument |
| `WATCHLIST.md` | (companion to SIMPLEST.md) | #4 "journals rot into mush" — confirmed FIRED |
| `archive/CODEX-DESIGN.md` | `OPENCODE-PLUGIN.md` §9 (conclusion doesn't transfer) | spawn/hook-mapping mechanism template |
| `archive/CODEX-CAPABILITIES.md` | (companion to CODEX-DESIGN.md) | capability probe methodology OPENCODE-PLUGIN.md's probes copy |

## docs/design/FALSIFIERS.md

The consolidated live falsifier list — every falsifier from the design corpus in one place,
classified STILL LIVE / RETIRED / STALE. Read this instead of hunting through individual docs'
falsifier sections.

## docs/audit/ — evidence, measurements, and reviews (110 docs: 42 CURRENT, 68 SUPERSEDED-BUT-HISTORICAL)

This tree is dense — use the clusters below rather than browsing file-by-file.

**Harness-capability research chain** (`_hc-*.md`, `_hcr-*.md`, `_hcrev-*.md`) — mostly CURRENT,
feeds `docs/design/HARNESS.md`. Start with `_hc-mech.md` (code trace), `_hc-industry.md`
(outside-view survey), `_hc-slm.md` (small-model research), `_hcr-evidence.md` (open findings
F-1/F-2/F-3 still load-bearing).

**Opencode-as-harness investigation** (`oc-*.md`, `opencode-*.md`) — mostly CURRENT. Start with
`oc-report-digest.md` (readable synthesis layer), which cites the primary-source docs
(`opencode-plugin-api.md`, `opencode-plugin-probe.md`).

**Falsifier-orphaning study** (`_falsifier-rubric.md`, `_fp-*.md`, `org-review-falsifier-*.md`) —
the rubric and shards are SUPERSEDED-BUT-HISTORICAL (headered; still actively cited by path —
see `CLEANUP-PROPOSAL.md`'s "What changed after review"), the synthesis
(`org-review-falsifier-2026-07-12.md`) is SUPERSEDED-BUT-HISTORICAL, kept for the "0 of 135
unfalsifiable, 17 fired" finding.

**Operator-structure review chain** (`org-review-*.md`, `red2-*.md`) — dated 2026-07-12, mostly
SUPERSEDED-BUT-HISTORICAL, feeds `docs/design/OPERATOR-STRUCTURE*.md`. Note:
`org-review-red-2026-07-12.md` is flagged in `CLEANUP-PROPOSAL.md` for a human check — its
"MAJOR SURGERY" verdict has no confirmed corrected successor in this file set.

**Model-fit / mandate chain** (`mandate-*.md`, `model-fit-eval-mining-2026-07-13.md`,
`ps-model-red*.md`) — SUPERSEDED-BUT-HISTORICAL, feeds the shipped `--reason` mandate in
`bin/swarm`. `_hcrev-modelfit-snapshot.md` is a reviewer-vetoed KEEP — see its header for why
(it's the citation substrate `_hcrev-fit.md` still resolves against).

**Field-evidence reports** (`field-evidence-*.md`) — SUPERSEDED-BUT-HISTORICAL, dated empirical
baselines behind shipped doctrine. `field-evidence-doctrine-2026-07-12-RED.md` is a
reviewer-vetoed KEEP (primary-artifact forensics its own successor summary doesn't preserve).

**Spawn-hardening review pair** (`spawn-hardening-2026-07-14.md`, `spawn-red-2026-07-14.md`,
`followup-config-writable-2026-07-14.md`) — SUPERSEDED-BUT-HISTORICAL / CURRENT respectively;
`followup-config-writable-2026-07-14.md` is CURRENT — an open, unfixed security follow-up.

**`docs/audit/bench/`** — versioned benchmark fixtures and results (fleet-briefs v1/v2/v3,
`fleet-rubric-v1.md`, `results-*.md`, `SCORING-AUDIT-V3.md`). v1/v2 fixtures are
SUPERSEDED-BUT-HISTORICAL (each fixed a rig bug the next version carried forward); v3 fixtures
and `results-v3-*.md` are CURRENT; `results-{claude-base,deepseek,glm}.md` (v2-run) are
SUPERSEDED-BUT-HISTORICAL — not a uniform "v3 is better" story, kept as the measured record of
which direction each rig-artifact correction moved a score. `fleet-rubric-v1.md` remains the
live scoring authority (no v2/v3 rubric was ever made).

**`docs/audit/weak-model-deleg-evidence/`** — the Haiku over-delegation experiment.
`weak-model-delegation-2026-07-13.md` is CURRENT (final synthesis); `RED-verdict.md` and
`report-opus.md` are SUPERSEDED-BUT-HISTORICAL, kept as primary unabridged evidence.

**Full per-file breakdown for all 110 audit docs**: see `docs/CLEANUP-PROPOSAL.md`'s audit-corpus
section, or read each file's own `> SUPERSEDED by ...` header for its specific successor and
what it's kept for.

---

## How to use this index

1. **Looking for current doctrine on a topic?** Check the CURRENT list under `docs/design/`
   first — that's the load-bearing corpus.
2. **Want the falsifiers/open questions?** `docs/design/FALSIFIERS.md`, not individual docs'
   scattered falsifier sections.
3. **Chasing "why was X decided this way"?** Follow a CURRENT doc's citations into the
   SUPERSEDED-BUT-HISTORICAL docs it names — each one's header tells you what it's kept for.
4. **Digging through `docs/audit/`?** Use the clusters above rather than browsing — it's dense
   and mostly evidence/review docs, not doctrine.
5. **This index goes stale.** When new docs land or old ones get superseded, update this file in
   the same PR — an index nobody maintains is worse than no index.
