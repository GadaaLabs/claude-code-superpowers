---
description: "Show a full token & cost analytics dashboard — by day, project, model, activity, tools, and shell commands"
---

Tell the user to run this command directly in their Claude Code prompt (the `!` prefix runs it in the real terminal with full color support):

For the period they requested, give them the exact command to type:

- No args or `week`  → `! tokenburn report --period week`
- `today`            → `! tokenburn report --period today`
- `30d` or `30days`  → `! tokenburn report --period 30days`
- `month`            → `! tokenburn report --period month`

Default when no argument given: `week`

Tell them: **Type this in your Claude Code prompt** (not as a message to Claude — type it directly into the prompt bar and press Enter):

```
! tokenburn report --period week
```

Explain that the `!` prefix runs commands directly in the terminal with full TTY support, which is what gives tokenburn its colors and layout. Running it through Claude's Bash tool strips the colors.

If `tokenburn` is not found, tell the user:
"tokenburn is not installed. Re-run the installer: `bash ~/.claude/plugins/superpowers-overrides/install.sh`"
