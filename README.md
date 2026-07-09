# swarm

Run other Claude Code sessions as a **swarm of subagents** to accomplish a goal.
One agent can spawn others (each a live session in its own [herdr](https://herdr.dev)
pane), message them, and see the whole tree — and any subagent can do the same,
so the structure nests as deep as the work needs.

The tool is one Python file with four verbs — `spawn`, `send`, `ps`, `close` —
plus `swarm world`, which prints the whole contract. Everything it stores is a
fact a file can witness; strategy (how to decompose, delegate, judge) is the
model's. Read [WORLD.md](WORLD.md) for the contract itself and
[docs/design/SIMPLEST.md](docs/design/SIMPLEST.md) for why it is shaped this way.

## What's in here

- `bin/swarm` — the tool. One file; it is also its own Claude Code hook
  (delivery, events, restore are wired automatically at spawn).
- `WORLD.md` — the contract every agent reads. Print it with `swarm world`.
- `skill/SKILL.md` — the Claude Code skill that triggers on "start a swarm".
- `install.sh` — wires it into your machine. `docs/` — philosophy and the
  dated design record.

## Requirements

`herdr` (the container that holds subagent panes), `claude` (Claude Code CLI),
`python3` — all on PATH.

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/vadrsa/swarm/main/bootstrap.sh | sh
```

This clones swarm into `~/.local/share/swarm` and runs its installer; re-running
the same command updates it. Override the location with `SWARM_HOME=...`.
(Piping a script to `sh` runs code you haven't read — if you'd rather review it
first, use the manual install below.)

**Manual install** (also the right choice if you want to hack on swarm):

```sh
git clone https://github.com/vadrsa/swarm.git ~/git/swarm
~/git/swarm/install.sh
```

`install.sh` is idempotent: it symlinks `swarm` into `~/.local/bin/`, symlinks
the skill into `~/.claude/skills/swarm/` (start a **new** Claude Code session
afterward so it loads), and checks the prerequisites. Verify with `swarm world`.

**Remove:** `./install.sh --uninstall` (removes the two symlinks; leaves your
`.swarm/` state and PATH edits alone).

## Use

Inside a **herdr** pane, in your project directory, start a fresh Claude session
and ask it to run a swarm:

> "start a swarm to build the CSV importer and its tests"

The skill triggers, the agent reads `swarm world`, and drives it — spawning
named subagents, judging their artifacts, and reporting to you. Messages to
`operator` are your mailbox: `swarm ps` shows them waiting, with the live tree
underneath.

State lives in your project's `.swarm/` directory (queues, journals, one
event fact per agent). It is a paper trail, safe to delete between runs — add
`.swarm/` to that project's `.gitignore`.

## License

Copyright (C) 2026 vadrsa

This program is free software: you can redistribute it and/or modify it under
the terms of the **GNU General Public License v3.0** as published by the Free
Software Foundation. See [LICENSE](LICENSE) for the full text.

It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. Under the GPL, if you distribute a modified version, you must also
release your changes under the GPL.
