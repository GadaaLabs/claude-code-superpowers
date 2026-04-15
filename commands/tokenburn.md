---
description: "Show a breakdown of token usage and cost by day, project, model, tool, and shell command"
---

Run the tokenburn analytics script and display the output exactly as returned.

Execute this command in your Bash tool:
```
python3 ~/.claude/plugins/superpowers-overrides/scripts/tokenburn.py $ARGS
```

Where `$ARGS` comes from the arguments the user passed to `/tokenburn`:
- No args or `today`  → `--today`
- `week`              → `--week`
- `30d` or `30days`  → `--30d`
- `month`             → `--month`

Display the full output verbatim — do not summarize, trim, or reformat it. Do not add commentary before or after unless the user asks a follow-up question.
