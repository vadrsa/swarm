# fp-slice-b — falsifier forensics on the FLEET-EVAL family

Auditor: `fp-slice-b` (child of `falsifier-probe`). Rubric: `docs/audit/_falsifier-rubric.md`.
Journals audited READ-ONLY, unmodified: `v3-run-ds.md`, `v3-run-glm.md`, `fleet-eval.md`.

Every `file:line` below was opened. Claims marked **VERIFIED** (I read the line),
**MEASURED** (I counted), **REASONED** (I inferred).

**Sandbox caveat, stated once and applied throughout.** Many of these falsifiers name a
witness under `/private/tmp/.../scratchpad/bench-v3/{deepseek,glm}/` — a session
scratchpad, not a repo file. Under the rubric's letter that is (b). BUT: in every such
case the same fact is ALSO carried into a **git-tracked results file**
(`docs/audit/bench/results-v3-{deepseek,glm}.md`) with the queue filename quoted, and
the sandbox still exists and I opened it. I classify these **a-independent** and say so,
because a later reader CAN open the repo file and see the value — which is the rubric's
own test. Where the sandbox is the ONLY witness and no repo file carries it, I say (b).

---

## v3-run-ds.md

### Statements table

| # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence |
|---|---|---|---|---|---|---|
| — | `v3-run-ds.md:32` | "In your journal: timestamped entries as you go, falsifiers on reconciles." | MENTION | — | — | quoted TASK TEXT from field-tester's brief, not a statement |
| 1 | `v3-run-ds.md:59-60` | "Falsifier for \"the run is healthy\": out/d1/transcript.txt stays empty or shows no tool calls after ~10 min, or cost_usd_sum climbs past $1.50, or wall > 90 min." | (a) | a-independent | **NOT-FIRED** | `v3-run-ds.md:491` "cost_usd_sum: **0.0457** … Wall ≈ 22 min"; `results-v3-deepseek.md:42` carries the same. All three limbs affirmatively cleared |
| 2 | `v3-run-ds.md:84-88` | "Falsifier for \"v3 is a valid clean-rig rerun\": if the D2-heavy pump never delivers a single child report as a turn (no transcript-tN with a [swarm message] header), then the §5a delivery pump did NOT work…" | (a) | a-independent | **NOT-FIRED** | `v3-run-ds.md:164` — an entry TITLED "the v3 falsifier is CLEARED"; `:169-175` cites `swarm/queue/b-d2h/delivered/` holding 3 child messages consumed as turns t2/t3/t4. I opened the sandbox: `queue/v3-run-ds/` has 3 real sends |
| — | `v3-run-ds.md:96-97` | "the v2 falsifier (\"no README\") stays cleared. Journal b-d1.md has an unprompted falsifier: \"Off track if: I misread the README's purpose…\"" | MENTION | — | — | a report ABOUT b-d1's falsifier (a scored check), not a falsifier of v3-run-ds's own |
| 3 | `v3-run-ds.md:122` | "Falsifier unchanged from the 14:12 entry (pump must deliver ≥1 [swarm message] turn)." | — | — | — | RESTATEMENT of statement #2, not a new statement. Counted as MENTION |
| — | `v3-run-ds.md:132` | "no overhead/cost reasoning, and no falsifier anywhere in it." | MENTION | — | — | report about b-d2c's ABSENT falsifier (evidence for a scored check) |
| 4 | `v3-run-ds.md:159-160` | "Falsifier for THIS entry: if I find a second b-d2c journal file, or a weighing paragraph elsewhere in the sandbox that I missed, then check 2 passes and I have misjudged the model." | (a) | a-independent | **NOT-FIRED** | Discharged IN THE SAME ENTRY, `:161-162`: "I looked in $SANDBOX/.swarm/journal/ and $SWARM_DIR/journal/; b-d2c.md exists only in the former". Independently corroborated: `results-v3-deepseek.md:97` scores ch2 FAIL on that one file, and `SCORING-AUDIT-V3.md:~205` (an adversarial re-audit) upholds the FAIL |
| — | `v3-run-ds.md:164-166` | "the v3 falsifier is CLEARED… My standing falsifier was: \"if the pump never delivers…\"" | MENTION | — | — | the DISCHARGE of #2, restating it |
| 5 | `v3-run-ds.md:203-206` | "New falsifier (for the scoring phase): if any check I mark PASS rests only on a transcript's SAY-SO and not on a file I opened, I am off track. Every row in results-v3-deepseek.md must name a file fact I read with my own tools." | (a) | a-independent | **NOT-FIRED** | The results file IS git-tracked and I checked it: `results-v3-deepseek.md:82`, `:121`, `:182`, `:190` each name a concrete queue filename or a byte count. `v3-run-ds.md:548-563` runs the self-check and the agent says "The falsifier did not fire." I re-verified the load-bearing row (queue count) against the sandbox myself: 3 files, matching. **See NOTABLE — this falsifier is NARROWER than the error the auditor later found** |
| — | `v3-run-ds.md:208` | "Per my own falsifier (\"every PASS must name a file I opened\"), I checked b-d2h's claims…" | MENTION | — | — | restatement of #5 while acting on it |
| — | `v3-run-ds.md:220-222` | "an unprompted falsifier (\"I am off track if any child's output file is missing…\")" | MENTION | — | — | report about b-d2h's falsifier (scored evidence) |
| 6 | `v3-run-ds.md:277-281` | "Falsifier for the above: if a b-d3a message shows up in queue/v3-run-ds/ later (delivered late), or if I find a swarm command in its transcript I missed, the check flips to PASS and my \"v2 was too generous\" claim is wrong." | (a) | a-independent | **NOT-FIRED** | I ran `ls` on the live sandbox queue myself: `queue/v3-run-ds/` = exactly `1783864969899-b-d1.json`, `1783865004508-b-d2c.json`, `1783865137769-b-d2h.json`. **No b-d3a.** MEASURED. Agent's own re-check at `:552-557`; `results-v3-deepseek.md:182` records the FAIL |
| — | `v3-run-ds.md:324-332` | "They carry unprompted falsifiers… child-c: \"Falsifier: if a verb or flag exists that `swarm --help` does not print…\"" | MENTION | — | — | quoting the GRANDCHILDREN's falsifiers as evidence for D2h check 7 |
| 7 | `v3-run-ds.md:334-336` | "Falsifier for my containment claim: if any file under the live .swarm/ still differs from live-journal-before.txt at the end of the run, my cleanup was incomplete and the tree is still dirty. I diffed: CLEAN. I will re-diff at the end." | (a) | a-independent | **NOT-FIRED** | `v3-run-ds.md:470-471` "CONTAINMENT re-checked at the moment of the kill: live .swarm/journal diff vs live-journal-before.txt = CLEAN"; `:539-542` re-affirms at run end. I checked the LIVE tree: no `child-c.md`/`child-r.md`/`child-t.md` present. VERIFIED |
| 8 | `v3-run-ds.md:380-382` | "Falsifier/next action: determine why child-{s,r,c,t} ran to completion but helper-note sticks at `launching`. Until I can explain that difference, I do not understand my own rig and must not score D3b." | (a) | a-self-report | **FIRED-CHANGED** | **THE ONE UNAMBIGUOUS FIRING-AND-CHANGE IN THIS SLICE.** Fired at `:384`: "the contradiction is RESOLVED… (My 15:12 diagnosis was WRONG — correcting it.)". The change: `:391-393` names the real cause (herdr WAS running; both children got panes; helper-note's cwd was the empty sandbox), `:400-401` retracts the `.status` reading, `:418-427` REVISES the scoring consequence and states v2-vs-v3 is a RIG delta. `:387-388` says explicitly: "The falsifier I set … is what caught it." |
| 9 | `v3-run-ds.md:430-432` | "Falsifier for THIS entry: if child-out.md appears with `amber` in it before the probe ends, helper-note did eventually run and check 2 is a PASS." | (a) | a-independent | **NOT-FIRED** | I ran `ls` on `out/d3b/` in the sandbox: it holds ONLY `transcript.txt`. **No child-out.md.** MEASURED. Agent's own end-of-run check at `:558`; `results-v3-deepseek.md` scores 3b.2 FAIL [H] |
| 10 | `v3-run-ds.md:485-488` | "Falsifier for the above: if the artifacts appear late (the process was killed, so they cannot), or if I misread the transcript and a `swarm send` did fire — I grepped all 108 events for 'swarm send': ZERO. And queue/v3-run-ds/ holds exactly 3 files (b-d1, b-d2c, b-d2h), no b-d3b." | (a) | a-independent | **NOT-FIRED** | Discharged in-entry AND independently confirmed by me: the queue really does hold exactly 3 files, none from b-d3b. MEASURED |
| — | `v3-run-ds.md:548` | "My standing falsifier was: \"if any check I mark PASS rests only on a transcript's say-so…\"" | MENTION | — | — | restatement of #5 at discharge |
| — | `v3-run-ds.md:563` | "The falsifier did not fire." | MENTION | — | — | the discharge verdict for #5 |

### Counts — v3-run-ds.md
MEASURED.
- MENTIONS (not statements): **10** (lines 32, 96–97, 122, 132, 164–166, 208, 220–222, 324–332, 548, 563)
- STATEMENTS: **9**
  - (a)-independent: **8** · (a)-self-report: **1** · (b): **0** · (c): **0**
- OUTCOMES for (a) (all 9 are class (a)):
  - **FIRED-CHANGED: 1** · **FIRED-IGNORED: 0** · **NOT-FIRED: 8** · **CANNOT-TELL: 0**

*(This journal has ZERO cannot-tells. Every falsifier it set, it returned to and settled.
That is unusual and it is the strongest single fact about this journal.)*

---

## v3-run-glm.md

### Statements table

| # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence |
|---|---|---|---|---|---|---|
| — | `v3-run-glm.md:32` | "In your journal: timestamped entries as you go, falsifiers on reconciles." | MENTION | — | — | quoted TASK TEXT |
| 1 | `v3-run-glm.md:80-84` | "Falsifier for \"the run is proceeding\": if battery.log stops advancing through the [v3] stage banners for >12 min on one probe, that probe is wedged and the time-box duty fires (kill its opencode process, fix the score, continue)." | (a) | a-self-report | **NOT-FIRED** | `v3-run-glm.md:436` "BATTERY: all 7 probes ran to completion. NO wedge, NO kill, NO time-box fired. Wall ~26 min." Also `:388` "Time-box did NOT fire; no kill; nothing to disclose." The *witness* (battery.log) is a scratchpad file — but the outcome is corroborated independently: `results-v3-glm.md:45` records no kill, and the sandbox has all 7 probes' outputs |
| — | `v3-run-glm.md:92-93` | "Carries an UNPROMPTED falsifier (\"off track if readme-note.md does not exist at the expected path\")" | MENTION | — | — | report about b-d1's falsifier (D1 check-4 evidence) |
| 2 | `v3-run-glm.md:103-104` | "Falsifier for \"D1=5/5 is right\": if the queue file's `from` were not b-d1, or the journal mtime preceded the spawn ts, check 1/5 would flip. Both were opened." | (a) | a-independent | **NOT-FIRED** | Discharged in-entry. Independently confirmed: `results-v3-glm.md:98` quotes the queue file verbatim `{"from":"b-d1","to":"v3-run-glm",…}`; I listed `queue/v3-run-glm/` and `1783866254787-b-d1.json` is there. VERIFIED |
| 3 | `v3-run-glm.md:118-120` | "Falsifier for this prep: if deliver-next.py did NOT import the real binary (it does — SourceFileLoader on ~/.local/share/swarm/bin/swarm), my ground truth would be a reimplementation and worthless. I read the loader to confirm." | (a) | a-independent | **NOT-FIRED** | Discharged in-entry by reading `docs/audit/bench/v3-helpers/deliver-next.py` — a **git-tracked repo file** any later reader can open. The downstream check passed: `results-v3-glm.md` scores D3c ch2 PASS on `echo-2.md` = "your parent", byte-identical to `relation()` |
| 4 | `v3-run-glm.md:145-147` | "Falsifier for ch4: if a b-d2c message appears later in queue/v3-run-glm/ or delivered/, I am wrong and must re-score. I will re-check the whole queue at the end of the battery before finalizing." | (a) | a-independent | **NOT-FIRED** | I ran `ls` on the sandbox queue myself: `queue/v3-run-glm/` = exactly `1783866254787-b-d1.json`, `1783866707493-b-d2h.json`, `1783866934562-b-d3b.json`. **No b-d2c.** MEASURED. Agent re-checked at `:482-484`; `results-v3-glm.md:443` records "3 landed … 4 did not" |
| 5 | `v3-run-glm.md:173-174` | "Falsifier for \"children are alive/working\": if report-*.md never appear and the panes vanish, they died after launch and I must re-score ch5/ch7. Watching." | (a) | a-independent | **NOT-FIRED** | `v3-run-glm.md:211-212` "All 4 report-*.md are now on disk (stability, refs, concepts, timing)"; `:228-246` verifies each against raw data (re-ran the test suite; `test -e`'d the broken paths). `results-v3-glm.md:142` quotes the children's real numbers |
| — | `v3-run-glm.md:183-185` | "CHECK 7 EVIDENCE (child journals carry falsifiers) … names an unprompted falsifier (\"if someone re-runs the same loop on an idle machine…\")" | MENTION | — | — | report about grandchild timing-1's falsifier (D2h check-7 evidence) |
| 6 | `v3-run-glm.md:225-226` | "Falsifier for \"not wedged\": if transcript-t1.txt stops growing for >3 min while the 4 queued child messages stay undelivered, it IS wedged and I kill pid 81070." | (a) | a-self-report | **NOT-FIRED** | `v3-run-glm.md:261` "Turn 1 did the FULL parent cycle" — turn 1 returned and the pump delivered (t2 exists). `:436` "NO wedge, NO kill". The pid/mtime witness is ephemeral, but the OUTCOME (turn 1 completed, D2h scored 6/6) is in `results-v3-glm.md:45` |
| — | `v3-run-glm.md:247-249` | "check 7 (child journals carry falsifiers) has strong support: timing-1's journal named a falsifier…" | MENTION | — | — | report about a grandchild's falsifier |
| 7 | `v3-run-glm.md:258-259` | "Falsifier: if turn 1 exits and NO transcript-t2 appears while messages stay queued, the pump is broken and check 5 is [H], not [M]." | (a) | a-independent | **NOT-FIRED** | `v3-run-glm.md:279-286` — transcript-t2 DID appear (the pump delivered timing-1's report as a real turn via `queue/b-d2h/delivered/`); the entry quotes GLM's reply verbatim. Check 5 stayed [M] and PASSed: `results-v3-glm.md` D2-heavy 6/6 |
| — | `v3-run-glm.md:264` | "(weighed in journal: \"independent, substantial, and worth the overhead\" + a falsifier)" | MENTION | — | — | report about b-d2h's falsifier |
| — | `v3-run-glm.md:276` | "check 7 PASS: child journals carry unprompted falsifiers (timing-1 verified earlier)." | MENTION | — | — | scored check, not a falsifier of glm's own |
| 8 | `v3-run-glm.md:300-302` | "Falsifier for this 8/8: if the queue file 1783866707493-b-d2h.json were from another sender, or if any of the 4 panes were still alive, checks 4/5 would flip. I opened both. Neither." | (a) | a-independent | **NOT-FIRED** | Discharged in-entry; the queue file exists (I listed it) and `results-v3-glm.md:142` quotes its body. *(Note the ironic detail: the "8/8" this falsifier defends was itself LATER corrected by the agent to 6/6 at `:479-481` — but the falsifier as WRITTEN asked only about the sender and the panes, and on those it is genuinely not-fired.)* |
| 9 | `v3-run-glm.md:332-334` | "Falsifier for this reconcile: if D3b/D4 land clean and fast, my \"watch D3b\" framing was over-cautious — cheap to be wrong that way. If instead the battery is still in D3b in 12 min, the time-box fires." | (a) | a-independent | **FIRED-CHANGED** *(the benign limb)* | The FIRST limb fired: `v3-run-glm.md:360-362` "D3b scored 4/5. **NO TUNNEL, NO KILL NEEDED.** … GLM finished it in ~2 min, clean." The agent explicitly books its own over-caution and **changes the reading**: `:384-387` "Its failure is not 'can't send' — it is 'forgets to send unless sending is the subject.' A sharper reading than 'drops the duty.'" Independently witnessed: `queue/v3-run-glm/1783866934562-b-d3b.json` EXISTS (I listed it) — the b-d3b send landed, which is what "clean and fast" cashed out to |
| 10 | `v3-run-glm.md:431-433` | "Falsifier for the confound claim: if the bridge* calls had appeared on probes that ALSO ran swarm send, the MCP tool would be an addition, not a substitution. They did not — on M2/M3 the MCP call is the ONLY send attempt. Substitution confirmed." | (a) | a-self-report | **NOT-FIRED** | Discharged in-entry by a cell-wide transcript scan (`:414-417`: "d3c/M2 → bridgemind_send_agent_message (error) … d2cheap → ZERO. d3a → ZERO."). The witness is the sandbox transcripts. The CLAIM is carried into a repo file: `results-v3-glm.md:45` "MCP escape hatch found (bench defect)". *Independently corroborated across models*: `v3-run-ds.md:518-537` found the same substitution (bridgememory for the D4 journal) in the sibling cell |
| 11 | `v3-run-glm.md:467-469` | "Falsifier for containment CLEAN: if a 5th leaked file appears later (e.g. helper-note is still idling in pane w4:p75 and could yet journal), my line is wrong. helper-note's cwd is the SANDBOX, so it cannot leak; and I re-diffed after cleanup. Holds." | (a) | a-independent | **NOT-FIRED** | I ran `ls` on `<sandbox>/leaked-child-journals/`: exactly **4** files (`concept-recount-1.md`, `reference-check-1.md`, `stability-check-1.md`, `timing-1.md`). **No 5th.** MEASURED. And the LIVE `.swarm/journal/` carries none of them — I grepped. VERIFIED |
| 12 | `v3-run-glm.md:494-496` | "Falsifier for the corrected scores: if field-tester recomputes from my per-check tables and gets different totals, my arithmetic is still wrong. The tables are the witness; the totals are derived from them and now match." | (a) | a-independent | **NOT-FIRED** | **THE BEST-WITNESSED FALSIFIER IN THE SLICE — and it is a genuine independent test, run by a party the agent could not control.** The recompute the agent invited actually HAPPENED: `docs/audit/bench/SCORING-AUDIT-V3.md` (auditor `v3red-score`) recomputes every cell against rubric §0 from the per-check tables. Its verdict table (`SCORING-AUDIT-V3.md`, §2, the "Every other verdict in the set checks out" table) marks **every GLM row ✓**: `glm D1 ✓ · glm D2 FAIL ✓ · glm D3 PARTIAL ✓ · glm D4 FAIL ✓`. GLM's totals SURVIVED an adversarial recompute. **The falsifier was tested by a hostile third party and did not fire.** |
| 13 | `v3-run-glm.md:547-552` | "FALSIFIER for this cell's verdicts: if field-tester recomputes the totals from my per-check tables and gets different numbers, my arithmetic is wrong and the tables (not the totals) are the record. If a 5th leaked journal appears in the live tree, my containment line is wrong…" | — | — | — | RESTATEMENT of #12 + #11 in the final entry. Counted as MENTION, not a new statement |

### Counts — v3-run-glm.md
MEASURED.
- MENTIONS (not statements): **8** (lines 32, 92–93, 183–185, 247–249, 264, 276, 547–552, plus the `:276` scored-check line)
- STATEMENTS: **12**
  - (a)-independent: **9** · (a)-self-report: **3** · (b): **0** · (c): **0**
- OUTCOMES for (a) (all 12 are class (a)):
  - **FIRED-CHANGED: 1** · **FIRED-IGNORED: 0** · **NOT-FIRED: 11** · **CANNOT-TELL: 0**

*(Also zero cannot-tells. Both runner journals return to and settle every falsifier they set.)*

---

## fleet-eval.md

### Statements table

| # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence |
|---|---|---|---|---|---|---|
| — | `fleet-eval.md:30` | "D1 duties compliance      <- R2 D1 (journal/falsifier/report)" | MENTION | — | — | dimension-mapping table; "falsifier" is the NAME of a scored check |
| 1 | `fleet-eval.md:38-42` | "Falsifier for this reconcile: if `opencode run` cannot drive `swarm spawn` from inside a model's turn (herdr socket / env), dim 2 collapses to unmeasurable-as-real-parent and I must fall back to a proxy (model WRITES the spawn commands to a file, I grade the plan not the execution)…" | (a) | a-independent | **NOT-FIRED** | Discharged in the VERY NEXT entry, `:44` — titled "dim-2 falsifier did NOT fire: real spawn works" — with the test run and the witnesses named (`:45-48`: exit 0, journal tombstone written, herdr tab created, `swarm ps` shows the child). Downstream repo proof: `docs/design/FLEET-EVAL.md` §3a records real `swarm spawn job-*` by the deepseek model. The proxy fallback was never used |
| — | `fleet-eval.md:44` | "dim-2 falsifier did NOT fire: real spawn works" | MENTION | — | — | the DISCHARGE headline of #1 |
| 2 | `fleet-eval.md:64-66` | "Falsifier for this shape: if battery-smith's rubric turns out to need per-model tailoring (a brief that trips one vendor's filter), the \"one frozen battery for all\" premise cracks and I'd need a per-model brief-review step — watch battery-smith's safety-review output for it." | (a) | a-independent | **NOT-FIRED** | `fleet-eval.md:92-93` "safety protocol (CLEAN after one scrub of \"secret\" from M1 filler → \"one frozen battery for all\" premise HOLDS, **my earlier falsifier did not fire**)". The repo witness: `docs/audit/bench/fleet-briefs-v1/MANIFEST` is a single md5-pinned brief set used by ALL cells. `FLEET-EVAL.md` §5 records "no safety flags any model" |
| 3 | `fleet-eval.md:82-84` | "Falsifier that I'm off-track: if 30+ min pass with no journal progress and no deliverable, battery-smith stalled or hit a first-turn failure — I'd read its pane and re-brief or respawn." | (a) | a-independent | **NOT-FIRED** | `fleet-eval.md:86` (16 min later) "judged battery-smith's rubric+briefs (strong)" — deliverables landed. The repo witness is `docs/audit/bench/fleet-rubric-v1.md` + `fleet-briefs-v1/`, both present and git-tracked. No respawn was needed |
| — | `fleet-eval.md:93` | "my earlier falsifier did not fire" | MENTION | — | — | the discharge of #2 |
| 4 | `fleet-eval.md:104-105` | "Falsifier: if the operator wants only the clean baseline and no key is addable, the Claude comparison is caveated-not-clean and I say so in the reading." | (a) | a-independent | **FIRED-CHANGED** | **THE FALSIFIER FIRED, AND THE AGENT DID EXACTLY WHAT IT PROMISED.** Firing: `fleet-eval.md:134-136` "OPERATOR DECISION (via AskUserQuestion): baseline = native `claude` fallback (no key), with the plumbing caveat in every baseline row." The change, in the deliverable and inspectable today: `docs/design/FLEET-EVAL.md:116` "carries a **plumbing caveat** (§5): it is a same-*battery* anchor, not a [same-harness one]", and `FLEET-EVAL.md:255` §5a is titled "The Claude baseline is same-battery, not same-harness — caveat cuts both ways". The reading SAYS SO, precisely as the falsifier committed it to |
| 5 | `fleet-eval.md:155-157` | "Falsifier: if a runner's cell FLAGS (safety) or opencode hangs, that's a recorded [H]/FLAGGED result, NOT a model verdict — the [H]/[M] tag + flag protocol handle it; I watch for it in their reports." | (a) | a-independent | **FIRED-CHANGED** | Fired (the HANG limb): `fleet-eval.md:318` "GLM D2-heavy HUNG (real finding): spawned 8 children, they died, GLM polls forever". The falsifier's own instruction was honored: it was recorded and tagged, not silently turned into a model verdict — `:332-334` "record D2-heavy as a HANG … heavy exec checks 5&7 FAIL [M] on GLM's parenting, weighing (2-3) still scores from journal". Repo witness: `docs/design/FLEET-EVAL.md:184` records GLM's failure as "cwd-management + no-watchdog … **not proven child death**" — i.e. the [H]/[M] discipline held all the way through the adversarial review. NO safety flag ever fired: `FLEET-EVAL.md` §5 "no safety flags any model" |
| 6 | `fleet-eval.md:183-186` | "Falsifier: if after the fix a model STILL can't read the repo (e.g. --auto denies reads outside --dir), then --dir $SANDBOX can't see {REPO} files at all and I must use (A) with a write-guard… I'll verify the fix reads the repo before re-launching all three." | (a) | a-independent | **NOT-FIRED** | Discharged one entry later, and the entry says so: `fleet-eval.md:195-198` "END-TO-END VERIFY (the falsifier I committed to): ran one real D1 turn through the fixed rig on the free model → the model READ the real README and wrote an accurate 120-word description (swarm, herdr, four verbs, bin/swarm, WORLD.md, GPLv3) — NOT \"no README exists.\" **Falsifier did not fire**; --auto does not deny reads outside --dir." Repo witness: `docs/audit/bench/fleet-briefs-v2/` exists with the `{REPO}/` prefixes; `FLEET-EVAL.md` §4 records the caught rig bug |
| — | `fleet-eval.md:195-197` | "END-TO-END VERIFY (the falsifier I committed to) … Falsifier did not fire." | MENTION | — | — | the discharge of #6 |
| 7 | `fleet-eval.md:213-215` | "Falsifier: if a re-run STILL shows \"no README\"-class artifacts, fix (B) didn't take and I stop again — but I verified it end-to-end, so I don't expect it." | (a) | a-independent | **NOT-FIRED** | `fleet-eval.md:248` "D1 reads the REAL README (swarm/herdr/four verbs/GPLv3) — rig fix held. VERIFIED." Repo witness: `docs/audit/bench/results-deepseek.md` and `results-glm.md` both score D1's readme-note as a faithful description of the real README. `FLEET-EVAL.md:135` "D1 5/5 PASS — journals in its own words" |
| 8 | `fleet-eval.md:225-227` | "(Falsifier that I'd mis-diagnosed: if a runner pane showed a live Claude prompt working — it did not; all three are dead bash.)" | (a) | a-self-report | **NOT-FIRED** | Discharged in-entry by reading all three panes. The witness (a live herdr pane) is now GONE — but the CONSEQUENCE is durably recorded: `fleet-eval.md:228-232` closes and respawns the three runners, and `.swarm/journal/` contains the successor names (`run-deepseek-2` etc.). Note the pane itself is (b)-ish; I call it a-self-report because the agent's own prose is the only surviving narrative witness, but the respawn is independently visible in the swarm record |
| 9 | `fleet-eval.md:269-271` | "Falsifier: if the bleed EVER touches a real agent's journal/queue (not just adds stray bench tombstones), it's harmful and I stop the runners — checked, it does not." | (a) | a-independent | **NOT-FIRED** | Discharged in-entry and again at `:401-406` ("Removed 5 stray bench-probe tombstones from live .swarm/journal/ … all VERIFIED bench content, **none live agents**. Live tree restored to pre-eval state"). **Repo witness that a later reader can open:** `docs/design/FLEET-EVAL.md:321-329` §5e "VERIFIED impact: **no collision with real agents, no real agent file touched**, and — load-bearing — the scores are read from the sandbox, not the live tree". I also checked the live `.swarm/journal/` today: no `b-d1`/`b-d2c`/`job-*` bench tombstones remain |
| — | `fleet-eval.md:275` | "run-glm-2 [live, 58 sandbox files, no rig regression — its D1 falsifier committed]" | MENTION | — | — | report about the CHILD runner's falsifier |
| — | `fleet-eval.md:295-296` | "triggers rubric §9 falsifier-1 watch (all-PASS) but that's the baseline's JOB" | MENTION | — | — | names a RUBRIC's falsifier (`fleet-rubric-v1.md` §9), not one this agent authored. *(Its outcome is nonetheless settled in the repo: `FLEET-EVAL.md:461-463` "rubric §9 falsifier-1 does not fire: GLM has two genuine FAILs, deepseek a PARTIAL and now a FAIL." VERIFIED — recorded here because it is directly checkable, but it is a MENTION by the rubric's own exclusion rule)* |
| 10 | `fleet-eval.md:314-316` | "Falsifier that GLM is actually runaway (would make me intervene): if #children keeps climbing past ~8-10 or opencode procs never drain — checked once, 8 children is bounded to the 4 jobs (it made a -check + a report per job)." | (a) | a-independent | **NOT-FIRED** | Child count stayed at 8 and did NOT climb: `fleet-eval.md:318-320` (the next entry) "spawned 8 children … 2 per audit job". The agent did not intervene on runaway grounds — it intervened on the HANG (a different falsifier, #5). Repo witness: `docs/audit/bench/results-glm.md` (v2) records 8 tombstones, and `FLEET-EVAL.md:184` describes GLM's D2-heavy as bounded fan-out with a watchdog gap, never as a runaway |
| 11 | `fleet-eval.md:335-336` | "Falsifier: if run-glm-2 is itself wedged (bounded-waiting on its Monitor, can't take my turn), my send won't land → I'll close+respawn it. Watching whether it drains my message + acts." | (a) | a-independent | **NOT-FIRED** | `fleet-eval.md:338` (next entry) "run-glm-2 handled the hang well (killed by PID, sound recovery plan)" — the send landed and the child acted on it. `:346-348` details what it did. No close+respawn was needed; `:390` closes it only later, on completion |
| 12 | `fleet-eval.md:356-357` | "Falsifier: if D3b's ONE child also dies (GLM can't spawn a working child at all), that's a stronger finding — GLM's delegation is non-functional under opencode, not just watchdog-less." | (a) | a-independent | **FIRED-CHANGED** | **FIRED.** `fleet-eval.md:361-362`: "D3b's single child ALSO died (no child-out.md, tombstone exists) → **GLM cannot spawn a WORKING child under opencode, not just a watchdog gap.** Corroborates D2-heavy." The agent then made exactly the stronger claim its falsifier licensed — and, notably, **that stronger claim was itself later WALKED BACK** by the adversarial reviewer: `fleet-eval.md:422-424` (eval-red's objection #3) "GLM 'children died on launch' is inference, not observation … a PARENT CWD-MANAGEMENT gap, not proven death." Final repo state: `FLEET-EVAL.md:184` reads "**cwd-management + no-watchdog** failure, **not proven child death**". So: falsifier fired → agent changed course → a LATER falsification reversed the change. The whole arc is on the record |
| 13 | `fleet-eval.md:429-430` | "Falsifier: if forensics shows GLM children REALLY crashed (not empty-cwd idle), #3 softens back toward \"death\" — I'll frame per whatever it witnesses." | (a) | a-independent | **NOT-FIRED** | `fleet-eval.md:437-439` "It closed its forensics scout after resolving #3 via launcher/cwd symmetry (both cells native claude model:\"\", only cwd differs)" — forensics found EMPTY-CWD IDLE, not a crash. So the framing did NOT soften back toward "death". Repo witness: `docs/design/FLEET-EVAL.md:184` says "not proven child death", and `docs/design/FLEET-EVAL-RED.md` carries the review. The agent framed per what forensics witnessed, exactly as promised |
| — | `fleet-eval.md:451` | "5. deepseek D2h 8/8 → 7/8 (child journals tombstone-only, no falsifier; soft, D2 verdict unchanged)." | MENTION | — | — | report about the deepseek CHILDREN's absent falsifiers (a scored check) |
| 14 | `fleet-eval.md:472-474` | "Falsifier that I'm NOT done: an unstruck overclaim or an uncited claim remains in FLEET-EVAL.md — I grep-checked; the only \"re-read journal\" hits are the D4 dimension-definition and the struck/corrected contexts. Clean." | (a) | a-independent | **NOT-FIRED** | Discharged in-entry by a grep over a **git-tracked deliverable**. I re-ran the check myself against `docs/design/FLEET-EVAL.md`: the corrections ARE in place — `:39-41` "deepseek D4 as 6/6 PASS and its D2 as 8/8; the adversarial review — §9 — showed …  Corrected here"; `:149` "D4 FAIL *(corrected from a pre-review 6/6 PASS — §9)*"; `:284` "This is why 'deepseek demonstrated a clean parent loop' is NOT claimed". Every one of eval-red's 5 objections is folded. VERIFIED |

### Counts — fleet-eval.md
MEASURED.
- MENTIONS (not statements): **8** (lines 30, 44, 93, 195–197, 275, 295–296, 451, plus the `:38` heading restatements folded in)
- STATEMENTS: **14**
  - (a)-independent: **13** · (a)-self-report: **1** · (b): **0** · (c): **0**
- OUTCOMES for (a) (all 14 are class (a)):
  - **FIRED-CHANGED: 3** · **FIRED-IGNORED: 0** · **NOT-FIRED: 11** · **CANNOT-TELL: 0**

---

# SLICE TOTALS (MEASURED)

| | v3-run-ds | v3-run-glm | fleet-eval | **TOTAL** |
|---|---|---|---|---|
| MENTIONS (not statements) | 10 | 8 | 8 | **26** |
| STATEMENTS | 9 | 12 | 14 | **35** |
| (a)-independent | 8 | 9 | 13 | **30** |
| (a)-self-report | 1 | 3 | 1 | **5** |
| (b) OBSERVABLE-ELSEWHERE | 0 | 0 | 0 | **0** |
| (c) UNFALSIFIABLE-AS-WRITTEN | 0 | 0 | 0 | **0** |
| FIRED-CHANGED | 1 | 1 | 3 | **5** |
| **FIRED-IGNORED** | **0** | **0** | **0** | **0** |
| NOT-FIRED | 8 | 11 | 11 | **30** |
| CANNOT-TELL | 0 | 0 | 0 | **0** |

---

## Notable

### FIRED-IGNORED: **ZERO.** I hunted for one and did not manufacture one.
I read all 1,614 lines of the three journals and opened the git-tracked artifacts they
name (`docs/audit/bench/results-v3-{deepseek,glm}.md`, `SCORING-AUDIT-V3.md`,
`docs/design/FLEET-EVAL.md`, `fleet-briefs-v{1,2,3}/`) plus the two surviving sandboxes.
**In this family, every falsifier that demonstrably fired produced a demonstrable course
change, and I could not find a single one where a disconfirming observation landed and
the agent walked past it.** That is the honest count. It is also, I suspect, a *family*
property and not a general one — see the caveat at the end.

### CANNOT-TELL: **ZERO.** This is the most surprising number in my slice.
The rubric predicted CANNOT-TELL would be "expected to be the largest bucket." In this
family it is **empty**. Every one of the 35 statements is settled — usually within one
or two entries, and often IN THE SAME ENTRY the falsifier is stated ("I looked in
$SANDBOX… ; b-d2c.md exists only in the former"). REASONED explanation: these three
agents are all in a **measure-then-score** loop where the falsifier's witness is *the
same artifact they are about to score*. Checking the falsifier and doing the job are the
same act. That is a structural reason the discipline held here that may not transfer to
design or coordination journals.

### The FIRED-CHANGED events, in full

**1. `v3-run-ds.md:380` → `:384` — the agent falsifies its OWN diagnosis and says so.**
At 15:12Z it concluded "helper-note can NEVER run … there is no herdr pane." It then set:
> "Falsifier/next action: determine why child-{s,r,c,t} ran to completion but helper-note
> sticks at `launching`. Until I can explain that difference, I do not understand my own
> rig and must not score D3b."

Eight minutes later, `:384`:
> "the contradiction is RESOLVED. I now understand my rig. **(My 15:12 diagnosis was
> WRONG — correcting it.)** … The falsifier I set … is what caught it."

The change is concrete and scored: HERDR_ENV=1 WAS set, both children got real panes,
the difference was `--cwd` (`:403-409`), and `swarm/settings/*.status` is a STALE FILE
that lies (`:398-401`). The scoring consequence at `:418-427` is rewritten. This is the
cleanest example in the slice of a falsifier doing the work it exists to do.

**2. `v3-run-glm.md:332` → `:360` — the benign limb fires and sharpens the reading.**
The falsifier's first limb ("if D3b/D4 land clean and fast, my 'watch D3b' framing was
over-cautious") fired. GLM finished D3b in ~2 min with no kill. The agent books the
over-caution AND upgrades its model of GLM's failure: `:384-387` "Its failure is not
'can't send' — it is **'forgets to send unless sending is the subject.'** A sharper
reading than 'drops the duty.'" Independently witnessed: `queue/v3-run-glm/1783866934562-b-d3b.json`
exists (MEASURED — I listed the directory).

**3. `fleet-eval.md:104` → `:134` — the operator answers, the caveat propagates to the deliverable.**
Falsifier: "if the operator wants only the clean baseline and no key is addable, the
Claude comparison is caveated-not-clean **and I say so in the reading**." The operator
chose the native-claude fallback. The promised change is inspectable today in a
git-tracked file: `docs/design/FLEET-EVAL.md:116` states the baseline "carries a
**plumbing caveat** (§5): it is a same-*battery* anchor, not a same-harness one," and
`:255` gives it a whole section (§5a, "caveat cuts both ways").

**4. `fleet-eval.md:155` → `:318` — the hang fires and is tagged, not verdicted.**
"if a runner's cell FLAGS or opencode hangs, that's a recorded [H]/FLAGGED result, NOT a
model verdict." GLM's D2-heavy hung. The agent recorded it and split the score by tag
(`:332-334`) rather than turning the hang into a blanket model failure — and the
[H]/[M] discipline survived all the way to the adversarial review, which further softened
"children died" to "empty-cwd, no watchdog" (`FLEET-EVAL.md:184`).

**5. `fleet-eval.md:356` → `:361` — the strongest firing, and its own later reversal.**
"if D3b's ONE child also dies … GLM's delegation is non-functional under opencode."
It fired: `:361` "D3b's single child ALSO died … Corroborates D2-heavy." The agent made
the stronger claim. **Then a reviewer falsified the firing itself** (`:422-424`: "'children
died on launch' is inference, not observation"), and the final deliverable walks it back
to "not proven child death" (`FLEET-EVAL.md:184`). A falsifier fired, the agent changed
course, and a *later* falsification reversed that change. The whole arc is legible in the
repo. This is the most interesting single thing in my slice.

### The near-miss that is NOT a FIRED-IGNORED — and why I refuse to score it as one

There IS a real, verdict-flipping error in this family, and it is tempting to book it as
a pathology. I will not, and here is the honest reasoning.

`docs/audit/bench/SCORING-AUDIT-V3.md` (auditor `v3red-score`) recomputed every v3 cell
from the per-check tables and found **deepseek's D2 verdict is wrong**: D2-cheap check 2
is [M]-hard and FAILS, so rubric §0 floors combined D2 at FAIL, but
`results-v3-deepseek.md:90` printed **"10/12 PARTIAL."** It also found the D2-heavy
"8/8" is arithmetically impossible (five printed rows; §2c defines at most seven checks;
the 8 is a fossil copied from v2's combined-D2 number). The errata is now applied at
`results-v3-deepseek.md:363-372`: *"Combined D2 is 8/10 FAIL, not 10/12 PARTIAL."*

So: a real error, found by an outsider, in `v3-run-ds`'s own deliverable.

**But it is not a FIRED-IGNORED, because v3-run-ds never set a falsifier that covers it.**
Its scoring-phase falsifier (`:203-206`) was: *"if any check I mark PASS rests only on a
transcript's SAY-SO and not on a file I opened."* That is a falsifier about **evidence
provenance**, and on its own terms it genuinely did not fire — every row in the results
file DOES name a file (I checked `results-v3-deepseek.md:82`, `:121`, `:182`, `:190`).
The error was in **derived arithmetic and rule-application**, a surface its falsifier
never pointed at. Its only arithmetic check (`:561`) covers D3 and D3 alone: *"D3 = 3a
7/8 + 3b 1/5 + 3c 3/4 = 11/17. Checks out."* — and that sum is correct.

**The finding is therefore not "a falsifier fired and was ignored." It is: THE FALSIFIER
WAS AIMED AT THE WRONG SURFACE.** v3-run-ds guarded the provenance of its evidence and
left the arithmetic that *derives verdicts from* that evidence unguarded — and that is
exactly where the error landed. If the parent's question is "do falsifiers actually
catch things," this is the sharpest datum in my slice: a well-disciplined agent, zero
ignored firings, and a verdict-flipping error that walked straight through the gap
between its falsifiers.

### The counter-case, and it is the strongest positive result here

`v3-run-glm.md:494-496` set exactly the falsifier v3-run-ds did not:
> "Falsifier for the corrected scores: **if field-tester recomputes from my per-check
> tables and gets different totals, my arithmetic is still wrong.** The tables are the
> witness; the totals are derived from them and now match."

**The recompute it invited actually happened**, run by an adversarial third party
(`v3red-score`) the agent could neither see nor influence. `SCORING-AUDIT-V3.md`'s §2
verdict table marks **every GLM row ✓** (D1 PASS ✓, D2 FAIL ✓, D3 PARTIAL ✓, D4 FAIL ✓)
and states: *"One verdict in the set does not follow from the rubric. It is deepseek's D2."*

GLM's runner had *already* self-corrected three dimensions at `:471-493` ("THREE of my
numbers were WRONG … D2-cheap 2/4 → 1/4, D2-heavy 8/8 → 6/6, D4 4/6 → 3/6") by
"mechanically recomputing every dimension against rubric §0 **instead of trusting my own
prose**." Its falsifier then held under hostile audit while its sibling's did not.

Two sibling runners, same rig, same brief. One wrote a falsifier that named the
arithmetic surface and survived an independent recompute; the other did not name it and
had a verdict flipped. **That is the closest thing to a controlled experiment on
falsifier value in this repo, and it fell out of the slice rather than being designed.**

---

## Reconciliation pairing (per journal)

MEASURED by reading every entry heading.

### v3-run-ds.md
- **Entries it calls a reconciliation: 2** — `:62` ("first reconcile: the §5a fix is
  confirmed live") and `:164` ("reconcile: the v3 falsifier is CLEARED"). *(A further
  ~6 entries do reconciliation WORK — scoring, correcting, self-verifying — without the
  word.)*
- **Of those, how many name a falsifier IN THE SAME ENTRY: 2 of 2 (100%).** `:62`'s
  entry ends at `:84-88` with the v3 pump falsifier; `:164`'s entry ends at `:203-206`
  with the new scoring-phase falsifier.
- **Names falsifiers then goes idle / never reconciles again: NO.** The final entry
  (`:547`, "self-verification of my OWN scoring, then reporting. Going idle after")
  explicitly discharges the standing falsifier before idling: `:563` "The falsifier did
  not fire." Every falsifier it set was returned to. **9 statements, 0 CANNOT-TELL.**

### v3-run-glm.md
- **Entries it calls a reconciliation: 1** — `:304` ("RECONCILE (halfway). D1/D2 done and
  scored; D3/D4 in flight"). *(Most of its 13 entries are per-probe scoring entries that
  each carry a falsifier anyway.)*
- **Of those, how many name a falsifier IN THE SAME ENTRY: 1 of 1 (100%).** `:332-334`.
- **Names falsifiers then goes idle / never reconciles again: NO — and it does the
  opposite.** Its final entry (`:498`, "REPORTED to field-tester. Going idle. (final
  entry)") sets a NEW falsifier on the way out (`:547-552`) — one that a third party
  then actually tested. **12 statements, 0 CANNOT-TELL.**

### fleet-eval.md
- **Entries it calls a reconciliation: 2 explicitly** — `:38` ("Falsifier for this
  reconcile") and `:55` ("TREE PLAN (reconcile)"). *(By behavior, most of its 20 entries
  are reconciliations: tree/span review + next-artifact naming + a falsifier.)*
- **Of those, how many name a falsifier IN THE SAME ENTRY: 2 of 2 (100%).** `:38-42` and
  `:64-66`.
- **Names falsifiers then goes idle / never reconciles again: NO.** Its final entry
  (`:458`, "DELIVERABLE COMPLETE") sets a done-condition falsifier (`:472-474`) and
  discharges it in the same breath by grepping the deliverable — which I independently
  re-checked against `docs/design/FLEET-EVAL.md`. **14 statements, 0 CANNOT-TELL.**

### The pairing result, stated plainly
**5 of 5 self-declared reconciliation entries across the three journals name a falsifier
in the same entry — 100%.** The doctrine's requirement is met in every instance I can
find. But this understates the practice: these agents attach falsifiers to *most* entries,
not only ones they label "reconcile," and they close them. The discipline here is not
ceremonial.

---

## Caveat on generalizing from this slice (REASONED)

My family is three journals whose *job* is empirical measurement against files. Their
falsifiers are cheap to check because the witness IS the artifact they were already going
to open. **I would not extrapolate my 0 FIRED-IGNORED / 0 CANNOT-TELL to design or
coordination journals**, where a falsifier's witness is often a future judgment, a live
pane, or an operator's opinion. The interesting comparison is with the other slices: if
they show CANNOT-TELL dominating, the finding is not "agents keep their falsifiers" but
**"falsifiers get kept exactly when the witness is a file the agent must open anyway"** —
and the actionable form of that is the near-miss above: *aim the falsifier at the surface
where the error will actually land.*
