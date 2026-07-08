#!/usr/bin/env bash
# install.sh — wire the swarm package into this machine.
#
# The repo is self-contained and path-agnostic; this script does the three
# machine-specific things: put `swarm` on PATH, activate the skill for Claude
# Code, and check prerequisites. Safe to re-run (idempotent).
#
#   ./install.sh            install / update
#   ./install.sh --uninstall remove the symlinks this script created

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_SRC="$REPO/bin/swarm"
SKILL_SRC="$REPO/skill"
SKILL_DST="$HOME/.claude/skills/swarm"
# Prefer ~/.local/bin (usually on PATH); fall back to advising a PATH export.
BIN_DST="$HOME/.local/bin/swarm"

say()  { printf '  %s\n' "$*"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$*"; }
err()  { printf '  \033[31m✗\033[0m %s\n' "$*"; }

uninstall() {
  echo "Uninstalling swarm…"
  [ -L "$SKILL_DST" ] && { rm -f "$SKILL_DST"; ok "removed skill symlink $SKILL_DST"; } || say "no skill symlink"
  [ -L "$BIN_DST" ]   && { rm -f "$BIN_DST";   ok "removed bin symlink $BIN_DST"; }   || say "no bin symlink"
  echo "Done. (Your .swarm/ state dirs and PATH edits were left untouched.)"
  exit 0
}
[ "${1:-}" = "--uninstall" ] && uninstall

echo "Installing swarm from: $REPO"
echo

# 1. Prerequisites -----------------------------------------------------------
echo "Checking prerequisites:"
missing=0
for dep in herdr claude node python3; do
  if command -v "$dep" >/dev/null 2>&1; then ok "$dep"; else err "$dep not found on PATH"; missing=1; fi
done
if [ "$missing" -ne 0 ]; then
  warn "Some prerequisites are missing. swarm needs all of them at runtime:"
  say "  herdr   — the terminal multiplexer that holds subagent panes (herdr.dev)"
  say "  claude  — the Claude Code CLI (the agent harness)"
  say "  node    — runs the completion hook"
  say "  python3 — used by several swarm verbs"
  say "Install the missing ones, then re-run ./install.sh"
fi
echo

# 2. Put `swarm` on PATH -----------------------------------------------------
echo "Linking the CLI:"
chmod +x "$BIN_SRC" "$REPO/bin/swarm-hook.cjs" 2>/dev/null || true
mkdir -p "$(dirname "$BIN_DST")"
ln -sfn "$BIN_SRC" "$BIN_DST"
ok "symlinked $BIN_DST -> $BIN_SRC"
if ! command -v swarm >/dev/null 2>&1; then
  warn "$(dirname "$BIN_DST") is not on your PATH. Add this to your shell rc:"
  say "  export PATH=\"\$HOME/.local/bin:\$PATH\""
else
  ok "\`swarm\` is on your PATH"
fi
echo

# 3. Activate the skill for Claude Code --------------------------------------
echo "Activating the skill:"
mkdir -p "$(dirname "$SKILL_DST")"
if [ -e "$SKILL_DST" ] && [ ! -L "$SKILL_DST" ]; then
  warn "$SKILL_DST exists and is not a symlink — leaving it. Remove it and re-run to link."
else
  ln -sfn "$SKILL_SRC" "$SKILL_DST"
  ok "symlinked $SKILL_DST -> $SKILL_SRC"
fi
echo

echo "Done."
echo "  • Start a NEW Claude Code session so it picks up the skill."
echo "  • Inside a herdr pane, say e.g.  \"start a swarm to <goal>, max 3 agents\""
echo "  • The tool writes state into a .swarm/ dir in your project — add it to"
echo "    that project's .gitignore if you don't want it committed."
