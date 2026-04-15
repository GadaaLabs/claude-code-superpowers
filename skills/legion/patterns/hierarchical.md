---
name: LEGION — Hierarchical Topology
description: Queen-led coordinator + workers pattern for plan execution and structured tasks
---

# Hierarchical (Queen-led)

**Structure:** 1 coordinator (queen) + N workers. Coordinator assigns tasks, reviews output. Clear chain of command.

**Best for:** Executing written implementation plans, multi-feature development with clear requirements, tasks with defined sub-components.

**Use when:**
- Have implementation plan with distinct tasks
- Building features with clear component boundaries
- Need accountability (who did what)
- Tasks have different complexity levels

**Don't use when:** Exploratory work, research, highly collaborative design.

## Prompt Template

```
SWARM TOPOLOGY: Hierarchical

COORDINATOR AGENT:
You are the queen-coordinator for this implementation.
- Assign tasks to workers in order
- Review each worker's output against spec
- Request fixes if output doesn't match requirements
- Track overall progress
- Report status after each task completes

WORKER AGENTS:
Each worker receives one task with full context.
- Complete the task using TDD
- Self-review before reporting done
- Fix issues when coordinator requests
- Report: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED

TASKS:
<Task list from implementation plan>
```

## Example

```
Coordinator: Review all output against spec
Worker 1: JWT token service
Worker 2: Auth middleware
Worker 3: Login/logout endpoints
Worker 4: Frontend auth components
Worker 5: Integration tests
```
