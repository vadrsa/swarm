#!/usr/bin/env python3
"""Operator-span middleware — only top-level agents mail the human.

The operator is not in the swarm: it is the human's own tooling, and its job is
to manage its TOP-LEVEL AGENTS. What happens below them is those agents'
concern. This middleware makes that a fact instead of a hope.

    mail to `operator` from a top-level agent   -> PASS (queued as usual)
    mail to `operator` from anyone below        -> RE-ROUTED to its own parent
    everything else                             -> PASS, untouched

Nothing is ever dropped. A report from deeper in the tree goes UP ITS OWN CHAIN,
to the agent whose job it is to read it — which is where the model says it
belongs. That agent judges it and decides what the human needs to hear.

Enable it in .swarm/config:

    [middleware]
    command  = "python3 /path/to/skill-middleware/examples/operator-span.py"
    identity = "span"

Fail-open by design: any crash, timeout, or unreadable state passes the message
through. This protects the human who configures it; it is not a property of the
system. See docs/design/OPERATOR-STRUCTURE.md §4e′.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.realpath(__file__))


def parent_of(root, name):
    """The recorded parent of `name`, or None if we cannot tell."""
    try:
        with open(os.path.join(root, "agents", f"{name}.json")) as f:
            return json.load(f).get("parent") or "operator"
    except OSError:
        return None            # unknown sender: not ours to judge


def main():
    rec = json.load(sys.stdin)                 # {from, to, ts, body}
    if rec.get("to") != "operator":
        return 0                               # not operator mail: pass

    root = os.environ.get("SWARM_DIR") or os.path.join(os.getcwd(), ".swarm")
    sender = rec.get("from") or ""
    parent = parent_of(root, sender)

    # Top-level agents are the operator's correspondents. An unknown sender is
    # NOT refused — an honest unknown beats a confident wrong re-route.
    if parent is None or parent == "operator":
        return 0

    body = (f"[escalated: {sender} tried to mail the operator directly. "
            f"It is below your top layer, so this report is yours to judge. "
            f"Read it, decide what the human actually needs, and pass on only that.]\n\n"
            + (rec.get("body") or ""))
    swarm = os.environ.get("SWARM_BIN") or "swarm"
    try:
        subprocess.run([swarm, "send", parent, "--stdin"],
                       input=body, text=True, timeout=30, check=True)
    except Exception:
        return 0                               # could not re-route: pass, never drop
    return 100                                 # handled: nothing queued for the human


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)                            # fail open, always
