# FLEET — non-Claude models as leaf agents

**Author:** `fleet-scout`, design researcher. Writes no product code, changes
nothing; probes read-only and designs. Reports to the operator.
**Written at** `main@aa6063d`, 2026-07-11.

**Evidence discipline:** claims are **VERIFIED** (I ran the command / read the
line — quoted), **DOCUMENTED** (a named source says so), or **REASONED** (my
argument, with a falsifier where it decides something). Inputs read in full:
`swarm world`, `bin/swarm` (spawn/deliver/event/restore/close), `SIMPLEST.md`,
the archived codex work (`docs/design/archive/{CODEX-CAPABILITIES,CODEX-DESIGN,
HARNESS}.md`). Three read-only scouts produced the model-access, graveyard, and
opencode evidence cited inline; their probes ran on THIS machine.

---

## 1. THE RECOMMENDATION (up front, with the choice made visible)

Add Chinese models to the fleet as leaves by **changing only the launcher body** —
the one place swarm is coupled to Claude (§2). Two launcher bodies are worth
shipping, and the honest recommendation is to build them in this order, because
they cost different amounts of *new liveness machinery*:

- **First, the thin runner (simplest, and it is most leaves).** For a one-shot
  leaf — "read X, produce a summary to a file" — the launcher runs a ~5-line
  `curl | jq` against the model's `/v1/chat/completions` and exits (§3B). Here
  "done" is unambiguous: **the process exited and the artifact file exists.** No
  session-idle ambiguity, no plugin, no watchdog protocol. Most of §5's cost
  simply does not arise. This is the cheapest path to a *correct* leaf.

- **Then opencode, for leaves that need tool-use / file-editing / multi-step
  work** — the operator's primary track, and it earns that when the leaf is a
  small *agent*, not a single completion. opencode is installed here (v1.17.13),
  already holds DeepSeek and GLM keys, already lists those models, and its plugin
  API runs arbitrary shell on a session event, so `swarm send <parent>` wires
  itself (§3A). The price of that power is real and lives in §5: because
  `session.idle` is not "task complete," an opencode leaf needs a **done-signal +
  parent watchdog** — a small liveness protocol swarm does not have today.

**The choice to make visible to the operator:** a leaf that is one completion is
cheaper as the thin runner; a leaf that must use tools across turns is worth
opencode's plugin *and its §5 cost*. Do not pick opencode for a job the thin
runner does — you would build §5's protocol to solve a problem (ambiguous "done")
that the thin runner does not have. Both share the launcher-override; the
divergence is entirely in the done-signal.

The parent-drives-the-API-no-pane shape (§3C) is a third option that removes the
pane — the one thing the graveyard insisted a leaf keep — so it is not
recommended except for trusted high-volume one-shots where observability
genuinely does not matter.

**The pipe is proven, at zero cost:** `opencode run "Reply with exactly the word:
PONG" -m opencode/deepseek-v4-flash-free --pure` returns `PONG` and exits — a
Chinese model, full task→output→exit, no user key touched (VERIFIED, §8). The
first real leaf is that command (or its `curl|jq` twin) wrapped in the spawn
machinery.

---

## 2. WHAT A LEAF CAN SHED, AND WHAT IT CANNOT

The starting insight — a leaf needs almost none of the Claude-Code hook surface
— is **confirmed**, and from two directions.

**From the code (VERIFIED):** spawn writes `settings/<name>.json` with four
hooks — `UserPromptSubmit→deliver`, `Stop→event`, `Notification→event`,
`SessionStart→restore` (`bin/swarm:890-894`). Every one of those hook handlers
is `try/except → sys.exit(0)`, bulletproof and fail-safe (`cmd_deliver`
`:685`, `cmd_event` `:699`, `cmd_restore` `:737`). They are **Claude-Code
settings hooks**: if a non-Claude process runs in the pane, they simply never
fire. Nothing breaks — the machinery sits unused. **The launcher (`:823-835`,
hardcoded `claude --settings … "$PROMPT"`) is therefore the only point where
swarm is coupled to Claude.** A leaf is exactly a different launcher body.

**From the graveyard (VERIFIED by the graveyard scout):** the archived codex
integration already retreated to leaf-only for the non-Claude side — *"`swarm
spawn` from inside codex is unverified and fails hard … Spawn's load-bearing
call is `herdr tab create`, a unix-socket round-trip"* (HARNESS §1b). Leaf-only
is not a compromise this design invents; it is the safe subset the prior work
arrived at independently.

| Claude-Code surface | Does a leaf need it? | Why |
|---|---|---|
| `deliver` (one msg/turn injection) | **No** | A leaf receives its task at launch and reports once. No mid-session inbound queue to drain. |
| `Notification` event | **No** | Witnesses an agent waiting on approval. A leaf under a no-wait model never waits. (Codex had no such event anyway — CAP §5.) |
| `restore` / compaction | **No, if the leaf fits one context** | Re-injects task+journal after compaction. A one-task leaf that never compacts never fires it. Also sheds the foreign-transcript-format parse that broke codex's `last_words` (CAP §5). |
| doorbell / stop re-ring | **No** | Exists only to re-ring a pane so a *queued* message injects. No inbound queue → never used. Sheds codex's `›`-vs-`❯` prompt-match battle (DESIGN §2). |
| spawn / `herdr tab create` from inside the sandbox | **No — and this is the point** | A leaf never spawns. The graveyard's single hardest, unverified, fails-hard battle does not exist for a leaf. |

**The irreducible minimum a leaf still needs** (grounded in `cmd_spawn`
`:868-956`):

1. **A journal tombstone.** `claim_name` (`:761`) creates
   `journal/<name>.md` with `O_CREAT|O_EXCL` — this *is* the name claim. Without
   it there is no `ps` entry, no `send <name>` target, no successor anchor. A
   leaf still burns its name.
2. **A pane.** *"One tab per agent: the pane is what makes the society
   observable"* (`:905`). The graveyard explicitly refused headless codex
   agents *because* "a headless agent has no pane" (DESIGN §7). **Do not run
   leaves headless** — their first-turn failures and model refusals are only
   visible in-pane. `opencode run` streams to the pane, so this holds for free.
3. **Task in, report out.** The task-file → launcher path (`:832`, avoids argv
   escaping) delivers the one task; the report is the one message plane a leaf
   cannot skip. It needs the pane env `SWARM_DIR` / `SWARM_AGENT_ID` (`:907`),
   and opencode's `--dir` (run-directory) pointing at `SWARM_DIR` if cwd is
   outside the repo (opencode has no `--add-dir`; `--dir` is the real flag,
   VERIFIED in `run --help`).
4. **A launcher status/readiness signal** (`write_launcher` `:814`) so a started
   leaf is told from a dead one by a fired signal, not a screen-scrape.

Note what is **not** on this list: the four Claude-Code hooks. A leaf sheds all
four.

---

## 3. THE THREE EXECUTION SURFACES

Ranked by *fit to the leaf's job*, not by capability. The thin runner wins the
common one-shot case; opencode wins the tool-using case and is the operator's
primary track for that reason. The single fact that splits them: what "done"
means, and therefore whether you must build §5.

### (A) opencode as the leaf runtime — for tool-using leaves (operator's primary)

opencode is a single 130 MB Bun binary at `/Users/vadrsa/.opencode/bin/opencode`,
**v1.17.13** (VERIFIED). Every leaf obligation maps to something opencode
already does:

| Leaf need | opencode gives it | Evidence |
|---|---|---|
| Receive one task | `opencode run "<task>" -m <model> --agent <name>` | VERIFIED |
| Produce inspectable artifact in a pane | `run` streams to the pane; `--format json` for structured capture; its tools write files to cwd | VERIFIED (run), DOCUMENTED (flags) |
| Report once to parent | plugin `event` hook on `session.idle` runs `swarm send <parent>` via the Bun `$` shell | VERIFIED — a plugin doing this exact pattern is already installed (§below) |
| Drive Chinese models | native registry + custom `baseURL` providers; **DeepSeek & GLM keys already on this box** | VERIFIED (`auth.json`) |
| Enforce leaf-only | `tool.execute.before` denies any spawn tool; or simply never expose one | REASONED from VERIFIED hook signature |

**The report wires itself (the crux the operator predicted).** An installed
plugin `~/.config/opencode/plugins/bridgespace-notify.js` already runs a shell
command on a lifecycle event (VERIFIED):

```js
export const BridgeSpaceNotifyPlugin = async ({ $ }) => ({
  event: async ({ event }) => {
    if (event?.type === "session.idle") {
      await $`node ${helper} --agent opencode --event stop`.quiet();
    }
  },
});
```

Swap the body for `swarm send <parent> --stdin < artifact` and opencode reports
on completion — **no Claude-Code Stop hook.** The Bun `$` shell is handed to every
plugin: arbitrary CLI execution is a documented, in-use capability, not a hack.
**The double edge, stated honestly:** this same plugin is the source of §5's two
biggest risks — `session.idle` fires on *every* idle, not only completion, so the
report can fire early or mid-task, and a crash before idle fires nothing. The
plugin is what makes opencode attractive *and* what makes it need the §5 liveness
protocol. The thin runner (B) has neither the plugin nor those risks.

**Chinese models are a config-only add.** opencode is multi-provider over a
models.dev-style registry on the Vercel AI SDK. `opencode models` already lists
`deepseek/deepseek-chat`, `deepseek/deepseek-reasoner`,
`opencode/deepseek-v4-flash-free`, and via OpenRouter `moonshotai/kimi-k2*`,
`qwen/qwen3-coder`, etc. (VERIFIED). Any other OpenAI-compatible endpoint is
config, not code (DOCUMENTED, `ProviderConfig` in the SDK types):

```json
{ "provider": { "deepseek": {
    "npm": "@ai-sdk/openai-compatible",
    "options": { "baseURL": "https://api.deepseek.com/v1",
                 "apiKey": "{env:DEEPSEEK_API_KEY}" },
    "models": { "deepseek-chat": { "name": "DeepSeek Chat" } } } } }
```

### (B) Thin OpenAI-compatible runner — for one-shot leaves (simplest, most leaves)

Every target (DeepSeek, Qwen, Kimi, GLM, MiniMax) exposes OpenAI-format
`POST /v1/chat/completions` (DOCUMENTED per model). A **non-tool** leaf is ~5
lines (REASONED, grounded in the documented endpoint shape):

```sh
curl -s "$BASE_URL/chat/completions" -H "Authorization: Bearer $KEY" \
  -H 'Content-Type: application/json' \
  -d "$(jq -n --arg m "$MODEL" --arg p "$TASK" \
        '{model:$m,messages:[{role:"user",content:$p}]}')" \
  | jq -r '.choices[0].message.content' > artifact.txt
```

Swap `BASE_URL/MODEL/KEY` per vendor. Streams to the pane like anything else, so
it is just as observable as (A). **Why this is the pick for the common case, not
a mere fallback:** its "done" is unambiguous — the process exits and
`artifact.txt` exists — so §5's done-signal problem *does not arise* and there is
no plugin to fire early. The parent reads the file (or the exit code); no
liveness protocol to build. Its limits are real and bound its use: one completion,
not a tool-using multi-step agent, and you supply `BASE_URL/KEY` yourself rather
than reuse opencode's configured providers. **The trade in one line:** the thin
runner is cheaper to make *correct* (no §5); opencode is worth its §5 cost only
when the leaf genuinely needs to use tools across turns. Pick by the leaf's job.

### (C) Parent drives the API, no pane — NOT recommended here

The brief asks whether the parent can own the leaf's I/O — call the model's API
itself, poll the artifact — so the model never speaks swarm's CLI. It **can**
(it's just the runner of (B) executed inside the parent's own turn, writing a
file the parent then judges), and it removes even the tombstone and pane. But it
**trades away the pane** — the one thing the graveyard insisted a leaf keep
(DESIGN §7) — so you lose "watch it work" and the in-pane visibility of a
refusal/soft-kill. Keep it as a known option for a trivial, trusted, high-volume
one-shot where observability genuinely doesn't matter; do not make it the default.

---

## 4. THE LEAF CONTRACT IN REAL `bin/swarm` TERMS

A leaf is spawned by the **same** `cmd_spawn` path (`:845`), with two deltas:

1. **A launcher-override.** Today `write_launcher` (`:814`) hardcodes `claude`.
   Add a spawn flag — e.g. `swarm spawn <name> "<task>" --exec opencode` (or a
   per-model alias) — that selects the launcher body: `opencode run "$PROMPT" -m
   <model> --agent <name>` instead of `claude … "$PROMPT"`. Everything else in
   `write_launcher` (status file, `exec bash` to keep the pane inspectable) is
   unchanged. **Concept cost: one flag, one alternate launcher body.**
2. **A done-signal + report.** The leaf's opencode config carries the
   ~30-line plugin that, on completion (§5's done-signal, not bare
   `session.idle`), runs `swarm send <parent>` with the artifact (path or body).

   **The parent-identity wiring, specified (a real gap in the naive design):**
   spawn sets only `SWARM_AGENT_ID=<name>` in the pane env (`:907`) — that is the
   leaf's *own* name, **not its parent's**. The parent lives in
   `agents/<name>.json` (`:921`) but no env var carries it into the pane. So a
   report plugin cannot know whom to send to without either (a) reading
   `$SWARM_DIR/agents/$SWARM_AGENT_ID.json` and parsing `.parent` itself, or
   (b) spawn injecting a `SWARM_PARENT=<parent>` env var alongside
   `SWARM_AGENT_ID` at `:907`. **Recommend (b):** one added env var at one line,
   and the plugin becomes a trivial `swarm send "$SWARM_PARENT" --stdin <
   artifact`. This is counted in §9 — the leaf costs *one flag + one env var*,
   not "one flag."

**Identity.** The leaf runs under its spawned `<name>` in its pane, with
`SWARM_DIR`/`SWARM_AGENT_ID` in the pane env (`:907`) — the same identity every
agent gets. It does *not* need to understand the 40-line Claude spawn header
(`spawn_header` `:771`): that text is injected as the task prefix and a
non-Claude model can't act on it. For a leaf, the launcher should pass a **clean
task** (the operator's actual instruction, minus the swarm-duties preamble) —
the report wiring lives in the plugin, not in the model's understanding.

**How the report gets back as a judgeable artifact.** Two routes, prefer the
first: (a) the plugin runs `swarm send <parent> --stdin < <artifact-file>` on
completion — the artifact lands in the parent's queue as a normal one-turn
message; or (b) the parent polls a known artifact path in the leaf's cwd (works
even if the plugin's send fails — belt and suspenders). The pane is ground truth
throughout: the parent can read it directly at any time.

---

## 5. THE REAL DELIVERABLE: A LEAF-LIVENESS PROTOCOL (opencode path)

This is the honest cost of the opencode path, and it is **not** trivial — it is a
small distributed liveness protocol between a plugin and a parent-side watchdog,
neither of which swarm has today. The thin-runner path (§3B) mostly avoids it
(its "done" is process-exit + file-exists); this section is the price of
opencode's tool-use power. Both independent scouts converged on it, from opposite
ends:

- **opencode wall:** `session.idle` fires on idle, not specifically on "task
  complete" (DOCUMENTED — the installed `bridgespace-notify.js` fires on
  `session.idle` unconditionally; REASONED that a leaf pausing/idling mid-task
  would therefore trigger it — this is a behavioral prediction, to be measured by
  falsifier 2, not a run I made). And a crash/kill *before* `session.idle` fires
  **no report at all**.
- **Graveyard trap (VERIFIED twice, CAP §9):** a provider's safety layer can
  flag a session *mid-flight*; *"the flagged session then refuses further turns"*
  — and HARNESS §1b spells out the leaf consequence: *"for a leaf that is a lost
  worker."* The launcher's `"launching"` status already reads as *started*
  (`:935`) and spawn stops watching — a leaf soft-killed on turn one passes the
  readiness check and then **dies mute**.

So the design must treat **"leaf launched"** and **"leaf produced its artifact"**
as two distinct facts, and make a *missing* report a first-class, parent-noticed
state. Concretely:

- **Done-signal convention:** the leaf's completion is the artifact file
  existing (or a sentinel), *not* `session.idle` alone. The report plugin fires
  `swarm send` only when the artifact is present; an idle with no artifact is a
  non-event (or a distinct "idle, no artifact yet" note).
- **Watchdog:** the *parent* owns a timeout on the pane. If no report and no
  artifact arrive within the budget, the parent reads the pane (ground truth),
  journals the banner text, and treats the leaf as failed. **A refusal IS a
  result** (HARNESS §2f) — journal it, never silently retry, never rephrase to
  dodge a filter (rephrasing quietly changes the experiment).

This is the honest concept delta, and §9 counts it. It is **not** a new swarm
primitive, but it *is* real build work: a report plugin that distinguishes
"idle, no artifact" from "done," a parent-side watchdog (a timeout loop + a pane
read + banner-journaling) that `bin/swarm` does not have today, and the
"refusal is a result, never retry" discipline. An afternoon builds the happy
path; falsifiers 1–3 (§10) are exactly the unhappy paths that take the real time.
Pretending a spawned leaf will always report is the exact mistake the graveyard
already made — do not price it at zero.

---

## 6. ACCESS & COST (read-only discovery, this machine)

**Reachable TODAY (VERIFIED, `~/.local/share/opencode/auth.json`, values
redacted):** opencode already has **`deepseek`** (`type: api`, key set) and
**`zai-coding-plan`** (z.ai / GLM, key set). Plus the **free** gateway model
`opencode/deepseek-v4-flash-free`, which needs no user key at all. So a DeepSeek
or GLM leaf is reachable **right now** through opencode.

**Blocked today:** raw-env access to any Chinese vendor — `env` holds only
`OPENAI_API_KEY` (len 164, unvalidated, possibly a gateway key; no
`OPENAI_BASE_URL` override) and `LOCALSTACK_API_KEY` (VERIFIED). No Qwen /
Moonshot / MiniMax key anywhere. **Local weights: none live** — Ollama not
installed, `:11434` dead, `~/.ollama` empty (VERIFIED). The `~/secret-deepseek.
yaml` / `~/modelconfig-deepseek.yaml` files are **inert kagent k8s manifests**
(the modelconfig actually points at Ollama/llama3.2) — a red herring, not
credentials (VERIFIED).

**Cost (DOCUMENTED, July 2026, moves — re-verify at build):** per 1M tokens
in/out, vs a Claude Opus anchor of ~$15/$75:

| Model | in / out | Notes |
|---|---|---|
| DeepSeek V4 Flash | ~$0.14 / $0.28 | cheapest-and-strong; ~50–100× under Opus |
| MiniMax M2 | ~$0.26 / $1.02 | lightest active MoE |
| GLM-4.6 | ~$0.43 / $1.74 | keyed here already |
| Qwen Plus | ~$0.40 / $1.60 | Qwen family most local-friendly |
| Kimi K2.6 | ~$0.95 / $4.00 | official `kimi-code` CLI exists |

Only **Qwen** (`@qwen-code`) and **Kimi** (`kimi-code`) ship official terminal
CLIs (DOCUMENTED); DeepSeek/GLM/MiniMax do not — irrelevant for a leaf, which
wants the endpoint, not a coding agent.

---

## 7. JUDGMENT & SAFETY

- **Judged like everything else — by artifact.** A leaf is read, not trusted.
  It need not honor briefed duties (journaling, falsifiers); it does one thing
  and its output is the whole judgeable surface. The parent journals *about* the
  leaf.
- **Leaf-only is enforceable, cheaply.** opencode's `tool.execute.before` can
  deny any spawn/delegate tool; simpler still, never expose one. A leaf that
  cannot be trusted to run swarm commands is fine — the plugin (swarm-authored,
  trusted) owns the `swarm send`, not the model.
- **Data egress (flag, not moralize):** a Chinese-model leaf sends its task
  tokens to that vendor's API (DeepSeek, z.ai, etc.). Where the tokens go is a
  per-task call — do not route sensitive context to a leaf whose provider you
  wouldn't hand that context to. One sentence in the leaf's brief; the operator
  decides.
- **The soft-kill is a safety-relevant failure, not just a bug** (§5): scrub
  leaf briefs of provider-tripwire vocabulary before launch — the graveyard's
  two kills were phrasing-triggered.

---

## 8. THE SMALLEST COSTED FIRST STEP

The pipe is **run and confirmed**; the leaf *wiring around it* is designed, not
yet built:

1. **The pipe works (VERIFIED, $0 — actually executed by the opencode scout):**
   `opencode run "Reply with exactly the word: PONG" -m
   opencode/deepseek-v4-flash-free --pure` → `PONG`, exited. A Chinese model, full
   task→output→exit loop, no user key touched. (The steps below — launcher-override,
   plugin, watchdog — are designed here, not yet run; build them as follows.)
2. **First real leaf — the thin runner, because it proves the contract with no
   §5 protocol (to build, ~an afternoon of the *happy path*):**
   - Add the `--exec`/launcher-override flag to `write_launcher` and inject
     `SWARM_PARENT` at `:907` (§4, §9).
   - Launcher body = the ~5-line `curl|jq` (§3B) against
     `opencode/deepseek-v4-flash-free`'s endpoint (or `deepseek-chat` once keyed),
     writing `artifact.txt` and exiting.
   - One leaf task: "read file X, produce a 10-line summary to `artifact.txt`."
   - Report: the parent polls the cwd for `artifact.txt` (done = file exists +
     process exited). No plugin, no watchdog protocol yet — this is exactly why
     the thin runner is the cheapest *correct* first leaf.
   - **Only then, the opencode leaf** (when you want a tool-using leaf): swap the
     launcher body to `opencode run "$PROMPT" -m deepseek/deepseek-chat --agent
     <name>`, add the report plugin (on completion, `swarm send "$SWARM_PARENT"
     --stdin < artifact`), and build §5's done-signal + watchdog. This is the
     step that costs more than an afternoon — budget it as §5, not as this line.
3. **Cost to prove the *paid* path:** one DeepSeek `deepseek-chat` run of a
   small task ≈ a few thousand tokens ≈ **well under $0.01** at $0.14/$0.28 per
   1M. The free gateway model proves the mechanism at $0 first; flip `-m` to the
   keyed `deepseek-chat` to prove the real endpoint.

**What this proves:** the launcher-override, the pane-observable non-Claude run,
the plugin-driven report, and the done-signal/watchdog — the entire leaf
contract — for the price of one afternoon and a fraction of a cent.

---

## 9. CONCEPT COST (counted honestly, nothing laundered off-ledger)

**Shared by both launcher paths:**
- **New swarm concepts: 0.** The leaf reuses spawn, pane, tombstone, and the
  `send` report path unchanged. The Claude-Code hooks are shed (they no-op for a
  non-Claude process), not replaced.
- **New swarm mechanics (ride the verbs): one flag + one env var** —
  `spawn --exec` selecting the launcher body (mirrors `--model`/`--cwd`, SIMPLEST
  §3), and `SWARM_PARENT` injected in the pane env at `:907` so the report knows
  its recipient (§4). Not "one flag" — one flag *and* one env var.

**The thin-runner path (§3B) adds beyond that:** one small runner file. Its
"done" is process-exit + file-exists, so it needs **no liveness protocol.** This
is the cheap-and-correct path.

**The opencode path (§3A) adds beyond the shared cost — and this is the real
bill, on the ledger, not off it:** an opencode config + report plugin, **plus the
§5 leaf-liveness protocol** — a done-signal convention, a parent-side watchdog
(timeout loop + pane read + banner-journaling) that `bin/swarm` does not have
today, and refusal-handling discipline. It is not a new swarm *primitive*, but it
is genuine build work and the honest reason to choose the thin runner when the
leaf's job is a single completion. Do not read "no new primitive" as "no cost."

**The parent-drives-API shape (§3C)** adds nothing but a convention — and removes
the pane.

---

## 10. FALSIFIERS (with collectors)

Committed before any build:

1. **The report can't leave the pane without the model's cooperation.** If
   `opencode run` proves unable to emit an artifact a *parent* can read except by
   the leaf itself running commands (output only ever streams to the pane, never
   to a file), then "parent owns I/O" fails and only shape (C) is trustable —
   opencode-primary weakens. *Collector:* build step 2 — does `--format json` /
   file-writing tools / a polled cwd file actually yield a parent-readable
   artifact.
2. **`session.idle` fires so noisily the report is unusable.** If, in a real
   leaf run, `session.idle` fires many times mid-task and the done-signal
   convention can't cleanly gate it, the plugin-report path is fragile and the
   parent-poll (route b, §4) must carry the load. *Collector:* the first real
   leaf's plugin logs — count idle fires vs true completions.
3. **The soft-kill is silent even in-pane.** If a provider mid-flight refusal
   leaves *nothing* in the pane (no banner) and produces no artifact, the
   watchdog's "read the pane" has nothing to read and the only signal is a
   timeout. *Collector:* deliberately trip a refusal (a benign but filtered
   prompt) and read the pane.
4. **opencode's keyed providers aren't actually usable.** The `auth.json` shows
   `deepseek` and `zai-coding-plan` keys, but I did not spend a token to confirm
   they authorize a live call (cost-flagged, held). If a keyed run 401s, "keyed
   today" is false and step 2 needs a fresh key first. *Collector:* the one
   sub-cent `deepseek-chat` run in step 8.3.

---

## 11. NOT-LIST (what this design deliberately does not do)

- **Does not make non-Claude models full nodes.** No spawn, no children, no
  tree participation — the operator conceded leaf-only and the graveyard proved
  it the safe subset. Not reopened.
- **Does not wire the four Claude-Code hooks for a leaf.** They no-op; wiring
  them would be ceremony (SIMPLEST §4: a schema nobody reads).
- **Does not run leaves headless.** The pane is non-negotiable (§2) — the one
  thing the graveyard insisted a leaf keep.
- **Does not fork or patch opencode.** Everything rides its documented plugin +
  config surface. If that surface ever can't carry the report, fall back to (B).
- **Does not add a status taxonomy for leaves.** A leaf is judged by artifact
  like everything else (§7); "done" is the artifact existing, read by the
  parent — not a stored state (SIMPLEST §4).
- **Does not route sensitive context to a foreign provider by default.** Egress
  is a per-task operator call (§7), flagged, not automated.
