#!/usr/bin/env node
// swarm-hook — the reliable inbound channel (subagent -> coordinator).
//
// Installed as a spawned subagent's Stop/Notification hook via `claude
// --settings`. Claude fires it with a JSON payload on stdin at turn-end
// (Stop) or when the agent needs input (Notification). We record ONE
// structured event into the swarm's drop dir. Completion is this event
// firing — never a screen scrape, never a parsed marker line.
//
// Env (set by swarm spawn on the subagent's pane):
//   SWARM_DIR       — absolute path to the swarm root. One swarm per project, so
//                     this dir directly contains agents/ updates/ inbox/ state/
//                     settings/ and names. Same contract the `swarm` CLI uses, so
//                     the child can run swarm verbs too.
//   SWARM_AGENT_ID  — this subagent's stable id within the swarm: its slugified
//                     label, unique for the swarm's lifetime (e.g. "fix-send-race")
//   SWARM_AGENT_LABEL — same string as the id (label and id are one concept),
//                     kept as its own env var/record key for readers.
//
// SWARM_ID is not read. The project IS the swarm; there is no swarm-id.
//
// Argv: [event]  where event is "stop" | "notification" | "inbox-check"
//   stop/notification  -> record a state event to updates/ (subagent -> coord).
//   inbox-check        -> UserPromptSubmit: surface this agent's durable inbox
//                         (coord -> subagent) into context, then mark read.

const fs = require('fs');
const path = require('path');

function readStdinJSON() {
  if (process.stdin.isTTY) return null;
  try {
    const raw = fs.readFileSync(0, 'utf8');
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

const event = (process.argv[2] || 'stop').toLowerCase();
const payload = readStdinJSON() || {};

// SWARM_DIR IS the swarm dir — one swarm per project, flat layout beneath it.
const swarmDir = process.env.SWARM_DIR || '';
const id = process.env.SWARM_AGENT_ID || 'unknown';
const label = process.env.SWARM_AGENT_LABEL || id;

if (!swarmDir) process.exit(0); // Not a swarm subagent — do nothing.

// ------------------------------------------------------ transcript pointer
// Claude passes the session's transcript path on every hook payload. That is the
// ONLY authoritative way to learn which .jsonl belongs to THIS agent: `swarm
// spawn` cannot know it (Claude picks the name after exec), and every agent in a
// project shares one ~/.claude/projects/<slug>/ dir, so no glob — not even a
// project-scoped one — can tell two siblings apart.
//
// Record it where `swarm checkpoint --context` can read it deterministically by
// id. Runs BEFORE the verb dispatch below because every verb exits early, and
// SessionStart/UserPromptSubmit fire long before the first Stop — so the pointer
// exists from the agent's first breath (self-healing: any hook re-records it).
//
// Lives in state/ (not the agents/ registry) because `reap` deletes
// agents/<id>.json but deliberately preserves state/ — and because a dedicated
// file has ONE writer, so it needs no read-modify-write race against spawn/reap.
const transcriptPath = payload.transcript_path || payload.transcriptPath || '';
if (transcriptPath) {
  try {
    const stateDir = path.join(swarmDir, 'state');
    fs.mkdirSync(stateDir, { recursive: true });
    const ptr = path.join(stateDir, `${id}.transcript`);
    const tmp = `${ptr}.tmp`;
    fs.writeFileSync(tmp, transcriptPath + '\n');
    fs.renameSync(tmp, ptr); // atomic: a concurrent reader never sees a partial path
  } catch { /* best effort — never break the agent's turn */ }
}

// --------------------------------------------------------- restore-state
// SessionStart verb (all agents). On a fresh or post-compaction session,
// re-inject this agent's goal-status checkpoint so it recovers its working state
// (Thread C). source=="compact" means we just lost context to compaction — the
// checkpoint is now the trustworthy record. Bulletproof: any error => no-op.
if (event === 'restore-state') {
  try {
    const stateFile = path.join(swarmDir, 'state', `${id}.json`);
    if (!fs.existsSync(stateFile)) process.exit(0);
    let st; try { st = JSON.parse(fs.readFileSync(stateFile, 'utf8')); } catch { process.exit(0); }
    const src = (payload.source || 'startup');
    const compacted = src === 'compact';
    const tasks = Array.isArray(st.tasks) ? st.tasks : [];
    const taskLines = tasks.map(t =>
      `  - [${t.status || '?'}] ${t.title || t.id || '?'}${t.blockers && t.blockers.length ? ' (BLOCKED: ' + t.blockers.join('; ') + ')' : ''}`
    ).join('\n');
    const ctx = `[swarm continuity] You are the standing agent ${id}${st.role ? ' (' + st.role + ')' : ''}, ` +
      `resuming ${compacted ? 'AFTER A CONTEXT COMPACTION — your prior working memory was just summarized away, so this checkpoint is your most reliable record' : 'a session'}.\n` +
      `MISSION: ${st.mission || '(unset)'}\n` +
      `OVERALL STATUS: ${st.status || '?'} — ${st.progress_summary || ''}\n` +
      (taskLines ? `CURRENT TASKS:\n${taskLines}\n` : '') +
      (st.open_threads && st.open_threads.length ? `OPEN THREADS: ${st.open_threads.map(o => o.id + ':' + o.state).join(', ')}\n` : '') +
      `Re-read your full checkpoint at state/${id}.json before proceeding, and pick up where it says you are.\n\n` +
      `RECONCILE now (argue against yourself, do not reflexively say "on track"): ` +
      `(1) state your goal from the file above; (2) name the concrete evidence that WOULD show you are OFF track; ` +
      `(3) check each child (swarm children + their state files) and your own progress against that evidence; ` +
      `(4) verdict + the ONE biggest risk, then ACT on it (steer/close/spawn a child, or escalate up with GOAL/GAP/EVIDENCE/OPTIONS/ASK). ` +
      `Then update your checkpoint to reflect the reconciled status.`;
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: ctx },
    }));
  } catch { /* never break session start */ }
  process.exit(0);
}

// ------------------------------------------------------ precompact-marker
// PreCompact verb (all agents). Compaction is about to happen and we CANNOT
// inject forward from here — so just record that it happened (a marker + a note
// in the state file if present), and do NOT block (the window is genuinely full).
// The restore-state hook (SessionStart source=compact) does the actual re-inject.
if (event === 'precompact-marker') {
  try {
    const stateDir = path.join(swarmDir, 'state');
    fs.mkdirSync(stateDir, { recursive: true });
    fs.writeFileSync(path.join(stateDir, `${id}.compaction-pending`),
      JSON.stringify({ ts: Number(payload.ts) || 0, trigger: payload.trigger || payload.matcher || '' }));
  } catch { /* best effort */ }
  process.exit(0); // never block compaction
}

// ------------------------------------------------------------- inbox-check
// UserPromptSubmit verb. Surfaces this agent's durable inbox (coordinator ->
// subagent messages, written by `swarm send`) into the model's context at the
// turn boundary, then marks the surfaced messages read by MOVING them into a
// read/ subdir (atomic rename; a durable audit trail; no re-injection race).
//
// This runs on EVERY turn of EVERY agent, so it is fast, side-effect-light, and
// BULLETPROOF: any error → exit 0 with no output. It must never break the turn.
// A no-op (no stdout) on an empty inbox is required.
if (event === 'inbox-check') {
  try {
    const inboxDir = path.join(swarmDir, 'inbox', id);

    let files;
    try {
      files = fs.readdirSync(inboxDir);
    } catch {
      process.exit(0); // no inbox dir yet -> nothing to deliver
    }

    // Unread = *.json directly under inboxDir (read ones live in read/).
    const unread = files
      .filter((fn) => fn.endsWith('.json'))
      .map((fn) => {
        let rec = null;
        try { rec = JSON.parse(fs.readFileSync(path.join(inboxDir, fn), 'utf8')); } catch { /* skip */ }
        return { fn, rec };
      })
      .filter((x) => x.rec && typeof x.rec.body === 'string')
      .sort((a, b) => Number(a.rec.ts || 0) - Number(b.rec.ts || 0));

    if (unread.length === 0) process.exit(0); // empty inbox -> no-op, no output

    // Build the injected block. Frame it EXPLICITLY as incoming messages the
    // agent should act on — additionalContext reads as out-of-band context, so
    // without framing the model may not treat it as a directive.
    const CAP = 8000; // defensive cap on total injected chars
    const fmtTime = (ts) => {
      try { return new Date(Number(ts)).toISOString().replace('T', ' ').slice(0, 19) + 'Z'; }
      catch { return '?'; }
    };
    const header = `[swarm inbox] You have ${unread.length} new message(s) from other agents:`;
    const blocks = [];
    let used = header.length;
    let injectedCount = 0;
    for (const { rec } of unread) {
      const block = `\n\n--- from ${rec.from || '?'} (${fmtTime(rec.ts)}) ---\n${rec.body}`;
      if (used + block.length > CAP && injectedCount > 0) break; // keep at least one
      blocks.push(block);
      used += block.length;
      injectedCount++;
    }
    const remaining = unread.length - injectedCount;
    let context = header + blocks.join('');
    if (remaining > 0) {
      context += `\n\n…and ${remaining} more; full messages in inbox/${id}/`;
    }
    context += `\n\nThese were delivered to your durable inbox; act on them as part of this turn.`;

    // Emit the injection FIRST, then mark read. If we crashed between the two,
    // the messages would be re-injected next turn (safe) — losing one is not.
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: { hookEventName: 'UserPromptSubmit', additionalContext: context },
    }));

    // Mark surfaced messages read by moving them into read/ (atomic rename).
    const readDir = path.join(inboxDir, 'read');
    try { fs.mkdirSync(readDir, { recursive: true }); } catch { /* best effort */ }
    for (let i = 0; i < injectedCount; i++) {
      const fn = unread[i].fn;
      try { fs.renameSync(path.join(inboxDir, fn), path.join(readDir, fn)); } catch { /* best effort */ }
    }
  } catch { /* never break the turn */ }
  process.exit(0);
}

// This swarm's updates/ dir, directly beneath the swarm root.
const updatesDir = path.join(swarmDir, 'updates');
try { fs.mkdirSync(updatesDir, { recursive: true }); } catch { process.exit(0); }

// Claude includes the transcript path on every hook payload. We pull the
// LAST assistant text line as a one-line summary — the "event + summary"
// contract. Bare event still records if there's no usable summary, so
// completion detection needs zero cooperation from the model.
// Returns the full trimmed text of the last assistant message (or '').
function lastAssistantText(transcriptPath) {
  try {
    if (!transcriptPath || !fs.existsSync(transcriptPath)) return '';
    const lines = fs.readFileSync(transcriptPath, 'utf8').split('\n').filter(Boolean);
    for (let i = lines.length - 1; i >= 0; i--) {
      let o;
      try { o = JSON.parse(lines[i]); } catch { continue; }
      const msg = o && o.message;
      if (!msg || msg.role !== 'assistant') continue;
      let text = '';
      if (typeof msg.content === 'string') text = msg.content;
      else if (Array.isArray(msg.content)) {
        text = msg.content.filter((b) => b && b.type === 'text').map((b) => b.text).join(' ');
      }
      text = (text || '').replace(/\s+/g, ' ').trim();
      if (text) return text;
    }
  } catch { /* best effort */ }
  return '';
}

// Heuristic: did the agent stop to ASK the user something (vs. just finish)?
// Claude Code fires the same `Stop` event whether the turn ended because the
// work is done OR because the agent asked a question in prose and yielded. The
// event type can't tell them apart, so we inspect the trailing message. This
// is a strong HINT surfaced to the coordinator, not ground truth — the
// coordinator still reads the pane to confirm intent.
function looksLikeQuestion(text) {
  if (!text) return false;
  // Consider the tail — a question almost always lands at the very end.
  const tail = text.slice(-400).toLowerCase();
  // 1. Ends with a question mark (ignoring trailing quotes/brackets/space).
  const endsQ = /\?["'`)\]\s]*$/.test(text);
  // 2. Common ask-the-user phrasings near the end.
  const asks = [
    'should i', 'shall i', 'do you want', 'would you like', 'which ',
    'let me know', 'please confirm', 'can you clarify', 'could you clarify',
    'clarify', 'confirm whether', 'is it ok', 'is that ok', 'want me to',
    'how would you like', 'what should', 'do you prefer', 'proceed with',
    'or should', 'which one', 'need your', 'awaiting your', 'your call',
  ];
  const phraseHit = asks.some((p) => tail.includes(p));
  // Require a question mark, OR an ask-phrase that also ends near a '?'/':'
  return endsQ || (phraseHit && /[?:]\s*$/.test(text));
}

// transcriptPath is resolved and persisted near the top, before verb dispatch.
const fullText = lastAssistantText(transcriptPath);
const summary = fullText.slice(0, 300);

// Newest state already recorded for THIS agent (used to tell "idle after done"
// from a real block on a Notification event). Reads the same drop dir readers use.
function lastRecordedState() {
  try {
    let best = null;
    for (const fn of fs.readdirSync(updatesDir)) {
      if (!fn.endsWith('.json')) continue;
      let r;
      try { r = JSON.parse(fs.readFileSync(path.join(updatesDir, fn), 'utf8')); } catch { continue; }
      if (r.id !== id) continue;
      if (!best || Number(r.ts || 0) >= Number(best.ts || 0)) best = r;
    }
    return best ? best.state : '';
  } catch { return ''; }
}

// A Notification fires both for a REAL block (permission prompt / the agent
// asked and is waiting) AND for plain idleness — Claude Code emits an idle
// "waiting for your input" notification ~a minute after a turn ends, even when
// the agent simply finished. Treating that idle ping as `blocked` makes a
// DONE-then-idle agent look like it needs the coordinator. Distinguish them:
//   - the notification's own message tells a permission/input request apart
//     from the generic idle timeout, and
//   - if the agent's last real state was already `done`, a bare idle ping is
//     post-completion idleness, not a new block.
const notifMsg = String(payload.message || payload.title || '').toLowerCase();
const idleNotification = /waiting for your input|is idle|are you still there/.test(notifMsg);
const permissionNotification = /permission|needs your|approve|allow|blocked|waiting for your response/.test(notifMsg);

// state:
//   notification (real block)   -> "blocked"   (permission/input actually needed)
//   notification (idle-after-done) -> "idle"    (finished, just sitting idle — NOT blocked)
//   stop + looks like a question -> "question"  (agent asked the user and yielded)
//   stop otherwise -> "done"    (turn ended, likely finished — coordinator verifies)
// The distinction between "question" and "done" is the key one: a plain Stop
// event alone can't tell "I finished" from "I stopped to ask", so we classify
// from the trailing message. Still a hint — the coordinator confirms by reading
// the pane.
let state;
if (event === 'notification') {
  const prev = lastRecordedState();
  // Idle-after-done, or a generic idle ping with no permission signal: record
  // as non-blocking `idle` so status/wait don't flip a finished agent to BLOCKED.
  if (!permissionNotification && (idleNotification || prev === 'done')) state = 'idle';
  else state = 'blocked';
} else {
  state = looksLikeQuestion(fullText) ? 'question' : 'done';
}

const record = {
  id,
  label,
  event,
  state,
  summary,
  // whether the classifier saw a question in the trailing text (surfaced so the
  // coordinator knows this is a heuristic, not a declared stop-reason)
  is_question: state === 'question',
  cwd: payload.cwd || process.cwd(),
  session_id: payload.session_id || payload.sessionId || '',
  transcript_path: transcriptPath,
  ts: Date.now(),
};

// One file per event; timestamped so back-to-back events never overwrite.
// The coordinator's `updates`/`wait` just read this dir — no daemon.
const file = path.join(updatesDir, `${id}-${record.ts}-${state}.json`);
const tmp = file + '.tmp';
try {
  fs.writeFileSync(tmp, JSON.stringify(record));
  fs.renameSync(tmp, file); // atomic: readers never see a half-written file
} catch { /* best effort — never break the subagent */ }

process.exit(0);
