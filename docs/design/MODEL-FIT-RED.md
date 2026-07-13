# MODEL-FIT-RED — adversarial review of `docs/design/MODEL-FIT.md`

**Author:** `fit-red`, fresh adversarial reviewer, reporting to `model-fit`.
**Target:** `docs/design/MODEL-FIT.md` at `main@aa6063d` (as committed on
`swarm-dev/model-fit`). **Method:** read the doc, read every cited artifact at
the cited lines, read the sibling's raw journal (`.swarm/journal/weak-model-deleg.md`),
checked the wiring (`skill/SKILL.md`, `bin/swarm` USAGE and `cmd_ps`).

**Verdict up front: WOUNDED, not KILLED.** One finding is a genuine citation
defect that the doc must fix (KILL-tier, but locally fixable — it does not
bring down the ladder). The rest of the architecture — the three-rung ladder,
the seat/leaf distinction, the "inherit" default — survives the attack. Where I
could not kill it, I say exactly what survived and why, per the brief.

---

## Ranked findings

### 1. [KILL — but narrow] The "scored from transcripts, not absence-of-file" claim misrepresents its own citations

**§2, lines 118-122:** *"the eval scored from transcripts and session logs
(`FLEET-EVAL-V3.md:64-65`, `:136`, `:244`), and the non-Claude cells ran headless
under `opencode run --auto` (`FLEET-EVAL.md:108`) — auto-approve, so there was no
dialog to block on. The citation survives."*

I checked all three internal cites. **None of them supports the claim they are
stacked to support.**

- `FLEET-EVAL-V3.md:64-65` — *"queued to the model-agent's name and injected
  into its later turns (witnessed by the TRANSCRIPTS...)"*. This is a narrow
  statement about **one D2 sub-check**: whether deepseek's children's reports
  were actually delivered/injected. It says nothing about how D1/D3/D4
  *failures* — the 8/10, 11/17, 3/6 FAIL numbers the doc leans its whole
  argument on — were scored.
- `FLEET-EVAL-V3.md:136` — *"the Claude control had the same doors open and
  took them 0 times in 7 probes (verified by the reviewer from session logs:
  ... 0 `mcp__` calls...)"*. This is the **MCP-substitution control** — a count
  of tool calls in the Claude anchor's sessions. It is not a statement about
  how the *weak-model* failure rows were scored.
- `FLEET-EVAL-V3.md:244` — restates the same MCP control in the review's
  "cleared under hostile reading" list. Same scope, same non-applicability.

The actual methodology statement in the doc (`FLEET-EVAL-V3.md:14-15`) says
scores came from "results files" opened by a runner and "spot-checked against
sandboxes" — closer to file-based scoring than transcript-based. And line 110
(*"everything scored from files"*) is a **local aside about GLM's word-count
tic**, not a global methodology claim either — but note its plain content cuts
**against** MODEL-FIT's claim, not for it.

Worse: line **159-161**, which sits in the same cluster the doc is citing
around (`:136`, `:244` bracket it), is about the **opposite** failure — the
Claude anchor's *pane-less registered runner* reading as `dead` in `swarm ps`,
causing **native probes to be misjudged as failed when they weren't** ("four
native probes sent correct reports and then despaired incorrectly — scored
from files"). That passage is evidence *for* the very risk MODEL-FIT is trying
to rule out (absence-of-file misread as failure) happening **in this exact
eval**, on the Claude cell. MODEL-FIT never mentions that this happened to the
*Claude* anchor too, only that the confound "could have" affected
deepseek/GLM and didn't. It did not check whether it affected the row it now
calls clean.

**Why this matters, concretely:** the whole rhetorical move at lines 113-122 is
"I checked this confound rather than assumed it" — offered as the load-bearing
proof that §2's deepseek/GLM numbers are trustworthy evidence for the axis
Rung 3 is built on. The proof does not hold up against its own citations. I
went and read them; they say something narrower and in one case something
adjacent-but-different from what's claimed.

**What survives:** the *outcome* — deepseek/GLM's D1/D3/D4 failures probably
were scored from real artifacts, because `run-cell.sh` ran headless under
`opencode run --auto` (`FLEET-EVAL.md:108`, verified — this cite is accurate,
I read it) so there's no permission-dialog mechanism available in that harness
to produce a false "block" reading in the first place. **That's the actual
argument that should be made** — the harness structurally can't hit the
permission-block confound, full stop, because auto-approve means there is no
dialog — and it's a good one. But it's not the argument the doc makes. The doc
reaches for three internal V3 cites that don't say what it needs and skips the
one clean argument (`FLEET-EVAL.md:108`, headless auto-approve) that would
have actually settled it without needing the transcript claim at all.

**What the doc must do:** rewrite lines 118-122. Drop `:64-65`, `:136`, `:244`
as support for "scored from transcripts" — they don't carry that weight. Lean
on `FLEET-EVAL.md:108` alone (headless, auto-approve, structurally no dialog
possible) and, if the transcript point is still wanted, cite `:14-15`
("results files... spot-checked against sandboxes") accurately, with the
weaker claim it actually supports. Also disclose that the same eval **did**
misjudge a live cell as dead (`:159-161`, the Claude anchor) — because that's
exactly the class of error the doc is claiming didn't happen here, and burying
the one instance where it *did* happen (even though it hit the "wrong" cell
for the doc's purposes) is the kind of selective citation the document
explicitly says it's trying not to do (§2's whole stated ethic is "I checked
this rather than assumed it").

**Severity: KILL** on the specific paragraph — it must be rewritten, the
citation chain is broken. **Does not KILL the document** — a correct version
of the same argument is available and is stronger anyway, so §2's actual
position (Rung 3 rests on a directional extension, disclosed as such) is
unaffected once the paragraph is fixed.

---

### 2. [WOUND] §4's over-delegation acquittal quietly drops the sibling's second-strongest negative finding

MODEL-FIT §4 (lines 218-276) accurately reports the headline (zero descendants,
temporal argument, honest scope-down to "no spawn reflex during
ingestion/setup"). It even fixes the reviewer's rescoped-headline requirement
correctly.

But `weak-model-deleg`'s own report has a **second, co-equal finding** that
`wmd-red` forced onto the same footing as the delegation count:

> *"Protocol adherence is a co-equal NEGATIVE, not a caveat... Across ~16+ min
> of life over two runs, Haiku: never completed a journal write, never used
> `swarm send`, never produced a byte of artifact... That is the FLEET-EVAL-V3
> 'passes leaf duties, drops the protocol' shape model-fit explicitly warned
> me to watch for — and I buried it."* (journal, 01:00Z, item 3)

MODEL-FIT's own §7 falsifier section **does** mention this ("Status: live...
both were blocked on a permission dialog at the very call that would have
written one, so this is not yet a clean protocol-drop observation") — so credit
where due, it isn't fully buried. But it is filed as a *falsifier watch-item*
in §7, one bullet among four, rather than surfaced in §4 where the
over-delegation acquittal is made. A reader who reads §4 alone (the section
that actually makes the "Rung 3 stands" ruling) gets the clean acquittal; the
co-equal negative that the sibling itself insisted on promoting to equal
footing with the delegation count is one section away and easy to miss. Given
that MODEL-FIT explicitly asks the reader to trust its self-correction ethic
("the honest limits, which I will not bury"), putting the *second* co-equal
finding in a different section than the first, rather than beside it, under-
weights it relative to how the source material weighted it.

**What the doc must do:** in §4, next to the delegation acquittal, add one
sentence: *"the same two runs also showed zero completed journal writes and
zero `swarm send` uses — confounded by the same permission block, and it is
the FLEET-EVAL-V3 leaf-duty-drop shape repeating on a third model family. Not
yet attributable to Haiku specifically, but it is not nothing, and it belongs
next to the delegation finding it was promoted to sit beside."* This is a
one-sentence fix, not a redesign.

**Severity: WOUND.** Doesn't invalidate the ruling, does understate a finding
the source material treats as load-bearing.

---

### 3. [WOUND] Rung 3's "verify in seconds" claim is true for presence-errors, false for omission-errors, and the doc never says so

This is the sharpest conceptual attack in my brief, so I pushed on it hard:
does "mechanically checkable... verify it in seconds" (§1, rung 3; restated
§4 rung 3, §6) actually hold?

**It does not hold uniformly, and the doc's own text half-admits this without
naming it.** A census that says "there are 40 call sites" when there are 43 is
not caught by a parent spot-checking the 40 listed items — every one of them
is real, so every spot-check the parent runs passes. The 3 missing ones are
invisible to inspection of what *is* there; they're only findable by an
independent count, which is exactly the "redo the work" cost Rung 2 is built
to avoid paying. This is a structurally different failure mode from a wrong
grep result (which spot-checking one row does catch) — **omission errors on
Rung-3 work are not "cheap to catch," they're free of any signal that catching
is needed.**

The doc gestures near this without landing it. §6 says "an annoyance with a
known, bounded price, visible on a bill" for the *expensive-wrong* direction,
and separately the whole §7 caveat block is about **observable-lies** (a
blocked child looking like a stalled one) — but that caveat is about
*liveness* observables, not about *completeness* of a delivered artifact. The
doc never states, anywhere, that a Rung-3 count/inventory/sweep can be
**wrong by omission and pass every spot-check a parent will actually run.**
That is a real gap given how much weight Rung 3 puts on "verify in seconds."

**Why it doesn't KILL Rung 3:** the ladder's actual safety argument isn't "the
parent will always catch it" — it's "a leaf's mistake lands somewhere safe: a
strong parent reading the artifact" (§4, "What survives"). For most Rung-3 use
(build a census to decide what to look at next, not to certify a security
property), a 3-of-43 miss is low-consequence: the parent's next action is
informed by a slightly-incomplete list, not a load-bearing certification. The
risk is real specifically when a Rung-3 artifact is being used for a
**completeness-load-bearing** decision — e.g., "we grepped every `--model`
call site, so we know the blast radius is 9 files" (§5, exactly this move is
made in the doc itself, sourced from a census). If that census under-counts,
the "measured blast radius" claim silently inherits the omission error, and
nobody would know to re-check it, because the parent trusts a Rung-3 number by
design.

**What the doc must do:** add one paragraph to §4/Rung 3 naming the
omission-vs-commission asymmetry explicitly: spot-checking catches wrong
entries, not missing ones; a Rung-3 artifact used to certify **completeness**
(blast radius, "every call site," "all N agents") deserves either a second
independent count or an explicit caveat that the number is a floor, not a
verified total. This is the same discipline §7 already applies to liveness
observables ("no artifact is evidence of nothing until you look") — the doc
should apply the identical skepticism to its own census outputs, and currently
doesn't.

**Severity: WOUND.** A real, load-bearing gap in the "cheap to verify" claim,
but scoped: it attacks completeness-claims specifically, not general Rung-3
use, and the ladder's actual justification (bounded blast radius at the leaf)
survives for the common case.

---

### 4. [SCRATCH, on reflection] The "inherit" default — I tried to kill it and it held

I went in planning to argue this was the doc choosing the elegant answer over
the effective one: 142/143 inherited, doctrine-only fixes have a bad track
record, and a default is the one lever that touches all 143 without anyone
reading anything.

**The counter-argument in §5b actually survives contact.** The reason it holds:
the "doctrine has a bad track record" argument proves too much if taken
consistently. This document's *own* evidence base (§5, the falsifier-audit:
0/135 unfalsifiable, 17/114 fired-and-changed-behavior) is a **direct,
measured rebuttal** to "doctrine that asks a parent to think doesn't work here."
This repo has one clean natural experiment on "does a compelled field in the
frame change behavior" and it came back strongly positive. If doctrine-only
compulsion is shown (elsewhere, in this same repo, with a pre-registered
audit) to move behavior in 17/114 cases and mislead in 0/135, then the
"doctrine alone won't work, only a default will" objection needs its own
evidence, and none is offered against it — it's argued from a general prior
("doctrine has a bad track record") that this repo's own audit already
contradicts for the *adjacent* mechanism (falsifier compulsion). The
asymmetry argument (§5b.3 — inherit fails by overpaying, Sonnet-default fails
by silently underpowering a seat) is also just correct on its face: a default
cannot distinguish a coordinator spawn from a leaf spawn, so *any* fixed
non-Opus default necessarily mis-sizes some seats, and seats are exactly the
place the doc argues (correctly, per Rung 1's blast-radius logic) you must not
economize.

The one place I can still push: the "142/143" fact is about the **whole
population of past spawns**, most of which were probably leaves (the doc
itself says "scouts, red-teamers, hardeners, census-counters" — a mix of seats
and leaves). If the *leaf* subpopulation is large, a leaf-only default change
(not proposed here, but a real fourth option nobody considered) could have
captured most of the savings without touching seat safety at all. The doc
doesn't consider "default to Sonnet only when we structurally know it's a
leaf" because the CLI has no way to know that at spawn time — but that's a
tooling gap, not a proof the idea is bad. This is a real gap in the option
space considered, not a flaw in the reasoning about the two options actually
compared.

**Severity: SCRATCH.** The comparison the doc makes (inherit vs. flip-to-Sonnet)
is argued correctly and I could not break it. There's an uncompared third
option (leaf-typed default) worth a footnote, but it doesn't unseat the ruling
as stated.

---

### 5. [SCRATCH] The thing I went looking for and did not find

Per the brief's ask for "the one I haven't thought of" — I looked specifically
for: internal contradictions between rungs, a hidden assumption in the
"confidently wrong costs more" argument, and whether the mandate ruling (§5)
and the default ruling (§5b) are consistent with each other. They are: §5
ships nothing enforced (doctrine + a reader fix only), §5b keeps a default that
requires the same doctrine to work, and both point to the same falsifier-audit
evidence for why unenforced doctrine can still move behavior. I could not find
a load-bearing contradiction between the two rulings. The closest near-miss:
§5 argues a *mandated reason field* would manufacture confident-wrong
justifications ("why is Haiku right for this" — nobody knows), while the doc
itself, in §2, writes several confident-sounding directional claims about
Haiku's suitability that read exactly like the fabrication §5 warns against
avoiding. That's not a contradiction so much as the document occasionally
doing, in prose, the thing it says a mandated field would force parents to do
badly. I considered promoting this to a WOUND but decided it's really a
restatement of finding #1 and #3 (the places where confident directional
claims outrun their citations) rather than a new independent defect.

---

## Summary table

| # | Finding | Severity | Fixable in-doc? |
|---|---|---|---|
| 1 | `:64-65`/`:136`/`:244` don't support "scored from transcripts"; the real argument (`FLEET-EVAL.md:108`, headless auto-approve) is available but uncited for this purpose; the eval's one real absence-of-file misjudgment (`:159-161`) hit the Claude cell and isn't disclosed | **KILL** (of the paragraph) | Yes — one paragraph rewrite |
| 2 | Protocol-drop co-finding from `weak-model-deleg` is in §7 but not surfaced beside the §4 acquittal it was promoted to sit next to | **WOUND** | Yes — one sentence |
| 3 | "Verify in seconds" is true for wrong-entry errors, false for omission errors; the doc never names the asymmetry, and it's load-bearing for its own §5 blast-radius claim | **WOUND** | Yes — one paragraph |
| 4 | Inherit-vs-Sonnet-default argument attacked directly; held. Leaf-typed default is an uncompared third option, not a refutation | **SCRATCH** | Optional footnote |
| 5 | No independent structural contradiction found beyond restating #1/#3 | **SCRATCH** | N/A |

## What I could not break

The seat/leaf split (Rung 1 vs Rungs 2-3) and its blast-radius argument is
sound and I found no attack on it. The "confidently wrong costs more than
tokens" framing (§6) is correctly the load-bearing spine, not decoration —
it's what makes Rung 2's Opus-for-judgment default correct even before any
Haiku-specific evidence exists, since it only needs "verifying costs what
making it cost," which is true by definition of what a judgment task is, not
an empirical claim about any specific model. The wiring (`skill/SKILL.md:46-62`,
`bin/swarm:1105-1109`) is genuinely actionable at spawn time — it states the
question ("can I cheaply tell this child was wrong?"), gives the two poles,
and points at the doc; I don't find a paragraph nobody could apply. And
`swarm ps`'s line format (`bin/swarm:539-548`) does confirm the doc's own claim
that it doesn't render `model` — that citation is accurate, unlike finding #1.
