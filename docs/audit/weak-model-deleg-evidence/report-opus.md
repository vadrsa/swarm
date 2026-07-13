# CONTRADICTION AUDIT — WORLD.md vs STRUCTURE / OPERATOR-STRUCTURE / DECISIONS

**Author:** `wmd-opus`. **Read at:** working tree of `main@aa6063d`, 2026-07-12/13.
**Method:** WORLD.md read as the contract; each of its promises tested against the three
design docs, quoting both sides. Verdicts: **CONSISTENT** / **EXTENDS** (adds a rule WORLD
does not state, without denying it) / **CONTRADICTS** (cannot both be believed).

## 0. The finding that reorganizes everything else — READ THIS FIRST

**WORLD.md is in two states right now, and which one you read decides half the verdicts
below.**

- **Committed HEAD** (`git show HEAD:WORLD.md`) still says: *"Nothing pushes to the human, and
  **nothing ever refuses a message to the operator**."*
- **The working tree** (uncommitted, `git diff HEAD -- WORLD.md`, +8/-3) says: *"**a message to
  the operator is never dropped** — but a configured middleware may **re-route** it to the
  agent whose job it is to read it, and say so."*

The second text is **verbatim the repair OPERATOR-STRUCTURE §6 proposed** as a diff. So:

1. **WORLD.md at HEAD contradicts itself**, fourteen lines apart — *"nothing ever refuses a
   message to the operator"* against the middleware bullet's *"100 means the middleware handled
   it itself… and nothing is queued."* OPERATOR-STRUCTURE §4e′/§6 **found this and is right**
   (VERIFIED, I re-read both lines at HEAD).
2. **The repair is on disk but not committed.** An agent that runs `swarm world` — which prints
   the file, not the commit — gets the new text; an agent that reads the repo at `origin/main`
   gets the old one. **The contract currently depends on which copy you read.** That is not a
   doc-vs-doc contradiction; it is the contract contradicting itself in time, and it is the
   single most damaging item in this report (rank 1, §2).

Everything below judges against the **working-tree WORLD.md** (the file `swarm world` prints
today), and flags separately where the verdict flips at HEAD.

---

## 1. THE TABLE

WORLD's promises, numbered: **C1–C9** = the nine concepts ("What exists"); **P1–P5** = the five
bullets of "What is promised, plainly".

| # | WORLD promise (quoted) | doc | verdict | quoted evidence from the doc |
|---|---|---|---|---|
| **P3** | *"a message to the operator is **never dropped** — but a configured middleware may **re-route** it… **The operator queue alone is drained by its reader: the tool never delivers there**"* (working tree) | **OPERATOR-STRUCTURE** | **CONTRADICTS at HEAD; CONSISTENT in the working tree — and the doc is the *cause* of the difference** | §4e′: *"`WORLD.md:59` promises '**nothing ever refuses a message to the operator**' — and a middleware that exits 100 on a grandchild's operator-mail **refuses one**. … **That must be resolved in `WORLD.md`, and the honest resolution is escalate-don't-drop**"* + §6's diff, which *is* the working-tree text. **The doc diagnosed a live self-contradiction in the contract and shipped the fix to disk but not to a commit.** |
| **P3** | *"**Nothing pushes to the human**"* | **OPERATOR-STRUCTURE** | **CONSISTENT** | §4g: *"**So: announce-only.** The session says its top layer in one line and proceeds; **it never waits**."* Announce-only is the *anti*-push choice; the doc kills its own confirm gate rather than press the human. |
| **P3** | *"The operator is a mailbox, **not a node**."* | **OPERATOR-STRUCTURE** | **CONSISTENT — and it is the doc's whole thesis, quoting the tool back at WORLD** | §2a: *"`operator` is a parent, not a participant. That is exactly 'outside the swarm, and the parent of its top-level agents' — **already implemented, already true.** The model does not need a contract change; **it needs the contract to be *read*.**"* Cites `bin/swarm:1037`'s own comment: *"# operator is a mailbox, not a node."* |
| **C2** | *"The human **operator** roots the tree."* | **OPERATOR-STRUCTURE** | **EXTENDS — with a reframe that reads as a contradiction and is not** | §0: *"**The operator is not in the swarm.** An operator session is the human's **own tooling**."* §2a answers the collision head-on: *"**Both, and there is no contradiction — because the tool already models the operator as a parent that is not a node.**" **Verdict EXTENDS, not CONTRADICTS** — "roots the tree" and "is not a node in it" are both true of a parent that has no `agents/operator.json`. But this is the most *readable-as-contradiction* pair in the corpus (rank 3, §2). |
| **C9 / P5** | *"Duties — **briefed, not enforced**"* + *"**Nothing tracks obedience.**"* | **OPERATOR-STRUCTURE** | **EXTENDS, and it says so out loud** | §4e: *"we told them, in the one channel that reaches them — **and telling is not binding**."* §4e′: *"This makes the tree's impoliteness **unrepresentable on the exact path that carries the load**."* WORLD promises no *tracking* of obedience; the middleware does not track — it **prevents**. Prevention is not tracking, so this does not break P5's letter. **But it is a new enforcement surface WORLD's "briefed, not enforced" spirit does not lead you to expect** — and the doc concedes the price: *"It is a CONTRACT change, and I will not let 'no tool change' smuggle that in."* Honesty noted; the extension is still an extension. |
| **C9** | *"keep your span — direct children and live workstreams — small enough that you still truly read each one's work"* | **OPERATOR-STRUCTURE** | **EXTENDS — adds a numeric default WORLD never states** | §4c: *"**Start with one.** One agent beneath you… A second top-level agent is something you **earn on a real bottleneck**."* WORLD states **no number**, for anyone (VERIFIED: `grep -n "~3\|three" WORLD.md` → no hit). The doc knows it is on thin ice and argues it: *"**A default says where you *start counting*** … Allowed."* |
| **C9** | *"**delegate by default** (parallelizable work ground through serially is off-track)"* | **OPERATOR-STRUCTURE** | **EXTENDS — sharpens "delegate" into "never hold workers"** | §4a: *"**If you find yourself spawning workers, stop.** A worker under you is you doing swarm-internal work."* WORLD says delegate; the doc says *what you delegate to must itself own a subtree*. New rule, compatible direction. |
| **C9** | *"**close what is done** — keep a child only if you can name its next task"* | **STRUCTURE** | **CONSISTENT — and it applies the rule to its own tree** | §2d: *"The distinguishing test (already latent in the existing doctrine, **WORLD concept 9**…) is exactly 'can you name its next task' — and for `codex-scout` today, the honest answer is no."* §7.3: *"Close `codex-scout`… this is not a design change, it is an overdue action."* |
| **C9** | *"a **reconciliation** is a journal entry that names its falsifier"* + *"When you dispatch to a name you have dispatched to before, say what recurred, in the same entry"* | **STRUCTURE** | **CONSISTENT — and STRUCTURE is the *source* of the second clause** | §7.1 proposed verbatim: *"When you dispatch to a name you have dispatched to before, say what recurred, in the same entry — this is how repeated shapes of work become visible to anyone reading your journal."* **VERIFIED shipped**: that sentence is now in `bin/swarm` `spawn_header` (`:795-798`) and in WORLD C9. **A design doc's proposal became contract; nothing to reconcile.** |
| **C9** | *"split a stream under a coordinator when it outgrows you"* (attention/span) | **STRUCTURE** | **CONTRADICTS in evidence, not in text — and this is the sharpest true contradiction I found** | §2a: *"**Structure in this swarm has never once come from momentary attention pressure.**… **MEASURED, three times, zero for three**."* §4b: *"**SPAN was probing for a coordinator layer that this swarm's actual structure-forming mechanism never needed** — none of the four standing arms is a coordinator."* WORLD C9 hands every agent a *mechanism* (split under a coordinator when span is exceeded) that STRUCTURE reports has **never once fired in the recorded history of the system**. WORLD does not say "coordinators appear under load" — but the clause has no other trigger, and STRUCTURE's own dispatcher-side name-reuse mechanism (its §2b) is **absent from WORLD entirely**. |
| **C3** | *"`swarm spawn` — create a child. **The name is chosen, not derived; a name ever used is an error to reuse.**"* | **STRUCTURE** | **EXTENDS — and pushes right up against C3's edge** | §4b: *"**A fifth rung belongs in the ladder… rung 0, *name reuse*** — before any spawn decision, 'is this shape of work already owned by a **warm name** I should **re-address** instead of spawning fresh?'"* **Not a contradiction, and the distinction is load-bearing**: C3 forbids reusing a *dead* name (the journal is its tombstone); STRUCTURE urges re-*addressing a live* one. Same two words, two different acts. **Anyone who conflates them will read STRUCTURE as licensing exactly what C3 forbids** (rank 2, §2). |
| **C8** | *"**Judge artifacts, never claims.** … There is no ack, **no status taxonomy, no compliance record**"* | **DECISIONS** | **EXTENDS — it builds a stored, cited, audited record of verdicts, and defends the line carefully** | §4b.2: *"The seat auto-answers a hop-2 decision point **only** when it can cite a specific authorization line covering it, and **the verdict entry names the line**."* §4b.5: *"Per stint: **proxied count, pass-through count, sampled overturn check**."* This is a **compliance-shaped ledger** — of the *operator's* grants, not of agents' obedience. WORLD's C8 bans a taxonomy *the tool stores about messages*; DECISIONS' §4d.2 explicitly honors that ban: *"**No wire-side anything**: no decision-point or priority field in message records, no rules evaluated at delivery, no tool-stamped tags."* **Verdict EXTENDS, decisively — but it is the closest any doc comes to reintroducing the thing C8 exists to forbid, and it knows it** (§2, "Grave 2"). |
| **C8 / P5** | *"whether a message was *obeyed* is judged by its sender, from the work"* / *"Nothing tracks obedience"* | **DECISIONS** | **CONSISTENT** | §1e: *"An engine trained on 'operator approves 95% of X' learns a policy whose validity depends on the reading it would remove… **Goodhart, in one sentence.**"* §4d.1: *"**No learned classifier, confidence score, or threshold over decision features that issues answers.**"* DECISIONS refuses to build the obedience-statistic WORLD forbids, *on WORLD's own grounds*. |
| **C4** | *"**a message is a claim on one turn**… delivered **whole, one per turn, oldest first**"* | **DECISIONS** | **CONSISTENT** | §4d.7: *"**No latency SLO on pass-throughs.** The one aged decision aged because it deserved to; making 'open' uncomfortable rebuilds the nag."* Nothing in DECISIONS touches delivery order, wholeness, or the one-turn claim. |
| **P1** | *"**Delivered means delivered.** … **Nothing is ever silently dropped.**"* | **DECISIONS** | **CONSISTENT** | §4b.2: *"No citable line → **pass through to the human, whole**."* The engine's default is pass-through-whole; it drops nothing. |
| **P1 / P4** | *"**Nothing is ever silently dropped**" / "100 means the middleware handled it itself… **and nothing is queued**"* | **OPERATOR-STRUCTURE** | **CONSISTENT — but only because of the escalate-don't-drop repair it authored** | §4e′: *"the grandchild's report is **not dropped**: it is routed **up its own chain**, to the agent whose job is to read it."* The example middleware `send(p, "[escalated from …]" + body); sys.exit(100)` **sends before it exits 100**. **Silence would be a contract breach; escalation is not.** Note the residual the doc names itself (§5, F-MIDDLEWARE run 1): *"A **misconfigured fail-open middleware is indistinguishable from a working one** until you measure the mailbox."* — that is a *safety* limit, not a contract breach (fail-open passes mail through). |
| **C5** | *"The journal — Append-only, timestamped, your own words… **World-readable**"* | all three | **CONSISTENT** | All three docs treat journals as read-only evidence: STRUCTURE §1 builds its whole dataset from `.swarm/journal/*.md`; DECISIONS §4b.1 puts grants *in* the operator journal (*"their words to their sessions, **content not contract**"*) — using the journal as text, adding no field to it. |
| **C7** | *"`swarm close` — end an agent and its whole subtree. **Files stay.**"* | **STRUCTURE** | **CONSISTENT** | §3: *"`dead:` in `swarm ps` already lists every closed name, and each has a journal (**files survive close, VERIFIED WORLD.md concept 7**)."* Quotes the promise and relies on it. |
| **C6** | *"`swarm ps` — the one view… **with the operator's waiting mail at the top**"* | **OPERATOR-STRUCTURE** | **CONSISTENT, with a latent-bug warning** | §7: *"`is_dead()` treats a **paneless record as dead** (`:514-517`), and `eff_parent()` then **reattaches its live children to `operator` in the view**… so *any* future paneless agent record will silently reproduce a flat row in `ps`."* This does not contradict C6; it warns that the *one view* can lie about the tree. Worth carrying forward as a bug, not a doctrine conflict. |
| **P2** | *"**Promptness is best-effort.** … delayed, never lost."* | all three | **CONSISTENT (untouched)** | No doc addresses ringing, Stop-hook re-ring, or promptness. Recorded so the "every promise" requirement is met honestly rather than padded. |
| **C1** | *"**Agent** — a Claude session in a herdr pane… **The pane is ground truth**"* | **OPERATOR-STRUCTURE** | **EXTENDS — carves the operator out of C1, on measurement** | §3 (VERIFIED, ran it): *"`env -u HERDR_ENV -u SWARM_AGENT_ID swarm ps` → **WORKS. No herdr needed.**… The single gated verb is `spawn`."* §2 table: the operator lives *"**anywhere.** Its own pane, another machine, **outside herdr entirely**"*. C1 says *agents* are pane-bound; the operator is not an agent, so no contradiction — **but WORLD never tells you the operator is exempt from C1, and this doc is where that exemption is written down.** |

---

## 2. RANKED BY DAMAGE — what breaks if a new agent believes the wrong side

Ranked by *how bad the wrong belief is*, not by how confident I am the conflict is real.

### 1. The operator-refusal promise exists in two versions, and only one is committed — CONTRADICTION (contract-class)

**The wrong belief:** *"Nothing ever refuses a message to the operator"* (HEAD) — held by an
agent who then writes, reviews, or trusts a swarm whose middleware **does** refuse one.

**Damage: maximal, because it is the only item here that can make a message *appear* to have
been unlawfully suppressed.** An agent holding the HEAD promise sends to `operator`, sees `send`
exit 0, and believes the human will see it. Under a configured operator-span middleware, the
human never does — the mail went up the sender's own chain instead. The agent's model of the
world is now wrong in the one place WORLD explicitly promises it can't be, and **it has no way
to detect this** (`cmd_send` returns success either way). Worse, an agent auditing the system
will read HEAD, find the middleware bullet fourteen lines down, and reasonably conclude *the
tool is broken or the middleware is illegal* — and then "fix" one of them.

**Why it outranks everything else:** every other item on this list is a doctrine an agent could
be talked out of by reading a design doc. This one is **the contract lying to itself**, in the
file `swarm world` prints, with the correction sitting uncommitted on one machine's disk. It is
also the cheapest to fix (`git add WORLD.md`), which makes leaving it open the least defensible
state in the repo.

**Aggravating:** OPERATOR-STRUCTURE §10.2 says this repair *"is **owed whether or not the rest
of this ships**"* — the doc's own author ranked it as independently mandatory, and it is still
sitting outside a commit.

### 2. "A name ever used is an error to reuse" (C3) vs "rung 0: name reuse" (STRUCTURE §4b) — EXTENSION that reads as a contradiction

**The wrong belief, in either direction, and both are costly:**
- An agent that takes C3 literally and STRUCTURE loosely concludes *reuse is forbidden*, and
  **spawns `hardener-2` rather than re-addressing `hardener`** — paying full onboarding cost for
  every recurring task shape, which is precisely the waste STRUCTURE's entire §2b exists to
  prevent, and which would have prevented the only persistent structure this swarm has ever
  grown.
- An agent that takes STRUCTURE loosely and C3 not at all concludes *warm names are good*, and
  **reuses a closed name** — colliding with a tombstone journal, corrupting the one record that
  makes a dead agent's history readable.

**Damage: high and *bidirectional*, which is what pushes it above the doctrine items.** The two
readings fail in opposite directions, so no single cautious default protects you. The words are
identical ("name reuse"), the acts are opposite (re-address a **live** name vs. re-spawn a
**dead** one), and **neither document draws the distinction explicitly** — I had to derive it.
STRUCTURE §4b never says "live"; C3 never says "dead" (it says "ever used", which is *broader*
than dead and, read strictly, forbids STRUCTURE's rung 0 outright).

**Honest note:** I judged this EXTENDS rather than CONTRADICTS because the charitable reading is
available and clearly intended. But my *damage* ranking is about what a new agent believes, and
a new agent gets the strict reading of a contract before it gets the charitable reading of a
design doc.

### 3. "The human operator roots the tree" (C2) vs "The operator is not in the swarm" (OPERATOR-STRUCTURE §0) — EXTENSION, high blast radius

**The wrong belief:** *the operator is outside the swarm* → an agent decides the operator's
mailbox, journal, and queue are somebody else's tooling and **stops treating `operator` as an
addressable parent** — stops reporting to it, or starts treating "top-level agent" as a
protected class it may not be.

**Damage: high, because it changes who talks to the human.** This is the doc whose thesis is
most likely to be *adopted* (it is the newest, it is the one with the shipped SKILL.md diff),
and its headline sentence flatly denies WORLD's C2 as a matter of English. §2a's reconciliation
("a parent that is not a node") is correct, verified against `bin/swarm`, and **buried on line
140 of an 824-line document.** A new agent reads §0 and stops.

**Why it is only rank 3:** the reconciliation genuinely holds — no `agents/operator.json`, hooks
`sys.exit(0)` on operator, `ps` renders it as a header line. Nothing *breaks*; an agent just
acquires a confusing and partly-wrong model. The fix is one clause in WORLD C2 ("roots the tree
as a parent that is not a node") and would cost nothing.

### 4. WORLD C9's coordinator-split clause has never once fired — CONTRADICTION between doctrine and record

**The wrong belief:** *when I'm over span, I split under a coordinator* — an agent dutifully
spawns a coordinator layer that STRUCTURE §2a shows, **3-for-3 MEASURED**, never emerges under
real pressure and, per SPAN's own text (quoted in OPERATOR-STRUCTURE §4b), risks being *"a
middle layer that only forwards… structure lying about work."*

**Damage: moderate — a forwarder layer costs a pane, a name, and a hop, but nothing is lost or
corrupted.** It ranks below the three above because the failure is *waste*, not *incoherence*.

**But it is the item I'd most want the operator to look at**, because the *right* mechanism —
STRUCTURE's dispatcher-side name reuse, the only force ever observed producing standing
structure in this system — **is not in WORLD at all.** Half of STRUCTURE's finding shipped (the
"say what recurred" sentence is in C9 and `spawn_header:795`); the half that explains *why*
(reuse a warm name instead of spawning) shipped nowhere. WORLD hands agents the mechanism that
has never worked and withholds the one that has.

### 5. DECISIONS' authorization ledger vs C8 "no status taxonomy, no compliance record" — EXTENSION, contained

**The wrong belief:** *the system keeps no record of who approved what* → someone builds, or
tolerates, a proxied-answer flow with no audit line, which is exactly the *unmeasured drift*
DECISIONS §1c documents (*"contract-class attention collapsed **16h → 14s in a day**,
unrecorded"*).

**Damage: low-to-moderate, and mostly *pre-empted by the doc itself*.** DECISIONS is the most
disciplined doc of the three about staying inside WORLD's lines: its §4d NOT-list bans wire-side
fields, keyword detection, tool-stamped tags, and answers in the operator's voice — every one of
them a C8 hazard, refused. Its ledger lives in the **operator's own journal text**, which C5
already blesses as free-form. The extension is real (there *is* now a compliance-ish record) but
it is a record of **the human's grants**, not of **agents' obedience**, and C8 forbids only the
latter.

**The residual risk worth naming:** it is one sloppy adoption away from becoming the thing C8
buried. If a future implementer moves the grant lines out of the journal and into `.swarm/` as a
schema, grave 2 is exhumed and C8 breaks for real. DECISIONS §4d.2 saw this coming; nothing
enforces it.

### Not ranked, but recorded: two latent bugs the audit surfaced

- `is_dead()` + `eff_parent()` (OPERATOR-STRUCTURE §7): **any paneless agent record silently
  reproduces a flat row in `ps`** — i.e. C6's "one view" can misdraw the tree, which would
  corrupt exactly the observation this whole audit depends on.
- `relation()` gates the `OPERATOR` sender class on the **literal string** `"operator"` — any
  future rename of the root **silently downgrades the human's voice to "another agent"**,
  breaking WORLD C4's promise of four sender classes.

Neither is a doc contradiction, so neither is in the table; both are contract-breaking if
touched, so I refuse to drop them.

---

## 3. WHAT I AM LEAST SURE OF

**The judgment I would most expect to be wrong: my verdict that OPERATOR-STRUCTURE's send
middleware only *EXTENDS* C9's "briefed, not enforced" / P5's "nothing tracks obedience", rather
than *CONTRADICTING* them.**

**The argument I made:** WORLD forbids *tracking* obedience (a compliance record, an ack, a
status taxonomy). The middleware doesn't track anything — it *prevents* a send from reaching the
operator's queue. Prevention ≠ tracking. And WORLD's "briefed, not enforced" is stated about
**duties** (C9's list: journal, report, reconcile, delegate), not about **who may send to whom**
— so a code-level constraint on the send path doesn't falsify it on the letter.

**Why I think I may be wrong, stated as strongly as I can make it against myself:**

WORLD's opening sentence is *"It stores no claim about attention, compliance, or intent"* and C2
says *"**Who may message whom is judgment, not a rule engine.**"* An operator-span middleware is
**a rule engine deciding who may message whom.** That is not a strained reading — it is the
plainest possible reading of C2, and it is a sentence I did **not** put in my table as a promise
in its own right, which is itself a tell. If I had tested the middleware against **C2's second
sentence** rather than against C9 and P5, I think the honest verdict is **CONTRADICTS**, and it
would rank at or near the top of §2 — because it is a *permanent* structural change to the
system's stated philosophy, not a text bug like rank 1.

**Three things pull the other way, which is why I left the verdict as EXTENDS:** (a) the
middleware is **opt-in per swarm** and configured by the human, so "the system" still ships no
rule engine — a human installed one, which OPERATOR-STRUCTURE §4e′.3 argues is *"exactly what
this model says an operator session is for"*; (b) it is **fail-open**, so the default state of
any swarm is still pure judgment; (c) WORLD's own middleware bullet (P4) **already blesses exit
100 as legitimate** — the contract has *already conceded* that a configured middleware may
decide a message's fate, and it did so before OPERATOR-STRUCTURE was written. If P4 is in the
contract, C2's "not a rule engine" is *already* qualified, and OPERATOR-STRUCTURE is merely using
a seam WORLD opened.

**But I hold that reasoning at maybe 60/40.** The strongest counter I cannot dismiss:
**OPERATOR-STRUCTURE's own author agrees with the version of me I'm arguing against.** §4e′
lists as cost #1: *"**It is a CONTRACT change, and I will not let 'no tool change' smuggle that
in.**"* When the doc's author calls their own change contract-class and I grade it EXTENDS, the
burden is on me, and I am not certain I have discharged it. **If one verdict in this report gets
overturned on review, I expect it to be this one — and the overturn would move a
`CONTRACT-class` change into the ranked damage list above `name reuse`.**

**Second-place uncertainty, briefly:** I graded STRUCTURE's rung-0 name reuse as EXTENDS on the
live/dead distinction. **That distinction is mine, not either document's.** If the operator
intended C3's *"a name ever used is an error to reuse"* to mean exactly what it says — *ever
used*, live or dead — then STRUCTURE §4b's rung 0 is a flat **CONTRADICTION** of the contract,
and its rank-2 damage assessment is if anything understated. I could not find a line in either
doc that settles it, and I did not invent one to make my table cleaner.
