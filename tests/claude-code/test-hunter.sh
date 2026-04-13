#!/usr/bin/env bash
# Test: HUNTER skill (systematic debugging)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "=== Test: HUNTER skill (systematic debugging) ==="
echo ""

# Test 1: Root cause required before fixing
echo "Test 1: Root cause first..."
output=$(run_claude "In HUNTER, can you apply a fix before identifying the root cause?" 30)
assert_contains "$output" "root cause\|no\|never\|must.*identify\|investigate first" "Root cause required first"
echo ""

# Test 2: Three-strike rule
echo "Test 2: Three-strike rule..."
output=$(run_claude "In HUNTER, what does it mean if you've applied three consecutive failed fixes?" 30)
assert_contains "$output" "architectural\|design\|wrong approach\|deeper\|systemic" "Signals architectural problem"
echo ""

# Test 3: Reproduce before fixing
echo "Test 3: Reproduce first..."
output=$(run_claude "What must HUNTER do before proposing a fix for a bug?" 30)
assert_contains "$output" "reproduce\|replicate\|confirm\|isolate" "Must reproduce first"
echo ""

# Test 4: Pattern storage after solving
echo "Test 4: Pattern storage..."
output=$(run_claude "After HUNTER solves a bug, what should happen to the solution?" 30)
assert_contains "$output" "pattern\|store\|chronicle\|CHRONICLE\|record\|save" "Store the pattern"
echo ""

echo "=== All HUNTER skill tests passed ==="
