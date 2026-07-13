#!/usr/bin/env python3
"""deliver-next.py <SWARM_DIR> <recipient> [--peek] — v3 rig helper (§5a fix).

The delivery pump: emits on stdout EXACTLY what bin/swarm's deliver hook would
inject for <recipient>'s next turn (header + body via the tool's own
next_delivery/build_delivery — imported, not reimplemented), then moves the
file to delivered/ (the same order deliver_once uses: only after the bytes
drained — here, after a successful stdout write). Exit 4 if the queue is empty.
--peek prints without consuming (for watchdog checks).

This is the harness performing for an `opencode run` model exactly what the
Claude-pane deliver hook performs for a native agent: one message per turn,
oldest first, standard relation header. Byte-fidelity is guaranteed by import.
"""
import importlib.machinery
import importlib.util
import os
import sys

SWARM_BIN = os.environ.get("SWARM_BIN", os.path.expanduser("~/.local/share/swarm/bin/swarm"))
spec = importlib.util.spec_from_loader(
    "swarmmod", importlib.machinery.SourceFileLoader("swarmmod", SWARM_BIN))
sw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sw)

root, name = os.path.abspath(sys.argv[1]), sys.argv[2]
peek = "--peek" in sys.argv[3:]
if root.endswith("/.swarm"):
    sys.exit(f"FATAL: refusing live-looking SWARM_DIR: {root}")

nd = sw.next_delivery(root, name, sw.parents_of(sw.load_agents(root)))
if not nd:
    sys.exit(4)
fn, ctx = nd
if ctx is None:
    sys.exit(f"FATAL: undeliverable head {fn} (hand-crafted oversize?)")
sys.stdout.write(ctx)
sys.stdout.flush()
if not peek:
    os.makedirs(sw.delivered_dir(root, name), exist_ok=True)
    os.replace(os.path.join(sw.q_dir(root, name), fn),
               os.path.join(sw.delivered_dir(root, name), fn))
