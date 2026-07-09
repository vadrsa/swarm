# Proposal 003 — Bound what `swarm updates` prints, not what the swarm keeps

**STATUS:** proposed · **From:** product · **Date:** 2026-07-09
**Routed by:** the chief-of-staff, after three independent rediscoveries

---

**TITLE**

The swarm's event log grows forever. Fix the verb that reads it, not the directory
that stores it — and add a way to archive a finished generation rather than a rule
that deletes history on a timer.

**RECOMMENDATION**

Three changes, in this order. Only the first is urgent.

1. **Bound the default output of `swarm updates`.** It currently prints *every event
   ever recorded*, unfiltered. Default it to the most recent 50, newest last, with a
   one-line header when records were withheld: `(showing 50 of 1,350 — use --all or
   --since)`. Add `--all`, `--since <duration>`, and keep `--id`.
2. **Add `swarm archive`**, an explicit verb that moves the current event records into
   `.swarm/archive/<timestamp>/` and leaves the live directory empty. The operator runs
   it when a generation of work ends. Nothing runs it automatically.
3. **Do not prune, do not expire, do not cap the directory.** The records stay on disk
   until a human archives them.

**WHY NOW**

The chief-of-staff routed this after it was independently rediscovered three times —
by itself, by the research analyst, and by the release manager, who is about to name it
a known limitation in the next release notes. Three rediscoveries of the same thing is
a signal that it lacks an owner, not that it is urgent.

The read-cost half is already fixed and should not be re-litigated: a merged change
(`2101ccc`) made the per-event hook scan filenames instead of parsing every record,
measured at roughly 46× faster. The engineer who did it **deliberately declined to
prune** and said why: the `wait` verb needs an agent's newest record, `updates` is the
only history surface that exists, and there is no archive verb — so retention needs
that verb before it needs a policy. That reasoning is correct and this proposal follows
it.

**EVIDENCE**

Measured on this repository, just now:

- The live event directory holds **27 records in 108 KB** — after a full generation of
  five standing agents doing real work. About 4 KB per record.
- The previous per-run directory, left behind by the layout change, holds **216 records
  from a single run**.
- The name ledger holds **9 entries and zero collision suffixes.** It grows by one line
  per agent ever created.

Projecting the observed rate:

| Generations | Records | Disk | Text `swarm updates` prints |
|---:|---:|---:|---:|
| 1 | 27 | 0.1 MB | ~2 KB |
| 10 | 270 | 1.1 MB | ~22 KB |
| 50 | 1,350 | 5.3 MB | ~108 KB |
| 200 | 5,400 | 21 MB | **~432 KB** |

**This inverts the framing the gap was handed to me with.** Disk is not the problem and
will not become one: 21 MB after two hundred generations is nothing. The problem is that
`swarm updates` reads the whole directory and prints all of it, every time — so the
operator's *only* inbox verb, and the one an agent calls to see what its children
reported, degrades into an unreadable wall long before the disk notices. I read the
code to confirm: `cmd_updates` iterates the directory, filters only by `--id`, and
prints every record it finds. There is no limit anywhere.

The structural readers are already safe, which is why pruning buys so little:

- `wait` wants **one** record — an agent's newest at or after a mark.
- `status`, `graph`, and `children` want **the newest record per agent**, keyed by id.
- Only `updates` wants history at all.

So every machine reader is indifferent to how much history exists. The single consumer
that suffers is the human, and the fix for a verb that prints too much is to make the
verb print less.

**COST**

- Change 1 is a small change to one verb: a slice, three flags, and a header line. It
  is the only urgent piece.
- Change 2 is a new verb of maybe thirty lines: create a directory, move files, print
  the path. It adds a verb to the world document, so the release manager should classify
  it — by the project's own rules a new verb is a MINOR, and it is purely additive.
- **A behavior change worth naming:** today `swarm updates` shows everything, and
  someone somewhere may be relying on that. After change 1 they must pass `--all`. This
  is a visible, one-flag migration, and the header line tells them exactly what to do.
- Ongoing: none. Nothing runs on a timer, so nothing can delete history at 3am.

**ALTERNATIVES**

- *Prune records older than N days, automatically.* Rejected, and this is the one worth
  arguing. It trades a bounded, visible cost (a long list) for an unbounded, invisible
  one (history silently disappearing). The event log is the **only** record of what
  agents reported; a dead agent's final report is already hard to reach, and the gap
  register records that no verb surfaces it. Deleting it on a timer would make the
  system's memory shorter than its projects. It also violates the project's own
  posture — nothing else in this tool deletes on a schedule, and `reap` explicitly
  refuses to remove an agent when it cannot prove the agent is dead.
- *Cap the directory at N records, dropping the oldest.* Rejected for the same reason,
  plus a sharper one: the cap would silently break `swarm updates --since` for any
  window older than the cap, and nothing would say so.
- *Re-scope the directory per swarm-run, as it was before the layout change.* Rejected:
  it would reintroduce the run-id concept that the project deliberately deleted ("we
  just have one swarm per project"), to solve a disk problem that does not exist. That
  is configuration bought with a concept.
- *Index the records by agent id into subdirectories.* Rejected as premature: it speeds
  up readers that are already fast enough (they scan filenames now), and it does nothing
  for the verb that actually hurts.
- *Accept and document.* Rejected only for change 1 — a verb that becomes unusable is a
  defect, not a limitation. **Accepted for the name ledger:** see below.

**DECISION**

Yes/no, and they are separable — say yes to 1 alone if you prefer:

1. Bound `swarm updates` output by default (most recent 50), with `--all` / `--since`.
2. Add a manual `swarm archive` verb. Nothing automatic.
3. Never prune or expire event records.

**IF NO**

Product records the growth in the gap register as an accepted, documented limitation,
and the release manager's known-limitation note stands as the only user-facing warning.
The cost of declining is that `swarm updates` keeps getting slower to read for as long
as this repository lives, and the first person to feel it will be the operator, since it
is his inbox. Nothing breaks; something gets steadily worse.

---

## The name ledger: accept and document

The chief-of-staff flagged the same unbounded-growth pattern in `.swarm/names`, which
records every agent id ever minted so a name is never reused.

**Product's position: leave it exactly as it is, and do not treat it as the same
problem.** It is one line per agent for the life of the repository — nine lines here,
zero collision suffixes. Two hundred generations of five agents would be a thousand
lines, which is a small text file.

More importantly, the ledger is the mechanism that makes a name mean one agent forever.
That guarantee is load-bearing: it is why reading old history never blurs two different
agents together, and it is the reason `reap` frees a pane but never a name. **Trimming
the ledger would trade a stated guarantee for kilobytes.** The growth is the feature
working.

The one real consequence — suffixes like `-2`, `-3` accumulating as names are reused —
has not happened once in this repository, and if it ever does, it is informative rather
than harmful: it tells you a name has been used before.

---

## Provenance

Routed by the chief-of-staff with the engineering half already scoped and closed —
explicitly as a decision to own, not a task to execute. This is exactly the flow that
[proposal 002](002-product-engineering-coordination.md) asks to make normal: engineering
established the facts and declined to invent scope on a product surface; product decides
the scope and hands the decision back for implementation.

Worth noting that it happened **before** proposal 002 was accepted. The convention proved
itself in practice first, which is the order this project's own
[philosophy](../PHILOSOPHY.md) says tooling should follow.
