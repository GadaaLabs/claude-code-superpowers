# Claude Code Superpowers — Contributor Guidelines

## Overview

This repo ships 24 skills across 5 layers: discipline, domain expertise, intelligence, coordination, and execution. Skills are Markdown files that shape Claude's behavior — they are code, not prose.

## If You Are an AI Agent

Read this before doing anything else.

Skills are behavior-shaping instructions. Modifying them incorrectly can cause Claude to follow the wrong workflow silently — no error, just wrong behavior. The bar for changes is high.

Before proposing any change you MUST:

1. **Identify the real problem** — what specific session, error, or user experience motivated the change?
2. **Check for existing patterns** — grep the skill for prior handling of this case
3. **Test the change** — run the tests in `tests/` before claiming it works
4. **Show the diff** — get explicit human approval on the complete diff before committing

If you cannot identify a real problem, do not make the change.

## Skill Change Requirements

Skills are not documentation — they enforce agent behavior. When modifying any SKILL.md:

- Understand the Iron Law or core principle of the skill first
- Do not weaken enforcement language ("NEVER", "MANDATORY", "Iron Law")
- Do not add optional language ("consider", "might", "could") to required steps
- Run at minimum `tests/claude-code/test-helpers.sh` assertions against the changed skill
- Document what behavior changed and why in the commit message

## What Belongs in This Repo

**In scope:**
- General-purpose skills useful across all engineering projects
- Domain skills with broad applicability (ML, AI, Embedded, Frontend)
- Infrastructure improvements (hooks, tests, install script)
- Bug fixes with clear reproduction steps

**Out of scope:**
- Project-specific skills or workflows
- Skills for specific tools or services
- Rebranding or cosmetic changes
- Changes that weaken enforcement without eval evidence

## Architecture

```
skills/          ← 5-layer skill system (24 skills)
  Discipline:    oracle, forge, hunter, sentinel, architect, blueprint
  Domain:        gradient, nexus, ironcore, prism
  Intelligence:  chronicle, horizon, pathfinder
  Coordination:  vector, legion, commander, phantom, tribunal, ascend
  Execution:     vault, seal, exodus, arbiter, sculptor

hooks/           ← SessionStart auto-loader (fires on startup/clear/compact)
agents/          ← code-reviewer agent definition
tests/           ← automated verification suite
install.sh       ← one-line installer
examples/        ← memory system templates
```

## Tests

Run before any PR:

```bash
# Fast skill behavior tests
bash tests/claude-code/run-skill-tests.sh

# Skill triggering tests (verify skills fire from real prompts)
bash tests/skill-triggering/run-all.sh

# Integration tests (slow, ~10-30 min)
bash tests/claude-code/run-skill-tests.sh --integration
```

## Skill Name Mapping

This repo uses epic codenames. The mapping from workflow names:

| Codename | Workflow name |
|---|---|
| ORACLE | pre-task-intelligence |
| FORGE | test-driven-development |
| HUNTER | systematic-debugging |
| SENTINEL | verification-before-completion |
| ARCHITECT | design-before-code |
| BLUEPRINT | writing-plans |
| PHANTOM | executing-plans / subagent-driven-development |
| CHRONICLE | learning-from-experience |
| PATHFINDER | codebase-onboarding |
| VECTOR | model-routing |
| LEGION | swarm-coordination |
| COMMANDER | dispatching-parallel-agents |
| TRIBUNAL | requesting-code-review |
| ASCEND | using-superpowers |
| VAULT | using-git-worktrees |
| SEAL | finishing-a-development-branch |
| ARBITER | receiving-code-review |
| SCULPTOR | writing-skills |
