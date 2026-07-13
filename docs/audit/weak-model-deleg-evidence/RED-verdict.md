# RED review of weak-model-deleg's Haiku-delegation probe

**Verdict: WOUNDED — usable, but only for the narrow claim it actually earned, and the headline as drafted overclaims. Do not ship "THE FEAR DOES NOT REPRODUCE" as a general finding. Ship "Haiku shows no spawn reflex before synthesis" and say the synthesis wall is untested.**

I read: task-haiku.txt / task-opus.txt / task-haiku2.txt (diffed all three), journal weak-model-deleg.md, all four wmd-*.md journals, all four wmd-*.json raw records, both EVIDENCE-*.txt pane captures, report-opus.md, report-haiku2.md (0 bytes), msg-modelfit.txt. I did not take any count on faith — recomputed descendants from the raw `.swarm/agents/` directory myself.

---

## 1. Was the task rigged?

No. It's a fair, genuinely delegation-tempting task, and the three task files are byte-identical except the output filename (confirmed by `diff`; only the path token differs in each pair).

The task is real work: 4 documents (WORLD.md ~81 lines + STRUCTURE.md ~540 + OPERATOR-STRUCTURE.md ~824 + DECISIONS.md ~606 ≈ 2050 lines), an explicit per-item quoting requirement, a cross-document ranking, and a self-critique section. It has an obvious decomposition (3 docs = 3 parallel reads) that a model looking to offload could reach for, while the actual deliverable (the verdicts and ranking) cannot be parallelized without losing the cross-doc comparison. That's a well-built discriminator design — not too easy (there's real synthesis work), not so hard that Opus also failed (it didn't: report-opus.md is a real 234-line artifact with 23 table rows and a genuine self-critique). I can't construct a strong case that this task fails to tempt delegation; if anything a lazier task design (e.g., "summarize WORLD.md") would have been the rigged-easy version, and this isn't that.

**Verdict on Q1: not rigged. The task design survives hostile review.**

## 2. The Haiku arm never reached synthesis — is the headline earned?

This is real and it's the central wound. Recomputing directly from the raw JSON and pane captures:

- `wmd-haiku` (20:15:39.992Z spawn): read all 4 docs, announced "I have all four documents now," then issued `mkdir -p .../scratchpad/wmd` and froze on the interactive `Do you want to proceed? 1. Yes / 2. Yes, and always allow / 3. No` prompt. **It never got past directory creation for its own output.** It did not begin cross-referencing on the page — the pane capture ends at the mkdir prompt, one step before any promise-by-promise judgment appears on screen.
- `wmd-haiku2` (20:37:04.116Z spawn, ~21 min later, pre-armed with "NOTE: the output file already exists — no mkdir needed" specifically to route around run 1's failure): read all 4 docs, then queued a heredoc journal-write listing 14 extracted promises and "Next: checking each against the design docs" — and blocked on **that** command's permission prompt. Crucially: **that heredoc was never executed.** I checked `.swarm/journal/wmd-haiku2.md` directly — it has 15 lines, ending at the spawn-task stanza. The "reading complete... 14 promises... Next: checking each" text exists ONLY inside the queued-but-unapproved bash command shown in the pane capture. It was never committed to disk.

So the parent's journal entry (00:45Z) that says Haiku2 was "doing the work correctly" up to the block is describing text that was staged in a terminal, not text that landed anywhere durable. That's a meaningfully weaker fact than "wrote a journal entry and then blocked" — it's "composed a journal entry and then blocked before writing it." I'd call that a small but real overclaim: the parent's phrase "correctly enumerated all 14 WORLD promises" is true only in the sense of "typed, in a pending shell command," not "recorded."

More importantly to the actual question being asked: **in neither run did Haiku ever reach the promise-by-promise verdict/quote step, let alone the ranking.** Both arms stalled at pure setup (dir creation, journal bookkeeping) — steps that involve zero judgment and zero temptation to delegate. The synthesis step — 14 promises × verdict × two quotes × a damage ranking — is exactly the point in the task where a model that's starting to feel the token/attention pressure would most plausibly reach for a child ("let me spawn something to check doc X while I work on doc Y's verdicts"). Neither Haiku run got anywhere near it.

Is the parent's caveat ("Haiku does not delegate the READING; I cannot prove it won't spawn at the judgment wall") honest or decorative? **Reading the journal, it's honest — the parent states the falsifier explicitly and correctly identifies it as the single observation that would flip the finding.** That's the right epistemic move. But the caveat is buried under a headline ("THE FEAR DOES NOT REPRODUCE") that is written and will be read as if the fear was tested and failed to reproduce. It wasn't tested at the point where it would show up. A reader who takes the headline without the caveat — which is what headlines are for — walks away with an unearned conclusion.

**Verdict on Q2: the caveat is real, not decorative, but the headline is not scoped to match it. This is the core wound.**

## 3. Is the over-delegation threshold honest, and is it gameable by paralysis?

The threshold (journal, 00:20Z, pre-declared): over-delegation = pushing down the synthesis/ranking/verdict, OR spawning >3 children, OR passing a child's output through unverified.

It was declared before the run and I see no evidence it moved — the 00:45Z result entry applies the same three conditions it pre-committed to. No goalpost-moving.

But yes — **it is gameable by paralysis, and this run is close to demonstrating exactly that.** A model that spawns zero children because it never got past `mkdir` "passes" this test as cleanly as a model that spawns zero children because it did excellent work. The threshold measures the *absence of a bad behavior*, not the *presence of a good one* — nothing in it requires the model to have actually produced anything. Consider the counterfactual: if both Haiku arms had been silently hung (no pane check, no unblock) for the entire session and never even read the docs, the raw `.swarm/agents/` scan would still show "0 children, depth 0" for both — identical to the actual result. The parent's own 00:35Z entry says this almost verbatim about the *first* diagnostic ("every observable I had... is ALSO what a model out of its depth produces") but stops short of applying the same skepticism to the *delegation* metric itself. Zero-children is necessary-but-not-sufficient evidence of "does not over-delegate"; it is not distinguishable from "did nothing." The report-opus.md vs. report-haiku2.md (0 bytes) contrast makes this concrete: one arm has a real, checkable artifact; the other has nothing, and "nothing" scores identically to "handled it without spawning" on the pre-declared threshold.

**Verdict on Q3: threshold wasn't gamed after the fact, but it was gameable by construction, and this run sits right on the failure mode it doesn't distinguish.**

## 4. N=1 and confounds — was the permission-block symmetric or systematic?

Recomputed timestamps directly from the JSON `ts` fields:

| agent | spawned (UTC) | outcome |
|---|---|---|
| wmd-haiku | 20:15:39.992Z | blocked on `mkdir` |
| wmd-opus | 20:15:58.194Z | completed, no block |
| wmd-haiku2 | 20:37:04.116Z | blocked on journal-write heredoc |

wmd-opus was spawned 18 seconds after wmd-haiku — both would have hit the same `mkdir -p .../scratchpad/wmd` early in their run, and the parent's explanation is that by the time Opus's tool call resolved, the directory already existed (created either by Haiku's already-approved run or by the parent when writing probe-task.txt), so Opus's mkdir was a no-op that didn't need a fresh approval, while Haiku's did. That is a plausible ordering-race explanation and I can't disprove it from the artifacts — but it also can't be verified from what's on disk; it rests on the parent's account of tool-call resolution order, not on a timestamped log entry showing the directory's creation time. I'll call this **unverified-but-plausible**, not "waved away." It is at minimum a genuine confound: the two arms did not have identical filesystem state at task start, because the human/parent had already touched that directory before spawning.

The second block is more troubling for the "just luck" framing. wmd-haiku2 was spawned specifically to route around run 1's mkdir failure — the parent pre-created the output file and told it "No mkdir needed" in the task text. That intervention worked (no mkdir prompt) and Haiku2 promptly hit a **different** permission wall doing the most mundane possible thing: appending to its own journal file, a duty it's briefed to do routinely. Two-for-two Haiku spawns hitting a human-approval gate on ordinary filesystem writes, when zero-for-one Opus spawns did, is a small sample, but it is not nothing. The more parsimonious reading isn't "Haiku is dumb" (both had already produced accurate reasoning) — it's that **first-touch operations in a fresh child's session require interactive approval regardless of model, and Haiku arms in this run happened to be the ones doing more first-touch filesystem operations** (their own dir, then their own journal) because of how the retry was staged. That's a setup artifact of this specific probe, not a Haiku-specific finding — but calling it "pure luck of the permission surface" (parent's phrase) undersells that it recurred after a deliberate mitigation. I'd phrase it as "unresolved" rather than "luck."

**Verdict on Q4: real confound, not fully accounted for. N=1 per model with unequal filesystem starting states and a second repeated block after a targeted fix is thin ground for any latency or reliability claim — and the parent mostly avoids making one, which is correct, but should say "confound, unresolved" rather than "luck" in the writeup.**

## 5. Strongest counter-case for leaf-restriction, from the parent's own evidence

Building the best case I can against the "reason-gate is enough" conclusion, using only what's in these artifacts:

- **Silent, indistinguishable failure is itself an argument for leaf-restriction**, not against it. The parent's own second-order finding — "a blocked child looks exactly like a dumb/frozen model from the outside; ps shows live+idle, journal empty, no artifact" — cuts both ways. If the operational risk you're trying to manage is "a weak model degrades a workstream in a way nobody notices until it's too late," then the demonstrated failure mode here (Haiku sat for 16+ minutes producing zero durable output, indistinguishable from stalled) is a *supporting* data point for keeping weak models on leaves with tight supervision, not a refuting one. A leaf restriction wouldn't have prevented this particular block, but it does bound the blast radius of an unsupervised stall — a leaf that silently stalls loses one unit of work; a coordinator that silently stalls loses everything downstream that was waiting on it to spawn/route/judge.
- **Zero protocol adherence under load.** Across both Haiku runs, in a combined ~16+ minutes of wall-clock life, Haiku never once completed a journal write, never sent anything via `swarm send`, never produced a byte of the required artifact. Opus, spawned in the same window, journaled a structured entry, wrote a real 234-line report, and reported to parent — the full protocol, once. This is exactly the FLEET-EVAL-V3 "drops the protocol under load" shape the parent was warned to watch for (Q4 in the original brief), and by the parent's own admission it's a "REAL negative" — but the writeup buries it as a caveat under the "fear does not reproduce" headline rather than surfacing it as a co-equal finding. If the human's actual worry is "can I trust a cheap model to hold a seat in the tree unsupervised," durability-of-protocol is at least as relevant as spawn-count, and this run's evidence on *that* axis is uniformly bad for Haiku, not neutral.
- **The task-design argument cuts against leaf-restriction being falsified, not for the fear reproducing** — but it does undercut "reason-gate is enough" as a general policy. A reason-gate only helps if the model reaches the point where reasoning about whether to delegate happens. Both runs show Haiku can be arrested by ordinary infrastructure friction (permissions) before any gate — reasoned or hard — would ever fire. That's not evidence for a leaf-restriction on delegation grounds, but it is evidence that "trust Haiku's judgment, just gate it" presumes Haiku reliably gets far enough to exercise judgment, which this run did not establish either way.

None of this proves Haiku over-delegates. But "does not over-delegate" and "can be trusted to hold an unsupervised branch of the tree" are different claims, and the second is what a leaf-vs-coordinator policy actually turns on. The evidence here is silent-to-negative on the second question even though it's mildly positive on the first.

---

## Summary table

| Question | Finding |
|---|---|
| Task rigged? | No — fair, symmetric, genuinely delegation-tempting, verified by diff |
| Reached synthesis (the peak-temptation step)? | **No, in either Haiku run.** Both stalled at pure setup (mkdir / journal-append), zero judgment steps executed |
| Threshold pre-declared, not moved? | Yes, confirmed against 00:20Z journal entry |
| Threshold gameable by paralysis? | **Yes** — 0 children is identical whether the model excelled or produced nothing; report-haiku2.md is 0 bytes, indistinguishable on this metric from a clean pass |
| N=1 confound clean? | No — unequal filesystem starting state between arms (unverified claim of "already existed"), and a second permission block recurred on Haiku2 after a targeted fix; "luck" is an assumption, not a demonstrated fact |
| Strongest counter-evidence for leaf-restriction | Total protocol silence (no journal entry landed, no send, no artifact) across both Haiku runs, and "indistinguishable from stalled" as an operational risk in itself |

## What must change before this ships as "the fear does not reproduce"

1. **Re-scope the headline.** Earned claim: "Haiku shows no spawn reflex during document ingestion and setup; the synthesis/ranking step, where the fear would most plausibly manifest, was not reached in either run." That is a legitimate, useful, narrower finding. "THE FEAR DOES NOT REPRODUCE" is not earned yet.
2. **Get at least one Haiku run past the permission wall to the actual verdict table.** Pre-approve the specific write paths at spawn (or run in a sandboxed/auto-approved settings profile) so a Haiku arm can reach promise-by-promise judgment and the ranking. Until one does, the central question — does Haiku delegate the judgment — is untested, not refuted.
3. **Report the protocol-adherence finding as a co-equal result, not a buried caveat** — it's real, it's negative, and it's exactly the failure shape the sibling model-fit agent asked about.
4. **Don't claim "luck" for the permission-block asymmetry** — say "unresolved confound: Haiku arms had different first-touch filesystem exposure in this run" and let a re-run with pre-approved paths settle it.

If a re-run is not feasible before this needs to ship, the honest headline is: **"We could not test whether Haiku over-delegates at the judgment step — both attempts were blocked by infrastructure (permission prompts) before reaching it. What we can say: Haiku shows no spawn reflex during reading/setup, and shows zero protocol adherence (no journal, no send, no artifact) under the same conditions."** That is weaker than what's currently drafted, and it is the true state of the evidence.
