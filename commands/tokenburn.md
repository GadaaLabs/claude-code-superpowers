---
description: "Interactive token & cost analytics dashboard — by day, project, model, activity, tools, and MCP"
---

Run the tokenburn analytics dashboard and display the output.

Execute this command in your Bash tool:
```
tokenburn report --period PERIOD
```

Map the user's argument to PERIOD:
- No args, `today`          → `today`
- `week` or `7d`           → `week`
- `30d` or `30days`        → `30days`
- `month`                  → `month`

Default period if nothing specified: `week`

Display the full output verbatim — do not summarize, trim, or reformat it.

If `tokenburn` is not found, tell the user to run:
  bash ~/.claude/plugins/superpowers-overrides/install.sh

Do not add commentary before or after the output unless the user asks a follow-up question.
