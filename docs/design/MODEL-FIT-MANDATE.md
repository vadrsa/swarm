# MODEL-FIT-MANDATE — should `swarm spawn` force a model choice and a reason?

**Author:** `mandate-red` (red team), reporting to `model-fit`. **Date:** 2026-07-13.
**Brief:** attack the operator's proposal — *"make `swarm spawn` pass a MANDATORY
model-choice REASON, recorded in the agent record"* — and return one recommendation.

**Overrule note (2026-07-13, added by `mf-amend`, not by the original author).** The
headline box immediately below reads *"`--model` stays OPTIONAL"* — read past that word
to lines 19-20 and §6: what this document actually specifies is that `swarm spawn`
**requires** `--model M` *or* the explicit token `--model inherit`, plus a required
`--why "<clause>"`. Nothing here was ever "omit the flag and get the default silently" —
that silent path is exactly what §6 closes. The operator has since ruled on the adjacent,
optional-leaning language in `docs/design/MODEL-FIT.md` §5 (see the superseded-ruling note
there): both fields are required, a spawn missing either fails. That ruling and this
document's own §6 mechanism are the same shape — `inherit` remains a legal, honorable
answer for `--model`; it is simply no longer sayable by omission. Read "OPTIONAL" in the
next paragraph as this document's own (since-clarified) shorthand, not as a claim that the
flag can be left off.

Every number below is cited to the line I read. I went in believing a forced
free-text reason would be compliance theater. **The repo's own evidence refuted my
prior, and I am reporting against it.** That reversal is the finding.

---

## THE RECOMMENDATION, up front

> **Option 2, hardened: `--model` stays OPTIONAL, but silence is no longer free.
> Make the CLI *ask*, make `ps` *show*, and let the parent answer "inherit" —
> out loud.**
>
> Concretely: `swarm spawn` requires **`--model M`** *or* the explicit token
> **`--model inherit`**, and in both cases a **`--why "<clause>"`** that is recorded
> in the agent record and **rendered by `swarm ps`**.

This is *not* option 1, 3, or 4 as stated. It is closest to 2, with the one change
that makes it bite: **the default is not removed, it is made SAYABLE.** The parent
may still inherit — they simply may not do it *silently*. See §6.

**The one-line rationale:** the failure in the field is not that parents choose
badly. It is that **no choice event ever occurs** — 142 of 143 spawns had no
decision point at all. You do not fix a missing decision by removing an option.
You fix it by making the tool *ask the question*, and by giving the answer a reader.

---

## 0. Two premises in the brief are wrong, and the corrections drive the answer

**(a) "Nothing in doctrine tells a parent that choosing is a thing a parent does."
FALSE — it already does, in the tool's own help.**

`bin/swarm:1104-1109`, in the `USAGE` string every agent can print with `swarm -h`:

> ```
>   swarm spawn <name> "<task>" [--model M] [--cwd DIR]   create a child; the name
>                                 is chosen, not derived; a name ever used errors.
>                                 --model is a CHOICE, not a default to inherit:
>                                 ask "can I cheaply tell this child was wrong?"
>                                 Seats and adopted judgment -> the strong model;
>                                 mechanically-checkable work -> a cheap one. Say
>                                 why in your journal. (docs/design/MODEL-FIT.md)
> ```

**This is option 4, verbatim, already shipped.** "`--model` is a CHOICE, not a
default to inherit… Say why in your journal." Doctrine-only is not a candidate to
be argued *for*. **It is the control arm, and it has already reported out: ~0%
adoption.** Any recommendation of option 4 must explain why the same text will work
the second time. I cannot construct that argument, so I do not make it.

> ⚠️ *Caveat I owe you:* that USAGE text is **new** (it is in the working tree, part
> of `model-fit`'s in-flight work — `docs/design/MODEL-FIT.md` is `Status: DESIGN`).
> So it has not yet had its fair trial in the field. But the *substance* of it —
> "the flag exists, use it when it fits" — has been available for the entire life of
> the swarm, and produced 1 real pin in 158. The control arm's result stands; the
> exact wording is what is untested. **This is the strongest thing an advocate of
> option 4 can say, and I flag it rather than bury it.**

**(b) "142 of 143 inherited; exactly one was ever pinned." Nearly right, and the
error is the most interesting number in this document.**

Measured, just now, over `.swarm/agents/*.json` (158 records):

| | count |
|---|---|
| records total | **158** |
| `"model": ""` (inherited — no decision) | **153** |
| `"model"` non-empty (pinned) | **5** |
| …of those, pinned to **`opus`** — *which is already the default* | **4** (3 are my own children; 1 is `updater-v2`) |
| …of those, pinned to a genuinely **cheap** model | **1** — `wmd-haiku` → `claude-haiku-4-5-20251001` |

So **four of the five "decisions" were no-ops** — a pin to the model you'd have got
anyway. And the *one* real cheap pin was not a fit judgment at all. Reading
`.swarm/journal/weak-model-deleg.md`: `wmd-haiku` and `wmd-opus` were spawned with a
**byte-identical task and one variable (`--model`)** — a deliberate **A/B experiment**
to find out whether a weak model over-delegates.

> **In 158 agents, nobody has ever once pinned a model because it fit the work.
> The single real pin was made to measure whether such pinning is even safe.**

That is a far stronger indictment than the brief's "142 of 143." The mechanism is
not underused. **It is unused.** And the mechanism-is-there-but-unused shape is
exactly what a tool-level prompt fixes and a doc does not.

---

## 1. The compliance-theater objection — REFUTED, on this repo's own data

This was my going-in position and the operator's first objection: *a required
free-text string is gameable; the agent will type "fits the task" and the field will
have forced nothing.*

**The repo has already run this exact experiment, and it is the closest available
evidence on Earth for this question.** Doctrine already compels one free-text
justification from every agent: *"a reconciliation entry names its falsifier (the
observation that would show you are off track)"* — a compelled, unenforced,
free-text justification, carried in the spawn header, across 158 agents. Same shape
as the proposed reason. **Did it produce mush?**

`docs/audit/org-review-falsifier-2026-07-12.md` — a pre-registered audit
(`docs/audit/_falsifier-rubric.md` fixes the classes *before* the count), four
independent readers:

| class of the 135 compelled falsifier statements | count | cite |
|---|---|---|
| (a) OBSERVABLE-IN-FILE — a real, checkable observation | **114** | `:75-76` |
| (b) OBSERVABLE-ELSEWHERE — real but no repo witness | 21 | `:77` |
| **(c) UNFALSIFIABLE-AS-WRITTEN — the predicted mush** | **0** | **`:78`** |

> **Class (c) = 0 of 135.** The audit's own words (`:39-40`): *"the predicted 'ritual
> mush' (**"if this turns out wrong"**) **does not exist in this corpus**."*

And the forward-hunt on the 114 checkable ones (`:84-87`):

| outcome | count |
|---|---|
| **FIRED-CHANGED** — the falsifier fired and the agent *changed course* | **17** |
| **FIRED-IGNORED** — the pathology | **0** |
| NOT-FIRED | 84 |
| CANNOT-TELL | 13 |

**Seventeen documented cases of a compelled free-text justification changing what an
agent did.** The specimen the audit rates best (`opencode-plugin-scout.md:429→435`):

> `:429` — *"FALSIFIER: if `messages.transform`'s injected message does NOT persist
> into the session's stored history … the agent would 'forget' its mail. THIS MUST BE
> TESTED."*
> `:435` — ***"MY OWN FALSIFIER FIRED.** `messages.transform` is a VIEW transform, not
> a session write. **Option (c) is DEAD as stated.**"*

That agent killed its own preferred design because a field it was *forced* to fill
made it look. **That is compelled articulation doing exactly the work the operator
hoped for, and it is measured, not argued.**

### The honest caveat on this number

My child `mr-theater` (grepping independently) surfaced ~3 journal falsifiers it
judged vacuous, against the audit's 0. Two instruments disagree. Even taking the
pessimistic reading, the theater rate is **~2-3%, not the ~90% my prior assumed.**
The direction of the finding does not move. I flag the disagreement rather than
report the tidier number.

**VERDICT: the "it's gameable, so it's theater" objection is empirically false in
this repo, with these models.** Claude agents, told to justify, mostly *justify*.
This is the single strongest argument FOR the operator's mechanism, and it is the
operator's own counter-counter. **I could not defeat it. I concede it.**

### The corroborating null: the name

`swarm spawn` **already has a mandatory, un-defaultable free-text field: the name.**
`claim_name` (`bin/swarm:761-768`) makes it physics — `O_CREAT|O_EXCL` on the journal;
a name ever used *errors, forever*. Result across 158 agents:
`grave-priorart`, `ps-model-red`, `wmd-haiku`, `fpc-s2-tail`, `weak-model-deleg`…

> **Generic slop names (`agent1`, `worker`, `test`, `tmp`): 0 of 158.** (measured)

A forced field on `swarm spawn`, filled by a Claude parent, **has already been shown
in this repo to produce non-degenerate output at a 100% rate.** The name is the
existence proof.

---

## 2. Blast radius — measured, and it is small

`grep -rn "swarm spawn"`, classified:

These numbers are not read off a grep — `mr-blast` **patched a scratch copy of
`bin/swarm`** with a required-model guard and **ran the suite** (`docs/audit/mandate-blast-radius.md`):

| class | count | what breaks |
|---|---|---|
| **(A) EXECUTABLE CALLERS** — code that *runs* `swarm spawn` | **9** | all in `tests/` |
| **(B) NORMATIVE DOCS/EXAMPLES** — text agents read and copy; a required flag makes these **stale** | **12** | `WORLD.md`, `skill/`, `docs/design/*` |
| **(C) HISTORICAL PROSE** — journals + audit describing past runs | **166** | nothing; they are history |

**MEASURED, not reasoned:** baseline `80 passed`. With the guard inserted at
`bin/swarm:857`: **6 failed, 74 passed** — one of which fails in an unpatched scratch
copy too (a symlink artifact). **Attributable failures: 5.**

**There is no machine-generated spawning anywhere.** No hook, no `install.sh`, no
middleware, no script calls `swarm spawn`. **Every real caller is a human or an agent
typing at a shell.** That is the point: the *only* audience for a required flag is a
reasoning model that will read the error and answer it. There is no brittle
automation to break.

**Cost: ~9 test call-sites, 12 doc files. An afternoon.** **Blast radius is NOT a
reason to reject the mandate.** I expected this to be the killer objection. It isn't.

### But the patch found a REAL bug, and it changes the implementation

Three of the five failures are not "test needs a flag." They are the guard firing
**in the wrong place**:

| test | expected stderr | got instead |
|---|---|---|
| `test_spawn_confirmed_failure_tears_down_but_keeps_tombstone` | `"did not start"` | **the model-guard message** |
| `test_spawn_outside_herdr_refused_before_tombstone` | `"not inside herdr"` | **the model-guard message** |
| `test_swarm.py:536` name-refusal | `"bad name"` | **the model-guard message** |

A naive `if not model: die(...)` placed after flag-parsing **pre-empts the name check,
the herdr check, and the teardown path** — it masks better errors and fires *before*
`claim_name`, changing which failures burn a name. **Moving the guard to just after the
herdr check (`bin/swarm:872`) drops attributable failures 5 → 2** (measured).

**And the dangerous one is a test that stays GREEN.** `test_spawn_bad_names_refused`
(`test_swarm_process.py:264-268`) asserts only `returncode == 1`. Under a required
flag, **everything** exits 1 — so it keeps passing while **silently ceasing to test name
validation at all** (all six cases: `Worker`, `has space`, `-lead`, `x*41`, `operator`,
`delivered`). A green test that tests nothing is worse than a red one. **Fix it to
assert on stderr, in the same commit.**

*Also measured, and a trap for whoever implements this:* `grep -rn "swarm spawn" .`
**does not descend into `.swarm/`** and finds **zero** literal hits in `skill/` — which
nonetheless holds **two** normative surfaces (`skill/SKILL.md:59,143`). **A literal-grep
doc sweep would skip the skill entirely.** Count by explicit path.

---

## 3. The write-only objection — CONCEDED, and it is the real defect

*Does an audit trail nobody reads change behavior? Who is the consumer?*

**Today: nobody. The field is genuinely write-only.**

- The record `.swarm/agents/<name>.json` **already has a `model` field** —
  `bin/swarm:920-923` writes `{name, parent, pane, tab, model, cwd, task, ts}`. The
  data the operator wants recorded **is already being recorded.**
- `swarm ps` — "the one view" — **does not show it.** `walk()` at `bin/swarm:539-548`
  renders name, liveness, `q=`, idle-age, and last-words. **No model.**
- Nothing else parses `agents/*.json` outside `bin/swarm` and `tests/`.

> **So the "record the reason in the agent record" half of the operator's proposal is
> the half that does nothing.** A reason written to a JSON file that no view renders
> is a reason nobody will ever read. Recording is necessary; it is not sufficient,
> and on its own it is theater *of a different kind* — the tool would be
> accumulating evidence in a drawer.

**This is the strongest surviving objection to the proposal as literally stated, and
the fix is one line.** `render_ps` is a pure function that already receives the full
records; `a.get("model")` is in scope at `:539`. Put the model on the tree line:

```
├─ mr-blast [live] q=0 idle 4m                     ← today
├─ mr-blast [opus] [live] q=0 idle 4m              ← one line, and the field has a reader
```

**A mandate without this change is write-only and I would oppose it.** With it, every
`swarm ps` — the view every parent and the operator already look at constantly —
becomes a standing audit of every model decision in the tree. **The reader problem is
real, and it is cheap. Fix it in the same change or don't ship the mandate.**

---

## 4. The objection I could NOT defeat, and it is not the one anybody named

Not gameability. Not blast radius. This:

> **A mandated reason forces a parent to justify a choice the repo cannot yet inform
> — and a recorded reason LAUNDERS a guess into a decision.**

The one agent that ever really chose a cheap model (`weak-model-deleg`) did so to
**find out whether cheap models are safe as swarm children at all** — and *that
experiment has not landed.* Its own journal names the open question: does a weak
model, out of depth, **over-delegate to escape a task it cannot hold?** Unknown.
`FLEET-EVAL-V3` measured deepseek and GLM, never Haiku, and never asked this.

So on the day you make `--why` mandatory, a parent spawning a grep-sweeper must type
a justification for Haiku while the repo's own open question is *"is Haiku safe to
spawn at all?"* The reason field will be filled — **confidently, fluently, and
without evidence.** And unlike a falsifier (which is cheap to make honest: *"I am
wrong if X"*), a *fit* claim asserts knowledge about a model's competence that the
parent does not have. **The falsifier precedent does not cover this**, because
falsifiers are self-referential and model-fit reasons are not.

### The hazard, corrected — it is not fabrication, and this is the sharpest point in the document

`mr-reader` reframed my own objection and the corrected version is worse than mine:

> **The danger is not a parent writing a FALSE reason. It is a parent writing an
> HONEST one** — *"cheap: this is mechanically checkable"* — **obeying Rung 3
> exactly, and getting a child that reasons fine and never reports.**

**A mandate makes every parent CITE Rung 3 at every spawn. Rung 3 is the one rung the
repo has not benchmarked.** So the mechanism would propagate an untested claim *under
the appearance of diligence*, 158 times, with a written justification attached to each.
Compelled articulation doesn't make the claim true — it makes it **look adjudicated.**

**And Rung 3's own falsifier appears to be firing RIGHT NOW.** `MODEL-FIT.md:293-299`
pre-registered it; `mr-reader` observed it live in `wmd-haiku` (n=1, unreviewed, still
running — a raw observation, not a finding):

| arm | over-delegated? | held the seat? |
|---|---|---|
| `wmd-haiku` (Haiku 4.5) | **No — spawned zero children.** The feared failure did *not* happen. | **No.** No journal, no `swarm send`, no artifact, 18m idle. **It went silent.** |
| `wmd-opus` (control) | No | Yes — delivered 25KB and explained its own non-delegation |

That is **exactly** the FLEET-EVAL-V3 shape — *"it knows who its parent is and does not
use the verb"* (`:76-78`) — reproducing **in-family, on a Claude model**, on the rung a
mandate would have parents lean on. The cheap model didn't reason badly. **It stopped
holding the seat.** If that survives review, Rung 3 as written is not just unbenchmarked;
it is pointing the wrong way, and a mandate would have been busily generating honest,
well-formed, *wrong* justifications for it.

**This is the argument against the mandate that I could not fully defeat, and it is not
the one anybody named going in.** It does not kill the mechanism — it **sequences** it.
See §6.5.

**Why it does not kill the recommendation — the thing that dissolved the *fabrication* version.**
`docs/design/MODEL-FIT.md:29-31` does not ask "which model is smarter?" It asks:

> **"Can I cheaply tell that this child was wrong?"**

That is a question **about the parent's own verification capacity**, and the parent
**always knows the answer.** *"I will read every line of this doc anyway"* is
knowable at spawn without a single benchmark. The ladder (`:41-45`) is answerable
today, from facts the parent already holds. **That is what makes a mandated reason
answerable honestly rather than fabricated** — and it is why the reason must be
**scoped to that question**, not to "why is this model good."

**But the residue is real and I concede it:** rung 3 ("mechanically checkable →
Sonnet/Haiku") *does* rest on unlanded evidence. **Until `weak-model-deleg` reports,
the honest mandate can force the QUESTION but must not pretend the ANSWER is
known.** Which is exactly what option 2-hardened does — it lets the parent answer
`inherit`, out loud, and that is a *legitimate, evidence-respecting answer* today.

---

## 5. Why not the other options

**Option 1 (`--model` mandatory, reason optional) — NO.** Forces the *cheap* half and
drops the *valuable* half. Naming `opus` is free and decides nothing — we measured
that: **4 of the 5 pins in repo history were `--model opus`, a no-op pin to the
existing default.** A mandatory `--model` would have produced 158 of those. It
manufactures the *appearance* of decisions. Worst option on the table.

**Option 3 (BOTH mandatory always) — NO, on one specific ground.** It abolishes
inheritance, and **inheritance is usually correct.** `MODEL-FIT.md:47` sets the
ladder's fall-through to Opus *on purpose*. A rule whose right answer is "the
default" ~80% of the time, but which forbids saying "the default," trains parents to
dress up the default in fresh prose 158 times. **That is where theater would actually
be manufactured** — not by the reason field per se, but by forcing a *distinct-looking*
answer where the honest one is "same as usual, and here's why that's right." Option 3
takes the one thing that reliably produces honest text (a real question) and attaches
it to a fake choice.

**Option 4 (doctrine-only) — NO. It is the control arm and it already reported.**
See §0(a): the doctrine is *already in the USAGE string*, and the field result is
1 real pin in 158. `references/COORDINATING.md:28-31`, quoted in `MODEL-FIT.md:16-18`,
explains why, and it is the load-bearing sentence in this whole argument:

> **"agents do not invent structural moves that are not in their frame, and reliably
> execute the ones that are."**

A doc is not the frame. **The command line is the frame.** An agent typing
`swarm spawn foo "task"` is not reading `MODEL-FIT.md`; it is completing a command it
has seen 158 times. **The only place to put the question is in the thing the agent
actually types.** That is the entire case for a CLI-level mandate, and it is why the
operator's instinct — *put it in the tool* — is right.

---

## 5b. Where I disagree with my own parent — narrowly, and it is the whole question

`MODEL-FIT.md` §5 has already ruled on this, and I am partly *agreeing* with it. Its
ruling: *"the default does NOT change… What changes is that 'unspecified' stops being
invisible."* And: *"`swarm spawn` help / `swarm world` — the flag stops being a bare
token in a usage line and starts **asking the question**."*

**We agree on almost everything.** Keep `inherit` as the default (its reason 3 is
right and I adopt it: *"inherit is the correct direction to fail in"*). Don't build a
classifier. Make the choice visible. **My recommendation is §5's own principle, taken
one step further than §5 takes it.**

The disagreement is exactly one step wide:

> §5 makes the choice mandatory **in doctrine and in the help text**. It leaves the
> CLI able to accept a spawn that makes no choice at all.

**That is the control arm, and it has already reported (§0a).** §5's own diagnosis is
the refutation of §5's own remedy — it quotes `references/COORDINATING.md:28-31`:
*"agents do not invent structural moves that are not in their frame, and reliably
execute the ones that are."* **A help string is not the frame. The command the agent
types is the frame.** An agent writing `swarm spawn foo "task"` is completing a
pattern it has seen 158 times; it is not printing `--help` first. §5 correctly
identifies that the fix must sit "exactly where the decision is made" — and then
places it one layer away from there.

**So: adopt §5 entire, and close the last gap by making the CLI refuse a spawn that
answers nothing.** `inherit` remains available, honorable, and usually right. It just
has to be *typed*. That is the minimum change that puts the question in the frame
rather than adjacent to it.

---

## 6. The recommendation, precisely

```
swarm spawn <name> "<task>" --model <M|inherit> --why "<clause>" [--cwd DIR]
```

1. **`--model` is REQUIRED, but `inherit` is a legal, honorable answer.** This is the
   crux. We are not removing the default — we are **removing the SILENT default.**
   The parent must *say* `inherit`, which converts a non-event into a decision with a
   name. Nothing is forbidden; something is now *asked*.
2. **`--why "<clause>"` is REQUIRED, and the prompt scopes it.** The error text must
   ask the ladder's question, not "justify yourself":
   > `spawn: --why is required. Answer ONE question: can you cheaply tell this child`
   > `was wrong? Seat-holding or judgment you will adopt -> a strong model. Mechanically`
   > `checkable (a count, a grep, a list of paths) -> a cheap one. If you cannot tell`
   > `cheaply, say so and inherit. (docs/design/MODEL-FIT.md)`
   A scoped question gets a real answer; "give a reason" gets "fits the task." **The
   prompt is the mechanism.** This is the difference between the name field (which
   works) and a generic string (which wouldn't).
3. **Record it:** add `"why"` beside the existing `"model"` at `bin/swarm:920-923`.
4. **RENDER IT — non-negotiable, ships in the same commit.** `render_ps`/`walk`
   (`bin/swarm:539-548`) puts the model on the tree line. **Without a reader, do not
   ship any of this** (§3).
5. **Place the guard AFTER the herdr check, immediately before `claim_name`
   (`bin/swarm:872`)** — not after flag-parsing. **MEASURED: correct placement drops
   attributable test failures from 5 to 2** (`mr-blast`). The naive placement hijacks
   the stderr of the `"bad name"` and `"not inside herdr"` refusals — refusals that
   *must* fire before the tombstone is claimed. Getting this wrong doesn't just break
   tests; it changes which failures burn a name forever.
6. **Pay the blast radius:** 9 test call-sites, 12 normative surfaces (§2). **Three of
   the twelve are inside `bin/swarm` itself and must change together** — and the
   highest-leverage line in the whole radius is **`spawn_header` (`bin/swarm:777`)**,
   the text injected into *every child's task*. It currently teaches the bare, no-flag
   form, and it is frozen into 162 emitted `.task` files. **That line is where 158
   agents learned to spawn without choosing.** Changing the USAGE string without
   changing `spawn_header` fixes nothing.

## 6.5 The sequencing condition — ship it, but not alone

Because of §4, the mandate must **not** ship pointing at an unbenchmarked Rung 3.
Either:

- **(a) Land the eval first.** `MODEL-FIT.md:293-299` says two cells through the
  **already-built** rig (`docs/audit/bench/`) collapse the confound in *a few hours*.
  That is cheap. Do it, then mandate.
- **(b) Or ship the mandate with Rung 3 marked, at the point of decision, as
  `directional — unbenchmarked`,** in the `--why` error text itself. A parent told the
  truth ("we think cheap is fine for mechanically-checkable work; we have not proven
  it") will write an honest, *hedged* clause and stay alert. A parent told a confident
  rule will write a confident clause and stop looking.

**(a) is better and it is nearly free. Prefer (a).**

**Escalation, out of my scope and passed up:** the `wmd-haiku` experiment — the *only*
real model-fit evidence this repo has ever generated — currently has **its sole artifact
in `/private/tmp` and nothing in `docs/`**, while `weak-model-deleg` sits live with
unread mail and never spawned the adversarial reviewer its own brief mandated. **One
cleanup and the evidence evaporates.** `model-fit` should get that arm decided and
written into `docs/audit/` before it ships Rung 3.

**Why this is the strongest version and not a compromise:** it forces the *question*
(which the field proves parents answer honestly, §1) without forcing a *fake choice*
(which is where theater would be born, §5). It respects the one thing we do not yet
know — whether cheap models are safe in seats (§4) — by making `inherit` a
first-class, sayable answer rather than a silent one. And it gives the record a
reader, which is the only thing that makes any of it more than a drawer.

---

## 7. The falsifier for this recommendation

I name what would show me wrong, per the doctrine I am arguing about:

> **Ship it, then read the next 30 spawns' `--why` clauses in `.swarm/agents/*.json`.**
>
> **I am WRONG if:** ≥1/3 of them are vacuous — *"fits the task"*, *"appropriate for
> this work"*, *"standard choice"* — i.e. class-(c) mush at a rate the falsifier
> corpus never produced (0 of 135). That would mean model-fit reasons are *unlike*
> falsifiers: the knowledge isn't there, so the field fabricates, and §4's objection
> beats §1's evidence. **Roll back to doctrine-only and wait for `weak-model-deleg`.**
>
> **I am RIGHT if:** the clauses name the *verification* ("I will read this doc line
> by line anyway"; "this is a path list I can diff in 5s"), **and** the pin rate moves
> off the floor — i.e. at least a few spawns choose `sonnet`/`haiku` and their work is
> not visibly worse. The tell is `inherit` clauses that give a *reason to inherit*
> rather than a reason to exist.
>
> **The cheap early read:** the first 10 spawns. If `--why` is being answered with the
> *ladder's* vocabulary (verifiability), it is working. If it is answered with
> *task-difficulty* vocabulary ("this is complex"), the prompt failed and the field
> is mush — because the whole design rests on asking about the PARENT's checking
> ability, not the child's smarts.

---

## Appendix — sources, all read at the line

| claim | cite |
|---|---|
| `cmd_spawn`, flag parse, `--model`/`--cwd` optional | `bin/swarm:845-857` |
| agent record written, incl. existing `model` field | `bin/swarm:920-923` |
| `write_launcher` — inheritance is *defaulting* (no `--model` passed at all) | `bin/swarm:833-836` |
| `claim_name` — the one physics-enforced mandatory field | `bin/swarm:761-768` |
| USAGE already carries the model doctrine (= option 4, shipped) | `bin/swarm:1104-1109` |
| `swarm ps` `walk()` renders no model → field is write-only | `bin/swarm:539-548` |
| falsifier corpus: 0/135 unfalsifiable; 17 FIRED-CHANGED; 0 FIRED-IGNORED | `docs/audit/org-review-falsifier-2026-07-12.md:75-87` |
| pre-registered rubric (classes fixed before counting) | `docs/audit/_falsifier-rubric.md` |
| the ladder; "can I cheaply tell this child was wrong?" | `docs/design/MODEL-FIT.md:29-47` |
| "agents do not invent structural moves not in their frame" | `references/COORDINATING.md:28-31` |
| the one real cheap pin was an A/B experiment, not a fit call | `.swarm/journal/weak-model-deleg.md` |
| FLEET-EVAL-V3: weak models pass duties, fail the *seat* | `docs/design/FLEET-EVAL-V3.md:23-27, 76-78, 90-103` |
| 9 executable spawn call-sites, all tests; guard patched into a scratch tree and the suite RUN (80 passed → 5 attributable failures); the guard-ordering bug | `docs/audit/mandate-blast-radius.md` (`mr-blast`) |
| `model` field is write-only: no reader in `ps`/`send`/`close`; `render_ps:491` is the one-line fix | `docs/audit/mandate-reader-and-choice.md` (`mr-reader`) |
| 158 records / 153 inherited / 5 pinned / 4 no-op / 1 real | measured over `.swarm/agents/*.json` |
