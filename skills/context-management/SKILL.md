---
name: context-management
description: Manage context window budget across long sessions — when to compress, what to give subagents, when to start fresh. Prevents silent quality degradation as conversations grow.
type: process
---

# Context Management

## Overview

**Core principle:** A full context window is a silent quality killer. Proactively manage it — don't wait until things break.

Long sessions accumulate stale reasoning, superseded decisions, and irrelevant history. Subagents given bloated context lose focus. Claude running near the limit compresses its own earlier thinking without telling you.

**Announce at start:** "I'm using the context-management skill to manage session context."

---

## Context Health Monitor

Check context health at these triggers:

```
TRIGGER context health check when:
- Session has had 10+ back-and-forth exchanges
- About to dispatch a subagent
- About to start a new task after completing one
- User says "you seem confused" or repeats a correction
- You notice yourself re-reading earlier decisions
```

### Health Assessment (30 seconds)

Ask yourself:

| Question | Signal |
|----------|--------|
| Can I summarize the current task in 2 sentences? | Yes → healthy \| No → overloaded |
| Are there superseded decisions still in context? | Yes → stale |
| Would a subagent need > 500 words of context? | Yes → compress first |
| Have I re-explained the same thing twice? | Yes → context drift |
| Am I about to start a completely new task? | Yes → consider fresh session |

---

## The 4 Context States

### State 1: HEALTHY (< 40% full, task focused)
```
Action: Continue normally
Subagent dispatch: Include full relevant context
```

### State 2: LOADED (40–70% full, some stale content)
```
Action: Compress before dispatching subagents
Run: Context Compression Protocol (below)
Subagent dispatch: Compressed context only
```

### State 3: HEAVY (70–90% full, multiple topics mixed)
```
Action: Mandatory compression + summarize decisions
Consider: Fresh session for next major task
Subagent dispatch: Minimal essential context only
Warn: "Context is heavy — I'll give subagents a focused summary."
```

### State 4: CRITICAL (> 90% full or visibly degrading)
```
Action: Stop. Save state. Recommend fresh session.
Announce: "Context is near limit. I recommend starting a fresh
           session with a state handoff to maintain quality."
DO NOT: Continue with complex reasoning at this state
```

---

## Context Compression Protocol

Run this before dispatching any subagent or starting a new task:

### Step 1: Extract Active State

Identify and keep only:
```
ACTIVE STATE (always keep):
- Current task: [one sentence]
- Current files in play: [list of paths]
- Decisions made THIS session that affect the work: [list]
- Constraints discovered THIS session: [list]
- Where we are in the plan: [step N of M]
```

### Step 2: Archive Superseded Content

Mentally mark as "stale" (don't repeat in subagent context):
```
STALE (exclude from subagent context):
- Approaches we tried and rejected
- Earlier versions of the same decision
- Diagnostic output that led to a fix (keep the fix, drop the output)
- Exploration that dead-ended
- Re-explanations of things already understood
```

### Step 3: Build Subagent Context Block

```markdown
## Subagent Context (Compressed)

**Task:** [1 sentence]
**Goal:** [1 sentence — what done looks like]

**Key files:**
- `path/to/file.ts` — [what it does, 1 line]
- `path/to/other.py` — [what it does, 1 line]

**Decisions already made (don't re-decide):**
- [decision 1: what + why]
- [decision 2: what + why]

**Constraints (non-negotiable):**
- [constraint 1]
- [constraint 2]

**Completed steps:**
- [x] Step 1: [what was done]
- [x] Step 2: [what was done]

**Your task:**
- [ ] Step N: [exact instructions]
```

**Target: < 400 tokens for subagent context. Ruthlessly cut anything not needed for the specific task.**

---

## Fresh Session Handoff Protocol

When context is CRITICAL or switching to a completely new major task:

### Step 1: Write State File

Save to `docs/superpowers/session-state-<date>.md`:

```markdown
# Session State — <date> <time>

## What Was Accomplished
- [bullet list of completed tasks with file paths]

## Current State
- In progress: [task name]
- Next steps: [numbered list]
- Blockers: [any open questions]

## Key Decisions Made
| Decision | Rationale | Affects |
|----------|-----------|---------|
| [decision] | [why] | [files] |

## Architecture Discovered
- [any non-obvious patterns in the codebase]
- [any gotchas or traps to know]

## Files Modified This Session
[git diff --stat output]

## Resume Prompt
To resume: "Continue work on [task]. State file at docs/superpowers/session-state-<date>.md. 
Run `git log --oneline -10` to see recent changes."
```

### Step 2: Commit State

```bash
git add docs/superpowers/session-state-<date>.md
git commit -m "chore: save session state for handoff"
```

### Step 3: Announce Handoff

```
SESSION STATE SAVED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
State file: docs/superpowers/session-state-<date>.md
Commit:     <sha>

To resume in a fresh session, share the state file and say:
"Resume from session state."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Subagent Context Budget Rules

| Subagent Type | Max Context | What to Include |
|---------------|-------------|-----------------|
| Implementer (single task) | 300 tokens | Task only + relevant file paths |
| Code reviewer | 500 tokens | What was built + requirements + git range |
| Debugger | 400 tokens | Error + reproduction + relevant files |
| Researcher/Explorer | 200 tokens | Question only + scope constraint |
| Coordinator (swarm) | 600 tokens | Full plan + progress state |

**Rule:** If your context block exceeds budget → cut. If you can't cut below budget → split into two subagents.

---

## Context Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Sending full conversation to subagent | Subagent distracted by irrelevant history | Compress to active state only |
| Keeping rejected approaches in context | Muddies current direction | Mark stale, exclude from subagent context |
| Re-explaining decisions each dispatch | Wastes tokens, inconsistent | Make one canonical decision block, reuse |
| Ignoring context state until it breaks | Quality degrades silently | Check health at every task boundary |
| Never starting fresh sessions | Context accumulates errors | Save state, start fresh for major task switches |

---

## Integration with Superpowers

**Run before:**
- `dispatching-parallel-agents` — compress before each dispatch
- `subagent-driven-development` — check health before each task
- `swarm-coordination` — build clean context per topology type

**Triggered by:**
- `task-intake` — check context health as part of pre-task assessment
- `learning-from-experience` — store patterns before fresh session

---

## Final Rule

```
Context is a resource — budget it like tokens
Compress before dispatching
Save state before switching
Fresh session > degraded session
Quality over continuity
```
