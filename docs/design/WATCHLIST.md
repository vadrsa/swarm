# WATCHLIST — what to keep an eye on in SIMPLEST, and the simple fix if it bites

**Author:** `simplest`. **Companion to** `docs/design/SIMPLEST.md` (its §6 falsifiers, made
operational). Untracked, like the design. Each entry: the observable to WATCH, how to CHECK it
cheaply, the TRIGGER that means it is real, and the SIMPLEST FIX consistent with the design —
sized so that applying it never reopens the concept count by more than it must.

Rule of use: check on evidence, not on schedule — most of these are checkable in one command
the moment you suspect them. None of the fixes should be built preemptively; every one is a
concept or a mechanism, and §8 of the philosophy applies: it earns its way in only when the
record shows the convention failing.

---

## 1. Senders don't look (the design's central bet — relocated F2)

- **WATCH:** a directive whose `delivered/` file is older than one of the sender's
  reconciliation cycles, with no trace in the recipient's journal or artifact afterward, and
  the sender's journal showing no follow-up.
- **CHECK:** pick any directive you sent yesterday; `ls -la .swarm/queue/<child>/delivered/`
  for the timestamp, then read the child's journal entries after it. As operator: spot-check
  one parent's journal for whether its reconcile entries mention checking sent mail at all.
- **TRIGGER:** a dropped directive discovered by anyone *other than its sender* (the F4 shape
  recurring). One occurrence is the trigger — this is the failure the whole design bets
  against.
- **SIMPLEST FIX:** a `ps --sent` view: your own sent messages with delivered-at timestamps
  and a `journal-touched-since: yes/no` column derived from the recipient's journal mtime.
  Sender-side instrument, zero recipient-side machinery — do NOT reintroduce the nag; the nag
  was tried and its absence read as compliance.

## 2. Turn floods (one-message-per-turn is the wrong quantum)

- **WATCH:** agents whose turns are mostly message-consumption instead of work.
- **CHECK:** count delivery-headed turns vs. total turns in a busy agent's transcript (same
  measurement method as the design's verb count).
- **TRIGGER:** a sustained stretch where queue-drain turns are the majority for any agent, or
  a sender visibly rationing messages it should have sent.
- **SIMPLEST FIX:** coalesce *consecutive messages from the same sender* into one turn — one
  bounded exception, no priority tiers, no batching flags. Different senders never share a
  turn (that is the co-injection failure coming back).

## 3. The stop re-ring stalls (the one unproven mechanism)

- **WATCH:** messages waiting on an idle recipient. Also the inverse failure, found by the
  implementation review: the ring must fire only when the queue's HEAD is *deliverable* —
  a ring on mere non-emptiness plus an undeliverable head is an indefinite self-ring loop
  burning turns unattended (ruled fixed as R7; the regression test is the instrument).
- **CHECK:** `ps` — any agent idle longer than its oldest queued message has existed. One
  line of shell over `queue/` mtimes vs. the last-event timestamp.
- **TRIGGER:** queue files repeatedly older than the recipient's idle period; delivery
  degrading to "whenever it next wakes."
- **SIMPLEST FIX:** first, fix the contract, not the code — change WORLD's wording from
  "promptly" to "on its next turn" so the promise matches reality (a false sentence is the
  worse bug). If prompt delivery is genuinely needed, the re-ring's retry belongs in herdr
  (the thing that owns panes and timers), not in a daemon bolted onto the CLI.
- **RESIDUAL (2026-07-10):** the Stop-path ring is a single attempt with no settle/confirm
  loop (the loop blocked a busy pane ~3m — field evidence 2026-07-10, finding 1), so under
  load the ring may be skipped and pickup waits for the next natural turn — delayed, never lost.

## 4. Journals rot into mush (free text was too free)

- **WATCH:** whether parents actually read child journals, and whether entries carry
  falsifiers or just vibes.
- **CHECK:** measure reads the way the design measured verbs (journal paths appearing in
  parents' Bash calls); skim three reconcile entries from any agent — do they name evidence
  that would show off-track?
- **TRIGGER:** parents demonstrably not reading journals (allowed-and-never-used — the F3
  test inverted), or reconcile entries that are status reports wearing a costume.
- **SIMPLEST FIX:** seed each journal at spawn with a 3-line entry template (goal / off-track
  if / checked+verdict) — a convention made visible in the file itself, not a schema, not
  validation. If parents still don't read them, the design's §6 falsifier 4 has fired and the
  structured checkpoint deserves reconsideration — say so honestly rather than patching.

## 5. Post-compaction floundering (4KB tail is too thin)

- **WATCH:** agents that restore and then re-ask their parent what they were doing, redo
  finished work, or contradict their own journal.
- **CHECK:** read the first few turns after any SessionStart(compact) against the agent's
  last pre-compaction journal entries.
- **TRIGGER:** more than one agent floundering after restore in the same way.
- **SIMPLEST FIX:** in order of cheapness — (a) brief agents to write a dense "note to my
  amnesiac self" entry when context runs high; (b) raise the tail cap; (c) inject the last
  *reconcile* entry specifically (it has the goal + falsifier shape) plus the tail. All three
  are parameter changes, not concepts.

## 6. Operator-bound questions stay malformed (the stall comes back)

- **WATCH:** questions in your queue you cannot decide from their own text; your own
  answering latency as the proxy.
- **CHECK:** you know it when you stall. Secondary: count how many waiting messages carry a
  recommendation and a default.
- **TRIGGER:** malformed questions still arriving weeks after you started returning them
  unanswered (the convention has failed in the record, G14-style).
- **SIMPLEST FIX:** a `swarm ask` wrapper verb that refuses to send to the operator without
  the three elements (decision / recommendation / default-or-must-wait). One verb, template
  enforcement at the source, only for the operator target. Until that trigger fires: return
  bad questions, ten seconds each — the convention needs your verdicts to hold.

## 7. Scope creep in the rewrite itself (the disease that built the 27)

- **WATCH:** the new tool growing verbs, flags, fields, or states the design does not name.
  Every concept in the current system was added by someone with a reason that sounded local
  and sane.
- **CHECK:** the reviewer's concept recount at review time; after that, diff `--help` output
  against the design's §2 whenever the file changes.
- **TRIGGER:** any addition that cannot point to a WATCHLIST entry whose trigger fired.
- **SIMPLEST FIX:** this file is the fix. An addition with no fired trigger behind it gets
  reverted, and the urge behind it gets written here as a new entry with a falsifier instead.

## 8. The shared-tree hazard, still out of scope but still real (G13)

- **WATCH:** two agents mutating one checkout; an agent's uncommitted work destroyed by a
  sibling's git operation. The rewrite does not fix this — it was ruled not-this-tool's-job,
  and the implementation was built in an isolated worktree for exactly this reason.
- **CHECK:** `git -C <repo> worktree list` vs. `ps` — more than one live agent with the same
  cwd doing write-work is the exposure.
- **TRIGGER:** the third lost-work incident (there have been two shapes of it already).
- **SIMPLEST FIX:** convention in the spawn brief — writers get `--cwd` pointed at their own
  worktree, created by the spawner. If that convention fails in the record, the earned
  mechanism is spawn creating the worktree itself — a real scope change; take it to the
  operator as a decision, not a patch.
