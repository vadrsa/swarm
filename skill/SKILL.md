---
name: swarm
description: "Run other Claude sessions as a swarm of subagents to accomplish a goal. Use when the user wants to start a swarm, run agents in parallel, or delegate a larger goal to a team of subagents (triggers: 'start a swarm', 'swarm of agents', 'run agents to do X', 'delegate to subagents'). Requires running inside herdr (HERDR_ENV=1)."
---

# Swarm

The user wants you to run a swarm — spawn other Claude sessions as subagents and
drive them toward a goal. You become one agent in a tree of agents; how you
reach the goal is your call.

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
