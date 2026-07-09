#!/usr/bin/env bash
# bootstrap.sh — one-line installer for swarm.
#
#   curl -fsSL https://raw.githubusercontent.com/vadrsa/swarm/main/bootstrap.sh | sh
#
# Clones swarm into ~/.local/share/swarm (override with SWARM_HOME) and runs its
# install.sh. Re-running updates an existing clone (git pull + re-install).
#
# For development, prefer a manual clone somewhere you'll work in:
#   git clone https://github.com/vadrsa/swarm.git ~/git/swarm && ~/git/swarm/install.sh

set -eu

REPO_URL="${SWARM_REPO_URL:-https://github.com/vadrsa/swarm.git}"
# XDG data dir by default; SWARM_HOME overrides where the checkout lives.
DEFAULT_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/swarm"
SWARM_HOME="${SWARM_HOME:-$DEFAULT_HOME}"

say()  { printf '  %s\n' "$*"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
err()  { printf '  \033[31m✗\033[0m %s\n' "$*" >&2; }

command -v git >/dev/null 2>&1 || { err "git is required but not found on PATH"; exit 1; }

echo "swarm bootstrap"
echo "  target: $SWARM_HOME"
echo

if [ -d "$SWARM_HOME/.git" ]; then
  # Already installed here — update it (idempotent re-run).
  say "existing clone found — updating"
  # Refuse to clobber local edits (someone hacking on it).
  if ! git -C "$SWARM_HOME" diff --quiet || ! git -C "$SWARM_HOME" diff --cached --quiet; then
    err "$SWARM_HOME has uncommitted changes — commit/stash them, or pull and re-install yourself"
    exit 1
  fi
  git -C "$SWARM_HOME" fetch --quiet --tags origin
  git -C "$SWARM_HOME" checkout --quiet main 2>/dev/null || true
  git -C "$SWARM_HOME" pull --quiet --ff-only origin main
  ok "updated $SWARM_HOME"
elif [ -e "$SWARM_HOME" ]; then
  err "$SWARM_HOME exists but is not a swarm git clone. Remove it or set SWARM_HOME to another path."
  exit 1
else
  mkdir -p "$(dirname "$SWARM_HOME")"
  git clone --quiet "$REPO_URL" "$SWARM_HOME"
  ok "cloned into $SWARM_HOME"
fi
echo

# Hand off to the repo's own installer (symlinks + prereq checks).
"$SWARM_HOME/install.sh"
