# HARNESS-RED — an adversarial review of `docs/design/HARNESS.md`

**Reviewer:** `hc-red`, spawned fresh with no sight of the author's reasoning. I read the
doc as a stranger would: the argument on the page, and the sources it points at.
**Written at** `swarm-dev/spawn-slash-shim@cfb3113`, 2026-07-13.

**Method.** Three children swept in parallel and I kept judgment, verification and glue.
Every WRONG verdict below I re-checked at source myself before adopting it; where a child
and I disagreed, the source decided, and twice it decided against me (noted in place).
Child artifacts, all on disk: `docs/audit/_hcr-evidence.md` (45 cite-checks),
`docs/audit/_hcr-doctrine.md` (§5/§6), `docs/audit/_hcr-ux-slm.md` (§4/§7).

**The one-line finding.** The design is largely right and the doc is largely wrong about
*why* — and on the two places where the recommendation itself must be trusted (the
survivability gate and the simplicity claim), the citation says the opposite of the text.

---

## VERDICTS

| Surface | Verdict |
|---|---|
| **(i) The pattern ruling (§5)** | **WOUNDED.** The ruling survives; two of its three deciding arguments do not. Its factual premise — *"the convention… has not even shipped"* — is false. |
| **(ii) The remodel ruling (§6)** | **WOUNDED, one clause REFUTED.** The identity argument holds for *same-tier* change and was never restricted to it — §6 is an un-gated bypass of the mandate §3 declares settled. |
| **(iii) UX simplicity (§4)** | **REFUTED.** "Two flags, both mandated elsewhere (PR #83)" — PR #83 is open, and its ruling is *"`--model` stays optional."* |
| **(iv) The SLM rulings (§7)** | **Cuts mostly HOLD; the KEEP is WOUNDED.** The mirror-failure charge is **not sustained** — and I say so on the record. But §7e's central safety rule is unenforceable at its own seam. |
| **(v) Evidence integrity** | **REFUTED as a discipline.** Of 45 tags: 21 REACHES, 15 OVERSTATED, 7 WRONG, 2 UNVERIFIABLE — and the errors run one way, concentrated in the sources only the author had read. |

**The two findings to read first**, both checkable in a minute and neither a matter of
taste: **F1** (the survivability gate's source argues against the gate) and **F2** (the
simplicity claim's source rules the opposite). Everything else is repair work.

---

## F1 — THE SURVIVABILITY GATE IS BUILT ON A SOURCE THAT FORBIDS IT

This is the most serious finding in the review, because §2.4 is not a footnote: the doc's
own preamble elevates it — the Haiku ban is *"the type specimen of a missing axis"* — and
the gate is one of the five things §1 recommends.

**The doc (§2.4), tagged MEASURED:**

> Haiku "is unusable as a swarm agent — not for reasoning quality, but **because it cannot
> run in auto permission mode, so its first dialog wedges it forever, invisibly** (MEASURED
> — both Haiku arms of `docs/audit/weak-model-delegation-2026-07-13.md` blocked on a
> permission dialog before the synthesis step)."

On this it builds a **per-model spawn refusal**: `swarm: haiku cannot hold an agent pane:
no auto permission mode`.

**The cited source, `docs/audit/weak-model-delegation-2026-07-13.md:87`, in bold in the
original:**

> "**The stall was caused by a permission gate swarm hands EVERY child regardless of
> model. Opus would block too**, on a first-touch path it hadn't been granted — the
> difference between the arms was *filesystem starting state*, not model strength. **A tier
> rule about cheap models does not fix an infrastructure gate that fires on all models.**
> Aim the fix at the gate."

**:89** — the falsifier that would settle it (*"spawn an **Opus**-pinned child into the same
first-touch permission wall"*) is *"**the top re-run item**"* and **was never run**.
**:91** — the section is headed, literally: *"**WHAT MUST HAPPEN BEFORE ANYONE LOCKS A TIER
RULE ON THIS**."*

**The gap.** The MEASURED tag is attached to a *causal* claim — the wedge is
**model-linked** — that the measurement's own author explicitly rejects in favour of an
**infrastructure** cause, in a section whose title forbids the exact move HARNESS makes.
The observation (both Haiku arms stalled) is real. The *inference* the gate rests on is
not measured, is contradicted by the source, and its settling experiment was skipped.

`grep -c permissions bin/swarm` → **0**. There is no permissions block. The gate fires on
every model.

**And the doc concedes this, one section later.** §8:

> "no permissions redesign (the missing `permissions` block in spawned settings is a named
> defect that belongs to the spawn path's owner — MODEL-FIT §7 flagged it first; **the
> Haiku ban is its bill arriving**)."

§2.4 says the cause is *Haiku*. §8 says the cause is *the missing permissions block*. Both
cannot be true, and §8 is the one the source supports. The doc refutes itself in print.

**Consequence.** §2.4's gate is not merely unsupported — it is **actively harmful in the
direction the source warns about**: it hard-codes a per-model refusal into `bin/swarm`,
which will read to every future parent as *"the Haiku problem is solved"*, while the
infrastructure gate that actually fires on all models stays unbuilt. The doc's own §9
falsifier 4 asks for "one probe spawn per gated token per claude-cli release" — the wrong
probe. The probe that matters is the one the source named and nobody ran: **Opus into the
same wall.**

**Repair.** Either run the Opus falsifier and let it decide, or restate the gate honestly:
*swarm hands every child a permission gate it cannot clear unattended; until spawn writes a
`permissions` block, no model can be trusted to survive a first-touch dialog, and Haiku is
the specimen because it was the one we watched.* That is a stronger doc and a true one, and
it points the fix at the gate — where the source says to aim it.

---

## SURFACE (iii) — UX SIMPLICITY (§4): **REFUTED**

*(Taken before §5/§6 because it is the same disease as F1 and it is the shortest kill.)*

**The doc (§4.4):**

> "**Two flags, both mandated elsewhere (PR #83)**; zero new flags for priorities. If this
> design had made `swarm spawn` take five flags it would have failed its own brief; **it
> takes the two the org already decided on**."

**And §3:** *"Required `--model` and `--reason` are **treated here as settled input**."*

**What the sources say. Four legs, all broken:**

1. `gh pr view 83` → **`"state": "OPEN"`**. Not merged. `MODEL-FIT.md` is not on `main`.
2. `MODEL-FIT.md:444`, its actual ruling: *"**The ruling: `--model` stays optional**, but
   silence stops being free."*
3. `MODEL-FIT.md:476-477`: *"The CLI mandate is specified and recommended here, and
   **deliberately left unimplemented in this PR**."*
4. `grep -c -- "--reason" bin/swarm` → **0**. Live confirmation: spawning my own children
   today, the CLI answered **`swarm: spawn: unknown flag --reason`**.

**The gap.** The doc's central UX move is *the complexity is not mine — the org already
bought these two flags*. The org did not. The cited authority **ruled the opposite** and
deferred the mandate on purpose. So HARNESS is not "adopting a settled input"; it is
**assuming an unmerged proposal's rejected alternative**, then spending it as sunk cost to
make its own complexity look free.

**It is internally inconsistent about this.** §8 bills *"the mandate's blast radius
(required `--model`/`--reason`): at least ~9 test call-sites and 12 doc files"* — §8 knows
it is unbuilt, unpaid work. §4.4 spends the same work as someone else's completed purchase.
The doc cannot have it both ways in one document.

**Knock-on.** §4.3's `--model default` is justified by: *"a spawn with no `--model` at all
**remains an error under the mandate**."* There is no mandate. Today a spawn with no
`--model` is not an error — it runs the ambient default, which is the 142/143 bug. So
`--model default`'s entire justification is unfooted.

### The concept count (the claim "zero new flags" is true and measures nothing)

`hcr-ux` enumerated **22 concepts** a new operator must hold; two of them are spawn flags.
The complexity did not vanish, it **moved**: into 2 config keys, 3 token classes with
*different done-signals and different duty contracts* (a Claude seat journals and restores;
an opencode leaf needs a parent-owned watchdog; a thin runner needs neither), 3 prose
contracts (PLAYS.md, the priority line, the leaf-brief discipline), and **≥4 unenforced
operator duties**. `swarm remodel` itself ships 2 more flags. Flag-counting is a proxy that
the design was optimised against rather than a measure of what it costs to learn.

**WOUNDED, not refuted, on that** — the design may still be the simplest available. But
"zero new flags" is a claim about a number the design chose to keep small, offered as proof
of a property (simplicity) it does not establish.

### `--model default`: **HOLDS, wounded**

I sent `hcr-ux` to kill this and it came back saying it survives, and I agree. `--model
default` is **not** the silent non-choice: a human decided, once, on the record; the
resolution is printed (`via default`); the pin is greppable and lands in `ps`. That is a
real difference from an ambient default nobody can name.

**The surviving attack:** the doc's own example reason — *"operator static policy; I read
every scout report in full anyway"* — is **structurally invariant**: it is the same
sentence for every spawn forever. MODEL-FIT's anti-theater evidence (0/135 mush, 17
behavior changes) was measured on a field whose content *varied per spawn*. A field that
cannot vary has not been tested against the theater hypothesis. The doc owes a falsifier
here and does not have one.

### `[models] priority`: **REFUTED — cut it**

Three independent kills:

1. **It fails the doc's own §5 test.** PHILOSOPHY §5: *"when you reach for a config field,
   first ask whether the thing it configures should exist at all."* The doc applies this
   test to the human's registry and the human's router. It does not apply it to its own two
   config keys. `[models] priority` configures a convention **never once tried** — the exact
   §8 argument ("it has not even shipped") the doc uses to kill `--play`, unapplied to
   itself.
2. **It is an unexamined prompt-injection surface.** An unvalidated, operator-authored prose
   string, *"injected **verbatim, once,** into every spawn header"* — writable by any agent
   with repo write access, which is every agent. The doc spends a paragraph in §2.3
   establishing that pane text is attacker-controlled and must be laundered through a closed
   enum, then pipes a free-text file straight into every future agent's prompt without a
   word about it.
3. **Its falsifier cannot fire.** §9-3: *"if spawn reasons never reference the declared
   priority… the line is dead text."* That cannot distinguish *"the line is dead"* from
   *"the line never reached the deciding agent"* — and the doc's own §4.2 admits nothing in
   code interprets it.

**And the citation is wrong too.** §4.2: *"`.swarm/config` (**the file that already carries**
`[middleware]` — `WORLD.md:66`)."* `cat .swarm/config` → **no such file.** The whole "no new
mechanism, just one more stanza in a file you already have" argument rests on a file that
does not exist. (The middleware *code* is real, `bin/swarm:347-371`. The file is not.)

---

## SURFACE (i) — THE PATTERN RULING (§5): **WOUNDED**

**The ruling survives. Two of its three deciding arguments do not, and its factual premise
is false.**

### The steelman, at full strength — and the hang is MEASURED

My brief told me to steelman the registry harder than the doc did, especially on
**atomicity**. Here it is, and I checked my own best argument at source before using it
(twice — see the note at the end of this section).

The doc concedes the atomicity case and then rules against it:

> "(a) *atomicity*: a play bundles model + harness + watchdog duty + permissions in one
> token, so a parent **cannot assemble half a play** (spawn the GLM leaf, forget the
> watchdog — and the eval says a watchdog-less GLM harvest loop hangs, V3:98-100)."

**The hang is not hypothetical. It was observed, once, in this repo's own eval.**
`FLEET-EVAL.md:181-183`:

> "GLM then **misread `swarm ps` liveness** ("children still live … working"), re-spawned
> **4 retries**, and **hung** with no watchdog."

That is 35 minutes of tree, dead, on exactly the omission the registry would have made
impossible. The doc's answer is falsifier 2: wait for a parent to mis-assemble a documented
play *"more than once after one doctrine edit."* So the **first** hang is priced as the cost
of the earning condition — while a hang has **already happened**.

### Argument 2's factual premise is FALSE

**The doc (§5, deciding argument 2):**

> "**§8's earning condition has not been met — the convention has not failed; it has not
> even shipped.** The ladder is days old; PLAYS.md does not exist yet."

**`FLEET.md:286` — the doc HARNESS adopts by name:**

> "**Watchdog:** the *parent* owns a timeout on the pane. If no report and no artifact
> arrive within the budget, the parent reads the pane (ground truth), journals the banner
> text, and treats the leaf as failed."

The watchdog convention **is written**, in the document whose bill HARNESS §2.2 adopts
("**parent-owned watchdog** (FLEET §5 — the honest bill, not priced at zero)"), whose §5
grounds the `glm-tool-leaf` play, and which §8 re-bills. And the record shows it failing:
FLEET-EVAL.md:181-183 (the 35-minute hang) and FLEET-EVAL-V3.md:98-100 (*"no watchdog… dead
children would hang it again"* — the half that **survived** the clean rig). **Both rows are
in the author's own harvested evidence** (`_hc-eval-table.md:32,54`) and he cites them in his
own steelman before ruling against them.

*The one turn this could take, and my ruling on it:* `git status` shows `?? docs/design/FLEET.md`
— untracked. Could the author answer *"an untracked design doc is not a shipped convention"*?
**No.** You cannot cite a document as the evidentiary ground of your play (§5:
*"Ground: … V3:96-98"*), adopt its cost line in your token table, and re-bill it in your own
§8, while disowning it as unshipped. But the honest form of the finding is narrower than
"the convention shipped and failed," so I state it that way: **the convention is written in
the document this design is built on, and the one time the record shows it being relied on,
it was not followed and the tree hung.** That is §8's earning condition — *the record shows
the convention failing* — met on the author's own evidence.

### Argument 1 (142/143) is off-point, and the doc already knows it

> "**The last mechanism that chose for parents produced 142/143 spawns nobody decided**
> (MEASURED). A `--play` flag is a new way of not choosing."

142/143 measures the **absence of a required choice** — spawns with no `--model` at all.
A `--play` flag *under the mandate the doc adopts* would still carry `--reason`. And the doc
**concedes this itself**, 150 lines earlier (§3):

> "an empty `--reason "play: cheap-sweep"` with no verification clause **is a skipped step,
> the same as today**."

So the play-token failure mode is *the reason field going empty* — which is a failure of the
reason field, identical with or without `--play`. The MEASURED number is deployed to carry a
REASONED claim; by the doc's own evidence discipline (*"REASONED (my argument; if it decides
something, its falsifier is in §9)"*), that must be marked and it is not.

### Argument 3 is SIMPLEST §3.5 by name

> "**Registries rot into ceremony** (SIMPLEST §3.5…)"

Which leaves the tally: the author opens by declaring himself *"an outside contractor…
**not bound by this repo's doctrine**; I read it as anthropology"* — and then decides the
collision with **two doctrine citations and one off-point number**. That is the charge my
brief sent me to test (*did the author argue it, or rationalize the doctrine?*), and on §5
the answer is: **he rationalized it, and the ruling happens to be right anyway.**

### The asymmetry — the sharpest structural finding in §5

The doc gives its **own** prose a falsifier and gives **PLAYS.md prose none.**

- §4.2's priority line, §9-3: *"If spawn reasons never cite the declared priority… **the
  line is dead text — delete it** rather than mechanize it."*
- PLAYS.md gets no equivalent. Falsifier 2's collector is *"journal grep for play names vs.
  the briefs actually sent"* — which can **only** see a parent who **read** the play and got
  it partly wrong. **A parent who never opens PLAYS.md** spawns a bare GLM leaf, hangs, and
  leaves **zero rows in the grep.** Silence scores as compliance.

The same skepticism, applied to one prose artifact and withheld from the other — and the one
it is withheld from is the one whose failure mode is a measured 35-minute hang.

**Second asymmetry, never argued:** §2.3 imposes a **pre-emptive MUST** — *"any harness that
admits models with differing permission and limit behavior MUST render blocked distinct from
idle"* — on **one** measured invisibility. §5 **refuses** pre-emption for the watchdog on a
**twice-recorded** hang. Both failures are the same shape: *the tree silently stops and
nobody notices.* One gets a MUST; the other gets "wait for it to fail again."

**Verdict: WOUNDED.** Convention-over-registry is probably still right — the industry
corroboration (§5's eleven-framework survey; aider and CrewAI the only two that shipped the
abstraction) is real, genuinely independent of local doctrine, and I could not shake it.
But the doc must stop claiming the convention has not shipped, must mark argument 1 as
REASONED, and must add **one line** to falsifier 2 to close the silence hole:

> *Collect spawns of a leaf token with **no watchdog clause in the brief** — play named or
> not.*

Zero new concepts; catches the omission case; costs one grep.

---

## SURFACE (ii) — THE REMODEL RULING (§6): **WOUNDED, one clause REFUTED**

The identity argument is **stronger than I expected** and I could not break it in general.
The name/session distinction is real, the restore path does treat the process as disposable,
and *"a killed-and-relaunched pane is indistinguishable from a fresh launch to this hook"* is
independently true (`cmd_restore`, `bin/swarm:916-935` — any non-`compact` source takes the
same branch as a first launch).

**It breaks on one axis the doc never restricts: direction.**

### The un-gated downgrade — a mid-flight bypass of the mandate §3 declares settled

`hcr-doc` grepped every remodel/tier/direction term in the file. §6's restrictions are
**cross-vendor** (:456-458) and **cross-harness** (:631-634) **only**. There is no tier gate.
So this is legal:

```
swarm remodel <a-live-opus-coordinator> --model sonnet --reason "cost"
```

**MODEL-FIT — which HARNESS declares settled input at §3 — rules (`:201`, `:215-216`):**

> "…it runs **Opus 4.8. No exceptions on cost grounds.**"
> "**Downgrading a seat to save tokens spends children to save on the parent. That trade is
> always backwards.**"

§2.4 builds a **gate at spawn**. §6 builds **no gate at remodel**. The design therefore
ships a verb that walks around the mandate it adopted, mid-flight, and never notices. That
is a contradiction with a settled input — the thing my brief named as an automatic finding.

### "Exactly the loss at compaction" is false in the word *exactly*

> "What is genuinely lost is in-context state not yet journaled: **exactly the loss at
> compaction**, which the contract already prices and survives."

Compaction: the **same reasoner** rebuilds from a 4000-char tail using its own judgment.
Downgrade-remodel: a **weaker reasoner** must rebuild from the same 4000 chars. Not the same
loss. And the inductive base the doc leans on — *"~10 agents carry same-day resume entries…
nobody calls them successors"* (`_hc-field.md` §B1) — is **10/10 same-model**. There is not
one instance in the record of the variable being generalized over. The evidence for
"restarts are safe" is entirely evidence about restarts *that did not change the model*.

*(Also: `_hc-field.md` §B1 flags its own count as a floor with an open falsifier — 6 of the
13 named orphan-survivors "**were not directly checked**." HARNESS reports "~10, MEASURED"
and drops the caveat. See the transit pattern in §(v).)*

### REFUTED — the tombstone clause gets its own source backwards

> "Burning a name to change an attribute… **splits one task's history across two journals**,
> which is **closer to violating "one agent, one record"** than the remodel is."

**SIMPLEST §3.3** — which the doc quotes *correctly* eight lines earlier — says the tombstone
exists so that *"history never **blurs two agents into one record**."*

A successor split = **two records for two workers** = the mechanism **working as designed**.
A remodel = **two differently-capable workers in one record** = **the named harm, exactly**.
The doc has its own cited source backwards. This clause should be struck; the ruling does not
need it and is weakened by it.

### Self-remodel is one clause, and it rebuilds a field MODEL-FIT forbade

> "**Who may call it:** the parent on a child (steering), **the agent on itself** (scope
> change)… **Enforcement is judgment, not a rule engine.**"

A self-remodel's `--reason` answers *"am I good enough for this?"* — a **claim about
oneself**, which is precisely what PHILOSOPHY §4 says the system must not store, and precisely
the scoping MODEL-FIT §5 refused ("scoping the reason to anything else **launders a guess into
a decision**"). The reason field works *because the parent fills it*. Self-remodel hands the
field to the party being judged.

And the doc's safety net for this is: *"flips the `ps` pin every reader sees"* — while §2.3 is
a two-page argument that **there was no reader**: trigger-scout died and *"nobody noticed for
~2 hours."* §6 leans on a reader §2.3 proves absent.

### The scope-change trigger: I attacked it and it HELD — with one correction

§6's best passage is the scope-change case (a Sonnet leaf that discovers its task is a tree
remodels **up**). I sent `hcr-doc` to kill it and it held: upgrading on scope growth is the
correct-size response, no name burned, one journal line.

**But the doc mis-uses its evidence for it.** §6: *"MODEL-FIT measured 16% of leaves growing
into seats unbriefed."* `MODEL-FIT:372-374` actually says:

> "**18 of 115 agents — 16% — carry a coordinator role they were never briefed for.** …
> Leaves grow into seats *on their own*, **regardless of model**."

The paraphrase reaches, but it drops **"regardless of model"** — the qualifier that decides
the remedy. MODEL-FIT's own prescription from this number is **structural, not model-tier**
(`:393-400`):

> "Making it *structural* — **a spawned child that cannot itself spawn** — is the natural
> mechanism… **It is the first thing to build if Rung 3 is taken seriously.** Until it
> exists, 'cheap → leaf' is **a promise the parent makes and must actually keep**."

Remodel changes the **model**. The measured bug happens **regardless of model**. So remodel
does not fix it — and §8's "what I did not build and why" lists four omissions (auto-failover,
`--play`, router, permissions) and **does not list the one its own primary source calls "the
first thing to build."**

**This is a live hole, not a bookkeeping one.** I checked: `cmd_spawn` (`bin/swarm:1098-1110`)
has no relation check, no leaf flag, no spawn suppression — every child gets the full verb
set. §2.2 quotes `FLEET.md:88` (*"a leaf never spawns"*) as though the design holds it. It does
not hold it; nothing does. **A design that adds foreign leaf tokens while leaf-cannot-spawn
remains unbuilt has widened the blast radius of the measured 16%, not narrowed it:** a GLM
leaf that decides it needs three helpers can spawn them, on a model the eval says does not
journal, does not restore, and does not time-box.

**Verdict: WOUNDED.** Build `remodel` — but with a **direction gate at the verb** (the twin of
§2.4's spawn refusal), a **flat refusal of tier-lowering self-remodel**, and the **incumbent
model written into every journal entry header** so attribution survives in the file rather than
only in a `ps` pin nobody was watching.

---

## SURFACE (iv) — THE SLM RULINGS (§7): cuts mostly HOLD; the KEEP is WOUNDED

### The mirror-failure charge is NOT SUSTAINED, and I put that on the record

My brief sent `hcr-ux` to find that the author killed the human's ideas by inherited dogma —
this org's standing rule. **It came back refusing the charge, and I adopt its refusal.** A red
team whose children only confirm the red team's priors is a rubber stamp with extra steps.

The tabulation (`_hcr-ux-slm.md` §S4.1): the router cut (a) is **not** a doctrine kill. The doc
ran **adverse** prior art, quoted its real wins (RouteLLM: 85% cost reduction at 95% of GPT-4
performance; FrugalGPT: up to 98%), and killed the router on a **swarm-specific mechanism gap**
— router systems catch wrong routes by *offline benchmark re-scoring*, a surface swarm does not
have. That is an argument, not a reflex. (d), the hook-path cut, is a genuine PHILOSOPHY §10
application and correct. (c)'s **filtering** cut is a hard WORLD.md contract (never-drop) and I
could not shake it.

**Two of the five cuts do rest on the "§8: the convention has not failed" stall** — (b) and
(c)-annotation — and only one of those is a genuine dogma-kill. Here it is.

### (c) The mailbox — **REFUTED (the annotation half): a self-refutation in consecutive sentences**

> "…nothing in the record yet shows the human failing to find the important message, so §8
> refuses the tooling today. **The mailbox's real pressure (30 waiting messages this morning,
> VERIFIED in `ps`)** is an *ordering and batching* convention for senders, not a model."

The doc demands *a record of a missed message* — and then, in the **very next sentence**, cites
the record. Live `swarm ps` as I write: **30+ waiting, oldest 20h, and 17 of them from a single
sender**, rendered oldest-first. That is burial.

And the demand is **unmeetable by construction, as the doc itself explains one paragraph
earlier** when it kills filtering: *"when it drops the one message that mattered, **the operator
never sees what they never saw**."* A missed message is invisible in the record **by the doc's
own argument**. §7c therefore requires, as its earning condition, a record that its own insight
proves cannot exist. That is a stall built out of the doc's best sentence.

Filtering stays cut — correctly, on the never-drop contract. **Annotation (a priority hint,
full queue untouched, degrades to noise rather than loss) is killed by a §8 stall the doc's own
next clause falsifies.**

### (b) The classifier — **WOUNDED: "cannot be sweet-talked" is false, and I executed the refutation**

> "But the regex **ships, is pure, is testable, and cannot be sweet-talked** — an agent can
> print anything into its own pane, and prompt-injecting a model into emitting the wrong enum
> member is a real attack on a surface **the regex is immune to**."

`BLOCKED_SIGNATURES` (`bin/swarm:57-61`) is **three plain substrings matched with `in`**:

```python
BLOCKED_SIGNATURES = (
    ("trust",      "trust the files in this folder"),
    ("permission", "Do you want to proceed?"),
    ("rate-limit", "resets"),
)
```

I ran `classify_blocked` against text a **healthy** agent could print. Three for three:

```
classify_blocked("I asked the user: Do you want to proceed?")   -> 'permission'
classify_blocked("the rate limit resets at 3pm, I am fine")     -> 'rate-limit'
classify_blocked("should I trust the files in this folder? no") -> 'trust'
```

`hcr-ux` reproduced this independently. The regex needs no sweet-talking — **one literal
string**, which *ordinary work on this subject matter produces*. This journal entry, sitting in
my own pane, would do it.

**The code was honest and the doc overclaimed on its behalf.** `bin/swarm:545-547` claims only
the narrower, **true** property — a *closed codomain*: the output is one of three fixed kinds,
so it "cannot forge a tree row, a fake `dead:` line, or the `(you)` marker." That protects the
**rendering**. It says nothing about the **verdict**. HARNESS upgrades output-safety into
general un-forgeability and **wins the SLM argument with it**.

*Honest narrowing (checked before I banked it):* `read_blocked`/`blocked_candidates`
(`bin/swarm:764-800`) only pane-read agents idle past 120s — so the forgery is not instant. But
that gate is explicitly a **cost** control ("*worth the cost of a live pane read*"), not a
security control, and the residual path needs no malice at all: an agent whose last turn
mentioned a permission prompt goes idle and is classified blocked. **False positive on ordinary
work.**

**The cut still stands** — on determinism, inspectability and §8, which are good reasons. The
**security argument for it must be struck**: regex-vs-SLM here is a difference of *degree*, not
of *kind*, and the doc asserts a difference of kind.

**A side-defect neither section owns, created by the doc's own wiring.** §6 makes
`[blocked: rate-limit]` the visible trigger a parent acts on. §7b names the harm out loud — *"A
wrong `blocked: rate-limit` label triggers a parent's remodel of a healthy agent"* — as an
argument **against the SLM**, without noticing the **shipping regex already produces it**. Any
agent can print `resets` + `limit`, go idle, and induce its parent to remodel it. **The design
has built a forgeable path from pane text to a model swap.**

### (e) The one-shot leaf — **placement HOLDS; the central safety RULE is REFUTED**

The placement is right: a one-shot leaf holds no session, clears no dialogs, keeps no journal —
every seat-discipline failure mode is structurally absent, and the artifact is mechanically
checkable. That is the fit rule, correctly applied.

**But the rule that makes it safe cannot be enforced where the doc puts it.**

The doc measures that the class's weakest axis is **trigger judgment** — *38.2% unnecessary
calls (Qwen3-8B), 39.0% missed calls (Llama-3.2-3B), judgment **not** scaling monotonically
with size* — and then deletes that axis by fiat:

> "**the SLM leaf is always a forced function call against a parent-supplied schema — the model
> never decides *whether* to call, only fills *what*.** **That deletes the measured weak axis**
> (over/under-triggering)."

**The seam it must be enforced at (§2.2)** is *"the ~5-line `curl | jq` thin runner"*, sourced to
**FLEET §3B** (`FLEET.md:24-29`):

> "the launcher runs a **~5-line `curl | jq` against the model's `/v1/chat/completions`** and
> exits."

A bare chat-completions call. **No `tool_choice`, no schema, no `response_format`** — and no code
anywhere in the design inspects a leaf brief to reject one that lets the model choose whether to
act. The doc states the enforcement in the passive, with no agent: *"A leaf brief that lets the
SLM choose whether to act has left rung 3 and **must be refused**."* Refused **by whom**? The
only candidate is the parent's judgment — **the party this repo has measured dropping unenforced
duties three separate times** (142/143 unchosen spawns; 18/115 leaves grown into seats; deepseek's
4/7 report drops).

And it fails **silently, in the omission direction** (39.0% *missed* calls) — which the doc's own
stated safety net, the parent's spot-check, **structurally cannot see**. MODEL-FIT §4's own
discipline says it: *absence is invisible to inspection.*

**So the central safety argument for the only kept placement is an unenforced convention** — and
`write_launcher` (`bin/swarm:1041-1066`) emits only `claude`. **The thin runner does not exist
yet.**

**The mirror, and this is the real §7 finding.** §7a cuts the *human's* router with exactly this
move:

> "the spawn record still shows a model and a reason, so **the audit surface reads as healthy
> while the thinking it was built to witness has stopped**."

§7e keeps the *author's own* placement on a rule with an **identical compliance surface**: the
artifact exists and looks well-formed, so the surface reads healthy, while **nothing witnesses
whether the call was forced**. The doc applies a standard to the operator's idea that it exempts
its own from. *That* is the mirror failure — not "dogma killed the human's ideas" (it did not),
but **one standard, applied in one direction.**

**Repair, ~2 lines and honest:** make the thin runner *itself* refuse a brief with no schema +
`tool_choice=required`, and put it on §8's bill. Then the rule is enforced at the seam that
carries it, and the "deletes the measured weak axis" claim becomes true instead of aspirational.

---

## SURFACE (v) — EVIDENCE INTEGRITY: **REFUTED as a discipline**

The doc opens by making evidence discipline its authority:

> "**Evidence discipline:** **VERIFIED** (I ran it / read the line — quoted, file:line),
> **MEASURED** (instrumentation, method stated), **DOCUMENTED** (a named source says so),
> **REASONED** (my argument…)."

**45 tags checked** (`docs/audit/_hcr-evidence.md`, both sides quoted per row; every WRONG
re-verified by me at source):

| Verdict | Count |
|---|---|
| **REACHES** — the source supports the claim | **21** |
| **OVERSTATED** — true core, cite/caveat/scope does not survive contact | **15** |
| **WRONG** — the cited source does not contain the claim | **7** |
| **UNVERIFIABLE** — no locatable source | **2** |

**Half the tags hold.** That is the honest headline, and it is stated first because the
defect list below is long and would otherwise read as a demolition. The `bin/swarm`
mechanical claims are **exact** (`:1061-1062` *is* the only `claude` invocation;
`classify_blocked` *is* `:694-715` with exactly that enum; the `ps` pins render; the
30-message mailbox is real). **MODEL-FIT is cited impeccably — 9 of 9 section cites land.**

**And one suspicion I raised was cleared.** I flagged `arXiv 2606.07587` ("Routing
Plateau", §7.2a) as a probable hallucinated pincite — a June-2026 id, one month before the
doc, carrying a conveniently decisive finding. `hcr-ev` sent a child to hunt it expecting a
laundered fabrication. **The paper is real** — verified live; title, authors and finding all
match. Reported clean, and I say so as plainly as I said the rest.

**The WRONG list** (each independently re-checked):

1. **§2.4 / the Haiku ban** — the source argues the opposite. **F1 above.** *(Filed OVERSTATED
   by the auditor, load-bearing; I rate it the doc's most serious error.)*
2. **§7b "cannot be sweet-talked"** — false; forgery executed 5/5. *(Above.)*
3. **§4.2 "`.swarm/config`, the file that already carries `[middleware]` — WORLD.md:66"** —
   `cat .swarm/config` → **no such file**; and `:66` is mid-sentence (the section head is `:64`).
4. **§6 *"picked up exactly where it left off"* — VERIFIED, "its journal :1528".**
   `grep -c` in `trigger-scout.md` → **0**. The phrase is `_hc-field.md:26` — **the collector's
   own summary prose**, put in quote marks and attributed to the primary journal, under the tag
   that exists to prevent exactly this.
5. **§6 "`_hc-mech.md` §5.3"** — **`_hc-mech.md` has no §5.3.** §5 is a flat, unnumbered list. A
   **fabricated pincite**. The underlying fact (no targeted stop verb; I grepped: only `pane
   list/read/send-text/send-keys/run/close`) is **true** — which makes it worse: a true claim
   given a fake address.
6. **§3 "4/7 drops" vs §5 "3/7 report delivery"** — the source says **4/7** (`V3:49`, `V3:76`);
   `3/7` appears in **neither** eval document. The doc contradicts itself on its own headline eval
   number. *(I had reconciled these arithmetically — 4 dropped of 7 = 3 delivered — and my child
   checked the **source string** instead and found §5 restates the same measurement with a number
   that is nowhere. My reconciliation was charity. **Second time a child caught me being
   charitable to the doc**; the first is noted in §5.)*
7. **§5 "excellent tool-user… well-formed all battery long" (V3:96-98)** — the text is at
   **V3:101-102**, and the "quote" is **reworded while wearing quote marks**. The cited range is
   about something else.
8. **§1 "`_hc-eval-table.md` (83 rows)"** — it has **87**.

**UNVERIFIABLE:** §2.3's *"DOCUMENTED — operator correction, 2026-07-13"* — DOCUMENTED promises
*"a named source says so"*; the named source is an unlogged remark with no transcript, message, or
journal pointer.

**Two more worth naming:**

- **§1/§2.1, "every hook is fail-safe `try/except → exit 0`", sourced to FLEET §2.** **Every line
  number in FLEET §2 has rotted** (hooks at 1156-1160, cited as 890-894; `cmd_deliver` 864 cited
  as 685; `cmd_event` 878 cited as 699; `cmd_restore` 916 cited as 737). HARNESS independently
  re-verified the *launcher* line and **passed the hook cite through unchecked** — inherited rot,
  under a VERIFIED tag. (Also: `cmd_event` opens with `die(...)` → `sys.exit(1)`, **outside any
  try** — so "every hook" is absolute where the code is not. No live bug; the claim is still
  overstated.)
- **§2.1's "4000-char tail"** — the number is **true** but is **not in the cited range**
  (`build_restore`, :462-472, contains no cap; `JOURNAL_TAIL_CAP = 4000` is at **`:34`**). The doc
  feels the gap and sources the number to *a child's doc* rather than to the primary line it is one
  grep away from.

### The finding *about* the findings, part 1: **citation quality tracks distance from the source**

The defects are not scattered. They are **concentrated exactly where nobody else was going
to check**:

- **Into MODEL-FIT — a document with its own author, its own PR, its own reviewers: 9 of 9
  section cites LAND.** Impeccable.
- **Into `bin/swarm` — code anyone can run: exact.** Line ranges, enum, invocation count all
  verify.
- **Into the author's OWN HARVESTED CHILDREN — documents only he had read: 3 of 7 cites are
  defective**, including **two invented addresses**: `_hc-mech.md §5.3` (§5 is a flat,
  unnumbered list — *no subsections exist*) and `_hc-industry.md "finding 4"` (points at
  nothing).

And **three VERIFIED tags carry paraphrase inside quotation marks** — worst is §6's *"picked
up exactly where it left off"*, attributed to `trigger-scout.md:1528`, where the phrase has
**zero hits**; it is `_hc-field.md:26`, *the collector's own summary sentence about that
journal*, promoted to a quotation from the journal itself.

The doc's own preamble defines the tag it is breaking: **VERIFIED** = *"I ran it / read the
line — **quoted, file:line**."* Three VERIFIED tags do not meet the doc's own definition of
VERIFIED. The discipline is real where it was going to be audited and decorative where it
was not.

### The finding *about* the findings, part 2: **the caveat dies in transit**

And it has a direction. Three independent instances:

- **E-8:** `V3:33-35` footnotes the D4 failure as *"**confounded in MAGNITUDE** by the MCP escape
  hatch — read as **'at most this bad'**"*. HARNESS cites the D4 hard-fail to justify a strong
  structural ruling (*"may not be trusted with restore-dependent continuity"*) and **drops the
  confound**.
- **M-10:** `_hc-field.md` §B1 flags its own "~10 resumes" as a **floor with an open falsifier**
  (6 of 13 never checked). HARNESS reports *"~10, MEASURED"*, **caveat gone** — and it is the
  inductive base for §6's identity claim.
- **M-8:** *"three independent witnesses"* — three *observers*, **one instrument**: all three read
  the same `last_words` string as surfaced by `ps`. Three readers of one signal.

**Every single drop makes the claim stronger.** A document whose entire rhetorical authority rests
on its evidence-discipline preamble is exactly the document where a one-directional caveat leak is
disqualifying. The tags are doing persuasion work the sources do not support.

---

## WHAT I COULD NOT BREAK

Stated plainly, because a red-teamer's negative is the cheapest sentence to write and the most
useful one to trust.

- **The core recommendation** — *keep the harness, make the launcher body the one variable, key it
  on the model token* — is **right**, and the coupling claim underneath it (`bin/swarm:1061-1062`
  is the single `claude` invocation) **verifies**. The doc is wrong about many of its reasons and
  still lands in the right place.
- **§5's industry corroboration** — eleven frameworks, only aider's main/editor/weak triad and
  CrewAI's `manager_llm` shipped as abstractions; LangGraph and the OpenAI Agents SDK document the
  cheap/expensive idea **as prose only**. This is genuinely independent of local doctrine and I
  could not shake it. *(Caveat, minor: of the eleven, two are self-labeled non-LLM analogies and
  two are routing gateways — the honest count of surveyed agent frameworks is ~7.)*
- **§6's scope-change trigger** — remodelling **up** on scope growth is the correct-size response.
  I attacked it and it held.
- **§7a's router cut** — argued on a real, swarm-specific mechanism gap (no offline benchmark
  surface to catch a wrong route), with the adverse prior art quoted rather than buried. **Not
  dogma.**
- **§7c's filtering cut** — the WORLD.md never-drop contract is hard and correctly applied.
- **`--model default`** — explicit deference, not silence. A human decided once, on the record,
  and the resolution is greppable.
- **§2.3's blocked-visibility requirement** — right, and shipping. *(It now needs the forgery
  finding folded in, but the requirement itself stands.)*

---

## THE REPAIR LIST, ranked

1. **§2.4 — run the Opus falsifier, or restate the gate.** The source says the gate is
   infrastructure, not model. Either run *"spawn an Opus-pinned child into the same first-touch
   permission wall"* (the source's own "top re-run item") and let it decide, or aim the fix where
   the source says: **spawn writes a `permissions` block.** Do not ship a per-model refusal on an
   inference the measurement rejects.
2. **§3/§4.4 — stop calling the mandate settled.** PR #83 is open and rules *"`--model` stays
   optional."* Either the mandate is this design's own cost (then §4's simplicity claim goes), or
   it is a prerequisite (then say so and price it). §8 already bills it; §4.4 must stop spending it.
3. **§6 — gate the direction.** A tier-lowering remodel of a seat is a mid-flight bypass of
   MODEL-FIT's *"no exceptions on cost grounds."* Add the gate at the verb; refuse tier-lowering
   self-remodel outright; write the incumbent model into every journal entry header.
4. **§7e — enforce the rule at the seam.** Make the thin runner refuse a brief with no schema +
   `tool_choice=required`. ~2 lines, and it converts the design's central SLM safety claim from
   aspiration into fact.
5. **§7b — strike "cannot be sweet-talked."** Keep the cut; fix the argument. And **own the
   side-defect**: forged pane text → `[blocked: rate-limit]` → a parent's remodel. That path is
   built by this design and unguarded.
6. **§5 — one line in falsifier 2:** collect leaf-token spawns with **no watchdog clause in the
   brief**, play named or not. Closes the silence hole where a parent who never read PLAYS.md
   leaves zero rows in the grep.
7. **§5 — fix the premise.** The watchdog convention **is** written (`FLEET.md:286`) and the record
   **does** show it failing (`FLEET-EVAL.md:181-183`, a 35-minute hang). Say that, and let the
   ruling stand on the arguments that survive.
8. **§7c — un-cut annotation**, or state honestly that the earning condition is one the doc's own
   argument makes unmeetable.
9. **§8 — add the omission your own primary source calls "the first thing to build":**
   leaf-cannot-spawn. `cmd_spawn` has no relation check today, and this design **adds foreign leaf
   tokens on top of that hole.**
10. **Everywhere — re-check the tags into your own children.** 7 WRONG, 15 OVERSTATED, 2
    UNVERIFIABLE of 45 — and they cluster in `_hc-*.md`, the sources only you had read (3 of 7
    defective, two of them invented addresses), while MODEL-FIT is cited 9 for 9. Fix the two
    fake pincites, strip the quotation marks off the three paraphrases carrying VERIFIED tags,
    and restore the caveats the sources attached: the D4 confound, the ~10-resumes floor, the
    one-instrument witness count.

---

*Children: `hcr-ev` (evidence, 45 checks, 3 sub-agents), `hcr-doc` (§5/§6), `hcr-ux` (§4/§7).
All three artifacts on disk and cited above. Two of my own readings were corrected by a child
mid-review; both corrections are recorded in `.swarm/journal/hc-red.md` rather than quietly
repaired.*
