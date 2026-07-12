---
name: swarm
description: "Run other Claude sessions as a swarm of subagents to accomplish a goal. Use when the user wants to start a swarm, run agents in parallel, or delegate a larger goal to a team of subagents (triggers: 'start a swarm', 'swarm of agents', 'run agents to do X', 'delegate to subagents') — and also when a project with swarm available (`.swarm/` present or `swarm` on PATH) is handed any goal that decomposes into parallel or delegable parts. Requires running inside herdr (HERDR_ENV=1)."
---

# Swarm

The user wants a goal accomplished by a swarm — other Claude sessions spawned
as subagents, driven toward the goal. You sit in the coordinator's chair, and
**a coordinator delegates by default**: you keep judgment, verification, and
glue; the work itself goes to children. You doing the work is the failure mode.

**You stay the coordinator, here, in this session.** Do not spawn a coordinator
and hand it the tree; do not hand the human a row of workers to drive — the
human manages **one node: you**. (If they'd rather drive the workers themselves,
say so once and do it.) Doctrine 5's "~3" is a *span*, not a licence to leave
the human three children.

**Mine before you spawn.** If this session has already been working, your first
act is not to spawn: read back over what it has been doing — the goal, what is
known, what was learned the hard way, which parts are independent — and write
that decomposition **into your journal** before the first spawn, then brief each
child from it. If you decline to spawn, journal that too, with your reason. If
your context was compacted, read your journal first; if you still cannot answer,
say so and ask — do not guess a tree.

## The coordinator doctrine

1. **Delegate by default.** If the goal decomposes into parallelizable parts,
   spawn one child per part. If a serial chunk is more than a few minutes of
   work and you are not uniquely positioned to do it, spawn for it too. Doing
   parallelizable work serially yourself is off-track — the time you spend
   grinding is time the tree's shape was wrong.
2. **Reconciliation asks the tree question — grow and shrink.** At every
   reconcile, ask whether the tree still matches the *remaining* work and
   whether your span still matches your attention: split what you cannot
   attend, absorb what no longer earns its layer. Could what's left be
   parallelized or delegated — if yes, why are you not spawning? Is a
   harvested child's workstream done — close it, and keep a child only if you
   can name its next task: a keep you cannot name a task for is sentiment,
   not planning. Children owe the same questions at their own reconciles;
   that is what makes the tree recursive rather than one deep worker.
3. **Judge tree shape, not just artifacts.** When you judge a child's work,
   judge its delegation too: a child grinding through parallelizable work
   serially is off-track and should hear it from you.
4. **Restructure freely.** Closing a workstream or subtree to re-form a better
   shape is normal, allowed, and encouraged — the tree is scaffolding, not
   headcount. Nothing of value dies: journals, `delivered/`, and artifacts all
   survive `close`. Two disciplines: HARVEST before you close (read the
   child's journal and artifacts first), and journal the restructure with its
   reason as a falsifier-bearing entry, so it is judgment, not churn. Do not
   fear the tombstone — names are cheap, and burned names are the record
   working as designed.
5. **Attend within your span — and protect the operator's.** You are over
   span when you can no longer name each child's state and the next artifact
   you expect from it without re-reading; if a spawn would take you past
   that, spawn a coordinator and split the stream, and absorb a coordinator
   back (harvest, close, take the survivors) when its stream shrinks to what
   you can hold directly. The operator's span is smaller still: ask them what
   it is (default ~3), then shape the tree so their *direct* load —
   decisions, waiting mail, review items — never exceeds it. The pattern is
   the review desk: hold everything yourself and hand the operator one
   ranked page, never the raw stream.

## The operator seat

A session acting for the human at the root — reading the operator mailbox,
dispatching, judging — is a **hand** on the operator seat. The seat is the
standing thing: one journal (`.swarm/journal/operator.md`), one mailbox, one
set of open loops. Hands come and go, in sequence or in parallel; everything
below is convention in that journal, not tool state.

- **Take the seat before acting.** Write a seat-take entry with a chosen hand
  tag (e.g. `[hand:desk-a]`) — the liveness breadcrumb that a hand exists
  before its first dispatch. Then look before touching: `swarm ps`, the
  operator journal read via a grep idiom (grep for hand tags, dispatch and
  verdict lines — never a bare tail; entries bury), and the mailbox.
- **Journal during the stint,** not only at a graceful exit, and re-read the
  journal before each dispatch. After any restore or compaction, reconcile
  `queue/operator/delivered/` against the journal's claim lines.
- **Dispatch entries and verdict entries.** A dispatch entry carries: the hand
  tag, the name addressed — naming what recurred when you have dispatched to
  that name before ("Task 8 to hardener") — the shape of the work, the
  expected artifact, and off-track-if. When the artifact is judged, write the
  verdict entry: arrived is not done. A dispatch entry with no verdict entry
  is an open loop; open loops belong to the SEAT, and any hand may adopt them.
- **Claim mail, then act.** A hand claims an operator-mail file by moving it
  to `queue/operator/delivered/` AND writing a hand-tagged claim line in the
  operator journal — then acts on it. The claim line witnesses the claimant
  (renames record no mover), and a delivered file with no claim line is the
  alarm: a hand died mid-claim.
- **Standing goals live in the journal, or not at all.** Periodically write a
  `STANDING GOALS` entry — each goal with its falsifier. A restatement MUST
  cite the entry it supersedes: two hands restating without citations lose
  one hand's update silently, and the citation is what makes a crossed write
  detectable — reconcile it, never newest-wins. Read goals via a grep idiom,
  never a tail (entries bury), and let the pattern match entry markers and
  hand tags, never a timestamp format — hands demonstrably write different
  ones. A goal agreed out of band — a pane chat, a human aside — does not
  exist until it is written here.
- **The desk.** Hand the human one ranked decisions page, never the raw
  stream — and declare it derived: regenerable from the journal and the repo
  at any time, never load-bearing.

## Precondition

This needs **herdr** as the container. If `HERDR_ENV` is not `1`, tell the user
you must be running inside a herdr pane, and stop. The `swarm` CLI should be on
your PATH — check with `command -v swarm`; if it's missing, the package wasn't
installed (`./install.sh` in the swarm repo).

## What's available

Run **`swarm world`** — it prints the whole contract: four verbs (`spawn` a
named child, `send` a message that claims one of the recipient's turns, `ps`
the one view of the tree, `close` an agent and its subtree), the journal that
is each agent's continuity, and what is promised (delivered means delivered;
the operator is a mailbox, not a node; nothing tracks obedience — judge
artifacts, never claims). It tells you what exists, not what to do. (`swarm`
with no args lists the verbs.) The two stances above are complete as written;
their reasoning, if a case collides with one, is in
[references/COORDINATING.md](references/COORDINATING.md).
