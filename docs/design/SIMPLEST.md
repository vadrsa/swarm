# SIMPLEST — a clean-slate representation of swarm

**Author:** `simplest`, clean-slate designer, contracted from outside the org. Reports to the
operator only. **Written at** `main@54a0b63`, 2026-07-09. Untracked by instruction; not code.

**Evidence discipline:** claims are marked **VERIFIED** (I read the line / ran the command),
**MEASURED** (my own instrumentation, method stated), or **SUSPECT** (my judgment). Inputs read
in full: COHERENCE-FINDINGS.md, PHILOSOPHY.md, WORLD.md, bin/swarm (1694 lines),
bin/swarm-hook.cjs (571 lines), flows-as-they-are.md, AUDIT-MAP.md. PRDs/proposals skimmed as
instructed. I wrote no code and ran no prototypes; every mechanism this design keeps is already
running in production here, and the one mechanism it adds is flagged as such (§6).

---

## 1. THE CORE

An agent is a Claude session in a pane, with a **name**, a **parent**, and a **journal**. Four
verbs: `spawn`, `send`, `ps`, `close`.

A **message is a claim on one turn**. `send` writes a file to the target's queue; the hook
delivers **exactly one message per turn**, whole, headed by its sender and the sender's relation
to you. Delivery moves the file to a world-readable `delivered/`. There is no ack, no nag, no
unacked count: the system stores only what a file can witness — *delivered* — and *obeyed* is
judged the way all work is judged: the sender reads the recipient's reply, pane, or artifact.

The **journal** is each agent's append-only, timestamped working memory, in its own words. Its
tail is re-injected after compaction or restart. Anyone can read anyone's journal, so freshness
and trajectory are observable facts, not self-claims.

`ps` shows the whole society as a tree: name, parent, alive, queue depth, idle-since, last
words — and the operator's own waiting mail. The **operator** is a name you can send to; his
queue drains only when the human looks. Stated plainly, promised nowhere.

Everything else is deleted.

*(198 words.)*

---

## 2. THE CONCEPT COUNT

### The current system: 27 concepts

Counted honestly from WORLD.md and bin/swarm — each row is something an agent must understand
to use the system correctly, because the contract or the code will surprise it otherwise.
**VERIFIED** (every row cites behavior I read in the source or contract):

1. the swarm / `.swarm/` root (project = swarm)
2. agent (session + pane + registry record)
3. id = slugified label (slugify rules, filler-word derivation)
4. the names ledger: lifetime uniqueness, `-2/-3` suffixing, "reap never frees a name"
5. tree topology + the talk-up/down/sideways rule (convention; unenforced in code)
6. operator as special non-agent target (no registry, no pane, no doorbell)
7. `spawn` (+ `--label/--model/--cwd/--role`)
8. the spawn briefing / reconcile ritual (falsifier discipline, 40 lines injected per agent)
9. the escalation format (GOAL/GAP/EVIDENCE/OPTIONS/ASK)
10. the message record (id/to/from/ts/type/body/read — `type` hardcoded, `read` vestigial)
11. two size numbers: 6000-byte send limit vs 8000-char injection cap, and why they differ
12. the doorbell (best-effort, screen-scraping settle loop)
13. inbox three-state machine: `inbox/` → `rendered/` → `read/`
14. ack semantics: cumulative, no `--all`, must name an outstanding id, sweep disclosure
15. the nag (one line, every turn, ids only)
16. `updates/` records + the reported-state taxonomy DONE/QUESTION/BLOCKED/IDLE (+ the
    question heuristic and idle-after-done disambiguation)
17. `wait`
18. four more views: `list`, `status`, `graph`, `children` (+ live/DEAD reconciliation)
19. `reap`
20. `close` subtree vs `--self`
21. the checkpoint schema: mission, tasks[].status, delegated_to[], blockers, open_threads,
    progress_summary, seq, work_cache, context
22. `checkpoint --context` + the transcript-pointer mechanism
23. restore-state injection + the precompact marker
24. "done means approved" (vs hook-done vs tasks[].done — three dones, C5)
25. identity via env (`whoami`/`parent`)
26. `swarm update` semver machinery (--major guard)
27. WORLD.md itself (275 lines)

### This design: 9 concepts

1. **Agent** — a Claude session in a pane; has a name, a parent, a journal.
2. **The tree** — your parent judges and approves your work; you judge your children's; the
   operator (human) roots it.
3. **`spawn <name> "<task>"`** — create a child. Name is chosen, not derived; a name ever used
   is an error to reuse.
4. **`send <name>` — a message is a claim on one turn.** Queued as a file; delivered whole, one
   per turn, sender-headed; `delivered/` is the world-readable record. A message must fit one
   turn's injection (~8000 chars); bigger content goes in a file, send the path.
5. **The journal** — `journal/<name>.md`, append-only, timestamped, the agent's own words.
   Tail re-injected on restart/compaction. World-readable.
6. **`ps`** — the one view: the living tree, each agent's liveness, queue depth, idle-since,
   last words; the operator's waiting mail at the top.
7. **`close <name>`** — end an agent and its subtree. Files stay.
8. **Judge artifacts, never claims** — work, replies, and journals are judged by reading them;
   panes and transcripts are ground truth and anyone may read them.
9. **Duties** (briefed, unenforced): journal before idle; report to your parent when done or
   stuck; a reconciliation is a journal entry that names a falsifier.

27 → 9. Verbs: 18 → 4 (+ `world` printing the contract, which should fit two screens).

---

## 3. WHAT EACH CONCEPT EARNS

No concept survives on elegance; each names the concrete failure without it.

1. **Agent.** Without a durable name+pane binding, you cannot address, observe, or kill
   anything. The pane is what makes "judge by artifact" include "watch it work" — the
   human-observable society is the product's whole point vs. the harness's built-in subagents.
2. **The tree.** Without a parent edge, nobody in particular is responsible for judging any
   given result, so everything routes to the operator — the exact channel-pollution failure
   that created the chief-of-staff on day one (PHILOSOPHY §9). One recorded fact (parent) buys
   the whole attention economy. Note what the tree is *not*: the code never enforced
   who-may-message-whom (VERIFIED — `cmd_send` checks existence, not relation), and this design
   keeps that honest: topology is one fact plus judgment, not a rule engine.
3. **spawn with a chosen name.** Without spawn there is no delegation. The name is a required
   argument because naming is delegation hygiene; without lifetime uniqueness, history blurs
   two agents into one record. The tombstone is the journal file itself: `journal/<name>.md`
   exists ⇒ the name is taken, forever. No ledger, no suffix minting, no slugifier, no
   filler-word list (VERIFIED: all four exist today, bin/swarm:165–289).
4. **Message-as-turn.** This is the load-bearing change; it earns its place three times over.
   (a) *The co-injection failure becomes impossible to build.* Both dropped operator directives
   (F4, cos §2.1) were delivered in a turn shared with an absorbing sibling message — 7,170
   chars, nothing withheld, one attended, one dropped. One message per turn means a directive
   never arrives as the quiet second thing. (b) *Sender class is structural:* the delivery
   header names the sender and relation ("from the OPERATOR", "from your parent cos") — G19
   ("a directive framed as agent chatter") cannot be written. (c) *The record can only claim
   what happened.* `delivered/` is set by one atomic rename at the moment the bytes drained
   into a turn (the G17 drain-callback mechanism, kept verbatim). Every representation the
   current schema carries falsely or vestigially — `type`, `read`, rendered-vs-acked — is gone.
   What a message record must be able to SAY (the F2 question) is: *who, to whom, when, what,
   and whether it has yet consumed its turn.* Nothing else is a fact the filesystem can witness.
5. **The journal.** Three failures without it: an agent that compacts loses its goal (the one
   thing PHILOSOPHY §1 says to save); a parent cannot see whether a child is fresh or stalled
   without a readable trace (F1's table, rows 3–5); and trajectory claims are unfalsifiable
   when state overwrites itself (F7). Append-only + timestamps + world-readable answers all
   three with one concept. It is free text because every *structured* field of the current
   checkpoint is verifiably dead or rotten: `seq`/`updated_ts` written and never read by any
   code (VERIFIED, audit F1 + my own read of bin/swarm), `delegated_to[].status` rots
   (AUDIT-MAP q6), blockers re-inject verbatim forever, and ~105 `tasks[].status="done"` are
   all self-claims with zero parent verdicts (CORROBORATED). A schema nobody reads is not a
   schema; it is ceremony with fields.
6. **ps.** Without a view, seeing-is-global is a slogan. It is ONE verb because the current
   five (`graph`, `children`, `list`, `status`, `updates`) are five renderings of the same
   facts — MEASURED: of 594 real `swarm` executions recovered from all 84 transcripts (regex
   over Bash tool_use blocks; undercounts nesting; comparative use only), those five verbs
   split 190 calls. Nobody needed five answers; they needed one question answered well.
   `whoami`/`parent` (55 calls for facts stated in every agent's spawn header) fold in: `ps`
   marks "(you)".
7. **close.** Without it, dead work holds panes forever. Subtree-close only; the `--self`
   variant is documented "rare" today and its absence costs a re-spawn.
8. **Judge artifacts.** Without it, the system trusts summaries — the oldest principle here
   and the one the record shows actually working. It is what replaces every compliance
   mechanism this design deletes: *obeyed* is read off the work, by the party who cares.
9. **Duties.** Without briefed duties there is nothing for a parent to judge between
   artifacts. They stay unenforced on the operator's own reasoning (PHILOSOPHY §2): a hook
   that forces a journal entry produces an entry, not a reconciled agent.

**Substrate note** (kept out of the concept count, but a position): one language, one file.
The current CLI is bash that shells into python 20+ times with a node hook (VERIFIED); three
languages, two files, 2,265 lines. A single python file (CLI + hook entrypoints) plausibly
lands near a quarter of that — SUSPECT until built, but python-for-the-hook is *safer* on the
one bug that mattered: G17 was node discarding queued stdout at exit; python flushes
(VERIFIED: bin/swarm:885–893 documents exactly this asymmetry). herdr stays the container:
the pane-per-agent observability is the product. Mechanisms inherited verbatim because they
are the verified-working half (cos §1): durable file queue, atomic rename as state machine,
drain-callback before side effects, task-as-file spawn (G14), launcher status file.
Mechanics that ride the verbs without being concepts (added post-review, owning finding 5 of
the implementation review): `spawn --model/--cwd`, and `send --stdin` as the recommended body
path — a positional body is a shell word, the same G14 lesson task-as-file already encodes.

---

## 4. WHAT I DELETED, AND WHAT BREAKS

| Deleted | What is lost, concretely | Why acceptable |
|---|---|---|
| `inbox read`/`ack`, `rendered/`, the nag, cumulative-ack semantics, no-`--all` rule | Nothing tracks "outstanding-ness"; an agent that ignores a delivered message leaves no standing reminder in its own context. | The reminder was tried and its own builder priced it: it carries strictly less information than the ignored body, is cleared by a command that proves nothing, and its absence reads as compliance (cos §4.1, VERIFIED replay). The party incentivized to check — the sender — now has eyes: `delivered/` + the recipient's pane/journal. Losing the recipient-side reminder is losing a guardrail the philosophy condemns anyway. |
| The checkpoint schema (tasks[], status enums, delegated_to[], blockers, seq, open_threads, work_cache) | Machine-readable status; any future dashboard over task states. | No code ever read the machine-readable parts (VERIFIED). The fields that were read by humans (mission, progress) survive as journal prose. A dashboard can be built over journals *when something reads it* — conventions earn tooling (§8). |
| `wait` | Synchronous blocking on a child. | MEASURED: 11 uses in the system's entire life. Children push reports; parents poll `ps`. |
| `updates/` event history + DONE/QUESTION/BLOCKED/IDLE taxonomy + question heuristic | At-a-glance "the child is asking you something". | The taxonomy is a heuristic over facts the transcript already holds; it misclassifies by design ("a hint, not ground truth"). `ps` shows idle-since + last words — the facts — and the pane is one command away. The unbounded `updates/` dir (170 files and growing, open question 4, never ruled) ceases to exist; the transcript is the tense-bearing history. |
| The names ledger, slugify, filler-word derivation, `-2` suffixing | Auto-naming; graceful collision handling. | Collision becomes an error and the spawner picks another name. Uniqueness-forever survives via the journal tombstone at zero concepts. |
| `reap` | Roster pruning. | MEASURED: 6 uses ever. `ps` renders the dead compactly (name-only, one shared line); there is nothing to prune. Corrected post-review (owning finding 7): a binding record of *immutable* facts per agent (name, parent, pane, task, spawn-ts) does exist and is never pruned — it cannot rot into *wrong*, because nothing in it claims the present; liveness is derived from herdr at every read. The cost owned honestly: the roster grows for the swarm's lifetime, so compact-dead rendering is what keeps the one view readable, and `ps` height is the ceiling this trades for reap's two extra concepts. |
| The escalation format (GOAL/GAP/…) | A structured interface for escalations. | VERIFIED (audit): 4 of 51 operator-bound messages ever used it — a convention with no consumer. Replaced by one briefed sentence: say what you need decided and why it exceeds your authority. |
| Two size numbers (6000 send / 8000 inject) | The guarantee dance between them. | One number: a message fits one turn's injection or you send a file path. One-per-turn deletes the budget arithmetic (header/nag/trailer fixpoint loop, bin/swarm-hook.cjs:301–334 — 30 lines of reserved-width computation) whole. |
| `swarm update` semver machinery | In-tool upgrade management. | An installation concern, not a concept agents live inside. `git pull` + reinstall script. The `--major` guard is already inert under the operator's own standing MINOR policy (PHILOSOPHY §7, VERIFIED). |
| The operator-terminus guarantee ("an escalation never has nowhere to go") | The comforting sentence. | It was never true in the way it reads — the operator's mailbox drains only by human action (F6). The design states the truth instead: *messages to the operator wait until the human looks; `ps` shows them waiting.* Push-to-human is the multiplexer's job (a tab badge), not a CLI's promise. |
| `--role`, `--self`, `--live-only`, `start`, `checkpoint --context` | Assorted conveniences. | Mission = the task (journal seeds with it). Context usage: the agent notes what it wants in its journal; a wrong-looking number that no code consumes earns nothing. |

**The one loss I flag as genuinely painful:** with no recipient-side reminder at all, a message
delivered into a turn that then *compacts* survives only in `delivered/` on disk and in the
sender's patience. The sender's reconciliation duty ("is my child acting on what I sent?") is
now the *only* compliance mechanism. That is deliberate — it is F1's repair (give the
incentivized party eyes, then rely on the incentive) — but it is a bet, and §6 names its
falsifier.

---

## 5. HOW THE EIGHT FINDINGS FARE

- **F1 (philosophy has no word for observability)** — **Fixed, as a rule of the design:**
  every claim the system stores names who can see it, and every row of the audit's blindness
  table gets eyes: sender → `delivered/` + recipient's pane; parent → child's journal mtime
  and text; operator → `ps` shows his waiting mail; trajectory → append-only journal. The
  vocabulary gains the third word: a duty needs an incentive *and an instrument*.
- **F2 (schema says delivered; problem is obeyed)** — **Unstateable.** There is no message
  schema to enrich and no acknowledgement to mistake for compliance. The record claims
  delivery only; obedience is judged from artifacts by the sender. The *reality* that a model
  can read and not comply remains — no representation fixes attention — but the system no
  longer stores any claim that pattern-matches to it, so no fix can converge to a
  representable neighbor: the neighbor does not exist.
- **F3 (claims stored where the subject can't be checked)** — **Unstateable.** There is no
  store whose only reader is its subject. `delivered/` is world-readable and written by the
  delivery mechanism, not the recipient; journals are world-readable; panes are ground truth
  for anyone. The theorem has nothing to bite.
- **F4 (the halt consumed by the mechanism under audit)** — **Fixed structurally** for the
  attention half: a halt arrives as its own turn, never as the second message under a
  sibling's absorbing one. The 2-second merge race is physics and remains.
- **F5 (three tenses on one commit; doc-rot)** — **Reduced, honestly still present.** A
  9-concept contract that fits two screens has less surface to rot, and deleting the PRD
  corpus from the agent-facing world removes the "verified against the installed hook" class
  of claim. But a document is still a claim about the present and nothing re-checks it; this
  design does not solve that and says so.
- **F6 (backpressure cap vs escalation terminus)** — **Unstateable.** There is no unacked
  count, so nothing can gate on it; nothing ever refuses a message to the operator. Queue
  depth is observable in `ps` and gates nothing.
- **F7 (nothing stores tense)** — **Fixed.** The journal is append-only and timestamped; the
  queue and `delivered/` files are timestamped; the transcript was always tense-bearing.
  "Am I repeating myself?" is answerable by reading your own journal — the operator's
  "no separate log" ruling is respectfully unmade, because the audit showed the evidence it
  deleted was the evidence reconciliation needs.
- **F8 (the operator's suspicions, attacked)** — The push/poll asymmetry is **kept and
  named** rather than papered over: the operator is a mailbox, not a node; that is now a
  sentence in the contract instead of an unexamined assumption under a false guarantee. The
  register's open question 1 gets answered by the design taking a position. Whether the human
  should get push is herdr's decision to make, and the design says whose job it is.

---

## 6. WHAT WOULD FALSIFY THIS DESIGN

Committed before defense:

1. **Senders don't look.** The design bets everything on the sender-side check. If, in live
   use, directives are ignored and the sender does not notice within one of its own
   reconciliation cycles — observable as: a `delivered/` file older than a cycle whose
   instruction visibly did not happen, discovered by anyone other than the sender — then I
   have only relocated F2 from a schema that couldn't say "obeyed" to a duty nobody performs,
   and the recipient-side reminder I deleted was load-bearing after all.
2. **Turn floods.** If an agent's transcript shows message-consumption turns crowding out its
   work (queue-drain turns a majority over any sustained stretch), one-message-per-turn is
   the wrong quantum and coalescing was load-bearing.
3. **The re-ring is the one unproven mechanism.** One-per-turn needs the queue to keep
   draining after the agent goes idle: on Stop, the hook rings the pane's own doorbell if the
   queue is non-empty (same send-text/Enter primitive as today's doorbell, new call site).
   If that self-ring proves unreliable, later messages stall until the next natural turn —
   observable as queue files older than the recipient's last idle period. Degradation is to
   today's behavior, but the "promptly" half of the contract would be false and the contract
   must then say so.
4. **Free-text journals rot into mush.** If parents demonstrably stop reading child journals
   (the F3 test, inverted: allowed-and-never-used), the structured checkpoint earned its
   fields and I deleted a working instrument. Measurable the same way I measured verb usage.
5. **Post-compaction floundering.** If agents restored from a 4KB journal tail + original
   task measurably fail to resume (re-ask their parent what they were doing, redo finished
   work) more than under the schema checkpoint, the schema was carrying real weight.

**One more uncomfortable conclusion, owed under the brief:** the operator's stated goal —
"the simplest representation of this tool to rewrite" — is half wrong. The *mechanisms* do
not need rewriting; the verified-working half of this system (durable files, atomic renames,
drain-conditional side effects, the launcher) is exactly what a rewrite would rebuild, worse,
and this design keeps them byte-for-byte in spirit. What needs rewriting is the
*representation layer* — the vocabulary of claims the system is allowed to store — and the
contract that teaches it. That is a 2,265-line codebase becoming one small file, and a
275-line world becoming two screens, not because the code was bad but because most of its
concepts were compensations for claims the system should never have stored.
