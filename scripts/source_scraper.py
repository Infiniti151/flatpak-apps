#!/usr/bin/env python3
"""
    SPDX-FileCopyrightText: 2026 Infiniti151
    SPDX-License-Identifier: GPL-3.0-or-later
    ---
    External Source Scraper & Spec Updater Utility

    Fetches external dependency source URLs from JSON configuration files and updates spec file Source declarations.
    Process order:
      1. Fetch external configuration files (flatpak manifests, requirements files) across candidate branches/tags
      2. Recursively search JSON structures for target keywords to extract dependency source URLs
      3. Automatically update and sync SourceX lines in the RPM spec file

    Usage:
        source_scraper.py <provider> <instance> <repo> <version> <spec_path> <file_path> <keyword1> [keyword2 ...]
"""
import sys
import json
import urllib.request
import re

# ANSI Color Codes
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RED = "\033[1;31m"
RESET = "\033[0m"

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            return response.read().decode('utf-8')
    except Exception:
        return None

def search_json_for_url(data, keyword):
    """Recursively search JSON structures (dicts or lists) for a source URL containing the keyword."""
    if isinstance(data, dict):
        if 'url' in data and isinstance(data['url'], str) and keyword in data['url']:
            return data['url']
        for v in data.values():
            res = search_json_for_url(v, keyword)
            if res:
                return res
    elif isinstance(data, list):
        for item in data:
            res = search_json_for_url(item, keyword)
            if res:
                return res
    return None

def fetch_remote_json(provider, instance, repo, version, file_path):
    """Fetch and parse the external JSON configuration file across candidate references."""
    refs = list(dict.fromkeys([version, f"v{version}", "main", "master"]))
    base_url_templates = {
        "github": "https://raw.githubusercontent.com/{repo}/{ref}/{file_path}",
        "gitlab": f"https://{instance or 'gitlab.com'}/{{repo}}/-/raw/{{ref}}/{{file_path}}",
        "codeberg": "https://codeberg.org/{repo}/raw/branch/{ref}/{file_path}"
    }

    if provider not in base_url_templates:
        print(f"::error::==> [ERROR] Unsupported provider: {provider}")
        sys.exit(1)

    template = base_url_templates[provider]
    raw_data = None

    for ref in refs:
        url = template.format(repo=repo, ref=ref, file_path=file_path)
        raw_data = fetch_url(url)

        if not raw_data and provider == "codeberg":
            tag_url = f"https://codeberg.org/{repo}/raw/tag/{ref}/{file_path}"
            raw_data = fetch_url(tag_url)

        if raw_data:
            break

    if not raw_data:
        print(f"::error::==> [ERROR] Failed to fetch external source file '{file_path}' from {repo} (refs tried: {refs})")
        sys.exit(1)

    try:
        return json.loads(raw_data)
    except Exception as e:
        print(f"::error::==> [ERROR] Failed to parse JSON from {file_path}: {e}")
        sys.exit(1)

def process_spec_sources(spec_path, json_data, file_path, keywords):
    """Compare extracted source URLs with existing spec Source declarations and update if needed."""
    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            spec_content = f.read()
    except Exception as e:
        print(f"::error::==> [ERROR] Failed to read spec file {spec_path}: {e}")
        sys.exit(1)

    updated_spec = spec_content
    changes_made = False

    for idx, keyword in enumerate(keywords, start=1):
        source_url = search_json_for_url(json_data, keyword)
        if not source_url:
            print(f"::error::==> [ERROR] Could not find source URL for keyword '{keyword}' in {file_path}")
            sys.exit(1)

        print(f"{CYAN}==> [INFO] Found source URL for '{keyword}': {source_url}{RESET}")

        source_pattern = re.compile(rf"^(Source{idx}:\s+)(.*)$", re.MULTILINE)
        match = source_pattern.search(updated_spec)

        if match:
            current_url = match.group(2).strip()
            if current_url == source_url:
                print(f"{CYAN}==> [INFO] Source{idx} for '{keyword}' is already up to date.{RESET}")
                continue

            updated_spec = source_pattern.sub(f"Source{idx}:        {source_url}", updated_spec)
            changes_made = True
        else:
            print(f"::error::==> [ERROR] Source{idx} declaration not found in {spec_path}")
            sys.exit(1)

    if changes_made:
        try:
            with open(spec_path, 'w', encoding='utf-8') as f:
                f.write(updated_spec)
            print(f"{GREEN}==> [SUCCESS] Successfully updated external sources in {spec_path}{RESET}")
        except Exception as e:
            print(f"::error::==> [ERROR] Failed to write updated spec file {spec_path}: {e}")
            sys.exit(1)
    else:
        print(f"{CYAN}==> [INFO] All external sources in {spec_path} are already up to date. No changes made.{RESET}")

def main():
    if len(sys.argv) < 8:
        print("::error::==> [ERROR] Usage: source_scraper.py <provider> <instance> <repo> <version> <spec_path> <file_path> <keyword1> [keyword2 ...]")
        sys.exit(1)

    provider = sys.argv[1].lower()
    instance = sys.argv[2]
    repo = sys.argv[3]
    version = sys.argv[4]
    spec_path = sys.argv[5]
    file_path = sys.argv[6]
    keywords = sys.argv[7:]

    # Orchestrator / Aggregator flow
    json_data = fetch_remote_json(provider, instance, repo, version, file_path)
    process_spec_sources(spec_path, json_data, file_path, keywords)

    sys.exit(0)

if __name__ == "__main__":
    main()