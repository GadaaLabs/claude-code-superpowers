# Contributing to Claude Code Superpowers

Contributions are welcome and encouraged. This document explains how to add new skills, improve existing ones, and submit pattern files.

## Types of Contributions

### New domain skills
Skills for domains not yet covered: DevOps/Kubernetes, security engineering, data engineering, mobile (iOS/Android), game development, etc.

### New pattern files
Code examples and configuration templates for existing skills. If a skill's SKILL.md references "load patterns/X.md" but the file does not exist, that is an open contribution opportunity.

### Improved entry points
Better assessment questions that route more accurately to the right section.

### Community custom skills
Skills your team built for your domain — share them so others benefit.

### Bug fixes
Incorrect patterns, broken code examples, outdated configurations.

---

## Skill Design Principles

Before writing, read one existing SKILL.md to understand the format. Key principles:

**Every skill must have an entry point.** Never dump all patterns immediately. Ask what stage or type of work before applying anything.

**Distinguish rigid from flexible.** Rigid skills (TDD, debugging, verification) are followed exactly every time. Flexible skills (domain expertise) adapt to context. Know which yours is.

**Red flags are mandatory.** The "Never" and "Always" section prevents the most common mistakes. If you cannot list at least 3 red flags, the skill is not specific enough.

**Final checklist = completion gate.** Every checklist item must be verifiable. "Code is good" is not a checklist item. "All tests pass and P99 latency is under budget" is.

**Extract heavy code to patterns/.** If a section contains more than ~20 lines of code or configuration, move it to `patterns/<section-name>.md` and reference it: "Load patterns: `patterns/<section-name>.md`".

---

## File Structure

```
skills/
  your-skill-name/
    SKILL.md           ← required, lean (target <900 tokens)
    patterns/          ← optional, created if SKILL.md references patterns
      section-one.md
      section-two.md
```

---

## SKILL.md Template

```markdown
---
name: your-skill-name
description: Specific one-line description of WHEN this skill applies. Be concrete.
type: process | domain | implementation
---

# Your Skill Title

## Overview

**Core principle:** One sentence capturing the essential insight of this domain.

This skill provides **[what it provides]** for **[who uses it]**.

**Announce at start:** "I'm using the [name] skill for [purpose]."

---

## Entry Point — First 5 Minutes

When invoked, determine [what you need to know] before applying any patterns:

\`\`\`
ASSESSMENT:

"[Question that determines which section applies]"
A) Option A
B) Option B
C) Option C

→ Go to the relevant section.
\`\`\`

**Option → Section mapping:**
- A → [Section name]
- B → [Section name]
- C → [Section name]

**After identifying [dimension], ask:**
"[The one question whose answer shapes all trade-offs]"

---

## Section A: [Name]

[Content, or: Load patterns: `patterns/section-a.md`]

---

## Red Flags

**Never:**
- [Specific thing to never do]
- [Another specific thing]

**Always:**
- [Specific thing to always do]
- [Another specific thing]

---

## Integration with Superpowers

**Used with:**

| Skill | Integration |
|-------|-------------|
| `test-driven-development` | [How] |
| `verification-before-completion` | [How] |

---

## Final Checklist

Before claiming [domain] work complete:

- [ ] [Verifiable criterion]
- [ ] [Verifiable criterion]
- [ ] [Verifiable criterion]
```

---

## Pattern File Template

```markdown
# [Domain] — [Section Name] Patterns

## [Pattern Group 1]

\`\`\`[language]
[code example]
\`\`\`

## [Pattern Group 2]

\`\`\`[language]
[code example]
\`\`\`
```

---

## Submission Process

1. Fork the repository
2. Create a branch: `git checkout -b skill/your-skill-name`
3. Add your skill directory under `skills/`
4. Test it:
   - Install with `bash install.sh`
   - Open Claude Code in a project
   - Invoke your skill: `/your-skill-name`
   - Verify the entry point routes correctly
   - Verify the red flags section is actionable
5. Open a PR with:
   - **Title:** `skill: add [skill-name] — [one-line description]`
   - **Body:** What domain it covers, what failure modes it prevents, example invocation

---

## Skill Quality Bar

A PR will be merged if the skill:

- Has a specific `description` that enables accurate relevance matching
- Has an entry point that asks before dumping patterns
- Has a Red Flags section with ≥ 3 concrete never/always items
- Has a Final Checklist with ≥ 3 verifiable items
- Keeps SKILL.md under ~900 tokens (move code to patterns/ if larger)
- Includes a code example (inline or in patterns/) that compiles/runs

---

## Questions

Open an issue or start a discussion. Community questions help improve the documentation.
