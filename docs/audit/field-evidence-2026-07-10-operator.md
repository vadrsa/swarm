# Field evidence — operator-capabilities probes PR-A and PR-B — 2026-07-10

**Author:** `field-tester`. Spec: `.swarm/briefs/operator-capabilities-proposal.md`
(FINAL, post-adversarial-review). Evidence classes VERIFIED / MEASURED / SUSPECT.

## PR-A — warm-name reuse (validates F3 / rung 0), BASELINE

**Question:** given a coordinator holding one idle capable prior child, does the same
task shape dispatched again reuse the warm name or respawn — under the *installed*
doctrine (delegation v2; rung 0 exists in no header today)?

**Protocol:** `warm-coord-1` spawned 16:48:33Z (installed binary) with a brief that
constructs the precondition: spawn ONE child for the first task, verify its artifact,
keep the child alive ("more tasks may follow"). Task 1 (summarize REVIEW.md) → it
spawned `warm-worker-1`, briefed as a *persistent summary worker* — a capability-shaped
name. Task 2 (same shape, different doc, **zero structural guidance**) sent 16:51:05Z.

**Result: REUSE (VERIFIED).** Task 2 was routed to `warm-worker-1` as a message
(observed in the child's `delivered/` within seconds; no new agent record ever
appeared). The coordinator had *pre-planned* the reuse before task 2 existed (journal
at task-1 verdict: *"I'll route follow-up summaries to it"*), and named the economics
at dispatch: *"Sent to warm-worker-1 (this is why I kept it alive — no new spawn
needed)."* Both artifacts verified by the coordinator against full sources before
DONE; both DONE reports carried real verification detail.

**Verdict: rung 0 codifies an instinct that already exists.** Confound stated
honestly: my brief planted "more tasks may follow," which made keeping the child warm
(the precondition) also a hint of recurrence; the *reuse-vs-respawn* decision itself,
though, got no guidance. The scarcer half of rung 0 in practice is warm names
*existing at all*: the delegation doctrine's close-rule ("keep a child only if you can
name its next task") makes unprompted agents close eagerly (MEASURED: the heavy
delegation probe closed all four children on harvest). Rung 0's useful work is naming
recurrence as a legitimate "next task."

## PR-B — two-hand probe (gates P6b; exercises F5), sandbox

**Setup (all in `SWARM_DIR=/tmp/swarm-sandbox-2h`, live `.swarm/` untouched):**
seeded operator journal with standing goal G1 ("ship the widget by Friday; priority:
correctness over speed"); 3 mails queued to the sandbox operator from distinct senders
(widget-team, deploy-bot, qa-team), each requesting a tiny verifiable desk action. Two
unnamed claude sessions ("hands") launched simultaneously in herdr panes over the
sandbox (no SWARM_AGENT_ID → operator identity), each briefed with: seat-take entry
with hand tag; F5 claim discipline (move file to delivered/ → journal hand-tagged
claim line → only then act); one goal restatement of G1 with a hand-specific change
(A: deadline→Thursday; B: priority→speed); hand-B additionally briefed to claim the
qa-team mail with a 90 s pause between move and claim line — the kill window.

### What happened (journal + files, VERIFIED)

```
20:52:40  [hand-B] SEAT-TAKE
20:52:50  [hand-B] CLAIM deploy-bot.json      (move→claim→act: clean)
16:52:52Z [hand-A] SEAT-TAKE
16:53:01Z [hand-A] CLAIM widget-team.json     (move→claim→act: clean)
20:53:23  [hand-B] GOAL RESTATEMENT: Friday, priority now SPEED over correctness
16:53:28Z [hand-A] GOAL RESTATEMENT: THURSDAY, correctness over speed   <- 5 s later,
                                                     neither entry cites the other
16:53:37Z [hand-A] STINT END — and it flags, unprompted: "the journal now contains
          two divergent G1 restatements … a coordinator will need to reconcile"
20:53:38  qa-team.json moved to delivered/ by hand-B (claim started)
20:53:47  hand-B's pane KILLED by me — 9 s into its 90 s pause; no claim line, and
          the qa desk action never happened (desk/qa-status.txt absent)
```

Both clean claims were executed in the correct order; both desk actions verified
(`widgets: 42`, `deploy: saturday`).

### Verdict 1 — does newest-wins lose an update? **YES (Race 3 FIRED, harmlessly).**

Two G1 restatements landed 5 s apart, neither citing the other. The true merged state
(Thursday AND speed-over-correctness) exists in **no single entry**; a newest-wins
reader takes hand-A's and silently loses hand-B's priority flip. P6b's held amendment
("restatements must cite what they supersede; reading is a grep idiom") earns its
evidence. Mitigating observation: an attentive hand caught the divergence at stint
end and *flagged* it rather than resolving it — detection is natural, resolution
still needs the convention.

### Verdict 2 — do claim lines make a crash visible? **YES (alarm fires, one loop).**

```
for f in delivered/*.json: grep "CLAIM <basename>" journal/operator.md
OK    1783702200933-widget-team.json
OK    1783702201988-deploy-bot.json
ALARM 1783702203041-qa-team.json — delivered but NO claim line
```

The killed hand left exactly the predicted fingerprint: a delivered file with no
claim line, and the mail's requested action absent. Without the claim-line convention
this mail would read as *handled* (it sits in `delivered/`) while nothing happened —
F5's keystone works as designed.

### Incidentals

- The two hands wrote different timestamp formats (local vs UTC-Z) into the shared
  journal — harmless here, but a grep idiom over hand entries should not assume a
  format (the recurring journals-timestamp-as-claims theme).
- Concurrent appends interleaved cleanly (whole lines, no corruption) — POSIX append
  semantics carried the two-writer journal without machinery.
- During the stint, a prompt appeared in hand-A's pane that I did not send
  ("reconcile the two G1 restatements") — consistent with the human operator
  interacting live; that pane was left open, unsubmitted prompt intact.

## Cleanup

PR-A subtree closed (`warm-coord-1`, `warm-worker-1`; artifacts in session
scratchpad `warm-1/`). PR-B: hand-B's tab closed by the kill (that was the
experiment); hand-A's tab left open for the operator; sandbox
`/tmp/swarm-sandbox-2h` left intact for inspection (journal, delivered/, desk/).
