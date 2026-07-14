# OPERATOR-STRUCTURE-FIX — the root session is not the operator

> SUPERSEDED by OPERATOR-STRUCTURE.md, which retracts the root-naming fix wholesale; kept for the record (the clearest "real reversal" case in the corpus — a 9-hunk diff was built, tested 79/80 green, run, and then abandoned once RED2 showed it fixed rendering, not attention).

Author: `structure-mech`, 2026-07-12. For: `operator-structure-scout`.
Companion to `docs/audit/structure-mechanics-2026-07-12.md` (the mechanics probe; every
`bin/swarm:NNN` here was verified there) and `docs/audit/field-evidence-doctrine-2026-07-12-RED.md`
(dp-red R3, which named the bug).

**Recommendation: fix (a), by the (a3) implementation — the root session names itself,
lazily, in `my_name()`, via a file that `spawn` writes on first use.** It is a bug fix,
not a new concept; it costs **0 verbs, 0 concepts, 1 file, ~14 lines**; it makes the flat
row *unrepresentable* rather than *discouraged*; and it breaks neither the ~90 existing
records nor the live tree. Fix (b) is cheap and honest but cannot deliver the guarantee —
I cost it fully below and explain exactly where it fails.

The rest of this document is the argument, the blast radius, the diff, and the migration.

---

## 0. The bug, stated once, in the code's own terms

`WORLD.md:57` promises:

> - **The operator is a mailbox, not a node.** Messages to `operator` wait until
>   the human looks; `ps` shows them waiting.

`bin/swarm:63-64` breaks that promise:

```python
def my_name():
    return os.environ.get("SWARM_AGENT_ID") or "operator"
```

A session with no `SWARM_AGENT_ID` — i.e. the root session, the human's hand — **is
named `operator`**. So `operator` is simultaneously (i) the human's mailbox, (ii) the
"no parent" sentinel (`parents_of`, `:133`; `roots = kids.get("operator")`, `:553`), and
(iii) the *identity of a live Claude session that spawns things*. Three roles, one string.

The consequence, from `bin/swarm:869` + `:921`:

```python
    parent = my_name()                                    # :869 → "operator"
    write_atomic(agent_rec_path(root, name), json.dumps(
        {"name": name, "parent": parent, ...}))           # :921 → "parent": "operator"
```

**A root session cannot write any parent but `operator`.** There is no flag (`:845-853`
accepts only `--model`/`--cwd` and dies otherwise). So "human → flat row of workers" is
not a shape the model *chose*; it is **the only shape the tool can represent** from a
fresh session. dp-red R3 is right, and my probe confirms it independently: the doctrine
was never given a chance to fail or succeed.

This is the whole bug. Everything below is about which of two repairs to make.

---

## 1. THE CONCEPT QUESTION — is a named root a 10th concept?

My parent's read: *"the operator-is-a-mailbox concept ALREADY says the root session isn't
the operator; the code just never implemented it — that is a BUG FIX, not a concept.
Test that argument, don't just agree with it."*

**I tested it. It survives — but not for the reason given, and the distinction matters.**

### The argument as posed is *almost* circular

"The mailbox concept already says the root session isn't the operator" is doing work the
text does not quite do. `WORLD.md:57` says the operator is a mailbox rather than a node.
It does **not** say "and therefore the human's Claude session is a separate, named thing."
A reader could consistently hold: *the operator is a mailbox, AND the root session is the
operator, AND the operator therefore both has a mailbox and spawns children* — which is
precisely what the code does today. The sentence alone doesn't forbid it.

So I can't rest on `:57` by itself. But the concept list settles it two lines earlier.

### The argument that actually holds: concept 1 already entails it

`WORLD.md:9-10`, concept 1:

> 1. **Agent** — a Claude session in a herdr pane, with a **name**, a **parent**,
>    and a **journal**. The pane is ground truth; anyone may read anyone's pane.

The root session **is a Claude session in a herdr pane**. By concept 1 it therefore *is an
agent*, and an agent *has a name, a parent, and a journal*. Today it has:

- a **journal** — `.swarm/journal/operator.md` exists, 55 KB, actively written (probe Q7);
- a **name** — `operator`, but one it *shares with the mailbox*;
- a **parent** — none, and none is representable.

**The root session is already an Agent under concept 1.** It is simply a *malformed* one:
its name collides with the mailbox and its parent is missing. Naming it does not add a
concept — it makes an existing instance of concept 1 **well-formed**. The 55 KB journal is
the proof: the repo has been *treating* the root session as an agent (journal, seat, open
loops) for its whole history, while the tool refused to give it a name.

The `skill/SKILL.md:53-56` text says the same thing out loud, and calls the gap by name:

> A session acting for the human at the root — reading the operator mailbox,
> dispatching, judging — is a **hand** on the operator seat. The seat is the
> standing thing: one journal (`.swarm/journal/operator.md`), one mailbox, one
> set of open loops. Hands come and go...

"Hands come and go" is *exactly* "a session with a name and a lifetime, distinct from the
standing mailbox." SKILL.md invented the hand concept **because the tool wouldn't provide
it** — and then had to implement it as pure convention (probe Q7: `bin/swarm` never writes
`journal/operator.md`; all three hooks `sys.exit(0)` for operator at `:687`, `:705`, `:740`).

**Verdict: BUG FIX, not a concept.** Concept count stays at **9**. The stronger claim —
"the mailbox sentence already implies it" — is weaker than it looks; use concept 1 instead.
A named root is the *first correct instance* of concept 1 at the root, plus the deletion of
a hand-rolled workaround (the "hand" convention) that existed only to paper over its absence.

### The honest cost of that argument

`WORLD.md` gets **one clarifying sentence** and one word changed (§5 below). If the reviewer
insists that any WORLD.md edit = a concept change, then (a) costs 1 concept and I would
still recommend it — but I do not think that's the right accounting, because the edit
*removes* an exception rather than adding a rule.

---

## 2. FIX (a) — ROOT GETS A DISTINCT NAME. Full cost.

**The idea:** the root session is a *child of the human*, not the human. It gets its own
name and its own node. `human → [w1, w2, w3]` becomes unrepresentable, because a root
session can no longer write `parent: operator` — it writes `parent: <its own name>`.

### 2a. Where does the name come from? (The hard question.)

The root session **cannot be spawned** — nobody runs `spawn` for it; the human opens a
terminal and types. So the name cannot come from spawn's argv. Three sub-options:

| | how the root gets its name | new verb? | fails when |
|---|---|---|---|
| **a1** | human exports `SWARM_AGENT_ID=desk-a` before `claude` | no (works TODAY — probe Q2) | the human forgets. Silent, total regression to the current bug. **Unenforceable.** |
| **a2** | new verb `swarm take <name>` writes the root's record + prints the export | **YES (+1 verb → 5)** | the human forgets to run it. Same failure, now with a verb to pay for. |
| **a3** | **`my_name()` self-names lazily, persisting to a file; `spawn` is what forces it** | **no** | — |

**a1 and a2 both fail on the same thing: they are opt-in.** The bug is that the *default*
is wrong. A fix whose correct path requires the human to remember an extra step leaves the
default broken, and the default is what the field evidence caught. And a2 spends a verb
(4 → 5, a 25% increase in the repo's scarcest currency) to buy nothing a1 doesn't already
give for free.

**So: a3.** The root names itself, on demand, at the only moment its name can matter.

The key insight from the probe: **`SWARM_AGENT_ID` has exactly one reader** —

```
$ grep -n SWARM_AGENT_ID bin/swarm
64:    return os.environ.get("SWARM_AGENT_ID") or "operator"     # the ONLY reader
907:  ... "--env", f"SWARM_AGENT_ID={name}"])                    # writer: spawn's tab
1022:  env = {**os.environ, "SWARM_AGENT_ID": identity, ...}     # writer: middleware
```

One reader. That is the whole seam. Change what `my_name()` returns when the env var is
absent, and *every* call site — spawn's `parent = my_name()` (`:869`), the three hook gates
(`:687`,`:705`,`:740`), `relation()` (`:165`), `ps`'s `(you)` marker (`:1063`) — follows,
with no other edit.

**The name itself:** `root-<n>`, the lowest free integer (`root-1`, `root-2`, …), matching
`NAME_RE` (`:29`) and claimed through the *existing* tombstone mechanism (`claim_name`,
`:764-767`) so two concurrent root sessions cannot collide. Persisted to
`.swarm/settings/root.id` so a *restarted* root session in the same terminal reads back the
same name instead of burning a new one.

**Crucially: the root record is written lazily — only when a root session actually spawns.**
A human who opens a terminal to run `swarm ps` and nothing else creates no node, no journal,
no clutter. **The first spawn is what brings the root node into existence**, which is exactly
the moment the tree needs it. This is why a3 needs no verb: `spawn` already exists and is
already the only event that can create structure.

### 2b. Blast radius — every site, honestly

I traced all seven sites my parent named, plus three they didn't.

| # | site | today | under (a3) | verdict |
|---|---|---|---|---|
| 1 | `my_name()` `:64` | `env or "operator"` | `env or root_name(root)` | **the change** |
| 2 | `parents_of()` `:133` | `a.get("parent") or "operator"` | **unchanged** | ✅ still correct — a record with a blank parent is still a human-rooted orphan |
| 3 | `roots = kids.get("operator")` `:553` | root-level = children of operator | **unchanged** | ✅ `root-1`'s own record has `parent: "operator"`, so `root-1` IS the single root line. Workers hang under it. **This is the fix, visible.** |
| 4 | hook gate: `deliver` `:687` | `if my_name()=="operator": sys.exit(0)` | → `if my_name() in ("", "operator")` | ✅ **resolved in §7d.** Harmless: hooks are wired only into the *child's* settings file, so these never fire in a root session at all. **NB: my first draft gated on the agent *record* (`is_agent()`) — the test suite proved that a real defect (silent mail loss); gate on the NAME.** |
| 5 | hook gate: `event` `:705` | same | same | ✅ same |
| 6 | hook gate: `restore` `:740` | same | same | ✅ same |
| 7 | `spawn_header` `parent_desc` `:772-773` | `"the human operator" if parent=="operator"` | **unchanged code**, new behavior: a worker spawned by `root-1` is now told *"your parent: agent `root-1`"* | ✅ **desirable** — today it lies to the worker, telling it the human judges its work when in fact a Claude session does |
| 8 | reserved names `:861` | `if name in ("operator","delivered"): die` | **add `root-*` prefix guard** | ✅ 1 line |
| 9 | human's mailbox `queue/operator/` | `send operator` queues here | **unchanged** | ✅ mailbox stays exactly put — this is the point: mailbox and session are now *different names* |
| 10 | `subtree()` `:579-582` (close) | walks recorded edges | **unchanged** | ✅ `swarm close root-1` now closes the whole tree — a new, sane capability |
| 11 | `relation()` `:165` `if sender=="operator"` | root session's sends are headed "the OPERATOR (the human at the root)" | now headed **"your parent"** | ✅ **more truthful.** But see the caveat in 2c. |
| 12 | `render_ps` `me_name` `:537` | `(you)` never shows for root | root sees `(you)` on its own line | ✅ pure gain |

### 2c. The hazard, named plainly: the three hook gates

**This is the one place fix (a) can go wrong, and my parent was right to flag it.**

The gates at `:687`, `:705`, `:740` exist because the operator has **no settings file, no
pane it owns, and no hooks wired**. Under (a3), `my_name()` returns `root-1`, the gates stop
firing... **and nothing happens.** Here is why it is safe, from the code:

The hooks are not ambient. They only run because `cmd_spawn` *wires them into the child's
settings file* (`:889-895`):

```python
    settings = os.path.join(sdir, f"{name}.json")
    write_atomic(settings, json.dumps({"hooks": {
        "UserPromptSubmit": [h("deliver")],
        "Stop": [h("event stop")],
        ...
```

and the child is launched with `claude --settings <that file>` (`:834`). **The root session
was never launched with a swarm settings file** — the human just ran `claude`. So the root
session **has no `UserPromptSubmit`/`Stop`/`SessionStart` hooks pointing at `bin/swarm` at
all.** `cmd_deliver` is never *invoked* in a root session, so it does not matter what its
gate would decide.

**The gates are therefore dead code in the root path — belt-and-braces, not load-bearing.**
The falsifier is precise: if a human *did* run `claude --settings .swarm/settings/root-1.json`,
the hooks would fire. Nothing creates that file under (a3) — spawn only writes
`settings/<child>.json` — so the situation cannot arise by accident.

**But I recommend keeping the gates and re-pointing them at the mailbox anyway:**

```python
    if my_name() == "operator":     →     if not is_agent(root, my_name()):
```

i.e. *"if I have no agent record, I have no hooks to service."* This is strictly safer than
today (it also protects a hand-set `SWARM_AGENT_ID=typo`), costs 3 line-edits + 2 lines for
`is_agent()`, and — importantly — it means **a root session that DOES get a settings file
later (a future `swarm take`) would work correctly rather than silently no-op.** It removes
an exception instead of adding one.

> **Honest residual risk.** If `root-1` ever *did* acquire an agent record AND a settings
> file, it would start receiving queued mail one-per-turn — which is correct and desirable,
> but is a live behavior change. Under the minimum diff below, `root-1` **gets an agent
> record** (that's what makes `ps` render it) but **no settings file**. So: record yes,
> hooks no. `swarm send root-1 "..."` would queue a file that nothing delivers. That is a
> real wart, and I state it rather than hide it — see §7, Known wart.

### 2d. What (a) buys that (b) cannot

**Unrepresentability.** After (a3), a root session's `parent = my_name()` returns `root-1`,
so **every** child it spawns is recorded `parent: root-1`. `kids["operator"] == ["root-1"]`.
The human has exactly one direct child, **by construction, with no rule, no warning, no
override, and nothing for a model to reason its way around.** The flat row is not
discouraged; it *cannot be written*. That is the difference between a fix and a nudge, and
it is the entire reason to prefer (a) despite its larger diff.

---

## 3. FIX (b) — SPAWN-GUARD. Full cost, and why I do not recommend it.

**The rule, exactly:** in `cmd_spawn`, after `parent = my_name()` (`:869`) and before
`claim_name` (`:873`):

> If `parent == "operator"` and the count of existing records with `parent == "operator"`
> is `>= 1`, refuse — unless `--flat` is passed.

```python
    # (b) — after :869
    if parent == "operator":
        flat = [n for n, a in load_agents(root).items()
                if (a.get("parent") or "operator") == "operator"]
        if flat and "--flat" not in argv:
            die(f"you already have {len(flat)} direct child(ren) of the human "
                f"({', '.join(sorted(flat))}). A root session is the human's "
                f"COORDINATOR, not the human: spawn workers under an existing "
                f"child, or pass --flat if you truly mean to hand the human a "
                f"{len(flat)+1}-wide row.")
```

**Cost:** 0 verbs, 0 concepts, ~8 lines, +1 flag on `spawn` (`--flat`), 0 new state. It is
genuinely cheap and I would ship it tomorrow if (a) were unavailable.

**Three reasons it is the wrong fix.**

1. **It cannot enforce what it asks for.** The message says *"spawn workers under an
   existing child."* **A root session cannot do that.** `parent = my_name()` is `operator`,
   full stop (`:869`, `:64`) — there is no `--parent` flag (`:845-853`). The guard therefore
   refuses the only action the session is *capable of taking* and advises an action it is
   *incapable of taking*. The session's sole escape is `--flat`... which is the bug. **A rule
   whose compliant path is unrepresentable is not a rule; it is a wall with a door marked
   "violate me."** This is the decisive objection and it comes straight from the mechanics.
   *(The compliant path does exist for a **spawned** session — `coordinator` spawning under
   itself works fine today. But the failure mode dp-red caught is specifically the **root**
   session's first spawns, where it does not.)*

2. **The override is indistinguishable from the failure.** My parent asked how (b)
   distinguishes "the human deliberately wants 3 workers" from the failure mode. **It
   cannot** — and worse, the field evidence shows *the sessions sincerely believed they were
   compliant* (dp-red R4: run 3 "reasoned explicitly about the coordinator layer and decided
   against it, citing doctrine 5"). A session that reasons its way to `--flat` while quoting
   the doctrine at itself has satisfied the guard and reproduced the bug. Guards stop
   *accidents*; this is a *sincere, reasoned* wrong turn.

3. **It leaves the data model broken.** `operator` still means three things. Every future
   feature that walks the tree still has to special-case the root. The `hand` convention in
   SKILL.md still has to exist. We would be paying to *preserve* the conflation.

**(b) is a lint. The bug is a type error.**

---

## 4. IS THERE A THIRD FIX? Yes — and it is (a3), which is why I recommend it.

My parent invited a third option. (a3) *is* that third option: it is neither "a1/a2
name-the-root-by-hand" (opt-in, unenforceable, and a2 costs a verb) nor "(b) guard the
spawn" (a lint over a broken model). It gets **(a)'s guarantee at (b)'s implementation
cost**, by exploiting the one-reader seam at `my_name()`.

I also considered and **rejected** a fourth: *make `parents_of`/`render_ps` treat the root
session's children as grandchildren by rewriting the view.* Rejected outright — it makes
`ps` lie about the files, which is the one thing this repo will not do
(`WORLD.md:3-5`: *"Everything the system stores is a fact a file can witness"*).

---

## 5. WORLD.md RECONCILIATION — the exact diff

**Affected sentences.** Two, quoted exactly.

`WORLD.md:11-13`, concept 2:

> 2. **The tree** — your parent judges and approves your work; you judge your
>    children's. The human **operator** roots the tree. Who may message whom is
>    judgment, not a rule engine.

`WORLD.md:57-61`, the promise:

> - **The operator is a mailbox, not a node.** Messages to `operator` wait until
>   the human looks; `ps` shows them waiting. Nothing pushes to the human, and
>   nothing ever refuses a message to the operator. ...

**Does the fix require an edit? Yes — one sentence, and it *strengthens* an existing
promise rather than adding one.** `WORLD.md:57` is currently **false in the code**: the
operator IS a node, because a live session answers to that name and spawns children as it.
The diff makes the text true.

```diff
--- a/WORLD.md
+++ b/WORLD.md
@@ -9,9 +9,11 @@
 1. **Agent** — a Claude session in a herdr pane, with a **name**, a **parent**,
    and a **journal**. The pane is ground truth; anyone may read anyone's pane.
 2. **The tree** — your parent judges and approves your work; you judge your
-   children's. The human **operator** roots the tree. Who may message whom is
-   judgment, not a rule engine.
+   children's. The human **operator** roots the tree — as a mailbox, never as an
+   agent: the session the human types into is itself an agent (`root-1`, `root-2`,
+   …, named on its first spawn), so the human's direct children are the root
+   sessions, and everything else hangs under one of them. Who may message whom is
+   judgment, not a rule engine.
 3. **`swarm spawn <name> "<task>"`** — create a child. The name is chosen, not
```

and, at `:57`, one clause:

```diff
-- **The operator is a mailbox, not a node.** Messages to `operator` wait until
-  the human looks; `ps` shows them waiting. Nothing pushes to the human, and
+- **The operator is a mailbox, not a node.** No session is ever named `operator`
+  — the human's own session is an agent like any other. Messages to `operator`
+  wait until the human looks; `ps` shows them waiting. Nothing pushes to the human, and
   nothing ever refuses a message to the operator. The operator queue alone is
```

**Concept count: still 9.** Line 3's *"Nine concepts, four verbs"* is **unchanged** — no new
verb, no new concept. The edit is confined to concept 2's body (which already claimed the
human roots the tree; it now says *how*) and to making the `:57` promise true. Per §1: this
is the repair of concept 1's first instance, not a tenth concept.

**`skill/SKILL.md` also gets simpler** (not required for the fix, but it is the payoff):
the "hand" convention (`:52-75`) exists *only* to hand-roll what the tool now provides. A
follow-up can collapse it — the seat's journal becomes `journal/root-1.md`, written by the
tool's own `claim_name`, and "hands come and go" becomes "root sessions come and go, and
each has a name." **That is a net deletion of doctrine**, which is the strongest possible
sign this is a bug fix and not a feature.

---

## 6. MIGRATION / COMPAT — the ~90 existing records and the live tree

I checked this against the actual `.swarm/` (90 records, 23 with `parent: "operator"`).

| question | answer | why, from the code |
|---|---|---|
| Do the ~90 existing `agents/*.json` break? | **No. Not one is modified or read differently.** | `load_agents` (`:119-131`) reads whatever is on disk. `parents_of` (`:133`) still defaults a blank parent to `operator`. An old record saying `parent: "operator"` still means "direct child of the human" — which is exactly what it meant when written, and still true. **The fix is forward-only: it changes what NEW root sessions write, never how OLD records are read.** |
| Does `ps` still render? | **Yes, identically for the existing tree.** | `roots = kids.get("operator")` (`:553`) is unchanged. Today's 23 flat agents keep rendering as 23 root lines. After the fix, a *new* root session adds one more root line (`root-1`) with its workers nested beneath. Old and new coexist in one view with no special-casing. |
| Does an existing agent's `send` still work? | **Yes, unchanged.** | `cmd_send`'s only check is `if to != "operator" and to not in agents` (`:986`). `operator` remains a valid recipient forever — the mailbox is untouched. `relation()` (`:158-174`) still resolves every pair. A live `field-tester` sending to `operator` right now is byte-identical before and after. |
| Do live agents' hooks change? | **No.** Their settings files (`:889`) are already written and point at the same entrypoints. The gate rewrite (`my_name()=="operator"` → `not is_agent(...)`) is FALSE for every real agent both before and after, since they all have records. |
| Does the human's mailbox move? | **No.** `queue/operator/` and its 60 `delivered/` files stay exactly where they are. |
| Do the tests break? | **Two do, and they are the two that encode the bug.** See below. |

**The two tests that must change** (this is the honest cost, and it is the *right* kind of
cost — the tests assert the buggy behavior):

1. `tests/test_swarm_process.py:204` — `self.assertEqual(rec["parent"], "operator")` in
   `test_spawn_happy_path_with_fake_herdr`. This test spawns from a no-`SWARM_AGENT_ID`
   env (`run_swarm` strips it, `:68-69`) and asserts the child's parent is `operator`.
   **After the fix it must assert `rec["parent"] == "root-1"`** — and a *new* assertion
   should check `agents/root-1.json` exists with `parent: "operator"`. **This test change
   IS the fix's acceptance criterion.**
2. `tests/test_swarm_process.py:266` — `for bad in (..., "operator", "delivered")`. Extend
   to include a `root-*` name, e.g. `"root-1"`, once the reserved-prefix guard is in.

Every other `operator` reference in the 1172-line suite is about the **mailbox** (`send
operator`, `deliver` no-op, mail-on-top, `parent: "operator"` fixtures written by hand) and
**stays green untouched** — including `test_cli_deliver_operator_is_noop` (`:147`), because
a session with no record still gets no delivery under the rewritten gate.

**Rollback:** delete `.swarm/settings/root.id` and revert `my_name()`. Records written in
the interim keep working (they name a real `root-1` node that still has a record and a
journal). **There is no destructive migration and no data rewrite.**

---

## 7. THE FINAL DIFF — hardened, and **executed**

> **Status: this diff was applied to `bin/swarm`, run against the full test suite, driven
> end-to-end against a fake herdr, and then reverted. `bin/swarm` is clean at HEAD.**
> Result: **79/80 green; the single failure is `test_swarm_process.py:204`, the assertion
> that encodes the bug** (`assertEqual(rec["parent"], "operator")` after a root spawn).
> That failure *is* the acceptance criterion. Diff: **+66 / −8**, one file.

Everything below §7 in the previous revision (the `pane: ""` record, the `settings/root.id`
file, the `is_agent()` gate, the "known wart") is **superseded**. Three of those four were
defects. This section records what actually happened, because the corrections are the most
load-bearing content in this document.

### 7a. The defect my parent caught — confirmed, and it was fatal

My earlier diff wrote the root record with `"pane": ""`. `is_dead` (`:516-517`) is:

```python
    def is_dead(a):
        return live is not None and a.get("pane") not in live
```

`"" not in live` is **True** → `root-1` is **dead the moment it is born** → `eff_parent`
(`:519-526`) does exactly what it is built to do and **reattaches its live children to the
nearest living ancestor, `operator`**. I ran the real, unmodified `render_ps` on it:

```
operator — no waiting mail
├─ w1 [live] q=0 idle ?
└─ w2 [live] q=0 idle ?
dead: root-1
```

**The flat row, back on the human's screen — the exact failure the fix exists to abolish —
while the files were perfectly correct.** My parent is right that this is not a rough edge:
it is a fix whose only observable effect would have been invisible at the one place the
human looks. I had scored the `eff_parent` reattach as a coordinator-death edge case in my
probe; it is the **default state** of a paneless root. I got that wrong and the correction
is theirs.

### 7b. **Q1 — VERIFIED BY DIRECT OBSERVATION: a root session has `HERDR_PANE_ID`.**

My parent read `HERDR_PANE_ID` from their own env — but they are a *spawned* agent, whose
pane swarm created. That proves nothing about a **root** session, whose pane nobody created
for swarm. It is the same evidence I had, and it does not carry the claim. So I tested the
actual case: **I created a pane the way a human does — `herdr tab create` with NO `--env`,
no swarm involvement — and read its environment.**

```
created pane=w4:p8Y tab=w4:t8Y   (no --env passed)
--- env inside that pane ---
PANE_ID=w4:p8Y
TAB_ID=w4:t8Y
HERDR_ENV=1
SWARM_AGENT_ID=[]          <-- empty: it is a ROOT session
MATCH: HERDR_PANE_ID == w4:p8Y
```

**Herdr injects `HERDR_PANE_ID`/`HERDR_TAB_ID`/`HERDR_ENV` into every pane it creates,
itself.** Swarm's `tab create` passes only `SWARM_DIR` and `SWARM_AGENT_ID` (`:906-907` — the
only `--env` in the file), yet a swarm-spawned pane *also* has `HERDR_WORKSPACE_ID` and
`HERDR_SOCKET_PATH`, which swarm never passes. The pane env comes from herdr, not swarm.

And it is in the live set: `live_pane_set()` (`:609`) returns 20 panes here, and both
`w4:p8M` (my parent's) and `w4:p1` (**the human's own root pane, `focused: true`**) are in
it. **CONFIRMED — no fallback needed for the herdr case.**

**The one gap, stated:** if `HERDR_PANE_ID` is somehow absent, `root_name()` returns `""`.
That is handled and safe — see 7e (`""` is falsy: `my_name()` yields `""`, the hook gates
no-op, and `send` attributes the message to `operator`). The session simply cannot *spawn*
without being named, and `claim_root_name` would then record `pane: ""`… which `is_dead`
would call dead. **So hunk 2 (the `is_dead` guard) is still required as the backstop**, even
though hunk 1 makes its trigger unreachable in practice. Belt and braces, and it costs one
line.

### 7c. **Q4 — pane staleness: I found the better fix, and it DELETES `settings/root.id`.**

My parent's worry is real. I reproduced it: a record holding a **stale** pane id (human
closed the pane, opened a new session) renders `dead: root-1` and **the children reattach to
`operator` — the bug returns.** Their proposed repair (refresh `pane`/`tab` on every spawn)
does close it; I verified that too.

**But `root.id` is itself the mistake, and removing it removes the staleness class entirely.**
`root.id` stores *one name per repo* — yet identity belongs to the **session**, and herdr
already hands every session a unique, stable id. So: **key the lookup on the pane, not on a
file.**

```python
def root_name(root):
    pane = os.environ.get("HERDR_PANE_ID", "")
    if not pane:
        return ""
    for n, a in load_agents(root).items():
        if n.startswith("root-") and a.get("pane") == pane:
            return n
    return ""
```

| case | `root.id` (my old design) | pane-keyed (this design) |
|---|---|---|
| restart in the **same** pane | same name ✅ | same name ✅ (the pane id is unchanged) |
| human opens a **new** pane | **stale record → renders dead → BUG RETURNS** ❌ | no match → claims `root-2`. Correct: it *is* a different session ✅ |
| **two concurrent** root sessions | both read `root.id` → **both call themselves `root-1`**, share one identity, and fight over the `pane` field; last writer wins the `(you)` marker, silently ❌ | different panes → `root-1` and `root-2`. **No sharing.** ✅ |
| a recorded pane going stale | possible | **structurally impossible** — the pane *is* the lookup key ✅ |

**The concurrent-root case is one my parent did not raise and `root.id` actively causes.**
Pane-keying kills it, kills Q4's staleness, needs no refresh-on-spawn, and **removes a state
file from the cost table.** This is the one place where I am proposing something better than
what was asked for, and it is strictly simpler.

### 7d. **Q3 — the hook gates: CONFIRMED harmless. And then the tests found a real bug.**

My parent's trace is exactly right: **hooks are not ambient.** They exist only because
`cmd_spawn` writes them into the **child's** settings file (`:889-895`) and the launcher runs
`claude --settings <that file>` (`:834`). Spawn writes `settings/{name}.json` where `name` is
always the **child** — it **never** writes a settings file for the parent. The human's root
session was launched by the human typing `claude`, with no swarm settings. **So `cmd_deliver`
/`cmd_event`/`cmd_restore` can never be *invoked* in a root session, and what their gate
would decide is moot.** Confirmed.

**But my proposed gate — `if not is_agent(root, my_name())` — was a real defect, and the
test suite caught it.** Applying it turned 3 tests into ERRORs. The reason matters far more
than the fixtures: **`is_agent()` gates on the presence of `agents/<name>.json`, so a live
agent whose record is missing or momentarily unreadable would have its `deliver` hook
silently no-op — and its queued mail would never be injected.** That converts a recoverable
state into **permanent, silent mail loss**, breaking `WORLD.md:51-53` (*"Nothing is ever
silently dropped"*). It is a worse bug than the one I was fixing.

The correct invariant is the **name**, not the record — the two things with no hooks are the
mailbox and an unnamed root:

```python
    if my_name() in ("", "operator"):   # unnamed root / the mailbox: no hooks
        sys.exit(0)
```

Three ERRORs → gone. **This is why the gate change is a 1-token edit, not a helper function.**

### 7e. The second bug the tests found: an unnamed root sent **anonymous** mail

With `my_name()` returning `""` before the first spawn, `cmd_send` stamped `{"from": ""}`.
`relation()` (`:158-174`) would then resolve `""` to **"another agent"** — so a message from
the human, sent before they ever spawned anything, would arrive at a child stripped of its
authority instead of headed **"the OPERATOR (the human at the root)"**. A silent contract
break, caught by `test_send_stdin_queues_exact_bytes` (`:171`).

Fix: an unnamed root **speaks as the human**, because that is precisely what it is — a
session with no node, standing at the mailbox.

```python
    sender = my_name() or "operator"   # an unnamed root speaks as the human
```

Naming is forced at **spawn** — the only moment a name is load-bearing. **Sending needs no
node.** This also preserves today's behavior exactly for a human who never spawns.

### 7f. **Q2 — refusing mail to `root-*`: consistent with WORLD.md:57? Yes. Argued.**

`WORLD.md:57-61` promises *"nothing ever refuses a message to **the operator**."* The
refusal I add is to **`root-1`**, which is **not** the operator — it is a *session*. The
promise is about the human's **mailbox**, and **`queue/operator/` remains open, unrefusing,
and unchanged.** We are not making the human unreachable; **we are keeping ONE mailbox for
the human instead of accidentally creating a second, broken one.**

The refusal is in fact *required* by the neighbouring promise. `root-1` has an agent record
but **no settings file** (7d) → **no `UserPromptSubmit` hook** → **nothing ever drains its
queue.** Allowing `send root-1` would create a queue file that is *never* delivered — which
breaks `WORLD.md:51-53`, *"Delivered means delivered… Nothing is ever silently dropped."*
**Refusing at send time is the only way to keep that promise**: an undeliverable message is
refused to its sender's face, loudly, instead of rotting in a queue nobody reads.

Exact message text (verified in the run above):

```
swarm: 'root-1' is a root session: it runs no delivery hook, so a message queued there
would never be delivered. The human has ONE mailbox -- send to `operator`; they see it at
the top of `swarm ps`.
```

### 7g. THE DIFF (verified: applied, tested, reverted)

**7 hunks, +66/−8, one file. No new state files. No new verbs. No new concepts.**

```diff
--- a/bin/swarm
+++ b/bin/swarm
@@ -60,8 +60,31 @@ def root_dir():
     return os.environ.get("SWARM_DIR") or os.path.join(os.getcwd(), ".swarm")
 
 
+def root_name(root):
+    """This root session's agent name, or "" if it has not named itself yet.
+
+    Keyed on HERDR_PANE_ID, not on a file: herdr injects a unique, stable pane
+    id into every pane it creates (verified: a pane created with no --env still
+    carries HERDR_PANE_ID). The pane IS the session's identity. So a restart in
+    the same pane finds the same name; a second, CONCURRENT root session sits in
+    a different pane and claims a different name; and a recorded pane can never
+    go stale, because it is the lookup key."""
+    pane = os.environ.get("HERDR_PANE_ID", "")
+    if not pane:
+        return ""
+    for n, a in load_agents(root).items():
+        if n.startswith("root-") and a.get("pane") == pane:
+            return n
+    return ""
+
+
 def my_name():
-    return os.environ.get("SWARM_AGENT_ID") or "operator"
+    # The ONE reader of SWARM_AGENT_ID (spawn's tab env and the middleware are
+    # its only writers). A root session has no SWARM_AGENT_ID and is NOT the
+    # operator -- the operator is a mailbox (WORLD.md:57), never a session. It
+    # is an agent that may not have named itself yet: "" is falsy, and spawn is
+    # what forces the name.
+    return os.environ.get("SWARM_AGENT_ID") or root_name(root_dir())
 
 
 def q_dir(root, name):
@@ -512,7 +535,10 @@ def render_ps(...):
     def is_dead(a):
-        return live is not None and a.get("pane") not in live
+        # No pane => no pane to be dead in. Absence of a pane is not evidence
+        # of death. Without this, a paneless record is born dead and eff_parent
+        # reattaches its live children to `operator` -- the flat row, restored.
+        return live is not None and bool(a.get("pane")) and a.get("pane") not in live
     dead = sorted(n for n, a in agents.items() if is_dead(a))
 
@@ -684,7 +710,7 @@ def cmd_deliver():
 def cmd_deliver():
     # UserPromptSubmit. Bulletproof: any error -> exit 0, no output, turn intact.
-    if my_name() == "operator":
+    if my_name() in ("", "operator"):   # unnamed root / the mailbox: no hooks
         sys.exit(0)

@@ -701,7 +727,7 @@ def cmd_event(kind):
-    if my_name() == "operator":
+    if my_name() in ("", "operator"):   # unnamed root / the mailbox: no hooks
         sys.exit(0)

@@ -736,7 +762,7 @@ def cmd_restore():
-    if my_name() == "operator":
+    if my_name() in ("", "operator"):   # unnamed root / the mailbox: no hooks
         sys.exit(0)

@@ -768,6 +794,30 @@ def claim_name(root, name):
     return fd
 
 
+def claim_root_name(root):
+    """Name this root session, once, on its FIRST spawn -- the only moment the
+    name can matter. Lazy: a human who only runs `ps` creates no node. The
+    record carries the session's REAL pane, so `ps` renders it live with its
+    children beneath it (a paneless record would render dead: see is_dead)."""
+    pane = os.environ.get("HERDR_PANE_ID", "")
+    tab = os.environ.get("HERDR_TAB_ID", "")
+    for i in range(1, 1000):
+        name = f"root-{i}"
+        try:
+            fd = claim_name(root, name)   # O_CREAT|O_EXCL settles the race
+        except FileExistsError:
+            continue
+        with os.fdopen(fd, "w") as f:
+            f.write(f"# journal of {name}\n\n## {fmt_ts(now_ms())} -- root session\n"
+                    f"The human's own session. Parent: operator (the mailbox).\n")
+        write_atomic(agent_rec_path(root, name), json.dumps(
+            {"name": name, "parent": "operator", "pane": pane, "tab": tab,
+             "model": "", "cwd": os.getcwd(), "task": "(root session)",
+             "ts": now_ms()}))
+        return name
+    die("could not claim a root name (root-1..root-999 all used)")
+
+
 def spawn_header(name, parent):

@@ -858,7 +908,7 @@ def cmd_spawn(argv):
-    if name in ("operator", "delivered"):
+    if name in ("operator", "delivered") or name.startswith("root-"):
         die(f"'{name}' is reserved")

@@ -866,7 +916,11 @@ def cmd_spawn(argv):
     root = root_dir()
-    parent = my_name()
+    # The root session names ITSELF here, on its first spawn: the human is a
+    # mailbox, so the human's SESSION must be an agent in order to have
+    # children. This is what makes `human -> flat row of workers`
+    # unrepresentable -- every child of a root session records parent=root-N.
+    parent = my_name() or claim_root_name(root)
 
     # Claim the name FIRST: journal-as-tombstone. A name ever used errors here.

@@ -985,7 +1039,11 @@ def cmd_send(argv):
     if to != "operator" and to not in agents:
         die(f"unknown agent: {to}")
-    sender = my_name()
+    if to.startswith("root-"):
+        die(f"'{to}' is a root session: it runs no delivery hook, so a message "
+            f"queued there would never be delivered. The human has ONE mailbox "
+            f"-- send to `operator`; they see it at the top of `swarm ps`.")
+    sender = my_name() or "operator"   # an unnamed root speaks as the human
     rec = {"to": to, "from": sender, "ts": now_ms(), "body": body}
```

### 7h. END-TO-END PROOF — the falsifier I have been carrying for three reports, discharged

Fake herdr + fake claude, a **root session** (`HERDR_PANE_ID=w9:pROOT`, **no
`SWARM_AGENT_ID`**), reproducing the exact field-evidence failure — a root session spawning
two workers back to back:

```
$ swarm spawn w1 "task one"   ->  w1
$ swarm spawn w2 "task two"   ->  w2

=== THE FILES ===
  root-1   parent=operator  pane=w9:pROOT
  w1       parent=root-1    pane=w9:pKID
  w2       parent=root-1    pane=w9:pKID

=== WHAT THE HUMAN SEES (swarm ps) ===
operator — no waiting mail
└─ root-1 (you) [live] q=0 idle ?
   ├─ w1 [live] q=0 idle ?
   └─ w2 [live] q=0 idle ?

=== send to a root session ===
swarm: 'root-1' is a root session: it runs no delivery hook, so a message queued there
would never be delivered. The human has ONE mailbox -- send to `operator`; ...
```

**One root line. Workers nested. `parent: root-1` in the files. The human's direct span is
1 — in the view as well as on disk.** This is the falsifier from my probe and both prior
reports, and it passes.

### 7i. Test results, exact

```
$ python3 -m unittest discover -s tests      # WITH the diff applied
Ran 80 tests    FAILED (failures=1)

FAIL: test_spawn_happy_path_with_fake_herdr
  tests/test_swarm_process.py:204
  AssertionError: 'root-1' != 'operator'
```

**One failure, and it is the assertion that encodes the bug.** It must be updated to
`assertEqual(rec["parent"], "root-1")`, plus a new assertion that `agents/root-1.json` exists
with `parent: "operator"`. **That edit IS the acceptance criterion.** `:266` (reserved names)
should also gain a `root-*` case. The other **78 tests pass untouched** — including every
mailbox test, the middleware suite, the deliver/event/restore hooks, and
`test_cli_deliver_operator_is_noop`.

`bin/swarm` has been **reverted to HEAD** (`git status` clean; suite green at HEAD). The
verified diff is preserved for whoever ships it.

## 8. THE COST, in the repo's own currency

| currency | today | fix (a3) | fix (b) |
|---|---|---|---|
| **verbs** | 4 | **4** (unchanged — spawn does the naming) | 4 (+1 flag `--flat`) |
| **concepts** | 9 | **9** (repair of concept 1's root instance; §1) | 9 |
| **state** | `agents/ queue/ journal/ event/ settings/` | **+0 new state kinds, +0 new files.** (Earlier draft added `settings/root.id`; pane-keying **deleted it** — §7c.) `agents/root-N.json` + `journal/root-N.md` are *ordinary instances of existing state*. | +0 |
| **bytes (`bin/swarm`)** | 1150 lines | **+66 / −8** (measured, `git diff --stat`: 1150 → 1208). 7 hunks. | +8 |
| **WORLD.md** | 79 lines | +3, −2 (concept 2's body; the `:57` promise made true) | +0, or +1 to document `--flat` |
| **tests** | 1172 lines, 80 green | **MEASURED: 79/80 green with the diff applied. The 1 failure is `:204`, the assertion that encodes the bug** — it becomes the acceptance criterion. `:266` gains a `root-*` case; +1 new test. | +1 test |
| **migration** | — | **none.** Forward-only; 90 records untouched; live tree unaffected | none |
| **doctrine** | SKILL.md "hand" convention (24 lines) | **net DELETION available** — the tool now provides what the convention hand-rolled | unchanged |

---

## 9. RECOMMENDATION

**Ship (a) via (a3).**

The one-line summary: **`my_name()` returning `"operator"` for an unnamed session is the
bug. Every other symptom — the flat rows, the sincere false compliance, the "hand"
convention, the false sentence at `WORLD.md:57` — is downstream of that one `or`.**

(b) is a lint over a broken data model. It refuses the only action a root session can
perform and recommends one it cannot, and its necessary override (`--flat`) is exactly the
door the field-evidence sessions would have walked through while quoting the doctrine at
themselves (dp-red R4). It cannot deliver the guarantee.

(a3) makes the failure **unrepresentable** rather than discouraged, for **0 new verbs, 0 new
concepts, 0 new state files, +66/−8 lines, and no migration**. It costs one test assertion —
the one that currently asserts the bug — and it *removes* doctrine rather than adding it.

**THE FALSIFIER IS DISCHARGED.** I carried it through three reports; §7h runs it. A root
session (no `SWARM_AGENT_ID`) spawning two workers back to back now writes
`parent: root-1` for **both**, and `swarm ps` shows **one root line with the workers nested
beneath it**. The human's direct span is 1, in the view as well as on disk. The suite is
79/80 with the single failure being the assertion that encodes the bug. `bin/swarm` is
reverted to HEAD and green.

**What the machine caught that I did not.** Three of my four earlier claims were wrong, and
*every* correction came from running code rather than reading it:

1. **My parent caught** the `pane: ""` defect — `is_dead` marks a paneless record dead, and
   `eff_parent` then reattaches its children to `operator`. **The flat row would have come
   back on the human's screen while the files were correct.** I had scored this as an edge
   case in my probe; it was the default state. Their one-line fix (record the real
   `HERDR_PANE_ID`) is correct, and **I verified the premise they could not** — a pane
   created with **no `--env`** still carries `HERDR_PANE_ID`, so herdr, not swarm, injects it.
2. **The test suite caught** my `is_agent()` hook gate: it would have silently disabled
   delivery for any agent with a missing record — **permanent, silent mail loss**, a worse
   bug than the one being fixed. Gate on the **name**, not the record.
3. **The test suite caught** an unnamed root sending **anonymous** mail (`from: ""`), which
   `relation()` would render as "another agent" instead of "the OPERATOR" — stripping the
   human's word of its authority.
4. **I caught** that `settings/root.id` was itself a mistake: it gives two *concurrent* root
   sessions the same name, and it is what makes pane-staleness (my parent's Q4) possible at
   all. **Keying identity on the pane deletes the file, deletes the staleness class, and
   gives concurrent roots distinct names.** This is the one thing here that is better than
   what was asked for.

**Remaining risk, stated.** The end-to-end ran against a *fake* herdr and a *fake* claude
(the tests' own fixtures). It has not been run against live herdr with a real `claude`
launching a real pane. I judge that low-risk — the fake implements the same `pane list` /
`tab create` JSON contract, and I separately verified the real herdr's live pane set and env
injection against the real binary (§7b) — but it is not the same as shipping it. **If the
reviewer wants one more check before merge, that is the one to run.**
