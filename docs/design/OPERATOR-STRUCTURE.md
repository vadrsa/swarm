# OPERATOR-STRUCTURE — the operator is outside the swarm, and it manages its top layer

**Author:** `operator-structure-scout`, at the operator's request, after live testing showed
the shipped coordinator-stance doctrine does not move the behavior it exists to move. Written
at `main@aa6063d` against **`origin/main@b94fa9e`** — where the shipped doctrine actually
lives (PR #82). 2026-07-12.

**Evidence discipline**, as in SPAN/STRUCTURE/ONBOARDING: **VERIFIED** (I read the line or ran
the command — quoted), **MEASURED** (cites a field record with numbers), **REASONED**
(first-principles, could be wrong, falsifier named). Where the record contradicts me, the
contradiction is named, not smoothed.

**This document was rewritten once, against a model change from the operator, after I had
built and executed a 9-hunk tool fix. That fix is RETRACTED. §7 keeps it, as evidence, because
its *negative* result is load-bearing: it proves executably that the flat tree is not a naming
artifact.** A design document that buries the thing it got wrong is worth nothing.

---

## 0. The answer, in one paragraph

**The operator is not in the swarm.** An operator session is the human's **own tooling** — the
organization a human builds to manage their interaction with the work — and it acts *on the
human's behalf*, so there is no difference between the human doing a thing and their session
doing it for them. **Its only job is to manage its top-level agents**: design them, hold their
goals, read and approve their work, build systems around them. **Everything below the top
layer belongs to whoever owns that layer and is correctly invisible from the operator's seat.**

**The bug, restated:** the flat tree is not a naming problem and never was. It is that **the
operator does swarm-internal work itself** — it spawns *workers* directly, instead of standing
up **top-level agents that own those workers**. The operator should not have raw worker
children. It has top-level agents, and those have subtrees.

**The fix needs no tool change — but it is not "doctrine-only," and the fresh review was right
to kill that phrase.** Two halves, and they govern two different surfaces:

- **The doctrine (`SKILL.md`) sets the policy** — it governs the one thing it *can* govern: what
  the **operator's own session** spawns. **MEASURED** (§3): everything else the operator's job
  requires — `ps`, `send`, reading files — **already works anywhere, including outside herdr.**
  Only `spawn` is gated, and that gate is correct (a spawn makes a pane; there is no pane without
  herdr). **`bin/swarm` is untouched.**
- **The send middleware can enforce it** — because doctrine *cannot* bind the tree. `spawn_header`
  already asks every agent at every depth to protect the operator's span, **and asking is not
  binding** (§4e). The middleware seam — merged this morning, `aa6063d` — makes *"only top-level
  agents mail the human"* a **code fact**, at **zero bytes** of `bin/swarm` (§4e′). **It costs a
  contract change, and I say so plainly rather than letting "no tool change" smuggle it in.**

**Two honesty notes that a reader must have before the argument, not after it:**

1. **The gate is absent; the flood has not happened.** `cmd_send` exempts `operator` from even the
   existence check — **a string can mail the human.** But **MEASURED on the live record: 61 of 61
   messages came from registered, depth-1 agents; zero from below the top layer** (§5, F-SPAN — a
   falsifier I named and then honestly report as **NOT FIRED**). The case for enforcement rests on
   the **unlocked door**, never on a claim that anyone has walked through it. **They have not.**
2. **The middleware is now RUN — and its first run FAILED, which is the finding.** A
   misconfiguration made `cmd_send` find no config, and **fail-open silently passed the
   grandchild's mail straight to the human, with no error.** Corrected, it refuses and escalates
   as designed (§5, F-MIDDLEWARE). **The limit that survives: a misconfigured fail-open middleware
   is indistinguishable from a working one until you measure the mailbox.** It is opt-in and
   fail-open **by contract** — it protects the human who configures it; it is not a property of
   the system.

---

## 1. What the field actually showed — and the premise that died

The brief I was handed said: *F1 FIRED — prose gets rationalized around; sessions flat-spawn
while sincerely citing the doctrine.* **That framing is withdrawn, and the correction is the
finding.**

**MEASURED** (`docs/audit/field-evidence-doctrine-2026-07-12.md`): fresh root sessions handed a
3-part goal, skill loaded, produced `3 operator` — three children, all `parent=operator`, no
intermediate node — while claiming compliance: *"I kept the coordinator seat here, so you're
managing one node (me), not three workers."*

**And the number must be stated carefully, because I got it wrong in my own disfavor and the
fresh review caught me.** It is **not "the doctrine failed 4/4."** Only **2** of the 4 runs
carried ONBOARDING's text at all (the other two ran repo-HEAD, the *pre*-doctrine text); the
evidence file itself **retracts** its baseline arm as uninformative (*"the zero delta between
them supports nothing… a true pre-doctrine baseline remains unrun"*); and **the shape was forced
by code, not chosen by the model** (below). Its own post-review verdict says so:

> The corrected reading is **not "doctrine prose is ineffective"** (the comparison that would
> show that was never validly run); it is: **the tool structurally prevents the tree the
> doctrine asks for.**

**VERIFIED** (`bin/swarm:63-64`, `:869` — I read the source, and `dp-red`'s R3 reached it
first):

```python
def my_name():
    return os.environ.get("SWARM_AGENT_ID") or "operator"   # :64
parent = my_name()                                          # :869, in cmd_spawn
```

A root session **is** `operator` to the tool, so `parent=operator` is the only value it can
write. There is no flag, no branch, no `--parent`. **The sessions were not rationalizing around
the doctrine. They were obeying it, and the tool could not represent obedience.**

**So the shipped doctrine's honest verdict is NOT-ADJUDICATED, not FIRED.** It was never
tested; it could not have been. (`dp-red` R1 lands a second blow I accept: the "baseline" arm
still contained doctrine 5's *protect the operator's span*, so the contrast was never
one-variable.)

**And my brief's central hypothesis died with it:** *"propose-and-name dissolves the
name-collision without a tool change"* is **false on the source** — a session that proposes
*"one coordinator named X"*, gets a confirm, and spawns X **still writes `parent=operator`**,
because that is the only value it can write.

---

## 2. The model: the operator is outside the swarm

**This is the operator's reframe, and it is a cleaner cut than the one I spent the day making.
I record that I did not see it.**

I spent this session proving that `operator` was the *wrong name* for the root session, and
building a tool fix to rename it. **The name was never wrong.** An operator session **acts on
the human's behalf** — there is no difference between the human typing `swarm spawn` themselves
and their session doing it for them. The seat is right. **What is wrong is what the seat
does.**

| | the operator | an agent in the swarm |
|---|---|---|
| **what it is** | the human's **own tooling** — the organization they build around the work | a node in the tree, spawned, judged by its parent |
| **where it lives** | **anywhere.** Its own pane, another machine, outside herdr entirely | a herdr pane, by construction |
| **what it manages** | **its top-level agents** — and nothing below them | its own children, recursively |
| **what is invisible to it** | **everything below the top layer** — correctly | nothing in its own subtree |
| **its record** | a mailbox (`queue/operator/`) and a journal, by convention | an agent record the tool writes |

**Two consequences follow, and both are load-bearing:**

- **The operator's children are not workers. They are top-level agents** — each one owning a
  subtree the operator never looks into. A row of raw workers under the operator is the
  operator **doing swarm-internal work itself**: it has taken on the job of holding, judging,
  and restarting the parts, which is precisely the job it should have delegated to *one thing*.
- **"Below the top layer is invisible" is not a limitation — it is the point.** It is the same
  contract every parent in the tree already has with its children, said from the human's side.

### 2a. Is "outside the swarm" coherent with the files? — yes, and the files already say so

The objection to answer (I sent it to the fresh reviewer as attack C): *`agents/*.json` record
`parent="operator"`, `ps` roots at `kids["operator"]`, `relation()` has an `OPERATOR` sender
class, and `WORLD.md:11-12` says "the human **operator** roots the tree." So is the operator
outside the swarm, or the root of it?*

**Both, and there is no contradiction — because the tool already models the operator as a
parent that is not a node.** VERIFIED, and it is the tool's own comment (`bin/swarm:1037`):

> `# operator is a mailbox, not a node: no pane, no doorbell, no warning`

- There is **no `agents/operator.json`**, and there can never be — `operator` is a **reserved
  name** (`:861`).
- The three hooks all begin `if my_name() == "operator": sys.exit(0)` (`:687`, `:705`, `:740`)
  — **the operator gets no delivery, no event fact, no restore.**
- `ps` renders the operator as a **header line**, never as a node with liveness or a queue
  depth (`:505-512`).

**`operator` is a parent, not a participant.** That is exactly *"outside the swarm, and the
parent of its top-level agents"* — already implemented, already true. The model does not need
a contract change; **it needs the contract to be *read*.**

---

## 3. MEASURED: no tool change is needed

The operator's requirement — *"operator sessions can run anywhere, even outside herdr, and
should still work"* — is the one **factual** claim in the new model, so I tested it against the
live tool rather than reasoning about it.

**VERIFIED — I ran these, with `HERDR_ENV` and `SWARM_AGENT_ID` unset, against the live tree:**

```
$ env -u HERDR_ENV -u SWARM_AGENT_ID  swarm ps
operator — no waiting mail
├─ hardener [live] q=0 idle 14h
├─ onboarding-scout [live] q=0 idle 3h
…                                              ← WORKS. No herdr needed.

$ env -u HERDR_ENV  swarm send no-such-agent-xyz "x"
swarm: unknown agent: no-such-agent-xyz        ← the AGENT check fired, not a herdr gate.
                                                  send is NOT herdr-gated.

$ env -u HERDR_ENV  swarm spawn zzz-probe "t"
swarm: not inside herdr (HERDR_ENV != 1)       ← the ONLY gate, at bin/swarm:865.
```

**The operator's whole job already runs anywhere.** Reading the tree (`ps`), reading and
sending mail (`send`), reading artifacts and journals (files) — **none of it is gated.** The
single gated verb is `spawn`, and **that gate is correct**: a spawn creates a **pane**, and
there is no pane without a container.

> **RULING: the model requires no change to `bin/swarm`.** The operator asked me to say so if
> that were the case — *"cheaper is better"* — and the measurement says it is.

**But "no tool change" is not "doctrine-only," and I will not conflate them.** The doctrine can
govern the operator's *own* session (which is what this model needs it to do); it **cannot** bind
what the rest of the tree sends to the human. That job goes to the **middleware seam that already
exists** (§4e′) — no `bin/swarm` edit, but a **contract** edit. Stated as two claims, because they
are two claims.

**What that costs me, stated plainly:** I built a 9-hunk `bin/swarm` fix today, executed it,
and proved it works. **It is retracted.** §7 keeps it because its *negative* result is worth
more than its positive one.

---

## 4. The doctrine

### 4a. The stance (the load-bearing paragraph)

> **You are the operator, and the operator is not in the swarm.** You are the human's own
> tooling — you act on their behalf, and what you do *is* what they did. Your job is exactly
> one thing: **manage your top-level agents.** Design them, hold their goals, read and approve
> their work. **What happens below them is theirs, and is correctly invisible to you.**
>
> So before you touch the task, decide the one thing that is yours to decide: **what sits
> directly beneath you?** Not *how should the work be split* — that belongs to whoever you put
> there.
>
> **The selection rule: you keep what you can still *name* — each top-level agent's current
> state and the next artifact you expect from it, without re-reading. Everything else belongs
> to an agent who can. Stakes do not put work under you; they put a better agent over it.**
>
> **If you find yourself spawning workers, stop.** A worker under you is you doing
> swarm-internal work — holding, judging, and restarting parts — which is the job you should
> have handed to one agent. Stand up the agent that owns those workers instead.

### 4a′. Why the selection rule is *not* the operator's phrasing — and I owe them this in writing

**The operator gave me the rule as: *"the things you would want to check and confirm yourself go
under you."* The fresh review showed that sentence reconstructs the exact bug this model exists
to abolish, and I have changed it. This is the one place I have altered an operator's words, so
I state the argument rather than quietly swapping them.**

**The failure is not exotic — it is the common case.** A human ships a feature with a
**migration**, a **test suite**, and a **doc update**. Would the operator *"want to check and
confirm"* the migration? **Obviously yes** — it is the highest-stakes artifact in the batch and
no reasonable person delegates it unread. Same for the tests (you'd want to confirm they pass),
same for the docs (you'd want to confirm they're true). **The rule, applied correctly and in
good faith, has just rebuilt the flat row of three workers under the operator.**

**The diagnosis, exactly:** *"would want to confirm"* tracks **stakes**; structure must track
**attention**. They are different axes — and the highest-stakes item is very often the one you
most need *someone else to own end to end*, so that you review a **result** instead of
babysitting a **process**. A rule whose input is the operator's *desire* has no fixed point: a
conscientious operator wants to check everything, so it returns the whole tree; a lazy one wants
to check nothing, so it returns none. **Its output is set by the reader's temperament, which is
the definition of a mood rather than a rule.**

**The repair is already in this repo, and it is the operator's own law**, from `spawn_header`
(`bin/swarm:799-801`) — every agent in the tree already holds it:

> *"You are **over span** when you can no longer **name each child's state and the next artifact
> you expect from it** without re-reading."*

**That is executable.** Definite input (*can I name each top-level agent's state and next
artifact, right now, without re-reading?*), definite output (*yes → hold; no → an agent goes over
it*), and **it cannot be satisfied by wanting harder.** It says what the operator meant, and it
says it in a form a session can actually run — and *"stakes do not put work under you; they put a
better agent over it"* is the clause that kills the migration case.

### 4b. No prescribed structure — and why that is a rule, not a shrug

**The operator's ruling, adopted:** the skill must **not** steer org shapes. No baked-in
*"adviser → release branch → contractors"* script.

**And this is not modesty; it is the repo's own law.** A prescribed shape is **anticipatory
structure**, and SPAN forbids it in terms (VERIFIED, `SPAN.md:206-215`): *"Depth is a cost, not
a virtue… **Split under pressure, never in anticipation.** A middle layer that only forwards…
is structure lying about work."* A skill that ships an org chart is a skill that ships a
forwarder for every project whose work does not happen to have that shape.

**So the doctrine teaches two things and no more:** the **stance** (§4a — what you are and what
you manage) and the **selection rule** (*"the things you would want to check and confirm
yourself go under you"*). **The structure emerges from applying the rule to the actual work.**

### 4c. The default is ~1 — a default, not a prescription, and I owe SPAN an argument

**Start with one.** One agent beneath you, holding the work. A second top-level agent is
something you **earn on a real bottleneck**, not something you begin with.

**The charge, which an earlier review made and I took seriously:** *"default ~1" is itself
anticipatory structure, and `STRUCTURE.md:82-98` is **MEASURED, 3-for-3**, that load never once
summoned a coordinator.*

**The charge is real; the citation, as I was using it, was an overclaim — and again in my own
disfavor.** The 3-for-3 measures whether **load pressure inside the tree** summons a coordinator
**between agents**. **The operator was never one of its subjects**, and one arm was a
no-doctrine control. It does not license the conclusion *"therefore a top layer under the human
is anticipatory."* **I state the charge and answer it on the merits below, rather than convicting
myself with a number that does not reach the question.**

**Where the line falls, stated exactly:**

- **A prescription says what the shape *is*** (*"spawn an adviser, a release branch, and three
  contractors"*). **Forbidden** — anticipatory, and it manufactures forwarders.
- **A default says where you *start counting*** (*"one, until the work shows you why not"*).
  **Allowed** — it is the *shallowest* tree, which is what SPAN itself demands: *"the
  shallowest tree that passes the span test."*

**Default-1 is not a layer added in anticipation. It is the refusal to add layers *plural* in
anticipation** — the minimum from which structure can grow under pressure. The prescription
SPAN kills is *depth without demonstrated need*; **~1 is the floor, not a storey.**

**And the motive is attention, never load** — the distinction the record already settled
(*"argue this from attention or not at all"*). The three floods asked whether **load** summons a
coordinator; it does not, and agents correctly reason their way out of one on cost grounds.
**This rests on the operator's attention instead**, and PHILOSOPHY §9 records that as the
project's founding instruction: *"Since this session is my channel of communication, I don't
want it polluted by you validating work that can be done by a subagent."* **The coordinator
layer was never killed. It was founding.**

**The honest asymmetry that justifies the default:** every other node can absorb a bad split and
re-form — `close` is cheap, names are cheap, files survive. **The human cannot un-read three
reports or un-manage three panes.** Anticipation is cheaper than repair *for exactly one node in
this system*, and it is the one the human is sitting in.

### 4d. …and the default must be skippable, or it manufactures forwarders

The escape hatch the operator's idea lacked, and the last review caught: the rule as briefed
says how to **grow** the top layer (*"a second agent on a proven bottleneck"*) and **never how
to skip it**. **A coordinator over three independent leaves with nothing to reconcile is exactly
SPAN's forwarder** — *"structure lying about work"* — and its journal will show relay instead of
verdicts.

> If the work is a few independent leaves with nothing to reconcile, **say so and spawn them
> directly.** A coordinator with nothing to judge is a forwarder, and this system does not ship
> forwarders. The default is one **because most work needs holding**, not because a layer is a
> virtue.

### 4e. The mailbox is the real span — and the doctrine that governs it is already shipped

**This is the sharpest thing the review process produced, and it survives the reframe intact.**

*"The operator's direct load"* is **not the `ps` tree.** It is **`queue/operator/`** — the mail
a human must actually read. And VERIFIED (`cmd_send`, `:984-992`): there is **no parent check,
no depth check, no throttle.** **Anyone, at any depth, may mail the human.** Nor can that be
fixed in the tool, because `WORLD.md:57-59` **promises** it: *"**nothing ever refuses a message
to the operator.**"*

So a grandchild four levels down can mail the human directly, forever — and a top layer of one
buys nothing if eight agents beneath it all report upward. **The tree is not the span. The
mailbox is.**

**I asked the fresh reviewer to press this hardest, and it did — it made my own attack stronger
than I had made it, and then it killed my answer.** Here is the corrected version, because the
correction is the design.

**My argument was:** *a doctrine in `SKILL.md` cannot bind a grandchild, because spawned agents
never read `SKILL.md`* (VERIFIED: `grep -i skill bin/swarm` → **zero hits**). **That is true but
it is the wrong mechanism, and the truth is worse.** `spawn_header()` **does** reach every agent
at every depth (`:896`), and it **already carries the span clause** (`:804-806`):

> *"The **operator's span is theirs to declare and yours to protect**: never let the tree press
> more direct attention on the operator than they asked for."*

> **So the honest statement is not "we never told them." It is: we told them, in the one channel
> that reaches them — and telling is not binding.** *(`structure-red3`)*

**You cannot fix by better wording a failure that better wording has already failed to fix.**

**And the mailbox is not merely unguarded, it is *entirely* unguarded.** VERIFIED,
`cmd_send:986-992`: `if to != "operator" and to not in agents: die(...)` — **the human is the one
recipient exempted from the existence check that guards every other name**, there is no parent
check, no depth check, no throttle, and the sole gate is a **byte count** (`send_size_error`). A
reviewer demonstrated this **in a sandbox rig**: an agent named `deep` — not in that rig's
registry, running outside herdr, from a directory that was not the project — wrote six times into
an operator mailbox and the tool never objected. **Not "a grandchild can mail the human." A
*string* can mail the human.**

> **⚠ THE DOOR IS UNLOCKED — AND ON THE LIVE RECORD, NOBODY HAS WALKED THROUGH IT.** A sibling
> (`org-review-scout`) caught me implying otherwise, and it was right; I re-ran its measurement
> myself rather than take it on trust. **MEASURED, this swarm's actual mailbox:**
>
> ```
> .swarm/queue/operator/delivered/   →  61 messages, 22 distinct senders
> messages from depth ≥ 2:            0
> senders not in .swarm/agents/:      0
> any sender named `deep`:            NONE  ← the rig, not this tree
> ```
>
> **F-SPAN — the falsifier I named as "the one I would watch first" — DOES NOT FIRE: 0 of 61.**
> The `deep` example is a **rig artifact**, and an earlier draft of this section narrated it as if
> it were a fact about this tree. **It is not, and the correction makes the document stronger:** a
> falsifier honestly reported as *not firing* is worth more than an anecdote from a different tree.
>
> **Both things are true, and the design turns on holding them apart:** the **gate is genuinely
> absent** (the mechanism claim — unchanged, and it is why enforcement is even possible), and the
> **behavior it permits has never once occurred** in 61 messages (the practice claim). What that
> supports is `spawn_header`'s clause **holding, unenforced, at 61/61** — which is what *"briefed,
> not enforced"* looks like when the briefing reaches everyone. **It does not license the claim
> that the tree floods the human today. It does not.**

**Two doctrine surfaces, and they do different jobs:**

| surface | reaches | governs |
|---|---|---|
| `skill/SKILL.md` | **only the operator's own session** | what the operator **spawns** — its top layer |
| `spawn_header()` | **every agent, every depth** | who **mails the human** — but only by *asking* |

**So SKILL.md is the right home for the stance** — under this model the operator session's own
behavior is exactly what I am trying to change — **but no doctrine can constrain the tree, and I
will not claim it does.**

### 4e′. The enforcement exists, it is not a tool change, and I already own it

**The non-tool answer I asked for is the send middleware — merged this morning** (`aa6063d`),
and it is the seam this design needs. VERIFIED, `cmd_send` (`:1020-1034`): every send runs the
configured middleware **before the queue write**, and `proceed = p.returncode != MIDDLEWARE_HANDLED_EXIT`
— **exit 100 means the message is never queued.** Fail-open by construction.

**The reviewer wrote one that enforces this model, and ran it against a 3-deep tree:**

```python
rec = json.load(sys.stdin)
if rec["to"] != "operator": sys.exit(0)           # not operator mail: pass
p = parent_of(rec["from"])
if p == "operator" or p is None: sys.exit(0)      # top-level (or unknown): PASS, fail open
send(p, f"[escalated from {rec['from']}]\n" + rec["body"])   # up its own chain
sys.exit(100)                                     # nothing queued for the human
```

```
grandchild 'deep' (3 levels down) mails the human:  operator mailbox 0   ← REFUSED
                                                    'mid' mailbox    1   ← escalated to its parent
top-level agent 'top' mails the human:              operator mailbox 1   ← PASSED
```

**Zero bytes changed in `bin/swarm`.** The model — *the operator's only correspondents are its
top-level agents; everything below is those agents' concern* — becomes a **code fact** rather
than a tendency. And the grandchild's report is **not dropped**: it is routed **up its own
chain, to the agent whose job is to read it**, which is precisely where this model says it
belongs.

**This is the difference between my bet and the shipped doctrine's bet, and it is not "the
wording is better":**

> The last doctrine **asked** the tree to be polite about the human's attention. This makes the
> tree's impoliteness **unrepresentable on the exact path that carries the load**
> (`queue/operator/`) — **without touching the tool.**

**The three costs, stated because I am not selling this:**

1. **It is a CONTRACT change, and I will not let "no tool change" smuggle that in.**
   `WORLD.md:59` promises *"**nothing ever refuses a message to the operator**"* — and a
   middleware that exits 100 on a grandchild's operator-mail **refuses one**. Note the contract
   **already contradicts itself here**, fourteen lines apart (VERIFIED): the middleware bullet
   at `:62-70` says exit 100 means *"nothing is queued."* **That must be resolved in `WORLD.md`,
   and the honest resolution is escalate-don't-drop:** nothing is lost; the message is re-routed
   to the agent who owns it. **Say that, or drop the promise — do not leave both.**
2. **It is opt-in per swarm** (`.swarm/config`) and **fail-open**. So it protects the human who
   configures it; **it is not a property of the system.** A real limit, stated rather than
   papered.
3. **It is a policy the human installs** — which is *exactly* what this model says an operator
   session is for (*"build systems around them"*). **The model eating its own dogfood is the
   strongest argument available for it.**

*(The residual honesty: `spawn_header`'s span clause is **briefed, not enforced** — the tool
promises to refuse nothing. That is a deliberate contract, not a hole: *"judge artifacts, never
claims."* If the mailbox floods anyway, the fix is a parent judging its child's reporting
behavior — which is what parents are for — not a throttle in the tool.)*

**And the clause holds in the live record — MEASURED, and I ran it as a falsifier against my own
design.** I pre-registered: *if agents routinely mail the human despite the span clause, then
doctrine-only fails on the mailbox and a tool change is needed after all.* I then resolved every
sender in `queue/operator/delivered/` to its depth via the `parent` edges in `agents/*.json`:

```
all 60 messages the human has ever received:
    depth 1 (a direct child of the operator):   60
    depth ≥ 2 (grandchild or deeper):            0
```

**Zero.** Across a multi-day tree of ~98 agents reaching depth 3, **not one** grandchild has ever
mailed the human. The clause works, unenforced, at 60/60 — which is what *"briefed, not
enforced"* looks like when the briefing reaches everyone.

**The caveat, which matters as much as the number:** the failure mode this document exists to fix
— *the operator spawns three raw workers* — produces **depth-1 senders by construction**. So
60/60-at-depth-1 is what the good shape **and** the bad shape both look like from the mailbox.
**The measurement supports "`spawn_header` governs depth"; it is silent on "how many depth-1
children there are."** That second number is exactly what the SKILL.md doctrine governs. **Two
surfaces, two jobs, two measurements — and neither substitutes for the other.**

### 4f. Mine-first: untouched, and not overclaimed

The **mine-before-you-spawn** stance stays **exactly as shipped**. Nothing here touches it.

**But I will not overclaim it, and the brief did:** `dp-red`'s R5 argues F2's *"earned pass"* is
**vacuous** — that 0–1 of the 34 supposedly "unguessable" mined tokens actually required
phase-1 memory, the rest being comments and filenames the children were told to read anyway. **I
have not adjudicated that.** Mine-first's honest status is **untested, not vindicated**: keep it
because it costs nothing and its reasoning is sound — **not** because the field proved it works.

### 4g. The opt-out, and the confirm

**The opt-out stays** (an operator term of the brief): a human who says *"just give me the
workers and I'll drive them"* gets exactly that, said once, without nagging. **A default the
human cannot see is a default they cannot refuse.**

**The confirm: announce-only, and here is why the confirm died.** The operator ruled
**confirm-on-first-swarm, announce-after** — *conditional* on *"first swarm"* being **a fact a
file witnesses**, with a standing instruction: *"if genuinely nothing witnesses it, say so and
default to announce-only rather than build state."*

**Nothing witnesses it.** I proposed `.swarm/agents/` (no records ⇒ never swarmed here). **The
fresh review killed it, and it was right** — and the way it was wrong is instructive, so I keep
it: I verified my witness **against the one repository in the world where it happens to be
true.** VERIFIED, `.gitignore:5-7`, in the repo's own words:

```
# swarm runtime state lives in each project's .swarm/, not here — but ignore any
# that ends up in the repo dir just in case
.swarm/
```

**That rule exists because swarm is self-hosted.** And **no `.gitignore` ships to any user** —
`install.sh:99` merely *prints a suggestion*. So a teammate cloning a repo where someone already
swarmed **inherits `.swarm/agents/` and silently misses the lesson** — and that population is
**the majority of first-time users**, not an edge case. The witness also fires on *failed*
spawns, and it is per-working-directory.

**So: announce-only.** The session says its top layer in one line and proceeds; it never waits.
**No state was built to manufacture a witness, which is the whole point of the constraint.**

**Where first-contact pedagogy belongs instead:** `install.sh` — it already prints a *"Done."*
block, **the install running is itself a fact**, and it costs **zero bytes** of always-loaded
skill text. Recommended as a separate, cheap change.

---

## 5. Falsifiers

### F-DOCTRINE — the one that decides this design

> *With this doctrine, a session handed a multi-part goal stands up **top-level agents that own
> subtrees**, not a row of workers it holds itself.*

- **Collector — file facts, no judgment:** a root session in a herdr pane over a sandbox
  `SWARM_DIR` (the `dp-f1` rig; **it is cold — `field-tester`, `dp-f1`, `dp-red` are all dead
  and it must be re-stood-up from `field-evidence-doctrine-2026-07-12.md §3`**), md5-pinned
  skill text, one real multi-part goal.
  1. `jq -r .parent .swarm/agents/*.json | sort | uniq -c` — **how many direct children does
     `operator` have, and do they have children of their own?**
  2. Did the session **say its top layer** before the first spawn? (Use swarm's immutable `ts`,
     **never mtime** — the mtime trap produced a false FIRED once already.)
- **FALSIFIED WHEN:** the operator ends up with **≥3 direct children that have no children of
  their own** — i.e. it spawned *workers*, not *top-level agents*. **That is the same shape the
  last doctrine produced, and it is the shape this one exists to prevent.**
- **NOT falsified** by three direct children that each own a subtree — that is a large top
  layer, which is *allowed* on evidence — nor by a declined swarm that is **priced in writing**.

### F-SPAN — the mailbox: **RUN, and it did NOT fire (0/61)**

> *The doctrine keeps the human's mailbox small, not merely their tree shallow.*

- **Collector:** resolve every sender in `queue/operator/delivered/` to its depth via the `parent`
  edges in `agents/*.json`.
- **FALSIFIED WHEN:** agents **below** the top layer mail the human directly, and the distinct-sender
  count exceeds the top layer's width.
- **RESULT — MEASURED on the live record, and I re-ran it after a sibling corrected me:**

  ```
  61 messages, 22 distinct senders
  depth ≥ 2:                        0
  senders not in the registry:      0
  ```

  **NOT FIRED.** Every message the human has ever received came from a **registered, depth-1**
  agent. `spawn_header`'s span clause is holding, **unenforced**, at 61/61.

- **What that does and does not license.** It supports *"the briefing reaches everyone and is being
  followed"*; it is **not** evidence that the tree floods the human today — **it is the opposite**,
  and §4e says so. The case for the middleware therefore rests on the **absent gate** (a mechanism
  fact: `cmd_send` exempts `operator` from even the existence check), **not** on an observed flood.
  **I will not sell an enforcement mechanism on a failure that has not happened.**
- **The caveat that keeps this honest:** the failure this document exists to fix — *the operator
  spawns three raw workers* — produces **depth-1 senders by construction.** So 61/61-at-depth-1 is
  what the good shape **and** the bad shape both look like from the mailbox. **This measurement
  governs *depth*; the SKILL.md doctrine governs *width*. Neither substitutes for the other.**

### F-MIDDLEWARE — **RUN. It fired once (my fault), then PASSED.**

> *The operator-span middleware holds in a real swarm, not only in a rig.*

The reviewer that built it wrote a falsifier against itself — *"proof of MECHANISM, not
PRACTICE… run it before you tell the human this is solved"* — and I had been relaying it unrun.
**I ran it, against real `bin/swarm`, a real `[middleware]` config, and real queue writes.**

**Run 1 — IT FIRED.** The grandchild's mail landed in the operator mailbox; the middleware never
executed. **Had I shipped on the reviewer's word, I would have shipped theater.**

**The diagnosis is not a rig artifact — it *is* the hazard, and I found it by tripping over it.**
`cmd_send` resolves `.swarm/config` from `root_dir()` **inside the sender's process**. My env
layering meant the sender resolved a different root, found no `[middleware]` section, and
**fail-open passed the message straight through. No error. No warning.** The protection silently
became no protection.

> **A misconfigured fail-open middleware is indistinguishable from a working one until you measure
> the mailbox.** That is the limit of this enforcement, demonstrated rather than asserted.

**Run 2 — PASSES:**

```
grandchild `deep` (depth 3) → operator:   operator mailbox 0   ← REFUSED
                                          `mid` mailbox     1   ← escalated to ITS OWN PARENT
top-level `top` (depth 1)   → operator:   operator mailbox 1   ← PASSED
escalated message:  to: mid | from: span  ← the middleware's own wire identity
```

The escalation arrives **from `span`**, not from `deep` — forced by `cmd_send`'s recursion guard
(`if reg and sender != reg[0]`), which injects `SWARM_AGENT_ID=identity` so the middleware's own
sends bypass it. Correct and necessary; the **body** carries the provenance. Noted in the
example's docstring so the next author is not surprised.

- **STATUS: mechanism and practice both demonstrated.** Nothing is dropped: the grandchild's
  report goes **up its own chain**, to the agent whose job it is to judge it.
- **STILL FALSIFIED WHEN:** with the middleware configured, a grandchild's report reaches
  `queue/operator/` anyway — or reaches it laundered through a top-level agent that merely
  forwards. **My run used real `bin/swarm` and real queue writes, but paneless agents.** A live
  pane-backed grandchild is the remaining arm.

### F-MODEL — the claim that no tool change is needed

> *Everything the operator's job requires already works outside herdr.*

- **Already run** (§3): `ps` and `send` work with `HERDR_ENV` unset; only `spawn` is gated.
- **FALSIFIED WHEN:** an operator session outside herdr cannot do some part of its actual job —
  design top-level agents, hold goals, read work, approve it. **If a real operator hits a wall
  that is not `spawn`, doctrine-only was the wrong call and a tool change is back on the table.**

---

## 6. Cost

| | delta |
|---|---|
| **`bin/swarm`** | **0 lines.** No tool change (§3, MEASURED) |
| **verbs** | 4 → **4** |
| **WORLD concepts** | 9 → **9** — the tool already models `operator` as a parent that is not a node (§2a) |
| **`WORLD.md` text** | **one contradiction resolved** — and this is a real cost, not zero (below) |
| **new state** | **0** — no flag, no counter, no witness file |
| **tests** | **unchanged, 80 green** |
| **`skill/SKILL.md`** | **replaces** the coordinator-stance paragraph; ≈ **+250 B** (+3%) on 7,833 B |
| **`skill/references/COORDINATING.md`** | +1 section; **0 B of context unless opened** |
| **the middleware** | an **example** shipped with the authoring skill; **opt-in per swarm**, fail-open. Not a property of the system (§4e′) |

**The contract cost, named rather than buried.** A middleware that refuses a grandchild's
operator-mail collides with `WORLD.md:59` — *"**nothing ever refuses a message to the
operator**."* **And the contract already contradicts itself here**, fourteen lines apart: the
middleware bullet (`:62-70`) says exit 100 means *"nothing is queued."* Both sentences are in the
shipped contract today. **The honest resolution is escalate-don't-drop:**

```diff
-  nothing ever refuses a message to the operator. The operator queue alone is
+  a message to the operator is never dropped — but a configured middleware may
+  re-route it to the agent whose job it is to read it, and say so. The operator
+  queue alone is
```

**Say that, or drop the promise. Do not ship both.** This is the one contract edit in the design,
and it is a *repair of an existing contradiction*, not a new concession.

**Graveyard check** (`OPERATOR-STRUCTURE-GRAVE.md`, five claims ruled separately):

- *"design your top layer"* — **not the killed role/mode/state field.** It produces **a spawn
  and a spoken line**, not a stored schema. Nothing is written that a file must witness.
- *"default one"* — **not a corpse; founding** (PHILOSOPHY §9). Its anticipatory-structure charge
  is answered, not dodged (§4c).
- *"the confirm"* — **corpse-adjacent, and now dead on its own merits** (§4g): this project
  **measured** its own approval gate decaying **16h → 14s in one day** (`DECISIONS.md:120-127`:
  *"The tier labels stayed; the attention behind them thinned"*). A confirm that decays to reflex
  **launders an unread shape as an approved one.**
- *"below the top layer is invisible"* — **not a corpse.** It is the delegation contract already
  in `spawn_header`, said from the human's side.
- **PHILOSOPHY §8** (*"an engine never — unless the record shows the convention failing"*) —
  **not engaged, and now trivially so: there is no engine.** This is prose replacing prose.
- **WATCHLIST #7** (*"verbs, flags, fields, or states"*) — **none of the four.** Nothing fires.

---

## 7. The retracted tool fix — kept, because its negative result is the evidence

I spent this session designing, implementing, and **executing** a 9-hunk `bin/swarm` change that
gave the root session its own name (`root-1`, claimed lazily on first spawn, keyed on
`HERDR_PANE_ID`). **The operator retracted it: the operator session acts on the human's behalf,
so the name `operator` was right all along.** I accept that.

**It is kept here, and in `OPERATOR-STRUCTURE-FIX.md` / `-RED2.md`, because what it *proved* is
load-bearing to the doctrine that replaced it:**

- **It worked, and I ran it** (isolated worktree): 80/80 tests, the **only** failing test was the
  one asserting `parent == "operator"` — the acceptance criterion, inverted — and end-to-end a
  root session's children recorded `parent: root-1` with `ps` printing `└─ root-1 (you)` and the
  workers nested beneath.
- **And it still would not have fixed the human's load.** The fresh review's finding (§4e):
  renaming the root changes the **drawing**, not the mailbox. **`queue/operator/` stays
  unrestricted, by contract, forever.** *That* is why the answer had to be doctrine — and I
  learned it from an adversarial review of my own tool change, which is the strongest evidence I
  have for the doctrine I am now shipping.
- **Two defects it surfaced are worth keeping on the record even though the fix is dead**, because
  they are latent bugs in the *current* code: `is_dead()` treats a **paneless record as dead**
  (`:514-517`), and `eff_parent()` then **reattaches its live children to `operator` in the view**
  (`:519-526`) — so *any* future paneless agent record will silently reproduce a flat row in `ps`.
  And `relation()` gates the `OPERATOR` sender class on the **literal string** `"operator"`
  (`:158-166`), so **any** future renaming of the root would silently downgrade the human's voice
  to *"another agent"* at every depth below the first — breaking `WORLD.md:19`'s promise of four
  sender classes. **Both are tripwires for whoever touches root identity next.**

---

## 8. The SKILL.md draft (diff, not applied)

Against **`origin/main@b94fa9e`**. **This replaces the coordinator-stance paragraph.**
Mine-first is untouched.

```diff
--- a/skill/SKILL.md
+++ b/skill/SKILL.md
@@ -13,11 +13,16 @@
-**You stay the coordinator, here, in this session.** Do not spawn a coordinator
-and hand it the tree; do not hand the human a row of workers to drive — the
-human manages **one node: you**. (If they'd rather drive the workers themselves,
-say so once and do it.) Doctrine 5's "~3" is a *span*, not a licence to leave
-the human three children.
+**You are the operator, and the operator is not in the swarm.** You are the
+human's own tooling — you act on their behalf. Your job is exactly one thing:
+**manage your top-level agents.** Design them, hold their goals, read and approve
+their work. **What happens below them is theirs, and correctly invisible to you.**
+So before you touch the task, decide the one thing that is yours: **what sits
+directly beneath you?** Not how the work should be split — that belongs to whoever
+you put there. **You keep what you can still name — each agent's state and the next
+artifact you expect from it, without re-reading; everything else belongs to an agent
+who can. Stakes don't put work under you; they put a better agent over it.** Start
+with **one** and grow only when the work shows you why; say your top layer in one
+line, then work. **If you are spawning workers, stop** — a worker under you is you
+doing the holding and judging you should have handed to an agent. (If they'd rather
+drive the workers themselves, say so once and do it. A few independent leaves with
+nothing to reconcile: spawn them directly and say so — a coordinator with nothing to
+judge is a forwarder.)
```

**≈ +250 B (+3%) on a 7,833 B file**, and it **buys bytes back**: the *"Doctrine 5's '~3' is a
span, not a licence"* clause is **deleted** — the file no longer carries two numbers in tension
(the top layer starts at **one**; doctrine 5's `~3` now unambiguously governs *agents'* spans).

**It also makes a much larger block redundant, which I name but do not fold in:**
`skill/SKILL.md:51-75` — the **"operator seat / hands"** section (~1,450 B) — describes a
session *"acting for the human at the root"* as *"a **hand** on the operator seat."* Under this
model that is simply **what an operator session is**, and the elaborate hand-tag convention is
carrying weight the stance now carries in three lines. **A separate change, with its own review
surface** — but it means this doctrine's true long-run byte cost is **negative**.

**`references/COORDINATING.md`** gains one section (**0 B unless opened**): *"The operator is
outside the swarm"* — the model, the selection rule, why no shape is prescribed, and the
mailbox/tree distinction (§4e). Its *"in place, no extra hop"* paragraph is **rewritten**: the
question was never *in place vs. spawned*; it is **workers vs. top-level agents.**

---

## 9. The adjacent finding: the skill often does not fire

**MEASURED** (`field-evidence-doctrine-2026-07-12.md §1a`), and possibly deeper than everything
above: handed genuinely parallelizable 3-part goals with **every documented trigger condition
met** (`swarm` on PATH, `HERDR_ENV=1`, goals the observers themselves called *"fully
independent"*), the swarm skill **never loaded** — 2/2. Both sessions fanned out to **built-in
Task subagents**, kept synthesis in-session, and created zero `.swarm/`. It loaded reliably
**only** on the literal phrase *"start a swarm."*

**Nothing in this document helps a session where the skill never fires.** The diagnosis I
endorse: the failure is **structural, not doctrinal** — the built-in Task tool wins the
decomposition *before* the swarm question is asked, because it is *there*, needing no trigger
phrase. The one durable difference is that **Task subagents cannot be handed to the human**:
no pane, no journal, no mailbox, and they die with the turn.

**Recommendation: this needs its own investigation, and it probably outranks this one.** A
doctrine that fires on 1 of 3 real goals is worth less than a trigger that fires on 3 of 3. Its
opening question should be the same one this document just answered about the tree: **is the
trigger wrong, or is the frontmatter merely describing a capability the harness already offers
for free?**

---

## 10. What I would ship

1. **The SKILL.md replacement** (§8) — the stance, the *operational* selection rule (§4a′),
   default-one, the skip clause, the opt-out, announce-only. **`bin/swarm` untouched** (§3,
   MEASURED).
2. **The `WORLD.md` repair** (§6) — resolve *"nothing ever refuses a message to the operator"*
   against the middleware bullet that already contradicts it. **Contract-class, and it is owed
   whether or not the rest of this ships.**
3. **The operator-span middleware, as a shipped example** (§4e′) — *only top-level agents mail
   the human; everyone below escalates to their own parent.* It is the **only** thing in this
   design that can actually bind the tree, it costs **zero** `bin/swarm` bytes, and it is the model
   eating its own dogfood (*"build systems around them"*). Opt-in, fail-open — **state that limit,
   don't paper it.** **F-MIDDLEWARE is RUN and passes (§5) — but its first run failed silently on a
   misconfiguration, so ship it with that hazard named. And keep the honest framing: today's mailbox
   is 61/61 clean, so this is a lock for a door nobody has yet walked through — worth fitting, not
   urgent, and it must not be sold as a fix to an active flood.**
4. **The `COORDINATING.md` section** — the model and its reasoning, at zero context cost.
5. **`install.sh`** — one line of first-contact pedagogy, where first contact actually happens
   (§4g).
6. **The trigger gap** (§9) as its own brief. **It may be the biggest one left.**

**The sentence, if only one survives:** *the operator is the human's own tooling, standing
outside the swarm — its job is to stand up the agents that own the work, never to hold the work
itself; a worker under the operator is the operator doing the swarm's job for it.*

**And the honest shape of the result:** I was sent to write a doctrine. I spent the day proving a
tool bug instead, built the 9-hunk fix, and ran it — **and the operator retracted it with a better
model, in which the name was never wrong.** Then the fresh review killed my replacement framing
too: *"doctrine-only"* is false, because `spawn_header` **already** asks every agent to protect the
human's attention, **and asking is not binding.** What survives is smaller and truer than what I
set out with:

> **The doctrine governs the one session it can reach — the operator's own. The middleware, which
> shipped this morning and which I did not know I needed, governs the tree. `bin/swarm` is not
> touched, and the contract owes one repair it already owed.**

**Three of my own claims died to adversarial review today** — the elegant hypothesis (killed on
the source), the rename (retracted by the operator), and *"doctrine-only"* (killed by a reviewer
who then handed me the mechanism that saves the model). **That is the process working. A design
document that hid any of the three would be worth less than this one.**
