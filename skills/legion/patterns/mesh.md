---
name: LEGION — Mesh Topology
description: Peer-to-peer equal agents for exploration, research, and collaborative design
---

# Mesh (Peer-to-peer)

**Structure:** All agents equal. Each explores different angle. Synthesize findings collectively. No central coordinator.

**Best for:** Codebase exploration, bug investigation (multiple hypotheses), research tasks, design exploration.

**Use when:**
- No clear structure yet (exploration needed)
- Multiple independent hypotheses to test
- Need diverse perspectives on same problem
- Collaborative design session

**Don't use when:** Implementation work (needs coordination), clear task breakdown exists, sequential dependencies.

## Prompt Template

```
SWARM TOPOLOGY: Mesh

ALL AGENTS:
You are one of N equal investigators.
- Explore your assigned angle completely
- Share findings with other agents
- Build on other agents' discoveries
- No coordination needed — work in parallel

SYNTHESIS:
After all agents report, combine findings into unified diagnosis.

INVESTIGATION ANGLES:
Agent 1: <angle 1>
Agent 2: <angle 2>
Agent 3: <angle 3>
Agent 4: <angle 4>
```

## Example: Bug Investigation

```
Agent: logs-analyst    → Examine error logs, find patterns
Agent: code-tracer     → Trace data flow through call stack
Agent: recent-changes  → Check git blame, recent commits
Agent: env-checker     → Verify environment/config differences

Synthesis: All agents share findings → collective diagnosis
```
