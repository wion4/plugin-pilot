# Privacy Policy — plugin-pilot

**Last updated:** April 4, 2026

## Overview

The `plugin-pilot` plugin operates entirely on the user's local machine. It does not collect, transmit, or store any personal data on external servers controlled by the plugin author.

## Data collected locally

| Data | Purpose | Storage |
|------|---------|---------|
| Plugin catalog | Index of available plugins from configured marketplaces | `data/catalog.json` |
| Usage statistics | Track which plugins are used to inform cleanup suggestions | `data/usage_stats.json` |
| Community search cache | Cache GitHub search results to reduce API calls | `data/community_cache.json` |
| User consent record | Whether user accepted privacy policy and disclaimers | `data/consent.json` |

## External services

| Service | When | Purpose |
|---------|------|---------|
| **GitHub API** (`api.github.com`) | Only when searching for community plugins | Search repositories, verify plugin structure |

GitHub API requests are authenticated using the user's existing `gh` CLI token if available. No additional credentials are required or stored.

All other operations (catalog building, usage tracking, cleanup) are fully offline and read only from local Claude Code plugin directories.

## Data sharing

This plugin does **not**:
- Send any data to the plugin author or third parties
- Include analytics, telemetry, or tracking
- Upload user data to any cloud service
- Share data between users
- Access any user files or code outside of Claude Code plugin directories

## Third-party plugins

Plugin Pilot may suggest installing third-party plugins from GitHub or unofficial marketplaces. **The plugin-pilot authors bear no responsibility for the content, behavior, safety, or functionality of any third-party plugin.** Users install third-party plugins entirely at their own risk.

## Data retention

All data is stored locally on the user's device. Delete the `data/` directory to remove all plugin-pilot data, including consent records.

## Contact

For questions, open an issue at https://github.com/wion4/plugin-pilot/issues or contact wion4@vk.com.
