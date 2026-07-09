# PRD 05 — Agent naming

*Label-derived slug ids, unique for the swarm's lifetime. Landed as PR #14.*

## The problem

Agents were named `a1`, `a2`, `a3`. Two things were wrong with that, one cosmetic
and one a correctness bug.

**The cosmetic one:** `a7` tells a reader nothing. A coordinator holding a graph of
twelve agents, and a human reading a paper trail six hours later, both need to know
what an agent *was for* without a lookup. A separate `--label` field existed, which
meant every id had a shadow name and readers had to carry both.

**The correctness one, which is the real reason this PR exists:** id allocation
scanned `agents/a$n.json` for the first free slot. `swarm reap` deletes exactly
those files. So reaping `a3` **freed the name `a3`**, and the next spawn took it —
while `state/a3.json`, `inbox/a3/`, `settings/a3.*` and every `updates/` record
bearing `id: "a3"` *survive reap*. Two different agents, with different missions
and different work, silently merged into one identity across every durable record
in the swarm. A paper trail that blurs two agents together is worse than no paper
trail: it is a paper trail that lies.

The insight is that uniqueness **cannot live in `agents/`**, because `agents/` is
the one directory that gets pruned.

## Who uses it

**Agents** — every id passed to `send`, `wait`, `close`, `updates --id`.

The **operator** — reading `swarm graph`, `swarm list`, and the on-disk paper
trail. This is the capability that makes those readable.

## Current behavior

### The id *is* the label

There is one concept, not two. `swarm spawn "…" --label fix-send-race` creates,
prints, and addresses the agent `fix-send-race`. The registry still carries a
`label` key, holding the same string, for readers that expect it.

That string is the filename everywhere under the swarm: `agents/<id>.json`,
`state/<id>.json`, `inbox/<id>/`, `settings/<id>.{json,task,launch.sh,status}`, and
the `id` field in every `updates/` record.

### Slugification

`slugify()`: NFKD-normalize, strip combining marks (so `café` → `cafe`, not
`caf`), lowercase, replace every non-alphanumeric run with `-`, collapse repeats,
strip leading/trailing hyphens, truncate to 30 characters, then re-strip a trailing
hyphen.

A `--label` that slugifies to nothing (`"!!!"`) is a **hard error**, not a silent
fallback. The old default label `claude` is gone.

### Derivation when no label is given

`derive_slug()` takes the task's first eight *meaningful* words — skipping a filler
list (`you are the a an and or of to in on for with please your my this that it its
is be do go make just now then so as at by from into we i us`) — and slugifies
them. `swarm spawn "build the CSV importer"` → `build-csv-importer`.

If every word is filler, the words are kept rather than emitting nothing. A wholly
empty task yields `task`. **You never get an uninformative name.**

### Lifetime uniqueness

An **append-only ledger**, `$SWARM_ROOT/names`, one slug per line. `swarm start`
creates it empty. `mint_id()` appends to it. **Nothing ever prunes it** — that is
its entire purpose.

`mint_id(base)`:

0. **Seed the ledger from `agents/`** — `init_swarm_paths` ledgers any registry row
   whose name the ledger lacks. Every verb calls it, so a name is recorded before
   anything can delete the record that carries it. (Added by PR #24; see the defect
   below.)
1. Take an **atomic `mkdir` lock** on `names.lock` (up to 100 tries at 100ms, then
   proceed anyway). This serializes check-and-append, so two concurrent spawns
   cannot claim the same name.
2. Compute `taken` = the ledger **∪** whatever `agents/` currently holds. The union
   is belt-and-braces: a hand-created or pre-ledger registry row still blocks its
   name.
3. Walk `base`, `base-2`, `base-3`, … until one is not taken.
4. Append the winner. Release the lock. Print it.

**The ledger was, until PR #24, incomplete — and the "one agent, forever" guarantee
did not actually hold.** Absorption used to happen *inside* the collision loop, so it
only ran for a candidate that collided. A registry row that never passed through
`mint_id` — hand-created, restored from a backup, or left by an older layout — was
never absorbed. It still blocked its name at mint time (because `taken` unions
`agents/`), but the instant `reap` deleted that row the name was **silently freed**,
and a later spawn re-minted it: two different agents, same id, in one swarm's history.

Absorbing at mint time could never have closed this, and the reasoning is worth
keeping: `mint_id` runs on **spawn**, which is *after* the `reap` that already dropped
the name. The fix had to move earlier than spawn — into the path every verb takes.

This is a gap the PRDs missed. These documents asserted the guarantee held because
`WORLD.md` and three code comments said so; the code disagreed with all four, and
engineering found it. Recorded here rather than quietly corrected, because the
register's whole premise is that *"where the code and the docs disagree, that
disagreement is recorded."* The docs were not wrong about the intent — they were wrong
that the intent was implemented.

A **confirmed-failed spawn keeps its name burned**: `cmd_spawn` deletes
`agents/<id>.json` on failure but never touches the ledger, because that id's
`settings/` and `state/` files bear it.

`swarm reap` frees a **pane**, never a **name**. This is stated three times in the
codebase and once in `WORLD.md`, which is proportionate to how easy it is to
reintroduce the bug.

## Contracts and guarantees

**Guaranteed:**

- A name identifies **exactly one agent for the swarm's entire lifetime**. Not one
  live agent — one agent, ever. Including dead ones. Including reaped ones.
  Including ones whose spawn failed. *(True as of PR #24. Before it, a registry row
  that had never passed through `mint_id` lost its name on `reap` — the guarantee was
  documented in four places and implemented in none of the cases that mattered.)*
- An id is always informative: derived from an explicit label, or from the task's
  meaningful words. Never `a1`, never `claude`, never empty.
- A label that cannot produce a slug is an error at spawn time, not a silent
  default.
- Concurrent spawns cannot collide. The check-and-append is lock-serialized.
- The ledger is append-only and self-healing: a swarm directory created before the
  ledger existed grows one on first mint, and pre-existing `agents/` names are
  absorbed into it.
- Slugs are ASCII, ≤30 characters, and never start or end with a hyphen.

**Best-effort:**

- The `mkdir` lock gives up after ~10 seconds and mints anyway. Under
  pathological contention two spawns could theoretically race; PR #14 verified 12
  concurrent `mint_id` calls produced 12 unique names.

## Edge cases and known limitations

**Truncation can collide.** Two distinct labels sharing their first 30 characters
slugify identically, and the second gets `-2`. The suffix pushes the total past 30
(`<30 chars>-2` is 32), which is harmless — the cap applies to the base, not the
minted id — but it means the "30 characters" property is about the slug function,
not about ids.

**Readers key off the record's `id` field, not the filename.** This matters
because `fix-send-race` and `fix-send-race-2` share a filename prefix. `swarm
updates --id fix-send-race-2` filters on `r.get("id") != only`, an exact match, so
prefix-sharing agents never bleed into each other. PR #14 verified this explicitly.
Any future reader that globs by prefix would reintroduce the bug.

**The ledger is per-project, and now that is the same as per-swarm.** Before
PR #16 a project could hold many swarms, each with its own ledger, so two runs
could each have a `csv-importer` and only the swarm-id told them apart. Now the
project *is* the swarm: one ledger, one `agents/`, one `state/`. A name identifies
one agent for the life of the **repository**, which is a strictly stronger and
simpler guarantee than the one the feature was designed to give.

The corollary is that the ledger never resets. Every id ever minted in a project
is burned forever, so a long-lived repo accumulates `csv-importer-2`,
`csv-importer-3`, … across unrelated work months apart. That is the intended
trade — a name must only ever mean one agent — but the suffix now encodes repo
history rather than run history, and nothing surfaces why.

**Derivation is language-dependent.** The filler list is English. A task written in
another language will yield a slug of its first eight words verbatim — informative,
but not filtered. Accent folding works (PR #14 tested `café` → `cafe`).

**The `label` field is now redundant.** It holds the same string as `id` in the
registry, the same string in `SWARM_AGENT_LABEL`, and prints alongside `id` in
`swarm list` (`fix-send-race  fix-send-race  opus  live`) and `swarm graph`
(`fix-send-race [fix-send-race]`). Retained for readers; visually noisy.

**The name a failed spawn burned is invisible.** It is in the ledger but not the
registry, so nothing reports it. Spawning `--label importer` twice after a first
failure yields `importer-2` with no explanation of where `importer` went.

## Open product questions

1. **Should `label` be removed from the display surface?** `swarm list` and `swarm
   graph` both print the id twice. PR #14 kept the field for readers; the *rendering*
   was not revisited. Purely cosmetic, but it is the first thing a reader sees.

2. **Is 30 characters right?** It was chosen to keep filenames and tree renderings
   tidy. A task-derived slug of eight meaningful words routinely hits the cap and
   truncates mid-word (`asked-build-csv-importer-reply` in PR #14's own test), which
   costs some of the informativeness the feature exists to provide.

3. **Should the ledger record *why* a name was burned?** It is one slug per line.
   A second column (`spawned`, `spawn-failed`) would let `swarm list` explain the
   `-2` suffix, at the cost of making an append-only file into a format with a
   schema. Probably not worth it; noted because the question recurs.

4. ~~**Does lifetime uniqueness need to span swarms?**~~ **Answered by PR #16.**
   The question was whether an operator reading two swarms' paper trails could tell
   two `cos` agents apart. There are no longer two swarms to read: uniqueness spans
   the project, which is the whole world. The concern is resolved by deleting the
   thing that caused it — noted here because it is a clean example of a product
   question being closed by simplification rather than by mechanism.

5. **Should the ledger ever be prunable?** It now grows for the life of a
   repository (see above). A repo that runs swarms weekly for a year carries every
   name it ever minted, and the `-N` suffixes stop being informative. Against
   pruning: a freed name can be reused, and the whole feature exists to make that
   impossible. The tension is real and currently unacknowledged.
