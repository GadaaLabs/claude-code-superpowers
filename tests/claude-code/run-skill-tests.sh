#!/usr/bin/env bash
# Run all Claude Code skill tests
# Usage: ./run-skill-tests.sh [--integration] [--verbose] [--test <file>] [--timeout <seconds>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INTEGRATION=false
VERBOSE=false
SPECIFIC_TEST=""
TIMEOUT=300
PASS=0
FAIL=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --integration) INTEGRATION=true; shift ;;
        --verbose) VERBOSE=true; shift ;;
        --test) SPECIFIC_TEST="$2"; shift 2 ;;
        --timeout) TIMEOUT="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

run_test() {
    local test_file="$1"
    local test_name="$(basename "$test_file" .sh)"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Running: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if $VERBOSE; then
        if timeout "$TIMEOUT" bash "$test_file"; then
            echo "✅ PASSED: $test_name"; ((PASS++))
        else
            echo "❌ FAILED: $test_name"; ((FAIL++))
        fi
    else
        output=$(timeout "$TIMEOUT" bash "$test_file" 2>&1) && {
            echo "✅ PASSED: $test_name"; ((PASS++))
        } || {
            echo "❌ FAILED: $test_name"; echo "$output"; ((FAIL++))
        }
    fi
}

echo "Claude Code Superpowers — Skill Tests"
echo "======================================"

FAST_TESTS=(
    "$SCRIPT_DIR/test-phantom.sh"
    "$SCRIPT_DIR/test-forge.sh"
    "$SCRIPT_DIR/test-hunter.sh"
)

if [ -n "$SPECIFIC_TEST" ]; then
    run_test "$SCRIPT_DIR/$SPECIFIC_TEST"
else
    for test in "${FAST_TESTS[@]}"; do
        [ -f "$test" ] && run_test "$test"
    done
    if $INTEGRATION; then
        echo ""
        echo "Running integration tests (this may take 10-30 minutes)..."
        for test in "$SCRIPT_DIR"/test-*-integration.sh; do
            [ -f "$test" ] && run_test "$test"
        done
    fi
fi

echo ""
echo "======================================"
echo "Results: $PASS passed, $FAIL failed"
echo "======================================"
[ "$FAIL" -eq 0 ]
