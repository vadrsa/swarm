# What Claude Code's harness gives swarm for free

Inventory only — no recommendation. One row per capability. This is meant to be
read as the strongest case AGAINST "swarm should drive provider APIs directly,"
so it is deliberately unfair to a custom loop: every load-bearing free thing is
named, and rebuild cost is graded honestly (TRIVIAL / REAL / HARD).

"HARD" = the thing IS Claude Code's/Anthropic's core product competency —
years of dedicated engineering, not a gap a contractor closes in a sprint.

---

## 1. Agentic loop (tool-call orchestration, retries, error recovery)

**What it is:** the read-plan-act-observe loop that turns a model's tool_use
blocks into executed actions, feeds results back, retries transient failures
(rate limits, network blips, malformed tool calls), and knows when to stop.

**Evidence it's load-bearing for THIS swarm:** every agent in `.swarm/journal/*`
IS a Claude Code session — the loop is the substrate every artifact in this
repo was produced inside. It's invisible precisely because it never breaks;
the one place it's visible is what happens *around* it (hooks, restore) —
see rows 4 and 5. No journal entry documents the loop itself misbehaving.

**Rebuild cost: HARD.** This is literally Anthropic's product. A custom loop
needs: tool-call parsing robust to malformed/truncated JSON, retry/backoff
policy tuned against real rate-limit behavior, partial-response handling,
multi-turn tool-result threading, and enough production mileage to find the
edge cases Anthropic has already found. Not a rebuild a contractor scopes in
"days" — it is the thing being bought when you buy Claude Code.

---

## 2. Tool suite (Read/Edit/Write/Bash/Grep/Glob + safety semantics)

**What it is:** line-precise `Edit` (exact-match old_string/new_string,
`replace_all`), `Read` with pagination/offset for huge files, `Bash` with a
persistent working-directory shell, `Grep`/`Glob` as fast non-agentic search
primitives, plus tool-specific safety rules (e.g. Edit requires a prior Read;
Write refuses to blind-overwrite).

**Evidence it's load-bearing for THIS swarm:** every artifact under
`docs/audit/`, `docs/design/`, and every code change referenced in
`.swarm/journal/*` (e.g. spawn-repair's herdr-slash-shim commit, ps-model's
`render_ps` diff reviewed line-by-line in `operator.md`) was produced via these
tools. `operator.md`'s PR #84 review explicitly leans on line-precision
("+61 bin/swarm all inside render_ps... whitespace/control/tree-glyphs
dropped") — that kind of surgical diff-reading assumes Edit's match semantics.

**Rebuild cost: REAL.** The individual tools are not exotic — a file-read,
a grep wrapper, a shell-exec are each an afternoon. What's REAL, not TRIVIAL,
is the *safety semantics as a coherent set*: uniqueness-checked edits that
fail loud instead of silently mismatching, sandboxed Bash with timeout/
background-job handling, and the accumulated edge-case hardening (symlinks,
permissions, huge-file truncation) that turns "a script that edits files"
into something you can hand to an autonomous agent unsupervised. Days-to-weeks
per tool, done right; longer if it must match Claude Code's specific
guarantees (e.g. Edit's "fails if old_string isn't unique" contract that
`operator.md` PR review implicitly depends on).

---

## 3. Permission system (modes, allowlists, dialogs)

**What it is:** per-tool prompts ("Do you want to proceed?"), allow/deny
lists in settings, auto-mode classifiers, and (per the hooks doc, row 8)
`PreToolUse` hooks that can programmatically `allow`/`deny`/`ask`/`defer`.

**Evidence it's load-bearing for THIS swarm:** `operator.md:306-326` — the
orphan-tab incident: ~90 of 105 leaked herdr tabs were CC sessions wedged on
the **folder-trust prompt**, and a further subset wedged on the
**rate-limit prompt**, because each spawned into a temp dir CC had never
seen. `bin/swarm:695-785` implements `classify_blocked_pane` to detect
exactly these three prompt classes (`trust`/`permission`/`rate-limit`) from
raw pane text, because — per `operator.md:318` — "a session parked on a
trust/permission prompt reports as `idle` in swarm ps AND herdr status —
INVISIBLE." That invisibility bug is independently rediscovered in
`weak-model-delegation-2026-07-13.md` ("a permission-blocked child is scored
as a weak/slow one," `docs/audit/_hc-field.md` §citing `blocked-vis*`).
Separately, `bin/swarm:1072` (`pre_trust_dir`) and the `--trust` spawn flag
exist specifically to pre-approve throwaway sandbox dirs — ratified by the
human explicitly ("I am ok with temp dirs being auto approved in any way,"
`operator.md` ruling on spawn-repair's security flag).

**Rebuild cost: REAL.** The *gate* itself (a y/n prompt before a risky call)
is TRIVIAL. What's REAL: the safety-classifier judgment of what's dangerous
enough to gate (this repo's own `blocked-vis` work shows even Claude Code's
own signal for "blocked" had to be reverse-engineered from pane text before
herdr 0.7.3 exposed `agent_status='blocked'` natively) and a working
allowlist/mode model that survives ~100-agent fleets without either
(a) prompting a human 90 times or (b) silently rubber-stamping destructive
ops. A custom loop starts with neither the classifier nor the modes and has
to invent both from scratch under the same fleet-scale pressure that just
broke swarm's own visibility once already.

---

## 4. Hooks (UserPromptSubmit / Stop / Notification / SessionStart)

**What it is:** lifecycle hook points; per `bin/swarm:1155-1160` swarm wires
all four for every spawned agent:
```
UserPromptSubmit -> deliver          (inject exactly one queued message)
Stop             -> event stop       (record + re-ring doorbell if queue non-empty)
Notification     -> event notification
SessionStart     -> restore          (inject original task + journal tail)
```

**Evidence it's load-bearing for THIS swarm:** this **is** swarm's entire
mailbox and continuity mechanism, not an add-on to it. `bin/swarm:421-436`
(`deliver_once`) injects queued messages via `UserPromptSubmit`'s
`additionalContext` field — every `swarm send` in this tree's history
depends on this. `bin/swarm:928-935` (`cmd_restore`) is the literal restore
hook: `docs/audit/_hc-field.md` §B names it directly, and its table of
2026-07-13 same-day resumes (`trigger-scout`, `hardener`,
`harness-contractor`, `hc-industry`, `model-fit`, `org-review-scout`,
`spawn-repair`, `updater`) is the "~10 agents through a restart" evidence the
task brief anticipated. `field-evidence-2026-07-09.md` §5 separately proves
the mechanism experimentally (deliberate kill+relaunch resumed intent
perfectly) and flags the one open gap: **compaction-source restore
(`source=compact`) remains untested** — "Forcing a real compaction was not
cheaply possible... untestable cheaply today." `field-evidence-2026-07-09.md`
also documents a real defect in the hook's own use: `build_restore` says
"resuming a fresh session" for every non-compact SessionStart *including
first startup*, so 3-of-3 sampled agents wrote a spurious "resumed after
restore" entry at their actual initial spawn — a same-day, first-hand
confound in the mechanism swarm depends on.

**IMPORTANT NUANCE — swarm does NOT use hooks' strongest documented power.**
Per the hooks reference (row 8, DOCUMENTED), Stop hooks CAN force
continuation via exit code 2 or `{"decision":"block"}`. Reading
`bin/swarm:878-910` (`cmd_event`): swarm's Stop handler never emits `block`
or exits 2 — it records the event and, if the queue is non-empty, "rings its
own doorbell" so the NEXT natural turn drains the queue; the code comment
calls this "the ONE UNPROVEN MECHANISM," explicitly a soft nudge that
degrades to "later messages stall until the next natural turn" rather than a
hard gate. So today's swarm uses hooks purely as **observation + soft
re-prompt** points, not as enforcement gates — even though the harness
supports harder enforcement it isn't using.

**Rebuild cost: TRIVIAL for the mechanism itself, REAL for what it silently
buys.** A lifecycle-hook system with 4 named event points and a JSON
stdin/stdout contract is an afternoon to wire in a custom loop — swarm's own
hook shell-outs are ~15 lines each (`h(cmd)` in `bin/swarm`). What's REAL:
Claude Code guarantees these fire at the *right* moments (exactly once per
prompt/stop/session-boundary, ordered, with transcript access) across every
failure mode of its own loop (crash, compaction, rate-limit) — a custom loop
has to invent its own reliable equivalent of "the turn boundary" and "the
context got wiped and this is a fresh window," including the compaction
case swarm has NOT yet been able to test against the real harness.

---

## 5. Session persistence + restore + context compaction

**What it is:** durable session state across process death (crash, machine
restart, `/clear`), automatic summarization when context fills
(compaction), and `SessionStart`'s `source` field distinguishing
`startup`/`resume`/`compact`/`clear`.

**Evidence it's load-bearing for THIS swarm:** `docs/audit/_hc-field.md` §B
is built entirely around a 2026-07-13 machine-restart incident: 118 herdr
tabs total, only 13 recorded live agents kept, and a table of 8+ agents whose
journals show an explicit same-day resume entry (e.g.
`harness-contractor.md:241` "Fresh session (restore hook fired). Journal had
only the spawn entry — no prior work lost"; `model-fit.md:399` "resumed
after restart; verified nothing to redo... Woke to the same task text"). This
is process-level session persistence working as advertised: agents came back
with their task and journal tail intact with zero human re-briefing.
**Compaction specifically is the one sub-case with NO direct positive
evidence in this repo** — `field-evidence-2026-07-09.md` §5 states outright
that forcing real compaction "was not cheaply possible" in-session and marks
`source=compact` restore as **untestable cheaply today; recheck when a real
agent compacts naturally.** So: restore-after-crash/restart is empirically
verified multiple times; restore-after-compaction is assumed by design
(same hook, same `source` field) but not yet independently witnessed here.

**Rebuild cost: HARD.** Durable session state that survives an OS-level
restart mid-tool-call is REAL-to-HARD by itself. Automatic context
compaction — summarizing a long transcript so the model doesn't hit its
context window, in a way that preserves enough continuity for an agent to
resume unsupervised — is a core piece of Claude Code's own engineering
investment (the whole point of the `PreCompact`/`SessionStart{source:compact}`
hook pair). A custom loop driving raw provider APIs gets zero of this: no
persisted transcript format, no compaction algorithm, no crash-safe resume —
building one that's trustworthy for ~10+ unattended agents is not a
side-project.

---

## 6. MCP client support

**What it is:** Claude Code as an MCP *client* — connecting to and calling
tools on external MCP servers (this very session has `bridgememory` and
`bridgemind` MCP servers wired in, visible as `mcp__bridgememory__*` /
`mcp__bridgemind__*` tools).

**Evidence it's load-bearing for THIS swarm:** direct, live, in this
session's own tool list (not a journal citation — the system reminders in
this conversation show both servers connecting and their tool surfaces
becoming available mid-session). `blocked-visibility.md:61+` independently
shows multiple live `bridgememory-mcp/server.cjs` node processes running
across dozens of panes — i.e., MCP connections are a standing, per-pane
resource in this fleet's actual footprint, not a hypothetical.

**Rebuild cost: REAL.** The MCP spec itself (JSON-RPC-ish tool discovery +
invocation) is documented and implementable in days. What's REAL: robust
lifecycle handling of external server processes at fleet scale — the exact
failure mode `codex-audit.md` flags for a *different* harness ("MCP startup
interrupted: codex_apps" warning) is the class of bug a custom client would
have to debug itself, multiplied by however many MCP servers real usage
demands, with no existing client library to lean on other than the MCP SDKs
(which handle the wire protocol, not the "should I retry a wedged server"
policy).

---

## 7. TUI / pane rendering ("the pane is ground truth")

**What it is:** Claude Code's terminal rendering of the live turn —
streaming tool calls, output, and (per herdr 0.7.3) an `agent_status` field
a wrapper can read — inside a herdr pane a human can watch directly.

**Evidence it's load-bearing for THIS swarm:** the swarm design's own
premise, named verbatim in the task brief ("the pane is ground truth"), and
`bin/swarm:1174` comments it explicitly: "One tab per agent: the pane is
what makes the society observable." The orphan-tab incident
(`operator.md:306-326`) is a direct case of a human eyeballing the herdr UI
to catch what `swarm ps` couldn't see (trust/rate-limit-blocked panes
reporting `idle`) — i.e., the raw pane view caught a blind spot in swarm's
own structured status layer. `ps-model-red.md`/`ps-model-red2.md` and the
whole `render_ps` review thread in `operator.md` exist because the
*textual* status summary is a lossy derivative of the pane, and the swarm
team keeps having to reconcile the two.

**Rebuild cost: REAL, with a hard floor.** Streaming a model's raw output to
a terminal is TRIVIAL (any SDK's streaming response piped to stdout). What's
REAL: replicating everything a Claude Code pane shows beyond raw
text — tool-call formatting, diff rendering, permission-prompt UI, spinner/
status states herdr can introspect (`agent_status`) — few of which exist for
free if you're issuing raw provider API calls yourself; you'd be writing
your own terminal renderer for tool calls and, per this fleet's own
experience, *still* need to invent a "trust/rate-limit prompt" visual state
because a bare API loop wouldn't emit interactive prompts at all (there'd be
nothing analogous to hang on) — a different problem, not a solved one.

---

## 8. Prompt caching

**What it is:** automatic prompt-cache-write/read on repeated context
(system prompt, tool defs, conversation prefix) to cut cost/latency,
transparent to the calling code.

**Evidence it's load-bearing for THIS swarm:** weak, indirect only. The one
concrete cache-accounting number in this repo's journals is for a
*different* harness/model: `run-glm-2.md:37` — "151k fresh in + 9.4k out +
4.3M cache-read → ~$0.08 (fresh) to ~$0.27 (w/ cache-read)" for a GLM cell
run via opencode, not Claude Code. No journal entry quantifies Claude Code's
own prompt-cache savings for this swarm specifically (no cost-tracking
artifact was found for Claude-model agents' token bills). Treat this row as
plausible-but-unverified for THIS swarm; the mechanism is real in the
Claude API generally, just not evidenced here.

**Rebuild cost: TRIVIAL to REAL.** Anthropic's API supports prompt caching
directly (`cache_control` breakpoints) — a custom loop calling the API
directly gets the *same* underlying caching if it sets the breakpoints
correctly (TRIVIAL: an afternoon of reading the caching docs). What Claude
Code adds beyond that is doing it *automatically* without the caller having
to reason about breakpoint placement — REAL effort if a custom loop wants
the harness to always place breakpoints optimally rather than the
integrator hand-tuning them per prompt shape.

---

## 9. Model routing / fallback

**What it is:** picking a model, retrying/falling back across model
variants or providers on error/overload, without the calling code managing
it.

**Evidence it's load-bearing for THIS swarm:** no journal entry documents
Claude Code itself performing an automatic model fallback. What IS
evidenced is swarm's own model *pinning* machinery (`ps-model-red*.md`,
`operator.md`'s PR #84 review of `render_ps`: "pinned agents render
` model=<id>` in their OWN slot") and multiple explicit multi-provider
routing decisions made BY THE OPERATOR/swarm, not by Claude Code:
`battery-smith.md:32` — picking between openrouter/anthropic/claude-haiku-4.5
vs native `claude` cell depending on which API keys existed in `auth.json`;
`codex-audit.md` auditing a *different* harness's (Codex) model/version
currency entirely by hand. I.e. this swarm's routing/fallback logic across
providers is currently hand-built and hand-audited, not inherited free from
Claude Code — Claude Code's own internal fallback (if any, between Anthropic
model variants) is not something this repo's evidence touches either way.

**Rebuild cost: REAL.** Falling back from a 529/overload or model-deprecation
error to an alternate model, mid-fleet, without an operator noticing, is
ordinary distributed-systems work — days, not a core-competency wall. This
repo's own evidence shows the swarm team already doing analogous
provider-selection logic by hand (`battery-smith.md`), suggesting the actual
gap here is smaller than for rows 1/5.

---

## 10. Auth / subscription vs. API keys

**What it is:** Claude Code sessions can run against a Claude subscription
seat (Pro/Max) rather than metered API-key billing.

**Evidence it's load-bearing for THIS swarm:** `battery-smith.md:32` is
direct: "auth.json has ONLY deepseek + zai-coding-plan keys; openrouter/
anthropic/claude-* are listed but NOT keyed, no free gateway claude... Same-
harness Claude cell needs an OpenRouter key added." This is firsthand
evidence that at least one point in this swarm's history, running a
Claude-model cell required deliberately reasoning about auth-key
availability as a blocker — i.e., auth mode is a live, load-bearing
constraint on what this swarm can even spin up, not a background detail.
Separately, `operator.md:315` records agents wedging on a **rate-limit
prompt** ("weekly limit hit") — direct evidence of subscription-seat
quota being a real, hit-in-practice ceiling for this fleet.

**Rebuild cost: TRIVIAL for API keys, HARD for subscription-seat economics.**
Calling the Anthropic API with a metered key is TRIVIAL — any HTTP client.
What a custom loop CANNOT buy back at any engineering cost is the
subscription/flat-rate seat economics (fixed weekly quota instead of
per-token billing) — that pricing model is Anthropic's product decision,
not a technical component; a custom loop is necessarily metered-API-only,
which is a cost-structure difference, not a rebuild task.

---

## 11. Updates / maintenance

**What it is:** Anthropic ships fixes, new tool capabilities, and model
support for Claude Code on its own release cadence; swarm's `updater` agent
consumes these (installs new versions, verifies clean state before
merging).

**Evidence it's load-bearing for THIS swarm:** `docs/audit/_hc-field.md:98`
— `updater.md:141-152`: "git status on ~/.local/share/swarm shows bin/swarm
modified in the working tree... the file was edited directly in the install
clone outside my update cycle... dirty clone is a fail-closed condition."
This shows swarm has its OWN update-maintenance burden (the `swarm` CLI
itself, self-authored) layered on top of consuming Claude Code's updates —
and that self-authored layer already produced a fail-closed incident from a
dirty install clone. Separately, `operator.md`'s herdr-update entries
("Upgraded: brew upgrade herdr -> 0.7.3... TESTED the raw bug on 0.7.3: ...
STILL yields... the leading-slash strip is UNCHANGED") show the team
actively tracking and testing a *third-party* dependency's release cadence
for regressions/fixes — direct precedent for what "maintained by us" costs
in practice when a dependency's owner doesn't fix a known bug across two
patch releases.

**Rebuild cost: HARD, structurally (not a task, a standing cost center).** A
custom loop has no Anthropic team fixing tool-call parsing edge cases,
patching security issues, or adding new model support on its behalf — every
one of the rows above (1-10) that Claude Code currently gives for free
converts into an ongoing maintenance obligation owned by swarm's own team
(or whoever the "harness contractor" role becomes permanently, not for one
inventory task). This fleet's own herdr-update entries show that even
*consuming* someone else's fixes reliably (checking whether 0.7.3 actually
fixed the slash-strip bug: it didn't) is nontrivial, ongoing work — and that
was for a dependency swarm doesn't have to build, only track.

---

## The flip side — what Claude Code's harness WITHHOLDS from swarm

Brief, not exhaustive; no recommendation attached.

- **No control over the loop itself.** Swarm cannot change retry policy,
  tool-call parsing, or context-window management — it can only wrap the
  harness (hooks, pane text, CLI flags) from outside. Every mechanism in
  rows 1-9 is consumed as a black box.

- **Duties are briefed, not enforced, and hooks are the ceiling on
  enforcement.** Per the task brief's own framing and confirmed above (row
  4): hooks are **observation + soft-nudge points that CAN be gates but
  swarm doesn't use them that way today.** DOCUMENTED (fetched from
  `code.claude.com/docs/en/hooks`): `PreToolUse` can genuinely gate
  (`permissionDecision: "deny"/"ask"`); `UserPromptSubmit` can genuinely
  block a prompt (exit 2 or `decision:"block"`) AND inject context; `Stop`/
  `SubagentStop` can genuinely force continuation (exit 2 or
  `decision:"block"`, distinct from `additionalContext`, which only adds a
  non-blocking note read at the end of a turn); `PreCompact` can block
  compaction; `SessionEnd`/`Notification` are pure observe-only with zero
  decision fields. So the harness DOES expose real gates — swarm's own
  `cmd_event`/`cmd_restore` (row 4) simply use the softer, observational half
  of that surface (record + re-ring; inject context) and leave the harder
  half (block a message, force a stuck agent to keep going, veto a risky
  compaction) unused. Whether that's a gap in swarm's use of the harness or
  a deliberate choice is outside this inventory's scope.

- **The pane-vs-status gap is real and already bit this fleet once.**
  `agent_status` / pane text is the only ground truth Claude Code exposes;
  `swarm ps`'s own structured view is a derivative that has already gone
  stale relative to it once (row 3, row 7) — 105 orphaned, blocked tabs
  invisible to `swarm ps` until a human looked at the raw herdr UI.

- **No structural way to make an agent honor its journal/reconciliation
  duties.** The SessionStart/Stop hooks can inject reminders
  (`build_restore`, the doorbell re-ring) but cannot force a model to
  actually write a falsifier-bearing journal entry — that remains entirely
  a matter of the model choosing to comply with its briefed duties, same as
  any other instruction-following.

---

## The 5 hardest-to-rebuild rows (for harness-contractor)

1. **Row 1 — the agentic loop itself.** HARD. Everything else in this
   inventory runs inside it; there is no partial-credit version of "the
   tool-call loop mostly works."
2. **Row 5 — session persistence + compaction.** HARD. Empirically load-
   bearing (8+ agents resumed cleanly through a real 2026-07-13 machine
   restart, `_hc-field.md` §B) for the crash/restart case; the compaction
   sub-case is assumed-but-unwitnessed (`field-evidence-2026-07-09.md` §5),
   which if anything understates the risk of losing it.
3. **Row 11 — updates/maintenance.** HARD as a standing cost center, not a
   one-time task: every capability rebuilt converts into permanent
   ownership, and this fleet's own herdr-update experience shows even
   tracking a third party's fixes reliably is real, recurring work.
4. **Row 2 — tool suite safety semantics.** REAL, trending HARD at fleet
   scale: the individual tools are easy: the coherent safety contract
   (uniqueness-checked edits, sandboxed exec, the specific guarantees this
   repo's own PR reviews lean on) is not.
5. **Row 7 — TUI/pane rendering ("the pane is ground truth").** REAL with a
   hard floor: this fleet's entire observability model is built on watching
   real Claude Code panes, and its own structured status view has already
   proven lossy relative to that raw view once (row 3's orphan-tab
   incident).
