# HARNESS — the simplest harness for swarm, and how a model gets chosen

**Author:** `harness-contractor`, an outside contractor engaged by the human operator,
in the tradition of `simplest` (`docs/design/SIMPLEST.md`) and `patterns-contractor`
(`docs/design/INDUSTRY-PATTERNS.md`). I am not bound by this repo's doctrine; I read it
as anthropology. Where my answer collides with local law I say so plainly — twice below,
in §5 and §6, the collisions are named and argued rather than translated away.
**Written at** `swarm-dev/spawn-slash-shim@cfb3113`, 2026-07-13. Design only; no product
code; nothing in `bin/swarm` changed.

**Evidence discipline:** **VERIFIED** (I ran it / read the line — quoted, file:line),
**MEASURED** (instrumentation, method stated — mine or a named child's),
**DOCUMENTED** (a named source says so), **REASONED** (my argument; if it decides
something, its falsifier is in §9). Inputs read in full by me: `docs/PHILOSOPHY.md`,
`docs/design/SIMPLEST.md`, `docs/design/FLEET.md`, `WORLD.md`,
`docs/design/MODEL-FIT.md` (via `git show swarm-dev/model-fit`), `bin/swarm` seams
(`cmd_restore` :916, `build_restore` :462, `write_launcher` :1041, `cmd_spawn` :1098,
`classify_blocked` :694 on this branch). Child evidence artifacts, harvested:
`docs/audit/_hc-eval-table.md` (87 rows, every FLEET-EVAL score with file:line),
`docs/audit/_hc-field.md` (limit-deaths and the hand-relaunch, quotes on disk),
`docs/audit/_hc-mech.md` (mechanical trace of the launcher/restore/relaunch path),
`docs/audit/_hc-industry.md` (outside frameworks), `docs/audit/_hc-slm.md`
(small-model verification and prior art).

**Two operator addenda folded in as settled input:** (1) the small-function-calling-model
strand (§7); (2) the Haiku ban of 2026-07-13 — *"it doesn't have auto mode"* — which this
design treats not as an ops note but as the type specimen of a missing axis (§2.4, §4.1).

---

## 1. THE RECOMMENDATION

**Keep the harness swarm already has — pane, hooks, file queue, journal, restore — and
make exactly one thing variable at exactly one seam: the launcher body, selected by a
single model token.** Everything the human asked for lands as: one token vocabulary
(§2.2), one new verb (`swarm remodel`, gated by direction — §6), one documented page of
plays that opens with the operator's standing priority (§5, §4.2), one config key for
the static operator (§4.3), and one refusal mechanism whose current contents are
provisional pending a named, cheap probe (§2.4). No registry engine, no router, no
policy file, no auto-failover daemon. *(This document was adversarially reviewed after
its first draft — `docs/design/HARNESS-RED.md` — and repaired against it; §10 is the
disposition of every finding, including two refuted claims and a corrected evidence
discipline.)*

The license was "change swarm in any way we want, keep the core ideas." I examined the
radical options — replace the harness with opencode everywhere, drive every model from a
parent-owned API loop, adopt a graph-engine runtime like the industry's
(`_hc-industry.md` surveys the field: ~7 agent frameworks, 2 routing gateways,
2 analogies) — and the honest finding is that the deletion pass has already been
run on this system (`SIMPLEST.md` took 27 concepts to 9), and what remains *is* the
minimal harness that holds the core ideas. FLEET.md proved the coupling claim I would
otherwise have had to prove: **the only place swarm is welded to Claude is the launcher
body** (VERIFIED — `bin/swarm:1061-1062` is the single `claude` invocation; the hooks
simply never fire for a non-Claude process. FLEET §2 said this first, but its line
numbers have rotted and are re-verified here at current lines: hooks wired at
`:1157-1160`, handlers `cmd_deliver` `:864`, `cmd_event` `:878`, `cmd_restore` `:916` —
each handler's body is try-wrapped and exits 0, though `cmd_event`'s arg-check `die()`
precedes its try, so "fail-safe" is near-universal rather than absolute). So the
simplest-and-best harness is not a new harness. It is the current one with the weld
replaced by a socket.

**The core ideas I chose to hold invariant** (this list is itself a design decision —
judge it):

1. **An agent is a named session in a pane** — name + parent + journal; the pane is
   ground truth; the society is observable (`WORLD.md` #1).
2. **A name is one agent forever** — the journal tombstone (`WORLD.md` #3,
   `bin/swarm:940-947`). §6 argues this binds the *name*, not the process behind it.
3. **A message is a claim on one turn** (`WORLD.md` #4).
4. **Judge artifacts, never claims**; the system stores only facts a file can witness
   (`WORLD.md` #8, PHILOSOPHY §4).
5. **The tree of judgment** — parent judges child; the operator roots it; the
   operator's attention is the scarcest resource (PHILOSOPHY §9).
6. **Incentives over guardrails; conventions earn their tooling** (PHILOSOPHY §2, §8).

**What I was willing to break, and do:** the equation *agent = the Claude session*.
In this design the session — and the model driving it — is the **incumbent** of a seat
whose identity is name + parent + task + journal. That break is what makes §6 possible,
and I argue it is not a break of core idea #2 but a correction of a conflation (the
evidence is that this repo already survives session replacement daily). I also break:
the Claude-only launcher (per FLEET), `ps` rendering a wedged pane as `idle` (already
being fixed on this branch), and the assumption that model fitness is a
cost/quality scalar (§2.4: it is gated first, traded second).

**The two doctrinal rulings, up front:**

- **Patterns (§5): convention, not machinery — with the machinery case made at full
  strength first and the earning observation named.** A `docs/PLAYS.md` of named,
  eval-grounded model+harness recipes that parents read and cite; no `--pattern` flag,
  no schema. Decided by MODEL-FIT's own measured record: the last mechanism that chose
  for parents produced 142/143 spawns nobody decided.
- **On-the-fly switch (§6): design what the human asked for, and it turns out the
  doctrine and the ask do not actually collide.** "A name is one agent forever" binds
  accountability and history to the *name*; the model is an attribute of the current
  incumbent session, which the restore path already treats as disposable. `swarm
  remodel` changes the incumbent and journals the change. The genuine loss (in-context
  state not in the journal) is exactly the loss at compaction — an event this system
  already survives by design.

---

## 2. THE HARNESS, AT THE SEAM

### 2.1 What stays byte-for-byte in spirit

Pane-per-agent under herdr (the observable society is the product — FLEET §2 and the
graveyard both refused headless), the four fail-safe hooks for Claude sessions, the
file queue and atomic-rename delivery, journal-as-continuity with the 4000-char tail
re-injection on SessionStart (VERIFIED — `build_restore`, `bin/swarm:462-472`; the cap
itself is `JOURNAL_TAIL_CAP = 4000`, `bin/swarm:34`), task-as-file,
launcher-status readiness, the
journal tombstone. None of these is Claude-specific except by accident of the launcher.

### 2.2 The one variable: the launcher body, keyed by the model token

Today `write_launcher` bakes one of two bodies: `claude --settings S --model M "$PROMPT"`
or the bare form when no `--model` was given (VERIFIED — `bin/swarm:1061-1062`; the bare
form means the child runs *the binary's ambient default, which nobody chose* —
MODEL-FIT §5b's correction, re-verified by `_hc-mech.md` §1).

This design makes the launcher body a function of the model token, from a small **table
of facts** inside `bin/swarm` (plus a config section for custom endpoints):

| token class | launcher body | done-signal | duties |
|---|---|---|---|
| Claude family (`opus`, `sonnet`, `fable`, …) | `claude --settings S --model <id> "$PROMPT"` + the four hooks | Stop hook / turn semantics, as today | full agent: journal, report, reconcile |
| tool-using non-Claude leaf (`deepseek`, `glm`, …) | `opencode run "$TASK" -m <provider/model>` + report plugin | artifact-exists + plugin send; **parent-owned watchdog** (FLEET §5 — the honest bill, not priced at zero) | leaf only; the parent journals *about* it |
| one-shot endpoint (any OpenAI-compatible URL, incl. small models, §7) | the ~5-line `curl \| jq` thin runner writing `artifact.txt` and exiting (FLEET §3B) | process exit + file exists — unambiguous | none; artifact is the whole surface |

Three deliberate properties of this table:

- **It maps names to launch commands; it decides nothing.** PHILOSOPHY §5's test is
  "should the thing this configures exist at all?" — and different vendors genuinely
  require different launch commands; that is the world, not a mode someone invented.
  A table of facts is not a policy engine. The moment a row tries to encode *when to
  use* a token rather than *how to launch* it, it has crossed into §5's territory and
  belongs in PLAYS.md prose instead.
- **The harness is part of the token.** The user never names a harness. `--model
  deepseek` *is* the opencode-leaf launcher; `--model opus` *is* the Claude session.
  One flag, one concept, and "chinese models + opus operator" becomes a pair of spawn
  lines rather than a configuration.
- **Non-Claude leaves get a clean task** (the operator's instruction minus the Claude
  duties preamble) and `SWARM_PARENT` in the pane env — FLEET §4's one-flag-one-env-var
  bill, adopted unchanged. Leaf-only for foreign models stands on FLEET's evidence and
  the eval's (§3 below) — and *"a leaf never spawns"* (FLEET.md:88) is made
  **structural for these rows, not quoted as if it held itself** (the review caught the
  first draft doing exactly that — nothing in `cmd_spawn` checks relations, and nothing
  today stops any child spawning): the thin runner has no tools at all, and the
  opencode leaf's config **denies the swarm verbs** via `tool.execute.before` (FLEET §7
  priced this at near-zero). On §8's bill; its falsifier is §9 — a foreign leaf with a
  descendant means the denial failed. For **Claude-family** cheap leaves the promise
  remains a promise: the structural leaf-cannot-spawn change is MODEL-FIT's "first
  thing to build if Rung 3 is taken seriously," named in §8 as unbuilt.

### 2.3 Blocked is a first-class state — a harness requirement, not a nicety

The single most expensive fact the field evidence produced: **a dying or wedged agent
is invisible.** trigger-scout's session-limit death rendered in `ps` as an ordinary
`[live] q=0 idle` agent, distinguishable only by reading the frozen last-words string
(VERIFIED — `_hc-field.md` §A1; three observers, though honestly counted they share
**one instrument** — all three read the same `last_words` string `ps` surfaces). The
operator's own journal
names three structural bugs from that incident: Stop hook skipped on limit-death → no
event fact → no re-ring; `ps` cannot distinguish frozen-on-limit from busy;
doorbell-Enter unreliable (VERIFIED — `.swarm/journal/operator.md:199`, quoted in
`_hc-field.md` §A2). And the Haiku ban exists because a permission-wedged pane has the
same invisibility (DOCUMENTED — the operator's correction of 2026-07-13, on disk at
`.swarm/queue/harness-contractor/delivered/1783949599092-operator.json`).

The fix is already being built on this very branch — `classify_blocked`
(`bin/swarm:694-715`, VERIFIED): pane text, explicitly treated as attacker-controlled,
classified into a **closed enum** (`trust | permission | rate-limit | None`) and rendered
as `[blocked: kind]` in `ps`. This design adopts that work as a requirement and adds
nothing beside it: **any harness that admits models with differing permission and limit
behavior MUST render blocked distinct from idle.** Every avenue-3 trigger below assumes
this surface exists; without it, "change the model on the fly" has no eyes.

### 2.4 The survivability axis — the gate aimed where the source aims it

*(Rewritten after adversarial review — the original version of this section tagged a
per-model causal claim MEASURED against a source that rules the opposite; see §10, F1.)*

There is an axis the cost/quality framing misses entirely: **can this model survive this
harness at all?** Fitness is gated first, traded second. But the evidence must be read
in the order it actually runs:

1. **The measured cause of the Haiku wedge is infrastructure, not the model.** The
   probe's own bolded conclusion: *"The stall was caused by a permission gate swarm
   hands EVERY child regardless of model. Opus would block too… A tier rule about cheap
   models does not fix an infrastructure gate that fires on all models. Aim the fix at
   the gate."* (VERIFIED — `docs/audit/weak-model-delegation-2026-07-13.md:87`; and
   `grep -c permissions bin/swarm` → 0: spawn writes hooks only, no `permissions`
   block.) The settling probe — an Opus-pinned child into the same first-touch wall —
   is that source's *"top re-run item"* and **has never been run.**
2. **So this design's first survivability fix is the one the source names: `cmd_spawn`
   writes a `permissions` block.** That is moved onto *this* design's bill (§8), not
   left as someone else's defect — every model admitted by the token table depends on it.
3. **The operator's Haiku ban stands above that as standing policy** (DOCUMENTED — the
   operator's correction of 2026-07-13, on disk at
   `.swarm/queue/harness-contractor/delivered/1783949599092-operator.json`), on a
   capability claim — *"it doesn't have auto mode"* — that is the operator's assertion,
   not an independent measurement. If true, it is exactly the kind of per-model fact
   the gate exists for: a model that cannot clear its own dialogs *even with
   permissions configured* cannot hold a pane.

The mechanism this section ships is therefore a **gate whose rows are facts with
sources, and whose current contents are provisional**: the token table may mark a row
*not agent-capable*, and spawn refuses it with the recorded reason printed:

```
$ swarm spawn scout "read the doc" --model haiku --reason "cheap read"
swarm: haiku is marked not agent-capable (operator ban 2026-07-13: no auto
permission mode; settling probe not yet run — see HARNESS.md §9.4). Use
sonnet, or a one-shot leaf token if the task is a single completion.
```

The refusal text carries its own epistemic status on purpose: a gate that reads as
"the Haiku problem is solved" while the all-models permission gate stays unbuilt would
be the harm the source warns about. The probe that settles the row is cheap and named
in §9.4. A refused token stays available where its weakness cannot bite: the one-shot
runner row, which has no session, no dialogs, and no turns to wedge.

---

## 3. THE THREE AVENUES, RECONCILED

The three avenues are not three features. They are one decision — *who runs this seat* —
made at three times: at spawn (avenue 1), by recipe (avenue 2), and under change
(avenue 3). The same question governs all three (MODEL-FIT's ladder: *"can I cheaply
tell that this child was wrong?"*), the same reader renders all three (`ps` model pins,
already shipped — VERIFIED in live `ps` output), and the same journal records all three.

**Avenue 1 — spawn-time choice — is settled as doctrine by MODEL-FIT (PR #83) and
survives the other avenues intact.** On the mandate, the status is stated precisely,
because the review caught this document spending it loosely (§10, F2): the *decision*
that `--model` and `--reason` both become required is the human's, declared in this
contract's engagement brief (DOCUMENTED — my task text, on disk in
`.swarm/settings/harness-contractor.task`); the *mechanism* is specified and costed in
MODEL-FIT §5 and **deliberately left unimplemented** in PR #83, whose shipped ruling is
"`--model` stays optional, but silence stops being free" — and today's CLI rejects
`--reason` outright. This design is written for the post-mandate world and carries the
mandate's build cost on its own bill (§8); nothing below spends it as already paid. The one question this document owes: *does the per-spawn reason become ceremony
once plays (avenue 2) exist?* **No.** A play names a combo; the reason answers the
parent's verification capacity — *"can I cheaply tell if this child is wrong?"* — which
no play can know, because it is a fact about the parent, not the task (MODEL-FIT §5:
scoping the reason to anything else "launders a guess into a decision"). Citing a play
is legitimate *shorthand inside* a reason — `--reason "play cheap-sweep; I diff each
artifact against its source"` — and an empty `--reason "play: cheap-sweep"` with no
verification clause is a skipped step, the same as today. One sentence in PLAYS.md says
exactly that.

**Avenue 2 — patterns — becomes `docs/PLAYS.md`,** argued and ruled in §5. The plays
are executable through avenue 1's one flag: a play *is* two or three spawn lines.

**Avenue 3 — change under way — becomes `swarm remodel`,** argued and ruled in §6, with
its triggers made visible by §2.3. The three avenues meet in the journal: spawn writes
`spawned <name> on <model> — <reason>`; remodel appends `remodeled <old>→<new> by
<caller> — <reason>`; the play, if one was used, is named in both.

**Where the eval constrains all three** (MEASURED rows, `_hc-eval-table.md`, each with
file:line into FLEET-EVAL/-V3): the claude-native anchor swept its battery (10/10 D2,
17/17 D3, 6/6 D4); deepseek and GLM both passed duties 5/5 and **heavy delegation 6/6**
— the human's parent-capable hypothesis is real — but both are leaf-duty-weak (deepseek
narrates reports instead of sending, 4/7 drops; V3:76-80), neither journals for
continuity (V3 D4 hard-fails — with the source's own caveat carried, not dropped: the
D4 failure is *"confounded in magnitude"* by an MCP escape hatch and reads as *"at most
this bad"*, V3:33-35), neither time-boxes (deepseek's 11-minute harness detour,
V3:84-86; GLM's watchdog-less sleep loop, V3:98-100). So: **foreign models may hold
constrained seats and tool-leaves; they may not be trusted with report-driven
protocols, and their restore-dependent continuity is at best unproven.** The plays in §5 encode exactly these rows.

---

## 4. THE PRIORITY AXIS — cost / quality / static

Three layers, in order of application. The first is a gate, the second is one line of
prose, the third is one config key. No weights, no scoring function, no classifier.

### 4.1 The gate (binary, first)

§2.4's survivability gate. Not a preference — a refusal, with the measured reason
printed. A model that cannot run here is not "low quality"; it is out.

### 4.2 The operator's standing priority (one line of prose, stated once)

*(Rewritten after adversarial review, which killed the first version's config key three
ways — see §10. The original had the tool inject a config line into every spawn header;
that was, as the review put it, a wired free-text injection channel built two pages
after this document argued untrusted text must be laundered through a closed enum — and
a mechanism for a convention never once tried, exactly the §5 test this document applies
to everyone else's machinery.)*

The operator's standing priority is **the first line of `docs/PLAYS.md`** — the page
every parent already reads at the moment of choice (§5):

```markdown
> Operator priority: quality-first — when the ladder is ambiguous, buy the
> stronger model.
```

Nothing in code reads, injects, or interprets it. A cost-lean operator writes
`cost-lean: prefer the cheapest tier the ladder allows` and every play below it is read
in that light. This is prompt-level convention, first (PHILOSOPHY §8) — no config key,
no injection wiring, no new mechanism at all. Who notices if it is ignored? The
operator, reading `ps` pins and spawn reasons — the audit surface that already exists.
Its falsifier (§9.3) is the same one every doctrine line carries, no better and no
worse; the previous design pretended a config key would make it more enforceable, and
it would not have.

### 4.3 Static choice (the "stop being clever" user, served first-class)

```ini
[models]
default = opus
```

in `.swarm/config` — the config file `WORLD.md:64-75` defines for the `[middleware]`
section; no file exists until an operator writes a stanza, and this adds the second
stanza that file can carry — enables the token `--model default`, which resolves to
the configured value and prints what it resolved to. The static operator sets it once;
every spawn thereafter is:

```
$ swarm spawn scout "survey the auth code" --model default --reason "operator static policy; I read every scout report in full anyway"
spawned scout (model: opus, via default)
```

This is **explicit deference, not silence** — the distinction MODEL-FIT §5b drew when it
refused to change the ambient fallback: the bug was never which model the default picked,
it was that nobody was thinking. `--model default` is a choice a parent *says*; a spawn
with no `--model` at all **becomes** an error once the mandate lands (today it is legal
and silently runs the ambient default — the 142/143 bug, live until the mandate is
built). And the resolved model is pinned in the record and shown in `ps`, so the tree
never contains a model nobody can name (which is today's actual resting state — the
bare launcher line runs an ambient default that can change under the swarm's feet,
VERIFIED `bin/swarm:1061-1062`). One honest debt from the review: MODEL-FIT's
anti-theater evidence (0/135 mush) was measured on a field whose content varied per
spawn; a static operator's reason risks becoming one frozen sentence. The verification
clause must still vary with the task ("I diff the artifact" vs "I read it in full"),
and a wholly invariant reason string is the theater case — §9.3 collects it by
grep-uniqueness.

### 4.4 The UX, end to end

```
$ swarm spawn census "count every call site of write_launcher" --model sonnet \
    --reason "grep-checkable in seconds; completeness published as a floor"

$ swarm spawn sweep-3 "extract every --model mention from docs/, to artifact.txt" \
    --model deepseek --reason "one-shot; the artifact is the whole surface and I diff it"

$ swarm spawn x "do a thing"
swarm: spawn needs --model <M> and --reason "<one clause>" — the parent chooses
the child's model. Ask: can you cheaply tell that this child was wrong?
tokens: opus sonnet fable (agents) · deepseek glm (leaves) · default (if configured)

$ swarm ps
├─ census   model=sonnet [live] q=0 idle 40s
├─ sweep-3  model=deepseek [leaf] artifact: pending, watchdog 12m
└─ scout    model=opus [blocked: rate-limit] q=2
```

Two flags — both the human's declared direction, **neither built today**; their build
is on this design's bill (§8), not spent as someone else's completed purchase. And the
honest accounting the review forced: "two flags" is a number this design chose to keep
small, not proof of simplicity — the real cost is the concepts an operator must hold
(the reviewer's count: ~22, most of them inherited from swarm itself rather than added
here; the additions are the token classes with their differing done-signals, one verb,
one config key, and the PLAYS page). The claim this design actually makes is
comparative: every alternative examined — a registry, a router, a policy engine —
carries those same concepts *plus* its own machinery. The complexity floor is the
domain's, not the flag count's.

---

## 5. THE PATTERN QUESTION — §5/§8 versus a registry, argued and ruled

**The collision, plainly:** the human wants "well defined patterns in the graph for
different model and harness combinations." PHILOSOPHY §5 and §8 are hostile to that by
default: *"when you reach for a config field, first ask whether the thing it configures
should exist at all"*; *"prompt-level convention first, a visibility verb second, an
engine never — unless the record shows the convention failing."* A named registry of
combos is exactly the machinery those principles refuse. Neither watering down the
human's idea nor rubber-stamping the doctrine is acceptable; here are both cases at
full strength.

**The case for patterns-as-machinery (the strongest I can make it).** A registry —
`.swarm/plays.json`, `swarm spawn --play cheap-sweep` — buys four real things:
(a) *atomicity*: a play bundles model + harness + watchdog duty + permissions in one
token, so a parent cannot assemble half a play (spawn the GLM leaf, forget the watchdog
— and the eval says a watchdog-less GLM harvest loop hangs, V3:98-100); (b) *consistency
at scale*: fifty spawns of the same recipe do not drift; (c) *evolvability*: when the
eval re-runs and a row changes, one registry edit re-tunes every future spawn, versus
hoping every parent re-reads a doc; (d) *machine-checkability*: `ps` could render the
play name, and an auditor could diff practice against definition. These are genuine
goods, and dismissing them as "configuration" would be dogma doing the thinking.

**The case for patterns-as-convention.** A `docs/PLAYS.md` — named recipes in prose,
each with its evidence row and its copyable spawn lines — costs zero new concepts,
zero schema, zero registry-rot surface, and it keeps the deciding mind at the spawn.
The plays, concretely (each grounded in MEASURED rows from `_hc-eval-table.md`):

- **house-tree** — Fable/Opus seats, Sonnet checkable leaves. Ground: MODEL-FIT's
  ladder; the anchor's clean sweep (V3:25).
- **cheap-sweep** — N one-shot thin-runner leaves + a Claude parent that diffs
  artifacts against sources. Ground: FLEET §3B (done = exit + file, no liveness
  protocol to build).
- **glm-tool-leaf** — GLM on the opencode row for tool-heavy sweeps, **parent owns a
  watchdog, and the clause travels inside the play's copyable brief text**. Ground:
  "excellent tool-user" (V3:24, the bottom-line row) *and* "no watchdog… dead children
  would hang it again" (V3:98-100 as harvested in `_hc-eval-table.md`; the primary
  wording sits at V3:101-102 per the review's re-check).
- **foreign-seat** — deepseek/GLM as a mid-tree seat for heavy fan-out, **parent polls
  artifacts and never waits on a report**. Ground: D2-heavy 6/6 both (V3:23-24) against
  4/7 report drops (V3:76-80) and no continuity journaling (D4 rows, magnitude-confounded
  per V3:33-35). This is the human's "chinese models + opus operator" pattern, shipped
  in the only form the measurements support.

**The ruling: convention.** *(This passage was rebuilt after adversarial review — the
original's three arguments included one false premise and one mis-deployed number; the
ruling survives on what follows, and §10 records what did not. An outside contractor
who decides a collision with doctrine citations has rationalized, not argued; here is
the argument.)*

1. **REASONED — the thinking-preservation argument, with its falsifier.** A `--play`
   flag compresses the decision back into a token. Under the mandate a play-spawn still
   carries `--reason`, so the honest version of this argument is narrower than "142/143
   again": the play token invites the reason to degenerate into a play *citation*, and a
   reason that no longer states the parent's own verification plan is the field going
   empty in a new uniform. (142/143 — MEASURED — is what *absence of required choice*
   produced; it is context for why silence is expensive, not a measurement of play
   tokens, which have never existed.) Falsifier: §9.2's grep — if reasons on play-cited
   spawns keep their verification clauses at the same rate as free spawns, this argument
   is wrong and costs the ruling its first leg.
2. **The earning condition is closer than the original draft claimed, and the honest
   statement helps the registry's case, not mine.** The watchdog convention *is*
   written — `FLEET.md:286`: *"Watchdog: the parent owns a timeout on the pane."*
   *(A later correction, from LOOP.md's adversarial review: this argument's original
   evidence — GLM's v2 "misread liveness… 4 retries… hung" incident,
   `FLEET-EVAL.md:181-183` — is a **v2 GLM D2 row the eval itself retired** as
   substantially a rig artifact: "No v2 GLM D2 row should be cited again",
   `FLEET-EVAL-V3.md:123-124`. What survives, and is live in v3: GLM's harvest loop
   has **no watchdog** — "dead children would hang it again" — graded as an
   unexercised risk, not a demonstrated hang.)* What has *not* yet happened is the
   convention failing in the hands of its addressee: no Claude parent, briefed with
   the watchdog duty, has yet spawned a foreign leaf in production and dropped the
   duty. The earning condition stays a hair trigger rather than a stall: **one**
   briefed-parent omission earns the bundling (below), not "more than once."
3. **Registries rot into ceremony** (SIMPLEST §3.5: every structured field nobody reads
   was "verifiably dead or rotten"). A prose play that drifts from the eval is caught by
   the next reader; a JSON play consumed by a flag is caught by nobody until it
   mis-spawns at scale.

**And the asymmetry the review caught, resolved rather than defended.** §2.3 imposes a
MUST (blocked ≠ idle) pre-emptively; the first draft gave the watchdog — the same
silent-stop failure shape, twice recorded — a wait-and-see. The difference in treatment
was never argued. The resolution: the visibility MUST is a cheap render on machinery
already building; a watchdog MUST would be an engine (a timer daemon swarm does not
have). What closes most of the gap at zero concepts: **each leaf play's copyable brief
text embeds its watchdog clause** — a parent who copies the play cannot drop the duty
without deleting a line they are looking at — plus the omission collector in §9.2.

The outside view corroborates rather than opposes (DOCUMENTED — `_hc-industry.md`):
across the surveyed systems (~7 agent frameworks, plus 2 routing gateways and 2
non-LLM analogies — the honest count, per the review), *model-per-role is a
near-universal raw capability, but a named combo pattern with its own API vocabulary
is rare* — aider's main/editor/weak triad and CrewAI's `manager_llm` are the only two
shipped as abstractions; LangGraph and the OpenAI Agents SDK document the
cheap/expensive-model idea **as prose guidance only**. The industry, with every
incentive to productize, mostly landed where §8 lands: the recipe is documentation,
the mechanism is the one existing per-agent field.

**What would earn the machinery, precisely** (committed, §9.2): **one** instance of a
briefed parent mis-assembling a documented play — the model right, the duty absent (a
GLM leaf spawned without a watchdog clause in the brief; a foreign-seat waited on
reports) — and the atomicity argument (a) stops being theoretical. The collector must
also see the silent case the review named: **grep for spawns of any leaf token whose
brief carries no watchdog clause, play named or not** — a parent who never opened
PLAYS.md leaves zero play-name rows but cannot avoid leaving a leaf-token spawn. Then
build `--play`, and let it *expand to* spawn lines (visible, auditable) rather than
*hide* them.

---

## 6. THE ON-THE-FLY SWITCH — "a name is one agent forever," argued and ruled

**The collision, plainly:** standing doctrine says never switch a live agent's model —
respawn a successor; the name is one agent forever; the journal is continuity. The human
has now said, verbatim: *"the children should be able to change their model or the
parents should be able to change the child's model."* That is a request for real
in-place change. I design what was asked, and I find the collision is **apparent, not
real** — but the argument must be made honestly, because if it is wrong the doctrine
should win.

**What "one agent forever" actually protects.** The tombstone exists so history never
blurs two agents into one record (SIMPLEST §3.3); the journal-as-continuity contract
exists so a session that dies or compacts can resume (`WORLD.md` #5). Both are about the
**name** — accountability, history, addressability — not about the process currently
holding it. And the system already treats the process as disposable, routinely and by
design: `cmd_restore` re-injects task + journal tail on every SessionStart, and *"a
killed-and-relaunched pane is indistinguishable from a fresh launch to this hook"*
(VERIFIED — `_hc-mech.md` §3; `bin/swarm:916-935`). The field record agrees, within its
stated limits: **at least** ~10 agents carry same-day resume entries from this
morning's machine restart and picked up their tasks — a floor, not a total; 6 of the 13
named survivors were never individually checked (MEASURED — `_hc-field.md` §B1, caveat
carried); trigger-scout resumed *from its own session-limit death* with the journal as
its only memory: *"resumed after a session-limit death; reconciliation, not new
investigation"* (VERIFIED — `.swarm/journal/trigger-scout.md:1528`). **The model is an
attribute of the incumbent session. Changing it is a restart with a different launcher
line — an event this system already survives daily.** What is genuinely lost is
in-context state not yet journaled — the same *class* of loss as compaction, with one
difference the review made me state instead of eliding: at a compaction the **same
reasoner** rebuilds from the tail; at a downgrade-remodel a **weaker one** must. And
every resume in the record above is same-model, so the safety of *cross-tier* restarts
is REASONED here, not measured — §9.1 is its falsifier, and the direction gate below is
its guard.

**The steelman for respawn-successor, owed before the ruling:** a successor forces a
judgment point — the parent harvests, judges, re-briefs; an in-place switch lets a
failing agent continue un-judged, and burned names are "the record working as designed."
Answer: the judgment point survives, because the switch is itself a recorded, judgeable
act — `remodel` requires a `--reason` and auto-appends `remodeled <old>→<new> by
<caller> — <reason>` to the agent's journal. (Not, as the first draft had it, "flips
the `ps` pin every reader sees" — §2.3 spends two pages proving that reader was absent
for two hours when it mattered. The journal line is the record; the pin is a bonus.)
What respawn-successor buys beyond that is a burned name, and a burned name is the
record of *ended work* — here the work has not ended. But the review refuted the first
draft's further claim that a successor-split *violates* "one agent, one record," and
the refutation is folded rather than argued around: SIMPLEST §3.3's harm is two agents
blurred into **one** record, and a remodel genuinely runs toward that harm — two
differently-capable incumbents now share one journal. What keeps the record honest is
the partition line the verb writes: every tool-written journal entry (`spawned`,
`remodeled`) carries the incumbent model, so a reader can attribute any stretch of the
journal to the tier that produced it. If that proves insufficient in practice — a
parent misjudges pre-swap work by post-swap capability — the blur harm is real,
successor-respawn wins, and §9.1 says how we would see it.

**The ruling: build `swarm remodel`; amend the doctrine sentence rather than the core
idea.** WORLD.md gains one clause: *a name is one agent forever; the session and model
behind it may be replaced, and the journal records each replacement.*

```
swarm remodel <name> --model M --reason "<one clause>"
```

Mechanics — and this is nearly free, which is itself evidence the identity claim is
right (VERIFIED against `_hc-mech.md` §5): rewrite `settings/<name>.launch.sh` via the
existing `write_launcher` with the new token's body; update the `model` field in
`agents/<name>.json` (the `ps` pin); append the journal entry; end the pane's current
occupant; re-run the launcher with the existing `herdr pane run <pane>` — spawn's own
verb, reusable against a live pane id; the SessionStart hook then re-injects task +
journal tail with no new code at all. **One honest gap, priced:** `bin/swarm` today has
no targeted way to stop a pane's occupant (only whole-pane close — `_hc-mech.md` §5,
final item); remodel needs a stop sequence (send-keys exit, verified against a
wedged-at-prompt pane, which is the main real case). That is the verb's build cost, and
it is the same primitive the doorbell already fumbles with (operator.md:199's
second-Enter bug), so building it well pays twice.

**Who may call it, and the direction gate** *(added after adversarial review, which
correctly found the first draft shipped a verb that walked around the mandate
mid-flight — a legal `swarm remodel <live-opus-coordinator> --model sonnet --reason
"cost"` against MODEL-FIT's "downgrading a seat… is always backwards. No exceptions on
cost grounds")*:

- **The parent on a child** — steering, any direction, reason journaled and judged like
  any act. But when the target has live children (it holds a seat) and the move is
  tier-lowering, the verb prints the warning before proceeding:
  `warning: <name> holds a seat (N live children); MODEL-FIT: "downgrading a seat
  spends children to save on the parent." Proceeding — your reason is on the record.`
  A warning, not a refusal: the legitimate case exists (a coordinator whose subtree is
  harvested and closed is a seat in name only), the parent is the party with judgment,
  and the record is the enforcement — consistent with `cmd_send` checking existence,
  not relation (SIMPLEST §3.2).
- **The agent on itself — upward only.** The scope-change case (a leaf discovers its
  task is a tree and remodels up) survived the review's attack and stands. A
  tier-lowering self-remodel is **refused at the verb**: a self-remodel's reason is a
  claim about oneself, the one scoping MODEL-FIT §5 refused because it launders a guess
  into a decision — and self-downgrade is that claim in its least checkable form ("I am
  enough for what remains"). Self-upgrade's error direction is cheap and visible
  (over-spend on a bounded task, on the bill); self-downgrade's is the silent
  fluent-failure §6 of MODEL-FIT exists to prevent. Downgrades go through the parent.
- Tier ordering for the gate is one more fact column in the token table
  (haiku < sonnet < opus, fable unranked pending seat evidence — MODEL-FIT declined to
  invent Fable's mapping and so does this), applying within the Claude family only;
  cross-vendor moves are already restricted below.

**The two triggers the human named, honestly assessed:**

- **Usage limit.** The measured record (MEASURED — `_hc-field.md` §A) says something the
  framing missed: a session-limit death **costs nothing durable** — docs, journal, and
  queue all survive; only `/tmp` scratch was lost; resume-on-restore worked. The binding
  failure was that *nobody noticed for ~2 hours*, because the death rendered as `idle`
  and the Stop hook never fired. So the first-order fix for the limit case is §2.3's
  visibility (already building) plus the re-drive fix — after which the cheapest
  redundancy is often **patience**: the pane says when the limit resets; the agent
  resumes free. `remodel` is the second-order move, for when waiting is wrong — with
  one caveat stated rather than buried: whether a within-Anthropic remodel escapes a
  given limit depends on how the limit is scoped (session vs account), which this repo
  has not measured (§9). The outside record leans against assuming escape: **Claude
  Code's own `--fallback-model` explicitly excludes rate-limit, auth, and billing
  errors from its fallback chain** (DOCUMENTED — `_hc-industry.md:433`, the Claude Code
  row: "excludes rate-limit errors"; restated in its cross-cutting findings) — the
  vendor that knows the limit's scope chose not to route around it with a model
  switch. Cross-vendor remodel of a *seat* is refused by the eval
  evidence (§3): a GLM incumbent in a Claude seat's restore-dependent, report-driven
  contract is precisely what the measurements say fails silently.
- **Scope change.** MODEL-FIT measured 16% of leaves growing into seats unbriefed —
  and the qualifier the first draft dropped is restored, because it decides the remedy:
  **"regardless of model"** (MODEL-FIT §4). Leaf-to-seat drift is not a model problem,
  so `remodel` does not *fix* it — MODEL-FIT's own prescription is structural
  (leaf-cannot-spawn, "the first thing to build if Rung 3 is taken seriously"), and
  that goes on §8's bill where the first draft omitted it. What `remodel` fixes is the
  narrower, real thing: once a leaf's growth into a seat is *noticed and legitimate*,
  the tier can follow the role without burning the name — the child remodels up (or
  asks its parent), one line in the journal, no successor briefing overhead. The
  alternative — it silently coordinates on a leaf model — is the measured 16% with a
  paper trail pointing at the wrong tier.

**No auto-failover, ruled explicitly:** a daemon that remodels on detecting
`[blocked: rate-limit]` would move models with nobody deciding — the 142/143 bug
rebuilt as an engine, against PHILOSOPHY §2. The trigger surface is visible; the verb
is one line; the parent decides. If the record ever shows parents reliably making the
same remodel decision N times in a row, that is a convention proving out, and §8 says
*then* consider the tooling.

---

## 7. THE SMALL-MODEL STRAND — where a non-agentic model fits, if anywhere

The operator's addendum asks where SMALL function-calling models (the Cactus/Needle
family was named as a pointer, explicitly unverified) belong in swarm. The hard
constraint is PHILOSOPHY §4: an SLM's output is a *claim*, so every proposed placement
must answer, in print: **when it is wrong, who notices?** If nobody, the placement is
cut regardless of price — and per PHILOSOPHY §1, the case for any placement must be a
goal argument, never a token-savings argument.

### 7.1 What Cactus/Needle actually is (verification, not inheritance)

Both are real, and the human's pointer was close (DOCUMENTED — `_hc-slm.md` Part 1):
**Cactus** is an on-device/edge inference engine (Cactus Compute, Inc. — mobile and
wearable targets, an OpenAI-compatible local HTTP server, a tiered proprietary
license); **Needle** is their **26M-parameter function-calling model** built for it
(MIT license, JSON-schema tool I/O). Two honest gaps: Needle's context window is
undocumented in every source checked, and *nothing* in either project describes
multi-agent orchestration — the "fits a tree-of-agents system" framing is unsourced
and is not inherited here. The wider class is real and active (Gorilla/OpenFunctions,
Salesforce xLAM 1B–70B, Hammer 0.5B–7B, Octopus-v2, Phi-4-mini, small Qwen, Gemini
Nano, Apple's ~3B "constrained tool calling" — all DOCUMENTED), so the placements
below are argued on the class; Needle's OpenAI-compatible local server means it drops
into the thin-runner row (§2.2) with zero new mechanism if placement (e) is taken.

### 7.2 The placements, each with "when wrong, who notices?"

**(a) The router — an SLM that reads a task and emits `{model, harness, reason}`. CUT,
and this is the sharpest ruling in the strand.** The router answers the ladder's
question *for* the parent. But the ladder's question — "can I cheaply tell that this
child was wrong?" — is a fact about **the parent's own verification capacity**, which
only the parent can answer; that scoping is the load-bearing finding of MODEL-FIT §5
(a reason scoped any other way "launders a guess into a decision", and the compelled
field works *because the parent fills it* — 0/135 mush, 17 recorded behavior changes,
MEASURED). An SLM router does not assist that mechanism; it **deletes** it and replaces
the answer with a guess wearing the mechanism's clothes: the spawn record still shows a
model and a reason, so the audit surface reads as healthy while the thinking it was
built to witness has stopped. When it routes wrong, who notices? **Nobody** — a wrong
routing is indistinguishable from a decision, which is the worst artifact this system
can store (PHILOSOPHY §10). This also disposes of "the SLM makes avenue 2 executable":
making the pattern registry executable is §5's refused engine with a model inside it.

The prior art was checked rather than presumed (DOCUMENTED — `_hc-slm.md` Part 3):
LLM-router research is real and its wins are real (FrugalGPT, RouteLLM: up to 85% cost
reduction at 95% of GPT-4 performance) — but its notice mechanism is an **offline
benchmark**: wrong routes are caught by re-scoring against a labeled evaluation set,
a surface swarm does not have and whose absence is the whole point of judge-by-artifact.
A dedicated study (`arXiv 2606.07587`, "Routing Plateau") finds routers structurally
plateau below oracle accuracy **with failures concentrated on the hardest queries** —
which in swarm terms means the router is most wrong exactly where a wrong model is most
expensive, the inverse of the fit rule (MODEL-FIT §6). And no major framework's official
docs mandate a small model for their router/triage patterns; model size is left to the
developer. The cut stands on its own argument; the prior art, read closely, does not
oppose it.

**(b) The classifier — replace `classify_blocked`'s regex with an SLM. CUT today, with
the door named — and the first draft's security argument struck, because the review
executed its refutation.** The shape genuinely fits — a fixed schema over untrusted
text is exactly what function-calling models are for, and the closed-enum discipline is
already this branch's law (`bin/swarm:694-715`). The first draft claimed the regex
"cannot be sweet-talked"; that is **false** — `BLOCKED_SIGNATURES` is plain substring
matching, and the review forged all three kinds with text ordinary work produces
(`classify_blocked("the rate limit resets at 3pm, I am fine") → 'rate-limit'`). The
code itself only ever claimed the narrower, true property: a **closed codomain** — the
output cannot forge a tree row or the `(you)` marker, whatever the pane says
(`bin/swarm:545-547`). Regex-vs-SLM on forgeability is a difference of degree, not
kind, and the cut does not rest on it. It rests on what survives: the regex ships, is
pure, is deterministic, is unit-testable, and adds no inference dependency to a `ps`
render — and §8's condition (the regex demonstrably failing on a class it cannot
express) has not occurred. The door stays as before.

**A side-defect this design creates and must own** (the review's sharpest §7 catch):
§6 makes `[blocked: rate-limit]` a trigger a parent acts on, and §2.3's labels are
derived from attacker-controlled pane text — so this design builds a **forgeable path
from pane text to a model swap**: any agent can print `resets` + `limit`, go idle, and
read as blocked. The guard is doctrine already latent in MODEL-FIT's standing caveat
("observables lie… it is evidence of nothing until you read the pane") and is now
stated as a rule of this design: **a `[blocked]` row is a prompt to read the pane,
never a sufficient condition to act.** `remodel`'s reason, on a limit trigger, is
expected to quote what the parent saw in the pane itself, not the `ps` label.

**(c) The operator mailbox — triage/summarize the queue. CUT as filtering, on the hard
contract; the annotation half rewritten after the review caught a self-refutation.**
WORLD.md promises *"a message to the operator is never dropped"*; an SLM that filters
or deprioritizes breaks it in the worst way — when it drops the one message that
mattered, the operator never sees what they never saw. Who notices? Nobody, by
construction. That cut is absolute and stands.

The first draft then demanded, as annotation's earning condition, "a record of the
human failing to find the important message" — an observation its own filtering
argument proves can never exist (a missed message is invisible in the record), while
citing live pressure (30 waiting, oldest 20h, 17 from a single sender) in the next
sentence. A stall built out of the document's best sentence, as the review put it.
Rewritten honestly, in three parts: (1) the burial pressure is real and live, and its
first-order answer needs no model at all — `ps` grouping the operator's mail **by
sender** (17-from-one-sender collapses to one line) is a rendering change on the
existing view, and sender-side batching is a convention senders already owe §9 of the
philosophy; (2) annotation (a priority hint beside the full, untouched queue) remains
unbuilt but now has an earning condition that **can** fire: the *duplicate-directive
collector* — an operator directive that duplicates or contradicts an already-queued,
unread report is on-disk proof the queue beat the human's attention
(delivered-timestamps vs directive text; collectible by grep); (3) when that fires,
the annotator that gets built must answer wrong-annotation with "the human, reading
the full list anyway" — which only holds if annotation never reorders or hides, only
marks. The prior-art check came back empty in the direction that would have
challenged the filtering cut: frameworks document LLM triage patterns, but none with
an in-loop party who catches a wrong triage (DOCUMENTED — `_hc-slm.md` Part 3).

**(d) Mechanical harness internals — e.g. summarize the journal tail at restore instead
of truncating at 4000 chars. CUT, and the cut generalizes.** A verbatim tail is a fact;
a summary is a claim — and a subtly wrong resume memory is invisible until the agent
rebuilds on it. *"An honest unknown beats a plausible wrong value"* (PHILOSOPHY §10) is
the whole argument. The same reasoning cuts SLMs from every hook-path role: the four
hooks are deliberately `try/except → exit 0` fact-witnesses; putting a model call inside
one adds a nondeterministic dependency to the machinery whose only job is to witness
facts deterministically.

**(e) The model of a one-shot leaf — KEEP; it is the one placement, and it is already
in the design.** The thin-runner row (§2.2) takes any OpenAI-compatible endpoint. A
small function-calling model behind that row does rung-3 work at volume: schema-filling,
tagging, extraction into a fixed format — a *forced function call as the artifact*.
When wrong, who notices? **The parent, cheaply, by construction**: rung 3's whole
definition is that the artifact is mechanically checkable, and the parent's spot-check
plus the floor-not-total discipline (MODEL-FIT §4) is the safety net. The leaf holds no
session, clears no dialogs, keeps no journal — every survivability and seat-discipline
failure mode from §2.4 and §3 is structurally absent. This is a goal argument, not a
cost one: it puts bulk mechanical work where being wrong is cheap to catch, which is
the fit rule verbatim (MODEL-FIT §6).

The class's measured failure modes size the discipline (DOCUMENTED — `_hc-slm.md`
Part 2): reliability numbers are real but largely self-reported (xLAM-7B 88% on
BFCL-v1-era scoring; Octopus-v2's 99.5% is its own narrow benchmark), and the
quantified weakness is **trigger judgment** — 38.2% unnecessary calls (Qwen3-8B) and
39.0% missed calls (Llama-3.2-3B) on the same 2026 benchmark, with judgment *not*
scaling monotonically with size. Design consequence, stated as a rule: **the SLM leaf
is always a forced function call against a parent-supplied schema — the model never
decides *whether* to call, only fills *what*.**

The review refuted the first draft's enforcement of that rule, and the refutation is
adopted as a design change rather than argued with. The draft said briefs violating
the rule "must be refused" — in the passive, with no agent, which meant: by the
parent's unenforced judgment, the mechanism this repo has measured failing three
separate ways. And FLEET §3B's bare `curl` carries no `tool_choice` and no schema, so
nothing at the seam held the rule. **Fixed at the seam it must live at: the SLM-token
launcher body is a distinct runner template whose request embeds the parent-supplied
JSON schema with `tool_choice: required`, and which exits with a refusal — written to
the status file, like any launch failure — when the leaf brief carries no schema.** No
schema, no launch; the rule is structure, not vigilance. (On §8's bill with the other
launcher bodies — none of which exists today.) What remains for the parent is what a
parent can actually do: spot-check the filled artifact (malformed args and
hallucinated enum values are exactly what mechanical inspection catches) and honor the
floor-not-total discipline for the omission direction, which no inspection sees
(MODEL-FIT §4). The review's mirror charge — that the first draft held the operator's
router to a witnessing standard its own kept placement failed — was correct, and this
is the repair: the forced call is now witnessed by the runner's own refusal behavior,
not by an audit surface that reads healthy while nothing checks it.

### 7.3 Inside or beside the harness — ruled

**Beside. Never inside.** "Inside" means the launcher/hook path — deterministic,
fail-safe, fact-witnessing machinery; (d) shows why a model call does not belong there.
"Beside" means: as the *workload* of a one-shot leaf (e), or — if ever earned — behind
a closed-enum contract in a `ps`-side classifier (b) or an annotate-never-drop
middleware (c), all of which are readable, optional, and fail toward today's behavior.
The Haiku ban seals the general point from the other direction: if a frontier chat
model can fail the *agent slot* on a permissions capability, a model that can only emit
a tool call was never a candidate for it. The small model's place is beside the
harness, emitting checkable artifacts — never holding a seat, never inside a hook.

---

## 8. WHAT I WOULD BREAK, AND WHAT THIS COSTS

The honest bill, nothing laundered:

- **`bin/swarm` changes:** the token table + three launcher bodies beyond `claude`
  (opencode leaf with swarm-verb denial in its config, thin runner, and the SLM runner
  variant that refuses schema-less briefs — **none of the three exists today**) with
  `SWARM_PARENT` (FLEET's costed one-flag-one-env-var, adopted); **spawn writing a
  `permissions` block** — moved onto this bill by the review's F1: it is the measured
  cause of the wedge the first draft misattributed to Haiku, and every admitted model
  depends on it; the survivability gate refusal at spawn (contents provisional, §2.4);
  `--model default` resolution; **`swarm remodel`** — three writes, one reused pane
  verb, the direction gate (§6), plus the one genuinely new mechanic: a verified
  stop-the-occupant sequence (`_hc-mech.md` §5 — does not exist today, and its cousin,
  the doorbell's unreliable Enter, is a known bug; budget it as real work, not a line).
- **The FLEET §5 liveness protocol** for opencode leaves — done-signal convention +
  parent-side watchdog. FLEET priced this honestly and this design repeats it: the
  happy path is an afternoon; the unhappy paths (early idle, silent soft-kill, crashed
  plugin) are the real time. cheap-sweep avoids the whole bill (exit+file is the done
  signal); glm-tool-leaf pays it.
- **The mandate's blast radius** (required `--model`/`--reason`): at least ~9 test
  call-sites and 12 doc files — a floor, not a total (MEASURED, MODEL-FIT §5) — plus
  every existing skill/brief that spawns.
- **Doctrine edits:** one WORLD.md clause (§6's amendment — this *is* a change to a
  core idea's letter, defended above, and the human should judge it as such); a spawn
  step in `skill/SKILL.md`; the new `docs/PLAYS.md`.
- **What non-Claude rows give up:** leaves do not journal, do not restore, do not hold
  the duties contract — the parent journals about them and owns their liveness. This is
  leaf-only by evidence, not caution (FLEET + the eval), and it means the "chinese
  models" patterns are narrower than the human's original sketch: constrained seats and
  tool-leaves, not peers.
- **Remodel's real loss:** un-journaled in-context state dies at the switch, and a
  remodel across harness classes (claude ↔ opencode) carries *only* the journal — for
  seats that is a migration, not a switch, and the design says so rather than enabling
  it casually.
- **What I did not build and why:** no auto-failover (§6), no `--play` flag (§5), no
  router (§7a). And the omission the review caught this list hiding, now named: **the
  structural leaf-cannot-spawn change for Claude-family leaves** — `cmd_spawn` checks
  no relations; every child gets the full verb set; MODEL-FIT calls the structural fix
  *"the first thing to build if Rung 3 is taken seriously"* and this design does not
  build it. Foreign-row leaves are structural leaves by construction (§2.2: toolless
  runner; opencode config denies swarm verbs), which contains the blast radius of the
  new tokens — but a *Claude* cheap leaf's "I will not become a parent" remains an
  unenforced promise, and this design knowingly ships on top of that.

---

## 9. FALSIFIERS

Committed before defense; each names the observation and its collector.

1. **The remodel-identity ruling (§6).** Two observations, either kills it: (a) if
   remodeled agents measurably flounder — re-ask the parent what they were doing, redo
   finished work — at a rate worse than fresh spawns briefed from the same journal,
   the "restart with a different launcher line" equivalence is wrong (note the
   baseline's limit: today's clean-resume record is all same-model, a floor of ~10
   with 6 of 13 unchecked — `_hc-field.md` §B1); (b) if a reader demonstrably
   misattributes journal work across a remodel partition line — judges pre-swap work
   by post-swap capability — the two-workers-one-record blur is real and
   respawn-successor should stand. *Collector:* the first N remodels' journals +
   parent judgments.
2. **The plays-as-convention ruling (§5).** **One** briefed parent mis-assembling a
   documented play — right model, missing duty — earns `--play` (expanding to visible
   spawn lines, never hiding them). *Collector, both holes covered:* journal grep for
   play names vs. briefs actually sent, **plus** a grep for any leaf-token spawn whose
   brief carries no watchdog clause, play named or not — the silent case where a
   parent never opened PLAYS.md. Also collect the reason-degeneration signal from
   §5's argument 1: verification clauses on play-cited spawns vs. free spawns.
3. **The priority line and the static reason (§4.2, §4.3).** If spawn reasons never
   cite the declared priority within the first fifty mandated spawns, the line is dead
   text — delete it rather than mechanize it. And if a static operator's
   `--model default` reasons converge to one frozen string including the verification
   clause, that is the theater case MODEL-FIT's 0/135 was never tested against.
   *Collector:* grep of recorded reasons; uniqueness count on default-spawn reasons.
4. **The survivability gate's rows (§2.4).** The probe that matters first — named by
   the gate's own source as its top re-run item and never run: **spawn an Opus-pinned
   child into the same first-touch permission wall.** If Opus clears what Haiku could
   not, the per-model row is earned; if Opus also wedges, the row is the infrastructure
   defect wearing a model's name, and the permissions-block fix (§8) is the whole
   story. Independently: a gated model demonstrably holding a session (e.g. Haiku
   gains an auto mode) makes its row stale — re-verify per harness release.
   *Collector:* the Opus probe (cheap, scriptable today); one probe spawn per gated
   token per claude-cli release thereafter.
5. **The SLM leaf (§7e).** If small-model one-shot artifacts fail parent spot-checks at
   a rate that consumes the parallelism they bought — or fail in the omission direction
   spot-checks cannot see — the tokens come off the table. *Collector:* spot-check hit
   rate on the first real cheap-sweep, with one double-counted census as the
   omission control (MODEL-FIT §4's floor-not-total discipline).
6. **The foreign-seat play (§5).** A deepseek/GLM seat run under the constrained
   protocol (artifact-polling parent) that drops work *despite* the constraints — or,
   symmetrically, a clean run that suggests the constraints are too tight. Either moves
   the play's text. *Collector:* re-run one FLEET-EVAL-V3 delegation cell under the
   play's exact protocol.
7. **The limit-remodel caveat (§6).** Whether a within-Anthropic remodel escapes a hit
   limit is unmeasured. If it does not (account-scoped limits), remodel's usage-limit
   trigger shrinks to cross-row moves and patience, and the doc must say so.
   *Collector:* one deliberate remodel of a limit-blocked scratch agent.
8. **The no-router ruling (§7a).** The prior-art check ran: router systems catch wrong
   routes by *offline benchmark re-scoring*, a surface swarm does not have — so the cut
   stands. The live falsifier is now narrower: if swarm ever grows a labeled evaluation
   surface for spawn decisions (e.g. parent verdicts systematically recorded against
   model pins, making wrong-routes *scorable in the loop*), the router must be
   re-argued against that mechanism. *Collector:* the existence of that surface, plus
   `_hc-slm.md` Part 3's plateau caveat (router failures concentrate on the hardest
   queries) re-checked against it.
9. **The structural leaf denial (§2.2).** A foreign-row leaf (opencode or runner
   token) that ever produces a descendant means the swarm-verb denial failed and
   FLEET §7's "enforceable, cheaply" was wrong — the foreign tokens then widen the
   measured 16% leaf-to-seat drift instead of containing it, and they come off the
   table until the denial is fixed. *Collector:* `ps`/`agents/` parent fields — any
   child whose parent is a leaf-token agent.
10. **The duplicate-directive collector (§7c).** An operator directive that duplicates
    or contradicts an already-queued, unread report is on-disk proof the mailbox beat
    the human's attention; the first confirmed instance earns annotate-never-drop
    middleware (and only that). *Collector:* `queue/operator/` timestamps vs. the
    directive's content and time.

---

## 10. ADVERSARIAL REVIEW DISPOSITION

The first draft was reviewed by `hc-red` (fresh eyes, refute-brief, Opus; report at
`docs/design/HARNESS-RED.md`, evidence in `docs/audit/_hcr-*.md` — 45 tag-checks: 21
clean, 15 overstated, 7 wrong, 2 unverifiable). Every finding is disposed of below;
nothing was folded silently and nothing rebutted was left unedited in place.

**Folded (the review was right, the doc changed):**

- **F1 — the survivability gate was built on a source that forbids it.** The wedge's
  measured cause is an all-models permission gate; the Opus settling probe was never
  run; the first draft's §2.4 and §8 stated contradictory causes for the same event.
  §2.4 rewritten: gate contents provisional, permissions block moved onto this bill,
  the Opus probe is now §9.4's first item. The most serious error in the draft.
- **F2 — the mandate was spent as sunk cost.** PR #83 is open and its shipped ruling
  keeps `--model` optional; the mandate is the human's declared direction, specified
  but unbuilt. §3 and §4.4 rewritten to price it rather than spend it.
- **§4.2's config-injected priority line — cut entirely** (three kills: the §5 test
  unapplied to my own key; a wired free-text injection channel; a falsifier that could
  not fire). The priority is now the first line of PLAYS.md — prose, no wiring.
- **§6 had no direction gate** — a legal mid-flight seat downgrade against MODEL-FIT's
  "no exceptions on cost grounds." Added: seat-downgrade warning, flat refusal of
  tier-lowering self-remodel, model-stamped tool entries in the journal.
- **§6's tombstone clause** ("a successor-split is closer to violating one-agent-one-
  record") — struck; it read SIMPLEST §3.3 backwards. The remodel-side blur risk is now
  owned, with the partition-line mitigation and §9.1(b) as its falsifier.
- **§7b's "cannot be sweet-talked"** — struck; the review forged all three enum kinds
  with ordinary text. The cut re-rests on determinism/testability/§8, and the
  forgeable pane-text→remodel path is owned as this design's own side-defect with the
  read-the-pane rule as its guard.
- **§7c's annotation earning-condition** — was unmeetable by the doc's own filtering
  argument; replaced with the duplicate-directive collector (§9.10), which can fire.
- **§7e's forced-call rule** — was an unenforced convention at a seam (bare curl) that
  couldn't hold it; moved into the SLM runner template itself (no schema, no launch).
  The review's mirror charge — one witnessing standard for the operator's router,
  another for my kept placement — was correct and this is its repair.
- **§5's argument 2 premise** — "the convention has not even shipped" was false
  (FLEET.md:286 writes the watchdog convention). Rewritten; the earning condition
  dropped from "more than once" to a one-strike hair trigger with the
  silent-omission grep added. *(Second-pass correction via LOOP-RED: the v2 GLM
  hang first cited as the failure record was itself retired by the eval —
  V3:123-124; the argument now stands on the live v3 no-watchdog risk instead.)*
- **§5's argument 1** — 142/143 was a MEASURED number deployed to carry a REASONED
  claim about play tokens that have never existed; re-marked REASONED with its own
  falsifier (§9.2).
- **§8's omission list was missing its largest omission** — structural
  leaf-cannot-spawn, "the first thing to build" per this design's own primary source.
  Named; foreign rows made structural leaves by construction (§2.2, §9.9).
- **Evidence repairs throughout:** the fabricated pincite (`_hc-mech.md §5.3`), the
  misattributed quotation (the collector's summary promoted to a journal quote —
  replaced with the real line from `trigger-scout.md:1528`), the nonexistent
  `.swarm/config` file claim, 3/7-vs-4/7 normalized to the source's 4/7, 83→87 rows,
  rotted FLEET §2 line numbers re-verified at current lines, and the three caveats
  that had died in transit restored (the D4 magnitude confound; the ~10-resumes
  floor; three-observers-one-instrument).

**Rebutted or narrowed (with the reasoning on the record):**

- **"22 concepts" (§4.4):** accepted as the honest measure over flag-count, but most
  of the enumerated concepts are swarm's own, not this design's additions; the claim
  is now stated comparatively (every examined alternative carries the same floor plus
  its own machinery) rather than rebutted outright.
- **Parent-called seat downgrades are warned, not refused (§6):** the review asked for
  a gate at the verb; the legitimate case (a harvested seat, now a seat in name only)
  is real, the parent is the judging party, and a hard refusal would be a rule engine
  where the record is the enforcement. Self-downgrade *is* refused — there the
  reason-scoping argument (a self-claim) has no counterparty.
- **The review's own headline framing** ("evidence REFUTED as a discipline") was
  self-corrected by the reviewer mid-flight (45 checks, 21 clean, not 24/24 bad) — a
  correction it sent unprompted, in its own disfavor, and which is noted here because
  the review earned the same honesty it demanded.

**What the review could not break, on its own record:** the core recommendation
(launcher-body-as-the-one-variable), the coupling claim, `--model default`, the
scope-change remodel trigger, the router cut, the mailbox filtering cut, the
blocked-visibility requirement, and the industry corroboration for
patterns-as-convention. The signature it found — citation quality tracking distance
from the source, exact into audited code and decorative into my own children's
artifacts — is owned as this document's most instructive defect, and it is exactly
the confident-wrong shape this repo's doctrine exists to catch.

---

*All five child evidence artifacts (`_hc-eval-table`, `_hc-field`, `_hc-mech`,
`_hc-industry`, `_hc-slm`) are harvested and folded in; the adversarial review
(`HARNESS-RED.md`, `_hcr-*.md`) is disposed above. No sections pend.*
