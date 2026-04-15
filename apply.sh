#!/bin/bash
# Applies custom superpowers skill overrides to whatever version is currently installed.
# Runs on every SessionStart so it survives plugin updates.

OVERRIDES_DIR="$HOME/.claude/plugins/superpowers-overrides"

INSTALL_PATH=$(python3 -c "
import json, sys
try:
    data = json.load(open('$HOME/.claude/plugins/installed_plugins.json'))
    print(data['plugins']['superpowers@claude-plugins-official'][0]['installPath'])
except Exception as e:
    sys.exit(0)
" 2>/dev/null)

if [ -z "$INSTALL_PATH" ] || [ ! -d "$INSTALL_PATH" ]; then
  exit 0
fi

# ── Skill overrides ──────────────────────────────────────────────────────────
for skill in ascend chronicle blueprint forge pathfinder phantom vector legion commander; do
  src="$OVERRIDES_DIR/skills/$skill/SKILL.md"
  dst="$INSTALL_PATH/skills/$skill/SKILL.md"
  if [ -f "$src" ] && [ -f "$dst" ]; then
    cp "$src" "$dst"
  fi
done

# ── Legion topology patterns ─────────────────────────────────────────────────
if [ -d "$OVERRIDES_DIR/skills/legion/patterns" ] && [ -d "$INSTALL_PATH/skills/legion" ]; then
  mkdir -p "$INSTALL_PATH/skills/legion/patterns"
  cp "$OVERRIDES_DIR/skills/legion/patterns/"*.md "$INSTALL_PATH/skills/legion/patterns/" 2>/dev/null || true
fi

# ── Slash commands ───────────────────────────────────────────────────────────
if [ -d "$OVERRIDES_DIR/commands" ] && [ -d "$INSTALL_PATH/commands" ]; then
  cp "$OVERRIDES_DIR/commands/"*.md "$INSTALL_PATH/commands/" 2>/dev/null || true
fi
