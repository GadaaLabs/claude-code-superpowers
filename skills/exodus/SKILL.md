---
name: exodus
description: Use when you have a written implementation plan to execute in a completely fresh isolated session — no context inheritance, clean slate execution with review checkpoints
type: process
---

# Executing Plans (Isolated Session)

## Overview

**EXODUS** — *An exodus is a deliberate departure into clean, uncharted territory — leaving all baggage behind.*
When invoked: loads a written plan into a completely fresh session with zero context inherited from the current conversation, executes each task exactly as specified, stops on any blocker, and hands off to SEAL when done.

**Core principle:** Fresh session per plan. No context pollution. Stop when blocked — never guess.

**Announce at start:** "Running EXODUS to execute this plan in an isolated session."

---

## EXODUS vs PHANTOM — Which to Use

| Question | EXODUS | PHANTOM |
|----------|--------|---------|
| Do you want zero session context? | **Yes — required** | No — same session |
| Do you need fastest iteration? | No | **Yes** |
| Do you have a complex plan needing full isolation? | **Yes** | No |
| Are tasks tightly sequential? | **Yes** | Works either way |

**Rule:** Large plans where context pollution is a real risk → EXODUS. Faster iteration in-session → PHANTOM.

> **Note:** EXODUS delivers the highest quality output when subagents are available (Claude Code, Codex). If your platform supports it, consider `phantom` as an alternative that keeps the human in the loop between tasks.

---

## The Process

### Step 1: Load and Review Plan

1. Read the plan file completely
2. Review critically — identify any gaps, contradictions, or unclear steps
3. **If concerns exist:** raise them before starting. Do not guess.
4. **If plan is clear:** create task list and proceed

### Step 2: Set Up Isolated Workspace

**REQUIRED:** Run `vault` before touching any files.

```
Running VAULT to set up an isolated workspace.
```

Never start implementation on `main` or `master` without **explicit user consent**.

### Step 3: Execute Tasks

For each task in order:
1. Mark as `in_progress`
2. Follow every step exactly as written — do not improvise
3. Run all verifications specified in the plan
4. Mark as `completed`

**Do not batch tasks.** Complete and verify one at a time.

### Step 4: Complete the Branch

After all tasks are complete and verified:

```
Running SEAL to complete this branch.
```

**REQUIRED:** invoke `seal` — do not merge or push manually.

---

## When to Stop Immediately

Stop and ask for help when:
- A dependency is missing or unavailable
- A test fails and you don't know why
- An instruction is unclear or contradictory
- A verification fails repeatedly (2+ times)
- The plan has a gap that prevents starting a step

**Never guess your way through a blocker.** Stop, explain what's blocked, and wait for direction.

---

## Red Flags

**Never:**
- Begin on `main`/`master` without explicit user consent
- Skip the VAULT workspace setup
- Improvise when a step is unclear — stop and ask
- Continue past a failing verification
- Batch-implement multiple tasks without verifying each

**Always:**
- Review the plan critically before starting
- Set up the isolated workspace with VAULT first
- Complete tasks one at a time with verification
- Hand off to SEAL — never merge manually

---

## Integration

**Required skills:**
- `vault` — workspace isolation before any task starts
- `blueprint` — creates the plan this skill executes
- `seal` — branch completion after all tasks finish

**Alternative:**
- `phantom` — same-session plan execution with subagent-per-task and two-stage review
