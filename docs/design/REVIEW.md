# REVIEW — simplest/swarm vs docs/design/SIMPLEST.md

> SUPERSEDED by absorption into shipped `bin/swarm` (review of the `simplest/swarm` prototype); kept for the record (the evidentiary trail behind SELF-AUDIT.md's R1–R6 fixes — queue-depth trailer, truncation hole, broken-pipe exit code).

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

---

# ADDENDUM — targeted re-check of rulings R1–R6 (2026-07-09)

**Scope:** the five amended behaviors at `simplest-impl` HEAD `780b4ef`, per `simplest`'s
request. The original review above examined `d98213c` and stays true of it. Commit
provenance confirmed: `780b4ef` is code-identical to the implementer-reported `5bdf2eb`
(`git diff 5bdf2eb 780b4ef -- simplest/swarm simplest/test_swarm.py` is empty; the amend only
evicts two `.pyc` files, adds `.gitignore`, and commits this REVIEW.md). **Method unchanged:**
their amended suite re-run under my own hand — **38/38 pass**; my original 22-test suite
re-run — exactly the 3 finding-demonstration tests now fail; plus a new 10-test targeted
suite, **10/10 pass**:
`/private/tmp/claude-501/-Users-vadrsa-git-swarm/760d36ec-d7c8-451c-a899-e32d20eb57c5/scratchpad/addendum_tests.py`

Because my finding-2 and finding-3 tests died on the *removed API* (`delivery_parts` gone,
`build_delivery` re-signatured) — an incidental reason — I did not accept those failures as
proof; each ruling below was re-verified against the new behavior directly.

## Per-item verdicts

1. **R1, trailer gone / delivered whole at any depth — PASS.** `grep -c 'more waiting' swarm`
   → 0. Executed: a boundary message (head+body = exactly 8000) with **150** messages queued
   behind it is accepted by send's check and delivered by `deliver_once` at exactly 8000
   chars, ending at the body's last byte — no truncation marker, no trailer, file moved to
   `delivered/`. The size check now measures precisely what delivery injects
   (`send_size_error` = `delivery_head` + body, swarm:227–238), so "delivered whole" is
   unconditional, not pessimistically approximated. My finding-2 hole is closed by
   construction, not by widening a margin.
2. **R2, undeliverable file — PASS, and the blocking call is the right one, with one hazard
   to own.** Executed: a hand-crafted record whose header alone exceeds the cap → `deliver_once`
   emits **nothing** (my emit callback would have failed the test if called), moves nothing,
   and the file stays counted in q=. A good message queued behind it is not delivered — the
   deliberate block. **Judgment:** consistent. One-per-turn *oldest-first* is the design's
   ordering promise; silently skipping the head would make delivery order lie, and the old
   bare-header alternative moved a file to `delivered/` whose content never arrived — the
   exact class of false claim this design exists to kill. Never-delivered ≠ dropped, and the
   file is visible. **The hazard (SUSPECT, components demonstrated):** while such a file heads
   a queue, every Stop sees a non-empty queue and re-rings, and every rung turn delivers
   nothing — an indefinite self-ring loop burning turns until a human deletes the file. Both
   components verified (select_next stays non-empty; deliver_once stays False); the live loop
   itself is pane behavior I did not run. Reachable only by a hand-crafted write. Worth one
   sentence in WORLD.md or a `ps` marker on an undeliverable queue head; the designer should
   own it, not the implementer.
3. **R3, broken stdout — PASS.** Process-level with a real closed-read-end pipe: exit code is
   now **0** (was 120) and the message file still does not move. The fd-1-to-/dev/null
   re-point (swarm:265–274) does exactly what the commit claims. My finding-6 test fails
   precisely on `rc == 120` with rc now 0 — the right reason.
4. **R4, junk counted not hidden — PASS.** A non-JSON `.json` file in the queue renders as
   `q=1+1?` at the CLI level (real `swarm ps` subprocess) and via `count_junk` = 1; selection
   still skips it and delivers the good message. No junk → no suffix. My finding-8
   "invisible" observation is resolved: the unknown is now shown as an unknown.
5. **R5, dead compact / reattach — PASS.** Pure-renderer tests: dead agents collapse to ONE
   shared `dead: a, b` line, names only (no q=, no [DEAD] tokens); a live child of a dead
   parent reattaches to its nearest **living** ancestor (verified two ways: dead parent at
   root → child renders at root depth; dead middle of a three-deep chain → leaf renders
   nested under the live grandparent, and `dead: mid`); herdr-unreachable still renders
   every agent `[?]` with **no** dead line — liveness is never asserted without ground truth.
6. **R6, disclosures — PASS.** The deviations table now lists `SWARM_READY_TIMEOUT`
   (swarm:760), the `help` verb (swarm:911), reserved names `operator`/`delivered`
   (swarm:695–696), and `LAST_WORDS_CAP` (swarm:34) — all four citations spot-checked against
   the amended file and exact. The trailer's former deviation entry is marked deleted. The 7
   new shipped regression tests cover findings 1, 2, 3, 6, 8 and both R5 behaviors.

## Addendum verdict

**PASS.** All five amended behaviors do what the rulings say under execution; the disclosure
gap is closed. Open items for the designer, unchanged from the original review: finding 5
(design doc vs brief on `--model`/`--cwd`/`--stdin`), finding 7 (the `agents/` registry
sentence — R5 fixes the *rendering* consequence; the never-pruned records remain, now
costing one shared line), and the R2 self-ring hazard above. Concept recount unchanged: 9 —
R1 removed the one borderline sub-fact; R4's `+M?` suffix is `ps` showing a fact, not a new
concept. I fixed nothing.
