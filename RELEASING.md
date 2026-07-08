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

Newest first. One entry per breaking (MAJOR) release.

<!-- Template:
### vX.0.0 — <title>
**Breaking:** <what changed>.
**Migrate:** <exact steps a user must take, e.g. finish/close active swarms,
delete old .swarm/ dirs, re-run install>.
-->

_(none yet — no breaking releases so far.)_
