---
name: pilot
description: Manually trigger plugin analysis — scan your project and suggest plugins to install or remove
argument-hint: "[scan|cleanup|catalog|status]"
allowed-tools: ["Bash", "Read", "Glob", "Grep", "AskUserQuestion"]
---

Manually trigger Plugin Pilot actions.

## Modes

- **No arguments / `scan`**: Analyze current project and task, suggest relevant plugins
- **`cleanup`**: Find unused, conflicting, or deprecated plugins and offer to remove them
- **`catalog`**: Refresh the plugin catalog from all marketplaces, show new additions
- **`status`**: Show current plugin status — installed, usage stats, recommendations

## Execution

1. Load the plugin-pilot skill for full context
2. Use the plugin-resolver agent for analysis
3. Present results and act on user choices
