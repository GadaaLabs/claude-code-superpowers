---
name: vector
description: Select optimal AI model by task complexity — route to cheap/fast models for simple tasks, capable models for complex reasoning
type: process
---

# Model Routing

## Overview

**VECTOR** — *A vector has both direction and magnitude — it points precisely at the right target.*
When invoked: evaluates task complexity and routes to the least-capable model that can succeed — Tier 0 (no LLM) through Tier 3 (Opus). Systematic routing cuts API costs 50–65% vs treating everything as Opus.

**Core principle:** Use the least capable model that can handle the task — save cost and latency without sacrificing quality.

**Announce at start:** "Running VECTOR to assign the correct model tier."

## Single-Session vs Subagent Context

| Context | How VECTOR applies |
|---------|-------------------|
| **Main session** | Tier selection is advisory — informs reasoning depth, not model invoked |
| **Spawning subagents** (COMMANDER or PHANTOM) | Tier selection is literal — specify model when dispatching |
| **Multi-agent swarms** (LEGION) | Assign each agent a tier based on its sub-task complexity |

Full cost savings come from subagent dispatch: Haiku for mechanical tasks, Opus only for critical reasoning.

## Tier Summary

```
TIER 3: Opus 4.6     — Architecture, security-critical, cross-system, novel problems, review of Tier 2 work
TIER 2: Sonnet 4.6   — Multi-file features, bug investigation, API integration, complex test design
TIER 1: Haiku 4.5    — Single file edits, simple refactors, obvious test writing, docs, format fixes
TIER 0: No LLM       — Mechanical single-pattern transforms (sed/awk/prettier/eslint)
```

## Model Selection

Security-critical OR novel problem OR cross-system integration → **Tier 3**
Touches 3+ files OR requires investigation → **Tier 2**
Single file, mechanical, obvious → **Tier 1**
No judgment needed, pure pattern → **Tier 0**

## Tier Details

### Tier 0: Direct (Zero-LLM)

Latency: <1ms | Cost: $0 | Accuracy: 100% for exact patterns

Gate — ALL must be true: mechanical transform, unambiguous pattern, single file, reversible.

Examples: `var` → `const` (sed), sort imports (eslint --fix), format (prettier --write), rename single identifier (sed).

If Tier 0 fails → escalate to Tier 1.

### Tier 1: Haiku — Fast/Cheap

Single file edits, simple refactors, mechanical transformations, obvious test writing, documentation, format fixes.

### Tier 2: Sonnet — Standard

Multi-file features, bug fixes requiring investigation, API integration, complex test design, module-level refactoring, code review.

### Tier 3: Opus — Most Capable

Architecture decisions, security-critical code, cross-system integration, novel problem-solving, elusive bugs (survived 3+ fix attempts), review of Tier 2/3 work before merge.

## Dynamic Model Switching

**Escalate when:**
- Tier 1 gets stuck → Tier 2
- Tier 2 encounters novel problem → Tier 3
- Security implications discovered → Tier 3
- Task scope grows (1 file → 5 files) → Tier 2 or 3

**De-escalate when:**
- Tier 3 completes architecture → Tier 2 for implementation
- Tier 2 completes design → Tier 1 for mechanical edits

## Model Capabilities Reference

| Capability | Haiku | Sonnet | Opus |
|------------|-------|--------|------|
| Simple edits | ✓ | ✓ | ✓ |
| Test writing (basic) | ✓ | ✓ | ✓ |
| Multi-file features | ✗ | ✓ | ✓ |
| Bug investigation | ✗ | ✓ | ✓ |
| Architecture design | ✗ | △ | ✓ |
| Security analysis | ✗ | △ | ✓ |
| Novel problem-solving | ✗ | △ | ✓ |
| Code review | ✗ | △ | ✓ |

✓ = Strong | △ = Adequate | ✗ = Not recommended

## Routing Feedback Loop

After every routed task, append to `routing_log.md`:
```
| <date> | <task-1-line> | Tier N | Success/Escalated | <why> |
```

And add/update pointer in `MEMORY.md`:
```
- [Routing: <task-type>](routing_log.md) — Tier N → [Success|Escalated|Failed]
```

| Pattern | Adjustment |
|---------|-----------|
| Tier 1 escalated to Tier 2 ≥ 3x | Start that task type at Tier 2 |
| Tier 2 escalated to Tier 3 ≥ 2x | That pattern = Tier 3 default |
| Tier 3 completed trivially | Over-routed — note for next time |

## Red Flags

**Never:**
- Use Tier 3 for mechanical tasks (waste of money)
- Use Tier 1 for security-critical code (false economy)
- Use Tier 1 for novel problems (will get stuck)
- Stay in Tier 2 after 3 failed attempts (escalate)
- Skip Tier 3 review for architecture decisions

## Final Rule

```
Tier 0: mechanical single-pattern transforms — $0
Tier 1: single file, obvious behavior — cheap/fast
Tier 2: multi-file, investigation — standard
Tier 3: architecture, security, novel — capable

Default to lowest tier that can handle it
Escalate when stuck, de-escalate after hard parts resolved
```
