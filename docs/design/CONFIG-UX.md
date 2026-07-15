# CONFIG-UX — one spawn command, one config file, one discovery verb

> **Superseded in mechanism by [docs/design/PRODUCTIZE.md](PRODUCTIZE.md).** The
> unification goal here — one spawn command, one config file, one discovery
> verb — stands, and PRODUCTIZE.md builds it. Four operator overrides changed
> *how*, not *whether*: config is **JSON**, not the flat-TOML sketched below;
> an alias names its harness **explicitly** (`{"harness": "yoke", "model":
> "..."}`), not by a `/` in the token; there is **no `default` alias** — a
> spawn naming no model is always an error; and `--permission-mode` is
> **expressible for yoke** (mapped to opencode's permission model), not
> refused outright. This document is kept as the record of the goal and the
> reasoning that got there — read PRODUCTIZE.md for what was actually built.

*config-ux, 2026-07-15. Design for Layers 1–2 of model/harness configuration.
Layer 3 (configuration-as-conversation) is acknowledged in §8 and deliberately not designed.*

---

## The answer first

Three surfaces, and only one of them is new machinery:

1. **`swarm spawn --model X` is the only spawn tool.** After alias lookup, a model
   token containing `/` (like `deepseek/deepseek-v4-flash`) routes to the opencode
   harness; a bare token (`opus`, `sonnet`, `fable`, `haiku`, `default`) routes to
   Claude, exactly as today. You never call spawn-oc.py yourself.
2. **`.swarm/config` grows one section: `[models]`.** It is an alias table — short
   names you choose, mapped to real model tokens. `default` is just an alias with a
   special job. One more key, `[harness] opencode`, says where the opencode launcher
   lives. That is the whole schema.
3. **`swarm models`** shows everything you can spawn — Claude tokens and opencode
   providers in one table — with harness, readiness, and what each is trusted for.

The state layer needs **nothing**: the opencode launcher already writes the same
journal tombstone and agent record as `bin/swarm` (spawn-oc.py:6–16 mirrors
bin/swarm:1424–1497), so mixed trees already render in `swarm ps` — a Fable parent
with Sonnet and DeepSeek children in one tree is on record (harness/MIXED-TREE-PS.txt).
The whole gap is dispatch and discovery. That is what this design adds, and only that.

---

## 1. Sixty seconds from nothing to a GLM-cheap, Opus-judgment swarm

```console
$ swarm models
MODEL      HARNESS   READY   TRUSTED FOR
opus       claude    yes     seat — judgment, coordination
sonnet     claude    yes     seat
fable      claude    yes     seat
haiku      claude    yes     leaf
default    claude    yes     alias — not set; resolves to bare `claude` (its default)

no opencode harness configured — cheap providers (deepseek, zai-coding-plan) are
authed but unreachable. To enable, add to .swarm/config:
  [harness]
  opencode = /Users/vadrsa/git/swarm-rnd/harness/spawn-oc.py
```

The user edits `.swarm/config` (creating these sections; `[middleware]` may already
be there — this file already exists as a read surface, bin/swarm:479, :514):

```toml
[harness]
opencode = /Users/vadrsa/git/swarm-rnd/harness/spawn-oc.py

[models]
default = sonnet
glm     = zai-coding-plan/glm-4.7
flash   = deepseek/deepseek-v4-flash
judge   = opus
```

```console
$ swarm models
MODEL      HARNESS    READY   TRUSTED FOR
opus       claude     yes     seat — judgment, coordination
sonnet     claude     yes     seat
fable      claude     yes     seat
haiku      claude     yes     leaf
default    claude     yes     alias → sonnet
judge      claude     yes     alias → opus
glm        opencode   yes     leaf — alias → zai-coding-plan/glm-4.7 (duty-loop, verified 2026-07-15)
flash      opencode   yes     leaf — alias → deepseek/deepseek-v4-flash (duty-loop, verified 2026-07-15)

opencode providers authed: deepseek, zai-coding-plan. Any provider/model id they
serve is spawnable directly, e.g. --model deepseek/deepseek-reasoner.
seat = trusted to coordinate children. leaf = verified worker; judgment work stays
on Claude models pending evidence (docs/design/LOOP.md §4).
```

Then spawning is one command regardless of harness:

```console
$ swarm spawn extract-1 "pull every cite from FLEET.md into a table" \
    --model flash --reason "table I will spot-check row by row"
extract-1

$ swarm spawn review-1 "judge extract-1's table against the source" \
    --model judge --reason "judgment I would otherwise redo myself"
review-1

$ swarm ps
├─ you (operator)
│  ├─ extract-1 model=deepseek/deepseek-v4-flash [live] q=0 idle 10s
│  └─ review-1 model=opus [live] q=0 idle 4s
```

Note what `ps` shows for the opencode child: the **resolved** token, not the alias.
The record keeps the decision (which real model runs); the alias was just how you
typed it. Same rule as today's `default` → launcher-silence collapse (bin/swarm:1397–1403 —
the launcher gets `""`, but the record keeps `default` verbatim): the journal
keeps what you asked for, the record keeps what runs.

---

## 2. How `swarm spawn --model X` dispatches — the mechanics

All inside `cmd_spawn`, after the existing name/reason mandate checks
(bin/swarm:1384–1395) and before any file is written:

```
token = --model value
1. Alias lookup: if .swarm/config [models] has `token = value`, token becomes value.
   One hop, no recursion — an alias must resolve to a real token, not another alias.
2. If token contains "/":                            → OPENCODE PATH
     provider = token up to first "/"
     a. [harness] opencode must be configured and executable, else die (§5 error text)
     b. provider must be a key in ~/.local/share/opencode/auth.json, else die
     c. run (subprocess, NOT exec — bin/swarm stays alive to report):
        <harness-script> <name> "<task>" --model <token>
            --parent <own agent id> --reason "<--reason value>" --swarm-dir <root>
     d. propagate: bin/swarm waits, passes the harness's stdout/stderr through,
        and exits with its exit code. On a harness failure, bin/swarm is the one
        that says "spawn failed" and points at the boot log — never a silent death.
     The harness script claims the name, writes the record, boots the agent —
     bin/swarm writes NOTHING on this path. One name-claimer per path, no race.
3. Else:                                             → CLAUDE PATH (unchanged)
     token must be in SPAWN_MODELS (bin/swarm:66) or die listing what IS accepted —
     the same synchronous refusal as today (bin/swarm:1389–1392), now also naming
     configured aliases and pointing at `swarm models`.
```

Why `/` is the dispatch key and not a new `--exec`/`--harness` flag:

- **It is already the format.** spawn-oc.py requires `provider/model` and dies
  without the slash (spawn-oc.py:161–163). Claude tokens never contain one. The
  distinction exists in the data; a flag would configure a distinction the token
  already carries — the §5 failure exactly.
- **It survives `ps`.** `/` is not in `MODEL_STRUCTURAL` (bin/swarm:47) and real
  provider/model ids fit `MODEL_CAP = 40` (bin/swarm:36). Verified against the
  rendering rules, not assumed.
- **It is what FLEET.md designed, minus the flag.** FLEET.md §4 proposed
  `--exec opencode` "(or a per-model alias)" selecting the launcher body
  (FLEET.md:217–222). This design takes the per-model-alias branch: the launcher
  body is selected by the resolved token's shape. Concept cost drops from one flag
  to zero flags.

What stays uniform across both paths — the parts of the spawn contract that make a
child a swarm citizen regardless of harness:

| Contract item | claude path | opencode path |
|---|---|---|
| `--model`/`--reason` mandate | bin/swarm:1384 | same check, same place (before exec) |
| journal tombstone, O_CREAT\|O_EXCL | bin/swarm:1426 | spawn-oc.py:86–93 |
| agent record with model+reason | bin/swarm:1494–1497 | spawn-oc.py:204–208, 249–253 |
| herdr pane, observable process | bin/swarm launcher | spawn-oc.py:235–247 |
| queue created on demand by senders | bin/swarm:422–445 | same (spawn-oc.py:14–15) |
| readiness | status-file wait; ambiguity is life (bin/swarm:1499–1508) | health assert inside the harness (spawn-oc.py:255–268); **a boot failure burns the name — see below** |

What is honestly NOT uniform yet — refuse loudly rather than pretend:

- **`--permission-mode` is Claude-only.** The opencode harness runs headless; an
  "ask" is a silent wedge, so its policy is fixed at wildcard-allow with the two
  interactive gates denied (spawn-oc.py:177–191, operator-authorized 2026-07-15).
  Passing `--permission-mode` with a `/` model dies with one sentence saying so.
- **`--cwd`/`--trust` are Claude-only.** Opencode agents get harness workspaces
  (`ws-<name>/`, spawn-oc.py:168). Same rule: die, one sentence, no silent ignore.

These two refusals are the honest edge of the unification: one command, but not a
pretense that the harnesses are the same machine.

**The name-burn asymmetry, stated plainly** (found by red-team, finding #1): on the
claude path every refusal fires before the name is claimed, so a failed spawn never
burns a name. On the opencode path the harness claims the tombstone and writes the
record (spawn-oc.py:86–93, :204) *before* its 60-second health assertion — so a
server that never comes healthy exits 2 with the tombstone on disk. **The name
burns.** This design keeps that, deliberately, rather than rolling back: deleting a
tombstone after a maybe-just-slow boot is exactly the tear-down-healthy-agents
mistake bin/swarm already made once and reversed (PHILOSOPHY §4 — "ambiguity as
life"). A burned name recording a failed boot is the record working as designed.
What the design requires instead is honesty at both ends: spawn-oc.py appends a
"boot failed" entry to the tombstone it leaves behind, and bin/swarm (alive,
because subprocess) prints the failure with the boot-log path. The §5 "name was
not burned" promise is therefore scoped: it holds for every pre-dispatch refusal
on both paths, and does not hold past the handoff.

**Required changes to spawn-oc.py — three, not one** (the first draft of this doc
said "one flag"; the red-team showed that was wrong):

1. **`--reason`** (today it fabricates its own at spawn-oc.py:166). The parent
   chose the model; the parent's reason belongs in the record — same mandate as
   every other spawn.
2. **Root threading.** spawn-oc.py hardcodes `SWARM_DIR = "/Users/vadrsa/git/
   swarm/.swarm"` (:49); it matches bin/swarm's dynamically-resolved root only by
   coincidence on this one machine. It must honor a `--swarm-dir` argument (passed
   in step 2c) or the `SWARM_DIR` env var, else the "same file contract" claim is
   false anywhere but this checkout and `swarm ps` splits across two `.swarm` dirs.
3. **Real port acquisition.** `4200 + (abs(hash(name)) % 400)` (:164–165) is
   per-process randomized (Python salts `hash()`; verified by the red-team) and
   collision-prone with no retry — a colliding bind is a failed boot, which is a
   burned name. Replace with bind-`:0`-and-read-back (or an equivalent free-port
   scan) before this script is called "the mechanism."

---

## 3. `.swarm/config` — the exact schema

The file already exists as a wired surface: `[middleware]` on the send path
(bin/swarm:479) and `[spawn] permission_mode` on the spawn path (bin/swarm:514),
both parsed by `read_flat_toml` (bin/swarm:448), both fail-open. This design adds
**two sections, no new parser, no new file**:

```toml
# .swarm/config — everything swarm reads is in this one file.

[spawn]
permission_mode = auto            # exists today (bin/swarm:514)

[middleware]                      # exists today (WORLD.md:73-84) — unchanged
# command = ...

[harness]                         # NEW
opencode = /Users/vadrsa/git/swarm-rnd/harness/spawn-oc.py

[models]                          # NEW — an alias table, nothing more
default = sonnet
glm     = zai-coding-plan/glm-4.7
flash   = deepseek/deepseek-v4-flash
judge   = opus
```

Every key defended against PHILOSOPHY §5 ("first ask whether the thing it
configures should exist at all"):

- **`[harness] opencode`** configures a machine-specific fact swarm cannot derive:
  where the fork's launcher lives. Today that is an R&D checkout path; no default
  could be right. When the harness graduates into the swarm repo, this key gets a
  shipped default and disappears from most users' files. Fail-closed on purpose:
  a `/` model with no harness configured is a refusal with instructions, not a
  guess. (Fail-open is for degrading extras like middleware; a spawn target is not
  an extra.) It is a section of one key, and that is fine because a path key wants
  a home named by what it locates — not because it anticipates more keys. If a
  third harness ever exists, it must earn its key then (§8); this section is not
  pre-provisioning for it.
- **`[models]` aliases** exist because the real tokens are unmemorable
  (`zai-coding-plan/glm-4.7`) and because a name is where policy lives. "Role-based
  defaults" from the brief collapse into this table with zero new concepts: name an
  alias `judge` or `cheap` and you have stated "judgment → opus, cheap → GLM" as
  vocabulary rather than as a rules engine. **PLAYS.md folds in the same way**: a
  play, at this layer, is a named model choice. Anything richer — "which model
  combo for which kind of task" — is delegation doctrine and lives where doctrine
  lives (skill/SKILL.md:45–65, MODEL-FIT.md), not in config. A recipe engine fails
  §8: no convention of multi-model recipes exists yet to earn tooling.
- **`default = <token>`** closes a gap bin/swarm's own comment names: "142 of 143
  spawns inherited a default nobody chose" (bin/swarm:53–56). Today `--model
  default` collapses to bare `claude` — whatever Claude's own default is. With this
  key, `default` resolves through the same alias table as everything else, to a
  value the user chose. Unset, behavior is exactly today's. No new mechanism —
  `default` is one more row in the table.

Deliberately absent, by name:

- **No `[roles]` section, no per-task routing rules.** The parent choosing
  `--model` *is* the router — that judgment is the delegation doctrine's job, and
  automating it is Layer 3's job if it is anyone's.
- **No per-model cost/price keys.** No price data exists in the system; a config
  key would be a guess wearing a schema (§10: honest unknown beats plausible wrong).
- **No harness registry / plugin list.** There are exactly two harnesses. Two is a
  conditional, not a framework. A `[harness]` section with one key leaves room for
  a second key if a third harness ever earns one.
- **No seat/leaf capability keys.** Capability is evidence, not configuration —
  it lives in LOOP.md's measured record and surfaces read-only in `swarm models`.

---

## 4. `swarm models` — the discovery verb

One read-only command, PHILOSOPHY §8's permitted "visibility verb." It reads three
things and writes nothing:

1. **Builtin Claude tokens** — `SPAWN_MODELS` (bin/swarm:66), ready if `claude` is
   on PATH (same check install.sh:52 makes).
2. **Opencode providers** — the key names of `~/.local/share/opencode/auth.json`
   (values never read past the key list), ready if `[harness] opencode` is set and
   executable. The user never opens auth.json; this command is why.
3. **Aliases** — `.swarm/config [models]`, each shown with its resolution and the
   harness it lands on.

Output is the table shown in §1. Three honesty rules in its design:

- **Per-provider model ids are not enumerated.** Nothing on disk lists what
  `deepseek/*` serves, and inventing a list would print plausible-wrong ids. The
  footer says the true thing: any `provider/model` the provider serves is
  spawnable, and a wrong id fails at spawn with the provider's own error.
- **TRUSTED FOR states the measured record, defined in the footer** (§9: define
  the term or drop it). Claude models: seats. Opencode models: "leaf — duty-loop,
  verified <date>" — because that is exactly what has been verified (6/6 CONFIRMED,
  harness/SEAT-VERIFY.md; judgment seats explicitly UNKNOWN pending LOOP.md §4's
  Build 2). When Build 2 passes for a model, this column changes — evidence in,
  doctrine out, never config.
- **Cost shown per harness, only as measured.** Claude tokens: plan/subscription.
  Opencode: "API-billed; measured ~$0.015 per real task" (harness/MORNING.md:32).
  No per-model price table to rot.

---

## 5. The errors a user actually sees

Typo in a model name (claude path unchanged, message extended):

```console
$ swarm spawn w1 "..." --model gml --reason "..."
spawn: unknown model 'gml'. Accepted: opus, sonnet, fable, haiku, default,
and your aliases from .swarm/config: glm, flash, judge. Run `swarm models`
to see everything spawnable. (Name 'w1' was not burned.)
```

A `/` model with no harness configured:

```console
$ swarm spawn w1 "..." --model deepseek/deepseek-v4-flash --reason "..."
spawn: 'deepseek/deepseek-v4-flash' needs the opencode harness, and .swarm/config
has no [harness] opencode entry. Add:
  [harness]
  opencode = /path/to/spawn-oc.py
(Name 'w1' was not burned.)
```

A provider that is not authed:

```console
$ swarm spawn w1 "..." --model openrouter/qwen3-coder --reason "..."
spawn: provider 'openrouter' is not authed — auth.json has: deepseek,
zai-coding-plan. Run `opencode auth login` to add one. (Name 'w1' was not burned.)
```

A Claude-only flag on an opencode spawn:

```console
$ swarm spawn w1 "..." --model glm --permission-mode plan --reason "..."
spawn: --permission-mode applies to claude models only; the opencode harness runs
a fixed policy (allow-all, interactive gates denied — headless agents cannot
answer an ask). Drop the flag. (Name 'w1' was not burned.)
```

All four keep today's refusal contract: synchronous, before any file is written,
name not burned (bin/swarm:1373–1383's ordering preserved). **That promise is
scoped to pre-dispatch refusals.** Past the handoff there is one more failure a
user will meet — the opencode server never comes healthy — and there the name IS
burned (see §2). What the user sees, from bin/swarm, alive because subprocess:

```console
$ swarm spawn w1 "..." --model flash --reason "..."
spawn: opencode harness failed — server on port 4361 never passed health in 60s.
Boot log: /Users/vadrsa/git/swarm-rnd/harness/ws-w1/boot.log
Name 'w1' is burned; its journal records the failed boot. Pick a new name.
```

---

## 6. What happens to spawn-oc.py — migration, said clearly

**It stays, as the mechanism. `swarm spawn` becomes the only doorway.**

- spawn-oc.py is the harness: workspace, plugin pump, permission policy, serve-mode
  boot, health assertion, liveness probe. All of it proven overnight and
  adversarially verified. `swarm spawn` execs it — it does not reimplement it.
- Its CLI already matches the dispatch needs (`<name> "<task>" --model --parent`);
  it grows exactly one flag (`--reason`, §2). Nothing else changes in it now.
- Calling it directly keeps working — it is plumbing, and plumbing that refuses
  direct use is a lie about layering. But no doc points users at it; `swarm world`
  and SKILL.md's model doctrine (skill/SKILL.md:45–65) describe only `swarm spawn`.
- **Later, not now:** when the fork leaves the R&D checkout, the launcher body gets
  absorbed into bin/swarm the way FLEET.md §4 sketched, and `[harness] opencode`
  gains a shipped default. That absorption is earned by the harness stabilizing —
  §8's sequencing — not scheduled by this design.

install.sh gains one honest line only when dispatch ships: its prereq check
(install.sh:52–59) mentions that opencode models additionally need `bun` and a
configured `[harness]` — stated as optional, not a new hard prerequisite.

---

## 7. Adversarial review — what the red-team found, and what changed

An independent opus red-team (cfg-red) attacked the first draft on the two axes
the brief ordered. Full findings with evidence: `.swarm/tmp/config-ux/red.md`.
Score: 0 kill, 3 fix, 3 nit, 6 attacks that failed (failed attacks are data too).
All three fixes are incorporated above; none required changing the architecture.

**Minimality survived.** `default` is genuinely one more alias row, not a smuggled
mechanism (finding #9, attack failed). The PLAYS/roles→aliases fold loses nothing
a user needs today (finding #10, attack failed — richer routing is doctrine, not
config). The one hit: the `[harness]` section's original defense ("room for a
second key") contradicted the doc's own registry refusal — the defense is now
honest (finding #8, fixed in §3). Verdict stands: 5 example keys, each with a
named user need.

**Dispatch survived, but the first draft hand-waved three joints:**

1. **Name-burn on boot failure** (finding #1, the worst): the opencode path claims
   the name before its health assert, so a failed boot burns the name — and the
   draft promised blanket "name not burned." Resolution: honest burn, scoped
   promise, boot-failure journal entry, bin/swarm reports (§2, §5).
2. **Hash-derived ports** (finding #2): per-process-randomized and collision-prone
   with no retry. Resolution: required harness change — real free-port acquisition
   (§2).
3. **Hardcoded swarm root** (finding #3): the "same file contract" held only by
   coincidence of one machine's paths. Resolution: required harness change —
   `--swarm-dir` threading (§2). Related nit #4: "exec" was ambiguous wording; the
   design now says subprocess-and-propagate, which is what makes failure-reporting
   possible at all.

**Attacks that failed, kept as evidence the dispatch is sound:** alias shadowing a
builtin cannot misroute (dispatch keys on the resolved token's shape — `glm = opus`
just routes claude); a hypothetical `/`-containing Claude token doesn't exist and
the check order handles it; case sensitivity matches today's exact-match behavior;
all three spot-checked citations were accurate (one relabeled for precision,
finding #13).

The remaining untested joint is argv passthrough of a multi-line task string from
bin/swarm to spawn-oc.py — plain subprocess argv, no shell, so no quoting layer;
it is the first thing the build slice verifies (§9).

---

## 8. Layer 3 — the door left open, on purpose

The operator's vision — "tell the operator session my management style and a cheap
model rewrites the harness system prompts to match," configuration as conversation —
is the top layer and is his to shape. This design's only obligation is to not block
it, and the way it complies is by being boring underneath:

- `.swarm/config` stays a plain flat-TOML text file. No binary state, no interactive
  wizard, no write-path tooling that would fight an agent editing it. A future
  Layer 3 agent reads and writes the same file a human does.
- Everything a Layer 3 agent would need to know is already discoverable through the
  same two surfaces a human uses: `swarm models` (what exists) and the config file
  (what is chosen). No hidden state to reverse-engineer.

Nothing in Layers 1–2 needs to change when Layer 3 arrives; it composes on top.

---

## 9. BUILD FIRST — one slice

**`swarm spawn --model <token>` dispatches: alias resolution from `[models]`,
`/`-token subprocess to the `[harness] opencode` script, exit-code propagation,
and the five refusal/failure messages of §5.** The harness script takes its three
required changes with it (`--reason`, `--swarm-dir`, free-port acquisition — §2).
That single slice deletes the two-tool problem — the user never types spawn-oc.py
again. Estimated diff: ~40 lines in bin/swarm, ~30 in spawn-oc.py.

`swarm models` is slice two, not slice one: discovery is worthless until the thing
it discovers is spawnable through the front door. Everything else in this document
(footer wording, install.sh line, SKILL.md doctrine update) rides behind those two.

First verification of the slice, per §4-judge-artifacts: spawn a real DeepSeek
child through `swarm spawn --model flash`, confirm it appears in `swarm ps` beside
a Claude child, confirm its journal tombstone and agent record carry the resolved
model and the parent's `--reason`, confirm a multi-line task survives the argv
handoff intact, and force one boot failure (bad port, or provider key removed) to
confirm the user sees §5's failure message and the tombstone records the failed
boot.

---

## Appendix — facts this design stands on

- bin/swarm: SPAWN_MODELS policy list (:53–66), MODEL_CAP/MODEL_STRUCTURAL
  rendering rules (:36–47), read_flat_toml (:448), registered_middleware (:479),
  configured_permission_mode (:514), mandate checks (:1384–1395), default→""
  collapse (:1397–1403), launcher construction (:1264–1303), record writes
  (:1426, :1494–1497).
- spawn-oc.py: CLI and slash requirement (:130–166), file-contract mirror
  (:6–16, :86–93, :204–253), fixed permission policy (:177–191), hardcoded R&D
  paths (:49–53), auto-fabricated reason (:166).
- Fact reports with full citations: .swarm/tmp/config-ux/spawn-side.md,
  .swarm/tmp/config-ux/oc-side.md (by cfg-read-spawn, cfg-read-oc, 2026-07-15).
- Adversarial review of the first draft: .swarm/tmp/config-ux/red.md (cfg-red,
  opus, 2026-07-15) — 0 kill / 3 fix / 3 nit / 6 failed attacks; all fixes
  incorporated (§7).
- Proven-overnight record: harness/MORNING.md (6/6 CONFIRMED via SEAT-VERIFY.md;
  costs measured; mixed-tree ps snapshot MIXED-TREE-PS.txt).
- Seat/leaf evidence state: docs/design/LOOP.md §4 (:215–248) — protocol-capable
  predicted yes, judgment-capable UNKNOWN pending Build 2; FLEET.md §4 (:217–222)
  launcher-override design this dispatch descends from.
- Philosophy constraints applied: PHILOSOPHY §5 (:147–177), §8 (:245–267),
  §9 (:270–303), §10 (:306–326).
