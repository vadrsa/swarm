# SELF-AUDIT — simplest/swarm vs the SIMPLEST spec

Written last, against the committed file. Line numbers are from `simplest/swarm`
at this commit. Tests: 31/31 pass (`python3 -m unittest test_swarm`).

## Every §2 concept → where it lives

| # | Concept | Where |
|---|---------|-------|
| 1 | Agent = session in a pane + name + parent + journal | binding record written at `swarm:699-701` (agents/<name>.json: name, parent, pane, tab); pane created per agent `swarm:684-694`; journal seeded `swarm:656-658` |
| 2 | The tree (parent judges; operator roots it) | parent recorded at spawn from caller identity `swarm:648` (`my_name()`, `swarm:52`); stated in the spawn header `swarm:574-590` and WORLD.md §2; parent edges drive `relation` `swarm:147` and `subtree` `swarm:408` |
| 3 | `spawn <name> "<task>"`, chosen name, tombstone uniqueness | `cmd_spawn` `swarm:624`; name validated not derived `swarm:637-643`; tombstone claim via `O_CREAT\|O_EXCL` on the journal `claim_name` `swarm:564`, collision error `swarm:651-654`; tombstone survives failed spawn `swarm:724-729` (binding removed, journal kept) |
| 4 | Message = a claim on one turn | send writes one queue file `cmd_send` `swarm:738` (record: to/from/ts/body only, `swarm:769`); ONE per turn, oldest first `select_next` `swarm:184`; delivered whole + sender-headed `build_delivery` `swarm:201`, relation header `relation` `swarm:147`; `delivered/` move ONLY after the stdout drain `deliver_once` `swarm:250` + `emit_hook_output` `swarm:234` (G17 in python: blocking write/flush); one size rule `TURN_CAP=8000` `swarm:32`, refusal `send_size_error` `swarm:217` ("put it in a file, send the path") |
| 5 | The journal, tail re-injected | seeded at spawn `swarm:656-658`; tail cap 4000 + truncation marker `journal_tail` `swarm:275`; re-injection `build_restore` `swarm:288` via `cmd_restore` `swarm:540` (SessionStart, startup + compact) |
| 6 | `ps` — the one view | `cmd_ps` `swarm:785`; pure renderer `render_ps` `swarm:344`: tree, liveness (herdr ground truth `live_pane_set` `swarm:432`), queue depth, idle-since + last words (event fact), "(you)" marker, operator mail at top `swarm:352-358`; unresolvable parent still rendered `swarm:391-404` |
| 7 | `close <name>` — subtree, files stay | `cmd_close` `swarm:801`; subtree walk `subtree` `swarm:408`; deletes nothing, says so `swarm:821` |
| 8 | Judge artifacts, never claims | nothing to point at — by construction: no field anywhere stores acked/read/obeyed/done (see greps below); the only message state is its directory (queued vs delivered) |
| 9 | Duties, briefed unenforced | spawn header text `spawn_header` `swarm:574-590` (journal before idle, report to parent, reconciliation names a falsifier); WORLD.md §9; zero enforcement hooks (settings wire only deliver/event/restore, `swarm:665-671`) |

Hook mechanics required by the brief:
- **deliver** `cmd_deliver` `swarm:494` — one message, oldest first, whole, sender+relation head; move to delivered/ only after drain (`deliver_once` `swarm:250`).
- **event** `cmd_event` `swarm:508` — ONE file per agent `record_event` `swarm:334` (event, ts, last words; overwritten, no history dir). **Stop re-ring** `swarm:523-536`, marked as THE ONE UNPROVEN MECHANISM; wrapped so any failure degrades to pickup-on-next-natural-turn.
- **restore** `cmd_restore` `swarm:540` — original task file + journal tail (4000 hard cap, marker points at full file).
- Inherited mechanisms: atomic tmp+rename `write_atomic` `swarm:80`; task-as-file launcher with status file `write_launcher` `swarm:593`; readiness = launcher signal, ambiguity-is-life `swarm:705-736`; doorbell settle/drain loop `ring_doorbell` `swarm:457`.

## Every §4 deleted concept → grep proving absence

Run from `simplest/`; counts are hits in `swarm`.

| Deleted | Grep | Hits |
|---|---|---|
| ack / inbox verbs, rendered/ state | `grep -cE '\back\b\|inbox\|rendered' swarm` | 0 |
| the nag | `grep -ci 'nag' swarm` | 0 |
| `wait` verb | `grep -cE '^\s*(elif\|if).*"wait"' swarm` | 0 (verb table `swarm:855-873` has spawn/send/ps/close/world + 3 hook entrypoints only; the 3 hits of `\bwait\b` are prose in comments at 459, 525, 697) |
| `reap` | `grep -ci 'reap' swarm` | 0 |
| list/status/graph/children/updates/whoami/parent verbs | dispatcher `swarm:855-873` accepts only spawn/send/ps/close/world + deliver/event/restore. `grep -nE '"(list\|status\|graph\|children\|updates\|whoami\|parent)"' swarm` | 5 hits, none a verb: 4× the stored `"parent"` record field (`swarm:122,362,412,700` — concept 2 requires the parent edge) and 1× the herdr CLI arg `pane list` (`swarm:439`) |
| checkpoint verb/schema | `grep -ci 'checkpoint\|mission\|tasks\[\|blockers\|open_threads\|work_cache\|progress_summary' swarm` | 0 |
| updates/ history | `grep -c 'updates' swarm` | 0; and events are one overwritten file (`record_event` `swarm:334`), no history dir |
| names ledger / slugify / filler words / -2 suffix | `grep -ciE 'ledger\|slugif\|filler\|suffix\|mint' swarm` | 1 — the comment at `swarm:566` saying "no ledger, no suffixing"; a bad name is an error `swarm:637-641`, never transformed |
| message `type` / `read` fields | message record is `{to,from,ts,body}` only (`swarm:769`); `"type"` appears twice — claude settings schema `swarm:666` and transcript block filter `swarm:323`, neither a message field; `"read"` appears once as a herdr CLI arg `swarm:448` |
| semver self-updater | `grep -ci 'semver\|update' swarm` | 0 |
| `--role`, `--self`, `--live-only`, `start` | `grep -c '\-\-role\|\-\-self\|\-\-live-only' swarm` → 0; no `start` verb (dispatcher) |
| question-detection heuristic | `grep -ci 'question' swarm` | 1 — the comment at `swarm:336` saying the taxonomy does not exist; `looksLikeQuestion` logic not ported |
| escalation format | `grep -c 'GOAL:\|EVIDENCE:\|OPTIONS' swarm` | 0 |
| second size number | `grep -c '6000' swarm` → 0; the only caps are `TURN_CAP=8000` (`swarm:32`), `JOURNAL_TAIL_CAP=4000` (`swarm:33`, a restore bound, not a message size), `LAST_WORDS_CAP=500` (`swarm:34`, an event-fact bound) |

## Size

`swarm`: 880 raw lines = 685 code + 68 comment-only + 127 blank (PEP8 double-blank
between defs). Code is inside the brief's 500–700 target; the raw count crosses
the 800 report line and is reported as such, not hidden by reformatting.
Current system for comparison: 2,265 lines across two files, three languages.

## Deviations / additions (all reported, none silent)

1. **`agents/<name>.json`** — a per-agent binding file not named in the brief's
   layout list. Required by §2.1 ("durable name+pane binding") and by ps/close/
   doorbell; without it no pane can be addressed. Not a registry that rots:
   liveness is still derived from herdr on every read, and nothing depends on
   the file ever being pruned.
2. **`event/<name>.json`** — the FACT file the brief's own `event` entrypoint
   requires ("ONE file per agent"); placed in its own dir rather than inside
   settings/ so `ps` reads one predictable path.
3. **Queue-depth trailer** on delivery ("N more waiting") — not in the spec.
   It is a fact about undelivered files, not an unacked reminder; included so
   one-per-turn doesn't hide a backlog from its own recipient. Trivial to
   delete if judged as more.
4. **`spawn` prints a launch-unconfirmed warning** to stderr on readiness
   timeout (ambiguity-is-life, inherited from current spawn).
