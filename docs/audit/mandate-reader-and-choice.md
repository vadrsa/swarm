# mandate-reader-and-choice — is a recorded model-REASON load-bearing, and is there a choice to justify?

> SUPERSEDED by the shipped mandate; kept for the record (the analysis that shaped record-vs-journal placement and the in-flight wmd-haiku/wmd-opus natural-experiment discovery).

**Author:** `mr-reader`, reporting to `mandate-red`. **Status:** AUDIT — findings, cited.
**Written at** `swarm-dev/model-fit`, 2026-07-13. **Method:** read `bin/swarm` at the
source; grep the whole tree for record readers; read `MODEL-FIT.md` + `FLEET-EVAL*` +
`docs/audit/bench/`; forensics on the one genuinely-cheap pin in the swarm's history.

**Brief:** the operator proposes making `swarm spawn` require a model-choice REASON,
recorded in the agent record. Two questions decide whether that reason is WRITE-ONLY
(a field nobody reads = worthless) or LOAD-BEARING.

**The two answers, up front — they split.**

- **JOB 1 — IS THERE A READER? No. Confirmed, exhaustively.** Nothing reads `model`
  today. `swarm ps` — "the one view" — does not surface it. A reason recorded today
  would be seen by **nothing**, unless a human `cat`s the JSON. *But the fix is one
  line in one pure function.*
- **JOB 2 — IS THERE A CHOICE? Yes — a real menu, and a real, non-fabricated basis
  for a reason.** This is where the adversarial case **fails**, and I report that
  plainly. There is a run eval, a scored head-to-head, and an applicable a-priori
  rule. A mandated reason would not be fabricated.

**The finding that most sharpens the adversarial case is neither of those.** It is
that **`MODEL-FIT.md` §5 already rejected the record-field mechanism** and chose the
journal instead. See §5 below — that is the strongest version of my parent's case, and
it is not the one the brief was aiming at.

---

## 1. JOB 1 — the read paths, enumerated

The record `.swarm/agents/<name>.json` is written once (`bin/swarm:920-922`) with
fields `name, parent, pane, tab, model, cwd, task, ts`.

There are exactly **two accessors** and **five read sites**, all inside `bin/swarm`.
Nothing outside `bin/swarm` reads the record at all — I grepped the tree for
`.swarm/agents`, `agents/*.json`, `agent_rec_path`, and `load_agents`; the only other
hits are in `tests/`, which *construct* records rather than consume them. No hook, no
middleware, no `install.sh`, no `skill/`.

| # | Site | Function | Fields it actually touches |
|---|---|---|---|
| 1 | `bin/swarm:729` | stop-hook doorbell | `rec["pane"]` — **only** |
| 2 | `bin/swarm:692` | `deliver_once` → `parents_of()` | `parent` — **only** |
| 3 | `bin/swarm:727` | `next_delivery` → `parents_of()` | `parent` — **only** |
| 4 | `bin/swarm:985` | `cmd_send` | `parent` (for `relation()`) + name-existence |
| 5 | `bin/swarm:1053` | `cmd_ps` | hands whole records to `render_ps()` |
| 6 | `bin/swarm:1071` | `cmd_close` | `tab` / `pane` (to kill the pane) |

`parents_of()` (`:136-137`) is a one-line projection: it reads **`parent` and nothing
else**. So sites 2–4 are structurally incapable of seeing a new field.

**`render_ps` is the crux, and it is decisive.** `render_ps` (`bin/swarm:491-575`) is
the entire `swarm ps` view — a pure function that receives the full records. Its
complete agent-record surface is:

- `:515` `a.get("pane")` — liveness (`is_dead`)
- `:522`, `:526` `.get("parent")` — tree shape (`eff_parent`)
- `:545` the rendered line itself:
  ```python
  lines.append(f"{prefix}{branch}{name}{you} [{alive}] {q_of(name)} {idle}")
  ```
- `:548` optional `last:` line — but that comes from the **event** file
  (`event/<name>.json`), not the agent record.

**`model` never appears — not in `ps`, not in `send`, not in `close`, not in the
doorbell.** The string `"model"` occurs in the whole lifecycle only at the *write*
(`:922`) and in arg-parsing/help (`:851-852`, `:1105-1110`).

### VERDICT (Job 1): the EXISTING `model` field is ALREADY write-only.

If a `reason` were recorded today, **who or what would ever see it? Nothing.** There
is no read path. Not a human running `swarm ps`, not a parent inspecting its children,
not a hook. **Only someone who `cat`s `.swarm/agents/<name>.json` by hand.** And this
is not a hypothetical about the *new* field — it is already true of the `model` field
that has existed since the CLI did. We have shipped a write-only model field for 143
spawns and nobody noticed, which is itself the evidence for how much a record field
gets read: **zero.**

### The minimum change that gives it a reader

**One line, in one pure function: `render_ps` (`bin/swarm:491`).**

`render_ps` already receives the full `agents` records, so at `:539` (`a = agents[name]`)
the model is already in scope — no new parameter, no new plumbing, no signature change.
The walk-line at `:545` becomes something like:

```python
mdl = a.get("model") or "inherit"
lines.append(f"{prefix}{branch}{name}{you} [{alive}] {mdl} {q_of(name)} {idle}")
```

That is the whole cost of making the field load-bearing. `render_ps` is *pure and
offline-testable by design* (its own docstring: "Pure: every input is a plain value, so
it tests offline") — so this is a one-line change with a cheap test. **The
"nobody-reads-it" objection is real but it is one line deep.** An objection that costs
one line to answer is not a reason to kill a proposal; it is a reason to require the
line. If the mandate ships without touching `render_ps`, it is worthless. If it ships
with it, the objection evaporates.

---

## 2. JOB 2 — the real choice menu

`swarm spawn --model M` does **no validation whatsoever** (`bin/swarm:851-852`): it
takes the next argv token and passes it straight to `claude --model M` in the launcher
(`write_launcher`, `:834-835`). So the choice space is exactly the `claude` CLI's, and
`swarm` neither narrows nor checks it.

Per `claude --help`:

> `--model <model>  Model for the current session. Provide an alias for the latest
> model (e.g. 'fable', 'opus', or 'sonnet') or a model's full name (e.g.
> 'claude-fable-5').`

**The menu is real:**

- **Aliases:** `opus`, `sonnet`, `fable` (named in help), and `haiku` — the
  full-ID pin `claude-haiku-4-5-20251001` is *proven to work* by `wmd-haiku` (§4).
- **Full IDs:** `claude-opus-4-8`, `claude-sonnet-5`, `claude-haiku-4-5-20251001`,
  `claude-fable-5`.

This is a genuine menu spanning a large cost/capability range, not a one-item list.
**A parent asked to choose has something real to choose between.** (Caveat worth
flagging to the operator: because `spawn` does not validate, a typo like
`--model spnnet` is recorded verbatim and fails only later, inside the child's
`claude` invocation. That is an independent bug, not an argument about the mandate.)

---

## 3. JOB 2 — the fit-evidence inventory: is a reason INFORMED or FABRICATED?

**This is where the adversarial case fails, and I will not shade it.** The brief's
hypothesis was: *if no fit data exists, a mandatory reason forces agents to fabricate
justification.* **Fit data exists.** The repo has run the experiment.

### (a) MEASUREMENT — real runs, real artifacts, real scores

`docs/audit/bench/` is **not a design; it is a rig that was executed.** It contains a
runner (`run-cell.sh`, `run-cell-v3.sh`), briefs (`fleet-briefs-v1/ v2/ v3/`), a rubric
(`fleet-rubric-v1.md`), a scoring audit (`SCORING-AUDIT-V3.md`), and **six results
files with actual outcomes** — `results-claude-base.md`, `results-deepseek.md`,
`results-glm.md`, and the v3 set. `FLEET-EVAL-V3.md:23-27` carries the scored
head-to-head across four dimensions:

| Model | D1 duties | D2 delegation | D3 tool/CLI | D4 long-horizon |
|---|---|---|---|---|
| deepseek-chat | 5/5 PASS | 8/10 FAIL | 11/17 FAIL | 3/6 FAIL |
| GLM-4.7 | 5/5 PASS | 7/10 FAIL | 14/17 PARTIAL | 3/6 FAIL |
| claude-native (anchor) | 5/5 PASS | 10/10 PASS | 17/17 PASS | 6/6 PASS |

And it was **adversarially reviewed** — `FLEET-EVAL-RED.md`, `FLEET-EVAL-V3-RED.md`,
which flipped verdicts. This is measurement, with a control arm and a red team.

**What it measured is the load-bearing part.** The weaker models were *not stupid* —
GLM was graded an "excellent tool-user" whose commands were "well-formed all battery
long" (`FLEET-EVAL-V3.md:96-98`). They failed the **seat**, not the thinking:
deepseek "knows who its parent is and does not use the verb" (`:76-78`); neither wrote
its plan to the journal (D4 FAIL both); both substituted a broken MCP door for
`swarm send` while "the Claude control had the same doors open and took them 0 times
in 7 probes" (`:117-125`). **The degradation is in protocol and self-governance, not
domain reasoning.** That is a genuine, non-obvious, empirically-discovered axis — and
it is exactly the axis a parent needs to reason about when picking a child's model.

### (b) The honest limit — the eval measured the WRONG MODELS for the question asked

The eval scored **deepseek-chat and GLM-4.7 through `opencode run`**, against an anchor
that is *native Claude, unpinned* (i.e. Opus). **No Sonnet cell and no Haiku cell was
ever run in this battery.** Every `haiku`/`sonnet` string in `docs/audit/bench/` is a
*proposed* baseline that never happened — `fleet-rubric-v1.md:348` literally carries a
results row `| claude-haiku (base) | ... | ... | ... |` with the ellipses never filled,
blocked on an OpenRouter key (`results-v3-claude-base.md:9-10`: "§5a's same-harness
Claude cell is still not reachable — no OpenRouter key").

MODEL-FIT.md marks this against itself, unprompted:

> "**I am not claiming Haiku behaves like GLM.** I am taking the *axis* the eval
> discovered — that seat-holding fails before reasoning does — and I am declining to
> assume the axis vanishes inside the Claude family. That is a directional read, and I
> mark it as one."

and `:274-276`: **"the eval watched DeepSeek and GLM, not Sonnet and Haiku. I extended
an *axis*, not a measurement."** Rung 3's specific claim is flagged `:191`
**"(Directional, from watching this tree; I have not benchmarked it.)"**

**One fair hit on the doc:** its §2 heading — *"What the field actually says (this is
not reasoned from priors)"* (`MODEL-FIT.md:55`) — is an overreach, because §7 concedes
the Sonnet/Haiku extension **is** reasoned from priors. The body walks the heading back;
the heading should be fixed. (To the doc's credit, it *refuses* to fabricate where it
has nothing: `:194-198` declines to give `claude-fable-5` a rung because "a rule that
assigns a model a job it has not been watched doing is exactly the confident-wrong
artifact this whole document exists to prevent." That is the right instinct, applied
inconsistently — Rungs 2 and 3 assign Sonnet and Haiku jobs they have not been watched
doing either.)

**So: the rule's *axis* is earned by measurement; the rule's *thresholds* — where
Sonnet stops and Haiku starts — are assertion.** A parent choosing `sonnet` today is
extrapolating across a Claude-vs-Chinese/harness confound the eval names as its own
headline caveat (`FLEET-EVAL-V3.md:41-44`, 54: "REMAINS").

**And the missing experiment is cheap.** MODEL-FIT §7 (`:293-299`) names it exactly:
"Run two more cells — `claude-sonnet-5` and `claude-haiku-4-5-20251001` — through the
**same** battery, and the confound that caveats this whole document **collapses**… a few
hours of rig time on a rig that is already built." **The rig exists. Nobody has run it.**
That is the real gap — and it is a reason to run the eval, not a reason to say reasons
would be *fabricated*.

### (c) The DECISION RULE — and why it is applicable without measurement

`MODEL-FIT.md` §1 gives a parent an actual rule, not a vibe. The axis, verbatim:

> **Can I cheaply tell that this child was wrong?**

with a three-question ladder (seat-holding → Opus; adopted judgment → Opus;
mechanically checkable → Sonnet/Haiku; **fall-through → Opus**). Its justification is
an asymmetry, not a benchmark: "Model spend is bounded and known at spawn.
Confident-wrong work is unbounded."

**This is the finding that decides Job 2.** The ladder is **answerable from the task
description alone** — a parent writing a brief already knows whether the child will
spawn and judge (rung 1), whether it will hand back judgment the parent intends to
adopt (rung 2), or whether the answer is a count/list/grep the parent can check in
seconds (rung 3). **No measurement is required to apply it.** It is a-priori reasoning
about *checkability*, and checkability is a property of the brief the parent is
writing at that very moment.

### VERDICT (Job 3-way question): **informed by an applicable a-priori heuristic, backed by a real (if out-of-family) eval — NOT fabricated.**

The brief's sharpest hypothetical — *a mandate forces agents to invent justification
for a choice they cannot inform* — **does not survive contact with the repo.** A parent
asked "why this model?" can answer from the ladder, honestly, in one clause, without
inventing anything. The reason would be *thin* (a rung, not a number), and it would be
extrapolating across the harness confound — but thin-and-honest is not fabricated.

---

## 4. The one real data point: `wmd-haiku` — and it is IN FLIGHT, not history

**The brief's premise was off in two ways, and both corrections cut against the
adversarial case.** Five records carry a non-empty `model` — but four are `"opus"`
(a pin to the model that was *already* the inherited default: a no-op pin). **Exactly
one is a genuinely cheap pin:**

```
.swarm/agents/wmd-haiku.json
  "model":  "claude-haiku-4-5-20251001"
  "parent": "weak-model-deleg"          # "weak model delegation"
```

### 4a. The parent who chose DID record a reason — a pre-registered one

This is the single most important fact for the operator's proposal, and it **destroys**
the "a mandated reason would be fabricated" hypothesis at its one available data point.
`weak-model-deleg` did not guess. It ran a **controlled A/B with a pre-declared
threshold**, and wrote the reason down before the run:

- **The reason traces to the human's own `idk`**, quoted in the parent's task record:
  *"we should research how we make sure a haiku model doesn't start delegating too
  much, if it can't keep up with the complexity of the task. or maybe it's ok, idk."*
  The pin is the **independent variable of an experiment** — the most defensible reason
  a model choice can have.
- **A byte-identical control arm exists:** `wmd-opus` (`"model": ""`, inherited Opus)
  got the same task, differing only in the report path. One variable.
- **A threshold declared *before* the run**, in `.swarm/journal/weak-model-deleg.md`:
  *"OVER-DELEGATION THRESHOLD, declared BEFORE the run so I can't move it"* — and a
  falsifier for the experiment itself (*"if the task turns out to be rigged…then the
  arms don't discriminate and I have measured nothing"*).

**The one parent in 143 spawns who made a real model choice had a real, written,
pre-registered reason.** A mandate would have cost that parent nothing — it was
*already* doing what the mandate asks.

### 4b. The outcome so far: the feared failure did NOT happen; a worse one may be happening

**The experiment is still running** (both arms live at the time of this audit). There is
**no verdict**. But the state is legible, and it is not the state anyone predicted:

| Observable | `wmd-haiku` (Haiku 4.5) | `wmd-opus` (control) |
|---|---|---|
| Report artifact | **absent** | delivered, ~25KB |
| Children spawned | **0** | 0 |
| Journal after spawn | **nothing** | full substantive entry |
| `swarm send` to parent | **never sent** | sent |
| Last sign of life | *"…begin the analysis. I have all four documents now."* then **silence** | *"Report delivered."* |

**The over-delegation fear did not materialize** — Haiku spawned zero children; it did
not escape the task by delegating. **But the *other* known weak-model failure is what
the record shows: it dropped the protocol.** No journal, no `swarm send`, no artifact —
the exact FLEET-EVAL-V3 signature ("knows who its parent is and does not use the verb";
journaled nowhere). The Opus control not only delivered but **explained its own
non-delegation** — *"Did not delegate, deliberately… the verdicts ARE the deliverable"* —
which is seat-holding working.

**This is MODEL-FIT.md §7's own pre-registered falsifier for Rung 3, coming true:**

> "**Falsifier for Rung 3 (Haiku/Sonnet on leaves):** a Sonnet or Haiku leaf whose
> *artifact* is fine but whose **seat behavior** fails the way the eval's models failed
> — narrates its report instead of `swarm send`-ing it, never journals, does not
> terminate. If that shows up, Rung 3 is wrong **not because the model can't count, but
> because it can't be a swarm agent**."

(Unconfirmed — the agent is live and could still deliver. But this is what the record
shows, and it is the in-family evidence §3b said was missing. It is arriving *now*.)

### 4c. And it is about to be lost

**Nothing about this experiment is written in `docs/`.** It lives in untracked journals,
two unread queue messages, and — for its only artifact — **`/private/tmp`**, the OS temp
dir, which does not survive a reboot. Meanwhile `docs/design/MODEL-FIT.md` is committed
with Rung 3 shipped but its central safety claim explicitly untested and blocked on this
very report. **The swarm's only real model-choice experiment is one cleanup away from
evaporating.** I flag this to `mandate-red` as urgent and out-of-scope for me: someone
should get `weak-model-deleg` to decide the Haiku arm and write the result into
`docs/audit/`, not `/private/tmp`.

### 4d. The census the mandate targets is real

MODEL-FIT reports independently: **"142 of 143 agents took the inherited default;
exactly one was ever pinned"** — "not a decision anyone made. It is a decision nobody
made, 143 times." My independent grep of `.swarm/agents/*.json` reproduces it (the four
`"opus"` pins are no-ops against the default). **The problem the mandate targets is real
and it is counted.**

---

## 5. The strongest form of the adversarial case (and it is not the one I was sent to find)

The brief framed the attack as *"a recorded reason is write-only, therefore
worthless."* Job 1 confirms the write-only half — but the fix is one line, so that
attack is weak on its own. **The genuinely strong objection is this:**

**`MODEL-FIT.md` §5 already considered the enforcement question and did not choose a
record field.** It chose the **journal**:

> "**Say it at the spawn.** The doctrine is one line in the parent's journal:
> `spawned <name> on <model> — <the clause>`. That is the whole enforcement mechanism,
> and it is enough: it makes the choice inspectable, which is how everything else in
> this repo is judged."

and its wiring section names exactly two touch-points — **`skill/SKILL.md` doctrine**
and **`swarm spawn` help / `swarm world`** — closing with:

> "Neither builds a classifier. Both make the choice **visible and inspectable**, which
> is the only enforcement this repo has ever used, and the only one it needs."

Note also that the help text **already ships the mandate as a norm** (`bin/swarm:1105-1110`):

> "`--model` is a CHOICE, not a default to inherit: ask 'can I cheaply tell this child
> was wrong?' Seats and adopted judgment -> the strong model; mechanically-checkable
> work -> a cheap one. **Say why in your journal.** (docs/design/MODEL-FIT.md)"

**So the operator's proposal is not new doctrine — it is a proposal to move an
existing "say why in your journal" norm into an enforced record field.** The
adversarial question that actually bites is therefore:

> **What does the record field buy that the journal line does not?** The journal is
> already read — by the parent judging the child, by a restore, by a human reading the
> tree. The record is read by *nothing*. Moving the reason from a medium that is read
> into a medium that is not read is a **downgrade**, unless `render_ps` is changed in
> the same commit.

That is the case I would put to the operator. It does not say "don't require a
reason" — the census (143 unchosen spawns) says the requirement is warranted, and §3
says a parent can answer honestly. It says: **requiring a reason is right; recording it
where nothing reads it is the part that is worthless.**

---

## 6. What I recommend the mandate must include, to not be write-only

1. **Touch `render_ps` (`bin/swarm:491`, the walk-line at `:545`) in the same commit.**
   One line. Without it, both `model` and `reason` are write-only and the field is
   decoration. This is the load-bearing requirement.
2. **Prefer/keep the journal line** (`spawned <name> on <model> — <clause>`), which
   already has readers, and treat the record field as the *machine-inspectable*
   companion — not the replacement.
3. **Validate `--model` at spawn** (`bin/swarm:851`) — currently a typo is recorded
   verbatim and fails inside the child. Independent of the mandate, but adjacent.
4. **Run the in-family eval — the rig already exists.** The one real gap is Sonnet/Haiku
   on a swarm seat. MODEL-FIT §7 (`:293-299`) says two more cells through the built
   battery collapse the confound in "a few hours of rig time." Until then, every reason
   is a rung, not a number — honest, but thin.
5. **Rescue `weak-model-deleg`'s experiment before it evaporates** (§4c) — its only
   artifact is in `/private/tmp`. This is the urgent one.

### The failure mode to actually guard against

**It is not fabrication. It is a parent obeying Rung 3 and getting burned.** The
realistic bad outcome is a parent writing an *honest* reason — *"cheap: mechanically
checkable"* — choosing Haiku on Rung 3's authority, and receiving a child that reasons
fine but **never reports, never journals, and idles silently**. The repo has now watched
that shape twice: once measured and reviewed (deepseek/GLM), and once — provisionally,
n=1, live — in `wmd-haiku`. A mandate that makes parents *cite* Rung 3 while Rung 3's
Haiku band is unbenchmarked would propagate an untested claim under the appearance of
diligence. **The mandate should therefore ship with the eval, or ship with Rung 3
explicitly marked "directional, unbenchmarked" at the point of decision.**

---

## 7. Falsifiers — what would show me wrong

- **Job 1 (write-only):** a reader of `agents/*.json` outside `bin/swarm` — a hook, the
  skill, `install.sh`, a middleware that parses the record. I grepped the tree for
  `.swarm/agents`, `agent_rec_path`, `load_agents`; hits landed only in `bin/swarm` and
  `tests/`. Find one such reader and my write-only verdict collapses.
- **Job 2 (informed, not fabricated):** show that the three-question ladder is *not*
  answerable from a brief the parent is writing — i.e. produce a real spawn where the
  parent genuinely cannot tell whether the child holds a seat, hands back adopted
  judgment, or returns a mechanically-checkable answer. If the ladder cannot be applied
  a priori, then reasons *would* be fabricated and the adversarial case wins.
- **§5 (the journal beats the record):** show a consumer that needs the reason
  *machine-readable* — something that must parse it rather than read it. If one exists,
  the record field earns its place independent of `render_ps`.
