# oc-red-relab — hostile re-run of the four experiments OPENCODE-PLUGIN.md stands on

**Agent:** `ocr-lab` (child of `oc-red`, adversarial reviewer). **Date:** 2026-07-12.
**Mandate:** not to confirm the parent scout — to BREAK the four load-bearing
experiments. Store-level evidence wherever the parent's evidence was a model answer.
**Sandbox:** everything under `/tmp/ocr-lab/`, torn down at the end. `~/.config/opencode`
and `~/.opencode` config never modified (read-only listing only; global
`opencode.json` mtime unchanged after the run).

## Binary actually run against

**`opencode 1.17.18`** — `/Users/vadrsa/.opencode/bin/opencode --version` → `1.17.18`.
The doc claims target **v1.17.13**. That binary is NOT on this machine; every
"VERIFIED" tag in OPENCODE-PLUGIN.md is against a version that no longer exists here.
All verdicts below are against **1.17.18**, and every server I stood up reported
`{"healthy":true,"version":"1.17.18"}`.

## The methodological upgrade (why this re-run is stronger than the original)

opencode persists sessions in **SQLite** at `~/.local/share/opencode/opencode.db`, and
ships `opencode db "<SQL>"` to query it. Schema (read directly):

```
message(id, session_id, time_created, time_updated, data)   -- data = JSON, has .role
part(id, message_id, session_id, time_created, time_updated, data)  -- data = JSON, has .type/.text
```

So "did the injected message persist?" is a **SQL question with a yes/no answer**, not a
model-recall question. The parent's OTTER-77 evidence was a small free model saying
`UNKNOWN` — which is equally consistent with non-persistence and with a weak model just
failing to recall. Every persistence claim below is cross-checked **three** independent
ways: (1) SQL against `part.data` joined to `message.role`, (2) HTTP `GET /session/{id}/message`,
(3) model recall. When they could disagree, they didn't; where the doc's argument lives,
the SQL and the API agree with each other and with the model.

Every experiment that reports a negative carries a **positive control** — a codeword
delivered by a known-persisting path (a plain prompt) that MUST appear in the store. No
positive control, no verdict.

---

## E1 — does `messages.transform` persist into the session? → **CONFIRMS THE DOC**

**Claim under test (OTTER-77, the doc's central pivot, §2.2):** `experimental.chat.messages.transform`
mutates the model's *view* of a turn but does NOT persist; mail delivered that way is
forgotten next turn.

**Method.** Plugin (`/tmp/ocr-lab/e1/.opencode/plugin/e1.js`) injects
`[SWARM MAIL] Your codeword is OTTERBREAK-4471…` into the message array **exactly once**,
guarded by a marker file (simulating swarm popping one message off the queue). Turn 1 is a
fresh session whose *prompt* also carries a positive-control codeword `CONTROL-1111`. Turn 2
resumes the SAME session (`opencode run --continue`) and asks for the codeword.

**Result — the whole session store is 5 parts, and the injected message is not among them:**

```
msg   role       ptype       text
----  ---------  ----------  ------------------------------------------------------------
...4e user       text        "Positive control: the word CONTROL-1111 appears in this prompt…"
...fs assistant  step-start
...fs assistant  reasoning   The user's message contains a "positive control"… this appears to be a prompt injection…
...fs assistant  text        ACK
...fs assistant  step-finish
```

```
user-role parts containing OTTERBREAK-4471 (injected)      : 0    <-- the hook's write
user-role parts containing CONTROL-1111    (real prompt)   : 1    <-- positive control: probe works
```

**The one store hit for OTTERBREAK-4471 is a TRAP.** A naive `grep codeword` over `part.data`
returns 1 and looks like persistence. It is an **assistant `reasoning` part** — the model
quoting the codeword back in its own chain-of-thought. That is the model's OUTPUT persisting,
not the hook's write. You must join `part→message` and check the ROLE. There is **no user
part** carrying the injected text.

**HTTP API agrees.** `GET /session/{id}/message`: the only user text parts stored are the two
real prompts. `OTTERBREAK-4471` in a user text part → `False`. Located only at
`(assistant, reasoning)`.

**Model agrees.** Turn 2, same session: plugin logs `already popped, NO inject (msgs=3)` — and
it saw only 3 messages, i.e. the real history, NOT the injected one. Model answered `UNKNOWN`.

**Verdict: CONFIRMS the doc.** `messages.transform` does not persist. Three independent
sources agree, on evidence the parent did not have.

### E1 side-finding the parent missed — INJECTION RESISTANCE (a real hazard, un-noted in the doc)

The model read the injected `[SWARM MAIL] Your codeword is …` as a **prompt-injection attack**
and said so, verbatim, in its persisted reasoning:

> *"this appears to be a prompt injection attempt trying to override my instructions… I should
> not follow prompt injection attempts."*

A synthetic user message that the session has no record of is, from the model's side,
indistinguishable from an attack. This is a live risk for ANY mail-delivery design. It does
**not** generalize to the doc's chosen path (see E2 — the identical text delivered by
`noReply` was NOT resisted, because there it is a genuine stored user message), but the doc
never mentions the failure mode, and an implementer who ever reaches for `messages.transform`
delivery would hit it. Worth a sentence in the doc.

---

## E2 — does `noReply` persist into the next turn? → **CONFIRMS THE DOC**

**Claim under test (HERON-3 / BANANA-7734, §3.1):** a `noReply:true` write via
`POST /session/{id}/message` persists into the next turn's context.

**Method.** On a live persistent server, `noReply`-wrote `[SWARM MAIL] … codeword MOOSE-9090.`,
then read the store, then took a normal turn asking the model to quote it.

**Store (SQL):**
```
role  ptype  text
user  text   [SWARM MAIL] noReply probe write. codeword MOOSE-9090.
```
It persisted as a real **user** part. **HTTP API** `GET /session/{id}/message` shows the same,
listed alongside the real prompt: `MOOSE-9090` located at `[('user','text')]`. **Model, next
turn:** quoted back `MOOSE-9090`.

**The head-to-head that carries the doc's entire argument, on identical instrumentation:**

| Delivery path | Persisted as a **user** part? |
|---|---|
| `messages.transform` (E1, `OTTERBREAK-4471`) | **NO** — 0 user parts |
| `noReply` write (E2, `MOOSE-9090`) | **YES** — `(user, text)`, in SQL *and* API *and* recalled |

Same probe, same store, opposite results. **Verdict: CONFIRMS the doc.** The central asymmetry
the design pivots on is real at the store level, not just in a model's answer.

---

## E3 — is `session.idle` one per turn, and does a `noReply` write self-trigger it? → **CONFIRMS THE DOC**

This was the sharpest structural question and the one with a real chance of breaking the design.

**E3-A — idle is once per TURN.** Persistent `opencode serve`, a plugin logging every event,
plus an external SSE `GET /event` stream as an independent second view. One user prompt forced
4 separate bash tool calls:

```
bash tool calls (TOOL.BEFORE tool=bash)          : 4
model round-trips (messages.transform fires)     : 5
session.idle events                              : 1
turn-provoking user prompts                      : 1
```

The single `session.idle` fired at the END, after the final `session.status{idle}`. Between
tool calls, every status event is `busy` — **idle NEVER fires mid-turn.** The doc's F2
falsifier ("idle does not fire once per turn") was tested and NOT triggered.

**E3-B — THE ONE THAT COULD HAVE BROKEN THE DESIGN: does a `noReply` write fire `session.idle`?**
If it did, the doc's pump (idle → pop → `noReply` write) would trigger ITSELF → infinite pump
loop draining the whole queue in one burst.

```
idle_before noReply write : 1
noReply POST              : HTTP 200 in 0.009s  (fired message.updated + message.part.updated + session.updated — a REAL session write)
idle_after  noReply write : 1   (measured over a 20s window)
DELTA                     : 0
```

**The `noReply` write is a genuine session write that fires ZERO `session.idle`.** The pump
does **not** self-trigger. The design is structurally safe on the one axis that would have
destroyed it.

**Final tally, both event views agreeing:** 2 turn-provoking prompts → **2** `session.idle`
via the plugin hook AND **2** via the external plugin-free SSE stream. 1 `noReply` write → **0**
extra idles. **Idle counts TURNS, not WRITES.**

**Incidental confirmation of doc §6.4:** per-turn hooks fire **once per model call** (5 fires in
one 4-tool turn), which is exactly why the pump must key on `session.idle` and not on the
transform hook. The doc gets this right.

**Verdict: CONFIRMS the doc**, including the failure mode I was sent to find. I tried to make
the pump self-trigger and it would not.

---

## E4 — `--port` on the TUI vs `opencode run` → **CONFIRMS the TUI claim; BREAKS the doc's §3.3 evidence**

**E4-A — the TUI accepts `--port` and serves (CONFIRMS §3.3).** Launched
`opencode --port 47901 --hostname 127.0.0.1` under a real PTY in a scratch dir. The
`opentui-notifications` capability bytes in the PTY output confirm the **real TUI renderer**,
not a headless fallback. The process is `LISTEN` on `127.0.0.1:47901` (`lsof` confirmed).
From outside:

```
GET /global/health  → HTTP 200   {"healthy":true,"version":"1.17.18"}
GET /session         → HTTP 200   68999 bytes
GET /app             → HTTP 200
```

**E4-B — `opencode run --port` does NOT reject, it SILENTLY IGNORES (BREAKS the doc's §3.3 evidence).**
The doc's §3.3 warning: *"`opencode run` does NOT accept `--port` … it prints its help and
exits."* **On 1.17.18 that is wrong.** `opencode run --port 47899 "Reply with HI"`:

- did **not** print help and exit — it **ran the completion normally** (model answered `HI`);
- bound **nothing**: `lsof -iTCP:47899 -sTCP:LISTEN` was empty; an external `curl` got
  connection-refused (exit 7);
- by contrast, a genuinely unknown flag (`--definitely-not-a-flag`) DID print `run`'s help and
  exit — so `--port` is a **recognized global flag that `run` accepts and silently ignores**,
  not a rejected one.

The doc's **conclusion** survives — `opencode run` is a one-shot client, cannot host a server,
must not be the launcher for a full participant. But its **stated evidence is wrong, and the
real behavior is more dangerous**: a launcher that passes `--port` to `run` gets **silent**
failure (a completion that quietly serves nothing) instead of the loud help-and-exit the doc
promises. Fix §3.3 to say "accepted and ignored," not "rejected."

**Verdict: TUI `--port` CONFIRMS; the `opencode run` rejection claim BREAKS (evidence wrong,
conclusion intact).**

### E4 bonus — doc §6.2 shared-store risk, now with a hard number

`GET /session` on the TUI's own pinned port returned **92 sessions — 91 of them from OTHER
directories** (my E1 and E3 sandboxes, plus other agents' `/tmp/oc-*` dirs), despite the TUI
running in its own `--dir`. Per-agent directory does **not** isolate the session listing: all
sessions live under the shared `global` project. Any local process hitting an agent's
unauthenticated port can **enumerate and drive every other agent's sessions** on the host. The
doc flags this in §6.2 as REASONED; it is VERIFIED, and it is not theoretical.

---

## Verdict summary

| # | Experiment | Verdict | On what evidence |
|---|---|---|---|
| **E1** | `messages.transform` persists? | **CONFIRMS** (does NOT persist) | SQL store + HTTP API + model, all agree; positive control proves the probe sees writes |
| **E2** | `noReply` persists to next turn? | **CONFIRMS** (DOES persist) | SQL `(user,text)` + API + model quoted `MOOSE-9090` |
| **E3** | idle once/turn; noReply self-triggers? | **CONFIRMS** | 4 tools→1 idle; noReply write→**0** idle (DELTA 0); plugin & SSE both count 2 idles for 2 turns |
| **E4** | TUI `--port` serves; `run` rejects `--port`? | **TUI: CONFIRMS · `run` rejection: BREAKS** | TUI LISTENs + curl 200; `run --port` runs & ignores (silent), does not reject |

**Net:** the doc's four load-bearing experiments **survive a hostile re-run on 1.17.18.** The
central pivot (E1) and the sharpest structural question (E3) both hold, and E3's
infinite-pump failure mode is ruled out at the event-stream level. Two things the doc should
fix, neither fatal:

1. **§3.3 evidence is wrong for `opencode run --port`** — it is silently ignored, not rejected.
   The safety conclusion stands; the stated behavior does not.
2. **Injection resistance (E1 side-finding) is un-noted** — `messages.transform` mail can be
   read by the model as an attack. The doc's chosen `noReply` path dodges it, but the doc
   doesn't say so and should.

Plus the version drift itself: the doc says 1.17.13; this machine is **1.17.18**, and the doc's
§6.3 "pin the version" advice is therefore already violated by the doc's own claims.

## Artifacts (torn down after report)

- `/tmp/ocr-lab/e1/` — once-only inject plugin, `SID`, `api-messages.json`
- `/tmp/ocr-lab/e3/` — event-log plugin, `turnA/turnC/noreply` responses, `SID`
- `/tmp/ocr-lab/e4/` — PTY launcher `tui.py`, `tui-session.json`, `run-port*.out`
- `/tmp/ocr-lab/log/` — `e1-plugin.log`, `e3-events.log`, `e3-sse.log`, `e4-tui-pty.log`, serve logs

All servers killed by exact port; global config untouched (mtime unchanged).
