# `_hcr-evidence` — evidence audit of `docs/design/HARNESS.md`

**Auditor:** `hcr-ev`, evidence auditor under `hc-red`. **Date:** 2026-07-13.
**Target:** `docs/design/HARNESS.md` @ `swarm-dev/spawn-slash-shim` (cfb3113), 693 lines.
**Method:** every evidence tag (VERIFIED / MEASURED / DOCUMENTED) spot-checked against its
actual named source. Both sides quoted. No charity: an off line number is a finding, a
number absent from the cited source is a finding, a cite pointing at a self-reported doc
where the tag promises primary evidence is a finding.

**Delegation:** four clusters, split by source file. `hcrev-eval` (FLEET-EVAL/-V3 numbers),
`hcrev-fit` (MODEL-FIT + field + mechanics), `hcrev-slm` (Haiku + industry + SLM). I kept the
`bin/swarm` / `WORLD.md` / `FLEET.md` cluster. **Every WRONG verdict below I re-checked
against the same lines myself** before publishing; I overturned one of my children's
verdicts in the process (see the correction note on E-4). Child artifacts:
`_hcrev-eval.md`, `_hcrev-fit.md`, `_hcrev-slm.md`.

---

## VERDICT COUNTS

| Verdict | Count |
|---|---|
| **REACHES** — the source says what the doc says it says | 21 |
| **OVERSTATED** — true core, but the cite/caveat/scope does not survive contact | 15 |
| **WRONG** — the cited source does not contain the claim | 7 |
| **UNVERIFIABLE** — no locatable source | 2 |

**Headline:** HARNESS.md's evidence discipline is *real but unevenly applied*. Where it cites
`MODEL-FIT.md` it is excellent (9 of 9 section cites land). Where it cites **its own harvested
child artifacts** it degrades sharply — fabricated subsection numbers, a collector's summary
prose attributed to a primary journal, caveats dropped in transit. **And the single
most load-bearing MEASURED claim in the document — the Haiku survivability gate — is
contradicted by its own source document and by HARNESS's own §8.**

---

## THE THREE FINDINGS THAT CHANGE THE DESIGN

### F-1. The survivability gate rests on a claim its own source explicitly forbids. (§2.4, §4.1, §7.3)

This is the most serious finding in the audit. §2.4 makes Haiku the "type specimen" of a new
axis and builds a **hard spawn-time refusal** on it. Tagged **MEASURED**.

> **HARNESS §2.4:** "Haiku ... cannot run in auto permission mode, so its first dialog wedges
> it forever, invisibly (MEASURED — both Haiku arms of
> `docs/audit/weak-model-delegation-2026-07-13.md` blocked on a permission dialog before the
> synthesis step)"

What the cited source **actually says**, in its own author's voice:

> **`weak-model-delegation-2026-07-13.md:75`:** "**ROOT CAUSE (a swarm bug, bigger than this
> probe): `swarm spawn` writes `.swarm/settings/<name>.json` with HOOKS ONLY and NO
> `permissions` block** ... So **every spawned child** is exposed to interactive dialogs on
> ordinary work."
>
> **:87:** "**The stall was caused by a permission gate swarm hands EVERY child regardless of
> model. Opus would block too**, on a first-touch path it hadn't been granted — the difference
> between the arms was *filesystem starting state*, not model strength. **A tier rule about
> cheap models does not fix an infrastructure gate that fires on all models.**"
>
> **:89:** "**The falsifier that would settle it, and it is cheap:** spawn an **Opus**-pinned
> child into the same first-touch permission wall. ... **This is the top re-run item.**"
>
> **:91 (section header):** "**WHAT MUST HAPPEN BEFORE ANYONE LOCKS A TIER RULE ON THIS**"

The source document is a **rebuttal of the exact inference HARNESS draws from it**, and it
titles a section forbidding that inference. The falsifier it names was never run.

Independently confirmed by me: `grep -n 'permissions' bin/swarm` → **zero hits**. Spawn
(`bin/swarm:1156-1160`) writes hooks only. The gate fires on *every* model.

**HARNESS contradicts itself on this inside one document.** §8 concedes the real cause:

> **HARNESS §8:** "the missing `permissions` block in spawned settings is a named defect that
> belongs to the spawn path's owner — MODEL-FIT §7 flagged it first; **the Haiku ban is its
> bill arriving**."

If the ban is the *bill of an infrastructure defect* (§8), it cannot also be the *type specimen
of a model-capability axis* (§2.4). **Both cannot be true.** What was measured: two Haiku agents
hit a permission dialog that swarm hands to every child. What was *not* measured, and is stated
as fact: that Haiku specifically "cannot run in auto permission mode."

**Verdict: OVERSTATED, and load-bearing.** The observational core (two arms, genuine
`Do you want to proceed?` Bash-tool dialogs — verified from raw pane captures, not trust
prompts, before any synthesis work) **REACHES**. The causal claim, the axis, and the spawn-time
refusal built on it do not. §2.4 and §4.1 need to be rewritten around the defect, or the
falsifier at `wmd:89` needs to be run first.

### F-2. `.swarm/config` — the file that "already carries `[middleware]`" does not exist. (§4.2)

> **HARNESS §4.2:** "`.swarm/config` (the file that already carries `[middleware]` —
> `WORLD.md:66`) gains: `[models]` / `priority = ...`"

Two defects, one fatal:

- **`cat .swarm/config` → No such file.** The file does not exist in this repo. The *code*
  supports the section (`registered_middleware`, `bin/swarm:347-371`) and `WORLD.md` *describes*
  it — but "the file that **already carries**" is present-tense false.
- The `[middleware]` bullet begins at **`WORLD.md:64`** ("**A configured send middleware sits on
  the send path.** When `.swarm/config` carries a `[middleware]` section..."). Line **66** is
  mid-sentence: "sender's process, before the message is queued, with the full envelope —".

**Verdict: WRONG.** §4.2's whole argument is "no new mechanism, just one more stanza in a file
that's already there." There is no file. The design must either create it or drop the framing.

### F-3. "The regex ... cannot be sweet-talked" — the input is attacker-controlled and forgeable. (§7.2(b))

§7.2(b) cuts the SLM classifier by contrasting it against the regex on *security*:

> **HARNESS §7.2(b):** "the regex **ships, is pure, is testable, and cannot be sweet-talked** —
> an agent can print anything into its own pane, and prompt-injecting a model into emitting the
> wrong enum member is a real attack on a surface **the regex is immune to**."

`BLOCKED_SIGNATURES` (`bin/swarm:57-61`) is **plain substring matching**, and its input is
`pane_text()` (`:750-761`) = `herdr pane read --source visible --lines 40` — **the raw last 40
lines of the agent's own terminal.** The code's own docstring says so:

> **`bin/swarm:545-547` (`render_ps`):** "'blocked' carries the SAME hazard, sharper: **its
> source is live pane text, which an agent fully controls** (it is that agent's own terminal)."

The code claims only that the **output** is safe (a closed enum cannot forge a tree row). It
never claims the **input** cannot be forged — and it cannot be. I ran it:

```
BLOCKED_SIGNATURES = (('trust', 'trust the files in this folder'),
                      ('permission', 'Do you want to proceed?'),
                      ('rate-limit', 'resets'))

'permission'   <- agent echoes "Do you want to proceed?" into its own pane
'trust'        <- agent echoes "trust the files in this folder"
'rate-limit'   <- agent echoes "You've hit your session limit - resets 4:30am"
'rate-limit'   <- INNOCENT prose: "I hit the limit of what grep resets can do here"
'permission'   <- an agent merely QUOTING THIS AUDIT DOC into its pane
```

Any agent can forge any blocked state with one `echo`. Innocent prose false-positives.
**An agent that quotes this very audit into its pane renders as `[blocked: permission]`.**

HARNESS conflates two different attacks. The regex is immune to **prompt-injection of the
classifier**; it is *not* immune to **forgery of the signal** — and both read the same untrusted
string. The doc's own stakes make this matter: §7.2(b) says "a wrong `blocked: rate-limit` label
**triggers a parent's remodel of a healthy agent**," and §2.3 makes `[blocked: kind]` the surface
"every avenue-3 trigger below assumes." A forgeable signal drives a real state change.

**Verdict: WRONG.** "Cannot be sweet-talked" is false as written. The honest claim is: *the
regex is deterministic and its output is a closed enum, so a forged input can produce a wrong
label but never a forged tree row.* That is a much weaker property than the one §7.2(b) uses to
win the argument — and it is the same property the SLM behind a closed-enum contract would have.
**The regex-vs-SLM comparison is false on the axis §7.2(b) chose to argue.**

---

## FULL TABLE — one row per checked tag

### A. `bin/swarm` / `WORLD.md` / `FLEET.md` (checked by me, `hcr-ev`)

| # | CLAIM (quoted from HARNESS.md) | SOURCE CHECKED (file:line, quoted) | VERDICT | NOTE |
|---|---|---|---|---|
| A-1 | §1: "the only place swarm is welded to Claude is the launcher body (VERIFIED — **`bin/swarm:1061-1062` is the single `claude` invocation**)" | `bin/swarm:1061-1062`: `(f'claude --settings {shlex.quote(settings)} --model {shlex.quote(model)} "$PROMPT"'` / `if model else f'claude --settings {shlex.quote(settings)} "$PROMPT"'),`. Full-file grep for `claude`: only other hits are the PATH check (`:1050-1052`), the exit-code check (`:1064`), comments, and `~/.claude.json` (Claude Code's own config, `:1018-1022`, `:1084`) — **no second invocation**. | **REACHES** | Correct on both counts: it *is* the only invocation, and the lines are right on this branch. The cite covers a single Python ternary emitting one of two bodies — accurate as written. |
| A-2 | §1/§2.1: "**every hook is fail-safe `try/except → exit 0`** and simply never fires for a non-Claude process, FLEET §2" | The four wired hooks (`bin/swarm:1156-1160`): `UserPromptSubmit→deliver`, `Stop→event stop`, `Notification→event notification`, `SessionStart→restore`. `cmd_deliver` (:864-875), `cmd_event` (:878-913), `cmd_restore` (:916-935) all end `sys.exit(0)`. **But** `cmd_event` opens with `die(f"event: unknown kind '{kind}'...")` (:882) — and `die` is `sys.exit(1)` (:81-83) — **outside any try**. `my_name()`/`root_dir()`/`read_stdin_json()` also run *before* the try in all three. | **OVERSTATED** | True of the three wired paths in practice (the hooks only ever pass `stop`/`notification`), so no live bug. But the claim is stated absolutely ("every hook") and there is a non-zero exit path in the code. Narrow. |
| A-3 | §1/§2.1: the fail-safe claim is sourced to "**FLEET §2**" | `FLEET.md:65-73`: "spawn writes `settings/<name>.json` with four hooks ... (**`bin/swarm:890-894`**). Every one of those hook handlers is `try/except → sys.exit(0)` ... (`cmd_deliver` **`:685`**, `cmd_event` **`:699`**, `cmd_restore` **`:737`**). ... **The launcher (`:823-835`...)**" | **OVERSTATED (inherited rot)** | **Every line number in FLEET §2 is stale.** Hooks are at 1156-1160 (not 890-894); `cmd_deliver` 864 (not 685); `cmd_event` 878 (not 699); `cmd_restore` 916 (not 737); launcher 1041-1066 (not 823-835). HARNESS inherits a claim whose citations have all rotted. HARNESS *did* independently re-verify the launcher line (A-1), but it passes FLEET §2's hook cite through unchecked. |
| A-4 | §2.1: "the **4000-char** tail re-injection on SessionStart (VERIFIED — `build_restore`, **`bin/swarm:462-472`**; tail cap per `_hc-mech.md` §3)" | `bin/swarm:462-472` = `build_restore` — correct range, but **contains no cap**: it calls `journal_tail(jpath)`. The cap lives at `:34` (`JOURNAL_TAIL_CAP = 4000`) and is applied by `journal_tail` at `:449-459`. | **OVERSTATED** | Lines are right for `build_restore`; the **number is not in the cited range**. The doc feels the gap and patches it by sourcing the number to a *child's doc* ("tail cap per `_hc-mech.md` §3") rather than to `bin/swarm:34`, the primary line it is one grep away from. The number is true; the citation does not reach it. |
| A-5 | §2.3: "`classify_blocked` (**`bin/swarm:694-715`**, VERIFIED): pane text ... classified into a **closed enum** (`trust \| permission \| rate-limit \| None`)" | `bin/swarm:694-715` = `classify_blocked` exactly. `:695`: "Pure. pane_text -> one of `'trust' \| 'permission' \| 'rate-limit' \| None`." `BLOCKED_SIGNATURES` at `:57-61` has exactly those three kinds. | **REACHES** | Line range exact, enum exact. Clean. |
| A-6 | §7.2(b): "the regex ships, is pure, is testable, and **cannot be sweet-talked** ... a surface **the regex is immune to**" | See **F-3** above. `BLOCKED_SIGNATURES` (:57-61) is substring matching on `pane_text()` (:750-761) = raw pane capture. `bin/swarm:545-547`: "its source is live pane text, **which an agent fully controls**." Forgery demonstrated executably (5/5 forgeries land, incl. innocent-prose false positive). | **WRONG** | The headline finding of this cluster. The regex is immune to *classifier* injection, not to *signal forgery*. The code claims output-safety only; HARNESS upgrades it to general un-sweet-talkability and wins the SLM argument with it. See F-3. |
| A-7 | §4.2: "`.swarm/config` (**the file that already carries `[middleware]`** — **`WORLD.md:66`**)" | `cat .swarm/config` → **no such file**. `WORLD.md:64`: "**A configured send middleware sits on the send path.** When `.swarm/config` carries a `[middleware]` section..." — `:66` is mid-sentence ("sender's process, before the message is queued"). | **WRONG** | See **F-2**. Both the file's existence and the line number are wrong. Code support is real (`registered_middleware`, :347-371); the *file* is not. |
| A-8 | §2.2: "*'a leaf never spawns'* (**FLEET.md:88**)" | `FLEET.md:88`: "\| spawn / `herdr tab create` from inside the sandbox \| **No — and this is the point** \| **A leaf never spawns.** ..." | **REACHES** | Exact line, exact quote. Clean. |
| A-9 | §3: "the same reader renders all three (`ps` model pins, **already shipped — VERIFIED in live `ps` output**)" | Live `swarm ps` this session: `├─ hcr-ev (you) model=opus [live] q=0`, `├─ model-fit model=sonnet [live]`. Pins render. **Note:** they render *only for pinned agents* — my own three children show no `model=` slot, which `bin/swarm:534-538` documents as intended ("An empty one means the agent was NOT pinned... so ps says nothing"). | **REACHES** | Shipped and verified in live output, as claimed. The absent-pin case is by design, not a defect in the claim. |
| A-10 | §7.2(c): "The mailbox's real pressure (**30 waiting messages this morning**, VERIFIED in `ps`)" | Live `swarm ps`: "operator — **31 message(s)** waiting for the human (queue/operator/)"; `ls .swarm/queue/operator/ \| wc -l` → **32**. | **REACHES** | ~30 at time of writing, 31-32 now and still growing. The claim is accurate and, if anything, understated. |

### B. FLEET-EVAL / FLEET-EVAL-V3 numbers (`hcrev-eval`; every WRONG re-checked by me)

| # | CLAIM (quoted from HARNESS.md) | SOURCE CHECKED (file:line, quoted) | VERDICT | NOTE |
|---|---|---|---|---|
| E-1 | §3: "the claude-native anchor swept its battery (**10/10 D2, 17/17 D3, 6/6 D4**)" | `FLEET-EVAL-V3.md:25`: "\| **claude-native** (anchor) \| 5/5 PASS \| **10/10 PASS** (cheap 4/4 · heavy 6/6) \| **17/17 PASS** \| **6/6 PASS** \| clean sweep — 37/37 [M] + 1 check won on plumbing (D3b.2); **same-harness caveat REMAINS** \|" | **REACHES** (caveat dropped) | Every number exact. But the same source line ends "**same-harness caveat REMAINS**" — the anchor is Claude judging Claude on Claude's own harness. HARNESS quotes the sweep and drops the caveat the source attached to it in the same cell. |
| E-2 | §3: "deepseek and GLM **both passed duties 5/5 and heavy delegation 6/6**" | `V3:23`: "\| **deepseek-chat** \| **5/5 PASS** \| 8/10 FAIL (cheap 2/4 FAIL · **heavy 6/6 PASS**)* ..." `V3:24`: "\| **GLM-4.7** \| **5/5 PASS** \| 7/10 FAIL (cheap 1/4 FAIL · **heavy 6/6 PASS**) ..." | **REACHES** | Exact on both. The "parent-capable hypothesis is real" reading is fair — the source's own v3 column says "parent-capable, leaf-duty-weak." |
| E-3 | §5: "D2-heavy 6/6 both (**V3:23-24**)"; §5: "the anchor's clean sweep (**V3:25**)" | `V3:23-24` = the deepseek and GLM rows; `V3:25` = the claude-native anchor row. | **REACHES** | Both line cites land exactly. |
| E-4 | §3: "deepseek's **11-minute harness detour, V3:84-86**" | `V3:82-83`: "deepseek **abandoned the brief and spent 11 min debugging the harness** (read spawn internals, simulated arg-insertion, spawned a test tab)". Cited range `V3:84-86` = "without returning to its remaining steps. It was killed by the runner ... deepseek does not time-box a blocked dependency". | **OVERSTATED** | ⚠ **I overturned my child's verdict here.** `hcrev-eval` first reported the "11 min" figure appears *nowhere* — false; it is verbatim at V3:82. The real defect is narrower: the cited range **starts 2 lines after the sentence it cites**, and "harness detour" is HARNESS's paraphrase, not a quote. (`_hc-eval-table.md:30` propagates the identical off-by-2.) Child corrected its artifact and logged the correction. |
| E-5 | §5: "*'excellent tool-user… well-formed all battery long'* (**V3:96-98**)" | `V3:101-102`: "- **Tool-user: excellent.** Every swarm command all battery long was well-formed (D3b 4/5 in ~2 min...)". Cited `V3:96-98`: "timing samples), closed all 4, reported up. D2-heavy 6/6 — the strongest non-Claude delegation execution in either run. / - **The half that SURVIVES v2:** no watchdog." | **WRONG** | The quoted text is at **101-102**, not 96-98. The cited range is about D2-heavy and the watchdog — different content. The "quote" is also reworded, not verbatim, while dressed in quote marks. |
| E-6 | §5: "*'dead children would hang it again'* (**V3:98-100**)"; §3: "GLM's **watchdog-less sleep loop, V3:98-100**" | `V3:98-100`: "- **The half that SURVIVES v2:** no watchdog. Its harvest loop is blind sleep-escalation (`sleep 5/15/30` + `swarm ps`); it terminated only because its children delivered. **Dead children would hang it again.** Unattended-parent risk." | **REACHES** | Both cites land exactly, and the quote is verbatim. The doc's cleanest citation. |
| E-7 | §3: "deepseek narrates reports instead of sending, **4/7 drops**; V3:76-80" **vs** §5: "against **3/7 report delivery** ... (V3:76-80, D4 rows)" | `V3:49`: "It immediately produced signal: **deepseek dropped 4/7, GLM dropped-or-misrouted 4/7, Claude 7/7.**" `V3:76`: "- **Leaf duties are the weakness the clean rig exposed:** **4/7 report-to-parent**". Grep for `3/7` across both eval docs: **zero hits.** | **WRONG** | HARNESS contradicts itself: §3 says 4/7, §5 says 3/7, for the same measurement citing the same lines. **The source says 4/7.** §5's "3/7" appears in *neither* eval document. One of the doc's two internal statements of its own headline eval number is unsourced. |
| E-8 | §3: "neither journals for continuity (**V3 D4 hard-fails**)" | `V3:23-24`: both Chinese cells score "3/6 FAIL†" on D4. **The dagger, `V3:33-35`:** "† D4 for both Chinese cells is **confounded in MAGNITUDE by the MCP escape hatch** (§4.2) — read as **'at most this bad'** — but the Claude control (§4.2) shows the confound is not the whole story." | **OVERSTATED** | D4 does fail for both, so "hard-fails" has a basis. But the source **footnotes its own number as confounded** and says to read it as an upper bound. HARNESS uses the D4 failure to justify "may not be trusted with restore-dependent continuity" — a strong structural ruling — while dropping the confound the source attached. |
| E-9 | §1: "`docs/audit/_hc-eval-table.md` (**83 rows**, every FLEET-EVAL score with file:line)" | `_hc-eval-table.md`: 91 lines total; 89 begin with `\|`; minus header and separator = **87 data rows**. | **WRONG** | 87, not 83. Minor in consequence, but it is a VERIFIED-adjacent count in the doc's own evidence manifest — the one place a reader checks to calibrate how carefully the author counts. |

### C. MODEL-FIT / field / mechanics (`hcrev-fit`; every WRONG re-checked by me)

| # | CLAIM (quoted from HARNESS.md) | SOURCE CHECKED (file:line, quoted) | VERDICT | NOTE |
|---|---|---|---|---|
| M-1 | §1/§5: "the last mechanism that chose for parents produced **142/143 spawns nobody decided** (MEASURED — MODEL-FIT's headline)" | `MODEL-FIT.md` §1: "**142 of 143 agents took the inherited default; exactly one was ever pinned.** ... It is a decision nobody made, 143 times." | **REACHES** | Number exact, characterization fair. Lives in MODEL-FIT §1 (HARNESS doesn't pin a section here, so no mis-cite). |
| M-2 | §7.2(a): "**0/135 mush, 17 recorded behavior changes**, MEASURED" (cited to MODEL-FIT §5) | MODEL-FIT §5: "unfalsifiable mush — the predicted theater \| **0 of 135**"; "**17 documented cases** where the compelled field *changed what the agent did*" | **REACHES** | Both numbers exact, both in §5 as cited. **Note the chain:** MODEL-FIT is itself reporting a grandchild's count (`org-review-falsifier-2026-07-12.md`), so MEASURED here means "a child measured it," not "the author measured it." HARNESS's tag matches MODEL-FIT's own, so this is inherited, not introduced. |
| M-3 | §6: "MODEL-FIT measured **16% of leaves growing into seats** unbriefed" | MODEL-FIT §4: "**18 of 115 agents — 16% — carry a coordinator role they were never briefed for.**" | **REACHES** | Number exact. Real section is §4 (HARNESS prints no section number here, so nothing to be wrong about). |
| M-4 | §8: "at least **~9 test call-sites and 12 doc files** — a floor, not a total (MEASURED, MODEL-FIT §5)" | MODEL-FIT §5: "blast radius measured by patching a scratch copy of `bin/swarm` and running the suite: **at least ~9 test call-sites and 12 doc files** — *a floor, not a total, per the omission caveat in §4*" | **REACHES** | Numbers exact, section exact, and HARNESS correctly carries the floor-not-total caveat forward. Model citation. |
| M-5 | §3/§7: "MODEL-FIT §5: scoping the reason to anything else *'launders a guess into a decision'*" | MODEL-FIT §5: "*A mandated reason forces a parent to justify a choice the repo cannot yet inform — and a recorded reason **launders a guess into a decision**.*" | **REACHES** | Verbatim, correct section. Minor: in MODEL-FIT this is voiced as the *reviewer's* objection ("the one objection the review could not defeat"), which HARNESS flattens into MODEL-FIT's own voice. |
| M-6 | §2.2/§4.3: "**MODEL-FIT §5b's** correction" (the bare launcher runs an ambient default nobody chose) | MODEL-FIT §5b exists: "## 5b. The default: do not change the fallback — and stop calling it 'inherit'" ... "There is **no inheritance.** ... the child gets whatever the `claude` binary resolves as its **ambient default**, which is nobody's decision" | **REACHES** | §5b exists and says precisely what HARNESS attributes to it, on both mentions. |
| M-7 | §5/§7e/§8/§9: "the fit rule verbatim (**MODEL-FIT §6**)"; "floor-not-total discipline (**MODEL-FIT §4**)"; "**MODEL-FIT §7** flagged it first" | MODEL-FIT §6 contains the fit-rule blockquote ("Put the strong model where being wrong is expensive and invisible..."). §4 contains "publish it as a floor, not a total". §7 names the missing `permissions` block and hands it off. | **REACHES** | All three section cites land. **9 of 9 MODEL-FIT section cites in the document are correct** — the doc's strongest citation surface by far. (Pedantic: §4 also names the permissions defect earlier, so §7 is not literally "first.") |
| M-8 | §2.3: "trigger-scout's session-limit death rendered in `ps` as an ordinary `[live] q=0 idle` agent (VERIFIED — `_hc-field.md` §A1, **three independent witnesses**)" | `_hc-field.md` §A1 cites three records: the event file `.swarm/event/trigger-scout.json`; `trigger-scout.md:1530-1531`; `.swarm/journal/blocked-visibility.md:47-48`. | **OVERSTATED** | Three *observers*, one *instrument*. All three read the same `last_words` string as surfaced by `ps` — three readers of one signal, not three independent derivations. "Three independent witnesses" oversells the independence. The underlying fact (a limit-death renders as idle) is not in dispute. |
| M-9 | §2.3: "The operator's own journal names **three structural bugs** ... (VERIFIED — **`.swarm/journal/operator.md:199`**)" | `operator.md:199` = the entry **header**: "## 2026-07-12 — [ops-main] BUG FOUND: usage-limit freeze leaves agents unrecoverable by doorbell". The three-bug list is on **:200**: "THREE REAL BUGS: (1) Stop-hook-skipped-on-limit -> no event fact -> no re-ring; (2) ps can't distinguish frozen-on-limit from busy-first-turn; (3) doorbell Enter unreliable (needed a second Return)." | **OVERSTATED** | The three bugs are genuinely there and HARNESS paraphrases them accurately — but they are on **line 200**, not 199. One line off, in a document whose whole rhetorical claim is file:line citation discipline. |
| M-10 | §6: "**~10 agents** carry same-day resume entries from this morning's machine restart (MEASURED — `_hc-field.md` §B1)" | `_hc-field.md` §B1: "That is 9 distinct other agents plus this one (**10 total**) with an explicit dated resume entry today — **short of the operator's reported '~13,'** ... several of the 13 named orphan-survivors ... **were not directly checked** for a same-day resume entry in this pass (**see Falsifier below**)." | **OVERSTATED** | The count is accurate to the source. But `_hc-field.md` flags its own number as a **floor with an open falsifier** (6 of 13 never checked). HARNESS presents "~10, MEASURED" as clean and drops the caveat its own child attached. Same pattern as E-1 and E-8: the caveat dies in transit. |
| M-11 | §6: "trigger-scout resumed from its own session-limit death ... and *'picked up exactly where it left off'* (VERIFIED — **its journal :1528**)" | `.swarm/journal/trigger-scout.md:1528` = "## 2026-07-13 13:23Z — resumed after a session-limit death; reconciliation, not new investigation". **`grep -c 'picked up exactly where it left off' trigger-scout.md` → 0.** The phrase is at `_hc-field.md:26` — the *collector's own summary sentence* introducing the quote. | **WRONG** | ⚠ Re-verified by me directly. HARNESS puts a **secondary document's framing prose in quote marks and attributes it to the primary journal, tagged VERIFIED.** The phrase does not exist in trigger-scout.md. The underlying event (it did resume and reconcile) is real — but this is the exact failure mode the VERIFIED tag is supposed to prevent. |
| M-12 | §6: "`bin/swarm` today has no targeted way to stop a pane's occupant (only whole-pane close — **`_hc-mech.md` §5.3**)" | **`_hc-mech.md` has no §5.3.** §5 ("Mechanically: relaunching an existing agent's pane with a different `--model`", `:390`) is a **flat, unnumbered list**; grep for "5.1"/"5.2"/"5.3"/"### 5" → zero hits. The matching content is in item 1. | **WRONG** | ⚠ Re-verified by me. **A fabricated subsection number** — HARNESS invents citation granularity the source does not have. The *fact* is independently true (I grepped `bin/swarm`: only `pane list/read/send-text/send-keys/run/close`; no targeted stop), which makes this worse, not better: a true claim was given a fake address. |
| M-13 | §6: "*'a killed-and-relaunched pane is indistinguishable from a fresh launch to this hook'* (VERIFIED — `_hc-mech.md` §3; `bin/swarm:916-935`)" | `_hc-mech.md` §3 (nearest match): "restore does not distinguish 'relaunched after a kill' from 'very first launch'; both look like a fresh SessionStart to this hook." `bin/swarm:916-935` = `cmd_restore`, confirmed: `payload.get("source") or "startup"` sends any non-`compact` source down the same branch as a true first launch. | **OVERSTATED** | Section right, line range right, mechanism right and independently verified. But the **quotation marks are false** — that exact sentence is not in `_hc-mech.md` (grep: 0 hits for "killed-and-relaunched"). It is HARNESS's paraphrase dressed as a verbatim quote under a VERIFIED tag. |
| M-14 | §6: "re-run the launcher with the existing **`herdr pane run <pane>`** — spawn's own verb, reusable against a live pane id (VERIFIED against `_hc-mech.md` §5)" | `_hc-mech.md` §5 item 1: "Getting a pane to run something new is done exactly once in this codebase via `herdr pane run <pane> <path>` ... it is **mechanically reusable against an EXISTING pane id**". Independently confirmed: single call site, `bin/swarm:1185`. | **REACHES** | Content and section both land. The one `_hc-mech.md` cite that holds. |

### D. Haiku / industry / SLM (`hcrev-slm`)

| # | CLAIM (quoted from HARNESS.md) | SOURCE CHECKED (file:line, quoted) | VERDICT | NOTE |
|---|---|---|---|---|
| S-1 | §2.4: "**MEASURED** — both Haiku arms ... **blocked on a permission dialog before the synthesis step**" | `weak-model-delegation-2026-07-13.md:32-33`: "`wmd-haiku` \| Haiku 4.5 (pinned) \| **Blocked** on a permission dialog (`mkdir`). No artifact." / "`wmd-haiku2` \| ... **Blocked** on a permission dialog (journal write). **0-byte** artifact." Raw pane captures show genuine Bash-tool prompts: "Do you want to proceed? ❯ 1. Yes / 2. Yes, and always allow / 3. No" — **not** trust dialogs. | **REACHES** | The *observational* claim is solid, and verified against **primary** evidence (raw pane text), not self-report. Exactly two arms; both permission (not trust); both before any synthesis. |
| S-2 | §2.4: "**Haiku ... cannot run in auto permission mode**, so its first dialog wedges it forever" — and the spawn refusal built on it: "swarm: haiku cannot hold an agent pane: no auto permission mode ... (measured: ...)" | `weak-model-delegation-2026-07-13.md:87`: "**The stall was caused by a permission gate swarm hands EVERY child regardless of model. Opus would block too** ... **A tier rule about cheap models does not fix an infrastructure gate that fires on all models.**" `:89`: the Opus-into-the-wall falsifier, "**the top re-run item**" — never run. `:91`: "**WHAT MUST HAPPEN BEFORE ANYONE LOCKS A TIER RULE ON THIS**". `grep permissions bin/swarm` → **0 hits**. | **OVERSTATED (load-bearing)** | See **F-1**. The causal claim is **not** what was measured, and the cited source **argues against it by name**. HARNESS's own §8 concedes the real cause ("the Haiku ban is its bill arriving"). §2.4 and §8 cannot both be true. |
| S-3 | §2.3: "the Haiku ban exists because a permission-wedged pane has the same invisibility (**DOCUMENTED — operator correction, 2026-07-13**)" | No locatable standalone artifact for an "operator correction" distinct from the weak-model-delegation doc itself. | **UNVERIFIABLE** | DOCUMENTED promises "a named source says so." The source named is an unlogged operator remark with no transcript, message, or journal pointer. |
| S-4 | §1: "`_hc-industry.md` **surveys eleven of them**" (in a sentence about "a graph-engine runtime like the industry's") | `_hc-industry.md` has exactly 11 top-level sections — but §10 (Temporal) and §11 (Ray) are self-labeled in their own headers "**(analogy only — worker/task retry, not LLM-specific)**", and §8 (LiteLLM) / §9 (OpenRouter) are routing gateways, not agent frameworks. | **OVERSTATED** | The count of 11 is literally right. Calling all eleven *frameworks* — in a sentence about agent graph-engines — folds in 2 explicitly-non-LLM analogies and 2 non-agent routers. Real count of surveyed LLM agent frameworks: ~7. |
| S-5 | §5: "aider's main/editor/weak triad and CrewAI's `manager_llm` are **the only two** shipped as abstractions" | `_hc-industry.md:585-592`: "**Only aider** (main/editor/weak triad...) **and CrewAI** (`manager_llm` + `Process.hierarchical`) have an officially named pattern. LangGraph and OpenAI Agents SDK document the... idea only as **prose guidance**..." | **REACHES** | Near-verbatim match to the source's own cross-cutting finding, including the LangGraph/OpenAI-SDK prose-only detail HARNESS also uses. |
| S-6 | §6: "Claude Code's own `--fallback-model` **explicitly excludes rate-limit, auth, and billing errors** (DOCUMENTED — `_hc-industry.md` **finding 4**)" | `_hc-industry.md:313-314`: "Explicitly: '**Authentication, billing, rate-limit, request-size, and transport errors never trigger a switch.**' (Source: code.claude.com/docs/en/model-config.)" — this is item **1** under §5(c), **not** "finding 4". The doc's only numbered findings list is the 5-item cross-cutting section; its item 4 is about fallback-list ordering. | **OVERSTATED (miscited)** | Content is accurate and primary-sourced (verbatim from Anthropic's docs). The **pincite "finding 4" points at nothing** — a reader following it lands on an unrelated item. Same disease as M-12: true claim, invented address. |
| S-7 | §7.1: "**Needle** is their **26M-parameter** function-calling model (**MIT license**)"; "**Cactus** ... a **tiered proprietary license**" | `_hc-slm.md:61`: "**License: MIT** ... DOCUMENTED — huggingface.co/Cactus-Compute/needle". `:46`: "**Custom proprietary license with a tiered free-use carve-out** ... DOCUMENTED — github.com/cactus-compute/cactus/blob/main/LICENSE". | **REACHES** | Both sourced with live URLs. HARNESS also correctly carries the source's two honest gaps (Needle's context window undocumented; nothing about multi-agent orchestration). |
| S-8 | §7.2(a): "A dedicated study (**arXiv 2606.07587**, 'Routing Plateau') finds routers structurally plateau below oracle accuracy **with failures concentrated on the hardest queries**" | `_hc-slm.md:241-245` cites it. **Independently verified live (WebSearch + WebFetch):** arXiv 2606.07587 is **real** — "The Routing Plateau: Understanding and Breaking the Accuracy Limits of LLM Routers"; 21 routing methods, 5 benchmarks; routers learn "global averaged model-performance trends" and fail on queries needing instance-specific judgment. | **REACHES** | ⚠ **Explicitly hunted as a suspected hallucination (2606 = June 2026, one month before this doc) and cleared.** The paper exists; title, method count, and core finding all match. HARNESS's "concentrated on the hardest queries" is a fair gloss. **Not** a laundered cite. |
| S-9 | §7.2(a): "**FrugalGPT, RouteLLM**: up to **85% cost reduction at 95% of GPT-4 performance**" | `_hc-slm.md:235` — that figure is **RouteLLM's**: "reduce costs by up to 85% while maintaining 95% of GPT-4's performance" (github.com/lm-sys/RouteLLM). `_hc-slm.md:230` — **FrugalGPT's** own number is different: "up to **98%** cost reduction". | **OVERSTATED (attribution blur)** | Both numbers are genuinely sourced; HARNESS fuses two frameworks' distinct results into one shared figure. Doesn't change the argument, but it is a citation the reader cannot follow back. |
| S-10 | §7.2 (last): "**38.2% unnecessary calls (Qwen3-8B)** and **39.0% missed calls (Llama-3.2-3B)** on **the same 2026 benchmark**" | `_hc-slm.md:165` (38.2%, Qwen3-8B) is dual-sourced to arXiv 2605.18882 **and** Local Agent Bench; `:167` (39.0%, Llama-3.2-3B) is sourced **only** to Local Agent Bench. The source's own hedge: "directly quantified in **at least one** 2026 benchmark". | **OVERSTATED (minor)** | Both numbers are named and sourced — *not* the unsourced-number finding I sent the child hunting for. But "**the same** 2026 benchmark" hardens the source's own hedge into a confident shared provenance. |
| S-11 | §7.2 (last): "**xLAM-7B 88%** on BFCL-v1-era scoring; **Octopus-v2's 99.5%** is its own narrow benchmark" — framed as "largely **self-reported**" | `_hc-slm.md:110`: "xLAM-7b-fc-r **88.24%** ... Flag: these are old (mid-2024) **BFCL-v1-era** numbers." `:124`: "Octopus v2 (2B) **99.524%** ... Caveat: this is a **single-paper, author-run benchmark** on a narrow Android-API task set". | **REACHES** | Numbers exact, and HARNESS **faithfully carries the source's skepticism** rather than dropping it. The best-behaved citation in the document — the one place a caveat survives transit intact. |
| S-12 | General: do `_hc-slm.md`'s **DOCUMENTED** tags rest on primary sources, or on a child's assertion? | ~15 DOCUMENTED tags spot-checked: nearly all carry inline URLs (github, huggingface, arxiv, vendor docs). Where a claim rests on a blog post, the doc self-downgrades ("secondary source, could not confirm this exact framing"). | **REACHES** | `_hc-slm.md`'s own evidence discipline is genuinely good. **No bare unsourced DOCUMENTED tag found.** The SLM strand is HARNESS's best-sourced section. |

---

## PATTERNS WORTH NAMING

1. **The caveat dies in transit.** Five times (E-1, E-8, M-8, M-10, and F-1's whole shape),
   a child artifact attaches a caveat to its own number — *same-harness caveat REMAINS*;
   *confounded, read as "at most this bad"*; *6 of 13 never checked*; *the gate fires on all
   models* — and HARNESS cites the number and drops the caveat. Each drop makes the number
   stronger than its source allows, and each drop is in the direction of the doc's argument.
   That is the signature of motivated citation, not of sloppiness.

2. **Section-number citation quality tracks how close the source was.** All **9 of 9**
   MODEL-FIT section cites land (M-1..M-7) — that doc was clearly open while writing. But
   **3 of 7** cites into HARNESS's *own harvested children* have defects, including **two
   invented addresses** (`_hc-mech.md §5.3` and `_hc-industry.md "finding 4"` — neither
   exists). The child docs were cited from memory of a summary pass. **The irony is exact:**
   the doc is least rigorous precisely where it cites the evidence it commissioned itself.

3. **Paraphrase dressed as quotation, under a VERIFIED tag.** Three times (E-5, M-11, M-13)
   HARNESS puts quotation marks around text that is not in the cited source — most seriously
   M-11, where a *collector's summary sentence* from `_hc-field.md` is attributed to the
   primary journal it summarizes. VERIFIED is defined in the doc's own preamble as "**I ran it
   / read the line — quoted, file:line**." Three VERIFIED tags do not meet that definition.

4. **What holds up.** This is not a doc built on sand. The `bin/swarm` mechanical claims
   (A-1, A-5, A-9, A-10, M-14) are exact. MODEL-FIT is cited impeccably. The SLM strand is the
   best-sourced section in the document, and the arXiv cite I was sent to break **survived a
   live check**. 21 of 45 tags reach cleanly. The failures are concentrated, not diffuse — and
   they concentrate in the places the argument most needs them to hold.

---

## WHAT I'D PUT TO `hc-red`

- **F-1 is disqualifying for §2.4 as written.** The survivability gate — a new axis, a new
  spawn-time refusal, and the doc's own "type specimen" — is built on a causal claim the cited
  source explicitly rebuts under a header reading *"WHAT MUST HAPPEN BEFORE ANYONE LOCKS A
  TIER RULE ON THIS."* The cheap falsifier (`wmd:89`) was never run. Either run it, or rewrite
  §2.4 around the actual measured fact: **swarm spawns every child without a `permissions`
  block, and any model can wedge on the first dialog.** That reframing does not weaken the
  design — §2.3's blocked-visibility requirement survives intact, and it is arguably
  *strengthened*, because the bug is universal rather than Haiku-shaped.
- **F-3 breaks §7.2(b)'s argument, not its conclusion.** The cut of the SLM classifier may
  still be right — but "the regex cannot be sweet-talked" is false, and it is the load-bearing
  premise as written. Both the regex and an SLM read the same attacker-controlled string. The
  honest difference is *determinism and a closed output enum*, which an SLM behind the same
  contract would also have. **Rewrite the premise or the ruling loses its support.** Worth
  noting to the branch owner separately: `[blocked: kind]` is forgeable by any agent with an
  `echo`, and it false-positives on innocent prose containing "resets".
- **F-2 is a one-line fix** but it falsifies §4.2's "no new mechanism" framing: there is no
  `.swarm/config` to add a stanza to.
- **E-7 must be fixed regardless of anything else:** the document states its own headline eval
  number two different ways (4/7 in §3, 3/7 in §5) and the source supports only 4/7.

*Falsifier for this audit:* if a re-read shows `.swarm/config` exists somewhere I did not look,
or `_hc-mech.md` gained a §5.3, or the Opus-into-the-wall falsifier was in fact run and I
missed the artifact, then F-2, M-12, and F-1 respectively collapse. I checked each by direct
grep and re-read; the child verdicts I report as WRONG I re-verified against the same lines
myself, and I overturned one child verdict (E-4) that did not survive that check.
