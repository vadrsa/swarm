---
name: swarm
description: "Run other Claude sessions as a swarm of subagents to accomplish a goal. Use when the user wants to start a swarm, run agents in parallel, or delegate a larger goal to a team of subagents (triggers: 'start a swarm', 'swarm of agents', 'run agents to do X', 'delegate to subagents') — and also when a project with swarm available (`.swarm/` present or `swarm` on PATH) is handed any goal that decomposes into parallel or delegable parts. Requires running inside herdr (HERDR_ENV=1)."
---

# Swarm

The user wants a goal accomplished by a swarm — other Claude sessions spawned
as subagents, driven toward the goal. You sit in the coordinator's chair, and
**a coordinator delegates by default**: you keep judgment, verification, and
glue; the work itself goes to children. You doing the work is the failure mode.

## The coordinator doctrine

1. **Delegate by default.** If the goal decomposes into parallelizable parts,
   spawn one child per part. If a serial chunk is more than a few minutes of
   work and you are not uniquely positioned to do it, spawn for it too. Doing
   parallelizable work serially yourself is off-track — the time you spend
   grinding is time the tree's shape was wrong.
2. **Reconciliation asks the tree question — grow and shrink.** At every
   reconcile, ask whether the tree still matches the *remaining* work. Could
   what's left be parallelized or delegated — if yes, why are you not
   spawning? Is a harvested child's workstream done — close it, and keep a
   child only if you can name its next task: a keep you cannot name a task
   for is sentiment, not planning. Children owe the same question at their
   own reconciles; that is what makes the tree recursive rather than one
   deep worker.
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
with no args lists the verbs.)
