---
name: ascend
description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
---

**ASCEND** — *To ascend is to rise above the default — from reactive assistant to proactive engineering partner.*
When loaded: establishes the skill invocation protocol that governs all other skills. Every session starts here. If a skill might apply, it must be invoked — no exceptions, no rationalization.

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## Instruction Priority

Superpowers skills override default system prompt behavior, but **user instructions always take precedence**:

1. **User's explicit instructions** (CLAUDE.md, GEMINI.md, AGENTS.md, direct requests) — highest priority
2. **Superpowers skills** — override default system behavior where they conflict
3. **Default system prompt** — lowest priority

If CLAUDE.md, GEMINI.md, or AGENTS.md says "don't use TDD" and a skill says "always use TDD," follow the user's instructions. The user is in control.

## How to Access Skills

**In Claude Code:** Use the `Skill` tool. When you invoke a skill, its content is loaded and presented to you—follow it directly. Never use the Read tool on skill files.

**In Copilot CLI:** Use the `skill` tool. Skills are auto-discovered from installed plugins. The `skill` tool works the same as Claude Code's `Skill` tool.

**In Gemini CLI:** Skills activate via the `activate_skill` tool. Gemini loads skill metadata at session start and activates the full content on demand.

**In other environments:** Check your platform's documentation for how skills are loaded.

## Platform Adaptation

Skills use Claude Code tool names. Non-CC platforms: see `references/copilot-tools.md` (Copilot CLI), `references/codex-tools.md` (Codex) for tool equivalents. Gemini CLI users get the tool mapping loaded automatically via GEMINI.md.

# Using Skills

## The Rule

**Invoke relevant or requested skills BEFORE any response or action.** Even a 1% chance a skill might apply means that you should invoke the skill to check. If an invoked skill turns out to be wrong for the situation, you don't need to use it.

On every message:
1. Might any skill apply (even 1%)? → Invoke Skill tool first
2. Announce: "Using [skill] to [purpose]"
3. Skill has checklist? → Create TodoWrite per item
4. Follow skill exactly → then respond

About to EnterPlanMode without brainstorming? → Invoke `architect` first.

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (architect, hunter) - these determine HOW to approach the task
2. **Domain skills second** - apply engineering-specific knowledge for the domain
3. **Implementation skills third** (prism, mcp-builder) - guide execution

"Let's build X" → architect first, then domain skill, then implementation skills.
"Fix this bug" → hunter first, then domain-specific skills.

## Domain Skill Triggers

| Situation | Skill to Invoke |
|-----------|----------------|
| Any non-trivial task (start here) | `oracle` |
| First time in a codebase or new module | `pathfinder` |
| Building UI, selecting design style, choosing charts | `prism` |
| ML pipelines, model training, MLOps, drift detection | `gradient` |
| RAG systems, agents, prompt engineering, LLM eval | `nexus` |
| Firmware, ISRs, RTOS, state machines, timing | `ironcore` |
| 2+ independent tasks with no shared state | `commander` + `legion` |
| Task touches 3+ files with clear complexity tiers | `vector` |
| Complex task needing past pattern search | `chronicle` |
| Session 10+ exchanges or about to dispatch subagent | `horizon` |
| Code review with domain-specific criteria needed | `tribunal` (set DOMAIN) |
| Task spans 2+ engineering domains | `oracle` (multi-domain synthesis) |

## Task Intake — The First Step

**For ANY non-trivial task, invoke `oracle` FIRST.**

`oracle` classifies complexity, selects skill chain, searches patterns, and assigns model tier in 60 seconds. It replaces manual skill selection guesswork.

```
Non-trivial = touches code OR makes decisions OR has more than one step
Trivial     = pure Q&A, single-line answers, file reads
```

## Skill Chain Templates

Pre-built chains for common scenarios. Use these instead of reasoning from scratch:

```
NEW PROJECT / UNFAMILIAR CODEBASE:
  pathfinder →          ← ALWAYS first in any new codebase
  oracle →
  → continue with appropriate chain

DEBUG CHAIN:
  chronicle (search) →
  hunter →
  forge →
  sentinel (+ confidence gate) →
  oracle (after-action review) →
  chronicle (store)

FEATURE CHAIN:
  oracle →
  chronicle (search) →
  [domain skill if applicable] →
  architect →
  blueprint →
  horizon (check health before dispatch) →
  vector + legion →
  phantom →
  sentinel →
  tribunal (with DOMAIN set) →
  oracle (after-action review) →
  chronicle (store)

ARCHITECTURE CHAIN:
  oracle →
  chronicle (search) →
  architect →
  blueprint (SPARC REQUIRED) →
  tribunal (DOMAIN: security or relevant) →
  oracle (after-action review) →
  chronicle (store)

REFACTOR CHAIN:
  oracle →
  forge (baseline tests first) →
  blueprint →
  horizon (check before dispatch) →
  sentinel →
  oracle (after-action review) →
  chronicle (store)

LONG SESSION (10+ exchanges):
  horizon (health check + compress) →
  → continue or handoff to fresh session

ML/AI/EE/FRONTEND WORK:
  oracle →
  [gradient | nexus | ironcore | prism] →
  → continue with feature-chain or debug-chain as appropriate
  (multi-domain: run synthesis step in oracle first)
```

## Skill Types

**Rigid** (forge, hunter, sentinel, oracle): Follow exactly. Don't adapt away discipline.

**Flexible** (domain patterns, vector): Adapt principles to context.

The skill itself tells you which.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
