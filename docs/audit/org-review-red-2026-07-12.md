# RED TEAM — the adversarial review of ORG-REVIEW.md

> SUPERSEDED by nothing directly (no corrected "ORG-REVIEW.md v2" found in this file set — a live, consequential disagreement); kept for the record (the "MAJOR SURGERY" verdict — kills the flagship BLOCKED example as factually false, narrows SPAN clearance — flagged for a human check whether docs/design/ORG-REVIEW.md was actually revised post-review).

**Reviewer:** `org-red`, spawned to kill. Child of `org-review-scout` (the doc's author).
**Target:** `docs/design/ORG-REVIEW.md` @ `main@aa6063d`, 2026-07-12.
**Method:** the repo's audit procedure — evidence read in full **before** the target; the findings
file read **last**. Every number below I re-ran myself at source. I trusted neither the doc, nor
its audits, nor my parent's mid-review injection.

---

# VERDICT: **MAJOR SURGERY**

Not a kill. But not a clearance either, and the doc does not survive in the form it was written.

**The single strongest argument for killing the whole thing** — the one I would lead with if the
operator wanted it dead — is this:

> **The document's flagship example is false, and it is false in exactly the way the document
> predicted its own evidence base would fail.**
>
> §4b′ prints `⚠ BLOCKED — hardener, your most productive agent, has been blocked for 15 hours
> waiting on field-tester, which is dead.` The doc calls this *"the best line on the page,"* *"the
> design's central claim, tested on a live example and holding,"* and *"worth more than every
> recommendation I could have written."* **It is not true.** `field-tester` was alive and working
> all day today — it mailed the operator at 18:41, 19:41 and 20:02, *fourteen hours after* the
> `hardener` journal line the doc quotes as proof of blockage. It was the busiest agent in the
> swarm and was closed **on harvest**, at the end, having finished. `hardener` is not blocked on a
> corpse. Its own quoted sentence says what it is waiting for: *"field-tester verification / **next
> dispatch**"* — it is idle awaiting **the operator**.
>
> The doc read a `swarm ps` snapshot taken *after* the close and back-projected deadness onto a
> fifteen-hour-old journal line. **That is precisely §6d hole #1 — the doc's own finding that
> "THE RECORD HAS NO DEATH; a deliberate close and a crashed pane are byte-identical in the
> files"** — firing on the doc's own showpiece, six hundred lines after it wrote the warning.
>
> The reason this is an argument for killing the *whole thing*, not just deleting a block, is that
> §4b′ is not decoration. It is the **load-bearing proof of the design's central thesis** — that a
> reader beats an adviser because *"the reader cannot make that mistake, because it does not have
> an opinion to be wrong about."* The doc's own reader **did** make a mistake, of exactly the kind
> it claimed structural immunity to. A fact-sheet is not opinion-free if the facts are wrong; it
> just launders a wrong opinion into the voice of a file. **The instrument's promise — "it cannot
> be wrong in a damaging direction" — is refuted by the instrument's own demo.**

That said: I attacked the doc's §8 argument as hard as I know how, and **it held.** So the honest
verdict is surgery, not death. Findings below, ranked.

---

## The attacks that FAILED — stated first, because a red team that hides its losses is worthless

I was briefed that attack line **A** (the §8 equivocation) was the doc's weakest joint and that if
the doc was redefining "convention" to rescue a deliverable, that alone should kill it. **I went at
it hardest, and I could not break it.** I am obliged to say so.

**A1. The §8 "convention" reading is NOT a motivated redefinition. It is the repo's own.**

The prosecution's case (`org-review-phil8`) is that §8's four bullets all describe *a convention
the agents or the human were already performing*, so "the convention" can only mean "the human
reviewing their top layer" — which has zero instances — so the escape clause never opens. That is a
strong reading and I expected it to win.

It loses to a document the prosecutor quoted and stopped two lines short of. **`SPAN.md:236-239`,
VERIFIED verbatim at source:**

> *"**`ps` load metrics** (child counts, task counters per node): **not rejected — deferred.** `ps`
> already shows the tree and queue depths; span is visible by looking. **If the record shows
> parents failing the span test *because they cannot see it*, a derived count column is the
> instrument that earns its way in** (convention → instrument, in order)."*

This is the bullet **immediately after** the overseer/nag-reborn kill the prosecution used as its
hammer. The same document, in the same list, kills the standing overseer **and pre-registers a
read-only view**, and it states the trigger in operational terms: *a structural failure caused by
not being able to see it.* That is not `org-review-scout`'s paraphrase of §8 — it is the repo's own
restatement of §8, written by the doc that owns span, distinguishing the two rungs in consecutive
bullets. **The doc did not invent the reading. It found it.**

And the trigger is met. I verified `updater-v2` at source myself: `.swarm/agents/updater-v2.json`
exists (spawned by the operator, 07-10 17:09), its journal contains **only the spawn stub and not
one line of work**, and the warm `updater` it was meant to re-brief went on running for two more
days (139 journal lines, last cycle today). A top-level role the operator briefed, which never took
a turn, unnoticed for 48 hours — and unnoticed *because there is nothing to look at*: `ps` collapses
~120 dead agents onto one comma-separated line and prints no per-agent turn count. That is
"failing because they cannot see it," in SPAN's own words.

**A2. The PROXY-WIRING precedent does not transfer. The doc's distinction holds.**

I verified `PROXY-WIRING.md:296-321` at source. It demotes a standing observer agent, citing §8 by
name. But read its actual reasons: *"this observer answers no one, delays no one, and its output is
consumed only at stint time; **nothing reads it between stints and nothing pushes**."* **Every one
of those objections is an objection to a thing that exists between invocations.** `swarm review` has
no pane, no journal, no mailbox, no tokens, no turn. It is a `cat` with a parent-chain walk. My
parent explicitly told me that if this distinction fails the doc dies; I tried to make it fail and
it does not. The precedent is about the *standing form*, and the doc proposes none.

**A3. F, the nag check — clean.** I grepped the design for any push, hook, cadence, watcher, or
backdoor surfacing. There is none. The offer is killed in §5 with five arguments and does not
reappear anywhere, including in a "coordinator writes it in its journal" form (that line is
explicitly *pull, not push*). F5 pre-registers the grep that would catch its return. **This attack
lands nothing, and the §5 kill is the strongest section in the document.**

**A4. D, the nulls — all three verified independently, all three hold.** I did not trust the doc or
the audits. I re-ran them:

| null | doc claims | I measured | verdict |
|---|---|---|---|
| F-SPAN (agents below top layer mailing the human) | 0 of 61 | **0 of 61.** I walked every `queue/operator/delivered/*.json` sender through `agents/*.json` parent chains. 61 messages, 22 senders, **every one depth-1.** | **HOLDS** |
| Top-layer breadth | peak concurrent 5 | **peak concurrent 5** (computed from spawn `ts` → journal-mtime lifetime overlap; peak at 07-10 19:46: field-tester, hardener, red-operator, red-simplest, updater) | **HOLDS** |
| Duplicate work | 0 pairs of 25 | **holds at the sibling level** — see W4, where it holds for the wrong reason | **HOLDS, with a wound** |

**The design's premise — "3 of 4 pathology collectors return null, so show don't suggest" — is
sound.** The top layer really is not sick. That reasoning survives intact and it is the best thing
in the document.

**A5. G, the F1 self-indictment — I argue this is honesty, not a stop-ship.** The brief invited me
to rule that *"a design whose author expects its decisive falsifier to fire is a design that should
not ship."* I decline, and here is why: F1 is not "this design is probably wrong," it is *"the human
may not use it."* Those are different failures. A tool that is correct and unused costs ~140 lines
and one verb; a tool that is wrong and used costs decisions. Naming the adoption risk first is
§10 behavior (*correct the record, even against yourself*), and punishing it would teach the next
designer to hide it. **But it does raise the bar on cost**, and it is why W1 below matters: if the
author expects it to go unused, the +1 verb is a worse bet than the zero-verb fallback.

---

## The findings, ranked

### K1 — **KILL (the block, and the argument it carries).** The `⚠ BLOCKED` showcase is factually false.

**The claim** (`ORG-REVIEW.md:354-359`, `367-393`, `795-799`): *"`hardener` — 17 dispatches, 14
shipped Tasks, your most productive agent — has been blocked for 15 hours waiting on `field-tester`,
which is dead. Nobody noticed."* Presented as *"the best line on the page,"* the proof that showing
beats suggesting, and one of the *"two live defects"* in the closing argument.

**The evidence, at source:**

```
hardener      last journal write : 2026-07-12 05:52
field-tester  last journal write : 2026-07-12 20:02      <- 14h LATER
field-tester → operator mail     : 07-12 18:41, 19:41, 20:02
hardener's own quoted last line  : "Idle, awaiting field-tester verification / NEXT DISPATCH."
```

`field-tester` was not a corpse. It was **the most active agent in the swarm today** — running the
onboarding-doctrine falsifier probes, spawning `dp-red`, reporting to the operator three times this
evening — and it was closed **on harvest** at the end, having finished. The doc's `ps` snapshot was
taken after that close. It then attributed `hardener`'s idleness, which began at 05:52, to a death
that had not yet happened.

`hardener` is idle for the ordinary reason: it finished Task 14, reported, and is **awaiting an
operator dispatch**. Its own sentence — quoted in the doc — says so. There is no dangling dependency
on a corpse. There is a coordinator who has not sent the next task.

**Why this is a KILL and not a WOUND.** Three compounding reasons:

1. **It is the doc's central thesis, tested and failing.** §4b′ exists to prove *"the reader cannot
   make that mistake, because it does not have an opinion to be wrong about."* The reader made the
   mistake. The `BLOCKED` predicate is not a file fact — it is an **inference** (`X is idle` +
   `Y appears in ps's dead list` ⇒ `X is blocked on Y`), and it is exactly the kind of inference
   §4c's predicate rule was written to forbid. A wrong fact in a fact-sheet is worse than a wrong
   suggestion in an adviser, because the fact-sheet's whole warrant is that it has no opinion to be
   wrong about. **This is the doc's own §4b′ argument, turned around: an advisory instrument would
   have said "close hardener" and been wrong; the reader said "hardener is blocked on a corpse" and
   was also wrong — it just used the indicative mood.**
2. **The doc diagnosed the exact bug and then committed it.** §6d hole #1, VERIFIED at source
   (`bin/swarm:514`): *"THE RECORD HAS NO DEATH. `is_dead` is computed at read time from herdr pane
   liveness. A deliberate `swarm close` and a crashed pane are byte-identical in the files."* The
   doc wrote that warning, then built its showpiece on the difference between a close and a crash.
   **A design that cannot obey its own stated bound in its own demo will not obey it in shipped
   code.**
3. **It reached the operator's desk.** §9 (`What I would ship`) tells the human they have *"two live
   defects on your tree right now."* One of them is not a defect. Under PHILOSOPHY §10 — *"if you
   cannot prove the number is yours, do not print a number"* — and §4 (judge artifacts, never
   claims), a false alarm delivered to the human as a verified file fact is the worst artifact this
   system can produce.

**Minimum fix.** Three parts, all required:
- **Delete the `⚠ BLOCKED` block from §4b.** Not repair it — delete it. The predicate cannot be
  stated mechanically under §4c, because the record has no death (hole #1) and no dependency edge
  (hole #5: *"nothing links an agent to its artifact"*). Blockage is not in the files.
- **Retract the `hardener` claim in §9 and §0's closing sentence** (*"your best implementer has spent
  fifteen hours blocked on a dead agent"* — false), and correct the record explicitly, per §10.
- **Rewrite §4b′.** The section's *argument* is good and I want it kept — an advisory instrument
  really would have said "close it," and that really would have been wrong. But it must be argued
  from an example that is true, or argued hypothetically and labelled as such. Right now the doc's
  best reasoning is welded to its worst fact.

---

### K2 — **KILL (as written) / WOUND (as fixable).** The verb is broader than the clearance, and the doc knows it.

**The claim** (§6a′): SPAN.md pre-cleared this instrument. **The doc's own honest limit** (`:565-570`):

> *"SPAN licensed 'a derived count column'* on `ps`. **This document proposes six blocks, which is
> more.** If a reviewer rules that the clearance covers only a count column and not a page, the
> correct response is to narrow the page, not to widen the clearance."*

**I am that reviewer, and I so rule.** The clearance covers a **column on an existing verb**. The doc
takes it as a licence for **a new verb printing six blocks**, one of which (`BLOCKED`) is an
inference (K1), one of which (`RECURRENCE`) is a classifier over brief text, and one of which
(`REVIEW LATENCY`) calls an external network API. That is not narrowing; that is a factor-of-six
extrapolation from a deferred bullet.

Two independent reasons the transplant does not carry as far as the doc needs:

**(a) SPAN's trigger is about PARENTS. This instrument is about the OPERATOR.** SPAN:236-239 says
*"if the record shows **parents** failing the span test."* The doc's fired trigger (`updater-v2`) is
an **operator** failure. My parent asked me to press this and it is a real gap — but I rule it
**survivable**, because `skill/SKILL.md:44-49` (VERIFIED) explicitly folds the operator into the
span doctrine (*"The operator's span is smaller still: ask them what it is (default ~3)"*), and
because the operator is, in the relevant sense, a parent of the top layer. **Wound, not kill.**

**(b) The doc's own null refutes the span framing anyway.** §3.2 measured peak concurrent top-level
agents = **5**, declared span ~3, *"the declared span and the realized span match. The operator's top
layer was never over-wide."* I verified this: peak 5. So the operator is **not failing the span
test**. SPAN's clearance is triggered by *"parents failing the span test because they cannot see
it."* **The doc has measured, and published, that the span test is not being failed.** It then claims
the clearance whose precondition is a span failure.

The doc will answer that `updater-v2` is a *span-adjacent* failure of a different kind (a role that
was never staffed). That is a fair reading — but it is **a wider reading of the trigger than the
words support**, and it is the *second* place in the argument where the doc widens a clause to fit
its deliverable. Once is a legitimate reading (A1, which I cleared). Twice, in service of the same
conclusion, is a pattern the operator should see named.

**Minimum fix — and this is the surgery:** **narrow to what was licensed.** Ship the fired evidence,
not the page:
- **`ps` gains what SPAN pre-cleared**: a per-agent **entry count** and a **turn count** (from
  `event/<name>.json`), and *stop collapsing the dead onto one line* — or at least flag, in the dead
  set, any agent whose journal has one `##` header and no event record. **That single change catches
  `updater-v2`, which is the entire fired trigger**, costs no new verb, no new concept, and is
  precisely *"a derived count column."*
- **Everything else on the page goes to the report artifact** (§2b, zero new verbs, an agent writes
  it on request) until a *second* trigger fires for it.

That is the §8-shaped path, and it is available today.

---

### W1 — **WOUND, severe.** No WATCHLIST trigger fired, and the doc names the rule it is breaking.

**The claim** (§8/cost, `:774`): *"+1 verb (`review`)… **This is the real price, and it is not
nothing** — SIMPLEST fought to five verbs and WATCHLIST §7's trigger is 'any addition that cannot
point to a WATCHLIST entry whose trigger fired.' **My answer to that trigger is §6a**."*

**VERIFIED, `WATCHLIST.md:106`:** *"**TRIGGER:** any addition that cannot point to a WATCHLIST entry
whose trigger fired."* And `:99-108`, the entry's own title: *"Scope creep in the rewrite itself —
the disease that built the 27."* And its fix: *"**An addition with no fired trigger behind it gets
reverted**, and the urge behind it gets written here as a new entry with a falsifier instead."*

**The doc's answer is not responsive.** §6a argues that **PHILOSOPHY §8's** escape clause has fired.
WATCHLIST §7 does not ask about §8. It asks: **which WATCHLIST entry's trigger fired?** I read all
eight entries. **None of them is about top-layer visibility.** Entry 4 (journals rot) is the
closest and its trigger is *parents not reading child journals* — not fired. So the correct
application of WATCHLIST §7 is its own stated remedy: **the addition gets reverted, and the urge
gets written into WATCHLIST as a new entry with a falsifier.**

This is not a technicality. WATCHLIST §7 exists precisely to stop a well-argued local case from
adding a verb — *"every concept in the current system was added by someone with a reason that
sounded local and sane."* **The doc has a reason that sounds local and sane.**

**Minimum fix:** either
- **(preferred)** take the fix WATCHLIST prescribes: **write a new WATCHLIST entry** — *"the top
  layer accumulates invisible defects (stillborn agents, un-reused roles); WATCH: an agent whose
  journal has one `##` header and no event record; TRIGGER: the second one; FIX: a count column on
  `ps`"* — **and ship K2's `ps` column, not a verb**; or
- **(if the operator overrules)** state plainly in §8 that WATCHLIST §7's trigger has **not** fired,
  that the operator is knowingly overriding it, and record the override. **Do not answer a
  WATCHLIST question with a PHILOSOPHY citation** — that is the equivocation the doc is otherwise
  careful to avoid.

---

### W2 — **WOUND.** The page is not opinion-free. Three of its six blocks carry judgment.

**The claim** (§4b, §4c): *"No verdicts, no scores, no recommendations… a fact-sheet has no opinion
to impose."* And the rule it adopts from the graveyard audit: *"The instrument may say what it read.
It may **never** say how the tree scored."* The doc invites me to treat any scoring line as a kill
under its own rule. I find three, and I do not think they are individually fatal — but together they
show the reader/adviser line is thinner than the doc claims.

1. **`RECURRENCE — shapes you have paid for more than once`.** *"Paid for"* is not a file fact. The
   files record no cost — **the doc says so itself** (§6d hole #2: *"THE RECORD HAS NO COST. No
   tokens, no dollars, no turn count."*). The header asserts a cost the instrument has just finished
   proving it cannot see, and it frames recurrence as **waste**. But recurrence here is **doctrine
   working, not failing**: `operator.md:54` (VERIFIED) — *"a future adversarial review spawns fresh
   reviewers by design (independence is the value; warm context is a **LIABILITY** for that shape)."*
   **The 25 REDs are the operator's own policy executing correctly, and the page's header calls them
   a bill.** That is an opinion in a fact's clothing, and it is an opinion the record contradicts.
   → **Fix: rename to `RECURRENCE — role shapes, and how many distinct names have held them`.** Print
   the count. Say nothing about payment.
2. **`STANDING` vs `EPHEMERAL`, `standing ≡ >24h and ≥2 dispatches`.** This threshold is the doc's
   invention. Nothing in the record defines it. It is *defensible* and it is *stated* (§4c) and
   re-derivable, which is what §4c demands — so it clears the doc's own bar. But note what it does:
   `field-tester`'s 16 children and `updater`'s cron loop land in the same bucket as `hardener`'s
   dispatch queue, and any agent at 23h is "ephemeral." → **Fix: print the two raw numbers (lifetime,
   dispatch count) and let the human bucket them. A sort order is a claim.** The doc's own §4c rule
   ("the human must be able to re-derive it in one command") is satisfied more cheaply by not
   bucketing at all.
3. **The `⚠` glyph.** On `updater-v2` it is warranted (that one is a real defect). On `BLOCKED` it
   was wrong (K1). A warning glyph **is** a judgment — it says *this one matters more than the
   others* — and the doc's claim that it is *"a description of a file, not a judgment of the human"*
   is not quite honest. → **Fix: keep it only where the predicate is purely mechanical and
   file-witnessed (the stillborn test qualifies; blockage does not).**

**None of these individually kills the reader/adviser distinction** — the doc is right that a page
with no score, no ranking and no "you should" is categorically different from the engine
`DECISIONS.md` killed, and F3's grep (`score|health|rating|%|should|recommend`) is a real tripwire.
But **the distinction is maintained by discipline, not by structure**, and the doc claims it is
structural (*"advisory-only, honored **structurally**"*). K1 is the proof that discipline slipped.

---

### W3 — **WOUND, half-fatal to the doc's strongest evidence.** The decay claim is half-verified.

**The claim** (§3.5): *"17.4h → 3s, still collapsed today (#81/#82 in 9s/3s)"* and *"**Merging is an
act only the human performs**… this is **the one channel in the entire system that measures the
human's own attention and cannot lie**."*

**Half 1 — the numbers: VERIFIED.** I re-ran `gh pr list --state merged` myself. The decay is real
and it is worse than the doc's table shows (it omits #74-#78's neighbours, which are also seconds):

```
#65 62733s(17.4h)  #66 62202s  #67 57918s  #68 57653s   <- the gate working
#72 10041s(2.8h)   #73 10021s                            <- thinning
#74 14s  #75 3s  #76 3s  #77 3s  #78 4s                  <- collapsed
#81 9s   #82 3s                                          <- TODAY
```
Every PR: `merged_by=vadrsa`. The operator's own ledger names it (`operator.md:90`, VERIFIED):
*"Uncomfortable mirror: my gate collapsed 16h→2.8h→14s under pre-auth, tier labels intact, attention
thinned."* **This is the doc's best evidence and it survives.**

**Half 2 — "only the human performs it": NOT ESTABLISHED, and the doc leans on it.** I attacked this
as briefed. `mergedBy=vadrsa` proves the *account*, not the *hands*. The record shows the operator
**pre-authorizing agents to merge in their name** — `operator.md:30`, VERIFIED: *"**User merged
#65-#70 (via my gh calls, user-authorized)**"* — that is an **agent** running `gh` under the
operator's credential. And `operator.md:90`'s own diagnosis is *"collapsed **under pre-auth**"* —
i.e. **the operator's own explanation for the 3-second merges is that authority was delegated**, not
that a human read the diff in three seconds. A 3s merge under standing pre-authorization is not
*"thinned human attention"* in the sense the doc needs; it is **an agent executing a grant** — which
is exactly what `DECISIONS.md`'s standing-authorization ledger was designed to make legitimate.

**This does not destroy the decay finding** — the operator themselves calls it a collapse and a
mirror, and the *authorization* thinning is itself the phenomenon. But it **destroys the doc's
stated warrant for the block**: the merge channel is **not** *"the one channel that measures the
human's own attention and cannot lie."* It measures **the human's account**, which agents drive
under grant. That is the same conflation the doc congratulates itself for avoiding in §3.6's
`delivered/`-ctime trap ("the instrument must never present session latency as human latency") —
**and it walked into it again one section earlier.** F4 pre-registers the trap for the mailbox block
and does not cover the merge block.

**Minimum fix:** the `YOUR REVIEW LATENCY` block must **not** be captioned *"only you merge."* Label
it for what it is: *open→merge latency on your account, including agent merges under standing
pre-authorization* — and **extend F4 to cover it**. If the operator wants a true human-attention
channel, it does not currently exist in the files, and the doc should say so under §6d as hole #6.

---

### W4 — **WOUND, minor but structural.** The duplicate-work null is true at the sibling level and blind at the layer that matters.

The doc reports *"Duplicate work: NULL. 0 pairs of 25."* I re-checked. It holds **for the predicate
it uses** (task-text similarity between agents). But the predicate is blind to the real duplication,
which is **serial**: the top layer ran `decision-scout` → `decision-wiring` → `proxy-scout` →
`pipeline-scout` → `hook-scout` → `patterns-contractor` — **five to six top-level agents, ~15 hours,
one question** (the decision-engine wiring), each closed on harvest and re-spawned under a fresh name
after the operator re-scoped. `pipeline-scout`'s own brief says *"third iteration of the
decision-engine wiring"*; `hook-scout`'s says *"v4."* Their task texts are **not** similar — they
explicitly inherit and diverge — so a text-similarity collector **structurally cannot see it**.

This is a **false negative, not a true zero**, and it matters because the doc's whole design rests on
the shape of the null/fire table (*"the three 'is it broken' collectors return null"*). One of the
three nulls is an artifact of the collector, not a property of the tree. → **Fix:** either measure
serial re-issue (successor chains: agent B's brief names agent A's deliverable) or **label the null
honestly as "no duplicate *sibling* work; serial re-issue not measured."** The doc's §6d holes
section is the right home for it.

---

### W5 — **WOUND, cheap fix.** The sibling correction is TRUE, and should be stated more strongly.

The doc corrects `OPERATOR-STRUCTURE.md`: its `deep` anecdote (an unregistered agent mailing the
human six times) *"is not in this tree."* **VERIFIED — I re-ran it independently:** 61 messages to
`queue/operator/delivered/`, **22 senders, all registered in `agents/*.json`, all depth-1, zero
unregistered.** There is no agent named `deep` in this tree at all. **The correction is correct**,
and under PHILOSOPHY §10 it should be delivered to the sibling as a correction to *its* record, not
buried in a footnote of a companion doc. → **Fix: `swarm send operator-structure-scout` with the
measurement.** (Composition otherwise is clean: `OPERATOR-STRUCTURE.md` defines the layer, this
reviews it; no collision. And I confirm it does **not** touch in-swarm restructure doctrine —
§6e(b) explicitly flags the falsifier-orphaning finding as out of scope and refuses to act on it,
which is correct behavior.)

---

### N1 — **NOT A FINDING, recorded because the brief asked.** Could the report artifact do the whole job?

The brief told me to press this: *"an agent that reads the same files on request is always current
too — if the report artifact is just as good, the verb is unjustified scope creep."*

**I pressed it, and the doc's rejection is thinner than it should be but the conclusion is right for
the wrong reason.** The doc says the report *"goes stale the moment it's written."* That is weak — as
the brief notes, an agent invoked on demand re-reads the files and is as current as a verb.

**The real difference is cost and reliability, and the doc has the evidence but doesn't use it
here:** an agent costs a pane, a spawn, tokens and a turn; a verb costs a process. And §2c's measured
finding — *the shipped `swarm` skill **never loaded**, 2 of 2, on goal-shaped prompts; it fired only
on the literal phrase* — cuts against **anything that depends on a model deciding to invoke it**.

**But that argument, followed honestly, points at K2's fix, not at a new verb:** if what fired is
`updater-v2` (one predicate), the right artifact is **a count column on `ps`** — a verb the human
already runs, with no invocation problem at all. **The report artifact and the new verb are both
answers to a question that a `ps` column answers more cheaply.** I therefore do not recommend the
report artifact **or** the verb. I recommend the column.

---

## What I would tell the operator, in one paragraph

The doc's diagnosis is right and its instinct is right: **your top layer is not sick, and the
suggestions were the wrong half.** The three "is it broken" collectors really do return null — I
re-ran all three and they hold. And it found a real defect: **`updater-v2`, a standing role you
briefed on 07-10, never took a single turn and nobody noticed for two days**, because `ps` shows no
per-agent turn count and buries the dead on one line. That is a genuine "failing because you cannot
see it," and `SPAN.md` pre-registered exactly that trigger and named exactly the remedy: **a derived
count column on `ps`.** Ship that. It costs no new verb, no new concept, breaks no WATCHLIST rule,
and it catches the one thing that actually fired. **Do not ship the six-block page**, because the
page's showcase block is false — `hardener` is not blocked on a corpse; `field-tester` was alive and
working all day and was closed on harvest — and a fact-sheet that gets a fact wrong is more dangerous
than an adviser, because it has borrowed the authority of a file.

---

## Sources — everything re-verified at source, nothing taken from the doc or its audits

- `docs/PHILOSOPHY.md` — read in full. §8 at 245-266 (the four bullets and the corollary), §9, §2, §3, §5, §10.
- `docs/audit/org-review-phil8-2026-07-12.md` — the prosecution, read in full. Its §8 reading is defeated by SPAN.md:236-239, which it quotes up to and stops short of.
- `docs/design/SPAN.md:220-255` — read at source. The overseer kill (:231-234) **and** the deferred-`ps`-metrics clearance (:236-239). Both verbatim.
- `docs/design/PROXY-WIRING.md:285-330` — read at source. The standing-observer demotion; its objections are all to the standing form.
- `docs/design/WATCHLIST.md` — all 8 entries read. §7's trigger verbatim at :106. **No entry's trigger has fired for this.**
- `docs/design/SIMPLEST.md` — the five verbs, the deleted-concepts table, the nag autopsy at :177.
- `skill/SKILL.md:40-60` — the span doctrine (:44-49) and the operator-seat/hand contract, verbatim.
- `.swarm/journal/operator.md` — read in full (195 lines). :23 (overseer rejected), :30 (**"user-authorized" agent merges** — W3), :45, :54 (**fresh reds are doctrine** — W2), :90, :183, :193.
- **Re-run myself:** parent-chain depth walk over 61 `queue/operator/delivered/*.json` × 135 `agents/*.json` → **61/61 depth-1, 0 unregistered.** Peak-concurrent top-layer computation → **5.** `gh pr list --state merged --json createdAt,mergedAt,mergedBy` over 40 PRs → the decay table, all `merged_by=vadrsa`.
- **The K1 kill:** `stat` on `.swarm/journal/{hardener,field-tester}.md` (05:52 vs **20:02**), and `field-tester`'s three operator mails at 18:41 / 19:41 / 20:02, all *after* the `hardener` line the doc reads as blockage.
- `.swarm/agents/updater-v2.json` + `.swarm/journal/updater-v2.md` — the stillborn agent, confirmed: spawn stub only, zero work entries, warm `updater` still running two days later.
