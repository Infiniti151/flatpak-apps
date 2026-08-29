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
    Changelog Scraper Utility

    Extracts release changelogs for RPM spec file automation.
    Priority order:
      1. AppStream Metainfo XML (.metainfo.xml / .appdata.xml)
      2. Forge Release API (GitHub / GitLab / Codeberg)
      3. Default fallback string ("- Update to <version>")

    Usage:
        changelog_scraper.py <provider> <instance> <repo> <app_id> <version>
"""
import sys
import re
import json
import urllib.request
import xml.etree.ElementTree as ET
import concurrent.futures

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=1.5) as response:
            return response.read().decode('utf-8')
    except Exception:
        return None

def fetch_and_parse(url, target_ver):
    content = fetch_url(url)
    if content:
        changelog = parse_appstream_xml(content, target_ver)
        if changelog:
            return changelog
    return None

def parse_appstream_xml(xml_content, target_ver):
    try:
        tree = ET.fromstring(xml_content)
        for release in tree.findall(".//release"):
            ver = release.get("version", "").strip()
            if ver == target_ver or ver == f"v{target_ver}":
                items = []
                for li in release.findall(".//li"):
                    text = "".join(li.itertext()).strip()
                    if text:
                        items.append(f"- {text}")
                if items:
                    return "\n".join(items)
    except Exception:
        pass
    return None

def generate_candidate_urls(provider, instance, repo, app_id):
    if not app_id:
        return []

    # 1. Use a set comprehension to generate unique names automatically
    names = list(dict.fromkeys([app_id, app_id.split('.')[-1].lower(), app_id.split('.')[-1]]))

    # 2. Build paths
    paths = []
    for name in names:
        paths.extend([
            f"data/{name}.metainfo.xml", f"data/{name}.metainfo.xml.in",
            f"data/{name}.appdata.xml", f"data/{name}.appdata.xml.in",
            f"data/{name}.appdata.xml.in.in", f"data/metainfo/{name}.metainfo.xml",
            f"data/appdata/{name}.appdata.xml"
        ])
    paths = list(dict.fromkeys(paths))

    # 3. Use dictionary routing for base URLs (eliminates if/elif blocks)
    base_urls = {
        "github": f"https://raw.githubusercontent.com/{repo}/{{branch}}/{{path}}",
        "gitlab": f"https://{instance}/{repo}/-/raw/{{branch}}/{{path}}",
        "codeberg": f"https://codeberg.org/{repo}/raw/branch/{{branch}}/{{path}}"
    }

    if provider not in base_urls:
        return []

    # 4. Use a flat list comprehension to build final URLs
    url_template = base_urls[provider]
    return [
        url_template.format(branch=branch, path=path)
        for branch in ("main", "master")
        for path in paths
    ]

def fetch_first_valid_changelog(urls, target_ver):
    chunk_size = 5
    for i in range(0, len(urls), chunk_size):
        chunk = urls[i:i + chunk_size]

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(chunk)) as executor:
            future_to_url = {executor.submit(fetch_and_parse, url, target_ver): url for url in chunk}

            for future in concurrent.futures.as_completed(future_to_url):
                result = future.result()
                if result:
                    executor.shutdown(wait=False, cancel_futures=True)
                    return result
    return None

def get_appstream_changelog(provider, instance, repo, app_id, target_ver):
    urls = generate_candidate_urls(provider, instance, repo, app_id)
    return fetch_first_valid_changelog(urls, target_ver) if urls else None

def get_api_changelog(provider, instance, repo):
    encoded_repo = urllib.parse.quote(repo, safe='')

    # 1. Configuration: Map providers to their endpoint and payload extraction logic
    api_config = {
        "github": (
            f"https://api.github.com/repos/{repo}/releases/latest",
            lambda data: data.get("body", "")
        ),
        "gitlab": (
            f"https://{instance}/api/v4/projects/{encoded_repo}/releases",
            lambda data: data[0].get("description", "") if isinstance(data, list) and data else ""
        ),
        "codeberg": (
            f"https://codeberg.org/api/v1/repos/{repo}/releases/latest",
            lambda data: data.get("body", "")
        )
    }

    if provider not in api_config:
        return None

    url, extract_body = api_config[provider]

    try:
        # 2. Execution: Unified fetching and JSON parsing
        raw = fetch_url(url)
        if not raw:
            return None

        body = extract_body(json.loads(raw))
        if not body:
            return None

        # 3. Formatting: Clean HTML/markdown tags
        clean_text = re.sub(r'<[^>]*>', '', body)
        clean_text = re.sub(r'^#*\s+', '', clean_text, flags=re.MULTILINE)
        lines = [re.sub(r'^\s*[-*•]\s*', '', l).strip() for l in clean_text.splitlines() if l.strip()]

        return "\n".join([f"- {l}" for l in lines]) if lines else None

    except Exception:
        return None

def main():
    if len(sys.argv) < 6:
        print("- Update to version")
        sys.exit(0)

    provider = sys.argv[1].lower()
    instance = sys.argv[2]
    repo = sys.argv[3]
    app_id = sys.argv[4]
    raw_ver = sys.argv[5]

    # Clean version string (v.0.3.1 -> 0.3.1)
    clean_ver = re.sub(r'^[vV]\.?', '', raw_ver)

    # 1. Try AppStream metainfo
    changelog = get_appstream_changelog(provider, instance, repo, app_id, clean_ver)

    # 2. Fall back to Release API
    if not changelog:
        changelog = get_api_changelog(provider, instance, repo)

    # 3. Ultimate fallback
    if not changelog:
        changelog = f"- Update to {clean_ver}"

    # Truncate if longer than 10 lines
    lines = changelog.splitlines()
    if len(lines) > 10:
        changelog = "\n".join(lines[:10]) + "\n- ... (see upstream for full release notes)"

    print(changelog)

if __name__ == "__main__":
    main()