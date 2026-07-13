# FLEET-EVAL-V3 — the clean-rig rerun (operator-ordered)

**Author:** `field-tester`, synthesizing three runner cells (`v3-run-ds`,
`v3-run-glm`, `v3-run-cb`). **Written at** `main@1e254e4`, 2026-07-12. **Status:**
RUN — executed, verified, adversarially reviewed (§8). Predecessor:
`docs/design/FLEET-EVAL.md` (v2); this run applies v2's own §5a/§5b/§5c/§5e
recommendations and re-measures. Same battery shape, same rubric
(`fleet-rubric-v1.md`), briefs `fleet-briefs-v3/` = v2 + ONE changed file
(`d2-heavy.md`; MANIFEST md5-pinned), so rows are v2-comparable except where a fix
changed what is *witnessable* — every such case is called out.

**Evidence discipline:** every score was written by a runner who opened the cited
artifact, and the load-bearing claims below were re-checked by me against the
results files (`docs/audit/bench/results-v3-{deepseek,glm,claude-base}.md`) and
spot-checked against sandboxes. VERIFIED / MEASURED / REASONED tags as in v2.

---

## 1. Bottom line

| Model | D1 duties | D2 delegation | D3 tool/CLI | D4 long-horizon | v3 reading |
|---|---|---|---|---|---|
| **deepseek-chat** | 5/5 PASS | 8/10 FAIL (cheap 2/4 FAIL · heavy 6/6 PASS)* | 11/17 FAIL | 3/6 FAIL† | parent-capable, leaf-duty-weak, does not time-box |
| **GLM-4.7** | 5/5 PASS | 7/10 FAIL (cheap 1/4 FAIL · heavy 6/6 PASS) | 14/17 PARTIAL | 3/6 FAIL† | strong parent execution, excellent tool-user, weak duty-keeper, **no watchdog** |
| **claude-native** (anchor) | 5/5 PASS | 10/10 PASS (cheap 4/4 · heavy 6/6) | 17/17 PASS | 6/6 PASS | clean sweep — 37/37 [M] + 1 check won on plumbing (D3b.2); same-harness caveat REMAINS |

\* Corrected per adversarial review (§8, OBJ-1/OBJ-2): the pre-review draft scored
deepseek's D2 10/12 PARTIAL while GLM's identical hard-check failure scored FAIL, and
copied a v2 number into the heavy slot. Corrected, **deepseek and GLM are LEVEL on
D2**: both FAIL via the cheap probe's hard check, both sweep the heavy probe's
applicable checks. Errata block appended to `results-v3-deepseek.md`.

† D4 for both Chinese cells is confounded in MAGNITUDE by the MCP escape hatch
(§4.2) — read as "at most this bad" — but the Claude control (§4.2) shows the
confound is not the whole story.

**Cost (operator's cap $5):** deepseek **$0.0457** metered + GLM **$0.2273**
token-derived (opencode meters zai at $0; FLEET §6 rates) = **$0.273 billed**, ≈5%
of cap. The native cell rides the Claude pool and is **unmetered** — ~400–600k
tokens REASONED, and that estimate is honestly unfalsifiable as run (v4 fix:
`--output-format stream-json` and sum usage). The two figures are not comparable.

---

## 2. What v3 changed, and what each fix bought (the caveats-resolved ledger)

| v2 caveat | v3 fix | outcome |
|---|---|---|
| **§5a** runner unregistered — report-to-parent structurally unwitnessable, scored [H]-excused | runner + every probe REGISTERED as sandbox agents; delivery via `deliver-next.py` (imports `bin/swarm`; injection byte-identical to the hook's — smoke-verified) | **RESOLVED.** Report-to-parent is now a real [M] check in all cells. It immediately produced signal: deepseek dropped 4/7, GLM dropped-or-misrouted 4/7, Claude 7/7. v2's "PASS-but-excused" rows retired. |
| **§5b** cwd management conflated with delegation competence | `d2-heavy.md` hands `--cwd {REPO}` uniformly | **RESOLVED — and it voids v2's GLM headline** (§4.1). Delegation is now scored on weigh/brief/verify/close only. |
| **§5c** M2 relation check asymmetric (hand-injected for one model, penalized for the other) | relation header rig-delivered via `bin/swarm`'s own `relation()` in opencode cells; native hook in the anchor; scored uniformly | **RESOLVED.** Both Chinese cells now PASS M2 legitimately (`echo-2.md` = "your parent", pre-verified against `relation()` by both runners independently). |
| **§5d** broken session-id extractor | sed capture fix | **RESOLVED** (no `--continue` fallbacks fired). |
| **§5e** live-tree bleed unverified | SWARM_DIR PATH shim + before/after live-journal snapshots per cell | **PARTIALLY RESOLVED — and it found a deeper leak** (§4.3): the shim provably contained everything that goes *through* swarm (live `agents/` byte-identical in all cells), but child journals are ordinary file writes and leaked in ALL THREE cells. §5b's fix *causes* this leak. v4 needs absolute journal paths in briefs. |
| **§5a-baseline** no same-harness Claude cell | none (no OpenRouter key provided) | **REMAINS.** The anchor is same-battery, not same-harness; a Claude-vs-Chinese gap still confounds model with harness. Cite the anchor row only with this header. |

---

## 3. Per-model corrected readings

### 3a. deepseek-chat — parent-capable; leaf-duty-weak; does not time-box

- The **parent loop is witnessed, with one honest asterisk the review sharpened.**
  It spawned 4 children `--cwd {REPO}`; the children's reports were queued to the
  model-agent's name and injected into its later turns (witnessed by the
  TRANSCRIPTS — the injected turns and the model's message-triggered replies). The
  `delivered/` directory in the opencode cells is moved by the RIG's pump, not by
  swarm's own emit-gated hook, so it is a rig log, not swarm's evidentiary record
  (disclosed; v4: the pump must not write `delivered/`). Verification was checked
  against the children's actual files (runner opened them); all four closed;
  report-up landed; M2 relation PASS. Second asterisk, volunteered by both opencode
  runners and initially filtered out of this synthesis (review OBJ-4): the parent
  verified-and-closed inside turn 1's own harvest loop, BEFORE the pumped
  deliveries — the delivered turns were *confirmations*, not first-contact
  verification. Real and file-based, but not delivery-triggered. Only the native
  anchor verified as reports arrived.
- **Leaf duties are the weakness the clean rig exposed:** 4/7 report-to-parent
  drops — it *narrates* the report as turn text instead of sending it ("it knows
  who its parent is and does not use the verb"). D2-cheap regressed vs v2 on a
  byte-identical brief: no spawn/no-spawn weighing journaled at all (v2 had a
  priced decline) — n=1 variance on the doctrine surface, see §4.4.
- **New [M] finding:** when its D3b child stalled (an [H] rig gap — that brief
  hands no cwd), deepseek **abandoned the brief and spent 11 min debugging the
  harness** (read spawn internals, simulated arg-insertion, spawned a test tab)
  without returning to its remaining steps. It was killed by the runner
  (disclosed; no winnable check lost). deepseek does not time-box a blocked
  dependency — directly relevant to unattended parent placement.
- D4 3/6: never wrote the journal; **used `bridgememory_append_to_memory`
  instead** (§4.2) and recovered from the deliverable on restart.

### 3b. GLM-4.7 — v2's headline VOIDED; strong parent execution; no watchdog; weak duty-keeper

- **v2's "children all died, model hung 35 min, fragile parent" does NOT
  reproduce and is retired.** It was the rig's empty cwd. In v3: 4/4 children ran
  real audits, GLM **verified each report against the child's actual output file**
  (runner re-derived: 52 tests OK, same broken refs deepseek's child found, raw
  timing samples), closed all 4, reported up. D2-heavy 6/6 — the strongest
  non-Claude delegation execution in either run.
- **The half that SURVIVES v2:** no watchdog. Its harvest loop is blind
  sleep-escalation (`sleep 5/15/30` + `swarm ps`); it terminated only because its
  children delivered. Dead children would hang it again. Unattended-parent risk.
- **Tool-user: excellent.** Every swarm command all battery long was well-formed
  (D3b 4/5 in ~2 min — sharp contrast with deepseek's tunnel). M2 PASS.
- **Duty-keeper: weak, with a new precise shape:** it reports when the brief is
  about coordination/CLI (D1, D2-heavy, D3b landed) and forgets when the brief is
  file-mechanics-dominated (D2-cheap, D3a). It will not use the journal for what
  the journal is *for*: D4's plan went into the deliverable; on restart it went
  looking for the journal it never wrote (`find -name b-d4.md`). Two of its report
  failures were **misrouted through MCP/socket doors** (§4.2), not skipped.
- Tic on the record: it consistently misreports its own word/line counts;
  everything scored from files.

### 3c. claude-native — the anchor: 38/38, with its header

Clean sweep; receive→verify is the strongest in the set (idled on the queue and
verified as reports arrived across turns — used swarm's mechanism rather than a
harvest loop). Genuine kill-and-restore D4. **Runner's own deductions kept:** D3b
ch2 is won partly on plumbing; two rig-unblocks disclosed and excluded from [M];
the same-harness caveat REMAINS (§2). Its D2-cheap **flipped vs v2**
(declined→delegated on a byte-identical brief) — logged as a rubric gap, §4.4.

---

## 4. Cross-cutting findings (the v4 agenda)

1. **v2's between-model delegation story was a rig artifact in both directions.**
   deepseek's v2 was inflated (unwitnessable duties scored as absence-of-failure);
   GLM's v2 was deflated (rig-killed children scored as model fragility). §5a+§5b
   turned both into honest observations. **No v2 GLM D2 row should be cited
   again;** deepseek v2 rows need the v3 correction alongside.
2. **The MCP escape hatch — bench defect AND model fact.** Probes inherit the
   operator's MCP servers. deepseek **attempted** to journal into `bridgememory` —
   the call ERRORED and it never noticed, so it journaled *nowhere* (corrected per
   review OBJ-6: an MCP-off v4 would NOT recover its D4 journal check); GLM tried
   `bridgemind_send_agent_message` (404) and `nc -U` to a nonexistent socket
   instead of `swarm send`. The **Claude control had the same doors open and took
   them 0 times in 7 probes** (verified by the reviewer from session logs:
   pendingMcpServers loaded, 0 `mcp__` calls of 7–19 tool calls per probe). So:
   confounded in magnitude for some checks, not in kind (choosing substitution is
   the model's). **v4: run probes with MCP disabled.**
3. **§5b and §5e are structurally in tension — proven in all three cells.**
   Children given `--cwd {REPO}` write their relative `.swarm/journal/<name>.md`
   into the LIVE tree (9 files leaked in the native cell — including via D2-cheap,
   which the d2-heavy-only brief fix cannot reach; 3–4 in each opencode cell). The
   SWARM_DIR shim contained every *swarm* operation (evidence scoped per review
   OBJ-5: the byte-identical live-`agents/` snapshot exists for the native cell;
   the opencode cells witness containment via their live-journal before/after
   diffs) but a journal write never touches swarm. All leaks were preserved into
   sandboxes (`leaked-*journals/`; the native and GLM runners recorded
   verification, the md5 logs live in their journals/sandboxes where recorded) and
   the live tree restored to its before-snapshot, verified by diff in every cell.
   **v4: briefs name an ABSOLUTE sandbox journal path.**
4. **The D2-cheap weighing is unstable run-to-run and the rubric cannot see it.**
   On byte-identical briefs: v2-Claude declined / v3-Claude delegated;
   v2-deepseek priced a decline / v3-deepseek wrote no weighing at all. n=1 per
   run cannot distinguish principled context-sensitivity from noise. **v4 rubric
   gap: a stability probe (same cheap brief ×3) is needed before any D2-cheap row
   is treated as a model property.**
5. **Smaller rig traps, all confirmed:** `swarm/settings/*.status` stays
   `launching` forever (a liveness trap that misled a probe); the pane-less
   registered runner reads as `dead` in `swarm ps`, so four native probes sent
   correct reports and then *despaired* incorrectly (scored from files); zai is
   unpriced in opencode's meter (cost must be token-derived); native claude is
   unmetered entirely.
6. **Concurrency caveat, on the record:** doctrine-probe observer sessions (a
   separate operator task) ran on this machine during parts of the GLM cell
   window. Timing-flavored artifacts (D2-heavy report-4) are load-sensitive in
   absolute terms; no rubric check scores absolute latency, so no verdict is
   affected — but v4 should serialize evals machine-wide if absolute numbers ever
   start being scored.

---

## 5. The corrected placement READING (not a policy — the operator decides)

- **Both Chinese models are now demonstrated parents at the execution level:**
  each spawned real children, harvested real reports, verified against real
  files, and closed cleanly — under a rig that can no longer be fooled by
  unwitnessable duties. The v2 asymmetry between them (deepseek-parent vs
  GLM-leaf) **does not survive the clean rig**; what separates them now is
  *failure-mode shape*, not competence: deepseek tunnels on blocked dependencies
  (no time-box), GLM busy-waits with no watchdog. **Neither is safe as an
  unattended parent; both are usable as attended parents or leaves.**
- **Both share the same two leaf-duty gaps:** report-to-parent is unreliable
  (narrated or misrouted instead of sent — the verb exists, the habit doesn't),
  and the journal is not used as continuity (plans live in deliverables; D4
  restarts recover from artifacts, not journals). If placed anywhere, their spawn
  headers need the report and journal duties stated *imperatively*, and even that
  is unproven at n=1.
- **Claude remains the only model in the set that passed every duty through the
  real machinery** — with the standing caveat that its cell ran a different
  harness, so cross-model magnitude comparisons carry the §5a header.
- Everything here is n=1 per cell per dimension: shapes, not rates. Rates need
  dated re-runs (the rubric's design). The v4 agenda (§4) is what would make a
  next run decisive: MCP-off, absolute journal paths, metered native cell,
  weighing-stability probe.

---

## 6. Artifacts

- Per-cell results (full per-check tables): `docs/audit/bench/results-v3-deepseek.md`,
  `results-v3-glm.md`, `results-v3-claude-base.md`.
- Rig: `run-cell-v3.sh`, `fleet-briefs-v3/` (MANIFEST md5-pinned; one file changed
  vs v2), `v3-helpers/{register-agent.py,deliver-next.py}`.
- Sandboxes with transcripts, queues, preserved leak files:
  `scratchpad/bench-v3/{deepseek,glm,claude-base}/`.
- Runner journals: `.swarm/journal/v3-run-{ds,glm,cb}.md`.

## 7. Spend vs cap

$0.273 billed (metered + token-derived) against the $5 cap; native cell unmetered
(Claude pool), ~400–600k tokens REASONED. The cost falsifier (>2× estimate)
fires on the cheap side only; estimates for both Chinese cells can be lowered.

## 8. Adversarial review (done — and it changed this document)

Fresh reviewer `v3-red` (did not run the eval) stress-tested the synthesis against
the primary artifacts: **10 objections, 6 cleared claims** — full report
`docs/design/FLEET-EVAL-V3-RED.md`. Verdict: *"the direction holds; two numbers do
not; one of your strongest sentences is backwards."* Everything below is folded in
above; the load-bearing corrections:

1. **[flipped a verdict] deepseek D2 10/12 PARTIAL → 8/10 FAIL** (OBJ-1/OBJ-2):
   the identical hard-check failure that FAILed GLM was scored PARTIAL for
   deepseek, on a denominator no other cell used, with a v2 number copied into the
   heavy slot. **This is eval-red's v2 finding recurring one dimension over, in the
   same direction** — cell arithmetic is not cross-checked between cells and drifts
   kind-to-deepseek. Errata appended to `results-v3-deepseek.md`; §1 corrected;
   **deepseek and GLM are LEVEL on D2.**
2. **[reversed a claim] "crossed the real queue / side-channel gone" was backwards**
   (OBJ-3): the rig's pump moves files into `delivered/` itself, ungated by the
   emit that makes the real hook's record evidentiary — exactly what WORLD.md's
   queue sentence warns about. Injection is witnessed by transcripts; `delivered/`
   in opencode cells is a rig log. Corrected in §3a; v4 item added.
3. **[one-way filter] the runners' own verify-in-harvest-loop caveat** (OBJ-4) was
   volunteered by both opencode runners and had been dropped from the synthesis;
   restored (§3a). Only the native anchor verified on receipt.
4. **[evidence scoping] md5/byte-identical containment claims** were one cell's
   evidence claimed for three (OBJ-5); scoped (§4.3). **38/38** included a check the
   cb runner itself called plumbing-won (OBJ-9); restated as 37/37+1. deepseek
   "journaled into bridgememory" was in fact an unnoticed ERROR — it journaled
   nowhere (OBJ-6); corrected (§4.2), and it cuts against the MCP-off hedge.
5. **Cleared under hostile reading:** the MCP control (§4.2 — reviewer verified 0
   `mcp__` calls across 9 native sessions from session logs), the voided GLM
   headline (§4.1), the D2-cheap instability finding (§4.4), D3b's [H] tagging,
   and the file-based verification itself.

The reviewer's meta-finding stands on the record: **where the pre-review synthesis
was kind, it was kind to the rig its author built.** The v4 agenda (§4) gains three
review items: the pump must not write `delivered/`; check 5 must distinguish
verify-on-receipt from verify-then-confirm; native cells must capture tool-call
logs so controls are witnessable in-cell.
