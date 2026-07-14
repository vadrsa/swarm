# fp-slice-c — falsifier forensics, 4 journals

> SUPERSEDED by org-review-falsifier-2026-07-12.md; kept for the record (the MENTION-vs-STATEMENT distinction and the "delegation self-falsifiers are structurally un-auditable" finding).

Auditor: fp-slice-c. Rubric: docs/audit/_falsifier-rubric.md, followed exactly.
Journals read READ-ONLY, in full, end to end. No journal was modified.
Every file:line below is real and quoted verbatim (VERIFIED = I read the line;
MEASURED = I counted; REASONED = I inferred).

---

## A NOTE THAT GOVERNS THE FIRST TWO TABLES (dp-f1, dp-f2)

dp-f1 and dp-f2 were **hired to run experiments whose SUBJECT is a named
falsifier** (F1 = the coordinator-stance doctrine; F2 = mine-first). Their
journals therefore carry two populations that a careless count would merge:

- **EXPERIMENT-SUBJECT falsifier** — the agent reporting the verdict on the
  pre-registered falsifier it was PAID to measure ("falsifier 1 NOT-FIRED",
  "VERDICT RUN 3: **FIRED**"). Per the rubric's MENTION exclusion ("a name of a
  test", "a report ABOUT someone else's falsifier") **these are MENTIONS, not
  statements.** They are the deliverable, not the self-check.
- **SELF falsifier** — the agent naming, in its own reconciliation, the
  observation that would show **IT** is off track ("FALSIFIER for this reading:
  …", "Falsifier for MY OWN method: …"). **These are the STATEMENTS** the
  parent's question is about.

I count them in separate columns and never add them together. Both journals
score well on the *self* population — and that is the finding, not the
experiment verdicts, which belong to field-tester.

---

## dp-f1.md

### Statements table (SELF falsifiers only — the agent's own self-check)

| # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence |
|---|---|---|---|---|---|---|
| 1 | .swarm/journal/dp-f1.md:110 | "FALSIFIER for this reading: if run 2's pane shows the swarm skill loading and the observer using `swarm spawn`, then the trigger works at least sometimes and run 1 was a trigger miss rather than a trigger failure. If run 2 also never loads the skill, the finding is that an uncoached goal in a swarm repo does not reliably reach the doctrine at all." | (a) | a-independent | **FIRED-CHANGED** | firing: dp-f1.md:124-126 ("Zero .swarm/agents/*.json … swarm skill never loaded"); change: dp-f1.md:134-139, 151-154 |
| 2 | .swarm/journal/dp-f1.md:156 | "FALSIFIER for THIS conclusion: if someone re-runs with .swarm/ seeded in the clone (or an explicit \"start a swarm\" phrase) and the skill loads and the observer STILL keeps the human at one node, then the doctrine is separately validated and my \"unexercised\" claim is too strong. If it loads and flat-spawns 3 children under operator, falsifier 1 fires for real." | (a) | a-independent | **FIRED-CHANGED** | firing: dp-f1.md:184-193 (skill LOADED; "3 operator"; "**FIRED**"); change: dp-f1.md:256-266 |
| 3 | .swarm/journal/dp-f1.md:229 | "FALSIFIER for that mechanism claim: if run 4 fires but its journal/pane shows the observer KNOWINGLY leaving the human three children (i.e. no sincere \"you manage one node: me\" claim), then it is not a name collision but ordinary instruction-noncompliance, and my structural fix argument is too strong. If run 4 does NOT fire, then run 3 is a single sample and I must not generalize from n=1." | (a) | a-independent | **NOT-FIRED** | dp-f1.md:246-254 ("my run-3 mechanism falsifier RESOLVED, and it SURVIVED" — run 4 DID make the sincere claim: "Tree: three children under me.") |
| 4 | .swarm/journal/dp-f1.md:278 | "FALSIFIER for THAT recommendation: if someone renames the root session and observers STILL leave three children on the human's node, the collision was not the cause and I am wrong about the fix. That is the experiment I would run next." | (a) | a-independent | **CANNOT-TELL** | none — journal ends at :293. The naming experiment was never run by dp-f1. |

### The EXPERIMENT-SUBJECT population (MENTIONS, counted separately)

The pre-registered falsifier-1 (defined in the *task text*, dp-f1.md:44-48:
"FALSIFIED = >=3 agents with parent 'operator' AND no intermediate coordinator")
and every verdict on it. These are MENTIONS by the rubric — the agent is
reporting a measurement it was hired to make, not self-checking a reconciliation.
Verdict lines: :62 (run 1 NOT-FIRED), :118 (run 2 NOT-FIRED), :174/:188 (run 3
**FIRED**), :239/:243 (run 4 **FIRED**), :257-258 (the four-run summary).
Also :151 ("Falsifier 1 is therefore currently UNFALSIFIABLE BY THIS METHOD") —
a *meta-judgment about the experiment's falsifier*, still a MENTION not a self-check.

### Counts (MEASURED)
```
MENTIONS (not statements): 8      [:4 task text, :44 task-text FIRED-condition,
                                   :57-58 task text, :62, :98, :118, :131, :151,
                                   :160, :174, :188, :192, :239, :257-258 — grouped
                                   as 8 distinct mention-events: the task text (1),
                                   the falsifier-1 definition restated (1), and the
                                   6 verdict/summary reports]
STATEMENTS: 4   |  (a)-independent: 4   (a)-self-report: 0   (b): 0   (c): 0
OUTCOMES for (a) only: FIRED-CHANGED 2 | FIRED-IGNORED 0 | NOT-FIRED 1 | CANNOT-TELL 1
```

### Notable
- **FIRED-IGNORED: ZERO.** VERIFIED — I read every entry forward from each
  statement. Nothing was named, fired, and then walked past.
- **FIRED-CHANGED #1 (dp-f1.md:110 → :134).** The agent named a disjunctive
  falsifier and then *answered it in the very next entry against its own
  optimistic reading*. Quote of the firing + change, dp-f1.md:134-139:
  > "RECONCILIATION — my falsifier from the last entry RESOLVED, and it resolved
  > against the optimistic reading. I said: \"if run 2 shows the skill loading and
  > using swarm spawn, run 1 was a trigger miss; if run 2 also never loads the skill,
  > the finding is that an uncoached goal in a swarm repo does not reliably reach the
  > doctrine at all.\" Run 2 also never loaded the skill. So the finding stands: the
  > trigger, not the doctrine, is what these runs measure."
  The course change is explicit and costly to the agent: it declares its own
  assignment's falsifier "UNFALSIFIABLE BY THIS METHOD" (:151) and escalates the
  method problem to its parent rather than banking a clean NOT-FIRED (:161-162:
  "I am flagging that to field-tester as the decision they own, not silently
  re-running a protocol they specified"). This is the healthiest single instance
  in my slice.
- **FIRED-CHANGED #2 (dp-f1.md:156 → :184).** The falsifier said "if it loads and
  flat-spawns 3 children under operator, falsifier 1 fires for real." field-tester
  ordered exactly that re-run; dp-f1.md:188-193 records the independent witness:
  > "VERDICT RUN 3: **FIRED**. Collector, verbatim:
  >   3 operator
  > Full list: summarist <- operator ; testwright <- operator ; pathcheck <- operator."
  The agent then rewrote its own headline (dp-f1.md:264-266: "the trigger gap is now
  precisely scoped, which is better than my first report: NOT \"the skill never
  loads\" but \"goal-shape triggering fails; the explicit phrase works\"").
- **NOT-FIRED #3 is a *survived* falsifier, correctly labelled as such** (:246,
  "RESOLVED, and it SURVIVED") — the agent distinguishes "my falsifier did not
  fire" from "I was right," which is the distinction most agents blur.
- Every one of dp-f1's four self-falsifiers is **a-independent**: each names a
  file fact (agents/*.json parent counts, the collector output, the pane
  transcript, the skill md5) that a later reader can open, not a promise to write
  something down later. Zero a-self-report in this journal. (MEASURED)

### Reconciliation pairing
- Entries the journal calls a reconciliation: **2** (dp-f1.md:134 "RECONCILIATION
  — my falsifier from the last entry RESOLVED"; dp-f1.md:246 "RECONCILIATION — my
  run-3 mechanism falsifier RESOLVED"). It also carries a "Delegation review"
  at :167-171 and a teardown reconciliation at :282-290 that it does not label.
- Of those 2, how many name a falsifier IN THE SAME ENTRY: **2/2.** The :118 entry
  contains both the RECONCILIATION (:134) and a new falsifier (:156); the :239
  entry contains both the RECONCILIATION (:246) and a new falsifier (:278). VERIFIED.
- Does it name falsifiers and then go idle without reconciling? **Partly — yes, for
  the last one.** Statement #4 (:278) is named in the final entry and never
  returned to; the journal ends at :293 with "Deliverable: /tmp/dp-f1/findings.md,
  436 lines, runs 3/4 appended. Reporting." That is the CANNOT-TELL. It is the
  benign form: the falsifier names an experiment *for someone else to run next*,
  and the agent says so.

---

## dp-f2.md

### Statements table (SELF falsifiers only)

| # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence |
|---|---|---|---|---|---|---|
| 1 | .swarm/journal/dp-f2.md:98 | "Falsifier for MY OWN method: if the observer's phase-1 work is trivially short (one turn's worth, no real learning), then \"accrued context\" is a fiction and any mining verdict is unearned. I check phase 1 produced real artifacts + real surprises before scoring phase 2." | (a) | a-independent | **NOT-FIRED** | dp-f2.md:111-124 — phase 1 produced tools/queue-stats.py + 6 fixtures + 3 flagged judgment calls; ":124 This is exactly the accrued context the falsifier needs — the phase-1 momentum is genuine, not faked." |
| 2 | .swarm/journal/dp-f2.md:106 | "Falsifier for that call: if run 1 shows the per-run work is mostly mechanical collection, I spawn a collector for run 2." | (a) | a-self-report | **NOT-FIRED** | dp-f2.md:181-185 ("Run 1 proved the per-run work is NOT mechanical — the mtime trap would have flipped the verdict, and catching it took live judgment mid-run") and again at :229-235 |
| 3 | .swarm/journal/dp-f2.md:140 | "Falsifier for this reading: if turn-2's transcript shows the observer answering \"add the test\" (i.e. the text WAS submitted at some point), my artifact diagnosis is wrong and the run is contaminated — I would kill and re-run." | (a) | a-independent | **NOT-FIRED** | REASONED-from-silence + positive evidence: the run proceeded to a full verdict (:144-175) with a clean phase-2 timeline, and the agent never reports contamination. The probe that settled it is quoted at :135-137 (`pane send-text ZZPROBE` → box read exactly "❯ ZZPROBE"). |
| 4 | .swarm/journal/dp-f2.md:184 | "Falsifier for continuing solo: if run 2 needs no judgment calls, I was wrong and should have parallelized." | (a) | a-self-report | **NOT-FIRED** | dp-f2.md:229-235 ("DELEGATION, final reconciliation: … I said in my first entry that if run 1 proved mechanical I was wrong to stay solo. It did not.") |
| 5 | .swarm/journal/dp-f2.md:213 | "FALSIFIER FOR MY OWN VERDICT (what would show me wrong): if someone re-scores these two runs from mtime alone they will get FIRED, because operator.md is APPENDED to and its mtime drifts LATER than the first spawn (run 1: journal mtime 19:10:49 vs first agent 19:01:23 — a 566s inversion). My NOT-FIRED rests on three non-mtime proofs … If all three of those were somehow wrong, the verdict flips." | (a) | a-independent | **CANNOT-TELL** | none — this is the final entry (journal ends :238). It names the trap and pre-empts it in the deliverable (:220-221) but the counterfactual re-score never happens in this journal. |

### The EXPERIMENT-SUBJECT population (MENTIONS, counted separately)
Falsifier 2 as defined in the *task text* (dp-f2.md:52-56: "FALSIFIED = spawns with
no prior journal decomposition, OR the first brief ignores the accrued context") and
its verdicts: :144 (RUN 1: NOT-FIRED), :175, :187 (RUN 2: NOT-FIRED), :200
("VERDICT: falsifier 2 NOT-FIRED, n=2"). Plus :86-90, a report on **dp-f1's**
falsifier 1 — explicitly a report about someone else's falsifier, the rubric's
canonical MENTION. Plus :158 and :197, noting that *the observer under test* wrote
a falsifier of its own — a report about a third party's falsifier.

### Counts (MEASURED)
```
MENTIONS (not statements): 8      [:4 task text, :52-56 falsifier-2 definition,
                                   :62 task text, :67 heading restatement,
                                   :86-90 report on dp-f1's falsifier,
                                   :144/:175 run-1 verdict, :158+:197 reports on the
                                   OBSERVER's own falsifier, :187/:200 run-2 verdict]
STATEMENTS: 5   |  (a)-independent: 3   (a)-self-report: 2   (b): 0   (c): 0
OUTCOMES for (a) only: FIRED-CHANGED 0 | FIRED-IGNORED 0 | NOT-FIRED 4 | CANNOT-TELL 1
```

### Notable
- **FIRED-IGNORED: ZERO.** VERIFIED.
- **FIRED-CHANGED: ZERO** in this journal — every self-falsifier it named was
  checked and *discharged*, not fired. That is a real outcome, not a gap: dp-f2
  names four falsifiers and explicitly returns to all four with an affirmative
  "did not happen." (:124, :181-185, :229-235.)
- **The two a-self-report statements are both DELEGATION falsifiers** (#2 at :106,
  #4 at :184) — "if the work turns out mechanical, I was wrong to stay solo." Their
  only possible witness is the agent's own later prose about whether the work
  *felt* mechanical. There is no mtime, no queue file, no artifact that settles
  "was this judgment or was this collection." The agent discharged both honestly
  and with a *specific* reason (the mtime trap it caught mid-run), but a reader
  cannot independently check the discharge. **This is the a-self-report shape the
  rubric asks me to be strict about, and it is worth the parent's attention:
  delegation self-falsifiers are structurally un-auditable.** (REASONED)
- **The strongest a-independent falsifier in my whole slice is dp-f2.md:213** — the
  agent names the exact way a *future auditor* would wrongly overturn its verdict
  (mtime on an appended file drifts later than the first spawn; 566s inversion) and
  pre-registers the three non-mtime proofs its verdict actually rests on. That is a
  falsifier aimed at the reader, not at the agent, and it is checkable from files.
  It is CANNOT-TELL only because the journal ends before anyone tries.

### Reconciliation pairing
- Entries the journal calls a reconciliation: **3** — :181 ("Reconciliation: still
  not delegating"), :229 ("DELEGATION, final reconciliation"), and :144's verdict
  entry does *not* self-label. Counting only self-labelled: 2 explicit + the
  orientation entry at :104-107 ("DELEGATION CALL") which functions as one.
  **MEASURED: 2 self-labelled "reconciliation" entries.**
- Of those 2, how many name a falsifier IN THE SAME ENTRY: **2/2.** :181's entry
  carries :184's falsifier; :229's entry sits in the same entry as :213's falsifier
  (both under the 19:35Z heading). VERIFIED.
- Does it name falsifiers and then go idle without reconciling? **Yes, once, and it
  says so.** :213 is named in the final entry and the journal then closes (:236
  "Going idle after reporting."). That is statement #5 = CANNOT-TELL. Every earlier
  falsifier was discharged before idle.

---

## opencode-plugin-scout.md

### Statements table

| # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence |
|---|---|---|---|---|---|---|
| 1 | .swarm/journal/opencode-plugin-scout.md:41 | "FALSIFIER for my current framing: if oc-probe's BANANA control FAILS — no hook can put text in front of the model on a turn — then the operator's \"edit the harness loop\" hypothesis is dead as stated, the plugin is event-hooks-only … and I must pivot the recommendation to FLEET's leaf path" | (a) | a-independent | **NOT-FIRED** | :109-131 — the scout ran the control itself: ":131 It answered **BANANA-7734**"; and :299-328 the probe plugin fired the hooks and the model answered PELICAN-9 + MANATEE-5. |
| 2 | .swarm/journal/opencode-plugin-scout.md:46 | "Second falsifier: if oc-priorart finds the SDK/server can push a message into a live session, then the PLUGIN is not the interesting surface at all — the SERVER is — and my deliverable should recommend that instead." | (a) | a-independent | **FIRED-CHANGED** | firing: :126-131 (the scout itself proved the server pushes into a live session) + :370-382 (oc-priorart converges on "the server is the harness"); change: :189-211 the design splits DELIVERY(plugin)/DOORBELL(server), and finally :475-492 delivery moves entirely onto the server route. |
| 3 | .swarm/journal/opencode-plugin-scout.md:104 | "FALSIFIER for THIS entry: oc-probe finds that `experimental.chat.messages.transform` never fires under `opencode run`, or that its mutation is dropped (types lie / hook is dead code) — then delivery falls back to whatever DOES fire, and if nothing injects, the pivot in my previous entry stands." | (a) | a-independent | **NOT-FIRED** | :316-328 — the scout's own probe log: "[messages.transform] FIRED, messages 1 -> 2 after my push" and the model returned MANATEE-5. Hook fires; mutation reaches the model. |
| 4 | .swarm/journal/opencode-plugin-scout.md:163 | "FALSIFIER for this entry: if the same injection fails against a session that is MID-TURN (busy) — i.e. noReply only works on an idle session — then delivery needs queueing/backpressure and the story gets more complicated." | (a) | a-independent | **NOT-FIRED** | :608-615 (oc-probe F1, harvested): "**THE SERVER SERIALIZES.** A noReply POST during ACTIVE GENERATION returns HTTP 200 in ~8ms, non-blocking, stored immediately, running turn untouched — and it LANDS". Also pre-answered at :301-302. |
| 5 | .swarm/journal/opencode-plugin-scout.md:166 | "Second falsifier: if a long-running `opencode run`/TUI agent does NOT expose its server (only `serve` does), the whole external path only works for a serve-hosted agent — I believe --port on the TUI refutes this but I have NOT yet run the TUI with --port and POSTed to it." | (a) | a-independent | **FIRED-CHANGED** (partially fired) | firing: :242-245 "`opencode run --port ...` is REJECTED … `run` is a ONE-SHOT CLIENT, not a server. My 16:52 entry implied otherwise; that was wrong." change: the launch line becomes the TUI (:250-254), and later :635-637 "A full-participant agent wants the PERSISTENT (TUI or serve) model, not `run`." The *TUI* half did NOT fire (:246-254 VERIFIED it serves). |
| 6 | .swarm/journal/opencode-plugin-scout.md:230 | "FALSIFIER for this entry: if oc-probe's F2 shows a TUI/`opencode run` agent does NOT expose a server on a pinned port, the doorbell half collapses and swarm must run opencode agents as `opencode serve` + `opencode attach` for the pane — a real cost I would have to write up honestly rather than gloss." | (a) | a-independent | **NOT-FIRED** | :250-254 (scout's own run: TUI on port 47333, `GET /global/health` healthy) and independently :625-630 (oc-probe F2: "the INTERACTIVE TUI under a PTY exposes its server on a pinned port (--port 47399)"). ":264 So F2 is REFUTED-as-a-risk in the good direction." |
| 7 | .swarm/journal/opencode-plugin-scout.md:292 | "FALSIFIER still open (oc-probe owns it, F1): injection into a BUSY (mid-turn) session. If a noReply POST mid-turn errors or is dropped, `swarm send` to a busy opencode agent needs retry/backpressure — a real cost I must write up. Nothing I have seen suggests it fails, but I have not run it." | (a) | a-independent | **NOT-FIRED** | :608-615 (oc-probe's F1 result, harvested by the scout: server serializes, POST lands). Duplicate-in-substance of #4 but re-registered in a new entry, so counted as its own statement per "one entry may carry one falsifier statement." |
| 8 | .swarm/journal/opencode-plugin-scout.md:362 | "FALSIFIER for this entry: the injection worked on a `run` (fresh session, 1 message). If `messages.transform` behaves differently on a LONG session — e.g. our pushed message gets dropped by compaction, or duplicated every turn because the hook fires on EVERY turn … — the plugin needs idempotency keyed on message id. I SAW that double-fire in hooks.log." | (a) | a-independent | **FIRED-CHANGED** | firing: :364-368 the double-fire is *observed in the agent's own hooks.log* ("it fired TWICE in my log — once per model call"); change: :414-419 promotes it to "**THIS IS THE #1 IMPLEMENTATION HAZARD**" and puts the idempotency guard in the design. |
| 9 | .swarm/journal/opencode-plugin-scout.md:429 | "FALSIFIER for option (c): if messages.transform's injected message does NOT persist into the session's stored history (i.e. it is a per-call transform that the model sees but the session never records), then a message delivered on turn N is INVISIBLE on turn N+1 — the agent would \"forget\" its mail. My run cannot distinguish these. THIS MUST BE TESTED before (c) is recommended without caveat." | (a) | a-independent | **FIRED-CHANGED** | **THE HEADLINE.** firing: :435-448 — "## MY OWN FALSIFIER FIRED. `messages.transform` is a VIEW transform, not a session write. Option (c) is DEAD as stated." / ":447 MODEL ANSWERS: **UNKNOWN**." change: :475-492 delivery is rebuilt on the documented server route; :514-548 the new pump is built and run. |
| 10 | .swarm/journal/opencode-plugin-scout.md:736 | "FALSIFIER for this entry: if oc-red's lab reproduces messages.transform and finds the message DOES persist across turns, §2.2 is wrong, the pump is unnecessary, and delivery could ride the hook directly. I would have to rewrite §3." | (a) | a-independent | **CANNOT-TELL** | none — journal ends at :770 with ":765-768 "Waiting on oc-red's adversarial verdict (it has ocr-lab re-running my key experiments…)". The verdict never lands in this journal. |

### Counts (MEASURED)
```
MENTIONS (not statements): 6   [:4 task text ("falsifiers", "graveyard-check");
                                :225 naming oc-probe's F1/F2/F3 as test names;
                                :236 "it is the falsifier that could have collapsed…"
                                     (referring back to #5, a report on it);
                                :301 report on oc-priorart answering "my F1 falsifier";
                                :640 "oc-probe's falsifiers" (a report about a child's);
                                :685 "I will NOT retract the falsifier list — F1/F2/F3/F5
                                     stand as written" (a report ABOUT the doc's list)]
STATEMENTS: 10  |  (a)-independent: 10   (a)-self-report: 0   (b): 0   (c): 0
OUTCOMES for (a) only: FIRED-CHANGED 4 | FIRED-IGNORED 0 | NOT-FIRED 5 | CANNOT-TELL 1
```

### Notable
- **FIRED-IGNORED: ZERO.** VERIFIED. I read all 770 lines forward from each of the
  ten statements. Every one that fired produced a *recorded design change within
  one or two entries*.
- **FIRED-CHANGED #9 is the cleanest instance of the doctrine working in my entire
  slice, and it is worth quoting at length.** The agent named the falsifier at
  18:05 (:429), tested it *immediately because it was load-bearing*, and it fired
  against the agent's own preferred design. opencode-plugin-scout.md:435-438:
  > "## 2026-07-12 18:20Z — MY OWN FALSIFIER FIRED. `messages.transform` is a VIEW
  > transform, not a session write. Option (c) is DEAD as stated.
  > I named the falsifier at 18:05 and immediately tested it, because it was cheap
  > and it was load-bearing. IT FIRED. This is the most important NEGATIVE result of
  > the whole investigation and it corrects MY OWN preferred design, not a child's."
  The firing is an independent witness (a model's answer in a sandbox run,
  :445-448: "MODEL ANSWERS: **UNKNOWN**"), and the course change is total — the
  delivery mechanism is torn out and rebuilt on the documented server route
  (:475-492), then *actually built and run* (:514-548, "THE PUMP IS PROVEN").
  Note also the honesty at :462-468: "THIS VINDICATES MY CHILD'S ARCHITECTURE,
  THOUGH NOT ITS REASONING. … I was wrong at 18:05 to think I had dissolved its
  dilemma; the dilemma is real and I have to answer it, not dodge it."
- **FIRED-CHANGED #5 (:166 → :242) is a falsifier that fired against a claim the
  agent had made in a *previous entry*, and the agent says so in plain terms**
  (:244-245: "My 16:52 entry implied otherwise; that was wrong"). Half the
  disjunction fired (`run` does not serve) and half did not (the TUI does), and the
  agent scored each half separately rather than calling the whole thing discharged.
- **FIRED-CHANGED #8 (:362 → :414)** — the double-fire hazard. Notable because the
  firing evidence is *the agent's own hooks.log*, which it read rather than assumed
  ("I SAW that double-fire in hooks.log", :368) and which it then escalated to the
  design's #1 hazard instead of quietly filing.
- **Zero a-self-report.** Every falsifier this scout wrote names an artifact, a run,
  a probe log, a child's deliverable, or a source file — never "if I later feel I
  was wrong." (MEASURED)
- The single CANNOT-TELL (#10, :736) is *pending on a live child at the moment the
  journal stops*, and the agent explicitly refuses to report until it lands (:768-770:
  "I will not report to the operator until I have that verdict — the brief requires
  adversarial review BEFORE reporting, and a red team that has not reported is not a
  red team."). That is the *good* form of CANNOT-TELL: an open falsifier with a named
  owner and a stated blocking condition.

### Reconciliation pairing
- Entries the journal calls a reconciliation: **3** self-labelled — :94
  ("RECONCILIATION: the tree still matches the work, but the CENTER OF GRAVITY
  MOVED"), :223 ("RECONCILIATION / span: 3 children…"), and the tree/span
  reconciliations at :422 ("TREE/SPAN:") and :573 ("TREE:") and :643 ("TREE
  DECISION:") which do the same job under a different word. **MEASURED: 3 using the
  word "RECONCILIATION", 6 doing the job.**
- Of those, how many name a falsifier IN THE SAME ENTRY: **3/3 for the
  word-labelled ones** — :94's entry carries :104; :223's entry carries :230; :422's
  TREE/SPAN entry carries :429. VERIFIED. Of the six span/tree-check entries, :573
  ("TREE: oc-api and oc-probe are still live but have produced NO artifact") and :643
  ("TREE DECISION: all three children are HARVESTED") carry **no falsifier in the
  same entry** — those are the two that miss the doctrine's requirement.
- Does it name falsifiers and then go idle without reconciling? **No — it does not go
  idle.** The journal's last entry (:740-770) is a state entry that explicitly holds
  open one falsifier (#10) awaiting a live red team. The agent is blocked, not idle.

---

## operator-structure-scout.md

### Statements table

| # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence |
|---|---|---|---|---|---|---|
| 1 | .swarm/journal/operator-structure-scout.md:24 | "Falsifier for my read: if `bin/swarm` gives the root session a distinct node of its own (not `operator`), then \"in place\" is representable and the collision is my invention. Checking that in code, not from memory." | (a) | a-independent | **NOT-FIRED** | :35-40 — "bin/swarm:64 `def my_name(): return os.environ.get(\"SWARM_AGENT_ID\") or \"operator\"` … ls .swarm/agents/operator.json -> NO SUCH FILE." The root session has no node; the collision is real. |
| 2 | .swarm/journal/operator-structure-scout.md:54 | "Falsifier of THIS claim: if structure-mech finds any way a root session spawns a child with parent != operator (a --parent flag, an env var it can set itself), then in-place IS representable and I am wrong. Awaiting that." | (a) | a-independent | **NOT-FIRED** | :63-65 — "my_name() = SWARM_AGENT_ID or \"operator\" (bin/swarm:64); parent = my_name() (bin/swarm:869). A root session CANNOT write any parent but \"operator\"." Confirmed by structure-mech + the agent's own code read. |
| 3 | .swarm/journal/operator-structure-scout.md:97 | "FALSIFIER for this reconcile: if structure-mech's diff turns out to need context it doesn't have (herdr/pane/env plumbing beyond bin/swarm), then re-dispatching it was wrong and I should have spawned a fresh reader with a wider brief." | (a) | a-independent | **NOT-FIRED** | :103-112 — structure-mech delivered docs/design/OPERATOR-STRUCTURE-FIX.md (32KB) with a working diff; and :219-234 shows mech ran the *herdr-pane* test correctly (the wider context) — it had what it needed. |
| 4 | .swarm/journal/operator-structure-scout.md:156 | "FALSIFIER of this recommendation: if the operator says the confirm's value is onboarding-pedagogical (teaching a NEW user what a top layer IS), not shape-enforcement, then decay doesn't matter — a rite that teaches on first use has done its job before it rots. That is a real argument and only the operator can make it." | (b) | — | — | (b): the witness is the human operator's stated reasoning, which arrives by mail and is not itself a repo file. In fact the operator's reply (:328-344) overturned the whole frame and never addressed this — so it is moot, not discharged. |
| 5 | .swarm/journal/operator-structure-scout.md:213 | "FALSIFIER of THIS entry: if the end-to-end run passed only because my fake herdr reported the root's pane as live, and a REAL herdr does not list the root session's pane in `herdr pane list`, then root-1 renders dead in the real world and the flat row returns in the view. THIS IS THE ONE THING MY RIG CANNOT PROVE — my fake herdr was WRITTEN BY ME to include w9:pROOT. MUST BE CHECKED AGAINST REAL HERDR." | (a) | a-independent | **NOT-FIRED** | :219-234 — structure-mech ran the real test ("created a pane the way a HUMAN does (herdr tab create, NO --env, no swarm) -> HERDR_PANE_ID present, injected BY HERDR ITSELF") and the scout re-verified independently (":230 the human's own root pane w4:p1 (focused:true) IS in live_pane_set() (22 panes)"). ":232 CONCLUSION HOLDS, now on VALID evidence." |
| 6 | .swarm/journal/operator-structure-scout.md:269 | "FALSIFIER of this reconcile: if red2 returns a KILL on the structural fix, the tree was wrong to have three children polishing a fix and only one attacking it." | (a) | a-independent | **FIRED-CHANGED** | firing: :272-293 — "the fresh review earned its keep: a KILL nobody else found … **A2 — KILLS IT**". The scout's own falsifier condition ("if red2 returns a KILL") is met verbatim. change: the ship list is rewritten (:321-322: "SHIP LIST IS NOW 9 HUNKS, 3 OF THEM REVIEW-FORCED AND MANDATORY") and the tree is re-shaped (:406-407: "Spawning structure-red3 (new name…)"). |
| 7 | .swarm/journal/operator-structure-scout.md:323 | "FALSIFIER of this entry: if red2-doctrine's pending verdict shows the doctrine half is redundant EVEN GIVEN the open mailbox (e.g. it argues the mailbox flood is self-limiting), then F' does not rescue the doctrine and I should cut it after all. Waiting on that before I report." | (a) | a-independent | **CANNOT-TELL** | none — the next entry (:328) is the operator's MAJOR REFRAME, which overturns the frame the falsifier lived in. The journal never returns to red2-doctrine's verdict. (docs/audit/red2-doctrine-2026-07-12.md exists in the repo but the *journal* never settles it.) |
| 8 | .swarm/journal/operator-structure-scout.md:374 | "FALSIFIER of this lean: if `swarm ps`/`send` already work outside herdr and only `spawn` is gated, then the gate is defensible (you cannot make a pane without herdr) and the answer really is DOCTRINE-ONLY, tool untouched." | (a) | a-independent | **FIRED-CHANGED** | firing: :378-386 — "MEASURED: the answer is DOCTRINE-ONLY. … `env -u HERDR_ENV -u SWARM_AGENT_ID swarm ps` -> WORKS … `swarm spawn zzz-probe` -> \"not inside herdr\"". change: :391-393 "=> NO TOOL CHANGE IS NEEDED. The falsifier I pre-registered for my own lean did not fire in the direction of a tool change; it fired toward DOCTRINE-ONLY." (An *inverted* falsifier — see Notable.) |
| 9 | .swarm/journal/operator-structure-scout.md:446 | "FALSIFIER for the rewrite: if red3 shows the operator's real load is NOT governed by spawn_header (e.g. agents routinely mail the human despite it, in the existing record), then doctrine-only fails on the mailbox and a tool change IS needed after all. That is checkable TODAY against queue/operator/delivered/ — 60+ real messages. CHECKING IT." | (a) | a-independent | **NOT-FIRED** | :451-464 — "## MY OWN FALSIFIER DID NOT FIRE. … RAN IT against the REAL record — all 60 messages in .swarm/queue/operator/delivered/ … depth 1: 60 messages / depth >=2: 0 messages <-- ZERO". |

### Counts (MEASURED)
```
MENTIONS (not statements): 5   [:4 task text ("a file-fact falsifier collected by the
                                herdr root-session rig");
                                :7 "F1 FIRED 2/2, F2 NOT-FIRED" (report on field-tester's);
                                :48 "That is why F1 fired 2/2" (report on someone else's);
                                :108 "Its OWN falsifier is pre-registered and executable"
                                     (report ABOUT structure-mech's falsifier);
                                :179+:192 "THEN I RAN THE PRE-REGISTERED FALSIFIER (F-FIX)"
                                     — running a CHILD's pre-registered falsifier, i.e. a
                                     report on someone else's, not a self-check]
STATEMENTS: 9   |  (a)-independent: 8   (a)-self-report: 0   (b): 1   (c): 0
OUTCOMES for (a) only: FIRED-CHANGED 2 | FIRED-IGNORED 0 | NOT-FIRED 5 | CANNOT-TELL 1
```
(The one (b) — statement #4, :156 — is excluded from the (a) outcome tally per the rubric.)

### Notable
- **FIRED-IGNORED: ZERO.** VERIFIED across all 535 lines.
- **FIRED-CHANGED #6 (:269 → :272) is a falsifier about the agent's own TREE SHAPE,
  and it fired.** The condition was "if red2 returns a KILL on the structural fix,
  the tree was wrong to have three children polishing a fix and only one attacking
  it." red2 returned exactly that KILL (:274-293, the A2 relation() finding: "THE
  HUMAN LOSES THEIR VOICE"). The agent accepted the verdict on its own delegation
  (:292-293: "NONE of the first three reviewers caught this. Nor did I. This is why
  the fresh review is mandatory and why it must be a NEW name, not a re-dispatch to
  red.") and changed the tree. This is the only falsifier in my slice aimed at the
  agent's **delegation** that has an **independent witness** (red2's artifact,
  docs/design/OPERATOR-STRUCTURE-RED2.md) rather than the agent's own prose — and it
  is the contrast case to dp-f2's two a-self-report delegation falsifiers.
- **FIRED-CHANGED #8 (:374 → :378) is an INVERTED falsifier and I want the parent to
  see the shape.** It is written so that firing *confirms* the agent's lean
  ("if ps/send already work outside herdr … the answer really is DOCTRINE-ONLY").
  The agent then ran it and reported (:391-392): "The falsifier I pre-registered for
  my own lean did not fire in the direction of a tool change; it fired toward
  DOCTRINE-ONLY." **This is a falsifier that cannot disconfirm the agent** — whichever
  branch obtains, the agent's design survives (either doctrine-only, or a
  tool change it had already flagged as the exception). I score it FIRED-CHANGED
  because the observation demonstrably occurred and was measured against the live
  tool, and it did close a design question. But its *form* is weak: it is a decision
  procedure dressed as a falsifier. (REASONED — this is my judgment of form, not a
  claim about the agent's honesty; the agent's measurement at :380-386 is real and
  reproducible.)
- **The single (b) — statement #4, :156** — "if the operator says the confirm's value
  is onboarding-pedagogical…". The witness is the human's stated reasoning. It is
  genuinely checkable *in principle* (the operator could say so) but the repo records
  no such statement. What actually happened is more interesting: the operator's reply
  (:328-344) **reframed the entire model** and never engaged this question at all, so
  the falsifier was not discharged — it was made moot by a change of premise. Worth
  the parent's note: *a (b)-class falsifier that depends on the human answering a
  specific question is at the mercy of the human answering a different one.*
- **The largest self-correction in my slice is at :328-344 and it is NOT a falsifier
  firing** — it is the operator overturning the model by mail ("MAJOR REFRAME from the
  operator. My structural fix is RETRACTED"). The agent had *no* falsifier registered
  that would have caught this (its falsifiers were all aimed at the mechanics of the
  fix, which were correct; the fix was retracted because the *premise* changed). The
  agent says so honestly at :348-351: "I spent the day proving `operator` was the wrong
  name for the root session. The operator says the name is RIGHT … That is a cleaner
  cut and I did not see it." **REASONED finding for the parent: falsifiers were dense,
  well-formed, and file-observable here, and the thing that actually killed the day's
  central artifact was invisible to every one of them.** That is not a pathology — it
  is a limit on what a falsifier can do.
- **Zero a-self-report.** Every (a) statement names code, a run, a queue directory, or
  a child's artifact. (MEASURED)

### Reconciliation pairing
- Entries the journal calls a reconciliation: **3** self-labelled ("RECONCILE" at :59;
  "FALSIFIER for this reconcile" at :97 implies the :59 entry; "TREE/SPAN CHECK" at
  :263; "FALSIFIER of this reconcile" at :269). Counting entries that do the job
  (tree/span check + falsifier): :59, :263, plus the TREE lines at :406, :442, :534.
  **MEASURED: 2 entries using the word "reconcile"/"RECONCILE" (:59, :263 via :269),
  5 entries doing a tree/span check.**
- Of those, how many name a falsifier IN THE SAME ENTRY: **2/2 for the word-labelled
  ones** (:59's entry carries :97; :263's entry carries :269). VERIFIED. Of the
  5 tree/span entries, :534 ("TREE: closing structure-red3 (harvested). All children
  closed; span = 0.") is the final entry and carries **no falsifier** — but it is also
  the terminal entry, where there is no next step to be off-track about.
- Does it name falsifiers and then go idle without reconciling? **One does not get
  settled: #7 (:323, red2-doctrine's pending verdict)** — the operator's reframe
  arrived in the next entry and the question was abandoned rather than answered. The
  journal does not acknowledge dropping it. That is the closest thing to a loose end
  in this journal, and it is a *dropped* falsifier, not an *ignored fired* one: there
  is no evidence in the journal that it fired.

---

# SLICE TOTALS (MEASURED)

| journal | MENTIONS | STATEMENTS | a-indep | a-self | (b) | (c) | F-CHANGED | **F-IGNORED** | NOT-FIRED | CANNOT-TELL |
|---|---|---|---|---|---|---|---|---|---|---|
| dp-f1 | 8 | 4 | 4 | 0 | 0 | 0 | 2 | **0** | 1 | 1 |
| dp-f2 | 8 | 5 | 3 | 2 | 0 | 0 | 0 | **0** | 4 | 1 |
| opencode-plugin-scout | 6 | 10 | 10 | 0 | 0 | 0 | 4 | **0** | 5 | 1 |
| operator-structure-scout | 5 | 9 | 8 | 0 | 1 | 0 | 2 | **0** | 5 | 1 |
| **TOTAL** | **27** | **28** | **25** | **2** | **1** | **0** | **8** | **0** | **15** | **4** |

Note: dp-f1's and dp-f2's MENTION counts are dominated by **experiment-subject
falsifier reporting** — 6 of dp-f1's 8 and 5 of dp-f2's 8 are verdicts on the
falsifier those agents were HIRED to test (F1 / F2). Those are their deliverable,
not their self-check. **Do not read "dp-f1 mentions falsifiers 8 times" as
"dp-f1 self-checks 8 times." It self-checks 4 times.** This is the distinction the
parent asked me to protect and it materially changes the numbers.

## The headline findings

1. **FIRED-IGNORED = 0 across all four journals, 28 statements.** I hunted forward
   through every (a)-class statement to the end of each journal. Nothing was named,
   observed to fire, and then walked past. **I did not manufacture a pathology and
   there was none to find here.** (VERIFIED / MEASURED)

2. **8 FIRED-CHANGED out of 27 (a)-class statements.** Falsifiers in this slice are
   not decorative: when they fired, the agent recorded the firing *and* rewrote the
   design. The strongest is opencode-plugin-scout.md:429 → :435 ("MY OWN FALSIFIER
   FIRED … Option (c) is DEAD as stated"), where a scout tested a load-bearing
   falsifier against its own preferred architecture within one entry and tore the
   architecture out.

3. **(c)-class = ZERO.** Not one vague or tautological falsifier in 28. Every
   statement named a concrete observation. (MEASURED)

4. **a-self-report = 2 of 27, and BOTH are DELEGATION falsifiers** (dp-f2.md:106 and
   :184 — "if the work turns out mechanical, I was wrong to stay solo"). This is the
   one structural weakness the slice reveals: **falsifiers about the agent's own
   delegation decision have no independent witness.** No mtime, no queue file, no
   artifact can settle "was this judgment or was this collection." Contrast
   operator-structure-scout.md:269, which is *also* a delegation falsifier but is
   a-independent because it outsourced the verdict to a fresh red team whose artifact
   is in the repo — and it FIRED, and the agent changed the tree. **The lesson the
   data supports: a delegation falsifier is only auditable if its judge is somebody
   else.** (REASONED, from a 2-vs-1 sample — weak but directionally clean.)

5. **CANNOT-TELL = 4, and every single one is the LAST falsifier in its journal.**
   Not a scattering of abandoned checks — each journal names a falsifier in its final
   entry and stops. Three of the four say what they are waiting on (dp-f1:278 "That is
   the experiment I would run next"; opencode-plugin-scout:736 "I will not report until
   I have that verdict"; dp-f2:213 pre-empts the trap in the deliverable). The one
   genuinely dropped falsifier is operator-structure-scout.md:323 (red2-doctrine's
   pending verdict), abandoned when the operator's reframe changed the premise under it.

6. **One falsifier is INVERTED and cannot disconfirm its author**
   (operator-structure-scout.md:374): whichever branch obtains, the design survives.
   The agent measured it honestly and against the live tool, so the *evidence* is
   sound — but the *form* is a decision procedure wearing a falsifier's clothes.
   Worth the parent's eye as a shape to name, not as misconduct.

7. **A limit worth reporting: the day's biggest retraction was invisible to every
   falsifier that could have caught it.** operator-structure-scout wrote 8
   well-formed, file-observable falsifiers and none of them fired; the artifact was
   nonetheless retracted (:328-344, :395-403) because the *operator changed the
   premise*. Falsifiers guard the mechanics you chose to test; they do not guard the
   frame. (REASONED)
