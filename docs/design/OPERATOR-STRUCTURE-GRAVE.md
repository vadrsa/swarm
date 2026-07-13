# OPERATOR-STRUCTURE-GRAVE — a graveyard and prior-art check on the top-layer doctrine

**Author:** `structure-grave`, dispatched by `operator-structure-scout`. Written at
`main@aa6063d`, 2026-07-12. **Verdict document; no code, no design.**

**Evidence discipline**, as in SPAN/STRUCTURE/ONBOARDING: **VERIFIED** (I read the line and
quote it), **MEASURED** (cites a field-evidence record with numbers), **REASONED** (argument,
falsifier named). Every ruling below cites the text it rests on. Where I rule against the
proposal I say so plainly; where I rule *for* it I say what the proposal must then survive.

---

## 0. THE PROPOSAL, AS I RECEIVED IT

> The operator designs and manages **ONLY its top-level agents** (the layer directly beneath
> it); below that is **invisible** to it. Before **ANY** task the operator **designs its top
> layer** (DEFAULT: one coordinator), **PROPOSES it to the human, gets a one-line confirm**,
> THEN works. No new verb, no new file, no new state, no tool change — doctrine text only,
> plus an extension of `skill/references/COORDINATING.md`.

It has **five separable claims**, and they do not live or die together. Ruling them as one
block is the mistake this document exists to prevent:

| # | claim | ruling (headline) |
|---|---|---|
| A | *design your top layer* (a design act) | **NOT a corpse.** Not the role/mode/state field. §1 |
| B | *default: one coordinator* | **NOT a corpse — it is founding.** But see the trap in §3. |
| C | *propose → human one-line confirm → then work* (the handshake) | **CORPSE-ADJACENT and the weakest limb.** §2 |
| D | *below the top layer is invisible to the operator* | **NOT a corpse — worse. A live contradiction with two shipped principles.** §4a |
| E | *extend `skill/references/COORDINATING.md`* | **The file does not exist.** §4e |

**And one finding that outranks all five** (§3c): the tool cannot represent the distinction
the doctrine is about. `bin/swarm`'s root session is *named* `operator`, so **`parent=operator`
is the only tree a root session can build.** A doctrine about "the layer directly beneath the
operator" is currently **unwitnessable** — no falsifier can collect on it, and this repo does
not ship a doctrine whose falsifier cannot be collected (ONBOARDING.md:742-743).

---

## 1. IS "DESIGN YOUR TOP LAYER" THE STATE / ROLE FIELD REBORN?

### 1a. The rulings that killed stored role/mode/state — quoted exactly

The founding kill is PHILOSOPHY §5, *"Simplicity over machinery; delete the distinction before
you configure it"*, and the record shows it **three times, each time as a removal**
(`docs/PHILOSOPHY.md:149`).

**`--standing` (the stored role flag):**
> *"The operator asked what `--standing` did, then* ***"Why do we need non-standing agents?"****,
> then closed it: **"Let's simplify things for now and only have standing agents"** — root
> L1897, L1904. Shipped as PR #12, "remove the --standing distinction." Every agent is
> standing."* — `docs/PHILOSOPHY.md:151-156`

**`trigger_mode` (the stored mode field) — the sharpest ruling, and the one the proposal must
survive:**
> *"ASK #31 proposed unifying reactive and self-paced agents "under one mechanism with a
> trigger-type field," and the operator agreed to unify. But when the implementation began to
> treat the trigger as* ***configuration****, he stopped it by recalling the actual decision:*
> **"Didn't we decide to not use trigger mode and let it be a happenstance?"** *— root L1622.*
> ***A field you set is machinery. A property that merely happens to be true of an agent … is
> not worth a schema.*** *ASK #34 … was **denied**."* — `docs/PHILOSOPHY.md:158-167`

**The test it leaves behind:**
> *"when you reach for a config field, first ask whether the thing it configures should exist
> at all. **Two modes behind a flag is usually one mode plus a decision nobody made.**"*
> — `docs/PHILOSOPHY.md:174-176`

**`--role` — deleted outright**, SIMPLEST's deletion table:
> *"| `--role`, `--self`, `--live-only`, `start`, `checkpoint --context` | Assorted
> conveniences. | Mission = the task (journal seeds with it)…"* — `docs/design/SIMPLEST.md:187`
> (confirmed dead in the shipped tool: `grep -c '\-\-role…' swarm` → 0,
> `docs/design/SELF-AUDIT.md:43`)

**A stored `span` field — killed on the exact reasoning the proposal will be measured by:**
> *"A stored per-agent `span` field is out — **it is config wearing the costume of a fact.** No
> file can witness "this agent can attend to 4"; the agent's own reconcile can witness "I can
> no longer summarize my children." … **the cap is a self-test, not a setting.**"*
> — `docs/design/SPAN.md:72-76`

**And, closest of all, a "coordinator mode" flag was pre-emptively killed by the very document
this proposal extends:**
> *"**NOT a stored "coordinator mode" flag.** Config wearing the costume of a fact — killed for
> span numbers (SPAN §2) and for trigger modes (PHILOSOPHY §5). **The stance is witnessed by
> what the session does** (does it hold the tree?), which is exactly what the collector in §5
> reads."* — `docs/design/ONBOARDING.md:244-247`

### 1b. The case FOR "it is the corpse"

Steelmanned, and it is not weak:

1. **"Design your structure" is a schema by another name.** The kills above are not really
   about the *storage medium* — they are about **an agent carrying a declared shape of itself
   that it then reasons from**. `trigger_mode: reactive` in a JSON file and "my top layer is
   one coordinator, as designed and confirmed" in a journal entry are the *same cognitive
   object*: a **declared self-description that outlives the decision that made it and gets
   reasoned from afterward**. SPAN's epitaph for the span field is precise about the failure:
   config *"invites **cargo budgeting** ("I have 2 slots left") instead of the self-test"*
   (`SPAN.md:224-226`). A confirmed top-layer design invites exactly that: *"my structure is
   one coordinator, confirmed — I do not revisit it."*
2. **It freezes what the record says must stay fluid.** The shipped doctrine says structure is
   re-decided **at every reconcile** — *"ask whether the tree still matches the remaining work
   … split what you cannot attend, absorb what no longer earns its layer"*
   (`skill/SKILL.md:20-28`). A *designed, proposed, confirmed* top layer is a structural claim
   with a **human countersignature on it**, which is the strongest possible anti-reconcile
   incentive the system could invent. Re-deciding now costs a second trip to the human.
3. **"Two modes behind a flag is usually one mode plus a decision nobody made."** The default
   ("one coordinator") plus the confirm ("or whatever the human says instead") is **exactly two
   modes behind a flag** — the flag is just spelled in English and stored in the human's reply.

### 1c. The case AGAINST — and it wins

1. **The kills are all of *stored fields the tool reads*, and every epitaph says so in its own
   words.** *"A **field you set** is machinery"*; *"config wearing the **costume of a fact**"*;
   *"a **schema** nobody reads is not a schema; it is **ceremony with fields**"*
   (`SIMPLEST.md:141`). Not one of them condemns *thinking about shape*. The proposal adds
   **no field, no flag, no schema, no file the tool reads**. There is nothing for the tool to
   branch on.
2. **The repo does not merely permit reasoning about tree shape — it MANDATES it, in the
   shipped contract, at every agent, at every reconcile.** This is the decisive quote and it
   is in the file the proposal wants to extend:
   > *"**Reconciliation asks the tree question — grow and shrink.** At every reconcile, ask
   > whether the tree still matches the *remaining* work and whether your span still matches
   > your attention: split what you cannot attend, absorb what no longer earns its layer. Could
   > what's left be parallelized or delegated — **if yes, why are you not spawning?**"*
   > — `skill/SKILL.md:20-28` (doctrine 2), and identically in every spawn header
   > (`bin/swarm:771-812`, quoted at `ONBOARDING.md:41-46`)

   And doctrine 3: *"**Judge tree shape, not just artifacts.**"* (`skill/SKILL.md:29-31`).
   **Tree-shape reasoning is not a corpse in this repo. It is doctrine 2 and doctrine 3.** A
   proposal that asks an agent to reason about its tree shape is asking it to do the thing the
   contract already tells it to do at every single reconcile.
3. **The operator's own words draw the line exactly where the proposal sits.** PHILOSOPHY §3
   quotes him dictating the reconcile loop:
   > *"It's a generic system that makes any agent **think what goal it has and what subagents
   > it has, what the state of the subagents are** … And it tries to **prove that either it
   > needs more agents or it doesn't need more agents.** … it should do something about it,
   > whether it's steering an agent in a different direction, closing the agent and opening a
   > few new ones, or whatever it would think is the correct option."* — root L1731,
   > `docs/PHILOSOPHY.md:94-100`

   That **is** "design your structure," in the operator's own dictation, and he specified it
   himself rather than choosing from options. What he **denied**, in the very same thread, was
   the *engine* to enforce it (ASK #35's *"Full reconciliation engine"* — *"It was not taken;
   the question was denied"*, `PHILOSOPHY.md:255-257`).

### 1d. RULING — and where exactly the line is

> **A design ACT is not a stored schema. The proposal's clause A is NOT the role/mode/state
> field reborn.**

**The line, stated so it can be applied to the next proposal too:**

> **The corpse is a self-description the TOOL can read and BRANCH on. The living thing is a
> judgment the agent RE-MAKES at every reconcile and can only witness by ACTING.**
>
> Three tests, all three must pass:
> 1. **Does any code read it?** (`--role`, `--standing`, `trigger_mode`, `--span`, message
>    `type` — all failed here. Clause A: nothing reads it. **PASS.**)
> 2. **Does it survive the reconcile that would contradict it?** (A stored field does — that is
>    what makes it config. A design act must not; if it does, it has become config in prose.
>    **Clause A passes ONLY under the amendment in §1e.**)
> 3. **Is it witnessed by the artifact, or by the declaration?** (SPAN's whole distinctive move:
>    *"the cap is a self-test, not a setting"* — the file cannot witness "I can attend to 4";
>    the reconcile can witness "I can no longer summarize my children." Clause A's witness is
>    the spawn record itself + the journal entry. **PASS** — and note the repo has already
>    accepted exactly this witness for the *mine-first* decomposition,
>    `ONBOARDING.md:194-199`, whose destination-in-the-journal is called *"the single most
>    load-bearing string in the file"*, `:371`.)

**The failing test is #2, and it is a real defect in the proposal as written, not a
technicality.** "Before ANY task the operator designs its top layer, proposes it, gets a
confirm, THEN works" is a **one-shot up-front design act with a human countersignature**. That
is not the reconcile loop; that is a **plan**, and a plan with an approval stamp on it is the
thing an agent will not revisit. SPAN is explicit that this direction is wrong:
> *"**Depth is a cost, not a virtue** … the shallowest tree that passes the span test.
> **Split under pressure, never in anticipation**; absorb eagerly on the way down."*
> — `docs/design/SPAN.md:206-215`

### 1e. The amendment that saves clause A (and it is one clause)

The design act survives — **as a reconcile, not as a plan.** Concretely: the doctrine must say
the top-layer design is **re-made at every reconcile like every other tree question**, and that
the confirmed shape carries **no authority against a later reconcile**. Without that sentence,
clause A is not the stored-field corpse — it is a **new** corpse: *the frozen plan*, held in
place by a human signature. With it, clause A is doctrine 2 pointed at the root, which is
exactly the gap ONBOARDING §1 identified (*"the doctrine reaches the whole tree and skips its
root"*, `ONBOARDING.md:36`).

---

## 2. THE HUMAN-CONFIRM HANDSHAKE — GUARDRAIL OR INSTRUCTION?

### 2a. PHILOSOPHY §2, quoted in full where it bites

> *"Asked how aggressively to enforce checkpoint-writing via a `Stop`-hook that exits nonzero,
> the operator initially said "Hard enforcement from the start" (ASK #29) — and then, within
> the same thread, abandoned enforcement entirely for something better:*
>
> > **"I think the model should be simpler, the agent should just know that it has to update
> > its checkpoint. Then the gameabolity concern is solved by the parent naturally pinging the
> > subagent… We need to setup the right incentives with the goal tracking - recursive goal
> > reconcilliation is gonna be the answer."** *— root L1671*
>
> *Note what is being rejected. Not the goal of reliable checkpoints — **the mechanism of
> forcing them.** A hook that blocks an agent until it writes a file produces a written file,
> not a reconciled agent; it is trivially gamed by writing anything. …*
>
> ***The test this gives you: before adding a guardrail, ask who is incentivized to notice if
> it is missing. If someone already is, the guardrail is ceremony. If nobody is, fix the
> incentive, not the guard.***"
> — `docs/PHILOSOPHY.md:51-83`

**And the second half, which is the one that actually fires here:**
> *"When the session pushed once more on how far to go to enforce a prompt-only convention …
> the operator **denied the question outright and said `STOP`** (ASK #25). **The question had
> already been answered; asking it again in mechanism-flavored clothing was not welcome.**"*
> — `docs/PHILOSOPHY.md:73-76`

### 2b. Is the handshake a guardrail?

**Mechanically, no — and this must be conceded before the real objection lands.** A guardrail
in this repo's vocabulary is *a thing that blocks*: a Stop-hook that exits nonzero, a spawn that
refuses child N+1, a `swarm ask` that rejects a malformed message. **The proposal has no
blocker.** It is prose telling a session to do something before it does something else. On the
literal PHILOSOPHY §2 test — *"who is incentivized to notice if it is missing"* — the answer is
**the human**, who is sitting right there and will notice immediately that nobody asked them
anything. So it is not ceremony by that test either.

**And the repo HAS shipped pre-flight duties. The task asked me to find them, and they are
real:**

| pre-flight duty | shipped where | controversial? |
|---|---|---|
| **"Take the seat before acting."** Write a seat-take entry with a hand tag, *then look before touching:* `swarm ps`, the operator journal, the mailbox. | `skill/SKILL.md:59-63` (live, on disk) | **NO — quiet.** INBOX calls it *"just approved… both text, both operator-owned"* (`INBOX.md:176-181`). Field-validated: the crash alarm fired as designed (`docs/audit/field-evidence-2026-07-10-operator.md:78-90`). |
| **"HARVEST before you close"** — read the child's journal and artifacts first. | `skill/SKILL.md:35-36`, doctrine 4; and `WORLD.md:40-42` | **NO — quiet.** Contract-class, shipped without argument. |
| **"Claim mail, then act."** Move the file AND write a hand-tagged claim line, *then* act. | `skill/SKILL.md:73-77` | **NO — quiet**, and its *absence* is the designed alarm. |
| **"Mine before you spawn"** — read back over the session, write the decomposition into your journal *before the first spawn*. | `docs/design/ONBOARDING.md:342-348` — **DRAFT, NOT APPLIED** | **YES — the most-argued pre-flight duty in the record.** Survived a "this is a cache, save the goal not the context" objection called *"the sharpest objection in the set"* (`ONBOARDING.md:593-599`); its helper verb was **refused** (`:93-96`); and its field test came back **VACUOUS** (`…-RED.md:478`). |

**So: "the session must do X before acting" is an established, uncontroversial shape here.** It
has shipped three times. The proposal is not asking for a new *kind* of thing.

### 2c. The objection that actually lands — and it is not §2

**The handshake's problem is not that it guards. It is that it BLOCKS ON THE HUMAN, and this
system's entire contract says the human does not answer.**

> *"**The operator is a mailbox, not a node.** Messages to `operator` wait until the human
> looks; `ps` shows them waiting. **Nothing pushes to the human**, and nothing ever refuses a
> message to the operator."* — `WORLD.md:57-61`

Every other pre-flight duty in the table above is **executable by the session alone, in the next
second, with no other party**. Take the seat: write an entry, run `ps`. Harvest: read a journal.
Claim mail: move a file, write a line. Mine: read your own context, write your journal. **Every
one of them terminates inside the agent.** The proposed handshake is the **only** pre-flight
duty in the history of this repo that **cannot complete without a second party who the contract
says is asleep.**

And the record has already MEASURED what happens to gates that wait on this human:

> *"**The gate collapsed into standing authorization within a day:** #65–#68 waited **16–17h**
> for the human's session (then merged as a batch 26 seconds apart); #72/#73, contract-class,
> got 2.8h; #74, also contract-class, was merged under pre-auth in **14 seconds**; #76/#78 in
> **3–4s** (MEASURED, pr-miner §c "tier drift"). **The tier labels stayed; the attention behind
> them thinned.**"* — `docs/design/DECISIONS.md:120-127`

That is the fate of the "one-line confirm," predicted from this repo's own data: **the human
will type "yes" in three seconds without reading, and the doctrine will have purchased a
ritual.** DECISIONS says so in its own summary: *"imagines **already runs as informal pre-auth**,
its contract-class attention collapsed 16h → 14s in a day, unrecorded"* (`DECISIONS.md:589-591`).

And the corroborating structural fact, MEASURED over the whole corpus:
> *"**Genuine human judgment, wherever the record shows it, is an initiation or a correction,
> never a gate answer**: rejected the overseer agent, "recon should shrink", R1/R2, the
> choice-doctrine process correction, "decision POINTS, not questions"."*
> — `docs/design/DECISIONS.md:130-134`

**The human in this record does not answer gates. He initiates and he corrects.** A doctrine
whose central move is "get a one-line confirm" is asking him for the one speech act the entire
two-day corpus shows he does not perform.

### 2d. RULING on clause C

> **The handshake is NOT a guardrail in PHILOSOPHY §2's sense — it blocks nothing and the
> incentive test passes. It is a legitimate instruction of a shape this repo has shipped three
> times. But it is the weakest limb of the proposal, and it should be CUT or WEAKENED, on
> different grounds than the ones I was pointed at:**
>
> 1. **It is the only pre-flight duty in the repo that cannot complete inside the agent**
>    (`WORLD.md:57-61` — the operator is a mailbox; nothing pushes to the human).
> 2. **This repo has MEASURED the decay of exactly this gate: 16h → 14s in one day, "the tier
>    labels stayed; the attention behind them thinned"** (`DECISIONS.md:120-127`). A confirm
>    that decays to reflex is *worse than nothing* — it launders an unread shape as an approved
>    one, which is the "obedience theater" this system stores no state for on purpose
>    (`SPAN.md:19-23`).
> 3. **A latency SLO on the human was explicitly refused** for the same reason: *"No latency
>    SLO on pass-throughs. … making "open" uncomfortable rebuilds the nag"*
>    (`DECISIONS.md:495-496`).
>
> **The version that survives** is the one the repo already ships for the opt-out: **state the
> shape, once, and proceed** — *"the session says so plainly once rather than nagging"*
> (`ONBOARDING.md:180-183`); the human's *"authority to say no"* is preserved without a gate
> (`ONBOARDING.md:613-634`). **Announce, don't ask.** A human who wanted something else says so
> — that is an *initiation/correction*, which is the speech act the record shows he actually
> performs. This costs nothing the proposal wanted and removes the one clause the record
> predicts will rot.

---

## 3. THE COORDINATOR LAYER — KILLED, OR FOUNDING?

The task asked me to reconcile two rulings that appear to contradict. **They do not contradict.
They are about two different things, and the distinction is load-bearing.**

### 3a. FOUNDING — the coordinator LAYER (the human's direct load is one node)

> *"The operator's **second instruction in the entire project**: **"Since this session is my
> channel of communication, I don't want it polluted by you validating work that can be done by
> a subagent. What other options do we have to keep this session clean?"** — root L31.
> **That question created the chief-of-staff (ASK #2).** The operator's attention is treated as
> the scarcest resource in the system — scarcer than tokens."* — `docs/PHILOSOPHY.md:270-278`

ONBOARDING §6.1 rules on this explicitly, and its sentence is the one to quote:
> *"A flat tree the human hand-manages **is** that channel pollution. **The coordinator layer
> was never killed; it was founding.** … This is a restoration, not an invention — **and it is
> argued from attention, never from load.**"* — `docs/design/ONBOARDING.md:586-591`

### 3b. KILLED — the coordinator PANE (a separate spawned node between human and workers)

> *"**NOT a separate spawned coordinator pane.** §3a — a forwarding layer, condemned by SPAN
> §3d, and one hop of fidelity loss for zero judgment added."* — `docs/design/ONBOARDING.md:238-240`

resting on:
> *"A middle layer that only forwards — adds no judgment, writes no synthesis — **is structure
> lying about work**, and its parent should close it (the anti-forwarder test: a coordinator's
> journal must show artifact reads and verdicts, not relay logs)."* — `docs/design/SPAN.md:212-215`

and on the anticipatory-structure rule:
> *"the shallowest tree that passes the span test. **Split under pressure, never in
> anticipation.**"* — `docs/design/SPAN.md:206-215`

ONBOARDING's §6.5 answer is the exact hinge, and I quote it because the proposal must land on
the right side of it:
> *"**It adds no layer, and this is the load-bearing reply.** ***In place*** *means the node
> count is **unchanged**: the human's session exists either way, and the only question is
> whether it delegates or grinds. There is no new rung, no forwarder, no hop of briefing
> fidelity — **which is also precisely why the design refuses a separate spawned coordinator
> pane (§3c), because THAT version would be the anticipatory layer SPAN condemns.**"*
> — `docs/design/ONBOARDING.md:658-665`

### 3c. WHICH RULING GOVERNS — and the trap the proposal is standing in

**Both govern, and they cut the proposal in half:**

- **"DEFAULT: one coordinator" as a description of the human's direct load being ONE NODE, and
  that node being THE SESSION ITSELF, IN PLACE** → **founding** (PHILOSOPHY §9, ONBOARDING §6.1).
  Not a corpse. Restoration.
- **"DEFAULT: one coordinator" as the operator SPAWNING a coordinator child and handing it the
  tree** → **the killed shape, by name** (ONBOARDING §3c, SPAN §3d). Anticipatory structure, a
  forwarding layer, and one hop of briefing fidelity for zero judgment added.

**The proposal's own wording does not tell me which one it means, and that ambiguity is its
single most dangerous property.** *"The operator designs and manages ONLY its top-level agents
(the layer directly beneath it)"* reads naturally as: *the operator spawns a coordinator; the
coordinator manages everything else; the operator sees only the coordinator.* **That is the
corpse.** It is `NOT a separate spawned coordinator pane` verbatim.

If instead it means *the human's session IS the coordinator, and it keeps its own direct
children few* — that is not a "top layer" doctrine at all; **it is the span test**, already
shipped (`skill/SKILL.md:40-49`, doctrine 5), and the proposal adds nothing but a restatement.

### 3d. DID ANYTHING CHANGE? — the "in-place version FAILS 2/2" claim, checked

**My parent's brief asserts field evidence proving the in-place version FAILS 2/2. I checked it,
and the claim does not survive contact with the record.** This is the single most important
correction in this document, because a "the ruling changed" argument is what would license
re-raising the killed pane — and the licence is not there.

**What the field evidence actually says (MEASURED, `docs/audit/field-evidence-doctrine-2026-07-12.md`):**

The shape-fact **did** fire — 4/4 runs, not 2/2: *"in every run where the skill loaded … the
observer spawned **3 children with `parent=operator`, flat**"* (`:30-33`). But **the adversarial
review flipped the reading**, and the corrected record is unambiguous:

> *"**[R3 — the probe's real prize] `parent=operator` is the only tree a root session can
> build.** `bin/swarm` `my_name()` returns `SWARM_AGENT_ID or "operator"`, and a pristine root
> session has no `SWARM_AGENT_ID` — so **every spawn it makes records `parent=operator`
> unconditionally. This is not a model illusion; it is a hard-coded default.** WORLD.md says
> "the operator is a mailbox, not a node"; the code makes `operator` the root session's own
> name. **The contract and the code contradict each other, and the observers reasoned CORRECTLY
> from what the tool represented:** their sincere claims ("you're managing one node: me")
> describe the tree they meant and **the tool cannot record**."*
> — `docs/audit/field-evidence-doctrine-2026-07-12.md:37-46`

> *"**[R1 — baseline arm RETRACTED as uninformative.]** The repo-HEAD text I used as
> "pre-doctrine" already carries the 5-point doctrine including operator-span protection … so
> **both arms contained the treatment and the zero delta between them supports nothing.**"*
> — `:53-59`

> **Verdict:** *"falsifier 1 **FIRED as a shape-fact** … but the corrected reading is **not
> "doctrine prose is ineffective"** (the comparison that would show that was never validly run);
> it is: **the tool structurally prevents the tree the doctrine asks for.** **The fix is
> therefore contract/tool repair, not more prose** … **The doctrine-prose question can only be
> re-asked after that repair.**"* — `:77-84`

And the RED review says it flatly:
> *"Because it is a tool default, **no amount of prose can fix it.** A session that fully
> understood the doctrine, wanted a coordinator layer, and tried to build one **would still
> write `parent=operator` for its first child**, because it has no way to name itself anything
> else. **The doctrine was never given a chance to fail or succeed.**"*
> — `docs/audit/field-evidence-doctrine-2026-07-12-RED.md:170-178`

**RULING on part 3:**

> **The in-place doctrine did NOT fail 2/2. It was never validly tested.** The record's own
> corrected verdict is that (a) the baseline arm is **retracted as uninformative** because it
> contained the treatment, and (b) `bin/swarm:64` makes the doctrine's target tree
> **unrepresentable**, so the probe *"was never given a chance to fail or succeed."*
>
> **Therefore nothing has changed that licenses reopening the killed coordinator pane.** The
> ruling that governs is still ONBOARDING §3c / SPAN §3d: **a separately spawned coordinator
> between the human and the workers is anticipatory structure and a forwarding layer.** The
> founding ruling (PHILOSOPHY §9) blesses the *layer* — the human's direct load being one node
> — and ONBOARDING §6.5 already discharges it **without a new node** by putting the session
> itself in the seat.
>
> **And the fix the record actually asks for is not a doctrine at all.** It is
> `docs/audit/field-evidence-doctrine-2026-07-12.md:81-84`: *"give root sessions their own name
> (make the flat-row-under-human unrepresentable), or have `swarm spawn` warn/refuse on
> `parent=operator` from a root spawner."* **A doctrine shipped now, on top of a tool that
> cannot represent its subject, is prose that cannot be collected on** — and this repo's
> standard is explicit: *"A doctrine whose falsifier cannot be collected is one this repo does
> not ship"* (`ONBOARDING.md:742-743`).

---

## 4. WHAT ELSE IN THE GRAVEYARD DOES THIS RE-RAISE?

### 4a. "Below the top layer is INVISIBLE to the operator" — **NOT a corpse. Worse: a live contradiction.**

I searched for a prior kill of an encapsulation/abstraction boundary and found **NO HITS** —
nobody has ever proposed this. **That is not a clean bill of health.** It is virgin ground that
runs directly into two *shipped, live* principles:

> *"Autonomy is bounded by **structure, not permission**: **seeing is global** (`swarm graph`
> shows the whole society), but acting is local."* — `docs/PHILOSOPHY.md:196-199`

> *"**Judge tree shape, not just artifacts.** When you judge a child's work, **judge its
> delegation too**: a child grinding through parallelizable work serially is off-track and
> should hear it from you."* — `skill/SKILL.md:29-31` (doctrine 3)

> *"`ps` — **the one view**: the living tree … Without a view, **seeing-is-global is a
> slogan.**"* — `docs/design/SIMPLEST.md:93-94`, `:143-145`

**Doctrine 3 is not compatible with "below the top layer is invisible to me."** To judge a
coordinator's delegation, you must see what it delegated. The proposal's own parent duty —
*"When you judge a child's work, judge its delegation too"* — **requires looking one level past
your children.** And this very swarm's brief (mine, and my parent's) says it in the spawn
header: *"When you judge a child's work, judge its delegation too."*

**RULING:** clause D is the one clause that is **not** a graveyard problem and **is** a doctrine
collision. It must be reworded from a **visibility** claim to an **attention** claim, which is
what SPAN actually says:

- ✗ *"below that is invisible to it"* — contradicts seeing-is-global and doctrine 3.
- ✓ *"below that is not yours to manage"* — this is just SPAN §3a, already shipped: you judge
  your children; **they** judge theirs. Seeing stays global; **managing** is local. That is
  PHILOSOPHY §6's sentence, unchanged, and it costs zero new concepts.

### 4b. A "planning phase" / design-then-execute gate — **partially a corpse, and the closest live analogue came back VACUOUS**

The nearest prior art is **mine-first** (`ONBOARDING.md:194-199`), which is a *journal-a-plan-
before-you-spawn* duty. It is **drafted, not shipped**, it was the most-contested item in the
record, and **its field test could not discriminate:**

> *"**VACUOUS.** Collector has no power: 33–34 of 34 tokens are `cat`-able (R5), the
> decomposition was in the prompt, no cold control arm was run…"*
> — `docs/audit/field-evidence-doctrine-2026-07-12-RED.md:478`

> *"A test whose FIRED and NOT-FIRED conditions produce identical observations has **zero
> power**, and "NOT-FIRED" from it is not a pass — earned or otherwise."* — `…-RED.md:284-288`

**RULING:** a "plan before you work" duty is **not dead** (it is drafted and defensible), but
**the repo's one attempt to prove such a duty works produced a test with zero power.** The
proposal inherits that liability exactly. Its falsifier must discriminate a session that
designed its top layer from a session that would have built the same tree anyway — and given
§3c (the tool can only build one tree from the root), **no such collector currently exists.**

### 4c. An approval gate — **NO PRIOR PROPOSAL, and the one real gate in the record DECAYED**

Covered in §2c. **NO HITS** for a pre-work human approval gate ever being proposed. The merge
gate — the only human gate the record has — **collapsed 16h → 14s in a day**
(`DECISIONS.md:120-127`), and the record's summary of human behavior is that judgment appears as
*"an initiation or a correction, **never a gate answer**"* (`:130-134`).

### 4d. A mode flag — **corpse, and it does not apply.** The proposal has no field, no flag, no
stored state. ONBOARDING already litigated this exact charge for the opt-out clause and won:
> *"**Rejected — the objection does not bite** … PHILOSOPHY §5 kills *"a field you set"* and
> *"two modes behind a flag."* **There is no field and no flag here.** … **The philosophy kills
> *machinery*; it does not kill *the human's authority to say no*.**"* — `ONBOARDING.md:613-634`

And it records a lesson aimed squarely at documents like mine:
> *"(This document's own graveyard scout advised cutting it outright on §5 grounds, quoting the
> very journal line that specifies it — **an object lesson in how a corpse-hunt can find a
> corpse that isn't there.**)"* — `ONBOARDING.md:631-634`

**I have tried not to repeat that error, and I want the operator to notice where I have refused
to:** I am ruling *for* the proposal on clauses A, B (in-place form), and against §5 as a
charge against any of it.

### 4e. "An extension of `skill/references/COORDINATING.md`" — **the file does not exist**

**VERIFIED.** `skill/` contains exactly one file: `SKILL.md`, 106 lines, the pre-ONBOARDING
version. `skill/references/` **is not on disk.** ONBOARDING §4 — including the entire two-file
split, the `COORDINATING.md` companion, and the two inline stances — is a **DRAFT, NOT APPLIED**
(ONBOARDING's own heading says so: *"## 4. The two-file split (drafts, not applied)"*, `:255`).

**The proposal is therefore not "an extension of an existing reference." It is a co-dependency
on an unshipped draft.** If ONBOARDING lands first, this proposal is an edit to it and must be
reconciled with it clause by clause (it *contradicts* ONBOARDING §3c on the coordinator pane —
see §3c above). If ONBOARDING does not land, this proposal is proposing to create the file, and
its byte cost is the full one, not a delta.

**And the byte cost is not free — the operator has already objected to it once:**
> *"**The number the operator objected to, honestly framed: 19.5% → 15.0%.** That is a real cut
> but a modest one, and I will not oversell it."* — `docs/design/ONBOARDING.md:451-453`

The standing law the proposal must satisfy:
> *"**INLINE:** anything whose absence changes what the session **does**. **REFERENCE:** anything
> that only makes a reader **agree** with what it already does. **And no falsifier may collect on
> an artifact that a reference-only instruction produces.**"* — `docs/design/ONBOARDING.md:299-301`

**This kills the proposal's chosen vehicle outright.** *"Before ANY task the operator designs
its top layer, proposes it, gets a confirm, THEN works"* is **pure instruction whose absence
changes what the session does**, and any falsifier collects on the artifact it produces.
**By ONBOARDING's own split rule, it CANNOT live in `references/COORDINATING.md`.** It must go
**inline in `SKILL.md`** — the hottest file in the repo, the one whose growth the operator has
already refused once. The proposal's "no new file, just a reference extension" framing
**understates its true cost by placing load-bearing instruction in a file that may never be
read.**

### 4f. An onboarding ceremony — **shipped three times, uncontroversially** (see the table in §2b).
Clause A's *form* (a pre-flight duty producing a journaled artifact) is well-precedented. Only
its *human-blocking* half (clause C) is novel, and §2d rules on it.

---

## 5. WATCHLIST — WHICH TRIGGERS FIRE?

### #7 Scope creep — **DOES NOT FIRE on the letter; the operator should not be told it does**

> *"## 7. Scope creep in the rewrite itself (the disease that built the 27)*
> *- **WATCH:** the new tool growing **verbs, flags, fields, or states** the design does not
> name. Every concept in the current system was added by someone with a reason that sounded
> local and sane.*
> *- **TRIGGER:** **any addition that cannot point to a WATCHLIST entry whose trigger fired.***
> *- **SIMPLEST FIX:** this file is the fix. **An addition with no fired trigger behind it gets
> reverted**, and the urge behind it gets written here as a new entry with a falsifier
> instead."* — `docs/design/WATCHLIST.md:99-108`

**Two readings, and I must be honest that they disagree:**

- **The WATCH line does not fire.** It is scoped to *"verbs, flags, fields, or states"* — the
  proposal has **none of the four**. ONBOARDING already made and won this argument:
  *"note #7 is scoped to "the new tool growing verbs, flags, fields, or states" (VERIFIED,
  `WATCHLIST.md:106`), and this addition has none of the four. **It is prose, and prose is the
  one thing this repo's philosophy says to try first.**"* (`ONBOARDING.md:757-761`).
- **The TRIGGER line DOES fire, read literally.** *"Any addition that cannot point to a
  WATCHLIST entry whose trigger fired."* **The proposal points to no fired WATCHLIST trigger.**
  Neither did ONBOARDING, and it said so:
  > *"the trigger I am pointing at is **the operator's own observation of two real adoption
  > failures** — not a measured audit. **No document in this repo quantifies the human's
  > hand-management burden.** That observation is the entire evidentiary basis for the default,
  > **and I will not oversell it as more.**"* — `ONBOARDING.md:647-652`

**RULING on #7:** it fires **as a caution, not as a veto** — the same standing the operator gave
ONBOARDING. But the proposal is **strictly worse positioned than ONBOARDING was**, on the
evidence: ONBOARDING at least pointed to two *watched* adoption failures. **This proposal points
to a field result (§3d) that the record has already retracted, and it proposes to fix by prose a
failure the record says prose cannot fix.**

### Other entries

- **#4 (journals rot into mush)** — **does not fire**, but is the entry to write the proposal's
  urge into if it is deferred. Its FIX line is the template: *"a convention made visible in the
  file itself, not a schema, not validation."*
- **#6 (operator-bound questions stay malformed)** — **relevant, and it cuts against clause C.**
  Its subject is exactly the human's queue: *"questions in your queue you cannot decide from
  their own text; **your own answering latency as the proxy**"* (`WATCHLIST.md:87-97`). A
  mandatory pre-task confirm **adds one message to the operator's queue per task, forever** —
  and #6's simplest fix is a wrapper that **refuses to send** malformed operator mail. **The
  proposal's handshake is an unconditional new stream into the queue that #6 exists to protect.**
- **#7's own SIMPLEST FIX is the recommendation I am making in §6:** *"the urge behind it gets
  written here as a new entry with a falsifier instead."*

---

## 6. THE VERDICT, CLAUSE BY CLAUSE

| clause | ruling | grounds |
|---|---|---|
| **A. "the operator designs its top layer"** (a design act) | **NOT A CORPSE — SHIP IT, amended.** It is doctrine 2 (`skill/SKILL.md:20-28`) pointed at the root, which is the exact gap ONBOARDING §1 found. **Amendment required:** say it is **re-made at every reconcile**, not designed once. Without that clause it is a NEW corpse — *the frozen plan*, and SPAN says *"split under pressure, never in anticipation"* (`SPAN.md:206-215`). | §1d, §1e |
| **B. "DEFAULT: one coordinator"** | **NOT A CORPSE — IT IS FOUNDING**, *if and only if* it means **the human's session, in place**. *"The coordinator layer was never killed; it was founding"* (`ONBOARDING.md:586-591`). **If it means a SPAWNED coordinator pane, it is the killed shape by name** (`ONBOARDING.md:238-240`). **The proposal's wording does not say which, and it must.** | §3 |
| **C. "propose → one-line human confirm → then work"** | **CUT IT.** Not a guardrail (§2 test passes), and pre-flight duties are well-precedented (3 shipped) — but it is **the only one that blocks on a party the contract says is asleep** (`WORLD.md:57-61`), and this repo **MEASURED** the identical gate decaying **16h → 14s in one day**, *"the tier labels stayed; the attention behind them thinned"* (`DECISIONS.md:120-127`). Human judgment here is *"an initiation or a correction, **never a gate answer**"* (`:130-134`). **Replace with: announce the shape once, then work.** | §2d |
| **D. "below the top layer is invisible"** | **REWORD OR CUT.** Not a corpse — a **live contradiction** with `PHILOSOPHY.md:196-199` (*"seeing is global"*) and doctrine 3 (*"judge tree shape… judge its delegation too"*, `skill/SKILL.md:29-31`). Say **"not yours to MANAGE"** (already shipped, zero cost), never **"invisible to you."** | §4a |
| **E. "extend `skill/references/COORDINATING.md`"** | **THE FILE DOES NOT EXIST** (VERIFIED — `skill/` holds one 106-line `SKILL.md`; ONBOARDING §4 is *"drafts, not applied"*). And by ONBOARDING's own split rule (`:299-301`), **load-bearing instruction MAY NOT live in a reference** — so the real vehicle is **inline SKILL.md**, whose growth the operator has already refused once at +19.5% and grudgingly accepted at +15.0%. **The proposal understates its cost.** | §4e |

### The overriding finding, which outranks every clause above

**The tool cannot represent the thing this doctrine is about.** `bin/swarm`'s `my_name()`
returns `SWARM_AGENT_ID or "operator"`, so a root session's every spawn records
`parent=operator` **unconditionally** — *"not a model illusion; a hard-coded default"*
(`field-evidence-doctrine-2026-07-12.md:37-46`). **"The layer directly beneath the operator"**
is therefore **the only layer a root session can create**, and the distinction between "operator
→ coordinator → workers" and "operator → workers" **cannot be written to disk from a root
session at all.** The record's own conclusion:

> *"**The fix is therefore contract/tool repair, not more prose** … **The doctrine-prose
> question can only be re-asked after that repair.**"* — `:81-84`
>
> *"Because it is a tool default, **no amount of prose can fix it.**"* — `…-RED.md:170-178`

**RECOMMENDATION TO `operator-structure-scout`:** the proposal is **not a corpse** — three of its
five clauses are live, and one (B, in-place) is *founding*. But it is **premature by one
repair**. Ship the tool fix the field evidence asks for (`give root sessions their own name`, or
`warn/refuse on parent=operator from a root spawner`) **first**; then clause A becomes
collectable, clause B becomes representable, clause D becomes unnecessary, and clause C can be
dropped without loss. Doctrine written before that repair is **prose whose falsifier cannot be
collected — and this repo does not ship those** (`ONBOARDING.md:742-743`).

---

## 7. WHAT WOULD FALSIFY THIS DOCUMENT

Committed, in the discipline this repo demands of every design it accepts:

1. **`skill/references/COORDINATING.md` exists.** If ONBOARDING's §4 diff lands before this is
   read, §4e's headline is wrong and clause E is an ordinary edit. (Checkable in one `ls`. It
   did not exist at `main@aa6063d`, and I ran the check.)
2. **`bin/swarm` gains a root-session name.** If the `parent=operator` default is repaired, the
   overriding finding evaporates and the proposal is merely *early*, not *uncollectable*. This
   is the falsifier I most expect to fire, and I would welcome it — it is the recommendation.
3. **A human confirm that does not decay.** If the operator answers pre-task shape proposals
   with substantive corrections over ≥5 tasks (not "yes"), then §2d's decay prediction — drawn
   from the merge gate's 16h→14s collapse — is wrong for *this* class of question, and clause C
   is a live instruction rather than a ritual-in-waiting. Collector: read the operator journal's
   dispatch entries for confirms that changed a shape.
4. **A coordinator pane that judges.** SPAN §3d's anti-forwarder test is the discriminator I
   leaned on to keep the pane dead: *"a coordinator's journal must show artifact reads and
   verdicts, not relay logs"* (`SPAN.md:212-215`). If a spawned coordinator's journal shows real
   verdicts on artifacts it read, then the killed pane was killed on a prediction that failed,
   and §3's ruling must be reopened. (Note: **this swarm is that experiment.** My parent
   `operator-structure-scout` is a coordinator between the human and me. Whether its journal
   shows verdicts or relay logs is the cheapest available test of the ruling I just wrote — and
   the operator can run it in ten seconds.)

---
---

# PART II — THE TOOL FIX (added 2026-07-12 16:5x, after the lock lifted)

**Brief changed mid-flight.** The operator lifted the doctrine-only lock
(`.swarm/journal/operator.md:189`: *"Operator lifted the no-tool-change lock -> structural
fix (root gets distinct name, OR spawn-guard on parent=operator) designed WITH the
doctrine, contract-class"*). The proposal is now **two things**, and Part I above rules on
the first. This part rules on the second — questions 6–9 — as a graveyard check, which is
my lane and the only thing I claim authority on.

**What I found that changes how to read this part:** `docs/design/OPERATOR-STRUCTURE-FIX.md`
and `docs/design/OPERATOR-STRUCTURE-RED.md` **already exist**. My siblings have designed the
fix and red-teamed it. **I am therefore not designing anything; I am checking the fix against
the graveyard, and testing its own concept argument rather than repeating it.** Where I agree
with FIX.md I say so and cite it; **where I rule against its self-accounting, I say that
too — and I do, twice** (§8b and §6d below).

---

## 6. IS "GIVE THE ROOT SESSION A NAME/NODE" A CORPSE?

### 6a. The hunt — and it comes back empty

**NO HITS.** I searched the whole corpus — `docs/`, `docs/design/archive/`, `docs/audit/`,
`WORLD.md`, `bin/swarm`, `.swarm/journal/*`, and git history — for any prior *proposal and
kill* of: an operator node, a root agent, a session record for the human's session, an
`agents/operator.json`, a registry entry for the root, or an identity field for the root.

**Nothing. The nodehood question has never been asked before 2026-07-12.** That is a real
finding and it is the first thing to say: **there is no corpse here, because there is no
grave.**

### 6b. But the absence of a grave is not a licence — so I tested what *was* decided

The sentence everybody is leaning on is `WORLD.md:57`:
> *"**The operator is a mailbox, not a node.** Messages to `operator` wait until the human
> looks; `ps` shows them waiting. Nothing pushes to the human, and nothing ever refuses a
> message to the operator."*

**I traced its origin, because a sentence's meaning is fixed by the decision that made it.**
It is born in SIMPLEST §5, finding F8 — and **the decision it records is about PUSH, not
about NODEHOOD:**

> *"**F8 (the operator's suspicions, attacked)** — **The push/poll asymmetry is kept and
> named** rather than papered over: the operator is a mailbox, not a node; that is now a
> sentence in the contract instead of an unexamined assumption under a false guarantee. …
> **Whether the human should get push is herdr's decision to make**, and the design says
> whose job it is."* — `docs/design/SIMPLEST.md:231-235`

And the deletion-table row that produced it kills the **operator-terminus guarantee**, not
the operator's nodehood:
> *"| The operator-terminus guarantee ("an escalation never has nowhere to go") | The
> comforting sentence. | It was never true in the way it reads — the operator's mailbox
> drains only by human action (F6). … **Push-to-human is the multiplexer's job (a tab
> badge), not a CLI's promise.** |"* — `docs/design/SIMPLEST.md:186`

**RULING on the origin:** `WORLD.md:57` is **ASSERTED-AS-DESIGN**, and it *was* a deliberate
decision — **but the thing decided was "nothing pushes to the human."** Nobody in SIMPLEST
considered making the root session a named agent and refused. **The nodehood question was
never put.**

### 6c. THE COUNTER-ARGUMENT I WAS TOLD TO TEST — and it FAILS as posed

My parent's framing:
> *"WORLD.md ALREADY says the operator is a mailbox and NOT a node — so naming the root is
> arguably not a NEW concept but the OVERDUE IMPLEMENTATION of an existing one (a bug fix,
> not an addition). Is that true, or is it a rationalization that smuggles a 10th concept
> past the count?"*

**As posed, it is a rationalization — and I would have ruled against it. FIX.md's author
caught the same hole and I independently confirm it:**

> *""The mailbox concept already says the root session isn't the operator" is doing work the
> text does not quite do. `WORLD.md:57` says the operator is a mailbox rather than a node. It
> does **not** say "and therefore the human's Claude session is a separate, named thing." **A
> reader could consistently hold: the operator is a mailbox, AND the root session is the
> operator, AND the operator therefore both has a mailbox and spawns children** — which is
> precisely what the code does today. **The sentence alone doesn't forbid it.**"*
> — `docs/design/OPERATOR-STRUCTURE-FIX.md:64-71`

**Correct. Do not run the argument that way.** A promise about *push* cannot be cashed as a
mandate about *registry records*. That inference is the smuggling my parent asked me to watch
for, and it is really there.

### 6d. THE ARGUMENT THAT ACTUALLY HOLDS — and the one FIX.md misses

**The load-bearing text is CONCEPT 1, not the mailbox promise:**
> *"1. **Agent** — a Claude session in a herdr pane, with a **name**, a **parent**, and a
> **journal**."* — `WORLD.md:9-10`

The root session **is a Claude session in a herdr pane**. By concept 1 it therefore **is an
agent** — and an agent has a name, a parent, and a journal. Today it has a **journal**
(`.swarm/journal/operator.md`, 55 KB, actively written), a **name** it *shares with the
mailbox*, and **no representable parent**. **It is a malformed instance of concept 1, not a
tenth concept.** FIX.md:89-93 says this and I agree, VERIFIED independently:

> *"**The root session is already an Agent under concept 1.** It is simply a *malformed*
> one… **Naming it does not add a concept — it makes an existing instance of concept 1
> well-formed.** The 55 KB journal is the proof: the repo has been *treating* the root
> session as an agent (journal, seat, open loops) for its whole history, **while the tool
> refused to give it a name.**"*

And the corroboration is the strongest kind — **the repo already hand-rolled the missing
concept and called it something else.** `skill/SKILL.md:51-57`'s **"hand on the operator
seat"** — *"Hands come and go, in sequence or in parallel; **everything below is convention
in that journal, not tool state**"* — is precisely *"a session with a name and a lifetime,
distinct from the standing mailbox."* **SKILL.md invented the hand because the tool would not
give it a name.** A concept that must be hand-rolled in prose to make the tool usable is not a
*new* concept when the tool finally provides it; it is a **debt being paid**.

### 6e. ★ THE FINDING NOBODY HAS MADE — the contradiction is CONTRACT-vs-CONTRACT, not code-vs-contract

**Everyone in this thread — dp-red, field-tester, FIX.md, my own parent — says the same
thing: "WORLD.md says the operator is a mailbox, not a node; the code says otherwise at line
64; the code contradicts the contract."** (`field-evidence-doctrine-2026-07-12.md:37-46`;
`…-RED.md:161-163`: *"That is a contradiction inside the artifact, and it is the probe's real
prize."*)

**I read WORLD.md and that is not what happened. Read concept 2:**

> *"2. **The tree** — your parent judges and approves your work; you judge your children's.
> **The human operator roots the tree.** Who may message whom is judgment, not a rule
> engine."* — `WORLD.md:11-13`

**`bin/swarm:64` is not contradicting the contract. It is implementing CONCEPT 2, faithfully
and exactly.** "The human operator roots the tree" is *precisely* `roots = kids.get("operator")`
(`bin/swarm:553`) and `parent = my_name()` → `"operator"` (`:64`, `:869`). The code is a
correct rendering of the sentence WORLD.md actually ships.

**The contradiction is INSIDE WORLD.md:** concept 2 says *the operator roots the tree* (a
node's job — you can only root a tree if you are in it); the promise at :57 says *the
operator is a mailbox, not a node*. **Both are contract-class. They cannot both be true.**
The code picked one, and it picked the one in the **concept list** — the normative half —
over the one in the **promises** — the descriptive half. That is a *defensible* reading, not
a bug.

**Why this matters, and it is not pedantry:**

1. **It reframes the fix from "repair the code" to "settle the contract."** You cannot fix
   `:64` without deciding *which of two contract sentences is wrong*. That is a
   **contract-class amendment** and it must go to the human as one — which is exactly the
   class my parent's own journal already assigned it (*"contract-class (reconcile the WORLD
   contradiction)"*, `.swarm/journal/operator.md:189`). **My finding says the reconciliation
   is bigger than advertised: concept 2's body has to change, not just a promise's wording.**
2. **It kills the cheapest version of the "it's just a bug fix" argument.** "The code
   contradicts the contract, so fixing the code is free" is **false** — the code agrees with
   half the contract. Somebody must *unmake a decision*, and that decision was made in the
   concept list.
3. **And the fix's own diff concedes it.** Under FIX.md's recommended (a3), **`root-1`'s own
   agent record still carries `parent: "operator"`** — VERIFIED, `OPERATOR-STRUCTURE-FIX.md:180`:
   > *"✅ `root-1`'s own record has `parent: "operator"`, so `root-1` IS the single root line.
   > Workers hang under it. **This is the fix, visible.**"*

   **So the fix does not abolish the operator-as-parent. It inserts a node beneath it.** The
   mailbox *still roots the tree* — concept 2 survives, mechanically. What changes is that
   the mailbox now has exactly **one** child instead of twenty-three. **That is a genuinely
   modest, genuinely honest change** — and it is a *better* argument than the one being made,
   because it means **`WORLD.md:57` never has to be reinterpreted at all.** The operator
   remains a mailbox that roots the tree and is not a session. **The bug was never that
   `operator` is a parent; it was that `operator` is also a NAME A SESSION ANSWERS TO.**

**RULING (Q6):**

> **NOT A CORPSE — no grave exists, and I hunted for one.** And **not a 10th concept**: the
> root session is a **malformed instance of concept 1**, whose absence the repo has already
> been paying for in prose (the "hand" convention, `skill/SKILL.md:51-57`, explicitly *"not
> tool state"*).
>
> **BUT my parent's argument for that conclusion is the wrong one and must not be shipped.**
> `WORLD.md:57` is a promise about **push**, born in SIMPLEST §5/F8 (*"whether the human
> should get push is herdr's decision"*). It does not entail nodehood, and leaning on it *is*
> the rationalization my brief asked me to catch. **Use concept 1.**
>
> **AND the contradiction is misdiagnosed across the whole thread.** `bin/swarm:64` faithfully
> implements **`WORLD.md:11-12`, concept 2 — *"The human operator roots the tree."*** The
> contradiction is **contract-vs-contract** (concept 2 vs the :57 promise), not
> code-vs-contract. **Nobody has said this, and it changes the amendment's size**: settling it
> means editing the *concept list*, the normative half. **The good news, which is also mine:**
> the fix's own diff (`FIX.md:180`) keeps `root-1.parent = "operator"` — so **concept 2
> survives untouched** and the true, minimal amendment is one sentence: ***the operator is a
> parent, never a session — no session is ever named `operator`.*** That reconciles both
> contract sentences at once, and it costs zero concepts.

---

## 7. IS THE SPAWN-GUARD THE KILLED SHAPE?

### 7a. What was actually killed

> *"- **Enforced caps** (spawn refuses child N+1): **an engine**, a wrong constant at some
> load, and **it teaches agents to fear the tool instead of testing themselves.** Rejected on
> §8 grounds before merit."* — `docs/design/SPAN.md:219-221`

> *"A spawn-refusing cap (engine) is out — and would be wrong anyway: **the right span is
> context-dependent.** Ten one-line children are lighter than three research streams. **Any
> constant the tool enforces is a lie at some load.**"* — `docs/design/SPAN.md:69-72`

And the founding kill, PHILOSOPHY §2: *"A hook that blocks an agent until it writes a file
produces a written file, not a reconciled agent; **it is trivially gamed**"* (`:65-70`).

### 7b. Does the distinction (guard on DATA vs guard on BEHAVIOR) hold? — **YES, and it is not a dodge. The tool already refuses 22 things.**

My parent asked whether the "it's a guard on the tool's own data model, not on an agent's
behavior" line is real or a rationalization. **It is real, and the proof is that the tool has
been refusing things since day one, uncontroversially.** VERIFIED — every `die()` in
`bin/swarm`, and none of these was ever objected to:

| what the tool refuses today | line |
|---|---|
| reserved names (`operator`, `delivered`) | `:861-862` |
| a name already used (the journal tombstone) | `:874-876` |
| a name failing `NAME_RE` | `:858-860` |
| an empty task | `:863-864` |
| spawning outside herdr | `:865-866` |
| a message over `TURN_CAP` (8000) | `:990-992` |
| an unknown recipient | `:986-987` |
| unknown verbs / flags / arity | `:703, :856, :967, :1051, :1069, :1146` |

**And the decisive datum: one of these refusals was COMMISSIONED BY THE HUMAN PERSONALLY.**
`.swarm/journal/operator.md:9,12` — the operator dispatched `hardener` to *fix* `NAME_RE` so
that `'abc\n'` would be **refused**, and then verified the refusal himself in a live sandbox
(*"'abc\n' spawn refused pre-claim"*). **The human does not merely tolerate data-validity
refusals; he orders them.**

**So the line is genuine, and I can state it:**

> **The tool may refuse an INPUT THAT IS NOT WELL-FORMED. It may not refuse a JUDGMENT THAT IS
> THE AGENT'S TO MAKE.** SPAN's cap was killed because *"the right span is context-dependent…
> any constant the tool enforces is a lie at some load"* — i.e. the tool would be **overruling
> a judgment it cannot make**. A reserved name is not a judgment; it is a collision.

### 7c. BUT THE GUARD (b) STILL FAILS — on a ground neither §2 nor SPAN supplies

**The distinction holds and it does not save option (b).** Here is why, and it is the sharpest
thing in FIX.md:

> *"1. **It cannot enforce what it asks for.** The message says *"spawn workers under an
> existing child."* **A root session cannot do that.** … **A rule whose compliant path is
> unrepresentable is not a rule; it is a wall with a door marked "violate me."**"*
> — `docs/design/OPERATOR-STRUCTURE-FIX.md:277-283`
>
> *"**(b) is a lint. The bug is a type error.**"* — `:300`

**A warn/refuse on `parent=operator` from a root spawner tells the root to do something the
root CANNOT DO.** It has no other name to write (`my_name()` returns `"operator"`
unconditionally; there is no flag, no branch — `RED.md:170-178`). So the guard is **not** a
data-validity refusal at all: there is no well-formed input the caller could have supplied
instead. **It is a behavioral scold with no compliant path — which lands it squarely in the
killed class, and worse than the killed class, because SPAN's cap at least had a compliant
path (spawn fewer children).**

**RULING (Q7):**

> **The DATA-vs-BEHAVIOR distinction HOLDS — it is not a dodge, and the record proves it: the
> tool refuses 22 things today, one of them commissioned and personally verified by the human
> (`operator.md:9,12`). Guards on ill-formed INPUT are shipped and uncontroversial; guards on
> an agent's JUDGMENT are killed (`SPAN.md:219`, `PHILOSOPHY.md §2`).**
>
> **BUT the spawn-guard (b) does not get to stand on that distinction, because it is not on
> the data side.** With `my_name()` hard-coded, **there is no well-formed alternative the
> spawner could write** — so (b) refuses a judgment the agent is *not free to make*. **That is
> the killed shape, and in its worst form.** ***The test that separates them, and I offer it
> as the general rule: a refusal is data-validity if a COMPLIANT PATH EXISTS; it is a
> guardrail if the caller is being told to do something it cannot do.***
>
> **Fix (a) is not a guard at all.** It makes the bad tree **unrepresentable** rather than
> **discouraged** — the difference between a type and a lint. Recommend (a); **reject (b) on
> the graveyard's own grounds.**

---

## 8. WATCHLIST — DOES A NAMED ROOT ADD A FIELD OR A STATE?

### 8a. #7, quoted

> *"## 7. Scope creep in the rewrite itself (the disease that built the 27)*
> *- **WATCH:** the new tool growing **verbs, flags, fields, or states** the design does not
> name. **Every concept in the current system was added by someone with a reason that sounded
> local and sane.***
> *- **TRIGGER:** any addition that cannot point to a WATCHLIST entry whose trigger fired.*
> *- **SIMPLEST FIX:** … **An addition with no fired trigger behind it gets reverted**"*
> — `docs/design/WATCHLIST.md:99-108`

And the count is a **tracked invariant**, held in the contract's first line (*"Nine concepts,
four verbs"*, `WORLD.md:3`), in the source header (`bin/swarm:4`), and paid in its own currency
by every design doc in the repo (*"Concepts: zero. WORLD.md stays at nine"*, `ONBOARDING.md:700`;
*"Zero new concepts, zero new verbs, zero new state"*, `SPAN.md:315`).

### 8b. ★ RULING — AND HERE I RULE AGAINST THE FIX'S OWN ACCOUNTING

**Verbs: zero.** ✅ (a3) adds none — this is real and it is (a3)'s whole reason for beating
(a2), which would have spent one (`FIX.md:135`).
**Flags: zero.** ✅
**Fields:** the root's agent record reuses the **existing** record schema. ✅ No new field.

**STATES: NOT ZERO. `#7`'s WATCH line FIRES, and FIX.md undersells it.**

FIX.md's own cost line reads *"0 verbs, 0 concepts, **1 file**, ~14 lines"* (`:8-13`) — and
that **one file is `.swarm/settings/root.id`** (`:162-164`: *"Persisted to
`.swarm/settings/root.id` so a restarted root session in the same terminal reads back the same
name"*). **That is a new persisted fact in a new location that no concept names.** It is
precisely *"the new tool growing … states the design does not name."*

**I will not wave this through, and I want the operator to see that I did not.** The honest
accounting is:

- **It is state.** A new file, a new directory (`settings/`), a fact that survives restart and
  that the tool reads to decide who it is. **`#7` fires on the letter.**
- **It is small, and it is the RIGHT KIND.** It stores an **identity**, not a **claim**. The
  corpse test I set in Part I §1d asks *"is it a self-description the tool BRANCHES on?"* —
  and this one **is** read by `my_name()`. **But every kill in the graveyard is of a field
  that stores a JUDGMENT** (`--role`, `--standing`, `trigger_mode`, `--span`, message `type`):
  things the system claimed to *know* about an agent's nature, which rot, which the agent
  could contradict, which *"config wearing the costume of a fact"* names exactly. **A name is
  not a judgment. It cannot rot. It cannot be wrong.** It is the same class of fact as
  `agents/<n>.json`'s `name` and `parent` — which SIMPLEST explicitly *keeps* and defends:
  > *"a binding record of **immutable** facts per agent (name, parent, pane, task, spawn-ts)
  > does exist and is never pruned — **it cannot rot into wrong, because nothing in it claims
  > the present**."* — `docs/design/SIMPLEST.md:182`

  **`root.id` is exactly that: an immutable fact that claims nothing about the present.** It
  passes SIMPLEST's own test for state that is allowed to exist.

**So: #7 FIRES, and the fix SURVIVES it — but it must PAY, not dodge.** The correct line in
the cost table is **not** *"1 file"* buried in a parenthesis. It is:

> **State: +1 (`.swarm/settings/root.id` — an immutable identity, not a judgment; the same
> class as `agents/*.json`'s `name`, which SIMPLEST §4 explicitly keeps because *"it cannot
> rot into wrong"*).**

**And #7's TRIGGER line** (*"any addition that cannot point to a WATCHLIST entry whose trigger
fired"*) — **this one the fix passes cleanly, and it is the only proposal in this thread that
does.** The trigger that fired is **WATCHLIST #7's own CHECK clause turned on the tool**: a
MEASURED, 4/4 field result (`field-evidence-doctrine-2026-07-12.md:30-33`) plus a code read
(`bin/swarm:64`) showing the tool cannot represent its own contract. **That is not "a reason
that sounded local and sane." It is an artifact.** Part I's doctrine, by contrast, points to
no fired trigger at all (§5 above). **The tool fix is better-evidenced than the doctrine it
was spawned to support** — and that inversion is worth the operator's attention.

**No WATCHLIST entry guards the concept count directly** (I checked all 8) — the count is held
by #7's WATCH line and by convention, not by a dedicated entry.

---

## 9. ★ THE SHARPEST QUESTION — DOES PHILOSOPHY §8 LICENSE AN ENGINE HERE?

### 9a. The question as posed

> *"§8: 'prompt-level convention first, a visibility verb second, an engine never — unless the
> record shows the convention failing.' The convention HAS now failed in the field (4/4 flat
> rows) — BUT dp-red R1/R3 argue it was never given a fair chance (the tool made compliance
> impossible). Does §8's 'unless the record shows the convention failing' license an engine
> change HERE, or does dp-red's rebuttal mean the convention is still untested and §8 still
> forbids it?"*

### 9b. RULING: **BOTH HORNS ARE WRONG. §8 IS NOT ENGAGED, BECAUSE THE FIX IS NOT AN ENGINE.**

My parent's question presupposes that this is a dispute about **whether the convention
failed**. It is not, and answering it on those terms would import a false frame.

**Read §8 for what it actually governs:**
> *"Nothing here was built because it seemed principled. **It was built after the convention
> proved out** — and refused when it had not. … **The corollary is a standing bias:
> prompt-level convention first, a visibility verb second, an engine never — unless the record
> shows the convention failing.**"* — `docs/PHILOSOPHY.md:245-263`

Look at what §8's own examples are. **Every one of them is machinery that FORCES OR CHECKS AN
AGENT'S CONDUCT:**
- checkpoints — *"It does not write the file, validate it, or enforce it"* (`:250-253`);
- the reconciliation loop — *"ASK #35 explicitly offered 'Full reconciliation engine' as an
  option. **It was not taken**"* (`:254-256`);
- `swarm send operator` — built only *"after the escalation contract had been exercised enough
  for its missing terminus to become a real, observed failure"* (`:256-257`).

**§8 is a rule about ENFORCEMENT MACHINERY. It asks: "before you build a thing that makes
agents comply, has the un-machined version failed?"**

**Now ask what the root-naming fix does. It does not make any agent do anything.**
- It does not check compliance.
- It does not watch behavior.
- It does not refuse, block, nag, or validate a judgment.
- It does not add a duty, and it does not enforce one.

**It changes what `my_name()` returns when an env var is absent** (`FIX.md:155-158`: *"One
reader. That is the whole seam."*). **It corrects a data model so that the contract's own
sentence becomes expressible.** An agent under the fix is **exactly as free** as it is today —
freer, in fact, since it gains a tree it could not previously write.

**§8 has nothing to bite on.** There is no engine. Calling this an "engine" because it is a
code change is a category error: by that reading, fixing `NAME_RE`'s trailing-newline bug
(which the operator **personally commissioned**, `operator.md:9`) was an engine too.

### 9c. And dp-red's rebuttal, on my reading, cuts the *other* way from how it is being used

dp-red is being cited as *"the convention was never fairly tested, so §8 still forbids
machinery."* **But dp-red's point, taken seriously, is that the convention CANNOT BE TESTED
AT ALL until the tool is fixed:**

> *"Because it is a tool default, **no amount of prose can fix it.** A session that fully
> understood the doctrine, wanted a coordinator layer, and tried to build one **would still
> write `parent=operator`** … **The doctrine was never given a chance to fail or succeed.**"*
> — `docs/audit/field-evidence-doctrine-2026-07-12-RED.md:170-178`

**So dp-red's rebuttal does not preserve §8's prohibition — it makes §8 INAPPLICABLE, in both
directions at once:**
- It **denies the licence**: the record does *not* show the convention failing, because the
  convention was never runnable. ✅ (My parent has this half right.)
- **But it equally denies the prohibition**: §8's *"convention first"* ladder presumes the
  convention is *possible*. **You cannot "try the convention first" when the tool makes the
  compliant behavior unrepresentable.** §8's first rung does not exist here. A ladder with no
  first rung is not a ladder you are standing on.

**dp-red says the fix is a prerequisite for the experiment, not a substitute for it.** Its own
words: the fix is *"not a de-biasing trick but **a correctness fix to the data model**"* and
*"a **genuine, artifact-grounded bug**"* (`RED.md:180-186`). **The convention gets tried AFTER
the fix — that is the whole recommendation, and it is the opposite of skipping to an engine.**

### 9d. THE PRINCIPLE THAT ACTUALLY GOVERNS: PHILOSOPHY §10

> *"**10. Correct the record, even against yourself.** The project's own documents were twice
> corrected *against* the project's interest … **'Where the code and the docs disagree, that
> disagreement is recorded as a gap rather than smoothed over.'** … And it is why
> `swarm checkpoint --context` now prints `{}` and explains itself on stderr rather than
> returning a plausible number from the wrong agent's transcript (PR #19). **An honest unknown
> beats a plausible wrong value — a wrong number that looks right is the worst artifact a
> system can produce, because §4 depends on artifacts being trustworthy.**"*
> — `docs/PHILOSOPHY.md:306-323`

**A tool whose data model cannot express its own contract, and which therefore writes a tree
that looks right and is wrong — 23 agents recorded as direct children of a human who never
spawned them — is the `checkpoint --context` case, in the registry instead of in a number.**
`agents/*.json` is the artifact everything else is judged from. §4 (*judge artifacts, never
claims*) depends on it being true. **It is not true.**

**RULING (Q9), stated plainly because I was asked to:**

> **§8 does NOT license an engine here — and it does not need to, because THE FIX IS NOT AN
> ENGINE.** §8 governs **machinery that forces or checks an agent's conduct** (its own three
> examples are the checkpoint hook, the reconciliation engine, and the escalation verb). The
> root-naming fix **constrains no agent, enforces no duty, checks no compliance, and refuses
> nothing.** It changes one return value so the tree the contract describes becomes
> *writable*. Asking whether §8 permits it is asking whether a spelling rule permits a
> haircut.
>
> **And dp-red's rebuttal, read honestly, does not save the prohibition — it dissolves the
> question.** §8's ladder starts at *"try the convention."* **Here there is no first rung: the
> tool makes the compliant behavior unrepresentable, so the convention cannot be tried, cannot
> fail, and cannot succeed.** The fix is the **precondition of §8's experiment**, not an
> escape from it. Ship the fix, *then* the convention gets its first fair trial — which is
> precisely what §8 demands and what the field evidence itself asks for
> (`field-evidence-doctrine-2026-07-12.md:81-84`: *"The doctrine-prose question can only be
> re-asked after that repair."*).
>
> **The governing principle is PHILOSOPHY §10, not §8.** *"An honest unknown beats a plausible
> wrong value."* The registry currently records 23 agents as direct children of the human — a
> plausible wrong value, in the exact artifact that §4 makes everything else depend on. §10's
> record is that this project has twice corrected its own documents **against its own
> interest** rather than ship a comfortable falsehood. **This is that, in code.**
>
> **FALSIFIER for this ruling, and I want it on the record:** show me that the fix makes an
> agent **do** or **not-do** something — a behavioral constraint, a refused action with no
> compliant path, a duty it must now discharge. If it does, it **is** an engine, §8 bites, and
> I am wrong. I read the diff (`FIX.md:172-200`, all ten sites): the only behavior change is
> that the root session now **receives hook delivery, events, and restore** like any other
> agent (sites 4–6), which is the *removal* of an exception, not the addition of a rule. **The
> one thing I cannot fully discharge is site 4–6's hazard — the root session gaining a hook
> path it never had — and FIX.md flags it as *"the one real hazard" itself (`:181`). That is a
> mechanism risk for `structure-mech` and the implementer to close, not a graveyard objection,
> and I do not claim authority over it.**

---

## 10. PART II SUMMARY — the four rulings

| Q | ruling |
|---|---|
| **6. Named root a corpse?** | **NO — no grave exists** (searched; the nodehood question was never asked). **Not a 10th concept** — the root is a **malformed instance of concept 1** (`WORLD.md:9-10`), and the repo already hand-rolled the gap as the *"hand on the operator seat"* convention, explicitly *"not tool state"* (`SKILL.md:51-57`). **BUT the argument as my parent posed it FAILS** — `WORLD.md:57` is a promise about **push** (origin: `SIMPLEST.md:231-235`, F8), and cashing it as a mandate about registry records *is* the smuggle I was told to catch. **Use concept 1.** ★ **AND THE WHOLE THREAD HAS MISDIAGNOSED THE CONTRADICTION:** `bin/swarm:64` faithfully implements **concept 2 — *"The human operator roots the tree"*** (`WORLD.md:11-12`). The clash is **contract-vs-contract**, not code-vs-contract. The minimal true amendment is one sentence — ***the operator is a parent, never a session*** — which reconciles both, keeps concept 2 (`root-1.parent` is still `"operator"`, `FIX.md:180`), and costs zero concepts. |
| **7. Spawn-guard the killed shape?** | **The DATA-vs-BEHAVIOR distinction HOLDS — not a dodge.** The tool refuses 22 things today; **one was commissioned and personally verified by the human** (`operator.md:9,12`). **But (b) does not get to stand on it:** with `my_name()` hard-coded there is **no well-formed alternative the spawner could write**, so (b) refuses a judgment the agent is **not free to make** — the killed shape in its worst form. *"A rule whose compliant path is unrepresentable is not a rule; it is a wall with a door marked 'violate me.'"* (`FIX.md:283`) **The general test: a refusal is data-validity iff a COMPLIANT PATH EXISTS.** **Recommend (a); reject (b).** |
| **8. WATCHLIST #7 — field or state?** | **0 verbs, 0 flags, 0 new fields — but STATE IS NOT ZERO, and I rule against FIX.md's own accounting.** `.swarm/settings/root.id` (`FIX.md:162-164`) is a new persisted fact in a new location. **#7's WATCH line fires on "states."** It **survives** — because it stores an **identity**, not a **judgment**, and SIMPLEST §4 explicitly keeps immutable facts that *"cannot rot into wrong, because nothing in it claims the present"* (`SIMPLEST.md:182`) — **but it must be PAID for in the cost table, not buried as "1 file."** ★ And note the inversion: **#7's TRIGGER line, which Part I's doctrine FAILS, the tool fix PASSES cleanly** — it points at a MEASURED 4/4 field result plus a code read. **The fix is better-evidenced than the doctrine it was spawned to support.** |
| **9. Does §8 license an engine?** | ★ **BOTH HORNS ARE WRONG. §8 IS NOT ENGAGED — THE FIX IS NOT AN ENGINE.** §8 governs machinery that **forces or checks an agent's conduct** (its own examples: the checkpoint hook, the reconciliation engine). The fix **constrains no agent, enforces no duty, refuses nothing** — it changes one return value so the contract's own tree becomes *writable*. **And dp-red's rebuttal dissolves the question rather than preserving the prohibition:** §8's ladder begins at *"try the convention,"* and **here there is no first rung** — the tool makes compliance unrepresentable, so the convention can neither fail nor succeed. **The fix is the PRECONDITION of §8's experiment, not an escape from it.** **The governing principle is §10** — *"an honest unknown beats a plausible wrong value"* — and the registry's 23-children-of-a-human is that wrong value, sitting in the one artifact §4 makes everything else depend on. |

### The bottom line for `operator-structure-scout`

**The tool fix is CLEAN — cleaner than the doctrine.** It re-raises **no corpse**; it passes
**#7's trigger**, which the doctrine fails; and **§8 does not reach it**. It should ship on
**§10**, as a record-correction, and it should be presented to the human as **contract-class**
— because it is, and for a bigger reason than anyone in this thread has yet said: **the
contradiction is inside WORLD.md itself.**

**Three honesty corrections I owe, and they cut against my own side:**
1. **My parent's "mailbox already says it" argument is a rationalization** — do not ship it.
   Use concept 1. (§6c)
2. **`FIX.md` undersells its state cost.** `.swarm/settings/root.id` is state; #7's WATCH line
   fires; pay it. (§8b)
3. **Fix (b), the spawn-guard, IS the killed shape** — and my parent offered it as a
   co-equal option. It is not. Kill it. (§7c)

**And the order stands, unchanged from Part I and now doubly earned:** ship the fix, *then*
re-ask the doctrine. **The doctrine cannot be tested before the repair** — that is not my
opinion, it is dp-red's finding and the field evidence's own verdict.
