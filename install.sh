#!/usr/bin/env bash
# Claude Code Superpowers — Installer
# https://github.com/GadaaLabs/claude-code-on-steroids
set -euo pipefail

# ─── Colors ──────────────────────────────────────────────────────────────────
RESET="\033[0m"
BOLD="\033[1m"
GREEN="\033[32m"
CYAN="\033[36m"
YELLOW="\033[33m"
RED="\033[31m"
DIM="\033[2m"

info()    { echo -e "${CYAN}${BOLD}→${RESET} $*"; }
success() { echo -e "${GREEN}${BOLD}✓${RESET} $*"; }
warn()    { echo -e "${YELLOW}${BOLD}!${RESET} $*"; }
error()   { echo -e "${RED}${BOLD}✗${RESET} $*" >&2; exit 1; }
dim()     { echo -e "${DIM}$*${RESET}"; }
header()  { echo -e "\n${BOLD}$*${RESET}"; }

# ─── Banner ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${CYAN}  ╔═══════════════════════════════════════╗${RESET}"
echo -e "${BOLD}${CYAN}  ║   Claude Code on Steroids — Installer   ║${RESET}"
echo -e "${BOLD}${CYAN}  ║        by GadaaLabs.com               ║${RESET}"
echo -e "${BOLD}${CYAN}  ╚═══════════════════════════════════════╝${RESET}"
echo ""

# ─── Detect install source ────────────────────────────────────────────────────
# Support: running from cloned repo OR piped from curl
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "")"
if [[ -n "$SCRIPT_DIR" && -d "$SCRIPT_DIR/skills" ]]; then
  SOURCE_DIR="$SCRIPT_DIR"
  dim "Installing from local repo: $SOURCE_DIR"
else
  # Download from GitHub
  info "Downloading skills from GitHub..."
  TMP_DIR="$(mktemp -d)"
  trap "rm -rf $TMP_DIR" EXIT
  curl -fsSL "https://github.com/GadaaLabs/claude-code-on-steroids/archive/refs/heads/main.tar.gz" \
    | tar -xz -C "$TMP_DIR" --strip-components=1
  SOURCE_DIR="$TMP_DIR"
  success "Downloaded"
fi

# ─── Check prerequisites ──────────────────────────────────────────────────────
header "Checking prerequisites..."

if ! command -v claude &>/dev/null; then
  error "Claude Code CLI not found. Install it first:\n  npm install -g @anthropic-ai/claude-code\n  then re-run this installer."
fi
CLAUDE_VERSION=$(claude --version 2>/dev/null || echo "unknown")
success "Claude Code found: $CLAUDE_VERSION"

# ─── Find Claude plugins directory ───────────────────────────────────────────
header "Locating Claude plugins directory..."

CLAUDE_HOME="${HOME}/.claude"
PLUGINS_BASE="${CLAUDE_HOME}/plugins/cache/claude-plugins-official"

# Try to find existing superpowers installation
EXISTING_SP=$(find "$PLUGINS_BASE" -maxdepth 2 -name "SKILL.md" -path "*/ascend/*" 2>/dev/null | head -1)

if [[ -n "$EXISTING_SP" ]]; then
  # Found existing superpowers — install into that version's skills directory
  SKILLS_DIR="$(dirname "$(dirname "$(dirname "$EXISTING_SP")")")"
  SP_VERSION="$(basename "$(dirname "$SKILLS_DIR")")"
  success "Found existing superpowers installation (v${SP_VERSION})"
  dim "  Target: $SKILLS_DIR"
else
  # No existing superpowers — create a standalone directory
  SKILLS_DIR="${CLAUDE_HOME}/superpowers/skills"
  warn "Superpowers plugin not found — installing as standalone"
  dim "  Run: claude plugin install superpowers  (to get the full plugin later)"
  dim "  Target: $SKILLS_DIR"

  # Add a hook so using-superpowers loads at session start
  HOOKS_FILE="${CLAUDE_HOME}/hooks.json"
  if [[ ! -f "$HOOKS_FILE" ]]; then
    echo '{"session_start": []}' > "$HOOKS_FILE"
  fi
fi

mkdir -p "$SKILLS_DIR"

# ─── Install skills ───────────────────────────────────────────────────────────
header "Installing skills..."

SKILLS=(
  arbiter
  architect
  ascend
  blueprint
  chronicle
  commander
  exodus
  forge
  gradient
  horizon
  hunter
  ironcore
  legion
  nexus
  oracle
  pathfinder
  phantom
  prism
  sculptor
  seal
  sentinel
  tribunal
  vault
  vector
)

INSTALLED=0
UPDATED=0

for skill in "${SKILLS[@]}"; do
  SRC="${SOURCE_DIR}/skills/${skill}"
  DEST="${SKILLS_DIR}/${skill}"

  if [[ ! -d "$SRC" ]]; then
    warn "Skill not found in source: $skill (skipping)"
    continue
  fi

  if [[ -d "$DEST" ]]; then
    rm -rf "$DEST"
    cp -r "$SRC" "$DEST"
    dim "  ↺ updated: $skill"
    ((UPDATED++))
  else
    cp -r "$SRC" "$DEST"
    dim "  + installed: $skill"
    ((INSTALLED++))
  fi
done

success "${INSTALLED} skills installed, ${UPDATED} updated"

# ─── Install examples ─────────────────────────────────────────────────────────
header "Installing examples..."

EXAMPLES_DEST="${CLAUDE_HOME}/superpowers-examples"
mkdir -p "$EXAMPLES_DEST"

if [[ -d "${SOURCE_DIR}/examples" ]]; then
  cp -r "${SOURCE_DIR}/examples/." "$EXAMPLES_DEST/"
  success "Examples copied to $EXAMPLES_DEST"
fi

# ─── Set up memory directory ──────────────────────────────────────────────────
header "Setting up memory system..."

# The memory dir is project-specific (<hash> of project path).
# We create a global template the user can copy per-project.
MEMORY_TEMPLATE="${CLAUDE_HOME}/memory-template"
mkdir -p "$MEMORY_TEMPLATE"

if [[ ! -f "${MEMORY_TEMPLATE}/MEMORY.md" ]]; then
  cat > "${MEMORY_TEMPLATE}/MEMORY.md" << 'EOF'
# Memory Index
# One line per memory file. Keep under 200 lines.
# Format: - [Title](file.md) — one-line hook

# Add your memories below:
# - [User Profile](user_profile.md) — your role, expertise, preferences
EOF
  success "Memory template created at $MEMORY_TEMPLATE/MEMORY.md"
  dim "  Copy to: ~/.claude/projects/<project-hash>/memory/"
else
  dim "  Memory template already exists"
fi

# ─── Install /tokenburn command file ─────────────────────────────────────────
header "Installing /tokenburn..."

COMMANDS_DIR="$(dirname "$SKILLS_DIR")/commands"
mkdir -p "$COMMANDS_DIR"

if [[ -f "${SOURCE_DIR}/commands/tokenburn.md" ]]; then
  cp "${SOURCE_DIR}/commands/tokenburn.md" "${COMMANDS_DIR}/tokenburn.md"
  success "/tokenburn slash command installed"
fi

# ─── Build & link tokenburn CLI ───────────────────────────────────────────────
header "Building tokenburn CLI..."

TOKENBURN_SRC="${SOURCE_DIR}/tools/tokenburn"

if [[ -d "$TOKENBURN_SRC" ]]; then
  if ! command -v node &>/dev/null; then
    warn "Node.js not found — tokenburn CLI requires Node.js 20+."
    dim "  Install Node.js and re-run: bash install.sh"
  else
    NODE_VER=$(node -e "process.stdout.write(process.version.slice(1).split('.')[0])" 2>/dev/null || echo "0")
    if [[ "$NODE_VER" -lt 20 ]]; then
      warn "Node.js v${NODE_VER} found, but tokenburn requires v20+."
      dim "  Upgrade Node.js and re-run: bash install.sh"
    else
      info "Building tokenburn (Node.js v${NODE_VER})…"
      (cd "$TOKENBURN_SRC" && npm install --silent 2>/dev/null && npm run build --silent 2>/dev/null)
      if [[ -f "${TOKENBURN_SRC}/dist/cli.js" ]]; then
        (cd "$TOKENBURN_SRC" && npm link --silent 2>/dev/null)
        if command -v tokenburn &>/dev/null; then
          success "tokenburn CLI installed → $(which tokenburn)"
        else
          # fallback: add a wrapper in ~/.local/bin
          mkdir -p "${HOME}/.local/bin"
          printf '#!/bin/bash\nnode "%s/dist/cli.js" "$@"\n' "$TOKENBURN_SRC" > "${HOME}/.local/bin/tokenburn"
          chmod +x "${HOME}/.local/bin/tokenburn"
          success "tokenburn installed → ~/.local/bin/tokenburn"
          dim "  Add ~/.local/bin to your PATH if not already present."
        fi
      else
        warn "Build failed — tokenburn CLI not installed. Check Node.js setup."
      fi
    fi
  fi
else
  warn "tools/tokenburn not found in source — skipping CLI build."
fi

# ─── Verify installation ──────────────────────────────────────────────────────
header "Verifying installation..."

SKILL_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l | tr -d ' ')
PATTERN_COUNT=$(find "$SKILLS_DIR" -path "*/patterns/*.md" | wc -l | tr -d ' ')

success "Installed: ${SKILL_COUNT} SKILL.md files + ${PATTERN_COUNT} pattern files"
dim "  Skills directory: $SKILLS_DIR"

# ─── Done ────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}═══════════════════════════════════════════${RESET}"
echo -e "${GREEN}${BOLD}  Installation complete!${RESET}"
echo -e "${GREEN}${BOLD}═══════════════════════════════════════════${RESET}"
echo ""
echo -e "  ${BOLD}Next steps:${RESET}"
echo -e "  1. Open your project:  ${CYAN}cd your-project && claude${RESET}"
echo -e "  2. Run task intake:    ${CYAN}/task-intake${RESET}"
echo -e "  3. Try a domain skill: ${CYAN}/ml-engineering${RESET}  or  ${CYAN}/ai-engineering${RESET}"
echo -e "  4. Check token usage:  ${CYAN}/tokenburn${RESET}"
echo ""
echo -e "  ${DIM}Full course (free): gadaalabs.com/courses/claude-code-on-steroids${RESET}"
echo -e "  ${DIM}Docs & issues:      github.com/GadaaLabs/claude-code-on-steroids${RESET}"
echo ""
