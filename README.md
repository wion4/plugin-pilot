# plugin-pilot

AI-driven plugin lifecycle manager for Claude Code. Automatically detects, installs, updates, and cleans up plugins and skills based on your current task.

## What it does

- **Auto-detect** — analyzes your project and task to suggest relevant plugins
- **Smart install** — installs plugins with one confirmation, reloads automatically
- **Community search** — finds plugins on GitHub, verifies structure and license before suggesting
- **Cleanup** — finds unused, conflicting, or deprecated plugins and offers removal
- **Catalog sync** — periodically refreshes available plugins from all marketplaces
- **Skill awareness** — not just plugins, also suggests relevant skills
- **Usage tracking** — tracks which plugins you actually use to inform cleanup decisions
- **License checks** — warns about restrictive or missing licenses on community plugins

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

On first launch, Plugin Pilot will ask you to accept the Terms of Service and Privacy Policy.

## Usage

Plugin Pilot works automatically — it analyzes your messages and project context, suggesting plugins when relevant.

Manual commands:

```
/plugin-pilot:pilot              # Scan project, suggest plugins
/plugin-pilot:pilot cleanup      # Find and remove unused plugins
/plugin-pilot:pilot catalog      # Refresh plugin catalog
/plugin-pilot:pilot status       # Show plugin stats and consent status
/plugin-pilot:pilot search <q>   # Search GitHub for community plugins
/plugin-pilot:pilot verify <r>   # Verify a GitHub repo (owner/repo)
/plugin-pilot:pilot reset        # Delete all local data (GDPR)
```

## Trust Score

Community plugins are scored based on:
- Plugin structure (manifest, skills, commands, agents)
- Documentation (README, LICENSE, PRIVACY.md)
- Repository metrics (stars, age)
- License type (permissive preferred, penalty for missing)

**Trust score is NOT a security audit.** It only indicates structural quality. Always review source code before installing community plugins.

## Legal

By using Plugin Pilot, you agree to:

- **[Terms of Service](TERMS.md)** — usage terms, liability limitations, indemnification
- **[Privacy Policy](PRIVACY.md)** — data handling, local storage, GitHub API usage
- **[Third-Party Disclaimer](DISCLAIMER.md)** — liability waiver for community plugins

Plugin Pilot requires explicit acceptance of Terms and Privacy Policy before operating. Community plugin search requires separate opt-in consent.

### Data deletion

All data is stored locally. Run `/plugin-pilot:pilot reset` or delete the `data/` directory to remove everything.

### Not affiliated with Anthropic

Plugin Pilot is a community project. It is not affiliated with, endorsed by, or sponsored by Anthropic, PBC. "Claude Code" and "Anthropic" are trademarks of Anthropic, PBC.

## License

[MIT](LICENSE)
