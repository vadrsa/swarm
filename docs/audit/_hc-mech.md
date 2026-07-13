# bin/swarm — mechanical code trace

Scope: `bin/swarm` in this repo (1429 lines, single Python file). Every claim
below is file:line + quoted code. No design commentary, no proposals.

---

## 1. `write_launcher()` — bin/swarm:1041-1069

Signature: `write_launcher(launcher, statusfile, settings, taskfile, model)` (bin/swarm:1041).

Full body written to `launcher` (mode `0o755`, bin/swarm:1069):

```
#!/usr/bin/env bash
set -uo pipefail
STATUS=<statusfile, shell-quoted>
if ! command -v claude >/dev/null 2>&1; then
  echo "failed: claude not found on PATH" > "$STATUS"
  echo "[swarm] ERROR: claude not found on PATH in this pane" >&2
  exec bash
fi
if [ ! -r <settings, shell-quoted> ]; then
  echo "failed: settings unreadable: <settings>" > "$STATUS"
  exec bash
fi
PROMPT="$(cat <taskfile, shell-quoted>)"
echo "launching" > "$STATUS"
claude --settings <settings> --model <model> "$PROMPT"      # only if model given
claude --settings <settings> "$PROMPT"                      # if model == ""
rc=$?
if [ "$rc" -ne 0 ]; then echo "failed: claude exited code $rc" > "$STATUS"; fi
exec bash
```

(bin/swarm:1046-1066, `lines = [...]` list joined with `"\n"`.)

**Fixed across every spawn:** the shebang, `set -uo pipefail`, the `claude`-on-PATH
preflight, the settings-readability preflight, `echo "launching" > "$STATUS"`,
the exit-code check, and the trailing `exec bash` (bin/swarm:1065, comment:
`"keep the pane inspectable after claude ends"`).

**Varies per spawn**, each baked in as a literal at write time (not read at
run time from env/argv):
- `statusfile` → `$STATUS` (bin/swarm:1049)
- `settings` → both the readability test and the `--settings` flag
  (bin/swarm:1055, 1061-1062)
- `taskfile` → the file `$PROMPT` is `cat`'d from (bin/swarm:1059)
- `model` → conditionally adds `--model <model>` (bin/swarm:1061-1062)

**Not varied by `write_launcher` itself:** `cwd` and `--trust` are NOT part of
the launcher script. `cwd` is applied earlier, when the herdr tab is created
(`herdr tab create --cwd cwd ...`, bin/swarm:1175) — the launcher script
inherits whatever directory the pane/shell was started in; there is no `cd`
line in the launcher body. `--trust` triggers `pre_trust_dir()`
(bin/swarm:1171-1172), which patches `~/.claude.json` directly — also outside
the launcher script.

**Where `claude` is exec'd:** bin/swarm:1061-1062 — note this is a plain
`claude ...` invocation, NOT `exec claude ...`. The script continues past it
(captures `$?`, may write to `$STATUS`, then unconditionally runs `exec bash`
at bin/swarm:1065) — so `claude` runs as a foreground child process of the
launcher script, and the launcher's own shell persists (via the final `exec
bash`) after `claude` exits, for either outcome.

**When no `--model` was given:** `model` is `""` because `cmd_spawn` defaults
`model = ""` (bin/swarm:1103) unless `--model` is passed. The ternary at
bin/swarm:1061-1062 (`if model else`) then selects the second branch:

```
f'claude --settings {shlex.quote(settings)} "$PROMPT"'
```

i.e. `claude` is invoked with no `--model` flag at all — bare `claude`, so
whatever model `claude` itself defaults to is what runs. The written
launcher script permanently reflects this branch (it is baked at spawn time,
not decided at run time by the script).

---

## 2. `cmd_spawn()` — bin/swarm:1098-1226

### Preconditions / validation (bin/swarm:1099-1132)
- Requires `argv` to have at least `name, task` (bin/swarm:1099-1101).
- Parses `--model`, `--cwd`, `--trust` (bin/swarm:1104-1122); unknown flags die.
- Name must match `NAME_RE = r"^[a-z0-9][a-z0-9-]{0,39}\Z"` (bin/swarm:48, checked at 1124-1126).
- `name` may not be `"operator"` or `"delivered"` (bin/swarm:1127-1128).
- `task` must be non-empty after strip (bin/swarm:1129-1130).
- Requires `HERDR_ENV == "1"` in the environment, else dies with `"not inside
  herdr (HERDR_ENV != 1); spawn needs herdr as the container"` (bin/swarm:1131-1132).

### State written to disk under `.swarm/` (in order)

1. **Journal-as-tombstone / name claim** (bin/swarm:1137-1145):
   `claim_name(root, name)` opens `journal/<name>.md` with `O_CREAT|O_EXCL`
   (bin/swarm:940-947) — raises `FileExistsError` if the name was ever used,
   which `cmd_spawn` turns into a `die()` (bin/swarm:1139-1142, message:
   `"name '{name}' was already used (journal/{name}.md exists); a name is
   one agent, forever — pick another"`). The journal is then written with an
   initial entry:
   ```
   # journal of {name}

   ## {fmt_ts(now_ms())} — spawned
   Task from {parent}: {task}
   ```
   (bin/swarm:1144-1145).

2. **Settings file** `settings/<name>.json` (bin/swarm:1155-1160), written via
   `write_atomic`:
   ```json
   {"hooks": {
     "UserPromptSubmit": [h("deliver")],
     "Stop": [h("event stop")],
     "Notification": [h("event notification")],
     "SessionStart": [h("restore")]}}
   ```
   where `h(cmd)` (bin/swarm:1152-1154) produces
   `{"matcher": "", "hooks": [{"type": "command", "command": "<self_path> <cmd>"}]}`
   and `self_path = shlex.quote(os.path.realpath(__file__))` (bin/swarm:1150)
   — i.e. every hook re-invokes this same `bin/swarm` script with a subcommand.

3. **Task file** `settings/<name>.task` (bin/swarm:1161-1162):
   `write_atomic(taskfile, spawn_header(name, parent) + task)` — the full
   briefing text (the "Nine concepts" contract preamble, bin/swarm:950-990)
   prepended to the literal task string passed to `spawn`.

4. **Status file** `settings/<name>.status` (bin/swarm:1163-1167): any
   pre-existing file at that path is unlinked (best-effort) before launch, so
   a stale status can't be misread as this run's signal.

5. **Launcher script** `settings/<name>.launch.sh` (bin/swarm:1168-1169):
   built by `write_launcher(launcher, statusfile, settings, taskfile, model)`
   — see §1.

6. **Optional trust patch** to `~/.claude.json` (bin/swarm:1171-1172, only if
   `--trust`) — outside `.swarm/`, not part of the per-agent state, described
   here only because it's part of the same spawn call: `pre_trust_dir(os.path.realpath(cwd))`.

7. **Agent record** `agents/<name>.json` (bin/swarm:1190-1192), written via
   `write_atomic` AFTER the herdr tab/pane is created and the launcher is
   told to run:
   ```json
   {"name": name, "parent": parent, "pane": pane, "tab": tab,
    "model": model, "cwd": cwd, "task": task, "ts": now_ms()}
   ```
   Comment at bin/swarm:1188-1189: *"Record the binding BEFORE the readiness
   wait: the record + the launcher signal are the truth; a slow start must
   never lose the agent."* Note `model` here is the raw `--model` value (or
   `""` if not given) — this is the ONE on-disk location of the "model pin"
   (see §4).

No separate "queue dir" is created explicitly at spawn — `queue/<name>/` is
implicitly a directory that `q_dir()` (bin/swarm:94-95) computes but nothing
in `cmd_spawn` calls `os.makedirs` on it; it is created lazily by whichever
`write_atomic` call from `cmd_send` first writes a message file into it
(pattern established at bin/swarm:118-125, `os.makedirs(os.path.dirname(path), exist_ok=True)`).
No `event/<name>.json` is written by spawn either — that's created lazily by
`record_event()` (bin/swarm:508-513) on the agent's first Stop/Notification hook.

### What the pane runs

1. `herdr tab create --cwd <cwd> --no-focus --label <name> --env
   SWARM_DIR=<root> --env SWARM_AGENT_ID=<name>` (bin/swarm:1175-1176) creates
   a new herdr tab/pane; `pane` and `tab` ids are read from the JSON result
   (bin/swarm:1177-1182); dies with `"herdr tab create failed"` if no pane id
   comes back (bin/swarm:1183-1184).
2. `herdr pane run <pane> <herdr_run_path(launcher)>` (bin/swarm:1185-1186)
   — this is the ONLY command actually typed into the new pane. `herdr_run_path`
   (bin/swarm:993-1011) is a pure shim: if `launcher` is an absolute path it
   doubles the leading slash (`//path/to/launch.sh`) to survive a confirmed
   herdr 0.7.3 bug that strips exactly one leading `/` from `pane run`'s
   command; a relative path passes through untouched.
3. The pane thus executes `settings/<name>.launch.sh`, i.e. the full script
   from §1 — which is what actually execs `claude`.

### Readiness wait (bin/swarm:1194-1225)

Polls `statusfile` up to `SWARM_READY_TIMEOUT` seconds (default 30, env
override, bin/swarm:1196) once per second (bin/swarm:1212), reading its first
line:
- starts with `"failed"` → `outcome = "failed"` (bin/swarm:1201-1204)
- starts with `"launching"` → `outcome = "started"` (bin/swarm:1205-1207)
- timeout with neither → `outcome = "unknown"` (loop exits at 1210-1211,
  default `outcome` stays `"unknown"` from 1197)

On `"failed"`: closes the herdr tab (`herdr tab close <tab>`, bin/swarm:1216-1217),
deletes `agents/<name>.json` (bin/swarm:1218-1221, comment: `"binding goes;
tombstone stays"` — the journal file from step 1 is NOT deleted, so the name
remains permanently claimed/burned), and `die()`s with the failure reason
read back from the status file (bin/swarm:1213-1222).

On `"unknown"`: prints a warning to stderr but keeps the agent
(bin/swarm:1223-1225).

On `"started"`: falls through and prints `name` to stdout (bin/swarm:1226) —
this is `cmd_spawn`'s only stdout output on success.

---

## 3. The restore hook — bin/swarm:916-935 (`cmd_restore`)

### What fires it

Wired into `settings/<name>.json` at spawn time as the `SessionStart` hook
(bin/swarm:1160: `"SessionStart": [h("restore")]`), which expands to a command
hook invoking `<self_path> restore` (bin/swarm:1152-1154). Per the file's own
header comment (bin/swarm:23): `# restore   SessionStart — re-inject the
original task + the journal tail`. `cmd_restore`'s own comment
(bin/swarm:917): `# SessionStart (startup or post-compaction): original task
and journal tail.` The dispatch source (`payload.get("source")`,
bin/swarm:932) distinguishes a fresh launch (`"startup"`, the fallback value
used if absent) from a post-compaction resume (`"compact"`) — see
`build_restore` below. Claude Code's SessionStart hook fires whenever a
session (re)starts in this pane, which is what happens both on the very
first `claude` invocation from the launcher AND whenever `claude` is
relaunched into an existing/compacted session in that same pane.

Guard at bin/swarm:918-919: if `my_name() == "operator"` (i.e.
`SWARM_AGENT_ID` env var unset), the hook exits immediately without emitting
anything — restore only fires meaningfully for spawned agents, never for the
human operator's own shell.

### Exactly what it re-injects

1. Reads `settings/<name>.task` (the file written at spawn — see §2 item 3 —
   which is `spawn_header(name, parent) + task`, i.e. the FULL original
   briefing text, not just the bare task string) into `task`
   (bin/swarm:923-928); on any `OSError` (e.g. file missing) `task` stays `""`.
2. Builds the injection via `build_restore(task, journal_path(root, name),
   source)` (bin/swarm:462-472):
   ```python
   def build_restore(task_text, jpath, source):
       resumed = ("AFTER A CONTEXT COMPACTION — your working memory was just "
                  "summarized away; your journal is your most reliable record"
                  if source == "compact" else "a fresh session")
       tail = journal_tail(jpath)
       return (f"[swarm restore] You are resuming {resumed}.\n\n"
               f"--- YOUR ORIGINAL TASK ---\n{task_text}\n\n"
               f"--- YOUR JOURNAL (tail) ---\n{tail or '(journal is empty)'}\n\n"
               f"Continue from where the journal leaves off, and keep appending "
               f"to it as you work.")
   ```
3. The journal tail comes from `journal_tail(path, cap=JOURNAL_TAIL_CAP)`
   (bin/swarm:449-459), where `JOURNAL_TAIL_CAP = 4000` (bin/swarm:34, chars
   not lines — comment: `# restore: at most this many chars of journal
   tail`). If the journal text is `<= 4000` chars it's returned whole
   (bin/swarm:456-457); otherwise the LAST 4000 chars are kept, prefixed with
   a truncation marker naming the full path (bin/swarm:458-459):
   ```python
   return (f"[…journal truncated to its last {cap} chars — "
           f"read the full file: {path}]\n") + text[-cap:]
   ```
   So: **not a line count — a 4000-character cap on the tail of the journal
   file**, taken from the end (most recent entries), with an explicit marker
   when truncation occurred.
4. Emitted via `emit_hook_output({"hookSpecificOutput": {"hookEventName":
   "SessionStart", "additionalContext": <the string above>}})`
   (bin/swarm:929-932) — Claude Code's SessionStart hook contract for
   injecting additional context into the new session.
5. Any exception in the whole try block is swallowed (bin/swarm:933-934,
   bare `except Exception: pass`) — restore never crashes the pane; worst
   case is a session that starts with no injected context.

### What an agent experiences after its pane is killed and relaunched

Mechanically, from what's traced above: if the pane is killed and `claude`
is started again in it via the SAME launcher script (`settings/<name>.launch.sh`,
still present on disk with the same `--settings`/`--model`/`taskfile`
baked in from the original spawn), SessionStart fires again, `cmd_restore`
runs again, and the agent's new session is seeded with:
- The header `[swarm restore] You are resuming a fresh session.` (since a
  brand-new `claude` process's hook payload `source` would be `"startup"`,
  not `"compact"`, per the ternary at bin/swarm:464-466) — restore does not
  distinguish "relaunched after a kill" from "very first launch"; both look
  like a fresh SessionStart to this hook. The `"compact"` branch is reserved
  for Claude Code's own post-compaction resume within a still-running
  session, not for a pane restart.
- The exact same original task text (`spawn_header + task`), read fresh from
  `settings/<name>.task` — unchanged since spawn, so identical to what the
  agent saw originally.
- The last (up to) 4000 characters of its own journal file at
  `journal/<name>.md` — i.e. whatever the agent itself had written before it
  was killed. If the agent journals right before going idle/dying (its
  briefed duty, per bin/swarm:960-963 in `spawn_header`), that journal tail
  is what carries state across the kill; if it hadn't journaled, the
  relaunch sees `(journal is empty)` for the tail (still gets the original
  task).
- Everything NOT in the task file or the journal (mid-task scratch state,
  unsaved reasoning, anything only in the killed process's memory or
  transcript) is gone — restore's only two inputs are the static task file
  and the journal file on disk.

---

## 4. The model pin on disk

### Where it lives

The ONLY on-disk record of a spawn-time model pin is the `"model"` field in
`agents/<name>.json`, written at bin/swarm:1190-1192:
```python
write_atomic(agent_rec_path(root, name), json.dumps(
    {"name": name, "parent": parent, "pane": pane, "tab": tab,
     "model": model, "cwd": cwd, "task": task, "ts": now_ms()}))
```
`model` is the raw string from `--model` parsing (bin/swarm:1103-1106),
default `""` if `--model` was never passed. `agent_rec_path` is defined at
bin/swarm:106-107 as `agents/<name>.json`.

The SAME value is also baked (not merely recorded) into the launcher script
via `write_launcher(..., model)` (bin/swarm:1169, body at bin/swarm:1061-1062)
— that's a second, independent place the value is written to disk (the
executable launcher), but it is not a "record" read back by other code; it's
consumed only by `bash`/`claude` when the pane runs.

### Every code path that reads it (grep for `"model"` / `.get("model")`)

```
$ grep -n '"model"\|\.get("model")' bin/swarm
616:        m = str(agents[n].get("model") or "")
1192:         "model": model, "cwd": cwd, "task": task, "ts": now_ms()}))
```

Only TWO hits in the whole file:
- bin/swarm:1192 — the WRITE, inside `cmd_spawn` (§2 item 7 above).
- bin/swarm:616 — the ONLY read, inside `model_of(n)` in `render_ps`
  (bin/swarm:591-622), used by `swarm ps` (see below). No other command
  (`cmd_send`, `cmd_deliver`, `cmd_event`, `cmd_restore`, `cmd_close`) reads
  `agents[*]["model"]` at all — the pin is write-once at spawn and read-once
  by the ps view. It plays no role in delivery, restore, or event handling.

### How `swarm ps` renders it, including the `(you)`-forgery guard

`model_of(n)` (bin/swarm:591-622):
```python
def model_of(n):
    m = str(agents[n].get("model") or "")
    m = "".join(c for c in m
                if c.isprintable() and not c.isspace()
                and c not in MODEL_STRUCTURAL)
    if len(m) > MODEL_CAP:
        m = m[:MODEL_CAP - 1] + "…"
    return f" model={m}" if m else ""
```
- Empty pin → empty string → nothing rendered (bin/swarm:591-594 docstring:
  *"A non-empty model means PINNED with --model at spawn; empty means NOT
  pinned... so ps says nothing."*).
- Non-empty pin is sanitized: drop non-printable chars, drop whitespace
  (`not c.isspace()`), drop every char in `MODEL_STRUCTURAL`
  (bin/swarm:617-619).
- `MODEL_STRUCTURAL = set("()") | set("─│├└┌┐┘┬┴┼")` (bin/swarm:47) — the
  parens (`(`, `)`) that delimit the `(you)` marker, plus every box-drawing
  glyph `render_ps` uses to draw the tree.
- `MODEL_CAP = 40` (bin/swarm:36-40, sized off the longest real id observed:
  25 for `claude-haiku-4-5-20251001`, 33 for a Bedrock id
  `us.anthropic.claude-opus-4-8-v1:0`; 40 leaves headroom). Over-cap values
  are cut to `MODEL_CAP - 1` chars plus a trailing `…` (bin/swarm:620-621) —
  never silently truncated without the ellipsis marker.
- Rendered as its own token, `" model=" + m"` (bin/swarm:622), concatenated
  onto the tree line at bin/swarm:643-644:
  ```python
  lines.append(f"{prefix}{branch}{name}{you}{model_of(name)} "
               f"[{alive}] {q_of(name)} {idle_of(name)}")
  ```
  where `you = " (you)" if name == me_name else ""` (bin/swarm:640) is
  computed and concatenated SEPARATELY, immediately before `model_of(name)`.

**The forgery guard, precisely:** since `model` is attacker-controlled
(any agent can run `swarm spawn --model 'you' ...`, bin/swarm:597-598
docstring), rendering it as `(you)`-shaped text (e.g. `(you)` directly, or
via literal parens in the pin) could become byte-identical to the `(you)`
marker that identifies the reader's own row (bin/swarm:540-543,
596-604 docstrings). The guard has two parts:
1. **Syntax separation**: the pin is rendered as `model=x`, a form that can
   never collide with `(you)` syntactically — bin/swarm:601-604:
   *"model=you is self-evidently a claim about a MODEL, so the forge defeats
   itself."*
2. **Character exclusion**: even so, `(` and `)` are stripped from the pin
   value before rendering (bin/swarm:619, via `MODEL_STRUCTURAL`) — so a pin
   value could never inject a literal `(you)` substring into the line either,
   independent of the `model=` prefix. Comment at bin/swarm:41-46 explains
   why this is an EXCLUDE list, not an allow-list: an allow-list would mangle
   legitimate ids (e.g. Bedrock's `v1:0`), whereas excluding only the
   specific glyphs that do structural work in this view (`()` and the
   box-drawing set) is safe by construction.

---

## 5. Mechanically: relaunching an existing agent's pane with a different `--model`

Describing ONLY existing mechanics (verbs/state that already exist in this
file) — no new verbs invented.

**State that would need to change:**
- `agents/<name>.json`'s `"model"` field (bin/swarm:1190-1192) — currently
  write-once at `cmd_spawn`; there is no existing verb that rewrites an
  agent record post-spawn. (`cmd_send`, `cmd_event`, `cmd_restore` never
  touch `agents/<name>.json`; only `cmd_spawn` writes it, and `cmd_close`
  reads but does not rewrite it — see below.) This is the field `swarm ps`
  reads (§4), so it alone governs the DISPLAYED pin.
- `settings/<name>.launch.sh` — the launcher script — currently baked at
  spawn time by `write_launcher(...)` (bin/swarm:1041-1069) with `model`
  fixed as a literal in the `claude --settings ... --model ...` line
  (bin/swarm:1061-1062). This is what governs the ACTUALLY EXECUTED model on
  next run of that script. `write_launcher` is a plain function — nothing
  stops calling it again with a new `model` argument to overwrite the file
  at the same path, but no CLI verb currently does so; `cmd_spawn` is the
  only call site (bin/swarm:1169).
- `settings/<name>.task`, `settings/<name>.json` (hooks) — would NOT need to
  change; neither embeds the model.

**Existing operations that would be involved:**
1. **herdr pane verbs available** (grepped above): `pane run`, `pane list`,
   `pane read`, `pane send-text`, `pane send-keys`, `pane close`. There is no
   `pane restart` or `pane kill` verb used anywhere in this file. `cmd_close`
   (bin/swarm:1342-1361) tries `herdr tab close <tab>` first
   (bin/swarm:1352-1355) and falls back to `herdr pane close <pane>`
   (bin/swarm:1356-1359: `subprocess.run(["herdr", "pane", "close",
   a["pane"]], ...)`) only if the tab-close didn't report success — the
   closest thing to a teardown primitive in this file, and it is destructive
   (the whole tab/pane), not a targeted process kill.
   Getting a pane to run something new is done exactly once in this codebase
   via `herdr pane run <pane> <path>` (bin/swarm:1185-1186), the same verb
   `cmd_spawn` uses for the initial launch — it is not spawn-specific, it's a
   general "type this command into this pane" primitive (per the herdr skill
   surface), so it is mechanically reusable against an EXISTING pane id
   (`agents[name]["pane"]`, already on disk) rather than only a freshly
   created one.
2. **Launcher rewrite**: `write_launcher(launcher, statusfile, settings,
   taskfile, new_model)` could be called again, pointed at the SAME
   `settings/<name>.launch.sh` path, to rewrite the script in place with the
   new `--model` value baked in (or removed, for bare `claude`). This is a
   plain file write (`open(launcher, "w")`, bin/swarm:1067-1069) — same
   mechanism `cmd_spawn` already uses, just re-invoked against an existing
   name's paths instead of freshly computed ones.
3. **Re-running the pane**: `herdr pane run <pane> <herdr_run_path(launcher)>`
   (the same call as bin/swarm:1185-1186) against the EXISTING `pane` id
   (read from `agents/<name>.json`) would type the (now-rewritten) launcher
   path into the pane again. Whether this needs the pane's current occupant
   (a running `claude`/`bash`) killed/exited first, and how, is not
   established anywhere in `bin/swarm` — this file's `herdr pane` usage is
   limited to `run/list/read/send-text/send-keys/close`; there's no code
   path here that stops a running process inside a pane other than `herdr
   pane close` (which tears down the whole pane, per `cmd_close`'s use).
4. **Restore on the next SessionStart**: once a new `claude` process starts
   in that pane (however it got started), `cmd_restore` (§3) fires
   automatically via the `SessionStart` hook already wired in
   `settings/<name>.json` (unchanged, still points at this same file) and
   re-injects the original task text plus the journal tail — exactly as it
   would for any other relaunch. This part requires no new state changes at
   all; it is what already happens whenever `claude` (re)starts under this
   settings file, per §3.
5. **`agents/<name>.json`'s `"model"` field** would separately need an
   overwrite (`write_atomic`, the same primitive used everywhere else in
   this file, e.g. bin/swarm:1190-1192) for `swarm ps`'s `model_of()` (§4) to
   display the new pin — this is purely cosmetic to the ps view and has no
   bearing on what the launcher/pane actually executes; the two are
   independent pieces of state written by two different lines in
   `cmd_spawn` today (bin/swarm:1169 vs. 1190-1192) and nothing keeps them
   in sync except that `cmd_spawn` happens to write both from the same
   `model` variable in one call.

**Net: three independent writes, one reused pane-typing verb, one hook that
already fires for free.** No existing single verb performs this; `cmd_spawn`
is the only call site that currently exercises `write_launcher` +
`herdr pane run` + the `agents/<name>.json` write together, and it does so
only for a NAME NEVER USED BEFORE (`claim_name`'s `O_CREAT|O_EXCL`,
bin/swarm:940-947, bin/swarm:1137-1142) — spawning is not reentrant for an
existing name today.
