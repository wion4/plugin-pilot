#!/usr/bin/env python3
"""Build, update, and query the plugin/skill catalog from all configured marketplaces."""

import json
import os
import sys
import time
import glob

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
CATALOG_FILE = os.path.join(DATA_DIR, "catalog.json")
USAGE_FILE = os.path.join(DATA_DIR, "usage_stats.json")
CATALOG_TTL = 3600 * 12  # refresh catalog every 12 hours

PLUGINS_BASE = os.path.expanduser("~/.claude/plugins")
MARKETPLACES_DIR = os.path.join(PLUGINS_BASE, "marketplaces")
INSTALLED_FILE = os.path.join(PLUGINS_BASE, "installed_plugins.json")


def scan_marketplace(marketplace_path: str, marketplace_name: str) -> list[dict]:
    """Scan a marketplace directory for plugins and skills."""
    entries = []

    # Internal plugins
    plugins_dir = os.path.join(marketplace_path, "plugins")
    if os.path.isdir(plugins_dir):
        for name in os.listdir(plugins_dir):
            plugin_dir = os.path.join(plugins_dir, name)
            if not os.path.isdir(plugin_dir):
                continue
            entry = parse_plugin(plugin_dir, name, marketplace_name, "internal")
            if entry:
                entries.append(entry)

    # External plugins
    ext_dir = os.path.join(marketplace_path, "external_plugins")
    if os.path.isdir(ext_dir):
        for name in os.listdir(ext_dir):
            plugin_dir = os.path.join(ext_dir, name)
            if not os.path.isdir(plugin_dir):
                continue
            entry = parse_plugin(plugin_dir, name, marketplace_name, "external")
            if entry:
                entries.append(entry)

    return entries


def parse_plugin(plugin_dir: str, name: str, marketplace: str, source_type: str) -> dict | None:
    """Parse a plugin directory for metadata, skills, and agents."""
    entry = {
        "name": name,
        "marketplace": marketplace,
        "source_type": source_type,
        "install_id": f"{name}@{marketplace}",
        "description": "",
        "keywords": [],
        "skills": [],
        "agents": [],
        "has_hooks": False,
        "has_mcp": False,
        "has_lsp": False,
        "languages": [],
    }

    # Read plugin.json
    for manifest_path in [
        os.path.join(plugin_dir, ".claude-plugin", "plugin.json"),
        os.path.join(plugin_dir, "plugin.json"),
    ]:
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                entry["description"] = manifest.get("description", "")
                entry["keywords"] = manifest.get("keywords", [])
                entry["version"] = manifest.get("version", "unknown")
            except (json.JSONDecodeError, OSError):
                pass
            break

    # Fallback description from README
    if not entry["description"]:
        readme_path = os.path.join(plugin_dir, "README.md")
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines[1:10]:
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("!"):
                        entry["description"] = line
                        break
            except OSError:
                pass

    # Scan skills
    skills_dir = os.path.join(plugin_dir, "skills")
    if os.path.isdir(skills_dir):
        for skill_name in os.listdir(skills_dir):
            skill_md = os.path.join(skills_dir, skill_name, "SKILL.md")
            if os.path.exists(skill_md):
                skill_info = parse_skill(skill_md, skill_name)
                entry["skills"].append(skill_info)

    # Scan agents
    agents_dir = os.path.join(plugin_dir, "agents")
    if os.path.isdir(agents_dir):
        for agent_file in glob.glob(os.path.join(agents_dir, "*.md")):
            agent_name = os.path.splitext(os.path.basename(agent_file))[0]
            entry["agents"].append({"name": agent_name})

    # Check for hooks, MCP, LSP
    entry["has_hooks"] = os.path.exists(os.path.join(plugin_dir, "hooks", "hooks.json"))
    entry["has_mcp"] = os.path.exists(os.path.join(plugin_dir, ".mcp.json"))
    entry["has_lsp"] = os.path.exists(os.path.join(plugin_dir, ".lsp.json"))

    # Detect language from LSP plugin names
    lsp_langs = {
        "typescript-lsp": ["typescript", "javascript"],
        "pyright-lsp": ["python"],
        "rust-analyzer-lsp": ["rust"],
        "gopls-lsp": ["go"],
        "clangd-lsp": ["c", "cpp"],
        "jdtls-lsp": ["java"],
        "kotlin-lsp": ["kotlin"],
        "ruby-lsp": ["ruby"],
        "swift-lsp": ["swift"],
        "lua-lsp": ["lua"],
        "php-lsp": ["php"],
        "csharp-lsp": ["csharp"],
    }
    if name in lsp_langs:
        entry["languages"] = lsp_langs[name]

    return entry


def parse_skill(skill_md: str, skill_name: str) -> dict:
    """Parse SKILL.md frontmatter for description."""
    info = {"name": skill_name, "description": ""}
    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                frontmatter = content[3:end]
                for line in frontmatter.split("\n"):
                    if line.startswith("description:"):
                        info["description"] = line.split(":", 1)[1].strip().strip('"\'')
                        break
    except OSError:
        pass
    return info


def build_catalog() -> dict:
    """Build full catalog from all marketplaces."""
    catalog = {
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "timestamp": time.time(),
        "marketplaces": [],
        "plugins": [],
    }

    if not os.path.isdir(MARKETPLACES_DIR):
        return catalog

    for mp_name in os.listdir(MARKETPLACES_DIR):
        mp_path = os.path.join(MARKETPLACES_DIR, mp_name)
        if not os.path.isdir(mp_path):
            continue
        catalog["marketplaces"].append(mp_name)
        entries = scan_marketplace(mp_path, mp_name)
        catalog["plugins"].extend(entries)

    catalog["total_plugins"] = len(catalog["plugins"])
    catalog["total_skills"] = sum(len(p.get("skills", [])) for p in catalog["plugins"])

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    return catalog


def get_catalog(force_refresh: bool = False) -> dict:
    """Get catalog, refreshing if stale."""
    if not force_refresh and os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        if time.time() - catalog.get("timestamp", 0) < CATALOG_TTL:
            return catalog

    return build_catalog()


def get_installed() -> dict:
    """Get currently installed plugins."""
    if os.path.exists(INSTALLED_FILE):
        with open(INSTALLED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": 2, "plugins": {}}


def record_usage(plugin_name: str):
    """Record that a plugin was used/relevant."""
    usage = {}
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r", encoding="utf-8") as f:
            usage = json.load(f)

    if plugin_name not in usage:
        usage[plugin_name] = {"first_used": time.strftime("%Y-%m-%dT%H:%M:%S"), "use_count": 0}

    usage[plugin_name]["use_count"] = usage[plugin_name].get("use_count", 0) + 1
    usage[plugin_name]["last_used"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(usage, f, ensure_ascii=False, indent=2)


def find_unused(days: int = 30) -> list[dict]:
    """Find installed plugins not used in N days."""
    installed = get_installed()
    usage = {}
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r", encoding="utf-8") as f:
            usage = json.load(f)

    threshold = time.time() - days * 86400
    unused = []

    for install_id in installed.get("plugins", {}):
        name = install_id.split("@")[0]
        plugin_usage = usage.get(name, {})
        last_used = plugin_usage.get("last_used", "")

        if not last_used:
            # Never tracked — check install date
            entries = installed["plugins"][install_id]
            if entries:
                installed_at = entries[0].get("installedAt", "")
                if installed_at:
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(installed_at.replace("Z", "+00:00"))
                        if dt.timestamp() < threshold:
                            unused.append({"name": name, "install_id": install_id, "reason": "never_used", "installed_at": installed_at})
                    except (ValueError, OSError):
                        pass
        else:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(last_used)
                if dt.timestamp() < threshold:
                    unused.append({"name": name, "install_id": install_id, "reason": "stale", "last_used": last_used})
            except (ValueError, OSError):
                pass

    return unused


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: catalog_manager.py <command> [args]"}))
        print("Commands: build, query, installed, record_usage, find_unused, refresh_check")
        sys.exit(1)

    command = sys.argv[1]

    if command == "build":
        catalog = build_catalog()
        print(json.dumps({
            "status": "ok",
            "plugins": catalog["total_plugins"],
            "skills": catalog["total_skills"],
            "marketplaces": catalog["marketplaces"],
        }, ensure_ascii=False))

    elif command == "query":
        catalog = get_catalog()
        print(json.dumps(catalog, ensure_ascii=False))

    elif command == "installed":
        installed = get_installed()
        names = list(installed.get("plugins", {}).keys())
        print(json.dumps({"installed": names, "count": len(names)}, ensure_ascii=False))

    elif command == "record_usage":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: record_usage <plugin_name>"}))
            sys.exit(1)
        record_usage(sys.argv[2])
        print(json.dumps({"status": "ok"}))

    elif command == "find_unused":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        unused = find_unused(days)
        print(json.dumps({"unused": unused, "count": len(unused)}, ensure_ascii=False))

    elif command == "refresh_check":
        if os.path.exists(CATALOG_FILE):
            with open(CATALOG_FILE, "r", encoding="utf-8") as f:
                catalog = json.load(f)
            stale = time.time() - catalog.get("timestamp", 0) >= CATALOG_TTL
            print(json.dumps({"needs_refresh": stale}))
        else:
            print(json.dumps({"needs_refresh": True}))

    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
