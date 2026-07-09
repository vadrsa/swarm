# Product requirements — swarm, as built

These documents describe **what swarm is today**, capability by capability. They
are written *as built*: every guarantee stated here was read out of `bin/swarm`,
`bin/swarm-hook.cjs`, `WORLD.md`, or `RELEASING.md`, not out of intent. Where the
code and the docs disagree, that disagreement is recorded as a gap rather than
smoothed over.

Baseline: `v0.8.0` + `main` through PR #14 (`09022aa`).

> **These PRDs describe committed `main` (`09022aa`).** At the time of writing, an
> uncommitted change in the shared working tree removes the swarm-id concept
> entirely. It is not merged, not on a branch, and not in any tag, so it is not
> "as built" — but it invalidates parts of every PRD here and, as it stands,
> breaks the running swarm. See **G12** below. These documents will need a pass
> once that change lands.

## Whose truth wins

`WORLD.md` is the **contract** — it is what every agent reads and therefore what
every agent believes. When these PRDs say something is *guaranteed*, it means
WORLD.md promises it and the code delivers it. When something is *best-effort*,
the code may not deliver it and WORLD.md says so. When the code does not deliver
something WORLD.md promises, that is a **defect**, listed below and in the
relevant PRD.

## The PRDs

| # | Capability | Primary user |
|---|---|---|
| [01](01-agent-lifecycle.md) | Agent lifecycle — spawn, registry, close, reap | Agents (coordinators) |
| [02](02-inbox-messaging.md) | Durable inbox messaging + doorbell | Agents |
| [03](03-checkpoints-continuity.md) | Goal-status checkpoints & continuity | Agents |
| [04](04-reconciliation-loop.md) | The goal-reconciliation loop | Agents |
| [05](05-agent-naming.md) | Agent naming — label-derived slug ids | Agents + operator |
| [06](06-release-and-update.md) | Release & update system | Operator |
| [07](07-herdr-world-integration.md) | herdr + world integration model | Operator + agents |

## Gap register

The onboarding pass that produced these PRDs surfaced twelve issues. They are
restated in context inside each PRD; this is the index. **Severity is product
severity** — how badly the thing a user was promised fails to happen.

Nothing here is fixed by these documents. Implementation belongs to `cos`.

### Critical — a stated guarantee does not hold

**G12. The in-flight swarm-id removal breaks the running swarm, and leaves the
contract doc describing a concept the CLI no longer has.** This is not a defect in
`main`; it is an uncommitted change in the shared working tree, observed while
writing these PRDs. Recording it here because it is the most urgent product issue
open, and because it is invisible in git history.

The change collapses `.swarm/swarms/<swarm-id>/…` to a flat `.swarm/…` and makes
`SWARM_ID` a deliberately-ignored no-op. The reasoning in the code comment is
sound — a running agent has `SWARM_ID` baked into its pane environment and cannot
have it changed, so *erroring* on it would break every live agent. But *ignoring*
it breaks them too, just more quietly:

- Every live agent's registry row, checkpoint, and inbox live under
  `.swarm/swarms/<swarm-id>/`. The new CLI resolves to the flat root.
- Verified against the current swarm: `swarm list` → `(no agents)`;
  `swarm parent` → `no registry entry for 'product'`. Every live agent's
  checkpoint is orphaned at a path nothing reads. The swarm becomes invisible to
  its own tooling the instant the CLI is updated, with no migration and no warning.
- `swarm swarms` and the `--id` override are removed. Both shipped in tagged
  releases (PR #7; PR #9 → `v0.5.0`). By `RELEASING.md`'s own definition —
  *"a verb is removed or renamed"* and *"the `.swarm/` state schema changes such
  that an in-progress swarm won't work"* — this is **twice over a MAJOR**.
- `WORLD.md` (10 references) and `README.md` still teach `swarm-id` and `SWARM_ID`
  as central. WORLD.md is the versioned contract loaded into every agent at
  runtime; `RELEASING.md` classifies a change to it as breaking. Shipping the CLI
  change without it means every agent is briefed on a world that no longer exists.

The change may well be right — one swarm per project is a real simplification, and
auto-init is a genuine ergonomic win. The gap is that it currently has **no
migration path for in-flight swarms** and **no accompanying contract update**, and
G1 below shows this project has already shipped exactly this class of breaking
change under a minor tag once.

**G1. The breaking change shipped as a minor release; the major guard never
fired.** PR #10 replaced live-pane `swarm send` with durable inbox messaging,
classified itself **MAJOR → v1.0.0**, and wrote a `### v1.0.0` migration note
into `RELEASING.md`. It was then tagged **`v0.6.0`**. So: `v1.0.0` does not
exist and the migration note in the repo documents a release that was never cut;
meanwhile a user on `v0.5.0` running `swarm update` is carried across a genuinely
breaking change — an in-flight swarm's agents have no inbox hook and silently
stop receiving messages — with **no `--major` prompt and no pointer to the
migration note**, because the guard keys off the tag's major component and
`0.5.0 → 0.6.0` does not cross one. The entire purpose of the guard was to make
this impossible. Discussed in [06](06-release-and-update.md).

**G2. Agents cannot escalate to the operator.** `WORLD.md` instructs *every*
agent, on finding a gap beyond its authority, to `swarm send` a
GOAL/GAP/EVIDENCE/OPTIONS/ASK escalation **to its parent**. For every agent
directly under the operator — the entire top layer, where scope decisions
actually live — the parent *is* the operator, and `swarm send operator` fails
with `unknown agent: operator`: the operator has no registry entry, no pane, and
no inbox. The escalation path that WORLD.md presents as universal is
unimplemented at precisely the layer that most needs it. The instruction is
issued to every agent regardless. Discussed in [02](02-inbox-messaging.md) and
[04](04-reconciliation-loop.md).

**G3. `swarm checkpoint --context` reads the wrong agent's transcript.** The
reader prefers `$CLAUDE_TRANSCRIPT_PATH`, but `swarm spawn` never sets that
variable on the agent's pane (it sets only `SWARM_DIR`, `SWARM_ID`,
`SWARM_AGENT_ID`, `SWARM_AGENT_LABEL`). So the fallback always runs, and the
fallback globs `~/.claude/projects/*/*.jsonl` — **every project on the machine** —
and takes the most recently modified. An agent asking "how full is my context
window?" is answered with whichever Claude session on the machine wrote last,
which under a live swarm is routinely a sibling. The number is reported without
qualification and agents are briefed to put it in their checkpoint, where a
parent then reads it as fact. Discussed in [03](03-checkpoints-continuity.md).

### Significant — behavior diverges from the documented model

**G4. `swarm close <id> --self` does not validate the agent exists.** The
subtree path dies with `unknown agent: <id>` on a bad id; the `--self` path skips
the check and prints `(nothing to close)`, exit 0. A typo in an id is
indistinguishable from a successfully closed agent.
[01](01-agent-lifecycle.md)

**G5. `swarm reap` frees a pane but leaves the checkpoint, inbox, and settings
files behind, and nothing ever reads them again.** This is deliberate for names
(the ledger is correct and well-reasoned), but the *artifacts* of a reaped agent
become unreferenced garbage: `state/<id>.json` will never be restored from,
`inbox/<id>/` will never be drained. There is no `swarm archive`, no retention
policy, and no verb that surfaces a dead agent's final checkpoint — which is
exactly the artifact a parent is told to judge it by.
[01](01-agent-lifecycle.md), [03](03-checkpoints-continuity.md)

**G6. A dead agent's checkpoint is invisible in every verb.** `swarm graph`
hides the dead by design. `swarm children` shows them (correctly — a dead child
is a re-plan signal). But neither surfaces `state/<id>.json`, and there is no
`swarm checkpoint <id>` read verb at all: `--help` and `--context` are the only
modes. The reconciliation loop tells every parent to "read each child state file
at `state/<child>.json`" — i.e. the loop's central survey step has **no CLI
support** and instructs agents to reach into the state directory by path.
[03](03-checkpoints-continuity.md), [04](04-reconciliation-loop.md)

**G7. Nothing enforces, validates, or ages the checkpoint schema.** `swarm
checkpoint --help` prints a schema; the agent hand-writes JSON to match it. No
verb validates a written checkpoint, and `updated_ts`/`seq` — the two fields that
exist *specifically* to detect staleness — are never read by any code in the
repo. A parent asked to judge whether a child's checkpoint is "fresh" must
compare timestamps by hand, and a checkpoint that is malformed simply fails to
restore (the hook `try`/`catch`es to a silent no-op). Continuity is a duty with a
schema but no instrument.
[03](03-checkpoints-continuity.md)

**G8. Delivery is guaranteed to the inbox, not to the agent.** The durability
claim is exactly true as written — the file is durable — but the *last mile*
depends on the agent taking another turn. An agent that has gone permanently idle
(finished, waiting, never prompted again) has its message sit unread forever;
the doorbell is the only thing that converts a durable file into a delivered
message, and the doorbell is best-effort. `swarm send` exits 0 in this case. A
sender has no way to observe whether the message was ever surfaced: the hook
moves files to `read/` but nothing reports that upward, and read-receipts were
explicitly deferred in PR #10.
[02](02-inbox-messaging.md)

### Minor — sharp edges and unstated limits

**G9. The doorbell scrapes the screen, and the reliability doctrine forbids
that.** `ring_doorbell` greps the pane for a `❯` prompt character to decide
whether text settled and whether the box drained. WORLD.md's central reliability
claim is "the hook firing is reliable; screen-scraping is not" — yet the
near-realtime delivery path is a screen-scrape against a hard-coded glyph of the
Claude Code TUI. It degrades safely (durability is unaffected) but it is a
coupling to another product's cosmetics, and it will break silently on a prompt
restyle.
[02](02-inbox-messaging.md)

**G10. The inbox injection cap silently truncates.** `inbox-check` caps injected
context at 8000 characters and tells the agent "…and N more; full messages in
`inbox/<id>/`" — but by then the *surfaced* messages have been moved to `read/`
and the un-surfaced ones remain, so the pointer is right. The sharp edge is that
a single message longer than 8000 characters is injected in full regardless (the
`injectedCount > 0` guard keeps at least one), so the cap is not a cap on any
individual message. There is no cap on inbox growth at all.
[02](02-inbox-messaging.md)

**G11. `swarm wait` treats `idle` as terminal, and `idle` is a heuristic on a
notification string.** The hook classifies a `Notification` as `idle` vs
`blocked` by regex-matching Claude Code's human-facing notification text
(`waiting for your input`, `is idle`, `permission`, …). A wording change upstream
reclassifies a real permission block as benign idleness, and `swarm wait` returns
it as a stop state. WORLD.md documents `BLOCKED` as "Claude Code itself is
prompting the agent for input" — presented as fact, sourced from a string match.
[01](01-agent-lifecycle.md)

## Open product questions

These are not defects — they are decisions nobody has made yet, surfaced while
writing the PRDs. Each belongs to the operator.

1. **Is the operator a node in the graph?** Today it is a hole: it is the root of
   every tree, it is named as everyone's ultimate parent, and it is the one entity
   that cannot be addressed, cannot be checkpointed, and cannot be reconciled
   against. G2 is the symptom. The fix is a design choice — give the operator an
   inbox (a file the human reads), or change WORLD.md to route top-layer
   escalation somewhere real.

2. **What is a swarm's end state?** There is `close` (keeps state) and `reap`
   (drops registry rows). There is no *finish*: no verb that says this swarm
   reached its goal, no place a swarm's outcome is recorded, and `swarm swarms`
   lists a completed run identically to an abandoned one. Long-lived standing
   agents make this pressing — the current swarm has five agents with no defined
   terminal condition.

3. **Should checkpoint staleness be observable?** `seq` and `updated_ts` are
   written and never read (G7). Either they are load-bearing — and something
   should surface "this child hasn't checkpointed in six cycles" — or they are
   ceremony and should be dropped from the schema.

4. **Who owns semver classification?** PR #10 classified itself MAJOR; the tag
   said otherwise (G1). PR #14 explicitly flagged its own classification as
   arguable and deferred to the operator. Classification currently lives in the
   PR author's judgment and the tag lives with the release manager, and nothing
   reconciles the two. `RELEASING.md` defines the rules but assigns them to
   nobody.

5. **Is "every agent is standing" affordable?** PR #12 gave every agent — including
   one-shot leaves — the full continuity briefing: roughly 40 lines of reconcile
   ritual prepended to every task. The stated rationale is that you cannot predict
   which agents turn out long-lived. That is sound, but the cost is paid per spawn
   in tokens and in first-turn latency, and nobody has measured it.

6. **Does the reconciliation loop actually change behavior, or does it produce
   compliant-sounding checkpoints?** PR #13's verification showed one agent
   honestly concluding OFF-TRACK, which is real evidence. But the loop is
   unenforced by construction, its only output is a self-written status field, and
   the agent grading itself is the agent being graded. There is no measurement of
   how often reconciliation changes a plan versus ratifies it.
