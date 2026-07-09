# SELF-AUDIT — simplest/swarm vs the SIMPLEST spec

Written against the post-review amended file (rulings R1–R6 applied; see
"Post-review amendments" below). Line numbers are from `simplest/swarm` at this
commit. Tests: 38/38 pass (`python3 -m unittest test_swarm`).

## Every §2 concept → where it lives

| # | Concept | Where |
|---|---------|-------|
| 1 | Agent = session in a pane + name + parent + journal | binding record written at `swarm:754-756` (agents/<name>.json: name, parent, pane, tab); pane created per agent `swarm:739-749`; journal seeded `swarm:711-713` |
| 2 | The tree (parent judges; operator roots it) | parent recorded at spawn from caller identity `swarm:703` (`my_name()`, `swarm:52`); stated in the spawn header `swarm:629-645` and WORLD.md §2; parent edges drive `relation` `swarm:147` and `subtree` `swarm:463` |
| 3 | `spawn <name> "<task>"`, chosen name, tombstone uniqueness | `cmd_spawn` `swarm:679`; name validated not derived `swarm:692-698`; tombstone claim via `O_CREAT\|O_EXCL` on the journal `claim_name` `swarm:619`, collision error `swarm:706-709`; tombstone survives failed spawn `swarm:779-784` (binding removed, journal kept) |
| 4 | Message = a claim on one turn | send writes one queue file `cmd_send` `swarm:793` (record: to/from/ts/body only, `swarm:824`); ONE per turn, oldest first `select_next` `swarm:184`; delivered whole + sender-headed `build_delivery` `swarm:215` (head + body, nothing else — no trailer, ruling R1), relation header `relation` `swarm:147`; `delivered/` move ONLY after the stdout drain `deliver_once` `swarm:277` + `emit_hook_output` `swarm:252` (G17 in python: blocking write/flush); one size rule `TURN_CAP=8000` `swarm:32`, refusal `send_size_error` `swarm:238` ("put it in a file, send the path") — check equals delivery size exactly, so an accepted message is delivered whole at ANY queue depth |
| 5 | The journal, tail re-injected | seeded at spawn `swarm:711-713`; tail cap 4000 + truncation marker `journal_tail` `swarm:307`; re-injection `build_restore` `swarm:320` via `cmd_restore` `swarm:595` (SessionStart, startup + compact) |
| 6 | `ps` — the one view | `cmd_ps` `swarm:840`; pure renderer `render_ps` `swarm:376`: living tree, queue depth (`+N?` suffix for unparseable files, ruling R4, `count_junk` `swarm:193`), idle-since + last words (event fact), "(you)" marker `swarm:426`, operator mail at top `swarm:391-397`; dead agents compact on one shared name-only line, live children reattach to nearest living ancestor (ruling R5, `swarm:399-459`); herdr unreachable → liveness unknown, never asserted; unresolvable parent still rendered `swarm:451-457` |
| 7 | `close <name>` — subtree, files stay | `cmd_close` `swarm:858`; subtree walk `subtree` `swarm:463`; deletes nothing, says so `swarm:878` |
| 8 | Judge artifacts, never claims | nothing to point at — by construction: no field anywhere stores acked/read/obeyed/done (see greps below); the only message state is its directory (queued vs delivered) |
| 9 | Duties, briefed unenforced | spawn header text `spawn_header` `swarm:629-645` (journal before idle, report to parent, reconciliation names a falsifier); WORLD.md §9; zero enforcement hooks (settings wire only deliver/event/restore, `swarm:720-726`) |

Hook mechanics required by the brief:
- **deliver** `cmd_deliver` `swarm:549` — one message, oldest first, whole, sender+relation head; move to delivered/ only after drain (`deliver_once` `swarm:277`); an undeliverable hand-crafted file (head alone over cap) emits nothing and stays queued, visible in q= (ruling R2, `swarm:287-292`); exit 0 holds even on a broken stdout (ruling R3, `swarm:265-274`).
- **event** `cmd_event` `swarm:563` — ONE file per agent `record_event` `swarm:366` (event, ts, last words; overwritten, no history dir). **Stop re-ring** `swarm:578-591`, marked as THE ONE UNPROVEN MECHANISM; wrapped so any failure degrades to pickup-on-next-natural-turn.
- **restore** `cmd_restore` `swarm:595` — original task file + journal tail (4000 hard cap, marker points at full file).
- Inherited mechanisms: atomic tmp+rename `write_atomic` `swarm:80`; task-as-file launcher with status file `write_launcher` `swarm:648`; readiness = launcher signal, ambiguity-is-life `swarm:760-791`; doorbell settle/drain loop `ring_doorbell` `swarm:512`.

## Every §4 deleted concept → grep proving absence

Run from `simplest/`; counts are hits in `swarm`.

| Deleted | Grep | Hits |
|---|---|---|
| ack / inbox verbs, rendered/ state | `grep -cE '\back\b\|inbox\|rendered' swarm` | 0 |
| the nag | `grep -ci 'nag' swarm` | 0 |
| `wait` verb | `grep -cE '^\s*(elif\|if).*"wait"' swarm` | 0 (dispatcher `swarm:910-933` has spawn/send/ps/close/world + 3 hook entrypoints only; the hits of `\bwait\b` are prose in comments) |
| `reap` | `grep -ci 'reap' swarm` | 0 |
| list/status/graph/children/updates/whoami/parent verbs | dispatcher `swarm:910-933` accepts only spawn/send/ps/close/world + deliver/event/restore. `grep -nE '"(list\|status\|graph\|children\|updates\|whoami\|parent)"' swarm` | 6 hits, none a verb: 5× the stored `"parent"` record field (`swarm:122,407,411,467,755` — concept 2 requires the parent edge) and 1× the herdr CLI arg `pane list` (`swarm:494`) |
| checkpoint verb/schema | `grep -ci 'checkpoint\|mission\|tasks\[\|blockers\|open_threads\|work_cache\|progress_summary' swarm` | 0 |
| updates/ history | `grep -c 'updates' swarm` | 0; and events are one overwritten file (`record_event` `swarm:366`), no history dir |
| names ledger / slugify / filler words / -2 suffix | `grep -ciE 'ledger\|slugif\|filler\|suffix\|mint' swarm` | 1 — the comment at `swarm:621` saying "no ledger, no suffixing"; a bad name is an error `swarm:692-696`, never transformed |
| message `type` / `read` fields | message record is `{to,from,ts,body}` only (`swarm:824`); `"type"` appears twice — claude settings schema `swarm:721` and transcript block filter `swarm:355`, neither a message field; `"read"` appears once as a herdr CLI arg `swarm:503` |
| semver self-updater | `grep -ci 'semver\|update' swarm` | 0 |
| `--role`, `--self`, `--live-only`, `start` | `grep -c '\-\-role\|\-\-self\|\-\-live-only' swarm` → 0; no `start` verb (dispatcher) |
| question-detection heuristic | `grep -ci 'question' swarm` | 1 — the comment at `swarm:368` saying the taxonomy does not exist; `looksLikeQuestion` logic not ported |
| escalation format | `grep -c 'GOAL:\|EVIDENCE:\|OPTIONS' swarm` | 0 |
| second size number | `grep -c '6000' swarm` → 0; the only caps are `TURN_CAP=8000` (`swarm:32`), `JOURNAL_TAIL_CAP=4000` (`swarm:33`, a restore bound, not a message size), `LAST_WORDS_CAP=500` (`swarm:34`, an event-fact bound — see deviations) |

## Size

`swarm`: 937 raw lines = 727 code + 76 comment-only + 134 blank (PEP8
double-blank between defs). Pre-review the file was 880 raw / 685 code; the
review rulings added ~42 code lines (junk counting, compact-dead rendering +
reattachment, the R2 undeliverable branch, the R3 devnull redirect, and their
comments). Code now slightly exceeds the brief's 500–700 target and the raw
count remains over the 800 report line — reported, not hidden by reformatting
(per the designer's standing instruction). Current system for comparison:
2,265 lines across two files, three languages.

## Deviations / additions (all reported, none silent)

1. **`agents/<name>.json`** — a per-agent binding file not named in the brief's
   layout list. Required by §2.1 ("durable name+pane binding") and by ps/close/
   doorbell; without it no pane can be addressed. Not a registry that rots:
   liveness is still derived from herdr on every read, and nothing depends on
   the file ever being pruned.
2. **`event/<name>.json`** — the FACT file the brief's own `event` entrypoint
   requires ("ONE file per agent"); placed in its own dir rather than inside
   settings/ so `ps` reads one predictable path.
3. **`SWARM_READY_TIMEOUT`** env var (`swarm:760`, default 30s) — the spawn
   readiness window, inherited from current `bin/swarm`; an env knob, not a
   concept.
4. **`help` verb** (`swarm:911`: bare/`-h`/`--help`/`help` print usage) — usage
   text only; not a view, adds no concept.
5. **Reserved names** `operator` and `delivered` (`swarm:695-696`) — `operator`
   is the root's address, `delivered` would collide with the queue subdir.
6. **`LAST_WORDS_CAP=500`** (`swarm:34`) — bounds the stored event-fact
   `last_words` so the fact file cannot grow unboundedly; a storage bound, not
   a message-size number.
7. **`spawn` prints a launch-unconfirmed warning** to stderr on readiness
   timeout (ambiguity-is-life, inherited from current spawn).

(The queue-depth trailer, formerly deviation 3, was DELETED per ruling R1.)

## Post-review amendments (REVIEW.md findings → rulings → regressions)

| Finding | Ruling | Change | Regression test |
|---|---|---|---|
| 1 (queue-depth trailer) | R1: delete | trailer removed; delivery is head+body only | `test_no_queue_depth_trailer_ever` |
| 2 (pessimism hole at depth ≥100) | mooted by R1 | send check now equals delivery size exactly | `test_boundary_size_message_delivered_whole_at_depth_150` |
| 3 (bare-header silent drop) | R2: never deliver | `build_delivery` returns None; file stays queued, nothing emitted, nothing moved | `test_undeliverable_file_stays_queued_and_emits_nothing`, `test_undeliverable_returns_none_never_bare_header` |
| 6 (exit 120 on broken stdout) | R3: make exit-0 true | fd 1 re-pointed at /dev/null after a failed drain | `test_deliver_exits_zero_on_broken_stdout` (process-level) |
| 8 (corrupt queue file invisible) | R4: count it | `count_junk` + `q=N+M?` suffix in ps | `test_corrupt_queue_file_counted_not_hidden` |
| 7 (ps grows monotonically) | R5: compact dead | dead agents render name-only on one shared line; live children reattach to nearest living ancestor | `test_dead_agents_render_compactly`, `test_live_child_of_dead_parent_reattaches` |
| 4 (undisclosed micro-additions) | R6: disclose | deviations 3–6 above | — (disclosure) |
| 5 (design doc vs flags) | designer's own | no code change | — |
