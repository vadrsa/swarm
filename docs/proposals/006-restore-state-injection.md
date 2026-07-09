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
3. **Rename the heading — only if (2) is declined.** Once (2) lands, `CURRENT TASKS:` lists
   only current tasks and the heading becomes true for free. Verified: an agent whose tasks
   are *all* finished does not get an empty list, because the hook already guards with
   ``taskLines ? `CURRENT TASKS:…` : ''`` — the heading is omitted entirely. So (2) needs no
   copy change. If (2) is rejected, the heading must become `TASKS:`, because listing
   `[done]` items under *current* is a plain copy defect.

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

**`cos` independently reproduced this decomposition by ablation** — zeroing one field at a
time against the installed hook — and arrived at 6,904 / 2,404 / 1,801, exact to the byte.
It went looking for a discrepancy and reported finding none.

**7. The monotonicity claim survives a deliberate attempt to falsify it.** The whole case
for a code fix rather than a habit rests on "no agent action reclaims done-task bytes."
That is a strong claim, so it was attacked rather than asserted. Against the real hook, with
sixteen finished tasks:

| what the agent does | injected bytes | verdict |
|---|---:|---|
| baseline: 16 done tasks, long `progress` bodies | 1,813 | — |
| empties every `progress` field | **1,813** | reclaims **nothing** — `progress` is never injected |
| shortens every title to one character | 1,013 | works, but the title is how a resumed agent identifies the task |
| deletes the tasks from `tasks[]` | 773 | destroys the durable record a parent judges |

There are exactly three levers and no fourth: `done` is terminal, with no state below it.
One reclaims nothing, one costs the agent its own index, and one costs the organisation its
paper trail. **An agent cannot fix this from inside its checkpoint** — which is precisely
what makes it the tool's problem rather than a discipline problem, and what distinguishes it
from `open_threads`, where `cos` closed thirteen and reclaimed 2,855 bytes.

The trap is worth noting for anyone tempted to economise: **trimming `progress` notes to
slim a checkpoint reclaims zero injected bytes.** It is the one field agents most naturally
prune, and the only one that costs nothing to keep.

**COST**

- (1) is a convention, already applied to the only checkpoint that violated it. Zero code.
- (2) is one predicate in `restore-state`. It does not change the on-disk schema, the
  checkpoint contract, or any verb. Additive-safe: an agent that never marks anything `done`
  sees no change.
- (3) is a string, and only if (2) is declined.
- **What it costs:** a resumed agent no longer sees its finished work in the injection. That
  is the point, and the hook already points it at the file. The one real loss is *ambient*
  awareness — an agent skimming the injection will not be reminded that it already did
  something. **The context belongs in the finished task's own `progress` body**, which is
  durable and costs zero injected bytes (verified: a 200,000-character task body adds *nothing*
  to the payload). That is exactly where the filter leaves it.

  > **Correction.** An earlier draft of this proposal said the loss was *"mitigated by
  > `progress_summary`, which survives and is where that belongs."* **That was wrong, and
  > backwards.** `progress_summary` is injected **verbatim, 1:1, every session, forever**. It
  > is the single worst place to put narrative about finished work. `cos` caught this from
  > `release-mgr`'s ablation data, and pushed back on *"where that belongs"* directly. It was
  > right. Following the old advice literally would have converted a monotonic 12–15% problem
  > into a discretionary 33% one — and called it a fix. See **THE THIRD BUCKET** below.

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

## THE THIRD BUCKET — and it is the one this proposal nearly recommended

`cos` routed a tension in *this document's own mitigation*, from `release-mgr`'s ablation
rather than its own. I reproduced the ablation independently against the installed hook,
zeroing one field at a time across the live roster:

| agent | total | `open_threads` | task lines | *…done* | **`progress_summary`** |
|---|---:|---:|---:|---:|---:|
| `cos` | 12,665 | 7,135 | 2,659 | 2,056 | 990 (**7%**) |
| `release-mgr` | 8,618 | 3,392 | 2,031 | 1,237 | 1,967 (**22%**) |
| `rd` | 5,917 | 1,760 | 891 | 802 | 2,041 (**34%**) |
| `audit` | 6,659 | 2,816 | 442 | 376 | 1,984 (**29%**) |
| `product` | 4,043 | 812 | 860 | 54 | 1,360 (**33%**) |

So there are **three buckets, not two**, and the middle one is a trap:

| bucket | reclaimable? | do agents reclaim it? |
|---|---|---|
| `open_threads` | yes | **yes** — closing a thread frees bytes, visibly |
| **`progress_summary`** | **fully** | **no** — rewriting it feels like bookkeeping, not accretion |
| finished tasks | **no** | cannot: only a filter reaches them |

**Two facts make the middle bucket worse than it looks**, both measured:

1. **A task's `progress` body costs zero injected bytes at any size.** A 200,000-character
   body adds *nothing* to the payload. `progress_summary` is injected **1:1** — 500 characters
   in, 500 bytes out.
2. **`progress_summary` is not drifting; the tool is asking for it.** The schema describes it
   as *"overall: is my structure right for my load?"* — a standing question, answerable in a
   sentence (44 characters). The reconcile ritual then tells every agent to write its
   reconciliation into the checkpoint, and this is the natural field. The result, measured
   across the roster:

   | agent | `progress_summary` | vs. the schema's own 44-char hint |
   |---|---:|---:|
   | `rd` | 2,033 | **46×** |
   | `audit` | 1,984 | **45×** |
   | `release-mgr` | 1,959 | **45×** |
   | `product` | 1,350 | **31×** |
   | `cos` | 983 | 22× (deliberately shrunk last cycle) |
   | `seedcheck` | 35 | 1× — *it never reconciled* |

   Every agent that has ever reconciled is 15–46× over. The one that never did sits at 1×.
   **That is not sloppiness; it is the ritual working as instructed**, into a field that is
   re-injected verbatim for the agent's whole life.

**This does not change decision 2.** The monotonic bucket is exactly the one a filter should
own, and the only one a habit cannot reach — `cos` still endorses it. But it corrects this
proposal's advice about where the displaced context should go, and it exposes a defect this
proposal does not fix:

> **`progress_summary` is a narrative field, injected 1:1 forever, that the reconciliation
> ritual actively instructs agents to grow.**

**The remedy is *not only* a habit, and `cos` is the one who saw that.** If the tool causes
the overrun, an agent cannot discover the cost of obeying it. `cos` grepped `bin/swarm`,
`bin/swarm-hook.cjs`, and `WORLD.md` for any statement of the asymmetry and found **zero
hits**; product confirmed, and found worse — all three sources say the *whole* checkpoint is
re-injected, when seven of twelve fields are. An agent reasoning correctly from the contract
reaches exactly the wrong economy.

That makes it a **documentation defect**, one sentence wide. It is not a seventh proposal, and
neither agent has filed one: `cos` has committed to carry it as a **rider** on decision 2's
implementation — *"the same PR that adds the filter can add one sentence to the schema hint,
and it costs nothing extra to review"* — the same way it committed to carry the G10 bound on
the mail-read change. Recorded in both checkpoints so it survives a months-long wait for a
ruling.

Beyond that one sentence, the remedy is a *habit* — write the verdict, not the narrative; put
the narrative in the task body, which is free — and this project's order is that conventions
earn tooling.

**Product's own `progress_summary` was 31× the hint while this document recommended the field
as a remedy.** It has been rewritten, and the discipline measured on the way through:

| | before | after |
|---|---:|---:|
| `progress_summary` | 1,350 chars | 121 chars |
| checkpoint on disk | 8,089 B | **8,273 B** (grew) |
| `restore-state` injects | 4,043 B | **2,806 B** (−31%) |

The narrative was not deleted. It moved into a finished task's `progress` body, where it is
durable and costs nothing. **The file grew while the injection fell by a third** — the shape
`cos` named and neither PRD had stated. That is the whole discipline in one measurement, and
it is available to every agent today, with no code and no decision from anyone.

**DECISION**

Three separable yes/no. The first needs no code and product has already done it to itself.

1. **Convention:** a task with an unresolved blocker is `blocked`, not `done`. Yes/no.
   *(Product has applied it to itself; `cos` verified the invariant now holds org-wide.
   If (2) lands, this invariant becomes load-bearing and wants a **test**, not just this
   line — `cos`'s point, and it is right: a documented invariant with no instrument is
   exactly what G7 says rots.)*
2. **Code:** `restore-state` injects only `status !== "done"` tasks. Yes/no.
   *(Product recommends yes. `cos` will brief and judge it.)*
3. **Copy:** if (2) is declined, rename `CURRENT TASKS:` → `TASKS:`. Yes/no.
   *(Moot if (2) lands — verified above.)*

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
