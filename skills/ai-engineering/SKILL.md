---
name: ai-engineering
description: RAG architectures, agent design patterns, prompt engineering, and LLM evaluation — domain expertise for AI application engineers
type: domain
---

# AI Engineering Patterns

## Overview

**Core principle:** LLM applications have unique failure modes — hallucination, prompt injection, context overflow, cost explosion. Engineer systems, not just prompts.

**Announce at start:** "I'm using the ai-engineering skill for AI application patterns."

---

## Entry Point — First 5 Minutes

```
SYSTEM TYPE ASSESSMENT:

"What are you building/debugging?"
A) RAG / knowledge retrieval system
B) Autonomous agent / tool-using agent
C) Prompt engineering / LLM integration
D) LLM evaluation / benchmarking
E) Multi-agent system
F) Debugging a hallucination / quality problem
G) Cost/latency optimization
```

**Type → Section mapping:**
- A → RAG Architecture (see patterns/rag-architecture.md)
- B → Agent Design Patterns: ReAct or Plan-Execute (see patterns/agent-patterns.md)
- C → Prompt Engineering Workflow (see patterns/prompt-engineering.md)
- D → LLM Evaluation Framework (see patterns/llm-evaluation.md)
- E → Agent Patterns: Multi-Agent Debate or Tool Routing
- F → Hallucination Detection + run `systematic-debugging`
- G → Latency/Cost Tracking + `model-routing` skill

**After identifying type, ask:**
"What model are you using and what's the context window limit?"

---

## RAG Architecture

Load patterns: **`patterns/rag-architecture.md`**

Key decisions in order:
1. **Chunking strategy** — fixed / semantic / recursive / code-aware
2. **Embedding model** — MiniLM (fast) vs bge-large (quality) vs text-embedding-3-large (enterprise)
3. **Retrieval method** — lexical (BM25) / semantic / hybrid (RRF) / MMR
4. **Re-ranking** — cross-encoder reranker from top-20 → top-5
5. **Context budget** — allocate: system 500 + query 100 + context 6000 + output 1592

Rule: **Test retrieval quality (precision/recall) before testing generation quality.**

---

## Agent Design Patterns

Load patterns: **`patterns/agent-patterns.md`**

| Pattern | Best For | Iteration Limit |
|---------|----------|-----------------|
| ReAct | Factual QA, tool use | 10 |
| Plan-Execute | Multi-step tasks | 5 plans |
| Reflection | Quality-critical output | 3 cycles |
| Multi-Agent Debate | High-stakes decisions | 3 rounds |
| Tool Routing | Multiple specialized tools | N/A |

**Always set max iteration limits.** Agents without limits will loop indefinitely on failure.

---

## Prompt Engineering Workflow

Load patterns: **`patterns/prompt-engineering.md`**

Process:
1. Write initial prompt
2. Test on 10 diverse examples — categorize failure modes
3. Add constraints / few-shot examples to address failures
4. Re-test until >90% success rate
5. Add output format schema + retry logic (max 3 retries)
6. Add injection defenses (keyword filter + context isolation)

Rule: **Never deploy a prompt tested on fewer than 10 diverse examples.**

---

## LLM Evaluation Framework

Load patterns: **`patterns/llm-evaluation.md`**

| Metric type | Method | Use when |
|-------------|--------|----------|
| Exact match | string equality | Factual QA, code gen |
| F1 score | token overlap | Extractive QA |
| Semantic similarity | cosine >0.8 | Open-ended QA |
| Rubric-based | LLM grades | Complex tasks |
| Hallucination | fact verification + self-consistency | High-stakes output |
| Human preference | blind A/B, win rate >0.55 | Model comparison |

Cost budgets: p99 latency <5s, cost per 1k requests <$10.

---

## Red Flags

**Never:**
- Deploy RAG without testing retrieval quality
- Use agents without max iteration limits
- Skip prompt injection testing
- Deploy without hallucination monitoring
- Ignore cost monitoring (can explode quickly)

**Always:**
- Test prompts on diverse examples before deploying
- Include few-shot examples for complex tasks
- Validate output format with schema + retry
- Log all prompts and responses for debugging
- Set up cost alerts before production deployment

---

## Integration with Superpowers

| Skill | Integration |
|-------|-------------|
| `test-driven-development` | Write eval tests before model/prompt changes |
| `systematic-debugging` | Debug hallucination, retrieval failures |
| `verification-before-completion` | Verify eval metrics before claiming success |
| `learning-from-experience` | Store prompt patterns that worked |
| `model-routing` | Route queries to appropriate model tier |

---

## Final Checklist

- [ ] RAG retrieval quality tested (precision/recall)
- [ ] Agent has max iteration limits
- [ ] Prompt injection testing passed
- [ ] Hallucination detection configured
- [ ] Cost monitoring and alerts set up
- [ ] Latency budgets defined and met
- [ ] Output format validation in place
- [ ] Human evaluation plan defined
- [ ] Rollback plan if model degrades
