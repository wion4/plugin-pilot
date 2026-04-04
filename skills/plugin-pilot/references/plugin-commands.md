# Official Claude Code Plugin Management Commands

This is the authoritative reference for plugin CLI commands. Use ONLY these commands.

## Plugin Installation

### From a marketplace (official or configured)
```
/plugin install <plugin-name>@<marketplace-name>
```
Example: `/plugin install typescript-lsp@claude-plugins-official`

### From a local directory (for development/testing)
```
/plugin install --plugin-dir /path/to/local/plugin
```

### From GitHub (two-step process)
GitHub repos CANNOT be installed directly. You must:
1. Add the repo as a marketplace first:
   ```
   /plugin marketplace add <owner/repo>
   ```
2. Then install from it:
   ```
   /plugin install <plugin-name>@<owner/repo>
   ```

**IMPORTANT:** `/plugin install github:owner/repo` does NOT work. Never use this syntax.

## Plugin Uninstallation

```
/plugin uninstall <plugin-name>@<marketplace-name>
```

## Plugin Enable/Disable

```
/plugin enable <plugin-name>@<marketplace-name>
/plugin disable <plugin-name>@<marketplace-name>
```

## Marketplace Management

### List configured marketplaces
```
/plugin marketplace list
```

### Add a marketplace (GitHub repo or URL)
```
/plugin marketplace add <owner/repo>
```

### Remove a marketplace
```
/plugin marketplace remove <marketplace-name>
```

### Update marketplace catalog
```
/plugin marketplace update
```

## Reload Plugins

After installing or uninstalling, reload to activate changes:
```
/reload-plugins
```

## Listing Installed Plugins

```
/plugin list
```

## Key Rules

1. Always use `/plugin install`, not `claude plugin install` or `claude /plugin install`
2. GitHub repos require adding as marketplace first — no direct GitHub install
3. The `@marketplace-name` suffix identifies which marketplace the plugin comes from
4. Always `/reload-plugins` after install/uninstall
5. For community GitHub plugins: add repo as marketplace → install from it
