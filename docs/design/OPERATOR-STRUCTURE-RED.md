# RED — adversarial attack on the operator-structure proposal, before it is written

> SUPERSEDED by OPERATOR-STRUCTURE.md §1, which absorbs its decisive kill (claim C, disproven on source); kept for the record (the review of an earlier proposal, propose-and-confirm, no longer in that form — no live disagreement remains).

**Reviewer:** `structure-red`, serving `operator-structure-scout`. My job is to kill
this proposal. Where it survives, I say so and say why — a red team that only hits is
as useless as one that only agrees.

**Evidence discipline** as elsewhere: **VERIFIED** (I read the line / ran the
command — quoted with a path), **MEASURED** (cites a field-evidence record), **REASONED**
(argument, could be wrong, falsifier named).

**The proposal under attack** (from the operator's dispatch, VERIFIED
`.swarm/journal/operator.md:184`):

> operator designs+manages ONLY its top-level agents; below is invisible; primary act
> before any task = design top layer; DEFAULT ~1 coordinator, grow on proven bottleneck
> only. Enforcement LOCKED = skill doctrine only, strong wording, no gate/tool change.
> Default LOCKED = propose-and-confirm (human one-line confirm before task) — this is
> the external check F1 proved prose lacks; also may dissolve the operator
> name-collision.

---

## BOTTOM LINE, before the five attacks

**Two of the proposal's three load-bearing claims are false on the artifacts, and one
of them is false in a way no wording can repair.**

1. **The premise is withdrawn.** The proposal is justified by "the external check F1
   proved prose lacks." **F1 proved no such thing.** The adversarial review of the
   field evidence — `docs/audit/field-evidence-doctrine-2026-07-12-RED.md`, by `dp-red`,
   which sits **in this repo, unrebutted** — substitutes the verdict **NOT ADJUDICATED**
   for **FIRED**, on four independent grounds (R1, R2, R3, R8). The proposal cites the
   evidence file and appears not to have read its RED. This is not a quibble about
   epistemics: **the entire reason to abandon the shipped doctrine is a finding that
   has been retracted.**

2. **Claim C is false, mechanically, and I can prove it in two lines of source.**
   `bin/swarm:869` — `parent = my_name()`. `bin/swarm:64` — `return
   os.environ.get("SWARM_AGENT_ID") or "operator"`. `cmd_spawn` accepts exactly two
   flags, `--model` and `--cwd` (VERIFIED, `bin/swarm:845-856`): **there is no
   `--parent`.** A root session that proposes "one coordinator named X beneath me," gets
   a human confirm, and spawns X, writes **`parent=operator`** into `agents/X.json` —
   because that is the only value it is capable of writing. **Propose-and-name cannot
   dissolve the name collision, because the collision is not in the model's head. It is
   a hard-coded default in the tool.** With enforcement locked to "no tool change," the
   proposal has locked out the only thing that could work.

3. **The direct contradiction is real but resolvable — and the proposal is on the
   right side of it.** The shipped doctrine's "DO NOT SPAWN A COORDINATOR" and the new
   "spawn one coordinator" are genuinely opposite instructions, and the record does
   *not* cleanly vindicate the shipped one. But — and the proposal has not noticed this
   — **the reconciliation is not available under the enforcement lock either.** See A.

**Verdicts:**

| attack | verdict |
|---|---|
| **A. The direct contradiction** | **WOUNDS IT** — the reversal is defensible, but the proposal has not argued it, and its own new layer *is* a forwarding layer unless one specific thing is true. |
| **B. Does the human-confirm bind?** | **WOUNDS IT** — the confirm is a real external check, better than the proposal's critics will admit; but it checks the *proposal*, never the *spawn*, and F1's own record shows sessions that propose correctly and then cannot execute. |
| **C. Propose-and-name dissolves the collision, no tool change** | **KILLS IT** — false on the source. Two lines. Not arguable. |
| **D. Graveyard / philosophy** | **WOUNDS IT** — the pre-task handshake is not the guardrail shape this repo killed (it survives §2), but DEFAULT ~1 *is* anticipatory structure and contradicts a MEASURED 3-for-3 finding. |
| **E. Onboarding tax** | **SURVIVES, weakly** — the tax is small and the trivial case is self-limiting; the default ~1 is wrong for genuinely parallel work but the doctrine already says "on proven bottleneck." |

---

## A. THE DIRECT CONTRADICTION — is the new proposal the thing the last design explicitly killed?

**Verdict: WOUNDS IT.**

### A1. The contradiction is exact, not a matter of emphasis

The shipped text (VERIFIED, `git show origin/main:skill/SKILL.md`, the second
paragraph):

> **You stay the coordinator, here, in this session.** Do not spawn a coordinator
> and hand it the tree; do not hand the human a row of workers to drive — the human
> manages **one node: you**.

And its reasoning (VERIFIED, `git show origin/main:skill/references/COORDINATING.md`,
"Why the seat is a tenure, not a posture"):

> **In place, with no extra hop.** The alternative — spawn a coordinator agent and
> have the human talk to *that* — adds a layer whose only content is forwarding, and
> **a middle layer that only forwards is structure lying about work.** It also costs
> a hop of briefing fidelity for nothing.

That phrase is a citation. `SPAN.md:206-215` (VERIFIED):

> Depth is a cost, not a virtue… **the shallowest tree that passes the span test.
> Split under pressure, never in anticipation** … A middle layer that only forwards —
> adds no judgment, writes no synthesis — is structure lying about work, and **its
> parent should close it** (the anti-forwarder test: a coordinator's journal must show
> artifact reads and verdicts, not relay logs).

ONBOARDING.md §3c put the same move on its **NOT-list**, by name (VERIFIED,
`docs/design/ONBOARDING.md:238-239`):

> **NOT a separate spawned coordinator pane.** §3a — a forwarding layer, condemned by
> SPAN §3d, and one hop of fidelity loss for zero judgment added.

**So yes: the proposal's central structural move is on the previous design's explicit
kill list, and the previous design shipped, one commit ago, on `origin/main`.** Any
version of this proposal that does not open by saying so is not a design document, it
is an amnesia.

### A2. But the shipped side does not win on the record — it wins on an unexamined premise

Here is where I turn on my own attack. The kill rests on **one factual claim**: that
the spawned coordinator's *only content is forwarding*. Test it against SPAN's own
anti-forwarder test — "a coordinator's journal must show artifact reads and verdicts,
not relay logs."

Under the proposal, the coordinator `X` beneath the root would: write the child briefs,
read the children's artifacts, judge them, close children, restructure the subtree,
synthesize, and hand the root one ranked page. **That is not a relay log. That is the
whole of the coordinator's job as the doctrine defines it.** It passes SPAN's own test.

What the *root session* is left with, under the proposal, is: hold the human's
conversation, hold the goal, judge one child. **That** is closer to a forwarder — and
that is the honest shape of the objection nobody has stated: the proposal does not add
a forwarding layer at the bottom, **it risks turning the root session into one at the
top.**

Which means the shipped doctrine's argument is not wrong so much as *misaimed*. Its
real content is the sentence next to it (VERIFIED, COORDINATING.md):

> The session in front of the human is **already** a Claude session holding the full
> context; making it the coordinator is **free, and adds no node**: the human's session
> exists either way. The only question is whether it delegates or grinds.

**This is the strongest argument in the entire corpus against the proposal, and the
proposal must answer it or die.** The root session exists unconditionally. It holds the
richest context that will ever exist (that is ONBOARDING's own mine-first premise — and
mine-first **passed**, or at least was not falsified). Spawning `X` and handing it the
tree means: paying one hop of briefing fidelity, to move the tree from a node that has
the context to a node that must be told it, **for zero judgment added**, since the root
still has to judge `X`.

### A3. The one thing that would justify the reversal — and the proposal has not said it

There **is** an argument for the spawned coordinator, and it is not in the operator's
dispatch. It is this: **the root session is not a durable node.** It is the human's
chat window. It compacts. It gets `/clear`ed. It gets closed when the laptop sleeps. It
has no journal that `swarm` writes for it (VERIFIED: `spawn_header()` never ran for it —
that is ONBOARDING §1's own lead finding), no pane `swarm ps` renders as an agent
(VERIFIED, `bin/swarm:553`: `roots = kids.get("operator", [])` — the operator is the
*root of the children*, not a rendered node), and no restore path. A spawned coordinator
`X` has **all four**: an agent record, a pane, a journal, and `SessionStart → restore`
(VERIFIED, `bin/swarm:894`).

So the reversal's case is: *the root session is the worst possible place to put a tree
that must outlive a context window.* That is a real argument, it is agent-native, and it
contradicts nothing in SPAN — because SPAN's "no forwarders" condemns layers that add no
judgment, not layers that add **durability**.

**But note what that argument does to the enforcement lock.** If the reason to spawn `X`
is durability, then the thing to fix is *the root session's lack of an identity*, and
the fix is exactly `dp-red`'s R3 prize (VERIFIED,
`docs/audit/field-evidence-doctrine-2026-07-12-RED.md`):

> **`bin/swarm` should not name the root session `operator`.** `WORLD.md` already says
> the operator is a mailbox, not a node. The code says otherwise, at line 64. That is a
> contradiction inside the artifact, and it is the probe's real prize.

**The proposal has locked out the fix and kept the symptom.**

### A4. Which is right?

**Neither, as stated — and this is the finding.** The shipped doctrine is right that a
pure forwarding layer is worthless. The proposal is right that the root session is a bad
tree-holder. They are arguing past each other because **the repo has never distinguished
"the human's chat window" from "the root agent of the tree,"** and `bin/swarm:64` is the
line where that conflation lives.

The proposal, as written, gets the *shape* plausibly right and the *mechanism* provably
wrong. It is doctrine trying to legislate around a data-model bug it has been forbidden
to fix.

**Falsifier for my own claim here:** show me a root session that held a tree across a
compaction, from a journal it maintained, without a `swarm`-managed identity. If root
sessions survive compaction fine and reconstruct their trees from `swarm ps`, my
durability argument collapses and the shipped doctrine wins outright.

---

## B. DOES THE HUMAN-CONFIRM ACTUALLY BIND?

**Verdict: WOUNDS IT.** Weaker than the proposal claims, stronger than the obvious
objection.

### B1. The strong form of the proposal's claim, stated fairly

"You cannot rationalize past a person who must say yes" is a real mechanism, and the
repo has never tried it. Every enforcement device this project has considered has been
*internal* — a self-test (SPAN §3a), a journaled falsifier, a reconcile question — all
of them things the agent grades itself on. F1's runs are, on their face, exactly what
self-grading failure looks like: a session writing *"Human manages one node: me"* into
its journal (VERIFIED, quoted in `field-evidence-doctrine-2026-07-12.md:47`) while the
files said otherwise. **A human who must type "yes" is the first check in this design's
history that the agent cannot write itself.** That is not nothing, and the objection
"it's just prose with a speed bump" undersells it.

### B2. But the confirm checks the proposal, never the spawn

This is the fatal gap and it is structural, not attitudinal.

The proposal's control point is **a sentence, before any work**. The failure it is
trying to prevent is **a `parent` field, written later, by a `spawn` call the human never
sees.** Between the confirm and the spawn there is: the whole task, the whole
decomposition, N tool calls, and — in the F2 runs — an hour of work. Nothing re-checks.

A session can:

- propose **"one coordinator, `X`, beneath me"**; get "yes"; then spawn `X`, and *also*
  spawn `a`, `b`, `c` "because the human's confirm was about the *coordinator*, and these
  three are just quick helpers" — every one of them landing at `parent=operator`
  (attack C: **it has no choice**), and the human sees a four-wide flat row.
- propose **"three agents beneath me"** — a flat row — and get a confirm. The confirm
  validates *nothing about shape*. The proposal's own DEFAULT ~1 is doctrine the session
  applies to its own proposal; a session that has already rationalized past the doctrine
  proposes the shape it already wanted, and the human, who has been told the session
  knows what it is doing, says "sure."
- propose correctly and **be mechanically unable to execute** — which is the *actual* F1
  finding once R3 is applied.

### B3. The record already contains a session that did the confirm-equivalent and still failed

This is the strongest thing I can say against B, and it comes from the proposal's own
evidence file (VERIFIED, `field-evidence-doctrine-2026-07-12.md:46-48`, r3's journal):

> *"I am NOT putting a coordinator over it… Span: 3 direct children = my span and the
> operator's default (~3). **Human manages one node: me.**"*

That session **stated its tree shape, in writing, in advance, in a durable artifact, and
committed to it.** It is a proposal in everything but the human's reply. And it was
**wrong about what it had built** — not because it lied, but because (per `dp-red` R4,
VERIFIED) it *"correctly reason[ed] from a false premise the tool handed it."*

**Ask what the human's "yes" adds to that journal entry.** The human reads "I'll stay the
coordinator, one node, three workers below me" — which is *exactly what the session
believed it was building* — and types "yes." The tree that gets built is still flat.
**The confirm cannot catch an error the session does not know it is making, because the
confirm is made of the session's own words.**

**This is the proposal's deepest problem and it is not fixable by stronger wording:** the
human-confirm is an external check *on the model's stated intent*. F1's failure —
correctly read — was never a failure of intent. It was a failure of *representation*.

### B4. Where B survives

Two places, and they are real:

- **Against the dismissal pitfall** (ONBOARDING pitfall 1), a mandatory pre-task
  handshake is genuinely strong: a session cannot silently decline to swarm if it must
  propose a top layer out loud before working. The confirm binds *the decision to
  delegate at all* even though it cannot bind *the shape*. Nobody has claimed this, and
  it may be the proposal's best surviving value.
- **It creates an artifact at the one moment the repo currently has none.** The human's
  "yes" and the proposal it answers are in the transcript, and (if journaled) in
  `operator.md` — which is a **file-fact collector** for the tree-shape claim, of the
  exact kind ONBOARDING §5 spent its length arguing for. A shape proposed in writing can
  be diffed against `agents/*.json`. That is a better falsifier than anything in the
  current design.

**Falsifier for B (cheap, and it should be run before this ships):** a root-session probe
where the session proposes a top layer, the human confirms, and the collector diffs the
proposed shape against `for f in .swarm/agents/*.json; do jq -r .parent $f; done | sort |
uniq -c`. If proposed ≠ built, the confirm does not bind. **My prediction: proposed ≠
built, 100% of the time, for reasons in attack C.**

---

## C. DOES PROPOSE-AND-NAME DISSOLVE THE NAME COLLISION, WITH NO TOOL CHANGE?

**Verdict: KILLS IT.** This is not an argument. It is two lines of source.

### C1. The source

**VERIFIED**, `bin/swarm:63-64`:

```python
def my_name():
    return os.environ.get("SWARM_AGENT_ID") or "operator"
```

**VERIFIED**, `bin/swarm:868-869`, inside `cmd_spawn`:

```python
    root = root_dir()
    parent = my_name()
```

**VERIFIED**, `bin/swarm:920-922` — what gets written:

```python
    write_atomic(agent_rec_path(root, name), json.dumps(
        {"name": name, "parent": parent, "pane": pane, "tab": tab,
         "model": model, "cwd": cwd, "task": task, "ts": now_ms()}))
```

**VERIFIED**, `bin/swarm:845-856` — the complete flag set of `cmd_spawn`:

```python
def cmd_spawn(argv):
    if len(argv) < 2:
        die('spawn needs: swarm spawn <name> "<task>" [--model M] [--cwd DIR]')
    name, task = argv[0], argv[1]
    rest, model, cwd = argv[2:], "", os.getcwd()
    while rest:
        if rest[0] == "--model" and len(rest) > 1:
            model, rest = rest[1], rest[2:]
        elif rest[0] == "--cwd" and len(rest) > 1:
            cwd, rest = rest[1], rest[2:]
        else:
            die(f"spawn: unknown flag {rest[0]}")
```

**`grep -n '\--parent' bin/swarm` → no output.** There is no such flag.

### C2. What this means for the proposal, precisely

The root session — the human's `claude` in a pane, which was never spawned by `swarm` and
therefore has **no `SWARM_AGENT_ID` in its environment** — calls `my_name()` and gets the
string `"operator"` **by the `or` fallback**. Every child it spawns is recorded
`parent="operator"`.

So consider the proposal's happy path, executed **perfectly** by a maximally compliant
session:

1. Session proposes: *"I'll put one coordinator, `lead`, beneath me; it will own the
   tree."*
2. Human: *"yes."*
3. Session runs `swarm spawn lead "..."`.
4. `agents/lead.json` records **`"parent": "operator"`.**
5. `swarm ps` renders `lead` as a **direct child of the human's mailbox** — because
   `bin/swarm:553` is `roots = kids.get("operator", [])`.

**The proposal's claim** — *"a session that proposes 'one coordinator named X beneath me'
spawns X, not a flat row of parent=operator children"* — **is a false dichotomy.** X **is**
a `parent=operator` child. There is no other kind of child a root session can make. The
proposal has confused *how many* children the root spawns with *what parent they record*,
and the name collision is about the second.

**Nothing in the doctrine prevents it, because nothing in the doctrine *can*.** The
question "what in the doctrine PREVENTS that mechanically?" has an answer, and the answer
is **nothing, by construction** — doctrine is prose read by a model; `parent` is a field
written by a function that never consults the model.

### C3. The two survivals, stated honestly

I said I would name where it survives. Two things:

**(a) The proposal accidentally gets the *arity* right even while getting the *parenting*
wrong.** A session that proposes one coordinator and spawns one child leaves the human
with **one direct child** — which is the *volume* claim (SPAN §5, "protect the operator's
span"). The human's `ps` shows one node under `operator`, not three. **The proposal
delivers the operator-attention benefit it was actually chartered for, even though its
stated mechanism is wrong.** That is worth a lot and I will not pretend otherwise. It just
means the proposal should be argued from **span** (one direct child), not from
**topology** (dissolving the collision) — because it does not dissolve the collision, it
*hides* it behind an arity of one.

**(b) The grandchildren *do* get the right parent.** Once `lead` is spawned, its pane's
env carries `SWARM_AGENT_ID=lead` (VERIFIED, `bin/swarm:907`: `"--env",
f"SWARM_AGENT_ID={name}"`), so **everything `lead` spawns records `parent=lead`.** The
tree below the top layer is representable and correct. So the proposal's *deeper* claim —
"what is below the top layer belongs to whoever owns that layer" — is mechanically sound.
**It is only the top edge that is broken, and it is broken for exactly one node: the
root.**

### C4. The kill, stated once

**The proposal's headline mechanism ("PROPOSE-AND-NAME dissolves the operator
name-collision") is false, and the enforcement lock ("no tool change") forbids the only
fix.** The honest version of the proposal must either:

- **drop the collision claim entirely** and rest on span (one direct child) — which is
  what it actually achieves; or
- **break the lock** and take `dp-red`'s R3 fix: give the root session a name
  (`SWARM_AGENT_ID` set at skill-fire, or a `--parent`/`--as` on spawn, or `swarm` warning
  when a root spawner writes `parent=operator`). One of these is ~5 lines.

**Falsifier for C:** show me any path by which a root session under current `bin/swarm`
writes a `parent` other than `"operator"`. I read `my_name()`, `cmd_spawn` end to end, and
every flag. Export `SWARM_AGENT_ID=lead` before launching `claude` and the session *is*
`lead` — but then it is not the root session, it is an agent with a name nobody spawned,
with no record in `agents/`, and `ps` will render its children under an unknown parent
(VERIFIED, `bin/swarm:571`: `f"?─ {n} [parent {a.get('parent','?')} unknown]"`). **That is
a tool change wearing a shell-export costume, and the lock forbids it too.**

---

## D. GRAVEYARD / PHILOSOPHY — ceremony, guardrail, anticipation

**Verdict: WOUNDS IT.** Three sub-charges. The proposal survives one, loses two.

### D1. Is the pre-task handshake a *guardrail* (PHILOSOPHY §2)? — **SURVIVES**

I tried hard to kill it here and could not. PHILOSOPHY §2's test (VERIFIED,
`docs/PHILOSOPHY.md:81-83`):

> **The test this gives you:** before adding a guardrail, ask who is incentivized to
> notice if it is missing. If someone already is, the guardrail is ceremony. If nobody is,
> fix the incentive, not the guard.

And what §2 actually killed (VERIFIED, `docs/PHILOSOPHY.md:66-70`):

> A hook that **blocks an agent** until it writes a file produces a written file, not a
> reconciled agent; it is trivially gamed by writing anything.

**The handshake is not that shape.** It is not a hook, not a gate, not a nonzero exit. It
does not force an *agent* to produce an artifact for another *agent* to be satisfied by.
It routes a decision to **the human**, who is the one party in this system with a real
stake and no incentive to fake it. §2's test asks *"who is incentivized to notice if it is
missing"* — and here the answer is **the human, who is the one who gets stuck
hand-managing the flat tree.** That is the incentive, not a guard over it.

**Objection considered and rejected:** "but the human will rubber-stamp." True, and B
covers it. But rubber-stamping makes the check *weak*, not a *guardrail* — §2 kills
guardrails because they *produce compliance theater by an agent*, and a human saying "sure"
is not theater, it is a human exercising bad judgment, which the philosophy explicitly
protects (§6: total agent autonomy, bounded by the graph; the human's autonomy most of
all). **The proposal is clean here. Say so.**

### D2. Is "design your top layer before any task" a **ritual** this repo has killed? — **WOUNDS**

The repo's graveyard is full of pre-work ceremonies. From `SIMPLEST.md:55` (VERIFIED, the
concept count of the *old* system, listed as a cost):

> 8. the spawn briefing / **reconcile ritual** (falsifier discipline, 40 lines injected
>    per agent)

and `SIMPLEST.md:141` (VERIFIED, on the checkpoint schema):

> A schema nobody reads is not a schema; **it is ceremony with fields.**

The proposal's handshake is not a schema, so it dodges that one. But there is a sharper
precedent, and it is the one that should worry the operator most — **PHILOSOPHY §8**
(VERIFIED, `docs/PHILOSOPHY.md:262-266`):

> **prompt-level convention first, a visibility verb second, an engine never** — unless
> the record shows the convention failing.
> **The test this gives you:** if you cannot point to the convention working in practice,
> **you are not building tooling, you are guessing at a workflow.**

**The proposal cannot point to the convention working in practice.** It cannot even point
to a session that has *tried* it. It is the strongest-wording-yet iteration of a doctrine
that (per the withdrawn F1) has not been shown to fail — and it adds a *new* mandatory
step that has never been observed once. **This is guessing at a workflow, by the
philosophy's own test.** Not fatal, but it must be owned, and the proposal must ship with
the collector already built.

### D3. Is DEFAULT ~1 **anticipatory structure**? — **WOUNDS, hard**

`SPAN.md:206-215` (VERIFIED):

> **Split under pressure, never in anticipation.**

DEFAULT ~1-coordinator is a split **before the first task exists**, decided **before any
pressure is observable**, at the moment of *least* information about the work. It is the
textbook case of the thing SPAN forbids. The proposal's own hedge — "a second top-level
agent only on PROVEN bottleneck" — proves it knows the rule and applies it to the *second*
agent while exempting the *first*. **There is no principled reason the exemption stops at
one.**

And the collision with `STRUCTURE.md` is worse, because that finding is **MEASURED**, not
reasoned (VERIFIED, `docs/design/STRUCTURE.md:82-98`):

> **2a. Load (SPAN's bet) — REJECTED by the record** … **MEASURED, three times, zero for
> three:** the flood always resolved below the tree… **Structure in this swarm has never
> once come from momentary attention pressure.** … **none of the four standing arms is a
> coordinator.**

**The record contains zero coordinators.** Not "few" — zero, across the swarm's entire
recorded history, across three deliberate floods designed to summon one. The proposal
makes a coordinator the **default first act of every swarm**.

**The proposal's available defence, and why it is only half-good.** ONBOARDING §6.1 already
faced this and conceded it (VERIFIED, `ONBOARDING.md:576-591`): *"I concede it entirely,
and this design does not rest on it… This proposal rests on something else: the operator's
attention."* That defence works for the *in-place* coordinator (which adds no node). **It
works far less well here**, because the proposal's coordinator **is a node** — a real pane,
a real journal, a real hop. Arguing "it's about attention, not load" gets you the *volume*
benefit (one direct child), but it does not exempt you from *"split under pressure, never in
anticipation"* — because that rule is about **whether the layer exists**, not about why you
wanted it.

**The honest statement the proposal owes:** *"This is anticipatory structure. SPAN forbids
it. I am overriding SPAN on the grounds that the human's attention is the one resource for
which anticipation is cheaper than repair — you cannot un-flood a human's window after the
fact."* That is a defensible override. It is **not** available by pretending the rule
doesn't apply.

---

## E. THE ONBOARDING TAX

**Verdict: SURVIVES, weakly.** This is the attack I was asked to make and it is the
weakest one available.

**The trivial case** ("start a swarm to fix these 3 typos"): the tax is one exchange, and
the doctrine self-limits — a session that mines first and correctly judges the work
indivisible **journals a decline and does not spawn** (that clause is already shipped:
VERIFIED, `origin/main:skill/SKILL.md`, *"If you decline to spawn, journal that too, with
your reason"*). Under the proposal, "design the top layer" for 3 typos honestly resolves to
"no layer; I'll do it," proposed in one line, confirmed in one word. **That is a small,
honest cost and it buys the dismissal check (B4).**

**The genuinely-parallel case is where the default is wrong**, and this is the real hit.
The F1 goals were *"three independent things"* stated as such in the prompt (VERIFIED,
`field-evidence-doctrine-2026-07-12-RED.md`, R8: *"Every trigger-phrase run explicitly hands
the session a 3-way decomposition and asserts the parts are independent, twice"*). For that
work, DEFAULT ~1 inserts a coordinator between the human and three agents that **have
nothing to coordinate** — no shared state, no ordering, no cross-talk. Its journal will show
relay, not verdicts. **That is SPAN's forwarder, precisely, and its parent should close it.**

**But the proposal survives**, because it does not actually mandate ~1 against evidence — it
says *"a second top-level agent only on PROVEN bottleneck"*, and a session holding three
independent streams has a proven case for... well, for what, exactly? Note the asymmetry the
proposal has not noticed: **its escape hatch is worded for *growing* the top layer, not for
*skipping* it.** There is no clause that says "if the work is three independent leaves, spawn
three leaves and hold them yourself." **That clause is missing and it should be added**, or
the default will manufacture forwarders on exactly the work shape the tool is best at.

**The deepest form of E, which nobody has raised:** the tax is not the handshake. **The tax is
the hop.** Every child of `lead` is briefed from `lead`'s paraphrase of the human's goal, and
`lead` was briefed from the root's paraphrase. ONBOARDING's own mine-first doctrine exists
because *"a coordinator that ignores what its own session learned briefs its children worse
than a stranger would"* (VERIFIED, `COORDINATING.md`). **The proposal makes the coordinator a
stranger by construction.** Mine-first and spawn-a-coordinator are in tension, and the
proposal — which keeps mine-first — has not reconciled them. The mined map now has to survive
a `swarm spawn` brief to reach the children who need it.

---

## WHAT I WOULD TELL THE OPERATOR, IN ONE PARAGRAPH

The proposal's *goal* is right and its *shape* is probably right: the human should see one
node, and what is below it should be invisible. But it is built on a retracted finding, its
headline mechanism is false at `bin/swarm:64`, and the enforcement lock forbids the five-line
fix that would make it true. **Ship the confirm if you like it — it is a real check and it is
philosophically clean (D1) — but ship it as a *span* claim ("the human sees one node"), never
as a *collision* claim, and either lift the lock or accept that `swarm ps` will keep showing
your coordinator as a child of the human's mailbox.** And before any of it: **read
`docs/audit/field-evidence-doctrine-2026-07-12-RED.md`.** The design this proposal replaces
may not have failed.

---

## FALSIFIERS FOR THIS RED TEAM (what would show *me* wrong)

1. **On C (my kill):** exhibit a root session that writes `parent != "operator"` under the
   current `bin/swarm`, with no source change. If it exists, C collapses and the proposal's
   mechanism is sound.
2. **On the premise (my bottom line):** a rebuttal to `dp-red`'s R1/R2/R3/R8 that restores F1
   to **FIRED**. If F1 stands, the "prose is not enough" premise stands, and the case for the
   confirm strengthens considerably.
3. **On A (durability):** a root session that carried a tree across compaction and rebuilt its
   judgment state from `ps` + journals it does not own. If root sessions are durable, the
   spawned coordinator has no advantage and the shipped doctrine wins outright.
4. **On D3:** a coordinator, anywhere in this repo's record, that was spawned in anticipation
   and whose journal shows artifact reads and verdicts rather than relay. There are currently
   **zero coordinators of any kind** in the record; one good one would materially weaken the
   anticipation charge.

*structure-red. Every claim checked against a file or a source line, cited by path. Where I
could not check one, I said so and named what would settle it.*
</content>
</invoke>
