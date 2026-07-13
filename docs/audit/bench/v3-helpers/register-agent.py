#!/usr/bin/env python3
"""register-agent.py <SWARM_DIR> <name> <parent> — v3 rig helper (§5a fix).

Registers <name> as a sandbox agent: writes agents/<name>.json (pane-less, so
send's doorbell degrades to the documented "durably queued" note) and creates
its queue dir. SANDBOX ONLY: refuses any SWARM_DIR that looks like a live tree.
This is what makes `swarm send <name>` deliverable-to in the sandbox — the v2
rig's "unknown agent" wall (FLEET-EVAL §5b) falls away.
"""
import json, os, sys, time

root, name, parent = sys.argv[1], sys.argv[2], sys.argv[3]
root = os.path.abspath(root)
if root.endswith("/.swarm") or "/git/" in root and root.endswith(".swarm"):
    sys.exit(f"FATAL: refusing live-looking SWARM_DIR: {root}")
os.makedirs(os.path.join(root, "agents"), exist_ok=True)
os.makedirs(os.path.join(root, "queue", name), exist_ok=True)
rec = {"name": name, "parent": parent, "pane": "", "tab": "", "model": "",
       "cwd": "", "task": "(v3 rig registration — pane-less sandbox agent)",
       "ts": int(time.time() * 1000)}
p = os.path.join(root, "agents", f"{name}.json")
tmp = f"{p}.tmp.{os.getpid()}"
with open(tmp, "w") as f:
    json.dump(rec, f)
os.replace(tmp, p)
print(f"registered {name} (parent={parent}) in {root}")
