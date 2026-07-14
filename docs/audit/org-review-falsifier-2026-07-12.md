# Is `falsifier-not-honored` detectable from the journal files?

> SUPERSEDED as a live question by org-review-graveyard-2026-07-12.md and ORG-REVIEW.md's RED review; kept for the record (the rigorous "falsifier orphaning" empirical finding — 114 statements, FIRED-IGNORED=0 — cited by later docs but not restated in full).

**Probe:** falsifier-probe (child of shape-forensics) · **Date:** 2026-07-12
**Question:** Can an instrument detect *"the agent named a falsifier, the falsifier FIRED, and the
agent did NOT change course"* by reading `.swarm/journal/*.md`?

**Every claim below is marked VERIFIED (I read the line) / MEASURED (I counted it) / REASONED (I inferred it).**

---

## THE ANSWER, up front

**NO — and not for the reason the hypothesis assumed.**

The pathology is **not hiding** in these journals. It is **absent**, and the corpus is structurally
incapable of recording it in the overwhelming majority of cases.

Two numbers carry the whole finding:

| | count | source |
|---|---|---|
| Class-(a) falsifier statements forward-hunted across the 10 richest journals | **114** | MEASURED (4 independent readers) |
| **FIRED-IGNORED (the pathology) found** | **0** | **MEASURED — VERIFIED by full-text read** |
| Journals naming a falsifier whose **last falsifier sits in their last entry** | **93 of 103** | MEASURED |
| Journals that ever wrote another entry after their final falsifier | **10 of 103** | MEASURED |

The doctrine says *journal before going idle*, and *a reconciliation names its falsifier*. The
combined effect is that **the final act of nearly every agent is to name a falsifier and then cease
to exist.** The falsifier is not ignored. It is **orphaned by the shape of the ritual itself** — there
is no "next course" in which a course-change could have been recorded.

**An instrument cannot detect a course-change that had no subsequent course.** For 93 of 103 journals
the state `falsifier-not-honored` is not FALSE — it is **UNDEFINED**.

### NULL RESULTS (named, as required)

1. **NULL: zero instances of the pathology.** 114 class-(a) statements, full forward-hunt by four
   independent readers, **FIRED-IGNORED = 0**. No reader manufactured one. (MEASURED)
2. **NULL: zero unfalsifiable-as-written falsifiers.** Class (c) = **0 of 135** statements. The
   predicted "ritual mush" (*"if this turns out wrong"*) **does not exist in this corpus**. (MEASURED)
3. **NULL: the pathology has no structural hiding place.** I hunted the only 4 journals that named a
   falsifier, kept writing, and never returned to it. **All four were exonerated on reading** — they
   had honored the falsifier in prose my regex could not see. (VERIFIED)
4. **NULL: the sub-hypothesis "journals name falsifiers ritually" is REFUTED.** The falsifiers are
   *well-formed and file-checkable*. The failure is not in their **form**; it is in the **absence of a
   later reader**. (MEASURED + REASONED)

---

## 1. Class counts — the core number

Method: four independent readers (fp-slice-a/b/c + me) applied one shared rubric
(`docs/audit/_falsifier-rubric.md`), written **before** any reading, so the counts are commensurable.
Full per-statement tables with verbatim quotes and real file:line live in
`docs/audit/_fp-slice-{a,b,c}.md`. **I spot-checked quoted line numbers against the raw journals for
fabrication; every one checked was real and verbatim** (VERIFIED — see §5).

### Rubric refinement I added (not in the brief)

I split class (a) into two, because I judged this was where the question would actually be decided:

- **(a)-independent** — the disconfirming observation has a witness the agent **does not author**:
  an mtime, a queue file, a test exit code, a git artifact, a record in `.swarm/agents/`.
- **(a)-self-report** — the observation is real, but the **only possible witness is the agent's own
  later prose about it**. If the agent stops narrating, the falsifier is unverifiable by anyone.

This distinction turned out to matter enormously (§4).

### Totals across the 10 richest journals (MEASURED)

| | field-tester | hardener | updater | v3-run-ds | v3-run-glm | fleet-eval | dp-f1 | dp-f2 | oc-plugin-scout | op-struct-scout | **TOTAL** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MENTIONS (not statements) | 12 | 2 | 0 | 10 | 8 | 8 | 8 | 8 | — | — | **~56** |
| **STATEMENTS** | 35 | 19 | 18 | 9 | 12 | 14 | 4 | 5 | 10 | 9 | **135** |
| **(a)-independent** | 32 | 18 | 0 | 8 | 9 | 13 | 4 | 3 | 10 | 8 | **105** |
| **(a)-self-report** | 1 | 1 | 0 | 1 | 3 | 1 | 0 | 2 | 0 | 0 | **9** |
| **(b) OBSERVABLE-ELSEWHERE** | 2 | 0 | **18** | 0 | 0 | 0 | 0 | 0 | 0 | 1 | **21** |
| **(c) UNFALSIFIABLE-AS-WRITTEN** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

### Outcomes, class (a) only — the forward-hunt (n=114) (MEASURED)

| outcome | count |
|---|---|
| **FIRED-CHANGED** (healthy: fired, agent changed course) | **17** |
| **FIRED-IGNORED** (**the pathology**) | **0** |
| **NOT-FIRED** (affirmatively shown not to have fired) | **84** |
| **CANNOT-TELL** (journal never returns to it) | **13** |

**The headline: FIRED-IGNORED = 0 of 114.** (MEASURED, by four readers who each hunted for it
independently and each declined to invent one.)

**Arithmetic check (MEASURED):** the class counts sum to the statement total (105 + 9 + 21 + 0 = 135),
and the outcome counts sum to the class-(a) total (17 + 0 + 84 + 13 = 114 = 105 + 9). The two
independent tallies reconcile exactly.

---

## 2. The healthy case is vivid and real — VERIFIED

The pathology's absence is not because falsifiers are toothless. When they fire, they **bite**, and
they bite their own author. Three I read in full:

**`opencode-plugin-scout.md:429` → `:435`** — the best specimen in the corpus. (VERIFIED)
> :429 — *"FALSIFIER for option (c): if messages.transform's injected message does NOT persist into
> the session's stored history … then a message delivered on turn N is INVISIBLE on turn N+1 — the
> agent would 'forget' its mail. My run cannot distinguish these. THIS MUST BE TESTED."*
>
> :435 — *"**MY OWN FALSIFIER FIRED.** `messages.transform` is a VIEW transform, not a session write.
> Option (c) is DEAD as stated."* … :447 *"MODEL ANSWERS: **UNKNOWN**."* … :460 *"**DELIVERY CANNOT
> RIDE messages.transform.**"*

The agent named the falsifier, built a sandbox to fire it, it fired, and it **killed the agent's own
preferred design**. Independent witness: a reproducible experiment, not narration.

**`run-claude-base-2.md:41` → `:47-48`** (VERIFIED)
> :41 — *"**Falsifier: I am off track if a child's swarm state (journal/tombstone/queue) lands in the
> LIVE `/Users/vadrsa/git/swarm/.swarm/` instead of the sandbox**"*
> :47 — *"RECONCILE: falsifier fired (journal leak to live), rig fixed"* — witnessed by the leaked
> file's **mtime**, root-caused to a relative-path bug, rig repaired.

**`operator-structure-scout.md:451`** — NOT-FIRED, but *earned* against real records. (VERIFIED)
> *"MY OWN FALSIFIER DID NOT FIRE."* — ran it against **all 60 messages** in
> `queue/operator/delivered/`, resolving each sender's depth from `agents/*.json`: `depth 1: 60,
> depth >=2: 0`.

**REASONED:** every clearly-decidable firing in this corpus resolved into a course change. The
discipline, where it is observable at all, is **working**.

---

## 3. Why the pathology cannot be found — the orphaning mechanism

This is the real finding, and I did not expect it.

**MEASURED** (corpus = 109 journals, this audit's own subtree excluded; 103 name a falsifier):

- **93 of 103** journals have their **last falsifier inside their last entry**.
- **10 of 103** ever wrote another entry after their final falsifier.
- **0 of 103** had only a single entry (i.e. this is not an artifact of short journals).

**Note on two numbers, so the record is not confusing:** an earlier pass of mine (quoted in my journal
and by my parent) reported this as **84 of 88**. That count was taken over a corpus that still included
this audit's own subtree and used a narrower falsifier regex. **93 of 103 is the corrected figure**,
recomputed on the clean 109-journal corpus with the audit subtree excluded. The ratio is unchanged
(95% vs 90%) and the finding is unchanged; I am reporting the correction rather than letting two
numbers for one fact circulate.

The doctrine composes two duties — *journal before going idle* and *a reconciliation names its
falsifier* — into an emergent trap: **the falsifier is the last thing the agent writes before it
stops existing.** Nobody is left to check it.

**REASONED:** `falsifier-not-honored` is a claim about what an agent did *after* the disconfirming
observation. For 93/103 journals there **is no after**. The state is not false; it is **undefined**.
An absence of course-change is **indistinguishable** from the falsifier having quietly never fired.
Both look like silence, and silence is what the corpus overwhelmingly contains.

The decidable population — journals that wrote past their final falsifier — is exactly **10**:
`deleg-heavy-after-1, grave-notlist, hook-drafter, opencode-plugin-scout, operator-structure-scout,
operator, org-review-scout, patterns-contractor, pipeline-scout, proxy-scout`. (MEASURED)
**Even inside it, I found zero pathology.** (VERIFIED — §5)

---

## 4. The two shapes where detection genuinely fails

These are the honest edges — where an instrument would be blind *even if the pathology existed*.

### (b) OBSERVABLE-ELSEWHERE — witnesses that evaporate. `updater.md` is 18-for-18.

The single most concentrated failure of detectability in the corpus. **All 18** of `updater.md`'s
falsifier statements are class (b), **zero** class (a). (MEASURED, fp-slice-a)

> `updater.md:11-12` (VERIFIED): *"Falsifier: if `git -C ~/.local/share/swarm rev-parse origin/main`
> on GitHub's main differs from eac88e2 **right now**, my 'up to date' verdict is wrong."*
> `updater.md:15-16` (VERIFIED): *"Falsifier: **watcher output file** shows the loop died without
> origin/main having moved."*

The witnesses are a **live git remote** and a **background-task output buffer**. Both are *real* and
*checkable in principle* — and both have since **moved or evaporated**. A later reader opening only
the repo can never adjudicate them. This is not a badly-written falsifier; it is a **well-written
falsifier pointed at a witness the files do not preserve.**

### (a)-self-report — the agent is the only witness. n=9.

Where the only possible record of the firing is the agent's own future prose, an agent that stops
narrating is **structurally unauditable**. fp-slice-c found both of `dp-f2`'s self-report cases were
**delegation falsifiers** (*"if run 1 shows the per-run work is mostly mechanical collection, I spawn
a collector"* — `dp-f2.md:106`, VERIFIED). Whether the work "was mechanical" is a **judgment that
exists only in the agent's head**. It honored them — but only its own say-so records that.

**REASONED:** these 30 statements (21 class-(b) + 9 self-report, = 22% of 135) are the population
where a bad actor *could* hide, and where an instrument is blind by construction.

#### The delegation falsifier, and the one rule that makes it auditable (VERIFIED)

The corpus contains a natural experiment, with a treatment and a control:

- **`dp-f2.md:106` and `:184`** — *"if run 1 shows the per-run work is mostly mechanical collection, I
  spawn a collector for run 2"* / *"if run 2 needs no judgment calls, I was wrong and should have
  parallelized."* Whether the work "was mechanical" or "needed judgment" is a **verdict that exists
  only in the agent's own head**. No mtime, no queue file, no artifact can settle it. **a-self-report
  — unauditable.** (The agent did honor them; only its own say-so records that.)
- **`operator-structure-scout.md:269`** — *"FALSIFIER of this reconcile: if red2 returns a KILL on the
  structural fix, the tree…"* — **also a delegation falsifier**, but the agent **handed the verdict to
  somebody else**: a fresh red team whose artifact (`OPERATOR-STRUCTURE-RED2.md`) is **in the repo**.
  It **FIRED** (red2's A2 KILL), and the agent changed the tree. **a-independent — fully auditable.**

**The rule the data supports (REASONED): a delegation falsifier is only auditable if its judge is
somebody else.** When an agent appoints *itself* judge of whether it should have delegated, the
falsifier is unfalsifiable in practice no matter how well it is worded — because the witness is a
private judgment. When it appoints an *external* judge who writes a file, the same falsifier becomes
checkable by anyone. This is the (a)/(b) boundary restated as a *design property of the falsifier's
judge*, not of its prose.

### The counter-mechanism (why the honest ones stay honest) — slice-b's discovery

fp-slice-b found **CANNOT-TELL = 0** across its whole family and explained why (REASONED, and I
concur): these agents are in a **measure-then-score loop where the falsifier's witness is the same
artifact they are about to score.** *Checking the falsifier and doing the job are the same act.* The
falsifier **cannot** be ignored without the work simply not happening.

This is the deep result: **falsifiers are honored where honoring them is inseparable from the work,
and unauditable where it is separable.** The discipline is not being enforced by virtue — it is being
enforced by *the falsifier and the deliverable having the same witness*.

---

## 5. My own falsifier FIRED — recorded, because this artifact lives by its own standard

I pre-registered (journal, 17:31Z): *"my 18-vs-106 number rests on a REGEX for discharge language. If
a journal honors a falsifier in prose using none of those words, my regex scores it as 'never returns'
when the agent actually DID honor it."*

**IT FIRED.** (VERIFIED) I chased the 4 journals my regex flagged as *named-a-falsifier-then-kept-
writing-and-never-returned* — the only structural hiding place for the pathology. **All 4 were
exonerated on reading**, and two refute the regex directly:

- `hook-drafter.md:124` — *"Falsifier of the rewrite (from last entry): 'any section assuming the
  engine persists between messages.' **Checked — none**; every section treats the hook as a cold
  per-invocation binary. On track."* — a textbook discharge, invisible to a regex hunting for
  "discharged/fired".
- `pipeline-scout.md:64` — names the falsifier and discharges it **in the same breath**: *"…but I
  greped both to zero."*

**Consequence, stated honestly: any regex-derived "never honored" count is a LOWER BOUND on honoring
and makes the corpus look worse than it is.** All headline counts in this document come from
**full-text reads**, not the regex. The regex was a probe, not a measurement.

**Note the direction of the correction: it makes the pathology LESS findable, not more.** Every case
flagged as a possible ignore turned out, on reading, to be an agent quietly doing the right thing.

### MY NAMED BLIND SPOT — kept in deliberately (VERIFIED, and unresolved)

My candidate-hunt for the pathology (§ NULL 3) selected journals **that had no back-reference
language at all**. That method is, by construction, **blind to the case where an agent DOES use the
vocabulary but ignores the substance** — an agent that writes "falsifier fired" and then carries on
regardless would never be nominated as a candidate by my selection rule. I named this blind spot in my
journal *before* seeing any child's answer, precisely so it could not be quietly dropped.

**It is only partially closed.** What closes it, as far as it goes: the four slice readers did **full-
text forward-hunts** — not regex, not candidate selection — over all 114 class-(a) statements, and
they would have seen exactly this case. They found zero. What does *not* close it: those reads covered
the **10 richest journals**, not all 103. In the other 93 the blind spot stands.

**I am reporting this as an open weakness, not a resolved one.** It is the second reason (after the
orphaning) that my "zero" must not be read as "there is none."

### One more shape I did not have a class for (VERIFIED)

`operator-structure-scout.md:374` — *"FALSIFIER of this lean: if `swarm ps`/`send` already work
outside herdr and only `spawn` is gated, then the gate is defensible … and the answer really is
DOCTRINE-ONLY, tool untouched."* This falsifier is written so that **firing confirms the agent's
lean** — whichever branch obtains, the design survives. It was measured honestly against the live tool
(the evidence is sound), but the **form** is a decision procedure wearing a falsifier's clothes. Named
as a shape, not as misconduct. An instrument that merely counted well-formed falsifiers would score
this one **perfect**.

### And the limit of the whole doctrine (VERIFIED)

`operator-structure-scout` wrote **8** well-formed, file-observable falsifiers. **None fired** — and
its central artifact was **retracted anyway** (`:328`: *"MAJOR REFRAME from the operator. My
structural fix is RETRACTED"*), because the **operator changed the premise underneath it**.

**REASONED — and this is the sharpest thing in the corpus:** *falsifiers guard the mechanics you chose
to test; they do not guard the frame.* An agent can honor every falsifier it names, perfectly, and
still be building the wrong thing. No journal-scanning instrument can see that.

### Fabrication check on my children (VERIFIED)

I spot-checked child-quoted file:line against raw journals — `dp-f1.md:110`, `dp-f1.md:124-126`,
`dp-f2.md:213`, `opencode-plugin-scout.md:362-366`, `updater.md:11-12`, `hardener.md:24`. **Every one
is real and verbatim. No fabrication found.** My own blind pre-classification of 8 statements (made
before any child reported) **agreed with the children's independent calls**, so the shared rubric held
and the sums across four readers are legitimate.

---

## 6. Doctrine compliance (brief item 4)

**Caveat, stated plainly: this section is weaker than the rest.** My child `fp-compliance` fanned out a
shard subtree over all 109 journals and **died before writing its synthesis** — `_fp-compliance.md`
does not exist. Rather than claim its numbers, I recomputed the load-bearing ones myself. **What I
could not personally recompute, I do not report.** (This is itself an honest negative: part of the
commissioned measurement was not delivered.)

**MEASURED, by me, on the clean corpus (109 journals, audit subtree excluded):**

| measure | count |
|---|---|
| journals in corpus | 109 |
| journals naming a falsifier | **103** (94%) |
| journals containing "reconcil" | 55 |
| journals with **both** | 54 |
| journals naming a falsifier but **never** writing a reconciliation | **51** |
| journals reconciling **without** ever naming a falsifier | **1** |
| falsifier statements corpus-wide (regex **lower bound**) | **408** |

**Ritual compliance is very high — 94% of journals name a falsifier — and *form* compliance is
perfect (0 class-(c) in 135 hand-read statements).** The doctrine is being followed.

**But the doctrine's *purpose* — that a named falsifier later gets checked — is met in only ~10% of
journals**, and only because the other 90% stop writing at the moment of naming. (MEASURED + REASONED)

---

## 7. Verdict on the instrument

**An instrument that scans journals for `falsifier-not-honored` would find nothing, and its silence
would be uninformative.** (REASONED, from the measurements above)

- It would return **zero** on this corpus. That zero is **true** — the pathology is genuinely absent
  from 114 hand-read class-(a) statements.
- But it would *also* return zero on a corpus **riddled** with the pathology, because in 93 of 103
  journals the agent stops writing at the moment of naming, and **an ignored falsifier and a never-
  fired falsifier produce byte-identical silence.**

A detector whose zero means both *"healthy"* and *"undetectable"* **is not an instrument.** Its output
carries no information about the thing it purports to measure.

**The honest statement of the finding, in the brief's own words:** the journals do **not** "name
falsifiers ritually" — the falsifiers are unusually well-formed, overwhelmingly file-checkable, and
demonstrably honored when they fire. **But the firing event is almost never written down, because the
naming is the agent's last act — so this pathology is NOT machine-detectable, and barely human-
detectable, in the 90% of the corpus where the agent's existence ends at the moment of naming.**

I found **no** pathology. I am **not** confident there is none. Those are different claims, and the
gap between them is exactly the 93 journals that stopped writing.

---

## Provenance

- Shared rubric (written before any reading): `docs/audit/_falsifier-rubric.md`
- Per-statement tables, verbatim quotes, real file:line: `docs/audit/_fp-slice-{a,b,c}.md`
- My working journal, including my own fired falsifier: `.swarm/journal/falsifier-probe.md`
- Children: `fp-slice-a` (field-tester, hardener, updater), `fp-slice-b` (v3-run-ds, v3-run-glm,
  fleet-eval), `fp-slice-c` (dp-f1, dp-f2, opencode-plugin-scout, operator-structure-scout),
  `fp-compliance` (**failed to deliver its synthesis — noted, not concealed**).
- **I designed nothing and recommended nothing.** Per brief.
