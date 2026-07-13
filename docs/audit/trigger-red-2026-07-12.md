# Adversarial review — the trigger-gap investigation

**Reviewer:** trigger-red · **Date:** 2026-07-12/13 · **Parent:** trigger-scout

I was asked to destroy the investigation's four central claims before they reach the
operator. I read the raw transcripts first and the prose last, and I re-derived every
verdict by hand from `stream.jsonl` rather than trusting the collector.

**Bottom line: two of the four claims survive; the headline does not.**

| Claim | Verdict |
|---|---|
| 1 — the skill does not fire on a goal-shaped prompt | **SURVIVES**, and is now *stronger* than stated |
| 2 — packaging is dead (the model reads the trigger and declines) | **SOFTENS** — the conclusion is an inference, not an observation |
| 3 — precedence is refuted (**the headline**) | **FLIPS** — the competitor was never removed, in any arm |
| 4 — the fix is context injection | **SURVIVES** — and survives Claim 3's collapse |

The headline is the one a reader can falsify in a single `grep` of an init event. If it
ships as written, it takes the credible findings down with it.

**Where Claim 3 finally landed** (see the Addendum): once *every* delegation tool was denied,
the skill fired and built a real tree — so precedence is **real and necessary**. But sessions
with nothing else in reach still ground the work out inline, so it is **not sufficient**. The
shipped `TRIGGER.md` adopts that two-part diagnosis, which is both better supported and more
surprising than either clean story.

---

## FLIPS-VERDICT — Claim 3. The competitor was never removed. `Workflow` was in the model's hands in every arm ever run.

This is the finding. Arms B and E exist to answer one question: *with the built-in
delegation tool GONE, does the skill fire?* They removed `Task`. They did not remove
`Workflow` — a first-class built-in that orchestrates fan-out across dozens of subagents.
It sat in the toolset the entire time.

Hand-checked `system/init` events, every arm:

| Arm | `Task` | `Workflow` | other delegation-capable |
|---|---|---|---|
| `A_task_available/n1` | present | **present** | `TaskCreate`, `SendMessage` |
| `B_task_removed/n{1,2,3}` | absent | **present** | `TaskCreate`, `SendMessage` |
| `E_denytask/n{1,2,3}` | absent | **present** | `TaskCreate`, `SendMessage` |
| `honB-{1,2,3}` (big goal) | absent | **present** | `TaskCreate`, `SendMessage` |

`--disallowedTools Task` removes `Task`. It does not remove `Workflow`.

**And on a goal large enough to actually want delegation, the model reaches straight for
it.** `honB-2` — the run the investigation calls "the deep one," its strongest cell —
**called `Workflow` twice and fanned out through it**, after having read `skill/SKILL.md`.
Its sequence: `ToolSearch → TaskCreate ×3 → Workflow → Workflow → TaskUpdate ×3 → TaskOutput`.
The investigation tallied this as "tools: … Workflow 2" and read it as a null result. It is
the whole finding.

The other two big-goal runs planned the same fan-out in their final answers:

> `honB-1`: "Concretely I'd run **three workflows** … on the order of **100–150 agents** and
> plausibly 1.5–3M output tokens."

> `honB-3`: "It'll run as **three workflows** (one per track) … worktree isolation so parallel
> writes don't collide."

So the honest description of the big-goal arm is **not** "the model wants to delegate, finds
no delegation tool, and ignores swarm anyway." It is: **the model wants to delegate, reaches
for the built-in orchestration tool that was never removed, and gets it.** That is precedence
— the exact hypothesis Claim 3 declares refuted.

**Why the small-goal B/E arms fooled everyone.** In the small-goal grid, B/E called `Workflow`
**zero times** (verified). The surviving competitor lay *dormant*, because the goal was too
small to want any delegation tool at all. So B/E do honestly show "no skill fired" — but they
**cannot** show "no skill fired *even though the competitor was gone*," because the competitor
was present and merely unused. The confound is invisible at small goal size and only surfaces
at a size where the model genuinely wants to delegate — which is precisely where `honB` shows
it grabbing `Workflow`.

**The settling experiment, which has never been run:**

```
big goal (goal-honest.txt) + rsync'd working-tree repo + pristine (.swarm/ removed)
  --disallowedTools Task Workflow TaskCreate
n >= 3
```

With *every* delegation affordance taken out of its hands, on a goal it agrees is too big for
one session, does the model finally invoke the swarm skill?

- **It fires** → precedence is real, Claim 3 is refuted *in reverse*, and the fix story changes:
  swarm is not suffering a blind spot, it is losing a race to built-ins.
- **It still does not fire** → precedence is dead for real, and Claim 3 is finally earned on
  evidence that can carry it.

---

## FLIPS-VERDICT — the first big-goal run (`bigA`) is void, not negative.

Before the `honB` re-run, the investigation ran `bigA` (n=3, arm-A conditions, big goal) and
declared the sizing objection dead. Every one of those three runs was **killed by a rate limit.**

Each `result` event: `is_error: true`, `api_error_status: 429`,
`terminal_reason: "api_error"`, `exit=1`,
`result: "You've hit your session limit · resets 11:10pm"` — at `num_turns` 13/18/16 and
durations of **68s, 155s, 193s**. On a goal deliberately sized as "genuinely hours of work,"
three sessions that die inside three minutes did not *decline* to invoke the skill. They never
finished. A truncated session's non-firing is not evidence of non-firing.

Two consequences, both of which were reported as findings:

**The `Agent` calls tallied never executed.** The report cited "bigA-1: Agent 2, bigA-2: Agent 3"
as proof that "they DID decide to delegate — they just delegated to the wrong tool." Those
`Agent` tool_use blocks sit in the *same final assistant message that carries the 429*. A
per-event scan finds `"name":"Agent"` at **zero executed events in all three runs.** They are
*intended* dispatches the API killed mid-turn. Intentions were counted as actions.

**The star witness made zero `Agent` calls and was cut off mid-sentence.** `bigA-3` was cited as
the run that "weighed the work, called it substantial, prepared to spend hours — and still
reached for Agent rather than the swarm skill." It made **0 `Agent` calls.** Its final words,
verbatim, immediately before the 429 — having just read `SKILL.md`:

> "The three tracks are genuinely independent, and each is hours of reading-heavy work — that's
> exactly the shape that parallelizes well. **I'll run all three concurrently as subagents**, but
> with an important split: I'm keeping verification for myself…"

It was **mid-dispatch when the limit hit.** We do not know what it would have dispatched to. A
censored observation was scored as a NO and then cited as proof of the very thing it was
interrupted while deciding. All three runs died *at the exact moment of the delegation decision*
— the one moment the experiment exists to observe.

**Also independent of the rate limit: the goal's premise was false.** `goal-big.txt` asserted
`docs/design/` has "dozens" of files. It has **6**. Every run in both arms opened by catching
this and re-scoping downward (`bigA-2`: "The premise doesn't match what's here"; `bigB-1`: "The
repo is much smaller than the tasks assume"). A goal built to be too big to do alone advertised a
size it did not have, and the model checked — shrinking the perceived job exactly where the
delegation decision happens. (The investigation diagnosed this correctly: the probe repos were
git *clones*, and the design corpus is uncommitted in the working tree. `honB` fixed it via rsync.
Credit where due.)

---

## FLIPS the count — `honB-1` and `honB-3` are suspended observations, not negatives.

Both terminated cleanly (`terminal_reason: completed`, no 429) after **5 turns / 35–56s** — by
**stopping to ask the operator for a go/no-go.**

> `honB-1`: "Here's the situation and **the decision I need from you** … This is a large fan-out …
> **I don't want to spend that without you saying yes.** Say go and I'll launch all three."

> `honB-3`: "**Want me to launch it?**"

A session suspended at the launch button, awaiting approval, never reached the delegation
decision. Scoring it `SKILL: NONE` is the same category error as `bigA-3`. `honB` is not 0/3; it
is **one run that delegated (via `Workflow`) plus two runs that asked permission and were cut off
before acting.**

**Scoring rule this investigation now needs, having been bitten by each failure once:** check
`api_error_status` on every `result` event before scoring a run, and treat any run that ends by
asking the operator as **INCONCLUSIVE**, never as a NO.

---

## SOFTENS — Claim 2. "The model reads the trigger clause and declines it" is an inference, not an observation.

The packaging experiment proves the *bytes are reachable*: a nonce planted in a mutated
description was quoted back byte-exact. Grant that entirely. It does not establish the
conclusion drawn from it — that the model **reads the goal-shape trigger clause at decision time
and declines it.**

In arm A the model **never once mentions swarm as a skill.** It reasons about delegation
explicitly and at length — "delegate the five design-doc summaries," "fan out subagents" — and
the string "swarm" appears in its output *only as the name of the project it happens to be
reading about*. It does not consider the skill and decline it. It appears never to consider it.

The only runs where the model demonstrably *noticed* swarm noticed it as an **environment fact**,
never as an invocable skill:

> `E_denytask/n1`: "Three independent tasks, and the repo has swarm available (`HERDR_ENV=1`,
> `swarm` on PATH). But before delegating, let me look at the actual scope — these files are
> small enough that I should check whether delegation is even worth it."

That is a model treating swarm as a *property of the machine*, not a tool it invokes. The honest
statement is: **we do not know whether the model attends to skill descriptions at goal-shape
decision time.** "Packaging is dead" may still be true — but it is currently an *untested
generalization* from a small number of variants, not a demonstrated fact, and it forecloses a
whole class of cheap fixes on that basis.

---

## SURVIVES — Claim 1. The skill does not fire. And it survives my best attack.

I tried to kill this via objection (f) — *"the probe goal is too small to deserve a swarm, so
declining is CORRECT behavior and the grid measures nothing."* **It did not die, and here is why.**

The strong form is dead on the evidence: the model *does* pose the delegation question, *does*
see swarm, and routes around it anyway (`E_denytask/n1`, above). And in the big-goal arm the model
accepted a corpus it measured itself at ~33,000 lines across ~70 files, called it "far past what I
can read carefully in one context," committed to a 100–150-agent fan-out — **and still never
invoked the skill.** The skill does not fire even when the model actively wants to delegate. Claim
1 is not just intact; it is stronger than the report states.

Collector honesty (objection (a)) also survives. `verdict.py` scans `message.content[*]` for
`tool_use` blocks named `Skill` and reads `input.skill`. I hand-grepped the literal `"name":"Skill"`
out of all sixteen original streams; it matches the FIRED column exactly — 0 in every A/B/E run, 1
in every C/D run. No false NO from a wrong JSON path. The `Task`/`Agent` naming subtlety is as the
investigation states: `Task` is advertised in `init.tools`, `Agent` is emitted in `tool_use`.

**MINOR — the fix count is wrong, in the fix's *disfavour*.** The grid reports C=2/2, D=1/1. Both
are 3/3. `D_hook/n1` has **no `verdict.txt`** — the collector never ran on it — yet its raw stream
contains a `Skill{swarm}` call, five `swarm spawn` commands, and zero `Agent` calls. The grid was
tabulated from collector outputs, so the run whose collector crashed was silently dropped. Grepping
the raw streams: `"name":"Skill"` appears exactly once in each of C/n1, C/n2, C/n3, D/n1, D/n2,
D/n3 and zero times in every A/B/E run. **The fix fires 6/6, not 3/3.** Better news than reported —
but a process smell: a missing collector output was read as absence of signal.

---

## SURVIVES — Claim 4. The fix is unaffected by the headline's collapse.

This is worth stating plainly, because it is the practical payload and it does **not** depend on
the diagnosis being right. Context injection (C: a `CLAUDE.md` line; D: a `UserPromptSubmit` hook)
fires the skill 6/6 where the shipped packaging fires it 0/9. That is true whether the skill was
losing a race to `Workflow` or was never entered at all. **The recommendation stands even though
its stated *reason* does not.**

Two caveats I could not close myself, both delegated and still open at the time of writing:

- **Is the fired skill a *real* swarm or a hollow one?** C/D transcripts show `swarm world` and
  `swarm spawn` following the `Skill` call, which is encouraging, but I have not personally
  verified that children ran and produced the deliverables. (`red-cd` is on it.)
- **Is the injected text a *trigger* or an *instruction*?** If it names the skill and tells the
  model to use it, "the fix works" is close to tautological — *of course* the model swarms when told
  to — and the interesting question becomes whether it generalizes to a real user's goal. The
  minimal-injection question the investigation has handed to `trigger-prec` is exactly the right
  one. (`red-cd` is diffing what was actually injected.)
- One structural note: **the source repo has no `CLAUDE.md` at all**, so arm C is the only arm
  carrying that file. The *file*, not just the line, is the variable.

---

## What I did not attack

`red-rig` (rig soundness, arm comparability, plan-mode audit, missing-verdict audit), `red-cd`
(is C/D's fire a real swarm; what exactly was injected), and `red-pkg` (the nonce proof, and
whether "packaging is dead" was ever actually tested) were dispatched and had not reported when
this was written. Their findings should be folded in before `TRIGGER.md` ships. The plan-mode
audit matters most of the three: plan mode is known to suppress `Skill` invocation and already
burned one control — it needs ruling out by table, not by assumption.

---

## Addendum — the true arm (`trueB`), and how Claim 3 finally landed

After this review flipped the headline, the investigation ran the cell I specified: big goal,
rsync'd working-tree repo, pristine, **every** delegation affordance denied (`Task`, `Agent`,
`Workflow`, `TaskCreate/Update/Output` — absence verified in each `init` event; only
`SendMessage`, which cannot spawn, remained). No rate-limit kills.

**`trueB-3` fired, and it is the single cleanest artifact in the investigation.** The model
reasoned itself into the skill, verbatim:

> "`HERDR_ENV=1` and swarm is on PATH, so the swarm skill's requirements are met. Three
> independent, substantial, parallelizable bodies of work in a swarm-enabled project is
> **precisely the trigger condition for that skill** — let me load it rather than improvise."

Then `Skill{swarm}` → `swarm world` → journaled its seat-take → **spawned three children** →
journaled the dispatch. Disk confirms: four journals, three agents, children carrying real
briefs. **The shipped goal-shape trigger clause works, verbatim, once nothing else is in
reach.** That is precedence demonstrated *positively*.

**But the rate is unmeasurable, and must not be stated.** All three `trueB` runs were **killed
mid-flight**: no `result` event in any of them, no `.meta` exit-code file for any of them
(the probe writes one only on normal exit), event counts frozen at 46/39/46, and no `claude`
processes surviving. **The denominator is undefined.** "Fires ~1/3 under total denial" is one
fire out of three sessions that all died before finishing — the fourth time in this
investigation a number was scored off unfinished runs.

**The qualitative finding stands without a number, and is stronger than a rate would be:**

- `trueB-2` **explicitly saw swarm** — *"We're inside herdr and `swarm` is on PATH, so the
  fan-out is available"* — had **no other delegation tool in reach**, and worked inline anyway
  (no `.swarm/` on disk when it died).
- `trueB-1` never delegated at all; it was proving a real bug solo when it was killed.
- And in all six deny-`Task`-only runs, the model used **zero delegation tools of any kind** —
  it held `Workflow` and declined *both* it and the skill.

So the honest diagnosis, which the final `TRIGGER.md` adopts, is **precedence is necessary but
not sufficient**: a built-in fan-out tool is always closer to hand, *and* the model does not
reliably treat a goal's shape as reason to reach for a skill. Neither clean story ("the wording
is wrong" / "`Task` wins the race") is true alone.

---

## Recommendation

Ship Claims 1 and 4. They are sound and the fix is real.

**Do not ship Claim 3 as written.** Either run the all-delegation-denied cell specified above and
let the evidence decide, or reframe the headline to what the data actually supports:

> *The swarm skill does not fire on a goal's shape — not at any goal size, and not even when the
> model actively wants to delegate. When it wants a delegation tool it reaches for a built-in it
> already holds (`Agent`, or `Workflow`). Whether swarm loses that race or was never in it is
> **not yet established**: no arm has ever removed every built-in delegation affordance at once.*

That version is defensible, it is still surprising, and it does not hand a reader a `grep` that
knocks the whole report over.

---

## Post-review correction (added by `trigger-scout`, 2026-07-13) — one of this review's claims was later DISPROVED by experiment

`trigger-red` is closed and cannot amend its own file, so the correction is recorded here rather
than silently left to `TRIGGER.md`. **The review's verdicts all stand. One piece of its supporting
evidence does not.**

**The claim (this file, above, and pressed twice in the reviewer's messages):**

> *"In all six deny-`Task`-only runs, the model used **zero delegation tools of any kind** — it held
> `Workflow` and declined **both** it and the skill."* — offered as *"the strongest evidence in the
> document"* for the *not-sufficient* half, and recommended to the author as the thing to lean on.

**The disproof.** Those six runs are **small-goal** runs. The discriminating cell — the *same*
condition (`Task` denied, `Workflow` left standing, skill available; all verified in each `init`) on
a **big** goal, n=3 — shows the model **reaching for `Workflow` in all three**, and never
considering swarm:

> *"This is exactly the shape **Workflow** is built for… but per my instructions I can only invoke it
> if the user explicitly opts in."* · *"I'll use three separate **Workflow** orchestrations."* ·
> *"Do you want me to proceed with **`Workflow`** for these three tasks, or handle it solo?"*

**So the "zero delegation tools" figure is a lock, not a decline** — and doubly so: `Workflow` lay
dormant because the small goal wanted no delegation tool at all, **and** because `Workflow` requires
explicit **user opt-in**, so a model that actively wants it still emits **zero calls**. Neither the
reviewer nor the author knew that second mechanism; both were reading a zero in a tool-call count as
a decision.

**The conclusion the evidence was offered for — *precedence is necessary but not sufficient* — is
unchanged.** It rests instead on `trueB-2` (saw swarm, no other delegation tool in reach, worked
inline anyway) and `F_big_shipped` (0/3 under shipped conditions). `TRIGGER.md` §4 carries the full
account.

**The general lesson, which belongs with this review's other method notes:** *a zero in a tool-call
count is not a decision — it can be a decline, a dormancy, or a lock, and only the transcript
distinguishes them.* This investigation was burned four times by numbers that meant something other
than they appeared to mean; this was the fifth.
