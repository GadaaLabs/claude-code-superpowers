---
name: LEGION — Ring Topology
description: Sequential pipeline where each agent transforms the previous agent's output
---

# Ring (Pipeline)

**Structure:** Agents in sequence. Each transforms output of previous. A1 → A2 → A3 → A4.

**Best for:** Data processing pipelines, multi-stage refactors, content generation (outline → draft → review → polish), ETL workflows.

**Use when:**
- Clear sequential stages
- Each stage transforms previous output
- Pipeline stages are independent (can debug individually)

**Don't use when:** Parallel work possible (use Star), iterative refinement needed (use Hierarchical), no clear stage boundaries.

## Prompt Template

```
SWARM TOPOLOGY: Ring (Pipeline)

PIPELINE STAGES:
Stage 1: <name> — <transformation>
Stage 2: <name> — <transformation>
Stage 3: <name> — <transformation>

RULES:
- Each agent receives output of previous stage
- Each agent adds transformation, passes to next
- If stage fails, notify pipeline coordinator
- Final agent produces pipeline output

INPUT:
<Initial input for Stage 1>

EXPECTED OUTPUT:
<Final output after last stage>
```

## Example: Content Generation

```
Agent 1 (Researcher): Gather requirements, examples, constraints
  ↓ output: Research summary

Agent 2 (Outliner): Create structure from research
  ↓ output: Detailed outline

Agent 3 (Writer): Write first draft from outline
  ↓ output: Complete draft

Agent 4 (Reviewer): Technical review for accuracy
  ↓ output: Annotated draft with fixes

Agent 5 (Polisher): Final polish, formatting, consistency
  ↓ output: Final document
```
