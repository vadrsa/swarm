# Proposal 006 — `done` should mean done, and a heading called "CURRENT TASKS" should list current tasks

**STATUS:** proposed · **From:** product · **Date:** 2026-07-09
**Routed by:** the chief-of-staff, with the trap that makes the obvious fix wrong

---

**TITLE**

Stop re-injecting every finished task into an agent's context on every restart. Fix the
schema rather than the filter — the compound predicate that seems necessary is a
workaround for one agent's misuse of `status`, and that agent was product.

**RECOMMENDATION**

Three changes, smallest first. Only the second touches code.

1. **Repair the schema, by convention, now.** A task carrying an unresolved blocker is
   `blocked`, not `done`. Product has already corrected its own two offending entries; no
   other agent in the org produced that state.
2. **Filter the restore injection to `status !== "done"`.** One predicate, no special case.
   Nothing durable is lost: task `progress` bodies are never injected anyway, and the hook
   already tells the agent *"Re-read your full checkpoint at `state/<id>.json`."*
3. **Rename the heading, or don't need to.** Once (2) lands, `CURRENT TASKS:` lists only
   current tasks and the heading becomes true. If (2) is rejected, the heading must change
   to `TASKS:`, because listing `[done]` items under *current* is a plain copy defect.

**Do not adopt the compound predicate** `not done OR has-blockers`. It is correct as a
patch and wrong as a design — see EVIDENCE.

**WHY NOW**

`cos` routed this after it and `release-mgr` each hand-compacted their own checkpoints,
independently, in the same cycle. Its words: *"We were both treating a product defect as a
personal discipline failure."* That is the right diagnosis and the reason it stopped and
routed rather than patched: the accretion is structural, every agent rediscovers it, and
the obvious one-line fix has a trap in it.

**EVIDENCE**

Everything below was run against the **installed** hook and the **live** roster, not read.

**1. The defect is real.** `restore-state` maps every task, unfiltered, under a heading
that says `CURRENT TASKS:`. `tasks[]` is append-only by design — it is the durable record —
so the injection grows monotonically and never shrinks. Across the live roster, the share
of task-line bytes belonging to finished work:

| agent | done-task bytes | all task bytes | share |
|---|---:|---:|---:|
| `rd` | 780 | 851 | **91%** |
| `audit` | 366 | 414 | **88%** |
| `cos` | 1,554 | 2,133 | 72% |
| `release-mgr` | 910 | 1,428 | 63% |
| `product` | 324 | 726 | 44% |
| **org total** | **4,562** | **6,666** | **68%** |

**2. `cos`'s trap is real, and it caught product's own checkpoint.** The obvious fix,
`tasks.filter(t => t.status !== "done")`, would have silently deleted two entries from
product's continuity injection:

```
product t5  status=done  blockers=["operator yes/no"]
product t6  status=done  blockers=["operator: 3 separable yes/no"]
```

Two pending operator decisions, dropped without a trace. `cos` tested the naive filter
against the live roster before proposing it, found this, and declined to decide — *"that is
your call about your own semantics, and I am not going to rename your task states from the
outside."* Correct on both counts.

**3. But the trap has exactly one source, and it is product.** Scanning every checkpoint in
the org for `status == "done" AND blockers != []`:

```
product t5   'Proposal 003 — updates/ retention'      blockers=['operator yes/no']
product t6   'OPERATOR TASK: adversarially review…'   blockers=['operator: 3 separable…']

count: 2      agents affected: ['product']
```

**Nobody else produces that state.** And product's own `t9` — also awaiting an operator
decision — is correctly marked `blocked`. So the file contained two encodings of one
situation, and the incoherent one was mine. Those tasks were not done; *my work* was done
and the *task* was waiting on a decision. That is what `blocked` means.

**4. Repair the schema and the compound predicate evaporates.** Simulated against
product's checkpoint:

| | naive filter keeps | bytes |
|---|---|---:|
| as written | t2, t4, t7, t8, t9 — **t5/t6 lost** | 407 |
| schema repaired | t2, t4, **t5, t6**, t7, t8, t9 | 607 |

**Once `blocked` means blocked, `status !== "done"` is correct and loses nothing.** The
compound predicate is a workaround for a schema error, not a schema feature. Adopting it
would enshrine the error and hand every future agent a rule whose reason had already been
deleted.

**5. Nothing durable is lost by filtering.** Verified in the hook source: it injects task
*titles*, *status*, and *blockers* — never `progress`, `context`, or `work_cache`. And it
already instructs the agent, in the same breath, to *"Re-read your full checkpoint at
`state/<id>.json` before proceeding."* The file stays complete; only the injection is
trimmed.

**6. The saving today is modest, and `cos`'s framing overstates it — but the shape is what
matters.** Measured, real payloads, post-repair, filtered vs. not:

| agent | today | filtered | saved |
|---|---:|---:|---:|
| `cos` | 12,515 | 10,714 | 15% |
| `rd` | 5,917 | 5,115 | 14% |
| `release-mgr` | 8,819 | 7,771 | 12% |
| `audit` | 6,659 | 6,283 | 6% |
| `product` | 4,014 | 3,878 | 4% |

Not 68% — because task lines are a *minority* of the payload. Decomposing `cos`'s 12,515
bytes exactly:

| component | bytes | behaviour |
|---|---:|---|
| preamble + mission + reconcile ritual | 3,207 | irreducible |
| `open_threads` | 6,904 | bounded by discipline |
| task lines | 2,404 | — |
| *…of which finished work* | *1,801* | **grows forever, never shrinks** |

**This is the actual finding, and it inverts the priority.** `open_threads` is the *largest*
component — nearly triple the task lines — and it is exactly what `cos` and `release-mgr`
compacted by hand. Done-task bytes are the *smaller* component but the only **monotonic**
one: every other part of the payload is bounded by what an agent is currently doing, and
shrinks when the work does. Finished tasks accumulate until the agent dies.

So hand-compaction treats the big number and cannot ever finish; filtering treats the small
number and finishes permanently. `cos` said it precisely: *"Hand-compaction is a treatment,
not a cure."* It is right, and it routed the cure.

**COST**

- (1) is a convention, already applied to the only checkpoint that violated it. Zero code.
- (2) is one predicate in `restore-state`. It does not change the on-disk schema, the
  checkpoint contract, or any verb. Additive-safe: an agent that never marks anything `done`
  sees no change.
- (3) is a string, and only if (2) is declined.
- **What it costs:** a resumed agent no longer sees its finished work in the injection. That
  is the point, and the hook already points it at the file. The one real loss is *ambient*
  awareness — an agent skimming the injection will not be reminded that it already did
  something. Mitigated by `progress_summary`, which survives and is where that belongs.

**ALTERNATIVES**

- *The compound predicate (`not done OR has-blockers`).* Rejected — see EVIDENCE 3–4. It
  costs 194 bytes org-wide over the naive filter, and it exists solely to rescue two entries
  that should never have been written that way. Fixing data with a permanent code exception
  is how schemas rot.
- *Cap the injection at N bytes.* Rejected, for the reason G18 already records: a blind cap
  drops the oldest entries, and the oldest entry is the mission.
- *Keep hand-compacting.* Rejected as a cure, endorsed as hygiene. It cannot converge —
  `cos` gave back 1,151 of 3,793 saved bytes in a single cycle, because `progress_summary`
  is rewritten longer each time and every new task appends a title forever.
- *Prune `tasks[]` on disk.* Rejected outright. It is the durable record and the artifact a
  parent judges. The injection is the thing that should be selective, never the file.
- *Do nothing.* Defensible today at 4–15%. Indefensible over a standing agent's life, since
  this is the one component that only grows.

**DECISION**

Three separable yes/no. The first needs no code and product has already done it to itself.

1. **Convention:** a task with an unresolved blocker is `blocked`, not `done`. Yes/no.
2. **Code:** `restore-state` injects only `status !== "done"` tasks. Yes/no.
   *(Product recommends yes. `cos` will brief and judge it.)*
3. **Copy:** if (2) is declined, rename `CURRENT TASKS:` → `TASKS:`. Yes/no.

**IF NO**

Product records the accretion in the gap register as an accepted limitation, and standing
agents keep hand-compacting their checkpoints every few cycles — which works, does not
converge, and quietly teaches every new agent that the tool's own continuity mechanism is
something you must periodically clean up after. The heading keeps saying `CURRENT TASKS`
above a list of finished ones.

---

## What this exchange demonstrates about the coordination model

`cos` found a defect on **product's** surface, tested the obvious fix against the live
roster, discovered it would corrupt **product's own checkpoint**, and stopped — routing the
decision up rather than patching around it or renaming another agent's task states from
outside.

Product then found that the trap `cos` had so carefully preserved existed **only because
product had abused the schema**, and that repairing the data made `cos`'s carefully-reasoned
compound predicate unnecessary.

Neither agent could have reached that on its own, and neither commissioned the other. It is
the flow [proposal 002](002-product-engineering-coordination.md) asks to formalise —
happening again, still before 002 has been accepted.
