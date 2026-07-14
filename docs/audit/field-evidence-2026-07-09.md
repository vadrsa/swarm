# Field evidence — dogfooding the simplest swarm tool — 2026-07-09

> SUPERSEDED by field-evidence-2026-07-10.md and later doctrine docs; kept for the record (the original WATCHLIST-trigger empirical baseline #1-#5).

**Author:** `field-tester` (child of the operator), testing the **installed** tool
(`~/.local/bin/swarm` → `~/.local/share/swarm/bin/swarm`, verified byte-identical to
`bin/swarm` at repo HEAD at test time).

**Method:** live grandchildren as instruments in the real tree (spawned, exercised,
closed); a 1 Hz file poller (`poller.sh`) logging `queue/<name>/`, `delivered/`, and
`event/<name>.json` for the agent under test; pane reads via herdr for turn attribution.
Synthetic experiments, if any, in `SWARM_DIR` sandboxes — the live `.swarm/` was never
hand-edited.

**Evidence classes** (as in the design docs): VERIFIED = observed directly in
output/files reproduced here; MEASURED = derived from timestamps/counts reproduced here;
SUSPECT = inference beyond what the record shows, marked as such.

Verdict key: **TRIGGER FIRED** / **NOT FIRED** / **UNTESTABLE**, per
`docs/design/WATCHLIST.md`.

## Summary of verdicts

| item | verdict | headline |
|---|---|---|
| #3 stop re-ring | **NOT FIRED** | mechanism proven live, twice: delivery ≈3.5–4 s after Stop; idle-sends ≤1 s |
| #5 restore | **NOT FIRED** (restart; compaction untestable today) | deliberate kill+relaunch resumed intent perfectly; spawn/restart injections indistinguishable (noted) |
| #2 turn floods | **NOT FIRED** | zero pure-drain turns observed; agent spontaneously coalesced a burst by hand (see #3 caveat) |
| #4 journal quality | **NOT FIRED** | every reconcile entry sampled carries a command-checkable falsifier |
| #1 senders don't look | **NOT FIRED** (weakly informative) | no drop opportunities in a 1-day fresh tree; recheck after a week of real traffic |

No SIMPLEST FIX is justified by today's evidence. Two contract-level warts surfaced
(details in #3): mid-turn rings degrade to bare "check queue" steering text, and a
cooperative recipient WILL hand-consume its own queue files when nudged — `delivered/`
then lies about turns. Cheapest countermeasure is one sentence in WORLD.md declaring
queue files the tool's job, not the agent's; probe-a obeyed exactly that sentence once
I put it in a message.

---

## #3 — The stop re-ring (the one unproven mechanism)

**Instrument:** grandchild `probe-a` (pane `w4:p33`), spawned 18:44:43Z with a real task
(run `python3 tests/test_swarm.py`, 41 tests, PASS — artifact verified). A 1 Hz poller
logged `queue/probe-a/`, `delivered/`, and `event/probe-a.json` throughout
(`probe-a-poll.log` in the session scratchpad).

### Test 3a — single send to an idle recipient (MEASURED)

probe-a idle since its Stop at 18:46:32Z (event ts 1783622792380). Then:

```
T0 2026-07-09T18:46:59Z 1783622819776
swarm send probe-a "TEST-3a: reply with exactly ACK-1 ..."
T1 2026-07-09T18:47:00Z 1783622820538
```

Queue file `1783622819849-field-tester.json`; by T1+0s it was already in `delivered/`
(dir ctime 1783622820). **Send→hook-delivery latency ≤ 1 s** to an agent idle for 27 s.
probe-a's reply (ACK-1) was queued for me at 18:47:08 — a ~9 s round trip including its
LLM turn.

### Test 3b — burst of 3 sends to an idle recipient (MEASURED + VERIFIED)

Three `swarm send probe-a` back-to-back (B0=1783622872029 … B3=1783622880914; each send
takes 0.7–4.2 s wall, dominated by the doorbell's settle loop). Poller transitions:

```
18:47:52  q=[msg1]              delivered=[3a]
18:47:53  q=[msg2]              delivered=[3a, msg1]     <- msg1 hook-delivered ≤1s
18:47:57  q=[msg2, msg3]        delivered=[3a, msg1]
18:48:44  q=[]                  delivered=[3a, msg1, msg2, msg3]   <- BOTH leave in one tick
```

msg1: hook-delivered ≤ 1 s (one message, one turn — correct). msg2+msg3: their doorbell
rings landed while probe-a was mid-turn; they surfaced as bare `check queue` steering
text **with no hook injection** (VERIFIED in probe-a's pane: *"Two more 'check queue'
nudges arrived without message content attached"*). The files sat queued ~47–51 s while
the turn ran, then **both left the queue in the same poller tick** — because probe-a
read `.swarm/queue/probe-a/*.json` directly, answered both, and ran `mv` into
`delivered/` itself (VERIFIED, pane transcript: `swarm send ... ACK-3 && swarm send ...
ACK-4 && mv .swarm/queue/probe-a/...`).

**Consequence:** the queue was empty by the time probe-a's Stop fired (18:48:50), so the
stop re-ring — the mechanism under test — never got a chance to run. The recipient
bypassed one-per-turn delivery, and `delivered/` now contains two files that were never
injected into any turn: **"delivered" as a record of "consumed a turn" was falsified by
a cooperative agent following the ring's own prompt text** ("check queue" reads as an
instruction to check the queue).

### Test 3d — clean isolation: THE RE-RING FIRED AND WORKED (VERIFIED + MEASURED)

Setup: instructed probe-a to hold a busy foreground turn ~90 s and to ignore any
`check queue` text without touching queue files (it complied — its own words at the
prior stop: *"Per the setup instructions I didn't touch anything under .swarm/queue —
this payload was delivered by the tool itself"*). Its harness blocked a bare foreground
`sleep`, so it kept the turn busy with a Monitor until-loop — same effect.

```
18:55:29.993Z  payload queued (1783623329993-field-tester.json); ring lands mid-turn,
               file confirmed still in queue/ immediately after send
18:55:30 – 18:57:09   poller: file waits in queue the whole busy turn (~99 s)
18:57:08.591Z  probe-a Stop fires (event ts 1783623428591)
18:57:12Z      payload in delivered/ (file ctime 1783623432)
```

**Stop → hook-delivery gap: ≈ 3.5 s.** No external ring existed in that window (my last
send was 18:55:33); the only mechanism that could have submitted the delivering prompt
is the Stop hook's own-pane re-ring. probe-a then sent ACK-6 (received). The one
unproven mechanism is now proven in the live tree, once.

### Test 3c — earlier attempt (backgrounded sleep; extra idle-send datum)

Instructed probe-a to run `sleep 75` and ignore any `check queue` text without touching
queue files. probe-a backgrounded the sleep (its harness's choice), so its turn ended in
23 s and the mid-turn window closed; the payload send at 18:52:53Z hit an idle pane and
was hook-delivered ≤ 1 s (queue already empty on the next `ls`). Another correct
single-send datum; superseded by 3d for the isolation.

### Also observed (SUSPECT, origin unknown)

After the burst drained, one extra `check queue` string sat **unsubmitted in probe-a's
input box**. All four of my sends' rings account for the four submitted prompts, so this
is likely a doorbell retry artifact (`ring_doorbell` types text and presses Enter up to
5×). Harmless here — it was flushed by the next ring — but it shows ring text can strand
in an input box and later submit as an empty-queue turn.

### Mid-turn rings degrade to steering (VERIFIED, both directions)

Symmetrically, on my own pane: probe-a's ACK replies rang me while I was mid-turn; I
received bare `check queue` steering texts and **none of my queued messages were
injected** (files verifiably still in `queue/field-tester/` after three such rings).
Mid-turn, the ring's `UserPromptSubmit` does not fire as a fresh turn; the message
waits. This is the exact window the stop re-ring exists to close.

### Verdict: **TRIGGER NOT FIRED.**

The WATCH condition — queue files older than the recipient's idle period, delivery
degrading to next-natural-wake — was never observed. Measured behavior: send to an idle
agent delivers ≤ 1 s (3 occurrences); a message queued against a busy agent waits (as
designed) and is then delivered by the stop re-ring ≈ 3.5 s after Stop (1 clean
occurrence, 3d — plus a second self-measured occurrence: my own Stop at 19:01:32Z with 5
queued messages was followed by the oldest being hook-delivered at 19:01:36Z, a 4 s
gap). No indefinite-self-ring loop observed (R7 held: after full drains, no
empty-queue ring turns appeared in probe-a's event history — its post-drain stops fired
with q=0 and rang nothing).

Two adjacent facts worth keeping (not #3 triggers, but they shape the contract's edges):
1. **Mid-turn rings degrade to bare steering text** ("check queue" with no injection) —
   the message correctly waits, but the recipient sees an uninterpretable nudge.
2. **A cooperative recipient can bypass one-per-turn** by reading world-readable queue
   files when nudged — and then `delivered/` records turns that never happened. WORLD.md
   says "anyone may read anyone's pane"; it does not say whose job queue files are. One
   sentence in WORLD.md ("never read or move your own queue files — delivery is the
   tool's job") would close it; probe-a obeyed exactly that instruction once given.

## #5 — Post-compaction / restart restore

Forcing a real compaction was not cheaply possible (probe-a's context never ran high),
so per the brief this tests **restart-restore** — the same injection path
(`SessionStart` → original task + 4 KB journal tail), different `source`.

### The experiment (VERIFIED)

Gave probe-a a two-phase task with recorded intent: phase 1 = write `ALPHA` to a file,
journal that phase 2 (`append BETA`) must wait for an explicit `GO`. Once it journaled
that and idled, I killed its session (`/exit` via its pane at 19:00:23Z) and re-ran its
own launcher in the same pane (19:00:41Z). The re-injected prompt contains its ORIGINAL
task — "run the unit tests" — a built-in trap: a floundering agent would redo it.

Post-restart behavior (one turn, ~30 s, journal quoted):

> *"Session restored again. Verified probe-a-phase.txt still contains only ALPHA and
> probe-a-tests.txt still ends with PASS. No GO message from field-tester arrived this
> turn, so I took no phase-2 action. Going idle, awaiting GO."*

- did NOT re-run the tests its re-injected task text ordered;
- did NOT redo or undo phase 1; did NOT act on phase 2 early;
- did NOT ask its parent anything (my queue: no question from it);
- actively re-verified its own artifacts against its journal claims, then waited.

I then sent `GO`; `BETA` was appended within 20 s. **Intent survived the restart, not
just state.**

### Adjacent finding — spawn and restart are indistinguishable to the agent

`build_restore` says "resuming a fresh session" for every non-compact SessionStart —
including the very first startup. All three agents in today's tree (me, hardener,
probe-a) wrote a "resumed after restore" journal entry at what was actually their
initial spawn. Harmless today (nothing to lose at spawn), but it means an agent cannot
tell "I just started" from "I crashed and lost my working memory," and each one burns a
little of its first turn reasoning about a restore that never happened.

### Verdict: **TRIGGER NOT FIRED** (for restart-restore; compaction untested).

The trigger is "more than one agent floundering after restore in the same way." Zero of
one deliberate restart floundered, and the three spawn-time pseudo-restores also
produced correct no-op resumes. The 4 KB tail was more than enough here — probe-a's
whole journal fit inside it; the cap remains ungauged for agents with long journals.
Compaction-source restore (`source=compact`) remains **UNTESTABLE cheaply today** —
recheck when a real agent compacts naturally.



## #2 — Turn floods

**Measurement (probe-a, the busy agent of this session):** 10 messages delivered to it
across ~18 minutes; its turn ledger from pane + events:

| turn | headed by | did real work? |
|---|---|---|
| 1 | spawn task | yes (ran 41-test suite) |
| 2 | TEST-3a message | yes (the message was the work order) |
| 3 | burst msg1 (+2 mid-turn nudges) | yes (answered all three) |
| 4–8 | one message each (3c setup/payload, nap, 3d setup/payload) | yes |
| 9 | TEST-5 phase 1 | yes |
| 10 | restart restore | yes (state verification) |
| 11 | GO | yes (phase 2) |

Zero turns were pure queue-drain: every message-headed turn carried the work the message
ordered. On my side: 6 one-word ACK replies each cost me one full wake-turn — that IS
the one-message-one-turn quantum being paid at its worst rate (one word per turn) — but
each such wake coincided with real audit work I was doing anyway, so no sustained
drain-majority stretch existed for any agent today (my two measured drain deliveries
arrived on turns that also produced evidence-file sections and the restore test).

The nearest thing to the WATCHed failure was self-inflicted and instructive: my burst of
3 caused **probe-a to consume three messages in one turn by hand**, i.e. the system's
one-per-turn quantum was too slow for the traffic I generated, and the agent routed
around it (see #3). That is a data point FOR the fix's shape (coalescing consecutive
same-sender messages) if floods ever become real — the agent invented coalescing
spontaneously.

**Verdict: TRIGGER NOT FIRED.** No sustained queue-drain-majority stretch, no observed
message rationing. Worth rechecking under genuinely chatty multi-agent work (many
siblings reporting to one parent).



## #4 — Journal quality

**Check performed (per WATCHLIST):** read every journal in the live tree
(`probe-a`, `hardener`, my own), looking for falsifiers vs. vibes; checked whether
parents read child journals.

- `probe-a.md`, entry 18:46:13Z (VERIFIED, quoted): *"Falsifier: if probe-a-tests.txt is
  missing, doesn't end with 'PASS', or its tail doesn't match a fresh run of `python3
  tests/test_swarm.py` (should say 'Ran 41 tests' and 'OK'), this entry is wrong."* —
  a concrete, one-command-checkable falsifier, written by a grandchild whose only
  briefing was the spawn header's one sentence about reconciliation entries.
- `hardener.md`, both work entries carry falsifiers of the same shape (VERIFIED,
  quoted): *"Falsifier: `cd /Users/vadrsa/git/swarm-hardening/tests && python3 -m
  unittest test_swarm test_swarm_process` not printing OK/59, or `git -C
  /Users/vadrsa/git/swarm status` showing anything but clean main."*
- Parents reading child journals: I read probe-a's and hardener's journals during this
  audit (this file quotes them — the reads are in my Bash history and this artifact).
  The operator's reading habits were not observable from my seat in this window.

**Verdict: TRIGGER NOT FIRED.** Small sample (3 journals, first day of the new tool),
but every reconcile-shaped entry named a checkable falsifier, and this parent does read
child journals. No status-reports-in-costume observed.



## #1 — Senders don't look

**Check performed:** for every `delivered/` record in the live tree, looked for a trace
in the recipient's journal/work afterward, and for sender follow-up.

- All 10 of my directives to probe-a: delivered, acted on (ACK replies received, artifact
  written, pane transcript matches), and I verified each — but I am the tester; my
  looking is the experiment, not evidence about ordinary senders.
- `hardener` → `operator` report (queue file 1783622829437, 18:47:09Z): in
  `queue/operator/delivered/` within ~1 minute — the human consumed it. Hardener's
  journal then shows it going idle awaiting Task 2 evidence, which is the correct
  follow-up posture for a report (nothing owed).
- No directive anywhere in today's record was dropped, so the trigger condition (a
  dropped directive discovered by someone other than its sender) had no opportunity to
  occur.

**Verdict: TRIGGER NOT FIRED — but weakly informative.** One day of a fresh tree with
two first-level agents, both of them explicitly briefed to be evidence-conscious, is not
the environment this failure grows in. The F4 shape needs directive-heavy, multi-day
traffic. Recommend re-checking after the swarm has run real work for a week.


