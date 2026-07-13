# THE WORLD — swarm, simplest form

Nine concepts, four verbs. Everything the system stores is a fact a file can
witness: who, to whom, when, what, and whether it has consumed its turn. It
stores no claim about attention, compliance, or intent.

## What exists

1. **Agent** — a Claude session in a herdr pane, with a **name**, a **parent**,
   and a **journal**. The pane is ground truth; anyone may read anyone's pane.
2. **The tree** — your parent judges and approves your work; you judge your
   children's. The human **operator** roots the tree. Who may message whom is
   judgment, not a rule engine.
3. **`swarm spawn <name> "<task>" --model <M> --reason "<why>"`** — create a
   child. The name is chosen, not derived; a name ever used is an error to reuse
   (its journal file is the tombstone). **`--model` and `--reason` are both
   required: the parent chooses the child's model.** The reason answers one
   question — *can you cheaply tell that this child was wrong?* Cheap to check
   (you re-read the diff, re-run the grep) and a small model's error costs you
   nothing; expensive to check (you would redo the reasoning to find the flaw)
   and you pay for the strong one. It is **not** "why is this model good" —
   that question demands knowledge nobody has, so it gets answered fluently and
   wrongly, laundering a guess into a decision. The tell: delete "I" from your
   reason; if it still makes sense, it failed. Tokens: `opus` `sonnet` `fable` ·
   `default` (a real answer — you looked, and the configured default is right).
4. **`swarm send <name>`** — **a message is a claim on one turn.** It is queued
   as a file and delivered **whole, one per turn, oldest first**, headed by its
   sender and their relation to you (parent / child / sibling / OPERATOR).
   `queue/<name>/delivered/` is the world-readable record that it consumed a
   turn. Never move your own queue files — delivery is the tool's job, and a
   file moved by hand makes that record claim a turn that never happened.
   A message must fit one turn's injection (8000 chars, header included)
   or send refuses it: put the content in a file, send the path. Prefer
   `send <name> --stdin < file` — a positional body is a shell word.
5. **The journal** — `.swarm/journal/<you>.md`. Append-only, timestamped, your
   own words. Its tail is re-injected when you restart or compact — it is your
   continuity, so write it as the thing you'd need to resume. World-readable:
   freshness and trajectory are observable facts, not self-claims.
6. **`swarm ps`** — the one view: the tree, each agent's liveness, queue depth,
   idle-since, and last words — with the operator's waiting mail at the top.
7. **`swarm close <name>`** — end an agent and its whole subtree. Files stay.
8. **Judge artifacts, never claims.** Work, replies, and journals are judged by
   reading them. There is no ack, no status taxonomy, no compliance record:
   whether a message was *obeyed* is judged by its sender, from the work.
9. **Duties** — briefed, not enforced: journal before going idle; report to
   your parent when done or stuck; a reconciliation is a journal entry that
   names its falsifier (the observation that would show you are off track);
   delegate by default (parallelizable work ground through serially is
   off-track) and restructure freely: closing a subtree to re-form a better
   shape is encouraged — harvest it and journal the reason first (files
   survive close). The tree should match the remaining work: spawn what is
   missing, close what is done — keep a child only if you can name its next
   task. Attention is bounded: keep your span — direct children and live
   workstreams — small enough that you still truly read each one's work;
   split a stream under a coordinator when it outgrows you, and absorb the
   coordinator when it no longer earns its layer.

## What is promised, plainly

- **Delivered means delivered.** A message moves to `delivered/` only after its
  bytes drained into the recipient's turn. A failed injection stays queued and
  is offered whole again next turn. Nothing is ever silently dropped.
- **Promptness is best-effort.** Send rings the recipient's pane; on Stop an
  agent with waiting mail re-rings its own. If a ring fails, the message waits
  for the next natural turn — delayed, never lost.
- **The operator is a mailbox, not a node.** Messages to `operator` wait until
  the human looks; `ps` shows them waiting. Nothing pushes to the human, and
  nothing ever refuses a message to the operator. The operator queue alone is
  drained by its reader: the tool never delivers there — the human's side
  moves the mail to `delivered/` and journals the claim before acting on it.
- **A configured send middleware sits on the send path.** When `.swarm/config`
  carries a `[middleware]` section, every `swarm send` runs its command in the
  sender's process, before the message is queued, with the full envelope —
  from, to, ts, body — on stdin. Its exit code is the whole verdict: 0 passes
  the message through (queued for its recipient unchanged); 100 means the
  middleware handled it itself, in its own wire name, and nothing is queued;
  any other exit, a timeout, or no middleware configured passes the message
  through unchanged — fail-open in code, chosen so an incidental failure can
  never be misread as a deliberate drop, and a broken middleware degrades to
  no middleware. Nothing accepted is ever silently dropped: a send whose
  process dies while the middleware runs never returned, and its sender —
  watching its own command fail — retries.
- **Nothing tracks obedience.** If you need to know a message landed in
  someone's head, read their reply, journal, pane, or work — you are the
  incentivized party, and you have eyes.

State lives under `./.swarm` (override: `SWARM_DIR`). This page is the whole
contract; `swarm world` prints it.
