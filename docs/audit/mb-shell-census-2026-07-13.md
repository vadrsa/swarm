# mb-shell census: executable `swarm spawn` calls in shell scripts

Scope: shell scripts only (per brief). Read-only, no edits/commits made.

## Bottom line

**Zero shell scripts in this repo literally execute `swarm spawn` as a command.**
The only executable subprocess calls to `swarm ... spawn ...` are in
`tests/test_swarm.py` (Python, not shell — flagging anyway, see bottom).

## How I searched (coverage proof)

1. `grep -n "swarm spawn" install.sh` — 0 hits.
2. `grep -n "swarm spawn\|swarm\b" bootstrap.sh` — 0 `spawn` hits (only clone/install
   references to the word "swarm" as a project name).
3. `find . -maxdepth 2 -iname Makefile` and a repo-wide
   `find . -iname Makefile -o -iname makefile -o -iname GNUmakefile` (excluding
   node_modules) — no Makefile anywhere in the repo.
4. `ls .git/hooks` — only `*.sample` template files present, nothing installed/executable.
   No `hooks/` directory exists anywhere else in the tree.
5. `grep -n "swarm spawn" docs/audit/bench/run-cell.sh` and
   `docs/audit/bench/run-cell-v3.sh` — 0 literal invocations in either (see below for
   what they actually do).
6. `grep -rn "swarm spawn" docs/audit/bench/fleet-briefs-v{1,2,3}` — hits only inside
   `.md`/`.txt` brief files, which are *prompt text fed to a model*, not shell code.
7. `grep -rn "spawn\|subprocess\|swarm" docs/audit/bench/v3-helpers/*.py` — the two
   Python helpers (`register-agent.py`, `deliver-next.py`) only `importlib`-load
   `bin/swarm` as a module to call its `next_delivery()`/`relation()` functions
   directly in-process; neither subprocesses `swarm spawn`.
8. `find .swarm/settings -iname "*.launch.sh" | wc -l` → **208** files.
   `grep -l "swarm spawn" .swarm/settings/*.launch.sh` → **0** matches.
   `grep -ho "swarm [a-z-]*" .swarm/settings/*.launch.sh | sort | uniq -c` → **0** matches
   (no file invokes any `swarm <subcommand>` at all).
   `grep -l "swarm" .swarm/settings/*.launch.sh` → all 208 match, but only because every
   file contains the literal log string `echo "[swarm] ERROR: claude not found..."` —
   a bracketed tag in an error message, not a command invocation.
   Read one file in full (`mb-tests.launch.sh`) plus a diversity spot-check of 8 more
   spread across the alphabet (`battery-smith`, `eval-red-glmforensics`, `grave-phil8`,
   `hc-tiers-qwen`, `mf-amend`, `pipeline-red`, `run-claude-base`, `theater-reader`,
   `ws-hooks-scout`) — **all 208 are the identical herdr-pane-launcher template**:
   check `claude` on PATH → check settings `.json` readable → `cat` the `.task` file →
   `exec claude --settings ... "$PROMPT"`. None shell out to `swarm` themselves.
9. Repo-wide backstop: `find . -name "*.sh" -not -path "./.git/*" -not -path
   "*/node_modules/*"` enumerated every `.sh` file in the tree (211 total: 208
   launch.sh + bootstrap.sh + install.sh + run-cell.sh + run-cell-v3.sh — nothing
   outside the categories already checked). Then
   `... | xargs grep -ln "swarm spawn"` against everything **not** already covered
   above → 0 hits.
10. `grep -n "swarm spawn" bin/swarm` — the CLI implementation itself never
    self-invokes `spawn` as a subprocess (hits are only in help text, docstrings,
    and the briefing string at bin/swarm:1015 that's *emitted to spawned agents*,
    not executed).

## Detail: the two "live-looking" scripts that are NOT literal spawn callers

### `docs/audit/bench/run-cell.sh` — LIVE/executable harness, but doesn't call spawn itself
Runs the fleet instruction-following battery. It calls `opencode run` (line 96-97,
`oc_turn()`) feeding it rendered briefs from `fleet-briefs-v2/`. **The model under
test**, not this script, is the one that may call `swarm spawn` at runtime — via a
sandboxed `SWARM_DIR` (line 61, `export SWARM_DIR="$SANDBOX/swarm"`) so it never
touches the live `.swarm/`. Comment at lines 13-17 states this explicitly: "This
script NEVER touches the live ./.swarm/. Every swarm operation — this script's and
the MODEL'S OWN `swarm spawn`/`send` — is redirected into the sandbox." This script
is still runnable today (it's parameterized, has usage docs, no dead paths) — it is
NOT a historical record. It also warns (line 77-81) that outside `HERDR_ENV=1` the
model's own `swarm spawn` attempts will fail — an `[H]` result the harness records,
not a call this script makes.

### `docs/audit/bench/run-cell-v3.sh` — LIVE/executable, same non-spawning pattern, one real `swarm send`
Same shape as run-cell.sh (clean-rig rerun). Also never literally calls
`swarm spawn`. It builds a **shim** at `$SANDBOX/bin/swarm` (lines 62-67) that
wraps the real `swarm` binary and puts it first on PATH — `exec "$SWARM_REAL" "$@"`
— so *whatever the model under test invokes* (including `spawn`) is forwarded
verbatim. The shim's own source text contains no literal `spawn`.
It DOES contain one literal executable call to `swarm send` (not spawn) at
**line 182**:
```
render "$BRIEFS/d3-$M.txt" "$N" "$O" \
  | SWARM_DIR="$SWARM_DIR" SWARM_AGENT_ID="$RUNNER" "$SWARM_REAL" send "$N" --stdin
```
This is `send`, unaffected by the `--model`/`--reason` requirement on `spawn`.
Positive test (expects success — script has no error handling around it beyond the
pipe, and a failure would just silently drop that message per the `||` on the next line).
Both v1/v2 (`fleet-briefs-v1/v2`) and v3 briefs are still live — v3 is the current
rig, but v1/v2 briefs remain referenced by `run-cell.sh` (which is pinned to
`fleet-briefs-v2/`, line 52) and are not deprecated/dead.

## `docs/audit/` `.sh`/brief files: historical vs. still-live

- **Still live/executable** (would actually run today if invoked): `run-cell.sh`,
  `run-cell-v3.sh`, and everything they read at runtime —
  `fleet-briefs-v2/*` (used by run-cell.sh), `fleet-briefs-v3/*` (used by
  run-cell-v3.sh), `v3-helpers/*.py`. `fleet-briefs-v1/*` is not referenced by
  either current script's `BRIEFS=` var, so it's superseded-but-not-deleted —
  treat as historical relative to current runs, though structurally identical
  and could be pointed to again trivially.
- **Historical/record-only** (past run outputs, not re-executed): everything else
  under `docs/audit/bench/` — `results-*.md`, `SCORING-AUDIT-V3.md`,
  `fleet-rubric-v1.md` (rubric doc, read by a human/runner, not executed),
  `factcheck-mcp-control.md`. And all the numbered/dated `.md` files directly
  under `docs/audit/` (e.g. `field-evidence-*.md`, `mandate-blast-radius.md`,
  `org-review-*.md`, `structure-mechanics-2026-07-12.md`, etc.) — these are prose
  audit reports; several contain `swarm spawn` example text but that's
  documentation of past findings, not something that runs.
- Judged by: does anything still read/exec this path? `run-cell.sh` and
  `run-cell-v3.sh` are parameterized CLI entry points with usage strings, actively
  reference frozen-but-current brief dirs (v2/v3), and their own headers describe
  ongoing/future paid runs ("the paid run is fleet-eval's ... call, on approval") —
  i.e., forward-looking, not archived. Everything else I found is dated output or
  narrative prose with no invocation path back to it.

## Out-of-slice flag: Python test file with real `spawn` subprocess calls

Not a shell script, so strictly outside my assignment, but directly relevant to the
`--model`/`--reason` breaking change and worth mandate-blast routing to whoever
owns Python/tests coverage:

`tests/test_swarm.py` — three live `subprocess.run([SWARM, "spawn", ...])` calls,
**none pass `--model` or `--reason`**:
- line 932: `subprocess.run([SWARM, "spawn", "abc\n", "task"], ...)` — tests that a
  newline-embedded name is rejected. Expects failure (negative test on the name
  arg), but will now *also* fail for missing `--model`/`--reason` — need to check
  which error message the test asserts on, since the assertion may currently target
  the name-validation message specifically.
- line 946: `subprocess.run([SWARM, "spawn", "abc\n", "task", "--trust"], ...)` —
  same shape, with `--trust`. Also missing `--model`/`--reason`.
- line 954: `subprocess.run([SWARM, "spawn", "ok-name", "task", "--bogus"], ...)` —
  tests rejection of an unknown flag `--bogus`. Positive-name/negative-flag test.
  Also missing `--model`/`--reason`.

All three are negative-path tests (asserting some other validation fires first), so
they may still pass by coincidence if the new required-flag check runs after the
checks these tests target — but that ordering is exactly the kind of thing that
silently flips when the requirement lands. Flagging for whoever owns test coverage.

## Non-hits worth naming explicitly (so absence reads as checked, not skipped)

- `install.sh`: no `swarm spawn` anywhere (in fact no `swarm` subcommand
  invocations of any kind — it only clones/builds/symlinks).
- `bootstrap.sh`: same — installer only, no swarm subcommands invoked.
- No Makefile exists in this repo (root or anywhere else).
- No live git hooks are installed (`.git/hooks/` has only Git's default `.sample`
  files).
- No `hooks/` directory exists outside `.git/`.
