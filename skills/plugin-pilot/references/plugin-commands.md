# Official Claude Code Plugin Management Commands

This is the authoritative reference for plugin CLI commands. Use ONLY these commands.

## Two Ways to Run Commands

1. **Slash commands** (inside Claude Code session): `/plugin install ...`
2. **Bash CLI** (from terminal or Bash tool): `claude plugins install ...`

Both are equivalent. **Agents MUST use the Bash CLI form** since they cannot type slash commands.

## Finding Plugin Names in a Marketplace

After adding a marketplace, the plugin name may not be obvious. To find it:
```bash
# List all installed plugins (shows name@marketplace format)
claude plugins list
```

If installation fails with "Plugin not found", the repo itself IS the plugin (single-plugin repo).
In that case, the marketplace name is the repo name without the owner prefix.
Check with: `ls ~/.claude/plugins/marketplaces/<marketplace-name>/`

## Plugin Installation

### From a marketplace (official or configured)
```bash
claude plugins install <plugin-name>@<marketplace-name>
```
Example: `claude plugins install typescript-lsp@claude-plugins-official`

### From a local directory (for development/testing)
```bash
claude plugins install --plugin-dir /path/to/local/plugin
```

### From GitHub (two-step process)
GitHub repos CANNOT be installed directly. You must:
1. Add the repo as a marketplace first:
   ```bash
   claude plugins marketplace add <owner/repo>
   ```
2. Then install from it:
   ```bash
   claude plugins install <plugin-name>@<marketplace-name>
   ```
   Note: `<marketplace-name>` is usually the repo name (e.g., `jmagar/claude-homelab` → marketplace name is `claude-homelab`)

**IMPORTANT:** `claude plugins install github:owner/repo` does NOT work. Never use this syntax.

## Plugin Uninstallation

```bash
claude plugins uninstall <plugin-name>@<marketplace-name>
```

## Plugin Enable/Disable

```bash
claude plugins enable <plugin-name>@<marketplace-name>
claude plugins disable <plugin-name>@<marketplace-name>
```

## Marketplace Management

### List configured marketplaces
```bash
claude plugins marketplace list
```

### Add a marketplace (GitHub repo or URL)
```bash
claude plugins marketplace add <owner/repo>
```

### Remove a marketplace
```bash
claude plugins marketplace remove <marketplace-name>
```

### Update marketplace catalog
```bash
claude plugins marketplace update
```

## Reload Plugins

After installing or uninstalling, reload to activate changes.

**There is NO bash equivalent.** You MUST ask the user to run:
```
/reload-plugins
```
Use AskUserQuestion: "Плагины установлены. Выполните /reload-plugins для активации." with options ["Готово", "Позже"].
Do NOT silently skip this step — plugins won't work until reloaded.

## Listing Installed Plugins

```bash
claude plugins list
```

## Key Rules

1. Agents use `claude plugins ...` (bash). Users may use `/plugin ...` (slash commands). Both work.
2. GitHub repos require adding as marketplace first — no direct GitHub install
3. The `@marketplace-name` suffix identifies which marketplace the plugin comes from
4. Always `/reload-plugins` after install/uninstall
5. For community GitHub plugins: `marketplace add` → `install` from it
6. If "Plugin not found" after adding marketplace: check plugin name with `claude plugins list` or `ls ~/.claude/plugins/marketplaces/<name>/`
