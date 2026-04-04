---
name: Plugin Pilot
description: This skill should be used when the user starts a task that could benefit from additional plugins or skills, when they ask to "install plugins", "find plugins", "clean up plugins", "what plugins do I need", "remove unused plugins", or when analyzing the current task context to suggest relevant marketplace plugins and skills. Also activates on "check for new plugins", "update plugin catalog", or "plugin conflicts".
version: 0.1.0
---

# Plugin Pilot — AI-Driven Plugin Lifecycle Manager

Automatically detect, install, update, and clean up Claude Code plugins and skills based on the user's current task, project context, and usage patterns.

## Core Responsibilities

### 1. Task-Aware Plugin Detection

When the user starts working on a task, analyze the context to determine if any available plugins would help. Consider:

- **File types in the project** — `.ts`/`.tsx` → typescript-lsp, `.py` → pyright-lsp, `.rs` → rust-analyzer-lsp, etc.
- **Frameworks detected** — `package.json` with React → frontend-design, Laravel → laravel-boost
- **Task keywords** — "PR review" → code-review/pr-review-toolkit, "deploy" → terraform/supabase/firebase
- **Services mentioned** — "Slack message" → slack, "Linear ticket" → linear, "GitHub issue" → github
- **Workflow patterns** — "test in browser" → playwright, "design UI" → frontend-design

### 2. Plugin Resolution

Query the catalog to find matching plugins:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/catalog_manager.py query
```

Cross-reference with installed plugins:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/catalog_manager.py installed
```

Only suggest plugins that are NOT already installed.

### 3. Installation Flow

When a relevant plugin is identified:

1. **Ask the user** via AskUserQuestion before installing:
   - Question: "Для этой задачи пригодится плагин **{name}** — {description}. Установить?"
   - Options: ["Да, ставь", "Нет, не нужно", "Расскажи подробнее"]
2. If confirmed, install:
   ```bash
   claude /plugin install {install_id}
   ```
3. Reload plugins to activate:
   ```bash
   claude /reload-plugins
   ```
4. Record usage:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/catalog_manager.py record_usage {name}
   ```

### 4. Cleanup and Removal

Periodically check for plugins that should be removed:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/catalog_manager.py find_unused 30
```

**Removal triggers:**
- **Unused** — installed but not used in 30+ days
- **Conflict** — two plugins providing overlapping functionality (e.g., duplicate LSP for same language)
- **Deprecated** — plugin no longer in marketplace catalog
- **User request** — explicit "remove/clean up plugins"

Before removing, always confirm with the user:
- Question: "Плагин **{name}** не использовался {days} дней. Удалить?"
- Options: ["Удалить", "Оставить", "Напомни позже"]

### 5. Catalog Synchronization

The catalog of available plugins may grow over time. Refresh periodically:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/catalog_manager.py refresh_check
```

If stale (>12 hours), rebuild:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/catalog_manager.py build
```

This scans all configured marketplaces (official and custom) for new plugins.

### 6. Skill Management

Not just plugins — also detect when individual skills within installed plugins could help:

- Read the catalog's skill entries with their trigger descriptions
- If a user's task matches a skill's triggers, inform them about it
- Skills don't need installation if their parent plugin is already installed — just inform the user about the skill

## Plugin-Task Mapping Reference

### By file type / language
| Detected | Plugin |
|----------|--------|
| `.ts`, `.tsx`, `.js`, `.jsx` | typescript-lsp |
| `.py` | pyright-lsp |
| `.rs` | rust-analyzer-lsp |
| `.go` | gopls-lsp |
| `.java` | jdtls-lsp |
| `.kt` | kotlin-lsp |
| `.rb` | ruby-lsp |
| `.swift` | swift-lsp |
| `.lua` | lua-lsp |
| `.php` | php-lsp |
| `.c`, `.cpp`, `.h` | clangd-lsp |
| `.cs` | csharp-lsp |

### By task type
| Task | Plugins |
|------|---------|
| Frontend/UI development | frontend-design, typescript-lsp |
| Code review / PR | code-review, pr-review-toolkit, github |
| Browser testing | playwright |
| API development | mcp-server-dev |
| Infrastructure | terraform |
| Database (Supabase) | supabase |
| Database (Firebase) | firebase |
| Laravel project | laravel-boost, php-lsp |
| Git workflow | commit-commands, github/gitlab |
| Team communication | slack, discord, telegram |
| Project management | linear, asana |
| Plugin development | plugin-dev |
| Skill creation | skill-creator |
| Math/competition | math-olympiad |
| Security audit | security-guidance |

### By framework (detected from config files)
| File | Framework | Plugins |
|------|-----------|---------|
| `package.json` with react | React | frontend-design, typescript-lsp |
| `Cargo.toml` | Rust | rust-analyzer-lsp |
| `go.mod` | Go | gopls-lsp |
| `composer.json` | PHP/Laravel | php-lsp, laravel-boost |
| `Gemfile` | Ruby | ruby-lsp |
| `*.tf` | Terraform | terraform |
| `supabase/` dir | Supabase | supabase |
| `firebase.json` | Firebase | firebase |

## Unofficial Marketplaces

Users may configure additional marketplaces beyond the official one. Plugin Pilot scans ALL configured marketplaces during catalog builds. However:

- Always note when suggesting a plugin from a non-official marketplace
- Warn: "This plugin is from an unofficial marketplace. Install at your own risk."
- Official marketplace plugins are preferred when multiple options exist

## Important Rules

1. **Never install without asking** — always confirm with the user first
2. **Never remove without asking** — always confirm before uninstalling
3. **Don't spam suggestions** — max 1-2 plugin suggestions per session, only for clearly relevant ones
4. **Track usage** — record when plugins are actually used to inform cleanup decisions
5. **Respect user preferences** — if user declines a plugin, don't suggest it again in the same session
6. **Batch suggestions** — if multiple plugins are needed, suggest them together in one question
