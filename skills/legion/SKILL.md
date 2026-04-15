---
name: legion
description: Select optimal subagent topology (hierarchical, mesh, ring, star) based on task structure; adds Ruflo-style swarm intelligence to Superpowers
type: process
---

# Swarm Coordination

## Overview

**LEGION** — *A legion is a large, coordinated force organized into precise, independent units.*
When invoked: selects the optimal agent topology for the task — parallel (independent tasks), pipeline (sequential stages), hierarchical (orchestrator + specialists), or mesh (peer review) — and coordinates execution across all agents.

**Core principle:** Match agent topology to task structure — the right coordination pattern prevents chaos and maximizes parallelism.

**Announce at start:** "Running LEGION to select agent topology and coordinate."

## Topology Selection

Independent tasks, no coordination needed → **STAR** (see `patterns/star.md`)
Sequential stages, each transforms previous output → **RING** (see `patterns/ring.md`)
Exploration, multiple hypotheses, no clear structure → **MESH** (see `patterns/mesh.md`)
Plan execution, coordinator + specialists → **HIERARCHICAL** (see `patterns/hierarchical.md`)

Load the matching pattern file for full prompt templates and examples.

## Quick Reference

| Topology | Parallelism | Best For |
|----------|-------------|----------|
| Hierarchical | Moderate | Plan execution, structured tasks |
| Mesh | High | Exploration, research, bug investigation |
| Ring | Low (sequential) | Data pipelines, multi-stage transforms |
| Star | Very High | Independent parallel work, batch processing |

## Swarm Size Guidelines

| Task Complexity | Swarm Size | Topology |
|-----------------|------------|----------|
| Single file edit | 1 agent | N/A (no swarm) |
| 2-5 files | 2-3 agents | Hierarchical |
| 5-10 files | 3-5 agents | Hierarchical or Star |
| Multi-module | 5-7 agents | Hierarchical-Mesh |
| System-wide | 7-15 agents | Adaptive with phases |

>10 agents: coordination overhead exceeds parallelism benefit. >15 agents: decompose into separate projects.

## Hybrid: Hierarchical-Mesh (Adaptive)

Complex projects with both exploration and execution:

```
PHASE 1: Exploration (Mesh) — explore angles, synthesize requirements
PHASE 2: Planning (Hierarchical) — coordinator writes plan, decomposes tasks
PHASE 3: Execution (Hierarchical) — workers execute, coordinator reviews
PHASE 4: Integration (Mesh) — collective debugging and integration
```

## Consensus for Disagreement Resolution

**Majority:** 3 agents agree A, 2 agree B → proceed with A, document dissent.
**Weighted:** Security decision → security-architect vote 3x weight.
**Byzantine:** f < n/3 faulty agents. With 4 agents: tolerate 1 faulty opinion. If no majority → escalate to human.

## Swarm Auto-Triggering

Auto-trigger when ALL of:
1. Task touches 3+ independent files
2. No sequential dependency between changes
3. Total estimated work > 20 minutes single-threaded

**Auto-trigger announcement:**
```
DETECTING: This task touches N independent files with no cross-dependencies.
AUTO-TRIGGERING: <topology> swarm (N spokes/workers)
Topology rationale: [reason]
```

Do NOT auto-trigger for: bug fixes (investigate first), tasks < 3 files, shared state changes.

## Integration with Existing Skills

| Skill | Integration |
|-------|-------------|
| `phantom` | Hierarchical topology by default |
| `architect` | Mesh topology for exploration phase |
| `hunter` | Mesh topology for multi-angle investigation |
| `blueprint` | Plan should specify recommended topology |
| `tribunal` | Star topology for parallel file review |

## Red Flags

**Never:**
- Use Ring when tasks are independent (waste of parallelism)
- Use Mesh for implementation (no coordination = chaos)
- Use Hierarchical for exploration (coordinator bottlenecks creativity)
- Use Star when subtasks have dependencies (integration fails)
- Deploy >10 agents without clear coordination plan

## Final Rule

```
Topology determines success — match structure to task
Hierarchical for execution | Mesh for exploration
Ring for pipelines | Star for parallel work
```
