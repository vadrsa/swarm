# Product proposals

A proposal is a **decision, pre-made, with its work shown** — a recommendation the
operator can accept or decline outright, never an open question handed back to him.
The shape and the reasoning behind it are in
[PRD 08](../prd/08-product-proposals.md).

Declined proposals stay here. A record that forgets what was rejected cannot show
that the same idea was rejected twice — the same reasoning that keeps resolved
entries in the gap register.

| # | Proposal | Status |
|---|---|---|
| [001](001-self-containedness-standard.md) | Make everything sent to the operator readable by a stranger | proposed |
| [002](002-product-engineering-coordination.md) | Let product and engineering talk directly about facts | proposed |
| [003](003-updates-retention.md) | Bound what `swarm updates` prints, not what the swarm keeps | proposed |
| [004](004-send-quoting-hazard.md) | Stop the docs teaching a message-corrupting quoting habit | proposed |
| [005](005-inbox-read-ack.md) | Notify-and-pull for the inbox — adopt the ack, reject the notification | proposed |
| [006](006-restore-state-injection.md) | `done` should mean done; stop re-injecting finished tasks forever | proposed |

Written by the `product` agent. Delivered to the operator with `swarm send operator`,
which carries the full text — never a path to it.
