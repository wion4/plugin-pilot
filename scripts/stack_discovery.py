#!/usr/bin/env python3
"""Auto-discover plugin stacks from GitHub — find repos that bundle multiple Claude Code plugins."""

import json
import os
import sys
import time
import urllib.request
import urllib.error

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DISCOVERED_STACKS_FILE = os.path.join(DATA_DIR, "discovered_stacks.json")
STACKS_CACHE_TTL = 3600 * 24  # 24 hours


def get_gh_token() -> str:
    try:
        import subprocess
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return ""


def github_api(endpoint: str, token: str = "") -> dict | list:
    url = f"https://api.github.com{endpoint}"
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "plugin-pilot"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def search_stacks(query: str = "", token: str = "") -> list[dict]:
    """Search GitHub for repos that look like plugin stacks/bundles."""
    if not token:
        token = get_gh_token()

    search_queries = [
        "claude code plugin stack godot game",
        "claude code skills bundle gamedev",
        "claude-code plugin collection workflow",
        "claude code plugin suite development",
    ]

    if query:
        search_queries = [f"claude code plugin {query}"]

    all_results = []
    seen = set()

    for sq in search_queries:
        try:
            encoded = urllib.request.quote(sq)
            data = github_api(
                f"/search/repositories?q={encoded}&sort=stars&per_page=15", token
            )
            for repo in data.get("items", []):
                full_name = repo["full_name"]
                if full_name in seen or repo.get("owner", {}).get("login") == "anthropics":
                    continue
                seen.add(full_name)

                all_results.append({
                    "name": repo["name"],
                    "full_name": full_name,
                    "description": repo.get("description", "") or "",
                    "url": repo["html_url"],
                    "stars": repo.get("stargazers_count", 0),
                    "updated_at": repo.get("updated_at", ""),
                    "topics": repo.get("topics", []),
                    "license": repo.get("license", {}).get("spdx_id", "") if repo.get("license") else "",
                })
        except (urllib.error.URLError, json.JSONDecodeError):
            continue
        time.sleep(0.5)

    all_results.sort(key=lambda x: x["stars"], reverse=True)
    return all_results


def analyze_repo_as_stack(repo_full_name: str, token: str = "") -> dict | None:
    """Analyze a GitHub repo to determine if it's a plugin stack and extract components."""
    if not token:
        token = get_gh_token()

    try:
        contents = github_api(f"/repos/{repo_full_name}/contents/", token)
        root_names = {item["name"] for item in contents}

        # Check if it's a multi-plugin or multi-skill repo
        has_skills = "skills" in root_names
        has_mcp = ".mcp.json" in root_names
        has_plugin_json = ".claude-plugin" in root_names

        # Count skills
        skill_count = 0
        skill_names = []
        if has_skills:
            try:
                skills_contents = github_api(f"/repos/{repo_full_name}/contents/skills", token)
                for item in skills_contents:
                    if item["type"] == "dir":
                        skill_count += 1
                        skill_names.append(item["name"])
            except (urllib.error.URLError, json.JSONDecodeError):
                pass

        # Count agents
        agent_count = 0
        if "agents" in root_names:
            try:
                agents_contents = github_api(f"/repos/{repo_full_name}/contents/agents", token)
                agent_count = sum(1 for item in agents_contents if item["name"].endswith(".md"))
            except (urllib.error.URLError, json.JSONDecodeError):
                pass

        # Count commands
        command_count = 0
        if "commands" in root_names:
            try:
                cmd_contents = github_api(f"/repos/{repo_full_name}/contents/commands", token)
                command_count = sum(1 for item in cmd_contents if item["name"].endswith(".md"))
            except (urllib.error.URLError, json.JSONDecodeError):
                pass

        # Read README for dependencies/requirements
        readme_text = ""
        for readme_name in ["README.md", "readme.md"]:
            if readme_name in root_names:
                try:
                    import base64
                    readme_data = github_api(f"/repos/{repo_full_name}/contents/{readme_name}", token)
                    if readme_data.get("encoding") == "base64":
                        readme_text = base64.b64decode(readme_data["content"]).decode("utf-8", errors="ignore")
                except (urllib.error.URLError, json.JSONDecodeError):
                    pass
                break

        # Get repo info
        repo_info = github_api(f"/repos/{repo_full_name}", token)

        # Determine if this qualifies as a "stack" (multiple components)
        total_components = skill_count + agent_count + command_count + (1 if has_mcp else 0)
        is_stack = total_components >= 3 or (skill_count >= 2 and has_mcp)

        # Extract mentions of other plugins/tools from README
        mentioned_tools = []
        tool_keywords = {
            "nano banana": "Image generation (Gemini)",
            "nano-banana": "Image generation (Gemini)",
            "godot": "Godot Engine",
            "godot-mcp": "Godot MCP bridge",
            "playwright": "Browser testing",
            "supabase": "Supabase backend",
            "firebase": "Firebase backend",
            "terraform": "Infrastructure as code",
        }
        readme_lower = readme_text.lower()
        for keyword, desc in tool_keywords.items():
            if keyword in readme_lower:
                mentioned_tools.append({"keyword": keyword, "description": desc})

        return {
            "full_name": repo_full_name,
            "name": repo_info.get("name", ""),
            "description": repo_info.get("description", "") or "",
            "url": repo_info.get("html_url", ""),
            "stars": repo_info.get("stargazers_count", 0),
            "license": repo_info.get("license", {}).get("spdx_id", "") if repo_info.get("license") else "",
            "is_valid_plugin": has_plugin_json,
            "is_stack": is_stack,
            "components": {
                "skills": skill_count,
                "skill_names": skill_names,
                "agents": agent_count,
                "commands": command_count,
                "has_mcp": has_mcp,
                "total": total_components,
            },
            "mentioned_tools": mentioned_tools,
            "install_cmd": f"github:{repo_full_name}",
        }

    except (urllib.error.URLError, json.JSONDecodeError) as e:
        return {"error": str(e), "full_name": repo_full_name}


def discover_stacks_for_task(task_keywords: list[str], token: str = "") -> list[dict]:
    """Find stacks relevant to a specific task."""
    if not token:
        token = get_gh_token()

    results = []
    for keyword in task_keywords:
        repos = search_stacks(keyword, token)
        for repo in repos[:5]:  # top 5 per keyword
            analysis = analyze_repo_as_stack(repo["full_name"], token)
            if analysis and not analysis.get("error") and analysis.get("is_valid_plugin"):
                results.append(analysis)
            time.sleep(0.3)

    # Deduplicate and sort
    seen = set()
    unique = []
    for r in results:
        if r["full_name"] not in seen:
            seen.add(r["full_name"])
            unique.append(r)
    unique.sort(key=lambda x: (x.get("is_stack", False), x.get("stars", 0)), reverse=True)
    return unique


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: stack_discovery.py <command> [args]",
            "commands": "search <query> | analyze <owner/repo> | task <keyword1,keyword2>",
        }))
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "search":
            query = sys.argv[2] if len(sys.argv) > 2 else ""
            results = search_stacks(query)
            print(json.dumps({"count": len(results), "results": results}, ensure_ascii=False))

        elif command == "analyze":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Usage: analyze <owner/repo>"}))
                sys.exit(1)
            result = analyze_repo_as_stack(sys.argv[2])
            print(json.dumps(result, ensure_ascii=False))

        elif command == "task":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Usage: task <keyword1,keyword2,...>"}))
                sys.exit(1)
            keywords = sys.argv[2].split(",")
            results = discover_stacks_for_task(keywords)
            print(json.dumps({"keywords": keywords, "count": len(results), "stacks": results}, ensure_ascii=False))

        else:
            print(json.dumps({"error": f"Unknown command: {command}"}))
            sys.exit(1)

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
