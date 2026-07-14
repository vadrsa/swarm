# CLEANUP PROPOSAL — repo-cleanup (post-review, FINAL)

Produced by `repo-cleanup` from two sonnet inventory scouts (`audit-scout` over `docs/audit/**`,
110 files; `design-scout` over `docs/design/**` + `docs/PHILOSOPHY.md` + `README.md` +
`WORLD.md`, 43 files — 153 files total, plus this proposal and `docs/design/FALSIFIERS.md` which
are new), then reviewed by `cleanup-red` (opus) as the record's advocate. Full per-file reasoning
is in `docs/_scout-audit.md` and `docs/_scout-design.md`; the reviewer's full reasoning is in
`docs/_cleanup-red-verdict.md`.

**Reviewer verdict: 0 of 4 proposed original-doc deletions survive.** All 4 are vetoed to KEEP,
each for a specific, checked reason (a live citation-by-path, a cited byte-count exhibit, a
citation substrate that's already drifted, or evidence a successor doc only summarizes). Full
reasoning below under "What changed after review." This proposal now reflects the **final**
state: 0 original docs deleted, all headered SUPERSEDED-BUT-HISTORICAL instead.

## Summary counts (final, recounted directly from both scout tables — supersedes the scouts'
own self-reported summaries, which undercounted design's SUPERSEDED-BUT-HISTORICAL class by 1:
REVIEW.md and SELF-AUDIT.md were present in the table but omitted from the scout's own summary
paragraph and from an earlier draft of this proposal's header table; both fixed below.)

| Class | docs/audit/** | docs/design/** + root | Total |
|---|---|---|---|
| CURRENT | 42 | 18 | 60 |
| SUPERSEDED-BUT-HISTORICAL | 68 | 25 | 93 |
| DEAD (deleted) | 0 | 0 | 0 |
| **Total classified** | **110** | **43** | **153** |

(The 4 originally-proposed-DEAD docs — all in docs/audit/ — moved to SUPERSEDED-BUT-HISTORICAL
after review: 64 → 68.)

Plus three scratch artifacts from this cleanup run — see disposition below, not part of the
153-file corpus count.

---

## WHAT CHANGED AFTER REVIEW

`cleanup-red` read all 4 proposed-DEAD files directly (not the scout summaries), checked the
docs claimed to absorb their content, and vetoed every one:

1. **`docs/audit/_falsifier-rubric.md`** — **VETOED, KEEP.** Cited *by path* in
   `org-review-falsifier-2026-07-12.md:52-53` and in all three `_fp-slice-{a,b,c}.md` as the
   pre-registered rubric behind the "0 of 135 unfalsifiable, 17 fired" finding that now
   propagates into `MODEL-FIT.md §5`, `MODEL-FIT-MANDATE.md`, and the shipped `--reason`
   mandate. It also defines the `a-independent`/`a-self-report` split used by name downstream
   but never redefined. Deleting it would fire ORG-REVIEW.md's own falsifier F6
   ("classifications rot — a printed classification can't be re-derived from its citation") by
   hand.
2. **`docs/audit/_fp-compliance-shard-brief.md`** — **VETOED, KEEP.** `docs/design/ORG-REVIEW.md:468`
   cites this file's existence *and byte count* (5,024 B) as VERIFIED evidence that a briefing
   artifact was real. A doc being kept in `docs/design/` cites this one as a verified exhibit —
   deleting it breaks that citation. It also carries the Q2i/Q2ii self-labelled-vs-substantive
   split and the Q6 power-separation design (parent keeps adjudication, children only surface),
   recorded nowhere else.
3. **`docs/audit/_hcrev-modelfit-snapshot.md`** — **VETOED, KEEP — the original proposal's worst
   call.** audit-scout's spot-check ("matches MODEL-FIT.md's opening section") verified a region
   that hadn't changed; the reviewer diffed the full files and found **87 changed lines** — the
   snapshot holds the *pre-overrule* ruling text, not a duplicate of current MODEL-FIT.md. Worse:
   it's the citation substrate for `_hcrev-fit.md`'s 9 line-number citations, and one of those
   citations (snapshot line 485) **has already drifted 33 lines** against current MODEL-FIT.md.
   The file is actively doing its job of anchoring citations against a moving target — that's the
   opposite of obsolete.
4. **`docs/audit/field-evidence-doctrine-2026-07-12-RED.md`** — **VETOED, KEEP.** The successor
   doc (154 lines) restates every R1–R9 *verdict* but drops nearly all of the *evidence*: a 9-row
   immutable-timestamp table (including the sharpest single observation in the probe — that
   `sum-a/b/c`, the only intermediate-coordinator subtree, spawned 24–43s after doctrine text was
   restored), an 8-token cold-recoverability table with file:line citations, a `bin/swarm:64`
   source quote, and every one of the review's own pre-registered, still-unrun falsifiers.
   Notably, the successor's own §5 argues that author summaries drift kind to the author and that
   a fresh reviewer's primary artifacts are what catch it — while being used to justify deleting
   exactly those primary artifacts.

**All 4 are headered SUPERSEDED-BUT-HISTORICAL below instead of deleted** — see the audit-corpus
table for the specific header text for each.

### Cleanup-run scratch files — final disposition

- **`docs/_scout-design.md`** — reviewer confirmed DEAD, no objection. Deleted in this PR.
- **`docs/_scout-audit.md`** — reviewer confirmed DEAD **conditional on the headers actually
  being written** (this proposal's audit-corpus section is a condensed summary that explicitly
  defers to this file for full per-file pairings). Deleted in this PR, in the same commit that
  applies the 68 audit-corpus headers — not before.
- **`docs/_scout-falsifiers.md`** — reviewer found 3 falsifiers **silently dropped** (not folded
  or dismissed — just absent) from `docs/design/FALSIFIERS.md`: INBOX.md P-VOL, INBOX.md
  P-TRIAGE, and ORG-REVIEW.md F4 (the one ORG-REVIEW falsifier the doc itself reports nearly
  firing already). **Fixed**: all 3 restored into `docs/design/FALSIFIERS.md` under STILL LIVE.
  The reviewer's spot-check of ~10 other entries also found 2 questionable RETIRED
  classifications (FLEET.md's build-step falsifiers overclaimed as fully exercised; SIMPLEST
  §6.3/WATCHLIST #3 retired despite an explicitly untested arm, inconsistent with how
  OPERATOR-STRUCTURE F-MIDDLEWARE's identical shape was handled) — both corrected in
  `docs/design/FALSIFIERS.md`, along with a filing nit (2 STALE-labeled entries were sitting
  under the RETIRED heading). `docs/design/FALSIFIERS.md`'s coverage is now confirmed complete
  against the raw extraction. Deleted in this PR.

---

## SUPERSEDED-BUT-HISTORICAL — headers to add (not deletions)

For every file below, add this line immediately after the title (or at the top if untitled):

`> SUPERSEDED by <doc>; kept for the record (<what it records>).`

Full list (88 files) — path, superseding doc, and what's kept, taken directly from the scouts'
per-file reasoning. See `docs/_scout-audit.md` / `docs/_scout-design.md` for the complete
original sentences; condensed here to the header's two fields.

### docs/design/ (25)

| Path | Superseded by | Kept for |
|---|---|---|
| FLEET.md | FLEET-EVAL.md | launcher-override architecture, leaf-contract §4, leaf-liveness §5, concept-cost accounting §9 |
| FLEET-EVAL.md | FLEET-EVAL-V3.md | first measured run; caught rig bug §4; adversarial-correction discipline §9 |
| FLEET-EVAL-RED.md | FLEET-EVAL.md §9 (folded) | raw review-process record; all 5 objections resolved |
| FLEET-EVAL-V3-RED.md | — (still-live, not fully folded) | unresolved "must fix" line-level corrections not yet applied |
| HARNESS-RED.md | HARNESS.md §10 (folded) | origin record of a mis-cited causal claim and a citation-integrity pattern recurring in LOOP.md |
| docs/design/archive/HARNESS.md | (different topic, not superseded on same axis) | benchmark protocol R2, quota-signal asymmetry R3, successor-based harness-switching R4 |
| LOOP-RED.md | LOOP.md §10 (folded) | measured finding that a v2 GLM-hang citation was wrongly used as live evidence |
| LOOP-RED3.md | LOOP.md §10 (mostly folded; repair #6 confirmed resolved by repo-cleanup, see FALSIFIERS.md) | quiescence predicate rebuild, M1b addition, confidence revision history |
| DECISION-WIRING.md | HOOK-WIRING.md §13 | foundational grant/claim/attribution ritual design PIPE/PROXY/HOOK inherit |
| DECISIONS.md | HOOK-WIRING.md §13 (via DECISION-WIRING) | cited evidentiary base — PR #62 case study, falsifier-corpus audit |
| PIPELINE-WIRING.md | HOOK-WIRING.md §13 | barrier-vs-tendency ordering-guarantee analysis |
| PROXY-WIRING.md | HOOK-WIRING.md §13 | interposition-safety asymmetry analysis, measured plane volume |
| MODEL-FIT-MANDATE.md | MODEL-FIT.md §5 | falsifier-audit evidence (0/135 unfalsifiable, 17 fired), blast-radius measurement |
| OPERATOR-STRUCTURE-FIX.md | OPERATOR-STRUCTURE.md (retracted wholesale) | clearest real-reversal case in the corpus — a 9-hunk diff built, tested 79/80 green, run, then abandoned |
| OPERATOR-STRUCTURE-GRAVE.md | OPERATOR-STRUCTURE.md | graveyard-check rulings; "seeing is global" doctrine contradiction; WORLD.md concept diagnosis |
| OPERATOR-STRUCTURE-RED.md | OPERATOR-STRUCTURE.md §1 (folded) | decisive kill of claim C, disproven on source |
| OPERATOR-STRUCTURE-RED2.md | OPERATOR-STRUCTURE.md (folded) | core finding that caused the pivot to doctrine+middleware |
| OPERATOR-STRUCTURE-RED3.md | OPERATOR-STRUCTURE.md §2/§4e/§4e′ (folded) | mechanism discovery, miscitation correction, authority/agent-graph distinction |
| OPENCODE-PLUGIN-RED.md | OPENCODE-PLUGIN.md §3.1/§8 (folded) | primary-source record of the self-ring ordering-bug reversal |
| REVIEW.md | (absorbed into shipped bin/swarm) | evidentiary trail behind SELF-AUDIT.md's R1–R6 fixes (queue-depth trailer, truncation hole, broken-pipe exit code) |
| SELF-AUDIT.md | (absorbed into shipped bin/swarm) | 27→9 concept traceability table; R1–R7 post-review amendment ledger, cited as prior art by ORG-REVIEW.md |
| SIMPLEST.md | WORLD.md | founding 27→9 concept-deletion argument WORLD.md/PHILOSOPHY.md build on |
| WATCHLIST.md | (companion to SIMPLEST.md) | #4 "journals rot into mush" confirmed FIRED by ORG-REVIEW.md §6c″ |
| docs/design/archive/CODEX-DESIGN.md | OPENCODE-PLUGIN.md §9 (conclusion doesn't transfer) | spawn/hook-mapping mechanism, NOT-in-v1 scoping decisions reused as template |
| docs/design/archive/CODEX-CAPABILITIES.md | (companion to CODEX-DESIGN.md) | VERIFIED-tagged capability probe methodology OPENCODE-PLUGIN.md's probes copy |

Note: `docs/design/archive/*` are already physically separated into an `archive/` subdirectory
— arguably they need no additional header since the directory name already signals status, but
the operator's instruction is uniform (add the header to every SUPERSEDED-BUT-HISTORICAL doc),
so they're included.

### docs/audit/ (68 — grouped by source cluster; see docs/_scout-audit.md for the full row-by-row list)

**The 4 reviewer-vetoed docs (moved here from the DEAD proposal):**

| Path | Superseded by | Kept for |
|---|---|---|
| `_falsifier-rubric.md` | (still actively cited by path, not truly superseded — headered for consistency with the rest of this list) | the pre-registered classification rubric behind the 0/135 + 17-fired counts; the a-independent/a-self-report distinction not restated downstream |
| `_fp-compliance-shard-brief.md` | (still actively cited by path + byte count in `docs/design/ORG-REVIEW.md:468`) | the Q2i/Q2ii self-labelled-vs-substantive split and Q6 power-separation design; cited as a VERIFIED exhibit |
| `_hcrev-modelfit-snapshot.md` | `docs/design/MODEL-FIT.md` (partially — the doc has since drifted 33 lines past §5) | the frozen citation substrate `_hcrev-fit.md`'s 9 line-cites resolve against; holds the pre-overrule ruling text (87 lines differ from current MODEL-FIT.md) |
| `field-evidence-doctrine-2026-07-12-RED.md` | `field-evidence-doctrine-2026-07-12.md` (verdicts only, not evidence) | primary-artifact forensics behind R1–R9 (the 9-row timestamp table, the 8-token cold-recoverability table, `bin/swarm:64`), and the review's own unrun pre-registered falsifiers |

**bench/ (25 files):** all of `fleet-briefs-v1/**` (11 files) and `fleet-briefs-v2/**` (11
files) superseded by the matching `fleet-briefs-v3/**` file, path-for-path;
`results-{claude-base,deepseek,glm}.md` (3 files) superseded by
`results-v3-{claude-base,deepseek,glm}.md`. Kept for: the v1→v2 bare-path rig-bug fix, the
v2→v3 cwd/reporting fix, and (for results files) the actual dated measurements — not a uniform
"v3 is better" story, deepseek's v3 score is worse, GLM's is better, both rig-artifact
corrections.

**Dated field-evidence/org-review/mandate/red2 (24 files):** each superseded by the shipped
doctrine/code/final-doc it fed into (see docs/_scout-audit.md rows 99–124 for the specific
superseding doc per file); kept for original measurements, repro steps, or evidentiary bases
not restated in full elsewhere (e.g. `org-review-red-2026-07-12.md`'s "MAJOR SURGERY" verdict —
flagged for a human check on whether `docs/design/ORG-REVIEW.md` was actually revised
post-review; `weak-model-deleg-evidence/{RED-verdict,report-opus}.md` kept as primary unabridged
evidence).

**Misc audit shards (11 files, excluding the 4 vetoed docs already tabled above):**
`_fp-slice-{a,b,c}.md`, `_hc-price.md` (partial), `_hcrev-*.md`
(4 files, excluding the vetoed modelfit-snapshot), `inline-work-audit-RED.md`,
`model-fit-eval-mining-2026-07-13.md`,
`ps-model-red.md`, `ps-model-red2.md`, `spawn-hardening-2026-07-14.md`,
`spawn-red-2026-07-14.md`, `structure-mechanics-2026-07-12.md`, `trigger-red-2026-07-12.md`,
and others — each superseded by a specific later doc/shipped-code fix, each kept for a specific
measurement, reasoning trail, or open item not restated elsewhere. Full per-file
superseded-by/kept-for pairs are in `docs/_scout-audit.md`; do not hand-copy them into headers
without checking that file, since the count and pairing here is a condensed summary.

---

## Flagged items for the operator (open, not resolved by this cleanup)

- **`docs/audit/org-review-red-2026-07-12.md`**: audit-scout found no corrected "ORG-REVIEW.md
  v2" in the file set despite this RED's "MAJOR SURGERY" verdict (it kills the flagship BLOCKED
  example as factually false). Recommend a human check whether `docs/design/ORG-REVIEW.md` was
  actually revised post-review, separate from this cleanup.

## Judgment calls made during this cleanup (for the record)

- **LOOP-RED3.md repair #6** — design-scout flagged this as possibly unresolved; repo-cleanup
  checked directly and confirmed `LOOP.md` §4b.3 (~line 361) does define the "per model
  generation" reopening trigger. Treated as resolved in `docs/design/FALSIFIERS.md` and the
  header table above.
- **`docs/audit/bench/.swarm/journal/bench-v1.md`** — untracked, gitignored swarm-session debris
  that leaked into the repo tree during `audit-scout`'s own sub-child fan-out. Removed directly
  by repo-cleanup (it was never tracked by git and would not have appeared in this PR's diff
  regardless).
- **`OPENCODE-PLUGIN-RED.md` / `FLEET-EVAL-RED.md` — considered and declined a stricter DEAD
  bar**: design-scout flagged these as the closest candidates for DEAD instead of
  SUPERSEDED-BUT-HISTORICAL, since their findings are fully folded into their targets with no
  unresolved items. Declined: the operator's own SUPERSEDED-BUT-HISTORICAL class exists
  precisely for "fully folded, but records a real decision/reversal/finding worth keeping" —
  design-scout's own reasoning for both docs names exactly that. Kept as
  SUPERSEDED-BUT-HISTORICAL.
- **`_hcrev-modelfit-snapshot.md` drift** — the reviewer's diff surfaced that
  `_hcrev-fit.md`'s citation into the snapshot at line 485 has already drifted 33 lines against
  current `MODEL-FIT.md`. Not fixed by this cleanup (out of scope — it's a citation-repair task,
  not a classification one); flagged here so it isn't lost. Whoever next touches `_hcrev-fit.md`
  or `MODEL-FIT.md` should be aware the line-cites past §5 need re-verification.

## Review process (for the record)

`cleanup-red` (opus) reviewed all 4 original-doc DEAD proposals by reading the files directly,
not the scout summaries, and checking the docs claimed to absorb their content. All 4 were
vetoed to KEEP — see "What changed after review" above. The reviewer also spot-checked
`docs/design/FALSIFIERS.md` against ~10 source entries and found 3 silent drops and 2
questionable RETIRED calls, both fixed. Full reasoning: `docs/_cleanup-red-verdict.md`.
