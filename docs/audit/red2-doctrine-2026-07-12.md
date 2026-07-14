# RED2 / DOCTRINE — attacks D, E, F on `OPERATOR-STRUCTURE.md`

> SUPERSEDED by whatever final OPERATOR-STRUCTURE.md revision incorporated its fixes; kept for the record (executed-probe evidence — pane-id durability tests, herdr session.json decode — behind those corrections).

**Author:** `red2-doctrine`, for `structure-red2`. 2026-07-12.
**Under review:** `docs/design/OPERATOR-STRUCTURE.md` (+ its `-FIX`, `-RED`, `-GRAVE` children).

**Which code each finding applies to.** My parent warned mid-run that `git stash@{0}` is a
**superseded draft** — the `is_agent()` hook gate and the bare `sender = my_name()` were both
found and fixed by `structure-mech` (`OPERATOR-STRUCTURE-FIX.md` §7g). **That correction does
not touch D, E, or F.** The three hunks my attacks exercise — `root_name()`, `claim_root_name()`,
and the `is_dead` guard — are **byte-identical in both versions**. Every scenario below therefore
holds against stash *and* corrected code. I mark this **BOTH** and do not revisit it.

**Evidence rule I held myself to:** every claim cites a file and line I read, or pastes the
output of a command I ran. **Two of my most promising attacks failed, and I say so** — §D.1 and
§D.3 below are written up as failures, because a manufactured hit is worse than useless.

**Verdicts up front:**

| attack | verdict |
|---|---|
| **D** — pane reuse / identity | **WOUNDS IT.** The foundation holds (my kill failed). Two real defects survive: two root nodes in one repo, and silent journal + child adoption on pane reuse. |
| **E** — "first swarm" witnessed by a file | **KILLS IT.** The witness is unsound, and §4e's VERIFIED evidence proves a fact about the *wrong repository*. Recommend the operator's own stated fallback: **announce-only**. |
| **F** — the span override & the doctrine's necessity | **SURVIVES — but not for the reason the design gives.** The fix fixes the *rendering* of the flat row, not the *attention* it costs. Ship both; rewrite §4b's justification, which cites doctrine about channel *content* to defend a claim about node *count*. |

---

## ATTACK D — PANE REUSE AND IDENTITY

### D.1 — MY KILL ATTEMPT FAILED. Pane ids are durable. Say it plainly.

I went after the foundation. The design asserts (`OPERATOR-STRUCTURE.md:249-250`):

> `"""Keyed on HERDR_PANE_ID, not a file: herdr gives every pane a unique, stable id,`
> `so the pane IS the session's identity."""`

and `OPERATOR-STRUCTURE-FIX.md:610-612` repeats it, and `-FIX.md` §7c tabulates *"restart in the
**same** pane | same name ✅ (the pane id is unchanged)"* — **with no test behind it.** It is an
assertion in a table.

Meanwhile **herdr's own documentation says the opposite.** `~/.claude/skills/herdr/SKILL.md:44`,
verbatim:

> **important: ids can compact when tabs, panes, or workspaces are closed. do not treat them
> as durable ids.** re-read ids from `workspace list`, `tab list`, `pane list`, or create/split
> responses when you need a current id. do not guess that an older `1-3` is still the same pane later.

If herdr recycles pane ids, then a *new* pane can inherit a *dead* pane's id, `root_name()` matches
a record that belongs to someone else, and **the entire seat model has no foundation.** That would
be a kill. So I tested it rather than asserting it.

**Test 1 — do ids recycle on close?** Ran against the live herdr:

```
created pane=w4:p93 tab=w4:t93
closed tab w4:t93
created NEXT pane=w4:p94
>>> NOT recycled (P1=w4:p93 P2=w4:p94)
```

**Test 2 — is the counter persisted, or does it reset on a herdr server restart?**
`~/.config/herdr/session.json`, decoded:

```
workspace id: w4
next_public_pane_number: 293
live mappings (internal -> public): 20
public numbers in use: [1, 98, 100, 162, 180, 189, 195, 206, 215, 229,
                        276, 280, 281, 282, 283, 285, 287, 288, 289, 290]
  pane p8M -> decimal 310      (base-36; the ids are the counter in base 36)
  pane p92 -> decimal 326
  pane p94 -> decimal 328
```

**The allocation counter is monotonic AND persisted to disk.** Closing panes drops entries from
`public_pane_numbers` but never rewinds `next_public_pane_number`. So a herdr server restart does
not reset it either.

**VERDICT ON D.1: MY ATTACK FAILS.** Pane ids are effectively unique-forever on this machine.
The herdr skill's warning is about *renumbering between reads* (don't cache an id and reuse it),
not about *reuse across panes*. The design's "stable" claim is **substantively correct**, even
though it was asserted rather than tested and it directly contradicts herdr's own docs.

**The one thing I could not test, and the design should own:** `herdr session delete <name>`
exists (`herdr session --help`), and `session.json` is the *only* place the counter lives. Whether
deleting a session, or losing that file, rewinds `next_public_pane_number` to 1 — thereby minting
`w4:p1` again into a `.swarm` that still holds a `root-1` claiming `w4:p1` — is **untested**. It
is one command away from being a real collision. **Ask for a one-line test, not a table row.**

### D.2 — TWO PANES, ONE REPO: the human gets TWO top-level nodes. REAL.

The design's entire selling point is `OPERATOR-STRUCTURE.md:195-196`:

> **The human's direct load is one node because that is the only tree the data model admits.**

That is false whenever the human opens a second Claude in a second pane on the same project — a
completely ordinary thing to do. Executed against the patched binary, sandbox `SWARM_DIR`, two
fake pane ids:

```
-- after pane pAAA spawns:
  first-worker   parent=root-1    pane=wX:p478
  root-1         parent=operator  pane=w4:pAAA
-- after pane pBBB spawns in the SAME repo:
  first-worker   parent=root-1    pane=wX:p478
  root-1         parent=operator  pane=w4:pAAA
  root-2         parent=operator  pane=w4:pBBB
  second-worker  parent=root-2    pane=wX:p133

-- swarm ps, as the human in pane pAAA sees it:
operator — no waiting mail
├─ root-1 (you) [live] q=0 idle ?
│  └─ first-worker [live] q=0 idle ?
└─ root-2 [live] q=0 idle ?
   └─ second-worker [live] q=0 idle ?
```

**The human's `ps` shows two top-level nodes.** `-FIX.md` §7c lists this in its comparison table
as a **win** (*"two concurrent root sessions | different panes → `root-1` and `root-2`. **No
sharing.** ✅"*) — and it *is* a win against the `root.id` alternative, which would have had both
sessions fighting over one identity. But it is scored against the wrong baseline. Against **the
design's own promise** — "one node" — it is a miss.

**Is it worse than today?** No. **VERIFIED** by running the same scenario on unpatched `bin/swarm`:
today both panes' children write `parent=operator`, so the human sees N workers flat. Two root
nodes is strictly better than eight workers. **So this WOUNDS the design's rhetoric, not its
value.** The honest sentence is *"the human's direct load is one node **per session they have
open**"* — which is a different and much weaker claim than §0 and §3a make, and it should be
written that way.

### D.3 — THE `cd`-TO-A-DIFFERENT-REPO CASE. My best-looking lead, and it is NOT the fix's bug.

The brief asked me to chase this as the killer. I chased it. **It is real, and it is pre-existing,
and the fix neither causes nor worsens it.** Reporting the failure rather than dressing it up.

**Case (a) — same pane, two repos, no `SWARM_DIR`: BENIGN.** Executed:

```
repoA/.swarm/agents:
  a-worker   parent=root-1    pane=wX:p138  cwd=repoA
  root-1     parent=operator  pane=w4:p8M   cwd=repoA
repoB/.swarm/agents:
  b-worker   parent=root-1    pane=wX:p416  cwd=repoB
  root-1     parent=operator  pane=w4:p8M   cwd=repoB
repoA UNCHANGED? yes
```

Two fully independent `.swarm/` dirs, each with its own well-formed `root-1`, each nesting its own
worker. A record from repo A is **never** read while CWD is repo B, because `root_dir()`
(`bin/swarm:59-60`) resolves `.swarm` per-CWD and `load_agents(root)` only ever reads that one
directory. **The design is right; my hypothesis was wrong.**

**Case (b) — `SWARM_DIR` set, human `cd`s to another repo: contamination, but NOT the fix's.**

```
PATCHED:    rX/.swarm: root-1  parent=operator  cwd=rX
                       x1      parent=root-1    cwd=rX
                       y1      parent=root-1    cwd=rY     <-- written into rX!
            rY/.swarm: does not exist
```

`y1` — a worker for repo Y — lands in **repo X's** `.swarm`, adopted by X's `root-1`. But I ran
the control, and this is the part that kills my own attack:

```
UNPATCHED (HEAD, no fix):
            uX/.swarm: ux1  parent=operator  cwd=uX
                       uy1  parent=operator  cwd=uY     <-- SAME BLEED
            uY/.swarm: does not exist
```

**Identical on unpatched code.** `SWARM_DIR` overriding CWD is a pre-existing property of
`root_dir()`, not something `root_name()` introduces. **VERDICT: not a finding against this
design.** (It is arguably a finding against `swarm`, and worth a separate ticket — an env var
that silently redirects a spawn into another project's tree is a foot-gun — but it is not
`OPERATOR-STRUCTURE`'s to answer for, and I will not inflate my report by pretending it is.)

### D.4 — PANE REUSE: a new conversation silently adopts a predecessor's journal AND its children.

This is the one the design predicted and blessed. It reproduces exactly. Executed: session ONE
spawns `old-work`; a **new, unrelated** session in the same pane spawns `new-work`:

```
  new-work   parent=root-1
  old-work   parent=root-1
  root-1     parent=operator

-- root-1 journal after session TWO (ONE root-session entry; session TWO wrote nothing):
# journal of root-1
## 2026-07-12 16:28:54Z -- root session
The human's own session. Parent: operator (the mailbox).

-- swarm ps, as session TWO sees it:
operator — no waiting mail
└─ root-1 (you) [live] q=0 idle ?
   ├─ new-work [live] q=0 idle ?
   └─ old-work [live] q=0 idle ?
```

**Session TWO is marked `(you)` and inherits session ONE's child as its own.** It did not spawn
`old-work`, has no memory of it, and cannot judge its work — but `ps` tells it that it owns it,
and the doctrine tells it to reconcile the tree it owns.

**Is it a feature or a data-integrity bug?** The design's answer (`:271-276`):

> **The residual edge, kept and named rather than hidden:** a *new* session started in the
> *same pane* inherits `root-1`'s name and journal. **I judge this correct, not a bug** — the
> same pane is the same seat, and the journal is the seat's continuity. That is precisely the
> model `skill/SKILL.md` already ships for the operator seat…

**I checked the SKILL.md citation, and it is HONEST — the design is not smuggling anything.**
`git show origin/main:skill/SKILL.md`, lines 65-71:

> ## The operator seat
>
> A session acting for the human at the root — reading the operator mailbox, dispatching,
> judging — is a **hand** on the operator seat. The seat is the standing thing: one journal
> (`.swarm/journal/operator.md`), one mailbox, one set of open loops. **Hands come and go**,
> in sequence or in parallel; everything below is convention in that journal, not tool state.

Grepping every occurrence of `seat`/`hand` in that file (lines 62, 65, 68, 73-98) confirms it:
**the seat model is asserted ONLY about the human's own root session, and never about a spawned
agent.** So the brief's suspicion — *"if the seat model is only ever asserted for spawned agents,
extending it to the human's chat window is a new claim wearing an old one's clothes"* — **does not
land. It is the reverse.** The seat model was *always* about the human's window. The design is
citing it correctly. I record this because my brief invited me to find a smuggle and there isn't one.

**But the argument still fails, on a distinction the design never draws — and this is the finding:**

The shipped seat model says *hands come and go* **for a single standing purpose**: one mailbox, one
set of open loops, one project's continuity. It presumes the successor hand is **taking over the
same work** — SKILL.md:86 is explicit: *"A dispatch entry with no verdict entry is an **open loop**;
open loops belong to the SEAT, and any hand may adopt them."* The whole convention exists so that a
successor **deliberately adopts** the open loops after **reading** the journal (SKILL.md:73-77:
*"Take the seat before acting… Then look before touching: `swarm ps`, the operator journal…"*).

**The fix's inheritance has neither property.** It is:
- **Silent.** No seat-take entry, no read, no adoption. `root_name()` is a pure lookup; the successor
  is `root-1` *before it has read anything*.
- **Unconditional on the work.** The seat convention binds a hand to *the project's* open loops. The
  pane binds a session to *whatever the pane last did* — and a terminal pane is not a project. The
  human who closes a Claude, `cd`s nowhere, and starts a new one on a **different task in the same
  repo** gets the previous task's children handed to them, marked `(you)`.

The design's own strongest paragraph is the one that should have caught this (`:147-151`, quoting
`structure-red`): *"**The root session is not a durable node.** It is the human's chat window. It
compacts. It gets `/clear`ed. It gets closed when the laptop sleeps."* **Exactly.** And the fix's
response is to make the *pane* — a thing even less durable in meaning, since its contents change
identity every time the human starts a new conversation — the sole key of a durable name. It binds a
**durable record** to an **ephemeral occupant** and calls the binding continuity.

**The 55 KB question.** `.swarm/journal/operator.md` is the human's own working notes. Under the fix,
that convention is **deleted** (§6a: *"Give it one and the convention is redundant"*) and replaced by
`journal/root-1.md`, which a fresh unrelated session now writes into by default. That is a
data-integrity regression in exactly the artifact this whole system says is load-bearing
(`WORLD.md:9`: an agent is *"a Claude session… with a name, a **parent**, and a **journal**"*).

**VERDICT D: WOUNDS IT.** The foundation is sound (D.1), the cross-repo attack fails (D.3), the
SKILL.md citation is honest — but D.2 falsifies the "one node" promise in the ordinary two-pane case,
and D.4 is a real silent-adoption bug that the design has *ruled correct by analogy to a convention
whose two safety properties (deliberate adoption, project-scoped loops) the fix does not preserve*.

**Cheapest repairs, if my parent wants one:** (i) make the inheritance **non-silent** — on a
`root_name()` hit, `claim_root_name` is skipped, so nothing writes; a two-line "resumed root-1 in
this pane" journal append restores the seat-take breadcrumb; or (ii) key on `HERDR_PANE_ID` **plus**
the Claude session id if one is in the env, so a new conversation is a new root. Neither is free, and
(i) is 3 lines.

---

## ATTACK E — "FIRST SWARM" WITNESSED BY A FILE

**VERDICT: KILLS IT.** The witness is unsound, and the design's `VERIFIED` block proves a fact about
the **wrong repository**. Per the operator's own instruction — *"if genuinely nothing witnesses it,
say so and default to announce-only rather than build state"* — **the answer he asked for is:
announce-only.**

### E.1 — §4e's VERIFIED evidence is a fact about swarm's own repo, not about user projects.

`OPERATOR-STRUCTURE.md:410-417`:

> **Something does witness it, exactly, and it costs zero state.** VERIFIED:
> ```
> $ git check-ignore -v .swarm/agents   →  .gitignore:7:.swarm/
> $ git ls-files .swarm                 →  (empty — untracked)
> ```
> **`.swarm/` is gitignored and untracked, so a fresh clone never carries one.**

**I reran both commands. They are true — and they are true of this repository only.**

```
$ git check-ignore -v .swarm          →  .gitignore:7:.swarm/	.swarm
$ git ls-files .swarm                 →  (count: 0)
```

**Now read the `.gitignore` the design is citing** — the full file, `/Users/vadrsa/git/swarm/.gitignore`:

```
1  # local backups, never part of the package
2  .backups/
3  *.bak
4
5  # swarm runtime state lives in each project's .swarm/, not here — but ignore any
6  # that ends up in the repo dir just in case
7  .swarm/
```

**Lines 5-6 say, in the repo's own words, that this rule is not about user projects at all.** It
exists because swarm is *self-hosted* — the swarm repo runs swarms on itself, so its `.swarm/`
lands in its own checkout. `.swarm/` state *"lives in each project's `.swarm/`, **not here**"*.
The inference `.swarm/` is gitignored **⇒ a fresh clone never carries one** generalizes from
swarm's own hygiene rule to every project in the world. It does not hold.

### E.2 — The package ships NO `.gitignore` rule to user projects. It ships an INSTRUCTION.

This is the part that settles it. **VERIFIED**, `install.sh:98-99` — the last thing a new user is
told:

```
echo "  • The tool writes state into a .swarm/ dir in your project — add it to"
echo "    that project's .gitignore if you don't want it committed."
```

and `README.md:65-67`:

> State lives in your project's `.swarm/` directory (queues, journals, one event fact per agent).
> It is a paper trail, safe to delete between runs — **add `.swarm/` to that project's `.gitignore`.**

**"add it… if you don't want it committed"** is an instruction to a human, conditional on their
preference. `git ls-files | grep -i gitignore` returns exactly one file — swarm's own. **Nothing in
the package writes an ignore rule into a user's project.** So a user who ignores the install hint —
or who deliberately commits `.swarm/` as a paper trail, which the README calls it and which is a
perfectly reasonable thing to want — ships `agents/*.json` into git.

**The design already names this failure mode and dismisses it** (`:430-434`):

> - **A repo commits `.swarm/` anyway** (against the shipped `.gitignore`) → a first-time user on
>   that clone gets announce-only, and misses the lesson. **This is the only real miss, it requires
>   deliberately un-ignoring runtime state**, and its cost is a missed lesson, not a wrong tree.

**Two errors in three lines.** (1) *"against the shipped `.gitignore`"* — **there is no shipped
`.gitignore`.** The one it means is swarm's own, which no user inherits. (2) *"it requires
deliberately un-ignoring runtime state"* — **it requires nothing.** It is the **default** for any
user who did not read line 99 of an install script's output. The failure mode is not an act of
deliberate perversity; it is **inaction**.

And the population it hits is precisely the population the pedagogy is *for*: **every teammate who
clones a repo where someone else already swarmed.** That is failure mode (d) in my brief, and it is
not an edge — on any team it is the *majority* of first-time users. The one moment the design says
the lesson is "load-bearing" (`:387`) is the exact moment it is most likely to be skipped.

### E.3 — What actually creates `.swarm/` first. It is not a spawn.

The design leans on laziness (`:192-195`: *"A human who only runs `swarm ps` creates no node…
Nothing appears until the session actually becomes a parent"*). **That is true of `ps`, and I
confirmed it. It is not true of `send`.** Executed in a clean dir with the patched binary:

```
  after 'swarm ps    ' -> .swarm exists? no
  after 'swarm world ' -> .swarm exists? no
  after 'swarm send operator' -> .swarm exists? YES
      .swarm/queue/operator/1783873841153-.json
```

`swarm send operator` creates `.swarm/` — **with no `agents/` directory at all.** This does not
break §4e's *stated* rule (which reads `.swarm/agents/`, `:423`) but it breaks the rule as it is
*written*: **`:423` says "if `.swarm/agents/` is empty **or absent**, confirm"**, while **`:419`
states the witness as "`.swarm/agents/` holding no record ⇒ never run a swarm"** and **`:417`
argues from "`.swarm/` is gitignored"**. Three different predicates in five lines. A doctrine that
a model must execute with an `ls` cannot be three predicates.

### E.4 — A FAILED spawn still witnesses "a swarm ran here".

Failure mode (c). I forced `herdr tab create` to fail — the spawn dies *after* `claim_root_name()`:

```
swarm: herdr tab create failed
  .swarm tree after the FAILED spawn:
    .swarm/journal/aborted.md
    .swarm/journal/root-1.md
    .swarm/settings/aborted.{task,launch.sh,json}
    .swarm/agents/root-1.json          <-- the witness fires
  agents/*.json count: 1
```

**Zero agents ever ran, and `.swarm/agents/` is non-empty.** The design calls this benign
(`:435-436`: *"An aborted prior run left records → announce-only. Correct: someone has already
spawned here"*) and I **partly agree** — the human did *attempt* a swarm and did see the machinery.
But note what it means: the witness records **attempted**, not **ran**. Combined with E.2, the
witness fires for a user who has never seen a swarm work.

### E.5 — Deletion (failure mode (a)) is the *only* one the design gets right.

`rm -rf .swarm/` → the confirm fires again. Harmless, exactly as `:428-429` says: the cost of a
false confirm is one line. Nothing else survives deletion — journals live inside `.swarm/`
(`bin/swarm:16`: `journal/<name>.md`), so git carries nothing. **This one is sound.**

### E.6 — The verdict, framed as the operator asked for it.

The operator's constraint was: *"'first swarm in a project' must be a fact a file witnesses… if
genuinely nothing witnesses it, **say so and default to announce-only rather than build state.**"*

**Nothing witnesses it.** `.swarm/agents/` witnesses **"someone has spawned in this working
directory, on this machine, since the last `rm -rf`"** — which is *neither necessary nor sufficient*
for **"this human has never seen a swarm"**:

| the fact the doctrine needs | what `.swarm/agents/` actually says |
|---|---|
| **this human** is new to swarms | says nothing about *who*; a teammate's clone with a committed `.swarm/` reads as "not first" for a brand-new user |
| this human has **seen a swarm run** | fires on a spawn that **failed** (E.4) |
| **first time in this project** | fires per **working directory**; the same human in a second checkout of the same repo gets the lesson again |

**The design's own escape hatch is the right answer, and it is already written into §4e:** *"a false
**announce** costs a lesson… Neither costs a bad tree"* (`:438-440`), *"because correctness is
carried by the fix, not by the confirm"* (`:433-434`). **Both halves of that are true.** So take the
consequence the design flinched from: if the confirm is not load-bearing for correctness, and its
witness cannot identify the population it exists to teach, **the confirm should be cut and the
announce kept — universally, with no file predicate at all.** That is fewer lines, zero state, no
`ls`, and it is what the operator pre-authorized.

**If the operator still wants first-contact pedagogy, it belongs where first contact actually
happens: `install.sh` already prints a "Done." block (`:95-99`). Teach there.** That *is* a fact a
file witnesses — the install ran — and it costs zero lines of always-loaded skill text.

**VERDICT E: KILLS IT.** Not the doctrine — the *witness*. Recommend **announce-only**.

---

## ATTACK F — THE SPAN OVERRIDE, AND WHETHER THE DOCTRINE STILL EARNS ITS BYTES

### F.1 — Is the SPAN override honest, or special pleading? **Honest in form; unsound in its citations.**

The design does not hide the override (`:309-330`), and that is to its credit. It states SPAN
correctly. **VERIFIED**, `docs/design/SPAN.md:210-212`:

> So the doctrine's direction is: **the shallowest tree that passes the span test. Split under
> pressure, never in anticipation;** absorb eagerly on the way down.

and STRUCTURE's measurement, **VERIFIED**, `docs/design/STRUCTURE.md:85-96`:

> ### 2a. Load (SPAN's bet) — REJECTED by the record
> SPAN.md §1 argued attention-pressure at a node should force a coordinator split. **MEASURED,
> three times, zero for three**… **Structure in this swarm has never once come from momentary
> attention pressure.**

So: **the record contains zero coordinators summoned by load, across three floods designed to
summon one, and the design makes one the default.** It says so itself (`:320-322`). Declaring an
override is the honest move, and I will not score it as dishonesty.

**But the override's *ground* does not survive checking.** It rests on two citations, and I read both.

**Ground 1** (`:324-329`): *"You cannot un-flood a human's window after the fact… The human cannot
un-read three reports, un-manage three panes, or un-spend the hour."* — This is a real asymmetry and
I accept it as **REASONED**. It is the strongest sentence in §4b.

**Ground 2** (`:331-336`): *"PHILOSOPHY §9 records the operator's second instruction… and notes that
question **created the chief-of-staff**. The coordinator layer was never killed. It was **founding**."*

**I read PHILOSOPHY §9. It does not say what §4b needs it to say.** `docs/PHILOSOPHY.md:270-280`:

> ## 9. Keep the operator's channel clean
> > **"Since this session is my channel of communication, I don't want it polluted by **you
> > validating work that can be done by a subagent**. What other options do we have to keep this
> > session clean?"** — root L31
>
> That question created the chief-of-staff (ASK #2).

**The complaint is about what the session was *doing in the channel* — validating work itself instead
of delegating it.** The remedy it produced is **delegate-by-default**, which is doctrine 1 and is
**not under review**. `docs/PHILOSOPHY.md:300-302` makes the section's actual test explicit:

> **The test this gives you:** anything reaching the operator must be **readable by someone who has
> not been in the room**. No internal codenames, no thread letters, no design-version numbers.

**That is a test on the CONTENT of what reaches the human. It is not a test on the NUMBER of nodes
in a tree.** §4b cites a doctrine about channel *quality* to justify a default about tree *shape*.
The chief-of-staff was founded to stop the human's session doing the work; it was not founded to
interpose a node between the human and a count of children.

**VERDICT F.1: the override is honestly *declared* and half-honestly *grounded*.** Ground 1 stands.
Ground 2 is a citation that does not carry its claim, and it is the one doing the rhetorical work
("*founding*"). **If §4b ships, it must ship on ground 1 alone** — and ground 1, standing alone, is
a REASONED bet against a 3-for-3 MEASURED record, which is a much weaker thing to write and should
be written as such.

### F.2 — THE BIG ONE. Steel-manning "ship the fix alone, delete the doctrine."

My parent asked for this as hard as I can make it. Here it is, and it is strong.

**(i) The data model already does the doctrine's job.** The design's own §3a (`:194-196`):

> **Unrepresentable, not discouraged.** After this, a root session's children record `parent=root-1`.
> `human → flat row of N workers` is not *frowned upon*; **it cannot be written.**

and §3a (`:197-199`):

> **It deletes doctrine.** The shipped stance's whole burden — *"do not hand the human a row of
> workers to drive"* — is now carried by the file format. **Prose that a mechanism makes true is
> prose you can cut.**

**The design argues for its own doctrine's deletion, in the design.**

**(ii) The doctrine must be skippable, so it reduces to "think about it."** §4c (`:347-352`) adds a
skip clause: *"If the work is a handful of independent leaves with nothing to reconcile, **say that
and spawn them directly**."* A default that any session may decline on its own judgment, with a
one-line rationale, is not a default. It is a prompt to reflect. **Is "reflect on your structure"
worth ~180 bytes of always-loaded context** (§7: *"≈ +180 B on a 7,833 B file (+2.3%)"*) **on every
single swarm invocation, forever?**

**(iii) The design concedes the point in advance.** Its own F-DOCTRINE falsifier (`:550-553`):

> **HONEST WEAKNESS, pre-registered:** after the fix, **the shape claim is no longer a test of the
> doctrine at all** — the files can't record a flat row whatever the session does. So F-DOCTRINE
> tests *only* whether the announce happens. **A doctrine whose only remaining job is speech is a
> doctrine you should be willing to cut if it doesn't happen.**

**(iv) It is dead text on 2 of 3 real goals.** §8 (`:697-700`), **MEASURED**:

> handed genuinely parallelizable 3-part goals with **every documented trigger condition met**…
> the swarm skill **never loaded** — 2/2. Both sessions fanned out to **built-in Task subagents**
> instead… The skill loaded reliably **only** on the literal phrase *"start a swarm."*

**A doctrine inside a skill that does not fire is bytes that cost context on the runs where it loads
and does nothing on the runs where it doesn't.**

**That is a genuinely strong case. Four independent grounds, three of them the design's own words.
If I stopped here I would recommend: ship the ~26-line fix alone.**

### F.3 — THE CRUX. And it flips the verdict. **The fix solves the RENDERING of the flat row. It does not solve the ATTENTION.**

My brief told me to chase this and said it might be the strongest surviving case for the doctrine or
the strongest attack on the fix's sufficiency. **It is both, and I have the output.**

**The question:** after the fix, can a session still spawn 8 flat workers under `root-1` — and does
the human still get flooded?

**Executed.** Patched binary, sandbox, one root session, eight spawns:

```
operator — no waiting mail
└─ root-1 (you) [live] q=0 idle ?
   ├─ w1 [live] q=0 idle ?
   ├─ w2 [live] q=0 idle ?
   ├─ w3 [live] q=0 idle ?
   ├─ w4 [live] q=0 idle ?
   ├─ w5 [live] q=0 idle ?
   ├─ w6 [live] q=0 idle ?
   ├─ w7 [live] q=0 idle ?
   └─ w8 [live] q=0 idle ?
```

**The flat row is not abolished. It is indented.** The eight workers exist, occupy eight herdr panes,
and are driven by the session the human is sitting in — which is to say, **by the human**. `ps` draws
one node at the top. The human's *life* has eight agents in it.

**And now the part that decides everything.** I had three of the eight report:

```
-- 3 of 8 workers send to the operator mailbox --
operator queue:
    1783873897119-w1.json
    1783873897160-w2.json
    1783873897203-w3.json

operator — 3 message(s) waiting for the human (queue/operator/):
    from w1, 0s ago
    from w2, 0s ago
```

**Every worker can mail the human directly, and the fix does not touch that.** It is not an accident
or an oversight — **it is a contract promise.** `WORLD.md:57-59`, **VERIFIED**:

> - **The operator is a mailbox, not a node.** Messages to `operator` wait until the human looks;
>   `ps` shows them waiting. Nothing pushes to the human, and **nothing ever refuses a message to
>   the operator.**

and `bin/swarm:165-166` — `relation()` grants *any* sender the operator as a recipient, with no
tree-position check:

```python
def relation(sender, recipient, parent_of):
    if sender == "operator":
        return "the OPERATOR (the human at the root)"
```

`cmd_send` refuses exactly one recipient class after the fix — `root-*` (the patched file's
`:1045-1048`, §3d's `+3 lines`) — and `operator` is explicitly always allowed, in both versions.

**So: what is "the human's direct load"?** Not the `ps` indentation. **SPAN.md:140-142** — the
sentence the whole doctrine descends from — defines it, **VERIFIED**:

> The operator's span is theirs to declare and yours to protect: **never let the tree press more
> direct attention on the operator than they asked for.**

**Attention.** Not nodes. And attention arrives through `queue/operator/` and through the eight panes
the human has to look at — **neither of which the fix narrows by one byte.**

**This is the answer to my parent's question, and it is not the one the fix's §0 promises.** §0
(`:34-37`) claims:

> **`human → flat row of workers` becomes unrepresentable.** … The human's direct load is one node
> because that is the only tree the data model admits.

**The row is representable. It is one indent deeper, and every member of it can still ring the
human's mailbox.** The fix makes the *tree render* correctly. It makes `parent=operator` stop being
a lie. Those are real and worth shipping — the tree is now *inspectable*, and `eff_parent` no longer
reattaches orphans to the human. But **"the human's direct load is one node" is a claim about a
picture, not about a person's day.**

### F.4 — Therefore the doctrine's remaining job is real, and it is the only thing that does it.

Take F.2's four grounds and re-read them against F.3:

- **(i) "the data model makes it unrepresentable"** — **FALSE, as executed.** The data model makes
  *one particular parent string* unrepresentable. Eight workers hanging off the human's own session,
  eight panes, eight mailbox-capable reporters: fully representable, and exactly what an
  undoctrined session will produce, because §8's field record shows sessions fan out to whatever is
  in front of them. **This is the argument the "ship the fix alone" case rests on, and the probe
  kills it.**
- **(ii) "the skip clause reduces it to 'think about it'"** — **stands, but that is now the point.**
  After F.3, "think about your top layer" is the *only* mechanism in the system that bounds the
  human's attention, because no file format can. The design half-sees this at `:354-357` (*"after
  the fix, spawning the leaves directly no longer produces the flat row"*) — **which is exactly the
  false comfort F.3 refutes.** §4c's escape hatch is safe *only* if the leaves really are few. It
  says nothing about **how many**.
- **(iii) "the design concedes the shape claim isn't a test"** — **stands, and is correct.** But it
  concedes the wrong thing. F-DOCTRINE should not have been narrowed to "did it announce". It should
  have been: **"how many agents did the human end up with direct visibility of, and how many pieces
  of mail did they get?"** That is collectable — `ls .swarm/queue/operator/ | wc -l` and a count of
  `root-*`'s children — and it is the falsifier this design is missing.
- **(iv) "the skill doesn't fire on 2/3 goals"** — **stands, and is the strongest of the four.** But
  it argues for **fixing the trigger**, not for deleting the payload. The design says so itself
  (`:717`: *"this needs its own investigation, and it should probably outrank this one"*). Deleting
  the doctrine because the skill misfires is treating the symptom.

### F.5 — What the announce still buys that the data model cannot.

Three things, all real:

1. **It is the only bound on the human's attention that exists anywhere in the system.** Not the
   tool (`WORLD.md:59` guarantees the opposite: the mailbox never refuses). Not the file format
   (F.3). Only prose. **SPAN.md:43-45** says this outright, **VERIFIED**: *"The operator names their
   own span — this operator says ~3 — and **nothing in the tool today respects, records, or even
   mentions it.**"* The fix does not change that sentence. **Doctrine is the entire mechanism.**
2. **The dismissal pitfall** (`:395-397`): a session cannot *silently* decline to swarm if it must
   name its top layer out loud. The data model cannot compel speech.
3. **It makes the default refusable** (`:398-399`). A human who reads *"I'll run eight workers under
   me"* can say no. A human who reads a `ps` tree with one indented row of eight has already paid.

### F.6 — VERDICT: **SHIP BOTH** — but the doctrine ships on repaired grounds, and the fix ships with a repaired claim.

**SURVIVES.** The steel-man for deleting the doctrine is strong, four-grounded, and — I want to be
precise about this — **it was the position I expected to end at.** It falls to one executed probe:
the flat row is representable one level down, and every worker in it can mail the human. The data
model does not do the doctrine's job; it does a *different* job (making the tree honest and
inspectable), and does it well.

**But my parent should not read this as a vindication, because two things he wrote must change:**

1. **The fix's headline claim is wrong and must be rewritten.** *"`human → flat row of workers`
   becomes unrepresentable"* (`:36`) and *"The human's direct load is one node because that is the
   only tree the data model admits"* (`:195-196`) are **false as executed**. The true claim is
   narrower and still excellent: ***`parent=operator` becomes unwritable, so the tree the tool
   records is the tree that exists, and `ps` stops reattaching a live human's children to a mailbox.***
   Ship that sentence. It is honest and it is worth 26 lines.
2. **§4b's justification must drop the PHILOSOPHY §9 citation** (F.1) and stand on the un-flooding
   asymmetry alone — while noting that STRUCTURE is 3-for-3 against it. And **§4c's comfort
   ("spawning the leaves directly no longer produces the flat row") must be struck**, because F.3
   shows it does.

**The doctrine that survives is not "default one coordinator." It is the sentence SPAN already
wrote and the tool still does not enforce:** *never let the tree press more direct attention on the
operator than they asked for* — where **attention** means panes to watch and mail to read, and where
the count that matters is **agents beneath the human's session**, not nodes in a `ps` render.

**Recommended F-DOCTRINE falsifier, replacing the one at `:539-553`:** after a real multi-part goal
in a root session, collect **(a)** `ls .swarm/queue/operator/ | wc -l` and **(b)** the number of
descendants of `root-*`. **FALSIFIED WHEN** either exceeds the operator's declared span (~3). That
tests the thing the doctrine is actually for, and — unlike the shipped one — **the fix does not make
it un-collectable.**

---

## Summary of every claim, with its evidence class

| # | claim | class | cite |
|---|---|---|---|
| D.1 | herdr pane ids are **not** recycled; the allocation counter is monotonic and persisted | VERIFIED (ran `herdr tab create`/`close`; decoded `session.json`) | `~/.config/herdr/session.json`; `~/.claude/skills/herdr/SKILL.md:44` |
| D.1 | **My kill attempt on the seat model's foundation FAILED.** The design's "stable id" claim is substantively right | VERIFIED | as above |
| D.1 | `herdr session delete` + a lost `session.json` is an **untested** id-rewind path | REASONED | `herdr session --help` |
| D.2 | Two panes in one repo → `root-1` **and** `root-2`; `ps` shows the human two top-level nodes | VERIFIED (executed, output pasted) | `OPERATOR-STRUCTURE.md:195-196` |
| D.3 | **The `cd`-to-another-repo attack FAILS.** Per-CWD `.swarm` is clean; the `SWARM_DIR` bleed is identical on unpatched HEAD | VERIFIED (ran the control) | `bin/swarm:59-60` |
| D.4 | A new session in a reused pane silently inherits `root-1`, its journal, and its predecessor's children, marked `(you)` | VERIFIED (executed) | `OPERATOR-STRUCTURE.md:271-276` |
| D.4 | The SKILL.md seat-model citation is **honest** — the seat model was always about the human's root session, never about spawned agents | VERIFIED | `origin/main:skill/SKILL.md:65-71`, and every `seat`/`hand` hit in that file |
| D.4 | …but the shipped seat convention requires **deliberate adoption after reading**; the fix's inheritance is **silent and pane-scoped, not project-scoped** | VERIFIED + REASONED | `origin/main:skill/SKILL.md:73-77, 86` |
| E.1 | §4e's `git check-ignore` evidence proves a fact about **swarm's own repo**, whose `.gitignore:5-6` says the rule exists for self-hosting | VERIFIED (read the full file) | `.gitignore:1-7` |
| E.2 | The package ships **no** `.gitignore` to user projects — only an instruction the user may ignore | VERIFIED | `install.sh:98-99`; `README.md:65-67`; `git ls-files \| grep gitignore` → one file |
| E.2 | §4e's dismissal (*"requires deliberately un-ignoring runtime state"*) is **false**; it requires inaction | VERIFIED | `OPERATOR-STRUCTURE.md:430-434` |
| E.3 | `swarm send operator` creates `.swarm/` with **no** `agents/` dir; §4e states the predicate three different ways in five lines | VERIFIED (executed) | `OPERATOR-STRUCTURE.md:417, 419, 423` |
| E.4 | A **failed** spawn writes `agents/root-1.json` — the witness fires when zero agents ran | VERIFIED (executed) | — |
| E.6 | **Nothing witnesses "this human's first swarm."** Per the operator's own instruction: **default to announce-only** | REASONED, on the above | operator's constraint, `OPERATOR-STRUCTURE.md:405-408` |
| F.1 | The SPAN override is honestly **declared** | VERIFIED | `SPAN.md:210-212`; `STRUCTURE.md:85-96` |
| F.1 | …but PHILOSOPHY §9 is about the **content** of the channel, not the **count** of nodes. The citation does not carry the claim | VERIFIED (read §9 whole) | `docs/PHILOSOPHY.md:270-302` |
| F.3 | **8 flat workers under `root-1` are fully representable.** The fix indents the row; it does not abolish it | VERIFIED (executed, output pasted) | `OPERATOR-STRUCTURE.md:36, 195-196` |
| F.3 | **Every worker can mail the human.** 3 of 8 filled `queue/operator/` in one second; the contract *guarantees* this | VERIFIED (executed) | `WORLD.md:57-59`; `bin/swarm:165-166`; patched `:1045-1048` |
| F.3 | The thing being protected is **attention**, not tree-drawing | VERIFIED | `SPAN.md:140-142` |
| F.4 | Therefore the "ship the fix alone" steel-man's load-bearing ground (i) is **false**, and the doctrine survives | REASONED, on F.3 | — |
| F.5 | **Nothing in the tool bounds the operator's span.** Doctrine is the entire mechanism | VERIFIED | `SPAN.md:43-45` |
| F.6 | **Ship both** — with the fix's headline claim narrowed and §4b's grounds repaired | REASONED | — |

**What I did not test, stated as the boundary of what I have shown:** every scenario above ran with
a **fake `herdr`** and a **fake `claude`** against a sandbox `SWARM_DIR`. They prove what the *tool*
records and renders. **They prove nothing about what a real model does when handed the doctrine** —
that arm still needs the cold root-session rig (`OPERATOR-STRUCTURE.md:530-533`). The one thing I
checked against the real herdr is the pane-id durability question (D.1), and that is real output
from the live instance, not my rig.
