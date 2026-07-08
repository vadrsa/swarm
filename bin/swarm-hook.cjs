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
//   SWARM_DIR       — absolute path to the PROJECT swarm root (holds swarms/).
//                     The active swarm's own dir is $SWARM_DIR/swarms/$SWARM_ID,
//                     and its updates/ lives under that. This matches what the
//                     `swarm` CLI expects, so the child can run swarm verbs too.
//   SWARM_ID        — the active swarm-id; combined with SWARM_DIR it locates
//                     this swarm's updates/ dir.
//   SWARM_AGENT_ID  — this subagent's stable id within the swarm (e.g. "a1")
//   SWARM_AGENT_LABEL — human label (e.g. "claude:opus")
//
// Back-compat: older `swarm spawn` passed SWARM_DIR = the swarm's OWN dir and no
// SWARM_ID. If SWARM_ID is absent we fall back to treating SWARM_DIR as the dir
// that directly contains updates/ (the legacy contract).
//
// Argv: [event]  where event is "stop" | "notification" (from the hook config).

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

const swarmDir = process.env.SWARM_DIR || '';
const swarmId = process.env.SWARM_ID || '';
const id = process.env.SWARM_AGENT_ID || 'unknown';
const label = process.env.SWARM_AGENT_LABEL || 'claude';

if (!swarmDir) process.exit(0); // Not a swarm subagent — do nothing.

// Resolve this swarm's updates/ dir. Under the current contract SWARM_DIR is the
// PROJECT root and the swarm's own dir is $SWARM_DIR/swarms/$SWARM_ID. If
// SWARM_ID is absent we honour the legacy contract where SWARM_DIR was already
// the swarm's own dir (updates/ directly beneath it).
const updatesDir = swarmId
  ? path.join(swarmDir, 'swarms', swarmId, 'updates')
  : path.join(swarmDir, 'updates');
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

const transcriptPath = payload.transcript_path || payload.transcriptPath || '';
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
