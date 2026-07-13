#!/usr/bin/env bash
# run-cell.sh — run the fleet instruction-following battery for ONE cell (one
# model) into a fresh sandbox, leaving all artifacts + a pinned header for the
# runner to SCORE BY READING (never by trusting this script's claims).
#
# Frozen with: fleet-briefs-v2/ (md5s in its MANIFEST.md), fleet-rubric-v1.md.
#   (v2 = v1 + {REPO}/ prefix on d1/d2-cheap; rig-bug fix, fleet-eval 2026-07-11.
#    The model's cwd is $SANDBOX, so bare repo paths resolved to nothing in v1 —
#    v2's briefs use absolute {REPO}/… paths, which --auto lets the model read.)
# Author: battery-smith → fleet-eval; v2 rig-fix by fleet-eval. DESIGN/FREEZE
# ARTIFACT — the paid run is fleet-eval's per-model runners' call, on approval.
#
# ── SAFETY INVARIANT (load-bearing) ────────────────────────────────────────
#   This script NEVER touches the live ./.swarm/. Every swarm operation — this
#   script's and the MODEL'S OWN `swarm spawn`/`send` — is redirected into the
#   sandbox by exporting SWARM_DIR=<sandbox>/swarm (bin/swarm:60 honors it). If
#   SWARM_DIR ever resolves to a real project .swarm/, this script aborts.
#
# ── COST (REASONED; FLEET.md §6 prices; falsifier: first metered run re-costs
#    if >2× off) ──────────────────────────────────────────────────────────────
#   Per cell ≈ 350–550k tokens (D2-heavy dominates: 150–300k, ×N if it spawns).
#   3-cell run (deepseek + GLM + claude-baseline):
#     deepseek-chat  ~$0.14/$0.28 per 1M  → ≈ $0.10–0.20 / cell
#     glm-4.7        ~$0.43/$1.74 per 1M  → ≈ $0.35–0.70 / cell
#     claude-haiku   (baseline)           → ≈ $0.40–0.90 / cell
#   DOLLAR CAP for the 3-cell run: request approval at <= $5 (headroom for
#   D2-heavy fan-out + re-runs of a FLAGGED cell-dimension). See rubric §8.
#
# ── USAGE ──────────────────────────────────────────────────────────────────
#   run-cell.sh <model-slug> <sandbox-dir> [runner-name]
#     <model-slug>   e.g. deepseek/deepseek-chat | zai-coding-plan/glm-4.7 |
#                    openrouter/anthropic/claude-haiku-4.5   (baseline, needs an
#                    OpenRouter key; else use the native-claude fallback rig,
#                    rubric §5a — NOT this script's opencode path)
#     <sandbox-dir>  fresh empty dir; becomes SANDBOX/{swarm,out,header.txt,...}
#     [runner-name]  the parent/runner agent name substituted for {RUNNER}
#                    (default: the value of $SWARM_AGENT_ID, else "fleet-eval")
#
# The script is intentionally linear and greppable. It runs each dimension,
# drops artifacts under SANDBOX/out/<dim>/, and writes SANDBOX/header.txt. It
# does NOT score — scoring is the runner's, from files, per fleet-rubric-v1.md.

set -uo pipefail

# ── args ───────────────────────────────────────────────────────────────────
MODEL="${1:?usage: run-cell.sh <model-slug> <sandbox-dir> [runner-name]}"
SANDBOX="${2:?usage: run-cell.sh <model-slug> <sandbox-dir> [runner-name]}"
RUNNER="${3:-${SWARM_AGENT_ID:-fleet-eval}}"

# resolve this script's dir so we find the frozen briefs regardless of cwd
SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRIEFS="$SELF/fleet-briefs-v2"   # v2: {REPO}/ prefix on d1/d2-cheap (rig-bug fix, see v2 MANIFEST)
REPO="$(cd "$SELF/../../.." && pwd)"   # docs/audit/bench → repo root

[ -d "$BRIEFS" ] || { echo "FATAL: briefs dir not found: $BRIEFS" >&2; exit 2; }
[ -f "$BRIEFS/MANIFEST.md" ] || { echo "FATAL: MANIFEST.md missing" >&2; exit 2; }

# ── sandbox + the safety invariant ─────────────────────────────────────────
mkdir -p "$SANDBOX/out" "$SANDBOX/swarm" || exit 2
SANDBOX="$(cd "$SANDBOX" && pwd)"
export SWARM_DIR="$SANDBOX/swarm"

# ABORT if SWARM_DIR could be a real project tree (belt + suspenders).
case "$SWARM_DIR" in
  "$REPO/.swarm"|*/git/*/.swarm)
    echo "FATAL: refusing to run — SWARM_DIR looks like a live tree: $SWARM_DIR" >&2
    exit 3 ;;
esac
if [ -e "$SWARM_DIR/journal" ] && [ -n "$(ls -A "$SWARM_DIR/journal" 2>/dev/null)" ]; then
  echo "FATAL: sandbox SWARM_DIR/journal is non-empty — not a fresh sandbox: $SWARM_DIR" >&2
  exit 3
fi

# swarm's own `spawn` needs herdr as the container (bin/swarm:865). If we are
# not inside herdr, D2-heavy delegation and D3b's spawn WILL fail — that is an
# [H] result the runner records, NOT a silent skip. Warn loudly, keep going.
if [ "${HERDR_ENV:-}" != "1" ]; then
  echo "[run-cell] WARNING: HERDR_ENV != 1 — the model's own \`swarm spawn\` will" >&2
  echo "[run-cell]          fail (bin/swarm:865). D2-heavy/D3b spawn checks will be" >&2
  echo "[run-cell]          [H] failures. Run this INSIDE herdr for the full battery." >&2
fi

# ── helpers ────────────────────────────────────────────────────────────────
# render a brief: substitute {NAME} {RUNNER} {OUTDIR} {REPO}. Reads a file,
# prints the rendered text on stdout.
render() {  # render <brief-file> <name> <outdir>
  sed -e "s|{NAME}|$2|g" -e "s|{RUNNER}|$RUNNER|g" \
      -e "s|{OUTDIR}|$3|g" -e "s|{REPO}|$REPO|g" "$1"
}

# run one opencode turn with a rendered prompt; capture session id (json) so a
# later turn can --session it. Streams to the pane AND tees a transcript file
# the runner reads for [H]/[M] tagging (rubric §3b, §4).
oc_turn() {  # oc_turn <name> <prompt-text> <transcript-file> [extra opencode args...]
  local name="$1" prompt="$2" tx="$3"; shift 3
  opencode run --auto --dir "$SANDBOX" -m "$MODEL" \
      --agent "$name" --format json "$@" -- "$prompt" 2>&1 | tee "$tx"
}

# NOTE on oc_turn: opencode `run` takes the message as positional args; we pass
# the rendered prompt as the final positional after `--` (so a prompt starting
# with `-` is never mistaken for a flag). `--format json` emits raw events incl.
# the session id — the runner greps the transcript for it. `--dir $SANDBOX` sets
# the model's cwd (so its file writes land in the sandbox); SWARM_DIR (exported)
# is what redirects any `swarm` command the model runs. Two different sandboxing
# axes — cwd vs swarm-root — and BOTH are required.
# Extra opencode args (e.g. --session <id>) go via "$@" BEFORE the `--`.

mkdir -p "$SANDBOX/out"/{d1,d2cheap,d2heavy,d3a,d3b,d3c,d4}

# ── D1 duties ──────────────────────────────────────────────────────────────
echo "[run-cell] D1 duties…" >&2
O="$SANDBOX/out/d1"; N="b-d1"
P="$(render "$BRIEFS/00-duties-preamble.md" "$N" "$O")
$(render "$BRIEFS/d1-duties.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript.txt"

# ── D2 cheap ───────────────────────────────────────────────────────────────
echo "[run-cell] D2 cheap…" >&2
O="$SANDBOX/out/d2cheap"; N="b-d2c"
P="$(render "$BRIEFS/00-duties-preamble.md" "$N" "$O")
$(render "$BRIEFS/d2-cheap.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript.txt"

# ── D2 heavy ── run ALONE (timing-sensitive; rubric §2c serialization note) ──
echo "[run-cell] D2 heavy (serialized)…" >&2
O="$SANDBOX/out/d2heavy"; N="b-d2h"
P="$(render "$BRIEFS/00-duties-preamble.md" "$N" "$O")
$(render "$BRIEFS/d2-heavy.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript.txt"

# ── D3a exact paths ────────────────────────────────────────────────────────
echo "[run-cell] D3a exact-paths…" >&2
O="$SANDBOX/out/d3a"; N="b-d3a"
P="$(render "$BRIEFS/d3a-exact-paths.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript.txt"

# ── D3b swarm-CLI syntax ───────────────────────────────────────────────────
echo "[run-cell] D3b swarm-CLI…" >&2
O="$SANDBOX/out/d3b"; N="b-d3b"
P="$(render "$BRIEFS/d3b-swarm-cli.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript.txt"

# ── D3c message-stream handling ────────────────────────────────────────────
# RIG (reconciled — rubric §3c). `opencode run` is NOT a live swarm pane draining
# its own queue: there is no Claude-Code `deliver` hook, so real `swarm send
# b-d3c …` cannot be consumed as an in-turn injection here. So the runner delivers
# M1/M2/M3 as CONTINUED SESSION TURNS (--session). Consequence, on the record:
# swarm's queue machinery (`delivered/` record, oldest-first queue order, the
# swarm relation-header) is NEVER exercised in this direction — those R2 D3 checks
# are DROPPED (rubric §7). What IS witnessed: M1 whole-context assembly (echo-1
# has amber+harbor, [H] on opencode's turn assembly), each turn's clause acted on
# (echo-1/2/3 exist & match), turn order (echo mtimes non-decreasing), and M3's
# completion note reaching the parent — the one message that DOES cross swarm's
# queue, because the MODEL runs `swarm send` itself (same path D3b verifies).
echo "[run-cell] D3c delivery…" >&2
O="$SANDBOX/out/d3c"; N="b-d3c"
P="$(render "$BRIEFS/d3c-standby.md" "$N" "$O")"
SID=""
TX="$O/transcript-setup.txt"
oc_turn "$N" "$P" "$TX"
SID="$(grep -oE '"sessionID"[: ]+"[^"]+"' "$TX" | head -1 | grep -oE '[^"]+$')"
for M in M1-nearcap M2-relation M3-plain; do
  MB="$(render "$BRIEFS/d3-$M.txt" "$N" "$O")"
  if [ -n "$SID" ]; then
    oc_turn "$N" "$MB" "$O/transcript-$M.txt" --session "$SID"
  else
    oc_turn "$N" "$MB" "$O/transcript-$M.txt" --continue
  fi
done

# ── D4 long-horizon coherence ──────────────────────────────────────────────
# turn1 (new session) → turn2 (--session, distractor) → turn3 (NEW session =
# simulated restart; the model must re-read its own journal). rubric §4.
echo "[run-cell] D4 coherence…" >&2
O="$SANDBOX/out/d4"; N="b-d4"
# turn 1
P="$(render "$BRIEFS/d4-turn1.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript-t1.txt"
SID="$(grep -oE '"sessionID"[: ]+"[^"]+"' "$O/transcript-t1.txt" | head -1 | grep -oE '[^"]+$')"
# turn 2 — same session (opencode continuity), distractor
P="$(render "$BRIEFS/d4-turn2-distractor.md" "$N" "$O")"
if [ -n "$SID" ]; then
  oc_turn "$N" "$P" "$O/transcript-t2.txt" --session "$SID"
else
  oc_turn "$N" "$P" "$O/transcript-t2.txt" --continue
fi
# turn 3 — FRESH session (no --session/--continue) = the simulated restart
P="$(render "$BRIEFS/d4-turn3-restart.md" "$N" "$O")"
oc_turn "$N" "$P" "$O/transcript-t3.txt"

# ── pinned header (rubric §5b) — facts, not claims ─────────────────────────
{
  echo "# Fleet bench cell — $(cd "$REPO" && git rev-parse --short HEAD 2>/dev/null)"
  echo "model:      $MODEL"
  echo "runner:     $RUNNER"
  echo "SWARM_DIR:  $SWARM_DIR   (sandbox — live .swarm/ untouched)"
  echo "repo:       main@$(cd "$REPO" && git rev-parse HEAD 2>/dev/null)"
  echo "bin/swarm:  md5 $(md5 -q "$REPO/bin/swarm" 2>/dev/null || md5sum "$REPO/bin/swarm" | awk '{print $1}')"
  echo "opencode:   $(opencode --version 2>/dev/null)"
  echo "harness:    opencode run --auto --dir $SANDBOX"
  echo "herdr:      HERDR_ENV=${HERDR_ENV:-<unset>}   (spawn checks are [H] if unset)"
  echo "briefs:     fleet-briefs-v2/ — md5s per MANIFEST.md:"
  ( cd "$BRIEFS" && for f in *.md *.txt; do
      printf '            %-26s %s\n' "$f" "$(md5 -q "$f" 2>/dev/null || md5sum "$f" | awk '{print $1}')"
    done )
  echo "scoring:    from files only, by $RUNNER, per fleet-rubric-v1.md; panes read only for flag/first-turn notes"
} > "$SANDBOX/header.txt"

# ── metered actuals for the cost-falsifier (VERIFIED: --format json emits
#    per-step "tokens":{…} and "cost":… — rubric §8) ─────────────────────────
# Sum the "cost" numbers across every transcript this cell produced. This is the
# MEASURED dollar figure the runner compares to the REASONED estimate (>2× off →
# re-cost). Best-effort text sum; the runner may recompute from the raw JSON.
{
  echo "# metered actuals (summed from --format json events; MEASURED)"
  cost="$(grep -rhoE '"cost"[: ]+[0-9.]+' "$SANDBOX/out" 2>/dev/null \
          | grep -oE '[0-9.]+' | awk '{s+=$1} END{printf "%.4f", s+0}')"
  echo "cost_usd_sum:   ${cost:-0}"
  echo "note: token fields are per-step under \"tokens\":{…}; sum them per the"
  echo "      rubric if a token total is wanted. Cell REASONED estimate: 350-550k tok."
} >> "$SANDBOX/header.txt"

echo "[run-cell] done. Artifacts + header under: $SANDBOX" >&2
echo "[run-cell] SCORE by reading — see fleet-rubric-v1.md. This script asserts nothing." >&2
