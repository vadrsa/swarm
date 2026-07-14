# CODEX-CAPABILITIES — what codex 0.142.5 can actually do for swarm

> SUPERSEDED by archival as a companion to CODEX-DESIGN.md, same archived status; kept for the record (the VERIFIED-tagged capability probe methodology — hooks, delivery, restore, sandboxing — that OPENCODE-PLUGIN.md's own probes copy).

Evidence from live probes of the installed binary (`codex-cli 0.142.5`,
`/opt/homebrew/bin/codex`, ChatGPT-account auth, default model `gpt-5.5`),
run 2026-07-10 in `/tmp/codex-scout-sandbox` and scratch herdr tabs (all
closed). Every claim is tagged:

- **VERIFIED** — I ran it; the exact command is in §10.
- **DOCUMENTED** — official docs / `--help` say so; not exercised live.
- **SUSPECT** — inference; could be wrong.

The one-line summary: **codex has a stable hooks system nearly isomorphic to
Claude Code's — the unmodified `bin/swarm deliver`, `event stop`, and
`restore` hook verbs ran under codex without a single edit** (§8). Swarm's
contract survives almost intact; the deltas are listed in §9.

## 1. Launch

- **Initial prompt** — `codex "<prompt>"` starts the interactive TUI and
  **auto-submits** the prompt as the first turn. VERIFIED (TUI probe: the
  task text appeared as `› …` and ran without a keypress).
- **Model** — `-m/--model <slug>` works; availability is account-dependent.
  VERIFIED: default `gpt-5.5` ran; `-m gpt-5.1-codex-mini` was rejected by
  the API ("not supported when using Codex with a ChatGPT account") — the
  flag reached the API, the account said no. A bad model errors *after*
  launch, at first turn.
- **cwd** — launching with the pane's working directory set is sufficient;
  `-C/--cd <dir>` also exists. VERIFIED (pane cwd) / DOCUMENTED (`-C`).
- **Env passthrough** — `SWARM_AGENT_ID` / `SWARM_DIR` set on the pane env
  reach (a) shell commands the model runs (`echo $SWARM_AGENT_ID` →
  `tui-probe`) and (b) **hook processes** (my hook logger captured both
  vars). VERIFIED in exec and TUI. Default `shell_environment_policy`
  inherits the environment.
- **Non-interactive** — `codex exec "<prompt>"` runs one task headlessly;
  `--json` (JSONL events), `-o` (last message to file), `--ephemeral` (no
  session persisted), `--ignore-user-config` (skip `~/.codex/config.toml`,
  auth still works) all exist. VERIFIED (used throughout probing).
- **TUI niceties** — `--no-alt-screen` keeps scrollback (good for pane
  reads). VERIFIED. On exit codex prints `To continue this session, run
  codex resume <session-id>` — the resume handle is observable in the pane.
  VERIFIED.

## 2. Hooks — the big one

Codex 0.142.5 ships a **stable** `hooks` feature (`codex features list`:
`hooks stable true`). Events (from the binary + docs, DOCUMENTED; starred
ones VERIFIED live): `SessionStart`*, `UserPromptSubmit`*, `Stop`*,
`SubagentStart`, `SubagentStop`, `PreToolUse`, `PostToolUse`,
`PermissionRequest`, `PreCompact`, `PostCompact`. There is **no
`Notification` event** (see §5).

- **Config** — `hooks.json` or `[hooks]` tables in `config.toml`, at user
  (`$CODEX_HOME`) or repo (`.codex/`) level. The JSON shape is Claude's:
  `{"hooks": {"UserPromptSubmit": [{"matcher": "", "hooks": [{"type":
  "command", "command": "..."}]}]}}`. DOCUMENTED. Two per-agent injection
  routes VERIFIED:
  1. **Inline overrides**: `-c 'hooks.UserPromptSubmit=[{matcher="",hooks=[{type="command",command="/path/cmd arg"}]}]'` — works per-invocation, touches no file.
  2. **Per-agent `CODEX_HOME`**: a generated `config.toml` with `[[hooks.X]]` tables (§6).
- **Hook trust** — non-managed hooks require interactive review (`/hooks`)
  before they run; `--dangerously-bypass-hook-trust` skips that for the
  invocation (prints a ⚠ warning line in the TUI). VERIFIED: without the
  flag untested; with the flag, hooks fire in both exec and TUI. Since
  swarm generates its own hooks, "automation that already vets hook
  sources" is literally our case.
- **Input payload** (stdin JSON) — Claude-compatible field names. VERIFIED
  captures:
  - common: `session_id`, `transcript_path`, `cwd`, `hook_event_name`,
    `model`, `permission_mode`, `turn_id` (turn-scoped events).
  - `UserPromptSubmit` adds `prompt`; `SessionStart` adds `source`
    (`startup`/`resume`); `Stop` adds `stop_hook_active` **and
    `last_assistant_message`** (the final text, directly — no transcript
    parsing needed).
- **Output** — `{"hookSpecificOutput": {"hookEventName": "...",
  "additionalContext": "..."}}` injects text into the model's turn.
  VERIFIED for `UserPromptSubmit` and `SessionStart` (model echoed my
  sentinel tokens back). A 7,830-char context was delivered **whole**
  (model reported first and last words) — swarm's 8,000-char cap fits.
  VERIFIED.
- **Stop continuation** — a Stop hook returning `{"decision": "block",
  "reason": "<text>"}` forces a continuation turn with the reason as input;
  the next Stop carries `stop_hook_active: true` (loop guard). VERIFIED in
  exec. This is a *native, in-process* stop re-ring — stronger than the
  send-text doorbell (not used in v1; see design NOT-list).
- **Observability bonus** — the TUI *displays* each hook run and its
  injected context in the transcript (`• UserPromptSubmit hook (completed) /
  hook context: [swarm message] …`). Delivery is visible in the pane.
  VERIFIED.

## 3. Delivery (swarm `deliver`)

Maps 1:1. VERIFIED end-to-end in the TUI with the **unmodified**
`bin/swarm deliver` as the UserPromptSubmit hook: a queued message was
injected whole (relation header included), the file moved to `delivered/`
only after the stdout drain, and the agent acted on the content. The
"delivered means delivered" promise holds unchanged: the hook process's
stdout is read by codex; a failed emit leaves the file queued.

The doorbell also works: `herdr pane send-text <pane> "check queue"` +
`Enter` submits reliably in the codex TUI (bracketed paste lands in the
composer; Enter submits; UserPromptSubmit fires). VERIFIED — swarm's
existing `ring_doorbell` rang a codex pane successfully during the live
send. One degradation: codex's composer prompt char is `›`, not `❯`, so
`pane_prompt_line`'s settle/drain detection never matches — the ring falls
through its bounded retries (~4 s extra) and still lands. Adding `›` to the
heuristic restores full settle detection (design names this).

## 4. Restore / resume (swarm `restore`)

- `codex resume <session-id> [prompt]` (interactive) and `codex exec resume
  <session-id>` both restore **full session memory** (the model recalled
  turn-1 facts). VERIFIED both.
- `SessionStart` hook fires on resume with `source: "resume"` and the same
  `session_id`; `additionalContext` output injects (the restore payload —
  task + journal tail — maps unchanged). VERIFIED: unmodified `bin/swarm
  restore` ran as the SessionStart hook.
- Session rollouts live under `$CODEX_HOME/sessions/…/rollout-<ts>-<id>.jsonl`;
  `transcript_path` in every hook payload points there. VERIFIED.
- Compaction: `auto_compaction` is stable/on; `PreCompact`/`PostCompact`
  hook events exist, and SessionStart's documented sources include
  `compact`. DOCUMENTED — not exercised live (would need a full context).
- The session id is capturable at birth: the SessionStart hook payload
  carries it (swarm can record it for later `codex resume`). VERIFIED
  (payload observed); recording it is a design item.

## 5. Events (swarm `event`)

- **Stop** — fires at end of every turn, in exec and TUI. Payload carries
  `last_assistant_message` directly. The unmodified `bin/swarm event stop`
  ran and wrote the event fact; only `last_words` came out empty, because
  it parses *Claude's* transcript format and codex's rollout format
  differs. Using the payload field instead is a two-line change. VERIFIED.
- **Notification** — **no such hook event exists in codex.** The closest
  natives: the `PermissionRequest` hook (fires before approval prompts —
  moot under `-a never`), and the legacy `notify = ["cmd"]` config, which
  invokes a program with one JSON arg on `agent-turn-complete`
  (`thread-id`, `turn-id`, `cwd`, `input-messages`,
  `last-assistant-message`). VERIFIED (payload captured). `notify` is
  redundant next to the Stop hook for swarm's purposes.

## 6. Identity, isolation, and the trust prompt

- **The TUI blocks on a trust prompt** ("Do you trust the contents of this
  directory?") when the cwd is not in the user's trusted-projects list.
  VERIFIED. A `-c 'projects."<path>".trust_level="trusted"'` override does
  **not** suppress it. VERIFIED (prompt still appeared).
- **Per-agent `CODEX_HOME` solves it cleanly.** VERIFIED: a scratch dir
  with (a) `config.toml` containing `[projects."<cwd>"] trust_level =
  "trusted"` plus the `[[hooks.*]]` tables, and (b) `auth.json`
  **symlinked** from `~/.codex/auth.json`, launched as
  `CODEX_HOME=<dir> codex …` — no trust prompt, auth works, model runs.
  Side effect: sessions/history/memories are per-agent (arguably a feature).
  Minor noise: "MCP startup interrupted: codex_apps" warning at launch
  (harmless; disable via config if desired).
- **Codex writes trust state itself**: `codex exec` silently appended the
  probe cwd to `~/.codex/config.toml` as trusted, and answering the TUI
  prompt did the same. With per-agent CODEX_HOME this lands in the agent's
  own file, not the user's. VERIFIED (I removed the two probe entries from
  the user file afterward; backup kept).

## 7. Sandbox and approvals

- Modes: `read-only`, `workspace-write`, `danger-full-access`; approvals:
  `untrusted`, `on-request`, `never` (+ deprecated `on-failure`).
  DOCUMENTED (help) / VERIFIED for the combination that matters:
  **`-s workspace-write -a never`** ran shell commands unprompted, and the
  macOS seatbelt in workspace-write includes **`/tmp` and `$TMPDIR`**
  (banner: `sandbox: workspace-write [workdir, /tmp, $TMPDIR]`).
- A codex agent in workspace-write **can run the swarm CLI**: it executed
  `bin/swarm send operator …` from inside the sandbox, which wrote a queue
  file under `SWARM_DIR` (in /tmp for the probe). VERIFIED. **SUSPECT for
  production**: if `SWARM_DIR` is the repo's `.swarm/` and the agent's cwd
  is that repo, writes are in-workspace and fine; if an agent's cwd is
  *outside* the swarm repo, `swarm send`'s queue write and journal appends
  would be blocked by the sandbox → launch such agents with
  `--add-dir <SWARM_DIR>` (flag exists, DOCUMENTED; not live-tested).
- `ring_doorbell` from *outside* codex (herdr) is unaffected by the sandbox.

## 8. Does a real codex agent follow briefed duties? Yes.

The gold-standard probe: a real codex TUI agent (`gpt-5.5`,
workspace-write, `-a never`), hooks wired to the **unmodified** `bin/swarm`
verbs, sandbox `SWARM_DIR`, and a swarm-style brief (journal duties, report
via `swarm send operator`, then a task). VERIFIED, all unprompted:

1. Read its journal before acting; wrote the artifact (`poem.txt`).
2. Appended a correct, timestamped journal entry **in the right form**
   before reporting, and again after the second turn.
3. Ran `swarm send operator "Completed: …"` — the report landed in the
   operator's queue.
4. On live delivery (a real `swarm send duties-probe …` from outside): the
   doorbell rang, the message injected whole with its relation header, the
   agent executed the instruction, journaled it, and reported back.
   `delivered/` showed the consumed claim.

## 9. Caveats that belong in the operator's head

- **OpenAI's safety layer can flag a session mid-flight.** Two probe
  sessions were flagged ("possible cybersecurity risk" — my prompts
  contained "secret token" phrasing) and the flagged session then refused
  further turns, including after resume. For swarm: a codex agent can be
  soft-killed by a false-positive flag; the queue and journal survive, the
  session may not. VERIFIED (happened twice).
- **Model availability is account-dependent** (§1); `spawn --model` for a
  codex agent can fail at first turn, visibly in the pane.
- The `--dangerously-bypass-hook-trust` warning prints in the pane every
  launch (cosmetic).
- `last_words` in `swarm ps` is empty for codex agents until `event stop`
  learns to prefer the payload's `last_assistant_message` (two lines).
- Codex TUI shows tips/usage-limit banners in the transcript; pane reads
  should tolerate noise. VERIFIED (observed).

## 10. Probe log (reproduce any claim)

Sandbox: `/tmp/codex-scout-sandbox` (left in place as evidence; scratch
herdr tabs w4:t36–t39 created and closed). Hook logger: `hooklog.sh`
(logs stdin JSON per event + `SWARM_*` env, emits sentinel
`additionalContext` for UserPromptSubmit/SessionStart).

1. **exec + hooks + env + notify** — `codex exec --ignore-user-config
   --skip-git-repo-check --dangerously-bypass-hook-trust -s workspace-write
   -c 'hooks.UserPromptSubmit=[{matcher="",hooks=[{type="command",command="/tmp/codex-scout-sandbox/hooklog.sh user_prompt_submit"}]}]'
   -c 'hooks.SessionStart=[…]' -c 'hooks.Stop=[…]'
   -c 'notify=["/tmp/codex-scout-sandbox/notifylog.sh"]'
   '…echo marker:$SWARM_AGENT_ID… repeat the token…'` → marker echoed,
   token echoed, 3 hook payloads + notify JSON captured (§1–§5).
2. **Stop block** — same shape, Stop hook = `stopblock.sh` (blocks once
   with `BANANA-99` instruction) → continuation obeyed;
   `stop_hook_active=false` then `true` (§2).
3. **exec resume** — `codex exec resume <sid> …` → memory retained;
   SessionStart `source: "resume"` (§4).
4. **TUI launch** — herdr tab, `codex --dangerously-bypass-hook-trust
   --no-alt-screen -s workspace-write -a never "<task>"` → trust prompt
   (fresh dir), then auto-submit, hooks fired and displayed, env reached
   shell; send-text + Enter submitted a follow-up (§1–§3, §6).
5. **Trust override attempt** — same launch + `-c
   'projects."<dir>".trust_level="trusted"'` in a fresh dir → prompt still
   appeared (§6).
6. **CODEX_HOME isolation** — scratch `CODEX_HOME` with `config.toml`
   (trust + hooks) and symlinked `auth.json` → no prompt, auth OK (§6).
7. **Interactive resume** — `codex resume <sid> …` in the pane → transcript
   replayed, SessionStart `source: "resume"` (§4).
8. **Duties probe** — per-agent CODEX_HOME, hooks =
   `/Users/vadrsa/git/swarm/bin/swarm deliver` / `event stop` / `restore`,
   sandbox SWARM_DIR seeded with agent record + journal tombstone; brief as
   in §8; live `swarm send duties-probe` from outside (§3, §5, §8).
9. **Size** — hook emitting 7,830-char context with start/end sentinels →
   model reported both (§2).

Cleanup performed: probe trust entries removed from `~/.codex/config.toml`
(codex wrote them, not me; pre-cleanup backup in session scratchpad); all
scratch tabs closed; `~/.codex/config.toml` otherwise untouched throughout
(`--ignore-user-config`, `-c` overrides, or per-agent CODEX_HOME only).
