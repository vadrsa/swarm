# mandate-audit — adversarial review of 9d6d62b (+ self-fix 8706d0c)

> SUPERSEDED as a live gate by the merged `--model`/`--reason` PR (9d6d62b); kept for the record (the audit trail — clean bill on merge-breakage, reason-theater re-grading, the one open reason-phrasing disagreement).

Fresh-eyes audit of `feat(spawn): --model and --reason are required`, against
`docs/design/MODEL-FIT.md` §5/§6 and `docs/design/HARNESS.md` §2.4 + falsifier #4.
Author (spawn-mandate) fixed three of my four targets before I reported — see
"folded" section. This doc covers what survives after that fold.

## (a) Merge-breaker census — CLEAN BILL

No call site breaks on merge. Verified two ways: my own reading of `cmd_spawn`'s
guard ordering (bin/swarm:1214, the mandate check sits after bad-name/unknown-flag/
empty-task/not-in-herdr, per the file's own comment explaining why), and an
independent sonnet child that greped both literal `"swarm spawn"` and argv-element
`"spawn"` forms, read `tests/test_swarm.py` in full, checked `install.sh` and
`skill/SKILL.md`, and ran both test files.

The three `test_swarm.py` calls missing `--model`/`--reason` (lines 932, 946, 954)
are **not latent-green**: each hits an earlier refusal (bad name / unknown flag)
that fires before the new mandate check, so they still test what they always
tested. Confirmed by running them.

`test_swarm.py` 93 passed, `test_swarm_process.py` 43 passed (136 total per your
last message — consistent). No hook, Makefile, CI config, or dynamically-built
verb string exists in this repo (none found; N/A rather than missed).

**Residual gap, disclosed not found:** child did not search for a verb held in a
variable then dispatched (e.g. `getattr`/dict-based command tables) outside
`bin/swarm`'s own `main()`. It checked `main()`'s own dispatch and found no other
table. I did not independently re-run that specific search myself — floor, not a
total, on that one axis only. Everything else here I did verify directly.

**On the untouched/uncommitted files (bench v1/v2/v3, `.swarm/briefs/review_tests.py`):**
Right call to exclude v1/v2 (frozen scored inputs — changing them retroactively
edits history) and the gitignored file (not part of the repo's tracked surface).
`bench/fleet-briefs-v3/` being live and edited-but-uncommitted is a real risk, but
it's a **pre-existing risk independent of this PR** — v3 lives outside git tracking
entirely (per `.gitignore`), so no version of this PR, merged or not, changes
whether `run-cell.sh` sees old or new content. Not this PR's blast radius.

## (b) Reason-theater grading — DISAGREE WITH MY OWN CHILD, ONE ITEM WORTH YOUR LOOK

I ran a second sonnet child to grade every `--reason` fixture against the delete-"I"
tell. It marked **all 16 as THEATER**, but on inspection its method was broken: it
flagged third-person phrasing itself as failure, then proposed fixes that just
prepend "I will" to the *same substantive content* — which by the tell's own logic
would then pass. That's grading grammar, not verification-capacity. I overrule it.

Re-graded by hand against the actual rule ("does this name a concrete check the
parent will do, not a claim about the model or task"):

- `"this test asserts the exact record fields, journal text and argv... every
  claim it makes is checked mechanically here"` (line ~200) — **PASS**. Names the
  exact check (assertions on record/journal/argv) and why it's cheap.
- `"the child's output here is a file whose contents this test greps; a wrong
  answer is caught by the assertion, so it costs nothing"` (GOOD fixture, ~326) —
  **PASS**. Concrete grep-based check named.
- The refusal-path fixtures ("the refusal is one string in stderr, checked right
  here", lines 251/278/304/311/337) — **PASS**, and your own comment at ~322
  already flagged why these need to be real ("nobody reads this one" is exactly
  where theater starts) — good instinct, borne out.
- The two attack-payload reasons (newline-forge, ANSI/glyph-forge, lines 483/498)
  are sanitizer-test fixtures, not reasons anyone would write in practice — grading
  them as theater/not-theater is a category error either way. Skip.
- `"   "` (blank) and `"x"*(CAP+1)` — deliberately invalid inputs for rejection
  tests, not reasons. Skip.

**Net: 0 real theater found in the surviving fixtures.** They're plainly written
in third person ("this test", "the refusal") rather than first person ("I will
grep..."), which is a style tic, not a substance failure — every one still answers
the verification-capacity question concretely. If you want first-person phrasing
for consistency with the runtime error text's own voice ("you re-read the diff"),
that's a polish pass, not a defect.

## (c) Error text — teaches, doesn't scold. No finding.

Ran both paths live:
- No flags → `spawn_mandate_error()`: teaches the question, the tell, and cheap-
  vs-expensive framing in 7 lines. Readable in one screen.
- `--model haiku` → `spawn_model_error()`: byte-for-byte matches HARNESS.md:210-212
  (verified with sed). Correctly frames the ban as unmeasured policy, names the
  unrun settling probe, does not claim "solved." Honest.

Minor/cosmetic only: HARNESS.md has no literal heading numbered "§9.4" — the
falsifier is item **#4** in a flat numbered list under `## 9. FALSIFIERS`. The
cited content is accurate and findable either way; not worth a code change, just
noting the citation is one level looser than it reads.

You already caught and fixed the "haiku (see below)" dangling reference — confirmed
gone from the current `spawn_mandate_error()` (no haiku mention at all in the no-
flags path now, which is correct: the ban only surfaces when someone actually
types `--model haiku`).

## (d) ps --reason forgery — could not break it (after 8706d0c)

Attempted: newline-injected reason to forge a second row → collapsed to spaces,
no forged row (confirmed live). ANSI + box-glyphs + fake `(you)` payload → after
your fix in 8706d0c (pin's MODEL_STRUCTURAL exclude-list applied to reasons too),
confirmed live that none of `├─│└()` or `\x1b` survive into the rendered block.
Before that fix this was a real hole (you found it first); after it, I could not
reproduce it. Cap at REASON_CAP=500 holds.

## Bottom line

Nothing survives beyond what you already found and fixed. Both attack surfaces I
was asked to hit hardest — merge-breakage and ps-forgery — are clean. The one
disagreement is (b): I think your self-graded reasons pass on substance and my own
child's all-THEATER verdict was a bad read of the tell (style vs. substance). Your
call whether third-person phrasing is worth a polish pass regardless.
