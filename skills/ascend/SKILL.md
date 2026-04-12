---
name: ascend
description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
---

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

```dot
digraph skill_flow {
    "User message received" [shape=doublecircle];
    "About to EnterPlanMode?" [shape=doublecircle];
    "Already brainstormed?" [shape=diamond];
    "Invoke brainstorming skill" [shape=box];
    "Might any skill apply?" [shape=diamond];
    "Invoke Skill tool" [shape=box];
    "Announce: 'Using [skill] to [purpose]'" [shape=box];
    "Has checklist?" [shape=diamond];
    "Create TodoWrite todo per item" [shape=box];
    "Follow skill exactly" [shape=box];
    "Respond (including clarifications)" [shape=doublecircle];

    "About to EnterPlanMode?" -> "Already brainstormed?";
    "Already brainstormed?" -> "Invoke brainstorming skill" [label="no"];
    "Already brainstormed?" -> "Might any skill apply?" [label="yes"];
    "Invoke brainstorming skill" -> "Might any skill apply?";

    "User message received" -> "Might any skill apply?";
    "Might any skill apply?" -> "Invoke Skill tool" [label="yes, even 1%"];
    "Might any skill apply?" -> "Respond (including clarifications)" [label="definitely not"];
    "Invoke Skill tool" -> "Announce: 'Using [skill] to [purpose]'";
    "Announce: 'Using [skill] to [purpose]'" -> "Has checklist?";
    "Has checklist?" -> "Create TodoWrite todo per item" [label="yes"];
    "Has checklist?" -> "Follow skill exactly" [label="no"];
    "Create TodoWrite todo per item" -> "Follow skill exactly";
}
```

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

1. **Process skills first** (brainstorming, debugging) - these determine HOW to approach the task
2. **Domain skills second** - apply engineering-specific knowledge for the domain
3. **Implementation skills third** (frontend-excellence, mcp-builder) - guide execution

"Let's build X" → brainstorming first, then domain skill, then implementation skills.
"Fix this bug" → debugging first, then domain-specific skills.

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
  codebase-onboarding →          ← ALWAYS first in any new codebase
  task-intake →
  → continue with appropriate chain

DEBUG CHAIN:
  learning-from-experience (search) →
  systematic-debugging →
  test-driven-development →
  verification-before-completion (+ confidence gate) →
  task-intake (after-action review) →
  learning-from-experience (store)

FEATURE CHAIN:
  task-intake →
  learning-from-experience (search) →
  [domain skill if applicable] →
  brainstorming →
  writing-plans →
  context-management (check health before dispatch) →
  model-routing + swarm-coordination →
  subagent-driven-development →
  verification-before-completion →
  requesting-code-review (with DOMAIN set) →
  task-intake (after-action review) →
  learning-from-experience (store)

ARCHITECTURE CHAIN:
  task-intake →
  learning-from-experience (search) →
  brainstorming →
  writing-plans (SPARC REQUIRED) →
  requesting-code-review (DOMAIN: security or relevant) →
  task-intake (after-action review) →
  learning-from-experience (store)

REFACTOR CHAIN:
  task-intake →
  test-driven-development (baseline tests first) →
  writing-plans →
  context-management (check before dispatch) →
  verification-before-completion →
  task-intake (after-action review) →
  learning-from-experience (store)

LONG SESSION (10+ exchanges):
  context-management (health check + compress) →
  → continue or handoff to fresh session

ML/AI/EE/FRONTEND WORK:
  task-intake →
  [ml-engineering | ai-engineering | embedded-systems | frontend-excellence] →
  → continue with feature-chain or debug-chain as appropriate
  (multi-domain: run synthesis step in task-intake first)
```

## Skill Types

**Rigid** (TDD, debugging, verification, task-intake): Follow exactly. Don't adapt away discipline.

**Flexible** (domain patterns, model routing): Adapt principles to context.

The skill itself tells you which.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
