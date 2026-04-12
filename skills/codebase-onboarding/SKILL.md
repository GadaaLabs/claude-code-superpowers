---
name: codebase-onboarding
description: Structured first-pass exploration of an unfamiliar codebase — what to read, in what order, what to map, what traps to find. Use when entering any new or inherited project before writing code.
type: process
---

# Codebase Onboarding

## Overview

**Core principle:** Never write code in a codebase you haven't mapped. 20 minutes of structured exploration prevents days of working against the grain.

Unfamiliar codebases have hidden conventions, undocumented constraints, landmine files, and established patterns. Violating them creates bugs that look mysterious but are obvious to anyone who knows the codebase.

**Announce at start:** "I'm using the codebase-onboarding skill to map this codebase before writing code."

**When to use:**
- First time working in a project
- Returning after > 2 weeks away
- Inheriting someone else's work
- Working in a new module/subsystem of a large project

---

## Phase 1: Orientation (5 minutes)

Read these in order. Do not skip:

### 1.1 Entry Points

```bash
# What exists at the root?
ls -la

# Package info / dependencies
cat package.json 2>/dev/null || cat pyproject.toml 2>/dev/null || \
cat Cargo.toml 2>/dev/null || cat go.mod 2>/dev/null

# Primary README
cat README.md 2>/dev/null | head -100
```

**Extract:**
- What does this project do? (1 sentence)
- What language/runtime?
- What are the install/run commands?
- What testing framework?

### 1.2 Project Instructions

```bash
# Claude-specific instructions
cat CLAUDE.md 2>/dev/null
cat .claude/CLAUDE.md 2>/dev/null

# General agent instructions
cat AGENTS.md 2>/dev/null
cat GEMINI.md 2>/dev/null
```

**These override everything else. Read completely before proceeding.**

### 1.3 Recent History

```bash
# What was recently worked on?
git log --oneline -20

# What's the current state?
git status
git diff --stat HEAD~5..HEAD
```

**Extract:**
- What was the most recent focus area?
- Any in-progress work?
- Any merge conflicts or dirty state?

---

## Phase 2: Structure Map (5 minutes)

### 2.1 Directory Layout

```bash
# Top-level structure (depth 2)
find . -maxdepth 2 -type d | grep -v node_modules | grep -v .git | \
  grep -v __pycache__ | grep -v .venv | sort
```

**Map to mental model:**
```
TYPICAL LAYOUTS:

Next.js/React:      app/ components/ lib/ public/ styles/
Python backend:     src/ tests/ scripts/ docs/ config/
ML project:         data/ notebooks/ src/ models/ experiments/
Embedded/C:         src/ include/ drivers/ tests/ hal/
Go service:         cmd/ internal/ pkg/ api/ handler/
```

### 2.2 Find the Entry Points

```bash
# What's the main executable / server entry?
grep -r "main\|server\|app\|index" --include="*.ts" --include="*.py" \
  --include="*.go" --include="*.c" -l | head -10
```

Trace: entry point → router/dispatcher → handlers → services → data layer.

### 2.3 Find the Tests

```bash
# Where are tests?
find . -name "*.test.*" -o -name "test_*.py" -o -name "*_test.go" | \
  grep -v node_modules | head -20

# Run them to establish baseline
npm test 2>/dev/null || pytest --tb=no -q 2>/dev/null || \
  go test ./... 2>/dev/null || cargo test 2>/dev/null
```

**Baseline:** All tests passing? If not — document which are broken BEFORE you touch anything.

---

## Phase 3: Convention Detection (5 minutes)

Read 2-3 existing files to extract conventions. Never guess — read the code.

### 3.1 Naming Conventions

```bash
# Pick 2 representative source files
# Read them completely
```

**Detect:**
- camelCase, snake_case, PascalCase, kebab-case?
- File naming: `component.tsx`, `ComponentName.tsx`, `component-name.tsx`?
- Function naming: `getUser`, `fetch_user`, `FetchUser`?
- Constants: `MAX_RETRIES`, `maxRetries`, `MAX-RETRIES`?

### 3.2 Import/Module Style

```bash
grep -r "^import\|^from\|^require\|^use " --include="*.ts" \
  --include="*.py" --include="*.rs" -l | head -5 | xargs head -20
```

**Detect:**
- Absolute vs relative imports?
- Barrel files (`index.ts` re-exports)?
- Path aliases (`@/components` vs `../components`)?

### 3.3 Error Handling Pattern

```bash
grep -r "try\|catch\|except\|Result\|Either\|unwrap" \
  --include="*.ts" --include="*.py" --include="*.rs" -l | head -3 | xargs head -40
```

**Detect:** Exceptions? Result types? Error callbacks? Error objects vs strings?

### 3.4 State Management (if frontend/full-stack)

```bash
grep -r "useState\|useStore\|zustand\|redux\|jotai\|Context" \
  --include="*.tsx" --include="*.ts" -l | head -5
```

### 3.5 Data Access Pattern

```bash
grep -r "prisma\|knex\|mongoose\|sqlalchemy\|diesel\|gorm" \
  --include="*.ts" --include="*.py" --include="*.rs" --include="*.go" -l | head -5
```

---

## Phase 4: Trap Detection (5 minutes)

These are the landmines. Find them before stepping on them.

### 4.1 Large / Complex Files

```bash
# Files over 300 lines are often load-bearing complexity
find . -name "*.ts" -o -name "*.py" -o -name "*.go" | \
  grep -v node_modules | grep -v .git | \
  xargs wc -l 2>/dev/null | sort -rn | head -20
```

**Rule:** If a file > 500 lines, read its top 50 lines to understand what it owns. Don't add to it without understanding it.

### 4.2 Shared Mutable State

```bash
# Global state, singletons, module-level variables
grep -rn "global\|singleton\|module_level\|^let \|^var " \
  --include="*.ts" --include="*.py" | grep -v test | head -20
```

### 4.3 Environment Dependencies

```bash
# What env vars does this need?
cat .env.example 2>/dev/null || cat .env.local 2>/dev/null || \
grep -r "process.env\|os.environ\|os.getenv" --include="*.ts" \
  --include="*.py" -h | sort -u | head -20
```

**Document:** Every env var required. Which ones have no defaults and will fail silently?

### 4.4 Known Broken / In-Progress

```bash
# TODOs, FIXMEs, HACKs
grep -rn "TODO\|FIXME\|HACK\|XXX\|BUG\|BROKEN" \
  --include="*.ts" --include="*.py" --include="*.go" --include="*.c" \
  | grep -v node_modules | grep -v .git | head -30
```

**Don't accidentally fix these without understanding why they're deferred.**

### 4.5 Critical Files — Do Not Touch Without Full Understanding

Identify files that, if broken, take down the whole system:
- Auth/session middleware
- Database connection pool
- Main router / API gateway
- Schema migration files
- CI/CD pipeline configs

```bash
# Find likely critical files
git log --oneline --all -- "**/*auth*" "**/*middleware*" \
  "**/*migration*" "**/*schema*" 2>/dev/null | head -10
```

---

## Phase 5: Onboarding Summary

After completing all 4 phases, produce this summary before writing any code:

```
CODEBASE ONBOARDING COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project:     [name — 1 sentence description]
Stack:       [language + runtime + key frameworks]
Entry:       [main file/command]
Tests:       [framework + baseline status (X passing, Y failing)]

Conventions:
  Naming:    [camelCase / snake_case / PascalCase]
  Imports:   [absolute / relative / barrel]
  Errors:    [exceptions / Result types / callbacks]
  State:     [local / Zustand / Redux / context]

Traps found:
  ⚠ [trap 1 — e.g., "auth.ts:340+ lines, owns session logic, fragile"]
  ⚠ [trap 2 — e.g., "3 pre-existing failing tests in payments/"]
  ⚠ [trap 3 — e.g., "STRIPE_KEY env var required, no default"]

Critical files (read before touching):
  - [path] — [why critical]

Safe to start work. ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Store the summary in auto-memory:
```
~/.claude/projects/<hash>/memory/onboarding_<project>.md
```
Register in `MEMORY.md` so it loads next session.

---

## Domain-Specific Additions

### ML / Data Science Codebases

Additional checks:
```bash
# Find notebooks (often undocumented experiments)
find . -name "*.ipynb" | head -10

# Data directories (don't commit these)
find . -name "*.csv" -o -name "*.parquet" -o -name "*.pkl" | \
  grep -v node_modules | head -10

# Model artifacts (large files)
find . -name "*.pt" -o -name "*.pkl" -o -name "*.h5" | head -10
```

Traps: Notebooks often have hardcoded paths. Models often assume GPU. Data pipelines often have environment-specific config.

### Embedded / Firmware Codebases

Additional checks:
```bash
# Build system
cat Makefile 2>/dev/null | head -50
cat CMakeLists.txt 2>/dev/null | head -50

# Target platform
grep -r "CPU\|MCU\|CORTEX\|ARM\|AVR\|STM32\|ESP32" \
  --include="*.h" --include="*.cmake" | head -10

# Flash/RAM constraints
grep -r "FLASH\|RAM\|HEAP\|STACK" --include="*.ld" \
  --include="*.cmake" | head -10
```

Traps: Linker scripts are critical. Stack sizes are often hardcoded. Clock initialization order matters.

### AI / Agent Codebases

Additional checks:
```bash
# Prompt files (often scattered)
find . -name "*.txt" -o -name "*.prompt" -o -name "prompts.py" | \
  grep -v node_modules | head -10

# API key management
grep -r "OPENAI\|ANTHROPIC\|GROQ\|GEMINI" --include="*.py" \
  --include="*.ts" -l | head -5
```

Traps: System prompts often have hidden constraints. Rate limits often not surfaced in code.

---

## Integration with Superpowers

**Run before:**
- Any first code change in a new project
- `brainstorming` — context for design decisions
- `writing-plans` — architecture decisions need codebase knowledge
- `task-intake` — includes codebase health in complexity assessment

**After completion:**
- Store onboarding summary in auto-memory
- Use `learning-from-experience` to record any unusual patterns found

---

## Final Rule

```
Map before you build
Read before you write
Conventions before creativity
Traps before touching
```
