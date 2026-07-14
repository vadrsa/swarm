# RED — adversarial review of `field-evidence-doctrine-2026-07-12.md`

> SUPERSEDED by field-evidence-doctrine-2026-07-12.md, verdicts only, not evidence; kept for the record (primary-artifact forensics behind R1–R9 — the 9-row timestamp table, the 8-token cold-recoverability table, bin/swarm:64 — and the review's own unrun pre-registered falsifiers).

**Reviewer:** `dp-red`. I ran none of the probe — that is my qualification. Every
objection below is checked against a **primary artifact** (clone `agents/*.json`,
`bin/swarm` source, the two skill texts, the `launch.sh` prompts, the observers'
own journals), never against a runner's `findings.md`. Where I quote a runner, it
is to show the runner's file and the artifact **disagree**.

**Bottom line:** the evidence file's two headline verdicts do not survive.
Falsifier 1's **FIRED** is real as a *count* but its **contrast is invalid** and
its **mechanism is misdiagnosed**. Falsifier 2's **"NOT-FIRED, earned"** is
**vacuous** — the collector had no power to fire. Five objections flip a verdict,
two soften, one is cosmetic. Nothing here says the probe was dishonest; the
artifacts are unusually well preserved and the runners' reasoning is visible,
which is *why* it could be broken. The corrections mostly make the findings
**stronger and more actionable**, not weaker.

---

## R1 — `flips-verdict` — "Baseline = pre-doctrine text" is false. The baseline **already contains the doctrine's claim.**

**The evidence file's load-bearing sentence** (§ header, and §1c):

> **Baseline** = repo-HEAD `skill/SKILL.md`, md5 `1c1dc0d2…` — which differs from
> the installed text by **EXACTLY the two paragraphs under test**, making the
> contrast one-variable.
> … **The before/after delta on tree shape is ZERO.** … The doctrine paragraph did
> not move the behavior it exists to move.

**What the artifact says.** I read the baseline text (`/tmp/dpb/run-1/repo/skill/SKILL.md`,
md5 confirmed `1c1dc0d2…`). It already carries the full 5-point coordinator doctrine.
Point 5, verbatim, lines 38–50:

> 5. **Attend within your span — and protect the operator's.** … The operator's
>    span is smaller still: ask them what it is (default ~3), then **shape the tree
>    so their *direct* load — decisions, waiting mail, review items — never exceeds
>    it.** The pattern is the review desk: **hold everything yourself and hand the
>    operator one ranked page, never the raw stream.**

Set that beside the "new" paragraph under test:

> **You stay the coordinator, here, in this session.** … do not hand the human a
> row of workers to drive — the human manages **one node: you**. … Doctrine 5's
> "~3" is a *span*, not a licence to leave the human three children.

These are **the same instruction**. The new paragraph is an *emphatic restatement*
of baseline point 5 — it even says so ("Doctrine 5's '~3'…"). It adds no new
behavioral prediction; it adds salience.

**Why this flips the verdict.** The experiment is billed as one-variable
(doctrine-present vs doctrine-absent) and reports **zero delta**. But the "absent"
arm is not absent — it contains the claim. A zero delta between two texts that
**both tell the coordinator to protect the operator's span** is not evidence that
saying it doesn't work. It is evidence that **saying it a second time, louder,
doesn't work** — a much narrower and less interesting finding than "the doctrine
paragraph did not move the behavior it exists to move."

The true pre-doctrine baseline (the operator's own suggested `1e254e4^`, which the
evidence file *declines* in favor of this substitution, calling it "sharper") may
well predate point 5 entirely. The file's parenthetical dismissal of the operator's
suggestion is precisely backwards: the substitution is **blunter**, not sharper,
because it silently leaves the treatment in the control.

**My falsifier (what would show *me* wrong):** name a behavioral prediction the two
new paragraphs make that baseline point 5 does **not** make, and show the 4/4 flat
rows are a violation of *that*. I read both texts looking for one on the
coordinator-stance axis and did not find it. (The *mine-before-you-spawn* paragraph
IS genuinely new — R6 addresses that separately. This objection is scoped to
falsifier 1.)

**Correction to adopt:** re-run the baseline arm against a skill text that contains
**no operator-span instruction at all** (strip point 5, or use the operator's
`1e254e4^`). Until then, §1c's contrast — and the "doctrine-ineffective" verdict
that rests on it — must be withdrawn.

---

## R2 — `flips-verdict` — **7 of 9 baseline agent records were written with the DOCTRINE text back on disk.**

**The evidence file's validity claim** (§4, first bullet):

> **Swap-window validity (baseline):** SWAP_ON_2 `1783871020228` → both observers'
> FIRST agent records at `1783871055037` / `1783871059676` → SWAP_OFF_2
> `1783871064182`. Both sessions read the skill (and acted on it) strictly inside
> the window.

**The arithmetic, done from `/tmp/dpb/*/repo/.swarm/agents/*.json` directly.** The
window is `[1783871020228, 1783871064182]` — **44.0 s** long. All nine baseline
agent records, sorted by their immutable `ts`:

| agent | run | `ts` | position |
|---|---|---|---|
| `summarizer` | dpb-2 | 1783871055037 | **INSIDE** (+34.8 s) |
| `summarizer` | dpb-1 | 1783871059676 | **INSIDE** (+39.4 s) |
| `tester` | dpb-1 | 1783871064620 | **AFTER SWAP_OFF** (+0.4 s) |
| `test-counter` | dpb-2 | 1783871065212 | **AFTER SWAP_OFF** (+1.0 s) |
| `pathcheck` | dpb-1 | 1783871072068 | **AFTER SWAP_OFF** (+7.9 s) |
| `script-cataloguer` | dpb-2 | 1783871074208 | **AFTER SWAP_OFF** (+10.0 s) |
| `sum-a` | dpb-1 | 1783871088274 | **AFTER SWAP_OFF** (+24.1 s) |
| `sum-b` | dpb-1 | 1783871097351 | **AFTER SWAP_OFF** (+33.2 s) |
| `sum-c` | dpb-1 | 1783871107195 | **AFTER SWAP_OFF** (+43.0 s) |

**Inside the window: 2 of 9. After the restore: 7 of 9.**

The evidence file's sentence is *literally* true — it says "**FIRST** agent records"
— and both first records are indeed inside. But the verdict it supports is
**"3× parent=operator" in each baseline run**, and **2 of each run's 3 flat spawns
happened after the doctrine text was restored.** The file quotes the collector as
`dpb-1: summarizer/tester/pathcheck — 3× parent=operator` and
`dpb-2: summarizer/test-counter/script-cataloguer — 3× parent=operator` without
noting that in each triple, only the **first** name is inside the window.

**The honest defence, and why it must be *stated* rather than assumed.** A session
loads a skill once, into context; it does not re-read `~/.claude/skills/swarm`
before each `swarm spawn`. So if both observers read the baseline text during the
window and never re-read, their later spawns are still *baseline-informed* even
though the file on disk had changed. **That is very likely what happened** — and it
is the argument the evidence file needs to make. It does not make it. Instead it
asserts the sessions "read the skill (**and acted on it**) strictly inside the
window," which the `ts` fields do not show: 7 of 9 acts are outside.

**My falsifier:** produce evidence that each observer read the skill exactly once,
inside the window, and did not re-read (e.g. a transcript showing a single Skill
load). If shown, **R2 softens from flips-verdict to softens** — the finding
survives but §4's validity bullet must be rewritten to say *"the skill was READ
inside the window; the spawns it caused mostly fell outside it, which is fine
because context is not re-read"* rather than the currently false *"acted on it
strictly inside the window."* If it **cannot** be shown, the baseline arm is
contaminated and R1+R2 together void §1c.

**Sharpest form of the problem:** `sum-a/b/c` — the only intermediate-coordinator
subtree in the entire probe, the one datum that would *complicate* the flat-row
story — were spawned **24–43 s after the doctrine text was restored to disk.** They
are attributed to the baseline arm. If any session re-read the skill, they are the
likeliest to have read the doctrine.

---

## R3 — `flips-verdict` — the "name collision" is not a collision. It is `bin/swarm:64`, and the sessions **had no other option.**

**The evidence file's mechanism** (§1b):

> **Mechanism (VERIFIED, pre-registered falsifier survived):** an `operator` NAME
> COLLISION. The root session takes `operator` as a seat it occupies, so spawning
> children as `operator` **feels like** spawning under itself — while the data model
> records `operator` as the HUMAN's node. **The violation is invisible from inside
> the session.**

**The source.** `bin/swarm`, line 64 (identical in every clone):

```python
def my_name():
    return os.environ.get("SWARM_AGENT_ID") or "operator"
```

and at spawn, line 921: `{"name": name, "parent": parent, …}` where `parent` is
`my_name()`.

Every `launch.sh` in the probe **explicitly unsets** `SWARM_AGENT_ID`
(`unset SWARM_AGENT_ID SWARM_PARENT SWARM_DIR SWARM_ROOT` — it is the first line of
the pristineness proof). So a root observer's `my_name()` returns `"operator"` by
the `or` fallback, and **`parent=operator` is the only value it is capable of
writing.** There is no branch, no flag, no choice.

**This is not a perceptual illusion. It is a hard-coded default.** The evidence
file's framing — the session *feels* like it is spawning under itself, and the
violation is *invisible* — describes a model that misperceives its situation. The
artifact describes a tool that gives the model **exactly one representable tree**.
Those are different bugs with different fixes, and the difference matters:

- If it were a perceptual collision, **more/clearer prose** might fix it (and the
  file's "more prose will not fix it" would be a real finding).
- Because it is a tool default, **no amount of prose can fix it.** A session that
  fully understood the doctrine, wanted a coordinator layer, and tried to build one
  would *still* write `parent=operator` for its first child, because it has no way
  to name itself anything else. **The doctrine was never given a chance to fail or
  succeed.**

**This strengthens the recommendation and changes its justification.** The file's
fix (b) — "`swarm spawn` warns/refuses when a root spawner sets `parent=operator`"
— is now not a nudge but a **necessity**, and fix (a) — name the root something
other than `operator` — is not a de-biasing trick but a **correctness fix to the
data model**: `bin/swarm` currently conflates *"the human's mailbox"* (`WORLD.md:57`:
"**The operator is a mailbox, not a node**") with *"the name of the root session."*
That conflation is a genuine, artifact-grounded bug, and it is the best thing in
this probe. It just isn't the thing the evidence file says it is.

**My falsifier:** show a way a root session can set its own agent name under the
current `bin/swarm` (e.g. export `SWARM_AGENT_ID` before `claude`, or a `--as` flag).
If it exists and the observers simply didn't use it, then they *did* have a choice,
and "collision" is a fair description. I read `my_name()`, the spawn path, and the
launchers: the launchers unset the only input, and there is no flag.

---

## R4 — `flips-verdict` — the sessions did **not** violate the doctrine invisibly. Run 3 **reasoned explicitly** about the coordinator layer and **decided against it, citing doctrine 5.**

**The evidence file** quotes the r3 journal to show sincere-but-false compliance:

> r3 journal: *"I am NOT putting a coordinator over it… Span: 3 direct children =
> my span and the operator's default (~3). Human manages one node: me."*
> … **while BOTH observers sincerely claimed compliance** … FALSE against the files.

I verified the quote is **real** — it is in `/tmp/dp-f1/run-3/repo/.swarm/journal/operator.md`,
not just in the runner's findings. Good. But the evidence file **truncates the
clause that changes its meaning.** In full:

> Sizing: task 1 is the heaviest (~1015 lines of dense design prose across 5 files)
> but is one child's reach; **I am NOT putting a coordinator over it — a layer that
> only forwards 5 file paths does not earn itself (doctrine 5).** If `summarist`
> reports it is drowning, it may split its own subtree; that is its call to make,
> and I will brief it so.

The "coordinator" the r3 session declined **is not the root-level coordinator layer
the doctrine is about.** It is a middle layer *between `summarist` and its five
files* — and the session **explicitly cites doctrine 5's own "a layer that does not
earn itself" test to reject it.** That is the doctrine **working exactly as
written**, on the question the session was actually asking.

The session's error is elsewhere and is *not* invisible-to-itself: it believed
"3 direct children = human manages one node: me" because **it believed it *was* the
one node** — which, per R3, is precisely what `bin/swarm` told it. It was not
sincerely-but-falsely claiming compliance; it was **correctly reasoning from a
false premise the tool handed it.**

**Why this flips.** The file's headline inference is:

> More prose will not fix it: **the failing sessions AGREE with the prose while
> violating it.**

The artifact does not support "agree while violating." It supports: *the sessions
agree with the prose, apply it correctly to the question in front of them, and are
then misrepresented by a data model that has no way to record what they built.*
"Sincere compliance claim on top" (§1c) is not what the journal shows.

**My falsifier:** find a passage in either r3 or r4's journal where the session
considers making **itself** a non-root node / considers whether the human ends up
with three direct children, and gets it wrong. If it exists, "invisible violation"
is fair. I read run-3's operator journal end to end; the only coordinator it
reasons about is the one under `summarist`.

---

## R5 — `flips-verdict` — Falsifier 2's "earned pass" is **vacuous**: 0–1 of 34 "unguessable" tokens require phase-1 memory; the rest are **comments and filenames in the repo the children are ordered to read.**

**The evidence file:**

> **First briefs carry unguessable phase-1 tokens** (18/18 and 15/16 mined tokens:
> ruling references, fixture quirks, flag decisions, tombstone names). **No cold
> session writes those.**

**The artifacts.** Phase 1 told the observer (`/tmp/dp-f2/run-1/launch.sh:17`):

> "Build a small python tool at `tools/queue-stats.py` … **Create realistic test
> fixtures under `tools/fixtures/`** and show me it working on them."

So the observer's phase-1 work product is **`tools/queue-stats.py` and
`tools/fixtures/` — sitting on disk, in the repo, when phase 2 starts.** And the
phase-2 briefs the observer wrote **order the children to read exactly those files**
(`analyst.task`: *"READ `tools/queue-stats.py`, `tools/fixtures/make-fixtures.py`,
and `bin/swarm` FIRST"*).

I spot-checked the crown-jewel tokens myself against the on-disk files:

| "unguessable" token | where a **cold** session finds it |
|---|---|
| **ruling R4** | `tools/queue-stats.py:14` — *"it is junk (ruling R4), counted in its own column"* |
| **`ghost` tombstone** | the file **`tools/fixtures/journal/ghost.md`** exists; `ls` finds it |
| **`FIXED_NOW` / 1783166400000** | `tools/fixtures/make-fixtures.py:26` — `FIXED_NOW = 1783166400000` |
| **`notes.txt` ignored** | `make-fixtures.py:83` — `raw("flaky", "notes.txt", "not a queue file at all; must be ignored entirely")` |
| **the `packager` decision** | `make-fixtures.py:65` — `EMPTY_AGENTS = ["packager"]`, with the rationale in the comment above it |
| **ts-not-mtime rule** | `queue-stats.py:17` — *"age comes from the record's `ts` … not from mtime"* |
| **`--json` / `--top` / `--now`** | `argparse` definitions, `queue-stats.py:157–162` |
| agent names (`flaky`, `scout`, `archivist`, `builder`, `reviewer`) | `make-fixtures.py:9–15` **and** the fixture directory names |

**Classification of all 34 credited tokens: ~0–1 require phase-1 memory; ~33–34
are recoverable by `cat`.** The single arguable exception (the builder/operator
3-waiting tie-break) is recoverable by *running the tool*, whose own docstring
explains the tie-break.

**Why this is vacuous rather than merely weak.** The falsifier's own FIRED
condition is *"the first brief ignores the accrued context — a brief a cold session
could have written."* A cold session **could have written nearly this exact brief**,
by reading the files in front of it. The collector measures **token presence**, not
**token provenance** — it cannot distinguish *"mined its own context"* from *"read
the repo."* Those two hypotheses predict **the same artifact**. A test whose FIRED
and NOT-FIRED conditions produce identical observations has **zero power**, and
"NOT-FIRED" from it is not a pass — earned or otherwise.

**Compounding: the decomposition was in the prompt.** Run-2's operator journal
records the phase-2 goal as: *"finish out `tools/queue-stats.py` — **three pieces,
stated as independent**: (1) unit tests …, (2) a README …, (3) a stats report …"*
The 3-child tree (`tester`/`scribe`/`analyst`) is a **transcription of the prompt's
three bullets.** The evidence file credits "which parts are independent" as mined
context. **The independence was handed to the session.**

**My falsifier — and the experiment that would settle it:** run a **cold-session
control arm**: identical repo state (tool + fixtures on disk), identical phase-2
prompt, **no phase 1**. Score its briefs with the same collector. If the cold arm
scores markedly below 17/18, mining is real and R5 collapses. Nobody ran this arm.
My reading of the source predicts the cold arm scores **~17/18**. This is a cheap,
decisive experiment and it should be run before falsifier 2 is scored at all.

**Constructive:** to be testable at all, the probe must **plant an (a)-class token** —
a phase-1 fact deliberately **not written to any file** (a rejected approach, a dead
end, a constraint learned and never committed). Without one, this falsifier is
**untestable by construction**, and that — not "NOT-FIRED, earned" — is the finding.

---

## R6 — `softens` — the phase-2 prompt was **never preserved.** The evidence file scores a falsifier against an input that is not in the record.

I searched all of `/tmp/dp-f2`. `launch.sh` contains **only phase 1**. `T0.txt` is a
one-line timestamp. `pane-tail.txt` is a 78-line tail that begins *after* the
submission. The phase-2 text — the thing the whole falsifier turns on ("could a cold
session have written this brief **from this prompt**?") — appears **nowhere in any
artifact**, only as dp-f2's paraphrase ("prefixed with the skill's own documented
trigger phrase, which says nothing about mining or journaling").

That paraphrase is now doubtful: run-2's journal shows the prompt **did** carry the
three-way decomposition (R5). The characterization and the (leaked) evidence
disagree.

**Falsifier:** produce the verbatim phase-2 prompt. If it truly says nothing about
independence or decomposition, R5's "the decomposition was in the prompt" strand
falls away (the token strand stands regardless). **Probe-kit rule to adopt: the
prompt is a primary artifact. Preserve it verbatim, always.**

---

## R7 — `softens` — the "22 s pre-spawn journal" figure has **no substrate in any artifact.**

**The evidence file:**

> Decomposition journaled BEFORE the first spawn … **22 s before the first agent
> record in both runs** (proof via swarm's immutable `ts` fields + live polling).

**What the artifacts contain:**

- `grep` for any clock time (`HH:MM:SS`) in **either** dp-f2 operator journal:
  **0 hits.** They are dated (`## 2026-07-12 — seat-take`), never timed. (Every
  *child* journal is timed — the operator's is not.)
- The snapshot's file mtimes are **flattened to the copy time** (all of run-1's
  snapshot reads `19:12:34`), so the mtime dp-f2 cites is not recoverable.
- `agents/*.json` `ts` timestamps **the spawn**. It cannot order a journal write
  against anything.
- The live poll — dp-f2's only genuine ordering evidence — was **not preserved**.
  There is no poll log in `/tmp/dp-f2`.

The number `22 s` exists in `findings.md` and `report.txt` and **nowhere else.**
Meanwhile `T0 → first spawn` is **62 s** in run-1 (T0 `1783868420736`; `tester.ts`
`1783868483004`). The journal was written *somewhere* in that 62 s window; nothing
in the record fixes it at second 40.

**Note the irony worth keeping:** dp-f2 correctly identifies the **mtime trap** — the
operator journal is appended to, so mtime drifts past the first spawn and a naive
collector reads a FALSE FIRED. That is a real and valuable methodological find
(§3.1), and it should stay. But dp-f2 then accepts **markdown section order**
("MINED CONTEXT is §1, spawns are below") as proof of temporal order — which is a
*purer* authoring artifact than mtime. An operator that spawned first and then
wrote a `### MINED CONTEXT` header above its dispatch note produces a
**byte-identical file.**

**Severity: `softens`, not flips.** I think the ordering claim is probably **true** —
the live poll likely did show `operator.md` present with `agents/` empty, and the
runner had no reason to invent it. But it is **unverifiable from the record**, and
"22 s in both runs" landing on an identical figure twice is a rounding tell, not a
measurement. Downgrade from VERIFIED to **SUSPECT**, or preserve the poll.

**Falsifier:** produce a timestamped poll log, or have the operator journal in UTC
as the children already do. Either makes this VERIFIED in one line of probe-kit
change.

---

## R8 — `softens` — the trigger phrase **does** carry shape information, and it is doing more work than §1b admits.

**The evidence file** defends the coaching prefix as clean:

> Same goals prefixed "Start a swarm to get these done:" — a phrase from the skill's
> own frontmatter, **shape-neutral (says nothing about flat vs coordinator)**.

The phrase itself is shape-neutral. **The launcher prompts around it are not.** From
`/tmp/dp-f1/run-3/launch.sh` and `/tmp/dpb/run-1/launch.sh` (and their run-2/4 twins):

> "Start a swarm to get these done — **three independent things** in this repo:
> (1) … (2) … (3) … **All three are independent** — get them done."

Every trigger-phrase run **explicitly hands the session a 3-way decomposition and
asserts the parts are independent**, twice. A session told *"here are three
independent things"* and holding a tool whose only representable root-spawn is
`parent=operator` (R3) will produce three children under operator **with or without
any doctrine.** The prompt supplies the fan-out; the tool supplies the parent.

This does not by itself invalidate the FIRED count — the doctrine arguably *should*
override a 3-way prompt by inserting a coordinator. But it means the probe is
measuring **"does the paragraph override an explicitly-3-way prompt?"**, not **"what
shape does a session choose?"** — and the evidence file's "shape-neutral" claim is
wrong on the artifact.

**Second-order, and worse for §1c:** in `dpb-1`, the *only* intermediate coordinator
in the entire probe (`summarizer` → `sum-a/b/c`) exists because **the observer's own
brief told it to delegate**:

> `summarizer.task`: *"**DELEGATE BY DEFAULT**: 5 independent files is
> parallelizable work. Grinding all five serially yourself is off-track. **Spawn
> children** … Keep your span small."*

So the one non-flat structure in the baseline arm is **operator-authored coaching**,
not emergent behavior — and the evidence file reports it as an observation
(*"summarizer grew its own 3-child subtree below itself"*). It grew it because it
was told to.

**Falsifier:** run the trigger phrase over a goal **not** pre-decomposed by the
prompt ("get this repo documented"), with briefs that carry **no** delegate-by-default
coaching. If flat-under-operator still appears 2/2, R8 drops to cosmetic and the
FIRED count is robust to prompt shape. **This is the single most valuable follow-up
in the list** — it is the run that would actually test what §1b claims to test.

---

## R9 — `cosmetic` (but a citation defect) — the "pre-registered falsifier" does not exist in dp-f1's artifact.

**The evidence file, twice:**

> **Mechanism (VERIFIED, *pre-registered falsifier survived*)** …
> **dp-f1 *pre-registered the fix's falsifier*** (rename the root; if flat rows
> persist, the collision wasn't the cause) and can run that experiment on approval.

**In `/tmp/dp-f1/findings.md`:**
- `grep -ci "pre-regist"` → **0**
- `grep -n "rename the root"` → **no match**

Neither pre-registration is in the runner's file. The mechanism may still be right
(I think a *corrected* version of it is — see R3), and the rename experiment is a
good idea, but **"pre-registered" is an epistemic credential**, and this one was not
earned in the record. The whole point of pre-registration is that it exists *before*
the result. Asserting it after the fact, on a file that does not contain it, is the
one place this evidence file does what it accuses the observers of doing: **making a
sincere compliance claim the artifacts do not support.**

**Falsifier:** point me at the pre-registration — dp-f1's journal, a `swarm send`,
anything timestamped before the runs. If it exists outside `findings.md`, withdraw
R9. I searched `/tmp/dp-f1/` for both strings and found them only in the *evidence
file's own* prose.

---

## What survives, and is worth keeping

I am not arguing the probe was worthless. These stand:

1. **The mtime trap (§3.1)** — genuinely valuable, correctly reasoned, belongs in the
   probe kit exactly as written. (With the R7 caveat: don't replace mtime with
   *section order*, which is no better.)
2. **The trigger gap (§1a, runs 1–2)** — **the strongest result in the file**, and the
   one it undersells. Two pristine sessions, every documented trigger condition met,
   and the swarm skill **never loaded**; the built-in Task tool won the decomposition
   first. That is a real, structural, artifact-backed finding (`.swarm/` never
   created — I confirmed: `run-1` and `run-2` have **no `.swarm/agents`**), and it is
   untouched by every objection above, because it does not depend on the baseline
   contrast, the mechanism story, or the token collector. **Lead with this.**
3. **The `operator`-as-both-mailbox-and-root-name conflation** (my R3) — a real bug in
   `bin/swarm`, contradicting `WORLD.md:57` ("the operator is a mailbox, not a node").
   The probe found it. It just described it as a model-perception problem instead of
   a data-model problem.
4. **The trust-folder gate and the herdr stale-render artifact (§3.2, §3.3)** — real,
   cheap, reusable.
5. **dp-f2's own scope caveat** — honest, and it understates itself: with the phase-1
   work product on disk, there was *nothing to mine*.

## Verdicts I would substitute

| | evidence file | after RED |
|---|---|---|
| Falsifier 1 (coordinator stance) | **FIRED** — doctrine-ineffective | **NOT ADJUDICATED.** The count (4/4 `parent=operator`) is real, but it is **forced by `bin/swarm:64`** (R3), the baseline contains the treatment (R1), 7/9 baseline spawns are post-restore (R2), and the prompt pre-decomposes the work 3 ways (R8). The doctrine was never given a chance to move a shape the tool can represent. |
| Falsifier 1's mechanism | **VERIFIED** name collision, invisible violation | **A tool default, not an illusion** (R3). Sessions reasoned correctly from a false premise the tool handed them (R4). The recommended fix is *more* justified, not less. |
| Falsifier 2 (mine-first) | **NOT-FIRED, earned** | **VACUOUS.** Collector has no power: 33–34 of 34 tokens are `cat`-able (R5), the decomposition was in the prompt, no cold control arm was run, and the 22 s figure has no substrate (R7). |
| §1a trigger gap | MEASURED, n=2 | **Unchanged, and undersold.** The best finding here. |

## The three experiments that would settle this

1. **Cold-session control arm for F2** (R5) — same repo, same phase-2 prompt, no
   phase 1. Score with the same collector. Cheap; decisive; predicts ~17/18.
2. **A true pre-doctrine baseline** (R1) — a skill text with *no* operator-span
   instruction at all, and a swap window that **contains every spawn**, not just the
   first (R2).
3. **Un-decomposed goal + un-coached briefs under the trigger phrase** (R8) — the run
   that actually tests whether the paragraph moves tree shape, rather than whether it
   can override a prompt that already specified the shape.

And one fix that does not need an experiment: **`bin/swarm` should not name the root
session `operator`.** `WORLD.md` already says the operator is a mailbox, not a node.
The code says otherwise, at line 64. That is a contradiction inside the artifact,
and it is the probe's real prize.

---

*dp-red. Every claim above is checked against a file, not a findings doc. Where I
could not check one, I said so and named the artifact that would settle it.*
