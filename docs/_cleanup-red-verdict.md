# RED VERDICT — review of `docs/CLEANUP-PROPOSAL.md`

**Reviewer:** `cleanup-red` (opus), the record's advocate. **Default: KEEP.**
Every file below was read in full by me. I did not rely on a scout's one-line summary,
and where the proposal asserts a successor "absorbs" a file, I read the successor and
checked the specific content.

**Bottom line: 1 of the 4 proposed deletions survives. 3 are vetoed to KEEP.**
The 3 cleanup-scratch files: 2 CONFIRMED-DEAD, 1 KEPT-UNTIL-FIXED.
The FALSIFIERS.md spot-check found **3 dropped entries and 2 questionable classifications.**

---

## 1. `docs/audit/_falsifier-rubric.md` — **KEEP** (veto)

**The proposal says:** "instructional dispatch text only, no standalone finding… content fully
consumed by the shard outputs it specifies."

**Why I veto.** Two reasons, and the second is the strong one.

**(a) It is a live citation, not a dead brief.** Four still-kept documents cite it *by path* as
the standard their numbers were produced against:

- `docs/audit/org-review-falsifier-2026-07-12.md:52-53` — *"four independent readers
  (fp-slice-a/b/c + me) applied one shared rubric (`docs/audit/_falsifier-rubric.md`),
  **written before any reading, so the counts are commensurable.**"* and again at `:353`
  under "Shared rubric."
- `_fp-slice-a.md:3`, `_fp-slice-b.md`, `_fp-slice-c.md` — each opens *"Rubric:
  docs/audit/_falsifier-rubric.md."*
- `docs/design/MODEL-FIT-MANDATE.md` cites it too.

Deleting it turns the single most-cited number in this repo — **"0 of 135 unfalsifiable,
17 fired"**, which propagates into `MODEL-FIT.md §5`, `MODEL-FIT-MANDATE.md`, `HARNESS.md §7.2`,
and the `--reason` mandate now shipped in `bin/swarm` — into a number whose measuring
instrument no longer exists. `ORG-REVIEW.md`'s own falsifier **F6** is *"classifications rot — a
printed classification can't be re-derived from its citation."* Deleting the rubric **fires F6
by hand.**

**(b) The rubric is not merely instructions; it contains the methodological decision the
finding rests on.** Lines 31–40 define the `a-independent` / `a-self-report` split:

> *"if the observation is file-observable ONLY because the agent itself would have to choose to
> write it down… that is still (a) — but flag it `a-self-report`. **This distinction matters
> enormously to the parent's question**… A TRUE (a) has an INDEPENDENT witness (mtime, a queue
> file, a git artifact… a record the agent does not author as narrative)."

That is a *designed epistemic control* — the thing that stops "the agent said it discharged its
falsifier" from counting as evidence. `org-review-falsifier` reports counts in those buckets
(`:201`, `:206` use `a-self-report` / `a-independent` as load-bearing terms) but **does not
restate the definition of the split or the borderline rule that produces it.** A future reader
of the 0-of-135 finding cannot tell what was counted. That is not "no standalone finding" —
that is the finding's definition living in exactly one file.

**Cheapest fix if the operator wants the tree tidier:** header it SUPERSEDED-BUT-HISTORICAL
("kept for: the pre-registered classification rubric behind the 0/135 + 17-fired counts, and the
a-independent/a-self-report distinction not restated downstream"). Do not delete it.

---

## 2. `docs/audit/_fp-compliance-shard-brief.md` — **KEEP** (veto)

**The proposal says:** "pure task instructions, no findings of its own."

**Why I veto.** Same shape as #1, and it has one thing #1 doesn't: **a doc that is being KEPT
cites this file's existence and size as evidence in an argument.**

`docs/design/ORG-REVIEW.md:468`:

> *"**`docs/audit/_fp-compliance-shard-brief.md` (5,024 B) DOES exist.** It briefed **8
> descendants.**"*

and `docs/audit/org-review-shape-2026-07-12.md:1005` repeats it, tagged VERIFIED on disk. That is
a doc in `docs/design/` — a current, kept design doc — asserting a fact about a file this
proposal wants to delete, **with a byte count**, as proof that a briefing artifact was real
rather than claimed. Delete the file and the design doc's own VERIFIED citation becomes
unverifiable. Whatever else this is, it is not "no findings of its own": it is a *cited exhibit*.

Substantively, it also carries decisions the shard outputs never restate — the Q1–Q6 measurement
design, including the **Q2i self-labelled vs Q2ii substantive-by-my-judgment** split (lines
38–42), the definition of a RECONCILIATION ENTRY (lines 20–24: *"A pure work-log… or a pure
spawn-notice is NOT a reconciliation"*), and the deliberate power-separation instruction at Q6
(lines 54–59): *"Do not decide; hand me the line. Over-report here rather than under-report."*
That last one is a real methodological choice — the parent kept adjudication and gave the
children only surfacing — and it is the reason the compliance rate is worth anything. It is
recorded nowhere else.

**Verdict: KEEP, header as SUPERSEDED-BUT-HISTORICAL.**

---

## 3. `docs/audit/_hcrev-modelfit-snapshot.md` — **KEEP** (veto) — *this is the worst one*

**The proposal says:** "Frozen line-number snapshot of MODEL-FIT.md… MODEL-FIT.md is now merged
to main (PR #83); **the snapshot's sole purpose is obsolete.** Spot-checked by audit-scout:
content matches `docs/design/MODEL-FIT.md`'s opening section."

**Both halves of that are wrong, and the second one is wrong in the exact way the snapshot exists
to prevent.**

**(a) The snapshot is NOT a copy of current MODEL-FIT.md.** I diffed them: **87 changed lines**,
656 vs 689 lines. The snapshot is the *pre-overrule* text. The current MODEL-FIT.md carries the
operator's reversal; the snapshot carries the ruling that was reversed:

- **Snapshot :444** — *"**The ruling: `--model` stays optional, but silence stops being free.**"*
- **Current :444–453** — *"This document originally ruled here that `--model` stays optional…
  **The operator overruled it: both `--model` and `--reason` are required; a spawn missing
  either fails.**"*

The scout's "content matches the opening section" is true and irrelevant — the opening section is
the part that *didn't* change. **A spot-check of the identical region is not a spot-check.** This
is the single clearest instance in the review of a summary being trusted where the file
disagrees.

(To be fair to the deletion: current MODEL-FIT.md *does* preserve the old ruling inline, quoting
PHILOSOPHY §10, so the reversal itself is not lost. The snapshot is not the only witness to it.
But that is not why it must be kept — see (b).)

**(b) The snapshot is the citation substrate for a whole audit doc that is being KEPT, and its
line numbers have ALREADY drifted.** `docs/audit/_hcrev-fit.md` is a citation-integrity audit of
`HARNESS.md` whose entire evidence column is *line numbers into this snapshot* — **9 citations**,
by my count, in the form "MODEL-FIT snapshot line 372", "snapshot lines 477–479", "snapshot line
485 header". I checked three against both files:

| `_hcrev-fit` cites | snapshot | current MODEL-FIT.md |
|---|---|---|
| snapshot :372 (the 18/115, 16% claim) | ✅ matches | ✅ still matches (lucky) |
| snapshot :434 (0 of 135) | ✅ matches | ✅ still matches (lucky) |
| **snapshot :485 (`## 5b.` header)** | ✅ `## 5b. The default: do not change the fallback` | ❌ **prose mid-paragraph** — off by 33 lines |

The 33-line insertion of the overrule text has **already broken** citations past §5. Delete the
snapshot and `_hcrev-fit.md` — a doc whose *entire purpose* is verifying that citations point at
what they claim — becomes a doc full of citations pointing at nothing. That is not ironic, it is
disqualifying.

The proposal's own rationale ("frozen line-number snapshot… for stable citation lines") states
the file's purpose correctly and then concludes it is obsolete *because the branch merged*. The
purpose is not "the branch is unmerged"; the purpose is **"the target keeps moving."** The target
moved. The snapshot is doing its job right now.

**Verdict: KEEP.** Header it SUPERSEDED-BUT-HISTORICAL with "kept for: the frozen citation
substrate `_hcrev-fit.md`'s 9 line-cites resolve against; MODEL-FIT.md has since drifted 33 lines
at §5b."

---

## 4. `docs/audit/field-evidence-doctrine-2026-07-12-RED.md` — **KEEP** (veto)

**The proposal says:** "Fully superseded by `field-evidence-doctrine-2026-07-12.md`, whose
POST-ADVERSARIAL-REVIEW status explicitly restates every R1–R9 correction with attribution.
**Nothing left uncaptured.**"

**The successor's restatement is real, correct, honest — and it is a summary.** I read both.
The successor is 154 lines; the RED is 500. Every R1–R9 *verdict* survives. Almost none of the
*evidence* does. What is lost:

- **R2's timestamp table** (RED :92–101) — all nine baseline agent records with immutable `ts`
  values, sorted, each marked INSIDE/AFTER the 44.0 s swap window. The successor compresses this
  to *"later agent records land 0.4 s–43 s after restore."* The nine rows, the window bounds
  (`1783871020228`–`1783871064182`), and the sharpest observation — that `sum-a/b/c`, **the only
  intermediate-coordinator subtree in the entire probe**, was spawned 24–43 s *after* the
  doctrine text was restored — are gone. The successor doesn't mention `sum-a/b/c`'s timing at
  all. `grep` for `1783871` in the successor: **zero hits.**
- **R5's provenance table** (RED :266–274) — the eight "unguessable" tokens, each with the
  `file:line` in the clone where a *cold* session finds it (`queue-stats.py:14`,
  `make-fixtures.py:26`, `make-fixtures.py:65`, `queue-stats.py:157–162`…). This is the *entire
  proof* that the collector had no discriminating power. The successor asserts the conclusion —
  *"Nearly all 'unguessable' tokens exist ON DISK in the clone"* — with **no table, no file,
  no line.** `grep` for `make-fixtures` or `FIXED_NOW` in the successor: **zero hits.**
- **R3's source quote** — the successor paraphrases `my_name()` correctly but drops the
  `bin/swarm:64` code block and the `unset SWARM_AGENT_ID` line from every `launch.sh` that
  proves the fallback is *unavoidable*, not merely *default*.
- **Every one of dp-red's own falsifiers.** The RED names, per objection, the observation that
  would show *dp-red* wrong (R1: *"name a behavioral prediction the two new paragraphs make that
  baseline point 5 does not"*; R5: *"run a cold-session control arm… my reading predicts ~17/18"*;
  R9: *"point me at the pre-registration"*). These are **standing, unrun, pre-registered
  predictions with a named collector.** The successor keeps three of them as a "follow-up menu"
  and drops the rest. A reviewer's falsifier is exactly the artifact this project's whole
  doctrine says must not evaporate.
- **The quote-truncation catch (R4).** The RED shows the evidence file *truncating* the r3
  journal quote in a way that changed its meaning, and prints the full clause. The successor
  records that the correction happened; it does not preserve the demonstration. The lesson —
  *how* an author's own summary silently loaded a quote — is only legible from the RED.

**And the successor's own §5 makes my argument for me:**

> *"the pre-review draft of this file repeated, at smaller scale, the failure v3-red found in the
> FLEET synthesis the same day — **kindness toward the author's own design**… **Two independent
> red reviews catching the same author-bias direction in one day is itself a datum in favor of
> the mandatory-fresh-reviewer convention.**"*

The doc that says "author summaries drift kind to the author, and the fresh reviewer's primary
artifacts are what caught it" is being used to justify **deleting the fresh reviewer's primary
artifacts and keeping only the author's summary.** That is the exact failure the file names,
performed on the file that names it. Six other docs (`OPERATOR-STRUCTURE-FIX/GRAVE/RED.md`,
`_theater-reader.md`, `_theater-bench.md`, the successor itself) cite `dp-red` by name.

**Verdict: KEEP.** This is the highest-value deletion candidate in the set and the one I'd fight
hardest for. Header as SUPERSEDED-BUT-HISTORICAL — "kept for: primary-artifact forensics behind
R1–R9 (the 9-row `ts` table, the 8-token cold-recoverability table, `bin/swarm:64`), and dp-red's
own unrun pre-registered falsifiers."

---

## 5–7. The three cleanup-scratch files

### `docs/_scout-audit.md` — **CONFIRMED-DEAD** ✅ (with one condition)
Its judgment is fully carried into `CLEANUP-PROPOSAL.md` and into the SUPERSEDED-header list.
**Condition:** `CLEANUP-PROPOSAL.md:129-136` itself says the audit-corpus header table is a
*condensed summary* and instructs *"do not hand-copy them into headers without checking
[docs/_scout-audit.md], since the count and pairing here is a condensed summary."* So this file
is **not dead until the headers are actually written.** Delete it in the same commit that lands
the headers, not before — otherwise the proposal points at a file that doesn't exist for the
detail it admits it doesn't carry.

### `docs/_scout-design.md` — **CONFIRMED-DEAD** ✅
Same status; the design-corpus table in the proposal (24 rows, each with superseded-by and
kept-for) is complete rather than condensed. Nothing lost. No objection.

### `docs/_scout-falsifiers.md` — **KEEP UNTIL FALSIFIERS.md IS FIXED** ⚠️
The absorption claim is **not fully true.** Three entries in the scout extraction appear
**nowhere** in `docs/design/FALSIFIERS.md` — not under STILL LIVE, not RETIRED, not STALE:

| Dropped entry | scout line | status in scout |
|---|---|---|
| **INBOX.md P-VOL** — volume-threshold probe gating E2 (seat-triage paragraph) | `:124` | open, designed-not-run |
| **INBOX.md P-TRIAGE** — one-stint triage-paragraph trial, contingent on P-VOL | `:125` | open, designed-not-run |
| **ORG-REVIEW.md F4** — session latency presented as human latency | `:135` | open/unrun (doc self-corrected one near-miss, §3.5/§4c′) |

FALSIFIERS.md carries INBOX's P-CLAIM-AUDIT and Idea-1 falsifiers, and ORG-REVIEW's F1/F2/F3/F5/F6
— so these three are **silent omissions, not deliberate merges** (nothing in FALSIFIERS.md says
they were folded or dismissed). ORG-REVIEW F4 is the notable loss: it is the one ORG-REVIEW
falsifier the doc itself reports having *nearly fired* already.

**These are lower-stakes only if FALSIFIERS.md is complete. It isn't.** Fix FALSIFIERS.md (add
the three), then this file is genuinely dead. Until then it is the only witness that they existed.

---

## FALSIFIERS.md spot-check — 3 drops + 2 questionable classifications

Sampled across clusters (fleet, harness-loop, operator-structure, model-fit, misc-meta) and
checked against the source docs, not the scout summary.

**Correct (verified against source):**
- ✅ **OPERATOR-STRUCTURE.md F-SPAN → RETIRED, "run, not fired, 0 of 61"** —
  `OPERATOR-STRUCTURE.md:383` says exactly that, in the doc's own voice: *"F-SPAN — the falsifier
  I named as 'the one I would watch first' — DOES NOT FIRE: 0 of 61."* Correctly classified,
  and FALSIFIERS.md correctly preserves the caveat ("doesn't prove the tree never floods").
- ✅ **OPERATOR-STRUCTURE-RED.md attack C → RETIRED** — source says "CHECKED, confirmed
  impossible (kills claim C)". Matches.
- ✅ **MODEL-FIT.md "a leaf stays a leaf" → RETIRED/FIRED-FALSE (18/115)** — matches
  MODEL-FIT.md:372 verbatim.
- ✅ **HOOK-WIRING.md §12 Condition 1 → RETIRED as VOID** — matches the scout and the doc's own
  declaration.
- ✅ **LOOP-RED3 repair 6 → RETIRED** — repo-cleanup checked `LOOP.md` §4b.3 directly and
  *corrected* the scout's "likely still OPEN." This is the review working: a scout flag
  overturned by reading the source. Good.
- ✅ **LOOP-RED3 repair 5 → STILL LIVE** — scout said "effectively still OPEN in substance";
  FALSIFIERS.md kept it live with that exact reasoning. Correct.
- ✅ **OPENCODE-PLUGIN F3 → RETIRED-as-FIRED (93 sessions)** — matches, and FALSIFIERS.md adds the
  right editorial note (a confirmed hazard, not an open question).

**Questionable — 2:**

1. ⚠️ **FLEET.md's 4 build-step falsifiers → "RETIRED: superseded by FLEET-EVAL.md's actual
   measured runs, which exercised all four paths directly."** The scout said three of the four
   were **UNOBSERVED**, and only the keyed-provider one was "later exercised by FLEET-EVAL's
   actual keyed runs." I checked: `grep -i soft-kill docs/design/FLEET-EVAL.md` → **0 hits**
   (FLEET.md has 4). FLEET-EVAL does not appear to exercise the silent-soft-kill path at all.
   "Exercised all four paths directly" is an upgrade of the scout's claim that the source doesn't
   support. The falsifiers may still be fairly retired (the design they gate moved on), but the
   *stated reason* is not true, and FALSIFIERS.md's own retirement rule requires either
   "answered/fired/refuted" or "the mechanism it gates is superseded" — the second may hold, the
   first is asserted and doesn't.

2. ⚠️ **SIMPLEST.md §6.3 / WATCHLIST.md #3 (re-ring stalls) → RETIRED "as partially fired."**
   The scout said **"partially fired (degraded, not fully broken)"** and noted the source docs
   themselves say live-pane reliability *"remains untested."* "Partially fired with an untested
   arm" is a live falsifier with a bounded result, not a retired one — this is the same shape as
   OPERATOR-STRUCTURE F-MIDDLEWARE, which FALSIFIERS.md *correctly* kept under STILL LIVE for its
   untested grandchild arm. Inconsistent treatment of the same shape. Recommend moving to STILL
   LIVE (or at minimum, RETIRED-with-open-arm noted).

**Filing nit (not a misclassification):** `OPERATOR-STRUCTURE-RED3.md §H` and
`archive/CODEX-DESIGN.md §8` are both labeled **STALE** in their entry text but physically filed
under the **RETIRED** heading, while a separate STALE section exists below. Cosmetic; makes the
summary counts (~35 / ~10) unreproducible from the file.

**Otherwise: the consolidation is good work.** The judgment calls I could check went the right
way, the duplicate merges (SIMPLEST §6.5 ≡ WATCHLIST #5, HARNESS §9.9 ≡ LOOP §8) are honest and
labeled, and the LOOP-RED3-repair-6 correction is a genuine improvement on its source. The
problems are three *omissions* and two *over-retirements*, not systematic error.

---

## Summary

| Item | Verdict |
|---|---|
| `_falsifier-rubric.md` | **KEEP** — cited by path as the pre-registered instrument behind 0/135+17; defines the a-independent/a-self-report split restated nowhere else |
| `_fp-compliance-shard-brief.md` | **KEEP** — `ORG-REVIEW.md:468` cites its existence + byte count as VERIFIED evidence; carries the Q2i/Q2ii and Q6 power-separation design |
| `_hcrev-modelfit-snapshot.md` | **KEEP** — not a duplicate (87 lines differ; it holds the pre-overrule ruling); it is the citation substrate for `_hcrev-fit.md`'s 9 line-cites, and MODEL-FIT.md has **already drifted 33 lines** past §5 |
| `field-evidence-doctrine-2026-07-12-RED.md` | **KEEP** — successor restates verdicts, not evidence: loses the 9-row `ts` table, the 8-token cold-recoverability table, `bin/swarm:64`, and every one of dp-red's own unrun falsifiers |
| `_scout-audit.md` | **CONFIRMED-DEAD** — but delete only in the commit that lands the headers (the proposal itself defers to it for the audit-corpus pairings) |
| `_scout-design.md` | **CONFIRMED-DEAD** — no objection |
| `_scout-falsifiers.md` | **KEEP until FALSIFIERS.md is fixed** — 3 entries (INBOX P-VOL, INBOX P-TRIAGE, ORG-REVIEW F4) were silently dropped, not folded |

**Of the 4 proposed original-doc deletions: 0 survive as DEAD. All 4 vetoed to KEEP.**

I set out expecting to confirm most of them and confirmed none. Each of the four is either
load-bearing as a citation target or holds evidence its successor only summarizes: the two "pure
instructions" files are cited by path (and by byte count) in docs that are being kept; the
snapshot is actively resolving line-cites that have already gone stale against current
MODEL-FIT.md; and the RED holds the forensics its successor compresses away.

**All 4 should be headered SUPERSEDED-BUT-HISTORICAL rather than deleted**, which costs nothing
and is what the rest of the corpus is already getting.

---

*`cleanup-red`. Every claim above is checked against a file I opened, not a summary. Where I
diffed, I ran the diff. Where I say "zero hits," I ran the grep.*
