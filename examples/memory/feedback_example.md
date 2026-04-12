---
name: Example Feedback Memory
description: Template for recording corrections and validated approaches
type: feedback
---

# Feedback: [Short Title]

[Lead with the rule itself — the thing Claude should do or never do.]

**Why:** [The reason you gave — a past incident, a strong preference, or a system constraint.
Include enough detail that future Claude can make judgment calls about edge cases.]

**How to apply:** [When and where this guidance kicks in.
Be specific about the trigger conditions so it does not apply too broadly.]

---

# Real examples to learn from:

## Example: Never Simplify Animated Admin Cards
The animated access cards on the DataLab admin page must never be simplified or reverted to static cards.

**Why:** A previous session "cleaned up" the CSS and replaced animated cards with static ones,
breaking the intentional visual identity. Required full re-implementation.

**How to apply:** Any CSS fix to the admin page must preserve animation logic.
If there is a conflict, resolve it without touching the animation keyframes.

---

## Example: No Database Mocks in Tests
Integration tests must hit a real database (test instance), never a mock.

**Why:** Last quarter, mocked tests all passed but a prod migration failed because
the mock did not enforce the same foreign key constraints as the real DB.
Cost 6 hours of incident response.

**How to apply:** Any time a test needs database access, use the test DB connection.
Never use `jest.mock()` or `unittest.mock` on database clients.
