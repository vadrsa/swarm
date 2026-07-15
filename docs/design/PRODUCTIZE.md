# PRODUCTIZE — the proven R&D, made real and reviewable

*productize, 2026-07-15. The unified design the operator approves FIRST. It folds in
three proven/designed pieces (the **yoke** harness, the **interactive coordinator**
path, and **config-UX**) under the operator's four config overrides and two rulings.
Read this before the code — the code is built to match it, as a stack of five small,
independently-reviewable PRs, none merged.*

---

## The plan, up front

Five PRs, each one concern, each keeping `bin/swarm`'s suite green (main is **163
passed, 10 subtests** — no PR regresses it) and each leaving existing **Claude**
spawning byte-for-byte unchanged on its own path.

| PR | Title | Touches | What it proves |
|----|-------|---------|----------------|
| **1** | **config foundation** — JSON config, alias schema, no-default mandate, `swarm models` | `bin/swarm` + tests | The config file is JSON; an alias names `{harness, model}`; a spawn with no `--model` is always an error; `swarm models` lists what is spawnable. Middleware + permission-mode readers still work. |
| **2** | **yoke** — rename + package the harness installable, the 3 fixes | `harness/` (new in-repo) + `install.sh` + tests | `yoke` is an installable command on PATH; it takes `--reason`, resolves its swarm-dir dynamically, and acquires a real free port. Stdlib-only. |
| **3** | **unified spawn dispatch** — `swarm spawn --model <alias>` routes to claude or yoke | `bin/swarm` + tests | One `swarm spawn` command reads the config and dispatches to the alias's **named** harness. Claude path unchanged; yoke path exercised end to end. |
| **4** | **interactive coordinator wiring** — yoke launches interactive-TUI-with-swarm-tools; MCP stripped | `harness/yoke` + tests | A yoke agent boots in interactive TUI mode with the swarm CLI + env + pump wired, and with non-swarm MCP tools stripped from its toolset. |
| **5** | **docs** — WORLD.md, SKILL.md, install.sh copy, the plain-language explainer | docs only | The user-facing story matches the built tool: yoke, the JSON config, one spawn command. |

**Dependency order:** 1 → 3 (dispatch reads the config schema PR 1 defines), 2 → 3
and 2 → 4 (dispatch and coordinator-wiring both call the `yoke` command PR 2 packages).
PR 5 rides last. Each branches off `origin/main`; PRs 3/4 will note their prerequisite
in the PR body so the operator reviews them in order. **None is merged** — the operator
reviews the design here first, then the PRs, and we iterate.

**Why this cut and not one big PR:** the operator asked to "see if we need to do more
changes." A five-way split lets him approve the config *schema* independently of the
*dispatch* that consumes it, and the *harness packaging* independently of the
*coordinator wiring* that rides on it — so a change of mind on any one joint is a
re-review of ~40 lines, not the whole system.

---

## The rulings and overrides this design obeys

Two rulings (settled) and four config overrides (which **supersede**
`docs/design/CONFIG-UX.md` where they conflict). Every one is discharged below; this
table is the checklist a reviewer runs against the design.

| # | Ruling / override | Where honored |
|---|---|---|
| R1 | Design doc first, code second | This doc is the primary artifact; §PR-1..5 are built to match it |
| R2 | Build against main, keep it green; don't break Claude spawning; test every new path | Every PR §; the green-invariant is restated per PR |
| C1 | **No default model** — remove the `default` alias/token; a spawn with no `--model` is always an error | §1, PR 1 |
| C2 | **JSON, not TOML** — one config file, JSON; handle what breaks (middleware + permission_mode readers) | §2, PR 1 |
| C3 | **Alias = harness + full model, explicit** — no slash-routing | §3, PR 1/3 |
| C4 | **Auto permission mode** — yoke default, and `--permission-mode` overridable for yoke too | §4, PR 3/4 |
| A | Harness → **yoke**, installable on PATH, 3 fixes | §5, PR 2 |
| B | Interactive coordinator path, wired, MCP stripped | §6, PR 4 |

---

## 1. C1 — No default model. Silence is always an error.

`SPAWN_MODELS` today is `("opus", "sonnet", "fable", "haiku", "default")`
(bin/swarm:66), and `default` is a real token that collapses to bare `claude`
(bin/swarm:1404). **The override removes it entirely.**

- `default` leaves `SPAWN_MODELS`. The builtin Claude tokens become
  `("opus", "sonnet", "fable", "haiku")`.
- The `launch_model = "" if model == "default" else model` collapse (bin/swarm:1404)
  **is deleted** — there is no longer a token that means "silence." Every accepted
  model resolves to a concrete launcher `--model`.
- A spawn with no `--model` still dies with `spawn_mandate_error()` (bin/swarm:1384,
  unchanged) — that mandate already exists. The change is that **no configured default
  can rescue it**: there is no `default` alias, and the resolver never invents one.
- The `unknown model` error (bin/swarm:1389-1392) drops its `default`-is-a-real-answer
  paragraph and instead names the accepted builtin tokens **plus the aliases the config
  defines**, pointing at `swarm models`.

Rationale, verbatim from the operator: *"always force to think."* A default is a way to
be silent; removing it means every spawn is a conscious model choice.

**What this costs, stated honestly:** the `default` token's original job — "I looked at
this child and the configured default is right, and that is a *decision*, not silence"
(bin/swarm:53-56) — goes away. The operator has judged that the decision is better
expressed by naming the actual model every time. There is no half-measure: the token is
gone, and a spawn that names no model is an error, always.

---

## 2. C2 — JSON config, one file. What breaks, and how it's handled.

The override: config is **JSON**, and prefer **one file**. Today `.swarm/config` is
flat-TOML-ish, read by `tomllib` (py3.11+) or the `read_flat_toml` fallback
(bin/swarm:448), on two wired paths:

- `registered_middleware(root)` (bin/swarm:479) — the send-path middleware.
- `configured_permission_mode(root)` (bin/swarm:514) — the spawn-path permission mode.

Both are **fail-open**: any error (no file, no section, unparseable) returns `None` and
the caller behaves as if unconfigured. That posture is the safety net that lets us
migrate without a flag day.

**Decision: one file, `.swarm/config`, migrated to JSON.** Not a second file — the
override prefers one, and two config files is exactly the split-brain the unification
goal (`swarm world`) exists to avoid.

The migration, concretely:

1. Introduce **one** reader, `read_config(root)`, that loads `.swarm/config` as JSON
   (`json.load`) and returns a dict, or `{}` on any error (same fail-open contract).
   `read_flat_toml` and the inline `tomllib` blocks in the two readers are **replaced**
   by calls to `read_config`.
2. The JSON shape maps the old sections to top-level keys:
   ```json
   {
     "spawn":      { "permission_mode": "auto" },
     "middleware": { "command": "python3 /path/to/mw.py", "identity": "middleware", "timeout": 60 },
     "harness":    { "yoke": "/absolute/path/to/yoke" },
     "models": {
       "glm51": { "harness": "yoke",   "model": "zai-coding-plan/glm-5.1" },
       "flash": { "harness": "yoke",   "model": "deepseek/deepseek-v4-flash" },
       "judge": { "harness": "claude", "model": "opus" }
     }
   }
   ```
   `spawn` and `middleware` keep their exact keys, so `registered_middleware` and
   `configured_permission_mode` read the same values from the same names — only the
   *parser* under them changes. `harness` and `models` are new (§3).
3. **Backward-compat, decided:** because the two live readers are already fail-open, an
   *old* flat-TOML `.swarm/config` on a user's disk will parse as invalid JSON →
   `read_config` returns `{}` → middleware and permission-mode silently fall back to
   their built-in defaults (no middleware; `DEFAULT_PERMISSION_MODE = auto`). That is a
   **silent config loss on upgrade**, and it is the one migration hazard. PR 1 handles
   it two ways, both cheap:
   - `read_config` detects a legacy file: if `json.load` fails **and** the first
     non-comment line looks like a TOML section (`[spawn]` / `[middleware]`), it emits a
     one-line stderr warning (`.swarm/config looks like the old TOML format; swarm now
     reads JSON — see docs/design/PRODUCTIZE.md §2`) and still returns `{}`. Loud, not
     silent.
   - `install.sh` gains a migration note (PR 5), and `swarm models` (which reads the
     config) prints the same warning when it sees a legacy file, so the first
     discovery command a user runs surfaces the problem.
   We do **not** auto-rewrite the user's file — a tool that silently rewrites a config
   it found is the self-modifying-config hazard bin/swarm already flags (bin/swarm:113).
   The warning tells the human to convert it; the format is trivial.
4. **Tests:** PR 1 adds JSON-config cases to the existing middleware and permission-mode
   test coverage (both already tested) — a JSON `[middleware]`/`[spawn]` equivalent
   drives the same behavior; a legacy-TOML file triggers the warning and the fail-open
   default; a malformed JSON file fails open. The existing 163 must stay green, which
   means the tests that today write a TOML `.swarm/config` fixture are updated to write
   JSON (the fixtures move with the format).

**Why `json`, no new dep:** `json` is stdlib; `tomllib` (py3.11+) and the hand-rolled
`read_flat_toml` both go away, so this is a net *reduction* in parsing surface, not an
addition.

---

## 3. C3 — Alias = harness + full model, explicit. No slash-routing.

CONFIG-UX's original dispatch keyed on a `/` in the token: a `provider/model` token
routed to opencode, a bare token to Claude (CONFIG-UX §2). **The override replaces that
heuristic with an explicit named harness in each alias.** The harness is *declared*, not
*deduced from token shape*.

An alias entry is an object naming both:
```json
"glm51": { "harness": "yoke",   "model": "zai-coding-plan/glm-5.1" },
"judge": { "harness": "claude", "model": "opus" }
```

There are exactly **two harnesses**: `"claude"` and `"yoke"`. The dispatch (§ PR 3):

```
token = --model value
1. It must be a KEY in config [models]  → resolve to { harness, model }.
   There is no bare-token fast path and no slash heuristic: --model always names
   an alias, and the alias names the harness explicitly.
   (Exception, kept minimal: the four builtin Claude tokens — opus, sonnet, fable,
    haiku — resolve as if aliased to { harness: "claude", model: <token> } WITHOUT
    needing a config entry, so a bare `swarm spawn --model opus` still works with no
    config file at all. This is the ONE implicit resolution, and it is the existing
    Claude behavior preserved, not new magic. See "the builtin question" below.)
2. harness == "claude"  → CLAUDE PATH (unchanged): validate model in the Claude
   token set, then the existing launcher (bin/swarm:1264). Byte-for-byte as today.
3. harness == "yoke"    → YOKE PATH: subprocess (NOT exec — bin/swarm stays alive to
   report) the installed `yoke` command:
     yoke <name> "<task>" --model <alias.model> --parent <own id>
          --reason "<--reason value>" --swarm-dir <root> [--permission-mode <mode>]
   bin/swarm waits, passes stdout/stderr through, exits with yoke's code. On a yoke
   failure bin/swarm is the one that says "spawn failed" and points at the boot log.
4. else (unknown harness name in an alias)  → die: "alias '<a>' names harness
   '<h>'; the harnesses are claude, yoke."
```

**The builtin question — decided.** Slash-routing is gone, so how does a bare
`--model opus` still work? Two honest options:

- **(chosen) Implicit builtin aliases.** The four Claude tokens resolve to
  `{ harness: "claude", model: <token> }` without a config entry. Rationale: it
  preserves today's zero-config Claude spawning exactly (R2 — don't break Claude
  spawning), it is *not* a slash heuristic (the override's target), and it is a closed
  set of four, not an open rule. A config `[models]` alias with the same name **shadows**
  the builtin (the config wins) — so `"opus": {"harness":"yoke","model":"..."}` is
  possible and does what it says, no special case.
- **(rejected) Require every model, including Claude, to be a config alias.** Cleaner in
  theory — every `--model` names an alias, no implicit set — but it breaks
  `swarm spawn --model opus` on a machine with no config file, which regresses Claude
  spawning (R2) and forces every user to write a config before their first spawn. The
  operator's override targets *harness deduction from token shape*, not *the existence
  of builtin Claude tokens*. So the builtins stay implicit; the slash heuristic dies.

This keeps C3's intent — **the harness is named, never guessed** — while honoring R2.
A reviewer checks: there is no code path that infers `yoke` from a `/` in the token; a
`/`-containing model reaches yoke **only** through an alias that says `"harness":"yoke"`.

---

## 4. C4 — Auto permission mode: yoke default, and overridable.

Two halves, both required:

1. **Auto is the yoke default.** The harness already sets auto-approve
   (`spawn-oc-tui.py` passes `--auto`, and denies only the two interactive-only gates
   `doom_loop`/`question` so they fail fast rather than wedge an unattended agent). PR 2
   keeps that as the default when no `--permission-mode` is given.
2. **`--permission-mode` is expressible for yoke too.** CONFIG-UX made `--permission-mode`
   a Claude-only flag that *refused* on a yoke spawn (CONFIG-UX §2, §5). **The override
   reverses that:** the flag must be passable to yoke. Mapping (opencode's permission
   model is a per-tool allow/ask/deny map, not Claude's named modes):

   | swarm `--permission-mode` | yoke's opencode.json `permission` |
   |---|---|
   | `auto` (default) | `{"*": "allow", "doom_loop": "deny", "question": "deny"}` (today's) |
   | `plan` | `{"*": "deny"}` (read-only-ish: no tool acts; the agent plans) — *see limit* |
   | `acceptEdits` | `{"*": "allow", "webfetch": "deny", "doom_loop": "deny", "question": "deny"}` (no network egress) |
   | `bypassPermissions` | `{"*": "allow"}` (drops even the interactive-gate denies) |
   | `manual` / `dontAsk` | **refused for yoke** — an unattended headless/TUI agent has no human to answer an "ask"; these two modes *are* "ask a human," which is a silent wedge. Die with one sentence. |

   So `--permission-mode` is **expressible** for yoke (C4 satisfied) for the modes that
   have an unattended meaning, and **honestly refused** for the two that mean "ask a
   human," rather than silently ignored. bin/swarm validates the mode before handing off;
   yoke translates it to the opencode map.

**Honest limit carried into the design:** the `plan`/`acceptEdits` mappings above are a
*best-effort translation* of Claude's named modes onto opencode's per-tool map, not a
1:1 semantic match (opencode has no first-class "plan mode"; `{"*":"deny"}` approximates
it). PR 4's tests assert the *map yoke writes* for each mode, not a claim that opencode's
behavior is identical to Claude's under that name. If a mapping proves wrong under real
use, it's a one-line table change — the design commits to *expressibility and honesty*,
not to a false equivalence.

---

## 5. A — yoke: the harness, renamed, packaged, and fixed.

`spawn-oc.py`/`spawn-oc-tui.py` become **`yoke`**, an installable command on PATH,
installed the way `swarm` is (symlink into `~/.local/bin`, via `install.sh`). It moves
from the throwaway R&D checkout (`/Users/vadrsa/git/swarm-rnd/harness/`) into the swarm
repo (`harness/yoke`), stdlib-only, no new deps.

**Which script is the reference.** The *interactive TUI* variant (`spawn-oc-tui.py`, 224
lines) is the productization target — it is the proven coordinator path (§6), and the
brief **shelves** the headless `serve` + `wake-oc.py` HTTP path. So `yoke` is built from
`spawn-oc-tui.py`, not the 491-line serve harness. This scoping decision has a
consequence for fix 3 (below).

**The three required fixes** (found by the CONFIG-UX red-team + coord runs — do not ship
without them):

1. **`--reason` accepted and recorded.** Today both scripts *fabricate* their own reason
   (`spawn-oc-tui.py:134`, `spawn-oc.py:251`). `yoke` takes `--reason "<clause>"` and
   writes it into the journal tombstone and agent record, exactly as bin/swarm's spawn
   does (bin/swarm:1438-1440). The parent chose the model; the parent's reason belongs in
   the record. bin/swarm's dispatch (§3) passes `--reason` through.
2. **Drop the hardcoded `SWARM_DIR`.** Today `spawn-oc-tui.py:42` hardcodes
   `SWARM_DIR = "/Users/vadrsa/git/swarm/.swarm"` (and `SWARM_BIN_DIR`, `FORK_DIR`,
   `HARNESS_DIR`, `PUMP_SRC` similarly). `yoke` resolves these dynamically:
   - `--swarm-dir <root>` argument (passed by bin/swarm's dispatch), else the `SWARM_DIR`
     env var, else refuse with a clear message. No machine-specific literal survives.
   - The swarm `bin` dir (for the child's PATH) is derived from where `yoke`/`swarm`
     actually live, not hardcoded.
   - The workspace root and pump source move into the repo (`harness/`) and resolve
     relative to `yoke`'s own location (`os.path.dirname(__file__)`), so an installed
     symlink still finds them (resolve through the symlink with `os.path.realpath`).
   - **Open item for the operator:** the fork path (`FORK_DIR` — where the opencode fork
     lives) is genuinely machine-specific and cannot be derived. It becomes a
     `[harness] yoke_fork` config key (or a `YOKE_FORK` env), same fail-closed posture as
     `[harness] yoke`. Flagged here because it's the one path that *must* be configured,
     not derived. (See "the fork dependency" below.)
3. **Real free-port acquisition.** `spawn-oc.py:250` uses
   `4200 + (abs(hash(name)) % 400)` — Python salts `hash()` per process, so it's
   effectively random and collision-prone with no retry; a colliding bind is a failed
   boot, which burns a name. **Scope:** this bug lives in the *serve* path (the TUI path
   binds no port). Since `yoke` is built from the TUI script, **the TUI mode has no port
   to fix.** The design's resolution: *if* `yoke` retains any port-binding mode
   (a shelved serve path kept in the fork for the future pane-less case), that path uses
   real free-port acquisition — bind `('127.0.0.1', 0)`, read back
   `sock.getsockname()[1]`, close, use it. PR 2 ships this helper and uses it wherever a
   port is bound; the primary TUI path simply never calls it. The fix is *present and
   correct* so the serve path can never regress to the salted hash, even though the
   default path doesn't exercise it.

**The fork dependency — stated plainly.** `yoke` launches the *opencode fork* (a `bun`
project at `FORK_DIR/packages/opencode`). That fork is **not** in the swarm repo and is
not something `install.sh` can vendor here. So `yoke` installs as a command, but it is
*inert* until `[harness] yoke` (the yoke command path — auto after install) **and**
`[harness] yoke_fork` (the fork checkout) are configured, and `bun` is on PATH. This is
the honest edge of packaging: the *harness* graduates into the repo; the *fork it drives*
does not, yet. `swarm models` reports yoke as "not ready" until the fork is configured,
with the exact key to add — the same fail-closed-with-instructions posture CONFIG-UX §3
established for a missing harness. This is called out for the operator because it means
PR 2 delivers an installable-but-not-yet-runnable command on a machine without the fork —
which is correct and honest, not a gap.

---

## 6. B — the interactive coordinator path, wired.

**Proven result** (source: `swarm-rnd/coord-tui/COORD-TUI-FINDINGS.md`, digested
separately): cheap models (GLM-5.1, DeepSeek-flash) *can* coordinate a subtree — spawn
workers, read files, catch a planted bug, steer a fix, stop cleanly — **when run in
interactive TUI mode**, and a TUI coordinator **wakes on the ordinary `swarm send`
doorbell** (measured 25-35s), with no HTTP wake-fix needed. That is why interactive is
the default coordinator-capable mode and the headless serve + `wake-oc.py` HTTP hack is
shelved.

So `yoke` must launch an agent in **interactive TUI mode with the swarm tools wired**.
`spawn-oc-tui.py` already does exactly this as a rig; PR 4 ports that wiring into `yoke`
properly. The wiring, made a first-class part of `yoke` rather than a rig:

- **`cd packages/opencode/` then `bun run src/index.ts <ws> -m <model> --auto --prompt
  "<task>"`** — the TUI boot sequence (`spawn-oc-tui.py:181-188`), with the `cd` that
  loads `bunfig.toml`'s JSX-transform preload and the no-subcommand invocation.
- **swarm CLI on PATH** — the swarm `bin` dir prepended to the child pane's `PATH`
  (dynamically resolved per fix 2, not hardcoded), so the coordinator can run
  `swarm spawn / ps / send`.
- **Env: `SWARM_AGENT_ID`, `SWARM_DIR`, `SWARM_PARENT`** (+ `SWARM_DIGEST_COOLDOWN=1`)
  in the pane env, so the pump identifies the agent and the swarm CLI targets the right
  state dir.
- **The pump plugin** (`.opencode/plugin/swarm-pump.js`) copied into the workspace and
  discovered by opencode's plugin glob — the duty pump that delivers queued mail on
  `session.idle` and rings the doorbell.
- **Initial task via the TUI's `--prompt`** — the task is the TUI's first turn, exactly
  like a Claude agent's initial prompt; later mail arrives via the swarm queue + pane
  doorbell.

**The MCP-leak quirk — fixed.** Non-swarm MCP tools leak into the cheap coordinator's
toolset and confuse it. The findings name the leaked servers as
`bridgemind`/`bridgememory`/`playwright` and note the per-workspace `opencode.json` does
**not** strip them today (COORD-TUI-FINDINGS.md:161-164); neither model chased them *this*
run, but "GLM headless" did in a prior run, and coord-test's standing advice is to strip
them. PR 4 **strips non-swarm MCP tools from a yoke agent's toolset**: the yoke workspace's
`opencode.json` disables MCP servers other than swarm's own (opencode's config can
disable/omit MCP tools per-project), so a yoke coordinator sees the swarm CLI and file
tools, and nothing else. PR 4's test asserts the launched agent's effective toolset
contains no non-swarm `mcp__*` tools.

*Citation caveat:* the exact strip *mechanism* (which `opencode.json` key disables an MCP
server, and the observation of GLM-headless chasing the tools) is **not** established by
the two sources I read — it traces to a separate `coord-test` report. PR 4's builder
confirms the precise key against the opencode fork's config schema and the coord-test
report before wiring it, rather than inventing a key name here. The design commits to the
*outcome* (no non-swarm MCP tools reach the agent), verified by the toolset assertion.

**Honest limits carried into the design** (do not overclaim — the operator reviews this):

- **"Checks its team via `swarm ps`" is driver-attested, not independently traced.** The
  findings mark this ("measure 2") as driver-attested for all four runs, because the saved
  pane captures preserved only the last ~23 lines, so an earlier `swarm ps` call is not
  re-verifiable from disk (COORD-TUI-FINDINGS.md:75-81). A *related* nuance the adversarial
  review flagged: the spawn ("measure 1") and clean-stop ("measure 6") claims also rest on
  the coordinator's **journals + pane transcript + coord-tui's own live `ps` reads**, not
  on a per-claim timestamped `ps.txt` artifact (COORD-TUI-FINDINGS.md:179-187) — it doesn't
  change the verdict, but the record should be exact. PR 4's end-to-end test makes ps-use
  **observable and re-checkable**: it spawns a real cheap coordinator, gives it a task that
  *requires* checking its team, and asserts a `swarm ps` invocation actually appears in the
  captured pane/log — turning an attested behavior into a traced one (and, by capturing
  full output rather than the last 23 lines, hardening the spawn/stop evidence too).
- **The `--permission-mode` → opencode-map translation is best-effort** (§4), not a
  semantic 1:1.
- **The fork is a runtime dependency `install.sh` can't vendor** (§5) — yoke is inert
  until the fork is configured.
- **Cheap coordinators fat-finger `swarm send` targets and mis-resolve relative paths.**
  Observed in the runs: `ds-tui-mm` sent its DONE report to *itself* instead of its parent
  (a target typo; the pump's duty-loop digest still delivered a terser report to the real
  parent, so nothing was lost), and a coordinator told to write `evidence/<name>/woke.txt`
  resolved it against its own workspace cwd, not the intended dir
  (COORD-TUI-FINDINGS.md:152-159). Design consequence: a productionized coordinator brief
  should use **absolute paths**, and the swarm contract's existing pump-digest fallback (a
  report reaches the parent even if the coordinator misaddresses it) is load-bearing for
  cheap models — not an accident to remove. Nothing to build here; a caveat the operator
  and the SKILL.md coordinator doctrine (PR 5) should carry.
- **PR 4's end-to-end test needs the fork + `bun` + provider auth on the runner.** If the
  CI/local runner lacks them, that one test is **skipped with a loud reason**, never
  silently passed — the rest of PR 4 (the wiring/toolset-map assertions, which are pure
  file/argv checks) runs without the fork. The green invariant (R2) is about the 163
  existing tests, which never touch the fork; the new end-to-end test is additive and
  gated on its dependencies being present.
- **Scale is small.** The proof is 2-worker subtrees, one task shape, 4 wake samples (not
  a distribution), no coordinator-managing-coordinators, no long-horizon run
  (COORD-TUI-FINDINGS.md:170-173). The capability is proven *at that scale*; the design
  claims no more.

---

## 7. The PR stack, in build detail

Each PR: branch off `origin/main`, keep the 163-test suite green, add tests for every
new path, `gh pr create`, **do not merge**.

### PR 1 — config foundation
- **Change:** remove `default` from `SPAWN_MODELS` and delete the `default→""` collapse
  (C1); replace `read_flat_toml` + inline `tomllib` with one JSON `read_config(root)`
  (C2); define the `[harness]` + `[models]` schema in the reader (C3, consumed by PR 3);
  add `swarm models` (read-only discovery: builtin Claude tokens, configured aliases with
  their named harness + resolved model, yoke readiness); legacy-TOML detection warning.
- **Green invariant:** middleware and permission-mode tests pass against JSON fixtures;
  Claude spawning unchanged (the `default` removal is the only Claude-path behavior
  change, and it's a policy tightening the operator ordered — a test asserting
  `--model default` now *errors* is added, replacing any test that asserted it worked).
- **Tests:** JSON config read; legacy-TOML warning + fail-open; malformed-JSON fail-open;
  `swarm models` output shape; `--model default` now refused; no-`--model` still refused.

### PR 2 — yoke (harness installable + 3 fixes)
- **Change:** move `spawn-oc-tui.py` → `harness/yoke` (stdlib-only); add `--reason` (fix
  1); dynamic swarm-dir/bin/pump resolution via `--swarm-dir`/env/`__file__` (fix 2);
  free-port helper for any port-binding path (fix 3); `install.sh` symlinks `yoke` onto
  PATH beside `swarm`.
- **Green invariant:** `harness/` is new/moved; no `bin/swarm` behavior changes here, so
  the 163 are untouched. `install.sh --uninstall` removes the new symlink too.
- **Tests:** `yoke --reason` writes the reason into tombstone + record; `yoke` with
  `--swarm-dir` writes to that dir (no hardcoded path); `yoke` with `SWARM_DIR` env same;
  `yoke` with neither refuses; free-port helper returns a bindable port; install/uninstall
  symlink round-trip. (Tests that need the fork are gated/skipped-with-reason.)

### PR 3 — unified spawn dispatch
- **Change:** in `cmd_spawn`, after the mandate checks, resolve `--model` through the
  config `[models]` alias (or the four implicit Claude builtins), dispatch to the claude
  path (unchanged) or subprocess `yoke` per the alias's **named** harness (C3); thread
  `--reason`, `--swarm-dir`, and the translated `--permission-mode` (C4) to yoke; the
  five refusal/failure messages (unknown alias, unknown harness, harness not configured,
  provider not authed, yoke boot failure with boot-log path).
- **Green invariant:** the claude path is entered by exactly the same tokens as today
  (the four builtins), so every existing Claude spawn test passes unchanged; a `/`-model
  can reach yoke *only* through an explicit alias — asserted by test.
- **Tests:** alias → yoke subprocess (mocked `yoke` for the unit path so no fork needed);
  alias → claude path unchanged; unknown-alias / unknown-harness / harness-not-configured
  refusals fire before the name is burned; `--reason` reaches yoke's argv; multi-line task
  survives the argv handoff; `--permission-mode plan` translates and is threaded.

### PR 4 — interactive coordinator wiring
- **Change:** `yoke` launches interactive TUI with swarm tools wired (§6); strip non-swarm
  MCP tools from the yoke workspace's `opencode.json`; make `swarm ps` use observable.
- **Green invariant:** additive; the pure wiring/toolset assertions run without the fork;
  the one live end-to-end coordinator test is gated on fork+bun+auth and
  skipped-with-reason otherwise.
- **Tests:** the launched agent's `opencode.json` disables non-swarm MCP servers (file
  assertion); the pane env carries `SWARM_*` and PATH (argv/script assertion); the pump is
  copied into the workspace; **[gated]** a real cheap coordinator spawns a worker, catches
  a planted bug, and a `swarm ps` call is observed in its pane/log.

### PR 5 — docs
- **Change:** WORLD.md, skill/SKILL.md, install.sh copy, and the plain-language explainer
  updated for `yoke`, the JSON config, the alias schema, and the one `swarm spawn` command;
  the CONFIG-UX doc gets a header pointing at this doc as the superseding design.
- **Green invariant:** docs only; no code, no test change.

---

## 8. What a reviewer checks (the adversarial pass, pre-report)

Before I report to the operator, a fresh reviewer (not a builder) verifies, against the
diffs and a real test run:

1. **All four config overrides honored** — C1 (no `default`, no-`--model` always errors),
   C2 (JSON one-file, middleware+permission-mode still work, legacy file warns), C3 (alias
   names harness explicitly; no `/`-routing anywhere in the code), C4 (auto is the yoke
   default and `--permission-mode` is expressible for yoke, refused honestly for
   ask-a-human modes).
2. **No regression** — the 163-test suite is green on every PR branch, and no existing
   Claude-spawn test changed behavior except the operator-ordered `default` removal.
3. **yoke's three fixes are actually in the diff** — `--reason` recorded, no hardcoded
   `SWARM_DIR`, real free-port acquisition present for any port-binding path.
4. **The honest limits are stated, not buried** — the ps-use-is-attested caveat, the
   permission-map best-effort caveat, the fork-dependency, and the gated end-to-end test.

The reviewer's verdict is reported to the operator alongside the PR list.

---

## Appendix — sources this design stands on

- **Overrides & rulings:** `.swarm/journal/operator.md.CONFIG-NOTES` (the 4 config
  overrides), `.swarm/journal/operator.md.HARNESS-NAME` (yoke naming + packaging), the
  task brief's two rulings.
- **The harness:** `swarm-rnd/harness/spawn-oc-tui.py` (the proven interactive path — the
  yoke reference), `spawn-oc.py` (the shelved serve harness — source of the port fix and
  the pump contract).
- **The coordinator proof:** `swarm-rnd/coord-tui/COORD-TUI-FINDINGS.md`,
  `coord-tui/tasks/DRIVER-PROTOCOL.md` (digested to `.swarm/tmp/productize/coord-digest.md`).
- **The prior design (superseded in mechanism, kept in goal):** `docs/design/CONFIG-UX.md`
  — the unification goal (one spawn command, one config, one discovery verb) stands; the
  slash-routing / TOML / `default`-alias mechanisms are replaced by the four overrides.
- **The tool:** `bin/swarm` — `SPAWN_MODELS` (:66), `default→""` collapse (:1404),
  `read_flat_toml` (:448), `registered_middleware` (:479), `configured_permission_mode`
  (:514), `cmd_spawn` mandate + dispatch (:1332-1464), launcher (:1264); `install.sh` (the
  symlink-on-PATH install pattern).
</content>
</invoke>
