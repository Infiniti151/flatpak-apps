#!/usr/bin/env python3
"""
    SPDX-FileCopyrightText: 2026 Infiniti151
    SPDX-License-Identifier: GPL-3.0-or-later
    ---
    App Registry & Matrix Sync Utility

    Parses an application's RPM spec file (Name, Version, Summary, %global forgeurl, %global app_id)
    and queries forge APIs (GitHub, GitLab, Codeberg) to locate high-resolution app icons. Updates
    README.md and apps.json with alphabetically sorted entries while preserving formatting.

    Usage:
        python3 scripts/update_readme_matrix.py [-f|--force] <app_name> [<app_name> ...]

    Examples:
        python3 scripts/update_readme_matrix.py netpeek
        python3 scripts/update_readme_matrix.py netpeek identity chess-clock
        python3 scripts/update_readme_matrix.py --force netpeek
        python3 scripts/update_readme_matrix.py -f netpeek identity chess-clock
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

FORGE_LABELS = {"github": "GitHub", "gitlab": "GitLab", "codeberg": "Codeberg"}


class SpecError(Exception):
    """Raised when an app's spec file is missing or incomplete."""


def attr_escape(text):
    """Escape text for an HTML attribute inside a Markdown table cell."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("|", "&#124;")
    )


def format_alt(app_name):
    """identity -> Identity, chess-clock -> Chess-Clock."""
    return "-".join(word[:1].upper() + word[1:] for word in app_name.split("-"))


def format_title(summary):
    """Capitalise only the first letter of the spec Summary."""
    return summary[:1].upper() + summary[1:] if summary else ""


def parse_spec_file(spec_path):
    """Parses Name, Version, Summary, %global forgeurl, %global app_id, and URL from the spec file."""
    if not os.path.exists(spec_path):
        raise SpecError(f"Spec file not found at {spec_path}")

    metadata = {}
    with open(spec_path, "r", encoding="utf-8") as f:
        for line in f:
            cleaned_line = line.strip()
            if not cleaned_line or cleaned_line.startswith("#"):
                continue

            if cleaned_line.lower().startswith("%global "):
                parts = cleaned_line.split(None, 2)
                if len(parts) >= 2 and parts[1].lower() in ("forgeurl", "app_id"):
                    metadata[parts[1].upper()] = parts[2].strip() if len(parts) == 3 else ""
                    continue

            if ":" in cleaned_line:
                tag, value = cleaned_line.split(":", 1)
                tag = tag.strip().upper()
                value = value.strip()

                if tag == "SUMMARY":
                    metadata.setdefault("SUMMARY", value)
                elif tag in ("NAME", "VERSION", "URL"):
                    metadata[tag] = value

    if not all(k in metadata for k in ("NAME", "VERSION")):
        raise SpecError(f"Could not find all required tags in {spec_path}")

    url = metadata.get("FORGEURL") or metadata.get("URL", "")
    url = url.replace("%{name}", metadata["NAME"]).replace("%{version}", metadata["VERSION"])

    app_id = metadata.get("APP_ID", "")
    summary = metadata.get("SUMMARY", "").replace("%{name}", metadata["NAME"]).replace("%{version}", metadata["VERSION"])

    if not url:
        raise SpecError(f"Could not find a non-empty %global forgeurl or URL field in {spec_path}")

    return metadata["NAME"], metadata["VERSION"], url, app_id, summary

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

def score_icon(path, filename, icon_regex):
    """Scores a candidate icon path on a unified priority scale (-1 means ignore)."""
    filename_lower = filename.lower()
    path_lower = path.lower()

    if "symbolic" in filename_lower:
        return -1

    if not filename_lower.endswith((".svg", ".png")):
        return -1

    # Tier 1: Explicit name, repo, or app_id match
    if icon_regex.search(filename):
        if filename.startswith("page.codeberg"):
            return 10
        if "48x48" in path_lower or "/48/" in path_lower:
            return 9
        if "scalable" in path_lower:
            return 8
        if "hicolor" in path_lower:
            return 7
        return 6

    # Tier 2: Fallback icons inside an icons/ directory
    if "icons/" in path_lower:
        stem = filename_lower.rsplit(".", 1)[0]
        if re.search(r"\d", stem):
            if "48" in stem:
                return 3
            if filename_lower.endswith(".svg"):
                return 1
        elif filename_lower in ("app.svg", "app.png"):
            return 2
        elif filename_lower.endswith(".svg"):
            return 1

    return -1

def find_best_icon(tree_entries, icon_regex, platform, host, owner, repo, branch):
    best_url = None
    best_score = -1

    for entry in tree_entries:
        if entry.get("type") != "blob":
            continue

        path = entry.get("path", "")
        filename = path.split("/")[-1]
        score = score_icon(path, filename, icon_regex)

        if score > best_score:
            best_score = score
            best_url = build_raw_url(platform, host, owner, repo, branch, path)

        if best_score == 10:
            break

    return best_url

def get_fallback_icon(platform, host, owner, repo, branch, app_name):
    if platform == "gitlab":
        return f"https://{host}/{owner}/{repo}/-/raw/{branch}/data/icons/hicolor/scalable/apps/{app_name}.svg"
    if platform == "codeberg":
        return f"https://codeberg.org/{owner}/{repo}/raw/branch/{branch}/data/icons/page.codeberg.{owner}.{repo}.svg"
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/data/icons/hicolor/scalable/apps/{app_name}.svg"

def get_icon_url(url, app_name, app_id=""):
    """Scans repository tree using APIs to locate an application icon."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path_parts = [p for p in parsed.path.strip("/").split("/") if p]

    if len(path_parts) < 2:
        return None, "github", "", ""

    owner, repo = path_parts[0], path_parts[1]
    repo = re.sub(r"\.git$", "", repo)

    # Build candidate names: app_name, repo name, app_id, and last part of app_id
    candidates = {app_name, app_name.replace("-", "").replace("_", "").lower(), repo.lower()}
    if app_id:
        candidates.add(app_id.lower())
        candidates.add(app_id.split(".")[-1].lower())

    # Build regex matching any candidate as the full filename or preceding extension
    pattern = r"(^|\.)(" + "|".join(re.escape(c) for c in candidates) + r")\.(svg|png)$"
    icon_regex = re.compile(pattern, re.IGNORECASE)

    platform, branch, tree_entries, instance_host = get_platform_details(host, owner, repo)

    best_url = find_best_icon(tree_entries, icon_regex, platform, instance_host, owner, repo, branch)
    if not best_url:
        best_url = get_fallback_icon(platform, instance_host, owner, repo, branch, app_name)

    return best_url, platform, f"{owner}/{repo}", host

def build_markdown_entry(app_name, version, url, icon_url, app_id, summary, platform):
    """Builds one README table row."""
    alt = attr_escape(format_alt(app_name))
    title_text = format_title(summary)
    title_attr = f' title="{attr_escape(title_text)}"' if title_text else ""

    links = []
    if app_id:
        links.append(f"[Flathub](https://flathub.org/en/apps/{app_id})")
    links.append(f"[{FORGE_LABELS.get(platform, 'Source')}]({url})")

    copr_badge = f"[![COPR Status](https://copr.fedorainfracloud.org/coprs/infiniti151/flatpak-apps/package/{app_name}/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/infiniti151/flatpak-apps/package/{app_name}/)"
    return (
        f'| {app_name} | <p align="center"><img src="{icon_url}" width="48" alt="{alt}"{title_attr} '
        f'style="vertical-align:middle"></p> | {" • ".join(links)} | {version} | {copr_badge} |\n'
    )


def update_readme(readme_path, version, url, icon_url, app_name, app_id="", summary="", platform="github", force=False):
    """Step 1: Inserts or replaces a sorted application entry in README.md."""
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_lines = f.readlines()

    existing_entry_pattern = re.compile(r"^\|\s*" + re.escape(app_name) + r"\s*\|", re.IGNORECASE)

    existing_index = next(
        (index for index, line in enumerate(readme_lines) if existing_entry_pattern.match(line)),
        None,
    )

    markdown_entry = build_markdown_entry(app_name, version, url, icon_url, app_id, summary, platform)

    if existing_index is not None:
        if not force:
            print(f"{CYAN}[Step 1/2] Entry for '{app_name}' already exists in README.md. Skipping README update.{RESET}")
            return

        readme_lines[existing_index] = markdown_entry
        with open(readme_path, "w", encoding="utf-8") as f:
            f.writelines(readme_lines)

        print(f"{GREEN}[Step 1/2] Successfully updated entry for '{app_name}' (v{version}) in README.md.{RESET}")
        return

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

def update_matrix(apps_json_path, app_name, platform, upstream_repo, host, force=False):
    """Step 2: Inserts or replaces an apps.json entry, preserving alphabetical order."""
    with open(apps_json_path, "r", encoding="utf-8") as f:
        matrix = json.load(f)

    existing_index = next(
        (index for index, item in enumerate(matrix) if item.get("app_name") == app_name),
        None,
    )

    if existing_index is not None and not force:
        print(f"{CYAN}[Step 2/2] Matrix entry for '{app_name}' already exists in apps.json. Skipping matrix update.{RESET}")
        return

    new_entry = {
        "app_name": app_name,
        "upstream_repo": upstream_repo,
        "provider": platform,
        "instance": host if platform == "gitlab" else "",
    }

    if existing_index is None:
        matrix.append(new_entry)
    else:
        matrix[existing_index] = new_entry

    matrix.sort(key=lambda x: x.get("app_name", "").lower())

    with open(apps_json_path, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=4)
        f.write("\n")

    action = "updated" if existing_index is not None else "inserted"
    print(f"{GREEN}[Step 2/2] Successfully {action} sorted entry for '{app_name}' in apps.json.{RESET}")

def process_app(root_dir, app_name, force=False):
    """Runs both README and apps.json updates for a single app."""
    spec_path = os.path.join(root_dir, "apps", app_name, f"{app_name}.spec")
    readme_path = os.path.join(root_dir, "README.md")
    apps_json_path = os.path.join(root_dir, "apps.json")

    _, version, url, app_id, summary = parse_spec_file(spec_path)
    icon_url, platform, upstream_repo, host = get_icon_url(url, app_name, app_id)

    update_readme(readme_path, version, url, icon_url, app_name, app_id, summary, platform, force)
    update_matrix(apps_json_path, app_name, platform, upstream_repo, host, force)


def main():
    parser = argparse.ArgumentParser(description="Update app lists across README and matrix config seamlessly.")
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite existing entries in README.md and apps.json",
    )
    parser.add_argument("app_names", nargs="+", metavar="app_name",
                        help="One or more application directory names (space separated)")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)

    readme_path = os.path.join(root_dir, "README.md")
    apps_json_path = os.path.join(root_dir, "apps.json")

    if not os.path.exists(readme_path):
        print(f"Error: README.md not found at {readme_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(apps_json_path):
        print(f"Error: apps.json not found at {apps_json_path}", file=sys.stderr)
        sys.exit(1)

    app_names = list(dict.fromkeys(args.app_names))  # drop duplicates, keep order
    failed = []

    for app_name in app_names:
        if len(app_names) > 1:
            print(f"{CYAN}==> {app_name}{RESET}")
        try:
            process_app(root_dir, app_name, args.force)
        except SpecError as err:
            print(f"Error: {err}", file=sys.stderr)
            failed.append(app_name)

    if failed:
        print(f"Error: failed for: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()