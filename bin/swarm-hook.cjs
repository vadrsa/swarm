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
//   SWARM_DIR       — absolute path to the ACTIVE swarm's dir (holds updates/)
//   SWARM_AGENT_ID  — this subagent's stable id within the swarm (e.g. "a1")
//   SWARM_AGENT_LABEL — human label (e.g. "claude:opus")
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
const id = process.env.SWARM_AGENT_ID || 'unknown';
const label = process.env.SWARM_AGENT_LABEL || 'claude';

if (!swarmDir) process.exit(0); // Not a swarm subagent — do nothing.

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

const transcriptPath = payload.transcript_path || payload.transcriptPath || '';
const fullText = lastAssistantText(transcriptPath);
const summary = fullText.slice(0, 300);

// state:
//   notification -> "blocked"   (Claude Code needs input: permission/idle prompt)
//   stop + looks like a question -> "question"  (agent asked the user and yielded)
//   stop otherwise -> "done"    (turn ended, likely finished — coordinator verifies)
// The distinction between "question" and "done" is the key one: a plain Stop
// event alone can't tell "I finished" from "I stopped to ask", so we classify
// from the trailing message. Still a hint — the coordinator confirms by reading
// the pane.
let state;
if (event === 'notification') state = 'blocked';
else state = looksLikeQuestion(fullText) ? 'question' : 'done';

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
