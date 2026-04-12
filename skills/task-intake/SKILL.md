---
name: task-intake
description: Pre-task intelligence layer — classify complexity, select skill chain, search patterns, assign model tier. Run BEFORE any non-trivial task begins. Turns the system from reactive to proactive.
type: process
---

# Task Intake

## Overview

**Core principle:** Never start a task cold. 60 seconds of classification prevents hours of wrong-direction work.

This skill is the **meta-intelligence layer** of Superpowers. It classifies every task before execution, selects the optimal skill chain, searches for relevant past patterns, and assigns the correct model tier — automatically.

**Announce at start:** "Running task-intake to classify and plan approach."

**WHEN TO RUN:**
- Before ANY task that touches code or architecture
- Before ANY bug investigation
- Before ANY new feature or design decision
- At the start of EVERY non-trivial conversation

**SKIP only for:** Trivial one-liner answers, pure information questions, file reads.

---

## Fast Path (Complexity ≤ 3)

Before running all 5 phases, do a **5-second triage**:

```
Is ALL of the following true?
  ✓ Single file or fewer than 3 files
  ✓ No investigation required — cause is known
  ✓ No security, architecture, or cross-system implications
  ✓ Similar task done before (no novelty)
  ✓ No domain skill triggers

→ FAST PATH: Skip Phases 2–5.
  Announce: "Complexity ≤ 3 — fast path. Tier 1, no plan needed."
  Proceed directly to implementation.
```

If ANY condition is false, run the full 5-phase intake.

---

## Phase 1: Task Classification (30 seconds)

### Step 1: Score Complexity (1–10)

Answer each question honestly:

| Question | +Points |
|----------|---------|
| Touches more than 3 files? | +1 |
| Requires investigation before implementation? | +1 |
| Touches 2+ engineering domains? | +1 |
| Has security implications? | +2 |
| Involves architecture decisions? | +2 |
| Novel problem (no precedent in codebase)? | +2 |
| Cross-system integration? | +1 |
| Strict performance or timing requirements? | +1 |

**Score → Tier:**
```
1-3:  SIMPLE     → Tier 0/1 model, single skill, no plan needed
4-6:  STANDARD   → Tier 1/2 model, 2-4 skills, plan recommended
7-9:  COMPLEX    → Tier 2/3 model, full skill chain, plan required
10:   CRITICAL   → Tier 3 model, SPARC structure, human review gate
```

### Step 2: Identify Domain(s)

Check all that apply:

- [ ] **Frontend / UI** → invoke `frontend-excellence`
- [ ] **ML / Data Science** → invoke `ml-engineering`
- [ ] **AI / LLM / RAG / Agents** → invoke `ai-engineering`
- [ ] **Embedded / Firmware / EE** → invoke `embedded-systems`
- [ ] **General backend / web** → standard skills
- [ ] **Multi-domain** → invoke all relevant domain skills

### Step 3: Identify Task Type

```
Is this a BUG?
└─ Yes → [debug-chain]

Is this a NEW FEATURE?
└─ Yes → [feature-chain]

Is this a REFACTOR?
└─ Yes → [refactor-chain]

Is this an ARCHITECTURE DECISION?
└─ Yes → [architecture-chain]

Is this a RESEARCH / EXPLORATION?
└─ Yes → [research-chain]
```

---

## Phase 2: Skill Chain Selection

**Pre-built chains — use the matching one, execute skills in order:**

### [debug-chain]
```
1. learning-from-experience  → search for similar past bugs
2. systematic-debugging      → root cause investigation
3. test-driven-development   → failing test before fix
4. verification-before-completion → verify fix works
5. learning-from-experience  → store pattern after success
```

### [feature-chain]
```
1. learning-from-experience  → search for similar past features
2. [domain skill(s)]         → apply domain expertise
3. brainstorming             → design before code (complexity ≥ 4)
4. writing-plans             → implementation plan (complexity ≥ 5)
5. model-routing             → assign tier per task
6. swarm-coordination        → topology if 3+ independent files
7. subagent-driven-development → execute plan (complexity ≥ 6)
8. verification-before-completion → gate before completion
9. requesting-code-review    → review gate (complexity ≥ 7)
10. learning-from-experience → store pattern after success
```

### [refactor-chain]
```
1. learning-from-experience  → search past refactor patterns
2. test-driven-development   → baseline tests before touching code
3. writing-plans             → plan the refactor (complexity ≥ 5)
4. model-routing             → tier 1/2 for mechanical work
5. verification-before-completion → no regression
6. learning-from-experience  → store pattern
```

### [architecture-chain]
```
1. learning-from-experience  → past architecture decisions
2. brainstorming             → explore 2-3 approaches
3. writing-plans (SPARC)     → SPARC structure REQUIRED
4. requesting-code-review    → architecture review gate
5. learning-from-experience  → store decision + rationale
```

### [research-chain]
```
1. learning-from-experience  → search existing knowledge
2. swarm-coordination (Mesh) → parallel investigation
3. brainstorming             → synthesize findings
4. learning-from-experience  → store findings
```

---

## Phase 3: Pattern Search

**BEFORE starting ANY task (complexity ≥ 4):**

```
SEARCH ReasoningBank:
Query: "<task-type> <domain> <key-keywords>"

Example:
- "feature ml-engineering data-drift detection"
- "debug frontend react useEffect stale closure"
- "architecture api jwt multi-tenant"

REVIEW matches:
- What worked? Apply directly.
- What failed? Avoid explicitly.
- What's different? Note context differences.

ANNOUNCE findings:
"Found [N] relevant patterns:
 1. [key] — [one-sentence summary]
 Applying: [how it influences this approach]"

If no matches:
"No prior patterns. Novel problem — will create pattern after solving."
```

---

## Phase 4: Model Tier Assignment

Use the decision from `model-routing` skill. Quick summary:

| Complexity Score | Start Tier | Notes |
|-----------------|------------|-------|
| 1–3 | Tier 0/1 (direct/Haiku) | Mechanical or single-file |
| 4–6 | Tier 2 (Sonnet) | Standard development |
| 7–9 | Tier 2→3 (Sonnet→Opus) | Escalate if stuck |
| 10 | Tier 3 (Opus) | Architecture/security critical |

---

## Phase 5: SPARC Gate

**SPARC is REQUIRED (not optional) when ANY of:**
- Complexity score ≥ 8
- Task involves security-critical code
- Task involves architecture decisions (system design)
- Task is cross-system integration
- Task has been attempted before and failed

**SPARC is optional when:**
- Complexity score ≤ 7
- Clear requirements exist
- Similar task done before (patterns found)

---

## Task Intake Output Template

After completing all 5 phases, announce:

```
TASK INTAKE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Complexity:   [score]/10 → [SIMPLE/STANDARD/COMPLEX/CRITICAL]
Domain(s):    [list]
Task type:    [debug/feature/refactor/architecture/research]
Skill chain:  [chain name]
Model tier:   [0/1/2/3]
SPARC:        [Required/Optional]
Patterns:     [N found | 0 found — novel]

Proceeding with [chain name] chain.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Multi-Domain Synthesis

When a task touches **2+ engineering domains simultaneously**, conflicting guidance can arise. Resolve it before starting work.

### Step 1: Identify Conflicts

After invoking domain skills, check for contradictions:

| Conflict Type | Example | Resolution |
|--------------|---------|------------|
| Language conflict | ML says Python, EE says C only | Platform constraint wins — use C with Python for offline tooling |
| Memory model conflict | ML wants dynamic allocation, EE says no malloc in ISR | ISR constraint is absolute — use static allocation + offline training |
| Latency conflict | AI wants cloud LLM, EE needs <10ms response | Latency is physical — use on-device model or precomputed responses |
| Framework conflict | Frontend wants React, Backend wants server render | Explicit user constraint wins; if none, prefer existing codebase pattern |

**Rule: Physical/hardware constraints always win over software preferences.**

### Step 2: Build Synthesis Statement

Before starting any multi-domain task, write:

```
MULTI-DOMAIN SYNTHESIS
━━━━━━━━━━━━━━━━━━━━━━
Domains:    [domain 1] + [domain 2] (+ [domain 3])
Conflicts:  [list any conflicting guidance]
Resolution: [which constraint wins and why]
Unified constraint: [the combined non-negotiables]
━━━━━━━━━━━━━━━━━━━━━━
```

### Step 3: Add Domain Reviewers

For multi-domain code review, specify ALL relevant domains:
```
DOMAIN: ml, embedded
```
The reviewer will apply both checklists.

---

## After-Action Review (Task Close Protocol)

**Run this AFTER every task completes — before moving to the next.**

This closes the learning loop. Without it, patterns are stored inconsistently or not at all.

```
AFTER-ACTION REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Did the skill chain work as planned?
   [ ] Yes — as expected
   [ ] Partially — [what deviated]
   [ ] No — [what went wrong]

2. Was the complexity score accurate?
   Predicted: [N] | Actual feel: [lower/accurate/higher]
   → [adjust future scoring for this task type]

3. Was the model tier right?
   [ ] Yes — tier [N] was appropriate
   [ ] Should have been higher — [why]
   [ ] Could have been lower — [why]

4. What pattern should be stored?
   Key: <domain>:<type>:<keywords>
   [ ] Storing now in auto-memory
   [ ] Nothing novel — skipping storage

5. What would I do differently?
   [one sentence or "nothing"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**After-action is mandatory when:**
- Task complexity was ≥ 6
- Something unexpected happened
- A novel approach was used
- The first approach failed

**After-action is optional when:**
- Complexity < 4 and everything went as expected
- Mechanical task with no surprises

**Storage:** If a pattern is worth storing, invoke `learning-from-experience` now.

---

## Integration with Superpowers

**Calls into:**
- `learning-from-experience` — pattern search before task
- `model-routing` — tier selection
- `swarm-coordination` — topology selection
- `brainstorming` — when complexity ≥ 4 + feature task
- `writing-plans` — when complexity ≥ 5
- `systematic-debugging` — when task type is debug

**Called by:**
- `using-superpowers` — task-intake is the FIRST process skill for non-trivial tasks

---

## Red Flags

**Never skip task-intake when:**
- You feel "this is obviously simple" (obvious ≠ simple)
- You're under time pressure (intake is 60 seconds, saves hours)
- The user says "just quickly..." (scope always grows)
- You've started before thinking (stop, run intake)

**Rationalization table:**

| Thought | Reality |
|---------|---------|
| "I know what to do" | Knowing ≠ best approach. Intake confirms. |
| "Too simple for intake" | Simple tasks rarely stay simple. |
| "User wants it fast" | Wrong approach is slower than 60-second intake. |
| "I'll plan as I go" | Unplanned work creates rework. |

---

## Final Rule

```
60 seconds of intake → hours saved
No task starts cold
Classify → chain → search → tier → execute
```
