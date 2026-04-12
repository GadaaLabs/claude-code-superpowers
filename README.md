# Claude Code Superpowers

**Turn Claude Code from a reactive assistant into a proactive engineering partner.**

24 elite skills across 5 layers: discipline, domain expertise, intelligence, coordination, and execution.
Named for what they do — not what they are.

Built and open-sourced by [GadaaLabs](https://gadaalabs.com) · [Full course →](https://gadaalabs.com/courses/claude-code-superpowers)

---

## Quick Install

**Requires:** [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) + Node.js 18+

```bash
curl -fsSL https://raw.githubusercontent.com/GadaaLabs/claude-code-superpowers/main/install.sh | bash
```

Or clone and run:

```bash
git clone https://github.com/GadaaLabs/claude-code-superpowers.git
cd claude-code-superpowers && bash install.sh
```

---

## The Skills

### Discipline Layer — *Process before code*

| Skill | Invoke | What it does |
|-------|--------|-------------|
| **ORACLE** | `/oracle` | Classify complexity, select skill chain, assign model tier before ANY task |
| **FORGE** | `/forge` | Red-Green-Refactor with AI — write the test before the code, always |
| **HUNTER** | `/hunter` | Evidence before hypothesis, bisect to root cause, store pattern |
| **SENTINEL** | `/sentinel` | Confidence gate before completion — HIGH / MEDIUM / LOW score |
| **ARCHITECT** | `/architect` | Design-before-code: 2-3 approaches, trade-offs, spec document |
| **BLUEPRINT** | `/blueprint` | SPARC-structured implementation plans for complex tasks |

### Domain Layer — *Expertise on demand*

| Skill | Invoke | Domain | Lazy-loaded patterns |
|-------|--------|--------|---------------------|
| **GRADIENT** | `/gradient` | ML pipelines → MLOps | data-pipeline, model-training, model-serving, mlops |
| **NEXUS** | `/nexus` | RAG · agents · prompts · eval | rag-architecture, agent-patterns, prompt-engineering, llm-evaluation |
| **IRONCORE** | `/ironcore` | ISRs · RTOS · state machines · hardware | state-machines, isr-safety, rtos-tasks, hardware-abstraction |
| **PRISM** | `/prism` | UI · accessibility · Core Web Vitals · bundle | 67 UI styles, 25 chart types, WCAG 2.1 AA, CWV targets |

### Intelligence Layer — *Memory that compounds*

| Skill | Invoke | What it does |
|-------|--------|-------------|
| **CHRONICLE** | `/chronicle` | Build a searchable ReasoningBank of solved patterns |
| **HORIZON** | `/horizon` | Track token budget, compress context, handoff to fresh session |
| **PATHFINDER** | `/pathfinder` | Map unfamiliar codebases in 5 phases before starting work |

### Coordination Layer — *Scale to parallel execution*

| Skill | Invoke | What it does |
|-------|--------|-------------|
| **VECTOR** | `/vector` | Route by complexity: Tier 0 (no LLM) → Tier 3 (Opus). Cuts costs 50-65% |
| **LEGION** | `/legion` | Parallel agent topologies: parallel, pipeline, hierarchical, mesh |
| **COMMANDER** | `/commander` | Dispatch subagents with isolated worktrees and context budgets |
| **PHANTOM** | `/phantom` | Subagent roles: implementer, reviewer, debugger, researcher |
| **TRIBUNAL** | `/tribunal` | Domain-aware code review: ML / AI / Embedded / Frontend / Security |
| **ASCEND** | *(auto-loads)* | The meta-skill governing all others — loads at every session start |

### Execution Layer — *Safe, verified delivery*

| Skill | Invoke | What it does |
|-------|--------|-------------|
| **VAULT** | `/vault` | Isolated git worktrees — safe workspace before any implementation begins |
| **SEAL** | `/seal` | Structured branch completion: verify tests → merge / PR / keep / discard |
| **EXODUS** | `/exodus` | Execute plans in a completely fresh isolated session — zero context pollution |
| **ARBITER** | `/arbiter` | Receive code review with technical rigor — verify before implementing, push back when wrong |
| **SCULPTOR** | `/sculptor` | TDD applied to skill creation — no skill ships without a failing test first |

---

## How It Works

Skills are Markdown files (`SKILL.md`) that Claude Code loads on demand. Only relevant skills incur token cost.

```
skills/
  oracle/        SKILL.md  ← ~700 tokens, loads when task starts
  gradient/      SKILL.md  ← lean index, ~700 tokens
                 patterns/
                   data-pipeline.md    ← loads only when you're working on pipelines
                   model-training.md   ← loads only when training
                   model-serving.md    ← loads only when working on serving
                   mlops.md            ← loads only for MLOps work
```

---

## The Chain System

ORACLE classifies every task and selects the right chain automatically:

```
BUG       →  CHRONICLE → HUNTER → FORGE → SENTINEL → CHRONICLE (store)
FEATURE   →  ORACLE → [domain] → ARCHITECT → BLUEPRINT → VAULT → PHANTOM → SENTINEL → TRIBUNAL → SEAL
REFACTOR  →  FORGE (baseline) → BLUEPRINT → VAULT → EXODUS → SENTINEL → SEAL
ARCHITECT →  ARCHITECT → BLUEPRINT (SPARC) → TRIBUNAL → CHRONICLE
REVIEW    →  TRIBUNAL (request) → ARBITER (receive) → SENTINEL
NEW SKILL →  SCULPTOR (TDD for skills)
```

---

## Model Tier Routing (VECTOR)

```
Complexity 1-3  →  Tier 0  (no LLM)   mechanical: rename, sort, format
Complexity 1-3  →  Tier 1  (Haiku)    simple lookups, single-file edits
Complexity 4-6  →  Tier 2  (Sonnet)   standard development — the default
Complexity 7-9  →  Tier 2→3 (Sonnet → Opus)  escalate if stuck
Complexity 10   →  Tier 3  (Opus)     security-critical, architecture decisions
```
Systematic tier routing cuts API costs **50-65%** vs treating everything as Tier 3.

---

## The Auto-Memory System

Skills work with Claude Code's persistent memory at `~/.claude/projects/<hash>/memory/`.

Four memory types:

```
user      — who you are, expertise, working preferences
feedback  — corrections + validated approaches (Why + How to apply)
project   — active initiatives, architecture decisions, constraints
reference — where to find external information
```

Example index (`MEMORY.md`):
```markdown
- [User Profile](user_profile.md) — Python engineer, new to React; frame frontend in Python terms
- [CHRONICLE: Stripe Webhooks](pattern_backend_stripe.md) — return 200 immediately, process async
- [FORGE: No DB Mocks](feedback_db_tests.md) — use real DB; mocks caused prod incident
- [Project: Auth Rewrite](project_auth.md) — compliance-driven; deadline fixed by legal
```

---

## Domain Pattern Files

### GRADIENT (ML Engineering)
- `data-pipeline.md` — schema validation, KS drift test, covariate shift AUC, leakage check
- `model-training.md` — Bayesian hyperparam search, early stopping, checkpointing, ablation
- `model-serving.md` — input validation, P99 latency test, fallback behavior, calibration
- `mlops.md` — versioning config, A/B test, PSI drift monitoring, rollback triggers

### NEXUS (AI Engineering)
- `rag-architecture.md` — chunking by doc type, embedding matrix, hybrid retrieval, reranking
- `agent-patterns.md` — ReAct, Plan-Execute, Reflection, Multi-Agent Debate, Tool Routing
- `prompt-engineering.md` — iterative refinement, few-shot selection, format enforcement, injection defense
- `llm-evaluation.md` — correctness metrics, hallucination detection, latency/cost tracking, human preference

### IRONCORE (Embedded Systems)
- `state-machines.md` — HSM pattern, transition table, guard conditions, coverage testing
- `isr-safety.md` — minimal ISR work, lock-free SPSC queue, memory barriers
- `rtos-tasks.md` — Rate Monotonic Scheduling, stack watermark, IPC, WCRT analysis
- `hardware-abstraction.md` — type-safe registers, MMIO safety, endianness, timing checklist

---

## Usage

Once installed, invoke skills by name:

```
/oracle          ← start EVERY non-trivial task here
/gradient        ← working on ML pipelines or MLOps
/nexus           ← building RAG, agents, or prompts
/ironcore        ← embedded, firmware, or hardware
/prism           ← frontend, UI, or accessibility
/hunter          ← debugging a hard problem
/forge           ← new feature or function (TDD)
/chronicle       ← store a solved pattern
/legion          ← parallel work across 3+ independent files
```

---

## Building Custom Skills

Create a `SKILL.md` in any subdirectory under `skills/`:

```markdown
---
name: your-skill-name
description: Specific description of when this applies — used for relevance matching
type: process | domain | implementation
---

# YOUR SKILL NAME

## Overview
Core principle. Announce: "Using [name] for [purpose]."

## Entry Point — First 5 Minutes
Assessment before applying any patterns. Never dump everything at once.

## Section 1
...

## Red Flags
**Never:** ...
**Always:** ...

## Final Checklist
- [ ] Verifiable completion criterion
```

Run `bash install.sh` again to pick up new skills. See `CONTRIBUTING.md`.

---

## Project Structure

```
claude-code-superpowers/
  README.md
  install.sh              ← one-line installer, auto-detects superpowers plugin
  CONTRIBUTING.md         ← skill contribution guide with quality bar
  skills/
    oracle/               ← ORACLE: classify before you code
    forge/                ← FORGE: test-driven development
    hunter/               ← HUNTER: systematic debugging
    sentinel/             ← SENTINEL: verification gate
    architect/            ← ARCHITECT: design before building
    blueprint/            ← BLUEPRINT: structured plans
    gradient/             ← GRADIENT: ML engineering + patterns/
    nexus/                ← NEXUS: AI engineering + patterns/
    ironcore/             ← IRONCORE: embedded systems + patterns/
    prism/                ← PRISM: frontend excellence
    chronicle/            ← CHRONICLE: learning & pattern bank
    horizon/              ← HORIZON: context management
    pathfinder/           ← PATHFINDER: codebase onboarding
    vector/               ← VECTOR: model routing
    legion/               ← LEGION: swarm coordination
    commander/            ← COMMANDER: parallel agent dispatch
    phantom/              ← PHANTOM: subagent execution
    tribunal/             ← TRIBUNAL: domain-aware code review
    ascend/               ← ASCEND: the meta-skill (auto-loads)
    vault/                ← VAULT: isolated git worktrees
    seal/                 ← SEAL: structured branch completion
    exodus/               ← EXODUS: isolated session plan execution
    arbiter/              ← ARBITER: code review reception
    sculptor/             ← SCULPTOR: TDD for skill creation
                 patterns/
                   persuasion-principles.md
  examples/
    CLAUDE.md.example
    memory/
      MEMORY.md.example
      user_profile.md.example
      feedback_example.md
```

---

## Full Course

12-lesson free course — installation through custom skills:

**[gadaalabs.com/courses/claude-code-superpowers](https://gadaalabs.com/courses/claude-code-superpowers)**

---

## Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

New domain skills needed: DevOps/Kubernetes, security engineering, data engineering, mobile.

---

## License

MIT — use freely, modify freely, share freely.

Built with care by [GadaaLabs](https://gadaalabs.com).
