# plugin-pilot

AI-driven plugin lifecycle manager for Claude Code. Automatically detects, installs, updates, and cleans up plugins and skills based on your current task.

## What it does

- **Auto-detect** — analyzes your project and task to suggest relevant plugins
- **Smart install** — installs plugins with one confirmation, reloads automatically
- **Cleanup** — finds unused, conflicting, or deprecated plugins and offers removal
- **Catalog sync** — periodically refreshes available plugins from all marketplaces
- **Skill awareness** — not just plugins, also suggests relevant skills
- **Usage tracking** — tracks which plugins you actually use to inform cleanup decisions

## Examples

| You say | Plugin Pilot suggests |
|---------|----------------------|
| "Build a React dashboard" | frontend-design, typescript-lsp |
| "Review PR #42" | code-review, github |
| "Write browser tests" | playwright |
| "Deploy to Supabase" | supabase |
| "Set up Terraform" | terraform |

## Installation

```bash
/plugin install github:wion4/plugin-pilot
```

## Usage

Plugin Pilot works automatically — it analyzes your messages and project context, suggesting plugins when relevant.

Manual commands:

```
/plugin-pilot:pilot           # Scan project, suggest plugins
/plugin-pilot:pilot cleanup   # Find and remove unused plugins
/plugin-pilot:pilot catalog   # Refresh plugin catalog
/plugin-pilot:pilot status    # Show plugin stats
```

## Unofficial marketplaces

Plugin Pilot scans all configured marketplaces, not just the official one. Plugins from unofficial marketplaces are flagged with a warning.

## Privacy

All data stays local. Usage stats and catalog are stored in `data/` within the plugin directory. No data is sent anywhere.

## License

[MIT](LICENSE)
