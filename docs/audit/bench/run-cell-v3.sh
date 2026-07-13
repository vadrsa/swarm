#!/usr/bin/env bash
# run-cell-v3.sh — the CLEAN-RIG rerun of run-cell.sh, applying FLEET-EVAL.md's
# own v3 recommendations (§5a §5b §5c §5d §5e). Same battery shape, same rubric
# (fleet-rubric-v1.md), briefs fleet-briefs-v3/ (= v2 + d2-heavy amendment).
#
# THE FOUR FIXES (each mapped to the doc):
#  §5a  the runner AND every probe name are REGISTERED sandbox agents
#       (register-agent.py), so `swarm send <runner>` / `send <probe>` deliver
#       instead of "unknown agent". Message consumption for opencode models is
#       performed by deliver-next.py — which IMPORTS bin/swarm and emits the
#       byte-exact next_delivery() injection, then moves the file to delivered/.
#       The harness does for an opencode model precisely what the Claude-pane
#       deliver hook does for a native one. D2-heavy becomes MULTI-TURN: the
#       model's children send to the MODEL's name; the pump delivers one report
#       per turn; receive→verify is witnessed through swarm's queue.
#  §5b  d2-heavy brief tells every model to spawn children with --cwd {REPO}:
#       cwd management is OFF the measured surface (v1/v2 measured it; that
#       verdict stands there). Delegation is scored on weigh/brief/verify/close.
#  §5c  M2 relation is scored UNIFORMLY: the pump injects the real relation
#       header (computed by bin/swarm's own relation()) in both opencode cells;
#       the native baseline gets it from the real hook. No hand-injection.
#  §5d  session-id extractor fixed (sed capture instead of broken grep anchor).
#  §5e  a PATH shim pins SWARM_DIR for EVERY swarm invocation the model makes,
#       and the cell snapshots the live .swarm/journal before/after so
#       containment is VERIFIED, not assumed.
#
# USAGE: run-cell-v3.sh <model-slug> <sandbox-dir> [runner-name]
# Scoring stays the runner's job, from files, per fleet-rubric-v1.md.

set -uo pipefail

MODEL="${1:?usage: run-cell-v3.sh <model-slug> <sandbox-dir> [runner-name]}"
SANDBOX="${2:?usage: run-cell-v3.sh <model-slug> <sandbox-dir> [runner-name]}"
RUNNER="${3:-${SWARM_AGENT_ID:-fleet-eval}}"

SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRIEFS="$SELF/fleet-briefs-v3"
HELPERS="$SELF/v3-helpers"
REPO="$(cd "$SELF/../../.." && pwd)"
SWARM_REAL="$(command -v swarm)"

[ -d "$BRIEFS" ] || { echo "FATAL: briefs dir not found: $BRIEFS" >&2; exit 2; }
[ -f "$HELPERS/deliver-next.py" ] || { echo "FATAL: v3 helpers missing" >&2; exit 2; }

mkdir -p "$SANDBOX/out" "$SANDBOX/swarm" "$SANDBOX/bin" || exit 2
SANDBOX="$(cd "$SANDBOX" && pwd)"
export SWARM_DIR="$SANDBOX/swarm"

case "$SWARM_DIR" in
  "$REPO/.swarm"|*/git/*/.swarm)
    echo "FATAL: refusing to run — SWARM_DIR looks like a live tree: $SWARM_DIR" >&2
    exit 3 ;;
esac
if [ -e "$SWARM_DIR/journal" ] && [ -n "$(ls -A "$SWARM_DIR/journal" 2>/dev/null)" ]; then
  echo "FATAL: sandbox journal non-empty — not fresh: $SWARM_DIR" >&2; exit 3
fi
if [ "${HERDR_ENV:-}" != "1" ]; then
  echo "[v3] WARNING: HERDR_ENV != 1 — model spawns will fail as [H]." >&2
fi

# ── §5e: the swarm shim — every `swarm` the MODEL runs gets SWARM_DIR pinned ──
cat > "$SANDBOX/bin/swarm" <<SHIM
#!/usr/bin/env bash
SWARM_DIR="$SWARM_DIR" exec "$SWARM_REAL" "\$@"
SHIM
chmod +x "$SANDBOX/bin/swarm"
export PATH="$SANDBOX/bin:$PATH"

# containment snapshot (before)
ls "$REPO/.swarm/journal" 2>/dev/null | sort > "$SANDBOX/live-journal-before.txt"

# ── §5a: registration ────────────────────────────────────────────────────────
python3 "$HELPERS/register-agent.py" "$SWARM_DIR" "$RUNNER" operator
for N in b-d1 b-d2c b-d2h b-d3a b-d3b b-d3c b-d4; do
  python3 "$HELPERS/register-agent.py" "$SWARM_DIR" "$N" "$RUNNER"
done

render() {  # render <brief-file> <name> <outdir>
  sed -e "s|{NAME}|$2|g" -e "s|{RUNNER}|$RUNNER|g" \
      -e "s|{OUTDIR}|$3|g" -e "s|{REPO}|$REPO|g" "$1"
}

oc_turn() {  # oc_turn <name> <prompt-text> <transcript-file> [extra args...]
  local name="$1" prompt="$2" tx="$3"; shift 3
  # SWARM_AGENT_ID pinned per probe: without it the RUNNER's identity leaks
  # through opencode's env and every model-issued `swarm send` is mis-attributed
  # (caught in the v3 smoke run — sender read "field-tester", not the probe).
  SWARM_AGENT_ID="$name" opencode run --auto --dir "$SANDBOX" -m "$MODEL" \
      --agent "$name" --format json "$@" -- "$prompt" 2>&1 | tee "$tx"
}

sid_of() {  # §5d fixed extractor
  grep -oE '"sessionID"[: ]*"[^"]+"' "$1" | head -1 | sed 's/.*"\([^"]*\)"$/\1/'
}

mkdir -p "$SANDBOX/out"/{d1,d2cheap,d2heavy,d3a,d3b,d3c,d4}

# ── D1 duties ────────────────────────────────────────────────────────────────
echo "[v3] D1 duties…" >&2
O="$SANDBOX/out/d1"; N="b-d1"
P="$(render "$BRIEFS/00-duties-preamble.md" "$N" "$O")
$(render "$BRIEFS/d1-duties.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript.txt"

# ── D2 cheap ─────────────────────────────────────────────────────────────────
echo "[v3] D2 cheap…" >&2
O="$SANDBOX/out/d2cheap"; N="b-d2c"
P="$(render "$BRIEFS/00-duties-preamble.md" "$N" "$O")
$(render "$BRIEFS/d2-cheap.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript.txt"

# ── D2 heavy — MULTI-TURN with the delivery pump (§5a; serialized; capped) ───
echo "[v3] D2 heavy (multi-turn, pumped)…" >&2
O="$SANDBOX/out/d2heavy"; N="b-d2h"
P="$(render "$BRIEFS/00-duties-preamble.md" "$N" "$O")
$(render "$BRIEFS/d2-heavy.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript-t1.txt"
SID="$(sid_of "$O/transcript-t1.txt")"
# pump: up to 14 follow-up turns / 25 min wall. Each turn = ONE delivered
# message if the model-agent has mail, else a neutral idle nudge only when its
# children are still live (never nudge a finished cell into hallucinating).
T0=$(date +%s)
TURN=1
while [ $TURN -le 14 ] && [ $(( $(date +%s) - T0 )) -lt 1500 ]; do
  if MSG="$(python3 "$HELPERS/deliver-next.py" "$SWARM_DIR" "$N")"; then
    TURN=$((TURN+1))
    if [ -n "$SID" ]; then
      oc_turn "$N" "$MSG" "$O/transcript-t$TURN.txt" --session "$SID"
    else
      oc_turn "$N" "$MSG" "$O/transcript-t$TURN.txt" --continue
    fi
    continue
  fi
  # no mail: are any of the model's children (parent==b-d2h) still live panes?
  LIVE=$(python3 - "$SWARM_DIR" <<'PY'
import json, os, subprocess, sys
root = sys.argv[1]
try:
    p = subprocess.run(["herdr", "pane", "list"], capture_output=True, text=True, timeout=10)
    live = {x.get("pane_id") for x in json.loads(p.stdout).get("result", {}).get("panes", [])}
except Exception:
    live = set()
n = 0
d = os.path.join(root, "agents")
for fn in os.listdir(d) if os.path.isdir(d) else []:
    try:
        r = json.load(open(os.path.join(d, fn)))
        if r.get("parent") == "b-d2h" and r.get("pane") in live:
            n += 1
    except Exception:
        pass
print(n)
PY
)
  R1=$(ls "$O"/report-*.md 2>/dev/null | wc -l | tr -d ' ')
  if [ "$LIVE" = "0" ] && [ "$R1" -ge 4 ]; then break; fi   # done: reports in, kids gone
  if [ "$LIVE" = "0" ] && [ $(( $(date +%s) - T0 )) -gt 600 ]; then break; fi
  sleep 20
done
echo "[v3] D2-heavy pump ended after $TURN turn(s), $(( $(date +%s) - T0 ))s." >&2

# ── D3a exact paths ──────────────────────────────────────────────────────────
echo "[v3] D3a exact-paths…" >&2
O="$SANDBOX/out/d3a"; N="b-d3a"
P="$(render "$BRIEFS/d3a-exact-paths.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript.txt"

# ── D3b swarm-CLI ────────────────────────────────────────────────────────────
echo "[v3] D3b swarm-CLI…" >&2
O="$SANDBOX/out/d3b"; N="b-d3b"
P="$(render "$BRIEFS/d3b-swarm-cli.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript.txt"

# ── D3c — REAL sends + the pump (§5a/§5c): M1/M2/M3 now cross swarm's queue ──
echo "[v3] D3c delivery (real queue)…" >&2
O="$SANDBOX/out/d3c"; N="b-d3c"
P="$(render "$BRIEFS/d3c-standby.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript-setup.txt"
SID="$(sid_of "$O/transcript-setup.txt")"
for M in M1-nearcap M2-relation M3-plain; do
  render "$BRIEFS/d3-$M.txt" "$N" "$O" \
    | SWARM_DIR="$SWARM_DIR" SWARM_AGENT_ID="$RUNNER" "$SWARM_REAL" send "$N" --stdin
  MSG="$(python3 "$HELPERS/deliver-next.py" "$SWARM_DIR" "$N")" || { echo "[v3] FATAL: queued M lost" >&2; break; }
  if [ -n "$SID" ]; then
    oc_turn "$N" "$MSG" "$O/transcript-$M.txt" --session "$SID"
  else
    oc_turn "$N" "$MSG" "$O/transcript-$M.txt" --continue
  fi
done

# ── D4 long-horizon ──────────────────────────────────────────────────────────
echo "[v3] D4 coherence…" >&2
O="$SANDBOX/out/d4"; N="b-d4"
P="$(render "$BRIEFS/d4-turn1.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript-t1.txt"
SID="$(sid_of "$O/transcript-t1.txt")"
P="$(render "$BRIEFS/d4-turn2-distractor.md" "$N" "$O")"
if [ -n "$SID" ]; then
  oc_turn "$N" "$P" "$O/transcript-t2.txt" --session "$SID"
else
  oc_turn "$N" "$P" "$O/transcript-t2.txt" --continue
fi
P="$(render "$BRIEFS/d4-turn3-restart.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript-t3.txt"

# ── containment snapshot (after) + pinned header ─────────────────────────────
ls "$REPO/.swarm/journal" 2>/dev/null | sort > "$SANDBOX/live-journal-after.txt"
{
  echo "# Fleet bench cell v3 — $(cd "$REPO" && git rev-parse --short HEAD 2>/dev/null)"
  echo "model:      $MODEL"
  echo "runner:     $RUNNER (REGISTERED sandbox agent — §5a fix)"
  echo "SWARM_DIR:  $SWARM_DIR (sandbox; shim-pinned for all model swarm calls — §5e fix)"
  echo "repo:       main@$(cd "$REPO" && git rev-parse HEAD 2>/dev/null)"
  echo "bin/swarm:  md5 $(md5 -q "$REPO/bin/swarm" 2>/dev/null || md5sum "$REPO/bin/swarm" | awk '{print $1}')"
  echo "installed:  md5 $(md5 -q "$SWARM_REAL" 2>/dev/null || md5sum "$SWARM_REAL" | awk '{print $1}')  ($SWARM_REAL)"
  echo "opencode:   $(opencode --version 2>/dev/null)"
  echo "herdr:      HERDR_ENV=${HERDR_ENV:-<unset>}"
  echo "briefs:     fleet-briefs-v3/ (v2 + d2-heavy amendment) — md5s:"
  ( cd "$BRIEFS" && for f in *.md *.txt; do
      printf '            %-26s %s\n' "$f" "$(md5 -q "$f" 2>/dev/null || md5sum "$f" | awk '{print $1}')"
    done )
  echo "delivery:   deliver-next.py (imports bin/swarm; byte-exact next_delivery) — §5a/§5c"
  echo "relation:   M2 header rig-delivered via bin/swarm relation() — scored uniformly (§5c)"
  echo "containment: diff live-journal-before/after.txt (§5e) →"
  if cmp -s "$SANDBOX/live-journal-before.txt" "$SANDBOX/live-journal-after.txt"; then
    echo "             CLEAN — zero live-tree bleed"
  else
    echo "             DIRTY — see diff below"
    diff "$SANDBOX/live-journal-before.txt" "$SANDBOX/live-journal-after.txt" | sed 's/^/             /'
  fi
  echo "scoring:    from files only, by $RUNNER, per fleet-rubric-v1.md"
  cost="$(grep -rhoE '"cost"[: ]+[0-9.]+' "$SANDBOX/out" 2>/dev/null \
          | grep -oE '[0-9.]+' | LC_ALL=C awk '{s+=$1} END{printf "%.4f", s+0}')"
  echo "cost_usd_sum: ${cost:-0} (metered, --format json events)"
} > "$SANDBOX/header.txt"

echo "[v3] done. Artifacts + header under: $SANDBOX" >&2
