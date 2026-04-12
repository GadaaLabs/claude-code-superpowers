# Claude Code Superpowers

**Turn Claude Code from a reactive assistant into a proactive engineering partner.**

A structured skill system for [Claude Code](https://claude.ai/code) that gives your AI persistent memory, domain expertise, disciplined process, and multi-agent coordination — so it compounds knowledge instead of starting from scratch every session.

Built and open-sourced by [GadaaLabs](https://gadaalabs.com) · [Full course →](https://gadaalabs.com/courses/claude-code-superpowers)

---

## Why This Exists

Default Claude Code is capable but structurally limited:

- **No process** — starts implementing immediately, no complexity classification
- **No domain awareness** — same reasoning for a one-line rename and a security overhaul
- **No memory** — every session is session one; corrections disappear overnight

This skill system addresses all three with four layers:

| Layer | What it does |
|-------|-------------|
| **Discipline** | Task intake, TDD, systematic debugging, verification — process before code |
| **Domain** | ML engineering, AI engineering, embedded systems, frontend — expertise on demand |
| **Intelligence** | Auto-memory, learning from experience, context management — knowledge that compounds |
| **Coordination** | Model routing, swarm coordination, multi-agent dispatch — scale to parallel execution |

---

## Quick Install

**Requires:** [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) + Node.js 18+

### Option A — One-line install (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/GadaaLabs/claude-code-superpowers/main/install.sh | bash
```

### Option B — Manual

```bash
# 1. Clone this repo
git clone https://github.com/GadaaLabs/claude-code-superpowers.git
cd claude-code-superpowers

# 2. Run the installer
bash install.sh
```

### Option C — Use as Claude plugin (if superpowers plugin is installed)

If you already have the official `superpowers` plugin, these skills extend it. Copy individual skill directories into your existing skills folder:

```bash
SKILLS_DIR=~/.claude/plugins/cache/claude-plugins-official/superpowers/5.0.7/skills
cp -r skills/ml-engineering "$SKILLS_DIR/"
cp -r skills/ai-engineering "$SKILLS_DIR/"
# ... etc
```

---

## What's Included

### Discipline Skills
| Skill | Purpose |
|-------|---------|
| `task-intake` | Classify complexity, select skill chain, assign model tier before ANY task |
| `test-driven-development` | Red-Green-Refactor with AI, confidence gate, cross-language |
| `systematic-debugging` | Evidence before hypothesis, bisect to root cause, canary tests |
| `verification-before-completion` | Confidence scoring gate before marking work done |
| `writing-plans` | SPARC-structured implementation plans for complex tasks |
| `brainstorming` | Design-before-code: 2-3 approaches, trade-offs, spec document |

### Domain Skills
| Skill | Domain | Patterns |
|-------|--------|---------|
| `ml-engineering` | ML pipelines, MLOps | data-pipeline, model-training, model-serving, mlops |
| `ai-engineering` | RAG, agents, prompts, eval | rag-architecture, agent-patterns, prompt-engineering, llm-evaluation |
| `embedded-systems` | ISRs, RTOS, state machines, hardware | state-machines, isr-safety, rtos-tasks, hardware-abstraction |
| `frontend-excellence` | UI, a11y, Core Web Vitals, bundle | 67 UI styles, 25 chart types, WCAG 2.1 AA, CWV targets |

### Intelligence Skills
| Skill | Purpose |
|-------|---------|
| `learning-from-experience` | Build a searchable ReasoningBank of solved patterns |
| `context-management` | Track token budget, compress context, handoff to fresh session |
| `codebase-onboarding` | Map unfamiliar codebases in 5 phases before starting work |

### Coordination Skills
| Skill | Purpose |
|-------|---------|
| `model-routing` | Tier 0 (no LLM) → Tier 3 (Opus); route by complexity to cut costs 50-65% |
| `swarm-coordination` | Parallel agent topologies: parallel, pipeline, hierarchical, mesh |
| `dispatching-parallel-agents` | Dispatch subagents with isolated worktrees and context budgets |
| `subagent-driven-development` | Subagent roles: implementer, reviewer, debugger, researcher |
| `requesting-code-review` | Domain-aware code review with ML/AI/Embedded/Frontend/Security checklists |

---

## How It Works

Skills are Markdown files (`SKILL.md`) that Claude Code loads on demand. They do not run automatically — they load into Claude's context when relevant.

```
skills/
  task-intake/
    SKILL.md              ← ~700 tokens, loaded when task starts
  ml-engineering/
    SKILL.md              ← lean index, ~700 tokens
    patterns/
      data-pipeline.md    ← loaded only when working on data pipelines
      model-training.md   ← loaded only when training models
      model-serving.md    ← loaded only when working on serving
      mlops.md            ← loaded only when working on MLOps
```

**Token cost:** Base skills are 600-900 tokens each. Pattern files are 400-800 tokens and load only when needed. The entire system is lazy-loaded — you only pay for what you use.

---

## The Skill Chain System

Every non-trivial task follows a chain. Task intake selects the chain automatically.

```
BUG:          learning-from-experience → systematic-debugging → TDD → verify → store pattern
FEATURE:      task-intake → [domain skill] → brainstorming → writing-plans → implement → verify → review
REFACTOR:     TDD (baseline tests) → writing-plans → implement → verify
ARCHITECTURE: brainstorming → writing-plans (SPARC) → review → store decision
```

---

## The Auto-Memory System

Skills work with Claude Code's auto-memory at `~/.claude/projects/<hash>/memory/`.

Four memory types persist across sessions:

```markdown
user      — who you are, your expertise, working preferences
feedback  — corrections Claude made, validated approaches (with Why + How to apply)
project   — current initiatives, architecture decisions, constraints
reference — where to find external information (Linear, Grafana, etc.)
```

Example `MEMORY.md` index:
```markdown
# Memory Index
- [User Profile](user_profile.md) — Python engineer, new to React; frame frontend in Python terms
- [Feedback: No Mocks on DB Tests](feedback_db_tests.md) — use real DB, mocks caused prod incident
- [Project: Auth Rewrite](project_auth.md) — compliance-driven, deadline fixed by legal schedule
- [Reference: Linear Bugs](reference_linear.md) — pipeline bugs in "INGEST" project
```

See `examples/memory/` for templates.

---

## Model Tier Routing

The `model-routing` skill assigns Claude model tiers by task complexity, cutting API costs 50-65%:

| Complexity | Tier | Model | Use for |
|-----------|------|-------|---------|
| 1-3 | 0 | None (direct) | Mechanical: rename, sort, format |
| 1-3 | 1 | Haiku | Simple lookups, single-file edits |
| 4-6 | 2 | Sonnet | Standard development (default) |
| 7-9 | 2→3 | Sonnet → Opus | Complex tasks, escalate if stuck |
| 10 | 3 | Opus | Security-critical, architecture decisions |

---

## Domain Pattern Files

Each domain skill has lazy-loaded pattern files for specific subtasks:

### ML Engineering patterns
- `data-pipeline.md` — schema validation, KS drift test, covariate shift, leakage check
- `model-training.md` — Bayesian hyperparameter search, early stopping, checkpointing, ablation
- `model-serving.md` — input validation, P99 latency test, fallback behavior, calibration
- `mlops.md` — versioning config, A/B test setup, PSI drift monitoring, rollback triggers

### AI Engineering patterns
- `rag-architecture.md` — chunking by doc type, embedding selection matrix, hybrid retrieval, reranking
- `agent-patterns.md` — ReAct, Plan-Execute, Reflection, Multi-Agent Debate, Tool Routing
- `prompt-engineering.md` — iterative refinement loop, few-shot selection, format enforcement, injection defense
- `llm-evaluation.md` — correctness metrics, hallucination detection, latency/cost tracking, human preference

### Embedded Systems patterns
- `state-machines.md` — HSM pattern, transition table, guard conditions, coverage testing
- `isr-safety.md` — minimal ISR work, lock-free SPSC queue, memory barriers
- `rtos-tasks.md` — Rate Monotonic Scheduling, stack watermark, IPC, WCRT analysis
- `hardware-abstraction.md` — type-safe registers, MMIO safety, endianness, timing checklist

---

## Usage

Once installed, skills activate through Claude Code's `Skill` tool or via `/skill-name` slash commands.

**Start every non-trivial task:**
```
/task-intake
```

**Invoke a domain skill:**
```
/ml-engineering
/ai-engineering
/embedded-systems
/frontend-excellence
```

**Load a pattern file** (Claude does this automatically when relevant, or you can ask):
```
Load the RAG architecture patterns for this retrieval implementation
```

**After completing a task:**
```
/learning-from-experience  (to store the pattern)
```

---

## Building Custom Skills

Create a `SKILL.md` in any subdirectory under `skills/`:

```markdown
---
name: your-skill-name
description: Specific description of when this skill applies — used for relevance matching
type: process | domain | implementation
---

# Your Skill Title

## Overview
Core principle and announcement line.

## Entry Point — First 5 Minutes
Assessment question before applying any patterns.

## Section 1
Patterns, checklists, configurations.

## Red Flags
**Never:** ...
**Always:** ...

## Final Checklist
- [ ] Verifiable completion criterion
```

Run `bash install.sh` again to pick up new skills. See `CONTRIBUTING.md` for contribution guidelines.

---

## Project Structure

```
claude-code-superpowers/
  README.md
  install.sh              ← automated setup script
  CONTRIBUTING.md         ← how to add skills and patterns
  skills/
    task-intake/          ← classify before you code
    test-driven-development/
    systematic-debugging/
    verification-before-completion/
    brainstorming/
    writing-plans/
    ml-engineering/       ← + patterns/
    ai-engineering/       ← + patterns/
    embedded-systems/     ← + patterns/
    frontend-excellence/
    learning-from-experience/
    context-management/
    codebase-onboarding/
    model-routing/
    swarm-coordination/
    dispatching-parallel-agents/
    subagent-driven-development/
    requesting-code-review/
    using-superpowers/
  examples/
    CLAUDE.md.example     ← template for project-specific Claude instructions
    memory/
      MEMORY.md.example   ← memory index template
      user_profile.md.example
      feedback_example.md
      project_example.md
```

---

## Full Course

The complete course on how to use this system — 12 lessons from installation to building custom skills — is free at:

**[gadaalabs.com/courses/claude-code-superpowers](https://gadaalabs.com/courses/claude-code-superpowers)**

Covers: task intake, TDD with AI, systematic debugging, ML/AI/embedded/frontend domain skills, auto-memory, learning from experience, multi-agent swarms, and building custom skills.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome for:
- New domain skills (DevOps, security, data engineering, mobile)
- New pattern files for existing skills
- Improved entry point assessments
- Community-contributed custom skills

---

## License

MIT — use freely, modify freely, share freely.

Built with care by [GadaaLabs](https://gadaalabs.com).
