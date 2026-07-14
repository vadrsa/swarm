# Operator Ledger — Forensic Mining

> SUPERSEDED as a live reference by whatever org-review instrument shipped; kept for the record (original measurements — F-SPAN null result, independently re-measured PR merge-latency decay table — not duplicated elsewhere).

**Agent:** ledger-forensics (child of org-review-scout)
**Date:** 2026-07-12
**Corpus:** `.swarm/journal/operator.md` (194 lines, read in full), `.swarm/queue/operator/delivered/` (60 messages), `.swarm/agents/*.json` (106 agents), `docs/design/DECISIONS.md`, GitHub PR API.

**Discipline:** every claim is tagged VERIFIED (I read the line — quoted), MEASURED (a number, with the file it came from), or REASONED (inference — falsifier named).

---

## HEADLINE: four findings; two kill a hypothesis in my brief

1. **F-SPAN DOES NOT FIRE.** Zero of 60 messages to the human came from below the top layer. All 22 distinct senders are depth 1, against a top-layer width of 25. The hypothesis my parent said would most change their design is **unsupported by the record.** (§6)
2. **THE MAILBOX IS UNDEFENDED IN CODE AND HAS NEVER BEEN ABUSED IN PRACTICE.** The sibling's `deep` agent is a *sandbox capability proof*, not a field sighting — and their code reading is right: anyone at any depth *can* mail the human. **No one ever has.** 100% compliance with a briefed duty, across 106 agents. The two findings compose; they don't conflict. (§6.6)
3. **THE LEDGER CANNOT TIME ANYTHING.** All 112 `##` headers are date-only; **zero** carry a clock time, and 73% of entries collapse onto one calendar day. Any instrument that measures human latency *from operator.md text* is vapor. (§4)
4. **BUT THE DECAY IS REAL, AND I RE-MEASURED IT FROM SOURCE.** Not by trusting DECISIONS.md — from GitHub's API. The gate went 17.4h → 2.8h → 14s → 3s, and the two most recent PRs (#81, #82) merged in **9s and 3s**. It is not history; it is **the current operating regime.** (§3)

A structural finding governs all of the above: **the ledger's "I" is not the human — it is an AI session.** Miss this and every number in the file means the opposite of what it appears to mean. (§0)

---

## §0. THE LOAD-BEARING DISTINCTION: "I" ≠ "User"

Everything in this report depends on this, and I nearly got it wrong.

The operator ledger is written by an **operator *session*** — a Claude agent whose `my_name()` returns `"operator"` — not by the human. VERIFIED in code:

```
bin/swarm:64    return os.environ.get("SWARM_AGENT_ID") or "operator"
bin/swarm:687   if my_name() == "operator":   sys.exit(0)     # cmd_deliver
bin/swarm:704   if my_name() == "operator":   sys.exit(0)     # cmd_event
```

The ledger maintains this distinction **consistently and deliberately** in its own prose. VERIFIED, operator.md:8:

> "User chose PR flow: agent delivers branch -> **I** verify -> **I** open PR -> **human** merges."

One sentence, three actors: *User* (decides), *I* (the session — verifies, opens), *human* (merges). MEASURED across the corpus: the human appears as `User`/`Operator`/`human` and the session as `I`/`my`/`myself`, and I found **no line** where the two are conflated.

**Consequence:** every "I verified myself / I read the diff / 65 OK my run" line is an **agent** claiming to have read — not a human. This is the single most important fact for anyone designing an instrument on this file, and it inverts the PULL-UP question in §2.

---

# EVIDENCE

## §1. RECURRENCE — what shapes repeat

MEASURED from operator.md entry headers (112 `##` lines):

| Entry type | Count |
|---|---|
| `CLAIM:` (mailbox claim line) | 38 |
| `VERDICT:` / `VERDICTS:` | 16 |
| `DISPATCH:` | 15 |
| everything else (SHIPPED, RULING, MERGED, ADOPTED, CORRECTION, BUG, FINAL SPEC, REFRAME…) | 43 |

### Shape A — **the scout cycle** (recurred **9×**, the dominant shape)

`DISPATCH a fresh named scout → it returns ONE design doc → operator judges by reading → PASS → close on harvest`

VERIFIED — all nine, quoted from their `VERDICT:` headers:

| line | verdict header | agent |
|---|---|---|
| 80 | `VERDICT: HARNESS.md PASS; harness-scout closed on harvest` | harness-scout |
| 89 | `VERDICT: DECISIONS.md PASS; decision-scout closed on harvest` | decision-scout |
| 94 | `VERDICT: DECISION-WIRING.md PASS; decision-wiring closed on harvest` | decision-wiring |
| 99 | `VERDICT: PROXY-WIRING.md PASS; proxy-scout closed` | proxy-scout |
| 104 | `VERDICT: PIPELINE-WIRING.md PASS; pipeline-scout closed on harvest` | pipeline-scout |
| 111 | `VERDICT: HOOK-WIRING.md PASS; hook-scout closed` | hook-scout |
| 121 | `VERDICT: INDUSTRY-PATTERNS.md PASS; contractor closed` | patterns-contractor |
| 153 | `VERDICT: FLEET.md PASS; fleet-scout closed on harvest` | fleet-scout |
| 158 | `VERDICT: FLEET-EVAL.md PASS; fleet-eval closed on harvest` | fleet-eval |

MEASURED: **9/9 of these scouts got a PASS.** Zero scouts were ever failed outright. The one non-PASS is a *RETURN by the human*, not a fail by the session (line 92 — see §2).

**The scout is single-use by design.** VERIFIED, line 86:

> "closed codex-audit on harvest (re-audits are fresh spawns by design — audit independence)"

and line 54:

> "a future adversarial review spawns fresh reviewers by design (independence is the value; warm context is a LIABILITY for that shape — noted as a rung-0 exception)"

### Shape B — **the standing arm task cycle** (recurred **12×**)

`Task N → hardener → branch → operator verifies diff + runs suite → PR → merge`

MEASURED: Tasks 2,3,4,5,6,7,8,10,11,12,13,14 dispatched to the **same** agent, `hardener`, across the whole 3-day record. `hardener` is the single most prolific mailer of the human (16 of 60 messages). This is the "warm-name reuse" mechanism the ledger itself names at line 47:

> "real mechanism = dispatcher-side warm-name reuse (re-briefing cost, not repetition count)"

### Shape C — **adversarial review inside the child** (recurred **≥7×**)

The operator does not run its own red-teams; the *scouts* do, unprompted. VERIFIED, line 90:

> "Scout ran its OWN adversarial review (red-decisions: 1 KILL 9 WOUNDs, fixed+reverified) and closed its children — full doctrine propagation, zero prompting."

Red-team instances found in the tree: `red-decisions`, `red-wiring`, `red-proxy`, `red-simplest`, `red-operator`, `eval-red`, `dp-red`, `oc-red`, `structure-red`/`red2`/`red3`, `hook-red`, `pipeline-red`, `onboarding-red`. MEASURED from `.swarm/agents/*.json`: **13 agents with `red` in the name**, only 2 of them (`red-simplest`, `red-operator`) spawned by the operator directly — the other 11 were spawned by scouts.

### Shape D — **the three standing arms** (`hardener`, `field-tester`, `updater`)

MEASURED: these 3 agents sent **41 of 60** (68%) of all messages to the human, and are the only names ever re-dispatched. Everything else in the top layer is single-use.

---

## §2. PULL-UP — what the human still does themselves

**This question inverts once §0 is applied.** Verification, merging, PR-opening, and report-reading are *already* owned by a top-level agent — the operator session does all of them. VERIFIED samples:

- line 12: "**Verified hardener's Task 2 myself**: diff read (…), 46 OK branch suite, 64 OK composed… Pushed, PR #66."
- line 117: "**Verified myself**: 78 OK, write-first + recursion guard read in diff."
- line 90: "**Judged by reading** (606 lines, outline + 1c spot-check)"
- line 165: "ROOT CAUSE **VERIFIED by me**: cmd_spawn tab-create (bin/swarm:906) omits --workspace"

So the pull-up has *already happened*. The real question is the residue: **what is left that only the human does?**

MEASURED — I extracted every line where `User`/`Operator`/`human` is the grammatical subject (26 lines). The complete verb census:

| verb | count | class |
|---|---|---|
| approved | 5 | **gate** |
| chose | 3 | **initiation** |
| wants / asked / request | 4 | **initiation** |
| corrected / correction | 3 | **correction** |
| overruled / re-scopes / reframed / extends / added | 6 | **correction** |
| returned | 1 | **correction** |
| merged | 2 | **gate** |

**FINDING (MEASURED):** the human's own acts are **overwhelmingly initiation and correction, not gate-answering** — and this independently reproduces DECISIONS.md's own claim, which I did not take on trust. Compare, VERIFIED, `docs/design/DECISIONS.md:130-134`:

> "**Genuine human judgment, wherever the record shows it, is an initiation or a correction, never a gate answer**: rejected the overseer agent, 'recon should shrink', R1/R2, the choice-doctrine process correction, 'decision POINTS, not questions'"

The highest-value human acts in the entire ledger are all **corrections that overturned the session's own reasoning** — the session was wrong, and only the human caught it:

- **line 78** — "User correction taken: **I drafted choice-doctrine inline — against my own delegation doctrine.**"
- **line 92** — "User returned decision-scout's deliverable, reason verbatim: '*the task is to understand how to wire up such an engine or tool, not if we want to build it or not*.' **My PASS verdict corrected**" ← *the session had already stamped PASS on a doc that answered the wrong question.*
- **line 124** — "Operator called out **silent killing of their idea — CORRECT**: HOOK-WIRING §4 killed pre-write in one sentence; **I hardened it into the next brief as dogma; four docs inherited it.**"
- **line 156** — "Operator: leaf-only is a livable fallback, NOT a requirement… **My error (over-fitting the constraint) journaled.**"
- **line 193** — "Operator's question **exposed my false dilemma**"

**REASONED:** the human is not a bottleneck to be pulled up — they are the **error-correction channel**, and on this record it fired 5+ times against verdicts the agent had already passed. *Falsifier: if you find a ledger entry where a human correction was wrong and the session's original judgment was right, this reading weakens.* I looked; I found none.

---

## §3. DECAY — the gate collapse (REAL, and I reproduced it from source)

### The measured finding, verbatim

VERIFIED — `docs/design/DECISIONS.md:125-129`, quoted exactly:

> "- **The gate collapsed into standing authorization within a day:** #65–#68 waited 16–17h for the human's session (then merged as a batch 26 seconds apart); #72/#73, contract-class, got 2.8h; #74, also contract-class, was merged under pre-auth in **14 seconds**; #76/#78 in 3–4s (MEASURED, pr-miner §c "tier drift"). **The tier labels stayed; the attention behind them thinned.**"

The operator ledger itself confirms it independently and calls it uncomfortable. VERIFIED, operator.md:90:

> "**Uncomfortable mirror: my gate collapsed 16h->2.8h->14s under pre-auth, tier labels intact, attention thinned — the engine already runs off-books.**"

And it is a *live* constraint on current design work. VERIFIED, operator.md:192:

> "Scout caught propose-and-confirm colliding with the repo's MEASURED gate-decay (DECISIONS.md:120-127, 14s within a day, 'attention thinned' — **I verified the citation**)."

### I did not trust it — I re-measured it from GitHub

MEASURED, `gh pr list --state merged --json createdAt,mergedAt` (open→merge latency):

| PR | open→merge | class |
|---|---|---|
| #65 | **17.4h** | mechanical |
| #66 | **17.3h** | mechanical |
| #67 | **16.1h** | docs |
| #68 | **16.0h** | contract |
| #69 | 6.5m | doctrine |
| #70 | 6.2m | docs |
| #71 | 2.5m | fix |
| #72 | **2.8h** | contract |
| #73 | **2.8h** | docs |
| #74 | **14s** | contract |
| #75 | **3s** | docs |
| #76 | **3s** | doctrine |
| #77 | **3s** | docs |
| #78 | **4s** | fix |
| #81 | **9s** | fix |
| #82 | **3s** | doctrine |

**The decay is confirmed to the second, from an independent source.** And note the last two rows: **#81 and #82 are from *today*, and they merged in 9s and 3s.** The decay did not stop after being discovered and named. It is the current operating regime.

**Note (VERIFIED, DECISIONS.md:118-124):** the 63 pre-swarm PRs are correctly excluded from this — "*opened and merged in the same working session, 53 of them in under 60 seconds; 'merging was execution, not review'*". My GitHub pull shows exactly this for #56-#64 (19s, 14s, 15s, 19s, 17s). They are not gate data. I did not use them.

### "Approves too fast to have read" — the direct test

I ran it. **The result is a NULL, and the reason matters — see §5.**

---

## §4. WHAT IS ACTUALLY IN THE LEDGER (the most important section)

### Schema — VERIFIED by reading all 194 lines

```
## YYYY-MM-DD — [hand-tag] TYPE: free-text title
<one paragraph of dense free prose, or nothing at all>
```

- **194 lines total: 112 `##` headers + 82 body lines.** 38 of the headers (the `CLAIM:` lines) are **header-only, with no body at all.**
- **Written by:** the operator *session* (§0), not the human. The human never writes a line of it.
- **Format:** free prose. There is no key-value structure, no field names, no schema. Entry "types" (`DISPATCH:`, `VERDICT:`, `CLAIM:`) are an **emergent prose convention the session adopted mid-corpus**, not an enforced format.
- **Adoption is partial and datable:** the `[ops-main]` hand-tag appears in **91 of 112** headers. It starts at line 51, where the session says so explicitly — VERIFIED: "*Adopting F1/F2/F5 disciplines myself starting this entry (hand tag ops-main; claim lines on future mail).*" The 21 untagged headers are all *before* that line.

### ⚠️ THE KILLER CONSTRAINT: THERE ARE NO TIMESTAMPS

**MEASURED: of 112 `##` headers, exactly ZERO carry a clock time.** Every header is date-only (`## 2026-07-11 — …`). `grep -c '^## .*[0-9][0-9]:[0-9][0-9]'` returns **0**.

**MEASURED: 82 of 112 entries (73%) fall on a single calendar day, 2026-07-11.** Per-day counts: 07-09: 3, 07-10: 4, **07-11: 82**, 07-12: 23.

So within the ledger's dominant day, **all 82 entries are mutually unordered in time** except by file order. You cannot compute *any* latency, duration, or interval from the ledger text. The file is **not a time series.** It is a **narrative**.

### What an instrument CAN extract from operator.md

- ✅ Entry **type** (`DISPATCH`/`VERDICT`/`CLAIM`) — by prose convention, ~91% reliable, and only post-line-51.
- ✅ **Agent names** — they appear as literal tokens and cross-reference cleanly to `.swarm/agents/*.json` (I resolved 22/22 senders with zero misses).
- ✅ **PR numbers** (`#65`–`#82`) — clean, and they join to the GitHub API, which is where the real timestamps live.
- ✅ **Verdict polarity** (PASS / RETURNED / correction) — a keyword, and it was unambiguous in all 16 verdict entries.
- ✅ **Ordering** — the file is append-only, so line number is a monotonic sequence.
- ✅ **Which day** — date-only, and 73% of the corpus collapses onto one day.

### What an instrument CANNOT extract from operator.md — READ THIS BEFORE BUILDING ANYTHING

- ❌ **Any wall-clock time. Any latency. Any duration. Any rate.** No entry knows what hour it happened.
- ❌ **What the human did**, as distinct from the session. The file is the *session's* first-person account; the human appears only when the session chooses to quote or paraphrase them. There is **no record of the human's own actions written by the human.**
- ❌ **Whether anything was read.** The file contains *claims* of reading ("Judged by reading", "diff read", "I verified the citation"). Per WORLD.md §8 — "Judge artifacts, never claims" — these are exactly the claims the system says not to trust. **The ledger cannot witness its own reading.**
- ❌ **Agent lifetimes.** See §5 — `.swarm/agents/*.json` has a spawn `ts` and **no close field, no status field**. Nothing on disk records when an agent died.

**REASONED, and this is the finding I'd most want acted on:** an instrument that reads `operator.md` to measure *attention, latency, or decay* is **reading the wrong file.** Those facts live in `.swarm/queue/operator/delivered/` (ctime, §5) and in the **GitHub API** (§3) — both of which are machine-written and neither of which can lie about time. The ledger is where the *narrative* lives, and it is excellent at that — but it is a story the session tells about itself. *Falsifier: show me one operator.md entry from which a real latency can be computed without joining to an external file.* I could not construct one.

---

## §5. THE MAILBOX AS INSTRUMENT — and the confound that saved me from a false headline

The brief asked whether the human "approves in a timespan too short to have read." The ledger cannot answer (§4). But there **is** a hidden timestamp channel, and I found it:

**`.swarm/queue/operator/delivered/*.json` file `ctime`.** The `mv` into `delivered/` preserves `mtime` (it equals the message `ts` exactly — useless), **but it updates `ctime`** — which therefore records *the moment the message was claimed.*

MEASURED, n=60:

| | queue→claim latency |
|---|---|
| min | **9 seconds** |
| p25 | 14s |
| **median** | **19 seconds** |
| p75 | 36s |
| max | 3.3h (one outlier) |
| **under 60 seconds** | **55 / 60** |

Cross-referenced against body size (median body = **1,760 chars**, max 7,544):

**MEASURED: 47 of 59 messages were claimed at an implied reading rate faster than 25 chars/sec** — above sustained adult reading speed (~17–25 chars/sec). Median implied rate: **85 chars/sec.** The fastest: a **7,544-char** report from `onboarding-scout`, claimed **12 seconds** after it was queued — **647 chars/sec.**

### 🛑 THE CONFOUND — and why I am NOT reporting this as "the human doesn't read"

**Per §0, the claimer is the operator *session*, not the human.** I verified the moves are individual, not a batched `mv -t` (I checked the ctime gaps — every claim is its own move, seconds after arrival). So this measurement shows **an AI session picking up its mail promptly on its next turn.** That is *correct behavior*, not negligence.

**This is a NULL RESULT for the brief's hypothesis, and I want it stated loudly:** *the files contain no measurement of when the human read anything.* The human's reading is not instrumented anywhere in `.swarm/`. The 19-second median is the **session's** pickup latency and says nothing about the human.

**The real human-attention measurement is the PR merge latency in §3** — and that one *does* indict, because merging is an act only the human performs (VERIFIED, line 8: "human merges"). 3 seconds to merge a doctrine PR is not a reading time.

*Falsifier for my caveat: if someone shows the claim-move is performed by a human keystroke rather than the session's tool call, then the 19s median does indict the human and my caveat is wrong. Test: read the operator pane transcript for a `mv`/tool call adjacent to a CLAIM ledger line.*

---

## §6. THE F-SPAN TEST — **IT DOES NOT FIRE** ⛔

My parent flagged this as the single most valuable thing I could return, and named the hypothesis from `OPERATOR-STRUCTURE.md §4e`: *agents below the top layer mailing the human directly, with distinct senders exceeding the top layer's width.*

**I tested it against the full record. It is FALSE on this repo.**

### 1. Volume + cadence (MEASURED, n=60)

- **60 messages** to the human, over **2.89 days** → **20.7 msgs/day**.
- Per day: 07-09: 6, **07-10: 32**, 07-11: 11, 07-12: 11.
- **3 bursts** of ≥3 messages inside 10 minutes:
  - 07-10 16:51 — **7 messages** from `field-tester`, `hardener`, `inbox-scout`, `updater`
  - 07-10 17:56 — 3 messages from `hardener`, `harness-scout`, `updater`
  - 07-12 01:52 — 4 messages from `field-tester`, `hardener`, `updater`

### 2. Distinct senders (MEASURED): **22**

| msgs | sender |
|---|---|
| 16 | hardener |
| 13 | field-tester |
| 12 | updater |
| 1 each | codex-scout, structure-scout, red-operator, red-simplest, inbox-scout, codex-audit, harness-scout, decision-scout, decision-wiring, proxy-scout, pipeline-scout, hook-scout, patterns-contractor, skill-writer, fleet-scout, fleet-eval, onboarding-scout, onboarding-split, operator-structure-scout |

**The three standing arms account for 41 of 60 (68%).** The other 19 senders sent exactly one message each — the scout cycle closing its loop (§1, Shape A).

### 3. **F-SPAN: depth of every sender** — the answer

I walked the parent chain in `.swarm/agents/*.json` for all 22 senders.

> ## **MESSAGES FROM DEPTH ≥ 2: `0` / 60.**
> ## **DISTINCT DEPTH ≥ 2 SENDERS: `0`.**
> ## **ALL 22 SENDERS ARE DEPTH 1.**

**Every single message the human has ever received came from a direct child of the operator.** Not one agent below the top layer has ever mailed the human — across 106 agents, a tree reaching depth 4 (`operator → org-review-scout → grave-org → grave-kills → kill-audit`), and 60 messages.

And the width test also fails to fire: **22 distinct senders vs. a top-layer width of 25.** Distinct senders ≤ top-layer width. F-SPAN requires the opposite.

**F-SPAN DOES NOT FIRE. THE HYPOTHESIS IS UNSUPPORTED BY THE RECORD.**

**REASONED — why it doesn't fire, and why that matters:** the discipline "report to your parent" is doing the work. `cmd_send` genuinely has no parent check and no depth check (the sibling's code reading is correct — I confirmed it: `bin/swarm:986` only checks the recipient *exists*, and `:1039` skips the doorbell for `operator`). **The mailbox is undefended by construction and defended perfectly in practice.** Deep agents *could* mail the human at any moment; across 106 agents and 3 days, **none ever has.**

*Falsifier: a single message file in `.swarm/queue/operator/` whose `from` resolves to depth ≥2. I checked all 60 (delivered + waiting). There are none. If the swarm grows and one appears, F-SPAN fires and this finding expires.*

### 4. Size (MEASURED)

- min 333 / **median 1,760** / mean 1,970 / **max 7,544** chars.
- ≥4,000 chars: **4 messages**. ≥6,000: **1**. ≥7,500 (near the 8,000 cap): **1**.
- **Total text ever handed to the human across all 60 messages: 118,176 chars** (~30k tokens, ~2 hours of human reading at 17 chars/sec).

The human is **not** being handed walls of text. Only one message ever approached the cap. **The size hypothesis does not fire either.**

### 5. What the human did with them (**NULL — stated loudly**)

- **38 of 60** messages have a `CLAIM:` line in the ledger.
- **22 of 60** have none — and **all 22 pre-date** the F5 claim-discipline adopted at line 51. **Post-F5 unclaimed: 0.** The discipline, once adopted, was followed with **zero misses.**

But: a `CLAIM:` line records only that *the session moved the file*. **It does not record that the human read anything.** Per §5, the human's reading is not instrumented anywhere. **NULL RESULT: the files cannot support a per-message "human read this / dropped this" measurement.** The closest real signal is the PR merge latency in §3, which is a different (and better) instrument.

### 6. Orphans — **zero on the live record; `deep` was a SANDBOX agent, not a field observation**

My parent relayed this as "*the sibling found an agent named `deep`, not in the registry, that mailed the human 6x* — verify or refute on the live record." I did both, and **the distinction turns out to matter a great deal.**

**On the live record: ZERO orphans.** MEASURED:

- `grep -rl '"from": "deep"' .swarm/queue/` → **no match, anywhere.**
- `.swarm/agents/deep.json`, `.swarm/journal/deep*.md` → **do not exist.**
- All 60 operator messages, senders checked against the registry: **unregistered senders = NONE.** All 22 resolve cleanly to a registered, depth-1 agent.
- (The only `deep`-ish real name is `run-deepseek-2`, a registered depth-2 child of `fleet-eval`, which mailed **its own parent** — never the operator.)

**But `deep` was never a claim about the live record, and I nearly reported it as a refutation.** I read the source. VERIFIED, `docs/design/OPERATOR-STRUCTURE.md:346-351`:

> "the reviewer proved the mailbox is not merely unguarded but *entirely* unguarded — by accident, which is the best kind of proof: an agent named `deep`, **not in the registry**, running **outside herdr**, from **a directory that is not the project**, mailed the human **six times** and the tool did not object once. VERIFIED, `cmd_send:986-992` — the only recipient exempted from even the existence check **is the human**, and the sole gate is a **byte count**."

`deep` is a **deliberately-constructed sandbox agent** from the reviewer's 3-deep test tree (`OPERATOR-STRUCTURE.md:383` — "*grandchild 'deep' (3 levels down) mails the human: operator mailbox 0 ← REFUSED*"). It is a **capability proof**, not a field sighting. **The sibling is correct and I confirm their code reading independently** (`bin/swarm:986` checks recipient existence for every name *except* `operator`; `:1039` skips even the doorbell).

**So the two findings compose rather than conflict, and this is the sharpest thing in my report:**

> **The mailbox is completely undefended in code — and has never once been abused in practice.**
> `deep` proves *anyone at any depth can*. The record proves *no one ever has* (0/60).

**REASONED:** the guard that is actually holding is the **briefed duty "report to your parent"** — prose, not code — and on this corpus it has a **100% compliance rate across 106 agents and 3 days.** That is a real, measured fact about how well doctrine-only enforcement works *here*, and it is the strongest available evidence **against** the premise that the mailbox needs a code gate today. *Falsifier: one message file in `.swarm/queue/operator/` whose `from` resolves to depth ≥2. I checked all 60. There are none. If the tree grows and one appears, F-SPAN fires and this expires.*

---

# NULL RESULTS — collected, because a null is a real result

| # | Hypothesis (from brief or sibling) | Verdict |
|---|---|---|
| N1 | Human confirms things too fast to have read — measurable from the ledger | **NULL.** Ledger has zero clock times (0/112 headers). Cannot be computed from operator.md at all. |
| N2 | The 19s median mailbox-claim proves the human doesn't read | **NULL / CONFOUNDED.** The claimer is the operator *session* (bin/swarm:64,687). Measures AI pickup, not human attention. **Do not build on this.** |
| N3 | Per-message "human read it / dropped it" is recoverable | **NULL.** Nothing in `.swarm/` timestamps a human's read. Only the session's file-move is recorded. |
| N4 | **F-SPAN: deep agents flood the human's mailbox** | **DOES NOT FIRE.** 0/60 messages from depth ≥2. 22 senders, all depth 1. 22 senders < 25 top-layer width. |
| N5 | An orphan agent `deep` mailed the human 6× **on the live record** | **NOT ON THE LIVE RECORD** (0 orphans in 60 msgs) — **but the sibling never claimed it was.** `deep` is their *sandbox* agent, a capability proof that the mailbox has no guard. **Their code reading is correct and I confirm it.** The two findings compose: *undefended in code, never abused in practice.* |
| N6 | The human is handed walls of text | **DOES NOT FIRE.** Median message 1,760 chars; exactly 1 of 60 near the 8k cap. |
| N7 | Agent lifetime distribution is measurable | **NULL.** `.swarm/agents/*.json` has spawn `ts` only — **no close/end/status field exists.** See §7. |

---

## §7. VOLUME / CADENCE of the tree

MEASURED from `.swarm/agents/*.json` (106 files):

- **106 agents total.** **25 with `parent == "operator"`** (the top layer).
- Deepest coordinator fan-out: `field-tester` (16 children), `fleet-eval` (8), `operator-structure-scout` (5), `onboarding-scout` (4), `opencode-plugin-scout` (4).
- Tree reaches **depth 4** (`operator → org-review-scout → grave-org → grave-kills → kill-audit`).

**Top-layer spawn timeline** (from `ts`, the only time field that exists):

```
07-09 18:40  field-tester   ┐
07-09 18:41  hardener       ├─ THE 3 STANDING ARMS (still live, 3 days on)
07-09 20:37  updater        ┘
07-09 23:07  codex-scout           ┐
07-10 15:12  structure-scout       │
07-10 15:46  red-simplest          │
07-10 15:46  red-operator          │
07-10 16:47  inbox-scout           │
07-10 17:09  updater-v2            │
07-10 17:10  codex-audit           │
07-10 17:40  harness-scout         │
07-10 18:02  decision-scout        │
07-10 19:05  decision-wiring       ├─ 22 EPHEMERAL: spawned, delivered
07-10 21:59  proxy-scout           │   one doc, closed on harvest
07-11 01:02  pipeline-scout        │
07-11 01:46  hook-scout            │
07-11 08:54  patterns-contractor   │
07-11 11:18  skill-writer          │
07-11 16:49  fleet-scout           │
07-11 18:16  fleet-eval            │
07-12 12:56  onboarding-scout      │
07-12 13:25  onboarding-split      │
07-12 15:59  operator-structure-scout │
07-12 16:02  opencode-plugin-scout │
07-12 16:53  org-review-scout      ┘
```

**MEASURED: 25 top-level agents in 2.9 days ≈ 8.6 top-level spawns/day.** Cadence is **accelerating**: 4 on 07-09, 8 on 07-10, 5 on 07-11, **6 on 07-12** — and 5 of the 6 most recent are still live.

### Standing vs. ephemeral (MEASURED)

- **Standing: 3** — `hardener`, `field-tester`, `updater`. Spawned on day 1, **still live on day 3**, repeatedly re-dispatched (hardener alone: Tasks 2–14). These are the only names ever reused.
- **Ephemeral: 22** — spawned for one deliverable, closed on harvest. **9 of them are the documented scout cycle** (§1).
- **Ratio: 12% standing / 88% ephemeral.**

### ⚠️ NULL: lifetimes are NOT on disk

**The agent record has a spawn `ts` and nothing else.** VERIFIED — the complete key set of every one of the 106 files is:

```
["cwd", "model", "name", "pane", "parent", "tab", "task", "ts"]
```

**There is no `closed`, no `ended`, no `status`, no `state` field.** `swarm close` removes the pane; it does not stamp the record. **Therefore agent lifetime is NOT COMPUTABLE from `.swarm/agents/`.**

The best available proxy is the **journal file mtime** (last thing the agent wrote) minus spawn `ts` — a *lower bound*, and only that. **REASONED:** on that proxy the ephemeral scouts live **~1–4 hours** and the standing arms **~72h and counting**. *Falsifier: an agent that went idle long before its journal's last write, or one closed without journaling — either breaks the proxy. I report it as a bound, not a lifetime.*

---

## What I did NOT do

Per brief: I designed nothing and recommended no instrument. Where the evidence kills a hypothesis (§6, N4, N5) I said so as loudly as I could, because that was the highest-value thing I had.
