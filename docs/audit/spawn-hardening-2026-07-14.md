# Spawn hardening — two field bugs, one root cause (2026-07-14)

Two bugs reported by the **first person outside this machine to run swarm**, on WSL. Both
are in the spawn path. They look unrelated — a permission dialog, a space in a path — and
they are the same bug wearing two hats:

> **Swarm specifies nothing and inherits whatever the author's machine happened to have.**

Neither bug could ever have fired on the dev machine, and that is not luck. Each one is
invisible *precisely because* of a property this machine has and a user's machine does not.
The bugs were not missed; they were **unreachable from here**.

---

## Bug 1 — the permission gate

`write_launcher()` emits `claude --settings <s> --model <M> "$PROMPT"`, and the settings
JSON swarm writes contains **only hooks** — no `permissions` block, no permission mode.
Swarm sets **no permission mode at all**. A child therefore gets whatever the machine's
ambient Claude Code config says.

**Why it never fired here.** This dev machine's own `~/.claude/settings.json` contains:

```json
"permissions": { "defaultMode": "auto" }
```

That is the **operator's personal config**, not swarm's. Every child ever spawned here
silently inherited `auto` from a file swarm does not own and does not ship. The WSL user
has no such line, so his children got Claude Code's real default — **manual** — and wedged
on the first permission dialog. A wedged pane renders as `idle` in `swarm ps`: invisible.

**This is the already-diagnosed root cause of a bug we misattributed.**
`docs/audit/weak-model-delegation-2026-07-13.md` reached exactly this conclusion in its own
bolded words — *"a permission gate swarm hands EVERY child regardless of model. Opus would
block too… Aim the fix at the gate."* — and we shipped a Haiku ban instead. `bin/swarm:133`
still carries a comment admitting the gate was never built, and `bin/swarm:145`'s refusal
text admits the settling probe was never run. The stall was never about Haiku. It was a
child that happened not to inherit the author's `auto` default.

**What Claude Code actually supports** (`claude --help`, verbatim):

```
--permission-mode <mode>   Permission mode to use for the session
                           (choices: "acceptEdits", "auto",
                            "bypassPermissions", "manual", "dontAsk", "plan")
```

`auto` and `bypassPermissions` are **distinct choices**. The mode that lets a child work
unattended is available *without* reaching for the bypass — so there is no honest reason to
hand every child `--dangerously-skip-permissions` and call it "auto." An agent that can edit
files unattended is the design. An agent that can do *anything* unattended is a liability.

---

## Bug 2 — the space in the path

`herdr_run_path()` returns a **bare, unquoted** string, and `cmd_spawn` hands it to
`herdr pane run`, which **types it into a shell**.

**Why it never fired here.** No path on this dev machine contains a space. Under WSL a
Windows path is `/mnt/c/Users/John Smith/…` — **spaces are normal there**.

**Reproduced in a real herdr pane** (herdr 0.7.3) with a launcher at
`…/scratchpad/spa ce dir/x.launch.sh`:

| construction | what the shell did |
|---|---|
| `"/" + path` (shipped code) | `zsh: no such file or directory: //…/scratchpad/spa` — **truncated at the space** |
| `"/" + shlex.quote(path)` | `LAUNCHER-RAN-OK: //…/spa ce dir/x.launch.sh` — **ran** |

### The construction is counterintuitive, and the obvious fix is wrong

herdr 0.7.3 has a bug: `pane run` **strips exactly one leading `/`** from the command it
types. Swarm already compensates by doubling the slash. Quoting has to compose with that,
and the order is decisive. Simulating the strip (`s[1:]`) and then `shlex.split`, over eight
adversarial paths, asserting the real contract — *strip-then-shell-parse must recover the
original path*:

- **`shlex.quote("/" + path)`** (double, *then* quote) — **fails on all 8**, even paths with
  no special characters. Quoting wraps the doubled slash *inside* the quotes, so herdr's
  strip eats the leading **quote character**, not a slash. The quote never protects anything.
  This is the trap: it is the natural-looking fix and it is wrong every time.
- **`"/" + path`** (shipped) — fails on space, `'`, and `"`. Two failure modes worse than
  reported: a `'` yields an **unterminated-string parse error**, and a `"` **silently mangles
  the path** to a *different* path (`/d"q"/c` → `/dq/c`). Silent corruption beats loud
  breakage for badness.
- **`"/" + shlex.quote(path)`** (slash **outside** the quoting) — **survives all 8**: space,
  `$`, `'`, `"`, backtick, parens, `;`, unicode, and the WSL-realistic path.

It works because the raw leading `/` is a **sacrificial character**: herdr's strip consumes
it and leaves `shlex.quote`'s output byte-intact for the shell. Confirmed in a live pane —
the launcher's `$0` arrives as `//private/…`, proving the doubled slash survived into the
shell and POSIX collapsed `//x` → `/x` at exec.

---

## The shell-interpolation sweep

Every site where a path reaches a shell, with a verdict. A site checked and found safe is a
real finding.

| # | site | verdict |
|---|---|---|
| 1 | `herdr_run_path()` → `herdr pane run` | **BROKEN** — bare, unquoted. The WSL bug. |
| 2 | `write_launcher()`: `echo "failed: settings unreadable: {settings}"` | **BROKEN** — `{settings}` unquoted *inside* a double-quoted shell string; a `$`, backtick, or `"` breaks or injects. Note the *rest* of `write_launcher` already quotes correctly — this error-message line is the one that was missed. |
| 3 | hook `"command": f"{self_path} {cmd}"` (settings JSON) | **SAFE** — `self_path` is `shlex.quote`d; `cmd` is an internal literal (`deliver`, `event stop`), never operator input. A genuine shell string, and worth checking, but sound. |
| 4 | `herdr tab create --cwd <cwd>` / `--env SWARM_DIR={root}` | **SAFE** — list-form `subprocess`, argv not shell. `pane run` is the only herdr verb that types into a shell. |
| 5 | `install.sh` / `bootstrap.sh` | **SAFE** — every expansion already double-quoted (`"$SWARM_HOME"`, `"$REPO"`, `"$BIN_DST"`). |

---

## The platform contract

Stated in `README.md` under Requirements, honestly and no wider than the ground truth:

- **macOS and Linux** — supported, exercised.
- **WSL** — the supported Windows path, now exercised by a real user. These two bugs are
  what he hit.
- **Git Bash / MSYS2 — not supported.** herdr's own installer rejects it outright
  (`✗ unsupported OS: MINGW64_NT-10.0-26200`), so swarm has no pane container to run in.

Swarm needs herdr; wherever herdr runs, swarm runs. That is the real boundary and it does
not overclaim.

---

## The lesson worth keeping

Both bugs are the same failure of imagination, and it is a **structural** one, not a
careless one:

- swarm sets **no permission mode** → and the author's machine happens to default to `auto`
- swarm quotes **no path** → and no path on the author's machine happens to have a space

In both cases the code relies on an ambient property of one laptop that it neither declares
nor ships. It passed every test and every day of real use here, and broke within minutes for
the first person who ran it somewhere else. **The dev machine is not a control; it is a
confounder.** The defect class to hunt next is not "another quoting bug" — it is *every
remaining place swarm declines to specify something and lets the environment decide.*
