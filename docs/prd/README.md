# Product requirements — swarm, as built

These documents describe **what swarm is today**, capability by capability. They
are written *as built*: every guarantee stated here was read out of `bin/swarm`,
`bin/swarm-hook.cjs`, `WORLD.md`, or `RELEASING.md`, not out of intent. Where the
code and the docs disagree, that disagreement is recorded as a gap rather than
smoothed over.

Baseline: `main` through PR #31 (`08f683b`). Newest tag: **`v0.9.0`** — `main` is
ten commits ahead of it, carrying four code fixes (PRs #23, #24, #25, #31). That tag is
itself a breaking change released as a minor, by decision (see G1).

> **The swarm-id concept is gone.** PR #16 made the project *be* the swarm: one
> swarm per project, rooted at `.swarm/`, no id to mint, every verb auto-creating
> its layout on first use. `swarm swarms` and the `--id` override are removed;
> `SWARM_ID` is deliberately ignored rather than an error. These PRDs are written
> against that model. The prior model (`.swarm/swarms/<swarm-id>/`, an exported
> `SWARM_ID`) survives only where it explains a live hazard — see **G12**, which
> is now about the *cutover*, not the code.

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
| [08](08-product-proposals.md) | Product proposals — how product reaches the operator | Operator + product |

The principles these capabilities were built on are recorded, with their evidence, in
[PHILOSOPHY.md](../PHILOSOPHY.md). Live proposals are in [docs/proposals/](../proposals/).

## Gap register

The onboarding pass that produced these PRDs surfaced thirteen issues; five more
(G14–G18) were found later, in use. They are restated in context inside each PRD;
this is the index. **Severity is product severity** — how badly the thing a user was
promised fails to happen.

Nothing here is fixed by these documents. Implementation belongs to `cos`.

**Status as of `08f683b`:** of the original four critical gaps, three are closed — G2
by PR #20, G3 by PR #19, and G12 by the operator sequencing the cutover. G1 is
half-closed: the phantom note was corrected (#18) and v0.9.0 got a migration note
(#21), but the guard that was supposed to make the miss impossible still cannot fire
on a minor bump — and cannot, while the milestone is preserved by policy. **G13 is a
decided no-op, not an open request** (see its entry). Closed gaps are kept below under
[Resolved](#resolved), not deleted: a register that forgets what was broken cannot
show that the same class of thing broke twice.

**G17 — message loss above ~64 KB — was filed, fixed, and installed the same day**
(PR #31). It was the only entry where a guarantee `WORLD.md` states in plain words was
provably false. It is now under [Resolved](#resolved), with its verification.

Five gaps were added *after* the onboarding pass, none of them visible by reading the
code: **G14** (a message can be silently corrupted by the caller's shell), **G15**
(`swarm updates` prints unbounded history), **G16** (reading the operator's mail
destroys it), **G17** (the delivery hook destroyed any message over ~64 KB — resolved),
and **G18** (`restore-state`'s injection grows every cycle, uncapped).

**Three entries here are corrections against the people who wrote them**, and that is
the point of keeping them:

- PR #24 fixed a case where `reap` *could* free a name — a guarantee `WORLD.md`, three
  code comments, and [PRD 05](05-agent-naming.md) all asserted held. It did not.
  Engineering found it; product had asserted it. **Four sources of documentation cannot
  corroborate one another.**
- G16 originally carried a second claim — that the inbox header's acknowledgement is
  *silent* — which was **wrong**, and which `cos` refuted by running the fixture rather
  than trusting a sibling who had been right three times running. Chasing that refutation
  is what uncovered G17. Product asserted a defect from reading; engineering disproved it
  by executing; executing found a real one. The retraction is kept in place.
- **G18 corrects both of us.** Product told `cos` that three sibling agents were carrying
  truncated missions — inferred, never checked; `cos` verified before acting and found all
  four intact, so nothing was dispatched. `cos` in turn justified the `restore-state` half
  of the G17 fix with *"my checkpoint is 38,883 bytes and grows"* — true of the file,
  misleading about the payload, which is 3× smaller because `progress` fields are not
  injected. The fix was right; the reasoning for it was not, and the **real** unbounded
  quantity turned out to be task and thread *count*. Both errors were caught the same way.

The method that produced every one of G14–G18, and caught every error in this list:
**run the code against a fixture; do not assert a guarantee from a document — including
your own, and including one a trusted sibling hands you.**

### Critical — a stated guarantee does not hold

**G13. Every agent shares one working tree, and nothing says so.** `swarm spawn`
defaults `--cwd "$PWD"`. In the swarm that produced these PRDs, **eleven agents
shared a single git checkout.** Git branch, index, and checkout state are global
to a working tree, so any two agents that touch code can silently destroy each
other's uncommitted work — `git checkout`, `git stash`, and `gh pr merge
--delete-branch` all move state out from under whoever else is editing.

This is not hypothetical. While one agent had an uncommitted rewrite of
`bin/swarm` in the tree, another (the author of these PRDs) committed and merged a
PR in the same tree; the uncommitted work vanished, and because it had never been
staged, git retained no blob to recover it from. It was reconstructed only because
its author still held it in context.

There is no worktree isolation, no clone-per-agent, no locking, and **`WORLD.md`
never warns that agents share a checkout** — while telling every agent it has full
autonomy and that *"nothing is merged, committed, or closed for you."* Agents are
handed unrestricted git and told nothing about who else is holding it.

**Re-verified after the v0.9.0 cutover:** the swarm was closed and restarted fresh,
and all five agents of the new generation again have `cwd=/Users/vadrsa/git/swarm`.
Nothing about starting over changes this — `--cwd "$PWD"` is the default, so the
hazard is reintroduced by every swarm at birth unless a coordinator opts out
per-spawn. This is the sense in which G13 is the last *live* critical gap: the
other three were fixed or sequenced away, and this one silently reset.

`git worktree` already solves this: N working trees off one repository, each with
independent branch and index state, at the cost of one `--cwd` at spawn.
Discussed in [07](07-herdr-world-integration.md).

> **The operator has decided this, twice, and the decision is "no."** Asked directly —
> *"working-tree isolation — your earlier no-op call ('not swarm's job') just cost
> flat-layout its uncommitted work. Revisit?"* — he answered **"Keep the original no-op
> entirely."** It is a considered scope call (isolation is the coordinator's job at
> spawn, not the tool's), made with the data loss already on the table, not an
> oversight.
>
> This entry therefore stays in the register as a **standing hazard, not an open
> request.** Product does not re-raise it. What the register records is the evidence:
> the default reintroduces it at every swarm's birth, and agents that write code should
> be spawned with an explicit `--cwd`. Re-escalating a settled call is the anti-pattern
> the delegation audit names, and [PHILOSOPHY.md](../PHILOSOPHY.md) records the decision
> under *"What this philosophy is not."*

**G1. A breaking change can still ship as a minor release, and the major guard
still cannot fire.** *Partially addressed — the record was corrected, the
mechanism was not.*

PR #10 replaced live-pane `swarm send` with durable inbox messaging, classified
itself **MAJOR → v1.0.0**, and wrote a `### v1.0.0` migration note into
`RELEASING.md`. It was then tagged **`v0.6.0`**. PR #18 corrected that phantom
note to `### v0.6.0` and recorded that no v1.0.0 tag ever existed; PR #21 added
the parallel `### v0.9.0` note for the one-swarm-per-project break. Both notes
now say, in the note itself, that `swarm update` will *not* warn a user crossing
them.

That is the fix for the *record*. The **defect is unchanged**: `swarm update`'s
`--major` guard keys off the tag's major component, so `0.5.0 → 0.6.0` and
`0.8.0 → 0.9.0` both carry a user straight across a breaking change with no
prompt and no pointer to the note that was written for them. Two breaking
changes have now shipped as minors, both by operator decision to keep the 1.0
milestone unspent. **A guard that a release process routinely routes around is
not a guard**, and honest documentation of that fact is not a substitute for
one. Discussed in [06](06-release-and-update.md).

The minor tag is **not drift.** Asked point-blank whether to spend the milestone —
*"release-mgr recommends v1.0.0 (genuine MAJOR, proper migration note). You previously
preserved the 1.0 milestone deliberately — spend it now?"* — the operator answered
**"Go with 0.9.0."** Preserving `1.0.0` as a stability *signal* rather than a version
*counter* is a coherent position ([PHILOSOPHY.md](../PHILOSOPHY.md) §7). What is not
coherent is holding that position while shipping a guard whose triggering condition
the policy guarantees will never occur. **The gap is between the policy and the
mechanism, and only one of them can survive.** That choice is the operator's, not
`cos`'s — the guard cannot be fixed into relevance while the policy stands.

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
[01](01-agent-lifecycle.md), [03](03-checkpoints-continuity.md) ·
the missing `swarm archive` is proposed in [proposal 003](../proposals/003-updates-retention.md)

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

**G14. A message can be silently corrupted before the tool ever sees it, and every
example we ship teaches how.** `swarm send`'s body is documented with double quotes
in all four places it appears (`WORLD.md` ×2, the usage string, the help text). In a
double-quoted shell string backticks are evaluated — so an agent writing markdown,
which is every agent, that sends `` the `wait` verb blocks `` transmits `the  verb
blocks`. The word is deleted and `wait` is executed.

Observed, not theorized: `cos` lost the two subjects of a sentence in a message to
`product`, caught it, and resent. `cmd_send` itself is correct (the body reaches
Python as an env var under a quoted heredoc); the corruption is strictly upstream, in
the caller's shell, where nothing can detect or recover it. **`spawn` already solved
this problem** — it writes the task to a file precisely because a quote-heavy prompt
re-parsed through a shell breaks — and the reasoning was never carried across to
`send`. Delivery is guaranteed; body integrity is not, and no document says so.
[02](02-inbox-messaging.md) · [proposal 004](../proposals/004-send-quoting-hazard.md)

**G18. `restore-state` has no cap, injects finished work forever, and calls it "CURRENT
TASKS".** `inbox-check` budgets its injection at 8,000 characters (imperfectly — see G10).
`restore-state` budgets nothing. It injects the agent's mission, every task **title**,
every **blocker**, and every **`open_threads`** entry, joined without limit — and it prints
the task list under the heading `CURRENT TASKS:` while including `[done]` ones. Across the
live roster, **68% of all injected task-line bytes are finished work** (`rd` 91%, `audit`
88%, `cos` 72%).

Two agents (`cos`, `release-mgr`) independently hand-compacted their own checkpoints in one
cycle before anyone noticed this was structural rather than a personal hygiene failure.

**A schema defect sits underneath it.** The naive fix — drop `status == "done"` tasks —
would silently delete continuity entries, because a `done` task can carry a live blocker.
`cos` found this by testing the fix against the live roster before proposing it, and
declined to decide. Scanning every checkpoint in the org, the state occurs **twice, both in
`product`**, and `product`'s own `t9` encodes the same situation correctly as `blocked`. So
the trap existed only because one agent misused `status`; repairing the data (done, this
cycle) makes the simple filter correct and loses nothing. **A permanent code exception to
rescue two malformed records is how a schema rots.** Proposed in
[006](../proposals/006-restore-state-injection.md).

Those fields only ever grow. Nothing in `bin/swarm` or the hook prunes, caps, or ages
them; the seed writes `"open_threads":[]` and it is append-only by convention thereafter.
Measured on the live swarm:

| Agent | Cycles | Tasks | Open threads | Checkpoint on disk | `restore-state` injects |
|---|---:|---:|---:|---:|---:|
| `cos` | 7 | 17 | 25 | 46,118 B | **15,415 B** |
| `product` | 3 | 9 | 8 | 8,908 B | 4,936 B |

The 3× gap between file size and payload matters, and it corrects a natural misreading:
`restore-state` does **not** inject the `progress` fields, which are the bulk of a
checkpoint. So a 46 KB checkpoint is not a 46 KB injection, and `cos` had ~4.3× headroom
to the old cliff rather than being on its edge. **The risk was never checkpoint bytes; it
is task and thread *count*.** Empirically the payload crosses 64 KiB at roughly **700
tasks** or **300 open threads** — implausible for a short-lived child, entirely plausible
for a standing agent that accumulates a thread per finding and never closes one.

Since PR #31 this can no longer *destroy* the restore (the drain fix landed), which is the
right outcome: an oversized payload now arrives whole. But it arrives into a finite context
window, on **every** `SessionStart`, and the continuity mechanism's own cost therefore rises
monotonically with an agent's age. An agent restored after a compaction pays for every
thread it has ever opened.

**Decomposed exactly** (`cos`'s 12,515-byte injection, measured against the installed hook):

| component | bytes | behaviour |
|---|---:|---|
| preamble + mission + reconcile ritual | 3,207 | irreducible |
| `open_threads` | 6,904 | bounded by discipline |
| task lines | 2,404 | — |
| *…of which finished work* | *1,801* | **grows forever, never shrinks** |

That decomposition inverts the obvious priority, and a later ablation across the whole roster
found a **third** bucket hiding in `progress_summary` — the one nobody reclaims:

| bucket | reclaimable? | do agents reclaim it? | injected |
|---|---|---|---|
| `open_threads` | yes | **yes** — closing a thread visibly frees bytes | joined, unbounded |
| **`progress_summary`** | **fully** | **no** | **verbatim, 1:1, forever** |
| finished tasks | **no** | cannot | title + status + blockers |
| *task `progress` bodies* | *n/a* | *n/a* | **never — free at any size** |

`progress_summary` is 33% of `product`'s payload and 34% of `rd`'s, and nobody prunes it
because **the reconcile ritual instructs every agent to write its reconciliation there.**
Every agent that has ever reconciled is 15–46× the schema's own 44-character hint; the only
one at 1× never reconciled. That is the ritual working as told, into a field re-injected
verbatim for the agent's life.

So the decision splits three ways, and only one part needs code:

- **`open_threads` → a closing discipline.** Not a cap: a blind cap drops the oldest entry
  and the oldest entry is the mission.
- **`progress_summary` → a habit nobody has.** Write the *verdict*; put the *narrative* in the
  finished task's `progress` body, which is durable and free. Product demonstrated it on
  itself: injection fell 4,043 → 2,806 bytes **while the file grew**.
- **Finished tasks → a filter.** Durable in the file, pointless in the injection, and
  reachable by no agent action at all.
[03](03-checkpoints-continuity.md) · [proposal 006](../proposals/006-restore-state-injection.md)

**G16. Reading the operator's mail destroys it — including `swarm updates --json`.**
`cmd_updates` prints, flushes, then calls `mark_read()`, which moves every surfaced
message into `read/`. It does this on the `--json` path too, *before* exiting. So any
script that polls `swarm updates --json` silently consumes the operator's escalations
and leaves nothing in the terminal for the human. Found by `rd`; the fix is held by
`cos` pending a decision on read semantics.

> **Retraction.** This entry originally carried a second claim: that the injected inbox
> header announces more messages than it shows, and that the product therefore performs
> *silent* cumulative acknowledgement. The first half is literally true — the header is
> built from `unread.length` while the loop injects `injectedCount` — but the conclusion
> was wrong, and `cos` disproved it by running the fixture rather than accepting it. The
> hook emits `…and N more; full messages in inbox/<id>/` whenever anything is withheld,
> unconditionally. **The acknowledgement is not silent; it is announced.** This document
> even quoted that line in G10 while the register asserted its absence two sections away.
>
> What survives is a copy improvement, not a defect: `Showing 3 of 5 new messages` names
> what *was* shown rather than only what was withheld. Filed as that, and nothing more.
>
> Kept rather than deleted, because the register's premise is that a record which forgets
> what was wrong cannot show how it was wrong. Product asserted a defect from reading;
> engineering refuted it by executing. The same method then found G17.

**G15. `swarm updates` prints the entire history of the swarm, every time.**
`cmd_updates` iterates the event directory, filters only by `--id`, and prints every
record it finds. There is no limit, no default window, and no pagination. Since the
one-swarm-per-project change the directory is **repo-lifetime**, so the output grows
without bound for as long as the repository lives.

Measured here: 27 records / 108 KB after one generation of five agents; a prior
per-run directory holds 216 from a single run. Extrapolated, 200 generations is 21 MB
on disk — irrelevant — but at ~255 bytes of *formatted output* per record (measured by
`cos`), **~1.4 MB of text dumped unpaginated into a terminal or an agent's context
window** by the operator's only inbox verb.

The framing matters, because this gap has been rediscovered three times as a *disk*
problem and it is not one. Every structural reader is already bounded: `wait` wants an
agent's newest record; `status`/`graph`/`children` want the newest per agent. Only
`updates` wants history, and only `updates` degrades. The read *cost* was fixed in
PR #25 (filename-only scan, ~46×); the unbounded *output* was not.
[01](01-agent-lifecycle.md) · [proposal 003](../proposals/003-updates-retention.md)

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

### Resolved

Kept, not deleted. Each entry states what was broken, what fixed it, and — where
the fix left something behind — what it did not fix.

**G17 — a message over ~64 KB was silently destroyed on delivery. Closed by PR #31
(`08f683b`), fixed and installed the same day it was filed.**

Both of the hook's stdout writes now route through `emitAndExit()`, which waits for the
drain callback before exiting. The bug was that `process.exit(0)` discarded whatever
`process.stdout.write()` had queued when the 64 KiB pipe buffer filled — and the message
was renamed into `read/` regardless, so it was consumed without ever being delivered.

**Verified independently by product against the installed hook**, not taken on report:

| Case | Result |
|---|---|
| 400 KB message | 400,264 bytes received, parses, correctly acked |
| Reader vanishes mid-write (`EPIPE`) | message stays **unread**, survives for retry |
| Capped multi-message path | unchanged: 5 announced, 3 shown, 3 acked, 2 remain |

The second row is the one worth dwelling on. `cos`'s *first draft* ran the `read/` rename
unconditionally once the drain callback fired — but under `EPIPE` that callback fires
**with an error**, the bytes never landed, and the message would have been acked anyway.
It caught this with a test rather than shipping it: *"I had reproduced the original bug in
a new costume."* The ack is now conditional on delivery (`done(!err)`), which is what the
emit-before-mark ordering always meant. **Failing toward re-injection is the safe
direction**, and the fix now says so in code rather than in a comment.

*What it did not fix:* nothing bounds what the hook tries to write. The drain fix means a
fat payload now *arrives* instead of being destroyed — strictly better, and it converts a
correctness bug into a context-budget one. See **G18**, and G10's uncapped first message.

*Provenance worth keeping:* three agents had been over this file — `rd` filed a finding on
it, a child of `cos` rewrote `lastRecordedState()` inside it, and `cos` reviewed that diff
line by line. **None of them saw a 64 KiB cliff sitting under a `process.exit()`.** It
surfaced only because product filed a *wrong* claim (G16), `cos` refuted it by execution,
and chasing *why* product had been wrong put someone back in front of the hook with a
fixture. The method found the bug; no amount of reading had.

**G2 — agents cannot escalate to the operator. Closed by PR #20 (`1892806`).**
The operator is now an addressable target: `swarm send operator "…"` writes a
byte-for-byte ordinary inbox message to `.swarm/inbox/operator/`, skipping only
the registry guard and the doorbell (it has no pane to ring). The human reads it
by running `swarm updates`, which drains that inbox when the caller is the
operator (`SWARM_AGENT_ID` unset) and marks messages read by moving them to
`inbox/operator/read/`, mirroring the agent hook's semantics exactly. Unknown
ids still fail hard: `swarm send bogus-id` → `unknown agent: bogus-id`
(verified). WORLD.md was updated in the same commit, so the escalation chain it
describes now terminates at a real mailbox.

*What it did not fix:* the operator is a mailbox, not a node. It has no pane, no
doorbell, and no notification — an escalation sits unread until the human
happens to run `swarm updates`. G8 (delivery is guaranteed to the inbox, not to
the recipient) therefore applies to the operator **most sharply of all**, since
the operator is the only recipient with no hook to surface its mail. See
[02](02-inbox-messaging.md).

**G3 — `swarm checkpoint --context` reads the wrong agent's transcript. Closed
by PR #19 (`5e5f545`).** `swarm-hook.cjs` now persists `transcript_path` — which
Claude puts on every hook payload — to `state/<id>.transcript` before its verb
dispatch, so the pointer exists from an agent's first hook and is re-recorded by
every subsequent one. `--context` resolves by identity (`$CLAUDE_TRANSCRIPT_PATH`,
else `state/$SWARM_AGENT_ID.transcript`) and the machine-wide glob is gone. When
nothing is recorded it prints `{}` and explains why on stderr rather than
reporting a sibling's number. Verified live: five sibling `.transcript` pointers
exist and `--context` returns the calling agent's own session.

The fix's real lesson is one the PRDs should keep: **a project-scoped glob would
not have worked either.** Every agent in a project shares one
`~/.claude/projects/<slug>/` directory, so no path heuristic can tell two
siblings apart — only an identity the harness hands you can. See
[03](03-checkpoints-continuity.md).

**G12 — the swarm-id cutover was unsequenced. Closed by the operator, not by
code.** The cutover has happened: the installed CLI resolves the flat `.swarm/`
root, and the swarm running against it is healthy (`swarm list` shows its agents
under the new layout). The safe order this register prescribed — finish or
`swarm close` every live swarm, advance the checkout, start fresh — was followed
by hand. Pre-cutover agents were closed; the current generation was started
fresh, so no live agent carries a stale `SWARM_ID`. PR #21 wrote the `### v0.9.0`
migration note that was missing.

*What it did not fix:* **nothing in the tool enforced or stated that order, and
nothing does now.** The cutover was survived by an operator who had been told
what to do, in a register that will not be read by the next person to advance a
checkout past a state-schema change. There is still no migration step, no
`.swarm/` schema version, and no check that a running agent's layout matches the
CLI's. The next such change will present exactly this hazard. This is the same
root cause as G1 — the release system relies on people reading notes — and the
two should be resolved together.

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
   reached its goal, and nowhere its outcome is recorded. PR #16 sharpened this
   rather than settling it — now that the project *is* the swarm, a swarm has no
   lifecycle distinct from the repository's, and the `.swarm/` dir accumulates
   every agent that ever ran there. Long-lived standing agents make it pressing:
   the current swarm has eleven agents and no defined terminal condition.

3. **Should checkpoint staleness be observable?** `seq` and `updated_ts` are
   written and never read (G7). Either they are load-bearing — and something
   should surface "this child hasn't checkpointed in six cycles" — or they are
   ceremony and should be dropped from the schema.

4. **Who owns semver classification?** PR #10 classified itself MAJOR; the tag
   said otherwise (G1). PR #14 explicitly flagged its own classification as
   arguable and deferred to the operator. PR #16 is a `feat!:` that removes two
   shipped verbs and changes the state layout, merged untagged with no migration
   note. Classification lives in the PR author's judgment, the tag lives with the
   release manager, and nothing reconciles the two. `RELEASING.md` defines the
   rules and assigns them to nobody.

5. **Should an agent get its own working tree?** G13 is a design gap, not a bug:
   `--cwd` exists and defaults to sharing. Making code-writing agents spawn into a
   `git worktree` would give each independent branch and index state for the cost
   of one flag. The counter-argument is that agents collaborating on one change
   *want* a shared tree — which is true, and is exactly why the choice should be
   explicit rather than defaulted.

6. **Is "every agent is standing" affordable?** PR #12 gave every agent — including
   one-shot leaves — the full continuity briefing: roughly 40 lines of reconcile
   ritual prepended to every task. The stated rationale is that you cannot predict
   which agents turn out long-lived. That is sound, but the cost is paid per spawn
   in tokens and in first-turn latency, and nobody has measured it.

7. **Does the reconciliation loop actually change behavior, or does it produce
   compliant-sounding checkpoints?** PR #13's verification showed one agent
   honestly concluding OFF-TRACK, which is real evidence. But the loop is
   unenforced by construction, its only output is a self-written status field, and
   the agent grading itself is the agent being graded. There is no measurement of
   how often reconciliation changes a plan versus ratifies it.
