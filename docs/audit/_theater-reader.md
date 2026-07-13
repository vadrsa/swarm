# Who reads a falsifier?

**One-line answer: falsifiers in this repo are read by: PARENTS judging their children's work (confirmed, multiple instances), RED/ADVERSARIAL agents who take a target's stated falsifier and run it as their attack surface (confirmed, strongest pattern), and — in one decisive, non-circular instance — the OPERATOR, who read a red-team's falsifier-test and used it to overrule an in-progress child's design. Outside those three roles, and outside the commissioned meta-audit, consumption is rare: most of the ~151 journals that name a falsifier are never cited by anyone but their own author.**

Author: theater-reader, child of mr-theater. READ-ONLY on journals. All quotes below are verbatim with file:line. Every claim tagged VERIFIED (I read the primary source myself) / MEASURED (I counted it) / REASONED (I inferred it).

---

## 0. Scope and method (MEASURED)

- 165 journal files under `.swarm/journal/`.
- 151 of them contain the string "falsifier" (case-insensitive) — higher than the brief's ~103 estimate; 103 was `falsifier-probe`'s count of journals that *name a falsifier in the doctrine sense* (a specific reconciliation-entry construct), not raw string occurrence. The two numbers measure different things; both are real.
- I did NOT re-run `falsifier-probe`/`fp-compliance`'s form-and-compliance analysis (docs/audit/org-review-falsifier-2026-07-12.md, `_fp-slice-*.md`) — that work answers "is the falsifier well-formed and does the author ever return to it," which is a **different question** from mine ("does anyone OTHER than the author consume it"). I read their headline numbers as background, cite them once below, and do not duplicate their method.
- Search surfaces: `.swarm/journal/*.md` (grep for possessive citations: `"X's falsifier"`, `"the falsifier X named"`, etc.), `docs/audit/*.md` (including all `*-RED.md`/`*red*.md`), `.swarm/queue/**/*.json` (message bodies, both `delivered/` and pending), and source (`bin/swarm`, `install.sh`, any hook/script) for tooling that reads the field.

---

## 1. PARENT reads CHILD's falsifier — CONFIRMED, multiple instances, READ-AND-ACTED

### 1a. `opencode-plugin-scout` reads `oc-probe`'s falsifier report — corrects a propagated error

VERIFIED. `.swarm/journal/opencode-plugin-scout.md:1081-1100`:

> `## 2026-07-12 22:30Z — drained oc-probe's falsifiers report. Nothing new, but it shows exactly HOW the bad claim propagated. Idle.`
> `oc-probe's F1/F2/F3 report: all already absorbed (F1 the server SERIALIZES so no backpressure; F2 the TUI serves on a pinned port; F3 identity + external SSE).`
>
> `But it contains, as an F2 CAVEAT, the exact sentence that became my worst error:`
> `   "sessions ... are shared across server instances on the host, so per-agent`
> `    session isolation needs a per-agent DIR/worktree, not just a per-agent port."`
> `oc-probe got HALF of it right (sessions ARE shared) and then ASSERTED A FIX IT HAD NOT TESTED (that a per-agent dir isolates them). I TRUSTED IT and wrote it into §6.2 as a prescription. oc-red independently RAN it and found a TUI in its own --dir seeing 92 sessions from other dirs; I re-ran it (fresh EMPTY dir -> 93 sessions from every directory on the host) and then found the deeper fact myself (the store is a WORLD-READABLE SQLite file — no server, port, or password gates a read at all).`

Reader: `opencode-plugin-scout` (parent). Whose falsifier: `oc-probe`'s F2 caveat (child). **READ-AND-ACTED, twice over** — first the parent acted WRONGLY on the child's unverified remedy (wrote it into the design doc as a prescription), then a sibling red agent (`oc-red`) tested it, the parent re-ran it, found the deeper cause, and rewrote the doc. The parent's own lesson, same entry: *"a VERIFIED observation does not launder the REASONED fix bolted onto it."*

### 1b. `opencode-plugin-scout` promotes `oc-red`'s unrun falsifier to top priority

VERIFIED. `.swarm/journal/opencode-plugin-scout.md:1137-1140`:

> `Each half is verified; the join is not. That join is the shipping configuration, so it is now the #1 untested item in the doc — I promoted it ABOVE F4 in §8 and rewrote §3.7's scope-honesty note to name it. oc-red's falsifier stands, unrun, as the first experiment an implementer must do. It deserves that status: it is the cheapest test that could still embarrass this design.`

Reader: `opencode-plugin-scout` (parent). Whose falsifier: `oc-red` (sibling/red-team child). **READ-AND-ACTED** — the parent re-ordered its own design document's priority list (§8) specifically because of this falsifier's status.

### 1c. `field-tester` corrects a citation after `dp-red` disputes `dp-f1`'s falsifier — full chain

This is the clearest, most complete instance in the corpus: author writes a falsifier → red-team agent disputes the citation → judge (parent) checks the primary source → judge issues a written correction in the shipped artifact.

**Step 1 — `dp-f1` states its falsifier** (author). `.swarm/journal/dp-f1.md` (cited by `field-tester` as lines 220–246; the pre-registration language: *"dp-f1 pre-registered the falsifier for the fix (rename the root; if observers still pile children on your node..."*, quoted in the operator message at §3 below).

**Step 2 — `dp-red` (fresh adversarial reviewer, sibling) disputes the citation.** VERIFIED, `docs/audit/field-evidence-doctrine-2026-07-12-RED.md:422-444`:

> `## R9 — `cosmetic` (but a citation defect) — the "pre-registered falsifier" does not exist in dp-f1's artifact.`
>
> `**The evidence file, twice:**`
> `> **Mechanism (VERIFIED, *pre-registered falsifier survived*)** …`
> `> **dp-f1 *pre-registered the fix's falsifier*** (rename the root; if flat rows persist, the collision wasn't the cause) and can run that experiment on approval.`
>
> `**In `/tmp/dp-f1/findings.md`:**`
> `- `grep -ci "pre-regist"` → **0**`
> `- `grep -n "rename the root"` → **no match**`
>
> `Neither pre-registration is in the runner's file. ... **Falsifier:** point me at the pre-registration — dp-f1's journal, a `swarm send`, anything timestamped before the runs. If it exists outside `findings.md`, withdraw R9.`

Reader: `dp-red`. Whose falsifier: `dp-f1`'s (cited secondhand via `field-tester`'s evidence doc). This is category 4 (red agent testing a falsifier) AND sets up category 1 (parent acts).

**Step 3 — `field-tester` (parent of both dp-f1 and dp-red) checks the primary source and issues a written correction.** VERIFIED, `.swarm/journal/field-tester.md:124`:

> `dp-red flipped both my headlines and the corrected file is the record: ... R9 partially dissolved (dp-f1's journal DOES carry the pre-registration; I cited the wrong artifact). Operator has the corrected report including the honesty line: two independent reds caught the same author-bias direction in my drafts today...`

And the shipped artifact itself, VERIFIED, `docs/audit/field-evidence-doctrine-2026-07-12.md:71-73`:

> `- **[R9 — credit corrected.]** dp-f1's mechanism falsifier IS pre-registered — in its journal (`.swarm/journal/dp-f1.md` lines 220–246: stated after run 3, resolved by run 4's sincere-claim evidence), not in findings.md as this file previously implied. The reviewer's underlying point stands: cite the artifact that carries the credential.`

**READ-AND-ACTED, verified end to end**: `field-tester` went back to `dp-f1`'s actual journal (not just `dp-red`'s claim), confirmed the falsifier really was pre-registered there, and rewrote the public evidence document with an explicit correction note. This is the single strongest, most falsifiable-by-me example in the corpus — I re-read `dp-f1.md` lines 220-246 myself via the grep above (`RECONCILIATION — my run-3 mechanism falsifier RESOLVED, and it SURVIVED` at `dp-f1.md:246`) and the citation holds.

---

## 2. AUDITOR consuming falsifiers — commissioned meta-audit, counted separately (per brief's instruction)

`docs/audit/org-review-falsifier-2026-07-12.md` (by `falsifier-probe`) and `docs/audit/_fp-slice-{a,b,c}.md` / `_falsifier-rubric.md` / `_fp-compliance-shard-brief.md` (by `fp-compliance` and its children `fpc-s0..s3`) are a dedicated study of the falsifier corpus itself — commissioned specifically to answer "how well-formed / how often reconciled are falsifiers." They read hundreds of falsifiers by design. **This does NOT count as ordinary-course consumption** — it is circular (they exist because the falsifier field was made the audit target), exactly as flagged in my brief. Labeled `commissioned meta-audit`, counted separately:

- `falsifier-probe`: MEASURED and quoted at `.swarm/journal/falsifier-probe.md:88-90`: *"395 falsifier STATEMENTS ... 106 journals name a falsifier. **18 journals ever RETURN to a falsifier they named** ... **88 journals name a falsifier and NEVER once revisit it.**"* — This measures self-return (author reconciling their own falsifier), not third-party consumption. Not a hit for this audit's question, but useful context: even the AUTHOR rarely re-reads their own falsifier (18/106).
- One incidental finding worth surfacing from that meta-audit, MEASURED, `.swarm/journal/falsifier-probe.md:202-207`: *"93 of 103 journals have their LAST falsifier [as] the final act ... The falsifier is not ignored. It is ORPHANED BY THE RITUAL'S OWN SHAPE"* — i.e., the doctrine's own "always journal before going idle" duty structurally produces falsifiers with no further entry to revisit them IN THE SAME JOURNAL. This is about self-consumption, not third-party, but it explains part of why third-party consumption is rare: many falsifiers are the last thing an agent ever writes before its subtree is closed.

---

## 3. OPERATOR (the human) — one decisive non-circular hit; otherwise flatly NOBODY

**Search performed:** `.swarm/journal/operator.md` (the coordinator-facing root journal) for "falsifier"; all `.swarm/queue/*/delivered/*.json` and pending queue files where `"from": "operator"` (44 such files — the human's own outbound sends, confirmed via `WORLD.md:57-63`: *"The operator is a mailbox, not a node ... the human's side moves the mail to `delivered/` and journals the claim before acting on it"*); and all `.swarm/queue/operator/delivered/*.json` (messages agents sent TO the human — 30 files).

**Negative result, most of the surface:** Of the 30 messages delivered to the operator that contain the word "falsifier" (listed in full below), every one is an AUTHOR reporting on their OWN falsifier(s) to the operator (a status report). I found **no reply from the operator that quotes or acts on a specific agent-authored falsifier from one of those reports.** Files checked (MEASURED, grep-verified): `field-tester` ×7, `hardener` ×2, `red-simplest`, `red-operator`, `inbox-scout`, `structure-scout`, `decision-wiring`, `proxy-scout`, `pipeline-scout`, `skill-writer`, `decision-scout`, `onboarding-scout`, `onboarding-split`, `fleet-scout`, `opencode-plugin-scout`, `org-review-scout` ×2, `operator-structure-scout`. None of these produced an operator reply citing the falsifier back.

**Positive result — one decisive hit.** VERIFIED, `.swarm/queue/operator-structure-scout/delivered/1783872374653-operator.json`, full body (operator → operator-structure-scout):

> `CRITICAL CORRECTION mid-design — the adversarial review of the doctrine probe (docs/audit/field-evidence-doctrine-2026-07-12.md, post-review; dp-red) OVERTURNED the premise in your brief. Re-read that file's corrected findings before proceeding. ... dp-red found the REAL cause IN THE CODE: my_name() (bin/swarm:~52-53) returns SWARM_AGENT_ID-or-"operator" ... The sessions reasoned correctly from a false premise the TOOL handed them. My "sincere violation / prose gets rationalized" framing in your brief is WRONG — drop it. ... THE LOCK IS LIFTED (operator's decision just now): you MAY and SHOULD design the STRUCTURAL TOOL FIX together with the doctrine. ... dp-f1 has a RENAME EXPERIMENT pre-registered ... cite it as your fix's falsifier collector.`

And the companion message, VERIFIED, `.swarm/queue/operator-structure-scout/delivered/1783872957390-operator.json`:

> `Falsifier: the herdr root-session rig runs dp-f1's pre-registered rename experiment — after the fix, a fresh root session's children record parent=root-1 (or whatever the root names itself), NEVER parent=operator, and the flat-row shape is unrepresentable. ... Pre-register the fix's own falsifier (if children still record parent=operator after renaming, the my_name change wasn't the cause).`

**This is the operator directly reading `dp-red`'s adversarial review — which itself was built by testing `dp-f1`'s falsifier (§1c above) — and using it to overrule an in-progress child's design premise mid-flight**, then explicitly instructing that child to inherit `dp-f1`'s pre-registered falsifier as its own fix's test. **READ-AND-ACTED**, unambiguously: the operator names the reviewing agent, names the mechanism it found, retracts a framing ("drop it"), lifts a prior design constraint ("THE LOCK IS LIFTED"), and hands the falsifier forward as a required collector for new work. This is one hop removed from an agent's own stated falsifier (the operator is consuming `dp-red`'s falsifier-test of `dp-f1`'s falsifier, not `dp-f1`'s falsifier directly) but it is non-circular, real, and decisive.

**Adjacent but NOT counted as a hit:** `.swarm/queue/field-tester/delivered/1783865646761-operator.json` — the operator orders SPAN's doctrine falsifiers "actually run" because they were "designed but unrun." This is the operator tracking that falsifiers EXIST and demanding execution, not reading a falsifier's STATED RESULT and acting on the content. Noted for completeness, not scored as consumption.

**Flat statement on the rest:** outside the one hit above, grep across all 30 operator-delivered falsifier-mentioning messages and all 44 operator-authored outbound messages finds **zero instances of the human quoting, citing, or visibly acting on the substance of a specific agent's self-reported falsifier in a status report.** The operator's engagement with falsifiers is real but occurs exactly once in the corpus, and it arrives via a red-team review, not via reading an author's own report.

---

## 4. RED/ADVERSARIAL agent using a falsifier as attack surface — CONFIRMED, the strongest and most common pattern

This is the highest-value consumption pattern named in the brief, and it is the one with the most instances.

### 4a. `dp-red` tests `dp-f1`'s falsifier citation (see §1c for full chain) — CONFIRMED, READ-AND-ACTED

### 4b. `inline-work-audit-RED` (`iwa-red`) runs the target report's OWN stated falsifier and refutes its headline claim

VERIFIED, `docs/audit/inline-work-audit-RED.md:20-29`:

> `The report's item I14:`
> `> | I14 | 2026-07-12/13, **UNJOURNALED** | **Edited `bin/swarm` + `tests/test_swarm.py` inline** — added `<model>` to `swarm ps` (working tree, uncommitted; `git diff` VERIFIED) | No journal entry exists. ... |`
> `— `inline-work-audit-2026-07-12.md` §1`
>
> `Every clause of that row is false.`
>
> `**The working tree does not contain it.** `git status --short` returns exactly three modified files: `WORLD.md`, `install.sh`, `skill/SKILL.md`. I ran the report's own falsifier: `git diff --quiet HEAD -- bin/swarm tests/test_swarm.py` exits **0 — identical to HEAD**.`

Reader: `iwa-red` (fresh adversarial spawn). Whose falsifier: the target report's own (`inline-work-audit`'s v1, author unnamed in this excerpt but same-agent-lineage). **READ-AND-ACTED, confirmed downstream**: VERIFIED, `docs/audit/inline-work-audit-2026-07-12.md:1-5` (the shipped v2):

> `# Inline operator work — a doctrine-failure audit (v2, post-red-team)`
> `Auditor: `inline-work-audit`. Adversarial reviewer: `iwa-red` (fresh spawn) — `docs/audit/inline-work-audit-RED.md`. **This is v2. The v1 census was materially wrong in two ways and iwa-red killed both. Both kills are ACCEPTED and folded in;`

This is a textbook case of category 4: the red agent didn't just critique the finding — it re-ran the ORIGINAL AUTHOR'S OWN NAMED FALSIFIER (`git diff --quiet HEAD -- bin/swarm tests/test_swarm.py`) and used the result to kill the headline claim outright.

### 4c. `dp-f2`'s journal references `dp-f1`'s falsifier as a point of contrast (weaker — self-comparison, not attack)

VERIFIED, `.swarm/journal/dp-f2.md:200-201`:

> `VERDICT: falsifier 2 NOT-FIRED, n=2. And unlike dp-f1's falsifier-1 pass, this one is EARNED...`

Reader: `dp-f2` (sibling, not a red agent — same field-tester subtree, running a DIFFERENT falsifier). This is READ-AND-NOTED at most: `dp-f2` cites `dp-f1`'s result for rhetorical contrast in its own verdict, but there's no evidence `dp-f2` changed anything because of it. Listed for completeness; not scored as a strong hit.

---

## 5. MESSAGES (not journals) — direct sends about a falsifier

Beyond the operator messages in §3, I searched all `.swarm/queue/**/*.json` for agent-to-agent sends (not to/from operator) containing "falsifier". MEASURED: most hits are the SAME messages already covered above (task briefs where a parent instructs a child to test a NEW falsifier — that is a parent AUTHORING a falsifier for a child to test, which is upstream design, not consumption of a PRIOR falsifier). I found no additional agent-to-agent send, beyond the `operator-structure-scout` pair in §3 and the `dp-red`/`field-tester` chain in §1c, where the message is centrally about the CONTENT of a falsifier someone else already wrote and reported.

---

## 6. TOOL / HOOK / CI check — CONFIRMED ZERO, doctrine-only

MEASURED, exhaustive grep of source (excluding `.swarm/journal/`, `.swarm/queue/`, `docs/audit/`):

```
grep -rn -i "falsifier" --include="*.sh" --include="*.js" --include="*.ts" --include="*.py" .
  -> zero hits outside docs/audit and .swarm/journal
grep -n -i "falsifier" install.sh
  -> zero hits
grep -n -i "falsifier" bin/swarm
  -> ONE hit, line 784
```

The one hit, `bin/swarm:784`:

> `f"its falsifier (the observation that would show you are off track). "`

This is a string literal inside the tool's spawn-header prompt text — it is the DOCTRINE INSTRUCTION the tool injects into every agent's briefing (the source of the "a reconciliation entry names its falsifier" mandate). **It is not a reader.** The tool writes the instruction to write falsifiers; it never reads, parses, validates, greps for, or checks the field afterward. No hook directory, no CI config, no linter, no test in the repo touches journal content for falsifier presence or validity.

**Confirmed: the field is doctrine-only from the tool's perspective.** Every case of consumption found in this report happened because an AGENT chose to read another agent's journal or artifact — never because a script did.

---

## Summary table

| Consumer | Whose falsifier | Action taken | Evidence | Verdict |
|---|---|---|---|---|
| `opencode-plugin-scout` (parent) | `oc-probe` (child) | Wrote wrong claim into design doc, then corrected after sibling `oc-red` tested it | `.swarm/journal/opencode-plugin-scout.md:1081-1100` | READ-AND-ACTED |
| `opencode-plugin-scout` (parent) | `oc-red` (child) | Reordered design doc §8 priority list | `.swarm/journal/opencode-plugin-scout.md:1137-1140` | READ-AND-ACTED |
| `dp-red` (red sibling) | `dp-f1` (sibling, via field-tester's doc) | Disputed citation, forced correction | `docs/audit/field-evidence-doctrine-2026-07-12-RED.md:422-444` | READ (attack), triggered §1c |
| `field-tester` (parent) | `dp-f1` (child), mediated by `dp-red`'s review | Rewrote shipped evidence doc with correction note | `.swarm/journal/field-tester.md:124`; `docs/audit/field-evidence-doctrine-2026-07-12.md:71-73` | READ-AND-ACTED |
| operator (human) | `dp-red`'s test of `dp-f1`'s falsifier | Overruled child's in-progress design, retracted a framing, lifted a constraint, ordered falsifier inherited | `.swarm/queue/operator-structure-scout/delivered/1783872374653-operator.json`, `...1783872957390-operator.json` | READ-AND-ACTED (one hop removed, non-circular) |
| `iwa-red` (red spawn) | `inline-work-audit` v1 (its own commissioning author's report) | Ran the report's own falsifier command, refuted headline claim I14 | `docs/audit/inline-work-audit-RED.md:20-29` | READ-AND-ACTED, confirmed in v2 |
| `dp-f2` (sibling) | `dp-f1` (sibling) | Rhetorical contrast only, no decision changed | `.swarm/journal/dp-f2.md:200-201` | READ-AND-NOTED |
| `grave-kills` (child, reading design doc not agent journal) | STRUCTURE.md's written falsifier (not agent-authored) | Flagged as procedural bar to carry to parent | `.swarm/journal/grave-kills.md:120-132` | adjacent, doctrine-not-agent falsifier |
| any tool/hook/CI | — | none | `bin/swarm:784` is the only source hit, and it WRITES the instruction, never reads the field | CONFIRMED doctrine-only |

## Bottom line

The mandate is **not pure theater**, but it is **not broadly load-bearing** either. Consumption is concentrated almost entirely in ONE STRUCTURAL PATTERN: **fresh adversarial review**. Every strong hit in this report (§1a/b via `oc-red`, §1c/§4a via `dp-red`, §4b via `iwa-red`) traces back to a repo convention of spawning a "fresh, uncontaminated" reviewer whose entire job is to attack a prior artifact — and a stated falsifier is the single most efficient thing to attack, because it's pre-formatted as a runnable test. Where that convention fired, falsifiers were read, tested, and sometimes flipped outcomes. Where it didn't fire — the ordinary case, 88+ of the ~106-151 falsifier-bearing journals — the falsifier appears to sit unread, often as literally the last sentence the agent ever wrote (per `falsifier-probe`'s independent measurement, §2 above).

The operator read exactly one falsifier-derived finding in this entire corpus and acted on it decisively — but it reached the operator BECAUSE a red-team agent had already turned it into a test, not because the operator reads raw journal falsifiers directly.

**If the analogous proposal my parent is weighing depends on unprompted, ordinary-course reading of a compelled free-text field, this repo's own evidence says: don't count on it. If it depends on that field being fed to a designated adversarial reader whose job is to test it, this repo's evidence says: that part works, repeatedly and traceably.**
