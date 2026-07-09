# Releasing & contributing

How changes land in `swarm`, how versions work, and how breaking changes are
managed. Short version: **branch → PR → merge → tag**, and **semver decides what
`swarm update` does**.

## Versioning (semver)

Releases are git tags `vMAJOR.MINOR.PATCH` (e.g. `v0.3.1`), plus optional
pre-releases `vMAJOR.MINOR.PATCH-rcN` (e.g. `v0.4.0-rc1`).

| Bump | When | Example |
|------|------|---------|
| **PATCH** | bug fix, no behavior/contract change | `v0.3.0 → v0.3.1` |
| **MINOR** | new feature, backward-compatible | `v0.3.1 → v0.4.0` |
| **MAJOR** | **breaking** change (see below) | `v0.4.0 → v1.0.0` |

What counts as **breaking** in this tool specifically:

- The **`.swarm/` state schema** changes such that an in-progress swarm started
  on the old version won't work on the new one (e.g. a required field added to
  agent records, a directory layout change).
- A **verb is removed or renamed**, or a verb's flags/output change in a way a
  caller relies on.
- The **hook record format** (`updates/*.json`) changes shape.
- **WORLD.md's contract** changes in a way that invalidates how agents were
  told the world works.

Additive changes (new verb, new optional flag, new record field with a default)
are **MINOR**, not breaking.

## How a change lands

`main` is protected — no direct pushes. Every change goes through a PR (you can
self-merge; 0 approvals required).

```sh
git checkout -b <type>/<short-name>      # feat/… fix/… docs/…
# … make changes, commit …
git push -u origin HEAD
gh pr create --base main
gh pr merge --squash --delete-branch
git checkout main && git pull
```

## How a release is cut

After merging the change(s) for a release:

```sh
git checkout main && git pull
git tag -a vX.Y.Z -m "vX.Y.Z — <one-line summary>"
git push origin vX.Y.Z
```

Pick `X.Y.Z` by the table above relative to the previous tag. For a pre-release,
tag `vX.Y.Z-rc1` (users only get it with `swarm update --pre`).

**When the release is breaking (MAJOR):** add a `## vX.0.0` entry to the
"Migration notes" section below describing what changed and what a user must do
(e.g. "close any active swarm first; old `.swarm/` dirs from vN are not read").
`swarm update` will refuse to cross a major boundary without `--major`, and
points users here.

## How users update

- `swarm update` — moves to the newest **stable** tag **within the current
  major**. Won't cross a major boundary on its own.
- `swarm update --check` — report only, apply nothing.
- `swarm update --pre` — include pre-release tags.
- `swarm update --major` — allow crossing into a new (breaking) major. Users
  should read the matching migration note first.
- `swarm update` refuses if the checkout has uncommitted local changes.

There's no build step — `install.sh` symlinks `~/.local/bin/swarm` straight into
a git checkout, so the version that runs is whatever tag/commit that checkout is
on. `swarm update` just moves that checkout to a new tag (`git checkout <tag>` +
`install.sh --update` to refresh symlinks, re-check prereqs, and warn about state
compatibility). Two things follow from this that trip people up:

- **`swarm update` only moves between _tagged, pushed_ releases.** It fetches
  tags and checks out the newest one; merged-but-untagged commits on `main` are
  invisible to it until someone cuts a tag (see "How a release is cut"). To run
  unreleased `main`, `git pull` a checkout yourself — `swarm update` won't.
- **It acts on the checkout the running `swarm` is symlinked into, and only
  that one.** The `curl … | sh` bootstrap clones into `~/.local/share/swarm` and
  points `~/.local/bin/swarm` there, so `swarm update` updates that clone. But if
  you instead ran `install.sh` from a dev checkout (e.g. `~/git/swarm`), the
  symlink points there and `swarm update` moves _that_ checkout's tag — leaving
  any bootstrap clone untouched. A machine can have both; whichever one your PATH
  resolves to is what runs and what `swarm update` operates on.

## Migration notes

Newest first. One entry per breaking release. Ideally every breaking change ships
in a MAJOR, so that `swarm update`'s `--major` guard stops users on the way in.
That has not always held: v0.9.0 and v0.6.0 below are both breaking changes that
shipped as MINORs, and the guard therefore never fired for either. Where a note's
version is not `X.0.0`, it is recording exactly that kind of miss — read it before
updating past it, because nothing in the tooling will make you.

<!-- Template:
### vX.0.0 — <title>
**Breaking:** <what changed>.
**Migrate:** <exact steps a user must take, e.g. finish/close active swarms,
delete old .swarm/ dirs, re-run install>.
-->

### v0.9.0 — one swarm per project; agent ids are label-derived slugs

> **This breaking change shipped as a MINOR, and `swarm update` will not warn
> you about it.** The `--major` guard only fires when the version's major
> component increments. It did not increment here — v0.8.0 → v0.9.0 is a minor
> bump — so `swarm update` carries users straight across this break with no
> prompt and no pointer to this note. If you are updating from v0.8.0 or
> earlier, this note is your only warning; follow **Migrate** below by hand.
>
> (For the record: this was classified MAJOR against the criteria above and
> released as a MINOR by operator decision, to keep the 1.0 milestone
> unspent — the same override that produced v0.6.0.)

**Breaking:** two changes, either of which alone would be breaking.

*One swarm per project* (`swarm swarms`, `--id`, and `SWARM_ID` are gone):
- The **`swarm swarms` verb is removed.** A project has exactly one swarm.
- **`--id <swarm-id>` is removed** from `list`, `status`, and `graph`, and
  `swarm start --id` is gone — `start` is now an idempotent init that every
  verb performs on first use, so it is never required.
- **`swarm status` no longer returns exit code 3** ("SWARM_ID set but no such
  swarm"). The condition is unreachable under auto-init; the code is retired,
  not reused.
- **`SWARM_ID` is ignored**, not an error: it prints a one-line note to stderr
  and leaves stdout and the exit code untouched. This is deliberate — live
  agents carry `SWARM_ID` baked into their pane environment and cannot be
  changed in place, so erroring would break every running agent's `swarm`
  verbs the moment the CLI is updated.
- **The `.swarm/` layout is flattened**: `.swarm/swarms/<swarm-id>/{agents,state,
  inbox,settings,updates}` and `.swarm/swarms/<swarm-id>/names` move to
  `.swarm/{agents,state,inbox,settings,updates}` and `.swarm/names`. **A swarm
  started on an older version cannot continue on this one** — the new CLI reads
  the flat layout and reports `(no agents)` against an old nested tree, silently
  orphaning `list`/`graph`/`send`/`wait` for every live agent.

*Agent ids are label-derived slugs* (the `a1`/`a2` id scheme is gone):
- `swarm spawn` **prints a slug, not `aN`** — `--label fix-send-race` yields the
  agent `fix-send-race`. Any caller parsing the old id format breaks. The id is
  the filename everywhere: `agents/<id>.json`, `state/<id>.json`, `inbox/<id>/`,
  `settings/<id>.*`, and the `id` field in `updates/*.json` records.
- A name belongs to **one agent for the swarm's entire lifetime**, including
  across `reap`. Uniqueness lives in a new append-only `names` ledger that
  `reap` never prunes.

**Migrate:** finish or `swarm close` any active swarm **before** upgrading — its
agents live in the old nested layout and this version cannot see them. Old
`.swarm/swarms/` dirs are harmless to leave on disk but are not read; nothing
migrates them. New swarms started on v0.9.0 get the flat layout automatically.
Unset `SWARM_ID` in any shell profile or wrapper that exports it (harmless if
you don't, but it prints a note on every verb). Update any script that parses
`swarm spawn`'s output for an `aN`-style id.

### v0.6.0 — durable inbox messaging replaces live-pane `swarm send`

> **This breaking change shipped as a MINOR, and `swarm update` will not warn
> you about it.** The `--major` guard only fires when the version's major
> component increments. It did not increment here — v0.5.0 → v0.6.0 is a minor
> bump — so `swarm update` carried, and still carries, users straight across
> this break with no prompt and no pointer to this note. The guard cannot
> protect anyone crossing v0.5.0 → v0.6.0. It never could. If you are updating
> from v0.5.0 or earlier, this note is your only warning; follow **Migrate**
> below by hand.
>
> (For the record: the change was authored as v1.0.0 and this note was
> originally filed under that heading, but no v1.0.0 was ever cut — the release
> was classified and tagged v0.6.0. `git tag --contains 8e192a4` reports
> v0.6.0 as the first tag containing it. There has never been a v1.0.0 tag.)

**Breaking:** `swarm send` no longer types the message into the target agent's
live TUI pane. It now writes the message to a durable file inbox
(`.swarm/inbox/<agent-id>/*.json`) and rings a best-effort doorbell;
the message is surfaced into the agent's context by a new `UserPromptSubmit` hook
that `swarm spawn` registers (alongside the existing Stop/Notification hooks).
Consequences:
- The `swarm send` **CLI signature is unchanged** (`swarm send <id> "<msg>"`), but
  its contract changed from synchronous-keystroke to **durable-async**: a message
  is *always delivered* to disk, but a busy agent may see it on its next turn
  rather than the instant it is sent.
- The per-agent settings schema and the `.swarm/` layout gained an `inbox/`
  subtree and a `UserPromptSubmit` hook. A swarm **started on an older version**
  has neither, so its running agents cannot receive new-style messages — an
  in-flight old swarm is not compatible with this version.
- The old live-typing helpers (`send_enter_when_settled`, `_prompt_box_content`)
  are removed from the send path.

**Migrate:** Finish or `swarm close` any active swarm started on a pre-v0.6.0
version before upgrading (its agents won't have the inbox hook). New swarms
started on v0.6.0 or later get inbox messaging automatically — no user action
beyond the normal `swarm update`. Old `.swarm/` dirs from prior runs are harmless
to leave on disk but won't receive messages under the new model.

**Note on the path above.** As shipped, v0.6.0 wrote to
`.swarm/swarms/<id>/inbox/<agent-id>/*.json`. The flat `.swarm/inbox/...` path
documented above is the *current* layout: a later change (`0e4d8b7`, "one swarm
per project") removed the swarm-id level entirely. That change is on `main` and
is not in any tag as of this writing, so it is not yet its own migration note.
The path is written in its current form here so that a reader landing on this
note is not sent looking for a directory that no longer exists.
