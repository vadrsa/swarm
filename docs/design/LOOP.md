# LOOP — the controlled-loop agent: owning the duties instead of hoping for them

**Author:** `harness-contractor`, outside contractor, reopened engagement of 2026-07-13.
This document answers the human's rebuttal of `HARNESS.md`'s central boundary
(foreign-models-are-leaves-only) and his proposal: *"if we ran opencode with heavy
modifications to the loop, where we have access and control over every part of the loop…
we could make almost any model usable inside the swarm."* Scope ruling from the operator:
design the controlled-loop agent, then rule between (A) fork opencode and (B) build our
own loop. Cost is a first-class driver and is measured here, not asserted.

**Evidence discipline:** VERIFIED / MEASURED / DOCUMENTED / REASONED as in `HARNESS.md`,
with the same post-review humility: child artifacts are cited by section, quotes are
quotes. Inputs read in full by me: the reopening brief; `docs/design/OPENCODE-PLUGIN.md`
(§0–§5) and `OPENCODE-PLUGIN-RED.md` (verdict table + Attack 1); child artifacts
`docs/audit/_hc-ocloop.md` (per-duty enforceability, three depths),
`docs/audit/_hc-claudeval.md` (what Claude Code gives free; what its hooks can gate),
`docs/audit/_hc-price.md` (measured cost). `HARNESS.md` remains the parent document;
§8 below lists exactly which of its rulings this document retracts.

---

## 1. WHAT TO BUILD, IN ORDER

The human asked for one readable answer. Here it is; everything after this section is
the evidence and the arguments.

**Build 0 (prerequisite, already owed):** the spawn `permissions` block and
blocked-visibility — both already on `HARNESS.md` §8's bill. Every step below assumes
children can clear their own dialogs and wedged panes are visible.

**Build 1 — the duty loop, both backends (the core of this design, ~the first real
sprint):** swarm stops *asking* agents to perform protocol duties and performs them
itself, at the harness layer:

- **Claude backend (BUILT on `swarm-dev/duty-loop` @ 65dc6e6, verified, pending
  merge; LOOP-RED3 correctly dinged an earlier draft for reading as if it existed
  before it was built):** extend the Stop hook swarm already wires (`cmd_event`,
  `bin/swarm:878`) — the digest fires on **quiescence, not on every stop** (a
  correction I owe to no reviewer — caught after both reviews: a digest per Stop would
  claim a parent turn per child turn and flood the queue): at Stop, if the inbound
  queue is empty (the quiescence test proper — a non-empty queue re-rings and
  another turn follows) AND no send-to-parent this turn AND the cooldown has elapsed
  (default 10m, a per-agent state file that survives restarts) AND **the digest
  content differs from the last digest sent** — the content-diff gate is LOOP-RED3's
  repair, and it is what kills the two healthy-shape misfires the first predicate
  had (heads-down work and waiting-on-children would otherwise digest-spam every T).
  The hook then sends the parent one digest (last assistant words + artifact paths
  touched) and arms the cooldown. Worst case is bounded (≤ 60/T digests per
  agent-hour, and only when state actually changes); an idle-after-work agent's
  parent hears within T. The journal append (mechanical layer) does fire every stop — journals are
  files, not turn claims. Today's hook surface, no new wiring — `cmd_event` already
  reads `last_words` from the transcript.
- **opencode backend:** the pump from `OPENCODE-PLUGIN.md` §3.1 — with its tag
  carried honestly per that doc's own §3.7: every component VERIFIED individually
  (write persists, idle is once-per-turn, `noReply` fires no idle, self-ring causes a
  turn, loop guard terminates), but the **two-phase pump as one program is REASONED
  and the pump-inside-a-live-TUI composition is unrun** — both are Build 1's first
  named checks, before any fleet use — extended the same way — its `event` hook on `session.idle`
  reads the turn's assistant text over the server API, sends the parent digest, appends
  the journal line. Plus the launcher body from that doc's §5: TUI with pinned port,
  health assertion, per-agent `OPENCODE_SERVER_PASSWORD`.
- Both backends: `swarm_spawn` as a schema'd tool (opencode: registered tool +
  `tool.execute.before` gate; Claude: the mandate's required flags) — `{model, reason}`
  required by structure. Time-box: parent-owned watchdog with a real terminator
  (opencode: `POST /session/{id}/abort`, DOCUMENTED; Claude: the remodel stop-sequence
  from HARNESS §6).

**Build 2 — the gate experiment (before any fleet migration; this is the decision
point):** re-run the FLEET-EVAL-V3 battery — deepseek, GLM, claude-anchor — with the
duty loop ON. The prediction this whole design stakes itself on, stated as a number:
**report-to-parent goes from 3/7-delivered to 7/7 by construction** (the measured
failure was "narrates the report as turn text instead of sending it" — a loop that
sends the narration makes narration sufficient), and **D4 journal hard-fails vanish**
(the journal is written by the loop, not the model). What the re-run must then actually
measure is what remains: **judgment** — does GLM's watchdog-less harvest style hang
on a genuinely dead child (an *unexercised* risk in v3: "terminated only because its
children delivered"); does deepseek still abandon its brief at a blocked dependency
(V3:82-83); is the auto-digest high-enough signal for a parent to judge from. Those are the model's properties, and
no loop fixes them; the loop only bounds them (time-box, watchdog).

**If Build 2 shows protocol absorbed but judgment still failing — the pre-registered
FAIL branch is §4b** (the operator's chosen path: try harder before taking the leaf
win — with the mechanisms named in advance, the cheapest lever first, and a numeric
stopping rule so "try harder" cannot eat a month). **Build 2b — the cheap-tier
roster** is a *separate follow-on* against the proven rig, never a Build 2 arm.
Live-verified 2026-07-13 against vendor pages (DOCUMENTED — `docs/audit/_hc-tiers.md`,
URLs + dates + an explicit UNVERIFIED list): **deepseek-v4-flash** ($0.14/$0.28 per
1M, 1M context, tool-calling confirmed — top pick, zero open caveats);
**kimi-k2.5** ($0.60/$3.00, cache-hit $0.10, 262K context, tool-calling confirmed —
a second model family, 37% cheaper than the Kimi tier previously priced);
**glm-4.7-flashx** (~$0.06–0.07/$0.40 — cheapest by far but tool-calling/context only
third-party-corroborated: run a one-turn tool-call smoke test before committing it as
an arm).

**Build 3 — open the seats (only if Build 2, or its §4b remediation, passes):** foreign tokens stop being
leaf-only; `PLAYS.md` gains the mixed-tree play (§7): Fable/Opus operator and judgment
seats, foreign protocol-carried seats below, Sonnet checkable leaves, thin-runner
one-shots. Cost per §6.

**Build 4 — fork, on a named trigger, not day 1:** vendor-pin opencode at the verified
version; fork when (a) an upstream release breaks the pinned plugin surface twice —
the binary already drifted 1.17.13→1.17.18 *during this repo's own investigation*
(VERIFIED, `_hc-ocloop.md` §0) — or (b) a duty emerges that genuinely needs a
turn-end gate (see §3: none does today). The fork is a maintenance patch-set on a
pinned base, not a rewrite.

**Refused: (B) build our own loop.** §5 is the full argument; the one-line version:
the three HARD rows of `_hc-claudeval.md` (the agentic loop itself, session
persistence + compaction, and maintenance as a standing cost center) are exactly what
opencode already is — building our own loop rebuilds a product to obtain control the
plugin surface plus a pinned fork already give.

---

## 2. THE REFRAME THE EVIDENCE FORCED — absorption, not gating, and not opencode-only

The human's framing was "control the loop so duties are enforced structurally." The
evidence sharpened this twice:

**First: the two harnesses have *inverted* enforcement surfaces** (this is the
reopening's most useful factual result):

- **Claude Code can GATE but swarm never gates:** its hooks support hard decisions —
  `Stop` can force continuation (`decision:"block"`), `PreToolUse` can deny,
  `UserPromptSubmit` can block (DOCUMENTED — fetched from the hooks reference,
  `_hc-claudeval.md` flip-side). Swarm today uses only the observational half:
  record + soft re-ring. The enforcement ceiling the human assumed we lacked is
  partially *already installed and unused*.
- **opencode can't gate turn-end at all:** no hook at any documented depth can refuse
  to let a turn end — turn-end is observe-only, fire-and-forget; there is no
  `decision:block` analog (VERIFIED — `_hc-ocloop.md` §1, all seven duty rows and the
  pattern section). What it has instead is *deeper in-loop mutation*: own the system
  prompt per turn, own the compaction prompt **by construction** (the vendor's own
  doc example for that hook is a multi-agent swarm continuation prompt), rewrite the
  agent catalog's models, block any tool call by throwing, drive the session over HTTP.

**Second: for the duties that actually failed in the eval, gating is the wrong tool
anyway.** The measured protocol failures — 4/7 report drops ("it knows who its parent
is and does not use the verb"), zero journals — are failures to *perform a mechanical
act after the thinking is done*. You can gate the model until it performs the act
(Claude-style), or you can **have the loop perform the act itself** — read the turn's
last words, send the digest, append the journal line. Absorption is strictly stronger
than gating: it requires zero model compliance, works identically on both backends
(Stop hook / idle pump), and cannot be performatively satisfied with a low-effort
token the way a gate can (a gated model can emit "reported ✓" to escape; an absorbed
report *is* the actual last words + artifact list).

**What absorption cannot absorb** — and this is where the leaf-only ceiling honestly
retreats to: **judgment**. Reconciliation quality, briefing quality, knowing a child's
silence means death, not abandoning the brief — the eval's *other* failure class
(deepseek's 11-minute harness detour, V3:82-83; GLM's watchdog-less harvest loop,
an unexercised live risk — see the correction below). The loop
bounds these (time-box, watchdog, every-turn reconcile scaffold via the system
prompt) but does not supply them. Whether bounded judgment is *enough* judgment for a
mid-tree seat is precisely what Build 2 measures — it is not decidable from the
current record, and this document does not pretend to decide it.

*(A correction from this document's own adversarial review, folded here: the first
draft cited "GLM's `ps` misread + 4-retry hang" as live judgment-failure evidence.
That is a **v2** finding the eval itself retired — "No v2 GLM D2 row should be cited
again" (V3:123-124); the v2 hang was substantially a rig artifact. The judgment
examples that ARE live in v3: deepseek's 11-minute harness detour abandoning its
brief (V3:82-83), and GLM's watchdog-less harvest loop — graded as an unexercised
risk, not a demonstrated hang.)*

**And the "engine never" confusion, settled in print** (the human could not tell what
HARNESS.md's refusal was based on, which is a §9 defect and mine): HARNESS.md §5
refused ONE thing — a config **schema for model+harness combo names** (avenue 2's
`--play` flag); it ruled the *recipes* should be prose. That ruling said nothing about
whether swarm may own an agent runtime. **Swarm already is a harness** — `bin/swarm`
plus four hooks is a thin loop-controller around Claude Code today, and PHILOSOPHY §8
("an engine never") is about not building machinery for conventions that haven't
failed, not a prohibition on the runtime layer. The duty loop is the same category of
thing as `cmd_deliver`/`cmd_event`: swarm-owned code binding a session to the swarm
contract. Deeper, but not different in kind.

---

## 3. THE DUTY TABLE — loop stage or prompt hope, per backend

The reopening's central question, answered per duty. **ABSORBED** = the loop performs
it; the model is not involved. **GATED** = the loop can refuse to proceed without it.
**PROMPTED** = still a briefed duty; the loop can scaffold and nag but not enforce.
Sources: `_hc-ocloop.md` §1 (opencode, per-hook, VERIFIED semantics),
`_hc-claudeval.md` row 4 + flip-side (Claude, DOCUMENTED).

| Duty | Claude backend | opencode backend | Net |
|---|---|---|---|
| **Report-to-parent** | **ABSORBED** — Stop hook sends last-words digest + artifact paths (extends `cmd_event`, which already reads `last_words`) | **ABSORBED** — pump's `event` hook reads the turn's messages over the API, sends digest | The measured 4/7 drop class is closed by construction. Model-authored reports remain welcome and better; the floor is no longer zero. |
| **Journal write** | **ABSORBED** (mechanical layer) — Stop hook appends turn digest | **ABSORBED** (mechanical layer) — same, from the pump | The *record-of-what-happened* layer is loop-written. The *reconciliation* layer (own words, falsifier) stays PROMPTED — see below. |
| **Reconcile (falsifier discipline)** | **PROMPTED** — cannot be absorbed (it IS thinking); scaffold injectable per-turn; a `Stop` gate could demand *an* entry but a compelled entry is what PHILOSOPHY §2 refused | **PROMPTED** — `system.transform` injects the scaffold every turn (VERIFIED) | Stays a judged duty on both. This is where model quality still decides seat-worthiness. |
| **Time-box / watchdog** | **GATED externally** — parent watchdog + the remodel stop-sequence | **GATED externally** — parent watchdog + `POST /session/{id}/abort` (DOCUMENTED) | Real terminator on both; the opencode one is cleaner (an HTTP call vs pane keystrokes). |
| **Done-signal** | Stop hook + queue state (today's semantics) | artifact-exists convention + idle, per FLEET §5; the pump can nag an idle-without-artifact | Unchanged from HARNESS; absorption of *reporting* makes silent completion visible either way. |
| **Spawn with model+reason** | **GATED** — the mandate's required flags (HARNESS §3, unbuilt, billed) | **GATED** — registered `swarm_spawn` tool with required schema args; `tool.execute.before` throws on absence (VERIFIED block primitive) | The opencode side is *stronger* than the Claude side here: a tool schema is harder to skip than a CLI convention. |
| **Restore (compaction)** | Existing `SessionStart` hook (VERIFIED in the field, `_hc-field.md` §B) | **ABSORBED BY CONSTRUCTION** — `experimental.session.compacting` replaces the compaction prompt itself (VERIFIED; the vendor's own example is a swarm continuation) | opencode's restore seat is *better* than Claude's-as-used-by-swarm. |
| **Restore (crash/restart)** | Existing hook, field-proven | **PARTIAL** — no session-start hook exists (VERIFIED negative); falls to launch-prompt + external watcher pushing `noReply` restore | The one place the opencode backend is weaker; the external watcher is the same watchdog process the time-box already needs. |

Two rows deserve emphasis because they are where the human's intuition was most right:
**spawn-gating and compaction-restore are *stronger* under the owned loop than under
Claude Code as swarm uses it today.** And one row where it was most wrong: nothing at
any depth of opencode gates turn-end — the "heavily modified loop" cannot make a turn
refuse to finish without a fork (and per the table, day-1 needs no such gate).

**Security note the design must carry** (VERIFIED — `_hc-ocloop.md` §0): the opencode
server is unauthenticated by default (any local process can prompt or run shell in an
agent) and its session store is a world-readable SQLite file. The *read* path is
actually consistent with swarm's own contract — seeing is global; anyone may read
anyone's pane and journal. The *drive* path (prompting/shelling another agent) violates
"acting is local" and is closed by the per-agent `OPENCODE_SERVER_PASSWORD` in the
launcher env. The read path cannot be closed and is accepted, stated here so it is a
decision and not an oversight.

---

## 4. WHICH MODELS BECOME SEAT-CAPABLE — the claim, cut to what the evidence supports

The honest form of the human's claim is conditional and two-layered:

- **Protocol-capable: predicted YES for any model that can drive tools** (GLM was
  graded an excellent tool-user; deepseek's tool work was real). The protocol layer is
  absorbed, so protocol failures stop being possible *for the loop-carried duties*.
  This half is nearly definitional — which is exactly why it must be checked against
  reality: **Build 2's re-run, predicted 3/7→7/7 delivered reports and journal
  hard-fails→zero.** If THAT fails, the loop implementation is buggy or the
  prediction was wrong, and this document is wrong at its foundation.
- **Judgment-capable: UNKNOWN, honestly.** The eval's live judgment concerns (brief
  abandonment, no self-time-boxing, a harvest style that would hang on a dead child)
  are untouched by absorption. The re-run measures them with the protocol noise
  removed — that is its real value: for the first time, judgment quality will be
  visible *unconfounded* by protocol drops. A model that reports 7/7 and still hangs
  its subtree on a dead child it never checks is a leaf with a megaphone, not a seat.

**The falsifier for the whole reopening** (committed): if the duties-in-loop re-run
still shows dropped reports/journals, OR if with protocol absorbed the judgment
failures alone still sink the delegation battery (D2-heavy no longer 6/6 under
realistic conditions), then the leaf-only ceiling was a **model property**, the
human's bet is wrong, and HARNESS.md's original boundary should be un-retracted. The
re-run is cheap: the V3 rig exists, the briefs are on disk, and the only new piece is
the duty loop from Build 1.

**A prediction registered before the re-run, so it can be scored:** deepseek and GLM
pass D1/D2-heavy clean, report 7/7 by construction; the dead-children hazard (GLM's
unexercised v3 risk) never materializes as a hang because the watchdog is now the
harness's, not a hoped-for behavior — the re-run should exercise it deliberately
(kill a child mid-battery) to convert the unexercised risk into a measured row;
deepseek still burns its time-box on the blocked dependency but the box now fires. Net: **mid-tree protocol seats open; judgment seats
(red-team, design, operator-adjacent) stay Claude.** If the re-run says otherwise in
either direction, the re-run wins.

---

## 4b. THE BUILD 2-FAIL BRANCH — pre-registered, because the operator bet against me

The operator was asked what happens if Build 2 shows protocol absorbed but judgment
still sinking the delegation battery. He chose **fork and try harder** over taking
the leaf win — a direct bet against this document's claim that *"the loop bounds
judgment but does not supply it."* Per his instruction this section designs his path
honestly, pre-registered before any Build 2 data exists, so nobody — including me —
can rationalize afterward.

### 4b.1 The decomposition that makes the branch designable

"Judgment" in the three measured failures is not one thing. Split it:

- **Inputs to judgment** — having the brief in mind, knowing the clock, seeing the
  children's true liveness. Recall and attention. **A loop CAN supply these**, the
  same way restore already supplies continuity: put the facts in front of the model
  every turn.
- **Inference over those inputs** — judging an artifact, scoping a child's brief,
  deciding what matters. **No loop supplies these.** A loop that tries gets
  compelled-compliance noise (PHILOSOPHY §2's exact refusal — and per the brief's
  instruction I say it to the operator's face: a *forced* reconciliation stage is
  trivially satisfied with a well-formed nothing, and the record would read as
  discipline while carrying none).

The honest reframe of the operator's bet: **how much of the measured judgment
failure was actually an inputs failure?** The evidence gives his side real ammunition:
GLM *verified each child's report against the child's actual output file* when it had
the data (V3's D2-heavy, 6/6) — its dead-child hazard is plausibly starvation of
liveness *inputs*, not missing inference. That is the strongest version of his case,
and it is testable cheap.

### 4b.2 The mechanism list, named in advance, mapped to the measured failures

Targets: **F-A** deepseek abandons its brief at a blocked dependency (V3:82-83);
**F-B** GLM's watchdog-less harvest would hang on a dead child (unexercised, to be
exercised deliberately in Build 2); **F-C** no self-time-boxing.

**Stock opencode — no fork (these come first):**

- **M1 — the per-turn operating frame** (`system.transform`, VERIFIED surface): every
  turn's system prompt carries: the task's one-line goal; the elapsed/budget clock;
  a pre-digested children table (name, last artifact age, pane liveness — computed by
  the plugin from `.swarm/` + herdr `agent_status`, the same closed-enum data §2.3 of
  HARNESS.md ships); and the standing rule *"blocked >N min on infrastructure →
  journal BLOCKED and return to the brief."* Targets **F-A** (re-anchoring), **F-C**
  (the clock is supplied), **F-B** (liveness is supplied). This is the mechanism I
  would bet on, and it needs no fork. *(Per LOOP-RED3, stated honestly as TWO
  mechanisms under one number: the **data half** — clock, liveness table — genuinely
  SUPPLIES inputs; the **instruction half** — the blocked-rule — is the same
  PROMPTED category as every briefed duty, and gets no structural credit. The split
  confidences in §4b.4 reflect this.)*
- **M1b — context curation** (`messages.transform`) — *added by the adversarial
  review (LOOP-RED3), which correctly found the stock list incomplete: I had ruled
  this hook out for mail delivery (non-persistence makes delivered mail vanish) and
  never noticed that for CURATION non-persistence is exactly right — pruning the
  model's per-call VIEW is the point.* Prune the perseveration tail (the 11 minutes
  of harness-debug spam) from the view; splice a system-content re-anchor line. No
  phantom user messages (the prior art's injection-refusal finding does not bite:
  nothing is added that claims to be mail). Targets **F-A**, plausibly stronger than
  M1's instruction half — and it needs **no fork**, which strengthens this branch's
  own stock-wins prediction.
- **M2 — the perseveration guard** (`tool.execute.before`, VERIFIED block primitive):
  after N near-identical failing commands in one turn-window, the guard refuses the
  N+1th with an injected instruction ("journal BLOCKED; return to the brief").
  Targets **F-A**'s specific measured shape (11 minutes of harness-debugging).
- **M3 — the hard time-box** (`POST /session/{id}/abort` + re-brief, DOCUMENTED):
  on budget breach the watchdog aborts the turn and injects "budget exceeded — report
  status now." Targets **F-C** as a bound (already in Build 1's watchdog; listed here
  because 4b tunes it per-failure).

**Fork-only (what the operator's fork would actually buy, honestly graded):**

- **M4 — hard turn-end gate** (`session/processor.ts`): the turn cannot end until a
  named predicate holds (e.g. a reconciliation block is present). Honest grade:
  **§2-refused for judgment predicates** — compels the form, not the thinking; for
  mechanical predicates (artifact exists, report sent) absorption already covers it
  without a fork. I list it because the operator asked for the fork's real contents,
  not because I endorse it.
- **M5 — the harvest interlock** (loop stage): refuse to execute harvest-shaped tool
  calls while any child is dead-unacknowledged; the model must acknowledge the death
  (one line) before the loop proceeds. Targets **F-B**. Marginal over M1 (which
  supplies the same fact passively) — but it is the *strongest defensible* fork
  mechanism, because acknowledgment is a one-bit act, not compellable prose.
- **M6 — forced brief re-read as a loop stage every N turns.** Dominated by M1
  (per-turn, cheaper, no fork). Listed for completeness; would not build.

### 4b.3 The order and the stopping rule (numbers, not vibes)

- **Build 2.5** — M1+M2+M3 on **stock** opencode, one battery re-run, foreign arms
  only. No fork. This is the cheapest lever and per the brief's own suspicion it is
  where the win lives if there is one.
- **Build 2.6** — only if 2.5 flips **at least one but not all** of the three named
  checks: the fork spike, timeboxed **one week of build**, implementing **at most
  M5 (+M4 only for mechanical predicates)**, then one battery re-run.
- **STOP — take the leaf win — when any of:** (a) Build 2.5 flips **zero** of the
  three checks; (b) after Build 2.6, a foreign arm still fails **≥2 of 3**; (c) total
  remediation spend exceeds **3 battery runs + 1 week of fork work**. On STOP, the
  ceiling stands as a **model property for this model generation**; a new model
  generation is a new experiment (Build 2b's roster), not a resumption of "try
  harder."
- **Pass, defined per-arm:** a foreign arm matches the anchor on the judgment
  sub-checks (the D2-heavy verification rows, the deliberately-exercised dead-child
  row, the time-box row). Seats open **per model**, not for "foreign models" as a
  class.
- **Rubric prerequisite (LOOP-RED3's catch, folded):** of the three checks, only
  D2-heavy exists as a scoreable rubric row today; **the dead-child row and the
  time-box row must be authored and pre-registered into the V3 rubric BEFORE Build 2
  runs** — otherwise "flips ≥2 of 3" is a judgment call wearing a number. That
  authoring is part of Build 2's prep, not an afterthought.
- **"Per model generation" reopening, defined:** a vendor's new major version
  (deepseek-v5, GLM-5…) permits **one** Build-2b-style run for that model against
  the same rubric. It does not reopen "try harder" for the same weights — the
  stopping rule's verdict on a model generation is final for that generation.

### 4b.4 The honest prior, registered before any data

- Build 2 alone (duty loop): protocol rows pass — **~85%**; the three judgment
  checks: mostly unchanged.
- Build 2.5 (stock scaffold): **F-C fixed ~80%** (clock + abort — the DATA half of
  M1 plus M3, nearly mechanical); **F-B fixed ~65%** (inputs-shaped — revised down
  one notch per LOOP-RED3's correct hedge: GLM's 6/6 was *harvest-time
  file-verification*, a different competency from live liveness-monitoring, so the
  supporting evidence is adjacent, not direct); **F-A improved ~60%** (revised UP
  from 50% for M1b context curation, which prunes the perseveration spam from the
  view rather than asking the model to resist it; the residual is model-internal
  attention drift); full judgment parity with the anchor on the battery: **~35%**.
- Build 2.6 (the fork spike), conditional on a partial 2.5: flips at least one
  additional check — **~15%**. The fork's mechanisms are mostly dominated (M6) or
  §2-refused (M4); M5 is the one real card.
- Net: **the operator's "try harder" bet succeeds with meaningful probability
  (~40–45%) — but if it succeeds, I expect the win to come from the STOCK scaffold,
  not the fork.** His instinct that judgment can be moved is better than my first
  draft allowed; his chosen instrument (the fork) is, on my reading of the measured
  surface, the wrong tool for it. If Build 2.6 is what flips the checks, I was wrong
  twice and the record will show it.
- *Asymmetry flag, per LOOP-RED3 and kept in the same spirit as this document's
  §10 self-findings: of the three outcome branches, two (STOP; 2.5-alone-succeeds)
  vindicate this author and only fork-succeeds costs him. The prior is registered
  anyway because a lopsided prior honestly held is still scoreable — but the reader
  should weight it knowing the author's incentives point the way they do.*

---

## 5. FORK vs BUILD vs PLUGIN — the ruling, with the anti-case at full strength

**(B) Build our own loop: REFUSED.** The inventory (`_hc-claudeval.md`) was built to
be the strongest case against a custom loop, and it is: the agentic loop itself
(tool-call orchestration, retries, malformed-JSON robustness) is HARD — it is the
product being bought; session persistence + compaction is HARD and empirically
load-bearing (8+ agents through a real machine restart); maintenance is HARD *as a
standing cost center* — every rebuilt row converts into permanent ownership, and this
fleet's own experience shows even *tracking* a third party's fixes (herdr's
slash-strip across 0.7.1→0.7.3) is real recurring work. A custom loop rebuilds all of
that to obtain control that the next paragraph gets for a patch-set. The only thing
build-own uniquely buys — zero upstream to fight — is bought at the price of
*becoming* the upstream for everything.

**(A) Fork opencode: YES, but on a trigger, not on day 1 — because the measured
plugin surface already carries the design.** Everything Build 1 needs is documented
or verified on stock opencode: the pump (all components VERIFIED individually; the
two-phase composition REASONED and the in-TUI composition unrun — `OPENCODE-PLUGIN.md`
§3.7's own scope-honesty, carried, not rounded up), compaction-owned restore (VERIFIED), catalog-level model enforcement
(`agent.transform`, VERIFIED wired), tool-call blocking (VERIFIED), external abort
(DOCUMENTED), system-prompt ownership (VERIFIED). A fork *today* would buy: turn-end
gating (not needed per §3), hook sandboxing (mitigated by the pump's own
catch-discipline), a session-start hook (worked around by the external watcher), and
insurance against upstream drift. Insurance is real — the binary moved mid-
investigation, and two of the load-bearing hooks are `experimental.*` — but insurance
is bought when the premium is due: **pin the version now; fork when the pinned
surface breaks twice or a turn-gate duty materializes — or the third trigger the
operator has now ruled into existence: Build 2 fails on judgment, Build 2.5's stock
levers move it partially but insufficiently, and the remaining named mechanisms are
fork-only (§4b.3's gate — the trigger fires only through the stopping rule, so "try
harder" is bounded by construction; note it is orthogonal to the first two triggers,
which are about upstream stability, not seat capability).** At that point the fork is a
patch-set on a known base — opencode's loop, tools, store, and TUI come along — not a
rewrite. The fork-depth facts (DOCUMENTED — `_hc-ocloop.md` §2): **MIT license, no
CLA — legally forkable**; upstream ships **~1 release per 1.5 days** from a core of
~8 company-affiliated committers — which cuts both ways and must be said honestly:
tracking unpinned stock at that velocity is untenable (the pin is not optional), and
a fork frozen at the pin decays — and not only at the provider edge: **the inherited
HARD rows are a one-time gift, not a permanent endowment.** Every pin-bump cycle
re-imports a fraction of build-own's maintenance burden, proportional to drift since
the pin; a fork held for years converges toward owning its loop layer outright. The
honest statement is that the fork defers build-own's cost and buys the option to
never pay most of it — it does not abolish it. (The provider edge is the best-case
layer: metadata-driven — 11+ wire adapters, a live 166-provider catalog, OAuth
plumbing — exactly what build-own would rebuild from zero.) What a fork uniquely reaches, from source: `session/processor.ts` (the
720-line tool-loop driver — where a turn-end gate would live), `session/llm.ts`
(request assembly), `session/compaction.ts` (the algorithm, not just the prompt),
`session/overflow.ts` (compaction-trigger policy), `session/retry.ts`. Those five
files are the fork's whole value; none is needed for Build 1–3.

**Why not "no fork ever":** the plugin surface's deepest layers are undocumented
(`aisdk.language`) or experimental-prefixed, and `permission.ask` is already a
documented-but-dead type — upstream's respect for this surface is an assumption with
a measured counterexample. The named trigger keeps the decision cheap and the record
honest, per §8 of the philosophy: the convention (pinned stock) first; the machinery
(fork) when the record shows it failing.

---

## 6. COST, MEASURED

The number the reopening said was missing, now measured (`docs/audit/_hc-price.md`;
method: token counts summed from 9 real session transcripts of this swarm's own
agents, costed at current API prices, normalized to **active-hours** — the sum of
inter-message gaps capped at 120s, because calendar-hours overstate by 10–20× for
long-lived scouts; trigger-scout ran a ~9% duty cycle):

- **Status quo, MEASURED:** Sonnet leaves ≈ **$18.86 per active-hour**; Opus seats ≈
  **$59.81 per active-hour**. A 10-agent tree with every agent bursting
  simultaneously ceilings at ≈ **$352/hour** (a ceiling, not a typical draw — the
  duty-cycle correction matters).
- **Mixed tree, ASSUMPTION-FLAGGED:** the same 10-agent tree with GLM-class models
  below a Fable/Opus operator prices at ≈ **$88–258/hour** depending on how much of
  the seat layer stays Claude — *if* foreign token volume per task equals Claude's,
  which is **unmeasured**, and a weaker model could plausibly burn 2–5× the tokens
  for the same task and erase the sticker advantage. §9.6 makes Build 2 measure
  exactly this; no correction factor is guessed here.
- **The constraint that binds today is not dollars:** the fleet runs on a
  subscription seat, and the operator's own journal records *"weekly limit at 82% —
  the swarm's token appetite is real."* There is no published conversion from
  subscription-% to API dollars. Foreign metered tokens bypass that ceiling
  entirely — **the mixed tree is a capacity buy at least as much as a cost cut**,
  and that may be the more honest headline.
- Price-staleness note (the doc corrects its own inputs): FLEET §6's July-2026
  anchor is stale in both directions — current Opus 4.8 is $5/$25 per 1M (not
  $15/$75), and GLM's price *rose* ~40%. Re-verify at build, as FLEET itself said.

**Affordability is a goal argument here — with a limiting principle, because the
review correctly found the unlimited version reusable by any future thrift proposal.**
PHILOSOPHY §1 refuses *token-thrift mechanisms inside the contract* — caches wearing
feature clothes. The human's statement is different in kind: the all-Claude
architecture is too expensive **to exist at the scale the goal requires**. The
limiting principle that keeps this from becoming a universal exemption: the
affordability argument is admissible **only when the operator states an
existence-level constraint** (this system cannot run as needed), **never for a
mechanism-level choice inside a system that runs** — and it licenses re-examining
*architecture*, not weakening any per-decision rule (the ladder's tie-breaks still
refuse thrift; MODEL-FIT §6's "the savings are refused" still governs each spawn).
And the design does not actually need the argument as load-bearing: the fit rule
alone (put the strong model where being wrong is expensive and invisible — *and
nowhere else*) reaches the mixed tree, now that the protocol floor that made it
unsafe is absorbed into the loop. Affordability motivates the reopening;
fit justifies the design.

---

## 7. THE MIXED TREE — one tree, two backends, one contract

The interop question dissolves cleaner than expected, because **swarm's substrate
was never Claude-specific** (FLEET's launcher-seam finding, still true):

- **The queue is files; the journal is files; `ps` reads records.** An opencode agent
  and a Claude agent already share them — `swarm send` writes the same queue file
  either way; the duty loop appends the same journal format; `agents/<name>.json`
  gains a `port` field for opencode agents (one field, `OPENCODE-PLUGIN.md` §5) and
  the doorbell branches: pane-ring for Claude, `POST` for opencode.
- **The pane contract holds:** an opencode TUI in a herdr pane is watchable ground
  truth exactly like a `claude` pane (VERIFIED — the TUI serves and renders).
- **One duty contract, two enforcement implementations** (§3's table) — the parent
  judging a child neither knows nor cares which backend the child runs; it reads the
  same journal, receives the same digests, and reads the same pane.
- **The operator and judgment seats stay Claude** (Fable/Opus) per §4, spawned and
  remodeled exactly as HARNESS.md designed — nothing in this document changes
  avenue 1, the plays mechanism, or the remodel verb; the plays just gain rows.

What does NOT interop: `swarm remodel` across backends remains a migration (journal
is the only carry — HARNESS §6's caveat stands); and foreign agents still get the
clean task, not the Claude duties preamble (the duty loop replaces the preamble's
protocol half; the judgment half travels in the system prompt via `system.transform`).

---

## 8. WHAT THIS RETRACTS FROM HARNESS.md — explicitly

1. **RETRACTED — §2.2's leaf-only ceiling for foreign models** ("Leaf-only for
   foreign models stands on FLEET's evidence and the eval's"). It stood on an
   unowned loop. Under the duty loop it becomes: *leaf-only until Build 2 passes;
   protocol-seat-capable after; judgment seats remain Claude pending evidence.* The
   prior art for this retraction existed before the reopening — `OPENCODE-PLUGIN.md`
   §4 already declared a pump-carried opencode agent "a full participant, not a
   leaf" — and HARNESS.md §2.2 failed to reconcile with it. That miss is mine.
2. **RETRACTED — §3's framing "may not be trusted with report-driven protocols."**
   True of the models; no longer relevant to the design: the protocol is not theirs
   to drop. The judgment caveat in the same sentence stands.
3. **NARROWED — the foreign-seat play's constraints** (artifact-polling parent,
   never wait on reports): superseded by the duty loop if Build 2 passes; retained
   verbatim until then.
4. **CORRECTED — the cost stance.** HARNESS.md §8 priced the changes and never
   priced the status quo; the reopening is right that this was the bill's largest
   omission. §6 above carries it.
5. **STANDS — everything else:** the launcher-seam recommendation (this document is
   more of it, not less), avenue 1 and the mandate, the plays-as-convention ruling
   (§5's "engine never" applied to combo-name schemas — clarified in §2 to not reach
   runtimes), the remodel verb and its gates, the SLM rulings (§7 — the SLM
   forced-call runner is untouched; note the duty loop is *also* the answer to how
   an SLM leaf reports), FLEET's thin runner for one-shots, and the survivability
   gate as repaired post-review. **One standing item must be cross-referenced, not
   silently stood on** (the review caught this list hiding it): HARNESS.md §8's
   last bullet — structural leaf-cannot-spawn for **Claude-family** leaves is a
   known, named, **unbuilt** safety gap, and Build 3 makes the leaf tier more
   populous and more capable while it remains open. Foreign rows are covered by
   construction (toolless runner; `tool.execute.before` denial); Claude cheap
   leaves are not, and a reader of this document alone must know that.

---

## 9. FALSIFIERS

1. **The absorption prediction (§4):** duties-in-loop re-run does not reach 7/7
   delivered reports / zero journal hard-fails → the loop is buggy or the failures
   were never harness-shaped; the retraction in §8.1 un-retracts. *Collector:*
   Build 2, scored on the V3 rubric by a fresh grader.
2. **The judgment layer (§4):** with protocol absorbed, foreign models still sink
   the delegation battery on judgment alone → seats stay Claude; the mixed tree
   remains operator+judgment-Claude over foreign *leaves* only, and the cost case
   shrinks to the leaf layer. *Collector:* same re-run, D2/D4 judgment sub-scores.
3. **Digest signal quality — both failure modes, loud and quiet:** (a) loud: parents
   of duty-loop agents measurably re-open pane-reading for every child because
   auto-digests are noise; (b) quiet, and per the review the likelier one: digests
   become an unread formality — parents rubber-stamp them, and the PHILOSOPHY §2
   concern fires (the loop-crutch atrophied the reporting discipline that
   distinguishes seat-capable models, and nobody noticed because the channel looked
   healthy). Either way absorption failed its purpose and model-authored reports
   (with a Claude-side Stop gate) were load-bearing. *Collector:* parent journals
   after the first live mixed subtree — for (b) specifically: do parent judgments
   ever *cite* digest content, or only artifacts? A judgment stream that never
   quotes a digest is evidence the digests are decoration.
4. **The pinned-stock bet (§5):** an opencode release breaks the pinned plugin
   surface twice, or a duty requiring turn-end gating materializes → the fork
   trigger fires; if the *license* forbids the fork, §5's ruling re-opens toward
   build-own for the loop layer only (keeping provider adapters via LiteLLM-class
   routers). *Collector:* the pin's re-run probes per bump (`_hc-ocloop.md` F1/F3).
5. **The pump composition — RESOLVED, did not fire (2026-07-13):** both named unrun
   compositions were run against a real opencode 1.17.18 TUI executing the shipped
   Build 1 code (VERIFIED — `docs/audit/_hc-build1-verify.md`: codeword round-trip
   proves persistence + a real self-ring turn; the journal's idle-ordering proves
   two-phase `delivered/` marks only after the read-turn). The run also caught and
   fixed a live F3 shared-store collision (94 foreign sessions; `sessions[0]` was
   wrong — now cwd-matched). Build 1 is implemented on `swarm-dev/duty-loop`
   (7 commits, 142 tests), verified by the parent, pending PR + human merge.
6. **The cost premise (§6):** if measured foreign-model token consumption per task
   (which `_hc-price.md` flags as unmeasured) is so much higher than Claude's that
   the per-token advantage evaporates at task granularity, the mixed tree's economics
   collapse and the reopening's premise with it. *Collector:* token-per-task
   comparison from Build 2's re-run cells — the same run answers the capability and
   the cost question.
7. **The registered prior (§4b.4):** it is itself falsifiable, on purpose. If Build
   2.5 flips zero checks, my ~70–80% confidence on F-B/F-C was wrong and the
   inputs-vs-inference decomposition overweighted inputs. If Build 2.6's fork spike
   is what flips the checks, my "the fork is the wrong tool" read was wrong and the
   operator's instrument choice was right, not just his direction. Either way the
   prior is scored against the runs, in the doc, not quietly forgotten.
   *Collector:* Build 2/2.5/2.6 scorecards vs §4b.4, one table, filled as they run.

---

## 10. ADVERSARIAL REVIEW DISPOSITION

Reviewed by `hc-red2` (fresh eyes, refute-brief, Sonnet per the operator's standing
directive; report at `docs/design/LOOP-RED.md`). Verdicts: seat-capability WOUNDED;
fork-vs-build HOLDS (barely); cost section HOLDS (spot-checked clean, including
"capacity buy" — the source's own words); affordability-as-goal WOUNDED; evidence
integrity REFUTED as a discipline claim (8 tags checked, 6 clean, 2 failed — both
failures on load-bearing claims, reproducing the distance-from-source signature
HARNESS.md §10 named).

**All seven repairs folded; none rebutted:**

1. **The retired-evidence citation (the review's best catch):** GLM's "ps misread +
   4-retry hang" was a v2 finding the eval itself retired ("No v2 GLM D2 row should
   be cited again", V3:123-124) — cited in §2/§4 as live judgment evidence. Struck;
   replaced with the live v3 facts (deepseek's detour V3:82-83; GLM's watchdog
   absence as an *unexercised* risk); §4's registered prediction now asks the re-run
   to exercise the dead-child case deliberately. The same defect was found and fixed
   in HARNESS.md §5, where the retired v2 hang had carried the hair-trigger
   argument — a two-document correction from one finding.
2. **The pump's tag:** "verified: self-ring, two-phase delivered/" overclaimed its
   source's own scope-honesty (components VERIFIED; two-phase-as-one-program
   REASONED; in-TUI composition unrun). Fixed in §1 and §5, with the unrun
   compositions as Build 1's first named checks.
3. **Affordability's limiting principle** added (§6): admissible only for
   operator-stated existence-level constraints, never mechanism-level choices; and
   demoted to motivation — the fit rule carries the design.
4. **The fork's decay cost** stated (§5): inherited HARD rows are a one-time gift;
   every pin-bump re-imports drift-proportional maintenance; the fork defers
   build-own's cost, it does not abolish it.
5. **The leaf-cannot-spawn cross-reference** added to §8's STANDS list: Build 3
   widens the leaf tier while a named, unbuilt safety gap for Claude-family leaves
   stands open — a reader of this document alone now knows.
6. **The deepseek pincite** restored, corrected (V3:82-83, not the :84-86 HARNESS.md
   had used).
7. **Falsifier 3 sharpened** to catch the quiet failure (digests as unread
   formality), with a collector that can see it (do parent judgments ever cite
   digest content?).

**What the review could not break, on its own record:** the protocol-absorption
logic itself, the fork-trigger structure, the cost section's method and framing, and
the §8 STANDS list's consistency (no logical contradictions — one omission, item 5).

**Owned, again:** both evidence failures landed in citations into material only I
had read closely. Same signature as HARNESS.md §10. Two reviews, same lesson: this
author's tags into unaudited corners must be treated as OVERSTATED until a second
reader lands on them — which is, of course, exactly the argument for the mandatory
fresh-eyes review that caught them both.

**Third review (`hc-red3`, narrow target: §4b + third trigger + Build 1 quiescence;
report at `docs/design/LOOP-RED3.md`).** Verdicts: quiescence rule REFUTED as first
specified (unbuilt-but-reads-as-shipped, and two healthy-shape misfires); mechanism
list REFUTED as complete (a missed **stock** mechanism — `messages.transform` context
curation, which I had ruled out for delivery and never re-examined for curation);
stopping rule WOUNDED (two of three checks had no scoreable rubric row); M1 WOUNDED
(data half vs instruction half bundled under one confidence); inputs-vs-inference
WOUNDED (the GLM 6/6 evidence is adjacent, not direct); the prior HOLDS barely
(asymmetry flagged). **All repairs folded:** the predicate rebuilt (queue-empty +
no-send + cooldown + content-diff) and corrected mid-flight to the builder before it
shipped the old one; M1b added as a named stock mechanism (F-A confidence 50→60);
F-B revised 70→65 carrying the evidence hedge; the rubric-authoring prerequisite and
the generation-reopening definition added to §4b.3; the unbuilt flag and the prior
asymmetry noted in place. Notably: the review's best finding *strengthens* the
document's own stock-wins prediction — the reviewer found a cheaper lever than the
author's, which is the review system working exactly as intended.

---

*All child evidence folded (`_hc-ocloop.md` incl. fork depth, `_hc-claudeval.md`,
`_hc-price.md`); adversarial review disposed above. No sections pend.*
