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

**The default is `acceptEdits`**, overridable per-spawn (`swarm spawn --permission-mode MODE`)
or as a standing default (`.swarm/config`, `[spawn] permission_mode`). Precedence: flag →
config → `acceptEdits`. An invalid mode is refused *before* the child's name is claimed, so a
rejected spawn never burns a name.

### What `acceptEdits` actually permits — measured, including the parts that are not flattering

An earlier draft of this document claimed `acceptEdits` "lets a child do its job and nothing
more." **That was false, and the adversarial review caught it** (`docs/audit/spawn-red-2026-07-14.md`).
The claim rested on a single probe — one `curl … > file` command — which is *doubly* confounded:
gated by network policy *and* refused by the model's own exfiltration-suspicion heuristic. It
generalized from an unrepresentative sample, which is the very error this document diagnoses
elsewhere. The measured boundary, against a real `claude` with an **empty settings file** (`{}`,
so this machine's ambient `"defaultMode": "auto"` cannot leak in and manufacture a pass):

| action under `acceptEdits` | result |
|---|---|
| Edit / Write a file **in the cwd** | **allowed, unattended** — the design |
| `echo marker > f.txt` (local Bash, in cwd) | **allowed, unattended** |
| **`rm -f victim.txt`** (destructive Bash, in cwd) | **allowed, unattended** |
| `echo x > /tmp/outside.txt` (**outside** the cwd) | **blocked** — sandbox |
| `curl …` (**network egress**) | **blocked** |

**The true contract: `acceptEdits` gates network egress and writes outside the cwd, but permits
arbitrary local action inside the cwd — including deletion.** A child can do real damage within
its own working directory. Say that plainly rather than hide it.

### Why `acceptEdits` is still the right default

The honest choice set is not "safe vs. unsafe," it is four modes:

- `manual` — **the bug.** Children wedge on the first dialog and render as `idle`: invisible.
- **`acceptEdits`** — local action in-cwd; network and out-of-cwd writes gated. **Chosen.**
- `auto` — broader: **permits network egress.**
- `bypassPermissions` — everything. Never the default; reachable only on purpose.

`acceptEdits` is the **narrowest mode that actually unwedges a child** — and, critically, it is
**narrower than the status quo it replaces.** Before this PR swarm passed *no* permission flag,
so a child inherited the machine's ambient default; on this machine that is `auto`. Measured on
an identical benign task:

| mode | `curl -s https://example.com -o f.html` |
|---|---|
| `auto` (**what every child here already ran with**) | **downloaded — 559 bytes. Network permitted.** |
| `acceptEdits` (this PR) | **blocked, requires approval** |

So on the machine where swarm was built and every prior agent ran, **this change reduces child
privilege.** It raises it only where the ambient default was `manual` — i.e. the WSL user, whose
children were wedged and doing nothing at all. That trade is the entire point of his bug report.

We did not ship a disguised bypass: `bypassPermissions` and `--dangerously-skip-permissions`
remain distinct, opt-in, and deliberately not the default.

### Known hardening gap (real, pre-existing, not a blocker on this PR)

The review traced a genuine escalation path: `.swarm/config` sits **inside** the cwd sandbox, so
a child can write it — and that file drives both the spawn permission default *and* the
pre-existing `[middleware] command`, which `subprocess.run`s on **every** `swarm send`. A child
could therefore raise its own future children to `bypassPermissions`, or register itself as
tree-wide middleware.

Stated honestly in both directions: the mechanism is **real** and worth fixing. It is **not
created by this PR** — the middleware-exec feature predates it (`499cb2e`), `.swarm/config` does
not exist in this repo today, and children here already ran with `auto`, which is *broader* than
what this PR gives them. Filed as follow-up hardening (ACL or provenance check on `.swarm/config`),
not silently absorbed and not overstated.

---

## The Haiku ban was wrong, and the control run proves it

The ban rested on the claim *"it doesn't have auto mode."* `bin/swarm`'s own refusal text
admitted the settling probe **was never run**. It has now been run — twice, independently, by
two agents using different methods (a non-interactive probe with the control below; and a live
pane spawn that reached a real `Stop` event with `swarm ps` showing `[live] idle`, never
wedged). Both agree.

| model + flags | Edit a file | network egress |
|---|---|---|
| sonnet + `acceptEdits` | edits, unattended | gated |
| **haiku + `acceptEdits`** | **edits, unattended** | gated |
| **haiku, no flag** (what we shipped) | **refused** | — |

The third row is the whole case. **haiku with no flag** returns:

> *"The tool requires permission to edit the file. This is a non-interactive session, so I
> cannot proceed with the edit without your explicit permission."*

That is the **exact stall we attributed to Haiku** — reproduced by *removing a flag* from a
model we never banned, and cured by *adding it back*. Permission mode is a property of the
**harness**, not the model. Haiku clears the wall exactly as Sonnet does, and is gated exactly
as Sonnet is — identically, because the gate does not know which model is behind it.

**The ban is lifted.** We banned a model for an infrastructure bug, and the record now says so.

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
| 4 | `herdr tab create --cwd <cwd>` / `--env SWARM_DIR={root}` | **SAFE** — and the reason is precise: not merely "we passed a list," but that **`tab create` does not re-type its arguments into a shell.** `pane run` is the only herdr verb that does. A future herdr verb that shells out would be unsafe *even in list form*, so the property to check is the verb, not the call style. |
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

## Two findings nobody asked for

**The test fixture was lying.** `FAKE_HERDR`'s `pane run` case ran the launcher via list-form
`bash "$@"` — real argv, no shell. But the real `herdr pane run` **types its argument into a
shell**. So the fixture never simulated the one behavior that breaks, and **the 138-test suite
was structurally incapable of catching this bug.** That is why a green suite coexisted with a
spawn path that could not survive a space. The fixture now `eval`s the stripped string, and the
new end-to-end test was confirmed to *fail* against the old shim — a real regression guard, not
a coincidental pass. A test that cannot fail is worse than no test.

**A clean textual merge hid a semantic conflict.** The two fixes were developed in parallel and
merged without a single git conflict — then the suite failed with three `TypeError`s. One branch
had made `permission_mode` a required argument of `write_launcher()`; the other had written new
tests against the old signature. Neither was wrong; neither could see the other. *No textual
conflict is not the same as no conflict*, and the only thing that caught it was running the
suite on the merged result rather than trusting two green branches.

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
