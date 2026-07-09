#!/usr/bin/env bash
# tests/inbox.sh — executable spec for the inbox read/ack contract.
#
#   bash tests/inbox.sh            # run everything, print PASS/FAIL per case
#
# Every case runs against a THROWAWAY SWARM_DIR under a mktemp root. Nothing here
# ever touches a live ./.swarm: that directory holds running agents' registry,
# state and inboxes, and corrupting it takes down the whole swarm. The trap wipes
# the temp root on exit, including on failure.
#
# No framework, no dependencies beyond what `swarm` itself needs (bash, python3,
# node). The repo has no test runner; this file is meant to be read as much as
# run, so each case states the property it is defending before it asserts it.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
SWARM="$REPO/bin/swarm"
HOOK="$REPO/bin/swarm-hook.cjs"

TMPROOT="$(mktemp -d "${TMPDIR:-/tmp}/swarm-inbox-test.XXXXXX")"
trap 'rm -rf "$TMPROOT"' EXIT

# CRITICAL: these tests distinguish the OPERATOR path from the AGENT path, and
# the only thing that distinguishes them is whether SWARM_AGENT_ID is set. When
# this suite is run BY an agent (which is how it was written), that variable is
# already in the environment — so every "operator" assertion silently exercised
# the agent path instead, against the agent's own inbox name. Unset it here; each
# case that wants the agent path sets it explicitly, per command.
unset SWARM_AGENT_ID SWARM_AGENT_LABEL

pass=0; fail=0
ok()   { pass=$((pass+1)); printf '  \033[32mPASS\033[0m %s\n' "$1"; }
bad()  { fail=$((fail+1)); printf '  \033[31mFAIL\033[0m %s\n' "$1"; [ $# -gt 1 ] && printf '        %s\n' "$2"; }
case_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# A fresh swarm root per case. Guard hard against ever pointing at a real one.
fresh() {
  SWARM_DIR="$TMPROOT/$1/.swarm"
  case "$SWARM_DIR" in "$TMPROOT"/*) :;; *) echo "REFUSING: SWARM_DIR outside temp root" >&2; exit 2;; esac
  rm -rf "$SWARM_DIR"; mkdir -p "$SWARM_DIR/inbox" "$SWARM_DIR/updates" "$SWARM_DIR/agents"
  export SWARM_DIR
}

# Plant a message file directly (bypasses `swarm send`, so we can simulate mail
# that predates the size limit — exactly what an upgraded swarm finds on disk).
plant() { # plant <box> <ts> <from> <body>
  local box="$SWARM_DIR/inbox/$1" ts="$2" from="$3" body="$4"
  mkdir -p "$box"
  BOX="$box" TS="$ts" FROM="$from" TO="$1" BODY="$body" python3 - <<'PY'
import json,os
r={"id":f"{os.environ['FROM']}-{os.environ['TS']}","to":os.environ["TO"],
   "from":os.environ["FROM"],"ts":int(os.environ["TS"]),"type":"message",
   "body":os.environ["BODY"],"read":False}
json.dump(r,open(os.path.join(os.environ["BOX"],f"{os.environ['TS']}-{os.environ['FROM']}.json"),"w"))
PY
}

# Run the delivery hook as agent <id> and capture the injected context (or '').
inject() { # inject <agent-id>  -> prints additionalContext to stdout
  echo '{}' | SWARM_AGENT_ID="$1" node "$HOOK" inbox-check 2>/dev/null \
    | python3 -c 'import json,sys
raw=sys.stdin.read()
if not raw.strip(): sys.exit(0)
print(json.load(open("/dev/stdin")) if False else json.loads(raw)["hookSpecificOutput"]["additionalContext"],end="")'
}

# The three states. `nunread` counts only NEVER-RENDERED messages (files directly
# under the box); `nrendered` counts delivered-but-unacked; `nread` counts acked.
# UNACKED = nunread + nrendered.
nunread()   { ls "$SWARM_DIR/inbox/$1"/*.json 2>/dev/null | wc -l | tr -d ' '; }
nrendered() { ls "$SWARM_DIR/inbox/$1"/rendered/*.json 2>/dev/null | wc -l | tr -d ' '; }
nread()     { ls "$SWARM_DIR/inbox/$1"/read/*.json 2>/dev/null | wc -l | tr -d ' '; }
nunacked()  { echo $(( $(nunread "$1") + $(nrendered "$1") )); }

# ---------------------------------------------------------------------------
case_ "V1 — send rejects an oversized body, and writes NOTHING"
fresh v1
# `send` to `operator` needs no registry entry, so this isolates the size guard.
big="$(python3 -c 'print("x"*6001,end="")')"
out="$("$SWARM" send operator "$big" 2>&1)"; rc=$?
[ "$rc" -ne 0 ] && ok "exit code nonzero ($rc)" || bad "exit code was 0"
case "$out" in
  *"message too big (6001 > 6000); store large content as a file and reference its path in the message."*)
    ok "exact error text: $out";;
  *) bad "error text mismatch" "$out";;
esac
[ "$(nunread operator)" = "0" ] && ok "nothing written to inbox" || bad "inbox got $(nunread operator) file(s)"

# Boundary: 5999 / 6000 accepted, 6001 rejected.
for n in 5999 6000; do
  body="$(python3 -c "print('x'*$n,end='')")"
  if "$SWARM" send operator "$body" >/dev/null 2>&1; then ok "$n bytes accepted"; else bad "$n bytes rejected (should accept)"; fi
done
body="$(python3 -c "print('x'*6001,end='')")"
"$SWARM" send operator "$body" >/dev/null 2>&1 && bad "6001 bytes accepted (should reject)" || ok "6001 bytes rejected"
# A multibyte body is limited by BYTES, not characters: 3000 × 2-byte chars = 6000.
mb="$(python3 -c "print('é'*3001,end='')")"
"$SWARM" send operator "$mb" >/dev/null 2>&1 && bad "6002 bytes (3001 × 'é') accepted" || ok "limit counts bytes, not characters"

# ---------------------------------------------------------------------------
case_ "V2 — 5-message overflow: honest header, remainder readable and ack-able"
fresh v2
for i in 1 2 3 4 5; do plant tester "100$i" "sender$i" "$(python3 -c "print('$i'*2600,end='')")"; done
ctx="$(inject tester)"
hdr="$(printf '%s' "$ctx" | head -1)"
printf '  header verbatim: %s\n' "$hdr"
case "$hdr" in
  "[swarm inbox] Showing 2 of 5 new messages (3 remain — they will be shown next turn):") ok "honest header names shown-vs-total";;
  *) bad "header does not name shown-vs-total" "$hdr";;
esac
case "$ctx" in *"…and 3 more; full messages in inbox/tester/"*) ok "'…and N more' disclosure preserved";; *) bad "lost the '…and N more' disclosure";; esac
[ "${#ctx}" -le 8000 ] && ok "injection ${#ctx} chars <= 8000" || bad "injection ${#ctx} chars > 8000"
[ "$(nunread tester)" = "3" ] && ok "3 messages never rendered" || bad "expected 3 unrendered, got $(nunread tester)"
[ "$(nrendered tester)" = "2" ] && ok "2 injected messages moved to rendered/" || bad "expected 2 rendered, got $(nrendered tester)"
[ "$(nread tester)" = "0" ] && ok "injection acked NOTHING into read/" || bad "injection put $(nread tester) in read/"
# The withheld remainder AND the rendered-but-unacked pair are all outstanding.
out="$(SWARM_AGENT_ID=tester "$SWARM" inbox read 2>&1)"
case "$out" in *"5 unacked message(s)"*) ok "'inbox read' shows all 5 unacked (3 unrendered + 2 rendered)";; *) bad "read did not show 5" "$(printf '%s' "$out" | head -1)";; esac
[ "$(nunacked tester)" = "5" ] && ok "read did not consume" || bad "read consumed messages"
# ...and ack-able by naming the highest id — sweeping BOTH states.
SWARM_AGENT_ID=tester "$SWARM" inbox ack sender5-1005 >/dev/null 2>&1 \
  && [ "$(nunacked tester)" = "0" ] && [ "$(nread tester)" = "5" ] \
  && ok "cumulative ack sweeps rendered/ and inbox/ alike" || bad "ack of remainder failed"

# ---------------------------------------------------------------------------
case_ "V3 — operator mail survives repeated 'updates --json' polls"
fresh v3
plant operator 2001 rd "escalation body"
for i in 1 2 3 4; do
  n="$("$SWARM" updates --json 2>/dev/null | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["inbox"]))')"
  [ "$n" = "1" ] && ok "poll #$i still sees the message" || bad "poll #$i lost it (inbox len=$n)"
done
"$SWARM" updates >/dev/null 2>&1
[ "$(nunread operator)" = "1" ] && ok "human-readable 'updates' also non-destructive" || bad "plain 'updates' consumed mail"
"$SWARM" inbox ack rd-2001 >/dev/null 2>&1
[ "$(nunread operator)" = "0" ] && [ "$(nread operator)" = "1" ] && ok "explicit ack consumes it (moved to read/)" || bad "ack did not consume"
n="$("$SWARM" updates --json 2>/dev/null | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["inbox"]))')"
[ "$n" = "0" ] && ok "after ack, inbox is empty" || bad "after ack, inbox len=$n"

# ---------------------------------------------------------------------------
case_ "V4 — ack is cumulative, must name an outstanding id, and there is no ack-all"
fresh v4
plant operator 3001 a "first"
plant operator 3002 b "second"
plant operator 3003 c "third"
# Bare `ack` errors.
"$SWARM" inbox ack >/dev/null 2>&1 && bad "'ack' with no id succeeded" || ok "'ack' with no id errors"
# An id that is not outstanding errors, and acks NOTHING.
"$SWARM" inbox ack nope-9999 >/dev/null 2>&1 && bad "ack of unknown id succeeded" || ok "ack of a non-outstanding id errors"
[ "$(nunread operator)" = "3" ] && ok "failed ack consumed nothing" || bad "failed ack consumed something"
# No ack-all, in any spelling. Assert BEHAVIOURALLY (each spelling must exit
# nonzero AND consume nothing), not by grepping the source for a string.
for spelling in --all -a --everything --yes all "*"; do
  "$SWARM" inbox ack "$spelling" >/dev/null 2>&1 \
    && bad "'ack $spelling' succeeded — an ack-all exists" \
    || ok "'ack $spelling' rejected"
done
[ "$(nunread operator)" = "3" ] && ok "no ack-all spelling consumed anything" || bad "an ack-all spelling consumed mail"
# Cumulative: acking the highest sweeps the prefix, and NAMES what it swept.
out="$("$SWARM" inbox ack c-3003 2>&1)"
case "$out" in *"acked 3 message(s) through c-3003"*) ok "cumulative prefix acked";; *) bad "not cumulative" "$out";; esac
case "$out" in *"a-3001"*"swept by cumulative ack"*) ok "names the swept N+1 messages (not silent)";; *) bad "swept ids not named" "$out";; esac
[ "$(nunread operator)" = "0" ] && [ "$(nread operator)" = "3" ] && ok "all three moved to read/" || bad "prefix move wrong"
# Re-acking an already-acked id errors rather than silently succeeding.
"$SWARM" inbox ack c-3003 >/dev/null 2>&1 && bad "re-ack succeeded" || ok "re-ack of a consumed id errors"
# Cumulative ack of a MIDDLE id leaves later messages outstanding.
fresh v4b
plant operator 4001 a "first"; plant operator 4002 b "second"; plant operator 4003 c "third"
"$SWARM" inbox ack b-4002 >/dev/null 2>&1
[ "$(nunread operator)" = "1" ] && [ "$(nread operator)" = "2" ] && ok "ack of middle id leaves the suffix unread" || bad "middle ack wrong"

# ---------------------------------------------------------------------------
case_ "V5 — no single message can exceed the injection budget"
fresh v5
# (a) At the largest size `send` will now accept.
"$SWARM" send operator "$(python3 -c 'print("z"*5999,end="")')" >/dev/null 2>&1
mv "$SWARM_DIR/inbox/operator" "$SWARM_DIR/inbox/tester"
ctx="$(inject tester)"
[ "${#ctx}" -le 8000 ] && ok "largest accepted send (5999B) injects ${#ctx} chars <= 8000" || bad "5999B blew the cap: ${#ctx}"
case "$ctx" in *"[truncated"*) bad "an accepted message should never truncate";; *) ok "an accepted message is injected whole";; esac
# (b) The hook guards independently — a hand-planted oversized file (a message
#     that predates the send limit, already on disk) must not blow the cap.
fresh v5b
plant tester 5001 a "$(python3 -c 'print("q"*20000,end="")')"
plant tester 5002 b "small"
ctx="$(inject tester)"
[ "${#ctx}" -le 8000 ] && ok "hand-planted 20KB message injects ${#ctx} chars <= 8000" || bad "20KB blew the cap: ${#ctx}"
case "$ctx" in *"[truncated"*) ok "oversized body truncated with a visible marker";; *) bad "no truncation marker";; esac
fresh v5c
plant tester 6001 a "$(python3 -c 'print("q"*100000,end="")')"
ctx="$(inject tester)"
[ "${#ctx}" -le 8000 ] && ok "hand-planted 100KB message injects ${#ctx} chars <= 8000" || bad "100KB blew the cap: ${#ctx}"

# ---------------------------------------------------------------------------
case_ "V6 — back-compat: agent --json stays a bare ARRAY, operator gets the object"
fresh v6
plant operator 7001 a "op mail"
shape="$("$SWARM" updates --json 2>/dev/null | python3 -c 'import json,sys; print(type(json.load(sys.stdin)).__name__)')"
[ "$shape" = "dict" ] && ok "operator --json -> object {updates,inbox}" || bad "operator --json shape = $shape"
shape="$(SWARM_AGENT_ID=someagent "$SWARM" updates --json 2>/dev/null | python3 -c 'import json,sys; print(type(json.load(sys.stdin)).__name__)')"
[ "$shape" = "list" ] && ok "agent --json -> bare array (unchanged)" || bad "agent --json shape = $shape"
shape="$("$SWARM" updates --id someagent --json 2>/dev/null | python3 -c 'import json,sys; print(type(json.load(sys.stdin)).__name__)')"
[ "$shape" = "list" ] && ok "--id --json -> bare array (unchanged)" || bad "--id --json shape = $shape"
# A pre-existing message with no 'id' field (written before ids existed) must not
# crash any reader; it simply cannot be acked by name.
fresh v6b
mkdir -p "$SWARM_DIR/inbox/operator"
python3 -c "
import json
json.dump({'to':'operator','from':'old','ts':1,'type':'message','body':'legacy','read':False},
          open('$SWARM_DIR/inbox/operator/1-old.json','w'))"
"$SWARM" updates >/dev/null 2>&1 && ok "legacy record (no id) does not crash 'updates'" || bad "'updates' crashed on legacy record"
"$SWARM" inbox read >/dev/null 2>&1 && ok "legacy record does not crash 'inbox read'" || bad "'inbox read' crashed on legacy record"
printf '{"broken' > "$SWARM_DIR/inbox/operator/2-corrupt.json"
"$SWARM" inbox read >/dev/null 2>&1 && ok "corrupt record is skipped, not fatal" || bad "'inbox read' crashed on corrupt record"

# ---------------------------------------------------------------------------
case_ "V7 — EPIPE mid-write leaves the message UNACKED (regression guard on emitAndExit)"
fresh v7
plant tester 8001 a "body that never lands"
# The reader vanishes: pipe the hook into a process that exits immediately. The
# hook's stdout write fails with EPIPE, so the post-write ack must not run.
echo '{}' | SWARM_AGENT_ID=tester node "$HOOK" inbox-check 2>/dev/null | true
rc=${PIPESTATUS[1]:-0}
[ "$(nunread tester)" = "1" ] && ok "message still UNREAD after EPIPE" || bad "EPIPE acked the message"
[ "$(nread tester)" = "0" ] && ok "nothing moved into read/" || bad "read/ got a file"
# ...and the hook still exits 0 (never breaks the turn).
[ "$rc" = "0" ] && ok "hook exit 0 under EPIPE" || bad "hook exited $rc under EPIPE"

# ---------------------------------------------------------------------------
case_ "V8 — prime directive: bogus SWARM_DIR / empty inbox -> exit 0, silent"
out="$(echo '{}' | SWARM_DIR=/nonexistent/nope SWARM_AGENT_ID=ghost node "$HOOK" inbox-check 2>/dev/null)"; rc=$?
[ "$rc" = "0" ] && [ -z "$out" ] && ok "bogus SWARM_DIR: exit 0, no output" || bad "bogus SWARM_DIR: rc=$rc out='$out'"
fresh v8
mkdir -p "$SWARM_DIR/inbox/tester"
out="$(echo '{}' | SWARM_AGENT_ID=tester node "$HOOK" inbox-check 2>/dev/null)"; rc=$?
[ "$rc" = "0" ] && [ -z "$out" ] && ok "empty inbox: exit 0, no output" || bad "empty inbox: rc=$rc out='$out'"
out="$(echo '{}' | SWARM_DIR="" SWARM_AGENT_ID=tester node "$HOOK" inbox-check 2>/dev/null)"; rc=$?
[ "$rc" = "0" ] && [ -z "$out" ] && ok "unset SWARM_DIR: exit 0, no output" || bad "unset SWARM_DIR: rc=$rc"

# ---------------------------------------------------------------------------
case_ "The incident: an injected message stays outstanding until claimed by id"
# Two messages arrive 37s apart, both small enough that BOTH are injected and
# nothing is withheld. Under the old hook both were auto-acked into read/ the
# instant they were injected, so a directive that was read-but-not-acted-on
# became indistinguishable from one that never arrived. That is the bug this
# whole change exists to prevent for the operator's channel.
#
# The asymmetry proposal 005 shipped with — "for AGENTS, injection acks" — is GONE
# (operator ruling, 2026-07-09). Injection now marks a message RENDERED, not read;
# nothing but an explicit `swarm inbox ack` reaches read/, for agent or operator
# alike. The operator's directive below must survive repeated reads, as before.
fresh incident
plant operator 9000 sibling "$(python3 -c 'print("s"*4699,end="")')"
plant operator 9037 operator "$(python3 -c 'print("d"*2036,end="")')"
"$SWARM" updates >/dev/null 2>&1   # the operator's channel is read...
"$SWARM" updates --json >/dev/null 2>&1
[ "$(nunread operator)" = "2" ] && ok "reading twice left BOTH messages outstanding" || bad "reading consumed operator mail"
# Act on the sibling message only, and claim exactly it.
"$SWARM" inbox ack sibling-9000 >/dev/null 2>&1
[ "$(nunread operator)" = "1" ] && ok "acking the sibling leaves the directive outstanding" || bad "the directive was swept"
out="$("$SWARM" inbox read 2>&1)"
case "$out" in *"operator-9037"*) ok "the unacted directive is still visible, by id";; *) bad "directive vanished" "$out";; esac

# ---------------------------------------------------------------------------
case_ "V9 — a rendered message is never re-injected; it becomes a one-line nag"
fresh v9
plant nagbox 1101 boss "the directive body"
ctx="$(inject nagbox)"
case "$ctx" in *"the directive body"*) ok "turn 1 injects the body";; *) bad "turn 1 did not inject the body";; esac
[ "$(nunread nagbox)" = "0" ] && [ "$(nrendered nagbox)" = "1" ] && [ "$(nread nagbox)" = "0" ] \
  && ok "moved to rendered/, NOT read/" || bad "state after render: $(nunread nagbox)/$(nrendered nagbox)/$(nread nagbox)"
ctx2="$(inject nagbox)"
printf '  nag verbatim: %s\n' "$ctx2"
case "$ctx2" in *"the directive body"*) bad "turn 2 RE-INJECTED the body";; *) ok "turn 2 does not re-inject the body";; esac
[ "$(printf '%s' "$ctx2" | wc -l | tr -d ' ')" = "0" ] && ok "the nag is exactly ONE line" || bad "nag spans multiple lines"
case "$ctx2" in
  "[swarm inbox] 1 message(s) delivered earlier and still UNACKED: boss-1101 — re-read with \`swarm inbox read\`; clear with \`swarm inbox ack <id>\` (cumulative).")
    ok "nag names the id and the ack hint";;
  *) bad "unexpected nag text" "$ctx2";;
esac
# It keeps nagging, turn after turn, until acked. That is the point.
ctx3="$(inject nagbox)"; [ "$ctx3" = "$ctx2" ] && ok "the nag repeats on every later turn" || bad "nag changed/stopped"
[ "$(nrendered nagbox)" = "1" ] && ok "nagging has no side effect (nothing moved)" || bad "the nag moved a file"
# Explicit ack clears it, and the hook falls silent.
SWARM_AGENT_ID=nagbox "$SWARM" inbox ack boss-1101 >/dev/null 2>&1
[ "$(nread nagbox)" = "1" ] && [ "$(nrendered nagbox)" = "0" ] && ok "ack moves rendered/ -> read/" || bad "ack did not consume the rendered message"
out="$(inject nagbox)"
[ -z "$out" ] && ok "after ack: hook is silent again" || bad "still nagging after ack" "$out"

# ---------------------------------------------------------------------------
case_ "V10 — unacked = inbox/ + rendered/; a turn with both nags only the carried"
fresh v10
plant mix 2101 a "first"
inject mix >/dev/null                 # a-2101 -> rendered/
plant mix 2102 b "second"             # never rendered
[ "$(nunacked mix)" = "2" ] && ok "unacked counts both states (2)" || bad "unacked = $(nunacked mix)"
ctx="$(inject mix)"
case "$ctx" in *"second"*) ok "the NEW body is injected";; *) bad "new body not injected";; esac
case "$ctx" in *"first"*) bad "the rendered body was re-injected";; *) ok "the rendered body is not re-injected";; esac
case "$ctx" in *"still UNACKED: a-2101"*) ok "the carried message is nagged by id";; *) bad "carried id not nagged" "$ctx";; esac
[ "$(nunacked mix)" = "2" ] && [ "$(nrendered mix)" = "2" ] && ok "both are now rendered, both still unacked" || bad "state wrong"
# `inbox read` sees both, marks which was already delivered, and consumes neither.
out="$(SWARM_AGENT_ID=mix "$SWARM" inbox read 2>&1)"
case "$out" in *"2 unacked message(s)"*) ok "'inbox read' shows both";; *) bad "read did not show 2" "$out";; esac
case "$out" in *"already delivered to your context; unacked"*) ok "read marks the delivered ones";; *) bad "no delivered marker";; esac
[ "$(nunacked mix)" = "2" ] && ok "read consumed nothing" || bad "read consumed"
n="$(SWARM_AGENT_ID=mix "$SWARM" inbox read --json 2>/dev/null | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')"
[ "$n" = "2" ] && ok "'inbox read --json' is a bare array of both" || bad "--json len=$n"

# ---------------------------------------------------------------------------
case_ "V11 — cumulative ack sweeps rendered/ and inbox/ in ARRIVAL order"
fresh v11
plant cum 3101 p "one"; plant cum 3102 q "two"
inject cum >/dev/null                       # p,q -> rendered/
plant cum 3103 r "three"; plant cum 3104 s "four"   # never rendered
[ "$(nunread cum)" = "2" ] && [ "$(nrendered cum)" = "2" ] && ok "2 unrendered + 2 rendered" || bad "setup wrong"
out="$(SWARM_AGENT_ID=cum "$SWARM" inbox ack r-3103 2>&1)"
case "$out" in *"acked 3 message(s) through r-3103"*) ok "ack sweeps the prefix across both dirs";; *) bad "prefix wrong" "$out";; esac
case "$out" in *"p-3101"*"swept by cumulative ack"*) ok "names the rendered messages it swept";; *) bad "swept rendered ids not named" "$out";; esac
[ "$(nunread cum)" = "1" ] && [ "$(nrendered cum)" = "0" ] && [ "$(nread cum)" = "3" ] && ok "s-3104 alone stays outstanding" || bad "final state $(nunread cum)/$(nrendered cum)/$(nread cum)"
# read/ still means acked-only: already_acked recognises a swept, rendered message.
out="$(SWARM_AGENT_ID=cum "$SWARM" inbox ack p-3101 2>&1)"; rc=$?
[ "$rc" -ne 0 ] && ok "re-acking a swept message errors" || bad "re-ack succeeded"
case "$out" in *"already acknowledged"*) ok "already_acked() sees it in read/";; *) bad "wrong error" "$out";; esac

# ---------------------------------------------------------------------------
case_ "V12 — EPIPE on the NAG path is also harmless, and nags again next turn"
fresh v12
plant epipe 4101 a "body"
inject epipe >/dev/null                     # -> rendered/
echo '{}' | SWARM_AGENT_ID=epipe node "$HOOK" inbox-check 2>/dev/null | true
rc=${PIPESTATUS[1]:-0}
[ "$rc" = "0" ] && ok "nag path exits 0 under EPIPE" || bad "nag path exited $rc"
[ "$(nrendered epipe)" = "1" ] && [ "$(nread epipe)" = "0" ] && ok "the nag has no side effect to lose" || bad "EPIPE moved a file"
ctx="$(inject epipe)"
case "$ctx" in *"still UNACKED: a-4101"*) ok "still nagging on the next turn";; *) bad "nag lost";; esac
# And an empty rendered/ dir is as silent as no inbox at all.
fresh v12b
mkdir -p "$SWARM_DIR/inbox/quiet/rendered"
out="$(echo '{}' | SWARM_AGENT_ID=quiet node "$HOOK" inbox-check 2>/dev/null)"; rc=$?
[ "$rc" = "0" ] && [ -z "$out" ] && ok "empty rendered/: exit 0, no output" || bad "empty rendered/: rc=$rc out='$out'"

# ---------------------------------------------------------------------------
case_ "V13 — a legacy record (no 'id' field) can still be named, nagged, and acked"
# Under the old hook this was harmless: injection acked it. Now an unnameable
# message would nag forever, because the agent could never name it to ack it.
fresh v13
mkdir -p "$SWARM_DIR/inbox/leg"
python3 -c "
import json
json.dump({'to':'leg','from':'old','ts':1,'type':'message','body':'legacy body','read':False},
          open('$SWARM_DIR/inbox/leg/1-old.json','w'))"
ctx="$(inject leg)"
case "$ctx" in *"[id old-1]"*) ok "the injection FRAMES it with a derived id";; *) bad "framed as [id ?] — unackable" "$(printf '%s' "$ctx" | sed -n 2p)";; esac
ctx2="$(inject leg)"
case "$ctx2" in *"still UNACKED: old-1"*) ok "the nag names the derived id";; *) bad "nag cannot name it" "$ctx2";; esac
SWARM_AGENT_ID=leg "$SWARM" inbox ack old-1 >/dev/null 2>&1 \
  && [ "$(nread leg)" = "1" ] && ok "and it can be acked by that id" || bad "legacy message is unackable"

# ---------------------------------------------------------------------------
case_ "V14 — backpressure: 49 unacked accepts, 50 refuses, nothing is queued"
fresh v14
# 49 unacked, all never-rendered. `send` to operator needs no registry entry.
for i in $(seq 1 49); do plant operator "$((10000+i))" s "m$i"; done
[ "$(nunacked operator)" = "49" ] && ok "setup: 49 unacked" || bad "setup wrong: $(nunacked operator)"
printf 'accepted at 49' | "$SWARM" send operator --stdin >/dev/null 2>&1 \
  && ok "at 49 unacked: send accepted (exit 0)" || bad "at 49 unacked: send refused"
[ "$(nunacked operator)" = "50" ] && ok "…and the message was written" || bad "nothing written at 49"
out="$(printf 'refused at 50' | "$SWARM" send operator --stdin 2>&1)"; rc=$?
[ "$rc" -ne 0 ] && ok "at 50 unacked: send refused (exit $rc)" || bad "at 50 unacked: send accepted"
printf '  error verbatim: %s\n' "$out"
case "$out" in *"agent busy, 50 unacked, try again later"*) ok "error names the count and the shape";; *) bad "error text mismatch" "$out";; esac
[ "$(nunacked operator)" = "50" ] && ok "NOTHING was queued on refusal" || bad "refusal queued a message: $(nunacked operator)"
ls "$SWARM_DIR/inbox/operator"/*.tmp >/dev/null 2>&1 && bad "a .tmp file was left behind" || ok "no partial write left behind"
# V15 below proves the refused body never appears later.

# ---------------------------------------------------------------------------
case_ "V15 — the cap counts BOTH unacked states, and read/ does not count"
fresh v15
mkdir -p "$SWARM_DIR/agents"
printf '{"id":"capped","pane":""}' > "$SWARM_DIR/agents/capped.json"
# Bodies big enough that the 8000-char injection cap withholds most of them, so the
# box ends up genuinely SPLIT across both unacked states.
for i in $(seq 1 49); do plant capped "$((20000+i))" s "$(python3 -c "print('b'*1000,end='')")"; done
# Render some of them: the injection moves a prefix into rendered/. They still count.
inject capped >/dev/null
r="$(nrendered capped)"; u="$(nunread capped)"
[ "$r" -gt 0 ] && [ "$u" -gt 0 ] && ok "split across both states: $r rendered, $u never rendered" \
  || bad "not a mix: $r rendered, $u unrendered"
[ "$(nunacked capped)" = "49" ] && ok "unacked still 49 across both states" || bad "unacked = $(nunacked capped)"
printf 'x' | "$SWARM" send capped --stdin >/dev/null 2>&1 && ok "49 across both states still accepts" || bad "refused at 49"
[ "$(nunacked capped)" = "50" ] && ok "now 50 unacked" || bad "count wrong"
printf 'REFUSED-BODY-MARKER' | "$SWARM" send capped --stdin >/dev/null 2>&1 && bad "50 accepted" || ok "50 refuses"
# Acked mail does not count: drain one, and a send is accepted again.
oldest="$(SWARM_AGENT_ID=capped "$SWARM" inbox read --json 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)[0]["id"])')"
SWARM_AGENT_ID=capped "$SWARM" inbox ack "$oldest" >/dev/null 2>&1
[ "$(nread capped)" = "1" ] && ok "one message acked into read/" || bad "ack failed"
[ "$(nunacked capped)" = "49" ] && ok "read/ does not count toward the cap" || bad "read/ counted: $(nunacked capped)"
printf 'accepted after ack' | "$SWARM" send capped --stdin >/dev/null 2>&1 && ok "the box accepts mail again" || bad "still refusing after drain"
# The REFUSED message never appears — not now, not later.
grep -rl "REFUSED-BODY-MARKER" "$SWARM_DIR/inbox/capped" >/dev/null 2>&1 \
  && bad "the refused body was queued after all" || ok "the refused body never appears (nothing queued)"

# ---------------------------------------------------------------------------
case_ "V16 — the cap applies to 'operator' identically, and to an agent target"
fresh v16
for i in $(seq 1 50); do plant operator "$((30000+i))" s "m$i"; done
out="$(printf 'to the human' | "$SWARM" send operator --stdin 2>&1)"; rc=$?
[ "$rc" -ne 0 ] && ok "operator target refuses at 50 (exit $rc)" || bad "operator target accepted at 50"
case "$out" in *"agent busy, 50 unacked"*) ok "same error shape for operator";; *) bad "operator error differs" "$out";; esac
[ "$(nunacked operator)" = "50" ] && ok "nothing queued for the operator" || bad "operator got a queued message"
# An unknown id still fails on the registry guard, not the cap.
out="$(printf 'x' | "$SWARM" send nosuchagent --stdin 2>&1)"; rc=$?
[ "$rc" -ne 0 ] && case "$out" in *"unknown agent: nosuchagent"*) ok "unknown id still fails the registry guard";; *) bad "wrong error" "$out";; esac

# ---------------------------------------------------------------------------
case_ "V17 — self-lockout is escapable: ack needs no incoming message"
fresh v17
mkdir -p "$SWARM_DIR/agents"; printf '{"id":"stuck","pane":""}' > "$SWARM_DIR/agents/stuck.json"
for i in $(seq 1 50); do plant stuck "$((40000+i))" s "m$i"; done
printf 'x' | "$SWARM" send stuck --stdin >/dev/null 2>&1 && bad "capped agent accepted mail" || ok "capped agent refuses mail"
# It can still SEE its unacked ids — on its own turn, through the hook (a different
# path from the send cap), and through its own `inbox read`. No incoming message needed.
ctx="$(inject stuck)"
[ -n "$ctx" ] && ok "the hook still surfaces its inbox to it (nag/injection path is not gated)" || bad "capped agent is blind"
n="$(SWARM_AGENT_ID=stuck "$SWARM" inbox read --json 2>/dev/null | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')"
[ "$n" = "50" ] && ok "'swarm inbox read' works on its OWN box with no incoming message" || bad "inbox read shows $n"
# Ack its way out, one message, and mail flows again.
first="$(SWARM_AGENT_ID=stuck "$SWARM" inbox read --json 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)[0]["id"])')"
SWARM_AGENT_ID=stuck "$SWARM" inbox ack "$first" >/dev/null 2>&1
[ "$(nunacked stuck)" = "49" ] && ok "ack drops it to 49 unacked" || bad "ack did not drain"
printf 'you are back' | "$SWARM" send stuck --stdin >/dev/null 2>&1 && ok "it can receive again" || bad "still refusing at 49"

# ---------------------------------------------------------------------------
case_ "V18 — the nag's id round-trips: read finds it, ack consumes it"
# The failure this defends: the nag names an id that `swarm inbox read` — the exact
# verb the nag recommends — cannot show. Announced and unfindable. So take the id
# STRAIGHT OUT OF THE NAG LINE and feed it to both verbs.
fresh v18
plant rt 1 a "one"; plant rt 2 b "two"
inject rt >/dev/null                        # both -> rendered/
nag="$(inject rt)"
ids="$(printf '%s' "$nag" | sed -n 's/.*still UNACKED: \(.*\) — re-read.*/\1/p')"
[ -n "$ids" ] && ok "the nag yields parseable ids: $ids" || bad "cannot parse ids out of the nag" "$nag"
first="$(printf '%s' "$ids" | cut -d, -f1 | tr -d ' ')"
SWARM_AGENT_ID=rt "$SWARM" inbox read 2>/dev/null | grep -q "id $first" \
  && ok "'swarm inbox read' shows the id the nag named" || bad "the nag named an id 'read' cannot show: $first"
SWARM_AGENT_ID=rt "$SWARM" inbox ack "$first" >/dev/null 2>&1 \
  && ok "'swarm inbox ack <that id>' succeeds" || bad "the nag named an id 'ack' rejects: $first"
last="$(printf '%s' "$ids" | cut -d, -f2 | tr -d ' ')"
SWARM_AGENT_ID=rt "$SWARM" inbox ack "$last" >/dev/null 2>&1
[ -z "$(inject rt)" ] && ok "acking every named id silences the nag" || bad "still nagging"

# ---------------------------------------------------------------------------
case_ "V19 — the count and the list agree across all three states; reading moves nothing"
fresh v19
plant agree 1 a "acked"; plant agree 2 b "rendered one"; plant agree 3 c "rendered two"
inject agree >/dev/null                     # all three -> rendered/
plant agree 4 d "never rendered"
SWARM_AGENT_ID=agree "$SWARM" inbox ack a-1 >/dev/null 2>&1
[ "$(nunread agree)" = "1" ] && [ "$(nrendered agree)" = "2" ] && [ "$(nread agree)" = "1" ] \
  && ok "on disk: 1 never-rendered, 2 rendered-unacked, 1 acked" || bad "state $(nunread agree)/$(nrendered agree)/$(nread agree)"
n="$(SWARM_AGENT_ID=agree "$SWARM" inbox read --json 2>/dev/null | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')"
[ "$n" = "3" ] && [ "$n" = "$(nunacked agree)" ] && ok "reader lists exactly the $n unacked (no counted-but-unlistable)" || bad "list=$n count=$(nunacked agree)"
d="$(SWARM_AGENT_ID=agree "$SWARM" inbox read --json 2>/dev/null | python3 -c 'import json,sys; print(sum(1 for r in json.load(sys.stdin) if r["delivered"]))')"
[ "$d" = "2" ] && ok "and marks exactly the 2 already-delivered" || bad "delivered flag count = $d"
ctx="$(inject agree)"
case "$ctx" in *"never rendered"*) ok "the hook injects only the never-rendered body";; *) bad "wrong body injected";; esac
case "$ctx" in *"b-2"*"c-3"*) ok "…and names both rendered-unacked ids in the nag";; *) bad "nag lost an id" "$ctx";; esac
# Reading three times leaves both dirs byte-identical.
fresh v19b
plant nd 1 a "x"; plant nd 2 b "y"
inject nd >/dev/null
before="$(find "$SWARM_DIR/inbox/nd" -name '*.json' | sort | tr '\n' ' ')"
for i in 1 2 3; do SWARM_AGENT_ID=nd "$SWARM" inbox read >/dev/null 2>&1; SWARM_AGENT_ID=nd "$SWARM" inbox read --json >/dev/null 2>&1; done
after="$(find "$SWARM_DIR/inbox/nd" -name '*.json' | sort | tr '\n' ' ')"
[ "$before" = "$after" ] && ok "3× 'inbox read' moves nothing (inbox/ and rendered/ unchanged)" || bad "read moved files"

# ---------------------------------------------------------------------------
printf '\n\033[1m%d passed, %d failed\033[0m\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
