# Measured Results Table: FLEET-EVAL-V3.md and FLEET-EVAL.md

| Model | Dimension | Score/Finding | Which Doc | File:Line |
|---|---|---|---|---|
| deepseek-chat | D1 duties | 5/5 PASS | FLEET-EVAL-V3 | 23 |
| deepseek-chat | D2 delegation | 8/10 FAIL (cheap 2/4 FAIL · heavy 6/6 PASS) | FLEET-EVAL-V3 | 23 |
| deepseek-chat | D3 tool/CLI | 11/17 FAIL | FLEET-EVAL-V3 | 23 |
| deepseek-chat | D4 long-horizon | 3/6 FAIL | FLEET-EVAL-V3 | 23 |
| deepseek-chat | D1 duties | 5/5 PASS | FLEET-EVAL | 34 |
| deepseek-chat | D2 delegation | 7/8 PASS — spawned real children, ran & closed them | FLEET-EVAL | 34 |
| deepseek-chat | D3 tool/CLI | 13/16 PARTIAL | FLEET-EVAL | 34 |
| deepseek-chat | D4 long-horizon | FAIL (no plan journaled) | FLEET-EVAL | 34 |
| GLM-4.7 | D1 duties | 5/5 PASS | FLEET-EVAL-V3 | 24 |
| GLM-4.7 | D2 delegation | 7/10 FAIL (cheap 1/4 FAIL · heavy 6/6 PASS) | FLEET-EVAL-V3 | 24 |
| GLM-4.7 | D3 tool/CLI | 14/17 PARTIAL | FLEET-EVAL-V3 | 24 |
| GLM-4.7 | D4 long-horizon | 3/6 FAIL | FLEET-EVAL-V3 | 24 |
| GLM-4.7 | D1 duties | 4/5 PARTIAL | FLEET-EVAL | 35 |
| GLM-4.7 | D2 delegation | judgment sound; execution failed (empty-cwd spawn + no watchdog → hang) | FLEET-EVAL | 35 |
| GLM-4.7 | D3 tool/CLI | 11/17 PARTIAL | FLEET-EVAL | 35 |
| GLM-4.7 | D4 long-horizon | 4/6 FAIL | FLEET-EVAL | 35 |
| claude-native | D1 duties | 5/5 PASS | FLEET-EVAL-V3 | 25 |
| claude-native | D2 delegation | 10/10 PASS (cheap 4/4 · heavy 6/6) | FLEET-EVAL-V3 | 25 |
| claude-native | D3 tool/CLI | 17/17 PASS | FLEET-EVAL-V3 | 25 |
| claude-native | D4 long-horizon | 6/6 PASS | FLEET-EVAL-V3 | 25 |
| claude-native | D1 duties | 5/5 PASS | FLEET-EVAL | 36 |
| claude-native | D2 delegation | 8/8 PASS (declined, solo) | FLEET-EVAL | 36 |
| claude-native | D3 tool/CLI | 17/17 PASS | FLEET-EVAL | 36 |
| claude-native | D4 long-horizon | 6/6 PASS | FLEET-EVAL | 36 |
| deepseek-chat | caveat: time-boxing behavior | does not time-box a blocked dependency | FLEET-EVAL-V3 | 85-86 |
| deepseek-chat | caveat: D3b brief gap | when its D3b child stalled (an [H] rig gap — that brief hands no cwd), deepseek abandoned the brief and spent 11 min debugging the harness | FLEET-EVAL-V3 | 84-86 |
| deepseek-chat | caveat: D4 journal duty | never wrote the journal; used `bridgememory_append_to_memory` instead and recovered from the deliverable on restart | FLEET-EVAL-V3 | 87-88 |
| GLM-4.7 | caveat: watchdog absence | no watchdog. Its harvest loop is blind sleep-escalation (`sleep 5/15/30` + `swarm ps`); it terminated only because its children delivered. Dead children would hang it again. | FLEET-EVAL-V3 | 98-100 |
| GLM-4.7 | caveat: duty-keeper weakness | weak duty-keeper: it reports when the brief is about coordination/CLI (D1, D2-heavy, D3b landed) and forgets when the brief is file-mechanics-dominated (D2-cheap, D3a). | FLEET-EVAL-V3 | 103-105 |
| GLM-4.7 | caveat: journal recovery | it will not use the journal for what the journal is *for*: D4's plan went into the deliverable; on restart it went looking for the journal it never wrote | FLEET-EVAL-V3 | 105-108 |
| GLM-4.7 | caveat: MCP report routing | Two of its report failures were misrouted through MCP/socket doors, not skipped | FLEET-EVAL-V3 | 108-109 |
| claude-native | caveat: D2-cheap flip | D2-cheap flipped vs v2 (declined→delegated on a byte-identical brief) | FLEET-EVAL-V3 | 119 |
| deepseek-chat | caveat: leaf-duty weakness | Leaf duties are the weakness the clean rig exposed: 4/7 report-to-parent drops — it narrates the report as turn text instead of sending it | FLEET-EVAL-V3 | 76-80 |
| deepseek-chat | caveat: D4 hard-check | never wrote the journal; plan was in the deliverable, exactly like GLM, which was FAILed for it | FLEET-EVAL-V3 | 149-157 |
| deepseek-chat | caveat: parent loop verification | parent verified by a file-existence read, not a recompute | FLEET-EVAL-V3 | 73-75 |
| deepseek-chat | caveat: report delivery routing | children reported to `operator`, not to the parent; there is no real queue/b-d2h/ | FLEET-EVAL-V3 | 68-70 |
| deepseek-chat | caveat: v2-v3 change in witnessable parent loop | parent verified-and-closed inside turn 1's own harvest loop, BEFORE the pumped deliveries — the delivered turns were confirmations, not first-contact verification. Only the native anchor verified as reports arrived. | FLEET-EVAL-V3 | 72-75 |
| GLM-4.7 | caveat: children empty-cwd issue | children spawned into an empty cwd (a parent cwd-management gap) with the same claude launcher as deepseek's working children | FLEET-EVAL-V3 | 144 |
| GLM-4.7 | caveat: parent cwd-management | spawned children without managing their cwd (so they had nothing to do) and had no watchdog to notice the silence | FLEET-EVAL-V3 | 204-205 |
| deepseek-chat | caveat: D2-cheap regression | D2-cheap regressed vs v2 on a byte-identical brief: no spawn/no-spawn weighing journaled at all | FLEET-EVAL-V3 | 79-80 |
| deepseek-chat | caveat: opencode runner verification method | parent "verified" by a file-existence read (re-stating each report's headline number), not a report received through swarm nor a recomputation | FLEET-EVAL | 54-58 |
| deepseek-chat | caveat: narrow parent story | parent story is narrower than a clean loop: children reported via a filesystem side-channel, not swarm delivery; verify was a file read, not a recompute | FLEET-EVAL | 163-169 |
| deepseek-chat | caveat: journal duty skip | skips the journal duty a restart-surviving parent depends on (D4 FAIL) — the same duty GLM skips | FLEET-EVAL | 167-169 |
| deepseek-chat | caveat: D2-heavy swept checks | Four real reports + `swarm close` ×4; the weighing varies with task size | FLEET-EVAL | 138-140 |
| deepseek-chat | caveat: parent loop not witnessed cleanly | parent never received a child report through swarm (children went to `operator`; parent did a file-existence read, not a recompute) | FLEET-EVAL | 52-58 |
| deepseek-chat | caveat: child-journal falsifier check | child-journal falsifier check is a soft FAIL (tombstone-only child journals) | FLEET-EVAL | 140-144 |
| deepseek-chat | caveat: pre-review D4 error | pre-review draft scored deepseek D4 as 6/6 PASS; deepseek never journaled its plan and its D2 as 8/8 | FLEET-EVAL | 38-41 |
| GLM-4.7 | caveat: children produced nothing | children produced nothing: GLM ran bare `swarm spawn stability` (no cwd management), so its children inherited cwd = the empty sandbox with nothing to audit | FLEET-EVAL | 178-180 |
| GLM-4.7 | caveat: empty-cwd vs deepseek | GLM ran bare `swarm spawn stability` (no cwd management), so its children inherited cwd = the empty sandbox with nothing to audit, whereas deepseek prepended `cd /Users/vadrsa/git/swarm` | FLEET-EVAL | 63-69 |
| GLM-4.7 | caveat: hang behavior | GLM misread `swarm ps` liveness, re-spawned 4 retries, and hung with no watchdog | FLEET-EVAL | 181-183 |
| GLM-4.7 | caveat: D2-cheap journal | D2-cheap FAILs on a different axis: GLM wrote no journal at all for it, so the no-spawn weighing is unwitnessed | FLEET-EVAL | 184-187 |
| GLM-4.7 | caveat: D4 journal absence | never journaled its plan (hard-check fail), and on restart it reached for its journal and found nothing there | FLEET-EVAL | 192-198 |
| GLM-4.7 | caveat: coherence behavior strength | coherence behavior is genuinely strong (held the catalog across a real session drop, resisted the distractor, recovered from `catalog.md`) | FLEET-EVAL | 192-198 |
| GLM-4.7 | caveat: tied with deepseek on journal duty | both skip it (neither journaled its D4 plan; both recovered from the deliverable on restart) | FLEET-EVAL | 207-212 |
| GLM-4.7 | caveat: broader journaling gaps | skipped journals on most probes, sinking D2-cheap and D4 on hard checks | FLEET-EVAL | 210-212 |
| GLM-4.7 | caveat: broadened journal gap | GLM and deepseek are tied on the journal duty; GLM's weaker read comes from the delegation-execution failure plus the wider journaling gaps | FLEET-EVAL | 207-212 |
| GLM-4.7 | caveat: pre-review cwd-management attribution | rig's empty cwd caused the failure, not proven child death | FLEET-EVAL | 62-69 |
| deepseek-chat | caveat: harness asymmetry note | deepseek's v2 was inflated (unwitnessable duties scored as absence-of-failure) | FLEET-EVAL-V3 | 125-126 |
| GLM-4.7 | caveat: v2 between-model rig artifact | GLM's v2 was deflated (rig-killed children scored as model fragility) | FLEET-EVAL-V3 | 125-126 |
| claude-native | caveat: same-harness constraint | anchor is same-battery, not same-harness; a Claude-vs-Chinese gap still confounds model with harness. Cite the anchor row only with this header. | FLEET-EVAL-V3 | 54 |
| deepseek-chat | caveat: MCP escape hatch use | attempted to journal into `bridgememory` — the call ERRORED and it never noticed, so it journaled nowhere | FLEET-EVAL-V3 | 131-132 |
| GLM-4.7 | caveat: MCP escape hatch use | tried `bridgemind_send_agent_message` (404) and `nc -U` to a nonexistent socket instead of `swarm send` | FLEET-EVAL-V3 | 133-134 |
| claude-native | caveat: MCP escape hatch absence | had the same doors open and took them 0 times in 7 probes | FLEET-EVAL-V3 | 136-137 |
| deepseek-chat | caveat: v2-baseline comparison caveat | deepseek v2 rows need the v3 correction alongside when cited | FLEET-EVAL-V3 | 129 |
| deepseek-chat | caveat: v3 reader deepseek D4 error correction | deepseek D4 was mis-scored 6/6 PASS; deepseek has no `b-d4.md` — its plan was in the deliverable, exactly like GLM, which was FAILed for it | FLEET-EVAL | 434-439 |
| deepseek-chat | caveat: journal plan crossing restart | plan was in the deliverable, exactly like GLM, which was FAILed for it | FLEET-EVAL | 434-439 |
| deepseek-chat | caveat: M2 relation asymmetry | `echo-2.md` = "your parent" only because the runner hand-injected the relation into the delivered prompt; should not credit deepseek while the same dropped check penalizes GLM | FLEET-EVAL | 291-296 |
| GLM-4.7 | caveat: children same launcher | same claude launcher as deepseek's working children | FLEET-EVAL | 66 |
| deepseek-chat | caveat: D3 report-to-parent harness limitation | 3 misses are all report-to-parent, 2 of them a harness fact, 1 a genuine [M] skip | FLEET-EVAL | 145-148 |
| deepseek-chat | caveat: parent loop report-to-parent structural limitation | children reported to `operator`, not to the parent; there is no `queue/b-d2h/` | FLEET-EVAL | 52-58 |
| GLM-4.7 | caveat: D3 child output absence | child **also** produced no `child-out.md` — corroborating the empty-cwd pattern | FLEET-EVAL | 188-192 |
| deepseek-chat | caveat: cwd management parenting competence | gave its children a working directory and GLM did not | FLEET-EVAL | 63-75 |
| GLM-4.7 | caveat: parenting failure root cause | delegation-execution failure and its broader journaling gaps; not on a journal-duty gap unique to it | FLEET-EVAL | 209-212 |
| deepseek-chat | caveat: report-to-parent narration skip | narrates the report as turn text instead of sending it ("it knows who its parent is and does not use the verb") | FLEET-EVAL-V3 | 76-80 |
| GLM-4.7 | caveat: MCP door socket attempt | tried `nc -U` to a nonexistent socket instead of `swarm send` | FLEET-EVAL-V3 | 133-135 |
| claude-native | caveat: plumbing advantage for relation check | Two checks the opencode cells structurally cannot witness PASS here because the native rig exercises swarm's real machinery: the M2 relation-header and a real `restore`-hook restart for D4 | FLEET-EVAL | 225-228 |
| claude-native | caveat: decline decision | declined the heavy delegation and did it solo (rubric-correct at that deterministic scale) | FLEET-EVAL | 221-224 |
| deepseek-chat | caveat: D2-cheap no journaling output | no spawn/no-spawn weighing journaled at all (v2 had a priced decline) | FLEET-EVAL-V3 | 79-80 |
| GLM-4.7 | caveat: D2-cheap 8 tombstones absence | D2-cheap: GLM wrote no journal at all for it; 8 tombstones, 0 reports | FLEET-EVAL | 184-187 |
| deepseek-chat | caveat: pre-review D2 arithmetic | pre-review draft scored deepseek's D2 10/12 PARTIAL while GLM's identical hard-check failure scored FAIL | FLEET-EVAL-V3 | 27-29 |
| deepseek-chat | caveat: D2 heavy slot copy | copied a v2 number into the heavy slot | FLEET-EVAL-V3 | 27-31 |
| deepseek-chat | caveat: errata appendance | Errata block appended to `results-v3-deepseek.md` | FLEET-EVAL-V3 | 31 |
| deepseek-chat | caveat: test case sampling | 50 real `run-NN` output files from a child session; real `perf_counter` numbers | FLEET-EVAL | 48-51 |
| GLM-4.7 | caveat: empty sandbox cwd limitation | children inherited cwd = the empty sandbox with nothing to audit | FLEET-EVAL | 63-69 |
| deepseek-chat | caveat: child task context | gave its children a real cwd | FLEET-EVAL | 64-75 |
| claude-native | caveat: baseline comparability | a same-*battery* anchor, not a same-*harness* one | FLEET-EVAL | 114-117 |
| deepseek-chat | caveat: operator placement | placement direction survived the review; deepseek is a parent candidate | FLEET-EVAL | 383-386 |
