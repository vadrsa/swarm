# _hcr-doctrine — adversarial review of HARNESS §5 (patterns) and §6 (remodel)

**Author:** `hcr-doc`, adversarial analyst under `hc-red`. **Written at**
`swarm-dev/spawn-slash-shim@cfb3113`, 2026-07-13.

**Target:** `docs/design/HARNESS.md` §5 (patterns-as-convention over a registry) and
§6 (`swarm remodel`; "a name is one agent forever" binds the name, not the session).

**Sources read in full:** `docs/design/HARNESS.md` (692 lines), `docs/PHILOSOPHY.md`,
`WORLD.md`, `docs/design/SIMPLEST.md`, `docs/design/MODEL-FIT.md` (via `git show
swarm-dev/model-fit`), `docs/design/FLEET.md`, `docs/design/FLEET-EVAL.md` (§ GLM rows),
`docs/design/FLEET-EVAL-V3.md` (§ GLM/deepseek rows), `docs/audit/_hc-eval-table.md`.

**Verdicts, up front:**

| Surface | Verdict | The one sentence |
|---|---|---|
| **§5 — patterns-as-convention** | **WOUNDED** (ruling survives; two load-bearing arguments do not) | The ruling is right for the wrong reasons: argument 1's evidence is off-point and self-defeating under the mandate it cites, and argument 2's factual premise — *"the convention… has not even shipped"* — **is false**: the watchdog convention shipped in `FLEET.md:286`, and the eval measured it failing **twice**. |
| **§6 — remodel-identity** | **WOUNDED, and one clause REFUTED** | The identity argument holds for a *lateral* remodel and is **unargued for a downgrade**, which the doc never restricts. And the doc's characterization of the tombstone (§6, citing SIMPLEST §3.3) **inverts its actual purpose** — SIMPLEST says uniqueness exists so *history never blurs two agents into one record*; the doc cites it to license blurring two sessions into one record. |

---

# SURFACE 1 — THE PATTERN RULING (§5)

## 1a. Argue or rationalize? — the deciding arguments are 1 measured + 2 citations, and the measured one is off-point

**The doc's own framing of its independence:**

> "I am not bound by this repo's doctrine; I read it as anthropology. Where my answer
> collides with local law I say so plainly" (`HARNESS.md:5-6`)

**The three deciding arguments (`HARNESS.md:341-356`), classified:**

| # | The argument | Independent of doctrine? |
|---|---|---|
| 1 | *"The last mechanism that chose for parents produced 142/143 spawns nobody decided (MEASURED — MODEL-FIT's headline). A `--play` flag is a new way of not choosing"* (`:344-346`) | **Measured — but off-point. See below.** |
| 2 | *"**§8's earning condition has not been met** — the convention has not failed; it has not even shipped… Building the engine first would be guessing at a workflow (**PHILOSOPHY §8's exact refusal**)"* (`:350-352`) | **NO — this is PHILOSOPHY §8 by name, and its factual premise is false (§1b).** |
| 3 | *"**Registries rot into ceremony** (**SIMPLEST §3.5**: every structured field nobody reads was 'verifiably dead or rotten')"* (`:353-354`) | **NO — this is SIMPLEST by name.** |

So of three deciding arguments, **two are the local law recited by section number**, which
is precisely what an "outside contractor" who "reads doctrine as anthropology" claims not
to be doing. The doc *names* the collision (`:300-309`) and then resolves it by citing the
two principles it named as the collision. **The one genuinely independent argument is #1 —
and it does not survive contact with the mandate it invokes.**

### The 142/143 analogy is broken, and PR #83 is what breaks it

**The doc's argument:**

> "The last mechanism that chose for parents produced 142/143 spawns nobody decided
> (MEASURED — MODEL-FIT's headline). **A `--play` flag is a new way of not choosing:**
> it compresses the decision back into a token, and the parent stops thinking again —
> precisely the bug PR #83 was bought to end." (`HARNESS.md:344-348`)

**What 142/143 actually measures** (MODEL-FIT, headline):

> "**142 of 143 agents took the inherited default; exactly one was ever pinned.** …
> That is not a decision anyone made. It is a decision nobody made, 143 times."

And MODEL-FIT §5b is explicit that the mechanism at fault was the **absence of any
required choice** — the bare launcher line with **no `--model` flag at all**:

> "There is **no inheritance.** `swarm spawn` does not read the parent's model and does
> not pass one down. When `--model` is absent, the launcher invokes `claude` with **no
> `--model` flag at all**" (MODEL-FIT §5b)

**THE NAMED GAP.** 142/143 is a measurement of *what happens when the tool asks for
nothing*. It is **not** a measurement of *what happens when a parent is given a
vocabulary token*. Those are different failures, and the doc's own design forecloses the
first one it cites:

> "a spawn with no `--model` at all remains an error under the mandate" (`HARNESS.md:269`)

Under PR #83's mandate — which HARNESS §3 explicitly *adopts as settled input*
(`:190-192`) — **`--reason` is required at every spawn.** So a `--play` spawn would be:

```
swarm spawn sweep-3 "..." --play glm-tool-leaf --reason "<one clause>"
```

The `--reason` field does not disappear because a play was named. The doc **knows this**
and says so, one section earlier, about *plays as prose*:

> "Citing a play is legitimate *shorthand inside* a reason — `--reason "play cheap-sweep;
> I diff each artifact against its source"` — and **an empty `--reason "play:
> cheap-sweep"` with no verification clause is a skipped step, the same as today.**"
> (`HARNESS.md:197-200`)

**That sentence refutes argument 1.** The doc has already established that a play-name is
not a substitute for the reason clause — under the *prose* regime. Nothing about
`.swarm/plays.json` changes that: the mandate is enforced by `cmd_spawn`, not by whether
the recipe lives in Markdown or JSON. **"A `--play` flag is a new way of not choosing" is
true only if `--play` were allowed to suppress `--reason` — and the doc never proposes
that, and the mandate it cites would forbid it.**

The residual, steelmanned for the doc: a *token* invites a shallower reason than a *recipe
you had to read*. That is a real psychological claim. But it is **REASONED, not MEASURED** —
and the doc presents it dressed in a MEASURED number that does not measure it. Per the
doc's own evidence discipline (`:11-13`), that mislabel is the finding.

**Sharper still: the 142/143 evidence cuts the *other* way on the registry's own turf.**
MODEL-FIT's actual lesson is *"agents do not invent structural moves that are not in their
frame, and reliably execute the ones that are"* (MODEL-FIT §intro, quoting
`references/COORDINATING.md:28-31`). A `--play` token **is** a structural move in the
frame. A paragraph in `docs/PLAYS.md` that a parent must remember to read **is not** — it
is exactly the "not in the frame" condition MODEL-FIT names as the cause of 142/143. The
doc cites the finding and then rules against the mechanism the finding recommends.

---

## 1b. The registry, steelmanned harder than the doc did — and the atomicity argument is ALREADY EARNED

The doc concedes the atomicity good and then defers it:

> "(a) *atomicity*: a play bundles model + harness + watchdog duty + permissions in one
> token, so **a parent cannot assemble half a play (spawn the GLM leaf, forget the
> watchdog — and the eval says a watchdog-less GLM harvest loop hangs, V3:98-100)**"
> (`HARNESS.md:314-317`)

And the earning condition it sets:

> "**§8's earning condition has not been met — the convention has not failed; it has not
> even shipped.** The ladder is days old; **PLAYS.md does not exist yet.**"
> (`HARNESS.md:350-352`)

> "What would earn the machinery, precisely (committed, §9): if journals/`ps` show parents
> **repeatedly mis-assembling** a documented play — the model right, the duty absent (a GLM
> leaf spawned without a watchdog clause in the brief…) — **at any rate that survives one
> doctrine edit**, the convention has failed in the recorded way §8 requires"
> (`HARNESS.md:368-372`)

### THE KILL: the watchdog convention HAS shipped, and the record shows it failing — TWICE

**The convention exists in prose, today, in the doc's own cited source.** `FLEET.md:286-290`:

> "**Watchdog:** the *parent* owns a timeout on the pane. If no report and no artifact
> arrive within the budget, the parent reads the pane (ground truth), journals the banner
> text, and treats the leaf as failed."

That **is** the convention. It is prose. It is written down. It is in a design doc HARNESS
cites eleven times and adopts by name (`HARNESS.md:116`: *"parent-owned watchdog (FLEET §5
— the honest bill, not priced at zero)"*). **"The convention has not even shipped" is
false as stated** — what has not shipped is a *file named PLAYS.md*. The doc has confused
the convention with its future filename.

**And the record shows the convention failing — not once, twice, both MEASURED:**

| Failure | The record |
|---|---|
| **Failure 1 (v2)** | *"GLM **misread `swarm ps` liveness** ('children still live … working'), **re-spawned 4 retries**, and **hung** with no watchdog"* — `FLEET-EVAL.md:181-183`, transcribed in `_hc-eval-table.md:54`. A **35-minute hang**, a real parent, in a real seat. |
| **Failure 2 (v3, clean rig)** | *"no watchdog. Its harvest loop is blind sleep-escalation (`sleep 5/15/30` + `swarm ps`); it terminated only because its children delivered. **Dead children would hang it again.** Unattended-parent risk."* — `FLEET-EVAL-V3.md:98-100`, transcribed in `_hc-eval-table.md:32`. |

Note what v3 says: the failure mode **did not go away when the rig was cleaned**. v2's
*other* GLM findings were retired as rig artifacts (*"v2's 'children all died, model hung
35 min, fragile parent' does NOT reproduce and is retired. It was the rig's empty cwd"*).
**The watchdog absence is explicitly named as "the half that SURVIVES v2."** It reproduced.

**THE NAMED GAP — the earning condition is met on the doc's own evidence.** §9's falsifier
2 asks for a parent that mis-assembles a documented play *"more than once after one
doctrine edit."* The count the doc demands:

- **failures required: ≥2**, and
- **they must occur after PLAYS.md exists**, and
- **they must be committed by parents in this swarm's production record**.

But the failure mode has **already been observed twice**, by a *measured model in a
measured seat*, against a convention (`FLEET.md:286`) that **already existed in prose when
the failures happened**. The doc's response is to require that the *same* failure be
re-observed **after being rewritten into a different prose file**. That is not an earning
condition tied to evidence; it is an earning condition tied to *format*. Rewriting a
sentence from `FLEET.md` into `PLAYS.md` and then waiting for it to be forgotten twice more
does not produce new knowledge — the knowledge is already on disk, at
`_hc-eval-table.md:32` and `:54`, which the author harvested and cited.

**The atomicity good is not theoretical. It is the *only* one of (a)–(d) that has a
measured failure behind it, and the doc dismisses it in the same breath as the unmeasured
ones:**

> "The registry's goods (a)–(d) are real, but **(a) and (b) are *also* a description of a
> parent who no longer needs to understand the recipe they are running.**"
> (`HARNESS.md:347-349`)

This is the weakest sentence in §5. It answers a *safety* argument with a *pedagogy*
argument. "The parent no longer needs to understand the recipe" is a cost — but the thing
being bought is **a parent that cannot silently omit the one duty whose omission is
measured to hang the tree for 35 minutes.** The doc never weighs those against each other;
it asserts that (a) is *also* a description of the bad thing and moves on. **A parent who
understands the recipe perfectly and forgets one clause under load is exactly the parent
the eval measured, and prose does not catch him.**

### The convention is the forgettable thing — and the doc says so about *other* prose

This is the sharpest asymmetry in the document, and it is quotable.

**On the priority line (§4.2), the doc applies full skepticism to its own prose:**

> "(Falsifier: **if spawn reasons never reference the declared priority, the line is dead
> text** — §9.)" (`HARNESS.md:248-249`)

**§9, falsifier 3, presses it further:**

> "**The priority line (§4.2).** If spawn reasons never cite the declared priority within,
> say, the first fifty mandated spawns, **the line is dead text — delete it rather than
> mechanize it.**" (`HARNESS.md:658-660`)

**And SIMPLEST §3.5 — which the doc cites *in favor of* prose — is a finding that prose
mechanisms rot:**

> "every *structured* field of the current checkpoint is **verifiably dead or rotten** …
> A schema nobody reads is not a schema; it is ceremony with fields."
> (SIMPLEST §3, concept 5)

**THE NAMED GAP — the asymmetry, stated plainly:**

- To the **priority line** (prose, §4.2), the doc says: *it may be dead text; here is the
  falsifier; delete it if unread.*
- To the **registry** (machinery, §5), the doc says: *registries rot into ceremony.*
- To **PLAYS.md** (prose, §5), the doc says: **nothing.** There is no falsifier in §9 for
  "PLAYS.md is never read." Falsifier 2 (`:653-657`) tests whether parents *mis-assemble*
  a play — which **presupposes they read it and got it partly right.** The case the eval
  actually measured — *the parent never consults the recipe at all and spawns a bare
  leaf* — has no collector, no observation, and no consequence anywhere in §9.

The doc holds prose to the "is anyone reading this?" standard **everywhere except the one
place where prose is doing safety-critical work.** That is the asymmetry, and it is not an
oversight of emphasis — falsifier 2 is *structurally* unable to see the failure the eval
recorded, because a parent who never reads PLAYS.md never *mis-assembles a documented
play*; he assembles nothing, from nothing, and the grep in falsifier 2's collector —
*"journal grep for play names vs. the briefs actually sent"* (`:657`) — **returns zero
rows, which reads as zero failures.** A parent who ignores the convention entirely is
**invisible to the falsifier built to catch him.** Silence scores as compliance. That is
the exact defect SIMPLEST names in the mechanism it deleted: *"its absence reads as
compliance"* (SIMPLEST §4, on the nag).

### "The next reader catches it" — name the reader

**The doc's claim:**

> "A prose play that drifts from the eval is **caught by the next reader**; a JSON play
> consumed by a flag is caught by nobody until it mis-spawns at scale."
> (`HARNESS.md:354-356`)

**THE NAMED GAP: there is no reader, and no mechanism, and the doc names neither.**
Compare what the doc demands of *every other* claim in the document — §9 gives each
falsifier a *Collector*, by name (`"Collector: journal grep for play names"`, `"Collector:
the first N remodels' journals"`, `"Collector: one probe spawn per gated token per
claude-cli release"`). The "next reader" gets **no collector, no name, no cadence, and no
trigger.** Concretely:

- When `FLEET-EVAL` re-runs and the GLM watchdog row flips, **what re-reads PLAYS.md?**
  Nothing. There is no link — `docs/PLAYS.md` would contain a prose sentence citing
  `V3:96-98`; no tool follows that citation, no test asserts it, no hook checks it. The
  registry's good (c) — *"one registry edit re-tunes every future spawn"* (`:317`) — is
  answered with *"versus hoping every parent re-reads a doc"* (`:318`) — the doc **writes
  the word "hoping" into its own steelman and then rules for the hope.**
- The doc's own §5 concedes the mechanism is absent in the very sentence it uses to
  dismiss it: *"the eval says a watchdog-less GLM harvest loop hangs"* is a fact **living
  in FLEET-EVAL-V3**, and the only thing that would carry it to a spawning parent is a
  human deciding, unprompted, to go read a doc.

Against this the industry citation (`:358-364`) is the doc's best independent evidence —
*"across eleven frameworks… a named combo pattern with its own API vocabulary is rare"* —
and it is real. But note what it does **not** say: it does not say the frameworks that
document cheap/expensive-model choice **as prose guidance only** have a *measured hang* in
their record that the prose is meant to prevent. The industry landed on prose for a
*preference*; swarm is being asked to land on prose for a *safety duty whose omission is
measured to hang a parent for 35 minutes*. Those are not the same artifact, and the
corroboration does not transfer.

---

## 1c. Is the earning condition fair, or an unfalsifiable stall?

**The structure, stated exactly as the doc leaves it:**

1. §8: *"prompt-level convention first… an engine never — **unless the record shows the
   convention failing**"* (PHILOSOPHY §8, quoted at `HARNESS.md:307-308`).
2. §5: *"the convention has not failed; **it has not even shipped**"* (`:350-351`).
3. §9 falsifier 2: `--play` is earned when a parent mis-assembles a play *"**more than
   once after one doctrine edit**"* (`:653-656`).

**Count the gates a registry must pass, in order:**

| Gate | What it requires | Can it be met before a hang? |
|---|---|---|
| 1 | `docs/PLAYS.md` must be written and shipped | — |
| 2 | A parent must **read it**, then **partly follow it** (a full ignore is invisible to falsifier 2's grep — §1b) | — |
| 3 | That mis-assembly must happen **once** | **A watchdog-less GLM leaf that hangs the tree** |
| 4 | A **doctrine edit** must be made in response | — |
| 5 | It must happen **again, after that edit** ("at any rate that **survives one doctrine edit**") | **A second hang** |

**THE NAMED GAP: the earning condition prices the first hang at zero — and then prices the
second one at zero too.** The doc's structure explicitly requires that the doctrine be
*edited once and fail anyway* before machinery is considered. So the registry cannot be
built until the measured failure has been re-run **in production, at least twice, after a
prose fix has already been tried and failed.** The eval already ran that experiment (v2
hang → v3 with a clean rig → **"dead children would hang it again"**), and the doc's answer
is that eval failures do not count because they happened to a foreign model in an eval
rather than to a Claude parent in production.

**Is that a fair distinction?** It is *a* distinction — and it is the strongest thing the
doc has here, so state it fairly: the eval's hang was **GLM's own harvest loop hanging**,
not a *Claude parent forgetting to brief a watchdog*. Those are different subjects. The
§5 play (`glm-tool-leaf`, `:331-334`) puts the watchdog duty on a **Claude parent**, and
**no Claude parent has ever been observed dropping it**, because none has ever been asked
to hold it. So the doc can honestly say: *the failure I am being asked to pre-empt has not
been observed in the party who will now own the duty.*

**But that defense has a price the doc does not pay.** Grant it, and §5's atomicity
concession collapses into a claim about a *Claude* parent — at which point the doc's
citation of `V3:98-100` in the steelman (`:316-317`) is **cited against the wrong subject**:
it proves GLM hangs itself, not that a parent forgets a clause. The doc uses the eval's
authority to make the atomicity danger vivid, then discards the eval's authority when
setting the earning condition. **It cannot have both.** Either the eval's hang is evidence
about this failure mode (in which case the record already shows it, twice, and §8's
condition is met), or it is not (in which case §5's steelman of atomicity has **no measured
grounding at all** and the parenthetical citation at `:316-317` should be struck).

**What would ever make the author build the registry before a failure?** On the doc's own
text: **nothing.** There is no pre-emption clause anywhere in §5 or §9. And the doc knows
the shape of the argument it is refusing, because it *makes* that argument itself, one
section away, about a different mechanism:

> "**Blocked is a first-class state — a harness requirement, not a nicety.** … **any
> harness that admits models with differing permission and limit behavior MUST render
> blocked distinct from idle.**" (`HARNESS.md:136`, `:152-154`)

That is a **MUST**, pre-emptively imposed, on the strength of a *measured invisibility*
(`_hc-field.md` §A1) — machinery built **because a failure was measured once and its
recurrence is not worth paying for.** The doc adopts pre-emption when the measured failure
is *invisibility of a wedged pane*, and refuses pre-emption when the measured failure is
*a hung harvest loop*. **Both are "the tree silently stops and nobody notices." The doc
prices one at MUST and the other at "wait for it to happen twice more."** The
distinction is never argued.

## VERDICT — SURFACE 1: **WOUNDED**

The **ruling survives**: a registry is not obviously right, prose is cheap, the industry
corroboration is real and independent, and MODEL-FIT's own lesson (the parent must think)
does genuinely cut against a token that could become a substitute for thought. I do not
find the ruling *refuted*.

But **two of the three deciding arguments do not survive**:

1. **Argument 1 (142/143) is off-point and self-defeating.** It measures the absence of a
   required choice, not the presence of a vocabulary token. Under the mandate the doc
   adopts, `--play` still carries `--reason`, and the doc **already conceded** that a bare
   play-citation with no verification clause *"is a skipped step, the same as today"*
   (`:199-200`). The number is MEASURED; the argument it is deployed to make is REASONED,
   and the doc's own evidence discipline (`:11-13`) requires that be said.
2. **Argument 2's factual premise is false.** *"The convention… has not even shipped"*
   (`:350-351`) is contradicted by `FLEET.md:286` (*"the parent owns a timeout on the
   pane"*) — the convention shipped, and the record shows it failing at
   `FLEET-EVAL.md:181-183` (a 35-minute hang) and `FLEET-EVAL-V3.md:98-100`
   (*"dead children would hang it again"* — explicitly the half that **survived** the
   clean rig). The doc harvested both rows into `_hc-eval-table.md:32,54` and cited them
   in its own steelman.

**The strongest surviving attack (the one hc-red should carry forward):** §9's falsifier 2
is **structurally blind to the failure the eval actually recorded.** Its collector —
*"journal grep for play names vs. the briefs actually sent"* (`:657`) — can only see a
parent who **read the play and got it partly wrong.** A parent who never opens PLAYS.md
spawns a bare GLM leaf, hangs, and **leaves zero rows in the grep.** The falsifier reads
that as zero failures. Silence scores as compliance — the precise defect SIMPLEST cites
when deleting the nag (*"its absence reads as compliance"*). §5 cannot be trusted to
falsify itself until falsifier 2 also collects **spawns of a play's model with no play
named at all**, which is the observable that would actually have caught GLM.

**Concrete repair, offered rather than withheld:** the doc does not need `.swarm/plays.json`
to close this. It needs one line in §9 — *Collector: grep every spawn whose `--model` is
`glm`/`deepseek` for a watchdog clause in the brief; a spawn of a leaf token with no
watchdog duty in its brief is the failure, whether or not a play was named.* That collects
the omission case, costs zero concepts, and would let the convention actually be judged.
As written, it cannot be.

---

# SURFACE 2 — THE REMODEL RULING (§6)

## 2a. The compaction analogy — sound for a *lateral* switch, and never argued for a *downgrade*

**The doc's identity argument, in full:**

> "**The model is an attribute of the incumbent session. Changing it is a restart with a
> different launcher line — an event this system already survives daily.** What is
> genuinely lost is in-context state not yet journaled: **exactly the loss at compaction,
> which the contract already prices and survives.**" (`HARNESS.md:398-401`)

**The evidence it rests on** (and this evidence is real — I checked it):

> "~10 agents carry same-day resume entries from this morning's machine restart, picked
> up their tasks, and nobody calls them successors (MEASURED — `_hc-field.md` §B1);
> trigger-scout resumed *from its own session-limit death* with the journal as its only
> memory and 'picked up exactly where it left off'" (`HARNESS.md:394-398`)

**THE NAMED GAP: every one of those ~10 restores was a *same-model* restore.** A restart
re-launches the identical launcher line — same model, same competence, same reasoning that
built the un-journaled state in the first place. The doc's inductive base is **10/10
lateral events**, and it generalizes from them to an event with a variable **none of the 10
contained.**

**The disanalogy, stated precisely:**

| | Compaction / restart | Remodel (downgrade) |
|---|---|---|
| What is lost | Un-journaled in-context state | Un-journaled in-context state |
| **Who must reconstruct it from the 4000-char tail** | **The same model that produced it** | **A different, possibly weaker model** |
| Can it re-derive the lost reasoning? | It is the model that derived it once already | **Unknown. Never measured. If it could have derived it, it would have been the right model for the seat.** |

**"The loss is exactly the loss at compaction" is false, and the error is in the word
"exactly."** The *quantity* lost is the same (whatever is not in the journal). The
*recoverability* is not — and recoverability is the entire thing the analogy is
load-bearing for. Compaction survives because the surviving reasoner is the one that
built the state. A downgrade-remodel removes that guarantee **by construction**: the whole
point of a downgrade is that the new incumbent reasons less well. **A loss the same mind
recovers from is not the same loss as a loss a weaker mind must recover from.**

### The doc's own §3 evidence proves the mechanism it leans on can fail

The identity argument leans **entirely** on journal-restore. But the doc measures, in §3,
that journal-restore is exactly what weaker models cannot do:

> "**neither journals for continuity** (V3 D4 hard-fails)" (`HARNESS.md:216`)

> "GLM put its plan in the deliverable, then on restart **went looking for the journal it
> had never written**" (MODEL-FIT §2, from `FLEET-EVAL-V3.md:100-103`)

The doc **sees this for cross-vendor** and restricts it:

> "**Cross-vendor remodel of a *seat* is refused by the eval evidence (§3):** a GLM
> incumbent in a Claude seat's restore-dependent, report-driven contract is precisely
> what the measurements say fails silently." (`HARNESS.md:456-458`)

**And there the restriction stops.** I grepped every occurrence of `remodel`, `downgrade`,
`weaker`, `stronger`, and `tier` in `HARNESS.md`. **There is no restriction anywhere on a
within-Anthropic downgrade.** Not in §6's ruling, not in the verb's spec (`:420`), not in
§8's honest bill (`:631-634` restricts only *"a remodel across harness classes (claude ↔
opencode)"*), not in §9's falsifiers. The syntax the doc ships:

```
swarm remodel <name> --model M --reason "<one clause>"
```

`M` is unconstrained within the Claude row. **`swarm remodel hc-red --model fable --reason
"cost"` is a legal, doctrine-blessed act on a coordinator holding a live judgment thread,
and nothing in the document says a word about it.**

**THE NAMED GAP, sharpened by the doc's own doctrine.** MODEL-FIT §3 — which HARNESS §3
adopts as settled input — states the rule the remodel verb silently punches through:

> "**Rule: if the child will spawn, judge, harvest, close, or survive a restore, it runs
> Opus 4.8.** **No exceptions on cost grounds.**" (MODEL-FIT §3)

> "**A bad seat produces a bad tree**: it mis-briefs four children, and now you are paying
> full price for four agents to do work that was scoped wrong… **Downgrading a seat to
> save tokens spends children to save on the parent. That trade is always backwards.**"
> (MODEL-FIT §3)

`swarm remodel <seat> --model sonnet` **is** downgrading a seat. MODEL-FIT forbids it at
spawn with the words *"no exceptions on cost grounds."* HARNESS §6 builds a verb that
performs it mid-flight, and **never notices that it has built a bypass around the mandate
it declared settled.** The gate exists at spawn (§2.4's survivability refusal) and **does
not exist at remodel.** A parent who could not have spawned a Fable coordinator can
*remodel one into existence* in one command.

**On the 4000 chars.** The doc VERIFIES the number (`:98-99`, `bin/swarm:462-472`) and
never asks what it holds. A coordinator's in-flight judgment state — which children are
trusted, which artifact was half-believed and why, which claim it was about to attack — is
precisely what a good journal *summarizes* and never *contains*. **The doc's own falsifier
5 in SIMPLEST names this exact risk** (*"Post-compaction floundering. If agents restored
from a 4KB journal tail + original task measurably fail to resume…"* — SIMPLEST §6.5),
**and it was never resolved — only survived, by same-model restores.** Handing that same
4KB to a weaker model is a *strictly harder* version of a test the system has never
formally passed; it has only ever been passed on easy mode.

**In fairness — what survives.** For a **lateral** or **upgrade** remodel (sonnet→opus on
scope growth, which is the doc's own §6 scope-change trigger, `:459-465`), the analogy is
**sound**, the evidence supports it, and the doc's case is good. A stronger incumbent
recovering from a 4KB tail is *easier* than the restores already measured. **The scope-change
trigger is the strongest part of §6 and I cannot break it.** The ruling's defect is that it
generalizes from that case to *all* remodels without ever naming the direction.

---

## 2b. Self-remodel — the judgment point does not survive, and the doc's answer is one clause

**The doc's claim that the judgment point survives:**

> "**The steelman for respawn-successor, owed before the ruling:** a successor forces a
> judgment point — the parent harvests, judges, re-briefs; **an in-place switch lets a
> failing agent continue un-judged**… Answer: **the judgment point survives, because the
> switch is itself a recorded, judgeable act** — `remodel` requires a `--reason`,
> auto-appends `remodeled <old>→<new> by <caller> — <reason>` to the agent's journal, and
> flips the `ps` pin every reader sees." (`HARNESS.md:403-409`)

**Who may call it:**

> "**Who may call it:** the parent on a child (steering), **the agent on itself** (scope
> change), each with the reason journaled. **Enforcement is judgment, not a rule engine** —
> consistent with `cmd_send`, which checks existence, not relation (SIMPLEST §3.2)."
> (`HARNESS.md:436-438`)

**THE NAMED GAP: "recorded" and "judged" are not the same predicate, and the doc swaps
them.** Compare the two acts honestly:

| | Respawn-successor | Remodel |
|---|---|---|
| Who acts | **The parent** | **Anyone — including the agent itself** |
| When judgment happens | **Before** the successor runs — the parent must harvest, judge, re-brief | **Never, necessarily.** A record is *written*. Whether anyone *reads* it is unconstrained. |
| Is it synchronous with the judging party | **Yes, by construction** — the successor cannot exist until the parent acts | **No.** The journal line is appended **by the machinery**, after the fact. |

The doc's answer converts a **synchronous act by the judging party** into a **durable
artifact that the judging party may or may not ever read.** That is not preservation of
the judgment point; that is **replacement of a judgment with a receipt.**

**And the doc's own §2.3 explains why the receipt may never be read:**

> "**The single most expensive fact the field evidence produced: a dying or wedged agent
> is invisible.** trigger-scout's session-limit death rendered in `ps` as an ordinary
> `[live] q=0 idle` agent" (`HARNESS.md:138-141`)

The whole premise of §2.3 is that **parents are not continuously watching** — the operator's
own record says nobody noticed for **~2 hours** (`:446-448`). The remodel design's entire
answer to the un-judged-failing-agent objection is *"the `ps` pin flips and every reader
sees it"* (`:408-409`) — **but §2.3 is a two-page argument that there was no reader.** The
doc establishes the absence of the watcher in §2.3 and then, in §6, spends that same
watcher as the mechanism that makes remodel safe. **You cannot argue "a wedged agent is
invisible, therefore build `[blocked:]`" and then argue "a remodel is visible, therefore it
is judged" — the visibility of the pin is only as good as the attention that the same
document just measured to be absent.**

**On self-remodel specifically, PHILOSOPHY §4 is the live wire:**

> "**Judge artifacts, never claims.** … *'`DONE` means a turn ended — it is NOT proof the
> work is correct or complete.'*" (PHILOSOPHY §4, quoting WORLD.md)

> "**The test this gives you:** if you would need to read an agent's conversation to know
> whether its work is good, the task was delegated wrong." (PHILOSOPHY §4)

**A self-remodel is an agent storing a claim about its own capability.** *"I am
under-modeled for this; I am now Opus"* is exactly a self-assessment — and the failing
case is not the honest one. **The failure mode: a floundering agent remodels itself,
appends a `--reason` in its own words, and the journal now reads as a legitimate
scope-change rather than a rescue attempt.** The `remodeled sonnet→opus by self — scope
grew` line is *indistinguishable in the record* from `remodeled sonnet→opus by self — I was
drowning and hoped a bigger model would save me.* The doc never distinguishes them, never
names the abuse, and never gives it a falsifier.

**What the doc actually says about it — the complete text, quoted, because it is one
clause:**

> "**Enforcement is judgment, not a rule engine** — consistent with `cmd_send`, which
> checks existence, not relation (SIMPLEST §3.2)." (`HARNESS.md:437-438`)

That is the whole treatment. **And the `cmd_send` analogy is weak in a way worth naming:**
`cmd_send`'s unenforced relation is safe **because a message is a claim on one turn** — the
worst a misrouted send can do is consume a turn, and the recipient reads the sender's name
in the header (`WORLD.md` #4). A self-remodel is not a claim on one turn. **It changes who
is doing the work, for the rest of the work.** The doc reaches for the repo's most
permissive precedent and applies it to its least reversible act.

**The asymmetry, since §6 explicitly invokes MODEL-FIT's authority elsewhere:** MODEL-FIT
took a *measured* result — 0/135 mush, 17 behavior changes — to justify trusting a
compelled free-text field at **spawn**, where **the parent fills it about a child.** §6
extends that trust to a field an **agent fills about itself**, and the two are not the same
epistemic object: the parent's `--reason` answers *"can I cheaply tell this child is
wrong?"* — a fact about the parent — whereas the self-remodeler's `--reason` answers
*"am I good enough?"* — a fact about the writer, which MODEL-FIT §5 explicitly names as the
question that **"launders a guess into a decision"** and which it scoped the reason field
**away from** on purpose:

> "A parent asked *'why is Haiku right for this?'* must assert knowledge about a model's
> competence **that nobody in this repo has** — and will assert it fluently, which is
> precisely the confident-wrong artifact §6 exists to prevent." (MODEL-FIT §5)

**A self-remodel `--reason` is that forbidden question, asked of the one party least able
to answer it.** §6 rebuilds the exact field MODEL-FIT ruled against, and does not notice.

---

## 2c. The tombstone claim — **REFUTED.** The doc inverts SIMPLEST §3.3

**The doc's claim:**

> "Burning a name to change an attribute spends the ledger's sharpest signal on a
> non-event, and ***splits one task's history across two journals*, which is closer to
> violating 'one agent, one record' than the remodel is.**" (`HARNESS.md:411-413`)

And earlier, its characterization of what the tombstone is for:

> "**What 'one agent forever' actually protects.** **The tombstone exists so history never
> blurs two agents into one record (SIMPLEST §3.3)**" (`HARNESS.md:387-388`)

**The source, quoted exactly** (SIMPLEST §3, concept 3 — the section the doc cites):

> "**spawn with a chosen name.** … The name is a required argument because naming is
> delegation hygiene; **without lifetime uniqueness, history blurs two agents into one
> record.** **The tombstone is the journal file itself:** `journal/<name>.md` exists ⇒ the
> name is taken, forever."

**The doc's *characterization* is accurate — and it is fatal to its own conclusion.**

Read what SIMPLEST is protecting against: **two agents sharing one record.** That is the
harm. The mechanism — a name may never be reused — prevents *agent B* from writing into
*agent A's* journal.

**Now apply it to the two options honestly:**

| | What ends up in `journal/<name>.md` | Does history blur two workers into one record? |
|---|---|---|
| **Respawn-successor** | Agent A's history in `journal/A.md`; agent B's in `journal/B.md`. B's brief cites A's journal. **The split is a tombstone — it is the visible, addressable marker that a different worker took over.** | **NO. Two workers, two records. Exactly what the mechanism is for.** |
| **Remodel** | Opus-A's reasoning and Sonnet-A's reasoning, **interleaved in one file**, separated only by a `remodeled opus→sonnet` line the machinery appended. | **YES — two differently-capable workers, one record.** |

**THE NAMED GAP.** The doc says burning a name *"splits one task's history across two
journals, which is closer to violating 'one agent, one record'"* — **but "one agent, one
record" is not a rule that a task's history must live in one file.** It is a rule that a
*record* must belong to *one agent*. SIMPLEST says so in the same breath the doc quotes:
the harm is *"history blurs two agents into one record"* — **blurring, not splitting.** The
doc has substituted *splitting a task* for *blurring a record*, and then argued that the
mechanism designed to prevent blurring is guilty of it.

**A split across two journals is not a loss of history. It is the *shape* of the history.**
Nothing is lost: `journal/A.md` persists forever (*"files stay"* — `WORLD.md` #7), the
successor's brief cites it, and any reader who lands on B and asks "what came before?" is
handed A by the tombstone. **A remodel, by contrast, produces one file in which a reader
must notice a single machine-written line — or silently attribute Sonnet's judgment to
Opus.**

**And the loss is worse than "must read carefully," because of the doc's own reader
model.** §6's safety rests on *"flips the `ps` pin every reader sees"* (`:408-409`). But
**`ps` shows the pin at time T — the current incumbent.** A reader who consults `ps` at
time T sees `hc-red model=sonnet` and has **no way to know** that the judgment recorded in
`journal/hc-red.md` at T-2h was made by Opus. The pin is a **point-in-time fact about the
present**, and the history it was cited to protect is a **claim about the past.** They are
different objects, and the doc uses one to secure the other.

**Which loses more history? The remodel does, and it is not close.** Burning a name loses
*nothing* — it costs an extra file and a re-brief. A remodel loses **the attribution of
every journal entry to the mind that wrote it**, recoverable only by a reader who thinks
to scan the whole file for machine-appended remodel lines and reconstruct the timeline by
hand. That is *precisely* "history blurring two agents into one record" — the exact harm
SIMPLEST §3.3 names, and the doc quotes it correctly one sentence before contradicting it.

**One concession, made because it is real:** the doc's *"a burned name is the record of
ended work. Here the work has not ended"* (`:409-411`) is a genuinely good point, and it is
why my verdict on this surface is not a clean refutation of the whole section. Burning a
name **does** overload a signal. But the answer to "this signal is overloaded" is not "so
let two workers share one record" — it is to note that the *journal already timestamps
everything*, and a remodel could be made honest at zero cost by **writing the incumbent
model into every journal entry's header**, so that attribution survives the file. The doc
does not propose this, and the absence is what turns a design tension into a real loss.

## VERDICT — SURFACE 2: **WOUNDED, and the tombstone clause is REFUTED**

- **The identity ruling holds for lateral and upgrade remodels.** The evidence base
  (`_hc-field.md` §B1's ~10 same-day restores; trigger-scout resuming from its own death) is
  real, I checked it, and it genuinely establishes that this system treats the session as
  disposable. The scope-change trigger (sonnet→opus, `:459-465`) is the strongest argument
  in §6 and I could not break it.

- **It is unargued for a downgrade, and the doc ships a verb that permits one.** There is
  **no restriction anywhere in `HARNESS.md`** on `swarm remodel <seat> --model sonnet` —
  I grepped every occurrence. The restrictions the doc *does* impose are cross-vendor
  (`:456-458`) and cross-harness (`:631-634`). MODEL-FIT §3 — settled input per `:190-192` —
  says *"if the child will spawn, judge, harvest, close, or survive a restore, it runs Opus
  4.8. **No exceptions on cost grounds**"* and *"downgrading a seat to save tokens spends
  children to save on the parent. That trade is always backwards."* **§6 builds the bypass
  and never sees it.**

- **"Exactly the loss at compaction" is false in the word that matters.** Compaction is a
  loss the **same** reasoner recovers from; a downgrade is a loss a **weaker** reasoner must
  recover from, from 4000 chars (VERIFIED, `bin/swarm:462-472`) that were never designed to
  carry in-flight judgment state. The doc's ~10 restores are **10/10 same-model events** —
  the inductive base contains zero instances of the variable being generalized over.

- **The tombstone clause is REFUTED.** `HARNESS.md:411-413` claims burning a name is
  *"closer to violating 'one agent, one record' than the remodel is."* SIMPLEST §3.3 —
  which the doc cites and characterizes **correctly** at `:387-388` — says the harm is
  *"history blurs **two agents into one record**."* A split across two journals is **two
  records for two workers**, which is the mechanism working. A remodel is **two
  differently-capable workers in one record**, which is the named harm. The doc has the
  source right and the conclusion backwards.

**The strongest surviving attack (for hc-red to carry):** the remodel verb needs a
**direction gate**, and it is the same gate §2.4 already builds. §2.4 refuses a spawn:
*"swarm: haiku cannot hold an agent pane…"* (`:170-174`). §6 needs the twin refusal:
**a remodel that lowers a seat's tier is refused at the verb**, for the reason MODEL-FIT
already gives (*no exceptions on cost grounds*), and a **self**-remodel that lowers a tier
is refused outright, because it is an agent storing a claim about its own competence —
the artifact PHILOSOPHY §4 says the system must never store, and the exact question
MODEL-FIT §5 scoped the `--reason` field **away from** on the grounds that it *"launders a
guess into a decision."* Upgrade-on-scope-growth needs no gate and should ship. **Ship the
verb; gate the direction; name the incumbent in every journal entry.** That is a three-line
repair, and it costs the ruling nothing it was right about.

---

*Reviewer's note on my own method, so it can be judged: I read the four sources in full,
grepped `HARNESS.md` exhaustively for every remodel/tier/direction term before asserting
the absence of a downgrade restriction, and traced the watchdog convention to
`FLEET.md:286` and its two measured failures to `FLEET-EVAL.md:181-183` and
`FLEET-EVAL-V3.md:98-100` (both transcribed by the author's own child at
`_hc-eval-table.md:32,54`). The two claims I could **not** break, and want on the record as
surviving: §5's industry corroboration (`:358-364`), which is real and independent of local
doctrine; and §6's scope-change trigger (`:459-465`), which is the correct-size answer to a
measured 16% problem.*
