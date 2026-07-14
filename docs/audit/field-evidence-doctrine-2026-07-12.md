# Field evidence — onboarding-doctrine falsifiers 1 & 2, run live — 2026-07-12

> SUPERSEDED by shipped onboarding doctrine and later OPERATOR-STRUCTURE.md/red2 fixes to the root-naming bug it identified; kept for the record (the corrected trigger-gap and parent=operator contract-contradiction findings).

**Author:** `field-tester` (runners `dp-f1`, `dp-f2`; baseline arm run by me).
**Status: POST-ADVERSARIAL-REVIEW.** The fresh reviewer (`dp-red`,
`docs/audit/field-evidence-doctrine-2026-07-12-RED.md`) flipped both of this
file's pre-review headline verdicts and reframed the probe's central finding.
This version is the corrected record; the pre-review draft is in git history.
Runner logs: `/tmp/dp-f1/findings.md`, `/tmp/dp-f2/findings.md`; raw sandboxes
`/tmp/dp-f1/`, `/tmp/dp-f2/`, `/tmp/dpb/`.

---

## 1. THE LEAD FINDING — the trigger gap (survived review untouched)

Two pristine root sessions, handed genuinely parallelizable 3-part goals with no
swarm vocabulary: **the swarm skill never loaded** — despite `swarm` on PATH,
`HERDR_ENV=1`, and goals the observers themselves called "fully independent"
(every documented trigger condition met). Both fanned the work to **built-in Task
subagents** in-session and delivered everything (7 and 5 artifacts, tests 80/80);
no `.swarm/` was ever created (reviewer re-verified: no such dir at all).

**The built-in Task tool wins the decomposition before the swarm question is ever
asked.** With the explicit frontmatter phrase ("Start a swarm…"), the skill loads
every time (4/4 across the later runs). Scope precisely: *goal-shape triggering
fails; phrase triggering works.* n=2 per half. This finding depends on none of the
contested machinery below and is the probe's most actionable behavioral result.

## 2. Falsifier 1 (coordinator stance) — the shape-fact FIRED; the real cause is a tool/contract contradiction

**The shape-fact (VERIFIED, 4/4):** in every run where the skill loaded — two with
the installed doctrine text (md5 `f6f30abd…`), two with the repo-HEAD text (md5
`1c1dc0d2…`) — the observer spawned **3 children with `parent=operator`, flat**
(collectors re-derived by the reviewer from the clones' `agents/` records).

**What this does and does not mean, post-review:**

- **[R3 — the probe's real prize] `parent=operator` is the only tree a root
  session can build.** `bin/swarm` `my_name()` returns
  `SWARM_AGENT_ID or "operator"`, and a pristine root session has no
  `SWARM_AGENT_ID` — so every spawn it makes records `parent=operator`
  *unconditionally*. This is not a model illusion; it is a hard-coded default.
  **WORLD.md says "the operator is a mailbox, not a node"; the code makes
  `operator` the root session's own name.** The contract and the code contradict
  each other, and the observers reasoned CORRECTLY from what the tool
  represented: their sincere claims ("you're managing one node: me") describe the
  tree they meant and the tool cannot record.
- **[R4 — quote corrected] the observers did not "agree with the prose while
  violating it."** r3's "I am NOT putting a coordinator over it — a layer that
  only forwards 5 file paths does not earn itself (doctrine 5)" declines the
  *sub*-coordinator between a child and its files — a correct application of the
  doctrine's own earn-itself test. The failure was upstream, in what the tool let
  them express.
- **[R1 — baseline arm RETRACTED as uninformative.]** The repo-HEAD text I used
  as "pre-doctrine" already carries the 5-point doctrine including operator-span
  protection ("shape the tree so their direct load never exceeds it") — the new
  paragraph is an emphatic restatement, so both arms contained the treatment and
  the zero delta between them supports nothing. My one-variable claim rested on a
  two-paragraph diff without reading the rest of the text — the reviewer read it.
  A true pre-doctrine baseline (no operator-span language at all) remains unrun.
- **[R2 — swap-window claim narrowed.]** Only each baseline observer's FIRST
  spawn is inside the swap window (later agent records land 0.4 s–43 s after
  restore). The single-load argument (a skill's text enters context once, at
  trigger) is REASONED, not witnessed; §4's old "read and acted strictly inside
  the window" claim is withdrawn. Moot for conclusions given R1, recorded for
  method honesty.
- **[R8 — coaching caveat.]** The goal prompts say "independent" twice — the
  fan-out was handed, not discovered; and the only intermediate coordinator that
  ever appeared (dpb-1's summarizer→sum-a/b/c) grew because the operator journal
  brief it received said "delegate by default: … spawn children" verbatim. No run
  yet tests an un-decomposed goal with un-coached briefs.
- **[R9 — credit corrected.]** dp-f1's mechanism falsifier IS pre-registered —
  in its journal (`.swarm/journal/dp-f1.md` lines 220–246: stated after run 3,
  resolved by run 4's sincere-claim evidence), not in findings.md as this file
  previously implied. The reviewer's underlying point stands: cite the artifact
  that carries the credential.

**Verdict:** falsifier 1 **FIRED as a shape-fact** in all four skill-loaded runs —
but the corrected reading is **not "doctrine prose is ineffective"** (the
comparison that would show that was never validly run); it is: **the tool
structurally prevents the tree the doctrine asks for, and the contract and code
disagree about what `operator` is.** The fix is therefore contract/tool repair,
not more prose: give root sessions their own name (make the flat-row-under-human
unrepresentable), or have `swarm spawn` warn/refuse on `parent=operator` from a
root spawner. The doctrine-prose question can only be re-asked after that repair.

## 3. Falsifier 2 (mine-first) — NOT-FIRED as written; the "earned pass" is UNPROVEN

The falsifier's FIRED conditions did not occur (n=2): a labelled decomposition
entry preceded the first spawn (swarm `ts` fields; live-poll method), and first
briefs carried phase-1 tokens (18/18, 15/16).

**But the review showed the pass proves less than claimed [R5–R7]:**

- **[R5] Token presence ≠ provenance.** Nearly all "unguessable" tokens exist ON
  DISK in the clone (comments in the built tool, fixture files, fixture-generator
  source) — and the briefs order children to read those files first. A cold
  session reading the repo could produce near-identical briefs. **No cold-control
  arm was run**, so "mined its live context" vs "read its own work off disk" is
  undetermined. (The distinction may not even matter for outcome quality — but
  then the falsifier as designed cannot fire on any competent session, which is a
  design finding, not a doctrine pass.)
- **[R6] The phase-2 prompt was not preserved** in the record; one scored check
  referenced an input that is nowhere on disk.
- **[R7] The "22 s pre-spawn gap, both runs" has no preserved substrate**
  (journals carry no clock lines; snapshot mtimes flattened; live-poll output not
  saved). Two identical 22s figures is a rounding tell. Downgraded
  VERIFIED→SUSPECT. The *ordering* (decomposition before spawn) still holds via
  swarm `ts` + file structure; the magnitude does not.

**Verdict:** **NOT-FIRED, provenance UNPROVEN.** The observed behavior is
consistent with the doctrine working and with ordinary repo-reading. dp-red's
cold-control experiment (same repo, same phase-2 prompt, no phase 1) is cheap and
decisive; dp-f2's compaction variant tests the paragraph's hard clause. Both are
designed, neither run.

## 4. What survives for the probe kit (uncontested)

1. **The mtime trap** — post-hoc journal-mtime comparison yields a false FIRED
   (append drift; run 1 read −566 s). Honest collectors: swarm's immutable `ts`,
   live polling (preserve the poll output — R7's lesson), file structure.
2. **The trust-folder gate** — fresh panes stall on Claude Code's workspace-trust
   prompt; the first baseline window closed with both observers never started
   (caught by pane read; zero contamination — the skill was never read by anyone
   in that window). Launchers must pass the gate before the window opens.
3. **The herdr stale-render artifact** — phantom composer text in one pane read;
   probe the input box, never trust a single pane read of it.

## 5. Adversarial review (the record)

`dp-red` (fresh; checked clone records, `bin/swarm` source, both skill texts, and
launchers — never a runner's findings file): **9 objections — 5 flips-verdict
(R1–R5), 3 softens (R6–R8), 1 miscite (R9, partially dissolved by dp-f1's journal
which does carry the pre-registration).** Both pre-review headline verdicts fell:
"doctrine-ineffective" (rested on a baseline arm that contained the treatment) and
"F2 earned pass" (rested on a collector with no discriminating power). What
survived, per the reviewer: the trigger gap ("your best finding and you undersell
it"), the mtime trap, and the root-name finding — which R3 made *stronger* by
grounding it in code. The reviewer's proposed settling experiments (cold-control
F2; true pre-doctrine baseline with a fully-containing window; un-decomposed
un-coached F1 rerun) are adopted as the follow-up menu, operator's choice.

Method note for the record: the pre-review draft of this file repeated, at
smaller scale, the failure v3-red found in the FLEET synthesis the same day —
kindness toward the author's own design (an uninformative baseline read as
confirmation; a non-discriminating collector read as an earned pass). Two
independent red reviews catching the same author-bias direction in one day is
itself a datum in favor of the mandatory-fresh-reviewer convention.

## 6. Accounting

All sessions on the Claude pool (unpriced): 4 F1 + 2 F2 + 2 baseline observers,
~17 short-lived sessions total including children, 2 runner agents + 1 reviewer;
wall ≈ 100 min end to end; no API dollars. Machine-contention overlap with the
FLEET v3 GLM cell window noted; no timing-scored checks here.
