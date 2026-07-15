// swarm-pump — the opencode backend of the duty loop (LOOP.md Build 1;
// mechanism per OPENCODE-PLUGIN.md §3.1, carried VERBATIM: the pump supplies
// its own turns; two-phase delivered/; one message per idle; self-ring;
// catch-everything-log-visibly; NEVER await your own server).
//
// Loaded from a project-local .opencode/plugin/*.js (no install step —
// OPENCODE-PLUGIN.md §5). The launcher writes a per-agent config pointing
// here and sets SWARM_DIR / SWARM_AGENT_ID / SWARM_PARENT in the process env.
//
// Three duties, same file, same event hook, same failure discipline:
//   1. DELIVERY — swarm's queue/<name>/*.json drains one-per-turn (the pump).
//   2. JOURNAL DIGEST — every idle, append a [loop]-tagged line to the
//      agent's own journal (mechanical; never the agent's own words).
//   3. PARENT DIGEST — quiescence-gated (queue empty AND cooldown elapsed
//      AND content differs from the last digest sent), same predicate as the
//      Claude backend's cmd_event (bin/swarm), so a parent judging a mixed
//      tree reads one contract regardless of which backend a child runs.
//
// `event` is the one hook opencode dispatches fire-and-forget (§2.3.3): no
// caller awaits it, so a throw here cannot break a turn — but the same
// property means a throw is SWALLOWED SILENTLY, with nothing in the pane and
// nothing in `ps` but a rising queue depth. Every path below is wrapped and
// logs visibly (console.error, which lands in the TUI's own log) rather than
// failing silent.

import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync,
         renameSync, statSync } from "node:fs"
import { join, dirname } from "node:path"

const LAST_WORDS_CAP = 500        // matches bin/swarm's LAST_WORDS_CAP
const JOURNAL_DIGEST_CAP = 200    // matches bin/swarm's journal digest slice
const DIGEST_COOLDOWN_S =
  (Number(process.env.SWARM_DIGEST_COOLDOWN) || 10) * 60

function logVisibly(where, err) {
  // The one thing this file must never do is fail silent (§2.3.3's trap).
  console.error(`[swarm-pump] ${where}:`, err && err.stack || err)
}

// ------------------------------------------------------------- swarm paths
// Same layout bin/swarm reads/writes (bin/swarm:67-95); the plugin and the
// Claude backend share one file contract so a parent never needs to know
// which backend a child runs.

function root() {
  const r = process.env.SWARM_DIR
  if (!r) throw new Error("SWARM_DIR not set in the launcher's env")
  return r
}

function myName() {
  const n = process.env.SWARM_AGENT_ID
  if (!n) throw new Error("SWARM_AGENT_ID not set in the launcher's env")
  return n
}

function qDir(name) { return join(root(), "queue", name) }
function deliveredDir(name) { return join(qDir(name), "delivered") }
function journalPath(name) { return join(root(), "journal", `${name}.md`) }
function agentRecPath(name) { return join(root(), "agents", `${name}.json`) }
function settingsDir() { return join(root(), "settings") }
function digestTsPath(name) { return join(settingsDir(), `${name}.digest-ts`) }
function digestLastPath(name) { return join(settingsDir(), `${name}.digest-last`) }

function nowMs() { return Date.now() }

function writeAtomic(path, text) {
  mkdirSync(dirname(path), { recursive: true })
  const tmp = `${path}.tmp.${process.pid}`
  writeFileSync(tmp, text)
  renameSync(tmp, path)
}

function readJson(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"))
  } catch {
    return null
  }
}

// --------------------------------------------------------- queue selection
// The oldest waiting message for `name`: {fn, rec} | null. Mirrors
// bin/swarm's select_next (bin/swarm:195-201) — oldest first, delivered/ and
// junk ignored.

function oldestQueuedMessage(name) {
  const d = qDir(name)
  if (!existsSync(d)) return null
  let best = null
  for (const fn of readdirSync(d)) {
    if (!fn.endsWith(".json")) continue
    const p = join(d, fn)
    let st
    try { st = statSync(p) } catch { continue }
    if (!st.isFile()) continue          // skips delivered/
    const rec = readJson(p)
    if (!rec || typeof rec.body !== "string") continue   // skips junk
    if (!best || rec.ts < best.rec.ts ||
        (rec.ts === best.rec.ts && fn < best.fn)) {
      best = { fn, rec }
    }
  }
  return best
}

function listWaitingCount(name) {
  const d = qDir(name)
  if (!existsSync(d)) return 0
  let n = 0
  for (const fn of readdirSync(d)) {
    if (!fn.endsWith(".json")) continue
    const p = join(d, fn)
    let st
    try { st = statSync(p) } catch { continue }
    if (!st.isFile()) continue
    const rec = readJson(p)
    if (rec && typeof rec.body === "string") n++
  }
  return n
}

function markDelivered(name, fn) {
  try {
    mkdirSync(deliveredDir(name), { recursive: true })
    renameSync(join(qDir(name), fn), join(deliveredDir(name), fn))
  } catch (e) {
    // worst case: re-delivered next turn; never lost (same discipline as
    // bin/swarm's deliver_once, bin/swarm:394-417)
    logVisibly("markDelivered (non-fatal, will retry next pop)", e)
  }
}

function relation(sender, recipient, parentOf) {
  // Mirrors bin/swarm's relation() (bin/swarm:158-174) closely enough for
  // the delivery header; the recipient's parent is the only edge the pump
  // needs (it never renders sibling/child relations for ITS OWN inbox).
  if (sender === "operator") return "the OPERATOR (the human at the root)"
  if (parentOf === sender) return "your parent"
  return "another agent"
}

function fmtTs(ms) {
  return new Date(ms).toISOString().replace(/\.\d+Z$/, "Z")
    .replace("T", " ")
}

function buildDelivery(rec, rel) {
  const head = `[swarm message] from ${rec.from || "?"} — ${rel} — ` +
               `sent ${fmtTs(rec.ts)}\n\n`
  return head + (rec.body || "")
}

// --------------------------------------------------------- duty: journal
// Every idle, mechanical, [loop]-tagged — never mistaken for the agent's
// own reconciliation prose (same contract as bin/swarm's
// append_journal_digest).

function appendJournalDigest(name, lastWords, ts) {
  const tail = (lastWords || "").slice(0, JOURNAL_DIGEST_CAP)
  const line = `\n[loop] ${fmtTs(ts)} — turn ended — last words: ${tail}\n`
  mkdirSync(dirname(journalPath(name)), { recursive: true })
  const existing = existsSync(journalPath(name))
    ? readFileSync(journalPath(name), "utf8") : ""
  writeFileSync(journalPath(name), existing + line)
}

// ----------------------------------------------------- duty: parent digest
// Same quiescence predicate as bin/swarm's digest_due (bin/swarm:565-604,
// per LOOP-RED3 §6's repair): queue empty AND cooldown elapsed AND content
// differs from the last digest actually sent. One contract, two backends.

function digestContent(lastWords) {
  return (lastWords || "").slice(0, LAST_WORDS_CAP)
}

function recentRealSendToParent(name, parent, nowMsVal, cooldownS) {
  // Mirrors bin/swarm's recent_real_send_to_parent — condition 1 of the
  // corrected predicate (harness-contractor's review pass, following
  // LOOP-RED3): without this check, an agent that sends a genuine report
  // and then idles gets a DUPLICATE digest right after (the report's own
  // content differs from the last digest, so content-diff alone does not
  // catch this case — the new content IS the report the agent already
  // sent itself). The absorbed digest is a floor under silent agents, not
  // a tax on agents already doing their own reporting duty. Scans both
  // queue/<parent>/ (still waiting) and queue/<parent>/delivered/ (already
  // read) for a message from == name with ts inside the cooldown window.
  const cutoff = nowMsVal - cooldownS * 1000
  for (const d of [qDir(parent), deliveredDir(parent)]) {
    if (!existsSync(d)) continue
    for (const fn of readdirSync(d)) {
      if (!fn.endsWith(".json")) continue
      const p = join(d, fn)
      let st
      try { st = statSync(p) } catch { continue }
      if (!st.isFile()) continue
      const rec = readJson(p)
      if (!rec || rec.from !== name) continue
      if (typeof rec.ts === "number" && rec.ts >= cutoff) return true
    }
  }
  return false
}

function digestDue(name, parent, nowMsVal, lastWords) {
  if (recentRealSendToParent(name, parent, nowMsVal, DIGEST_COOLDOWN_S)) {
    return false
  }
  if (listWaitingCount(name) > 0) return false
  const lastTs = readJson(digestTsPath(name))
  if (lastTs !== null) {
    const t = Number(lastTs)
    if (!Number.isNaN(t) && (nowMsVal - t) < DIGEST_COOLDOWN_S * 1000) {
      return false
    }
  }
  const lastBody = readJson(digestLastPath(name))
  if (lastBody !== null && lastBody === digestContent(lastWords)) return false
  return true
}

function queuePut(rec) {
  // Mirrors bin/swarm's queue_put (bin/swarm:263-286): O_CREAT|O_EXCL by
  // {ts}-{from}.json, bump ts on collision, bounded retries. Same file
  // shape, same collision discipline — a parent's queue/ dir is read by
  // both backends indifferently.
  const d = qDir(rec.to)
  mkdirSync(d, { recursive: true })
  for (let i = 0; i < 1000; i++) {
    const fn = `${rec.ts}-${rec.from}.json`
    const p = join(d, fn)
    try {
      writeFileSync(p, JSON.stringify(rec), { flag: "wx" })
      return fn
    } catch (e) {
      if (e.code === "EEXIST") { rec.ts += 1; continue }
      throw e
    }
  }
  throw new Error(`queue name space exhausted near ${rec.ts}`)
}

async function ringParentDoorbell(client, name, parent) {
  // Best-effort, exactly as cmd_send's doorbell is best-effort (§3.1.3:
  // sender rings are wake-ups, never the delivery mechanism). For a
  // port-bearing (opencode) parent this is an HTTP POST via the parent's
  // own client base URL if known; for a pane-bearing (Claude) parent this
  // plugin has no pane access, so bin/swarm's own doorbell branch
  // (cmd_send, extended in Phase B §3) is what actually rings it when the
  // digest is picked up as an ordinary queued message — this function only
  // covers the opencode-to-opencode case where SWARM_PARENT_PORT is set.
  const parentPort = process.env.SWARM_PARENT_PORT
  if (!parentPort) return   // no known port: the queued file is durable;
                            // the parent's own idle/turn cadence, or a
                            // human running `swarm send`, still finds it
  try {
    const res = await fetch(`http://127.0.0.1:${parentPort}/session`)
    if (!res.ok) return
    const sessions = await res.json()
    const sid = Array.isArray(sessions) && sessions[0] && sessions[0].id
    if (!sid) return
    await fetch(`http://127.0.0.1:${parentPort}/session/${sid}/message`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ parts: [{ type: "text", text: "check queue" }] }),
    })
  } catch (e) {
    logVisibly("ringParentDoorbell (best-effort, non-fatal)", e)
  }
}

function sendParentDigest(name, parent, lastWords, ts) {
  const content = digestContent(lastWords)
  const rec = { to: parent, from: name, ts,
                body: `[duty-loop digest from ${name}] ${content}` }
  queuePut(rec)
  writeAtomic(digestTsPath(name), String(ts))
  writeAtomic(digestLastPath(name), JSON.stringify(content))
  return true
}

async function lastAssistantText(client, sessionID) {
  try {
    const res = await client.session.messages({ path: { id: sessionID } })
    const msgs = (res && res.data) || res || []
    for (let i = msgs.length - 1; i >= 0; i--) {
      const m = msgs[i]
      const role = m && m.info && m.info.role
      if (role !== "assistant") continue
      const parts = m.parts || []
      const text = parts
        .filter(p => p && p.type === "text" && typeof p.text === "string")
        .map(p => p.text).join(" ").split(/\s+/).filter(Boolean).join(" ")
      if (text) return text
    }
    return ""
  } catch (e) {
    logVisibly("lastAssistantText (falling back to empty)", e)
    return ""
  }
}

// ------------------------------------------------------------------ setup

export const SwarmPumpPlugin = async ({ client }) => {
  let name, parent
  try {
    name = myName()
    parent = process.env.SWARM_PARENT || "operator"
  } catch (e) {
    logVisibly("plugin init (SWARM_AGENT_ID/SWARM_DIR missing — pump disabled)", e)
    return {}   // no env -> not a swarm-launched agent; do nothing, ever
  }

  // Pump state (OPENCODE-PLUGIN.md §3.1's own variable names, verbatim):
  //   pumping — re-entrancy guard so overlapping idle events can't double-pop
  //   staged  — the message written but not yet proven-consumed (Fix B / §3.1.1)
  let pumping = false
  let staged = null

  return {
    event: async ({ event }) => {
      try {                                    // the `event` hook swallows
                                                 // throws silently (§2.3.3) —
                                                 // catch everything, log
                                                 // visibly, never let a
                                                 // stray error stop the
                                                 // queue draining with
                                                 // nothing to see.
        if (event.type !== "session.idle") return   // a TURN just ended
        if (pumping) return                     // re-entrancy guard
        const sid = event.properties && event.properties.sessionID
        pumping = true

        // --- duty 1: DELIVERY (the pump, §3.1 verbatim) -----------------
        // A turn just ran. If a message was staged before it, that turn
        // HAD it in context -> only NOW is delivered/ a true statement
        // about a consumed turn (§3.1.1's two-phase fix).
        if (staged) {
          markDelivered(name, staged.fn)
          staged = null
        }

        const next = oldestQueuedMessage(name)

        // --- duty 2 + 3: JOURNAL + PARENT DIGEST ------------------------
        // Fire every idle regardless of whether the pump has mail to
        // deliver — a duty-loop agent's report/journal obligations are not
        // conditional on inbound traffic. Independently wrapped so a
        // broken digest can never suppress delivery, and vice versa.
        try {
          const lastWords = sid ? await lastAssistantText(client, sid) : ""
          const ts = nowMs()
          try {
            appendJournalDigest(name, lastWords, ts)
          } catch (e) {
            logVisibly("appendJournalDigest", e)
          }
          try {
            if (digestDue(name, parent, ts, lastWords)) {
              sendParentDigest(name, parent, lastWords, ts)
              // best-effort wake-up only; the queued file is the durable
              // fact regardless of whether this lands (§3.1.3)
              ringParentDoorbell(client, name, parent).catch(e =>
                logVisibly("ringParentDoorbell", e))
            }
          } catch (e) {
            logVisibly("sendParentDigest", e)
          }
        } catch (e) {
          logVisibly("duty-loop digests (non-fatal to delivery)", e)
        }

        if (!next) { pumping = false; return }  // EMPTY -> NO RING. the
                                                 // loop guard: ring only
                                                 // when something was
                                                 // actually popped, else
                                                 // idle->ring->idle forever
                                                 // (§3.1's own hazard note)

        const rel = relation(next.rec.from, name, parent)
        const text = buildDelivery(next.rec, rel)

        // FIRE AND FORGET — never await a call back into your own host
        // (§2.3.4's trap 4: a first draft that awaited this self-deadlocked
        // for the full 5-minute timeout).
        client.session.prompt({
          path: { id: sid },
          body: { noReply: true, parts: [{ type: "text", text }] },
        })
          .then(() => {
            staged = next               // 2. STAGED — still in queue/
            return client.session.promptAsync({    // 3. RING: the pump
              path: { id: sid },                    //    supplies the turn
              body: { parts: [{ type: "text", text: "check queue" }] },
            })
          })
          .then(() => { pumping = false })  // 4. delivered/ happens at the
                                             //    NEXT idle (Fix B, §3.1.1)
          .catch(e => {
            staged = null                   // write or ring failed: file
            pumping = false                 // stays QUEUED -> retried,
            logVisibly("pump delivery", e)  // never falsely marked
          })
      } catch (e) {
        pumping = false
        logVisibly("event hook (fail open, loudly)", e)
      }
    },
  }
}

export default SwarmPumpPlugin
