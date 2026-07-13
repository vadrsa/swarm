# ORG-REVIEW PRIOR ART — the living-prior-art prosecution

**Author:** `grave-priorart`, child of `grave-org`. Written at `main@aa6063d`, 2026-07-12.
**Method:** read every named file top to bottom (no skimming), `git log --oneline --all` on each,
and grep the *shipped surfaces* (`bin/swarm`, `skill/SKILL.md`, `WORLD.md`, `README.md`,
`install.sh`, `.claude/`) for any reference to any of them.

**Evidence discipline:** **VERIFIED** = I read the line and quote it. **MEASURED** = a count I ran.
**REASONED** = argument, falsifier named.

**Subject under prosecution:** an INSTRUMENT that reviews the swarm's TOP-LEVEL structure (the
shape of the tree directly under the human) and SUGGESTS improvements to the human — advisory
only, an explicitly-invoked named skill/command, plus a rare evidence-warranted OFFER from a
coordinator.

---

## THE HEADLINE, BEFORE ANY DETAIL

**Three findings, and the second is the one that hurts:**

1. **SELF-AUDIT.md / REVIEW.md / WATCHLIST.md are NOT prior art for this proposal.** Their names
   mislead. All three are about the **tool's own design** (the SIMPLEST rewrite), not about the
   **operator's top layer**. Two are DEAD LETTERS (never referenced from any shipped surface,
   never touched since the cutover commit); one (WATCHLIST) is a live *design ledger* that is
   still only ever cited by other design docs. **No shipped surface references any of them.**
   (MEASURED — grep below.)

2. **★ THE OPERATOR HAS NEVER, ONCE, RECEIVED A TOP-LAYER STRUCTURE REVIEW FROM ANY SHIPPED
   MECHANISM.** The closest shipped thing — **the review desk** (`skill/SKILL.md:47-49`) — is a
   **ranked *decisions* page**, not a structure review. It hands the human *what to decide*, never
   *how their top layer is shaped or how to reshape it*. The instrument the operator is
   considering **does not exist today and never has.** (VERIFIED + MEASURED, §c.)

3. **★ BUT: `OPERATOR-STRUCTURE-GRAVE.md` — written TODAY, by a sibling agent, in the same
   graveyard-audit shape as this one — already ruled on a *doctrine* that touches the same
   subject, and its rulings are LOADED GUNS pointed at this instrument.** It does **NOT** kill a
   structure-review *instrument* (nobody has ever proposed one — **NULL RESULT**), but it kills
   three of the four things an instrument like this would naturally be built out of. The full
   quotes are in §d, and I do not soften them.

**And one structural fact that changes how to read all of it:** **every OPERATOR-STRUCTURE\*.md
file is UNTRACKED.** They have zero git history. They were written today, by today's swarm, and
have never been committed, never reviewed by the human, never shipped.

```
$ git log --oneline --all -- docs/design/OPERATOR-STRUCTURE.md          # (and RED, RED2, RED3, FIX, GRAVE)
(empty)
$ git ls-files --error-unmatch docs/design/OPERATOR-STRUCTURE-GRAVE.md
error: pathspec ... did not match any file(s) known to git    → UNTRACKED
```
(MEASURED, all six files.) **They are the freshest thinking in the repo and the least ratified.**

---

## (a) WHAT IS EACH OF SELF-AUDIT.md / REVIEW.md / WATCHLIST.md — in its own words

### SELF-AUDIT.md — **a compliance audit of a code rewrite. Not an org instrument. Not a mechanism.**

Its own first line, VERIFIED (`docs/design/SELF-AUDIT.md:1-5`):

> `# SELF-AUDIT — simplest/swarm vs the SIMPLEST spec`
>
> *"Written against the post-review amended file (rulings R1–R6 applied; see "Post-review
> amendments" below). Line numbers are from `simplest/swarm` at this commit. Tests: 40/40 pass
> (`python3 -m unittest test_swarm`)."*

Its body is a table titled *"Every §2 concept → where it lives"* (`:7`) mapping WORLD concepts to
`swarm:NNN` line numbers, plus *"Every §4 deleted concept → grep proving absence"* (`:27`) with
literal grep hit-counts, plus a **deviations** list whose contract is *"all reported, none
silent"* (`:59`).

**What it IS:** a **one-shot artifact** — an implementer's self-report that the code it wrote
matches the spec it was given. **A document about `bin/swarm`, written once, in 2026-07-09.**
It is not an instrument, not a mechanism, not a role, not a recurring anything.

### REVIEW.md — **a one-shot adversarial code review of that same rewrite. Also not an org instrument.**

VERIFIED (`docs/design/REVIEW.md:1-11`):

> `# REVIEW — simplest/swarm vs docs/design/SIMPLEST.md`
>
> *"**Reviewer:** `review-simplest` (no stake in design or implementation). **Method:** execute,
> never infer — I ran the shipped suite (31/31 pass, reproduced), then wrote and ran 22 tests of
> my own at process level…"*
>
> *"## Verdict — **PASS** — all 9 concepts exist and behave per §2/§3 under execution…"*

**What it IS:** the **verdict document of a dead agent** (`review-simplest`), reviewing code, once.
It carries an ADDENDUM dated 2026-07-09 re-checking rulings R1–R6 (`:135`). Its findings are
numbered defects in `bin/swarm`, e.g. *"**[WRONG] `deliver` exits 120, not 0, when stdout is a
broken pipe**"* (`:84`). **This is a code review. It has nothing to do with the shape of the tree
under the human.**

### WATCHLIST.md — **a live design ledger of falsifiers-with-fixes. The closest of the three to an "instrument," and still not one.**

VERIFIED (`docs/design/WATCHLIST.md:1-12`) — quoted in full because its framing is the whole
answer:

> `# WATCHLIST — what to keep an eye on in SIMPLEST, and the simple fix if it bites`
>
> *"**Author:** `simplest`. **Companion to** `docs/design/SIMPLEST.md` (its §6 falsifiers, made
> operational). **Untracked, like the design.** Each entry: the observable to WATCH, how to CHECK
> it cheaply, the TRIGGER that means it is real, and the SIMPLEST FIX consistent with the design —
> sized so that applying it never reopens the concept count by more than it must.*
>
> ***Rule of use: check on evidence, not on schedule*** *— most of these are checkable in one
> command the moment you suspect them. **None of the fixes should be built preemptively**; every
> one is a concept or a mechanism, and §8 of the philosophy applies: **it earns its way in only
> when the record shows the convention failing.**"*

**What it IS:** a **static list of 8 entries about the TOOL's design risks** — *"Senders don't
look"* (#1), *"Turn floods"* (#2), *"The stop re-ring stalls"* (#3), *"Journals rot into mush"*
(#4), *"Post-compaction floundering"* (#5), *"Operator-bound questions stay malformed"* (#6),
*"Scope creep in the rewrite itself"* (#7), *"The shared-tree hazard"* (#8).

**Its subject is the tool, not the operator's org.** Not one of its eight entries is about the
shape of the top layer. Nobody runs it; it is a thing you *consult* when you suspect something.
It has no invocation, no output artifact, no offer, no schedule — **by its own explicit rule**
(*"check on evidence, not on schedule"*).

**The one place it touches this proposal is as a VETO, not as prior art** — WATCHLIST #7 (`:99-108`):

> *"## 7. Scope creep in the rewrite itself (the disease that built the 27)*
> *- **WATCH:** the new tool growing **verbs, flags, fields, or states** the design does not name.
> Every concept in the current system was added by someone with a reason that sounded local and
> sane.*
> *- **TRIGGER:** **any addition that cannot point to a WATCHLIST entry whose trigger fired.***
> *- **SIMPLEST FIX:** this file is the fix. **An addition with no fired trigger behind it gets
> reverted**, and the urge behind it gets written here as a new entry with a falsifier instead."*

**The org-review instrument points to no fired WATCHLIST trigger.** (I checked all 8. None of them
is about top-layer shape; none has fired for this.) By #7's TRIGGER line read literally, it is an
addition with no fired trigger behind it. `OPERATOR-STRUCTURE-GRAVE.md:568` already made exactly
this charge against the *doctrine* proposal and I make it again here against the instrument.

---

## (b) ALIVE OR DEAD — the shipped-surface grep

**MEASURED.** I grepped the entire repo outside `docs/design/` and `.git/` for the strings
`SELF-AUDIT`, `WATCHLIST`, `REVIEW.md`, `SPAN.md`, `STRUCTURE.md`:

```
$ grep -rn "SELF-AUDIT\|WATCHLIST\|REVIEW\.md\|SPAN\.md\|STRUCTURE\.md" -I . \
    | grep -v "^\./docs/design/" | grep -v "^\./\.git/"
(no hits from any shipped surface)
```

**Shipped surfaces are:** `bin/swarm` (the whole CLI incl. the `spawn_header()` brief text that
reaches every agent, `bin/swarm:770-812`), `skill/SKILL.md` (the ONE file in `skill/` — VERIFIED,
`ls skill/` → `SKILL.md`), `WORLD.md`, `README.md`, `install.sh`.

| doc | git history | referenced by a shipped surface? | verdict |
|---|---|---|---|
| **SELF-AUDIT.md** | **ONE commit ever**: `2b8e701 cutover: the simplest tool moves into place` | **NO** (0 hits) | **DEAD LETTER.** Written once at the cutover, never touched again, cited only by REVIEW.md and by graveyard docs. |
| **REVIEW.md** | **ONE commit ever**: `2b8e701` (same cutover) | **NO** (0 hits) | **DEAD LETTER.** Same. A finished verdict on a finished review. |
| **WATCHLIST.md** | **TWO commits**: `02745a1 docs(simplest): the design doc … + the watchlist`, then `37cb2fa fix: the Stop-path re-ring is a single attempt` (a RESIDUAL added to entry #3) | **NO** (0 hits from shipped surfaces) | **ALIVE AS A DESIGN LEDGER, DEAD AS A MECHANISM.** It is actively *cited* — GRAVE.md quotes #7 twice, ONBOARDING argues against it — and it was *amended* once by field evidence. But **nothing in the shipped system reads it, prints it, or tells anyone it exists.** |
| **SPAN.md** | 3 commits, last `3bc2b3a docs(span): rung 0 balances the close rule` | **partially — its DOCTRINE is shipped, the doc is not.** SPAN's §3c draft text is now live *verbatim* in `bin/swarm:799-806` and `skill/SKILL.md:40-49`. But the doc itself is never referenced. | **ALIVE, and its content SHIPPED.** The one doc here that made it into the product — as *prose in the spawn header*, not as an instrument. |
| **STRUCTURE.md** | **UNTRACKED — zero commits** | **NO** | **DEAD LETTER (not even committed).** Its suggestion #1 *did* ship (the "name what recurred" sentence is now in `bin/swarm:797-800`) but the doc has never been committed. |
| **OPERATOR-STRUCTURE{,-RED,-RED2,-RED3,-FIX,-GRAVE}.md** | **ALL SIX UNTRACKED — zero commits each** | **NO** | **TODAY'S WORK. Unratified.** Six documents, 4,624 lines, written by this swarm on 2026-07-12, none committed, none shipped, none seen by the human as merged text. |

**The pattern, stated plainly:** *the only thing that has ever escaped `docs/design/` into the
product is PROSE — sentences that got pasted into `spawn_header()` or `SKILL.md`.* **Not one
instrument, not one verb, not one report artifact, not one review mechanism has ever shipped from
any of these documents.** The verb count is still four (`spawn`, `send`, `ps`, `close`) and
WORLD.md still opens *"Nine concepts, four verbs"* (`WORLD.md:3`).

---

## (c) ★ THE KILLER QUESTION — is the operator ALREADY GETTING this today?

> **NO. Categorically no. There is no shipped mechanism — none — that reviews the operator's top
> layer or suggests improvements to it. The instrument has never existed, has never been proposed
> before today, and the human has never once received its output.**

I looked for it in four places and it is in none of them.

### 1. The four verbs do not do it. VERIFIED.

`WORLD.md:3` — *"Nine concepts, four verbs."* The verbs are `spawn`, `send`, `ps`, `close`.
**`ps` is the only view**, and WORLD.md says exactly what it shows (`WORLD.md:29-30`):

> *"6. **`swarm ps`** — the one view: the tree, each agent's liveness, queue depth, idle-since,
> and last words — with the operator's waiting mail at the top."*

**`ps` renders facts. It renders no judgment, no suggestion, no review.** It tells you the tree
*is* flat; it never tells you the tree *should not be*. SPAN.md already drew this line and
**deferred** the only instrument in the neighborhood (`SPAN.md:236-239`):

> *"**`ps` load metrics** (child counts, task counters per node): **not rejected — deferred.**
> `ps` already shows the tree and queue depths; span is visible by looking. **If the record shows
> parents failing the span test *because they cannot see it*, a derived count column is the
> instrument that earns its way in** (convention → instrument, in order)."*

That is the nearest live door — **a derived count column in `ps`, explicitly deferred pending a
trigger that has not fired.** It is not the proposed instrument (no suggestions, no advice, no
top-layer subject); it is a *number*.

### 2. The closest shipped mechanism is THE REVIEW DESK — and it is a DECISIONS page, not a structure review. VERIFIED.

This is the one the prosecution must confront honestly, because its *name* is closest.
`skill/SKILL.md:40-49`, doctrine 5, quoted in full:

> *"5. **Attend within your span — and protect the operator's.** You are over span when you can no
> longer name each child's state and the next artifact you expect from it without re-reading; if a
> spawn would take you past that, spawn a coordinator and split the stream, and absorb a
> coordinator back (harvest, close, take the survivors) when its stream shrinks to what you can
> hold directly. **The operator's span is smaller still: ask them what it is (default ~3), then
> shape the tree so their *direct* load — decisions, waiting mail, review items — never exceeds
> it. The pattern is the review desk: hold everything yourself and hand the operator one ranked
> page, never the raw stream.**"*

and `skill/SKILL.md:87-89`:

> *"- **The desk.** Hand the human one ranked **decisions** page, never the raw stream — and
> declare it derived: regenerable from the journal and the repo at any time, never load-bearing."*

**READ WHAT THE DESK ACTUALLY IS.** Its content is *decisions the human must make* — and the live
record proves it. Every desk entry in the operator journal is a decision item, never a structural
observation. MEASURED, `.swarm/journal/operator.md`:

- `:29` — *"**Desk items for user now:** #65-#70 + codex design."* (PRs to merge)
- `:33` — *"Remaining desk item: **codex design decision**."*
- `:81` — *"**Desk updated: 2 decisions** (codex+HARNESS approve; benchmark smoke ~0.5M run y/n)."*
- `:90` — *"**Desk: 3 decisions** (codex+HARNESS, benchmark run, decision ledger + 2wk pilot)."*
- `:159` — *"**DESK:** whether to (a) place any Chinese model as a real node now, (b) fund a v3 clean-rig rerun, (c) shelve."*

**Not one desk item, ever, in the whole journal, is "here is what your top layer looks like and
here is how to improve it."** The desk is a *queue of pending human decisions*, held by a
coordinator so the human's inbox stays small. **It answers "what must I decide?" It has never
answered "how is my org shaped?"** These are different instruments with different subjects, and
conflating them would be the charitable summary I was told not to write.

### 3. The spawn_header duties do not do it — they point AT THE AGENT'S OWN CHILDREN, never at the human's top layer as an object of review. VERIFIED.

`bin/swarm:770-812` — the brief every agent receives. The tree-shape duties are all *self*-directed:

> *"Each reconciliation, ask whether **the tree** still matches the remaining work and whether
> **your span** still matches **your attention**: spawn what is missing, close harvested children
> whose workstream is done, split what you cannot attend, absorb what no longer earns its layer…
> **You are over span when you can no longer name each child's state**… **The operator's span is
> theirs to declare and yours to protect: never let the tree press more direct attention on the
> operator than they asked for.**"*

This is the closest thing in the shipped product, and it is **the exact opposite instrument**: it
asks *each agent* to reason about *its own* children and *not to burden* the human. **It produces
no artifact for the human, offers the human nothing, and never reviews the top layer as such.** It
is a duty to *not bother* the human, not a duty to *advise* them.

`skill/SKILL.md:45-47` gets closest — *"ask them what it is (default ~3), then shape the tree so
their direct load… never exceeds it"* — and even that is **a coordinator shaping the tree
silently on the human's behalf**, not an instrument that shows the human their structure and
suggests changes. **Nothing is reported back. Nothing is suggested. There is no output.**

### 4. The record itself says the human has never gotten this. MEASURED.

I grepped `.swarm/journal/operator.md` (the human's own seat journal, 55 KB, the complete record of
what the human has been handed across the project's life) for any top-layer review ever delivered.
**NULL RESULT.** The journal contains: dispatch entries, verdict entries, PR merges, desk-decision
lists, standing goals. **Zero entries in which anyone reviewed the human's top layer and suggested
improvements.** The only structural observations in it are the human's *own* (`:45`, his
hypothesis that *"strict structure belongs at the operator interface"*) — **an initiation, which is
exactly the speech act `DECISIONS.md:130-134` says he performs, and never a report he received.**

### THE (c) VERDICT, PLAINLY

> **It has only ever been a doc. Not even that — for the top layer specifically, it has never even
> been a doc until today.**
>
> **The shipped system gives the human: a tree drawing with no opinion (`ps`), a queue of decisions
> to make (the desk), and a set of duties telling agents to keep their own houses in order and not
> to crowd him (`spawn_header`). It has never once told him "your top layer looks like this, and
> here is how to make it better."**
>
> **The proposal is NOT redundant with anything shipped.** That is the strongest fact in its favor
> and I found it while trying to kill it. **The prosecution's case is therefore not "you already
> have this" — it is §d.**

---

## (d) ★ DOES OPERATOR-STRUCTURE*.md ALREADY KILL A STRUCTURE-REVIEW INSTRUMENT?

### The direct answer, and it must be given in two halves.

> **NO — not the instrument. There is NO KILL of a structure-review instrument anywhere in the
> OPERATOR-STRUCTURE family, or in the whole corpus. NULL RESULT: nobody has ever proposed one.
> `OPERATOR-STRUCTURE-GRAVE.md` performed its own exhaustive hunt for adjacent corpses and its
> hunt did not turn up this one either.**
>
> **YES — three of its four load-bearing parts. GRAVE.md and OPERATOR-STRUCTURE.md, written TODAY,
> already killed: (1) the OFFER/confirm handshake, (2) the overseer-node shape, and (3) any
> instrument that cannot point to a fired trigger. Each kill is quoted in full below.**

---

### KILL 1 — **THE OFFER / CONFIRM. Killed twice, today, on MEASURED grounds. This is the deadliest one and it aims directly at the "evidence-warranted OFFER from a coordinator."**

The proposal's second invocation path is *"a rare evidence-warranted OFFER from a coordinator
('your top layer looks worth reviewing')."* **That is a message into `queue/operator/` that asks the
human to engage.** Both of today's docs killed exactly that shape.

**`OPERATOR-STRUCTURE-GRAVE.md:281-305` — RULING on clause C, quoted in full:**

> **### 2d. RULING on clause C**
>
> > **The handshake is NOT a guardrail in PHILOSOPHY §2's sense — it blocks nothing and the
> > incentive test passes. It is a legitimate instruction of a shape this repo has shipped three
> > times. But it is the weakest limb of the proposal, and it should be CUT or WEAKENED, on
> > different grounds than the ones I was pointed at:**
> >
> > 1. **It is the only pre-flight duty in the repo that cannot complete inside the agent**
> >    (`WORLD.md:57-61` — the operator is a mailbox; nothing pushes to the human).
> > 2. **This repo has MEASURED the decay of exactly this gate: 16h → 14s in one day, "the tier
> >    labels stayed; the attention behind them thinned"** (`DECISIONS.md:120-127`). A confirm
> >    that decays to reflex is *worse than nothing* — it launders an unread shape as an approved
> >    one, which is the "obedience theater" this system stores no state for on purpose
> >    (`SPAN.md:19-23`).
> > 3. **A latency SLO on the human was explicitly refused** for the same reason: *"No latency
> >    SLO on pass-throughs. … making "open" uncomfortable rebuilds the nag"*
> >    (`DECISIONS.md:495-496`).
> >
> > **The version that survives** is the one the repo already ships for the opt-out: **state the
> > shape, once, and proceed** — *"the session says so plainly once rather than nagging"*
> > (`ONBOARDING.md:180-183`); the human's *"authority to say no"* is preserved without a gate
> > (`ONBOARDING.md:613-634`). **Announce, don't ask.** A human who wanted something else says so
> > — that is an *initiation/correction*, which is the speech act the record shows he actually
> > performs. This costs nothing the proposal wanted and removes the one clause the record
> > predicts will rot.

**And the underlying MEASURED datum, `GRAVE.md:258-279`, quoted because it is the whole case:**

> And the record has already MEASURED what happens to gates that wait on this human:
>
> > *"**The gate collapsed into standing authorization within a day:** #65–#68 waited **16–17h**
> > for the human's session (then merged as a batch 26 seconds apart); #72/#73, contract-class,
> > got 2.8h; #74, also contract-class, was merged under pre-auth in **14 seconds**; #76/#78 in
> > **3–4s** (MEASURED, pr-miner §c "tier drift"). **The tier labels stayed; the attention behind
> > them thinned.**"* — `docs/design/DECISIONS.md:120-127`
>
> That is the fate of the "one-line confirm," predicted from this repo's own data: **the human
> will type "yes" in three seconds without reading, and the doctrine will have purchased a
> ritual.**
>
> And the corroborating structural fact, MEASURED over the whole corpus:
> > *"**Genuine human judgment, wherever the record shows it, is an initiation or a correction,
> > never a gate answer**: rejected the overseer agent, "recon should shrink", R1/R2, the
> > choice-doctrine process correction, "decision POINTS, not questions"."*
> > — `docs/design/DECISIONS.md:130-134`
>
> **The human in this record does not answer gates. He initiates and he corrects.** A doctrine
> whose central move is "get a one-line confirm" is asking him for the one speech act the entire
> two-day corpus shows he does not perform.

**And the parent design doc CONFIRMED the kill and shipped its replacement — `OPERATOR-STRUCTURE.md:454-483`:**

> **### 4g. The opt-out, and the confirm**
>
> **The confirm: announce-only, and here is why the confirm died.** The operator ruled
> **confirm-on-first-swarm, announce-after** — *conditional* on *"first swarm"* being **a fact a
> file witnesses**, with a standing instruction: *"if genuinely nothing witnesses it, say so and
> default to announce-only rather than build state."*
>
> **Nothing witnesses it.** … **So: announce-only.** The session says its top layer in one line and
> proceeds; **it never waits.** **No state was built to manufacture a witness, which is the whole
> point of the constraint.**

and `OPERATOR-STRUCTURE.md:550-553`, the graveyard-check line:

> - *"the confirm"* — **corpse-adjacent, and now dead on its own merits** (§4g): this project
>   **measured** its own approval gate decaying **16h → 14s in one day** (`DECISIONS.md:120-127`:
>   *"The tier labels stayed; the attention behind them thinned"*). A confirm that decays to reflex
>   **launders an unread shape as an approved one.**

**WHAT EXACTLY WAS KILLED:** *any pre-work handshake that puts a message in the human's queue and
waits for (or invites) a reply.* **WHAT SURVIVED:** **announce-only** — *"state the shape, once,
and proceed."*

**WHY THIS HITS THE OFFER:** the proposal's OFFER is a message to the human that invites engagement
(*"your top layer looks worth reviewing"*). It is not a *blocking* gate, which is a real
difference and I concede it. **But it lands in the same queue, asks for the same speech act
(assent), and decays the same way.** WATCHLIST #6 — the entry that exists *to protect the operator's
queue* — is the standing objection, and GRAVE.md already fired it at the confirm
(`GRAVE.md:586-591`):

> - **#6 (operator-bound questions stay malformed)** — **relevant, and it cuts against clause C.**
>   Its subject is exactly the human's queue: *"questions in your queue you cannot decide from
>   their own text; **your own answering latency as the proxy**"* (`WATCHLIST.md:87-97`). A
>   mandatory pre-task confirm **adds one message to the operator's queue per task, forever** —
>   and #6's simplest fix is a wrapper that **refuses to send** malformed operator mail. **The
>   proposal's handshake is an unconditional new stream into the queue that #6 exists to protect.**

**The OFFER must therefore satisfy: (i) it is not unconditional — it is rare and evidence-gated;
(ii) it does not wait; (iii) it does not decay into a reflex "yes." The design must show its
evidence gate is a FILE FACT, not a vibe — or it is the confirm with better manners.**

---

### KILL 2 — **THE OVERSEER NODE. Killed by the human personally, and it is the shape an "instrument that watches the top layer and advises" most naturally becomes.**

VERIFIED, `docs/design/SPAN.md:231-234`, quoted in full:

> - **A load-balancer/overseer node**: **the nag reborn, structurally — a node whose job is other
>   nodes' behavior.** Rejected in the delegation design for the same reason (VERIFIED: operator
>   journal 2026-07-11); **parents judging tree shape *is* the distributed overseer.**

And the corroborating record that the **human himself** killed it — `DECISIONS.md:130-134`, as
quoted by GRAVE:

> *"Genuine human judgment, wherever the record shows it, is an initiation or a correction… :
> **rejected the overseer agent**, "recon should shrink", R1/R2…"*

**WHAT EXACTLY WAS KILLED:** *a node whose job is other nodes' behavior.* **WHAT SURVIVED:**
*"parents judging tree shape is the distributed overseer"* — i.e. the duty is distributed into
`spawn_header`'s doctrine 3 (*"Judge tree shape, not just artifacts"*, `skill/SKILL.md:29-31`),
never centralized into a watcher.

**WHY THIS HITS THE INSTRUMENT — and where it MISSES.**
- **It hits** any version of org-review that is a **standing agent** or a **periodic prompt** — a
  thing that watches the top layer and reports on it. That is *a node whose job is other nodes'
  behavior*, verbatim.
- **It arguably misses** an **explicitly-invoked, human-pulled skill** — because the human pulling
  a report is not a node watching. **The distinction the proposal must hold onto for dear life is
  PULL vs PUSH.** A skill the human invokes is a tool. An agent that offers is a watcher. **The
  proposal contains BOTH, and the second half is the overseer with a softer name.**
- Note the precedent that supports the pull half: `.swarm/journal/operator.md:100` — the human
  already accepted exactly this distinction once: *"Ships instead: **read-only observer DUTY (stint
  step, not standing agent, until evidence earns one)** — reads delivered/ after the fact,
  surfaces + drafts predicted decisions BESIDE the plane."* **A DUTY, not a NODE. That is the
  survivable shape, and it is already the record's answer to "we want something watching."**

---

### KILL 3 — **PHILOSOPHY §8's LADDER: "an engine never," and "a visibility verb second" — meaning an instrument must FOLLOW a proven convention, not precede it. The instrument has no convention behind it because the human has NEVER DONE THIS BY HAND.**

VERIFIED, `docs/PHILOSOPHY.md:245-266`, quoted in full:

> **## 8. Conventions earn their tooling**
>
> Nothing here was built because it seemed principled. **It was built after the convention proved
> out — and refused when it had not.**
>
> - **Checkpoints** began as a prompt-only duty in the spawn briefing. Only after they proved
>   useful did `swarm checkpoint --help/--context` appear — and it is still only a *schema
>   reference and a reader*. It does not write the file, validate it, or enforce it.
> - **The reconciliation loop** ships as briefing text. ASK #35 explicitly offered "Full
>   reconciliation engine" as an option. **It was not taken; the question was denied.**
> - **`swarm send operator`** was built only after the escalation contract had been exercised
>   enough for its missing terminus to become **a real, observed failure**.
> - **ZCode support** was dropped the moment research showed no CLI and no hook…
>
> The corollary is a standing bias: **prompt-level convention first, a visibility verb second, an
> engine never — unless the record shows the convention failing.**
>
> **The test this gives you: if you cannot point to the convention working in practice, you are
> not building tooling, you are guessing at a workflow.**

**AND HERE IS THE PROSECUTION'S SHARPEST FACT, MEASURED, AND IT IS MINE:**

> **§8's test is: "point to the convention working in practice." For org-review, THE CONVENTION HAS
> NEVER BEEN RUN. I grepped the full operator journal (55 KB, the complete two-day record of the
> human's seat) and found ZERO instances of anyone — human or agent — reviewing the top layer and
> suggesting improvements to it. Not once. There is no hand-done version of this to tool.**
>
> **By §8's own words, that makes this instrument "guessing at a workflow."**

This is precisely the argument `OPERATOR-STRUCTURE-GRAVE.md:568-579` made against the doctrine, and
it applies with *more* force to an instrument (which is one rung *higher* on §8's ladder than
prose):

> - **The TRIGGER line DOES fire, read literally.** *"Any addition that cannot point to a
>   WATCHLIST entry whose trigger fired."* **The proposal points to no fired WATCHLIST trigger.**
>   … **RULING on #7:** it fires **as a caution, not as a veto** — the same standing the operator
>   gave ONBOARDING. But the proposal is **strictly worse positioned than ONBOARDING was**, on the
>   evidence.

**WHAT SURVIVED:** §8 does not forbid an instrument forever. It sequences it: **convention →
visibility verb → (never) engine.** *"`swarm send operator` was built only after the escalation
contract had been exercised enough for its missing terminus to become a real, observed failure."*
**The instrument's licence is a demonstrated, observed failure of doing this by hand.** The
proposal must produce one — or run the convention first, by hand, and *then* tool it.

---

### KILL 4 (partial) — **THE FROZEN PLAN. Killed as a NEW corpse, and it aims at "advice the human acts on."**

`OPERATOR-STRUCTURE-GRAVE.md:170-178`, quoted in full:

> **The failing test is #2, and it is a real defect in the proposal as written, not a
> technicality.** "Before ANY task the operator designs its top layer, proposes it, gets a
> confirm, THEN works" is a **one-shot up-front design act with a human countersignature**. That
> is not the reconcile loop; that is a **plan**, and **a plan with an approval stamp on it is the
> thing an agent will not revisit.** SPAN is explicit that this direction is wrong:
> > *"**Depth is a cost, not a virtue** … the shallowest tree that passes the span test.
> > **Split under pressure, never in anticipation**; absorb eagerly on the way down."*
> > — `docs/design/SPAN.md:206-215`

and the general test it leaves behind (`GRAVE.md:151-168`), which the instrument **must pass**:

> > **The corpse is a self-description the TOOL can read and BRANCH on. The living thing is a
> > judgment the agent RE-MAKES at every reconcile and can only witness by ACTING.**
> >
> > Three tests, all three must pass:
> > 1. **Does any code read it?**
> > 2. **Does it survive the reconcile that would contradict it?** (A stored field does — that is
> >    what makes it config. A design act must not; if it does, **it has become config in prose**.)
> > 3. **Is it witnessed by the artifact, or by the declaration?**

**WHY THIS HITS:** an org-review **report artifact** — a document saying "your top layer should be
X" — is *a self-description that outlives the reconcile that would contradict it.* Test 2 is where
it dies. **A ranked structural report the human reads and adopts is a plan; SPAN says split under
pressure, never in anticipation.**

**WHAT SURVIVED:** *"a judgment the agent RE-MAKES at every reconcile and can only witness by
ACTING."* **An org-review whose output is CONSUMED AND DISCARDED in one turn — advice, not a
document that sits on disk being reasoned from — passes test 2. One that produces a durable
`docs/ORG-REVIEW-<date>.md` that anyone later cites as "the approved structure" fails it.**

---

### ★ AND THE ONE FINDING GRAVE.md MADE THAT OUTRANKS ALL OF THEM

`OPERATOR-STRUCTURE-GRAVE.md:32-36` — the overriding finding, quoted in full:

> **And one finding that outranks all five** (§3c): **the tool cannot represent the distinction
> the doctrine is about.** `bin/swarm`'s root session is *named* `operator`, so **`parent=operator`
> is the only tree a root session can build.** A doctrine about "the layer directly beneath the
> operator" is currently **unwitnessable** — no falsifier can collect on it, and this repo does
> not ship a doctrine whose falsifier cannot be collected (`ONBOARDING.md:742-743`).

**HOWEVER — AND THIS IS THE ONE PLACE I CORRECT MY OWN SIDE'S BEST WEAPON.** GRAVE.md was written
*before* the operator retracted the tool fix, and `OPERATOR-STRUCTURE.md` (the parent doc, §2-§3)
**overturns this finding on the operator's own reframe.** VERIFIED, `OPERATOR-STRUCTURE.md:99-103`
and `:144-146`:

> **This is the operator's reframe** … *"I spent this session proving that `operator` was the
> *wrong name* for the root session, and building a tool fix to rename it. **The name was never
> wrong.**"*
>
> **`operator` is a parent, not a participant.** That is exactly *"outside the swarm, and the
> parent of its top-level agents"* — **already implemented, already true.**

**So the "unwitnessable" objection is WITHDRAWN by the parent design, and I will not run it.** The
top layer **is** representable: it is `jq -r .parent .swarm/agents/*.json | grep operator` — the
operator's direct children. `OPERATOR-STRUCTURE.md:498-508` even ships the collector:

> 1. `jq -r .parent .swarm/agents/*.json | sort | uniq -c` — **how many direct children does
>    `operator` have, and do they have children of their own?**
> - **FALSIFIED WHEN:** the operator ends up with **≥3 direct children that have no children of
>   their own** — i.e. it spawned *workers*, not *top-level agents*.

**That is a file fact an org-review instrument could read TODAY, with no tool change.** It is the
single strongest technical asset the proposal has, and it was built by a sibling this morning.

---

## THE PROSECUTION'S CASE, ASSEMBLED

**The instrument is NOT redundant** (§c: nothing shipped does this, ever). **The instrument is NOT
a corpse** (§d: nobody has ever proposed it; NULL RESULT on the hunt). **But it is built out of
four parts, and three of them are already dead:**

| part of the proposal | status | the kill that reaches it |
|---|---|---|
| **advisory-only output (suggests, never restructures)** | **CLEARED** — this is the one clean limb. `.swarm/journal/operator.md:100` already shipped the precedent: *"read-only observer **DUTY** (stint step, **not standing agent**, until evidence earns one)"* | none |
| **explicitly-invoked named skill/command (human PULLS)** | **CLEARED ON SHAPE, BLOCKED ON §8** — a pull is not an overseer. But `PHILOSOPHY.md:265` demands *"if you cannot point to the convention working in practice, you are not building tooling, you are guessing at a workflow"* — **and the human has NEVER done this by hand. MEASURED: zero instances in the 55 KB operator journal.** | PHILOSOPHY §8; WATCHLIST #7's TRIGGER |
| **evidence-warranted OFFER from a coordinator (agent PUSHES)** | **KILLED-BEFORE, TWICE, TODAY** — this is the confirm wearing a new coat. `GRAVE.md:281-305` (*"CUT IT"*), `OPERATOR-STRUCTURE.md:454-483` (*"So: announce-only… it never waits"*), MEASURED decay 16h→14s (`DECISIONS.md:120-127`), and it is *"an unconditional new stream into the queue that [WATCHLIST] #6 exists to protect"* (`GRAVE.md:589-591`) | the confirm kill; WATCHLIST #6; SPAN's overseer kill |
| **a durable report artifact** | **MUST-SATISFY** — a document the human reasons from later is *"config in prose"* and fails GRAVE's test 2 (`:151-168`): *"Does it survive the reconcile that would contradict it? … if it does, it has become config in prose."* Advice consumed in one turn passes; a doc on disk called "the approved structure" does not. | the frozen-plan kill (`GRAVE.md:170-178`) + `SPAN.md:206-215` |

### The single strongest argument AGAINST building this at all

> **PHILOSOPHY §8, with a number behind it.** *"If you cannot point to the convention working in
> practice, you are not building tooling, you are guessing at a workflow."* **I looked. The
> convention has never been run: in the entire 55 KB operator journal — the complete record of
> everything the human has ever been handed — there is not one instance of anyone reviewing the top
> layer and suggesting improvements. Not by an agent, and not by the human himself.** Every
> instrument this repo has ever shipped (`swarm checkpoint --context`, `swarm send operator`) was
> built *after* the hand-done version had been exercised into a *real, observed failure*. **This
> one is being designed before its first hand-run.** The repo's own answer to that is the one it
> gave ASK #35: *"It was not taken; the question was denied."*

### What would make it survivable (the MUST-SATISFY list, derived)

1. **PULL ONLY.** Drop the coordinator's OFFER, or make its trigger a **file fact** the design
   names (e.g. `≥3 operator-children with zero children of their own` — `OPERATOR-STRUCTURE.md:506`
   already defines it) **and make it announce-only, never wait.** *"Announce, don't ask."*
2. **RUN THE CONVENTION FIRST.** Do the review by hand, once, on this actual tree, and show it
   produced something the human acted on. That is §8's price and this repo has never waived it.
3. **NO DURABLE "APPROVED STRUCTURE" ARTIFACT.** Advice consumed in a turn, not a plan on disk.
4. **NOT A NODE.** A duty or an invoked skill — never a standing agent, never a periodic prompt.
   *"A node whose job is other nodes' behavior"* is the nag reborn (`SPAN.md:231-234`), and the
   human personally rejected it once already.

---

## WHAT WOULD FALSIFY THIS DOCUMENT

1. **A shipped surface that references WATCHLIST/SELF-AUDIT/REVIEW.** One grep hit from
   `bin/swarm`, `skill/SKILL.md`, `WORLD.md`, `README.md`, or `install.sh` and my "DEAD LETTER"
   verdicts are wrong. (I ran it. Zero hits. Re-runnable in one command.)
2. **A top-layer review in the operator journal.** If any entry in `.swarm/journal/operator.md`
   shows the human being handed a structural review of his top layer, my §c headline collapses and
   the convention *has* been run. (I grepped. Zero.)
3. **A prior kill of a review instrument.** If any doc in `docs/`, `docs/design/archive/`, or the
   git history proposes-and-kills an org-review instrument, my "NULL RESULT" in §d is wrong.
   (GRAVE.md ran the same hunt independently — `:681-688` — and also came back empty. Two
   independent hunts, same null.)
4. **The desk turns out to carry structure.** If desk items in the journal include structural
   observations rather than only decisions, my §c-2 argument weakens. (I read all of them. Every
   one is a decision.)
