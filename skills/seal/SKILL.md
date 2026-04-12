---
name: seal
description: Use when implementation is complete and all tests pass — guides branch completion through four structured options (merge, PR, keep, discard) with verification and worktree cleanup
type: process
---

# Finishing a Development Branch

## Overview

**SEAL** — *A seal closes and secures — nothing leaves without passing inspection.*
When invoked: verifies tests pass, presents exactly four structured completion options, executes the chosen path, and cleans up the isolated workspace. Nothing merges without evidence.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "Running SEAL to complete this branch."

---

## The Process

### Step 1: Verify Tests

**Before presenting any options:**

```bash
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:
[Show failures]
Cannot proceed until tests pass.
```

Stop. Do not present options.

**If tests pass:** proceed to Step 2.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or confirm: "This branch split from main — is that correct?"

### Step 3: Present Exactly 4 Options

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

No extra explanation — keep options concise.

### Step 4: Execute the Choice

#### Option 1 — Merge Locally

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
<test command>          # Verify merged result
git branch -d <feature-branch>
```

Then: cleanup worktree (Step 5).

#### Option 2 — Push and Create PR

```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: cleanup worktree (Step 5).

#### Option 3 — Keep As-Is

Report: `"Keeping branch <name>. Worktree preserved at <path>."`

Do **not** clean up the worktree.

#### Option 4 — Discard

**Confirm first — require typed confirmation:**

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: cleanup worktree (Step 5).

### Step 5: Cleanup Worktree (Options 1, 2, 4 only)

```bash
git worktree list | grep $(git branch --show-current)
git worktree remove <worktree-path>
```

Option 3: keep worktree intact.

---

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | — | — | ✓ |
| 2. Create PR | — | ✓ | ✓ | — |
| 3. Keep as-is | — | — | ✓ | — |
| 4. Discard | — | — | — | ✓ (force) |

---

## Red Flags

**Never:**
- Present options before verifying tests
- Merge without re-verifying tests on the merged result
- Delete work without typed confirmation
- Force-push without explicit user request

**Always:**
- Verify tests before offering options
- Present exactly 4 options — no more, no less
- Require `'discard'` typed confirmation for Option 4
- Only clean up the worktree for Options 1 and 4

---

## Integration

**Called by:**
- `phantom` — after all plan tasks complete
- `exodus` — after all execution batches complete

**Pairs with:**
- `vault` — cleans up the worktree that VAULT created
