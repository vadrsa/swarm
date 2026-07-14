# Mandate scoping — extracted verbatim from MODEL-FIT.md §5/§6/§7 and HARNESS.md §2.4

> SUPERSEDED by the shipped error text in bin/swarm's spawn_mandate_error(); kept for the record (the reasoning/citations behind the wording, including corrections to a misreading of MODEL-FIT.md).

Source: `git show swarm-dev/model-fit:docs/design/MODEL-FIT.md` (656 lines) +
`.swarm/journal/mandate-red.md` (adversarial review, this repo) + `docs/design/HARNESS.md`
§2.4 (current branch). All quotes verbatim with line numbers against the `/tmp/MODEL-FIT.md`
dump of the `swarm-dev/model-fit` blob, and against `docs/design/HARNESS.md` on disk.

---

## 1. The scoping rule, verbatim

The ladder's question, stated at the top of the doc (MODEL-FIT.md:29):

> **Can I cheaply tell that this child was wrong?**

The load-bearing distinction, MODEL-FIT.md:449-464 (§5):

> **The reason must be scoped to the ladder's question** — *"can I cheaply tell that
> this child was wrong?"* — **not to "why is this model good."** This distinction is
> load-bearing, and it comes from the one objection the review could not defeat:
>
> > *A mandated reason forces a parent to justify a choice the repo cannot yet inform —
> > and a recorded reason **launders a guess into a decision**.*
>
> That is the sharpest thing said in this workstream. A parent asked *"why is Haiku
> right for this?"* must assert knowledge about a model's competence **that nobody in
> this repo has** — and will assert it fluently, which is precisely the confident-wrong
> artifact §6 exists to prevent. A parent asked *"can you cheaply tell if this child is
> wrong?"* is asked about **their own verification capacity, and they always know the
> answer**: *"I will read every line of this doc anyway"* is knowable at spawn without a
> single benchmark. **The question the ladder asks is answerable honestly today. The
> question "which model is smarter" is not.**

Your brief's paraphrase ("a fact about the PARENT'S OWN VERIFICATION CAPACITY, which the
parent can always honestly answer" / "launders a guess into a decision") is faithful — both
phrases are lifted near-verbatim from the passage above. Confirmed correct.

**§6's tie-breaker**, which the reason should ultimately serve (MODEL-FIT.md:565-566, 576-578):

> **When you cannot cheaply tell whether the child is wrong, buy the model that is
> less likely to be wrong. Save money only where being wrong is cheap to catch.**
>
> **Put the strong model where being wrong is expensive and invisible. Put a cheap one
> only where being wrong is cheap to catch — because there, and only there, a mistake
> has somewhere safe to land: a strong parent who is reading the artifact anyway.**

And explicitly, MODEL-FIT.md:568-572 — **this is not a cost rule**:

> **And be clear about what this rule is for, because the repo will otherwise kill it
> correctly.** This is **not a cost-savings rule**, and it must not be defended as one.
> ... the scarce resource here has never been quota — it is **attention**, and
> correctness. A rule that says *"spend less"* earns nothing and would deserve the
> graveyard.

## 2. Where the reason is surfaced — record vs. journal, considered and ruled

You asked specifically whether §5 considered a record field and rejected it. **It did not
reject a record field — the record field already exists and is not the gap.** Precisely
(MODEL-FIT.md:465-472):

> **Give the field a reader, in the same change, or do not ship it.** The record
> `.swarm/agents/<name>.json` **already writes `model`** (`bin/swarm:916-919`) — the data
> the proposal wants recorded *is already recorded*, and it changed nobody's behavior for
> 143 spawns, because **`swarm ps` — "the one view" — does not render it**
> (`bin/swarm:539-548`). A reason written to a JSON file no view shows is evidence
> accumulating in a drawer. Putting the model on the `ps` line is one line, and it turns
> the view every parent already reads into a standing audit of every model decision in
> the tree. **A mandate without a reason is write-only, and should be opposed.**

So the actual ruling is: **record the model (already happens) → render it in `swarm ps`
(does not happen yet, costed at "one line") → the *reason* itself lives in the journal**,
not a new JSON field, per §5b (MODEL-FIT.md:535-537):

> **`skill/SKILL.md`** — the spawn doctrine gains a step: *choose the child's model by
> task-fit, and say why.* A coordinator that spawns without naming a model is skipping
> a step, the same way one that spawns without a brief is.

And the CLI-level version is the help text asking the question at the point of decision
(MODEL-FIT.md:538-540), not a stored field:

> **`swarm spawn` help / `swarm world`** — the flag stops being a bare token in a usage
> line and starts *asking the question*. This is the cheapest possible nudge and it
> sits exactly where the decision is made.

**Correction to your brief:** §5 does not "consider and reject a record field in favor of
the journal" as a binary choice — it says the record already has `model` (write-only,
unread), argues `ps` should render it (not yet built), and separately places the *why*
in the journal/doctrine, not in a new structured field. If you write "considered and
rejected," you'll be asserting something the doc doesn't quite say — cite it as above
instead. Also note: **§5 explicitly declines to implement the CLI mandate in that PR**
(MODEL-FIT.md:474-483) — it ships doctrine + help text only, and calls the mandate
"specified and recommended... deliberately left unimplemented," costed at "≥9 test
call-sites and 12 doc files (a floor)." If your PR *does* implement `--model`/`--reason`
as required flags, you are doing the thing §5 deferred — say so explicitly in your PR
body, since it's a scope decision beyond what MODEL-FIT shipped, not a mechanical
extraction of it.

## 3. Your error text — critique

Your draft:
```
swarm: spawn needs --model <M> and --reason "<one clause>" — the parent
chooses the child's model. Ask: can you cheaply tell that this child was wrong?
tokens: opus sonnet fable (agents) · haiku (see below) · default (if configured)
```

The doc has no CLI error string of its own to compare against for `--model`/`--reason`
(§5 didn't implement the mandate) — but HARNESS.md §2.4 *does* ship a live refusal-string
precedent for the haiku case (quoted in full in §4 below), and its shape is instructive:
it states the fact, cites the *source* of the fact, and names what to do instead, in
that order, in about three lines.

**Does your draft teach the distinction, or just scold?** Verdict: **partially teaches,
but buries the teaching.** "Ask: can you cheaply tell that this child was wrong?" is the
right question, verbatim from the doc — good. But:

1. It's phrased as an instruction to answer a question, not paired with what a *bad*
   answer looks like. A first-time reader has no signal that "sonnet, it's complex" is
   the failure mode being guarded against. The doc's own framing pairs the good question
   with the banned one explicitly ("not to 'why is this model good'") — your error text
   drops that half, so it under-teaches by omission.
2. "one clause" sets a length expectation but not a content expectation — an agent under
   pressure to be terse will happily produce a terse *bad* answer ("fits the task" is
   already one clause).
3. The tokens line is useful but disconnected from the teaching line above it — it reads
   as a separate reference card, which is fine, but means the error is really two
   messages stapled together.

**Proposed tightened version** (still 3-4 lines, adds the negative case in ~6 words):

```
swarm: spawn needs --model <M> and --reason "<clause>" — the parent chooses.
Answer: "can I cheaply tell this child was wrong?" — NOT "why is this model good"
(that launders a guess into a decision).
tokens: opus sonnet fable (agents) · haiku (see below) · default (if configured)
```

This keeps yours nearly intact but makes the banned framing a visible clause instead of
an implication, which is the one thing a CLI string can do that a doc paragraph does at
length. If you want it shorter than that, cut the tokens line to a `swarm world` pointer
instead — but I'd keep the negative case over the tokens line if forced to choose one.

## 4. Haiku refusal text — verdict: HARNESS.md already ships better wording than the brief's draft

Your brief's draft:
```
swarm: haiku is marked not agent-capable (operator ban 2026-07-13: no auto
permission mode). Use sonnet, or a one-shot leaf if the task is a single completion.
```

**This overclaims relative to what's on disk.** `docs/design/HARNESS.md:210-215` (current
branch, already written) ships this exact refusal, and it is more honest than your draft:

```
$ swarm spawn scout "read the doc" --model haiku --reason "cheap read"
swarm: haiku is marked not agent-capable (operator ban 2026-07-13: no auto
permission mode; settling probe not yet run — see HARNESS.md §9.4). Use
sonnet, or a one-shot leaf token if the task is a single completion.
```

The difference is exactly the caveat you were told not to bury: **"settling probe not
yet run — see HARNESS.md §9.4"**. Your draft omits it. HARNESS.md §2.4 states in prose why
that clause is non-negotiable (lines 217-219):

> The refusal text carries its own epistemic status on purpose: a gate that reads as
> "the Haiku problem is solved" while the all-models permission gate stays unbuilt would
> be the harm the source warns about.

And the underlying fact your draft's framing risks hiding, HARNESS.md:187-194 (§2.4, point 1):

> **The measured cause of the Haiku wedge is infrastructure, not the model.** The
> probe's own bolded conclusion: *"The stall was caused by a permission gate swarm
> hands EVERY child regardless of model. Opus would block too… A tier rule about cheap
> models does not fix an infrastructure gate that fires on all models. Aim the fix at
> the gate."* ... The settling probe — an Opus-pinned child into the same first-touch
> wall — is that source's *"top re-run item"* and **has never been run.**

And the ban's actual status, HARNESS.md:198-204 (§2.4, point 3):

> **The operator's Haiku ban stands above that as standing policy**... on a
> capability claim — *"it doesn't have auto mode"* — that is the operator's assertion,
> not an independent measurement. If true, it is exactly the kind of per-model fact
> the gate exists for...

**Verdict on your draft: it overclaims by omission.** "no auto permission mode" stated
bare, with no pointer to the unsettled probe, reads as an established fact about Haiku
rather than an untested operator assertion sitting above an infrastructure bug that
would wedge *any* model. Ship HARNESS.md's wording verbatim — it already says everything
your brief asked for, in the same length budget, and it's already reviewed (§10 of that
doc). Don't re-derive a weaker version.

## 5. Exemplars

### 6 passing exemplars (real reasons, ladder's verification vocabulary)

| Child kind | Model | Reason (verbatim, as you'd write it) | Why it passes |
|---|---|---|---|
| Test fixture's throwaway worker | sonnet | "asserts a fixed string in stdout; I diff the literal output, no reading required" | Names the exact cheap check the parent will run — not the model's ability, the parent's plan. |
| Doc example's coordinator | opus | "this is a seat — it will judge and harvest its own children; a coordinator's mistakes compound silently, I can't spot-check a tree" | Cites Rung 1's seat rule via verification cost (can't cheaply audit compounding judgment), not "opus is smarter." |
| Code-writing agent (a real diff) | opus | "I will read the diff line-by-line before merging regardless, but a subtly-wrong abstraction reads as correct on a skim — I want the model least likely to hand me that" | Explicitly invokes §6's tie-breaker: buy the model less likely to be wrong when wrongness is fluent, not loud. |
| Exhaustive-search / census agent | sonnet | "output is a list of call-sites; I'll grep-count it myself in 10 seconds against the same pattern" | Names the actual spot-check the parent will perform — textbook Rung 3. |
| Red-team / adversarial reviewer | opus | "the whole product is 'did it find the real hole' — a false 'no holes found' is invisible to me by construction, I have no independent check" | Directly matches §6's "a red-team that reports no holes found because it could not find them" — names why the parent cannot verify. |
| One-shot extraction leaf (e.g., this task) | sonnet | "quoting a doc verbatim with line cites — I will open the doc at those lines myself before using the quote, so a wrong extraction is caught for free" | States the check is already part of the parent's own workflow — the cheapest possible real reason. |

### 4-5 failing exemplars (plausible but fail the rule)

| Reason as written | Diagnosis |
|---|---|
| "sonnet — this task is fairly simple" | **Task-difficulty vocabulary.** Talks about the task, not the parent's ability to catch an error. Doesn't say what check exists. |
| "opus — needs strong reasoning for this" | **Model-virtue vocabulary.** Asserts a competence claim ("opus reasons better") that MODEL-FIT.md:457-459 explicitly names as unavailable knowledge in this repo — exactly the laundering the rule bans. |
| "fits the task" | **Vacuous.** The literal string the whole mechanism exists to prevent (MODEL-FIT.md:421-422); satisfiable by any child, teaches nothing, verifies nothing. |
| "haiku is cheaper and this is low-stakes" | **Cost-framed, and §6 explicitly forecloses this**: "this is not a cost-savings rule... a rule that says 'spend less' earns nothing and would deserve the graveyard" (MODEL-FIT.md:568-572). Even if the model choice is *correct*, the stated reason fails because it answers the wrong question. |
| "sonnet should be able to handle this fine" | **Unfalsifiable / hedge-without-a-check.** "Should be able to" names no verification step at all — nothing the parent commits to doing, so there's no observable that would prove the reason wrong. |

### The tell — one-sentence test

> **Does the clause name a check the parent will perform (or already trusts), or does
> it name a property of the model or the task? If you can delete "I" from the sentence
> and it still makes sense, it failed** — a real reason is always about what *you* (the
> parent) can or will do, not about what the child or the task *is*.

## 6. Summary for spawn-mandate

Verbatim rule (MODEL-FIT.md:449-464): reason must answer *"can I cheaply tell that this
child was wrong?"* — a fact about the **parent's verification capacity**, always honestly
answerable. It must NOT answer "why is this model good" — that "**launders a guess into a
decision**." Tie-breaker (§6): "when you cannot cheaply tell whether the child is wrong,
buy the model less likely to be wrong" — explicitly **not** a cost rule.

Surfacing: `model` is already recorded (bin/swarm:916-919) but `swarm ps` doesn't render it
(§5) — "a mandate without a reader is write-only, and should be opposed." The *reason*
itself belongs in doctrine/journal (SKILL.md step + help text), not a new JSON field — §5
did not reject a record field in favor of the journal as a binary choice; it found the
record field already exists, unread, and separately placed the "why" in doctrine. §5
explicitly ships doctrine-only and **defers the CLI mandate** as its own reviewed change
(≥9 test call-sites, 12 doc files, floor not total) — if your PR implements the mandate
itself, that's a scope step beyond MODEL-FIT, flag it as such.

Your error text: directionally right, undersells the banned framing by only implying it —
add the explicit "NOT 'why is this model good'" clause (see §3 above for tightened text).

Haiku refusal: **your draft overclaims** — it states "no auto permission mode" as bare
fact. HARNESS.md:210-215 already ships the honest version with "settling probe not yet
run — see HARNESS.md §9.4" included, plus the on-disk finding that the real cause is an
infrastructure gate hitting every model, not a Haiku-specific defect. Use HARNESS.md's
wording verbatim; don't re-derive a weaker one.

The tell: a real reason names a check the parent will perform; a failed one names a
property of the model or task. Delete-the-"I" test: if the sentence survives without
the first person, it failed.
