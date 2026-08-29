#!/usr/bin/env python3
"""
    Copyright (C) 2026  Infiniti151

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.

    ---
    App Registry & Matrix Sync Utility

    Parses an application's RPM spec file (Name, Version, URL) and queries forge
    APIs (GitHub, GitLab, Codeberg) to locate high-resolution app icons. Updates
    README.md and .github/workflows/copr-build.yml with alphabetically sorted
    entries while preserving formatting.

    Usage:
        python3 scripts/update_app_list.py <app_name>

    Example:
        python3 scripts/update_app_list.py netpeek
"""
import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from ruamel.yaml import YAML

CYAN = "\033[36m"
GREEN = "\033[32m"
RESET = "\033[0m"

def parse_spec_file(spec_path):
    """Parses Name, Version, and URL from the spec file reliably."""
    if not os.path.exists(spec_path):
        print(f"Error: Spec file not found at {spec_path}", file=sys.stderr)
        sys.exit(1)

    metadata = {}
    with open(spec_path, "r", encoding="utf-8") as f:
        for line in f:
            cleaned_line = line.strip()
            if not cleaned_line or cleaned_line.startswith(("%", "#")):
                continue

            match = re.match(r"^(Name|Version|URL)\s*:\s*(.+)$", cleaned_line, re.IGNORECASE)
            if match:
                tag = match.group(1).upper()
                value = match.group(2).strip()
                metadata[tag] = value

    if not all(k in metadata for k in ["NAME", "VERSION", "URL"]):
        print(f"Error: Could not find all required tags (Name, Version, URL) in {spec_path}", file=sys.stderr)
        sys.exit(1)

    url = metadata["URL"].replace("%{name}", metadata["NAME"]).replace("%{version}", metadata["VERSION"])
    return metadata["NAME"], metadata["VERSION"], url

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

    def fetch_json(api_url):
        try:
            req = Request(api_url, headers={"User-Agent": "Flatpak2RPM-Tree-Scanner"})
            with urlopen(req, timeout=8) as response:
                return json.loads(response.read().decode())
        except Exception:
            return None

    branch = "main"
    tree_entries = []
    platform = "github"

    if host == "github.com" or host.endswith(".github.com"):
        platform = "github"
        repo_data = fetch_json(f"https://api.github.com/repos/{owner}/{repo}")
        branch = repo_data.get("default_branch", "main") if repo_data else "main"
        tree_data = fetch_json(f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
        if tree_data and "tree" in tree_data:
            tree_entries = tree_data["tree"]

    elif host == "gitlab.com" or host.endswith(".gitlab.com"):
        platform = "gitlab"
        instance = host
        encoded_project = f"{owner}%2F{repo}"
        repo_data = fetch_json(f"https://{instance}/api/v4/projects/{encoded_project}")
        branch = repo_data.get("default_branch", "main") if repo_data else "main"
        tree_data = fetch_json(f"https://{instance}/api/v4/projects/{encoded_project}/repository/tree?recursive=true&per_page=100")
        if isinstance(tree_data, list):
            tree_entries = tree_data

    elif host == "codeberg.org" or host.endswith(".codeberg.org"):
        platform = "codeberg"
        repo_data = fetch_json(f"https://codeberg.org/api/v1/repos/{owner}/{repo}")
        branch = repo_data.get("default_branch", "main") if repo_data else "main"
        tree_data = fetch_json(f"https://codeberg.org/api/v1/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
        if tree_data and "tree" in tree_data:
            tree_entries = tree_data["tree"]

    best_url = None
    best_score = -1

    for entry in tree_entries:
        if entry.get("type") != "blob":
            continue
        path = entry.get("path", "")
        filename = path.split("/")[-1]

        if icon_regex.search(filename):
            if platform == "github":
                current_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
            elif platform == "gitlab":
                current_url = f"https://{instance}/{owner}/{repo}/-/raw/{branch}/{path}"
            elif platform == "codeberg":
                current_url = f"https://codeberg.org/{owner}/{repo}/raw/branch/{branch}/{path}"
            else:
                continue

            current_score = 0
            if "48x48" in path or "/48/" in path:
                current_score = 3
            elif "scalable" in path:
                current_score = 2
            elif "hicolor" in path:
                current_score = 1
            elif filename.startswith("page.codeberg") and not filename.endswith("-symbolic.svg"):
                current_score = 4

            if current_score > best_score:
                best_score = current_score
                best_url = current_url
            if best_score == 4:
                break

    if not best_url:
        if platform == "gitlab":
            best_url = f"https://{host}/{owner}/{repo}/-/raw/{branch}/data/icons/hicolor/scalable/apps/{app_name}.svg"
        elif platform == "codeberg":
            best_url = f"https://codeberg.org/{owner}/{repo}/raw/branch/{branch}/data/icons/page.codeberg.{owner}.{repo}.svg"
        else:
            best_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/data/icons/hicolor/scalable/apps/{app_name}.svg"

    return best_url, platform, f"{owner}/{repo}", host

def update_readme(readme_path, name, version, url, icon_url, app_name):
    """Step 1: Appends a sorted application entry in README.md if it doesn't exist."""
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_lines = f.readlines()

    existing_entry_pattern = re.compile(r"^\|\s*" + re.escape(name) + r"\s*\|", re.IGNORECASE)

    for line in readme_lines:
        if existing_entry_pattern.match(line):
            print(f"{CYAN}[Step 1/2] Entry for '{name}' already exists in README.md. Skipping README update.{RESET}")
            return

    copr_badge = f"[![COPR Status](https://copr.fedorainfracloud.org/coprs/infiniti151/flatpak-apps/package/{app_name}/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/infiniti151/flatpak-apps/package/{app_name}/)"
    parsed_url = urlparse(url)
    repo_display = parsed_url.path.strip("/")
    markdown_entry = f'| {name} | <p align="center"><img src="{icon_url}" width="48" style="vertical-align:middle"></p> | [{repo_display}]({url}) | {version} | {copr_badge} |\n'

    table_row_pattern = re.compile(r"^\|\s*[^: ]+.*\|$")
    table_separator_pattern = re.compile(r"^\|(\s*:?-+:?\s*\|)+$")

    final_readme_lines = []
    matrix_rows = []
    in_matrix_block = False

    for line in readme_lines:
        if table_separator_pattern.match(line.strip()):
            final_readme_lines.append(line)
            in_matrix_block = True
            continue

        if in_matrix_block:
            if table_row_pattern.match(line.strip()):
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

    print(f"{GREEN}[Step 1/2] Successfully inserted sorted entry for '{name}' (v{version}) into README.md.{RESET}")

def update_workflow(workflow_path, app_name, platform, upstream_repo, host):
    """Step 2: Updates copr-build.yml build matrix preserving style and layout."""
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow_data = yaml.load(f)

    try:
        matrix_include = workflow_data['jobs']['check-and-build']['strategy']['matrix']['include']
    except KeyError:
        print(f"Error: Could not trace target path 'jobs.check-and-build.strategy.matrix.include' in {workflow_path}", file=sys.stderr)
        sys.exit(1)

    for item in matrix_include:
        if item.get('app_name') == app_name:
            print(f"{CYAN}[Step 2/2] Matrix entry for '{app_name}' already exists in workflow. Skipping workflow update.{RESET}")
            return

    new_entry = {
        'app_name': app_name,
        'upstream_repo': upstream_repo,
        'provider': platform
    }
    if platform == "gitlab":
        new_entry['instance'] = host

    matrix_include.append(new_entry)

    matrix_include.sort(key=lambda x: x.get('app_name', '').lower())

    with open(workflow_path, 'w', encoding='utf-8') as f:
        yaml.dump(workflow_data, f)

    print(f"{GREEN}[Step 2/2] Successfully inserted sorted entry for '{app_name}' into copr-build workflow matrix.{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Update app lists across README and CI configs seamlessly.")
    parser.add_argument("app_name", help="The name of the application directory")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)

    spec_path = os.path.join(root_dir, "apps", args.app_name, f"{args.app_name}.spec")
    readme_path = os.path.join(root_dir, "README.md")
    workflow_path = os.path.join(root_dir, ".github", "workflows", "copr-build.yml")

    if not os.path.exists(readme_path):
        print(f"Error: README.md not found at {readme_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(workflow_path):
        print(f"Error: Workflow config not found at {workflow_path}", file=sys.stderr)
        sys.exit(1)

    name, version, url = parse_spec_file(spec_path)
    icon_url, platform, upstream_repo, host = get_icon_url(url, args.app_name)

    update_readme(readme_path, name, version, url, icon_url, args.app_name)
    update_workflow(workflow_path, args.app_name, platform, upstream_repo, host)

if __name__ == "__main__":
    main()