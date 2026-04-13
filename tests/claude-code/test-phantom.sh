#!/usr/bin/env bash
# Test: PHANTOM skill (subagent-driven development)
# Verifies that the skill is loaded and follows correct workflow
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "=== Test: PHANTOM skill (subagent-driven development) ==="
echo ""

# Test 1: Verify skill can be loaded
echo "Test 1: Skill loading..."
output=$(run_claude "What is the PHANTOM skill? Describe its key steps briefly." 30)
assert_contains "$output" "PHANTOM\|phantom\|subagent" "Skill is recognized"
assert_contains "$output" "plan\|task\|implement" "Mentions plan/task execution"
echo ""

# Test 2: Workflow order — spec compliance before code quality
echo "Test 2: Workflow ordering..."
output=$(run_claude "In PHANTOM, what comes first: spec compliance review or code quality review? Be specific about the order." 30)
assert_order "$output" "spec.*compliance\|spec compliance" "code.*quality\|code quality" "Spec compliance before code quality"
echo ""

# Test 3: Self-review is required
echo "Test 3: Self-review requirement..."
output=$(run_claude "Does PHANTOM require implementers to do self-review? What should they check?" 30)
assert_contains "$output" "self-review\|self review" "Mentions self-review"
echo ""

# Test 4: Plan is read once at the start
echo "Test 4: Plan reading efficiency..."
output=$(run_claude "In PHANTOM, how many times should the controller read the plan file? When does this happen?" 30)
assert_contains "$output" "once\|one time\|single" "Read plan once"
assert_contains "$output" "beginning\|start\|upfront\|first" "Read at beginning"
echo ""

# Test 5: Spec reviewer is skeptical
echo "Test 5: Spec compliance reviewer mindset..."
output=$(run_claude "What is the spec compliance reviewer's attitude toward the implementer's report in PHANTOM?" 30)
assert_contains "$output" "not trust\|don't trust\|skeptical\|verify.*independently\|independently" "Reviewer is skeptical"
echo ""

# Test 6: Review loops
echo "Test 6: Review loop requirements..."
output=$(run_claude "In PHANTOM, what happens if a reviewer finds issues? Is it a one-time review or a loop?" 30)
assert_contains "$output" "loop\|again\|repeat\|until.*approved\|fix.*review" "Review loops mentioned"
echo ""

# Test 7: Full task text provided directly
echo "Test 7: Task context provision..."
output=$(run_claude "In PHANTOM, how does the controller provide task information to the implementer subagent? Does it make them read a file or provide it directly?" 30)
assert_contains "$output" "provide.*directly\|full.*text\|include.*prompt\|context" "Provides text directly"
echo ""

# Test 8: VAULT is a prerequisite
echo "Test 8: VAULT prerequisite..."
output=$(run_claude "What skills are required before using PHANTOM? List any prerequisites." 30)
assert_contains "$output" "vault\|VAULT\|worktree" "Mentions VAULT/worktree requirement"
echo ""

# Test 9: Never start on main branch
echo "Test 9: Main branch red flag..."
output=$(run_claude "In PHANTOM, is it okay to start implementation directly on the main branch?" 30)
assert_contains "$output" "worktree\|branch\|not.*main\|never.*main\|consent\|permission" "Warns against main branch"
echo ""

echo "=== All PHANTOM skill tests passed ==="
