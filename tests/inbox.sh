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

nunread() { ls "$SWARM_DIR/inbox/$1"/*.json 2>/dev/null | wc -l | tr -d ' '; }
nread()   { ls "$SWARM_DIR/inbox/$1"/read/*.json 2>/dev/null | wc -l | tr -d ' '; }

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
[ "$(nunread tester)" = "3" ] && ok "3 messages left unread" || bad "expected 3 unread, got $(nunread tester)"
# The withheld remainder is readable, without consuming it.
out="$(SWARM_AGENT_ID=tester "$SWARM" inbox read 2>&1)"
case "$out" in *"3 unread message(s)"*) ok "remainder visible via 'swarm inbox read'";; *) bad "read did not show 3" "$out";; esac
[ "$(nunread tester)" = "3" ] && ok "read did not consume" || bad "read consumed messages"
# ...and ack-able by naming the highest id.
SWARM_AGENT_ID=tester "$SWARM" inbox ack sender5-1005 >/dev/null 2>&1 \
  && [ "$(nunread tester)" = "0" ] && ok "remainder ack-able by highest id" || bad "ack of remainder failed"

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
# NOTE the asymmetry, which is proposal 005's actual verdict: for AGENTS,
# injection still acks — delivery is atomic with the turn and that guarantee is
# worth keeping. For the OPERATOR, who has no hook and no turn, nothing acks but
# an explicit ack. The operator's directive below is the one that must survive.
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
printf '\n\033[1m%d passed, %d failed\033[0m\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
