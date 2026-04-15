#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# claude-code-on-steroids — install.sh
# Sets up the override layer and guides you through the one Claude Code step.
# Run: bash install.sh
# ─────────────────────────────────────────────────────────────────────────────

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OVERRIDES_DIR="$HOME/.claude/plugins/superpowers-overrides"
SETTINGS="$HOME/.claude/settings.json"
INSTALLED_PLUGINS="$HOME/.claude/plugins/installed_plugins.json"

# ── Colors ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
DIM='\033[2m'
BOLD='\033[1m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}✓${NC}  $1"; }
info() { echo -e "  ${CYAN}→${NC}  $1"; }
warn() { echo -e "  ${YELLOW}!${NC}  $1"; }
err()  { echo -e "  ${RED}✗${NC}  $1"; }
hr()   { echo -e "${DIM}  ────────────────────────────────────────────${NC}"; }

echo ""
echo -e "  ${BOLD}claude-code-on-steroids${NC} — installer"
hr

# ── Step 1: Check superpowers is installed ────────────────────────────────────
echo ""
info "Checking if superpowers plugin is installed…"

SUPERPOWERS_INSTALLED=false
if [ -f "$INSTALLED_PLUGINS" ]; then
  INSTALL_PATH=$(python3 -c "
import json, sys
try:
    data = json.load(open('$INSTALLED_PLUGINS'))
    p = data.get('plugins', {}).get('superpowers@claude-plugins-official', [])
    if p and p[0].get('installPath'):
        print(p[0]['installPath'])
except:
    pass
" 2>/dev/null)

  if [ -n "$INSTALL_PATH" ] && [ -d "$INSTALL_PATH" ]; then
    SUPERPOWERS_INSTALLED=true
    ok "superpowers is installed at: ${DIM}$INSTALL_PATH${NC}"
  fi
fi

if [ "$SUPERPOWERS_INSTALLED" = false ]; then
  warn "superpowers plugin is ${YELLOW}not installed${NC}."
  echo ""
  echo -e "  ${BOLD}Required first step:${NC}"
  echo -e "  Open Claude Code and run this slash command:"
  echo ""
  echo -e "      ${CYAN}/plugin install superpowers@claude-plugins-official${NC}"
  echo ""
  echo -e "  Then re-run this installer: ${DIM}bash install.sh${NC}"
  echo ""
  echo -e "  ${DIM}(superpowers provides the 24 base skills."
  echo -e "   claude-code-on-steroids overrides 9 of them with custom versions.)${NC}"
  echo ""
  exit 1
fi

# ── Step 2: Copy override files ───────────────────────────────────────────────
echo ""
info "Installing override files…"

if [ "$REPO_DIR" != "$OVERRIDES_DIR" ]; then
  mkdir -p "$OVERRIDES_DIR"
  cp -r "$REPO_DIR/skills"   "$OVERRIDES_DIR/"
  cp -r "$REPO_DIR/commands" "$OVERRIDES_DIR/" 2>/dev/null || true
  cp -r "$REPO_DIR/scripts"  "$OVERRIDES_DIR/" 2>/dev/null || true
  cp    "$REPO_DIR/apply.sh" "$OVERRIDES_DIR/"
  ok "Files copied to: ${DIM}$OVERRIDES_DIR${NC}"
else
  ok "Already in override directory: ${DIM}$OVERRIDES_DIR${NC}"
fi

# ── Step 3: Apply overrides now ───────────────────────────────────────────────
info "Applying skill overrides…"
bash "$OVERRIDES_DIR/apply.sh"
ok "Overrides applied"

# ── Step 4: Add SessionStart hook to settings.json ───────────────────────────
echo ""
info "Configuring SessionStart hook…"

mkdir -p "$(dirname "$SETTINGS")"

if [ ! -f "$SETTINGS" ]; then
  echo '{}' > "$SETTINGS"
fi

python3 << PYEOF
import json, sys, os

settings_path = '$SETTINGS'
hook_command  = 'bash \$HOME/.claude/plugins/superpowers-overrides/apply.sh'

try:
    with open(settings_path, 'r') as f:
        settings = json.load(f)
except:
    settings = {}

hooks = settings.setdefault('hooks', {})
session_hooks = hooks.setdefault('SessionStart', [])

# Check if hook already exists
already_exists = any(
    any(h.get('command') == hook_command for h in entry.get('hooks', []))
    for entry in session_hooks
    if isinstance(entry, dict)
)

if already_exists:
    print('  hook already present — skipping')
    sys.exit(0)

session_hooks.append({
    'hooks': [{'type': 'command', 'command': hook_command}]
})

with open(settings_path, 'w') as f:
    json.dump(settings, f, indent=4)

print('  hook added')
PYEOF

ok "SessionStart hook configured in ${DIM}$SETTINGS${NC}"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
hr
echo ""
echo -e "  ${GREEN}${BOLD}Installation complete!${NC}"
echo ""
echo -e "  What you have:"
echo -e "    ${CYAN}·${NC}  superpowers (24 base skills) — installed via Claude Code plugin"
echo -e "    ${CYAN}·${NC}  9 custom skill overrides (ascend, blueprint, chronicle, commander,"
echo -e "       ${DIM}forge, legion, pathfinder, phantom, vector)${NC}"
echo -e "    ${CYAN}·${NC}  ${BOLD}/tokenburn${NC} — token & cost analytics dashboard"
echo ""
echo -e "  The overrides re-apply automatically on every Claude Code session start,"
echo -e "  so they survive superpowers plugin updates."
echo ""
echo -e "  ${DIM}Try it: open Claude Code and type ${NC}${CYAN}/tokenburn${NC}"
echo ""
