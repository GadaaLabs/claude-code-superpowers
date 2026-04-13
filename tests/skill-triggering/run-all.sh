#!/usr/bin/env bash
# Run all skill-triggering tests
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
PASS=0
FAIL=0

run() {
    local skill="$1"
    local prompt_file="$SCRIPT_DIR/prompts/${skill}.txt"
    if [ ! -f "$prompt_file" ]; then
        echo "⚠️  SKIP: $skill (no prompt file)"
        return
    fi
    if bash "$SCRIPT_DIR/run-test.sh" "$skill" "$prompt_file" 3; then
        ((PASS++))
    else
        ((FAIL++))
    fi
}

echo "=== Skill Triggering Tests ==="
echo ""

for skill in forge hunter blueprint phantom tribunal commander; do
    run "$skill"
    echo ""
done

echo "=============================="
echo "Results: $PASS passed, $FAIL failed"
echo "=============================="
[ "$FAIL" -eq 0 ]
