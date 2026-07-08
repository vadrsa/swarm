# swarm

Run other Claude Code sessions as a **swarm of subagents** to accomplish a goal.
One agent can spawn others (each a live session in its own [herdr](https://herdr.dev)
tab), delegate work, receive reliable updates, and see the whole graph — and any
subagent can do the same, so the structure nests as deep as the work needs.

No daemon, no MCP, no git assumptions. Just a CLI, a hook, and a world doc the
agents read. The tools give reliable **spawn / send / receive**; the strategy
(how to decompose, delegate, judge, integrate) is the model's.

## What's in here

- `bin/swarm` — the CLI (`world, start, spawn, send, updates, wait, list,
  status, whoami, parent, graph, children, close, reap`).
- `bin/swarm-hook.cjs` — the completion hook each subagent runs (turns its
  Stop/Notification events into reliable update records — no screen-scraping).
- `WORLD.md` — the world every agent reads: the verbs, what the states mean,
  what's reliable, and how work is judged/approved in the graph. Facts, not a
  procedure. Print it with `swarm world`.
- `skill/SKILL.md` — the Claude Code skill that triggers on "start a swarm" and
  points the agent at `swarm world`.
- `install.sh` — wires it into your machine.

## Requirements

`herdr` (the container that holds subagent panes), `claude` (Claude Code CLI),
`node`, `python3`, `bash` — all on PATH.

## Install

```sh
git clone https://github.com/vadrsa/swarm.git
cd swarm
./install.sh
```

`install.sh` is idempotent and:

- symlinks `swarm` into `~/.local/bin/` (put it on your PATH if it isn't:
  `export PATH="$HOME/.local/bin:$PATH"` in your shell rc),
- symlinks the skill into `~/.claude/skills/swarm/` (start a **new** Claude Code
  session afterward so it loads),
- checks that `herdr`, `claude`, `node`, and `python3` are on your PATH.

After installing, verify with `swarm world` (prints the world doc) — if that
works, you're set.

**Update:** run `swarm update` — it moves you to the latest tagged release and
re-runs the installer (`swarm update --check` just tells you if one's available).
It only advances to versions that were deliberately tagged, never arbitrary
commits, and refuses to run if you have uncommitted local changes.

**Remove:** `./install.sh --uninstall` (removes the two symlinks; leaves your
`.swarm/` state and PATH edits alone).

Pre-releases: `swarm update --pre`. Crossing a breaking major version needs
`swarm update --major` — see [RELEASING.md](RELEASING.md) for the versioning
policy, how changes land, and any migration notes.

## Use

Inside a **herdr** pane, in your project directory, start a fresh Claude session
and ask it to run a swarm:

> "start a swarm to build the CSV importer and its tests, max 3 agents"

The `swarm` skill triggers, the agent reads `swarm world`, and drives it —
spawning subagents, monitoring them, judging their artifacts, and following
through. It surfaces only real blockers to you.

Under the hood the agent uses the verbs directly, e.g.:

```sh
SWARM_ID=$(swarm start); export SWARM_ID
id=$(swarm spawn "build the importer" --model opus --label importer)
swarm wait "$id"          # blocks until it reports done/question/blocked
swarm graph               # see the whole living tree
swarm close "$id"         # approve & clean up (closes it + its subtree)
```

## State

Runtime state lives in a `.swarm/` directory in your project (one subdir per
swarm run). It's a paper trail, safe to delete between runs. **Add `.swarm/` to
your project's `.gitignore`** so it isn't committed.

## How it stays reliable

- **Completion is a fired hook event**, not a guess from the screen. `DONE`
  means a turn ended; `QUESTION`/`BLOCKED` mean the agent yielded.
- **The pane and the artifact are ground truth** — a `DONE` isn't proof of
  correctness; work is judged by the deliverable, then approved.
- **Each agent watches only its direct children**; failures route up one hop at
  a time. Dead agents drop out of the graph; the living reparent upward.

## License

Copyright (C) 2026 vadrsa

This program is free software: you can redistribute it and/or modify it under
the terms of the **GNU General Public License v3.0** as published by the Free
Software Foundation. See [LICENSE](LICENSE) for the full text.

It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. Under the GPL, if you distribute a modified version, you must also
release your changes under the GPL.
