# Field evidence — usage-limit deaths, the hand relaunch, weak-model-delegation skim

**Collector:** `hc-field`. **Scope:** quotes and file paths only, no design, no recommendation.
Every claim below is tagged **VERIFIED** (path + verbatim quote, read directly off disk) or
**NOT FOUND**.

---

## A — USAGE-LIMIT DEATHS

### A1. The trigger-scout death, from the outside

**VERIFIED — the exact death message, captured in three independent places.**

- `.swarm/event/trigger-scout.json`:
  > `{"event": "notification", "ts": 1783891741274, "last_words": "You've hit your session limit · resets 4:30am (Asia/Yerevan)"}`
- `.swarm/journal/trigger-scout.md:1530-1531` (the agent's own account on resume):
  > "Picked back up after the prior incarnation hit its session limit mid-pass-12 (`swarm ps` showed "You've hit your session limit · resets 4:30am" as my own last words)."
- `.swarm/journal/blocked-visibility.md:47-48` (a sibling agent observing the tree):
  > "├─ trigger-scout [live] q=0 idle 8h │ last: "You've hit your session limit · resets 4:30am (Asia/Yerevan)""

**VERIFIED — what the parent/observer saw from outside:** the pane stayed `[live]`, `q=0`, and simply sat `idle` — `swarm ps` rendered the death as an ordinary idle agent, distinguishable only by reading the frozen last-words string. No crash, no dead-process signal.

**VERIFIED — what state survived:** `.swarm/journal/trigger-scout.md:1536-1547` — on resume the agent re-verified from scratch rather than trusting its own journal, and found: `docs/design/TRIGGER.md` (453 lines) and `docs/audit/trigger-red-2026-07-12.md` both intact on disk; doc content current through the last completed pass; all four children (`trigger-lab`, `trigger-prec`, `trigger-pkg`, `trigger-red`) confirmed dead/closed; **"Twelve delivered messages sit in `.swarm/queue/operator/`, oldest to newest, each a real incremental delta"** — i.e., every incremental report the agent had sent before dying was already delivered and did not need to be resent.

**VERIFIED — how work resumed:** the agent itself resumed via the swarm restore mechanism (same session-continuation pattern as other agents in §B) and picked up exactly where it left off: `.swarm/journal/trigger-scout.md:1528`:
> "## 2026-07-13 13:23Z — resumed after a session-limit death; reconciliation, not new investigation"

One thing did **not** survive: `.swarm/journal/trigger-scout.md:1548-1550`:
> "The `/tmp/trigger/*` probe directories referenced by the open falsifier (did b-1/b-2 terminate cleanly) no longer exist in this environment — they were scratch and are gone. I cannot re-check that specific exit status. It is not load-bearing..."
So scratch/tmp state was lost; the durable artifacts (docs, journal, queue) were not.

### A2. Other usage-limit / rate-limit incidents found across `.swarm/journal/*.md`

**VERIFIED — `.swarm/journal/operator.md:199-200`** (a named bug report, not just an anecdote):
> "## 2026-07-12 — [ops-main] BUG FOUND: usage-limit freeze leaves agents unrecoverable by doorbell
> Operator asked to debug post-usage-limit state. Found: trigger-scout subtree (7 agents) had substantial journals (scout=373 lines) but ZERO event files + queued mail undelivered (q=5,7,...) for ~2h. Panes ALIVE in herdr (frozen, not dead). ROOT CAUSE (pane-read confirmed): session hit "session limit resets 11:10pm" MID-TURN -> Stop hook never fired -> no event fact -> (a) ps shows idle? (indistinguishable from a long first turn), (b) stop-re-ring never triggers, so queued mail never nudged. Even after limit reset, pane sits idle-at-prompt with nobody driving it. RECOVERY: doorbell (send-text + send-keys Enter) — FIRST Enter did NOT submit (landed in composer unsubmitted); a SECOND Return keystroke submitted and the agent resumed. So: usage-limit freeze is a real gap — no automatic recovery path... THREE REAL BUGS: (1) Stop-hook-skipped-on-limit -> no event fact -> no re-ring; (2) ps can't distinguish frozen-on-limit from busy-first-turn; (3) doorbell Enter unreliable (needed a second Return). Worth a fix pass after this session. Also: weekly limit at 82% — the swarm's token appetite is real."

**VERIFIED — `.swarm/journal/operator.md:313-315`** (a distinct incident: rate-limit prompts wedging panes, tangled with a trust-prompt bug):
> "A few that passed trust later wedged on the RATE-LIMIT prompt (weekly limit hit). 118 herdr tabs, only 13 recorded swarm agents; 105 orphans, ~90 on trust prompt."

**VERIFIED — `docs/audit/trigger-red-2026-07-12.md:100`** (the `bigA` probe cell, all three runs killed by 429):
> "`result: "You've hit your session limit · resets 11:10pm"` — at `num_turns` 13/18/16 and durations of 68s, 155s, 193s."
Also `.swarm/journal/trigger-scout.md:546`:
> "All three `bigA` runs died on a 429 ("You've hit your session limit"). I scored killed..."
And `.swarm/journal/trigger-red.md:74`:
> "FINDING 1 — ALL THREE bigA RUNS DIED ON A RATE LIMIT (FLIPS)... `result: "You've hit your session limit · resets 11:10pm"`, exit=1."
(Same underlying 11:10pm-reset incident, corroborated independently in three files by two different agents.)

**VERIFIED — `.swarm/journal/opencode-plugin-scout.md:761-763`** (rate limiting affecting probe timing, not a death, but explicitly named):
> "probes — the last runs needed a ~280s window to reach session.idle where early ones took ~60s. Rate limiting, not a bug in the pump. Budget wall-clock accordingly when reproducing; a paid model would make these probes seconds."

**VERIFIED — `.swarm/journal/harness-contractor.md:139-141`** (this incident cited as the motivating example in a design discussion):
> "Avenue 3 — change model/harness on the fly (redundancy). Two triggers the human named: (a) hitting a usage limit — this ALREADY HAPPENS, `trigger-scout` died with "You've hit your session limit · resets 4:30am"..."

**NOT FOUND:** no incident text matching "usage limit" (as opposed to "session limit") or "limit hit" as standalone phrases elsewhere in `.swarm/journal/*.md`; the two recorded wall-clock reset times are 4:30am and 11:10pm (Asia/Yerevan), on two separate underlying limit windows (trigger-scout's own death vs. the probe-fleet's `bigA` cell).

---

## B — THE HAND RELAUNCH (2026-07-13, after machine restart)

**VERIFIED — the orphan-tab incident that names the count of live/recorded agents matching "~13":** `.swarm/journal/operator.md:306-326` ("incident + cleanup — orphan trust-prompt tabs — 2026-07-13"):
> "118 herdr tabs, only 13 recorded swarm agents; 105 orphans, ~90 on trust prompt... RESOLVED: human chose "close all orphans." Closed 104 orphan tabs (herdr tab close), 0 failures. KEPT 14: the control tab + the 13 recorded live agents (hardener, inline-work-audit, model-fit, onboarding-scout, onboarding-split, opencode-plugin-scout, operator-structure-scout, org-review-scout, ps-model, trigger-scout, updater, weak-model-deleg). No swarm value lost — orphans were experiment sub-sessions whose results were already folded into TRIGGER.md."

This is the closest on-disk match to "hand-relaunched ~13 agents" — it lists the 13 by name. Note: this entry documents *closing orphans down to* 13 kept agents, not explicitly the act of relaunching them onto Sonnet post-restart; no journal entry uses the words "relaunch" or names "Sonnet" as the target model for this specific event.

### B1. Journal entries from today (2026-07-13) mentioning restore/resume/fresh session

**VERIFIED — agents whose journals show an explicit resume/restore entry dated 2026-07-13:**

| Agent | File:line | Quote |
|---|---|---|
| trigger-scout | `.swarm/journal/trigger-scout.md:1528` | "resumed after a session-limit death; reconciliation, not new investigation" |
| hardener | `.swarm/journal/hardener.md:301` | "resumed cold, reconciled, nothing new to do" |
| harness-contractor | `.swarm/journal/harness-contractor.md:241` | "Fresh session (restore hook fired). Journal had only the spawn entry — no prior work lost." |
| hc-industry | `.swarm/journal/hc-industry.md:6` | "## 2026-07-13 (resume) — starting fan-out" |
| model-fit | `.swarm/journal/model-fit.md:399` | "resumed after restart; verified nothing to redo... Woke to the same task text (spawn brief re-delivered)." |
| org-review-scout | `.swarm/journal/org-review-scout.md:1659` | "resumed cold, verified rather than re-did. Task was already complete." |
| spawn-repair | `.swarm/journal/spawn-repair.md:18` | "orientation (resumed session, no prior work found)" |
| spawn-repair | `.swarm/journal/spawn-repair.md:115` | "resumed mid-flight, cleared inbox, spawned the DISCIPLINE reviewer" |
| updater | `.swarm/journal/updater.md:141` | "(resumed) DIRTY CLONE detected, fail-closed, reporting" |
| hc-field (this agent) | `.swarm/journal/hc-field.md` | resumed via SessionStart hook, same pattern |

That is 9 distinct other agents plus this one (10 total) with an explicit dated resume entry today — short of the operator's reported "~13," but several of the 13 named orphan-survivors above (onboarding-scout, onboarding-split, opencode-plugin-scout, operator-structure-scout, ps-model, weak-model-deleg) were not directly checked for a same-day resume entry in this pass (see Falsifier below).

### B2. What carried over

**VERIFIED — `.swarm/journal/model-fit.md:399-406`:**
> "Woke to the same task text (spawn brief re-delivered). Checked before acting: PR #83 (`swarm-dev/model-fit`) is still OPEN, `mergeStateStatus: CLEAN`/`mergeable: MERGEABLE`... Operator report is still queued at `.swarm/queue/operator/1783889648064-model-fit.json`, undelivered... No file changed since the last entry. Nothing to redo, nothing to add."

**VERIFIED — `.swarm/journal/harness-contractor.md:241`:** "Journal had only the spawn entry — no prior work lost" — i.e. for this agent the restore was effectively a first spawn (no prior state existed to lose).

**VERIFIED — `.swarm/journal/field-tester.md:7`** (from 2026-07-12, but the same restore mechanism, useful as a description of the mechanic itself):
> "Restored via [swarm restore] hook; journal had only the spawn entry, docs/audit/ empty, no grandchildren yet — so no work is lost, I'm starting fresh. My own restore is itself a #5 data point: I resumed from the journal tail + re-injected task without asking the operator anything."

### B3. What broke or was lost

**VERIFIED — dirty/stray state discovered on resume, `.swarm/journal/updater.md:141-152`:**
> "Resumed. Fetch: origin/main = b94fa9e = installed HEAD (no upstream move). BUT `git status` on ~/.local/share/swarm shows `bin/swarm` modified in the working tree (not staged, not stashed, no other file touched)... the file was edited directly in the install clone outside my update cycle, by someone/something else touching a directory my brief reserves for me alone. Per brief: dirty clone is a fail-closed condition — do not merge, do not..."

**VERIFIED — the tree-wide mis-attribution bug surfaced by the resume itself, `.swarm/journal/trigger-scout.md:1568-1583`:**
> "First send attempt (`swarm send operator --stdin`) exited 0 and looked clean, but the file it wrote was `from: operator, to: operator` — self-addressed... Cause: `SWARM_AGENT_ID` was unset in this shell... so every send I made was silently misattributed rather than failing loud... Checked whether this was mine alone before touching anything, and it is not — it is tree-wide right now. `queue/operator/` holds recent same-pattern files from `inline-work-audit`, `updater`, `onboarding-split`, and `onboarding-scout`, all `from: operator, to: operator`... Every one of those agents resumed cold this same wall-clock window and hit the same unset-env condition."

This names 5 agents total (trigger-scout + 4 others: inline-work-audit, updater, onboarding-split, onboarding-scout) hitting the identical `SWARM_AGENT_ID`-unset misattribution bug on today's resume — a concrete "what broke" for the relaunch.

**VERIFIED — separately, a spawn-breaking herdr bug discovered same day (not itself a resume defect, but hit during the same post-restart work session), `.swarm/journal/operator.md:334-350`:**
> "WHILE delegating the blocked-visibility fix, EVERY swarm spawn failed: child died at a shell with "zsh: no such file or directory: Users/.../launch.sh". ROOT CAUSE (VERIFIED, isolated in a fresh pane): herdr 0.7.1 `pane run` strips exactly ONE leading '/' from the command."
This blocked new spawns tree-wide until an inline shim fixed it same day (`.swarm/journal/operator.md:348-358`); confirmed still present on herdr 0.7.3 (`operator.md:368-379`).

**Falsifier for §B (stated honestly):** this pass grepped only for the phrases "restore/restart/fresh session/relaunch/resumed cold" and checked the journals that matched. It did **not** individually open onboarding-scout.md, onboarding-split.md, opencode-plugin-scout.md, operator-structure-scout.md, ps-model.md, or weak-model-deleg.md to confirm each independently shows a same-day resume — four of those six are already implicated by name in the mis-attribution bug quote above (trigger-scout.md:1578-1580), which is second-hand corroboration, not a first-hand read of their own journals. If the operator's "~13 onto Sonnet" claim depends on those files directly, they should be spot-checked before treating this section as exhaustive.

---

## C — weak-model-delegation-2026-07-13, in ≤10 lines

**Ruling:** over-delegation fear NOT SUPPORTED but NOT FULLY TESTED — Haiku showed zero spawn reflex (under-delegates, grinds serially) but was blocked by a permission dialog before reaching the synthesis/judgment step where the fear would actually live; reviewer verdict on the whole probe: WOUNDED (survives with corrections).
**Measured numbers:** 3 children spawned total across arms (wmd-opus, wmd-haiku, wmd-haiku2); **descendants ever created by any of them: 0**; Opus arm completed (234-line report, 23 rows, 5 findings), both Haiku arms blocked on a permission dialog (one produced a confirmed **0-byte** artifact); Opus's headline claim (WORLD.md self-contradiction) verified directly against git (`HEAD:WORLD.md` line 59 vs. uncommitted +5/−3 diff).
**Root cause found along the way:** `swarm spawn` writes `.swarm/settings/<name>.json` with hooks only, no `permissions` block, so every spawned child is exposed to interactive permission dialogs regardless of model.
**Honestly-stated limits:** (1) the two arms differed in model AND permission posture — "not a clean matched pair... any latency or cost comparison between them is dead"; (2) "zero-children is necessary-but-not-sufficient evidence... not distinguishable from 'did nothing'"; (3) the judgment/synthesis step — "exactly where the urge to offload judgment would peak" — was never reached by either Haiku run; (4) the falsifier the report says would settle model-vs-gate causation (spawn an Opus child into the same permission wall) was proposed but not yet run.

---

## Index of files read for this report

- `.swarm/journal/trigger-scout.md`, `.swarm/journal/trigger-red.md`, `.swarm/journal/operator.md`, `.swarm/journal/blocked-visibility.md`, `.swarm/journal/harness-contractor.md`, `.swarm/journal/hc-industry.md`, `.swarm/journal/opencode-plugin-scout.md`, `.swarm/journal/model-fit.md`, `.swarm/journal/updater.md`, `.swarm/journal/hardener.md`, `.swarm/journal/org-review-scout.md`, `.swarm/journal/spawn-repair.md`, `.swarm/journal/field-tester.md`
- `docs/audit/trigger-red-2026-07-12.md`, `docs/design/TRIGGER.md`
- `.swarm/event/trigger-scout.json`, `.swarm/agents/trigger-scout.json`, `.swarm/queue/trigger-scout/delivered/*`
- `docs/audit/weak-model-delegation-2026-07-13.md`, `docs/audit/weak-model-deleg-evidence/` (RED-verdict.md, report-opus.md, EVIDENCE-haiku{,2}-*.txt, task-{haiku,opus}.txt — listed, not all opened line-by-line)
