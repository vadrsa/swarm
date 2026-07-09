# REVIEW — simplest/swarm vs docs/design/SIMPLEST.md

**Reviewer:** `review-simplest` (no stake in design or implementation). **Method:** execute,
never infer — I ran the shipped suite (31/31 pass, reproduced), then wrote and ran 22 tests of
my own at process level (real `swarm` subprocesses against fixture `.swarm/` trees, a fake
`herdr`, a fake `claude`, and a real broken-pipe stdout). My suite:
`/private/tmp/claude-501/-Users-vadrsa-git-swarm/760d36ec-d7c8-451c-a899-e32d20eb57c5/scratchpad/review_tests.py`
— 22/22 pass. Every SELF-AUDIT grep re-run; every cited line number spot-checked; the size
claim recounted exactly (880 raw = 685 code + 68 comment + 127 blank).

## Verdict

**PASS** — all 9 concepts exist and behave per §2/§3 under execution, nothing on the §4
NOT-list survives any grep or the dispatcher, and the findings below are edge-depth defects
and disclosure gaps, none breaching a load-bearing mechanism.

## What I executed (presence pass, all VERIFIED)

- **Delivery is one-per-turn, oldest-first, whole, sender+relation-headed** — CLI round-trip:
  queue file → `swarm deliver` (real process, stdin payload) → stdout JSON contains body +
  "from boss" header → file moved to `delivered/`. Tie-break, junk files, and delivered/
  exclusion covered by the shipped suite (re-run, pass).
- **The delivered/ move is drain-conditional (G17)** — I ran `swarm deliver` with stdout a
  pipe whose read end was already closed: flush raises EPIPE inside the real process, **the
  file does NOT move**, and next delivery offers it whole. The safe direction holds under a
  real failed write, not just a mocked one.
- **Spawn** — with a fake herdr + fake claude: tombstone claimed first; journal seeded with
  task; settings wire exactly deliver/event/restore/notification hooks; task file carries the
  duties header (journal-before-idle, report-to-parent, falsifier); binding record written
  before readiness; launcher status reached "launching"; `spawn` printed the name. Collision
  on reuse errors ("already used"). **Confirmed-failure teardown**: no claude on PATH →
  status "failed: claude not found" → tab closed, binding removed, **tombstone kept**, name
  still burned. Refusals (bad names, reserved names, outside herdr) all happen **before** the
  claim — a refused spawn does not burn the name.
- **Send** — `--stdin` preserves bytes exactly (backticks, `$()`, quotes, multibyte,
  newlines); oversize refused with "put it in a file, send the path" and **nothing queued**;
  unknown agent refused; operator target never refused, never doorbelled; doorbell failure
  prints the durably-queued note and the message survives.
- **Stop re-ring (the one unproven mechanism)** — executed both branches: queue non-empty →
  fake herdr log shows `pane send-text <own pane>`; queue empty → no ring. Failure is wrapped;
  the queue file is durable either way. Live-pane reliability remains untested per both briefs
  — this is §6.3's open bet, correctly marked in code (swarm:523–528).
- **Restore** — real `swarm restore` with source=compact: original task + journal tail, tail
  hard-capped at 4000 with a marker naming the full path, compaction named in the preamble.
- **Event fact** — one file, overwritten, no history dir; last words extracted from a real
  transcript fixture, whitespace-collapsed, 500-char cap.
- **ps** — operator mail on top oldest-first; tree indentation; `(you)`; q=; idle-since; last
  words; herdr unreachable → `[?]` + "liveness unknown", **never** asserted DEAD; orphaned
  parent still rendered flat.
- **close** — subtree only (fake herdr log shows exactly the subtree's tabs closed, sibling
  untouched); every file stays and the tool says so.

## Findings, ranked

1. **[MORE] The queue-depth trailer** — `(one message per turn; N more waiting in your
   queue)` on every delivery with a backlog (swarm:196–198). The design promises "no unacked
   count" (§1) and deleted the nag (§4 row 1). This is not that — it counts *undelivered*
   files (a filesystem fact `ps` already shows), appears only on delivery turns, and names no
   ids — but it is a standing recipient-side reminder line the design does not name.
   Disclosed as deviation 3 in SELF-AUDIT with "trivial to delete if judged as more." It is
   the one addition that needs a designer's ruling, not a reviewer's. VERIFIED (test).
2. **[WRONG] "Delivered whole" has a 1-char-per-digit hole at queue ≥ 100** —
   `send_size_error` (swarm:217–231) checks against a pessimistic `more=99` trailer; with 100+
   messages waiting the real trailer is longer, so a message accepted at the exact boundary is
   delivered **truncated**, violating §2.4/WORLD.md "delivered whole." Demonstrated:
   `test_trailer_pessimism_hole_at_100_waiting` — accepted by send, `[truncated` on delivery.
   Requires a ≥100-deep queue and a body within ~1 char of the 8000 cap. VERIFIED, edge-depth.
3. **[WRONG] The `room <= 0` truncation branch drops a body silently** — a hand-written queue
   file whose `from` field alone exceeds the cap is delivered as bare header with **no
   truncation marker** (swarm:211–212), and the file still moves to `delivered/`. WORLD.md
   promises "Nothing is ever silently dropped." Unreachable via `send` (which caps the whole
   record); reachable only by hand-crafted files. Demonstrated:
   `test_giant_from_field_silently_drops_body`. VERIFIED, hand-crafted-input only.
4. **[MORE] Undisclosed micro-additions** — the SELF-AUDIT deviations list (its own contract:
   "all reported, none silent") misses: `SWARM_READY_TIMEOUT` env var (swarm:705), the `help`
   verb (swarm:854), the reserved-name list `operator`/`delivered` (swarm:640–641), and
   `LAST_WORDS_CAP=500` (swarm:34; greppable in its §4 row but absent from the deviations
   table). All are defensible plumbing; the failure is disclosure, not design. VERIFIED (read).
5. **[MORE] `--model`, `--cwd`, `--stdin` are in the code and the implementer's brief but not
   in the design doc** — SIMPLEST.md §2.3/§2.4 name bare `spawn <name> "<task>"` and
   `send <name>`; the brief (written by the designer) sanctions the flags. Not an implementer
   error — a doc/brief discrepancy the designer should reconcile so the design doc stays the
   single source of "everything, not more." VERIFIED (both documents read).
6. **[WRONG] `deliver` exits 120, not 0, when stdout is a broken pipe** — the comment at
   swarm:496 promises "any error -> exit 0", but after `sys.exit(0)` the interpreter's own
   exit-flush of the broken stdout fails and Python exits 120. The behavioral half that
   matters holds (file stays queued, verified); only the exit-code promise is false.
   Demonstrated: `test_cli_deliver_failed_write_file_does_NOT_move`. VERIFIED, trivial.
7. **[MORE, observation] `agents/` is a registry the design said would not exist** — §4's
   reap row argues "there is nothing to prune because there is no registry to rot."
   `agents/<name>.json` is a durable, never-pruned registry of bindings (disclosed, deviation
   1, and genuinely required by §3.1's "durable name+pane binding"). Liveness is still derived
   from herdr per read, so it cannot rot into *wrong* — but `ps` output grows monotonically:
   every agent ever spawned renders forever, dead ones at full line width, with no pruning
   verb by design. A long-lived swarm's "one view" gets tall. Consequence of the design,
   faithfully implemented; the designer should own the sentence rather than the reap row's
   "renders the dead compactly." VERIFIED (code + close test: record survives close).
8. **[SUSPECT, observation] A corrupt queue file is invisible everywhere** — a non-JSON file
   in `queue/<name>/` is skipped by selection, excluded from `q=` counts, and never surfaced
   by any view; it sits on disk unseeable except by `ls`. Consistent with "never delivered ≠
   dropped," and unreachable via `send` (atomic JSON writes) — but a crashed writer could
   strand one. Demonstrated skip-behavior: `test_corrupt_queue_file_is_skipped_not_fatal`;
   the "could strand" half is my judgment, hence SUSPECT.

## Fidelity spot-checks (SELF-AUDIT as a claims document)

Every §2 row's cited lines match the shipped file (spot-checked: 32, 234, 250, 344, 408, 564,
648, 769, 801, 824). Every §4 grep re-run from `simplest/` reproduces the claimed hit counts,
including the three prose-only `wait` hits and the five non-verb `parent`/`list` hits. The
"31/31 pass" claim reproduces. The size row is exact. The task-as-file launcher matches the
current `bin/swarm` mechanism precisely (`PROMPT="$(cat file)"` then positional to claude —
same as bin/swarm:469,478; "never on argv" means herdr's argv, and that holds: herdr sees
only the launcher path — verified in the fake-herdr call log). Atomic tmp+rename is used at
every inter-process handoff (queue, agents, event, settings, task); the launcher script and
journal seed are single-writer-then-read, where atomicity is not load-bearing. WORLD.md is 54
lines (two screens), and read hostilely its four promises survive: "delivered means
delivered" and "offered whole again next turn" I verified under a real failed write;
"promptness is best-effort" and "operator is a mailbox" claim nothing the code must keep;
"nothing silently dropped" is qualified only by finding 3's hand-crafted edge.

## Concept recount

Independent count of what an agent must understand to use what was actually built: **9** —
agent (name/parent/pane/journal), the tree with the operator at root, spawn + tombstone
collision, message-as-claim-on-one-turn (queue file, oldest-first, sender+relation header,
8000-or-send-a-path, `delivered/`), journal + tail-restore, `ps`, `close` (subtree, files
stay), judge-artifacts, duties. The queue-depth trailer and the positional-body-is-a-shell-word
caveat are sub-facts of the message concept, not new concepts — neither will *surprise* an
agent that knows concept 4. Plumbing (`agents/`, `event/`, `settings/`, the env vars) is set
up for the agent and never needs understanding to act correctly. The 27 → 9 claim holds for
the artifact as built.
