# PRD 06 — Release & update system

*`RELEASING.md` + `swarm update` + `install.sh` + `bootstrap.sh`.*

## The problem

swarm has no build step and no package registry. `install.sh` symlinks
`~/.local/bin/swarm` **straight into a git checkout**, so "the version that runs"
is literally whatever commit that checkout is sitting on.

That is a genuinely nice property — there is nothing to build, nothing to publish,
and the source you read is the source that runs. It also means updating is
`git checkout <tag>`, and everything hard about releasing this tool follows from
two consequences of that:

1. **A user can be on an arbitrary commit.** If updating is a checkout, nothing
   stops it from being a checkout of anything. The product's answer is that
   `swarm update` moves only between *deliberately tagged* releases.
2. **Updating can break a running swarm.** `.swarm/` state, the hook record
   format, the per-agent settings schema, and `WORLD.md`'s contract are all
   consumed by agents that are *currently alive*. Changing them under a live swarm
   is the breaking-change case this system exists to manage.

## Who uses it

The **operator**, and only the operator. Agents do not update the tool they run
inside. `RELEASING.md` also addresses whoever authors a change — which, in this
project, is usually an agent — and the release-manager role that cuts tags.

## Current behavior

### Versioning

Git tags, `vMAJOR.MINOR.PATCH`, optionally `-rcN`. `RELEASING.md` defines the
bumps, and — unusually and correctly — defines what **breaking** means *for this
tool specifically*:

- The `.swarm/` **state schema** changes such that an in-progress swarm started on
  the old version won't work on the new one.
- A **verb is removed or renamed**, or its flags/output change in a way a caller
  relies on.
- The **hook record format** (`updates/*.json`) changes shape.
- **`WORLD.md`'s contract** changes in a way that invalidates how agents were told
  the world works.

Additive changes — a new verb, a new optional flag, a new record field with a
default — are MINOR.

That last bullet is the interesting one: this project treats a **documentation
contract** as a versioned interface, because the doc is loaded into every agent's
context and is therefore an API.

### How a change lands

`main` is protected. Every change is a PR; **self-merge is allowed, 0 approvals
required.**

```sh
git checkout -b <type>/<short-name>      # feat/… fix/… docs/…
git push -u origin HEAD
gh pr create --base main
gh pr merge --squash --delete-branch
```

### How a release is cut

```sh
git tag -a vX.Y.Z -m "vX.Y.Z — <summary>"
git push origin vX.Y.Z
```

For a MAJOR, the releaser must add a `## vX.0.0` entry to `RELEASING.md`'s
"Migration notes" section describing what changed and what a user must do.

### `swarm update`

`swarm update [--check] [--pre] [--major]`

1. Requires `git` and a `.git` directory at `REPO_ROOT` (the resolved parent of
   `bin/`). Symlinks are dereferenced, so this is the *real* checkout.
2. `git fetch --tags`.
3. Select the target tag in Python, with explicit semver parsing — not
   `git tag -v:refname`, whose ordering is wrong for pre-releases. Sort key is
   `(major, minor, patch, is_stable, pre_identifier)`, where a stable release ranks
   **above** a pre-release of the same version.
4. Without `--pre`, pre-release tags are filtered out entirely.
5. Compare the target's major to the current tag's major. **If it crosses a major
   and `--major` was not given: print a warning, point at the migration notes, and
   change nothing.**
6. `--check` reports and stops.
7. **Refuse if the checkout has uncommitted changes.**
8. `git checkout <tag>` && `install.sh --update`.

`install.sh --update` re-links, re-checks prerequisites (`herdr`, `claude`, `node`,
`python3`), and prints a warning to close any active swarm started on an older
version.

### Install topology

Two paths, and `RELEASING.md` documents the trap:

- **`curl … | sh`** (`bootstrap.sh`) clones to `~/.local/share/swarm` and runs its
  installer. `swarm update` then operates on *that* clone.
- **A dev checkout** (`~/git/swarm/install.sh`) points the symlink there instead,
  and `swarm update` moves *that* checkout's tag — leaving any bootstrap clone
  untouched.

A machine can have both. Whichever your `PATH` resolves is what runs and what
`swarm update` acts on. `install.sh --uninstall` removes the two symlinks and
leaves `.swarm/` state and PATH edits alone.

## Contracts and guarantees

**Guaranteed:**

- `swarm update` only ever moves between **tagged, pushed** releases. Merged-but-
  untagged commits on `main` are invisible to it. To run unreleased `main` you must
  `git pull` a checkout yourself.
- It refuses to run with uncommitted local changes.
- It never crosses a major boundary without `--major`.
- Pre-releases are invisible without `--pre`.
- `install.sh` is idempotent.
- `--uninstall` never touches state.
- Semver comparison is correct for pre-release ordering (stable > rc).

**Best-effort:**

- The post-update compatibility check is a **generic warning**, not a check. It
  cannot scan for `.swarm/` dirs (state is per-project, anywhere on disk), so it
  prints the same advisory on every update regardless of whether anything is at
  risk.

## Edge cases and known limitations

### G1 — breaking changes ship as minor releases, and the guard never fires

This is the most serious defect in the product, and it is worth stating the
evidence rather than the conclusion.

**It has now happened twice, and the second time it was a decision, not an
accident.** v0.6.0 (PR #10) and v0.9.0 (PR #16) are both breaking; both were
classified MAJOR against this document's own criteria; both were released as
MINORs — the second, per its migration note, *"by operator decision, to keep the
1.0 milestone unspent."* A one-off miss is a process bug. A repeated, deliberate
one means the policy the guard implements is not the policy the project follows.
PRs #18 and #21 made the *record* of this honest (see below); neither changed the
mechanism, and no mechanism change is possible while the intent is to keep
shipping breaks below `1.0.0`.

PR #10 (`feat!: durable inbox messaging replaces live-pane swarm send (BREAKING)`)
replaced `swarm send`'s mechanism. Its own PR body says:

> **Semver: MAJOR → v1.0.0** (breaking: send contract change, `.swarm/` gains
> inbox/ + a new hook, WORLD.md contract change). Tagging routed to the
> release-manager, not cut here.

It also wrote a migration note into `RELEASING.md`, still there today:

> ### v1.0.0 — durable inbox messaging replaces live-pane `swarm send`
> **Migrate:** Finish or `swarm close` any active swarm started on a pre-1.0
> version before upgrading…

The tag that was actually cut on that commit is **`v0.6.0`**:

```
v0.5.0 -> feat: add --id <swarm-id> override to list/status/graph (#9)
v0.6.0 -> feat!: durable inbox messaging replaces live-pane swarm send (#10)
```

Two independent failures follow.

**First, the repository documented a release that does not exist. Fixed by
PR #18 (`42a9fbe`).** There is no `v1.0.0` tag, and never was. The
`### v1.0.0` heading was corrected to `### v0.6.0` — the tag that actually
contains the change (`git tag --contains 8e192a4`) — and the note now records
explicitly that no v1.0.0 was ever cut, so a reader who remembers the old heading
is not left wondering. PR #21 later added the parallel `### v0.9.0` note for the
one-swarm-per-project break, which had shipped to `main` with no note at all.

Each note now carries its own warning that `swarm update` will not stop a user
crossing it, and the section preamble states the general rule: *where a note's
version is not `X.0.0`, it is recording exactly that kind of miss.* The record is
now honest. What the record describes is still broken.

**Second, and materially: the `--major` guard is keyed on the tag, not on the
change.** `cmd_update` compares `target_major` to `major_of_current`. Going
`v0.5.0 → v0.6.0` crosses no major boundary, so:

- No warning is printed.
- No pointer to the migration notes is shown.
- `--major` is not required.
- The update applies silently.

So a user sitting on `v0.5.0` with a live swarm runs `swarm update`, is carried
across the exact change the migration note says requires closing the swarm first,
and their running agents — which have no `UserPromptSubmit` inbox hook, because
they were spawned under the old settings schema — **silently stop receiving
messages**. `swarm send` will report success (the file is durably written) and no
agent will ever read it. That is the precise failure mode
[PRD 02](02-inbox-messaging.md) calls G8, arrived at through the update path, with
every safety mechanism intact and none of them engaged.

The guard was built to make this impossible. It did not fire because nothing
connects a PR's self-declared semver classification to the tag that a different
actor later applies. The mechanism is sound; the process around it has no
interlock.

**And the project has now stated, in `RELEASING.md` itself, that it intends to
keep overriding it** — v0.9.0's note records that the release was classified MAJOR
and shipped MINOR to keep the 1.0 milestone unspent, *"the same override that
produced v0.6.0."* Staying below `1.0.0` while pre-1.0 (`0ver`) is a legitimate
choice, and PR #14 notes "pre-1.0, no users." But it cannot coexist with a guard
that keys on the major component: **under `0ver`, `crosses_major` can never be
true, so `--major` is unreachable and the guard is inert for every release this
project will ever make until someone tags a `1.x`.** The migration notes are
carrying the entire safety burden, and a note only protects a user who reads it
before running `swarm update` — which is precisely the user the guard existed to
stop needing.

Two coherent resolutions exist, and this document currently describes neither:
gate on the *declared classification* rather than the tag's major component (so a
`feat!:`/MAJOR-classified change requires `--major` regardless of what it is
tagged), or drop the pretense, tag `1.0.0`, and let semver mean what the guard
assumes. What is not coherent is a guard whose triggering condition the release
process is committed to never producing.

### Other limitations

**The compatibility check cannot check anything.** `install.sh --update` warns
about active swarms unconditionally, because `.swarm/` lives per-project and could
be anywhere. Users will learn to ignore it, which is what happens to warnings that
fire on every run.

**`swarm update` from an untagged commit reports `from (untagged/dev)`** and
`major_of_current` is empty, so `crosses_major` is never set — meaning **a dev
checkout can be moved across a major boundary without `--major`**. The guard
requires a current tag to compare against. `main` currently sits exactly on
`v0.9.0`, so it does not hit this case today; any commit merged on top of it will,
until the next tag. Under the `0ver` policy above the distinction is moot — the
guard cannot fire from a tagged commit either — but the two failures are
independent and would need fixing separately.

**There is no CHANGELOG.** `cmd_update` prints *"Review the CHANGELOG/RELEASING
notes"* when it blocks a major. There is no `CHANGELOG`. The PR bodies are the
change history, and they are excellent — but they are on GitHub, not in the
checkout the user just refused to update.

**Nothing validates that a MAJOR tag has a migration note.** `RELEASING.md` says
the releaser must add one. Nothing checks. Conversely nothing prevents a migration
note for a version that is never tagged, which is how the current state arose.

**`swarm update` cannot roll back.** There is no `swarm update --to vX.Y.Z`. A user
carried across a bad release must `git checkout` by hand in a directory the
installer chose for them.

**A pre-release is not sticky.** A user on `v0.10.0-rc1` running plain `swarm
update` (no `--pre`) is moved to the newest *stable* tag, which would be `v0.9.0` —
i.e. an apparent downgrade. The sort key ranks stable above pre for the *same*
version, but
across versions the newest stable simply wins. Whether this is correct is a
judgment call nobody has made.

## Open product questions

1. **Who owns semver classification, and what reconciles it with the tag?** Today
   an author (usually an agent) declares a bump in a PR body, and a release manager
   later chooses a tag, and nothing connects them. G1 is the result. Options: make
   the PR's `feat!:` / `BREAKING` marker mechanically drive the tag; require the
   release manager to reconcile every PR since the last tag; or accept that the
   operator decides and record the decision somewhere the guard can read.

2. **Is this project pre-1.0 or not?** PR #14 says "pre-1.0, no users" and skips a
   migration path. `RELEASING.md` carries a `v1.0.0` migration note and a major
   guard. These are two different policies. Pick one: either delete the phantom
   note and state that pre-1.0 makes no compatibility promises, or cut `v1.0.0` and
   let the guard start working.

3. **Should the guard key on something other than the tag?** A `BREAKING` marker in
   the tag message, or a version-of-state-schema file in `.swarm/`, would let
   `swarm update` refuse based on *what actually changed* rather than on whether a
   digit incremented. The state-schema-version idea is the stronger one: it would
   also let a running agent detect that its swarm was started on an incompatible
   version, which nothing can do today.

4. **Should there be a CHANGELOG in the checkout?** The tool tells users to read
   one that does not exist, at exactly the moment they have been blocked from
   updating and have no network context.

5. **Should `swarm update` handle the multi-checkout case?** `RELEASING.md`
   explains the trap clearly, which is a documentation fix for a design property.
   `swarm update` knows its own `REPO_ROOT`; it could say which checkout it is about
   to move, and warn if another swarm install exists on the machine.
