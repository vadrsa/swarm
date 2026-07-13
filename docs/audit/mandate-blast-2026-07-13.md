# mandate-blast census — every `swarm spawn` caller, ahead of the `--model`/`--reason` mandate

Agent: mandate-blast (parent: spawn-mandate). Branch: `swarm-dev/spawn-mandate` (off cfb3113).
Read-only census — no edits, no commits made by me or my children.

Work was split across three children, each covering a non-overlapping slice, plus a
historical sweep I did myself:

- **mb-tests** — every Python file (tests/*.py, .swarm/briefs/*.py) that invokes `swarm spawn`.
- **mb-shell** — every shell script in the repo (install.sh, bootstrap.sh, ~208 `.launch.sh`
  files, bench harness scripts, git hooks, Makefile).
- **mb-normative** — every file that *teaches* the spawn form (WORLD.md, skill/SKILL.md,
  README, docs/design/*, docs/PHILOSOPHY.md, bin/swarm's USAGE/spawn_header strings — read only).
- **mandate-blast (me)** — `docs/audit/*` historical sweep, and cross-checked the
  fleet-briefs live/historical judgment call independently of mb-shell/mb-normative.

All three children's raw reports are preserved on disk (not deleted): mb-tests' at
`/private/tmp/claude-501/.../scratchpad/mb-tests-census.md` (ephemeral scratchpad — copy the
table below if you need it later), mb-shell's at `docs/audit/mb-shell-census-2026-07-13.md`,
mb-normative's at `.swarm/research/mb-normative-findings.md`.

## The real counts

| Class | Count | Notes |
|---|---|---|
| **EXECUTABLE** call-sites (Python `swarm spawn` invocations that run) | **13** | 4 positive, 9 negative (see table below) |
| **EXECUTABLE** call-sites in shell scripts | **0** | Zero `.sh` files literally call `swarm spawn`. See "shell scripts" note below — two scripts feed a *live model* that may call spawn at runtime, sandboxed. |
| **NORMATIVE** files/locations needing a fix | **6** | bin/swarm×2 (not mine to edit, flagged), WORLD.md×1, fleet-briefs-v{1,2,3} preambles+cli-doc ×3 pairs (ambiguous, scoping call needed) |
| **HISTORICAL** files (docs/audit/*, untouched, do not edit) | **45** | grep -rl "swarm spawn" docs/audit/, excluding this census's own new output files |

The brief said "~9 tests and 12 docs, a floor." Actual: **13 executable Python call-sites**
(more than the floor — grouped across 3 files, 2 of which are near-duplicates), **0 executable
shell call-sites**, **6 normative fix locations**, **45 historical files** (well past the
"12 docs" floor once docs/audit is counted exhaustively — but per the task's own rule, those
45 are explicitly NOT to be touched).

## 1. EXECUTABLE — Python test/helper files (13 call-sites, 3 files)

Coverage method (mb-tests): `find . -name "*.py"` → 6 Python files repo-wide; only 3 contain
"spawn" anywhere (`tests/test_swarm.py`, `tests/test_swarm_process.py`,
`.swarm/briefs/review_tests.py`). Confirmed no indirect wrapper (`grep -n "def spawn_agent\|def do_spawn\|def _spawn\|def spawn("` → zero matches across all three) — the only helper,
`run_swarm(args, ...)`, is a generic argv-list subprocess runner, not spawn-specific.

| File | Line | Call | Pos/Neg | Needs both flags? | Latent-green risk |
|---|---|---|---|---|---|
| tests/test_swarm.py | 932 | `subprocess.run([SWARM, "spawn", "abc\n", "task"], ...)` | NEGATIVE (asserts `returncode==1`, `"bad name" in stderr`) | N/A — ordering-dependent | **Ordering-dependent, not silent**: if flag-check runs before name-check, fails loudly (stderr won't contain "bad name"); if after, still passes correctly. Must reverify against real validation order. |
| tests/test_swarm.py | 946 | `subprocess.run([SWARM, "spawn", "abc\n", "task", "--trust"], ...)` | NEGATIVE (`returncode==1`, `"bad name"` in stderr, `"unknown flag" not in stderr`) | N/A | Same ordering dependency as 932. Also: if the new missing-flag error text happens to contain "unknown flag", the `not in` assertion could spuriously break even when ordering is fine — wording-dependent, flag to whoever picks the error string. |
| tests/test_swarm.py | 954 | `subprocess.run([SWARM, "spawn", "ok-name", "task", "--bogus"], ...)` | NEGATIVE (`returncode==1`, `"unknown flag" in stderr`) | N/A | **Clearest ordering risk of the three** — `ok-name` is valid, so nothing else fires first; if missing-required-flag detection fires before unknown-flag detection, `"unknown flag"` never appears in stderr → loud failure, not silent, but currently untested against real order. |
| tests/test_swarm_process.py | 199 | `run_swarm(["spawn", "worker", "do the thing"], env, cwd=self.root)` | **POSITIVE** (asserts `returncode==0`, full happy-path side effects) | **YES — must add both flags** | None (will break loudly, this is the expected/required fix) |
| tests/test_swarm_process.py | 235 | `run_swarm(["spawn", "worker", "t"], env, cwd=self.root)` | **POSITIVE** | **YES** | Blocking dependency: lines 237/253/268 in the same test method rely on this spawn succeeding first. |
| tests/test_swarm_process.py | 237 | `run_swarm(["spawn", "worker", "t2"], env, cwd=self.root)` (collision) | NEGATIVE (`"already used"` in stderr) | N/A | Depends on 235 succeeding first (upstream break, not a false-pass at 237 itself). |
| tests/test_swarm_process.py | 243 | `run_swarm(["spawn", "worker", "t"], env, cwd=self.root)` (no claude on PATH) | NEGATIVE (`"did not start"`, `"claude not found"` in stderr) | N/A | Ordering-dependent — flag-check likely fires before the "is claude on PATH" check, so stderr assertions would fail loudly; the specific teardown behavior this test claims to check would stop being exercised. |
| tests/test_swarm_process.py | 253 | `run_swarm(["spawn", "worker", "t2"], env, cwd=self.root)` (burned name) | NEGATIVE (`"already used"`) | N/A | Same upstream dependency as 237. |
| tests/test_swarm_process.py | 258 | `run_swarm(["spawn", "worker", "t"], env, cwd=self.root)` (HERDR_ENV=0) | NEGATIVE (`"not inside herdr"`) | N/A | Ordering-dependent, same shape as 243. |
| **tests/test_swarm_process.py** | **268** | `run_swarm(["spawn", bad, "t"], env, cwd=self.root)` in a loop over bad names | NEGATIVE (`returncode==1` **only** — no stderr check) | N/A | **SILENT LATENT-GREEN-RISK.** Will keep returning 1 (now for missing-flag, not bad-name) forever — no assertion would ever catch this test testing the wrong thing. |
| .swarm/briefs/review_tests.py | 182 | `run_swarm(["spawn", "worker", "do the thing"], ...)` | POSITIVE (dup of 199) | YES | — |
| .swarm/briefs/review_tests.py | 213 | `run_swarm(["spawn", "worker", "t"], ...)` | POSITIVE (dup of 235) | YES | — |
| .swarm/briefs/review_tests.py | 215, 221, 230, 235 | dup of 237/243/253/258 | NEGATIVE | N/A | Same ordering-dependent risks as their originals. |
| **.swarm/briefs/review_tests.py** | **245** | dup of 268 (bad-names loop) | NEGATIVE (`returncode==1` only) | N/A | **SILENT LATENT-GREEN-RISK, duplicate of the one above.** Note: unclear if this file is collected by pytest/CI at all (looks like a parked reviewer artifact with a stale hardcoded `SWARM` path) — still in scope since it exists on disk with real assertions, but worth confirming with whoever owns test discovery before spending fix effort here. |

**The two latent-green tests, called out explicitly (this is the worst-outcome finding of the whole census):**
`tests/test_swarm_process.py:268` (`test_spawn_bad_names_refused`) and its duplicate
`.swarm/briefs/review_tests.py:245` assert **only** `returncode==1`, with no stderr content
check. Once `--model`/`--reason` become required, every call in this loop — already missing
both flags — will still return 1, but for "missing required flag," not "bad name." The test
will stay green forever while silently testing nothing about name validation.

## 2. EXECUTABLE — shell scripts (0 literal call-sites)

Coverage method (mb-shell): checked install.sh, bootstrap.sh, Makefile (doesn't exist), git
hooks (`.git/hooks` has only `.sample` templates, nothing live), all 208
`.swarm/settings/*.launch.sh` (verified identical herdr-pane-launcher template via full grep +
9-file spot check — none shell out to `swarm` at all), and the bench harness scripts.

**Zero shell scripts literally execute `swarm spawn`.** The one nuance: `docs/audit/bench/run-cell.sh`
and `run-cell-v3.sh` are live, runnable harnesses (not historical — parameterized, current
usage docs, actively referenced brief dirs) that feed briefs to a model under test via
`opencode run`, inside a sandboxed `SWARM_DIR`. **The model being benchmarked**, not the
script itself, may call `swarm spawn` at runtime — this is out of scope for "callers that
break the repo" since it's sandboxed and not this repo's CI, but worth knowing it exists.
`run-cell-v3.sh:182` does contain one literal executable `swarm send` call (not spawn,
unaffected by this mandate).

## 3. NORMATIVE — files that teach the bare form (6 locations)

| Location | Status | Owner |
|---|---|---|
| **bin/swarm:1015** (`spawn_header()`) | **Bare form, live-injected into every spawned agent's first message.** Highest-consequence hit in the whole census — not documentation someone might read, mechanically re-delivered on every single spawn. | Not mine to edit — spawn-mandate owns bin/swarm. |
| **bin/swarm:1441** (USAGE heredoc) | Shows `[--model M]` as **optional** and **omits `--reason` entirely** — self-contradicts `cmd_spawn`'s own die message at bin/swarm:1159, which already correctly requires both. A human running `--help` would copy the wrong form. | Not mine to edit — flagging alongside spawn_header. |
| **WORLD.md:14** | Bare form (`swarm spawn <name> "<task>"`), no flags. This is "the contract every agent is told to read before coordinating others" — printed verbatim by `swarm world`. | Needs fixing — mine/coordinator's file. |
| **skill/SKILL.md** | No literal form shown (tells agents to run `swarm world` for the contract) — no direct fix needed, but inherits WORLD.md's bare form transitively. | No action needed directly. |
| **README.md**, **docs/PHILOSOPHY.md** | Checked clean — neither shows the literal invocation syntax. | No action needed. |
| **docs/audit/bench/fleet-briefs-v{1,2,3}/00-duties-preamble.md** (line 5, 33) and **d3b-swarm-cli.md** (line 6) — all 3 versions | **Ambiguous — flagging for a scoping decision, not silently classified.** These live under `docs/audit/` but are confirmed **live-rendered** by `run-cell.sh`/`run-cell-v3.sh` into benchmark-agent briefings — not frozen records. Bare form in all three versions. Open question: are throwaway benchmark-harness agents in scope for this migration at all? If yes, all three versions need the same fix as WORLD.md. | **Needs your scoping call.** |

`docs/design/*` was swept in full (14 files hit on `"swarm spawn"`, including a
non-recursive-glob miss caught and fixed on a follow-up pass that found
`docs/design/archive/` too). All resolved to one of: already-correct (`docs/design/HARNESS.md`
already argues for `--model`/`--reason` and shows it correctly — no fix needed, arguably the
canonical example to copy), dated/retracted proposal (`OPERATOR-STRUCTURE-FIX.md` etc.), or
historical eval transcript quoting what an agent actually typed (`FLEET-EVAL*.md`). None need
action. Full per-file reasoning in `.swarm/research/mb-normative-findings.md`.

## 4. HISTORICAL — docs/audit/* (45 files, DO NOT TOUCH)

`grep -rl "swarm spawn" docs/audit/` (excluding this census's own newly-written output files)
→ **45 files**. These are past records — audit reports, bench result tables, forensic write-ups
— that quote what an agent actually typed or designed at some past moment. Rewriting them to
the new syntax would falsify the record. **Do not edit these; I have not.**

The one exception category already carved out and moved to NORMATIVE above:
`fleet-briefs-v{1,2,3}/*` (live-rendered templates, not frozen records). Everything else under
`docs/audit/bench/` (`results-*.md`, `SCORING-AUDIT-V3.md`, `fleet-rubric-v1.md`,
`factcheck-mcp-control.md`) is genuinely historical — read by a human, never re-executed.
`fleet-briefs-v1/` specifically is superseded (neither current run-cell script's `BRIEFS=` var
points to it) but structurally identical to v2/v3 and not deleted — treated as historical
relative to current runs.

## What surprised me

1. **The bin/swarm self-contradiction** (mb-normative's find): the USAGE `--help` string and
   the actual `cmd_spawn` die message already disagree with each other *today*, independent of
   this census — USAGE shows `--model` as optional and never mentions `--reason`, while
   `cmd_spawn` already dies demanding both. Someone reading `--help` right now gets misled.
2. **The two silent latent-green tests are exact duplicates** — `test_swarm_process.py:268`
   and `.swarm/briefs/review_tests.py:245` are the same test, copy-pasted into a second file,
   both with the identical blind spot (returncode-only assertion, no stderr check). Fixing one
   without the other leaves a false sense of coverage.
3. **Zero shell scripts call spawn directly** — the entire executable surface is 3 Python
   files. But the bench harness (`run-cell.sh`/`run-cell-v3.sh`) sandboxes a *live model* that
   itself calls `swarm spawn` at runtime — a caller that's neither "this repo's code" nor
   "documentation," a third shape neither of the three buckets quite named. It doesn't break
   the repo (it's sandboxed, and failures there are recorded as benchmark data, `[H]` results),
   but the fleet-briefs *text* that model reads is squarely NORMATIVE and does need the flag
   mandate reflected in it if benchmark runs should keep testing realistic spawn behavior.
4. **The floor estimate ("~9 tests") underspecified reality**: the true count is 13 Python
   call-sites, not ~9 — the review_tests.py duplicate file alone adds 6 more that a literal
   `grep -rn "swarm spawn"` (the trap this task warned about) would have missed entirely,
   exactly as briefed.
