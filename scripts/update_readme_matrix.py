#!/usr/bin/env python3
"""
    SPDX-FileCopyrightText: 2026 Infiniti151
    SPDX-License-Identifier: GPL-3.0-or-later
    ---
    App Registry & Matrix Sync Utility

    Parses an application's RPM spec file (Name, Version, %global forgeurl) and queries forge
    APIs (GitHub, GitLab, Codeberg) to locate high-resolution app icons. Updates
    README.md and apps.json with alphabetically sorted entries while preserving formatting.

    Usage:
        python3 scripts/update_readme_matrix.py <app_name>

    Example:
        python3 scripts/update_readme_matrix.py netpeek
"""
import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen

CYAN = "\033[36m"
GREEN = "\033[32m"
RESET = "\033[0m"

def parse_spec_file(spec_path):
    """Parses Name, Version, and %global forgeurl from the spec file reliably."""
    if not os.path.exists(spec_path):
        print(f"Error: Spec file not found at {spec_path}", file=sys.stderr)
        sys.exit(1)

    metadata = {}
    with open(spec_path, "r", encoding="utf-8") as f:
        for line in f:
            cleaned_line = line.strip()
            if not cleaned_line or cleaned_line.startswith("#"):
                continue

            # Handle %global forgeurl
            global_match = re.match(r"^%global\s+forgeurl\s+(\S+)$", cleaned_line, re.IGNORECASE)
            if global_match:
                metadata["FORGEURL"] = global_match.group(1).strip()
                continue

            # Skip other % lines
            if cleaned_line.startswith("%"):
                continue

            match = re.match(r"^(Name|Version)\s*:\s*(\S+)$", cleaned_line, re.IGNORECASE)
            if match:
                tag = match.group(1).upper()
                value = match.group(2).strip()
                metadata[tag] = value

    if not all(k in metadata for k in ["NAME", "VERSION", "FORGEURL"]):
        print(f"Error: Could not find all required tags (Name, Version, %global forgeurl) in {spec_path}", file=sys.stderr)
        sys.exit(1)

    url = metadata["FORGEURL"].replace("%{name}", metadata["NAME"]).replace("%{version}", metadata["VERSION"])
    return metadata["NAME"], metadata["VERSION"], url

def fetch_json(api_url):
    try:
        req = Request(api_url, headers={"User-Agent": "Flatpak2RPM-Tree-Scanner"})
        with urlopen(req, timeout=8) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None

def _fetch_github_platform(host, owner, repo):
    repo_data = fetch_json(f"https://api.github.com/repos/{owner}/{repo}")
    branch = repo_data.get("default_branch", "main") if repo_data else "main"
    tree_data = fetch_json(f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
    tree_entries = tree_data.get("tree", []) if tree_data else []
    return "github", branch, tree_entries, host

def _fetch_gitlab_platform(host, owner, repo):
    encoded_project = f"{owner}%2F{repo}"
    repo_data = fetch_json(f"https://{host}/api/v4/projects/{encoded_project}")
    branch = repo_data.get("default_branch", "main") if repo_data else "main"
    tree_data = fetch_json(f"https://{host}/api/v4/projects/{encoded_project}/repository/tree?recursive=true&per_page=100")
    tree_entries = tree_data if isinstance(tree_data, list) else []
    return "gitlab", branch, tree_entries, host

def _fetch_codeberg_platform(host, owner, repo):
    repo_data = fetch_json(f"https://codeberg.org/api/v1/repos/{owner}/{repo}")
    branch = repo_data.get("default_branch", "main") if repo_data else "main"
    tree_data = fetch_json(f"https://codeberg.org/api/v1/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
    tree_entries = tree_data.get("tree", []) if tree_data else []
    return "codeberg", branch, tree_entries, host

def get_platform_details(host, owner, repo):
    """Determine platform, branch, and tree entries using clean routing logic."""
    if host == "github.com" or host.endswith(".github.com"):
        return _fetch_github_platform(host, owner, repo)
    if "gitlab" in host or host == "gitlab.gnome.org":
        return _fetch_gitlab_platform(host, owner, repo)
    if host == "codeberg.org" or host.endswith(".codeberg.org"):
        return _fetch_codeberg_platform(host, owner, repo)
    return "github", "main", [], host

def build_raw_url(platform, host, owner, repo, branch, path):
    if platform == "github":
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    if platform == "gitlab":
        return f"https://{host}/{owner}/{repo}/-/raw/{branch}/{path}"
    if platform == "codeberg":
        return f"https://codeberg.org/{owner}/{repo}/raw/branch/{branch}/{path}"
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

def score_icon_path(path, filename):
    if "48x48" in path or "/48/" in path:
        return 3
    if "scalable" in path:
        return 2
    if "hicolor" in path:
        return 1
    if filename.startswith("page.codeberg") and not filename.endswith("-symbolic.svg"):
        return 4
    return 0

def find_best_icon(tree_entries, icon_regex, platform, host, owner, repo, branch):
    best_url = None
    best_score = -1

    for entry in tree_entries:
        if entry.get("type") != "blob":
            continue
        path = entry.get("path", "")
        filename = path.split("/")[-1]

        if not icon_regex.search(filename):
            continue

        score = score_icon_path(path, filename)
        if score > best_score:
            best_score = score
            best_url = build_raw_url(platform, host, owner, repo, branch, path)

        if best_score == 4:
            break

    return best_url

def get_fallback_icon(platform, host, owner, repo, branch, app_name):
    if platform == "gitlab":
        return f"https://{host}/{owner}/{repo}/-/raw/{branch}/data/icons/hicolor/scalable/apps/{app_name}.svg"
    if platform == "codeberg":
        return f"https://codeberg.org/{owner}/{repo}/raw/branch/{branch}/data/icons/page.codeberg.{owner}.{repo}.svg"
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/data/icons/hicolor/scalable/apps/{app_name}.svg"

def get_icon_url(url, app_name):
    """Scans repository tree using APIs to locate an application icon."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path_parts = [p for p in parsed.path.strip("/").split("/") if p]

    if len(path_parts) < 2:
        return None, "github", "", ""

    owner, repo = path_parts[0], path_parts[1]
    repo = re.sub(r"\.git$", "", repo)

    simplified_app_name = app_name.replace("-", "").replace("_", "").lower()
    icon_regex = re.compile(rf"(^|\.)({app_name}|{simplified_app_name}|{repo})\.(svg|png)$", re.IGNORECASE)

    platform, branch, tree_entries, instance_host = get_platform_details(host, owner, repo)

    best_url = find_best_icon(tree_entries, icon_regex, platform, instance_host, owner, repo, branch)
    if not best_url:
        best_url = get_fallback_icon(platform, instance_host, owner, repo, branch, app_name)

    return best_url, platform, f"{owner}/{repo}", host

def update_readme(readme_path, version, url, icon_url, app_name):
    """Step 1: Appends a sorted application entry in README.md if it doesn't exist."""
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_lines = f.readlines()

    existing_entry_pattern = re.compile(r"^\|\s*" + re.escape(app_name) + r"\s*\|", re.IGNORECASE)

    for line in readme_lines:
        if existing_entry_pattern.match(line):
            print(f"{CYAN}[Step 1/2] Entry for '{app_name}' already exists in README.md. Skipping README update.{RESET}")
            return

    copr_badge = f"[![COPR Status](https://copr.fedorainfracloud.org/coprs/infiniti151/flatpak-apps/package/{app_name}/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/infiniti151/flatpak-apps/package/{app_name}/)"
    parsed_url = urlparse(url)
    repo_display = parsed_url.path.strip("/")
    markdown_entry = f'| {app_name} | <p align="center"><img src="{icon_url}" width="48" style="vertical-align:middle"></p> | [{repo_display}]({url}) | {version} | {copr_badge} |\n'

    table_separator_pattern = re.compile(r"^\|(\s*:?-+:?\s*\|)+$")

    final_readme_lines = []
    matrix_rows = []
    in_matrix_block = False

    for line in readme_lines:
        stripped_line = line.strip()
        if table_separator_pattern.match(stripped_line):
            final_readme_lines.append(line)
            in_matrix_block = True
            continue

        if in_matrix_block:
            if stripped_line.startswith("|") and stripped_line.endswith("|"):
                matrix_rows.append(line)
            else:
                matrix_rows.append(markdown_entry)
                matrix_rows.sort(key=lambda x: x.split('|')[1].strip().lower())
                final_readme_lines.extend(matrix_rows)
                final_readme_lines.append(line)
                in_matrix_block = False
        else:
            final_readme_lines.append(line)

    if in_matrix_block:
        matrix_rows.append(markdown_entry)
        matrix_rows.sort(key=lambda x: x.split('|')[1].strip().lower())
        final_readme_lines.extend(matrix_rows)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(final_readme_lines)

    print(f"{GREEN}[Step 1/2] Successfully inserted sorted entry for '{app_name}' (v{version}) into README.md.{RESET}")

def update_matrix(apps_json_path, app_name, platform, upstream_repo, host):
    """Step 2: Updates apps.json matrix preserving style and alphabetical order."""
    with open(apps_json_path, "r", encoding="utf-8") as f:
        matrix = json.load(f)

    for item in matrix:
        if item.get("app_name") == app_name:
            print(f"{CYAN}[Step 2/2] Matrix entry for '{app_name}' already exists in apps.json. Skipping matrix update.{RESET}")
            return

    new_entry = {
        "app_name": app_name,
        "upstream_repo": upstream_repo,
        "provider": platform,
        "instance": host if platform == "gitlab" else "",
    }

    matrix.append(new_entry)
    matrix.sort(key=lambda x: x.get("app_name", "").lower())

    with open(apps_json_path, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=4)
        f.write("\n")

    print(f"{GREEN}[Step 2/2] Successfully inserted sorted entry for '{app_name}' into apps.json.{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Update app lists across README and matrix config seamlessly.")
    parser.add_argument("app_name", help="The name of the application directory")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)

    spec_path = os.path.join(root_dir, "apps", args.app_name, f"{args.app_name}.spec")
    readme_path = os.path.join(root_dir, "README.md")
    apps_json_path = os.path.join(root_dir, "apps.json")

    if not os.path.exists(readme_path):
        print(f"Error: README.md not found at {readme_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(apps_json_path):
        print(f"Error: apps.json not found at {apps_json_path}", file=sys.stderr)
        sys.exit(1)

    _, version, url = parse_spec_file(spec_path)
    icon_url, platform, upstream_repo, host = get_icon_url(url, args.app_name)

    update_readme(readme_path, version, url, icon_url, args.app_name)
    update_matrix(apps_json_path, args.app_name, platform, upstream_repo, host)

if __name__ == "__main__":
    main()