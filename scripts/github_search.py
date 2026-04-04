#!/usr/bin/env python3
"""Search GitHub for community Claude Code plugins and skills."""

import json
import os
import sys
import time
import urllib.request
import urllib.error

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
COMMUNITY_CACHE = os.path.join(DATA_DIR, "community_cache.json")
CACHE_TTL = 3600 * 6  # 6 hours


def github_api(endpoint: str, token: str = "") -> dict | list:
    """Make a GitHub API request."""
    url = f"https://api.github.com{endpoint}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "plugin-pilot",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def get_gh_token() -> str:
    """Try to get GitHub token from gh CLI config."""
    try:
        import subprocess
        result = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return ""


def search_plugins(query: str = "", token: str = "") -> list[dict]:
    """Search GitHub for Claude Code plugins."""
    if not token:
        token = get_gh_token()

    search_queries = []

    if query:
        # User-specific search
        search_queries.append(
            f"claude-plugin plugin.json {query} in:name,description,readme"
        )
    else:
        # General discovery
        search_queries = [
            "claude-plugin plugin.json in:path language:JSON",
            "claude code plugin .claude-plugin in:path",
            "claude-code-plugin topic:claude-code",
        ]

    all_results = []
    seen_repos = set()

    for sq in search_queries:
        try:
            encoded = urllib.request.quote(sq)
            data = github_api(
                f"/search/repositories?q={encoded}&sort=updated&per_page=30",
                token,
            )
            for repo in data.get("items", []):
                full_name = repo["full_name"]
                if full_name in seen_repos:
                    continue
                seen_repos.add(full_name)

                # Skip official Anthropic repos
                if repo.get("owner", {}).get("login") in ("anthropics",):
                    continue

                all_results.append({
                    "name": repo["name"],
                    "full_name": full_name,
                    "description": repo.get("description", ""),
                    "url": repo["html_url"],
                    "stars": repo.get("stargazers_count", 0),
                    "updated_at": repo.get("updated_at", ""),
                    "language": repo.get("language", ""),
                    "topics": repo.get("topics", []),
                    "owner": repo.get("owner", {}).get("login", ""),
                    "install_cmd": f"github:{full_name}",
                    "source": "github_community",
                    "license": repo.get("license", {}).get("spdx_id", "") if repo.get("license") else "",
                })
        except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
            continue

        # Rate limit courtesy
        time.sleep(0.5)

    # Sort by stars
    all_results.sort(key=lambda x: x["stars"], reverse=True)
    return all_results


def search_by_task(task_keywords: list[str], token: str = "") -> list[dict]:
    """Search GitHub for plugins relevant to specific task keywords."""
    if not token:
        token = get_gh_token()

    results = []
    seen = set()

    for keyword in task_keywords:
        query = f"claude code plugin {keyword}"
        try:
            encoded = urllib.request.quote(query)
            data = github_api(
                f"/search/repositories?q={encoded}&sort=stars&per_page=10",
                token,
            )
            for repo in data.get("items", []):
                full_name = repo["full_name"]
                if full_name in seen:
                    continue
                seen.add(full_name)

                if repo.get("owner", {}).get("login") in ("anthropics",):
                    continue

                results.append({
                    "name": repo["name"],
                    "full_name": full_name,
                    "description": repo.get("description", ""),
                    "url": repo["html_url"],
                    "stars": repo.get("stargazers_count", 0),
                    "updated_at": repo.get("updated_at", ""),
                    "topics": repo.get("topics", []),
                    "owner": repo.get("owner", {}).get("login", ""),
                    "install_cmd": f"github:{full_name}",
                    "source": "github_community",
                    "matched_keyword": keyword,
                    "license": repo.get("license", {}).get("spdx_id", "") if repo.get("license") else "",
                })
        except (urllib.error.URLError, json.JSONDecodeError):
            continue
        time.sleep(0.5)

    results.sort(key=lambda x: x["stars"], reverse=True)
    return results


def verify_plugin(repo_full_name: str, token: str = "") -> dict:
    """Verify a GitHub repo is actually a valid Claude Code plugin."""
    if not token:
        token = get_gh_token()

    checks = {
        "has_plugin_json": False,
        "has_readme": False,
        "has_license": False,
        "has_skills": False,
        "has_commands": False,
        "has_agents": False,
        "has_hooks": False,
        "plugin_name": "",
        "plugin_description": "",
    }

    try:
        # Check repo contents
        contents = github_api(f"/repos/{repo_full_name}/contents/", token)
        root_names = {item["name"] for item in contents}

        checks["has_readme"] = "README.md" in root_names or "readme.md" in root_names
        checks["has_license"] = "LICENSE" in root_names or "LICENSE.md" in root_names

        if ".claude-plugin" in root_names:
            try:
                plugin_dir = github_api(f"/repos/{repo_full_name}/contents/.claude-plugin", token)
                plugin_names = {item["name"] for item in plugin_dir}
                if "plugin.json" in plugin_names:
                    checks["has_plugin_json"] = True
                    # Fetch plugin.json content
                    pj = github_api(f"/repos/{repo_full_name}/contents/.claude-plugin/plugin.json", token)
                    if pj.get("encoding") == "base64":
                        import base64
                        content = json.loads(base64.b64decode(pj["content"]))
                        checks["plugin_name"] = content.get("name", "")
                        checks["plugin_description"] = content.get("description", "")
            except (urllib.error.URLError, json.JSONDecodeError):
                pass

        checks["has_skills"] = "skills" in root_names
        checks["has_commands"] = "commands" in root_names
        checks["has_agents"] = "agents" in root_names
        checks["has_hooks"] = "hooks" in root_names

    except (urllib.error.URLError, json.JSONDecodeError):
        return {"error": f"Could not access {repo_full_name}"}

    checks["is_valid_plugin"] = checks["has_plugin_json"]
    checks["trust_score"] = sum([
        checks["has_plugin_json"] * 3,
        checks["has_readme"] * 2,
        checks["has_license"] * 2,
        checks["has_skills"],
        checks["has_commands"],
        checks["has_agents"],
    ])

    return checks


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: github_search.py <command> [args]",
            "commands": "search <query> | discover | task <keyword1,keyword2> | verify <owner/repo>",
        }))
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "search":
            query = sys.argv[2] if len(sys.argv) > 2 else ""
            results = search_plugins(query)
            print(json.dumps({
                "query": query,
                "count": len(results),
                "results": results,
            }, ensure_ascii=False))

        elif command == "discover":
            results = search_plugins()
            print(json.dumps({
                "count": len(results),
                "results": results,
            }, ensure_ascii=False))

        elif command == "task":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Usage: task <keyword1,keyword2,...>"}))
                sys.exit(1)
            keywords = sys.argv[2].split(",")
            results = search_by_task(keywords)
            print(json.dumps({
                "keywords": keywords,
                "count": len(results),
                "results": results,
            }, ensure_ascii=False))

        elif command == "verify":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Usage: verify <owner/repo>"}))
                sys.exit(1)
            result = verify_plugin(sys.argv[2])
            print(json.dumps(result, ensure_ascii=False))

        else:
            print(json.dumps({"error": f"Unknown command: {command}"}))
            sys.exit(1)

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
