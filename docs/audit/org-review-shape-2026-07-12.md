# ORG-REVIEW: TREE SHAPE FORENSICS — what the swarm's own files actually record

**Author:** `shape-forensics` (child of `org-review-scout`), 2026-07-12.
**Mandate:** mine the tree shape and the top-level agents' journals as *evidence*.
Produce true numbers and honest nulls. **This document does not design an
instrument and does not recommend an org shape** — both were explicitly out of
scope, and both are downstream of whether the facts below hold.

**Evidence discipline** (as SPAN.md/STRUCTURE.md):
- **VERIFIED** — I read the line / the record. Cited file:line.
- **MEASURED** — I counted it from the files. Re-runnable; the method is stated.
- **REASONED** — inference. Could be wrong; a falsifier is named.

**Snapshot:** all counts taken 2026-07-12 ~17:00–17:25Z against `.swarm/` at
working-tree state. The tree was *growing while I measured it* (three sibling
subtrees were spawning); agent counts therefore drift upward by a few between
sections. Every number below states which population it was taken over. **The
top-level population (25) was closed for the whole measurement window** — no
new `parent==operator` agent appeared — so §1/§2 are stable.

---

## 0. THE EVIDENCE BASE — and its first surprise

**VERIFIED.** Everything the swarm records about an agent lives in four places:

| store | count | fields |
|---|---|---|
| `.swarm/agents/<name>.json` | 107 → 117 (grew during measurement) | `name, parent, pane, tab, model, cwd, task, ts` — **8 fields, that is all** |
| `.swarm/event/<name>.json` | 86 | `event, ts, last_words` — **3 fields**; only ever `event:"stop"` |
| `.swarm/journal/<name>.md` | 110 → 121 | free prose, append-only |
| `.swarm/queue/<name>/{,delivered/}` | 50 dirs | message envelopes: `to, from, ts, body` |

**VERIFIED — `.swarm/` is not in git.** `git ls-files .swarm` → **0 files**.
There is no version history of the tree. The only time-signal outside `ts` is
filesystem mtime, which is destroyed by any copy, and the only "who did what
when" is what agents chose to write in prose.

**VERIFIED — and this is the load-bearing fact for everything below: there is
no death record.** `ts` is spawn time. There is *no* close time, *no* closer,
*no* close reason, anywhere in the files. "Dead" in `swarm ps` is **derived at
read time from herdr pane liveness**:

> `bin/swarm:514-516`
> ```python
> def is_dead(a):
>     return live is not None and a.get("pane") not in live
> dead = sorted(n for n, a in agents.items() if is_dead(a))
> ```

**A deliberate `swarm close` and a crashed pane are byte-for-byte
indistinguishable in the record.** The closest proxy for a death time is
`event/<name>.json.ts` — the agent's **last Stop-hook firing**, i.e. when it
last *ended a turn*, which may precede its actual close by hours or days.
Every "lifetime" in §1 is therefore *spawn → last turn end*, and is a **lower
bound**, not a lifetime. I use it because it is the best the files support, and
I flag it rather than launder it.

**MEASURED — 30 of 117 agents have no event record at all** (never fired a Stop
hook that was captured). Most are agents that were live mid-first-turn at
snapshot time; but `updater-v2` is not (§3.2).

**MEASURED — 4 journals have no agent record:** `operator.md`, `ws-probe-1.md`,
`ws-probe-2.md`, `ws-probe-g1.md`. The operator is a mailbox, not a node
(WORLD, "the operator is a mailbox"), so it has a journal and no record — by
design. The three `ws-probe-*` were driven outside `swarm spawn`. **Any census
that trusts `.swarm/agents/` alone silently misses them.**

---

## 1. TOP-LEVEL CENSUS — every agent that ever had `parent == operator`

**MEASURED — exactly 25.** (Method: `parent` field over all
`.swarm/agents/*.json`.) Of 117 agents total, **25 are top-level (21%) and 92
were spawned by other agents.**

Lifetime = spawn → last stop-event (see §0: a lower bound, not a close time).
"Subtree" = transitive descendants.

| # | agent | spawned (UTC) | last stop-event | lifetime | direct kids | subtree | journal | state |
|---|-------|---------------|-----------------|----------|-------------|---------|---------|-------|
| 1 | `field-tester` | 07-09 18:40 | 07-12 16:04 | 4163m | **16** | 24 | 125L | dead |
| 2 | `hardener` | 07-09 18:41 | 07-12 01:53 | 3313m | **0** | 0 | 299L | **LIVE** |
| 3 | `updater` | 07-09 20:37 | 07-12 13:45 | 3908m | **0** | 0 | 139L | **LIVE** |
| 4 | `codex-scout` | 07-09 23:07 | 07-09 23:29 | 22m | **0** | 0 | 19L | dead |
| 5 | `structure-scout` | 07-10 15:12 | 07-10 15:18 | 6m | **0** | 0 | 77L | dead |
| 6 | `red-simplest` | 07-10 15:46 | 07-10 15:56 | 11m | **0** | 0 | 14L | dead |
| 7 | `red-operator` | 07-10 15:46 | 07-10 15:54 | 9m | **0** | 0 | 26L | dead |
| 8 | `inbox-scout` | 07-10 16:47 | 07-10 16:54 | 7m | **0** | 0 | 18L | dead |
| 9 | `updater-v2` | 07-10 17:09 | **— none —** | **—** | **0** | 0 | 57L¹ | dead |
| 10 | `codex-audit` | 07-10 17:10 | 07-10 17:19 | 10m | **0** | 0 | 17L | dead |
| 11 | `harness-scout` | 07-10 17:40 | 07-10 17:57 | 17m | **3** | 3 | 50L | dead |
| 12 | `decision-scout` | 07-10 18:02 | 07-10 18:35 | 33m | **3** | 3 | 59L | dead |
| 13 | `decision-wiring` | 07-10 19:05 | 07-10 19:57 | 52m | **3** | 7 | 56L | dead |
| 14 | `proxy-scout` | 07-10 21:59 | 07-10 23:36 | 97m | **2** | 2 | 227L | dead |
| 15 | `pipeline-scout` | 07-11 01:02 | 07-11 01:31 | 30m | **2** | 3 | 77L | dead |
| 16 | `hook-scout` | 07-11 01:46 | 07-11 02:20 | 34m | **3** | 3 | 79L | dead |
| 17 | `patterns-contractor` | 07-11 08:54 | 07-11 09:01 | 8m | **0** | 0 | 34L | dead |
| 18 | `skill-writer` | 07-11 11:18 | 07-11 11:25 | 6m | **0** | 0 | 54L | dead |
| 19 | `fleet-scout` | 07-11 16:49 | 07-11 17:06 | 17m | **0** | 0 | 109L | dead |
| 20 | `fleet-eval` | 07-11 18:16 | 07-11 19:56 | 101m | **8** | 9 | 474L | dead |
| 21 | `onboarding-scout` | 07-12 12:56 | 07-12 13:16 | 20m | **4** | 10 | 287L | **LIVE** |
| 22 | `onboarding-split` | 07-12 13:25 | 07-12 13:40 | 15m | **0** | 0 | 62L | **LIVE** |
| 23 | `operator-structure-scout` | 07-12 15:59 | 07-12 17:00 | 61m | **5** | 8 | 535L | **LIVE** |
| 24 | `opencode-plugin-scout` | 07-12 16:02 | — (live) | — | **4** | 7 | 770L | **LIVE** |
| 25 | `org-review-scout` | 07-12 16:53 | — (live) | — | **3** | 19 | 295L | **LIVE** |

¹ `updater-v2`'s 57 journal lines are **all spawn-stub** — see §3.2.

**What each did** (VERIFIED — brief's opening clause + its journal's *last*
entry header):

| agent | was spawned to | its own last words |
|---|---|---|
| `field-tester` | "dogfood the swarm tooling live and produce evidence for/against each WATCHLIST item" | "doctrine probe shipped post-review; day's reconciliation" |
| `hardener` | "do the already-justified code work on the swarm repo. Task 1: port the 22 process-level tests…" | "Task 14 GREEN, reported" |
| `updater` | "keep the installed swarm tooling current with origin/main" | "cycle: 1e254e4 → b94fa9e (PR #82, onboarding doctrine)" |
| `codex-scout` | "the operator wants codex support in swarm… you write NO product code" | "deliverables complete; reporting" |
| `structure-scout` | "deep design research into where tree structure actually comes from" | "STRUCTURE.md written; deliverable ready" |
| `red-simplest` | "adversarial design reviewer with no stake in the proposal you are attacking" | "deliverable written, reported, going idle" |
| `red-operator` | *(identical brief text to `red-simplest`)* | "deliverable written; reporting to operator" |
| `inbox-scout` | "research-only evaluation of the operator's inbox ideas" | "deliverable written: docs/design/INBOX.md" |
| `updater-v2` | "You are `updater`, a standing agent that keeps the swarm tool up to date" | **— never wrote an entry —** |
| `codex-audit` | "READ-ONLY audit of the operator's local Codex CLI setup" | "report delivered, going idle" |
| `harness-scout` | "own the multi-harness design the codex integration is missing" | "quota-scout's completion report delivered (no new action)" |
| `decision-scout` | "the operator's attention is the system's scarcest resource… every workstream routes decision points to them" | "N1-N3 patched; deliverable READY; reporting to operator" |
| `decision-wiring` | "you succeed decision-scout, whose deliverable the operator RETURNED" | "reported to operator; task complete pending judgment" |
| `proxy-scout` | "whether the assumed decision engine generalizes… to the WHOLE message plane" | "caught: report was drafted, never sent; corrected, subtree closed" |
| `pipeline-scout` | "third iteration of the decision-engine wiring" | "SENT. Task complete." |
| `hook-scout` | "v4 of the decision-engine wiring — the operator overruled the zero-tool-change constraint" | "delivered to operator; hook-drafter closed; DONE, going idle" |
| `patterns-contractor` | "an OUTSIDE CONTRACTOR… expressly NOT bound by this repo's philosophy" | "correction + reported, idle" |
| `skill-writer` | "Write one installable Claude Code skill teaching how to author a swarm send middleware" | "DONE, falsifier did not fire" |
| `fleet-scout` | "how to add Chinese models to the fleet as LEAF-ONLY agents" | "REPORTED to operator; idle" |
| `fleet-eval` | "You succeed fleet-scout… the operator's correction: leaf-only is a fallback" | "DELIVERABLE COMPLETE; revised per review; reporting to operator" |
| `onboarding-scout` | "Design a doctrine fix for two adoption pitfalls" | "red team landed a BLOCKING kill; I took it; deliverable final" |
| `onboarding-split` | "You revise an APPROVED doctrine design per two operator rulings" | "done. Deliverable written; reporting to operator." |
| `operator-structure-scout` | "Design the GENERALIZED doctrine that replaces the coordinator-stance half of the shipped onboarding doctrine" | "RED3 changed the design AGAIN, and for the better. Doc final." |
| `opencode-plugin-scout` | "DEEP technical research… of the installed opencode v1.17.13" | "the CORRECTED order is now VERIFIED too" |
| `org-review-scout` | "the operator wants an INSTRUMENT to review and improve the swarm's TOP-LEVEL structure" | "I ran the F-SPAN test myself. IT DOES NOT FIRE." |

---

## 2. SHAPE OVER TIME — and a direct contradiction of the flat-tree framing

### 2.1 The operator's top layer had a hard ceiling of 5. MEASURED.

Treating a top-level agent as *open* from spawn until its last stop-event
(§0's proxy), the number of simultaneously-open top-level agents was:

**MEASURED — peak = 5, first reached 2026-07-10 15:46**
(`field-tester`, `hardener`, `updater`, `red-simplest`, `red-operator`).

Concurrency at each of the 25 top-level spawn moments:

```
07-09 18:40  field-tester              -> 1      07-11 01:02  pipeline-scout           -> 5
07-09 18:41  hardener                  -> 2      07-11 01:46  hook-scout               -> 5
07-09 20:37  updater                   -> 3      07-11 08:54  patterns-contractor      -> 5
07-09 23:07  codex-scout               -> 4      07-11 11:18  skill-writer             -> 5
07-10 15:12  structure-scout           -> 4      07-11 16:49  fleet-scout              -> 5
07-10 15:46  red-simplest              -> 4      07-11 18:16  fleet-eval               -> 5
07-10 15:46  red-operator              -> 5      07-12 12:56  onboarding-scout         -> 4
07-10 16:47  inbox-scout               -> 4      07-12 13:25  onboarding-split         -> 4
07-10 17:09  updater-v2                -> 4      07-12 15:59  operator-structure-scout -> 3
07-10 17:10  codex-audit               -> 5      07-12 16:02  opencode-plugin-scout    -> 4
07-10 17:40  harness-scout             -> 5      07-12 16:53  org-review-scout         -> 4
07-10 18:02  decision-scout            -> 5
07-10 19:05  decision-wiring           -> 5
07-10 21:59  proxy-scout               -> 5
```

**The count touches 5 and never 6 — across 15 consecutive spawns over two
days.** The operator's declared span is **~3** (VERIFIED: SPAN.md §1, quoting
the operator: *"maybe for me it's max 3"*). The **observed** ceiling is **5**.

**REASONED:** the top layer is not an unbounded fan — something is holding it.
But I cannot tell from the files *what*. There is no record of the operator
declining to spawn, or of a close being timed to make room. The ceiling is a
real pattern in the data; its mechanism is **not in the record**. Falsifier: if
anyone finds an instant with 6+ open top-level agents, the ceiling claim is
dead — one re-run of the interval sweep settles it.

### 2.2 The flat-tree claim, as stated, is NOT SUPPORTED. MEASURED.

The hypothesis I was asked to check: *"the operator spawns workers directly
instead of top-level agents that own workers."*

**MEASURED — 12 of 25 top-level agents delegated (≥1 child). 13 have zero
children.** That is a near-even split, not a flat tree.

| | agents |
|---|---|
| **delegated (12)** | `field-tester`(16), `fleet-eval`(8), `operator-structure-scout`(5), `onboarding-scout`(4), `opencode-plugin-scout`(4), `harness-scout`(3), `decision-scout`(3), `decision-wiring`(3), `hook-scout`(3), `org-review-scout`(3), `proxy-scout`(2), `pipeline-scout`(2) |
| **zero children (13)** | `hardener`, `updater`, `codex-scout`, `structure-scout`, `red-simplest`, `red-operator`, `inbox-scout`, `updater-v2`, `codex-audit`, `patterns-contractor`, `skill-writer`, `fleet-scout`, `onboarding-split` |

**And the 13 zero-child agents are overwhelmingly SHORT, not
ground-serially-for-hours.** Lifetimes: `structure-scout` 6m, `skill-writer`
6m, `inbox-scout` 7m, `patterns-contractor` 8m, `red-operator` 9m,
`codex-audit` 10m, `red-simplest` 11m, `onboarding-split` 15m, `fleet-scout`
17m, `codex-scout` 22m. **Ten of the thirteen finished in under 25 minutes.**
An agent that answers one question in seven minutes has nothing to delegate;
its zero children are correct, not pathological.

**Only 2 of the 13 are long-lived zero-child grinders — and both are the
standing arms, by design:** `hardener` (3313m, 299-line journal, 0 children —
a serial task queue: "Task 1 … Task 14") and `updater` (3908m, 139 lines, 0
children — a self-triggering watch loop). `updater-v2` is the 13th, and it is a
stillborn (§3.2), not a grinder.

**So the honest statement of the shape is not "flat":**

> **MEASURED.** The operator's top layer is a **serial stack of short-lived,
> single-purpose scouts** — one research question each, a fresh name every
> time, most dead inside half an hour — running alongside **two long-standing
> arms** (`hardener`, `updater`) and **one long-standing measurement
> coordinator** (`field-tester`, 16 children, the single deepest delegator in
> the swarm). Delegation at the top layer is roughly 50/50, and the agents that
> *didn't* delegate mostly *shouldn't* have.

**This contradicts the flat-tree finding as I was given it, and I am reporting
the contradiction rather than the expected result.** Falsifier for my own
claim: if someone reads the 13 zero-child journals and finds that the short
ones were in fact fanning work out through harness subagents (SPAN.md §3d′
rung 2, invisible to `ps`), then "didn't delegate" is false — they delegated
*below the tree*, and my count measures only the tree. **I cannot rule this out
from the files: harness-subagent use leaves NO trace in `.swarm/`.** See §5.

### 2.3 Whole-tree shape. MEASURED.

Over all 117 agents: **27 ever spawned a child (23%); 88 are leaves.** Depth
histogram (1 = child of operator): **{1: 25, 2: 56, 3: 28, 4: 6}**. The tree is
wide and shallow — **maximum depth 4**, and only 6 agents ever reached it.

---

## 3. DETECTABLE PATHOLOGIES — what the files can and cannot see

For each: is it detectable from files alone, at what precision, with a real
instance or an honest null.

### 3.1 STALLED (journal mtime old, agent live) — **DETECTABLE, cheap, and it fires.**

**Detectable: YES.** Two `stat` calls and a `swarm ps`. Precision: exact — mtime
is a fact, liveness is a fact.

**MEASURED, current snapshot (21 live agents):**

| agent | journal mtime age | direct kids | top-level? |
|---|---|---|---|
| `hardener` | **15.1h** | 0 | yes |
| `onboarding-scout` | 3.7h | 4 | yes |
| `onboarding-split` | 3.3h | 0 | yes |
| `updater` | 3.2h | 0 | yes |
| *(17 others)* | <0.2h | — | — |

**One agent is stalled >12h. Three more >3h. All four are top-level.**

**Caveat that kills naive precision (REASONED):** `updater` is a *watch loop* —
its brief (VERIFIED, `.swarm/agents/updater.json`) says "keep the installed
swarm tooling current"; a 3.2h-quiet update watcher is **healthy**, not stalled.
A pure mtime threshold cannot tell a stalled agent from an idle-by-design one,
**because the record contains no field saying which kind an agent is.** The
brief says it — in prose. **Precision of a pure-mtime rule on this snapshot:
at best 3/4 (it flags `updater` falsely); the correct classification requires
reading a brief.**

### 3.2 STILLBORN / duplicate standing role — **DETECTABLE, and the instance indicts the name rule.**

**Detectable: YES, exactly.** A journal whose *only* `##` header is the spawn
stub = the agent never took a turn. **MEASURED: `updater-v2` is the one real
instance among 25 top-level agents.**

- **VERIFIED — `.swarm/agents/updater-v2.json`**: spawned by `operator`,
  2026-07-10 17:09:32Z. Its brief opens, verbatim: **"You are `updater`, a
  standing agent that keeps the swarm tool itself up to date."**
- **VERIFIED — `.swarm/journal/updater-v2.md`**: 57 lines, **exactly one `##`
  entry** — `## 2026-07-10 17:09:32Z — spawned` — and that entry's body is the
  spawn brief, written by the tool, not the agent. **The agent never wrote a
  single word.**
- **VERIFIED — no `.swarm/event/updater-v2.json`.** It never fired a Stop hook.
  It never completed a turn.
- **VERIFIED — `swarm ps`** lists it under `dead:`.
- **VERIFIED —** `updater` (spawned 20h earlier) was **live at that moment and
  is still live now**, with a 139-line journal of completed update cycles.

**What this is:** the operator wanted to **re-brief the standing `updater`
role** — a new brief with a cron wake-up and a corrected install model. WORLD
concept 3 (VERIFIED: *"a name ever used is an error to reuse"*) forbids
addressing the warm name with a new brief via spawn. So the operator minted
`updater-v2`, which collided with the still-running `updater` and **died
without taking a turn.**

**This is warm-name-reuse (SPAN.md §3d′ rung 0: "before spawning fresh: is this
shape of work already owned by a warm name? Reuse is cheaper than any rung
above it") failing in the record.** The doctrine says reuse the warm name; the
tool forbids reusing the name; the operator's workaround was stillborn.
**REASONED** (the operator's *intent* is inferred from the brief text — nothing
records why they spawned it). Falsifier: an operator journal entry saying
`updater-v2` was a deliberate throwaway would overturn this reading.

### 3.3 DEAD-BUT-LIVE (live, q=0, idle Nh) — **DETECTABLE, and the real instance is worse than "idle".**

**Detectable: YES** — `swarm ps` prints liveness, queue depth and idle time on
one line.

**VERIFIED, real instance — `hardener`:**
```
├─ hardener [live] q=0 idle 15h
```
Its journal's final line (**VERIFIED, `.swarm/journal/hardener.md:299`**):

> `Idle, awaiting field-tester verification / next dispatch.`

**And `field-tester` is DEAD** (VERIFIED: in `swarm ps`'s `dead:` list; last
stop-event 07-12 16:04). **`hardener` has been blocked for 15 hours waiting on
a corpse.**

The *cheap* half (live + q=0 + idle 15h) is one line of `ps` output. The
*interesting* half — that the thing it waits for **no longer exists** — needs
the journal's last line parsed and the named agent checked against the dead
list. That is still only file-reading, and it is exactly the kind of thing the
record *does* support. **This is the strongest positive detectability finding in
this document.**

### 3.4 NEVER-DELEGATED-BUT-SHOULD-HAVE — **DETECTABLE AS A COUNT, USELESS AS A VERDICT.**

**Detectable: the raw signal (long journal + zero children), YES.** The
**judgment** ("should have"), **NO — the files cannot support it.**

**MEASURED** — the top-level zero-child agents ranked by journal size:

| agent | journal | lifetime | verdict |
|---|---|---|---|
| `fleet-scout` | 25384B / 109L | **17m** | a big journal in 17 minutes — dense research, nothing to fan out |
| `hardener` | 20027B / 299L | 3313m | **serial by design** — 14 numbered Tasks, each dispatched by the operator |
| `updater` | 9589B / 139L | 3908m | **watch loop by design** |
| `onboarding-split` | 10717B / 62L | 15m | revision of an approved doc |
| `codex-scout` | 6881B / 19L | 22m | one design doc |

**The two agents that top the "long journal, zero children" ranking are the two
agents whose briefs make delegation wrong.** A rule of the form *"long journal +
no children ⇒ should have delegated"* would flag `hardener` and `updater`, the
two healthiest structures in the swarm — and STRUCTURE.md §2b/§2c already
explain *why* both are correct (a re-addressed name; a brief with no terminal
state).

**NULL RESULT, stated plainly: I found NO top-level agent that ground serially
through parallelizable work when it should have delegated.** Every zero-child
top-level agent is either (a) short and single-question, or (b) serial by brief.
The pathology is **real as a concept and absent from this record.** Falsifier:
read the 13 zero-child journals for a passage describing multiple independent
subtasks done one after another; I read the summaries and the last entries, not
all 13 in full — **this null is at MEASURED strength on the structure and only
REASONED strength on the intent.**

### 3.5 FALSIFIER-NOT-HONORED — **delegated to `falsifier-probe`; PRELIMINARY: the files barely support it.**

**MEASURED baseline (mine):** the word "falsifier" appears in **104 of 110
journals**. The word "reconcil" appears in **53**. So a falsifier is *named*
almost universally — it is ritual, and near-universal ritual carries almost no
signal.

The pathology requires three things in the record: (1) a named falsifier, (2)
the falsifying observation actually **firing**, (3) the agent **not changing
course**. (1) is everywhere. **(2) is the problem: an agent that keeps going has
no reason to write "my falsifier fired," and the record has no independent way
to observe the firing.** The disconfirming event lives in a tool result, a pane,
or the model's judgment — **none of which `.swarm/` records.**

I dispatched `falsifier-probe` to test exactly this, with an explicit
instruction that a null is a valid answer, and with the classification it must
produce: each falsifier statement as *observable-in-file* / *observable-elsewhere*
/ *unfalsifiable-as-written*. **Its result supersedes this section; see
`docs/audit/org-review-falsifier-2026-07-12.md`.**

**My prior, stated so it could be scored against the child's data (REASONED):
"this is NOT machine-detectable, because the journals name falsifiers *ritually*
and the firing event is almost never written down."**

### 3.5b — RESOLVED by `falsifier-probe`. My verdict was right; **my reasoning was WRONG, and it was refuted.**

`falsifier-probe` hand-read **135 falsifier statements** across the 10 richest
journals, with a rubric written *before* any reading, and four independent
readers. Its artifact:
`docs/audit/org-review-falsifier-2026-07-12.md` (backing per-statement tables
with verbatim quotes and real file:line in `docs/audit/_fp-slice-{a,b,c}.md`).

**CLASS COUNTS (MEASURED, n=135):**

| class | count | |
|---|---|---|
| **(a) observable-in-file, independently witnessed** | **105** | witness the agent does *not* author: mtime, queue file, test exit code |
| (a) observable-in-file, self-report only | 9 | the only witness is the agent's own later prose |
| (b) observable-elsewhere | 21 | fires in a pane / live git remote / background buffer — evaporates |
| **(c) unfalsifiable-as-written** | **ZERO** | **not one vague "if I turn out to be wrong" in the entire hand-read corpus** |

**FORWARD-HUNT on all 114 class-(a) statements:**

| outcome | count |
|---|---|
| **FIRED → agent CHANGED COURSE** (healthy) | **17** |
| **FIRED → agent IGNORED IT** (the pathology) | **ZERO** |
| never fired | 84 |
| cannot tell | 13 |

**My "ritual" hypothesis is REFUTED, and I record the refutation rather than
quietly dropping it.** I inferred from *"104 of 110 journals contain the word
falsifier"* that the practice was near-universal ritual and therefore
signal-free. **It is not ritual: zero of 135 statements were unfalsifiable
boilerplate, and 105 of them name a witness the agent cannot forge.** These
agents write *real, checkable* falsifiers. My frequency count measured the word;
it did not measure the practice, and I should not have reasoned from the one to
the other.

**A VERIFIED specimen of the healthy case, which I checked myself rather than
trusting the child's citation** — `.swarm/journal/opencode-plugin-scout.md:429`
names a falsifier:
> *"FALSIFIER for option (c): if `messages.transform`'s injected message does NOT
> persist into the session's stored history … the agent would 'forget' its mail.
> My run cannot distinguish these. THIS MUST BE TESTED before (c) is
> recommended without caveat."*

…and `:435`, six lines later, is the entry header:
> *"## MY OWN FALSIFIER FIRED. `messages.transform` is a VIEW transform, not a
> session write. Option (c) is DEAD as stated."*

**Named, tested, fired, course changed, recorded.** That is the doctrine working
exactly as designed, and it is in the files.

**THE VERDICT NEVERTHELESS STANDS — `falsifier-not-honored` is NOT detectable —
but for a structural reason neither I nor the brief anticipated.**
`falsifier-probe`'s real finding:

> **93 of 103 journals name their last falsifier in their LAST ENTRY, and then
> stop writing.**

**The agent's final act is to name the thing that would prove it wrong — and
then it ceases to exist.** The falsifier is not *ignored*; it is **orphaned by
the ritual's own shape**. There is no "next" in which to honor or defect. **An
instrument cannot detect a course-change that had no subsequent course**, and
the pathology is *undefined*, not hidden, for the overwhelming majority of the
corpus.

**FIRED-IGNORED count: ZERO.** Four readers hunted it and none manufactured one.
**And `falsifier-probe` keeps its own honest limit, which I ordered it to keep
and verified it did** (its §7): *"I found no pathology. I am not confident there
is none. Those are different claims"* — the gap between them is precisely the 93
journals that stopped writing.

**The asymmetry remains the honest one-liner, now properly grounded: agents
demonstrably honor falsifiers and record it (17 instances). The record has no
place to show one being ignored — and mostly no *later turn* in which it could
have been.** Compliance is self-reported; defection is self-concealing; and
death is the most common answer of all.

### 3.6 DUPLICATE WORK AMONG TOP-LEVEL AGENTS — **DETECTABLE from briefs; instances found, but MOST ARE LEGITIMATE SEQUELS.**

**Detectable: YES, cheaply** — the `task` field of `.swarm/agents/*.json` is the
full spawn brief, and overlapping briefs are readable side by side.

**The critical distinction (and the reason a naive duplicate-detector would be
mostly wrong): this swarm's top layer is FULL of near-identical briefs that are
NOT duplication — they are an ITERATION CHAIN, and each one says so in its own
first sentence.** VERIFIED from the briefs:

- `decision-scout` → `decision-wiring`: *"you succeed decision-scout, whose
  deliverable the operator **RETURNED** with the verbatim reason…"*
- → `proxy-scout`: *"the operator asks whether the assumed decision engine
  generalizes…"*
- → `pipeline-scout`: *"**third iteration** of the decision-engine wiring"*
- → `hook-scout`: *"**v4** of the decision-engine wiring — the operator
  **overruled** the zero-tool-change constraint every predecessor assumed"*
- `fleet-scout` → `fleet-eval`: *"You succeed fleet-scout; keep FLEET.md's
  execution-surface findings, **discard** its leaf-only emphasis. The operator's
  **correction**…"*

**Five top-level agents, each a fresh name, each re-attacking the same question
with one operator correction folded in.** That is not duplicate work; it is a
**design being iterated by close-and-respawn** — exactly the maneuver SPAN.md
§3b prescribes in place of re-parenting (*"harvest, close, respawn under a brief
that points at the predecessor's journal"*). **The record shows the doctrine
working.**

**Real duplication — the one instance: `updater` / `updater-v2` (§3.2).** Two
top-level agents, same standing role, same brief opening, overlapping in time,
one of them stillborn. This is the only pair I can call true duplication from
the briefs.

**Honest ambiguity — `structure-scout` (07-10) vs `operator-structure-scout`
(07-12):** both are "design research into where tree structure comes from," 2
days apart. The second's brief names a *new fact* (VERIFIED: *"replaces the
coordinator-stance half of the shipped onboarding doctrine, which live F1
testing proved fails 2/2"*), so it is a sequel, not a repeat — **but it is a
sequel that re-derives ground `structure-scout` already covered**, and *this
very document* is a third pass over the same territory. **REASONED: the shape
"re-research the tree's own structure" has now recurred 3× under 3 names in 3
days. That is the strongest standing-role signal in the record, and it is about
the very question this review was convened to answer.**

The full duplicate-work census over all 117 briefs is `role-census`'s
deliverable (`docs/audit/org-review-roles-2026-07-12.md`); §4 below reports the
counts I measured directly.

---

## 4. RECURRING ROLES — the standing-role signal, counted

**Method note (and a mistake I made and corrected):** my first pass classified
roles by grepping the briefs for adversarial verbs and got **67** hits — because
*every* brief contains the word "falsifier" (the spawn header injects the duty).
**That number is garbage and I am discarding it.** The defensible count is by
**name**, which is chosen deliberately by the spawning parent and is therefore
evidence of intent.

### 4.1 The RED role: **19 distinct names, 3 days, ZERO name reuse. MEASURED.**

**VERIFIED** — every agent whose name contains `red`:

```
07-10  red-simplest, red-operator, red-decisions, red-wiring, red-proxy
07-11  pipeline-red, hook-red, eval-red, eval-red-glmforensics
07-12  onboarding-red, v3-red, dp-red, structure-red, structure-red2,
       red2-trace, red2-mech, red2-doctrine, oc-red, structure-red3
```

**19 agents. 19 distinct names. Spread across 07-10, 07-11, 07-12 — three
consecutive days.** (Add the `*-redcheck` pair — `pipeline-redcheck`,
`hook-redcheck` — and it is 21.)

**MEASURED — the shape is structural, not incidental: 22 distinct coordinators
in this swarm spawned at least one adversarial child, and every single one
minted a fresh name for it.** `operator-structure-scout` alone burned three:
`structure-red`, `structure-red2`, `structure-red3` — the same role, three
times, in **46 minutes** (16:01, 16:22, 16:45).

### 4.2 The SCOUT role: **16 distinct names, 4 days. MEASURED.**

```
07-09  codex-scout
07-10  structure-scout, inbox-scout, harness-scout, quota-scout, switch-scout,
       decision-scout, ws-hooks-scout, proxy-scout
07-11  pipeline-scout, hook-scout, fleet-scout
07-12  onboarding-scout, operator-structure-scout, opencode-plugin-scout,
       org-review-scout
```

**16 names. 4 consecutive days. 12 of the 16 are top-level** (children of
operator) — the scout *is* the operator's standard top-level unit.

### 4.3 What this means against STRUCTURE.md. MEASURED + REASONED.

STRUCTURE.md §2b (VERIFIED, written 07-10 when the swarm had ~12 dead agents)
concluded:

> *"the structural signal is not 'this kind of work keeps arriving' — it is
> 'I, the dispatcher, keep choosing to reuse this name.'"*

**The data now available (94 dead agents, 5× the evidence STRUCTURE.md had)
puts that conclusion under real strain, and I report the strain rather than
resolve it:**

- **MEASURED:** by STRUCTURE.md's own test — *re-addressing a warm name* — only
  **2 roles ever stood**: `hardener` (14 Tasks to one name) and `field-tester`
  (9+ dispatches to one name). Everything else was close-and-respawn.
- **MEASURED:** meanwhile the **red role recurred 19 times across 3 days and the
  scout role 16 times across 4 days, and *not once* did a dispatcher re-address
  a warm one.**

**REASONED — and this is the finding I most want a red team to attack:** those
two facts are usually read as "red/scout are one-shot work, correctly
close-and-respawned." But the **name rule makes the alternative unobservable.**
WORLD concept 3 forbids reusing a name, so *no dispatcher who wanted a standing
`red` could have expressed it* — they'd have had to do what the operator did
with `updater-v2` (§3.2), and that died stillborn. **STRUCTURE.md's signal ("I
keep choosing to reuse this name") can only ever be emitted by roles the tool
permits to persist. It cannot, even in principle, detect a role that recurs 19
times under 19 names.** The measurement instrument and the naming rule are
entangled, and the 19-vs-2 gap is where that shows.

**Falsifier for this reading:** if the 19 red briefs turn out to be
substantively *different* jobs (attack a design doc / verify a benchmark / audit
a graveyard), then "the red role recurred" is my own pattern-matching on a
prefix, and the correct count is much lower. **`role-census` was testing exactly
this by classifying all 115 briefs by their verb, not their name.**

### 4.4 RECONCILED against `role-census` — my number was LOW, and the falsifier resolved in favour of the claim. MEASURED.

`role-census` has landed (`docs/audit/org-review-roles-2026-07-12.md`). **Its
brief-verb classification finds MORE recurrence than my name-prefix count, not
less:**

| role | **my count** (name prefix) | **`role-census`** (brief verb) |
|---|---|---|
| RED | 19 | **25** distinct names, 0 reused, **14 different parents**, 3 of 4 days |
| SCOUT | 16 | **21** |
| FORENSICS | *(not counted)* | **34** |

**My falsifier did not fire — it resolved the other way.** I had worried that
prefix-matching *inflated* the red count; classifying by what the brief actually
*asks for* **raises it from 19 to 25**, because six agents do adversarial work
without "red" in the name. `role-census` also reports the **`scout → drafter →
red` three-stage shape ran 4 times in full, with all-new names each time**
(VERIFIED, its §1 row 2).

**So the §4.3 reading stands and strengthens: three roles — RED (25), FORENSICS
(34), SCOUT (21) — were each re-instantiated dozens of times, under a fresh name
every single time, and not one name was ever reused.** The two counts were taken
by different methods over the same corpus and agree in direction; where they
differ, **`role-census`'s is the better number** and I adopt it.

**And it supplies the control that makes the "spread, not burst" claim
non-vacuous** (VERIFIED, its §C): RED spans **3 of 4 days / 49.2h / 14 different
parents**; SCOUT, FORENSICS and RUNNER span **all 4 days / 65–70h**. Against
that, the `OTHER` class (the three SPAN test fixtures) is **3 instances in 24
minutes under 1 parent** — a textbook burst. **The metric separates cleanly, and
the recurring roles land on the standing side of it.**

### 4.4b THE REPEATED PIPELINE — the same org shape rebuilt from scratch 4 times, 12 fresh names. VERIFIED.

`role-census` confirmed the specific hypothesis, and **I verified all 12 agent
records exist** (`.swarm/agents/*.json`, every name present):

| # | scout | drafter | red |
|---|---|---|---|
| 1 | `decision-wiring` | `wiring-drafter` | `red-wiring` |
| 2 | `proxy-scout` | `proxy-drafter` | `red-proxy` |
| 3 | `pipeline-scout` | `pipeline-drafter` | `pipeline-red` **+ `pipeline-redcheck`** |
| 4 | `hook-scout` | `hook-drafter` | `hook-red` **+ `hook-redcheck`** |

**The full `scout → drafter → red` three-stage shape ran EXACTLY 4 times, with 12
fresh names and no name shared with any predecessor.** The weaker
`design → attack` two-stage shape ran **9 times**.

**And the shape EVOLVED across its own repetitions** (VERIFIED): families 3 and 4
added a **second, independent red** — because a drafter's own child inherits its
blind spots. `hook-redcheck`'s brief says so verbatim. **Nobody designed that
improvement into a template; it was re-derived, and then improved, by
independent dispatchers.**

**The finding behind the finding** (VERIFIED from the briefs): those four
families are **one question asked four times** — the decision-engine wiring. The
briefs admit it themselves: *"third iteration"*, *"v4 — the operator overruled
the zero-tool-change constraint every predecessor assumed"*, *"you succeed
decision-scout, whose deliverable the operator RETURNED"*. **So it is iteration,
not waste (§3.6) — and simultaneously, the same org shape was rebuilt from
scratch five times with 5 scouts, 4 drafters and 6 reds, sharing not one name.**

### 4.5 The gap `role-census` found in STRUCTURE.md's doctrine — and why I think it is real. REASONED.

`role-census` reported a limit it was careful not to rule on (it was briefed to
count, not to design), and it is the sharpest observation either of us made:

> STRUCTURE.md §2b dismisses raw repetition with the span-probe case — **9 tasks
> in ONE queue, ONE hour, ONE parent** — and correctly calls that *backlog*, not
> structure. **But RED is the opposite on every axis: 25 instances / 14 parents /
> 3 days.** The doctrine rules out backlog-in-one-queue. **It is SILENT on a shape
> that 14 independent dispatchers each re-derive from scratch.**

**REASONED, and it is my §4.3 argument arriving from the other side:**
STRUCTURE.md's test — *"I, the dispatcher, keep choosing to reuse this name"* —
can only be satisfied by a **single** dispatcher re-addressing a **warm** name.
It is structurally incapable of registering a shape that **14 different parents
independently invent 25 times**, because (a) no one dispatcher repeats, and (b)
WORLD concept 3 forbids the name reuse the test watches for. **The doctrine's
signal and the tool's naming rule are entangled, and the 25-vs-2 gap is exactly
where that shows.**

**Falsifier:** if the 25 RED briefs are substantively different jobs, "the role
recurred" is pattern-matching on a role label. `role-census` classified by brief
verb precisely to test this, and its per-agent table (all 115 rows, cited) is the
audit surface. **I have not independently re-classified all 25; I spot-checked
its boundary calls and they held.** This is REASONED, not MEASURED, and I mark it
so.

---

## 5. WHAT THE JOURNALS DO NOT CONTAIN — the critical negative finding

This is the section I was asked to make the centerpiece, and it is the one I am
most confident in. Every item below is **VERIFIED** by enumerating the record's
fields (§0), not inferred.

**The record has 8 agent fields and 3 event fields. Here is what an instrument
would want and cannot have:**

1. **No death.** No close time, no closer, no reason. Death is *computed at read
   time* from herdr pane liveness (`bin/swarm:514`). **A closed agent and a
   crashed agent are identical in the files, and a restarted herdr would
   resurrect the entire graveyard.** Every lifetime in §1 is a proxy.

2. **No cost.** No tokens, no dollars, no turn count, no wall-clock-of-work.
   `fleet-eval` ran a **paid multi-model benchmark** with a costed dollar cap
   (VERIFIED: `battery-smith`'s brief says *"a costed dollar cap"*) — **and the
   swarm's own record does not know what it spent.** Any question of the form
   "was this subtree worth it" is unanswerable from `.swarm/`.

3. **No verdict.** `queue/<name>/delivered/` records that a message's **bytes
   reached a turn** — and, by explicit design, *nothing else*. WORLD concept 8:
   *"Judge artifacts, never claims. There is no ack, no status taxonomy, no
   compliance record."* **So the single most important fact about any agent —
   did its parent accept its work? — is nowhere in the files.** It exists only
   as prose in the parent's journal, if the parent bothered. **This is not an
   oversight; it is the contract.** An instrument that wants to know "which
   subtrees produced accepted work" must reconstruct it from natural language,
   or not at all.

4. **No harness-subagent trace.** SPAN.md §3d′ establishes that doctrine-bearing
   agents *prefer* rung 2 (in-session Task subagents) over rung 3 (swarm
   children) — the span-doctrine probe fanned nine tasks to harness subagents
   and beat baseline 3× **with zero tree footprint**. **Those subagents have no
   name, no pane, no journal, no record.** Consequence, stated bluntly: **`swarm
   ps` systematically under-counts delegation, and every "zero children ⇒ did
   not delegate" inference in §2.2 and §3.4 — including mine — is unsound
   against this blind spot.** This is the largest hole in the evidence base and
   it cannot be closed from `.swarm/`.

5. **No link from agent to artifact.** Nothing connects `structure-scout` to
   `docs/design/STRUCTURE.md`. The agent wrote the file; the record does not say
   so. I recovered every such link **by reading prose**. There is no field for
   "what did this agent produce."

6. **No falsifier firing.** (§3.5.) The journal records a falsifier being
   *named* and — when the agent is honest — being *honored*. It has no place to
   record one being *ignored*, and no independent observation of the firing
   event. **Compliance is self-reported; defection is self-concealing.**

7. **No reason for a spawn — or for a non-spawn.** The brief says *what*, never
   *why this shape*. And the negative decisions — the coordinator not spawned,
   the child not closed, the 6th top-level agent the operator didn't open (§2.1)
   — leave **no trace whatsoever**. **The tree records what happened; the
   structural *choices* that produced it are entirely absent.** For a review of
   *structure*, this is the deepest gap: the shape is visible, the judgment that
   made it is not.

8. **No idle-by-design flag.** (§3.1.) `updater` quiet for 3h is healthy;
   `hardener` quiet for 15h is blocked. **The record cannot tell them apart** —
   the difference lives in the prose of two briefs.

**One sentence: `.swarm/` is an excellent record of WHAT WAS SAID and a poor
record of WHAT WAS DONE, and it contains no record at all of WHAT WAS DECIDED
NOT TO DO.**

---

## 6. NULL RESULTS — things I looked for and did not find

Stated so they cannot be quietly dropped:

- **NULL — the flat top-level tree.** 12 of 25 top-level agents delegated. The
  claim "the operator spawns workers directly instead of coordinators" is
  **NOT SUPPORTED** by the census (§2.2).
- **NULL — never-delegated-but-should-have.** **No instance found** at the top
  level. Every zero-child top-level agent is short-and-single-question or
  serial-by-brief (§3.4). *Weakened by blind spot #4: harness-subagent
  delegation is invisible.*
- **NULL — falsifier-not-honored, detectable from files. RESOLVED, and it is a
  hard null:** 135 statements hand-read, 4 readers, rubric pre-registered.
  **FIRED-IGNORED = ZERO.** But the mechanism is not the one I predicted: **93 of
  103 journals name their last falsifier in their LAST ENTRY and then stop
  existing** — the falsifier is *orphaned*, not ignored, and the pathology is
  **undefined** rather than hidden (§3.5b). **My own "it's just ritual"
  hypothesis was REFUTED: zero of 135 statements were unfalsifiable boilerplate;
  105 name a witness the agent cannot forge.**
- **NULL — duplicate work as waste.** The five-agent decision-engine chain and
  the fleet chain *look* like duplication and are **not** — each brief names the
  operator correction that made it necessary. **One** true duplicate found
  (`updater`/`updater-v2`), and it was caused by the name rule, not by
  carelessness (§3.6).
- **NULL — the operator's declared span (~3) in the record.** The observed
  ceiling is **5**. Nothing in the files records the operator's span, or any
  agent respecting it. SPAN.md §1 says so itself: *"nothing in the tool today
  respects, records, or even mentions it."* Still true (§2.1).
- **NULL — any record of a structural decision.** No spawn reason, no close
  reason, no close time, no "I considered a coordinator and declined" (§5.7).
- **NOT NULL — the three long-lived top-level agents are STANDING, not leaked**
  (§6b). This was the one hypothesis I was re-scoped to test that came back
  **positive**, and it inverts the "close them" advice.

- **NOT DELIVERED — the full compliance-rate measurement.** My brief asked how
  many journals pair a reconciliation with a named falsifier. `fp-compliance`
  owned it, forwarded it to 8 descendants, and **died without writing its
  synthesis** (§7a). `falsifier-probe` recomputed the load-bearing numbers itself
  and refused to claim the dead child's shards. **I am recording this as a hole,
  not letting the surviving numbers imply full coverage. The layer that failed
  was one I created.**

**Cross-check against the sibling collectors** (`org-review-scout` reports these
independently; recording them here so this document is not read in isolation):
F-SPAN does not fire (0 of 61 operator-bound messages came from depth ≥2);
duplicate work does not fire among the 25 top-level agents; breadth does not
fire (peak concurrent = 5 — **which independently confirms my §2.1 ceiling by a
different method**). **Recurrence is the one signal that fires, and it fires
hugely** (§4.4).

---

## 6b. STANDING OR LEAKED? — the three long-lived top-level agents. **VERDICT: STANDING. All three.**

`org-review-scout` re-scoped me to settle one question, because his own
recommendation turns on it: **`hardener`, `field-tester` and `updater` are the
only three top-level agents that lived past 2h** (the other 22 all died under
2h). Is that longevity **real standing structure** — a role re-used across
sessions — or is it just **rot**: agents that finished, went idle, and nobody
closed? If it's rot, the honest advice inverts from "name these roles" to
"close them."

**The test, stated before I ran it:** a *standing* agent receives **separated
dispatches over time** — multiple distinct tasks, arriving at different times,
with real gaps between them, from a dispatcher who chose to re-address this name
rather than spawn fresh (STRUCTURE.md §2b's own criterion). A *leaked* agent
does one burst of work, files a terminal report, and sits.

**The evidence is the `delivered/` queue — a world-readable record of every
message that consumed a turn (WORLD concept 4).** This is a *harder* fact than
the journals: an agent can write anything, but a delivered message is a file
with a sender and a timestamp.

### MEASURED — dispatches received, by sender and day:

| | `hardener` | `field-tester` | `updater` |
|---|---|---|---|
| **delivered messages, total** | 17 | 67 | 6 |
| **from the operator** | **17** | **13** | **6** |
| from its own children | 0 | 54 | 0 |
| **days it received operator dispatches** | **07-09, 07-10, 07-11, 07-12** | **07-09, 07-10, 07-12** | **07-09, 07-10, 07-11, 07-12** |
| **first → last operator dispatch** | 07-09 18:58 → 07-12 01:50 | 07-09 18:46 → 07-12 15:59 | 07-09 22:22 → 07-12 13:43 |
| **span of dispatch** | **54.9h** | **69.2h** | **63.4h** |
| gaps between operator dispatches | 1.3, **15.6**, 0.2, 0.2, 0.9, 0.4, 3.2, 0.2, 1.0, **14.6**, 2.0, 0.0, 0.3, 0.1, 0.4, **14.5** h | 0.1, 0.0, 0.1, 1.1, 0.1, 0.3, 3.2, 0.2, **32.8**, 0.0, **12.0**, 0.4 h | **14.0, 23.1**, 0.1, **14.3, 11.8** h |
| **gaps > 4h (= a re-awakening)** | **3** | **2** | **4** |

**Every one of the three was re-addressed by the operator, by name, after gaps of
12–33 hours — repeatedly, across four calendar days.** Nobody re-dispatches to a
corpse. **This is precisely STRUCTURE.md §2b's signal — *"I, the dispatcher,
keep choosing to reuse this name"* — and here it is, three times, in the
hardest record the system keeps.**

### VERIFIED — separated work, from the journals' own entry headers:

**`hardener` — 20 entries, a numbered serial task queue spanning 4 days:**
```
07-09  spawned · Task 1 underway · Task 1 GREEN · Task 2 GREEN
07-10  Task 3 GREEN · Task 4 GREEN · Task 4 amendment · Task 5 · Task 6 ·
       Task 7 · Task 8 · Task 9 · Task 10 GREEN
07-11  Task 11 GREEN · Task 12 checkpoint · Task 12 correction · Task 12 FINAL
       SPEC · Task 12 COMPLETE · Task 13 GREEN
07-12  Task 14 GREEN, reported
```
**Fourteen numbered Tasks, individually dispatched, across four days.** This is
not one burst. It is a standing implementer being fed work by the operator, and
the operator's own dispatch style names the recurrence every time ("Task N") —
exactly the convention STRUCTURE.md §3 identified as already running by hand.

**`updater` — 18 entries, an unbounded watch loop across 4 days:**
```
07-09  spawned · watcher started · killed ×3, restarted · switched to Monitor
07-10  eac88e2→2272b38→85776d4 · →63d1a79 (PR#71) · →9402f94 (#72+#73) ·
       →ef72109 (#74) · →7e5a644 (#75+#76) · →6d30e12 (#77) · →834fec4 (#78)
07-11  →aa6063d (PR#80, send middleware) · v1.2.0 tag heads-up
07-12  →1e254e4 (PR#81) · →b94fa9e (PR#82, onboarding doctrine)
```
**Eleven distinct update cycles, each a real PR merged into the live install.**
Its brief has **no terminal state** ("keep the installed swarm tooling current")
— STRUCTURE.md §2c already classified this as *standing structure designed in
from the brief*, and the four-day cycle record confirms it empirically.

**`field-tester` — 37 entries, 3 days, and it is the swarm's only real
coordinator:** WATCHLIST probes (07-09) → delegation baseline/after pairs
(07-10) → SPAN flood ×3 (07-10) → workspace-bug verification (07-12) → FLEET v3
runners (07-12) → doctrine probe + red review (07-12). **16 children spawned and
closed across those campaigns — the largest subtree in the swarm.** It received
**54 messages from its own children** in addition to the operator's 13. That is
a standing measurement arm, doing genuinely separated campaigns with a 32.8h gap
between two of them.

### The three last entries — terminal, or naming a next task?

This is `org-review-scout`'s sharpest sub-test: *"an agent whose last entry is
'done, reported, no next task' and which has sat idle 15h is a leak, not a
role."* **All three fail the leak test — none is terminal:**

- **`hardener`** (VERIFIED, `.swarm/journal/hardener.md:299`, last line):
  > *"Idle, awaiting **field-tester verification / next dispatch**."*

  **It explicitly names a next task.** Not "done" — *awaiting*. Its work
  (`swarm-dev/workspace-pin`) is on a branch, unpushed, pending verification.
- **`updater`** (VERIFIED, final entry, 07-12 13:44): a completed cycle report
  ending in a falsifier about the *current* install state
  (*"origin/main != b94fa9e, HEAD != b94fa9e, or COORDINATING.md unreachable"*).
  **A watch loop between firings is not idle; it is watching.** Its Monitor is
  the next task.
- **`field-tester`** (VERIFIED, final entry, 07-12 16:35): *"All probe subtrees
  closed. **Open offers with the operator: root-rename experiment, F2 cold
  control, compaction variant, true pre-doctrine baseline.**"*

  **It closed its children and left four named next tasks on the table.** That is
  the opposite of rot: it is an arm that has tidied up and is holding, with a
  declared backlog.

### CORROBORATION FROM OUTSIDE `.swarm/` — the git record. VERIFIED.

Everything above is drawn from the swarm's own files. **`hardener` is the one
agent whose output can be checked against an *independent* record — git — and it
holds.**

**VERIFIED:** `hardener`'s journal names **11 distinct `swarm-dev/*` branches**
across its 14 Tasks. **Every one of them exists in git:**

```
swarm-dev/delegation-doctrine   swarm-dev/rering-bound
swarm-dev/engine-hook           swarm-dev/send-note
swarm-dev/hardening             swarm-dev/span-doctrine
swarm-dev/naming-edges          swarm-dev/standing-goals
swarm-dev/operator-seat         swarm-dev/workspace-pin
swarm-dev/world-queue-ownership
```
(12 local `swarm-dev/` branches exist; 11 are claimed by name in
`.swarm/journal/hardener.md`, and 8+ are pushed to `origin`.)

**This is the ONLY agent→artifact link anywhere in this review that is
verifiable outside `.swarm/`** — and it is exactly the link the record itself
does not store (§5.5). It is decisive for §6b: **a leaked agent does not produce
eleven merged-or-pushed branches across four days.** The standing verdict for
`hardener` no longer rests on the swarm's self-reporting at all.

**And it sharpens `role-census`'s most surprising number** (VERIFIED, its §77,
§85): **BUILDER = 3 of 115 agents (2.6%)** — `hardener`, `skill-writer`,
`battery-smith`. **~97% of this swarm's entire agent-population was research,
critique, and evidence; ~3% wrote code.** Cross-checked independently: **41 of
135 briefs *explicitly forbid* writing code** ("you write NO product code",
"design only", "research-only", "READ-ONLY").

**REASONED — the structural reading:** the swarm's *one* long-standing
implementer produced essentially all of its code, while a hundred short-lived
agents produced the design and evidence that told it what to build. **Whatever
else the top layer is, it is not a workforce — it is a research organization
with a single hands.** That is a fact about this swarm's shape that no pathology
scan would have surfaced, and it is measured, not asserted.

### VERDICT — and it inverts the "leak" hypothesis, but one caveat survives

> **MEASURED + VERIFIED: `hardener`, `field-tester` and `updater` are STANDING
> AGENTS, not leaked ones.** Each received repeated, separated, operator-issued
> dispatches across 55–69 hours and three-to-four calendar days, with 2–4
> re-awakenings after gaps of 12–33 hours. Each did real, distinct work in each
> window (14 numbered Tasks / 6 probe campaigns / 11 update cycles). **None of
> the three has a terminal last entry** — one names its next task explicitly, one
> is a watch between firings, one holds four open offers.

**The honest caveat, which I will not bury (REASONED):** *standing* and *idle
too long* are not exclusive, and `hardener` is currently **both**. It is a
genuine standing role **and** it has sat 15h waiting on `field-tester`, which is
now **dead** (§3.3). **The correct reading is not "close hardener" — it is
"hardener's standing role is real and its current block is a dangling
dependency on a closed agent."** A leak-detector keyed on idle-time alone would
have thrown away the swarm's most productive implementer. **The distinguishing
fact — that the thing it waits for no longer exists — is exactly the one
finding in this document that is both file-detectable and actionable.**

**Falsifier for this verdict:** if the 17/13/6 operator dispatches turn out to be
mostly acknowledgements or FYIs rather than *new work* (I counted delivered
messages by sender, and I read the journal entry headers that resulted from
them, but I did not read all 36 operator message bodies in full), then "repeated
dispatch" is inflated. The journal-header evidence — 14 numbered Tasks, 11
update cycles, 6 probe campaigns — is independent of the message count and
survives that objection, which is why I lead with it.

---

## 7. MY OWN SUBTREE, JUDGED — an instance of the pathology I was sent to find

Discipline requires I turn this on myself. I spawned 2 children; **they each
immediately spawned 4**, and `falsifier-probe`'s branch then split *again* —
`shape-forensics → falsifier-probe → fp-compliance → fpc-s2 → fpc-s2-ft`, **five
levels and twelve descendants**, for what was, in the end, **two counting
questions.** Both children journaled properly and both named falsifiers,
including plans to blind-check their own children's classifications — **the
delegation was well-run, and it was still far too much tree.**

**My parent caught this and ordered the collapse, and he was right.** I had
already reached the same judgment independently in this section — but *he acted
on it and I had only written it down*, which is the whole difference between a
reconciliation and a note. **I harvested `falsifier-probe`'s subtree (the three
slice artifacts, 145KB, were already on disk) and ordered the layer closed.**
The reason, journaled: SPAN.md §3d — *"Depth is a cost, not a virtue… Split
under pressure, never in anticipation"* — and a question whose honest answer is
a **null** never needed five levels to establish.

**The irony is the finding.** `falsifier-probe`'s result, arrived at *before* the
collapse, is that **93 of 103 journals name their last falsifier in their last
entry** — the ritual's own shape orphans the falsifier, because the agent's final
act is to name it and then cease to exist. **I did the same thing one layer up:
I wrote "I over-delegated" into §7 and would have gone idle on it.** The
correction came from *my parent reading my tree*, not from my own reconcile —
which is precisely the mechanism WORLD concept 2 relies on (*"your parent judges
and approves your work"*) and precisely the mechanism this document shows the
files cannot support on their own (§5.6).

### 7a. The over-delegation had a MEASURED COST, and it is the exact failure SPAN.md predicts. VERIFIED.

I can do better than confess to a bad tree — **I can price it.** The middle layer
I grew, `fp-compliance`, **died without producing its deliverable.**

- **VERIFIED —** `fp-compliance` was spawned by `falsifier-probe` to own the
  compliance-rate measurement. It **wrote a shard-brief**
  (`docs/audit/_fp-compliance-shard-brief.md`, 5024B, VERIFIED on disk) and
  **fanned out 8 descendants** (`fpc-s0..s3`, `fpc-s2-{ft,mid,small,tail}`,
  `fpcs3-{a,b,c}`).
- **VERIFIED — `docs/audit/_fp-compliance.md` DOES NOT EXIST.** Its synthesis was
  never written.
- **VERIFIED — `.swarm/journal/fp-compliance.md` has 3 entries** and ends
  mid-plan, on an instruction *to* its children: *"…all four children to
  OVER-report Q6 candidates for exactly this reason. If they return zero I did
  not already have, my number stands as a true total; if they return several, I
  must relabel Q6 as a lower bound and say so."* **It never got the answer. It
  briefed, it forwarded, and it died.**
- **VERIFIED — `falsifier-probe` reported this failure to me itself, unprompted,
  rather than papering over it:** *"fp-compliance FAILED: it fanned out a shard
  subtree and died before writing its synthesis; `_fp-compliance.md` never
  existed. I did NOT claim its numbers — I recomputed the load-bearing ones
  myself and NAMED THE FAILURE in §6."*

**This is SPAN.md §3d, quoted verbatim and then demonstrated:**

> *"A middle layer that only forwards — adds no judgment, writes no synthesis —
> is structure lying about work, and its parent should close it."*

**`fp-compliance` is exactly that layer, and the commissioned measurement it
owned was never delivered.** Part of the compliance-rate question in my own brief
is therefore **not answered**, and I am recording that as a hole rather than
letting the surviving numbers imply full coverage. The work was salvaged only
because `falsifier-probe` **recomputed the load-bearing numbers itself** instead
of trusting a dead child's shards.

**MEASURED cost of my over-delegation: one middle layer, 9 agents, zero
artifacts, one undelivered measurement.** This is the single most concrete
instance of a structural pathology anywhere in this document — **and I caused
it.** It is worth more as evidence than any of the pathologies I went looking for
and did not find.

**The recurrence I am obliged to name (spawn-header duty: "when you dispatch to
a name you have dispatched to before, say what recurred"): every coordinator in
this swarm, including me, fans out 2–5 children on its first turn.** `grave-org`
→ 3 → one of which spawned 3 more. `falsifier-probe` → 4. `role-census` → 4.
`operator-structure-scout` → 5. Me → 2 → 8.

**MEASURED, whole tree: 27 of 117 agents spawned a child; the modal
first-turn fan-out is 3.** **REASONED:** the delegation doctrine
(SPAN.md §2: *"agents reliably execute structural moves that are in their
frame"*) is working — perhaps *too* well. The frame says *delegate by default*
and *doing parallelizable work serially is off-track*, and agents obey it on
their first turn, **before they know whether the work is large enough to
need it.** The evidence for over-delegation is not opinion: it is that a
two-question mandate grew an 11-agent subtree, and I am the one who grew it.
**Falsifier: if `falsifier-probe`'s and `role-census`'s deliverables each show
work that genuinely required four parallel readers, this reads as correct
delegation and my self-criticism is wrong.** Their artifacts settle it, and I
have staked the claim before reading them.

---

## Appendix — reproduction

Every number here is re-derivable. Population: `.swarm/agents/*.json` (parent
map), `.swarm/event/*.json` (last stop), `.swarm/journal/*.md` (mtime, `^## `
entry count), `swarm ps` (liveness — **note this is computed live from herdr
panes, so it is not reproducible from the files alone**; see §0).

Top-level set = `{n : agents[n].parent == "operator"}` → 25 names, listed in §1.
