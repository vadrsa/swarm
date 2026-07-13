# ONBOARDING — the first five minutes, and the two ways they go wrong

**Author:** `onboarding-scout`, at the operator's request after watching people
start using swarm. Written at `main@aa6063d`, 2026-07-12. **Design only; no code.**
Recommendation, not survey.

**Evidence discipline**, as in SPAN.md and STRUCTURE.md: **VERIFIED** (I read the
line / ran the command — quoted), **MEASURED** (cites a field-evidence record with
numbers), **REASONED** (first-principles argument, could be wrong, falsifier named).
Where the record contradicts me, the contradiction is named, not smoothed.

---

## 0. The two pitfalls, as observed

Not hypothesized — watched, by the operator, in people picking the tool up:

1. **The long-session dismissal.** People run `/swarm` in the same session they
   have been developing in for an hour. Two harms compound: the accumulated
   context leans the session to **dismiss** swarm for most things — it has
   momentum as a *doer*, not a coordinator — and the prior context, which is the
   single richest description of the work that exists anywhere, is **never
   analyzed** for how that work could be done better with a tree. A wasted asset,
   and a biased judge deciding whether to use the tool at all.

2. **The flat tree under the human.** Out of the box, handing swarm tasks
   produces `operator(=the human) → N workers`. The human then hand-manages the
   whole flat tree: N panes, N reports, N judgments, N restarts. They wanted to
   manage *one thing* and instead they got a job.

Both are onboarding failures — they happen in the first five minutes, to someone
who has not yet learned what the tool is for. Neither is a bug in any mechanism.

---

## 1. The lead finding: the doctrine reaches the whole tree and skips its root

**VERIFIED** — `bin/swarm:771-812`, `spawn_header()`. Every agent the tool ever
creates is born holding the delegation doctrine, in its own spawn header:

> Delegate by default: keep judgment, verification, and glue; spawn children for
> the work itself — doing parallelizable work serially yourself is off-track. …
> You are over span when you can no longer name each child's state and the next
> artifact you expect from it without re-reading. If a spawn would take you past
> that, spawn a coordinator and split the stream instead… The operator's span is
> theirs to declare and yours to protect.

Every node in the tree gets that. **Except one.** The human's own session — the
node in the operator's chair, the one that actually decides the tree's shape — was
never spawned by `swarm`, so `spawn_header()` never ran for it. Its *entire*
doctrine surface is `skill/SKILL.md`, and nothing else.

This is the mechanical explanation of **pitfall 2**, and it is worth stating
precisely because it is easy to overclaim. SKILL.md is **not** silent: it already
says *"You sit in the coordinator's chair, and a coordinator delegates by
default"* (VERIFIED, `skill/SKILL.md:9-11`), and its §5 already says *"protect the
operator's span… hand the operator one ranked page, never the raw stream"*
(VERIFIED, `skill/SKILL.md:40-49`). The shipped delegation and span doctrine is
**already there**. So the honest gap is narrow, and it is these three things:

- **The seat is described as a chair, not a tenure.** "You sit in the coordinator's
  chair" reads as a posture for the duration of a spawn burst. It never says the
  session *becomes* the standing coordinator and **holds** the tree for the whole
  run — so after the spawn burst, the session drifts back to being a doer, and the
  children's reports drift up to the human. (REASONED.)
- **§5 tells the session to protect *the operator's span* — but never says the
  operator's span is, by default, ONE: this session.** "Hand the operator one ranked
  page" is about *volume*. It never establishes the *topology*: that the human's
  direct load should be a single node, and that node is the session they are typing
  into.
- **The skill presumes a fresh start.** It opens *"The user wants a goal accomplished
  by a swarm"* — a goal handed to an empty session. The mid-session case, which is
  how people actually invoke it, appears **nowhere**. That is **pitfall 1**, and it
  is a gap of omission, not of error.

**Why doctrine text is the right vehicle, and not a mechanism.** This is not a
matter of taste; it is the one thing in this design that is **MEASURED**
(`docs/audit/field-evidence-2026-07-10.md`, via SPAN.md §2): an agent that never
once *mentioned* spawning under a neutral brief went on to spawn, brief, verify,
judge, and close four children once four sentences entered its spawn header. The
lesson generalizes, and SPAN.md already states it as law:

> **agents do not invent structural moves that are not in their frame; they
> reliably execute structural moves that are.**

Both pitfalls are **frame gaps**. Standing up as a coordinator in place, and mining
one's own context before spawning, are both moves that are *mechanically available
today* — they need no verb that does not exist — and are *absent only from the
frame*. That is the exact profile of a problem this repo fixes with prose.

---

## 2. Recommendation: doctrine-only. Zero verbs, zero concepts, zero state.

**The costed answer to the brief's scope question is: no helper.** Not deferred —
refused, on evidence, and the evidence is stronger than "the philosophy prefers
prose."

`mine-probe` was dispatched to break this, and it did the honest thing: it **built**
the helper before arguing against it (`.swarm/research/mine-probe.md`, VERIFIED).

- **The mining helper is 100% buildable, and trivially so.** A session can address
  its own transcript with no archaeology: `$CLAUDE_CODE_SESSION_ID` plus a slugified
  `$PWD` gives `~/.claude/projects/<slug>/<session-id>.jsonl`. mine-probe computed its
  own path and read its own file from inside itself (VERIFIED, ran it). The whole
  reader is ~15 lines. The swarm hook **already** receives `transcript_path` in its
  hook payload and already parses transcripts for `ps` last-words
  (VERIFIED, `bin/swarm:450`, `bin/swarm:710`).
- **And it must still be refused, because it is anti-correlated with need.**
  Pre-compaction — the *only* window in which mine-first fires with anything worth
  mining — **the conversation IS the context**: a mining verb would print into the
  context a lossy summary of that same context. Post-compaction, the detail is
  already gone, and re-injecting raw JSONL is the most expensive possible move at the
  moment there is least room for it. *Most useless when context is fresh; most
  harmful when context is scarce.* (REASONED, and the strongest argument in this
  document — it kills the helper on **engineering** grounds before philosophy is
  even consulted.)
- **The repo already killed this exact mechanism once.** The transcript-pointer
  (`checkpoint --context`) is concept 22 in SIMPLEST §2's count and appears in its
  deletion table with the ruling: *"the agent notes what it wants in its journal; a
  wrong-looking number that no code consumes earns nothing"* (VERIFIED,
  `SIMPLEST.md:71`, `:187`). A mining verb re-raises that corpse under a new name.
- **PHILOSOPHY §8 then closes it:** *"prompt-level convention first, a visibility verb
  second, an engine never — unless the record shows the convention failing."*
  Mine-first has **never been tried**. There is no record of the convention failing
  because there is no record of the convention. Shipping the tool alongside the
  doctrine is the definition of guessing at a workflow.

**The one real gap, closed for free.** There *is* a case the doctrine cannot mine: a
session whose context was already compacted, whose working memory was *"summarized
away"* (VERIFIED — the codebase says exactly this, `bin/swarm:436-439`). The fix is
not a tool; it is **one clause** that turns the failure into an escalation:

> *If your context has been compacted and you cannot answer, say so and ask —
> do not guess a tree.*

That is PHILOSOPHY §10 (*an honest unknown beats a plausible wrong value*) applied to
tree shape. A hallucinated decomposition, built from a summary, is exactly the
"plausible wrong value" that §10 forbids — and it is *worse* than a wrong number,
because a wrong tree spawns agents that then do wrong work.

**What would earn the helper later** (stated now, so the door is honest rather than
merely shut): a real session producing a **bad delegation map that traces to missing
recall rather than to bad judgment** — the model demonstrably could not remember what
it had been doing, pre-compaction, and said so. Until that observation exists in the
record, building the reader is guessing. (This is mine-probe's own falsifier, adopted.)

---

## 3. The doctrine

Two additions to `skill/SKILL.md`, composing with — **not restarting** — the shipped
delegation, span, and operator-seat doctrine. §4 carries the drafts — and, per the
operator's ruling of 2026-07-12, they are **two files**: the load-bearing stances go
inline in SKILL.md, their reasoning to `skill/references/COORDINATING.md`. §4b states
the rule that decides which is which, and why a referenced file does not reintroduce
§1's bug.

### 3a. The seat is taken in place, and the human's span is one node

The stance the session must adopt when the skill fires, stated as tenure rather than
posture:

> **You become the coordinator, here, in this session.** Not a doer with helpers, and
> not a separate coordinator you spawn — *this conversation* is the coordinator seat,
> and it stays that way for the whole run: you own the tree, you hold the reports, you
> judge the work, and the human's direct load is **one node — you**.

Three properties of that sentence, each doing work:

- **In place, no extra hop.** The alternative — spawn a coordinator agent and have the
  human talk to *that* — adds a layer whose only content is forwarding, which SPAN §3d
  already condemns by name (*"A middle layer that only forwards… is structure lying
  about work"*, VERIFIED). It also costs a hop of briefing fidelity for nothing. The
  session in front of the human is **already** a Claude session with the full context;
  making it the coordinator is free, and this document's own parent session did exactly
  this (VERIFIED — the operator's dispatch entry for this task: *"coordinator form =
  human's session becomes coordinator IN-PLACE (as this session)"*).
- **It is the default, and it is opt-out-able.** A human who says *"just spawn me three
  workers and I'll drive them myself"* gets exactly that, and the session says so
  plainly once rather than nagging. The default protects the person who has not yet
  learned what to ask for; the opt-out protects the person who has. (PHILOSOPHY §6:
  autonomy bounded by structure, not permission — the human's autonomy most of all.)
- **It composes with SPAN, it does not restate it.** SPAN already made the operator's
  span a thing the tree must protect; this names its default *value* at the root — one
  — and its *shape* — the session itself. SPAN's §5 "player-coach degradation" is the
  hazard being avoided: a session both grinding work and judging children does both
  worse.

### 3b. Mine first: the prior context is the input, not the bias

The first act when the skill fires in a session that has already been working:

> **Your first act is to mine this session, not to spawn.** Before the first `spawn`,
> read back over what this session has been doing: what was the goal, what is already
> known, what did we learn the hard way, which parts are independent of each other, and
> what is the decomposition? **Write that decomposition into your journal** — the work,
> split, with what each part needs to know — and brief your first children from it.
> **And if you decline to spawn, journal that too, with your reason.**

(The last sentence was added in the §4 revision, and it closes a hole that had been in
this design since the first draft: §5's collectors have *always* read a **journaled
decline** — *"prices the stance in writing"*, *"no written weighing of delegation"* —
and no draft ever instructed the session to write one. A session that mined, judged the
work indivisible, and spawned nothing would have been scored as the dismissal pitfall
while behaving exactly as told.)

The load-bearing design choice here is **the artifact — and its destination**. "Be less
of a doer" is an attitude: unfalsifiable, unenforceable, and weak against an hour of
momentum. "Write the decomposition into your journal before you spawn" is a **structural
move producing an inspectable file** — the only kind of instruction the field evidence
says agents reliably execute (§1).

**The destination is not a detail; it is what makes the claim falsifiable at all.** An
earlier draft of this document said only *"write that decomposition down"* and claimed
the map "doubles as its own collector — it either exists in the transcript or it does
not." The adversarial review killed that, correctly: a session satisfies *"write it
down"* by typing into the chat, which is not an artifact but thinking aloud with a period
at the end; and the transcript is the exact store §2 spends its length proving is
unreadable (a probe cannot see it, and post-compaction it is gone). **The journal is the
repo's own designated durable record** — VERIFIED, `bin/swarm:436-439`: *"your working
memory was just summarized away; **your journal is your most reliable record**"* — it
costs **zero concepts** (WORLD concept 9 already makes the journal every agent's
continuity), it survives the one failure §2 worries about, and it turns the mine-first
collector from a judgment about vibes into **an `ls` and a read** (§5).

It also directly inverts the harm. The dismissal reflex (*"this is faster if I just do
it"*) is strongest exactly when the session knows the most — and a session that knows
the most is precisely the one best positioned to write a **good** decomposition. The
doctrine spends that knowledge on the tree instead of against it.

### 3c. What is deliberately NOT here (the NOT-list)

- **NOT a forced fresh session.** The operator ruled this out and the ruling is right:
  it throws away the asset. Mining is the fix; discarding is the failure it is fixing.
- **NOT a `swarm mine` verb, `swarm coordinate` verb, or any new verb.** §2. Both moves
  are `spawn` + `send` + prose; the four verbs stand.
- **NOT a separate spawned coordinator pane.** §3a — a forwarding layer, condemned by
  SPAN §3d, and one hop of fidelity loss for zero judgment added.
- **NOT a new WORLD.md concept.** WORLD is the *contract between agents*; this is
  *how the human's session enters the tree*. Concept 9 already carries delegate-by-
  default and the span clause, and the spawn header already carries them to every
  agent. Nothing here is a fact a file must witness. The nine concepts stand at nine.
- **NOT a stored "coordinator mode" flag.** Config wearing the costume of a fact —
  killed for span numbers (SPAN §2) and for trigger modes (PHILOSOPHY §5). The stance
  is witnessed by what the session *does* (does it hold the tree?), which is exactly
  what the collector in §5 reads.
- **NOT an overseer/load-balancer node.** SPAN §4 killed it as *"the nag reborn"*. The
  in-place coordinator is not that: it is not a node whose job is other nodes'
  *behavior*; it is the node that **owns** the work and delegates it, and it is the seat
  the human already occupies. See §6 for this objection taken seriously.

---

## 4. The two-file split (drafts, not applied)

**Revised per the operator's ruling of 2026-07-12: the doctrine does not all go
inline.** The first draft of this section put ~1,650 bytes of doctrine into the
skill's opening paragraph — +19.5% on the one file every root session reads —
and the operator refused the price. This section is the answer, and the answer
is **not** "the same text, moved." It is a split with a rule, and the rule is
forced by the mechanism.

### 4a. The mechanism, verified — a referenced file is a *maybe*

Before deciding what may be demoted, I established what a companion file actually
*is* to a firing skill. **VERIFIED**, from the official docs
(`code.claude.com/docs/en/skills`) and confirmed against two real installed
skills on this machine:

- **Only `SKILL.md`'s rendered body enters context when a skill fires.** The skill
  *directory* is not loaded. (Docs: *"the rendered `SKILL.md` content enters the
  conversation as a single message."*)
- **A companion file is read only if the model chooses to `Read` it.** Nothing
  injects a file listing; the model knows the file exists **only** because
  SKILL.md names its path. (Docs, on why the pattern exists: *"Large reference
  docs… don't need to load into context every time the skill runs."*)
- **The convention is a `references/` subdirectory and a relative markdown link.**
  VERIFIED verbatim in `claude-automation-recommender/SKILL.md:71` —
  *"See [references/mcp-servers.md](references/mcp-servers.md) for detailed
  patterns."* — and in `build-mcp-server` (`references/auth.md`,
  `references/tool-design.md`). So the file is **`skill/references/COORDINATING.md`**,
  not `RECOMMENDATIONS.md`. This repo has no companion-file precedent of its own
  (`skill/` and `skill-middleware/` each hold a lone SKILL.md), so the convention
  is borrowed, not invented.

**This is the whole design constraint, stated mechanically: what goes in the
reference is read *sometimes*, at the model's discretion, and must be assumed
never read.**

### 4b. The split rule, and its answer to the lead finding

§1's lead finding is that **doctrine the root session does not reliably see is the
bug** — every spawned agent gets the delegation doctrine in its header, and the
one node that shapes the tree does not. A referenced file the session may never
open is, on its face, that same bug in a weaker form. The split therefore cannot
be *"short things inline, long things out."* It has to be:

> **INLINE:** anything whose absence changes what the session **does**.
> **REFERENCE:** anything that only makes a reader **agree** with what it already does.
> **And no falsifier may collect on an artifact that a reference-only instruction produces.**

That rule dissolves the tension rather than trading against it, and the reason is
the distinction the lead finding turns on: **unread *instruction* is the bug;
unread *justification* is the ordinary, healthy state of a design document.**
`references/COORDINATING.md` carries **zero instructions** — it is the *why*, the
two pitfalls, the span/topology distinction, the compaction rationale, the
out-of-scope edge. If it is never opened, **nothing behavioral is lost**, and
that is not a hope: it is checkable by reading the file for imperatives, which
§4e does.

**The corollary is the cost discipline that killed this section's second draft.**
If the reference changes no behavior, then **SKILL.md must not pay real bytes to
advertise it.** A second draft spent 323 bytes — 27% of all growth, in the single
hottest file in the repo — on a pointer section whose own words told the model it
did not need to read what it pointed at. That is an advertisement for a token
sink, and worse: a compliance-inclined session that dutifully opens a 6.6 KB
reference at every fire pays *more* than the all-inline draft the operator
rejected. The pointer is now **one clause appended to an existing line** (156 B),
placed at the *bottom* of the file, phrased so that not reading it is the
expected outcome.

### 4c. The inline half — `skill/SKILL.md` (diff, not applied)

**Purely additive.** The shipped opening paragraph is now **untouched** (the
rejected draft rewrote it), so `STRUCTURE.md §7`'s citation of "SKILL.md point 2"
and the doctrine numbering both survive unchanged, as do the operator-seat
section and the precondition.

```diff
--- a/skill/SKILL.md
+++ b/skill/SKILL.md
@@ -12,6 +12,20 @@
 glue; the work itself goes to children. You doing the work is the failure mode.

+**You stay the coordinator, here, in this session.** Do not spawn a coordinator
+and hand it the tree; do not hand the human a row of workers to drive — the
+human manages **one node: you**. (If they'd rather drive the workers themselves,
+say so once and do it.) Doctrine 5's "~3" is a *span*, not a licence to leave
+the human three children.
+
+**Mine before you spawn.** If this session has already been working, your first
+act is not to spawn: read back over what it has been doing — the goal, what is
+known, what was learned the hard way, which parts are independent — and write
+that decomposition **into your journal** before the first spawn, then brief each
+child from it. If you decline to spawn, journal that too, with your reason. If
+your context was compacted, read your journal first; if you still cannot answer,
+say so and ask — do not guess a tree.
+
 ## The coordinator doctrine
@@ -106,3 +120,5 @@ artifacts, never claims). It tells you what exists, not what to do. (`swarm`
-with no args lists the verbs.)
+with no args lists the verbs.) The two stances above are complete as written;
+their reasoning, if a case collides with one, is in
+[references/COORDINATING.md](references/COORDINATING.md).
```

**Why each inline clause cannot be demoted — the test is §5, not taste.** Every
falsifier in §5 collects on an artifact that one of these clauses produces. A
clause whose artifact a collector reads **cannot** live in a file that may never
be opened, or the falsifier collapses into a judgment about vibes:

| inline clause | the artifact a §5 collector reads | why not demotable |
|---|---|---|
| *"You stay the coordinator, here, in this session"* | — | the stance itself: tenure + place. §1's whole gap (`:9` gives a chair, never a tenure, and never says the seat **is this conversation**) |
| *"Do not spawn a coordinator and hand it the tree; do not hand the human a row of workers to drive"* | Claim 1's `parent` counts in `agents/*.json` | **both forbidden moves, in the imperative** — this is what lets a cold session *fail the test and know it*. Claim 1's falsifier (*"≥3 direct children and no intermediate node"*) is only fail-able because this sentence was seen |
| *"the human manages **one node: you**"* | Claim 1's `parent` counts | the **topology** value. Doctrine 5 protects the operator's *span* (a volume claim); nothing else names the default at the root as **one** |
| *"(If they'd rather drive the workers themselves, say so once and do it.)"* | — | RULING 1: **kept, unchanged in substance**. An operator term of the brief (`.swarm/journal/operator.md`: *"P2=coordinator-layer default w/ opt-out"*); an instruction the session obeys, never state. §6.3 |
| *"Doctrine 5's '~3' is a span, not a licence to leave the human three children"* | Claim 1's falsifier threshold | without it the file carries **two numbers** and a cold session can rationalize a 3-wide flat tree as compliant. §7 called this "the most cuttable line"; the adversarial review of the split reversed that, and I agree — it is the *cheapest* defence of Claim 1 that exists, at one line |
| *"your first act is not to spawn: read back… the goal, what is known, what was learned the hard way, which parts are independent"* | Claim 2's grep of the first child's `.task` | the structural **first act**, and the four questions. Nothing in SKILL.md addresses prior context at all (VERIFIED by grep: zero hits) |
| *"write that decomposition **into your journal** before the first spawn"* | **Claim 2's whole instrument**: does a decomposition entry exist in `.swarm/journal/operator.md`, and does its **mtime precede** the earliest `agents/*.json`? | **the single most load-bearing string in the file.** Demote this one sentence and the entire mine-first falsifier collapses — the collector would be reading for an artifact that only an unread file asked for. This is the clause that proves the split rule is not cosmetic |
| *"then brief each child from it"* | Claim 2's instrument 2 (grep the `.task` for prior-context tokens) | the map must **reach the briefs**, or it is a status report wearing a costume |
| *"If you decline to spawn, journal that too, with your reason"* | Claim 1's *"prices the stance in writing"* and Claim 2's *"no written weighing"* branches | **NEW, and it closes a pre-existing hole** the split review found: §5 has always collected on a *journaled decline*, and **no instruction in any draft ever asked for one**. A session that mined, judged the work indivisible, and spawned nothing would have been scored as the dismissal pitfall while behaving correctly. Twelve words |
| *"If your context was compacted, read your journal first; if you still cannot answer, say so and ask — do not guess a tree"* | the §2/§5 recommendation-falsifier (*"could not remember, and said so"*) | §2's one-clause gap-closer, and the observation that would earn the refused helper. The gate is **"still cannot answer"**, not "you were compacted" — that word is what stops the clause becoming a bail-out |

### 4d. The referenced half — `skill/references/COORDINATING.md` (written)

**Written to `skill/references/COORDINATING.md`** (117 lines / 6,809 B). Its
opening paragraph is load-bearing and states the contract to its own reader:

> Background for the two stances at the top of SKILL.md. **Nothing here is a new
> instruction — the two stances are complete without this file.** This is the
> *why*, the two failures they exist to prevent, and what each looks like when
> done well. Read it if you want to know whether a stance applies to your case;
> you do not need it to obey them.

Its sections, and what each is doing:

| section | content | why it is safe to demote |
|---|---|---|
| **The two failures these stances prevent** | §0's two pitfalls, as *watched* — the long-session dismissal (the biased judge sitting on the best brief that will ever exist) and the flat tree under the human — plus §1's law: *agents do not invent structural moves that are not in their frame; they reliably execute the ones that are.* | **Motive.** A session that never learns *which* failures it is avoiding still avoids them, because the inline text names the moves, not the failures |
| **Why the seat is a tenure, not a posture** | the drift argument; **in place, no extra hop** (a forwarding layer is *structure lying about work*; the session is already a Claude session with full context, so making it the coordinator adds **no node**); **span is volume, topology is shape**; the seat is theirs to give; and **what this is not** — not an overseer, not a load-balancer, and *argue it from attention, never from load* (the record is 3-for-3 that load does not summon a coordinator) | **Justification and collision-resolution.** The inline text already *does* all of this; this section is what a session reads when it wants to know **why**, or when a case collides — e.g. it thinks "one node" contradicts doctrine 5 |
| **Why the map goes in the journal, and goes first** | why an artifact beats an attitude (*"be less of a doer"* is unfalsifiable and weak against an hour of momentum); why the **destination** is what makes it real (a session satisfies "write it down" by typing into the chat — *thinking aloud with a period at the end*); why the brief comes from the map (**briefing quality**, a claim about the goal — explicitly **not** context economy, which PHILOSOPHY §1 forbids); how it **inverts the harm**; and the compaction rationale (*the gate is "you still cannot answer", not "you were compacted"*) | **Justification.** Every *instruction* here — journal, before the spawn, brief from it, escalate if still stuck — is already inline. This is the argument for each |
| **The edge this does not cover** | §6.7's out-of-scope case: the session that *should* have fired `/swarm` and never did | **Scope honesty**, addressed to a human reader. Reworded from an imperative (an earlier draft ended *"Mine anyway"* — an instruction addressed to a session that by construction never reads this file: dead text) |

### 4e. Adversarial review of the split — what it found

The split was attacked on its own terms (does the inline stance survive alone?
does the reference add without duplicating?). Three findings changed the drafts;
they are recorded rather than smoothed:

1. **The inline stance survives alone — VERIFIED by reading only the new
   SKILL.md.** Both behaviors are caused by inline sentences (table in §4c), and
   **every §5 collector reads `agents/*.json`, the operator journal, or a child's
   `.task` — never the skill's prose.** No falsifier depends on the reference
   being opened. This is the load-bearing check, and it passes.
2. **The reference contained three live imperatives.** *"say so plainly once, then
   do it, and do not nag"* (an instruction constraining the opt-out's speech act —
   **folded inline**, into *"say so once and do it"*); *"Mine anyway"* (**reworded**
   to a scope note); and a *"what belongs in the map"* list that restated the inline
   list (**cut** — the reference now gives only the two additions the inline list
   does not: *the goal as this session now understands it*, and *what was learned
   the hard way*). A reference that claims to carry no instructions must be *checked*
   for them, not trusted.
3. **The second draft's pointer was the worst byte in the file, and the measurement
   caught it.** That draft came in at **+19.7% — reproducing the number the operator
   had just rejected.** The doctrine block had shrunk 47%, and the entire saving was
   spent on a 323 B pointer section explaining why not to read the reference. Cut to
   one clause (156 B). **The lesson is general and belongs in the record: in a split,
   the pointer is a cost line, and a pointer that costs more than a fifth of what the
   split saved has eaten the split.**

**The honest residue, stated rather than buried.** The split's *real* achievement is
**a 47% cut to the doctrine paragraph** (1,646 B → 865 B), not an extraction — because
**there was never any depth inside SKILL.md to extract.** The rejected draft was one
oversized paragraph; `references/COORDINATING.md` is a **new** document, not a moved
one. It earns its place on a fact worth naming: `install.sh:15` symlinks **only
`skill/`** into `~/.claude/skills/swarm` (VERIFIED), so `docs/design/ONBOARDING.md` —
where all of this reasoning already lives — **ships to nobody who installs rather than
clones**. Without the reference, an installed user has the *what* and the depth
**nowhere**. That is what the companion file is for, and it is the whole of what it is
for. It is also, honestly, a **third statement** of an argument that exists in
ONBOARDING §1/§3/§6 and upstream in SPAN/PHILOSOPHY, and it will drift from them
unless someone reconciles it. That is the price, named.

### 4f. Re-measured

MEASURED (`wc -lc`, not estimated):

| file | before | after | delta |
|---|---|---|---|
| `skill/SKILL.md` — **loaded on every fire** | 106 lines / 6,809 B | 122 lines / **7,833 B** | **+16 lines, +1,024 B, +15.0%** |
| — of which: the two inline stances | — | 865 B | (the rejected draft's block: **1,646 B** → **−47%**) |
| — of which: the pointer clause | — | 156 B | one clause on an existing line, not a section |
| `skill/references/COORDINATING.md`  — **0 B of context unless opened** | — |  117 lines / 6,809 B | new file |
| the rejected all-inline draft, for comparison | 106 / 6,809 | 125 / 8,140 | +1,331 B, **+19.5%** |
| numbered doctrine (1–5), operator seat, precondition | untouched | untouched | 0 |
| opening paragraph | untouched (the rejected draft rewrote it) | untouched | 0 |
| `spawn_header()`, `WORLD.md`, concepts, verbs, state | untouched | untouched | 0 |

**The number the operator objected to, honestly framed: 19.5% → 15.0%.** That is a
real cut but a modest one, and I will not oversell it — **the doctrine itself is 865
of those bytes, and none of it can be demoted without dropping a falsifier** (§4c).
If 15.0% is still too much, the next cut is named and it is a *real* one: reword
doctrine 5's *"default ~3"* so the span/topology reconciliation clause (~127 B)
becomes unnecessary, rather than patching over it. Cutting anything else in the
inline block deletes a collector, and a doctrine whose falsifier cannot be collected
is a doctrine this repo does not ship.

---

## 5. Falsifiers, with collectors

**The finding that reshapes every collector here, and it is mechanical:** every probe
this repo has ever run measures the **`spawn_header`** surface — and *both* of these
claims live on the **SKILL.md** surface, which **a spawned probe never sees**.
VERIFIED: `grep -i skill bin/swarm` returns nothing; a child's entire doctrine exposure
is `spawn_header(name, parent) + task` (`bin/swarm:896`). SKILL.md reaches Claude only
through the `~/.claude/skills/swarm` symlink (`install.sh:15-16`), which **only root
sessions traverse.** field-tester had already written this limitation down and it went
unactioned (VERIFIED, `docs/audit/field-evidence-2026-07-10.md:153-156`):

> *"the doctrine also lands in SKILL.md, which shapes ROOT sessions… **a spawned probe
> never sees it.** … SKILL.md's effect on root-session behavior is untested by this
> experiment."*

**So any collector that says "spawn a probe and watch it" is decorative.** Both
collectors below run **root sessions in panes** — the rig field-tester already built
(unnamed `claude` sessions over a sandbox `SWARM_DIR`; `bin/swarm:64` reads
`SWARM_AGENT_ID or "operator"`, so an unnamed session *is* the operator). And the
one-variable move for a SKILL.md claim is **repointing the skill symlink**, not
swapping the binary — the exact analogue of the binary-md5 discipline the existing
protocol rests on.

### Claim 1 — the coordinator stance (pitfall 2)

> *With this doctrine, a session handed a multi-part goal stands up as coordinator in
> place — the human's direct load stays at one node — instead of handing the human a
> flat row of workers to drive.*

- **Collector (cheap, ~0 tokens — recommended).** The next time the operator hands a
  real session a real multi-part goal, count the operator's direct children:
  `for f in .swarm/agents/*.json; do jq -r .parent $f; done | sort | uniq -c`.
  Ten seconds, real conditions, no synthetic-task risk.
- **Collector (expensive, the before/after pair).** Sandbox `SWARM_DIR`, root session
  in a herdr pane, one three-part goal of *real size* (each part long-running and
  stateful enough to want its own journal and turn stream), given verbatim to both
  arms. Baseline = installed skill symlink; after = symlink repointed at the branch's
  `skill/`, with the SKILL.md diff quoted into the evidence file. Poll
  `$SWARM_DIR/agents/*.json` for each record's `parent`.
- **FALSIFIED WHEN:** in the *after* arm the sandbox operator ends up with **≥3 direct
  children and no intermediate node** — the post-doctrine session still hands the human
  a flat tree.
- **NOT falsified** if the session declines to spawn but **prices the stance in
  writing**: the delegation pair established that "asked, priced, declined, with a
  stated falsifier" is a doctrine *success*, not a failure.
- **The way this probe tests the wrong thing** (the SPAN flood lesson, and it is the
  likeliest outcome if I am careless): if the three tasks are small, the session will
  do what SPAN's flood-1 probe did — **route around the tree entirely** via harness
  subagents (~10-way parallel, no names, invisible to `ps`), which is *correct* at that
  size and measures nothing about stance. That looks like falsification and is not. If
  the after-session still routes to subagents, the honest verdict is **INCONCLUSIVE —
  task too small**, scored exactly as flood 1 was.

### Claim 2 — mine-first (pitfall 1)

> *With this doctrine, a session firing `/swarm` after substantial prior work mines that
> work first and briefs its first children from it — rather than dismissing swarm and
> grinding on, or spawning generically.*

**The structural problem, stated honestly: this claim cannot be probed synthetically,
and pretending otherwise would be the flood-1′ error verbatim.** Mine-first fires only
in a session *with real doer-momentum* — and momentum is the one variable a seeded
prefix cannot manufacture. A spawned probe fails twice over: it never sees SKILL.md,
and its "prior context" would be authored by *my* brief, so its momentum is an artifact
of my framing. **Rejected.**

- **Collector (production spot-check — the recommendation).** This is where SPAN §6
  itself landed after three synthetic floods failed: *"the cheap watch is production
  use."* Standing instruction to field-tester: watch for the next root session where
  `/swarm` fires **after** substantial prior work.
- **The instrument is two file facts and one grep** — *not* a judgment about vibes.
  Because the doctrine names the journal as the map's destination, the artifact is a
  file, and the collector reads files (which is the evidence standard this repo already
  holds itself to: *"Files are the timeline"*):
  1. **Did the map get written, and did it come first?** Does a decomposition entry
     exist in `.swarm/journal/operator.md`, and does its **mtime precede the earliest
     `.swarm/agents/*.json`** of the children it describes? (The entry's *existence* and
     *mtime* are facts; only its self-written timestamp would be a claim.)
  2. **Did the map reach the briefs?** Take five concrete tokens from the session's
     prior work (file paths, symbol names) and grep the first child's `.task` for them.
- **FALSIFIED WHEN any of these fires:**
  - **the dismissal pitfall:** the session spawns nothing within two turns and keeps
    doing the work itself, with **no written weighing** of delegation;
  - **the ritual pitfall:** no decomposition entry in the journal before the first spawn
    — the doctrine was read and not performed; or
  - **the generic-spawn pitfall:** it spawns, but the first child's brief contains
    **zero** concrete artifacts of the prior context (the grep returns nothing) — the
    map was written and then ignored, which is a status report wearing a costume
    (PHILOSOPHY §3).
- **Cost:** ~0 probe tokens, one procedure, unknown wait. Its weakness is stated: no
  baseline arm, n=1. That is the honest price of testing a claim whose subject is real
  doer-momentum — the one variable a synthetic prefix cannot manufacture, and faking it
  would reproduce the flood-1′ error exactly ("my flood failed to exceed one agent's
  attention" ≈ "my prefix failed to create real momentum").

### Falsifier for the recommendation itself (§2)

**The helper earns its way in when:** a real session produces a **bad delegation map
that traces to missing recall rather than to bad judgment** — the model demonstrably
could not remember what it had been doing and said so. Collector: the same spot-check
above, reading *why* a map was bad. Until that observation exists, building the reader
is guessing at a workflow (PHILOSOPHY §8).

---

## 6. The sharpest objections, and my answers

**1. "You are defaulting a structure this system has never once needed — and the load
argument is dead, measured 3-for-3."** VERIFIED, `STRUCTURE.md:82-98`: *"Load (SPAN's
bet) — **REJECTED by the record** … MEASURED, three times, zero for three: the flood
always resolved below the tree… **Structure in this swarm has never once come from
momentary attention pressure.**"* And *"none of the four standing arms is a
coordinator."*

**I concede it entirely, and this design does not rest on it.** The three floods asked
whether *load* summons a coordinator; it does not, and agents reason their way out of
one on cost grounds — correctly. This proposal rests on something else, and the record
is unambiguous about it: **the operator's attention.** PHILOSOPHY §9 records the
operator's *second instruction in the entire project* —

> **"Since this session is my channel of communication, I don't want it polluted by you
> validating work that can be done by a subagent. What other options do we have to keep
> this session clean?"**

— and notes: *"That question created the chief-of-staff (ASK #2)."* A flat tree the
human hand-manages **is** that channel pollution. The coordinator layer was never
killed; **it was founding.** SPAN's own falsifier 5 names this failure directly:
*"Operator load ignores the declared span: the desk grows past ~3 standing decisions
while the coordinator keeps forwarding instead of holding."* This is a restoration, not
an invention — and it is argued from attention, never from load.

**2. "Mine-first is a cache, and you were told to save the goal, not the context."**
VERIFIED, PHILOSOPHY §1 — the load-bearing principle, in the operator's own words:
*"Let's step back on this, are we trying to save context or save the goal?"* …
*"Context efficiency is a side effect the design is allowed to enjoy, never a thing it
optimizes for."*

**This is the sharpest objection in the set, and it forced a rewrite of the doctrine's
motive.** The brief's own framing of pitfall 1 — *"the prior context is never analyzed…
a wasted asset"* — is context-economy framing, and §1 refuses it. Note what the doctrine
draft in §4 therefore **never says**: it never says "don't waste the context you already
paid for." It says the coordinator that ignores what its session learned **briefs its
children worse than a stranger would**. That is a claim about **briefing quality**,
which is a claim about **the goal**: SPAN §1.3 established that judgment is relational —
*"a parent can judge well because it wrote the brief"* — so a badly-briefed child is a
child that cannot be judged well either. Mining serves the goal. The token savings are a
side effect the design is allowed to enjoy and does not optimize for. (The related
objection — *"if you would need to read a conversation to know whether work is good, the
task was delegated wrong"*, §4 — does not bite: mining reads a conversation to **write**
briefs, not to **judge** artifacts.)

**3. "The opt-out is two modes behind a flag, and this record deletes distinctions rather
than configuring them."** VERIFIED, PHILOSOPHY §5: *"Two modes behind a flag is usually
one mode plus a decision nobody made"*; *"A field you set is machinery."*

**Rejected — the objection does not bite, and an earlier draft of this document was wrong
to half-concede it.** PHILOSOPHY §5 kills *"a field you set"* and *"two modes behind a
flag."* **There is no field and no flag here.** The draft's clause is *"if they say they'd
rather drive the workers themselves, do that — the seat is theirs to give"*: a session
**obeying a human instruction**, which requires no configuration to exist and stores no
state. A human's explicit instruction already overrides doctrine (PHILOSOPHY §6 —
*"an agent is free to do anything to achieve its goal"*, bounded by structure, not
permission); the sentence exists so the human **knows the default is refusable**, which
is the entire job of an onboarding document. A default the human cannot see is a default
they cannot refuse.

**And the opt-out is an operator decision, not a scout's addition:** VERIFIED,
`.swarm/journal/operator.md` — *"P2=coordinator-layer default **w/ opt-out**."* It is a
term of the brief. It ships as an instruction the session obeys, never as state. (This
document's own graveyard scout advised cutting it outright on §5 grounds, quoting the very
journal line that specifies it — an object lesson in how a corpse-hunt can find a corpse
that isn't there. The philosophy kills *machinery*; it does not kill *the human's
authority to say no*.)

**4. "You are reversing a decision this project already shipped deliberately."** VERIFIED
— commit `328cd56`, *"README: the optional coordinator posture"*, whose body says it
*"Documents (never applies)"* a per-project `CLAUDE.md` one-liner, and whose README text
reads: *"This is optional and per-project — the installer never touches your CLAUDE.md."*

**A real collision, and the distinction is genuine but narrow — I state both rather than
lean on either.** What `328cd56` made opt-in is *coordinate-by-default **without any
trigger phrase*** — i.e. should **every** session in a project coordinate, **even when
nobody asked for a swarm?** That is a question about sessions that never invoked the
skill. This proposal governs what happens **once the skill has already fired** — the user
*did* ask for a swarm. Different questions, and the answer "yes, coordinate" to the second
does not imply "yes" to the first. **But the honest accounting is this:** WATCHLIST #7
says *"any addition that cannot point to a WATCHLIST entry whose trigger fired"* gets
reverted, and the trigger I am pointing at is **the operator's own observation of two real
adoption failures** — not a measured audit. No document in this repo quantifies the human's
hand-management burden. That observation is the entire evidentiary basis for the default,
and I will not oversell it as more.

**5. "A coordinator layer by default is anticipatory structure, and SPAN says split under
pressure, never in anticipation."** VERIFIED, `SPAN.md:206-215`: *"Depth is a cost, not a
virtue… the shallowest tree that passes the span test. **Split under pressure, never in
anticipation** … A middle layer that only forwards… is structure lying about work."*

**It adds no layer, and this is the load-bearing reply.** *In place* means the node count
is **unchanged**: the human's session exists either way, and the only question is whether
it delegates or grinds. There is no new rung, no forwarder, no hop of briefing fidelity —
which is also precisely why the design refuses a *separate spawned coordinator pane* (§3c),
because **that** version would be the anticipatory layer SPAN condemns. A is about the
**posture of a node that already exists**. If a reader cannot hold that line reading the
draft in §4, the draft is badly worded and should be fixed — not shipped.

**6. "The overseer node was killed as 'the nag reborn.'"** VERIFIED, `SPAN.md:231-234`.
**Distinguishable, and the epitaph draws the distinction itself:** what was killed is *"a
node whose job is other nodes' **behavior**"* — a supervisor of conduct, doing no work of
its own — and the same sentence blesses the alternative: *"parents judging tree shape **is**
the distributed overseer."* The in-place coordinator's job is **the goal**: it writes
briefs, judges artifacts, synthesizes, and reports. It is not a new node at all.

**7. "The doctrine cannot reach the session that never fires the skill."** Raised by the
adversarial review, and **it is right — I am naming it as out of scope rather than
letting the next reader think it was solved.**

Everything in this document governs what happens **once `/swarm` has fired**. But the
deeper form of pitfall 1 is a session that **should** have fired it and never did: the
skill's own description triggers on *"a project with swarm available… handed any goal
that decomposes"* (VERIFIED, `skill/SKILL.md:3`) — and an hour-deep doer session was
handed its goal **an hour ago**, before it had decomposed into anything. **Nothing
re-evaluates.** The doctrine makes the *fired* case better and does nothing for the
*never-fired* case.

I am not proposing a fix, and the reason is a real one rather than fatigue: every
mechanism that suggests itself here — a periodic "should this be a swarm?" check, a
trigger on session length, a hook that watches for decomposable work — is a **guardrail**
whose job is another node's behavior, and this repo has killed that shape twice
(PHILOSOPHY §2, *incentives over guardrails*; SPAN §4, *the overseer is the nag reborn*).
The honest statement is: **this design improves the first five minutes after `/swarm`, and
minute sixty of a session that never typed it remains open.** If it turns out to be the
dominant failure in the field, it deserves its own document — and its first question
should be whether the trigger, not the doctrine, is what is wrong.

---

## 7. Cost

**Concepts: zero.** WORLD.md stays at nine. Nothing here is a fact a file must witness:
the stance is witnessed by what the session *does* (does it hold the tree?), which is
exactly what §5's collector reads off `agents/*.json`.

**Verbs: zero.** The four verbs stand. Both moves are `spawn` + `send` + prose.

**State: zero.** No flag, no mode, no field, no file.

**Helper: none.** Refused on evidence (§2), with the observation that would earn it
recorded (§5).

**Text — the only real cost, and it is not nothing:**

MEASURED (I ran `wc -c` on the file and on the replacement paragraph, rather than
estimating — an unmeasured cost claim has no business in a document that demands
measured claims):

| | before | after | delta |
|---|---|---|---|
| `skill/SKILL.md` — **loaded on every fire** | 106 lines / 6,809 bytes | 122 lines / 7,833 bytes | **+16 lines, +1,024 bytes, +15.0%** |
| — the two inline stances | — | 865 bytes | (all-inline draft's block: 1,646 → **−47%**) |
| — the pointer clause | — | 156 bytes | one clause on an existing line |
| `skill/references/COORDINATING.md` — **0 bytes of context unless opened** | — | 117 lines / 6,809 bytes | new file |
| the rejected all-inline draft | 106 / 6,809 | 125 / 8,140 | +1,331 bytes, +19.5% |
| the opening paragraph | untouched (the rejected draft rewrote it) | untouched | 0 |
| numbered doctrine (1–5) | untouched | untouched | 0 |
| operator-seat section | untouched | untouched | 0 |

`spawn_header()` is **not touched** — and that is a deliberate scope call, not an
oversight: both pitfalls are failures of the **root session**, which never reads the
spawn header, and every spawned agent already carries delegate-by-default and the span
test. Adding mine-first to the header would push doctrine at 100% of agents to fix a
problem that occurs at exactly one node. **WORLD.md is not touched:** it is the contract
*between agents*; this is *how the human's session enters the tree*.

**The honest liability, and it survived the split.** SKILL.md is the one document the
human's session actually reads, and every line in it is load-bearing. The operator
refused +19.5%; the split brings it to **+15.0%**, and I will not dress that up as more
than it is — **it is a 4.5-point cut on the number that was objected to, not an order of
magnitude.** The reason it cannot go lower is stated plainly in §4c: there was never any
depth *inside* SKILL.md to extract (the rejected draft was one oversized paragraph, not a
buried manual), so the split's real work was **cutting the doctrine paragraph 47%**, and
what remains — 865 bytes — is the set of clauses on which §5's falsifiers collect. A
doctrine whose falsifier cannot be collected is one this repo does not ship.

Where it could be cut, in the order I would cut it:
1. **The span/topology reconciliation clause** (*"Doctrine 5's '~3' is a span…"*, ~127
   bytes) — and the right way to take it is to **reword doctrine 5's "default ~3"** so the
   file no longer carries two numbers, rather than deleting the clause that reconciles
   them. (§7 of the first draft called this line "the most cuttable"; the split's
   adversarial review reversed that, and I agree — as written it is the cheapest defence
   of Claim 1 that exists.)
2. **Nothing else, without losing a falsifier.** The journal destination is what makes
   mine-first collectable at all (§5); the two forbidden moves are what let a cold session
   fail the test and know it; the decline-journaling clause is what §5 has always collected
   on and no earlier draft supplied; the opt-out is an operator decision (§6.3).

WATCHLIST #7 (scope creep) is the entry that would fire if this document's *successors*
keep adding to SKILL.md — though note #7 is scoped to *"the new tool growing verbs,
flags, fields, or states"* (VERIFIED, `WATCHLIST.md:106`), and this addition has none of
the four. It is prose, and prose is the one thing this repo's philosophy says to try
first.

</content>
