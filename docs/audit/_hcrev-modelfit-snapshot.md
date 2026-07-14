# MODEL-FIT — how a parent picks a child's model

> SUPERSEDED by docs/design/MODEL-FIT.md, partially (the doc has since drifted 33 lines past §5); kept for the record (the frozen citation substrate _hcrev-fit.md's 9 line-cites resolve against; holds the pre-overrule ruling text — 87 lines differ from current MODEL-FIT.md).

**Author:** `model-fit`, reporting to the operator. **Status:** DESIGN — proposed
doctrine + wiring. **Written at** `main@aa6063d`, 2026-07-13.

**The gap this closes.** `swarm spawn <name> "<task>" --model M` has existed since
the CLI did (`bin/swarm:851`). In this swarm's whole recorded life, **142 of 143
agents took the inherited default; exactly one was ever pinned.** Scouts,
red-teamers, hardeners, census-counters — every one of them on Opus 4.8. That is
not a decision anyone made. It is a decision nobody made, 143 times.

The flag is not the fix. Nothing in `WORLD.md`, `skill/SKILL.md`,
`references/COORDINATING.md`, or `swarm`'s help ever tells a parent that choosing
is *a thing a parent does* — `--model` appears only in an arg-parser and one usage
line. The record here is blunt about what that means: **agents do not invent
structural moves that are not in their frame, and reliably execute the ones that
are** (`references/COORDINATING.md:28-31`). Model choice is not in the frame. This
document puts it there, and §5 wires it in.

---

## 1. The bottom line (the rule, in one screen)

**At every spawn, the parent names a model and says why in one clause.** Not a
classifier; not a policy engine. A parent choosing is the point.

The axis is **not** "how hard is the thinking?" It is:

> **Can I cheaply tell that this child was wrong?**

Everything below follows from that question, because the cost that actually bites
is not tokens — it is a **confidently wrong child that the parent believes**. Model
spend is bounded and known at spawn. Confident-wrong work is unbounded: it is
adopted into a design doc, cited by a sibling, shipped in a doctrine edit, and the
bill arrives later, in work built on it.

**The three-question ladder.** Ask them in order; stop at the first "yes".

| # | Ask | If yes → |
|---|---|---|
| **1** | Does this child **hold a seat** — spawn children, judge them, keep a journal across a restore, decide when it is done? | **Opus 4.8** (`claude-opus-4-8`). Seat-holding is the *measured* failure mode of weaker models, not domain skill. §3. |
| **2** | Is this child's output **judgment I will adopt** — a design, a review verdict, a red-team's "this is safe", an edit to `bin/swarm` or doctrine? | **Opus 4.8**, unless I have a cheap independent check. §4. |
| **3** | Is the answer **mechanically checkable** — a count, a list of paths, a grep sweep, a transcription — such that I can verify it in seconds without redoing the reasoning? | **Sonnet 5** (`claude-sonnet-5`), or **Haiku 4.5** (`claude-haiku-4-5-20251001`) if it is *pure* retrieval with a verifiable answer. §4. |

Nothing matched? **Opus.** The ladder's fall-through is the strong model, on
purpose — see §6.

**One misreading to head off, because it is the natural one.** *"Read-only work is cheap
work"* does **not** follow, and the field record splits precisely on this: it **supports**
cheap models on mechanically-checkable **work** (reading, grepping, summarizing, exact-format
output, CLI syntax — all good to excellent) and **undermines** cheap models in read-only
**seats**. A scout reads and does not write code, but a scout must *report*, *journal*, and be
*recoverable* — and reporting, journaling, and recovering are exactly what broke (§2).

> **A read-only scout is not a mechanical seat. It is a seat.**

So `scout → cheap` does not follow, and the ladder does not produce it: a scout's output is
judgment you will adopt, which is **Rung 2 → Opus**. The tier is not a property of how much
*typing* the child does. It is a property of **what it costs you when the child is wrong, and
whether the child must hold a seat to deliver at all.**

**And say the coverage limit out loud, once, before the mapping is used.** *No Claude tier has
ever been evaluated in a swarm seat in this repo.* The fleet eval measured DeepSeek and GLM
against a native-Claude anchor; the Haiku cell was designed and **never keyed**. Everything
below about Haiku and Sonnet is an **extrapolation of a behavioral axis** across a vendor and
a harness boundary — argued in §2, falsifiable in §7. It is the honest basis available today,
and it is strictly better than 143 spawns of nobody thinking; it is *not* a measurement, and
nine thousand lines of eval must not be allowed to imply a coverage they do not have.

**Say it at the spawn.** The doctrine is one line in the parent's journal:
`spawned <name> on <model> — <the clause>`. That is the whole enforcement
mechanism, and it is enough: it makes the choice inspectable, which is how
everything else in this repo is judged.

---

## 2. What the field actually says (this is not reasoned from priors)

This repo has **already run the experiment.** `docs/design/FLEET-EVAL.md` (v2) and
`docs/design/FLEET-EVAL-V3.md` (v3, clean rig) put non-Claude models in real swarm
seats and scored them from artifacts across four dimensions — **D1 duties, D2
delegation, D3 tool/CLI, D4 long-horizon** — with an adversarial review that flipped
verdicts (`FLEET-EVAL-RED.md`, `FLEET-EVAL-V3-RED.md`). Two of the models were
substantially weaker than the Claude anchor. **The failures did not land where a
naive "weaker model = worse reasoning" prior would put them.**

The v3 bottom line (`FLEET-EVAL-V3.md:23-27`):

| Model | D1 duties | D2 delegation | D3 tool/CLI | D4 long-horizon |
|---|---|---|---|---|
| deepseek-chat | 5/5 PASS | 8/10 FAIL | 11/17 FAIL | 3/6 FAIL |
| GLM-4.7 | 5/5 PASS | 7/10 FAIL | 14/17 PARTIAL | 3/6 FAIL |
| claude-native (anchor) | 5/5 PASS | 10/10 PASS | 17/17 PASS | 6/6 PASS |

Read the *shape*, not the scores. The weaker models were **not stupid**. GLM was
graded an **"excellent tool-user"** whose swarm commands were "well-formed all
battery long" (`FLEET-EVAL-V3.md:96-98`); it ran four real child audits and
**verified each child's report against the child's actual output file**
(`:90-94`). That is not a model that cannot think. What they failed was **the
seat**:

- **They do not use the verb.** 4/7 report-to-parent drops for deepseek — it
  *narrates* the report as turn text instead of sending it. The finding is quoted
  in the record as: **"it knows who its parent is and does not use the verb"**
  (`FLEET-EVAL-V3.md:76-78`).
- **They do not journal.** Neither model wrote the plan to the journal (D4 hard-check
  FAIL for both). GLM put its plan in the deliverable, then on restart **went looking
  for the journal it had never written** (`FLEET-EVAL-V3.md:100-103`).
- **They substitute a door for the contract.** deepseek tried to journal into an MCP
  memory server — *the call errored and it never noticed, so it journaled nowhere*;
  GLM reached for `bridgemind_send_agent_message` (404) and a `nc -U` socket rather
  than `swarm send`. **The Claude control had the same doors open and took them 0
  times in 7 probes** (`FLEET-EVAL-V3.md:117-125`).
- **They do not time-box, and they do not watchdog.** deepseek hit a blocked
  dependency and **spent 11 minutes debugging the harness**, abandoning its brief
  (`FLEET-EVAL-V3.md:82-87`). GLM's harvest loop is blind `sleep`-escalation with no
  watchdog: **"dead children would hang it again"** (`:95-96`).

**And the protocol failures were *silent*, which is what makes them expensive.** The
domain work was genuine — three cells independently converged on the same real repo
defects, and the record's own verdict is *"the child did not fabricate."* What broke
broke invisibly:

- **GLM wrote a journal section headed `**Report to parent v3-run-glm:**`, with correct
  content — and never ran `swarm send`.** A parent reading that journal believes it was
  reported to.
- **deepseek's journal write errored; it wrote *"Done. Plan is in my reasoning above"*
  and never noticed.**
- Report-to-parent landed **3/7 (deepseek), 3/7 (GLM), 7/7 (Claude)**.

**The load-bearing generalization.** These are *protocol* and *self-governance* failures,
**orthogonal to domain difficulty**. A model can verify a child's output file correctly and
still be unable to hold a seat. What degrades first as you go down a tier is **not the
quality of the thinking — it is the discipline that makes an agent's thinking recoverable,
reportable, and self-terminating.**

That sharpens the ladder's question by one word. Not merely *"can I cheaply tell this child
was **wrong**?"* but:

> **"Can I cheaply tell this child *did what it says it did*?"**

Because the cheapest thing for any model to produce is a *claim* that the work happened —
and the weaker the model, the likelier that claim is the only thing that happened. **This is
also why the artifact, not the report, is the witness — at every tier.** The anchor is not
immune: four *Claude* probes sent their reports correctly and then falsely journaled that
they had failed. Self-narration is unreliable everywhere; it is merely *more* unreliable
cheap.

**The honest caveat, and why the rule still stands.** These were *DeepSeek and GLM*,
not Sonnet and Haiku. Sonnet 5 and Haiku 4.5 are Claude models on the Claude harness,
and this eval's own headline caveat is that a Claude-vs-Chinese gap **confounds model
with harness** (`FLEET-EVAL-V3.md:41-44`, §2 "REMAINS"). **I am not claiming Haiku
behaves like GLM.** I am taking the *axis* the eval discovered — that seat-holding
fails before reasoning does — and I am declining to assume the axis vanishes inside
the Claude family. That is a directional read, and I mark it as one. §7 says what
would falsify it and how to find out cheaply.

**One confound I checked rather than assumed** (because it would have voided the
citation above). A sibling probe found that **a child blocked on an interactive
permission dialog is observationally identical to a weak model**: `ps` says live,
the journal is empty, no artifact, stale last-words — every observable is also what
a model out of its depth produces. If the eval had scored its failures from *absence
of file*, the deepseek/GLM failures I lean on could be misread blocks.

**They are not, and the reason is structural rather than evidentiary.** The
non-Claude cells were run by `run-cell.sh` as **`opencode run --auto`**
(`FLEET-EVAL.md:108`). `--auto` is auto-approve: **there is no interactive dialog
mechanism in that harness at all.** A block of the kind that hit the Haiku probe
cannot occur there, so it cannot be masquerading as a deepseek or GLM failure. The
citation survives on that fact alone.

*(An earlier draft of this paragraph defended the point by citing `FLEET-EVAL-V3.md:64-65`,
`:136`, and `:244` as showing "the eval scored from transcripts and session logs." An
adversarial reviewer read them and I re-read them: they do not show that. `:64-65` is a
single D2 sub-check on deepseek's report-delivery; `:136` and `:244` are the MCP-call
control on the **Claude anchor**. I had read three cites generously in my own favor. They
are removed. Recorded rather than silently swapped, because the failure mode is the one
this document is about.)*

**And the law behind the confound is real — the eval hit a cousin of it, on the very row
I was defending.** Its pane-less runner read as `dead` in `swarm ps`, so **"four native
probes sent correct reports and then *despaired* incorrectly — scored from files"**
(`FLEET-EVAL-V3.md:159-161`). Note who that happened to: **the native Claude anchor**, not
the weak models. Nobody is immune, and the strong tier least of all deserves the
assumption. Two witnesses, two rigs, one law:

> **An agent's observables lie. "No artifact" is not evidence of a bad model — it is
> evidence of nothing until you look at the pane.**

That belongs in this document rather than a footnote, because **the entire tier rule
depends on a parent being able to tell "this child was wrong" from "this child was
blocked."** A parent who cannot make that distinction will conclude the cheap tier
failed, and revert to Opus-for-everything having learned nothing. §7 carries it as a
standing caveat on judging a cheap child.

---

## 3. Rung 1 — the seat: any child that parents, gets Opus

**Rule: if the child will spawn, judge, harvest, close, or survive a restore, it runs
Opus 4.8.** No exceptions on cost grounds.

A coordinator's real work is not the domain — it is the swarm contract itself:
weighing whether to delegate, briefing children well enough to judge them, keeping a
journal that a *restored* session can reload, harvesting before closing, knowing when
it is done and reporting up. Every one of those is exactly what the eval watched
weaker models drop, **while their domain reasoning stayed fine.**

The blast radius makes this the cheapest possible place to be strict. A bad leaf
produces one bad artifact, and the parent catches it. **A bad seat produces a bad
tree**: it mis-briefs four children, and now you are paying full price for four
agents to do work that was scoped wrong — and paying again to find out. A parent who
does not journal is a parent you cannot recover, and this repo's own restore path
(`swarm restore`, the journal-as-continuity contract) is *load-bearing*, not a nicety.
Downgrading a seat to save tokens spends children to save on the parent. That trade
is always backwards.

**This is the rung that keeps the whole rule safe.** Everything below it is a leaf,
which means everything below it is *caught by a parent who is strong*.

---

## 4. Rungs 2 and 3 — the leaves: sort by checkability, not by difficulty

For a leaf, the parent is the safety net. So the question is only ever: **when this
child hands me its artifact, what does it cost me to know if it is wrong?**

### Rung 2 — adopted judgment → **Opus 4.8**

The artifact *is* an argument, and I will build on it. Scouts, design-drafters,
red-teamers, reviewers, hardeners editing `bin/swarm` or doctrine.

Verifying a judgment costs **the same work as making it** — that is what makes it a
judgment. If a reviewer tells me "this design is sound" or a red-teamer tells me "I
found no hole", the *only* way to check is to redo the review. So a cheap model here
does not save me a review; it buys me a **second review I now have to do myself**,
plus the risk that I don't bother and just believe it.

**The red-teamer is the sharpest case, and it is the one people get wrong.** A
red-teamer's most valuable output is a *negative*: "I attacked this and it held."
That is precisely the output a weaker model produces most fluently and least
reliably — it is the cheapest sentence in the language to write and the most
expensive to falsify. A red-teamer that misses the hole doesn't *look* like a
failure. It looks like good news. **Never cheap out on an agent whose job is to tell
you that you are wrong** — you are, by construction, not in a position to grade it.

Same logic for a hardener touching `bin/swarm`: the tests are a real check, but tests
catch what they cover, and the failure that matters (a subtly wrong contract, a
plausible-but-wrong edit to the spawn path) is the failure tests were not written for.

### Rung 3 — mechanically checkable → **Sonnet 5**, and **Haiku 4.5** at the floor

The artifact is a *fact* I can spot-check without redoing the work:

- **Sonnet 5** (`claude-sonnet-5`) — the honest default for real leaf work with a
  checkable answer: a census across the tree, an inventory of every call site, a
  "which files mention X and what do they say" sweep, a mechanical refactor with a
  green test suite, a transcription or reformat. Sonnet is a strong model; this is
  not a downgrade to a toy. It is declining to pay Opus rates for work whose output I
  can verify with a `grep -c` and my own eyes.

**The asymmetry that "verify it in seconds" hides, and it is the sharpest limit on this
rung.** Checkable does not mean *equally* checkable in both directions:

| error | how you catch it |
|---|---|
| **wrong entry** — a listed call-site that isn't real | trivial. Open it. It isn't there. Spot-checking finds these immediately. |
| **omission** — a real call-site the child never listed | **spot-checking cannot see it.** You inspect the 40 items it *did* return; all 40 check out; the 3 it missed leave no trace in the artifact. |

**Absence is invisible to inspection.** This is the same law as the observables-lie caveat
in §7 — *"no artifact" is evidence of nothing* — applied to the child's output instead of
its liveness, and a document that states the law about liveness and then forgets it about
censuses has not learned its own lesson.

So the rung carries a condition: **when a count is load-bearing on its *completeness* — a
blast radius, a "we found every call site", a "these are all the affected files" — a single
cheap census is not sufficient evidence.** Either count it twice by different means (a
second agent, or a `grep -c` the parent runs itself), or **publish it as a floor, not a
total** ("at least 9 call-sites"). Verification in seconds is real for *what is there*.
There is no cheap check for *what is missing* — and a cheap model's most likely error is
precisely to return less than there was.
- **Haiku 4.5** (`claude-haiku-4-5-20251001`) — the floor, and it earns its place on
  a **narrow** band: *pure retrieval with a verifiable answer.* Count the agents.
  List the files matching this pattern. Extract every `--model` call site. Fetch and
  quote. The test is brutal and simple: **if I would accept the answer without
  reading the reasoning, Haiku can produce it. If I would want to read the reasoning,
  it is not a Haiku task.**

**Where the ladder cuts against the strong model.** Rung 3 is not purely a cost play,
and this is worth saying plainly: on a genuinely mechanical brief, a very strong model
is *not reliably better* — it is reliably **more**. It re-scopes the task, notices
adjacent problems, and hands back an essay where the parent asked for a number. That
is a real failure mode of putting Opus on a census: not that the count is wrong, but
that it arrives buried in an argument the parent did not ask for and now must read.
(Directional, from watching this tree; I have not benchmarked it. §7.)

### The over-delegation fear — asked, measured, NOT supported

The sharpest objection to Rung 3 did not come from a reviewer. It came from the human:

> *"If a parent puts a weak model on a child, does that child **over-delegate** — spawn
> its own children to escape a task it can't hold — and balloon the tree and the cost
> past the Opus it replaced?"*

It is a good fear, and it is aimed at the right place: nothing in Rung 3 stops a Haiku
scout from spawning. If it were true, the tier would have to be **coupled to the spawn
right** — cheap models restricted to children that structurally cannot delegate.

**It was measured, not argued.** A sibling probe (`weak-model-deleg`) ran three arms —
one Opus, two Haiku — on a byte-identical task built to *tempt* delegation: audit ~2000
lines across four docs, verdict every promise, rank by damage. Three docs are three
obvious parallel parts, but the value lives in the cross-doc synthesis, which cannot be
pushed down without losing it. The over-delegation threshold was **declared before the
run** so it could not be moved afterward.

**Result, MEASURED from the raw `.swarm/agents/` records rather than self-report:
descendants across all three arms, ever: ZERO.** Haiku spawned nothing. It read all four
documents and correctly enumerated all fourteen `WORLD.md` promises (the probe checked
the list against the source). Its failure mode is **the opposite of the fear**: it
*under*-delegates and grinds.

**So Rung 3 stands, and it stands without a new mechanism.** I was prepared to grow one —
couple the tier to the spawn right, restrict cheap models to structural leaves — and the
evidence asked for none. Declining to build the mechanism nobody's evidence calls for is
the point; a spawn-right restriction would have been a permanent constraint bought to
solve a problem that did not reproduce.

**The honest limits, which I will not bury — the probe asked me to encode its uncertainty
rather than my convenience, and it is right to have asked.** Two defects, both disclosed by
the probe itself, which went to prove its own convenient explanation and disproved it:

1. **The arms differed in two variables, not one.** Model *and* permission posture: a
   byte-identical `mkdir` was auto-approved for the Opus arm and **blocked** for the Haiku
   arm. Root cause — **`swarm spawn` writes its settings file with hooks only and no
   `permissions` block**, so a child's permission posture is inherited from ambient context
   rather than set by swarm. It is not a clean matched pair. **Every latency and cost
   comparison between those arms is dead, and none is cited here** — including the one that
   would have most flattered this document, the human's "does it balloon past the Opus it
   replaced?" cost number. I do not have it.
2. **Both Haiku arms blocked before the synthesis step** — exactly where the temptation to
   delegate would peak (documents read; now cross-reference and rank).

**What survives, and why — the argument is temporal.** A blocked agent obviously cannot
spawn. But Haiku was blocked *later*, at `mkdir` and at a journal write, **after** it had
read all four documents and chosen its approach. **The spawn-or-not decision came first, and
it chose not to spawn — twice, unprompted.** That is an observation about the model, not the
rig.

**The acquittal is narrow, and here is the other thing the same probe saw.** Across 16+
minutes alive, the Haiku arms wrote **nothing** to their journals and sent **nothing** —
zero `swarm send`, zero journal writes — while the Opus arm journaled, reported with a
substantive body, and left a real artifact on disk. That is confounded (both Haiku arms were
blocked at the very call that would have written the journal, so it is not a clean
protocol-drop observation) — but it is **the exact shape §2 says weak models fail in**, and
it sits here, next to the acquittal, rather than being filed somewhere quieter. **Haiku is
acquitted of over-delegating. It is not yet acquitted of holding a seat** — and Rung 3 does
not ask it to.

So the claim this document rests on is exactly this and no more: **Haiku shows no spawn
reflex on receiving a big, obviously-splittable task.** Its behavior *at the judgment wall*
is **untested**. This is not a clean acquittal, and Rung 3 does not lean on one — it leans on
the ladder's own logic (a leaf's mistake lands somewhere safe: a strong parent reading the
artifact). **If a Haiku child is ever observed spawning at the judgment wall, Rung 3 reopens**
(§7).

### The fear arrives by another road: leaves do not stay leaves

The probe tested *"does a weak model escape a hard task by spawning?"* and found no. But a
census of this tree found something the probe was not looking for, and it is the more
dangerous version of the same fear:

> **18 of 115 agents — 16% — carry a coordinator role they were never briefed for. Exactly
> one was ever asked to coordinate.** Leaves grow into seats *on their own*, regardless of
> model.

This is a genuine wound to Rung 3, and not one the over-delegation probe can heal, because it
is not about weakness at all: it is what agents in this swarm *do*. A cheap child spawned to
sweep a directory, which then decides the job needs three helpers and starts briefing and
judging them, **has become a seat** — and §3 says seats get Opus for reasons that do not care
how the agent got there.

**The answer is prior art this document should have cited from the start.** `FLEET.md:88`
already wrote it, for a different purpose:

> **"A leaf never spawns."**

That is the missing coupling. **The tier is not really a property of the model — it is a
property of the seat**, and a parent who puts a cheap model on a child is making a second,
implicit claim: *this child will not become a parent.* Today nothing holds that claim: `swarm
spawn` gives every child the full verb set, so a Haiku leaf can spawn an Opus subtree at 3am
and nobody chose that either.

So the honest statement of Rung 3 is **conditional**, and the doctrine says so: *cheap models
go to children that will not spawn.* Making it *structural* — a spawned child that cannot
itself spawn — is the natural mechanism, it is already named in this repo, and it is **not
built here**: it is a change to the spawn path with its own blast radius, and this document's
job is to establish that a parent must choose, not to ship a permission system. It is the
first thing to build if Rung 3 is taken seriously. **Until it exists, "cheap → leaf" is a
promise the parent makes and must actually keep** — which is precisely the kind of unenforced,
inspectable promise this repo runs on everywhere else.

### Fable 5

`claude-fable-5` has no seat in this rule. It is available at the flag; nothing in this
repo's record establishes what it is *for* in a swarm seat, and I decline to invent a
mapping to look complete. **A rule that assigns a model a job it has not been watched
doing is exactly the confident-wrong artifact this whole document exists to prevent.**
If someone puts it in a seat and writes down what happened, this section gets rewritten
from evidence.

---

## 5. Should the tool *force* the choice? (the mandate ruling)

The human proposed a mechanism: **make `swarm spawn` take a mandatory model-choice
reason, recorded in the agent record** — converting blind inheritance into a forced,
auditable decision. They asked for it to be challenged, not rubber-stamped. It was
(`docs/design/MODEL-FIT-MANDATE.md`), and **the challenge refuted the objection I
went in holding.**

**My prior, which was wrong.** I expected compliance theater: a forced free-text
field is gameable, agents will type *"fits the task"*, and a string always satisfiable
by a null string forces nothing. **This repo has already run that experiment.**
Doctrine already compels one free-text justification from every agent — *a
reconciliation entry names its falsifier* — the same shape, unenforced, across 158
agents. A pre-registered audit with four independent readers
(`docs/audit/org-review-falsifier-2026-07-12.md`) classified all 135 compelled
falsifier statements:

| | count |
|---|---|
| observable, checkable | 114 |
| observable elsewhere | 21 |
| **unfalsifiable mush — the predicted theater** | **0 of 135** (`:78`) |

And on the forward hunt: **17 documented cases where the compelled field *changed what
the agent did*** (`:84-87`), against **0** where it fired and was ignored. One agent
killed its own preferred design because a field it was forced to fill made it look.
**Compelled articulation works here, and it is measured, not argued.** (An independent
grep found ~3 arguably-vacuous entries against the audit's 0; even on the pessimistic
reading the theater rate is 2–3%, not the ~90% my prior assumed. The direction does not
move.)

**The ruling: `--model` stays optional, but silence stops being free.**

- **`swarm spawn` asks.** The parent may still inherit — they may not do it *silently*.
  An explicit `inherit` is a legitimate, evidence-respecting answer; a *missing* one is
  a skipped step.
- **The reason must be scoped to the ladder's question** — *"can I cheaply tell that
  this child was wrong?"* — **not to "why is this model good."** This distinction is
  load-bearing, and it comes from the one objection the review could not defeat:

  > *A mandated reason forces a parent to justify a choice the repo cannot yet inform —
  > and a recorded reason **launders a guess into a decision**.*

  That is the sharpest thing said in this workstream. A parent asked *"why is Haiku
  right for this?"* must assert knowledge about a model's competence **that nobody in
  this repo has** — and will assert it fluently, which is precisely the confident-wrong
  artifact §6 exists to prevent. A parent asked *"can you cheaply tell if this child is
  wrong?"* is asked about **their own verification capacity, and they always know the
  answer**: *"I will read every line of this doc anyway"* is knowable at spawn without a
  single benchmark. **The question the ladder asks is answerable honestly today. The
  question "which model is smarter" is not.** Scope the reason to the former, or the
  mandate manufactures the very fabrication it was built to prevent.
- **Give the field a reader, in the same change, or do not ship it.** The record
  `.swarm/agents/<name>.json` **already writes `model`** (`bin/swarm:916-919`) — the data
  the proposal wants recorded *is already recorded*, and it changed nobody's behavior for
  143 spawns, because **`swarm ps` — "the one view" — does not render it**
  (`bin/swarm:539-548`). A reason written to a JSON file no view shows is evidence
  accumulating in a drawer. Putting the model on the `ps` line is one line, and it turns
  the view every parent already reads into a standing audit of every model decision in
  the tree. **A mandate without a reader is write-only, and should be opposed.**

**What this repo ships now, and what it does not.** The doctrine and the help text (§5b)
are the *whole* of this change: they put the question in the frame, which is the thing
that was missing. The CLI mandate is **specified and recommended here, and deliberately
left unimplemented in this PR** — it is a breaking change to `swarm spawn` (blast radius
measured by patching a scratch copy of `bin/swarm` and running the suite: **at least** ~9
test call-sites and 12 doc files — *a floor, not a total, per the omission caveat in §4*)
and it deserves its own reviewed change, not a rider on a doctrine PR. The ordering is also the safer experiment: doctrine is
reversible by editing a paragraph, and if parents start choosing *because the frame now
contains the choice*, the mandate may prove unnecessary. If they do not, the mandate is
sitting there costed, argued, and ready.

## 5b. The default: do not change the fallback — and stop calling it "inherit"

**First, a correction, because this document was wrong about its own central noun and
the error is instructive.**

There is **no inheritance.** `swarm spawn` does not read the parent's model and does
not pass one down. When `--model` is absent, the launcher invokes `claude` with **no
`--model` flag at all** (`bin/swarm:834-835`) — so the child gets whatever the `claude`
binary resolves as its **ambient default**, which is nobody's decision, and is *not*
the parent's model. A child of a pinned-Opus parent does **not** get Opus.

An earlier draft of this section argued that *"inheritance is the one default that is
never silently wrong — whatever the parent is running was trusted with this subtree, so
inheriting it is the conservative failure."* **That argument is void: it rested on a
mechanism that does not exist.** It was caught by a child that read the source instead
of the prose. It is exactly the confidently-wrong artifact §6 is about, committed *in*
the document about it, by its author — and it is left on the record rather than quietly
deleted, because a design that claims a parent cannot self-verify judgment should not
pretend it verified its own.

**The ruling survives the correction: the fallback does not change.** An unspecified
spawn keeps doing what it does today. What changes is that **unspecified stops being
invisible.**

The tempting move is to flip the fallback to Sonnet — the field data screams waste, and
a default is the one lever that fixes 142 spawns without anyone reading a doc. **I am
rejecting that, for two reasons that survive the correction above.**

1. **It quietly downgrades the seat.** Coordinators are spawned by the same verb as
   census-counters. A Sonnet fallback puts every future coordinator — the thing §3 just
   argued is the *most* dangerous place to economize — on a weaker model **by accident**,
   which is the exact failure this document was written to end. Trading "nobody chose, and
   got Opus" for "nobody chose, and got Sonnet" does not add a decision; it moves which
   decision nobody makes, and moves it in the more dangerous direction. **The bug was
   never *which* model got picked by default. The bug is that nobody was thinking.**
2. **A default is a way of not choosing, and a parent choosing is the point.** Any
   mechanism that picks *for* the parent — a fallback tuned to be "usually right", an
   auto-classifier — re-creates the present bug with better manners.

**But the correction does hand the counter-argument a real weapon, and it deserves the
strongest form.** Today's fallback is not merely "unchosen" — it is *unknown to the tree*:
the ambient default can change under the swarm's feet without a single line of this repo
changing. That is a worse resting state than I first described, and it is a live argument
for making the fallback *explicit* rather than ambient. **That is a change to the spawn
path, not to doctrine, and it belongs with the mandate in §5** — where `--model inherit`
becomes a token the parent *says*, and the tool stops silently resolving a model that
nobody in the tree selected.

So the fix is **doctrine + the prompt at the point of decision**, not a new default:

- **`skill/SKILL.md`** — the spawn doctrine gains a step: *choose the child's model by
  task-fit, and say why.* A coordinator that spawns without naming a model is skipping
  a step, the same way one that spawns without a brief is.
- **`swarm spawn` help / `swarm world`** — the flag stops being a bare token in a usage
  line and starts *asking the question*. This is the cheapest possible nudge and it
  sits exactly where the decision is made.

Neither builds a classifier. Both make the choice **visible and inspectable**, which is
the only enforcement this repo has ever used, and the only one it needs.

---

## 6. The risk, stated as sharply as I can

**A too-weak model on a judgment task does not fail loudly. It fails *fluently*.**

This is the whole reason the ladder falls through to Opus instead of to Sonnet. Get it
wrong in the expensive direction and you have overpaid for a census — an annoyance with
a known, bounded price, visible on a bill. Get it wrong in the cheap direction on a
*judgment* seat and you get a design doc that reads beautifully and is subtly wrong, a
red-team that reports "no holes found" because it could not find them, a review that
approves the thing it did not understand. **None of those announce themselves.** They
are adopted, cited, built on, and shipped — and the cost lands later, denominated in
work, not tokens.

The eval already showed the mechanism in miniature: deepseek's memory call **errored,
and it never noticed** (`FLEET-EVAL-V3.md:117-121`). Not "it failed and reported the
failure." It failed and **carried on as if it had not**. That is what a weak model in
the wrong seat buys you, and it is why this document's tie-breaker is not "save money":

> **When you cannot cheaply tell whether the child is wrong, buy the model that is
> less likely to be wrong. Save money only where being wrong is cheap to catch.**

**And be clear about what this rule is for, because the repo will otherwise kill it
correctly.** This is **not a cost-savings rule**, and it must not be defended as one.
This project's own philosophy pre-refuses token-thrift arguments, and it is right to:
the scarce resource here has never been quota — it is **attention**, and correctness.
A rule that says *"spend less"* earns nothing and would deserve the graveyard.

The rule this document actually makes is about **fit**:

> **Put the strong model where being wrong is expensive and invisible. Put a cheap one
> only where being wrong is cheap to catch — because there, and only there, a mistake
> has somewhere safe to land: a strong parent who is reading the artifact anyway.**

Spending less at the leaves is a **consequence** of that, and a welcome one. It is not
the argument, and if the two ever conflict — if thrift would put a cheap model somewhere
its error would not be caught — **the fit rule wins and the savings are refused.**

---

## 7. What would falsify this, and how to find out cheaply

The mapping's weakest joint is stated in §2 and I will not paper over it: **the eval
watched DeepSeek and GLM, not Sonnet and Haiku.** I extended an *axis*, not a
measurement. Concretely:

- **Falsifier for Rung 3 (Haiku/Sonnet on leaves):** a Sonnet or Haiku leaf whose
  *artifact* is fine but whose **seat behavior** fails the way the eval's models failed
  — narrates its report instead of `swarm send`-ing it, never journals, does not
  terminate. If that shows up, Rung 3 is wrong **not because the model can't count, but
  because it can't be a swarm agent** — and the fix is that the parent must pull the
  artifact from the file rather than trust the report, or the tier floor rises. *(Status:
  live. The over-delegation probe's Haiku arms wrote **nothing** to their journals while
  alive — but both were blocked on a permission dialog at the very call that would have
  written one, so this is not yet a clean protocol-drop observation. It is the single
  thing most worth watching on the next cheap spawn.)*
- **Falsifier for the over-delegation ruling (§4):** a Haiku child that, hitting the
  **judgment wall** — the synthesis step the probe never reached — spawns children to
  escape it. That flips the answer, and Rung 3 must then couple the tier to the spawn
  right (cheap models only on structural leaves).
- **Falsifier for Rung 1 (seats must be Opus):** a Sonnet coordinator that runs a real
  subtree — briefs, judges, harvests, closes, survives a restore — with no protocol
  drops. That would make Rung 1 needlessly expensive, and it should be cheerfully
  demoted.
- **Falsifier for §4's "strong model is *more*, not better, on mechanical work":** an
  Opus census and a Haiku census of the same question where Opus's answer is *also*
  tighter. Then that paragraph is just snobbery and should be cut.
- **Already fired, and folded in:** *"an unpinned child inherits its parent's model."*
  **False** — `bin/swarm:834-835` passes no `--model` at all when unpinned, so the child
  takes the `claude` binary's ambient default. An earlier draft built an argument on the
  phantom mechanism (§5b). Left on the record as the specimen it is.
- **Already fired, and folded in:** *"a leaf stays a leaf."* **False** — 18 of 115 agents
  in this tree grew a coordinator role nobody briefed them for (§4). Rung 3's "cheap →
  leaf" is therefore a **promise the parent must keep**, not a fact the tool enforces,
  until `A leaf never spawns` (`FLEET.md:88`) is made structural.

**A standing caveat on judging a cheap child — read this before you conclude the tier
failed.**

> **An agent's observables lie. "No journal, no artifact, idle 16m, stale last-words" is
> not evidence of a weak model. It is evidence of nothing until you read the pane.**

Every one of those observables is *also* what a child parked on an interactive permission
dialog produces — and **`swarm spawn` writes its settings with hooks only and no
`permissions` block**, so *every* spawned child is exposed to this, on any tier. The
over-delegation probe nearly shipped "Haiku froze on a complex task"; it was false — the
model was blocked on a `1. Yes` dialog with good work behind it. The fleet eval hit a cousin
of the same trap from the opposite direction, headless: its pane-less runner read as `dead`,
so four native probes "sent correct reports and then *despaired* incorrectly — scored from
files" (`FLEET-EVAL-V3.md:159-161`).

This matters here more than anywhere, because **the entire tier rule depends on a parent
being able to tell "this child was wrong" from "this child was blocked."** A parent who
cannot will read a blocked Haiku as a failed Haiku, conclude the cheap tier does not work,
and revert to Opus-for-everything **having learned nothing — and having learned it
expensively.** The tier rule and this caveat ship together. *(The missing `permissions` block
is a swarm defect wider than this document, surfaced by `weak-model-deleg`; it is named here
so it does not evaporate, and it belongs to whoever owns the spawn path.)*

**The cheap experiment** — and it is genuinely cheap, because the battery already
exists. `docs/design/FLEET-EVAL-V3.md` is a *re-applicable rubric* (D1 duties, D2
delegation, D3 tool/CLI, D4 long-horizon) with briefs on disk. Run two more cells —
`claude-sonnet-5` and `claude-haiku-4-5-20251001` — through the **same** battery, and
the confound that caveats this whole document (§2) **collapses**: same harness, same
rig, same rubric, only the model varies. That is the one measurement that would turn
this document from a directional read into a measured one, and it is a few hours of
rig time on a rig that is already built and already reviewed.

Until then, this is doctrine with its evidence and its uncertainty both on the table,
which is the honest state to ship it in — and it is strictly better than 143 spawns of
nobody thinking.
