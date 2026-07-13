# ORG-REVIEW — the instrument for reviewing the operator's top layer

**Author:** `org-review-scout`, at the operator's request. 2026-07-12, against `main@aa6063d`.
**Companion to:** `OPERATOR-STRUCTURE.md` (which defines the layer; this reviews it).
**Evidence discipline:** **VERIFIED** (I read the line — quoted), **MEASURED** (a number, with
the command that produced it), **REASONED** (argument; falsifier named). Every collector below
was actually run. Where the evidence killed one of my own hypotheses, the corpse is on display.

---

## 0. The answer, in one paragraph

**Render the fact. Do not build the adviser.**

**The primary recommendation is three lines of change to `swarm ps` — no new verb, no new
concept, no skill.** `bin/swarm:574` is the *entire* render of every dead agent:
`lines.append(f"dead: {', '.join(dead)}")` — **one comma-joined line, names only.** A stillborn
agent and one that shipped forty artifacts **render byte-identically.** That is why `updater-v2`
— a standing role the operator briefed, which **never took a single turn** — sat unnoticed for
two days as the 114th name in an alphabetical list. **Un-collapse that line and print a per-agent
turn count and entry count, and the defect surfaces inside a command the human already runs.**
`SPAN.md:236` **pre-registered exactly this** — *"if the record shows parents failing the span
test **because they cannot see it**, a derived count column is the instrument that earns its way
in"* — and the failure it named is the failure that fired.

**Everything else is optional and the operator should feel free to decline it.** A second step
(§9.2) adds the one thing `ps` structurally cannot do — **joining a journal to an artifact on
disk**, which is `SPAN.md:213`'s *anti-forwarder test*, a test the doctrine **wrote and never
ran**. A third step (§9.3) adds the "memory" blocks — recurrence, standing/ephemeral, the mailbox
census, gate latency — which is **what the operator actually asked for** and which **SPAN did not
pre-clear.** I recommend it, I price it honestly, and **I do not pretend the record earned it.**

**Two rulings that do not depend on which step you take:**

- **The coordinator OFFER is dead.** The brief permitted me to drop it if I could not argue it out
  of nag-hood. I cannot. **The operator's own ledger already refused it** (`operator.md:23`:
  *"Rejected: overseer agent (nag reborn)"*). §5 buries it five times over.
- **The instrument SHOWS; it never SUGGESTS.** Three of four "is your top layer broken" collectors
  return **NULL** — the top layer is basically *healthy*. What fires is that it has **no memory**.
  The operator does not need a doctor. They need a **mirror** — and a mirror that keeps its mouth
  shut.

**And one warning earned the hard way, which is the truest sentence in this document** (from the
adversarial reviewer, after it killed my flagship example — §4b′): ***"A fact-sheet is not
opinion-free if the facts are wrong; it just launders a wrong opinion into the voice of a file."***
**A reader with bad inputs is *more* dangerous than an adviser, not less.** §4c′ is the rule that
exists because I proved it.

---

## 1. What I was asked, and the one word I am changing

The brief: *an instrument that reads world-readable evidence and **suggests** restructure moves,
advisory-only, explicitly invoked, plus a rare evidence-warranted **offer** from the coordinator.*

Two changes, both forced by evidence, both argued below:

| brief said | I recommend | why (short) |
|---|---|---|
| it **suggests** moves | it **shows** facts | The pathologies mostly aren't firing (§3). A suggestion engine over a healthy tree manufactures advice — and an instrument that prints an opinion the human then optimizes is the scored engine `DECISIONS.md` killed (§6). |
| coordinator **offers** a review | **no offer. Pull only.** | Killed on measured grounds. It is the nag, it violates §9, and the operator **already rejected an overseer agent in their own ledger** (§5). |

Everything else in the brief survives: advisory-only, no executor, explicit invocation,
world-readable evidence, per-item citation, no prescribed org shapes, in-swarm restructure
doctrine untouched.

---

## 2. The recommendation: `swarm review` — a visibility verb

**PHILOSOPHY §8** (`docs/PHILOSOPHY.md:262-266`, VERIFIED) sets a three-rung ladder and a bar:

> *"**prompt-level convention first, a visibility verb second, an engine never** — unless the
> record shows the convention **failing**."*
>
> *"**The test this gives you:** if you cannot point to the convention working in practice, you
> are not building tooling, you are guessing at a workflow."*

**Rung 2 — the visibility verb — is the recommendation, and it is the rung this repo has taken
twice before.** `swarm ps` is a visibility verb ("the one view"). `swarm checkpoint --context`
was one, and §8 itself notes it *"is still only a schema reference and a **reader**. It does not
write the file, validate it, or enforce it."* **That is exactly the shape of this instrument, and
it is the shape the repo has already blessed.**

### 2a. What it is

A read-only command. It reads `.swarm/agents/*.json`, the top-level agents' journals,
`.swarm/queue/operator/delivered/`, and the GitHub PR API. It prints **one page of file facts
about the top layer, each with its citation.** It then stops. It writes nothing, changes nothing,
spawns nothing, and recommends nothing.

**The human reads the page and decides.** That is the advisory-only ruling satisfied *structurally*
rather than by politeness: **a fact-sheet has no opinion to impose.**

### 2b. Why not the other four shapes

The instrument-first question was real and I tested all four. `grave-org`'s consolidated
graveyard verdict (`docs/audit/org-review-graveyard-2026-07-12.md`) ruled on each; where I
diverge from my own prosecutor, I say so and argue it.

| shape | verdict | reasoning |
|---|---|---|
| **Periodic prompt** | **DEAD. Killed three times.** | The nag. Not arguable. §5. |
| **Coordinator OFFER** | **DEAD. Killed today, twice, on measured grounds.** | §5. I asked for this to be killed and it was; I accept it. |
| **Coordinator duty** (a briefed sentence, no new surface) | **Rejected — and this is where I break with my prosecutor.** | The duty **already exists** and is **already failing**. `skill/SKILL.md:44-49` already says: *"The operator's span is smaller still: ask them what it is (default ~3), then shape the tree so their direct load … never exceeds it."* The doctrine is shipped. It did not prevent `updater-v2` (§3.4). **You cannot fix by better wording a failure that better wording has already failed to fix** (`OPERATOR-STRUCTURE.md:325`). Adding a 107th line to the skill is rung 1 applied to a rung-1 failure. |
| **Report artifact** (a doc an agent writes) | **CLEARED-CONDITIONAL, and it is the fallback.** | Legal *iff a human actually reads it* — the exact condition on which the last dashboard died. If the operator will not run a command, a generated report is strictly better than nothing. But it is **worse than the verb**, because it goes stale the moment it is written, and the verb is always current. |
| **Separate skill / command** | **RECOMMENDED.** | The lawful form. Cleared of the overseer kill: **invoked ≠ standing.** |

### 2c. Skill or verb? — a real fork, and I recommend the verb

The operator's instinct was a **skill**. I recommend a **verb** (`swarm review`), and the reason
is measured, not aesthetic:

**MEASURED** (`OPERATOR-STRUCTURE.md:627-636`, the sibling's field record): handed genuinely
parallelizable goals with **every documented trigger met**, the shipped `swarm` skill **never
loaded — 2 of 2.** It loaded reliably **only** on the literal phrase *"start a swarm."*

> *"the failure is **structural, not doctrinal** — the built-in Task tool wins the decomposition
> *before* the swarm question is asked."*

**A skill that only fires when you type its name is not a skill. It is a command with extra
steps.** So: ship the **command**. If the operator also wants a skill wrapper so `/org-review`
works conversationally, that is a free 20-line addition on top — but the *load-bearing* artifact
is the verb, because the verb cannot fail to fire.

**Cost of being wrong here:** near zero. The verb works with or without the skill; the skill
without the verb is a prompt that reads files by hand, badly.

---

## 3. The evidence — every collector, run, with its result

**This is the section that determined the design.** I ran these. Each is one command over
world-readable files.

| # | collector | result |
|---|---|---|
| 1 | **F-SPAN** — agents below the top layer mailing the human | **NULL. Does not fire.** |
| 2 | **Top-layer breadth** — is the operator over span? | **NULL. Does not fire.** |
| 3 | **Duplicate work** among top-level agents | **NULL — but a FALSE NEGATIVE. See below.** |
| 4 | **Stillborn agents** | **FIRES. 1 of 25 — and nobody saw it for 2 days.** |
| 5 | **Role recurrence** — shapes re-invented under fresh names | **FIRES, enormously.** |
| 6 | **Standing vs ephemeral split** | **FIRES. Bimodal, ~40× apart.** |
| 7 | **Gate decay** — the human's own review attention | **FIRES. Live today.** |
| 8 | **Operator ledger as a time series** | **UNUSABLE — and this kills half the brief's evidence plan.** |

**Read the shape of that table.** The three "is it broken" collectors return null. The four
"what have you built / what is happening to you" collectors fire. **That is why the instrument
shows instead of suggests.**

### 3.1 F-SPAN does not fire — NULL (and it refutes my own leading hypothesis)

`OPERATOR-STRUCTURE.md:498-506` names F-SPAN as the falsifier it *"would watch first"*: agents
below the top layer mailing the human directly. I weighted it first too. **It is wrong.**

**MEASURED** (I ran the depth-walk over `queue/operator/delivered/` × `agents/*.json` parent
chains; `ledger-forensics` reproduced it independently):

```
61 messages to the human.  22 distinct senders.
Messages from depth >= 2:  0
Unregistered senders:      0
```

**Zero.** Every message the human ever received came from a **depth-1** agent. The mailbox
discipline is **holding**. (The sibling's `deep` anecdote — an unregistered agent mailing the
human six times — **is not in this tree**; it was a sandbox-rig artifact. That correction is owed
to the sibling's record.)

### 3.2 Breadth does not fire — NULL (and it killed my second hypothesis)

I saw *"22 distinct agents mailed the human"* and reached for a breadth pathology. **Then I
measured concurrency and it collapsed.**

**MEASURED** (spawn `ts` from `agents/*.json` → journal mtime as last-sign-of-life):

```
Top-level agents EVER:            25
PEAK CONCURRENT top-level agents:  5     (modal state: 3–4)
Declared operator span (skill/SKILL.md:44, doctrine 5): ~3
```

**The declared span (~3) and the realized span (3–5) match.** The 22 was a *lifetime* count of a
*sequential* population. **The operator's top layer was never over-wide.** I record this because
I had written the opposite in my journal an hour earlier, and the collector fired against me.

### 3.2′ The duplicate-work NULL is a FALSE NEGATIVE — and the red team caught it

**I reported *"duplicate work: 0 pairs of 25"* and it is true of the predicate I ran and false of
the question the operator asked.** The predicate compares **siblings** — agents alive at the same
time doing the same thing. **It is structurally blind to *serial re-issue*:** `decision-scout` →
`decision-wiring` → `proxy-scout` → `pipeline-scout` → `hook-scout` — **five or six top-level
agents, over ~15 hours, circling one question.** No two are duplicates; the *sequence* is the
duplication.

**Corrected label: "no duplicate *sibling* work; serial re-issue NOT measured."** It is not
measured because I do not have a sound predicate for it, and **I will not print a number I cannot
prove is mine** (PHILOSOPHY §10). **This is a real hole in the evidence base and it belongs in the
NULL table as a hole, not as a clean bill of health.**

### 3.3 The recurrence — FIRES, and it is the spine of the design

**MEASURED** (`role-census`, over 115 agent records, classified by *brief text* not by name, via
four parallel classifiers on a pinned taxonomy — `docs/audit/org-review-roles-2026-07-12.md`):

| role | distinct names that held it | names ever reused |
|---|---:|---:|
| **FORENSICS** | **34** | 0 |
| **RED** | **25** | 0 |
| **SCOUT** | **21** | 0 |
| *literal name reuse, anywhere in the entire record* | | **ZERO** |

- The `scout → drafter → red` three-stage shape ran **4 times in full, with all-new names each
  time.** The weaker `design → attack` shape ran **9 times.**
- **The RED role was re-invented 25 times by 14 different dispatchers, not one of whom reached
  for an existing name.**

**Now put that against the human's own words.** VERIFIED, `.swarm/journal/operator.md:45` — the
ledger recording the human's own post-heavy-flood hypothesis:

> *"structure comes from repetition, and **nothing remembers structural repetitions**"*

**The human diagnosed this from intuition, unprompted. The file record now proves it to three
significant figures — 25 reds, 34 forensics, 21 scouts, zero reuse. Nothing remembered a single
one of them.** This is not a pathology to be fixed by advice. It is a **memory the operator does
not have and cannot build by hand.**

**The control that makes this non-vacuous** (the obvious red-team kill is *"that's just one
parent's busy afternoon"* — it is not): the taxonomy's `OTHER` class (the three SPAN load
fixtures) is **3 instances / 24 minutes / 1 parent — a textbook burst.** `RED` is **25 instances
/ 3 days / 14 different parents — spread.** **The metric separates cleanly, and the recurring
roles land on the standing side.**

**And here is why the shipped doctrine cannot see it — a real gap in `STRUCTURE.md`, surfaced by
`role-census` (REASONED, and it says so):**

`STRUCTURE.md` §2b dismisses repetition using the span-probe case — *9 tasks / one queue / one
hour / one parent* — and rightly calls that **backlog**, not structure. **But RED is the opposite
on every axis: 25 instances, 14 parents, 3 days.** The doctrine rules out backlog-in-one-queue.
**It is silent on a shape that 14 independent dispatchers each re-derive from scratch.**

`STRUCTURE.md`'s test is *"I, the dispatcher, keep choosing to reuse this name."* **That test is
structurally incapable of registering a role that 14 different parents independently invent 25
times** — because **no single dispatcher repeats**, and **WORLD concept 3 forbids the very
name-reuse the test watches for.** *The doctrine's signal and the tool's naming rule are
entangled.*

**`updater-v2` is that entanglement made flesh** (§3.4): the operator *tried* to reuse the warm
name, the tool refused, and the agent was **stillborn.** The doctrine said *reuse the warm name*;
the tool said *a name ever used is an error to reuse*; the operator's workaround died without
taking a turn. **This is not a gap the instrument closes — it is a gap the instrument makes
visible, which is the only honest thing a reader can do with it.**

### 3.4 `updater-v2` — the stillborn agent. The instrument's existence proof.

**VERIFIED** (`shape-forensics` §3.2; I re-read every file myself):

- **`.swarm/agents/updater-v2.json`** — spawned **by the operator**, 2026-07-10 17:09:32Z.
- **`.swarm/journal/updater-v2.md`** — 57 lines, **exactly one `##` entry**: the spawn stub,
  written by the tool. **The agent never wrote a word.**
- **No `.swarm/event/updater-v2.json`** — it never fired a Stop hook. **It never completed a turn.**
- Its brief opens, verbatim: *"You are `updater`, a standing agent that keeps the swarm tool
  itself up to date."* — the operator was trying to **re-brief the warm `updater` role.** WORLD
  concept 3 forbids reusing a name, so they minted `updater-v2`, which **collided with the
  still-live `updater` and died without taking a turn.**

**It was spawned on 07-10. It is 07-12. Nobody noticed for two days.**

Read what that single artifact contains:

1. A **real defect in the operator's top layer** — a role they wanted, briefed, and never got.
2. **100% visible in world-readable files** the entire time.
3. **Invisible to every human and agent for 48h**, because `ps` collapses ~100 dead agents onto
   one line and nobody re-reads 25 journals.
4. **Mechanically detectable in one line**: *a journal whose only `##` header is the spawn stub
   never took a turn.*
5. And it is **warm-name-reuse failing in the record** — SPAN's own rung 0 (*"before spawning
   fresh: is this shape of work already owned by a warm name?"*). The doctrine says reuse the
   warm name; the tool forbids reusing the name; the operator's workaround was **stillborn**.

**This is the whole case for the instrument in one file.** Not a hypothesized pain — a defect
that happened, in this repo, to this operator, and sat unread for two days.

### 3.5 The gate decay — FIRES, and it is running today

`ledger-forensics` refused to trust `DECISIONS.md`'s number and **re-measured it from the GitHub
API**. **MEASURED** (`gh pr list --state merged --json createdAt,mergedAt`, open→merge latency):

```
#65 17.4h  #66 17.3h  #67 16.1h  #68 16.0h   <- the gate, working
#72  2.8h  #73  2.8h                          <- thinning
#74   14s  #75  3s  #76  3s  #77  3s  #78 4s  <- collapsed
#81    9s  #82  3s                            <- TODAY. Still collapsed.
```

> **CORRECTION — the numbers survive; my warrant for them did not.** An earlier draft said
> *"merging is an act only the human performs… **the one channel in the entire system that
> measures the human's own attention and cannot lie**."* **The adversarial reviewer broke that and
> it is right.** `mergedBy: vadrsa` proves the **account**, not the **hands**. VERIFIED,
> `operator.md:30`: *"User merged #65–#70 (**via my gh calls, user-authorized**)"* — **an agent
> running `gh` under the operator's credential.** And `operator.md:90`'s own diagnosis is
> *"collapsed **under pre-auth**"* — **the operator's own explanation for the 3-second merges is
> that authority was delegated**, not that a human read a diff in three seconds.
>
> **This is the same conflation §3.6 congratulates itself for avoiding** (session latency ≠ human
> latency), committed one section earlier. It is Rule-2 violation #2 (§4c′).

**So what does this block actually measure?** *Open→merge latency **on the operator's account**,
including agent merges executed under standing pre-authorization.* **That is what the caption must
say, and the reader must never say more.**

**And the finding still stands, because the operator themselves named it** (VERIFIED,
`operator.md:90`):

> *"**Uncomfortable mirror: my gate collapsed 16h→2.8h→14s under pre-auth, tier labels intact,
> attention thinned** — the engine already runs off-books."*

**The thinning of *authorization* is the phenomenon**, whoever's hand ran `gh`. A gate that once
took 17 hours and now resolves in 3 seconds has been delegated away, and **the operator wrote that
sentence about themselves and the collapse continued anyway — #81 and #82 merged today, in 9s and
3s.** *Naming it in prose did not stop it.* **That** is the §8 escape clause, and it does not
depend on the claim I got wrong.

**⇒ A true human-attention channel does not exist in these files.** That is now §6d, hole #6, and
the reader's job is to say so rather than manufacture one.

And the decisive part: **the operator already found this, and named it, and it did not stop.**
VERIFIED, `operator.md:90`:

> *"**Uncomfortable mirror: my gate collapsed 16h→2.8h→14s under pre-auth, tier labels intact,
> attention thinned** — the engine already runs off-books."*

**They saw it. They wrote it down. It kept happening.** #81 and #82 merged **today**, in 9s and
3s. **A convention that has been named in prose and continues to fail is precisely §8's escape
clause** — and it is the clause that licenses rung 2.

### 3.6 The operator ledger cannot answer the question the brief asked of it

**This is the most important negative finding, and the operator needs it plainly.**

My brief told me to mine `.swarm/journal/operator.md` for *"what the human keeps pulling up to
themselves"* and *"confirm-but-never-read decay."* **That file cannot answer either question.**

**(a) It is not the human's ledger. It is an agent's.** VERIFIED — `skill/SKILL.md:51-59`
establishes the *operator seat*: a session acting for the human is a **hand**, and every entry
from 07-11 onward carries a `[ops-main]` hand tag. VERIFIED — `bin/swarm:1037`:
`# operator is a mailbox, not a node: no pane, no doorbell`. **The human has no pane, no session,
and writes nothing into `.swarm/`.** The human appears in that file only as *reported speech*
("User approved…", "Operator: …"). Every *"I verified it myself"* line is **an agent** claiming
to have read.

**(b) It has no clocks.** **MEASURED:** of 112 `##` headers, **exactly zero carry a clock time.**
All are date-only, and **73% of the corpus falls on a single calendar day**, mutually unordered.
**You cannot compute any latency, duration, or rate from that file.** It is a narrative, not a
time series.

**(c) It cannot witness its own reading.** It contains *claims* of reading — which is exactly
what WORLD concept 8 says not to trust: *"Judge artifacts, never claims."*

**Consequence for the design, and it is a hard one:** **the "confirm-but-never-read" signal the
brief asked me to detect is not in that file, and no instrument can put it there.** The honest
attention channels are **machine-written and cannot lie about time**: the **GitHub API** (§3.5)
and `delivered/` **ctime**. The instrument reads *those*. The ledger it reads only for **names and
PR numbers**, which cross-reference cleanly.

> **A trap I nearly walked into, recorded because it is instructive.** `delivered/*.json` ctime
> records mail-claim time: **median 19s**, and **47 of 59 messages were claimed faster than adult
> reading speed** (one 7,544-char report claimed in **12 seconds** = 647 chars/sec). That looks
> like a devastating "the human doesn't read" headline. **It is false.** Per the seat contract the
> claimer is the *operator session*, not the human — that is an **AI picking up its mail
> promptly**, which is correct behavior. `ledger-forensics` caught this and refused to ship the
> headline. **The instrument must never present session latency as human latency**, and §7 makes
> that a falsifier.

---

## 4. The design

### 4a. What it reads (all world-readable; nothing new is stored)

| source | what it yields | can it lie? |
|---|---|---|
| `.swarm/agents/*.json` | top-level census (`parent == "operator"`), spawn `ts`, the brief text | no — tool-written |
| `.swarm/journal/<top-level>.md` | `##` entry count, first/last entry, dispatch structure, whether the last entry names a next task | no — append-only, mtime is a fact |
| `.swarm/event/<name>.json` | did the agent ever complete a turn | no — hook-written |
| `.swarm/queue/operator/delivered/*.json` | sender, depth (via parent chain), volume, body size | no — tool-written |
| GitHub PR API | **open→merge latency = the human's actual review attention** | no — external, machine-stamped |
| `.swarm/journal/operator.md` | **names and PR numbers ONLY** (§3.6 — never times) | **yes, about time. Do not read times from it.** |

**Nothing is written. No new file, no new state, no schema.** This is the property that makes it
a reader and not an engine, and it is checkable: `swarm review` must be safe to run a thousand
times.

### 4b. What it prints — the page

Six blocks. **Each line carries the file fact that produced it.** No verdicts, no scores, no
recommendations, no ranking of the human's choices.

```
$ swarm review

TOP LAYER — 5 live, 25 ever

  STANDING (>24h, multiple separated dispatches)
    hardener        3313m  20 entries  Task 1 → Task 14        last: "Task 14 GREEN, reported"
                                                               next task named: YES
    updater         3908m  18 entries  cycle × 9               last: "cycle: 1e254e4 → b94fa9e"
                                                               next task named: YES (watch loop)
    field-tester    4163m  37 entries  16 children             last: "day's reconciliation"
                                                               next task named: YES (4 open offers)

  EPHEMERAL (<2h, one report, died)         19 agents
    codex-scout 0.3h · structure-scout 0.1h · red-simplest 0.2h · … (16 more)

  ⚠ NEVER TOOK A TURN
    updater-v2      spawned 07-10 17:09, journal has only the spawn stub,
                    no event record.  Its brief: "You are `updater`, a standing
                    agent…" — the warm name `updater` was live at the time.
                    .swarm/journal/updater-v2.md (1 entry)

RECURRENCE — roles re-instantiated under a fresh name
    RED         25 distinct names, 0 reused   spread: 3 days, 14 parents
    FORENSICS   34 distinct names, 0 reused
    SCOUT       21 distinct names, 0 reused
    scout → drafter → red: ran 4× in full, all-new names each time
    (control: OTHER = 3 names / 24 min / 1 parent — a burst, not a role)
    .swarm/agents/*.json, classified by brief text

    YOUR OWN DOCTRINE ON THIS (operator.md:54):
      "a future adversarial review spawns fresh reviewers BY DESIGN —
       independence is the value; warm context is a LIABILITY for that shape"
      ⇒ some of the RED count is deliberate policy, not waste. The reader
        prints the count and your policy. It does not tell you which is which.

YOUR MAILBOX — 61 messages, 22 senders
    from depth ≥ 2 (below your top layer):  0
    top senders: hardener 16 · field-tester 13 · updater 12
    19 agents mailed you exactly once, then died
    .swarm/queue/operator/delivered/

GATE LATENCY — open→merge on your ACCOUNT
    (includes agent merges under standing pre-authorization — this does NOT
     measure your reading; no file records that. §6d hole #6)
    #65 17.4h  #66 17.3h  #67 16.1h  #68 16.0h
    #72  2.8h  #73  2.8h
    #74   14s  #75 3s  #76 3s  #77 3s  #78 4s
    #81    9s  #82 3s          ← most recent
    merged_by: vadrsa (all)    gh pr list --json createdAt,mergedAt,mergedBy
    operator.md:90 — "my gate collapsed … attention thinned"  (2026-07-11)

SPAN — declared vs realized
    declared (skill/SKILL.md:44, doctrine 5):  ~3
    peak concurrent top-level agents:           5
    modal:                                      3–4
```

### 4b″. `⚠ FORWARDING LAYER` — the block I added last, because my own subtree generated the defect

**I did not find this pathology in the record. I caused it, today, and I am reporting it against
myself because a design document that illustrates its value with a defect it caused — and hides
the authorship — is exactly the self-serving evidence I would kill in someone else's work.**

While this investigation ran, a child of mine (`shape-forensics`) grew a subtree six levels deep.
I read `swarm ps`, judged it over-delegated, and ordered the layer collapsed. **The layer was
worse than untidy: it was already dead. VERIFIED — I ran all four checks myself:**

- **`docs/audit/_fp-compliance.md` DOES NOT EXIST.** Its synthesis was never written.
- **`docs/audit/_fp-compliance-shard-brief.md` (5,024 B) DOES exist.** It briefed **8 descendants.**
- **`.swarm/journal/fp-compliance.md`: 3 entries, ending mid-plan, addressing children whose
  answers it never received.**
- **It briefed, it forwarded, and it died.**

**`SPAN.md:213`, VERIFIED verbatim:**

> *"A middle layer that only forwards — adds no judgment, writes no synthesis — **is structure
> lying about work**, and its parent should close it."*

**That is `fp-compliance`, exactly. MEASURED cost: one middle layer, 9 agents, zero artifacts,
one undelivered measurement.** Part of a question in that child's brief is simply **not
answered**, and it recorded the hole rather than let the surviving numbers imply full coverage.

**Now the part that matters for this design, and it is an argument against my own competence:**

**`ps` did not catch this. I did not catch this.** `ps` showed me *depth* — a shape I disliked on
doctrinal grounds — and I got the right answer from a weak signal. **What `ps` never showed me,
and what I never asked, is the fact that actually mattered: `fp-compliance` had 8 children, 3
journal entries, and zero artifacts.** A page that printed that line would have made the failure
obvious to anyone who glanced at it.

**This is the instrument's case, made by my own failure to see properly** — and it is stronger
than any pathology I went hunting for, because **most of those came back null** (§3) while this
one is live, dated, file-verifiable, mechanically detectable, and **was generated under doctrine
by an agent that had read the doctrine.**

```
⚠ FORWARDING LAYER — has children, wrote no synthesis, produced no artifact
    fp-compliance   8 children · 3 journal entries · last entry ends mid-plan
                    named deliverable docs/audit/_fp-compliance.md — DOES NOT EXIST
                    SPAN.md:213 — "structure lying about work"
```

**Predicate (per §4c): an agent with ≥1 child, whose journal has no entry after its last spawn,
and whose named deliverable does not exist on disk.** Mechanical. No judgment. The human decides
what it means.

### 4b′. THE RETRACTION — my flagship example was false, and its refutation is the most important thing in this document

**An earlier draft of this section printed a `⚠ BLOCKED` block and called it *"the best line on
the page,"* *"the design's central claim, tested on a live example and holding."* It said:
`hardener`, the swarm's most productive agent, had been **blocked for 15 hours waiting on
`field-tester`, which is dead.`**

**It was false. The adversarial reviewer killed it, I re-ran the check at source, and it is
right.** VERIFIED:

- `field-tester` **was alive and working all day.** Journal entries at **15:50Z, 16:12Z,
  16:35Z**; it mailed the operator at **14:41, 15:41, 16:02Z** — *fourteen hours after* the
  `hardener` line I quoted as proof of blockage.
- It was **the busiest agent in the swarm**, and it was **closed on harvest, having finished.**
- **`hardener` is not blocked on a corpse.** Its own quoted sentence says what it waits for:
  *"field-tester verification / **next dispatch**"* — **it is idle awaiting the operator.**

**How I did it:** I read a `swarm ps` snapshot taken *after* `field-tester` was closed, and
**back-projected deadness onto a fifteen-hour-old journal line.**

**And this is the finding.** That is *precisely* the trap I documented in **§6d, hole #1**, in
this same document, six hundred lines earlier, in my own words: *"THE RECORD HAS NO DEATH.
`is_dead` is computed at read time from herdr pane liveness. A deliberate `swarm close` and a
crashed pane are byte-identical in the files."* **I wrote the warning, and then I walked into
it, and then I called the result the best thing on the page.**

> **The reviewer's sentence, which is the truest thing written about this design and which I
> adopt as its stated central risk:**
>
> ***"A fact-sheet is not opinion-free if the facts are wrong; it just launders a wrong opinion
> into the voice of a file."***

**My thesis was "a reader cannot be wrong in a damaging direction, because it has no opinion to
be wrong about." That thesis is FALSE, and my own instrument disproved it.** A reader with bad
inputs is **more** dangerous than an adviser, not less — because it wears the authority of the
record, and a human who would argue with a suggestion will not argue with a file.

**The reader's safety was never in the absence of opinion. It is in the correctness of its
inputs and the honesty of its captions.** That is a weaker claim. It is the true one. **The rest
of this design is rebuilt on it (§4c), and the block is deleted, not repaired** — because there
is no death field to repair it with.

**What survives, and why the design is not dead:** the *other* two live defects (§3.4
`updater-v2`; §4b″ `fp-compliance`) rest on **positive file facts** — an entry count, a child
count, a missing artifact — **never on a liveness inference.** I re-verified both under the same
suspicion after this kill landed:

```
updater-v2:     journal '## ' entries: 1   event record exists: False
                (a count and an absence — not a liveness read)
fp-compliance:  journal entries: 3   children: 4   named deliverable exists: False
                (a count and an absence — not a liveness read)
```

**That line — between what a file *witnesses* and what a snapshot *implies* — is now the
instrument's first law.**

**Note what is absent.** No "you should…". No health score. No "3 of 5 agents are underutilized."
No ranking. **The `⚠` on `updater-v2` is the single strongest thing it says, and it is a
description of a file, not a judgment of the human.** The human looks at that page and knows
instantly what to do about `updater-v2` — because they are the only one who knows what they meant
to build. **That is the advisory-only ruling, honored structurally.**

### 4c. The one interpretive line I do allow, and its strict rule

Three of the six blocks require a *definition* to be useful — "standing" vs "ephemeral,"
"never took a turn," "recurrence." Those are **classifications**, not judgments, and the rule
that keeps them honest is:

> **Every classification must be a stated, mechanical predicate over a named file, printed with
> the file it came from — and the human must be able to re-derive it in one command.**

- *standing* ≡ lifetime > 24h **and** ≥ 2 dispatches separated by > 1h. (Not "important.")
- *never took a turn* ≡ journal has exactly one `##` header **and** no `event/<name>.json`.
- *recurrence* ≡ two agents whose **brief text** asks for the same deliverable shape.

If a predicate cannot be stated that way, **the block does not ship.** This is the line between a
reader and a scorer, and §6 explains why the repo has already killed everything on the far side.

### 4c″. RULE 3 — print the raw numbers; do not invent the bucket. *(Adopted from the red team, W2.)*

The draft page sorted agents into **STANDING** vs **EPHEMERAL** on a threshold I invented
(`>24h ∧ ≥2 separated dispatches`). **The reviewer is right that this is a judgment wearing a
predicate's clothes** — *I* chose 24 hours, and the operator never agreed to it.

> **RULE 3: where a bucket is not in the files, print the raw numbers and let the human bucket
> them.**

So the page prints `lifetime · entries · dispatches · children · last entry`, sorted by lifetime,
and **the bimodality speaks for itself** (three agents at 55–69h; twenty-two under 2h; nothing in
between). **The human sees the gap and names it, or doesn't.** Same for the `⚠` glyph: it is
dropped from the shape blocks. It survives **only** on the two blocks whose predicate is a
*factual absence* — a journal with no entry after its last spawn, a named deliverable that is not
on disk — because *"this file does not exist"* is not an opinion.

### 4c′. RULE 2 — no block may assert a state the files do not record. *(This rule exists because I broke it twice.)*

**Rule 1 (mechanical predicates) is necessary and it is NOT SUFFICIENT.** I obeyed it and still
shipped two false claims, because **a predicate can be perfectly mechanical and still be a lie if
the field it reads is a *proxy* for the thing it claims.** I made the identical error twice, in
adjacent sections:

| | I asserted | what the file actually records | the field I invented |
|---|---|---|---|
| **§4b′ (killed)** | *"`field-tester` is **DEAD**"* | herdr **pane liveness**, computed at read time | **death** |
| **§3.5 (corrected)** | *"**only the human** merges — this cannot lie"* | a **GitHub account id** (`mergedBy`) | **the human's hands** |

**Both are mechanical. Both are measurements of something other than what I said they measured.**
And the second is worse than the first, because **§3.6 is the section where I congratulate myself
for avoiding exactly this trap** — refusing to report `delivered/`-ctime as human reading latency
— and then I committed the same conflation one section earlier.

> **RULE 2: The reader prints only what a file *witnesses*, in that file's own terms, and names
> the field it read. Where the fact the human wants is not in the files, the reader's job is to
> SAY SO — never to infer it.**

**In practice:**

- It may print `last journal entry: 16:35Z` and `last event record: <ts>` and `no event record`.
  **It may never print `DEAD`** — there is no death field (§6d #1).
- It may print `open→merge on your account: 3s (merged_by: vadrsa)`. **It may never print
  *"you merged this in 3 seconds"*** — there is no hands field (§6d #6, added below).
- It may print `journal has 1 entry; no event record; named deliverable absent`. **Those are
  facts.** *"This agent failed"* is not.

**This makes the instrument weaker and truer, and I would rather ship the true one.** Every block
in §4b was re-audited against Rule 2 after the red team landed; the one that failed it was
**deleted, not repaired**, because you cannot repair an inference with a field that does not
exist.

### 4d. Invocation — pull only

- **`swarm review`** — the verb. Human types it. That is the entire trigger surface.
- **Optionally** a thin `/org-review` skill that shells out to it, for conversational use.
- **Nothing else. No hook, no cadence, no offer, no watcher, no standing agent.**

**The offer is dead.** §5.

---

## 5. The offer: I recommended killing it, and here is the case

The brief asked me to design an evidence-warranted offer from the coordinator — *"your top layer
looks worth reviewing"* — and explicitly permitted me to **recommend dropping it if I could not
argue it out of nag-hood.** **I cannot. It dies. Five independent kills, any one sufficient:**

**1. The operator has already rejected it. In their own ledger.** VERIFIED,
`.swarm/journal/operator.md:23`:

> **"Rejected: overseer agent (nag reborn)."**

An agent that watches the swarm and tells the human about it **was proposed and refused by this
operator**. An offer that fires on evidence is an overseer with a politeness setting.

**2. It is the nag, and the nag's autopsy convicts it precisely.** VERIFIED, `SIMPLEST.md:177`:

> *"The reminder was tried and its own builder priced it: it carries **strictly less information
> than the ignored body**, is cleared by a command that proves nothing, and **its absence reads as
> compliance**."*

Test the offer against that: *"your top layer looks worth reviewing"* carries **strictly less
information** than the page it points at, and **its absence reads as compliance** ("no offer
fired, so I must be fine"). **Both failure modes, exactly.** The offer is the nag with a new
trigger.

**3. PHILOSOPHY §2's test settles it** (`docs/PHILOSOPHY.md:81-83`):

> *"before adding a guardrail, ask **who is incentivized to notice if it is missing.** If someone
> already is, the guardrail is **ceremony**."*

Who is incentivized to notice a bad top layer? **The human — it is their own work that degrades.**
Someone already is. **The offer is ceremony,** in the philosophy's own word.

**4. It violates the shipped contract on its face.** VERIFIED, `spawn_header` (`bin/swarm:804-806`),
which reaches **every agent at every depth**:

> *"The operator's span is theirs to declare and yours to protect: **never let the tree press more
> direct attention on the operator than they asked for.**"*

**The human did not ask for this attention.** An evidence-warranted offer is still the tree
pressing attention the human did not request.

**5. §9 — the operator's own first principle** (`docs/PHILOSOPHY.md:270-280`): *"I don't want it
polluted by you validating work that can be done by a subagent."* An unsolicited notice that an
agent has an opinion about the human's org is exactly that pollution, spending the scarcest
resource in the system.

**What replaces it costs nothing and is already legal:** *if a coordinator notices something, it
writes it in its journal.* World-readable. **Pull, not push.** The human looks when the human
wants to look — and now, with `swarm review`, looking is one command instead of an afternoon.

---

## 6. Graveyard check — is this the killed audit agent, or a metrics engine reborn?

I sent a prosecutor (`grave-org`) to kill this, with three sub-prosecutors, and told it a cleared
verdict it did not fight for was worthless. **It came back and convicted my deliverable.** Here is
its verdict, and here is exactly where I accept it and where I break with it.

**`docs/audit/org-review-graveyard-2026-07-12.md`:**

| the thing | its verdict | mine |
|---|---|---|
| periodic prompt | **KILLED. Dead three times.** | **Accept. Dead.** |
| the offer | **KILLED today, twice, on measured grounds** | **Accept. Dead.** (§5) |
| coordinator duty | CLEARED — *"the recommended form"* | **Reject** — the duty exists and is failing (§2b) |
| report artifact | CLEARED-CONDITIONAL | Accept as fallback |
| separate skill/command | **MUST-SATISFY** — the lawful form, *"cleared of the overseer kill (invoked ≠ standing)"* | **Accept — and I satisfy it below** |
| **the whole idea** | **MUST-SATISFY: §8's precondition is unmet — the human has never once reviewed their top layer by hand, and never said it hurt** | **This is the real fight. §6a.** |

### 6a. The §8 fight, and why I think the escape clause has fired

**My prosecutor's case, stated at full strength** (it deserves that): the human has never
performed a top-layer structure review by hand; a grep of the entire ledger and every brief for
*"too many agents | lost track | overwhelm | hard to manage"* returns **zero hits**; therefore the
pain is 100% hypothesized by agents on the human's behalf; therefore §8 forbids the tool. It also
found the deadliest line in the philosophy for me — §3, the operator's own dictation: **"There is
no reconciler role,"** and ASK #35's *"dedicated standing reconciler agent"* was **denied**.

**Where it is right, and I have changed the design because of it:** the offer dies, the cadence
dies, and **the instrument must hold no role.** `swarm review` is not an agent, not a watcher, not
a standing anything. **It is a command that prints and exits.** It cannot be a reconciler role
because it is not a role — it is a `cat` with a parent-chain walk. The reconciling is done by the
human, exactly as §3 demands; the verb just hands them the page. **That is the MUST-SATISFY,
satisfied.**

**Where I break with it — and this is my central argument:** my prosecutor read *"the convention"*
as **"the human reviewing their top layer."** I read it as **the convention the top layer actually
runs on** — warm-name-reuse, standing roles, the operator's own span rule. **And §8's escape
clause is not "has the human been doing the review." It is "does the record show the convention
failing."** VERBATIM: *"an engine never — **unless the record shows the convention failing**."*

**It is failing. Three times, with numbers, none of them disputed:**

1. **`updater-v2`** — warm-name-reuse (SPAN rung 0) **failed in the record**. A top-level agent the
   operator briefed, which never took a turn, **unnoticed for two days.** (§3.4)
2. **RED×25 / FORENSICS×34 / SCOUT×21, zero reuse** — the standing-role convention **failing at
   scale**, and the human said so themselves before any of us measured it: *"nothing remembers
   structural repetitions."* (§3.3)
3. **The gate decay, 17.4h → 3s, still collapsed today** — the human's review convention
   **measurably failing right now**, after being discovered *and named in prose* by the operator
   themselves. **Prose did not fix it.** (§3.5)

**That is the escape clause, fired three times.** And §8's ladder says what comes next when a
convention fails: not an engine — **a visibility verb.** Rung 2. The rung of `ps`. The rung of
`checkpoint --context`, which §8 itself blesses as *"still only a schema reference and a reader."*

### 6a′. And I do not have to argue §8 from first principles — SPAN.md already wrote this clause, and named the trigger

**This is the strongest thing in this document, and I found it only because my own prosecutor
quoted the bullet immediately above it and stopped two lines short.**

`SPAN.md:231-234` is the overseer kill my prosecutor used against me — *"a load-balancer/overseer
node: the nag reborn, structurally — a node whose job is other nodes' behavior."* **True, and I
accept it: it kills any standing org-reviewer agent, and this document proposes none.**

**The very next bullet, `SPAN.md:236-239`, pre-registers this instrument by name** (VERIFIED, I
read it):

> **"`ps` load metrics (child counts, task counters per node): NOT REJECTED — DEFERRED. `ps`
> already shows the tree and queue depths; span is visible by looking. **If the record shows
> parents failing the span test *because they cannot see it*, a derived count column is the
> instrument that earns its way in** (convention → instrument, in order)."**

Read what those two consecutive bullets do together. **The same document, in the same list,
kills the standing overseer and pre-clears the read-only view — and states the exact condition
that opens the second: *a span failure caused by not being able to see.*** That is not my
reading of §8. It is the repo's own operational restatement of §8, written by the doc that owns
span.

**And the condition is met, by the sharpest evidence in this file.** `updater-v2` (§3.4) is a
top-level agent the operator briefed, which **never took a turn**, and which **sat unnoticed for
two days**. Unnoticed *why*? Not through negligence — **because there is nothing to look at.**
`swarm ps` collapses ~100 dead agents onto a single comma-separated line and prints no per-agent
turn count, no entry count, no "this one never woke up." **The failure was invisible by
construction.** That is *"failing the span test because they cannot see it"* — SPAN's own words,
SPAN's own trigger, fired.

> **The honest limit of this argument, stated because §10 requires it:** SPAN licensed *"a
> derived count column"* on `ps`. **This document proposes seven blocks, which is more.** If a
> reviewer rules that the clearance covers only a count column and not a page, **the correct
> response is to narrow the page, not to widen the clearance** — and §2b's fallback (the report
> artifact, zero new verbs) is there for exactly that verdict. I asked the adversarial reviewer
> to rule on precisely this, and I will take the ruling.
>
> **The pre-committed narrowing, so the fallback is not improvised under fire.** If only a
> "derived count column" is cleared, the surviving instrument is **three lines on `ps`** — the
> three that name a *defect*, not a shape:
>
> ```
> hardener      [live] q=0 idle 15h   ⚠ waiting on field-tester (DEAD)
> updater-v2    [dead]                ⚠ never took a turn
> fp-compliance [dead] 8 children     ⚠ no synthesis, no artifact
> ```
>
> That is a count column with a warning flag, it is strictly inside SPAN's clearance, and **it
> still catches all three live defects this investigation found.** The other four blocks
> (recurrence, standing/ephemeral, mailbox, merge latency) are the *memory* half — they are what
> the operator asked for and what §3.3 argues they cannot build by hand, **but they are the half
> a strict reading of SPAN does not cover, and I will not pretend otherwise.**

### 6a‴′. And the FORWARDING-LAYER predicate is not my invention — SPAN wrote it

**VERIFIED, `SPAN.md:213-215`**, immediately after *"structure lying about work"*:

> *"(the **anti-forwarder test**: a coordinator's journal must show **artifact reads and
> verdicts, not relay logs**)."*

**SPAN specified the test. It exists as prose, it has never been run, and the one instance in
this repo's history went undetected until an agent stumbled over it — in my own subtree (§4b″).**
The `⚠ FORWARDING LAYER` block is that test, mechanized: *has children · journal has no entry
after its last spawn · named deliverable absent from disk.* **Rung 1 wrote the test; rung 2 runs
it. That is §8's ladder working exactly as designed, not a new concept.**

### 6a″. The precedent that cuts hardest AGAINST me, cited in full

**A graveyard check that only quotes the evidence in its favor is worthless, so here is the one
that hurts.** `PROXY-WIRING.md:296-321` (VERIFIED — and my prosecutor is right that I had not
cited it): a prior design proposed a **standing observer agent**. A red-teamer (`red-proxy`,
W6) caught it, and the published rewrite demotes it, **citing §8's standing bias by name**:

> *"(Rewritten after red-proxy W6: the first draft opened with 'one new standing agent',
> **asserted rather than argued**.) … The observer is a **duty, not (yet) an agent** … A standing
> `plane-observer` agent … is the **post-pilot option the numbers must earn**."*

**The repo has already published the correction to a proposal shaped like this one.** My answer,
and the reader should test it rather than accept it: **PROXY-WIRING's objection is to the
*standing* form specifically** — its stated reasons are that the observer *"answers no one,
delays no one, and its output is consumed only at stint time; **nothing reads it between stints
and nothing pushes**."* **Every one of those objections is an objection to a thing that exists
between invocations.** `swarm review` has **no pane, no journal, no mailbox, no tokens, no turn,
and no existence at all between the moments a human types it.** It is not a warm pane no
convention has earned; it is a `cat` with a parent-chain walk.

**If that distinction does not hold, this document is the corpse and should be killed.** I have
briefed the adversarial reviewer to try exactly that.

### 6a‴. The 'killed audit agent' in my brief is a phantom — and the real precedent is affirmative

My brief told me to check I was not resurrecting a killed `audit` agent. **There is none. NULL
RESULT** (`grave-org`, verified at source). The only one — `codex-audit` — was **closed on
harvest**, normal completion, and the operator's own ledger note is the *opposite* of a kill
(VERIFIED, `.swarm/journal/operator.md:86`):

> *"closed codex-audit on harvest — **re-audits are fresh spawns by design — audit independence**"*

**That is a shipped doctrine endorsing invoked, one-shot, read-only audits that die on report** —
which is the exact life-cycle of `swarm review`, minus the agent. It is the instrument's
strongest affirmative precedent, and it was hiding inside the charge against it.

**And on "the human never asked":** the human asked for *this*. The brief I was handed exists
because the operator said *"how is my top layer working, and how could it be better?"* More: they
named the exact gap, unprompted, before any agent measured it (`operator.md:45`) — *"nothing
remembers structural repetitions."* **`swarm review` is the memory.** My prosecutor could not see
that because it was grepping for complaint-words; the human did not complain, they **diagnosed**.

### 6b. Is it a metrics engine reborn?

**No, and the test is mechanical.** `DECISIONS.md` §1e killed the scored engine with a Goodhart
argument I accept completely:

> *"An engine trained on 'operator approves 95% of X' learns a policy whose validity depends on
> the reading it would remove. **Delegate the verdict on the strength of that statistic and the
> statistic decays underneath you.**"*

And `PHILOSOPHY §10`: *"if you cannot prove the number is yours, do not print a number."*

**`swarm review` prints no score, no index, no rating, no percentage of anything.** There is
nothing to optimize, therefore nothing to Goodhart. Every number on the page is a **count of a
file fact** with the file named — *25 agents, 3 entries, 17.4h, 0 senders below depth 1* — and
every one is re-derivable by the human in one command. **The moment it prints "your top layer
health: 73%", it has become the thing `DECISIONS.md` killed, and §4c's predicate rule is the
tripwire that stops it.**

**Is it the killed `audit` agent?** No — and the distinction is the one my own prosecutor drew:
**invoked ≠ standing.** The killed thing was an *agent* that watches. This is a *command* that
runs when a human types it and then exits. It has no journal, no mailbox, no pane, no turn, no
opinion, and no existence between invocations.

### 6c. What SELF-AUDIT / REVIEW / WATCHLIST are (they are not this)

`grave-priorart` checked, because the names are suspiciously close. **They are all about the
tool's own design** (the SIMPLEST rewrite), not the operator's top layer. **No shipped surface
references any of them.** WATCHLIST.md is the closest in *genre* — evidence-triggered,
advisory, human-decides, `WATCH / CHECK / TRIGGER / SIMPLEST FIX` — and its house rule is one I
have followed here: *"check on evidence, not on schedule."* **It is the right form for a design
ledger and the wrong form for this**, because a WATCHLIST entry is a thing a human reads *once*,
and `swarm review` is a thing that must be **current every time it runs.**

---

## 6c′. The reviewer's counter-proposal — tested, and it is not sufficient. *(The one finding I refuse, with the evidence.)*

**`org-red` recommends shipping a `ps` count column instead of the verb**, on this reasoning:

> *"Ship the `ps` column, not the verb: a per-agent entry/turn count, and stop collapsing the dead
> onto one line. **That single change catches `updater-v2`, which is your entire fired trigger.**
> Zero verbs, zero concepts, no WATCHLIST breach."*

**The proposal is good and I adopt half of it (below). But its load-bearing claim is false, and I
tested it rather than argue it. MEASURED:**

```
updater-v2       entries=1  children=0    ← a count column prints "1". CAUGHT.
fp-compliance    entries=3  children=4    ← a count column prints "3". LOOKS NORMAL.
```

**`updater-v2` is not "my entire fired trigger." There are two live defects, and the column
catches one.** `fp-compliance` has **three journal entries** — a count column shows `3` and
**nothing looks wrong.** Its defect is *"has children · wrote no synthesis · **its named
deliverable does not exist on disk**"* — and **`ps` cannot see that, because `ps` does not read
`docs/`.** `ps` reads `.swarm/`. **The missing artifact is the entire defect, and it lies outside
`ps`'s world.**

**And this is not a corner case — it is `SPAN.md`'s own test, the one it wrote and never ran**
(`SPAN.md:213-215`): *"the **anti-forwarder test**: a coordinator's journal must show **artifact
reads and verdicts**, not relay logs."* **The anti-forwarder test cannot be run from `ps`** — it
requires joining a journal to an artifact, and `ps` has no artifact half. **The counter-proposal
cannot execute the doctrine it claims to satisfy.**

**What I adopt from it, because it is right and free:**
1. **Add the per-agent entry count and stop collapsing the dead onto one line in `ps`.** This is
   strictly good, costs nothing, and is *exactly* what SPAN pre-cleared. **Recommend it
   regardless of what happens to the verb.**
2. **It genuinely narrows the case for the other four blocks** (recurrence, standing/ephemeral,
   mailbox, gate latency). Those are the *memory* half — what the operator asked for — but they
   are **not** what SPAN pre-cleared, and I say so in §6a′. **If the operator wants only what the
   evidence has strictly earned, they should take the `ps` column plus the artifact-join, and
   leave the memory blocks unbuilt until they ask for them a second time.** That is a legitimate
   reading of this document and I will not argue against it.

## 6c″. The WATCHLIST trigger that fired — the responsive answer W1 demanded

**The reviewer's charge is fair: `WATCHLIST.md` §7 asks *"which WATCHLIST entry's trigger fired?"*
and my first draft answered with a PHILOSOPHY §8 citation. That is not responsive.** Here is the
responsive answer.

**`WATCHLIST.md` §4 — "Journals rot into mush" — FIRED.** VERIFIED, its own text:

> **WATCH:** *"whether parents actually **read child journals**…"*
> **TRIGGER:** *"**parents demonstrably not reading journals** (allowed-and-never-used — the F3
> test inverted)…"*

**`fp-compliance` is that trigger, precisely:** a parent that briefed **8 descendants**, and
**demonstrably never read or synthesized their work** — it died mid-plan with its deliverable
unwritten (§4b″).

**And I am the second instance, which is why I believe it.** I did not read my own subtree's
journals closely enough to notice; I inferred the problem from `ps`'s *shape* and got the right
answer from the wrong signal. **Two parents, one day, both failing WATCHLIST §4's watch — and
neither caught by anything but luck.**

## 6d. What this instrument can NEVER show — the record's five holes

**MEASURED** (`shape-forensics` §5, verified at source). The evidence base is **8 agent fields +
3 event fields, and that is all.** A design document that hides what its own evidence cannot see
is worthless, so:

1. **THE RECORD HAS NO DEATH.** `is_dead` is computed **at read time from herdr pane liveness**
   (`bin/swarm:514`). **A deliberate `swarm close` and a crashed pane are byte-identical in the
   files.** A restarted herdr would resurrect the entire graveyard. → **Every lifetime number in
   this document is a *proxy* (spawn `ts` → last Stop hook), not a fact.** The page must label
   them as such and must never claim an agent "was closed."
2. **THE RECORD HAS NO COST.** No tokens, no dollars, no turn count. `fleet-eval` ran a **paid**
   benchmark under a dollar cap and **the files do not know what it spent.** → **The instrument
   can never tell the operator what their org costs.** That is the question they will most want
   answered, and the honest answer is *"not from these files."*
3. **THE RECORD HAS NO VERDICT.** *"The single most important fact about any agent — did its
   parent accept its work? — is nowhere in the files."* And this is **the contract, not an
   oversight**: WORLD concept 8 says *judge artifacts, never claims*, and `delivered/` is
   designed to record that bytes reached a turn **and nothing else.** → **`swarm review` shows
   SHAPE. It can never show QUALITY.** It cannot tell you whether an agent was any *good*, and
   it must never imply it can. **This is the deepest bound on the instrument and it is
   permanent.**
4. **THE RECORD IS BLIND TO HARNESS SUBAGENTS.** SPAN §3d′ says agents *prefer* rung 2 (in-session
   Task subagents) over swarm children — and those have **no name, no pane, no journal.** →
   **`ps` systematically under-counts delegation, and every "zero children ⇒ did not delegate"
   inference is unsound**, including the one in §6e below and including the sibling's flat-tree
   finding. **This is the largest hole in the evidence base and it cannot be closed from
   `.swarm/`.**
5. **NOTHING LINKS AN AGENT TO ITS ARTIFACT.** Nothing connects `structure-scout` to
   `STRUCTURE.md`. Every such link in this investigation was recovered **by reading prose.**
6. **THE RECORD HAS NO *HUMAN*.** *(Added after the red team; it is the hole I fell into.)* There
   is **no channel anywhere in these files that measures the human's own attention.** The mailbox
   `delivered/` ctime measures **a Claude session's** pickup (§3.6). The GitHub `mergedBy` field
   measures **an account**, which agents drive under standing pre-authorization (§3.5). The
   operator ledger is written by **an agent** and carries **no clocks** (§3.6). **Three plausible
   human-attention signals; all three are proxies for something else.** → **The instrument must
   never claim to measure the human.** It measures *the account*, *the session*, *the file* — and
   it must say which, every time (§4c′, Rule 2).

> **The one-sentence summary, which I adopt verbatim from `shape-forensics` because it is the
> truest thing written about this evidence base:**
>
> ***`.swarm/` is an excellent record of WHAT WAS SAID, a poor record of WHAT WAS DONE, and
> contains no record at all of WHAT WAS DECIDED NOT TO DO.***
>
> **For a review of *structure*, that last is the deepest gap: the shape is visible; the judgment
> that made it is not.** No instrument can close it. The operator should read every line of
> `swarm review` knowing that it shows the *residue* of their decisions, never the decisions.

## 6e. Two findings that are not mine to act on, surfaced because the operator should see them

**(a) The flat-tree claim is NOT SUPPORTED on the live record — qualified.**
`OPERATOR-STRUCTURE.md:24` states the bug as *"the operator does swarm-internal work itself — it
spawns **workers** directly."* **MEASURED:** **12 of 25 top-level agents delegated.** Of the 13
with zero children, **10 finished in under 25 minutes** — a 7-minute single-question scout has
nothing to delegate. The only long-lived zero-child agents are `hardener` and `updater`, which
are **serial by design**. **NULL: no top-level agent ground serially through parallelizable work
when it should have delegated.**
**But hole #4 above cuts directly against this**, and I will not overclaim: harness subagents are
invisible to `ps`, so *"zero children"* does not mean *"did not delegate."* **I report this as a
qualified null that the sibling's authors should weigh, not as a refutation.**

**(b) The falsifier discipline WORKS — and the finding is that its last act is structurally
unowned.**

> **CORRECTION, and it is against myself.** An earlier draft of this section said *"the ritual
> orphans its own falsifier; compliance is self-reported, defection is self-concealing"* — on a
> child's preliminary reasoning that I wrote into this document **before it was measured.** It
> was **wrong**, the child refuted itself, and PHILOSOPHY §10 requires I say so here rather than
> quietly swap the text. **A child's *finding* earns the same scrutiny as a child's *tree*, and
> I gave the tree more.**

**MEASURED** (`falsifier-probe`: **135 falsifier statements hand-read**, rubric pre-registered
*before* reading, four independent readers, both tallies reconciling exactly):

| | |
|---|---|
| unfalsifiable-as-written ("if I'm off base…") | **0 of 135** |
| **name a witness the agent CANNOT FORGE** (an mtime, a queue file, a test exit code) | **105 of 135** |
| **FIRED → CHANGED COURSE** | **17** |
| **FIRED → IGNORED** | **0** |

**The agents write real, checkable falsifiers, and they honor them.** VERIFIED — I read the
instance myself rather than trust the report. `.swarm/journal/opencode-plugin-scout.md:429` names
a falsifier about `messages.transform` persistence; **`:435` is the very next entry header:**

> *"**MY OWN FALSIFIER FIRED.** `messages.transform` is a VIEW transform, not a session write.
> Option (c) is DEAD as stated. … I named the falsifier at 18:05 and immediately tested it,
> because it was cheap and it was load-bearing. IT FIRED. This is the most important NEGATIVE
> result of the whole investigation and **it corrects MY OWN preferred design**, not a child's."*

Named → tested → fired → course changed → recorded, by a live sibling, today.

**The real finding, which is sharper than the false one it replaces:**

> **93 of 103 journals name their LAST falsifier in their LAST ENTRY, and then stop writing.**
> The falsifier is **not ignored — it is orphaned by the ritual's own shape.** There is no
> "next" in which to defect.

**⇒ `falsifier-not-honored` is UNDEFINED, not hidden.** An instrument cannot detect a
course-change that had no subsequent course, and **this is the one pathology in my brief that no
instrument can ever collect.** It is not an agent failure to be tooled away: it is a **structural
consequence of *"journal before going idle"* + *"a reconciliation names its falsifier"* — the
doctrine's last act generates an unowned claim, by construction.**

**This is out of my scope** (my brief forbids touching in-swarm doctrine) **and I do not propose
a change.** But if anything in this review earns a *doctrine* change rather than an instrument,
it is this, and it should be someone's brief.

---

## 7. Falsifiers, with collectors

Each is a file fact, checkable by anyone, with the observation that would show the design is
wrong.

**F1 — THE ONE THAT DECIDES IT. *The verb is run, and then it is not run.***
> The instrument earns its place only if the human uses it more than twice.
- **Collector:** shell history / the operator ledger. Count invocations of `swarm review` in the
  30 days after it ships.
- **FALSIFIED WHEN:** it is run once (at ship) and then **never again**. That is the
  confirm-but-never-read decay, applied to my own instrument — and it would mean the human never
  wanted the page, they wanted the *conversation*, and I built the wrong thing. **Kill the verb
  and say so.**
- *This is the falsifier I most expect to fire, and I want it named first.*

**F2 — *The page produces no decision.***
> A reader that changes nothing is a reader nobody needed.
- **Collector:** the operator ledger. After each `swarm review`, is there an entry within the same
  day naming a top-layer change (a close, a rename, a standing role declared, a re-brief)?
- **FALSIFIED WHEN:** three consecutive invocations produce **zero** top-layer decisions. The page
  is decoration.

**F3 — *It grows an opinion.***
> The moment it scores, it is the engine `DECISIONS.md` killed.
- **Collector:** `grep -E 'score|health|rating|%|should|recommend|suggest' <the verb's output>`.
- **FALSIFIED WHEN:** any hit. **One hit is the trigger** — §4c's predicate rule has been broken,
  and the instrument has crossed the line it exists to stay behind.

**F4 — *Session latency is presented as human latency.***
> The trap of §3.6, which nearly produced a false headline.
- **Collector:** read the verb's mailbox block. Does any line imply the *human* read/claimed mail
  at a given time?
- **FALSIFIED WHEN:** it does. Only the **GitHub merge latency** measures the human. `delivered/`
  ctime measures **a Claude session**, and conflating them slanders the operator with their own
  tooling's promptness.

**F5 — *The offer comes back.***
- **Collector:** `grep -ri 'top layer\|review your' skill/ bin/swarm`.
- **FALSIFIED WHEN:** any unsolicited surfacing of this ships. §5 named five kills; the first
  reviewer to re-propose it must answer all five.

**F6 — *The classifications rot.***
> "Standing" and "ephemeral" are predicates, not opinions — but only if they stay mechanical.
- **Collector:** re-derive one row of each block by hand from the cited file.
- **FALSIFIED WHEN:** a printed classification cannot be reproduced from its own citation. Then
  §4c has failed and the verb is asserting, not reading.

---

## 8. Cost — honest

| item | cost |
|---|---|
| `swarm review` verb | **~120–160 lines** of Python in `bin/swarm`: a parent-chain walk, a journal `##` counter, a brief-text classifier for recurrence, a `gh` call. All of it is code I **already wrote as throwaway probes for §3** — the collectors in this document are the implementation. |
| new concepts in WORLD | **ZERO.** It reads existing files. No new state, no new field, no new verb semantics beyond "one more read-only view." |
| new state stored | **ZERO.** Nothing is written. |
| the `/org-review` skill wrapper (optional) | ~20 lines. |
| **new concept count** | **+1 verb** (`review`), joining `spawn/send/ps/close/world`. **This is the real price, and it is not nothing** — SIMPLEST fought to five verbs and WATCHLIST §7's trigger is *"any addition that cannot point to a WATCHLIST entry whose trigger fired."* **My answer to that trigger is §6a: the convention is failing on the record, three times.** If the operator does not accept that argument, **the honest fallback is the report artifact (§2b) — zero new verbs, an agent generates the page on request.** |
| ongoing | **Zero.** It has no cadence, no watcher, no agent, no turn. It does not exist between invocations. |

**The one dependency worth naming:** the merge-latency block needs the **GitHub API** (`gh`).
Without network it degrades to printing the block as unavailable — it must never guess, and it
must never fall back to the ledger's timestamps, which do not exist (§3.6).

---

## 9. What I would ship

### 9.1 SHIP THIS. The `ps` fix. *(The recommendation. Not a fallback.)*

**Three lines of change, zero new verbs, zero new concepts, zero new invocation surface.**

- **Un-collapse the dead line.** `bin/swarm:574` renders all 124 dead agents as
  `dead: name, name, name…` — **names only.** `updater-v2` is the **114th name**, between
  `switch-scout` and `v3-red`. **A stillborn agent and one that shipped forty artifacts are
  byte-identical in that line.**
- **Print a per-agent turn count** (from `event/<name>.json`) **and entry count** (from the
  journal's `##` headers).
- **That alone surfaces `updater-v2`**: an agent with 1 entry and 0 turns becomes visible **the
  moment anyone runs the command they already run.**

**Why this is the answer and not the consolation prize** — and I am quoting my own adversarial
reviewer, who argued me out of my own verb:

> *"The `ps` fix is **not a narrower version of your instrument. It is the instrument SPAN
> pre-registered, for the exact failure that fired, at the exact rung §8 licenses.**"*

**And the argument that turned my own evidence against my own recommendation:** §2c is my citation
that **skills do not reliably auto-fire** — I used it to argue for a *verb* over a *skill*. **The
same measurement argues against a new invocation surface entirely.** F1 — the falsifier I named as
the one I most expect to fire (*"the human runs it once and never again"*) — **is answered not by
a better verb, but by putting the fact where the eye already goes.** *No new thing to remember
exists.* **I was one step short of my own conclusion, and the reviewer took it.**

### 9.2 THEN THIS, IF YOU WANT THE OTHER DEFECT: the artifact-join

**`ps` cannot do this, structurally: `ps` reads `.swarm/`; the defect lives in `docs/`.**

`SPAN.md:213` wrote the test and **never ran it**: *"the **anti-forwarder test**: a coordinator's
journal must show **artifact reads and verdicts**, not relay logs."* Running it means asking: *does
this agent's named deliverable exist on disk?* **`fp-compliance` — 4 children, 3 journal entries,
deliverable absent — is invisible to any count column** (a count column prints `3` and looks
normal), and it is the second of the two live defects this investigation found. **Rung 1 wrote the
test; this is rung 2 running it.**

### 9.3 AND ONLY IF YOU WANT IT: the memory blocks

Recurrence · standing-vs-ephemeral · mailbox census · gate latency. **This is what you actually
asked for** — *"how is my top layer working"* — and §3.3 argues you cannot build it by hand across
115 agents and 124 tombstones.

**But I will not pretend the record earned it.** SPAN pre-cleared *a derived count column*, not a
seven-block page (§6a′). These blocks carry the **entire** F1 adoption risk, because they are the
part that needs a surface you must remember to invoke. **Take them because you want them, not
because this document proved you need them.**

### 9.4 What is NOT recommended, in any variant

**No offer** (§5, killed five ways). **No cadence.** **No standing agent.** **No executor.** **No
score, ever** (§4c). **No doctrine change** — the briefed sentence is rung 1 applied to a rung-1
failure, and `skill/SKILL.md:44-49` already carries the span duty and **did not prevent
`updater-v2`.** As the reviewer put it: ***"the reason a briefed sentence failed is that nothing
renders the fact. Render the fact."***

**And one thing that is not mine to ship but belongs on the operator's desk:** `updater-v2` is a
role you briefed on 07-10 and never got. That is a live gap in your top layer today, and it was
found by reading files. **That single fact is the whole argument for this document.**

**Two defects are live on your tree right now. Both were found by reading files; neither is
visible in `ps`; and both rest on positive file facts, not on liveness inferences (§4c′):**

1. **`updater-v2`** — a standing role you briefed on 07-10 that **never took a turn** (journal: 1
   entry; no event record), unnoticed for two days. You tried to re-brief the warm `updater` name;
   the tool forbids name reuse; the workaround was stillborn.
2. **`fp-compliance`** — a forwarding middle layer: **4 children, 3 journal entries, named
   deliverable absent from disk.** It is `SPAN.md:213`'s *"structure lying about work"* — a test
   the doctrine wrote and never ran. **It was in my own subtree, and I report it against myself**
   (§4b″).

**A third — `hardener` "blocked on a dead agent" — was my flagship example and it was FALSE. The
red team killed it and I have retracted it (§4b′).** Its retraction taught this document more than
its truth would have, and it is the reason §4c′ exists.

**The sentence, if only one survives:** *your top layer is not sick — the collectors mostly come
back null — but it has no memory: you have paid to re-invent the red team twenty-five times, a
standing agent you briefed never took a turn and sat unnoticed for two days, a middle layer in my
own subtree briefed eight children and wrote nothing, and your review gate has fallen from
seventeen hours to three seconds while you watched and said so; none of that is a judgment, all of
it is in your files, and the instrument's only job is to show it to you — accurately, in the
files' own terms, claiming nothing they do not witness — and get out of the way.*

---

## 10. Artifacts (the evidence base, for re-reading and re-running)

| doc | what it establishes |
|---|---|
| `docs/audit/org-review-ledger-2026-07-12.md` | the mailbox census, the F-SPAN null, the GitHub-API decay re-measurement, and the ledger's fatal limits (§3.6) |
| `docs/audit/org-review-shape-2026-07-12.md` | the top-level census, the standing/ephemeral split, `updater-v2` |
| `docs/audit/org-review-roles-2026-07-12.md` | the recurrence counts (RED×25, FORENSICS×34, SCOUT×21, zero reuse) |
| `docs/audit/org-review-graveyard-2026-07-12.md` | the prosecution: what is dead, what is cleared, and the §8 charge I answer in §6a |
| `docs/audit/org-review-phil8-2026-07-12.md` | the §8 case against this document, at full strength |
| `docs/audit/org-review-priorart-2026-07-12.md` | why SELF-AUDIT / REVIEW / WATCHLIST are not this |
| `.swarm/journal/org-review-scout.md` | my own record, including the two hypotheses I killed |

**Composition with the sibling:** `OPERATOR-STRUCTURE.md` defines *what the top layer is* (the
operator is outside the swarm; its job is to stand up agents that own the work). **This document
does not redefine it and does not touch it.** It answers the next question: *given that layer, what
have you actually built, and how would you know?* One correction is owed to that document: its
`deep` anecdote (an unregistered agent mailing the human six times) **is not in this tree** — the
live record shows **0 of 61** messages from below the top layer, and 0 unregistered senders (§3.1).
