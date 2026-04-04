---
name: pilot
description: Manually trigger plugin analysis — scan your project and suggest plugins to install or remove
argument-hint: "[scan|cleanup|catalog|status|search <query>|reset]"
allowed-tools: ["Bash", "Read", "Glob", "Grep", "AskUserQuestion"]
---

Manually trigger Plugin Pilot actions.

## Modes

- **No arguments / `scan`**: Analyze current project and task, suggest relevant plugins
- **`cleanup`**: Find unused, conflicting, or deprecated plugins and offer to remove them
- **`catalog`**: Refresh the plugin catalog from all marketplaces, show new additions
- **`status`**: Show current plugin status — installed, usage stats, consent status, recommendations
- **`search <query>`**: Search GitHub for community plugins matching the query. Requires third_party_disclaimer consent.
- **`verify <owner/repo>`**: Check if a GitHub repo is a valid Claude Code plugin, show trust score and license info
- **`reset`**: Delete all Plugin Pilot local data (usage stats, catalog cache, consent). GDPR right to deletion.

## Language

Detect the user's system language from `$LANG` (run: `echo $LANG`) and conduct ALL output in that language (e.g. `ru_RU` = Russian, `en_US` = English, `de_DE` = German). This applies to table headers, recommendations, questions, and all other text. Pass the detected language to the plugin-resolver agent in the prompt.

## Execution

1. Detect system language: `echo $LANG`
2. Check consent: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/consent_manager.py check privacy_policy`. If not accepted, run onboarding first.
3. Load the plugin-pilot skill for full context
4. Use the plugin-resolver agent for analysis — **include the detected language in the agent prompt** so it also outputs in the correct language
5. Present results and act on user choices

## Reset Flow

When user runs `/plugin-pilot:pilot reset`:

1. Ask confirmation via AskUserQuestion: "This will delete all Plugin Pilot data: usage stats, catalog cache, and consent records. Continue?" with options ["Yes, delete everything", "No, cancel"]
2. If confirmed:
   ```bash
   rm -rf ${CLAUDE_PLUGIN_ROOT}/data/
   ```
3. Inform user that data is deleted and they'll need to re-accept privacy policy on next session.

## Search Flow

When user runs `/plugin-pilot:pilot search <query>`:

1. Check third_party_disclaimer consent
2. If not consented, explain risks and ask for consent first
3. Search GitHub:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/github_search.py search "<query>"
   ```
4. For each result, show: name, description, stars, license, install command
5. If user wants to install, verify first:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/github_search.py verify <owner/repo>
   ```
6. Show trust score, license risk, and warnings before proceeding
