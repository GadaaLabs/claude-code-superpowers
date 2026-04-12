---
name: vault
description: Use when starting feature work that needs isolation from the current workspace, or before executing implementation plans — creates isolated git worktrees with smart directory selection and safety verification
type: process
---

# Using Git Worktrees

## Overview

**VAULT** — *A vault is a sealed, isolated chamber — what happens inside cannot contaminate what's outside.*
When invoked: creates an isolated git worktree so implementation work is completely separated from the main branch — parallel agents cannot corrupt each other's state, and breaking changes stay contained until verified.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

**Announce at start:** "Running VAULT to set up an isolated workspace."

---

## Directory Selection Process

Follow this priority order:

### 1. Check Existing Directories

```bash
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

If found: use that directory. If both exist, `.worktrees/` wins.

### 2. Check CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

If a preference is specified: use it without asking.

### 3. Ask the User

If no directory exists and no CLAUDE.md preference:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global)

Which would you prefer?
```

---

## Safety Verification

### For Project-Local Directories (.worktrees/ or worktrees/)

**MUST verify the directory is gitignored before creating the worktree:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If NOT ignored — fix immediately:**
1. Add the line to `.gitignore`
2. Commit the change
3. Then proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents to the repository.

### For Global Directory (~/.config/superpowers/worktrees/)

No `.gitignore` verification needed — it's outside the project entirely.

---

## Creation Steps

### 1. Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create the Worktree

```bash
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. Run Project Setup (auto-detect)

```bash
if [ -f package.json ];      then npm install; fi
if [ -f Cargo.toml ];        then cargo build; fi
if [ -f requirements.txt ];  then pip install -r requirements.txt; fi
if [ -f pyproject.toml ];    then poetry install; fi
if [ -f go.mod ];            then go mod download; fi
```

### 4. Verify Clean Baseline

```bash
# Use the project's test command
npm test / cargo test / pytest / go test ./...
```

- Tests fail → report failures, ask whether to proceed or investigate
- Tests pass → report ready

### 5. Report Location

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → ask user |
| Directory not gitignored | Add to `.gitignore` + commit first |
| Tests fail at baseline | Report failures + ask before proceeding |
| No package.json / Cargo.toml | Skip dependency install |

---

## Red Flags

**Never:**
- Create a project-local worktree without verifying it is gitignored
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip the CLAUDE.md check

**Always:**
- Priority order: existing directory > CLAUDE.md preference > ask user
- Verify gitignore for project-local directories
- Auto-detect and run project setup
- Confirm clean test baseline before handing off

---

## Integration

**Called by:**
- `architect` — required when design is approved and implementation follows
- `phantom` — required before executing any plan tasks
- `exodus` — required before executing any plan tasks

**Pairs with:**
- `seal` — cleans up the worktree after work is complete
