# Blast radius: making `--model` (and/or `--reason`) a REQUIRED flag on `swarm spawn`

**Agent:** mr-blast · **Parent:** mandate-red · **Date:** 2026-07-13
**Question:** every place that invokes or documents `swarm spawn`; what breaks if the flag becomes required.
**Method:** `grep -rn 'swarm spawn' . --exclude-dir=.git` (**119** pre-existing hits, excluding this
report itself), **plus** two corrections the naive grep requires:

1. **It misses every executable caller.** No test types the string `swarm spawn`; they pass `"spawn"`
   as an argv element (`run_swarm(["spawn", …])`, `subprocess.run([SWARM, "spawn", …])`). A widened
   grep for those forms is what produces count(A). **The literal grep finds 1 hit in `tests/` — a
   comment. The real number of executable callers there is 9.**
2. **It never descends into `.swarm/`** (verified: `grep -rn … .` yields zero `./.swarm/` matches).
   Journals and runtime state must be counted by explicit path. Journals: **71**.

Counts below **exclude this file**, which itself contains 23 occurrences of the string.
**Falsification:** claims below are not read off the source — I patched a scratch copy of `bin/swarm`
with a required-`--model` guard and **ran the real suite**. Failures are observed, not predicted.

---

## The headline

| | |
|---|---|
| **count(A) EXECUTABLE CALLERS** | **9** (all in `tests/`) |
| **count(B) NORMATIVE DOC/EXAMPLE** | **12** (3 inside `bin/swarm` itself) |
| **count(C) HISTORICAL PROSE / RUNTIME STATE** | **342** (71 journal + 234 `.swarm/` state + 108 docs + 1 comment) |
| **Does `tests/` exist?** | **YES** — `tests/test_swarm.py`, `tests/test_swarm_process.py` |
| **Would any test fail?** | **YES — 5 tests fail, +1 silently rots.** Measured, not inferred. |
| **Machine-generated spawning anywhere?** | **NO** — outside `tests/`, `swarm spawn` has zero programmatic callers. |

---

## Measured test result (the load-bearing evidence)

Baseline, unmodified repo: **80 passed**.

I copied `bin/` + `tests/` to a scratch tree and inserted a required-model guard into `cmd_spawn`,
immediately after flag parsing (`bin/swarm:857`, before the name regex):

```python
if not model:
    die('spawn requires --model M (no default; name the model you chose)')
```

Patched result: **6 failed, 74 passed.**

One of those six — `test_swarm.py::TestWorldResolution::test_world_via_symlink_from_foreign_cwd` —
**also fails in an unpatched scratch copy** (control run: `1 failed, 79 passed`). It is a
copied-tree symlink artifact, **not** blast radius. **Attributable failures: 5.**

| # | Test | file:line | Dies because |
|---|---|---|---|
| 1 | `test_spawn_happy_path_with_fake_herdr` | `test_swarm_process.py:199` | `run_swarm(["spawn","worker","do the thing"])` → exit 1, not 0. `AssertionError: 1 != 0` |
| 2 | `test_spawn_name_collision_errors` | `test_swarm_process.py:235,237` | first spawn no longer returns 0; collision path never reached. `AssertionError: 1 != 0` |
| 3 | `test_spawn_confirmed_failure_tears_down_but_keeps_tombstone` | `test_swarm_process.py:243` | expects `"did not start"` in stderr; **gets the model-guard message instead** |
| 4 | `test_spawn_outside_herdr_refused_before_tombstone` | `test_swarm_process.py:258` | expects `"not inside herdr"`; **gets the model-guard message instead** |
| 5 | `test_spawn_refuses_trailing_newline_name_before_tombstone` | `test_swarm.py:536` | expects `"bad name"` in stderr; **gets the model-guard message instead** |

### The latent one — a test that stays GREEN while ceasing to test anything

`test_spawn_bad_names_refused` (`test_swarm_process.py:264-268`) asserts **only**
`returncode == 1`. Under the patch it still passes — for the **wrong reason**. Verified directly:

```
$ swarm spawn Worker t          # invalid name, HERDR_ENV=1
swarm: spawn requires --model M (no default; name the model you chose)
```

The name `Worker` is never validated. The test is now a tautology: every input exits 1, so it can
no longer detect a regression in name validation (`Worker`, `has space`, `-lead`, `x*41`,
`operator`, `delivered` — all six cases). **This is a silent hole, not a visible failure.**

### Guard-placement is itself a decision

Failures 3, 4, 5 all have the same shape: **a required-flag guard placed early hijacks the error
message of every other refusal path.** `cmd_spawn` currently refuses in a deliberate order
(`bin/swarm:857-866`): bad name → reserved name → empty task → not-inside-herdr. That order is
load-bearing — the herdr check and the name check must fire **before the tombstone is claimed**
(`bin/swarm:872`), which is precisely what tests 4 and 5 assert. Placing the model guard **after**
the herdr check (rather than before the name regex) would save failures 3/4/5 and reduce the
attributable count to **2**. Placement is a real lever, and this audit does not pick one.

---

## (A) EXECUTABLE CALLERS — 9

Every one runs `swarm spawn` as a real subprocess with **no `--model`**. A required flag makes each
exit 1. **All 9 are in `tests/`. There are none anywhere else in the repo.**

| # | file:line | Exact text | What breaks |
|---|---|---|---|
| A1 | `tests/test_swarm_process.py:199` | `p = run_swarm(["spawn", "worker", "do the thing"], env, cwd=self.root)` | happy path; expects exit 0 → gets 1 |
| A2 | `tests/test_swarm_process.py:235` | `self.assertEqual(run_swarm(["spawn", "worker", "t"], env,` | collision setup; expects exit 0 → gets 1 |
| A3 | `tests/test_swarm_process.py:237` | `p = run_swarm(["spawn", "worker", "t2"], env, cwd=self.root)` | collision probe; never reaches "already used" |
| A4 | `tests/test_swarm_process.py:243` | `p = run_swarm(["spawn", "worker", "t"], env, cwd=self.root)` | teardown test; stderr assertion breaks |
| A5 | `tests/test_swarm_process.py:253` | `p2 = run_swarm(["spawn", "worker", "t2"], env, cwd=self.root)` | name-burned-forever probe; unreachable |
| A6 | `tests/test_swarm_process.py:258` | `p = run_swarm(["spawn", "worker", "t"], env, cwd=self.root)` | outside-herdr refusal; wrong stderr |
| A7 | `tests/test_swarm_process.py:268` | `p = run_swarm(["spawn", bad, "t"], env, cwd=self.root)` | **latent** — stays green, stops testing names |
| A8 | `tests/test_swarm.py:536` | `p = subprocess.run([SWARM, "spawn", "abc\n", "task"], env=env,` | trailing-newline refusal; wrong stderr |
| A9 | `bin/swarm:1128-1129` | `if verb == "spawn":` / `cmd_spawn(rest)` | the dispatcher itself — the site of the change, not a victim |

**Not executable callers** (checked and cleared):
- `docs/audit/bench/run-cell.sh:15,78,79,202` — the strings appear only in **comments and a warning
  `echo`**. The script never invokes spawn; it warns that *the model under test* may try to.
- `docs/audit/bench/factcheck-mcp-control.md:25` references a launcher `claude-base/bin/native-cell.sh`
  that "calls `swarm spawn`" — **that file does not exist in this repo** (`find . -name native-cell.sh`
  → nothing). It is described, not present.
- `install.sh`, `bootstrap.sh` — **zero** `spawn` invocations (`grep -n 'spawn'` returns nothing).
- `skill-middleware/`, `.swarm/` hooks — no spawn invocations. Hooks wired at
  `bin/swarm:886-895` are `deliver`/`event`/`restore`; none spawn.

### Answer: is there ANY machine-generated spawning?

**No.** Outside the test suite, every `swarm spawn` in this repo is a **human or an agent typing it
at a shell**. `bin/swarm` shells out only to `herdr` (`bin/swarm:601, 618, 634, 649, 671, 676, 916,
947, 1079, 1083`) and to a middleware command (`:1024`) — **never to itself**. There is no script,
hook, cron, plugin, or generator that composes a spawn command. The `.swarm/settings/*.launch.sh`
files are *products* of a spawn, not callers of one.

Consequence: apart from `tests/`, a required flag breaks **no automation**. It breaks **habits and
documents** — which is the whole (B) and (C) surface below.

---

## (B) NORMATIVE DOC / EXAMPLE — 12

Text an agent **reads and copies verbatim**. A required flag makes these wrong or stale. The first
three are the highest-leverage: they are injected into or read by *every* agent.

| # | file:line | Exact text | What breaks |
|---|---|---|---|
| B1 | `bin/swarm:777` | `` f"You have the `swarm` CLI: `swarm spawn <name> \"<task>\"` to delegate, "`` | **`spawn_header` — the task text of EVERY spawned agent.** Teaches the no-flag form as the canonical one. Highest leverage in the repo: every child in every swarm reads this. |
| B2 | `bin/swarm:847` | `die('spawn needs: swarm spawn <name> "<task>" [--model M] [--cwd DIR]')` | the arity error itself shows `--model` as **optional** (`[…]`); must move into the required slot |
| B3 | `bin/swarm:1105` | `` swarm spawn <name> "<task>" [--model M] [--cwd DIR]   create a child; the name`` | **USAGE / `swarm world`** — the contract every agent is told to read. `[--model M]` brackets = optional. (`:1107-1110` already carry the "a CHOICE, not a default" prose — the *doctrine* exists; only the *grammar* says optional.) |
| B4 | `WORLD.md:14` | ``3. **`swarm spawn <name> "<task>"`** — create a child. The name is chosen, not`` | **the contract every agent reads.** Names the verb with no flag. |
| B5 | `skill/SKILL.md:59` | ``default. Say the choice in your journal at the spawn (`spawned <name> on`` | skill doctrine already asks the agent to *state* the model choice — but as journal prose, not a flag. Would need to become "the flag you passed". **NB: does not contain the literal string `swarm spawn`** — `skill/` has **zero** literal hits. Found via the widened grep for `spawn`. A doc-sweep driven by the naive grep **would miss `skill/` entirely.** |
| B6 | `skill/SKILL.md:143` | ``Run **`swarm world`** — it prints the whole contract: four verbs (`spawn` a`` | points agents at B3; stale if B3's grammar changes. Same caveat as B5 — no literal hit. |
| B7 | `docs/design/MODEL-FIT.md:6` | ``**The gap this closes.** `swarm spawn <name> "<task>" --model M` has existed since`` | the live design doc for this very change |
| B8 | `docs/design/MODEL-FIT.md:236` | ``- **`swarm spawn` help / `swarm world`** — the flag stops being a bare token in a usage`` | already names B3 as a surface to update — an explicit self-reference |
| B9 | `docs/design/FLEET.md:218` | ``Add a spawn flag — e.g. `swarm spawn <name> "<task>" --exec opencode` (or a`` | proposes a *further* optional flag on the same grammar; collides |
| B10 | `docs/design/DECISION-WIRING.md:147` | ``` `swarm spawn decision-engine "<brief>"` executed from the seat environment ``` | a **prescribed ritual command** an operator/seat is told to run. Would fail as written. |
| B11 | `docs/design/DECISION-WIRING.md:590` | `` \| 4 \| `swarm spawn decision-engine "<brief path>"` \| 1 command \| none — existing verb \|`` | wiring table step; the "1 command" cost estimate is now wrong |
| B12 | `docs/design/PIPELINE-WIRING.md:648` | `` \| 3 \| **[seat]** \| `swarm spawn decision-engine` (DW §9 #4); seat-take entry …`` | same ritual, second wiring doc |

Borderline, judged **not** normative (they describe rather than instruct): `docs/PHILOSOPHY.md:127`,
`docs/design/PROXY-WIRING.md:613`, `docs/design/DECISION-WIRING.md:23,661`,
`docs/design/OPERATOR-STRUCTURE.md:119`, `docs/design/archive/*`. The archive dir in particular is
explicitly historical. If mandate-red wants a **maximal** B, the four `docs/design/*WIRING*` ritual
lines plus the three archive lines would push B to **19**; the 12 above is the defensible core —
text that *tells an agent what to type*.

The benchmark briefs are a **special case worth flagging**:
`docs/audit/bench/fleet-briefs-{v1,v2,v3}/00-duties-preamble.md:5` each read
`` - `swarm spawn <name> "<task>"` — create a child agent to do a piece of work.`` and
`…/d3b-swarm-cli.md:6` reads `` Use `swarm spawn` to do this.`` These are **inputs to a scoring
rig** — a model graded on "well-formed spawn" (`fleet-rubric-v1.md:190`) against a *stale* brief
would now be marked correct for typing a command that fails. I count them as (C) because the rig is
historical, but **if the fleet eval is ever re-run they become (A)-adjacent: the rubric would score
the wrong thing.** Six files, six lines.

---

## (C) HISTORICAL PROSE / RUNTIME STATE — 342

No breakage. Counted for completeness; these describe or record past runs. All figures verified by
explicit-path grep, excluding this report.

| Source | Count | Note |
|---|---|---|
| `.swarm/journal/*.md` (excluded from breaks per brief) | **71** | how agents *actually type it* — see below |
| `.swarm/settings/*.task` | 162 | **emitted** `spawn_header` text — one per spawned agent. Not callers; *products* of `bin/swarm:777`. |
| `.swarm/` other (agents, queue, briefs, research, event) | 72 | delivered messages, agent records, brief prose |
| `docs/audit/**` (forensics, bench results, red-team traces) | 80 | includes the 6 fleet-brief lines flagged above |
| `docs/design/**` minus the 6 normative (B7–B12) | 27 | includes `archive/` |
| `docs/PHILOSOPHY.md` | 1 | descriptive |
| `tests/test_swarm.py:533` | 1 | a *comment*; the executable call beside it is A8 |
| **Total (C)** | **342** | |

**The 162 `.swarm/settings/*.task` hits are the loudest fact in this table.** Each is a frozen copy of
the `spawn_header` (B1, `bin/swarm:777`) — the no-flag form, stamped into the task text of every agent
this repo has ever spawned. They are inert history, but they measure B1's reach: **every agent that has
ever run was taught the bare form.**

**What the 71 journal lines show — the brief asked for this explicitly.** They are how agents
*actually type the command in the field*. Sampling them: the overwhelmingly dominant form is the
**bare** `swarm spawn <name> "<task>"` with **no `--model`**. The field-evidence docs record this as
a finding in its own right — `docs/design/FLEET-EVAL.md:63` and `FLEET-EVAL-RED.md:65`: *"GLM ran
bare `swarm spawn stability`"*, treated there as a **defect** (children inherited the wrong cwd/model).
`docs/audit/red2-trace-2026-07-12.md:68,103,249-251` and `structure-mechanics-2026-07-12.md:61` are
all bare-form.

**This is the strongest empirical argument in the audit, and it cuts both ways:**
- *For* requiring the flag: the bare form is what agents reach for by default, and the existing
  doctrine (`bin/swarm:1107-1110`, `SKILL.md:59`) — which *already* says "a CHOICE, not a default" —
  is demonstrably **not being obeyed**. Prose has not moved behavior.
- *Against*: 71 journal lines and ~12 doc examples of muscle memory means the flag-day cost is a
  documentation sweep, and every stale example is a trap an agent will copy.

I take no position; that is mandate-red's call. This is the ground truth.

---

## Ground-truth summary

```
count(A) EXECUTABLE CALLERS   =    9   (9/9 in tests/; ZERO elsewhere in the repo)
count(B) NORMATIVE DOC/EXAMPLE=   12   (3 of them inside bin/swarm itself)
count(C) HISTORICAL PROSE     =  342   (71 journal + 234 .swarm/ state + 108 docs + 1 comment)
```

**Two grep caveats any follow-up sweep must inherit** (both cost me a wrong number before I caught them):
- `grep -rn 'swarm spawn' .` **does not descend into `.swarm/`** — journals and the 162 emitted
  `.task` headers are invisible to it. Count them by explicit path.
- `skill/` contains **zero** literal `swarm spawn` hits, yet holds two normative surfaces (B5, B6).
  **A doc-sweep driven by the literal grep alone would silently skip the skill.**

- **`tests/` exists.** Two files, 80 passing tests today.
- **Tests would fail: YES — 5 attributable failures, measured.** Plus **1 latent rot**
  (`test_spawn_bad_names_refused` passes for the wrong reason and stops guarding name validation).
- **Machine-generated spawning: NONE.** `bin/swarm` never invokes itself; no script, hook, or plugin
  composes a spawn command. Every real-world spawn is typed by a human or an agent.
- **The three surfaces inside `bin/swarm` (`:777` spawn_header, `:847` arity die, `:1105` USAGE)
  must change together** — `:777` is injected into every child's task text and is the single
  highest-leverage line in the blast radius.
- **Guard placement is a live decision:** early (before the name regex) → 5 failures; after the
  herdr check → 2. Three of the five failures are only about *which error message wins*.

*Note on `--reason`:* the brief asks about `--model` **and/or** a `--reason` flag. `--reason` does
not exist today — `cmd_spawn` accepts exactly `--model` and `--cwd` (`bin/swarm:850-856`; any other
token → `die(f"spawn: unknown flag {rest[0]}")`). Its blast radius is therefore **identical** to
`--model`'s: the same 9 callers, the same 12 normative surfaces, the same 5 test failures. Requiring
both flags does not widen the radius — it is the *same* radius, since a single missing-required-flag
guard fails every one of these call sites regardless of how many flags it checks.
