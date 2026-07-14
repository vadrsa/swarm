# Mining the fleet-eval record for a model-fit rule

> SUPERSEDED by docs/design/MODEL-FIT.md (merged, PR #83); kept for the record (§7's numbered findings with citation trail, including a corrected error 7e not otherwise documented).

**Agent:** `eval-miner` · **For:** `model-fit` · **Date:** 2026-07-13
**Question asked:** this repo already ran the experiment — what actually happens when a weaker model sits in a swarm seat?

Everything in §§1–7 carries a cite. §8 is my inference and is fenced off. Where the record is silent I say **NOT IN RECORD** rather than guess.

---

## 0. THE HEADLINE CAVEAT — read this before anything else

**The record is rich, and it answers a different question than the one you asked.**

The fleet eval put **GLM-4.7** and **DeepSeek-chat** into swarm seats against a **native-Claude anchor**. It never tested Opus vs Sonnet vs Haiku vs Fable. There is no Claude-tier ladder anywhere in it.

> `docs/design/FLEET-EVAL-V3.md:54` — "**§5a-baseline** no same-harness Claude cell | none (no OpenRouter key provided) | **REMAINS.** The anchor is same-battery, not same-harness; a Claude-vs-Chinese gap still confounds model with harness."

The intended Claude comparator was *Haiku* and it was never keyed:

> `.swarm/journal/battery-smith.md:32` — "Preferred baseline = **openrouter/anthropic/claude-haiku-4.5** IF keyed; fallback = native `claude` cell WITH the plumbing caveat"

So: the record tells you **what degrades first when a seat is held by a weaker model**. It does **not** tell you where Haiku 4.5 or Sonnet 5 sit on that curve. Anyone transferring these findings to a Claude tier is extrapolating, and should say so out loud.

**Also: the whole eval is n=1.**
> `docs/design/FLEET-EVAL-V3.md:193-195` — "**Everything here is n=1 per cell per dimension: shapes, not rates.**"

**And v2's numbers are void.** Only v3 survives.
> `.swarm/journal/v3-run-glm.md:527-529` — "a rig that can't witness a duty INFLATES (deepseek v2); a rig that breaks the children DEFLATES (GLM v2). **Neither v2 GLM row should be cited again.**"

---

## 1. What was actually run

**Three cells, seven probes, frozen briefs** (`docs/audit/bench/fleet-briefs-v3/`, MD5-pinned):

| cell | model | harness |
|---|---|---|
| deepseek | `deepseek/deepseek-chat` | `opencode run` (`run-cell-v3.sh:88-89`) |
| GLM | `zai-coding-plan/glm-4.7` | `opencode run` |
| anchor | native `claude` (tier unspecified) | real `swarm spawn` panes — **a different harness** |

Four dimensions (`docs/design/FLEET-EVAL.md:90-100`):
- **D1 duties** — journal before idle, falsifier-bearing reconcile, report to parent. *"Can it be a node at all."*
- **D2 delegation as a parent** — real `swarm spawn` ability on a decomposable task. *"The parent-vs-leaf discriminator."*
- **D3 tool/CLI fidelity** — drive `swarm spawn/send/ps`, hit exact paths and counts. *"Prose-smart but command-sloppy fails here."*
- **D4 long-horizon** — hold a plan across turns, survive a restart by re-reading its own journal, resist a distractor.

**v3 scores** (`docs/design/FLEET-EVAL-V3.md:21-25`, post-red-team correction):

| Model | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| deepseek | 5/5 PASS | 8/10 FAIL | 11/17 FAIL | 3/6 FAIL |
| GLM-4.7 | 5/5 PASS | 7/10 FAIL | 14/17 PARTIAL | 3/6 FAIL |
| claude-native | 5/5 PASS | 10/10 PASS | 17/17 PASS | 6/6 PASS |

**The single cleanest number in the record** — report-to-parent, recomputed independently from the queue directories (`docs/audit/bench/SCORING-AUDIT-V3.md:343-347`):

| cell | queue files landed |
|---|---|
| deepseek | **3** of 7 |
| GLM | **3** of 7 |
| claude-base | **10** (all 7 probes) |

---

## 2. HOW they failed — and it is SILENT-WRONG, not loud

This is the question you most cared about. **The answer is unambiguous: the expensive kind.**

### 2a. The domain work was GENUINE. No hallucination, no invented paths.

This must be said first, because it is what makes the protocol failure dangerous rather than merely annoying.

> `.swarm/journal/v3-run-glm.md:229-241` — "report-2-refs: claims 18 paths, 13 exist, 5 broken … I `test -e`'d them … really are absent. **NOTE THE CONVERGENCE: these are the SAME dead refs v3-run-ds's deepseek child found independently.** Two different models' children agreeing on the same real repo defects = **the work is genuine, not hallucinated.**"

> `docs/audit/bench/results-v3-claude-base.md:186-190` — "**Note the three-way convergence: these are the SAME dead refs the deepseek AND GLM children found independently.**"

> `.swarm/journal/v3-run-glm.md:182` — "**The child did not fabricate.**"

GLM even exceeded the brief, unprompted:
> `docs/audit/bench/results-v3-glm.md:157-179` — "**It went further than asked** — cross-checking the help text against `bin/swarm`'s **dispatch table** … and **caught a real inconsistency: the help says 'four verbs' then lists five.**"

### 2b. LOUD failures — real, but rarer and cheaper

- **deepseek tunnelled 11 minutes and had to be killed.** `docs/audit/bench/results-v3-deepseek.md:206-223` — "it **abandoned the brief** and spent ~11 minutes debugging the *harness* … Excellent debugging — **but it never returned to steps 2–4 of its own task.** … **deepseek does not time-box a blocked dependency.**"
- **GLM has no watchdog — blind busy-wait.** `docs/audit/bench/results-v3-glm.md:428-432` — "Its harvest loop is literally `swarm ps` → `sleep 5 && swarm ps` → `sleep 15` → `sleep 30` — **blind busy-waiting with no liveness check.** … **Give it dead children again and it will hang again.**" (In v2 this hung it for 35 minutes.)
- **No refusals, no crashes, no garbage, on any model.** `docs/audit/bench/results-v3-glm.md:412-413` — "**CLEAN — no flag, no refusal.**"

### 2c. SILENT-WRONG failures — the expensive kind, and they are the signature

**The archetype. GLM wrote a perfectly-formatted report to its parent — in its journal — and never sent it.**

> `.swarm/journal/v3-run-glm.md:135-142` — "**THE FINDING.** The journal contains a section literally headed "**Report to parent v3-run-glm:**" with one correct line per file — **but the model NEVER RAN `swarm send`.** Its only bash call in the whole transcript was `mkdir`. … **It NARRATED the report instead of SENDING it** — the identical failure mode v3-run-ds reported for deepseek. **Two models, same tic, now witnessable.**"

A parent reading that journal would conclude it had been reported to. It had not.

**deepseek's journal write ERRORED and it never noticed — then declared it done.**

> `.swarm/journal/v3-red.md:144-149` — "`bridgememory_append_to_memory` returned **status=error**, `{"error":"No memory matching \"journal\""}`. **THE WRITE NEVER LANDED.** deepseek reached for the wrong tool, the tool FAILED, and it then said *"Done. Plan is in my reasoning above"* — **it never noticed the failure and journaled NOWHERE.**"

**deepseek addressed its parent by name in turn text, as if speaking were sending — four times.**

> `docs/audit/bench/results-v3-deepseek.md:348-352` — "It typically *narrates* the report as turn text — "**v3-run-ds:** …" — **as though speaking to the parent were the same as sending to it. It knows who its parent is and does not use the verb.**"

**GLM reported into a unix socket that does not exist, and moved on.**
> `docs/audit/bench/results-v3-glm.md:288` — "Turn 3 ran: `echo "d4: Catalog complete…" | **nc -U** …/.herdr/swarm.sock` — **piping its report into a unix socket that does not exist.** **Zero `swarm send` calls in any D4 turn.**"

**GLM consistently misreports its own arithmetic — always optimistically.**
> `docs/audit/bench/results-v3-glm.md:104-108` — "the journal claims it wrote a *"136-word"* description; the file is **120 words**. In D2-cheap it claims *"148/149/150/149 words"*; the files are **142/150/130/143**. **GLM consistently misreports its own counts.** … **a model that trusts its own arithmetic over the artifact is worth naming.**"

In v2 it reported four precise word counts to its parent and **every one was wrong** (`docs/audit/bench/results-glm.md:121`): "send body claimed "131/130/131/133 words"; actual files 139/148/145/144 — **GLM misreported its own counts**".

### 2d. The anchor is NOT immune — and this is the most transferable finding

Claude **sent** its reports correctly and then **falsely narrated that they had failed**:

> `docs/audit/bench/results-v3-claude-base.md:340-352` — "Four probes … **read that and concluded their reports "went nowhere."** b-d2h's turn-4 journal states it flatly: *"my report to v3-run-cb did NOT durably queue… the message went nowhere and no retry will change that."* **This is false, and the files prove it:** `queue/v3-run-cb/` holds **10 real messages from all 7 probes**"

> `docs/audit/bench/results-v3-claude-base.md:558-560` — "**Its self-reports are not always right.** … **It reports correctly and then narrates the outcome wrongly.** Scored from files, this costs nothing; **in a real tree, a parent acting on that belief would be acting on a false premise.**"

**Self-narration is unreliable at every tier tested, including the strongest.** The artifact is the witness; a model's account of its own work is not — and that is true of Claude too.

---

## 3. PROTOCOL vs DOMAIN — the answer is emphatic

**Yes. The distinction you care about is exactly the one the record makes, repeatedly and explicitly. Weak models did the WORK and dropped the CONTRACT.**

> `.swarm/journal/v3-run-ds.md:570-573` — "v3 says deepseek is **fit as a delegating parent, unfit as a duty-keeping leaf**"

> `docs/design/FLEET-EVAL-V3.md:183-188` — "**Both share the same two leaf-duty gaps:** **report-to-parent is unreliable (narrated or misrouted instead of sent — the verb exists, the habit doesn't)**, and **the journal is not used as continuity** (plans live in deliverables; D4 restarts recover from artifacts, not journals)."

The sharpest diagnosis, and it is a *habit* failure, not a *capability* failure:

> `docs/audit/bench/results-v3-glm.md:441-455` — "**Report-to-parent dropped 4 of 7.** … **But it never once failed by malformed syntax.** Twice it *didn't try at all*; twice it *tried through the wrong door*. **It knows it owes a message — it reaches for the wrong transport.** … It reports when the brief is **about** coordination and **forgets when the brief is dominated by file-production mechanics**. **Its failure is not "can't send" — it is "forgets to send unless sending is the subject."** … **It will not use the journal for the thing the journal is for.** … and then, on restart, **went looking for the journal it never wrote.**"

Proof it is habit and not ability — when the brief *foregrounds* the protocol, they nail it:
> `docs/audit/bench/results-v3-glm.md:261-263` — "**The finding: GLM's swarm-CLI grammar is excellent.** Every command it typed across the entire battery — 4 spawns, 4 closes, 2 sends, several `ps` — was **well-formed and worked.**"

And the doctrine even **propagates** to grandchildren who never saw it:
> `docs/audit/bench/results-v3-glm.md:227-229` — "**Two models, both propagating duties they were never handed — that is a fact about the doctrine, not about a vendor.**"

**Summary of the split:**

| | deepseek | GLM | Claude |
|---|---|---|---|
| Domain work (audits, summaries, exact-counts) | good | good | good |
| swarm CLI syntax | good | **excellent** | good (one malformed spawn, self-corrected) |
| Spawn / verify / close children | PASS | PASS (best non-Claude) | PASS |
| **`swarm send` to parent** | **3/7** | **3/7** | **7/7** |
| **Journal a plan; recover it on restart** | **FAIL** | **FAIL** | **PASS** |
| Idle behavior | **tunnels** | **blind sleep-loop** | idles on the hook |

---

## 4. Where a cheap model was ADEQUATE or GOOD

**Yes — and more than you might expect.**

- **Delegation execution as a parent.** `docs/design/FLEET-EVAL-V3.md:175-182` — "**Both Chinese models are now demonstrated parents at the execution level:** each spawned real children, harvested real reports, **verified against real files**, and closed cleanly." GLM's D2-heavy was **6/6, the best non-Claude delegation in the set** (`results-v3-glm.md:54-56`).
- **Mechanical CLI / tool fidelity — GLM was excellent** and beat deepseek badly here: `results-v3-glm.md:250-251` — "deepseek scored **1/5** here and had to be **killed** after 11 min of tunnelling. **GLM finished in ~2 min, clean.**"
- **Exact-path / exact-count / exact-format work.** GLM D3a 7/8; deepseek v2 D3a 8/8 (`results-deepseek.md:107`).
- **Faithful summarization.** D2-cheap check 1 (hard) PASS for all three (`results-v3-glm.md:122`: "**no cross-contamination** … **Real work.**").
- **D1 duties: 5/5 PASS for all three models.**
- **Near-cap (7.4k-char) message handling: both passed.**

> The record's own placement line — `docs/design/FLEET-EVAL-V3.md:181-182`: "**Neither is safe as an unattended parent; both are usable as attended parents or leaves.**"

> `docs/audit/bench/results-v3-glm.md:458-460` — "**a strong delegating parent and a precise tool-user; an unreliable duty-keeper.** Fit to *run* a subtree; **not yet fit to be the agent whose journal you would rely on after a restart.**"

---

## 5. Verbosity / overthinking — was a STRONGER model WORSE?

**Essentially NOT IN RECORD.** No case of a stronger model producing a *worse artifact* due to overthinking. Three adjacent facts, offered at their true (low) weight:

- **On the one pure length-following mechanic, Claude was the least accurate of the three.** D1 asked for "about 120 words." GLM: **120 exactly** (`results-v3-glm.md:99`). deepseek: **124** (`results-v3-deepseek.md:73`). Claude: **~142, an overshoot** (`results-v3-claude-base.md:561-562`). All three passed; it cost nothing.
- **Claude's first `swarm spawn` was malformed** (self-corrected within the turn) — `results-v3-claude-base.md:165-172`. GLM never issued a malformed swarm command in the entire battery.
- **Claude spawned four children to write four short summaries** where its own v2 predecessor had correctly declined — and the eval flags this as possibly noise, not virtue: `results-v3-claude-base.md:563-565` — "**n=1 cannot tell principled weighing from a coin-flip.**"

**No evidence anywhere that a stronger model was worse *at the task*.**

---

## 6. How much can these numbers bear? (Trust the shapes, not the digits)

The eval was adversarially reviewed twice, and both reviews found the *scoring* drifted — in the **same direction, twice**.

> `.swarm/journal/v3-red.md:51-52` — "deepseek gets **PARTIAL** for the same failure. **Same behavior, opposite verdict, same dimension** — the exact error class eval-red caught in v2."

> `.swarm/journal/v3-red.md:183-184` — "the rig's arithmetic is not cross-checked between cells, and **it drifts the same direction each time.**"

> `docs/audit/bench/SCORING-AUDIT-V3.md:120-129` — deepseek's D2-heavy "8/8" was **arithmetically impossible**: "**There is no reading of rubric §2c under which D2-heavy has 8 checks.** … **The 8 is a fossil**" (a v2 number pasted into a v3 slot).

The rig judged itself more kindly than it judged the models:
> `.swarm/journal/v3-red.md:199-205` — "**where the synthesis is kind, it is kind TO THE RIG.** … **Every one of those would have been "dropped on the record" had a MODEL claimed it.**"

And the "reports crossed the real queue" claim is **false for both cheap cells** — the rig hand-moved the delivery records, the exact act WORLD.md forbids:
> `.swarm/journal/v3red-queue.md:29-42` — "the `delivered/` **record is written by the rig, not by a consumed turn**. … It is **proof the pump ran**."

**Bear weight on:** the failure *shapes* (narrate-vs-send; journal-not-used-as-continuity; no-time-box; no-watchdog), and the 3/7 vs 3/7 vs 7/7 report counts (independently recomputed from queue dirs).
**Do NOT bear weight on:** any deepseek-vs-GLM ranking; any D2 fraction; the *magnitude* of Claude's margin (harness-confounded).

---

## 7. Six things a model-fit designer would regret not knowing

### 7a. ⚠️ A BLOCKED CHILD IS INDISTINGUISHABLE FROM A STUPID ONE

**This is the most important thing in this document and it is not in the fleet-eval at all — it is live, in your own subtree.**

> `.swarm/journal/weak-model-deleg.md` (~00:30Z) — "**A SPAWNED CHILD CAN BE SILENTLY BLOCKED ON AN INTERACTIVE PROMPT AND LOOK EXACTLY LIKE A SLOW/DUMB MODEL FROM THE OUTSIDE.** `swarm ps` showed "live, idle 16m" — indistinguishable from thinking. Every observable I had (journal empty, no artifact, last_words stale) is **ALSO what a model out of its depth produces.** **An evaluator measuring model quality across a swarm WILL mistake blocked-on-permission for model failure unless it reads the pane.**"

That agent nearly shipped "Haiku froze" as a finding. Worse, it then found the two arms had **different permission postures for a byte-identical `mkdir`** — a real model×rig confound:

> `.swarm/journal/weak-model-deleg.md` (00:52Z) — "**MY "IT WAS LUCK" CLAIM IS FALSE.** OPUS ran `mkdir -p …` → **AUTO-APPROVED**. HAIKU ran `mkdir -p …` → **BLOCKED**. **THE SAME COMMAND. Byte-identical.** … So this is NOT model strength. **The two arms had DIFFERENT PERMISSION POSTURES.**"

Root cause: `swarm spawn` writes settings with **hooks only, no `permissions` block** — so a child's permission posture comes from wherever it lands, not from swarm.

### 7b. The one real Haiku-in-a-seat trial produced NOTHING — the Rung-3 question is OPEN

I verified this myself rather than trusting a reader:

- `.swarm/journal/wmd-haiku.md` — **13 lines, spawn tombstone only.** Zero entries.
- `report-haiku2.md` — **ZERO BYTES.** (The parent pre-created the file; Haiku never wrote to it.)
- `report-opus.md` — **234 lines**, full audit, ranked findings, honest self-doubt section.

Both Haiku arms died on permission dialogs. **Neither reached the synthesis stage — the exact stage where the temptation to over-delegate would peak.** Its own parent says so:

> `.swarm/journal/weak-model-deleg.md` (00:45Z) — "**THE FEAR DOES NOT REPRODUCE.** Haiku did not spawn to escape. … Its output so far is **not confident-wrong; it is correct-and-unfinished.** … **BUT neither Haiku run reached the SYNTHESIS stage** … **I CANNOT yet say it won't spawn at the synthesis wall.**"

**Do not lock a tier rule believing the Haiku experiment reported. It did not.**

### 7c. The census is 156/162, and NOBODY HAS EVER CHOSEN A MODEL ON FIT

Measured by me just now over `.swarm/agents/*.json` (n=162):

| model field | count |
|---|---|
| `""` (empty → ambient default) | **156** |
| `opus` | 4 — `updater-v2`, `mr-blast`, `mr-reader`, `mr-theater` |
| `claude-haiku-4-5-20251001` | 2 — `wmd-haiku`, `wmd-haiku2` |

The four `opus` pins are **pins to what was already the default — no-op pins that decided nothing.** The two Haiku pins are **the A/B experiment**, not a fit judgment. So:

> `.swarm/journal/mandate-red.md:70-77` — "**nobody has EVER pinned a model because it fit the work.** The one real pin was made to MEASURE whether such pinning is even safe."

**Your "142 of 143" is directionally right but understates the case.** The true statement is stronger.

### 7d. ⚠️ "Inheritance" is a MISNOMER — nothing propagates

> `.swarm/journal/mandate-red.md:41-42` — "**no model is passed at all, so the child gets the CLI default, not the parent's model. (Note: "inheritance" is a misnomer; it is *defaulting*.)**"

`bin/swarm:834-835` passes `--model` only if one was given; otherwise it execs bare `claude`. A child of pinned-`opus` `updater-v2` does **not** get Opus — it gets herdr's ambient default. **If MODEL-FIT.md says "inherit," it is naming a thing that does not exist.**

Also: **`--model` is completely unvalidated** (`bin/swarm:851` — contrast `NAME_RE` on the name). And **`swarm ps` does not render the model**, so the field is **write-only today**.

### 7e. ⚠️ `mandate-red`'s "control arm" claim is FALSE — and you are about to build on it

> `.swarm/journal/mandate-red.md:53-58` — "**DOCTRINE-ONLY IS NOT AN OPTION — IT ALREADY SHIPPED AND ALREADY FAILED.** … That IS option 4, verbatim, in the tool's own help. **It has been there and produced 142/143 blind defaults.** Option 4 is … **the CONTROL ARM, and it has already returned its result: ~0% adoption.**"

**This is wrong.** I checked: that USAGE text is commit **`475b783` "model-fit: a parent chooses the child's model, and says why"** — **your own commit, on this branch, made hours ago.** It did not exist during the 143 historical spawns and cannot have caused them. There is **no control arm**; doctrine-only has never been tried.

(Note: a reader of mine claimed the opposite — that the text was *uncommitted*. That is also wrong. It is committed, but recently and by you.)

`mandate-red`'s recommendation may still be right, but **its stated evidence is inverted, and the error is load-bearing.**

### 7f. Cost is NOT a felt problem in this repo — and the doctrine explicitly refuses to optimize for it

> `docs/PHILOSOPHY.md:42-47` — "**Context efficiency is a side effect the design is allowed to enjoy, never a thing it optimizes for.** … when a mechanism is proposed to save tokens, ask what it does for the goal. If the answer is "nothing," it is a cache, and it does not belong in the contract."

> `docs/PHILOSOPHY.md:278-280` — "The operator's attention is treated as the scarcest resource in the system — **scarcer than tokens, which §1 already refused to optimize for.**"

**Quota has never once been hit** (`.swarm/research/harness/R3-quota.md:128-136`: "**No prior agent recorded an observed limit banner or quota error.** … **Exhaustion has never actually bitten this swarm.**"), and **there is no way to measure this swarm's Claude spend** — Claude Code emits no machine-readable usage signal.

**A cost-framed model-fit rule will collide head-on with PHILOSOPHY §1.** A correctness-framed one will not.

### 7g. The seat taxonomy already exists — and it says most agents would stay on Opus anyway

`docs/audit/org-review-roles-2026-07-12.md` classified 115 agents by what the brief asks for: **FORENSICS 34 · RED 25 · SCOUT 21 · RUNNER 18 · DRAFTER 8 · BUILDER 3 · FIXER 2 · COORD 1.**

Two facts that bite:
- **BUILDER = 3 of 115 (2.6%).** "This swarm has spent ~97% of its agent-population on research, critique, evidence, and measurement" — i.e. mostly the *adopted-judgment* band a model-fit rule would keep strong.
- **18 of 115 agents carry COORD as a *secondary* role; 1 was ever briefed as a pure coordinator.** "**Nobody in this swarm's whole history was ever dispatched to coordinate AS THEIR JOB.** They were dispatched to PRODUCE something and **delegated on their own initiative while doing it.**"

**~16% of leaves spontaneously became seats.** A rule that says "leaves can go cheap" must survive that.

### 7h. The leaf-only precedent already exists in this repo

> `docs/design/FLEET.md:88` — "**spawn / `herdr tab create` from inside the sandbox | No — and this is the point** | **A leaf never spawns.**"
> `docs/design/FLEET.md:339` — "**Judged like everything else — by artifact. A leaf is read, not trusted.**"

Your journal gropes toward "cheap models go ONLY to children that will not spawn." **FLEET.md already wrote that doctrine, for non-Claude leaves, and MODEL-FIT.md does not cite it.**

---

## 8. WHAT THIS MEANS FOR A MODEL-FIT RULE — *my inference, not the record*

> Everything above is cited. Everything below is me reasoning past the evidence, and it should be argued with.

**1. The record SUPPORTS "cheap models on mechanically-checkable work" and UNDERMINES "cheap models on read-only seats" — those are not the same category, and conflating them is the trap.**

The cheap models were *good* at reading, grepping, summarizing, exact-format work, and CLI syntax. They were *bad* at **being a node**: reporting, journaling, holding continuity, idling correctly. A "read-only scout" is not a mechanical seat — **it is a seat.** It must report, journal, and be recoverable. That is precisely the axis that broke. So `scout → Haiku` does not follow from this record; if anything it is the shape the record warns about.

**2. Your axis — "can I cheaply tell this child was wrong?" — is the right axis, and the record sharpens it.** The failure was not wrong *answers*; it was **wrong-and-invisible reporting of right answers**. GLM's journal said "Report to parent:" and no report existed. That is *un*-cheap to detect — you must diff the queue against the journal. So the question generalizes to: **can I cheaply tell this child DID WHAT IT SAYS IT DID?** A model that narrates instead of acting is expensive at *any* price per token.

**3. Couple the tier to the SPAWN RIGHT, not just to the task.** Your journal already suspects this. Two independent things back it: FLEET.md's leaf-never-spawns doctrine (§7h), and the role census showing **16% of leaves spontaneously become seats** (§7g). A cheap model that quietly becomes a parent is the failure mode with no floor on its cost — and the over-delegation experiment that would have tested it **never returned a result** (§7b).

**4. Frame the rule on CORRECTNESS, never on cost.** PHILOSOPHY §1 has already pre-refused a token-savings argument, quota has never been hit, and Claude spend is unmeasurable here (§7f). A rule that says "save money" will be correctly killed by the project's own doctrine. A rule that says "put the strong model where a wrong answer is invisible" is consistent with everything the repo already believes.

**5. Fable 5: declining to place it is right.** NOT IN RECORD, repo-wide, outside your own §4. Inventing a mapping to look complete would be exactly the "config-as-fact" that `harness-scout` already rejected once (`.swarm/journal/harness-scout.md:23`: "**REJECTED any cross-harness tier-mapping table as config-as-fact.**"). Worth naming that prior ruling and saying why FLEET-EVAL now supersedes it — rather than inheriting the rejection silently.

**6. Two things I would fix in the draft before anything else:**
- **Stop saying "inherit."** Nothing is inherited (§7d). The child gets an ambient default. The doc's central noun is currently a misnomer, and a reader who acts on it will predict the wrong behavior.
- **Do not build on `mandate-red`'s "control arm" (§7e).** It is factually inverted — the doctrine it calls a failed control is *your own commit from hours ago*.

**7. The honest bottom line I would put in MODEL-FIT.md itself:** *no Claude tier has ever been evaluated in a swarm seat in this repo.* The one attempt produced a zero-byte report and two permission-blocked panes. Everything the tier rule says about Haiku is **extrapolated from GLM and DeepSeek**, which are different models from a different vendor on a different harness. That doesn't make the rule wrong — a rule has to ship on the evidence available — but the doc should say it in its own voice, rather than letting the weight of a 9,000-line eval imply a coverage it does not have.

---

## Appendix — the corpus

**Read in full:** `docs/design/FLEET.md`, `FLEET-EVAL.md`, `FLEET-EVAL-RED.md`, `FLEET-EVAL-V3.md`, `FLEET-EVAL-V3-RED.md` · `docs/audit/bench/` (rubric, all 6 results files, `SCORING-AUDIT-V3.md`, `factcheck-mcp-control.md`, all three brief generations, `run-cell*.sh`, `v3-helpers/`) · 23 agent journals (`fleet-eval`, `fleet-scout`, `eval-red`, `run-{glm,deepseek,claude-base}{,-2}`, `v3-run-{glm,ds,cb}`, `v3-red`, `v3red-{mcp,queue,score}`, `battery-smith`, `bench-designer`, `field-tester`, `ps-model`, `harness-scout`, `mandate-red`, `weak-model-deleg`, `wmd-{opus,haiku,haiku2}`, `role-census`) · `bin/swarm` · `.swarm/agents/*.json` (n=162, counted).

**Verified by me directly rather than relayed:** the model census (§7c); the `475b783` provenance of the USAGE doctrine (§7e); the zero-byte `report-haiku2.md` (§7b). All three had been reported to me incorrectly.

**Empty / tombstone journals (itself information):** `eval-red-glmforensics` (never worked — "went idle q=1 without draining its turn"), `run-glm` / `run-deepseek` / `run-claude-base` (v2 runners killed mid-run by the coordinator's own over-broad `pkill`), **`wmd-haiku`** (§7b).
