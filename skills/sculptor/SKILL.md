---
name: sculptor
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment — applies TDD to process documentation with the same Iron Law as FORGE
type: process
---

# Writing Skills

## Overview

**SCULPTOR** — *A sculptor does not add clay randomly — every choice is deliberate, tested against the form, and refined until it holds.*
When invoked: applies TDD to skill creation — write a failing test (pressure scenario) first, then write the skill to pass it, then refactor to close every loophole. No skill ships without watching an agent fail without it first.

**Core principle:** Creating skills IS Test-Driven Development applied to process documentation.

**Announce at start:** "Running SCULPTOR to write this skill with TDD discipline."

**Required background:** You must understand `forge` before using this skill. The RED-GREEN-REFACTOR cycle is identical — only the artifact changes.

---

## The Iron Law (Same as FORGE)

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Applies to new skills AND edits to existing skills.

**No exceptions:**
- Not for "simple additions"
- Not for "just adding a section"
- Not for "documentation updates"
- Don't keep untested changes as "reference"
- Don't "adapt" while running tests
- Delete means delete — start over

---

## TDD Mapping for Skills

| FORGE Concept | SCULPTOR Equivalent |
|---------------|-------------------|
| Test case | Pressure scenario with subagent |
| Production code | SKILL.md |
| RED — test fails | Agent violates the rule without the skill |
| GREEN — test passes | Agent complies with the skill present |
| REFACTOR | Close loopholes while maintaining compliance |
| Write test first | Run baseline scenario BEFORE writing skill |
| Watch it fail | Document exact rationalizations the agent uses |
| Minimal code | Write skill addressing those specific violations only |

---

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious
- You'd reference it again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in `CLAUDE.md` instead)
- Mechanical constraints that can be enforced with regex or validation — automate instead

---

## SKILL.md Structure

```markdown
---
name: skill-name
description: Use when [specific triggering conditions and symptoms]
type: process | domain | implementation
---

# Skill Name

## Overview
[Codename meaning + execution description]
Core principle in 1–2 sentences.
Announce at start: "Running [NAME] for [purpose]."

## Entry Point / When to Use
[Small flowchart ONLY if decision is non-obvious]
[Symptom-based bullet list]

## Core Pattern
[Steps, tables, code]

## Quick Reference
[Table for fast scanning]

## Red Flags
Never: ...
Always: ...

## Final Checklist
- [ ] Verifiable completion criterion
```

---

## Claude Search Optimization (CSO)

Skills are useless if they can't be found. Optimize for discovery.

### The Description Rule — Most Critical

**Description = WHEN to use. Never WHAT it does.**

```yaml
# ❌ BAD: Summarizes workflow — Claude follows the description instead of reading the skill
description: Use when executing plans — dispatches subagent per task with review between tasks

# ✅ GOOD: Triggering conditions only
description: Use when executing implementation plans with independent tasks in the current session
```

**Why this matters:** When a description summarizes workflow, Claude takes it as a shortcut and skips reading the skill body. A description saying "code review between tasks" caused Claude to do ONE review, even though the skill showed TWO. Changing to triggering-conditions-only fixed it.

**Format rules:**
- Start with "Use when..."
- Describe symptoms and situations, not process steps
- Write in third person (injected into system prompt)
- Under 500 characters

### Keyword Coverage

Include words Claude would search for:
- Error messages: `"Hook timed out"`, `"race condition"`, `"ENOTEMPTY"`
- Symptoms: `"flaky"`, `"hanging"`, `"zombie"`, `"pollution"`
- Synonyms: `"timeout/hang/freeze"`, `"cleanup/teardown/afterEach"`
- Tool names, library names, file types

### Token Efficiency

**Target word counts:**
- Frequently-loaded skills: < 200 words total
- Other skills: < 500 words

**Techniques:**
- Move heavy reference (100+ lines) to `patterns/` files (lazy-load)
- Cross-reference other skills instead of repeating their content
- One excellent code example beats five mediocre ones

Load the `patterns/persuasion-principles.md` file for research-backed techniques on making skills behaviorally resilient under pressure.

---

## RED-GREEN-REFACTOR for Skills

### RED — Run Baseline First

Run a pressure scenario with a subagent **without** the skill. Document:
- What choices did the agent make?
- What rationalizations did it use (verbatim)?
- Which pressures triggered the violation?

**This is non-negotiable.** You must see the failure before writing the skill.

### GREEN — Write Minimal Skill

Write the skill to address those specific rationalizations only. No speculative content.

Run the same scenario **with** the skill present. The agent should now comply.

### REFACTOR — Close Loopholes

Agent found a new rationalization? Add an explicit counter. Re-test. Repeat until bulletproof.

---

## Bulletproofing Against Rationalization

For discipline-enforcing skills, close loopholes explicitly:

**State the rule AND forbid the workarounds:**
```markdown
❌ Write code before test? Delete it.

✅ Write code before test? Delete it. Start over.
   No exceptions:
   - Don't keep it as "reference"
   - Don't "adapt" it while writing tests
   - Don't look at it
   - Delete means delete
```

**Add the spirit-vs-letter block early:**
```markdown
Violating the letter of the rules is violating the spirit of the rules.
```

**Build a rationalization table from your baseline test:**
```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "Tests after achieve the same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
```

---

## Skill Deployment Checklist

**RED Phase:**
- [ ] Pressure scenarios written (3+ combined pressures for discipline skills)
- [ ] Baseline run without skill — behavior documented verbatim
- [ ] Rationalization patterns identified

**GREEN Phase:**
- [ ] `name:` uses letters, numbers, hyphens only
- [ ] `description:` starts with "Use when...", triggering conditions only, third person
- [ ] Addresses specific baseline failures from RED
- [ ] One excellent code example (not multi-language)
- [ ] Scenarios run WITH skill — agent now complies

**REFACTOR Phase:**
- [ ] New rationalizations identified and countered
- [ ] Rationalization table built from all test iterations
- [ ] Red Flags list written
- [ ] Re-tested until bulletproof

**Quality Checks:**
- [ ] No narrative storytelling ("in session 2025-10-03 we found...")
- [ ] Flowchart only if decision is non-obvious
- [ ] Supporting files only for tools or heavy reference
- [ ] Token-efficient — heavy content in `patterns/` files

---

## Red Flags

**Never:**
- Write a skill without a failing baseline test first
- Create multiple skills in batch without testing each one
- Move to the next skill before the current one is verified
- Keep untested changes as "reference"

**Always:**
- RED → GREEN → REFACTOR, in that order
- Deploy and test each skill before starting the next
- Build the rationalization table from real baseline failures
- Optimize description for discovery (triggering conditions only)

---

## Integration

**Required background:**
- `forge` — the TDD cycle this skill adapts to documentation

**Pairs with:**
- `oracle` — classify skill creation as a task before starting
- `sentinel` — verify the skill works before claiming it's done
