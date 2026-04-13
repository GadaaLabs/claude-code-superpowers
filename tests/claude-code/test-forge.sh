#!/usr/bin/env bash
# Test: FORGE skill (test-driven development)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "=== Test: FORGE skill (test-driven development) ==="
echo ""

# Test 1: Iron Law is enforced
echo "Test 1: Iron Law..."
output=$(run_claude "What is FORGE's Iron Law? Is it ever optional?" 30)
assert_contains "$output" "test.*first\|failing test\|no production\|Iron Law" "Iron Law mentioned"
assert_contains "$output" "no exception\|never\|mandatory\|always" "No exceptions"
echo ""

# Test 2: RED phase — test must fail first
echo "Test 2: RED phase..."
output=$(run_claude "In FORGE, what must you verify before writing implementation code?" 30)
assert_contains "$output" "fail\|RED\|failing" "Test must fail first"
assert_contains "$output" "verify\|watch\|confirm\|run" "Must verify the failure"
echo ""

# Test 3: GREEN phase — minimal code only
echo "Test 3: GREEN phase..."
output=$(run_claude "In FORGE's GREEN phase, how much code should you write?" 30)
assert_contains "$output" "minimal\|simplest\|minimum\|just enough\|only" "Minimal code"
assert_not_contains "$output" "add features\|extra\|over-engineer" "No over-engineering"
echo ""

# Test 4: API verification before writing tests
echo "Test 4: API verification..."
output=$(run_claude "In FORGE, what should you verify before writing a test that references an external library method?" 30)
assert_contains "$output" "verify\|exist\|check\|confirm" "Must verify API exists"
assert_contains "$output" "import\|method\|signature\|type" "Check import/method"
echo ""

# Test 5: Deleting code written before tests
echo "Test 5: Code before test = delete..."
output=$(run_claude "In FORGE, if you wrote implementation code before the failing test, what must you do?" 30)
assert_contains "$output" "delete\|start over\|remove" "Must delete pre-test code"
echo ""

echo "=== All FORGE skill tests passed ==="
