#!/bin/bash
# Bootstrap Claude's home (zin) on a new system.
# Run: ./setup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $*"; }
warn() { echo -e "${YELLOW}!${NC} $*"; }

echo "=== Setting up Claude's home (zin) ==="
echo ""

# ── 1. Install gh-token helper ─────────────────────────────────────────────
mkdir -p ~/.local/bin
cp "$SCRIPT_DIR/scripts/gh-token.sh" ~/.local/bin/gh-token
chmod +x ~/.local/bin/gh-token
ok "Installed gh-token → ~/.local/bin/gh-token"

# Ensure ~/.local/bin is on PATH
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  warn "~/.local/bin is not in PATH. Add this to your shell profile:"
  echo '    export PATH="$HOME/.local/bin:$PATH"'
fi

# ── 2. GitHub App credentials check ────────────────────────────────────────
echo ""
if [ -f ~/.config/github-app/credentials ] && [ -f ~/.config/github-app/private-key.pem ]; then
  ok "GitHub App credentials already at ~/.config/github-app/"
else
  warn "GitHub App credentials not found. Set them up:"
  echo "    mkdir -p ~/.config/github-app"
  echo "    # Create ~/.config/github-app/credentials:"
  echo "    #   GITHUB_APP_ID=<app-id>"
  echo "    #   GITHUB_APP_CLIENT_ID=<client-id>"
  echo "    #   GITHUB_APP_CLIENT_SECRET=<client-secret>"
  echo "    # Copy private key to ~/.config/github-app/private-key.pem"
  echo "    chmod 600 ~/.config/github-app/credentials ~/.config/github-app/private-key.pem"
fi

# ── 3. Install Claude skills ────────────────────────────────────────────────
echo ""
mkdir -p ~/.claude/skills
for skill_dir in "$SCRIPT_DIR/.claude/skills"/*/; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  target="$HOME/.claude/skills/$skill_name"
  # Remove existing symlink or directory, then re-link
  [ -L "$target" ] && rm "$target"
  [ -d "$target" ] && rm -rf "$target"
  ln -sf "$skill_dir" "$target"
  ok "Linked skill '/$skill_name' → ~/.claude/skills/$skill_name"
done

# ── 4. Done ─────────────────────────────────────────────────────────────────
echo ""
echo "=== Setup complete ==="
echo ""
echo "Start Claude Code from your project directory."
echo "Use /github to perform authenticated GitHub operations."
