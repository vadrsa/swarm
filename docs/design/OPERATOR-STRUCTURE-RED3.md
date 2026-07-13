# RED3 — fresh adversarial review of the REFRAMED operator-structure model

**Reviewer:** `structure-red3`. I did none of the design work; that is my qualification.
Written 2026-07-12 against `main@aa6063d`. I reviewed the **new model** as briefed
(operator-outside-the-swarm, doctrine-only, no tool change). The retracted `root-1`
design is treated as evidence, never as the proposal.

**Method.** Every load-bearing claim is checked against a primary artifact — source at
`file:line`, or a command I ran with its output pasted. I reproduced all three of the
author's evidence commands rather than trusting them, and I built and ran a working
counter-artifact for the attack that decides the review. Where I could not reach a
failure state I say so and rate the attack lower. Two reviews today caught the author
being kind to his own hypothesis, and one caught *itself* doing it; the way to meet that
bar is to bring artifacts, not adjectives.

---

## BOTTOM LINE

**Your central claim — "no tool change is needed" — is TRUE. Every reason you gave for it
is wrong, and the real reason is one you never mention.**

The tool change you need **already shipped, this morning, in your own repo.** `cmd_send`
runs a configurable **send middleware** before every queue write (`bin/swarm:993-1034`,
merged in `aa6063d`; contract in `WORLD.md:62-77`; there is even a `swarm-middleware`
authoring skill installed at `~/.claude/skills/swarm-middleware`). It is admission control
in code, on exactly the path — `queue/operator/` — that RED2 §2 proved is the human's real
load. You are arguing "doctrine-only, no tool change" while holding, unmentioned, the
enforcement mechanism that answers the one attack you flagged as possibly fatal.

So the honest headline is not *"doctrine-only is enough."* It is:

> **The doctrine sets the policy; the middleware enforces it; and neither one is a change
> to `bin/swarm`. "No tool change" is right, but only because you already made it.**

Attack B is the review. It is where you asked "THIS MAY BE FATAL — chase it," and you were
right to. I chased it, and it is fatal **to the doctrine-only framing**, not to the model.

| # | Attack | Verdict |
|---|---|---|
| **B** | Doctrine cannot bind a grandchild; the mailbox is wide open | **KILLS the "doctrine-only" framing** — and the model is *rescued* by a mechanism you already own (§B) |
| **A** | Is doctrine-only a cop-out — the same bet that failed 4/4? | **SURVIVES, but you must stop citing the 4/4** — your own evidence file *retracts* that reading. You are steel-manning an attack on yourself with a number that doesn't say what you think (§A) |
| **C** | Is "operator outside the swarm" coherent vs the files? | **WOUNDS IT** — the contract already contradicts *itself* (`WORLD.md:12` vs `:57`); your model must resolve that, and it can, but not by ignoring it (§C) |
| **D** | Is "default ~1" already a prescription / anticipatory structure? | **SURVIVES on the prescription charge; WOUNDS the citation.** The 3-for-3 does not license what you're using it for (§D) |
| **E** | Is the selection rule operational or a mood? | **WOUNDS IT** — it is a mood as written; it is salvageable, and I give the wrong-answer case (§E) |
| **F** | Citations, overclaims, misses | **Three real misses**, one of which invalidates a premise you built an attack on (§F) |

---

## §0 — A FACT THAT PRECEDES EVERY ATTACK: THE REPO YOU ARE REVIEWING FROM IS STALE

Before any verdict: **the skill text in this repo is not the skill text that runs.**

```
$ md5 -q skill/SKILL.md                        # the repo you are designing in
1c1dc0d23a0f6d422315785e796ad337
$ ls -l ~/.claude/skills/swarm
... -> /Users/vadrsa/.local/share/swarm/skill  # the one Claude Code actually loads
$ md5 -q ~/.claude/skills/swarm/SKILL.md
f6f30abd5df8c6ca35e227eab4460aa2
$ grep -c "stay the coordinator\|Mine before you spawn" skill/SKILL.md
0
$ grep -n "stay the coordinator\|Mine before you spawn" ~/.claude/skills/swarm/SKILL.md
13:**You stay the coordinator, here, in this session.** ...
19:**Mine before you spawn.** ...
```

ONBOARDING's doctrine **is merged and live** (`b94fa9e` / `5713a6d`, in
`~/.local/share/swarm`), and **absent from the checkout you are writing the design in.**

This matters twice. First, anyone reviewing from `git/swarm` alone concludes ONBOARDING
never shipped, which is false. Second — and this is the sharp end — **your attack-A premise
("the LAST doctrine-only answer FAILED IN THE FIELD 4/4") is being asserted from a repo
that cannot see the doctrine it is judging.** See §A.

---

## §B — THE OPERATOR'S F′ PROBLEM. **KILLS THE "DOCTRINE-ONLY" FRAMING; RESCUES THE MODEL.**

You asked the right question and you flagged it correctly as possibly fatal. Taking it in
the order the evidence forced on me.

### B.1 — The mailbox is wide open. I proved it by accident, which is the best kind of proof.

I built a 3-deep tree in a scratch directory (`operator → top → mid → deep`) to test whether
a grandchild can mail the human. Because `root_dir()` walks *up* to the enclosing `.swarm/`,
my sandbox agent records were ignored and **the sends landed in the real, live operator
mailbox — yours:**

```
$ env -u HERDR_ENV SWARM_AGENT_ID=deep python3 bin/swarm send operator "I am 3 levels down..."
exit=0
$ env -u HERDR_ENV python3 bin/swarm ps | head -3
operator — 6 message(s) waiting for the human (queue/operator/):
    from deep, 0s ago
    from deep, 0s ago      ... x6
```

(I removed all six; `ps` is back to "no waiting mail." The queue is clean. Recorded here
because the accident *is* the finding.)

Read what that actually demonstrates. An agent named `deep` — **which does not exist in the
live swarm's `agents/` registry**, running **outside herdr**, from a **scratch directory
that is not the project**, with **no parent, no pane, no spawn record** — wrote six times
into the human's mailbox, and the tool did not object once. Not "a grandchild can mail the
human." **A string can mail the human.**

The code says exactly this. `cmd_send`, `bin/swarm:986-992`:

```python
    if to != "operator" and to not in agents:      # <-- membership check
        die(f"unknown agent: {to}")                #     EXPLICITLY EXEMPTS operator
    sender = my_name()                             # <-- whatever SWARM_AGENT_ID says
    rec = {"to": to, "from": sender, ...}
    err = send_size_error(rec, relation(...))      # <-- the ONLY gate: byte count
```

The one guard that exists (`send_size_error`, `:249-260`) checks **character count against
the turn cap**. That is the entire admission policy on the human's attention. No parent
check, no depth check, no throttle, no membership check — and `to != "operator"` means the
*only* recipient in the system exempted from even the existence check **is the human**.

**Your framing of this attack is correct and if anything understated.** RED2 §2 is right,
you were right to accept it, and it is worse than RED2 said.

### B.2 — Your stated mechanism for why doctrine can't fix it is HALF WRONG, and the half you got wrong is the important half.

You wrote: *"spawned agents NEVER read SKILL.md; grep -i skill bin/swarm = zero hits. So how
does a doctrine in SKILL.md stop a GRANDCHILD from mailing the human??"*

The grep is right — I ran it, zero hits, `bin/swarm` never touches SKILL.md. But the
conclusion does not follow, **because SKILL.md is not the channel that reaches agents.**
`spawn_header()` is (`bin/swarm:771-811`), and it is injected into **every** spawned agent's
prompt (`:896`, `write_atomic(taskfile, spawn_header(name, parent) + task)`). And it already
carries operator-span doctrine — verbatim, `bin/swarm:804-806`:

> *"operator's span is theirs to declare and yours to protect: **never let the tree press
> more direct attention on the operator than they asked for.**"*

**Every agent in your tree, at every depth, is already briefed not to do this.** `deep` would
have received that sentence. So the true statement is not "no doctrine reaches the
grandchild." It is:

> **The doctrine already reaches every grandchild, and the grandchild can still flood the
> human anyway, because nothing enforces it.**

That is a *strictly stronger* version of your own attack, and it kills the doctrine-only
answer more cleanly than your version does. Your version says "we never told them." The
truth is "we told them, in the one channel that reaches them, and telling is not binding."
You cannot fix by better wording a failure that better wording has already not fixed.

**There are two doctrine channels and you have been reasoning about the wrong one:**

| channel | reaches | carries |
|---|---|---|
| `SKILL.md` (Claude Code skill autoload) | **only the human's own root session** | the 5-point doctrine + ONBOARDING's stances |
| `spawn_header()` (`bin/swarm:771-811`) | **every spawned agent, all depths** | delegate-by-default, span self-test, **operator-span protection** |

A doctrine you put in SKILL.md governs *the operator session's own behavior* and nothing
else. That is the correct place for the stance you are writing — because under your model
the operator session's behavior is exactly what you are trying to change. **But it can
never constrain the tree**, and you should stop claiming or implying that it will.

### B.3 — THE NON-TOOL ANSWER YOU ASKED FOR EXISTS, AND YOU BUILT IT THIS MORNING.

You asked: *"Is there a NON-tool answer?"*

**Yes. The send middleware.** `cmd_send` runs a configured middleware on **every send, before
the queue write**, and an exit of 100 means *not queued* (`bin/swarm:993-1034`; contract
`WORLD.md:62-77`; commits `1aadc04`, `8238815`, `ae4b3eb`, `b4647e1`, `7cd5086`, all in
`aa6063d`). There is an authoring skill for it installed on this machine.

I wrote one that enforces **your model** — *only top-level agents may mail the human;
everyone below is escalated to their own parent* — and ran it against the 3-deep tree:

```python
# mw.py — the whole thing
rec = json.load(sys.stdin)
if rec["to"] != "operator": sys.exit(0)          # not operator mail: pass
p = parent_of(rec["from"])
if p == "operator" or p is None: sys.exit(0)     # top-level (or unknown): PASS, fail open
subprocess.run([... "swarm", "send", p, "--stdin"],               # escalate to its parent
               input=f"[escalated from {rec['from']}...]\n" + rec["body"], text=True)
sys.exit(100)                                    # HANDLED: nothing queued for the human
```

```
TEST 1 — grandchild 'deep' (3 levels down) mails the human:
  operator mailbox:  0        <-- REFUSED
  'mid' mailbox:     1        <-- escalated to deep's own parent
  {"to":"mid","from":"gate","body":"[escalated from deep, who tried to mail the human]\nhuman, look at me"}

TEST 2 — top-level agent 'top' mails the human:
  operator mailbox:  1        <-- PASSED
  {"to":"operator","from":"top","body":"top-level report, legitimately yours"}
```

**Zero bytes changed in `bin/swarm`.** Your model — *the operator's only correspondents are
its top-level agents; everything below is those agents' concern* — is now a **code fact**,
not a tendency. The grandchild's mail did not reach the human because it *could not*, and
the report it was trying to make went where your model says it belongs: **up its own chain,
to the agent whose job is to read it.**

This is the difference between your bet and ONBOARDING's bet, and it is not "the wording is
better." It is:

> **ONBOARDING asked the tree to be polite about the human's attention. This can make the
> tree's impoliteness unrepresentable — on the exact path (`queue/operator/`) that carries
> the load — without touching the tool.**

### B.4 — The cost, stated honestly, because I am not here to sell you this.

1. **It contradicts the contract.** `WORLD.md:59` promises *"nothing ever refuses a message
   to the operator."* A middleware that exits 100 on a grandchild's operator-mail **refuses
   a message to the operator.** Note the contract *already* contradicts itself here — the
   middleware bullet at `:66-67` says exit 100 means "nothing is queued," in the same file,
   fourteen lines below the promise that nothing is ever refused. **You must resolve this in
   `WORLD.md`, and that is a contract change even though it is not a code change.** Do not
   let "no tool change" quietly smuggle in "no contract change." It is not the same claim,
   and RED2 §0 caught this design family losing track of its artifact once already.
   *(Escalate-don't-drop is the honest reading: nothing is lost, the message is re-routed to
   the agent who owns it. Say that in WORLD.md, or drop the promise. Don't leave both.)*
2. **It is opt-in per-swarm** (`.swarm/config`), fail-open by design (`:1029-1030`, any
   non-100 exit queues anyway). So it protects the human who configures it; it is not a
   property of the system. **That is a real limit and you should state it, not paper it.**
3. **It is a policy the human installs, which is precisely what your model says the operator
   session is for** ("build systems around them"). This is the model eating its own dogfood,
   which is the strongest thing I can say for it.

**Verdict on B: KILLS the "doctrine-only" framing.** The doctrine cannot bind the tree — and
you now have proof stronger than your own argument, since the tree *is* already briefed and
floods anyway. **The model survives, and survives well**, because the enforcement mechanism
exists, requires no tool change, and expresses your model exactly. **Ship the doctrine as the
policy and the middleware as the enforcement, name both, and stop calling it doctrine-only.**

---

## §A — IS DOCTRINE-ONLY A COP-OUT? **SURVIVES — BUT YOUR OWN EVIDENCE DOES NOT SAY WHAT YOU SAY IT SAYS.**

You asked me to score whether you are "repeating a proven failure with better prose," and
told me to say so if my only answer is "the wording is better."

**My answer is that the premise of your own attack is unsound — you are being *unkind* to
yourself with a number that does not support the charge.**

You cite: *"The LAST doctrine-only answer (ONBOARDING.md) FAILED IN THE FIELD 4/4
(docs/audit/field-evidence-doctrine-2026-07-12.md)."* I read that file. **It says the
opposite, in its own post-review verdict, at lines 77-81:**

> **Verdict:** falsifier 1 **FIRED as a shape-fact** in all four skill-loaded runs — but
> the corrected reading is **not "doctrine prose is ineffective"** (the comparison that
> would show that was never validly run); it is: **the tool structurally prevents the tree
> the doctrine asks for.** ... The fix is therefore contract/tool repair, not more prose.

Three separate defects in the "4/4" as you are using it:

1. **Only 2 of the 4 runs carried ONBOARDING's text at all.** Two ran the installed doctrine
   (md5 `f6f30abd…`), two ran repo-HEAD (`1c1dc0d2…` — the *pre*-ONBOARDING text). It is not
   4/4 for ONBOARDING; it is 2/2, with a 2-run arm that never received the treatment.
2. **The baseline arm is RETRACTED as uninformative by that very file** (`[R1]`, lines
   53-59): both arms already contained operator-span language, "the zero delta between them
   supports nothing," and "a true pre-doctrine baseline remains unrun."
3. **The 4/4 shape-fact was FORCED BY CODE, not chosen by the model.** `my_name()`
   (`bin/swarm:63-64`) returns `SWARM_AGENT_ID or "operator"`, so a root session's every
   spawn records `parent=operator` **unconditionally**. The observers could not have produced
   a different tree if the doctrine had been carved into their skulls. **A prose intervention
   that is mechanically prevented from having an observable effect has not been tested and
   cannot have failed.**

So: **ONBOARDING was never falsified. It was never validly tried.** "Doctrine-only failed
4/4" is a claim the record specifically declines to make.

**What this does to your attack.** It removes the "proven failure" you are afraid of
repeating — but it does **not** license doctrine-only, because §B killed that on independent
grounds (the tree is already briefed and floods anyway). The two findings are consistent and
they point the same way:

> **Doctrine is untested, not disproven. And it is structurally incapable of binding the
> tree. Both are true. So the answer is not "doctrine again, better" and not "doctrine is
> dead" — it is "doctrine for the session it can reach (the operator's own, via SKILL.md),
> enforcement for the tree it cannot (via middleware)."**

Which is exactly the split §B lands on. **The two attacks converge, and that convergence is
the strongest structural result in this review.**

**Verdict: SURVIVES.** You are *not* repeating a proven failure — there is no proven failure.
But **you must stop citing the 4/4 as one**: it is a miscitation of your own evidence, in the
direction of harshness rather than kindness, and it would have led you to abandon a correct
component (a doctrine aimed at the operator session) for a bad reason.

---

## §C — IS THE MODEL COHERENT? "OUTSIDE THE SWARM" vs THE FILES. **WOUNDS IT.**

You asked me to rule. Here is the ruling.

**The contradiction is real, it is already in the contract, and you did not create it —
but your model is the first thing that has to answer for it.**

```
WORLD.md:12   The human **operator** roots the tree.        <-- the operator IS the root node
WORLD.md:57   **The operator is a mailbox, not a node.**    <-- the operator is NOT a node
```

Fourteen lines apart, in the file that is supposed to be the contract. The code sides with
both, incoherently: `parents_of()` (`:132-133`) defaults every parentless agent to
`"operator"`, `render_ps` roots the display at it, `relation()` (`:165-166`) gives it a
privileged **sender class** ("the OPERATOR (the human at the root)") — all node-like. Yet it
has no `agents/operator.json`, no pane, no doorbell (`:1038-1040`: *"The operator is a
mailbox, not a node: no pane, no doorbell"*), and its queue is drained by a human, not the
tool.

**So: is "outside the swarm but the parent of its top-level agents" coherent? YES — but only
under a distinction you have not yet drawn, and must.**

The resolution is that **"the tree" is being used for two different graphs:**

- **The authority graph** — who briefs, judges, and approves whom. The operator **is** the
  root of this. It is the parent of its top-level agents. `relation()`'s OPERATOR class and
  the `parent="operator"` records are the authority graph, correctly recorded.
- **The agent graph** — the set of Claude sessions the tool manages: spawns, rings, delivers
  to, closes, renders liveness for. The operator is **not** in this. It has no record, no
  pane, no doorbell, and the tool never delivers to it.

**Your model is coherent, and it is exactly this: the operator is the root of the authority
graph and outside the agent graph.** That is not a contradiction; it is the ordinary shape of
a principal standing outside the system it directs. `my_name()` returning `"operator"` is
then *correct* — you are right that the name was never wrong — because the string names **a
seat in the authority graph**, and the human's session legitimately occupies that seat.

**But you do not get this for free, and here is the wound.** Under your model, the sentence
*"the human operator roots the tree"* (`WORLD.md:12`) and the sentence *"the operator is a
mailbox, not a node"* (`:57`) are **both true and about different graphs** — and **nothing in
the contract says so.** Every reader who has hit this has read it as a contradiction,
including the field-evidence authors (who called it *"the contract and the code contradict
each other"*) and RED2. You are proposing to *build on* the coherence of a distinction the
contract does not draw.

**Requirement, and I would block on it:** if the model ships, **WORLD.md must state the
distinction explicitly.** One sentence. Something with the shape of: *"The operator roots the
tree of authority and stands outside the tree of agents: it is every top-level agent's
parent, and it is not itself an agent — no pane, no record, no delivery."* Without that, the
next reader re-derives "contradiction," and the design's own central premise reads as papering.

**Verdict: WOUNDS IT.** The position is coherent — genuinely, and I tried hard to break it.
But it is coherent *only once you draw a distinction you currently leave implicit*, and the
contract as written actively contradicts itself on the point. **It is not a contradiction you
are papering over; it is one you are inheriting and have not yet paid off.** Pay it off in
WORLD.md or the model rests on a sentence that isn't there.

---

## §D — NO-PRESCRIBED-STRUCTURE vs DEFAULT ~1. **SURVIVES the prescription charge; WOUNDS the citation.**

Two questions; they have different answers.

**D.1 — Is "default ~1" already a prescription? NO, and your line is defensible.**

The line between a default and a prescribed shape is not fuzzy, and you can state it in one
test: **a default says what to do when you know nothing; a prescription says what to do
regardless of what you learn.** "Adviser → contractors" is a prescription: it names roles and
an arity before it has seen the work. "Start at ~1 and grow on real need" is a default: it is
a *starting point plus a growth rule*, and the growth rule is driven by observed load, not by
a template. The first cannot be falsified by the work; the second is *designed* to be
overridden by it.

The tell that yours is a default and not a shape: **it names no roles.** It does not say what
the one agent *is*. A prescription would.

**D.2 — Is default-~1 anticipatory structure, forbidden by SPAN's "split under pressure,
never in anticipation"? NO — and the citation you are worried about does not reach you.**

`SPAN.md:211` does say *"Split under pressure, never in anticipation"* — I verified it.
But **that sentence forbids splitting *upward into extra layers* in anticipation. Defaulting
to ONE agent is not a split; it is the floor.** "Never in anticipation" cannot possibly mean
"start with zero agents," because zero agents is not a swarm — it is the operator doing the
work itself, which is precisely the bug you are fixing. **~1 is the minimum non-degenerate
tree, and the rule against anticipatory structure has nothing to say about a minimum.** Your
own model's default is the *most* conservative structure that is still a structure. The
attack fails.

**D.3 — But your 3-for-3 citation is a real overclaim, and it cuts against you.**

You invoke *"STRUCTURE.md is MEASURED 3-for-3 that load never summoned a coordinator."* The
string exists (`STRUCTURE.md:82-98`: *"MEASURED, three times, zero for three"*). The
inference does not:

- **All three subjects were spawned in-tree agents**, children of `field-tester` on neutral
  standby briefs (`docs/audit/field-evidence-2026-07-10-span.md`). **The human operator was
  never an experimental subject in any of the three.** You are citing measurements taken on
  agents to constrain the *operator's* structure — the one seat the experiment never touched.
- **One of the three arms carried no span doctrine at all** (`span-base-1` — a control). A
  control that cannot summon a coordinator on doctrine it never received is not a trial of
  doctrine; folding it in over-counts n.
- **The record's own authors say the flood never exceeded span**: *"The doctrine did not
  fail; my flood failed to exceed one agent's attention"* — and the probe *"PASSED honestly
  at 7 streams."* **That is not evidence that pressure fails to summon structure. It is
  evidence the experiment never applied enough pressure.**

**This is the review's second miscitation-against-yourself.** As in §A, you are wielding a
number *more harshly than the record supports*, and it would have talked you out of something
defensible. `3-for-3` does not forbid your default; it says nothing about the operator at all.

**Verdict: SURVIVES.** Default-~1 is a default, not a prescription, and not anticipatory.
**But strike the 3-for-3 citation from the argument** — it is an extrapolation from in-tree
agents to the operator seat that the primary record does not license, and a reviewer who
checks it (as I did) will hole your evidence discipline, which is the thing this repo runs on.

---

## §E — THE SELECTION RULE. **WOUNDS IT.** It is a mood. It is fixable.

The rule: *"the things you would want to check and confirm yourself go under you."*

**As written, it is not operational, and I can show the failure precisely.** It is a rule
whose input is the operator's *desire* ("would want to") and whose output is *structure*. But
desire is unbounded and structure is bounded — **a conscientious operator wants to check
everything.** Applied honestly by a diligent session, "everything I'd want to confirm goes
under me" returns **the whole tree**, which is the flat-row bug you are trying to fix. Applied
by a lazy one, it returns nothing. **The rule's output is determined entirely by the
temperament of the reader, which is the definition of a mood, not a rule.**

**The case where it gives the WRONG answer** (you asked for one; this one is not exotic — it
is the common case):

> The human is shipping a feature with a **test suite, a migration, and a doc update**. Would
> the operator "want to check and confirm" the migration itself? **Obviously yes** — a bad
> migration is unrecoverable, it is the highest-stakes artifact in the batch, and no
> reasonable human delegates it unread. So the rule says: **migration goes under you.** By the
> same reasoning the tests go under you (you'd want to confirm they pass) and the docs go
> under you (you'd want to confirm they're true). **The rule has just reconstructed the flat
> row of three workers under the operator — the exact structure the entire model exists to
> abolish** — and it did so by being applied *correctly and in good faith.*

The rule fails because **"would want to confirm" tracks *stakes*, and structure must track
*attention*.** They are different axes, and the highest-stakes item is very often the one you
most need someone else to own end-to-end so you can review a *result* instead of babysitting a
*process*.

**The repair, and it is available in your own material.** You already have the operational
version — it is the span test in `spawn_header` (`bin/swarm:799-801`) and in your own duties:

> *"You are over span when you can no longer name each child's state and the next artifact you
> expect from it without re-reading."*

**That is executable.** It has a definite input (can I name each child's state and next
artifact, right now, without re-reading?), a definite output (yes → hold; no → split), and it
cannot be satisfied by wanting harder. Recast the selection rule against **what the operator
can hold**, not what they'd *like* to confirm:

> **You keep what you can still name — each top-level agent's current state and the next
> artifact you expect from it, without re-reading. Everything else belongs to an agent who
> can. Stakes do not put work under you; they put a better agent over it.**

That last clause is the one that kills the migration case, and it is the actual content of
your model — *"everything below the top level is those agents' concern."*

**Verdict: WOUNDS IT.** The stance is right; the rule as phrased is a mood that reconstructs
the bug under good-faith application. **Do not ship the sentence as written.** The span test
is already operational, already in the tool's own brief, and already says what you mean.

---

## §F — CITATIONS, OVERCLAIMS, MISSES

**I checked every citation in your brief. Three are wrong, and a fourth is missing.**

| your claim | verdict |
|---|---|
| `env -u HERDR_ENV -u SWARM_AGENT_ID python3 bin/swarm ps` → works | **VERIFIED.** Ran it; prints the live tree. |
| `send <unknown>` → "unknown agent", not a herdr error ⇒ send not herdr-gated | **VERIFIED** — but see the miss below; you tested the wrong recipient. |
| `spawn` → "not inside herdr" (`bin/swarm:865`) ⇒ only spawn is gated | **VERIFIED.** `grep -n HERDR_ENV bin/swarm` returns exactly one site, `:865`. Your "only spawn is gated" is exactly right. |
| `cmd_send` has no parent/depth/throttle check | **VERIFIED** (`:986-992`; only gate is `send_size_error`, a byte count). |
| `WORLD.md:57-59` promises "nothing ever refuses a message to the operator" | **VERIFIED**, line numbers exact. |
| `grep -i skill bin/swarm` = zero hits | **VERIFIED** — **but the conclusion you draw from it is wrong.** See §B.2: `spawn_header()` is the agent-facing doctrine channel, and it *already* carries operator-span protection. |
| "ONBOARDING failed in the field 4/4" | **FALSE as used.** Your own evidence file retracts this reading (§A). |
| "STRUCTURE.md is MEASURED 3-for-3 that load never summoned a coordinator" | **OVERCLAIM.** String is real; the operator was never a subject; one arm was a no-doctrine control (§D.3). |

**MISS 1 — the middleware.** The single most relevant artifact to attack B — shipped this
morning, in this repo, in the commit range at the top of your own `git log` — is **absent from
your brief.** You asked "is there a NON-tool answer?" while the answer sat in `cmd_send`. (§B.3)

**MISS 2 — `spawn_header` is a doctrine channel.** You reasoned "agents never read SKILL.md ⇒
doctrine cannot reach them." Half right, wrong conclusion: they never read SKILL.md, and they
*do* get `bin/swarm:771-811`, which contains the operator-span sentence. (§B.2)

**MISS 3 — `to != "operator"` exempts the human from the existence check.** You noted there is
no throttle. You did not note that `cmd_send:986` **explicitly exempts `operator` from the
membership check that guards every other recipient** — so the human's mailbox is the one
address in the system that anything at all can write to, including a name that was never
spawned. I demonstrated this by accident (§B.1). It is a stronger fact than the one you
briefed.

**MISS 4 — WORLD.md contradicts itself about refusal.** `:59` ("nothing ever refuses a message
to the operator") vs `:66-67` (exit 100 → "nothing is queued"). Any middleware-based answer to
B trips this, and the contract needs the fix. (§B.4, §C)

---

## §G — WHAT I THINK YOU SHOULD DO (the part where I say where you're right)

You are right about more than you think, and wrong about your own evidence in two places —
both times in the direction of being *harder* on yourself than the record supports. That is
the opposite of the failure mode the last two reviews caught, and it is worth naming: **you
over-corrected.** The 4/4 and the 3-for-3 are both being used as clubs against your own
position, and neither one lands.

**Right, and I confirmed it independently:**
- The operator name was never wrong. `my_name()` stays. **No tool change on identity.** (§C)
- "Only spawn is herdr-gated" — exactly right, verified, and it means the operator's real job
  (read tree, read mail, direct, judge) works anywhere. (§F)
- The diagnosis: the bug is that **the operator does swarm-internal work itself**, not that
  the tree is misnamed. The retracted `root-1` design renamed the symptom; this names the
  disease. (§B, and RED2 §2 independently)
- No prescribed shapes. Default-~1 is a default, not a prescription, and not anticipatory. (§D)

**Wrong, and you must change it:**
1. **Stop calling it doctrine-only.** It is **doctrine (for the operator session, via
   SKILL.md — the one session that channel reaches) + enforcement (for the tree, via the
   middleware you already shipped).** Name both. The doctrine cannot bind the tree; §B proves
   the tree is *already* briefed and floods anyway.
2. **Fix WORLD.md.** Draw the authority-graph/agent-graph distinction (§C) and resolve the
   refusal contradiction (§B.4). Neither is a code change; **both are contract changes, and
   "no tool change" must not be allowed to imply "no contract change."**
3. **Strike the 4/4 and the 3-for-3.** Both are miscitations of your own evidence. (§A, §D.3)
4. **Do not ship the selection rule as phrased.** It reconstructs the flat row under good-faith
   application. Use the span test — it is already operational and already in `spawn_header`. (§E)

**The strongest sentence available to you, which is not the one you wrote:**

> The last doctrine was never falsified — it was never validly tried, because the tool made
> its target tree unrepresentable. This one is different not because the prose is better, but
> because **the operator's model is now enforceable on the only path that carries the human's
> load — and the mechanism to enforce it shipped before the design did.**

---

## §H — METHOD NOTE, AGAINST MYSELF

The brief told me two prior reviews caught the author being kind to his own hypothesis, and
one caught *itself*. So: where am I kind to mine?

**My §B rests on a middleware I wrote myself, in a scratch tree, in five minutes.** That is a
proof of *mechanism*, not of *practice*. I have shown a middleware **can** enforce the model;
I have **not** shown that a human will configure one, that fail-open (`:1029-1030`) won't
quietly disable it in production, or that escalate-to-parent is the right policy rather than
the first one I thought of. **A middleware that is not installed protects no one, and the
system's default is no middleware.** If you ship on my §B and never write the config, you have
shipped doctrine-only with extra steps — and I will have handed you a *more* comfortable story
than "doctrine-only," which is exactly the kindness I was sent here to prevent.

**The falsifier for my central finding:** configure the middleware in a real swarm, spawn a
3-deep tree, and have the grandchild report. **If the human's mailbox fills anyway** — because
fail-open swallowed a crash, because the config wasn't read, because agents route around it by
mailing a top-level agent that just forwards — **then §B's rescue is theater and the honest
verdict reverts to "doctrine-only, and it will fail the same way."** That experiment is cheap.
**Run it before you tell the human this is solved.**

I did not run it. I am telling you that plainly, because the difference between "I showed the
mechanism works" and "I showed the fix works" is the exact gap the last two reviews were
written about.
