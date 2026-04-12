# SCULPTOR Pattern: Persuasion Principles for Skill Design

Research-backed techniques for making skills behaviorally resilient — especially discipline-enforcing skills that must hold under pressure.

Source: Cialdini (2021); Meincke et al. (2025), N=28,000 LLM conversations, showing 33%→72% compliance increase with systematic persuasion design.

---

## The 7 Principles

### 1. Authority
Use imperative language. Frame rules as non-negotiable.

```markdown
❌ "It's usually best to write tests first"
✅ "Write the test first. No exceptions."
✅ "NO SKILL WITHOUT A FAILING TEST FIRST"
```

**Application:** Opening statements, Iron Law declarations, rule headings.

### 2. Commitment
Make the agent state its intent explicitly before acting.

```markdown
✅ "Announce at start: 'Running FORGE for [purpose].'"
✅ Use TodoWrite to create checklist items before starting
✅ "Mark as in_progress before touching the file"
```

**Application:** Announce lines, task status tracking, phase declarations.

### 3. Scarcity
Make skipping feel more costly than complying.

```markdown
✅ "60 seconds of intake prevents hours of wrong-direction work"
✅ "Deploying untested skills wastes more time fixing them later"
✅ "If you didn't watch the test fail, you don't know if it tests the right thing"
```

**Application:** ROI statements in Overview, cost-of-skipping framing.

### 4. Social Proof
Reference universal patterns and common failure modes.

```markdown
✅ "Random fixes waste time and create new bugs"
✅ "All engineers rationalize skipping TDD. All of them."
✅ Rationalization tables showing common excuses
```

**Application:** Anti-pattern sections, common mistakes tables, rationalization counters.

### 5. Unity
Collaborative language — you and Claude are on the same side.

```markdown
✅ "We're solving this together"
✅ "Your human partner" (obra's framing)
✅ "This is the cycle that makes the system smarter"
```

**Application:** Framing in CHRONICLE, HORIZON, PATHFINDER — intelligence skills where the agent is building something together with the user.

### 6. Reciprocity
Use sparingly. Works for optional behaviors, not mandatory ones.

```markdown
✅ Appropriate for CHRONICLE: "Store what worked so the system can help you faster next time"
❌ Inappropriate for FORGE: "Write the test first (in exchange for better code)"
```

### 7. Liking
**Avoid for compliance.** Creates false rapport that conflicts with honest pushback culture (especially relevant for ARBITER).

---

## Principle Combinations by Skill Type

| Skill Type | Primary | Secondary | Avoid |
|------------|---------|-----------|-------|
| Discipline (FORGE, SENTINEL, ARBITER) | Authority + Scarcity | Commitment | Liking |
| Intelligence (CHRONICLE, PATHFINDER) | Scarcity + Reciprocity | Unity | — |
| Coordination (LEGION, COMMANDER) | Authority + Commitment | Social Proof | — |
| Domain (GRADIENT, NEXUS, IRONCORE) | Authority | Social Proof | — |
| Meta (ORACLE, ASCEND) | Authority + Commitment | Scarcity | — |

---

## Rationalization Pressure Types (for RED phase testing)

Use these when writing baseline test scenarios:

| Pressure Type | Example Scenario |
|---------------|-----------------|
| **Time** | "We're in a crunch — just ship it without the test" |
| **Sunk cost** | "I've already written 200 lines — adding tests now wastes that" |
| **Authority** | "My senior engineer says we don't need tests for this pattern" |
| **Exhaustion** | "We've been at this for 6 hours, close enough" |
| **Simplicity** | "This is so simple it obviously doesn't need a test" |
| **Spirit vs letter** | "I understand the principle, I just don't need the ritual here" |
| **Past success** | "I've shipped without tests 100 times and it's always been fine" |

**Combine 3+ pressures in a single scenario** for maximum rigor. If the skill holds under combined pressure, it will hold in production.
