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

Because `install.sh` symlinks into the repo, an update is just a tag checkout +
`install.sh --update` (refreshes symlinks, re-checks prereqs, warns about state
compatibility). No rebuild.

## Migration notes

Newest first. One entry per breaking (MAJOR) release.

<!-- Template:
### vX.0.0 — <title>
**Breaking:** <what changed>.
**Migrate:** <exact steps a user must take, e.g. finish/close active swarms,
delete old .swarm/ dirs, re-run install>.
-->

_(none yet — no breaking releases so far.)_
