# CODEX-DESIGN — codex agents in swarm, the simplest thing that is true

> SUPERSEDED by archival — its conclusion doesn't transfer to opencode per OPENCODE-PLUGIN.md §9; kept for the record (the spawn/hook-mapping mechanism and NOT-in-v1 scoping decisions OPENCODE-PLUGIN.md reuses as a template).

Companion to CODEX-CAPABILITIES.md (all mechanics cited there are VERIFIED
unless noted). Goal: `swarm spawn` can create an OpenAI Codex CLI session as
an agent, and every sentence of WORLD.md stays true of it.

The finding that shapes everything: codex's hook system is Claude-compatible
enough that **the existing hook verbs run under codex unmodified** — a live
codex agent delivered, evented, restored, journaled, and reported through
today's `bin/swarm` with zero code changes. The integration is therefore an
adapter at *spawn time only*: a different launcher and a per-agent
`CODEX_HOME`. Nothing in the message plane forks.

## 1. The shape: one spawn flag

```
swarm spawn <name> "<task>" [--model M] [--cwd DIR] [--agent codex]
```

`--agent` defaults to `claude`. The agent record gains one field
(`"agent": "codex"`). No new verbs, no adapter layer, no second code path
after launch: deliver/event/restore behave identically because codex calls
the same hook commands with the same JSON.

## 2. What bin/swarm gains, function by function

- **`cmd_spawn`** — parse `--agent`; on `codex`, call `write_codex_home`
  and the codex branch of `write_launcher`. Everything else (tombstone,
  task file, status file, tab create with `SWARM_DIR`/`SWARM_AGENT_ID` env,
  readiness wait) is unchanged.
- **`write_codex_home(dir, cwd)`** — new, small. Generates
  `settings/<name>.codex/` containing:
  - `config.toml`:
    ```toml
    [projects."<cwd>"]
    trust_level = "trusted"            # kills the TUI trust prompt

    [[hooks.UserPromptSubmit]]
    matcher = ""
    [[hooks.UserPromptSubmit.hooks]]
    type = "command"
    command = "<abs path to bin/swarm> deliver"

    # same shape for hooks.Stop -> "event stop"
    # and hooks.SessionStart  -> "restore"
    ```
  - `auth.json` — symlink to `~/.codex/auth.json` (verified: auth works
    through the symlink; the user's `~/.codex/config.toml` is never read or
    written — codex records its own trust/session state inside the agent's
    home).
- **`write_launcher`** — codex branch, same status-file protocol:
  ```bash
  # pre-flight: codex on PATH, auth.json resolvable, settings readable
  export CODEX_HOME=<settings/<name>.codex>   # exported, not inline:
  echo "launching" > "$STATUS"                # manual `codex resume` in
  codex --dangerously-bypass-hook-trust \     # this pane later just works
        --no-alt-screen -s workspace-write -a never \
        --add-dir "$SWARM_DIR" \
        ${model:+-m "$model"} "$PROMPT"
  rc=$? ; [ $rc -ne 0 ] && echo "failed: codex exited code $rc" > "$STATUS"
  exec bash
  ```
  Flag rationale: `--dangerously-bypass-hook-trust` — swarm wrote the hooks
  it is trusting, which is the flag's stated use; `--no-alt-screen` —
  scrollback survives for pane reads; `-s workspace-write -a never` — the
  only autonomous combination (nobody watches a child's approval prompt);
  `--add-dir $SWARM_DIR` — queue writes and journal appends stay legal when
  an agent's cwd is outside the swarm repo (one flag removes the failure
  class; untested live, the flag is documented).
- **`cmd_event`** — two lines: prefer the payload's
  `last_assistant_message` (codex provides it) over the transcript parse
  (Claude path, unchanged fallback). Without this, `ps` shows empty last
  words for codex agents.
- **`pane_prompt_line`** — one character: match `›` (codex composer)
  alongside `❯` (Claude). Without it the doorbell still lands (verified)
  but burns its settle retries, ~4 s slower and blind to the drain.
- **`cmd_deliver`, `cmd_restore`** — zero changes. Verified verbatim.

Two functions added-or-branched, three functions touched by a line or two.

## 3. Hook map — what each swarm verb rides on

| swarm verb | Claude Code | codex 0.142.5 | delta |
|---|---|---|---|
| `deliver` | UserPromptSubmit | UserPromptSubmit | none — same input, same `additionalContext` output, 8000-char cap fits (7.8 KB verified whole) |
| `event stop` | Stop | Stop | payload carries `last_assistant_message` directly — prefer it |
| `event notification` | Notification | **none** | degrades; see §4 |
| `restore` | SessionStart | SessionStart (`source: startup/resume/compact`) | none |

The doorbell (herdr send-text + Enter) and the stop re-ring reuse the same
pane primitive for both kinds — verified against a live codex TUI.

## 4. What degrades, stated honestly

- **No notification fact for codex agents.** Codex has no Notification
  hook. Under `-a never` codex also never waits on an approval — the state
  Claude's Notification mostly witnesses — so the fact is *mostly* moot,
  but `event/<name>.json` will only ever say `stop` for a codex agent, and
  `ps` idle detection rests on Stop alone.
- **A codex agent can be soft-killed by OpenAI's safety layer.** Verified
  twice: a flagged session refuses further turns, and stays refused across
  resume. Queue files and journal survive; the session may not. The pane
  shows the flag banner — observable, like every other failure here.
- **Model availability is account-shaped.** A `--model` the account can't
  use fails at the *first turn*, after the launcher reports "launching" —
  the readiness signal can say started for an agent whose first turn then
  errors in-pane. Same class as Claude's own first-turn failures; the pane
  is ground truth.
- **Restart is manual in v1.** On exit codex prints
  `To continue this session, run codex resume <session-id>` into the pane,
  and the launcher leaves `CODEX_HOME` exported in the pane shell, so the
  printed command works as-is. Restore then re-injects task + journal tail
  (verified). No automation on top.
- **Cosmetic**: the bypass-hook-trust warning and codex tips print in the
  pane; codex stores sessions/trust inside the per-agent home (isolated by
  design).

## 5. WORLD.md — the exact sentence changes

One sentence changes, one word each way. Current (WORLD.md concept 1):

> 1. **Agent** — a Claude session in a herdr pane, with a **name**, a
>    **parent**, and a **journal**. The pane is ground truth; anyone may
>    read anyone's pane.

becomes:

> 1. **Agent** — a Claude or Codex session in a herdr pane, with a
>    **name**, a **parent**, and a **journal**. The pane is ground truth;
>    anyone may read anyone's pane.

And the spawn header string in `bin/swarm` (`spawn_header`):

> You are agent {name} in a swarm — a tree of Claude agents.

becomes:

> You are agent {name} in a swarm — a tree of agents.

Nothing in "What is promised, plainly" changes: delivered-means-delivered,
best-effort promptness, the operator mailbox, and nothing-tracks-obedience
were each exercised against a live codex agent and hold as written.
`docs/design/SIMPLEST.md` stays as-is — it is the historical spec of the
system it describes, not the living contract; WORLD.md is.

## 6. Concept count

Still **nine concepts, four verbs**. "Codex" is not a tenth concept — it is
one word widening concept 1, one spawn flag, and one `"agent"` field in a
record that already exists. A reader of WORLD.md needs to learn nothing new
except that a pane may contain a different harness. The cost that is real
but sub-conceptual: two generated files per codex agent
(`settings/<name>.codex/config.toml`, symlinked `auth.json`) inside plumbing
that already generates per-agent files.

## 7. NOT in v1 — deliberately

- **`codex exec` (headless) agents.** The pane is ground truth; a headless
  agent has no pane. Not an agent kind, ever, without a WORLD.md rethink.
- **Stop-`decision:block` as the re-ring.** Verified working and strictly
  stronger than the doorbell (in-process, no pane race) — but it would give
  codex agents a *different* re-ring mechanism than Claude agents. One
  mechanism for both kinds until the doorbell is proven inadequate; the
  design watchlist inherits this as the named upgrade path.
- **`notify` config.** Redundant next to the Stop hook.
- **PermissionRequest / approval modes other than `-a never`.** No human
  watches a child's approval prompt; an agent that needs escalation should
  say so in its journal and report.
- **PreToolUse/PostToolUse/SubagentStart/SubagentStop wiring.** Swarm
  tracks facts, not tool calls. Compaction is already covered: codex fires
  SessionStart with `source: "compact"`, which `restore` handles today.
- **Automated crash-restart / session-id bookkeeping.** v1 restart is the
  printed resume command in the pane (§4). If restart automation ever
  lands, it lands for both kinds.
- **Codex cloud, MCP-server mode, app-server, profiles, plugins, skills,
  `--search`.** Not swarm's business.

## 8. Open items for hardener (after human review)

1. Live-verify `--add-dir $SWARM_DIR` actually legalizes queue writes from
   a cwd outside the swarm repo (documented, not probed).
2. Live-verify compaction restore (`source: "compact"`) once a codex agent
   naturally compacts — needs a long session; not cheaply probeable.
3. Phrase spawn briefs to avoid OpenAI's safety tripwires (the probe got
   flagged on "secret token" phrasing; swarm briefs are innocuous, but the
   flag is a live failure mode worth one WATCHLIST line).
