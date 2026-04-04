# Privacy Policy — plugin-pilot

**Last updated:** April 4, 2026

## Overview

The `plugin-pilot` plugin operates entirely on the user's local machine. It does not collect, transmit, or store any personal data on external servers.

## Data collected locally

| Data | Purpose | Storage |
|------|---------|---------|
| Plugin catalog | Index of available plugins from configured marketplaces | `data/catalog.json` |
| Usage statistics | Track which plugins are used to inform cleanup suggestions | `data/usage_stats.json` |

## External services

This plugin makes **no external network requests**. All data is read from locally cached marketplace directories managed by Claude Code itself.

## Data sharing

This plugin does **not**:
- Send any data to the plugin author or third parties
- Include analytics, telemetry, or tracking
- Access any data beyond the Claude Code plugin directories

## Data retention

All data is stored locally. Delete the `data/` directory to remove all plugin-pilot data.

## Contact

For questions, open an issue at https://github.com/wion4/plugin-pilot/issues or contact wion4@vk.com.
