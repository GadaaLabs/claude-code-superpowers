# Claude Code on Steroids

**The complete, production-grade Claude Code skill system — packaged, optimized, and update-proof.**

Built on [obra/superpowers](https://github.com/obra/superpowers) by Jesse Vincent. Extended with 10 new skills, specific engineering improvements directed by GadaaLabs, and an override infrastructure that makes your skills survive plugin updates automatically.

```bash
curl -fsSL https://raw.githubusercontent.com/GadaaLabs/claude-code-on-steroids/main/install.sh | bash
```

**Requires:** [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) · Node.js 18+

---

## How This Compares to the Original

| | [obra/superpowers](https://github.com/obra/superpowers) | **Claude Code on Steroids** |
|--|--|--|
| Total skills | 14 | **24** |
| New skills not in obra | — | **+10** (oracle, chronicle, vector, horizon, legion, pathfinder, gradient, nexus, ironcore, prism) |
| Domain expertise (ML/AI/EE/UI) | ✗ | ✓ |
| Intelligence layer (classifier, memory, router) | ✗ | ✓ |
| Multi-agent swarm templates | Concepts only | **4 topology prompt templates** |
| API pre-verification in TDD | ✗ | ✓ (forge + blueprint) |
| Skill chain recipes | ✗ | **6 end-to-end chains** |
| Domain trigger system | ✗ | **13 scenario → skill mappings** |
| Override protection | ✗ | ✓ **100% update survivability** |
| One-command install | ✗ | ✓ |

---

## The Skills — All 24

### Evolved from obra originals (12 skills)

These skills exist in obra but have been significantly expanded. Key GadaaLabs additions are marked.

| Skill | obra original | What was improved |
|-------|--------------|-------------------|
| **forge** | test-driven-development | + Mandatory API pre-verification step before writing any test. Prevents phantom-API test failures. |
| **blueprint** | writing-plans | + Phase 0 Documentation Discovery — verifies every API in the spec exists before a plan is written |
| **ascend** | using-superpowers | + 6 workflow chains, 13-entry domain trigger table, oracle-first intake rule |
| **commander** | dispatching-parallel-agents | + COMMANDER vs PHANTOM decision table — eliminates the most common dispatch mistake |
| **hunter** | systematic-debugging | + Root-cause bisect protocol, defense-in-depth patterns |
| **sentinel** | verification-before-completion | + Confidence scoring gate (HIGH / MEDIUM / LOW) with evidence requirements |
| **architect** | brainstorming | + Spec document reviewer, visual companion |
| **arbiter** | receiving-code-review | + Technical verification protocol before implementing any suggestion |
| **tribunal** | requesting-code-review | + Domain-aware criteria: ML / AI / Embedded / Frontend / Security |
| **vault** | using-git-worktrees | + Worktree lifecycle management, safety verification |
| **seal** | finishing-a-development-branch | + Four structured completion options with verification |
| **sculptor** | writing-skills | + TDD applied to skill creation — Iron Law for process documentation |

### Brand new — not in obra (10 skills)

| Skill | What it does |
|-------|-------------|
| **oracle** | Classifies task complexity, selects skill chain, assigns model tier. Run before every non-trivial task. |
| **chronicle** | Self-learning memory. Stores solved patterns in a ReasoningBank. 3-layer token-efficient retrieval before each task. |
| **pathfinder** | 5-phase codebase exploration protocol. Maps entry points, architecture, and traps before writing code. |
| **vector** | Model cost routing. Tier 0 ($0, no LLM) for mechanical tasks. Tier 3 (Opus) only when complexity demands it. |
| **horizon** | Context window budget management. Tracks token usage, compresses when needed, hands off cleanly. |
| **legion** | Multi-agent swarm coordination. Hierarchical / mesh / ring / star topologies with ready-to-use prompt templates. |
| **gradient** | ML domain expertise: data pipelines, model training, serving infrastructure, MLOps, drift detection. |
| **nexus** | AI engineering: RAG architectures, agent patterns, prompt engineering, LLM evaluation frameworks. |
| **ironcore** | Embedded systems: ISRs, RTOS task design, state machines, hardware abstraction, timing analysis. |
| **prism** | UI/UX engineering: 67 design styles, 25 chart types, WCAG 2.1 AA accessibility, Core Web Vitals targets. |

### Restructured from obra (2 → 3 skills)

obra's `executing-plans` and `subagent-driven-development` were split and restructured into:

| Skill | What it does |
|-------|-------------|
| **phantom** | In-session parallel plan execution with 2-stage review (spec compliance → code quality) |
| **exodus** | Plan execution in a completely fresh isolated session — zero context pollution |

---

## The Override Infrastructure

Both obra and the official plugin distribution have the same gap: when the plugin updates, any pinned customizations are overwritten.

Our installer adds `apply.sh` + a `SessionStart` hook to `~/.claude/settings.json`:

```
Session opens
  → SessionStart hook fires
  → apply.sh reads installed plugin path from installed_plugins.json
  → Copies 9 pinned skill files over the plugin files
  → Session begins with your locked versions in place
```

**Plugin updates to any future version?** Next session, your pinned versions win automatically. Zero maintenance.

Skills pinned by the override system: `ascend` `blueprint` `chronicle` `commander` `forge` `legion` `pathfinder` `phantom` `vector`

---

## The 6 Workflow Chains (in ascend)

Instead of manually reasoning which skills to combine, ascend gives you pre-built chains:

```
DEBUG     →  chronicle → hunter → forge → sentinel → oracle → chronicle(store)

FEATURE   →  oracle → chronicle → [domain] → architect → blueprint
             → horizon → vector + legion → phantom → sentinel → tribunal
             → oracle → chronicle(store)

ARCH      →  oracle → chronicle → architect → blueprint → tribunal
             → oracle → chronicle(store)

REFACTOR  →  oracle → forge → blueprint → horizon → sentinel
             → oracle → chronicle(store)

ML/AI/EE/UI → oracle → [gradient|nexus|ironcore|prism]
              → feature-chain or debug-chain

LONG SESSION → horizon → continue or fresh handoff
```

---

## Quick Start After Install

```bash
# In any project
cd your-project && claude

# Start every non-trivial task with:
/oracle

# Working on ML?
/gradient

# Building a RAG system?
/nexus

# Debugging a hard problem?
/hunter

# New codebase you've never seen?
/pathfinder

# Writing a feature?
/forge   # TDD first, always
```

---

## Credits

- **[Jesse Vincent (@obra)](https://github.com/obra)** — original 14-skill Superpowers foundation
- **[claude-plugins-official team](https://github.com/obra/superpowers)** — expanded distribution and codename system
- **[GadaaLabs](https://gadaalabs.com)** — engineering improvements (API verification, domain trigger system, decision tables, skill chains), override infrastructure, packaging, and community distribution

---

## Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

Priority needs: DevOps/Kubernetes skill, security engineering skill, mobile engineering skill.

---

## License

MIT — use freely, modify freely, share freely.
