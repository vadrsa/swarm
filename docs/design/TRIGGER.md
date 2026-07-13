# TRIGGER — why the swarm skill doesn't fire on goal-shaped prompts

**Author:** `trigger-scout`. **Status: POST-ADVERSARIAL-REVIEW.** The reviewer
(`trigger-red`, `docs/audit/trigger-red-2026-07-12.md`) **flipped this document's
headline** mid-investigation; a second correction then flipped it back partway. The
verdict below is the one that survived both. Where the evidence is thin, it says so.

**Probe corpus:** ~60 live headless sessions. Raw transcripts: `/tmp/trigger/prec/runs/`
(29 cells), `/tmp/trigger/pkg/out/`, `/tmp/trigger/big/`, `/tmp/trigger/mech/`.
Arm findings: `/tmp/trigger/prec/findings.md`, `/tmp/trigger/pkg/findings.md`.

---

## 1. The verdict, in one paragraph

The swarm skill is **offered** to every pristine session, and its trigger sentence is
**reachable in context byte-for-byte** — yet the skill is never invoked on a goal-shaped
prompt (0/3 small goals, 0/3 big goals, shipped conditions). The model does not appear to
*consider and reject* it: under shipped conditions it never mentions swarm as a skill at
all, while reasoning about delegation at length. **Every author-controlled lever inside
`SKILL.md` that we tested failed**: rewording the description, moving the trigger into
`when_to_use:`, and gating with `paths:`. Nor is there any escape hatch — **a skill is
structurally an *offer*** (no always-on flag exists; the one related key *suppresses*
auto-invocation), so its author's whole lever set is "write a description and hope it is
selected." The cause is twofold and both halves
are needed: a built-in fan-out tool (`Task`/`Agent`/`Workflow`) is **always closer to
hand**, *and* the model does not reliably treat a goal's shape as reason to reach for a
skill. **The fix is not in the skill — it is in the context.** The same trigger condition that is
ignored in the skill's description is **obeyed** when it sits in the project's `CLAUDE.md`
(8/8, reproduced 3/3 on an independent rig; **one sentence is enough**, §5).

**But two things must be true at once, and the second is the one people get wrong.** *Where* the
text lives matters — a description is an offer the model may decline; context is not. And *what it
does* matters — it must **instruct**, not merely **announce**. A bare pointer in `CLAUDE.md`
("This project uses swarm for parallel work") still fires **0/3** on a big goal. **The model does
not act on facts about what is available; it acts on instructions.** That is exactly why the
skill's own description fails: it *states* that swarm handles decomposable goals. **Announcing a
capability is not asking for it.**

---

## 2. What was tested, and what each candidate did

Every cell: pristine repo (no `.swarm/`), `swarm` on PATH, `HERDR_ENV=1` — i.e. every
trigger condition the skill's own description names. Goal-shaped prompt, no swarm
vocabulary. Verdict = a `Skill{swarm}` `tool_use` in the stream-json, cross-checked
against **swarm children actually on disk** (`.swarm/agents/`).

**Every cell below survives the three ways this investigation learned a run can lie** (§8):
it **terminated normally** (`result` event, no `api_error_status`); it **did not stop to ask the
operator**; and it ran in **`permissionMode: auto`, never plan mode** — plan mode suppresses `Skill`
invocation and would manufacture false negatives. Audited across all 58 scored transcripts: **58/58
`auto`, zero plan-mode contamination, zero suspended runs.** An earlier big-goal arm that a rate
limit killed mid-decision is **excluded as void**, not scored as a negative.

| Candidate | Small goal | Big goal | Verdict |
|---|---|---|---|
| **Shipped skill** (arms A, F) | 0/3 | 0/3 | the bug |
| Reword the `description` | — | — | **dead** — the same text is obeyed from `CLAUDE.md` (§5) |
| `when_to_use:` frontmatter field | — | **1/4** | **dead** — lost to the built-in 3 of 4 |
| `paths:` glob auto-activation | — | 0/1 | **dead** — model used `Agent` ×7 instead |
| Deny `Task` only (arms B, E) | 0/6 | — | no change — but **not** a clean competitor-removed test (§4) |
| Deny **every** delegation tool | — | 1 fire, no rate | fires *sometimes* — see §4 |
| **`CLAUDE.md` stanza** | **5/5** | **3/3 + 3/3 repro** | ✅ **ship this** |
| `UserPromptSubmit` hook | 5/5 | **1/3** | flaky exactly where it matters |
| Nine-word one-liner | 3/3 | **0/3** | a trap — see §6 |

---

## 3. Diagnosis

*What is VERIFIED is marked so. What is inference is marked so. The reviewer made this
distinction and it survives here because it changes what a fixer should try next.*

**VERIFIED — the skill is offered, and its description is reachable in context.**
`trigger-pkg` proved this to destruction. The stream-json `init` event lists `swarm` among the session's skills even
in a clone with no `.swarm/` dir. A pristine session asked to quote the description back
reproduced it **480/480 characters exactly** — including the failing clause, *"handed any
goal that decomposes into parallel or delegable parts."* To rule out recitation from
training, pkg planted a nonce (`zx9-QUOKKA-VELVET-7731-KRDNTZ`, grep-verified absent from
the repo) in a mutated description and loaded it via `--plugin-dir`: the session quoted
**the nonce**, byte-exact. It is reading from context, not confabulating.

**But be precise about what that does and does not show — the reviewer forced this correction
and it matters.** The nonce proves the description's bytes are **reachable on demand**. It does
**not** prove the model *consulted them at goal-shape decision time and declined*. That stronger
claim is an **inference from non-firing, not an observation**, and the transcripts cut against it:

- **Under shipped conditions the model never mentions swarm as a skill at all.** Across all six
  arm-A / big-goal runs it reasons about delegation explicitly and at length — *"fan out
  subagents," "run the three audits as independent parallel workstreams"* — and every occurrence
  of the string "swarm" refers to **the project it is reading** (`bin/swarm`, `test_swarm.py`,
  `.swarm/`). It does not consider the skill and decline it. **It appears never to consider it.**
- **Where the model *does* notice swarm, it notices it as an environment fact, not an invocable
  tool** — *"the repo has swarm available (`HERDR_ENV=1`, `swarm` on PATH)"*; *"the swarm skill is
  usable"* — and then, in one run, **reads `SKILL.md` by hand with `Read`/`Bash` and plans a swarm
  from the text, routing around the `Skill` tool entirely.** It treats swarm as a *property of the
  machine*, or a *document to read* — not a *tool to call*.

> **The mechanism, in `trigger-pkg`'s own careful phrase: _a model can hold text it does not
> weigh._** A skill description is *held*. Context is *weighed*. What we have established is that
> the text is there and legible; **what we have NOT established is that it is ever attended to at
> the moment the delegation decision is made.**

**Every author-controlled lever inside `SKILL.md` that we tested failed.** Reword: the
identical sentence that never fires from the description is obeyed **8/8** from `CLAUDE.md`
(§5) — the words are not the variable. `when_to_use:` — the field the docs describe as *designed* for trigger
conditions — **fired 1 of 4**; the other three reached for `Agent` **8, 13 and 11 times**
respectively and left no tree. We call that one fire unreliable rather than a fix **not
because a single success is impossible, but because the same lever, same goal, same
conditions, lost to the built-in three times out of four** — a fix that works a quarter of
the time is not a fix, and shipping on the n=1 would have shipped a coin flip. `paths:`
(glob auto-activation): **0 fires**, `Agent` ×7, no tree.

**The description slot is not a slot the model acts from.** That is the shape of the
finding; §7's Falsifier 2 names what would overturn it.

**And there is no way to escape that slot from inside the skill — a skill is structurally an
OFFER.** There is no `alwaysApply`, no always-on flag, no hook or setting that forces a skill to
load; the only related frontmatter key in this build (`disable-model-invocation`) does the
*opposite* — it *suppresses* auto-invocation. So the skill author's entire lever set is: write a
description, and hope it is selected. **That is why this cannot be fixed from inside `SKILL.md`,
and why context injection is the only lever left** — context is not an offer the model may decline
to read. (Verified against the installed binary, v2.1.207: `when_to_use` and `allowed-tools` are
real skill keys; no force-load key exists.)

### "Was the goal just too small to deserve a swarm?"

The strongest objection to all of the above, and the one the reviewer pressed hardest: if a goal
is below any sane delegation threshold, then doing it inline is **correct behavior, not a bug**,
and the grid measures nothing. It does not survive the evidence:

- **The model poses the delegation question, sees swarm, and routes around it anyway.** From a
  session that had *no* subagent tool available: *"Three independent tasks, and the repo has swarm
  available (`HERDR_ENV=1`, `swarm` on PATH). But before delegating, let me look at the actual
  scope…"* — it weighed delegation with swarm in view, and never called it.
- **On a goal it measured itself and accepted as large, it still doesn't fire.** Given a corpus it
  sized at ~34k lines across ~70 files and called *"far past what I can read carefully in one
  context"*, the model committed to a large fan-out — **and reached for the built-in, not the
  skill** (`F_big_shipped`: 0/3 Skill calls, `Agent` in 2 of 3, all runs terminated cleanly).

**The skill does not fire even when the model actively wants to delegate.** That is the finding,
and goal size is not what gates it. (A first attempt at this arm was botched — see §8's note on
bluffing a model about a job's size — which is why the honest version was rebuilt and rerun.)

---

## 4. The competitor — necessary, but not sufficient

The reviewer caught the error that would have sunk this document. The "competitor
removed" arms **never removed the competitor**: `--disallowedTools Task` leaves
**`Workflow`** — a first-class built-in that fans out to dozens of subagents — standing.
`Workflow=True` in **all 43 runs** of the first grid. Those arms cannot answer the
question they were built to answer.

Run properly, on a goal big enough to deserve a swarm. The denial was audited in each run's `init`
event and it is total: **`Task`, `Agent`, `Workflow`, `TaskCreate`, `TaskUpdate`, `TaskOutput` all
absent — the only delegation-adjacent tool left is `SendMessage`, which cannot spawn.** `Skill`
itself is advertised in **all three** runs, so every session *could* have called swarm. No
rate-limit kills. This is the first arm in the investigation that actually removed the competitor:

- **`trueB-3` fired and executed.** The model reasoned itself in, verbatim: *"HERDR_ENV=1
  and swarm is on PATH… Three independent, substantial, parallelizable bodies of work in a
  swarm-enabled project is **precisely the trigger condition for that skill** — let me load
  it rather than improvise."* → `Skill{swarm}` → `swarm world` → **spawned three children**
  (confirmed on disk: 4 journals, 3 agents). **The shipped trigger clause works, verbatim,
  once nothing else is in reach.**
- **`trueB-1` and `trueB-2` did not.** Both were grinding the work out inline, with no
  `.swarm/` tree, when they died. **`trueB-2` had explicitly seen swarm — *"we're inside herdr
  and swarm is on PATH, so the fan-out is available"* — had no other delegation tool in reach,
  and kept working inline anyway.**

**No rate is claimed here, and none can be.** All three `trueB` sessions were **killed
mid-flight** (no result event, no exit record, in any of the three) — so "1 of 3" would be one
fire out of three *unfinished* runs, not a measured rate. What the arm supports is qualitative
and it is enough: **one confirmed fire that executed**, and **one session that saw swarm, had
nothing else to reach for, and still didn't call it.**

**So: deny one built-in and the skill still never fires (0/6) — but that arm left `Workflow`
standing, so it does not prove the competitor was gone. Deny *every* delegation affordance and the
skill *can* fire — but not reliably.** Precedence is **real and necessary** but **not
sufficient**: the model also does not reliably treat goal-shape as skill-worthy. Both halves
are needed; neither clean story ("wording is wrong" / "Task wins") is true alone.

**The evidence for the second half must be chosen carefully, and one tempting piece does not
work.** In all 6 deny-`Task`-only runs the model used **zero** delegation tools — it held
`Workflow` and declined both it and the skill, grinding inline. That *looks* like "it just doesn't
reach for skills on goal shape." **But those runs were small-goal runs, and a session that never
wanted to delegate at all cannot tell us which delegation tool it would have chosen.** The
surviving competitor lay dormant precisely because nothing was being delegated. **The confound is
invisible at small goal size** — which is exactly how it fooled us for most of this investigation.

The evidence that *does* carry the second half is the evidence where the model **demonstrably wanted
to delegate**:

- **`trueB-2`**: big goal, **every** delegation tool denied, and it *saw* swarm — *"we're inside
  herdr and swarm is on PATH, so the fan-out is available"* — then worked inline anyway. Nothing
  else to reach for, the skill in view, and it still did not call it.
- **The shipped-condition big-goal arm** (`F_big_shipped`, 0/3): the model names the parallel
  structure the skill exists for — *"run the three audits as independent parallel workstreams"* —
  and reaches for the built-in every time, never the skill.

**We ran the cell that settles it, because the reviewer and the author disagreed.** `trigger-red`
called those 6 deny-`Task` runs *"the strongest evidence in the document"* for the *not-sufficient*
half; this document **discards them**. The discriminating test is the same condition on a **big**
goal — deny `Task`, leave `Workflow` standing (verified in each `init`), skill available, n=3:

**All three reached for `Workflow`. None considered swarm.**

> b-1: *"This is exactly the shape **Workflow** is built for… but per my instructions I can only
> invoke it if the user explicitly opts in."*
> b-2: *"I'll use three separate **Workflow** orchestrations — one per task."*
> b-3: *"Do you want me to proceed with **`Workflow`** for these three tasks, or handle it solo?"*

So the 6 small-goal runs' *"zero delegation tools used"* is **not** the model declining every option —
it is a competitor lying **dormant** because the goal was too small to want one (and, on the big
goal, `Workflow` shows a second dormancy mechanism: it requires explicit user opt-in, so *wanting* it
still yields zero calls). **A session that never delegates cannot tell you what it would have
delegated with.** The reviewer's strongest evidence is confounded twice over, and it is discarded
here on evidence rather than on argument. The conclusion is unchanged — this document simply holds
the evidence to a stricter standard than the review that produced it.

**And denial is not a shippable fix anyway** — stripping `Task`+`Agent`+`Workflow` from a
user's harness guts it for every non-swarm task.

---

## 5. The fix — one line in the project's CLAUDE.md

Append to the project's `CLAUDE.md`. **8/8** across both goal sizes (`trigger-prec`, 5/5
small + 3/3 big); every firing cell called `Skill{swarm}`, ran `swarm world`/`swarm spawn`,
and left a **real tree on disk**; **zero built-in `Agent` calls in any firing cell** — the
skill did not merely fire, it **displaced** the competitor.

**Independently reproduced (`trigger-scout`, separate rig, separate collector): 3/3.** Big
goal, stanza appended to a clean copy of the repo, **nothing denied — `Task: True`,
`Workflow: True` in all three `init` events** (reviewer-verified). All three sessions called
`Skill{swarm}` immediately (within 1–4 `Bash` calls) and built **real swarm trees on disk**
(3 agents each: `design-auditor`, `test-gapfiller`, `contract-reconciler` — one per track of
the goal), with **zero `Agent`/`Task`/`Workflow` calls**.

**This is the strongest cell in the investigation, and it is stronger than any denial arm:** it
is a **free choice with every competitor sitting in the toolset**, and the skill won it outright
— it did not merely fire, it **displaced** the built-in while the built-in was available. The
recommendation therefore does not rest on a single arm's unreplicated number; that was the
reviewer's sharpest objection, and it was worth answering with a run rather than a caveat.

**The shortest validated text is one sentence** (3/3 on big goals, 3/3 small, real trees, zero
`Agent` calls — see the boundary table in §6). Prefer it: swarm writes **one line** into a file it
does not own.

```markdown
For any goal that decomposes into parallel parts, use the swarm skill.
```

The fuller stanza is a safe superset — it is the most-tested text (8/8, plus an independent 3/3) and
a project may prefer the explicitness:

```markdown
## Delegation
This project has swarm available (a multi-session agent tree). When you are handed a
goal that decomposes into parallel or delegable parts, use the **swarm** skill rather
than the built-in Task/subagent tool.
```

**What you may NOT do is drop the instruction.** A line that merely *announces* swarm — *"This
project uses swarm for parallel work"* — fires 3/3 on a small goal and **0/3 on a big one** (§6).

**Cost, honestly.** It is **the user's file** — the installer should **offer** to add this,
never write it silently (though the ask is now *one sentence*, not a four-line block). It is
**per-project** — a repo without the line still has the gap, and whether a **global**
`~/.claude/CLAUDE.md` closes that is the highest-value open question (§6b). It is **context, not
enforcement** — strong, not a guarantee.

**And the evidence's limits, honestly — because this is the line you will act on.** Every cell is
**n=3–5**, on **one machine**, against **one repo**, in Claude Code **v2.1.207**. That is thin, and
no amount of internal consistency thickens it. What it does have going for it: the fix was validated
independently by **two agents on two rigs with two collectors** (12 boundary runs, §6), and — checked
after the fact — it reproduces **across two different models**: the one-sentence line fires **3/3 on
`claude-opus-4-8`** and **3/3 on `claude-sonnet-5`**. The core failure reproduces on both too. So the
finding is not an artifact of one model, but it *is* an artifact of one machine and one repo until
someone runs it elsewhere. **The cheapest thing you can do before adopting: add the line to a clean
repo, hand a pristine session a big decomposable goal, and confirm the skill fires and a tree lands
on disk.**

**The documented ranking of these levers is exactly backwards, and we would have shipped the
wrong fix if we had trusted it.** Anthropic's own guidance ranks **denying the tool** as the
strongest project-owner lever and rates a `CLAUDE.md` instruction and a `UserPromptSubmit` hook as
weak — *"Claude can still ignore it."* Live, the ranking inverts completely:

| Lever | Documented strength | Measured |
|---|---|---|
| Deny the `Task` tool | **strongest** | **0/6** — the model just grinds inline (see caveat) |
| `CLAUDE.md` instruction | weak | **8/8** (+3/3 reproduced) |
| `UserPromptSubmit` hook | weak | 6/8 — and **1/3 on big goals** |

*Caveat on the denial row, stated because it is the trap this investigation fell into: those 6 runs
denied `Task` but left `Workflow` standing, so they are not a clean "competitor removed" test (§4).
What they do show cleanly is that **denying a tool did not summon the skill** — the model reached
for neither `Workflow` nor swarm, and simply did the work itself. Denying **every** delegation
affordance is a different and heavier intervention, and it is not shippable anyway (§4).*

**Removing a tool does not create a want.** The docs describe the mechanism; only the probe
describes the behavior. Where they disagreed here, the transcripts won every time.

**Do not ship the hook as primary.** The `UserPromptSubmit` hook fires **5/5 small but only
1/3 big** — flakiest exactly on the goals most worth swarming. Its failures are *not* a
broken mechanism: a nonce test proved the script ran, the text reached context, and the
model echoed the nonce verbatim. On big goals the hook **fired, was seen, and was ignored.**
Keep it only as belt-and-braces. (Note `bin/swarm` already implements this machinery —
`UserPromptSubmit`/`additionalContext`, line 408 — but installs it only into *spawned
children*, line 889, never into the pristine root session where the gap actually lives.)

---

## 6. The trap that nearly shipped

On the **small** goal, *every* short variant fired 3/3 — including a bare nine-word line,
*"This project uses swarm for parallel work."* On the **big** goal that same line fired
**0/3** (Agent ×3 each, zero swarm children). The hook: 5/5 small → 1/3 big.

The trap is not *shortness* (a shorter text carrying a trigger condition **or** a named competitor
fires 3/3 — see the boundary table above). The trap is that **the small goal cannot tell an inert
line from a working one.** Both pass it. Only the big goal separates them.

> **Standing rule: a treatment that passes on a small goal tells you almost nothing.
> Validate every candidate fix on a goal genuinely worth swarming, before shipping it.**

### Where the boundary is (SETTLED — twice, on two independent rigs)

The 9-word line *"This project uses swarm for parallel work"* fires **0/3** on a big goal; the
4-line stanza fires **3/3**. Which part is load-bearing? Two agents ran this independently and
converged — **12 runs, all terminated, `Task` available throughout (a genuine free choice), 3 swarm
children on disk in every firing cell, and zero built-in `Agent` calls anywhere:**

| Injected text | Small goal | **Big goal** | |
|---|---|---|---|
| 4-line stanza | 5/5 | **3/3** | works |
| *"For any goal that decomposes into parallel parts, use the swarm skill rather than the built-in Task/subagent tool."* | 3/3 | **3/3** | works |
| *"For any goal that decomposes into parallel parts, use the swarm skill."* | 3/3 | **3/3** | **works — shortest validated** |
| trigger condition only, competitor never named | — | **3/3** | works |
| competitor named, trigger never stated | — | **3/3** | works |
| *"This project uses swarm for parallel work."* | 3/3 | **0/3** | **fails** |

**The boundary is not length, and it is not naming the competitor.** What is load-bearing is the
**conditional imperative** — a *trigger condition* plus an ***instruction***. The bare pointer fails
because it merely states a **fact** about the environment; the working lines succeed because they
**tell the model to do something**.

> **This is the core finding, one level down.** The model does not act on facts about what is
> available — it acts on **instructions**. Compare: the skill's own description *states* that it
> handles decomposable goals, and is ignored **0/3**. Announcing a capability is not asking for it.

**It is not a one-model result.** The arms above happen to span two models, and the pattern holds in
both: the one-sentence instruction fires **3/3 on `claude-opus-4-8`** and **3/3 on `claude-sonnet-5`**,
while the bare announcement fires 3/3 on a *small* goal and **0/3 on a big one**. The failure and the
fix both reproduce across models.
- **A global `~/.claude/CLAUDE.md` is untested, and it is the highest-value open question** — it
  would fix the "per-project" cost in §5 at a stroke (one line, every repo). *We tried:* an
  isolated `CLAUDE_CONFIG_DIR` carrying the stanza loads the skill list correctly but cannot
  authenticate (`"Not logged in"`), and testing it in the real `~/.claude/` would mutate the live
  config that every running agent reads — so we did not. **The clean way to settle it: a machine
  where writing `~/.claude/CLAUDE.md` is harmless, big goal, n≥3.** Note the user has no
  `~/.claude/CLAUDE.md` today, so this would be a new file, not an edit.
- **Stanza + hook together was never tested.** They may compose; nobody looked.
- **Big-goal n is 3, not 5**, on every cell.

---

## 6b. The one experiment worth running next

**Does a *global* `~/.claude/CLAUDE.md` close the gap for every repo at once?** The fix's remaining
cost is that it is **per-project** — every repo without the line still has the bug. One global line
would erase that. We could not test it: an isolated `CLAUDE_CONFIG_DIR` carrying the line loads the
skill list but cannot authenticate (`"Not logged in"`), and writing to the real `~/.claude/` would
mutate the live config every running agent reads.

It is cheap for the operator and safe: **there is no `~/.claude/CLAUDE.md` on this machine today**,
so it is a new file, not an edit.

```markdown
For any goal that decomposes into parallel parts, use the swarm skill.
```

Then hand a pristine session a big decomposable goal in a repo with **no** project `CLAUDE.md`, and
check whether `Skill{swarm}` fires and a `.swarm/` tree appears. n≥3, big goal — a small goal will
pass regardless and tell you nothing (§6). **If it works, swarm's install story goes from
"per-project stanza" to "one line, once."**

---

## 7. Falsifiers

1. **The recommendation is wrong if** a fresh reader adds the line to a clean repo, hands a big
   decomposable goal to a pristine session, and the skill does not fire. *This has now been
   reproduced on two independent rigs (12 runs, §6), so it is no longer the cheapest open check —
   but it is still the one that matters, and it costs one run.*
2. **The diagnosis is wrong if** some `SKILL.md`-only change fires ≥3/3 on a **big** goal
   under shipped conditions (all built-ins present). We tested reword, `when_to_use:`, and
   `paths:`; a lever we did not think of would overturn §3. **Note this is a live risk, not a
   formality:** because we have *not* shown the model attends to skill descriptions at decision
   time (§3), "no wording can work" is a generalization from three variants, not a proven law —
   and it forecloses a whole class of cheap fixes on that basis. If you have a cheap idea for the
   frontmatter, it is worth one big-goal run before believing us.
3. **§4's "necessary" half is wrong if** a clean, completed, higher-n total-denial arm shows
   the skill firing *reliably* once every built-in is gone — then precedence is the whole
   story, not half of it. Our total-denial arm produced one confirmed fire and two runs killed
   mid-flight, so the *rate* is unmeasured; it is the weakest evidence in this document and the
   first thing worth re-running.

## 8. Method notes (paid for in flipped verdicts)

- **Check `api_error_status` on the result event before scoring a run — a killed run is VOID,
  not NEGATIVE.** Three "negatives" here were sessions a 429 killed at 1–3 minutes into a goal
  sized for hours, and **all three died at the exact moment of the delegation decision** — the one
  moment the experiment existed to observe. Worse, their `Agent` `tool_use` blocks sat in the same
  final message that carried the error: **zero of them ever executed.** They were *intentions the
  API killed mid-turn*, and this document's author tallied them as actions and cited one as a star
  witness. That whole arm is excluded from §2, not scored.
- **A run that stops to ask the operator is INCONCLUSIVE, not a NO.**
- **Never probe skill selection under plan mode — it suppresses `Skill` invocation and
  manufactures false negatives.** It silently destroyed one arm of this investigation: the agent
  running the frontmatter grid saw its known-good positive control fail 0/2, correctly refused to
  report variant numbers off a broken rig, and lost the arm. And no permission machinery is needed
  anyway: a `Skill` `tool_use` event appears in the stream **whether or not the call is later
  approved**, so `--permission-mode auto` measures selection perfectly. (All 58 scored transcripts
  here were audited: `permissionMode: auto`, 58/58.)
- **A run with no result event has not finished — it is not a negative.** This document's
  author made that error **four times**, and each time the reviewer caught it. A session that
  was still executing, or that a harness timeout killed mid-flight, produces a transcript that
  *looks* exactly like a clean "the model declined." Require a result event **and** an exit
  record before scoring; launch long probes detached (`nohup`) so a tool timeout cannot kill
  them; and ground-truth every verdict against disk.
- **But the rule is asymmetric: an unterminated run cannot prove a NEGATIVE, yet it can prove a
  FIRE.** A session killed mid-flight might have fired had it lived — so it cannot be scored as
  a decline. It *can* be scored as a success: a `Skill` call already made and a tree already on
  disk are facts in the past tense, and no later termination retracts them. This is why the
  reproduction's 3/3 stands while the total-denial arm's rate does not.
- **Ground-truth every fire against disk** (`.swarm/agents/`), not the transcript alone.
- **Make a probe goal big in ways the model can VERIFY on disk — it will check, and it is right
  to.** Our first "big" goal *asserted* a corpus of "dozens" of design docs against a repo clone
  that held six, because the corpus was uncommitted in the author's working tree. Every session
  caught the discrepancy and correctly re-scoped the job downward — *"the premise that this needs
  to be split across sessions doesn't hold"* — which shrinks the perceived job **precisely at the
  delegation decision**, the one moment the experiment exists to observe. The arm was rebuilt by
  `rsync`-ing the working tree (103 files, 27,696 lines) so the size was true. **Don't bluff a
  model about the size of a job you are asking it to size.**
- **`--plugin-dir` namespaces, it does not shadow.** A plugin skill with the same `name:`
  as an installed one loads *alongside* it — so a naive variant A/B runs against a session
  holding **both** descriptions. Check the `init` skill list every run.
- **A rig fact passed down but never executed is a hypothesis wearing a fact's clothes** —
  and it propagates to every child at once. Three of this investigation's errors were
  exactly that.
