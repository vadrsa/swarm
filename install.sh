#!/usr/bin/env bash
# install.sh — wire swarm into this machine.
#
# swarm is one file (bin/swarm) plus the world doc it prints; this script does
# the three machine-specific things: put `swarm` on PATH, activate the skill
# for Claude Code, and check prerequisites. Idempotent — safe to re-run.
#
#   ./install.sh             install (or re-install)
#   ./install.sh --uninstall remove the symlinks this script created

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_SRC="$REPO/bin/swarm"
SKILL_SRC="$REPO/skill"
SKILL_DST="$HOME/.claude/skills/swarm"
SKILL2_SRC="$REPO/skill-middleware"
SKILL2_DST="$HOME/.claude/skills/swarm-middleware"
# Prefer ~/.local/bin (usually on PATH); fall back to advising a PATH export.
BIN_DST="$HOME/.local/bin/swarm"

say()  { printf '  %s\n' "$*"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$*"; }
err()  { printf '  \033[31m✗\033[0m %s\n' "$*"; }

uninstall() {
  echo "Uninstalling swarm…"
  [ -L "$SKILL_DST" ]  && { rm -f "$SKILL_DST";  ok "removed skill symlink $SKILL_DST"; }   || say "no skill symlink"
  [ -L "$SKILL2_DST" ] && { rm -f "$SKILL2_DST"; ok "removed skill symlink $SKILL2_DST"; }  || say "no swarm-middleware skill symlink"
  [ -L "$BIN_DST" ]    && { rm -f "$BIN_DST";    ok "removed bin symlink $BIN_DST"; }       || say "no bin symlink"
  echo "Done. (Your .swarm/ state dirs and PATH edits were left untouched.)"
  exit 0
}

case "${1:-}" in
  --uninstall) uninstall;;
  "")          ;;
  *)           err "unknown flag: $1"; echo "usage: ./install.sh [--uninstall]" >&2; exit 1;;
esac

if [ -L "$BIN_DST" ] || [ -L "$SKILL_DST" ] || [ -L "$SKILL2_DST" ]; then
  echo "Re-installing swarm from: $REPO (existing install detected)"
else
  echo "Installing swarm from: $REPO"
fi
echo

# 1. Prerequisites -----------------------------------------------------------
echo "Checking prerequisites:"
missing=0
for dep in herdr claude python3; do
  if command -v "$dep" >/dev/null 2>&1; then ok "$dep"; else err "$dep not found on PATH"; missing=1; fi
done
if [ "$missing" -ne 0 ]; then
  warn "Some prerequisites are missing. swarm needs all of them at runtime:"
  say "  herdr   — the terminal multiplexer that holds subagent panes (herdr.dev)"
  say "  claude  — the Claude Code CLI (the agent harness)"
  say "  python3 — the interpreter that runs swarm itself"
  say "Install the missing ones, then re-run ./install.sh"
fi
echo

# 2. Put `swarm` on PATH -----------------------------------------------------
echo "Linking the CLI:"
chmod +x "$BIN_SRC" 2>/dev/null || true
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
if [ -e "$SKILL2_DST" ] && [ ! -L "$SKILL2_DST" ]; then
  warn "$SKILL2_DST exists and is not a symlink — leaving it. Remove it and re-run to link."
else
  ln -sfn "$SKILL2_SRC" "$SKILL2_DST"
  ok "symlinked $SKILL2_DST -> $SKILL2_SRC"
fi
echo

echo "Done."
echo "  • Start a NEW Claude Code session so it picks up the skill (or its updates)."
echo "  • Inside a herdr pane, say e.g.  \"start a swarm to <goal>\""
echo "  • The tool writes state into a .swarm/ dir in your project — add it to"
echo "    that project's .gitignore if you don't want it committed."
echo "  • .swarm/config is JSON now (it used to be flat-TOML-ish). An old-format"
echo "    file still there after upgrading will warn on the next 'swarm models'"
echo "    or spawn and fail open (no middleware, no permission-mode default) —"
echo "    convert it to the JSON shape in docs/design/PRODUCTIZE.md §2."
# TODO(PR2): note the yoke prereq (bun + a configured opencode fork) here once
# yoke's install.sh wiring lands.
