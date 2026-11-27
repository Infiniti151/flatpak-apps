#!/usr/bin/env python3
"""
    SPDX-FileCopyrightText: 2026 Infiniti151
    SPDX-License-Identifier: GPL-3.0-or-later
    ---
    AppStream Version & Changelog Scraper Utility

    Extracts release version or changelogs for RPM spec file automation.
    Priority order:
      1. AppStream Metainfo XML (.metainfo.xml / .appdata.xml); for changelogs it is
         read at the exact tag passed in, for versions from main/master
      2. Flathub API (for version resolution) / Forge Release API (for changelogs)
      3. Default fallback string ("- Update to <version>")

    Usage:
        changelog_scraper.py get-version <provider> <instance> <repo> <app_id>
        changelog_scraper.py get-changelog <provider> <instance> <repo> <app_id> <version>
        changelog_scraper.py <provider> <instance> <repo> <app_id> <version> (Legacy fallback)
"""
import os
import sys
import re
import json
import subprocess
import tempfile
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import concurrent.futures

GIT_ONLY_HOSTS = {"gitlab.gnome.org"}

METAINFO_PATTERN = re.compile(
    r"(^|/).*\.(?:metainfo|appdata)\.xml(?:\.in(?:\.in)?)?$",
    re.IGNORECASE,
)

METAINFO_EXTS = [
    ".metainfo.xml",
    ".metainfo.xml.in",
    ".metainfo.xml.in.in",
    ".appdata.xml",
    ".appdata.xml.in",
    ".appdata.xml.in.in",
]

METAINFO_DIRS = ["", "data/", "data/metainfo/", "data/appdata/"]

def fetch_url(url, timeout=1.5):
    headers = {'User-Agent': 'Mozilla/5.0'}
    token = os.environ.get("GITHUB_TOKEN")
    if token and urllib.parse.urlparse(url).hostname == "api.github.com":
        headers['Authorization'] = f"Bearer {token}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8')
    except Exception:
        return None

def parse_appstream_changelog(xml_content, target_ver):
    try:
        tree = ET.fromstring(xml_content)
        for release in tree.findall(".//release"):
            ver = release.get("version", "").strip()
            if ver == target_ver or ver == f"v{target_ver}":
                items = []
                for elem in release.iter():
                    if elem.tag in ("p", "li"):
                        text = "".join(elem.itertext()).strip()
                        if text:
                            items.append(f"- {text}")
                if items:
                    return "\n".join(items)
    except Exception:
        pass
    return None

def parse_appstream_version(xml_content):
    try:
        tree = ET.fromstring(xml_content)
        release = tree.find(".//release")
        if release is not None:
            ver = release.get("version", "").strip()
            if ver:
                return ver
    except Exception:
        pass
    return None

def find_metainfo_paths_in_git(files):
    # Prioritize paths matching candidate_paths order first, then any other matching file
    matched = [p for p in files if METAINFO_PATTERN.search(p)]
    return sorted(matched, key=lambda p: (0 if "/" not in p or p.startswith("data/") else 1, p))

def fetch_via_git(provider, instance, repo, app_id, mode, target_ver=None, ref=None):
    if not app_id:
        return None
    host = {"github": "github.com", "codeberg": "codeberg.org"}.get(provider, instance)
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    with tempfile.TemporaryDirectory() as tmp:
        def git(*args):
            return subprocess.run(["git", "-C", tmp, *args], capture_output=True,
                                  text=True, timeout=60, env=env)
        try:
            clone = subprocess.run(
                ["git", "clone", "--depth", "1", "--filter=blob:none", "--no-checkout",
                 *(["--branch", ref] if ref else []),
                 f"https://{host}/{repo}.git", tmp],
                capture_output=True, timeout=60, env=env)
            if clone.returncode != 0:
                return None
            ls = git("ls-tree", "-r", "--name-only", "HEAD")
            if ls.returncode != 0:
                return None
            files = set(ls.stdout.splitlines())
            for path in find_metainfo_paths_in_git(files):
                if path in files:
                    content = git("show", f"HEAD:{path}").stdout
                    if mode == "get-version":
                        result = parse_appstream_version(content)
                    else:
                        result = parse_appstream_changelog(content, target_ver)
                    if result:
                        return result
        except Exception:
            pass
    return None

def fetch_and_parse(url, mode, target_ver=None):
    content = fetch_url(url)
    if content:
        if mode == "get-changelog":
            return parse_appstream_changelog(content, target_ver)
        elif mode == "get-version":
            return parse_appstream_version(content)
    return None

def candidate_paths(app_id, repo=""):
    app_short = app_id.split(".")[-1] if app_id else ""
    repo_short = repo.split("/")[-1] if repo else ""
    names = list(
        dict.fromkeys(
            [
                n
                for n in [
                    app_id,
                    app_short.lower(),
                    app_short,
                    repo_short.lower(),
                    repo_short,
                    "app",
                ]
                if n
            ]
        )
    )

    paths = []
    for name in names:
        for directory in METAINFO_DIRS:
            for ext in METAINFO_EXTS:
                paths.append(f"{directory}{name}{ext}")
    return list(dict.fromkeys(paths))


def raw_url(provider, instance, repo, ref, path, ref_type="branch"):
    """Raw-file URL for one path at a ref (branch or tag)."""
    if provider == "github":
        return f"https://raw.githubusercontent.com/{repo}/{ref}/{path}"
    if provider == "gitlab":
        return f"https://{instance}/{repo}/-/raw/{ref}/{path}"
    if provider == "codeberg":
        return f"https://codeberg.org/{repo}/raw/{ref_type}/{ref}/{path}"
    return None


def generate_candidate_urls(provider, instance, repo, app_id,
                            refs=("main", "master"), ref_type="branch"):
    """Build raw-file URLs for every candidate metainfo path.

    refs:     git refs to try (branches by default, or an exact tag)
    ref_type: "branch" or "tag" (only Codeberg/Gitea encodes this in the URL)
    """
    if not app_id or provider not in ("github", "gitlab", "codeberg"):
        return []

    paths = candidate_paths(app_id, repo)
    return [
        raw_url(provider, instance, repo, ref, path, ref_type)
        for ref in refs
        for path in paths
    ]


def list_tree_via_api(provider, repo, ref):
    """List every file path at a ref with ONE API call (GitHub/Codeberg only)."""
    quoted = urllib.parse.quote(ref, safe="")
    if provider == "github":
        url = f"https://api.github.com/repos/{repo}/git/trees/{quoted}?recursive=1"
    elif provider == "codeberg":
        url = f"https://codeberg.org/api/v1/repos/{repo}/git/trees/{quoted}?recursive=true&per_page=10000"
    else:
        return None
    raw = fetch_url(url, timeout=8)
    if not raw:
        return None
    try:
        tree = json.loads(raw).get("tree") or []
        return {e["path"] for e in tree if e.get("type") == "blob" and "path" in e}
    except Exception:
        return None


def fetch_via_tree(provider, instance, repo, mode, ref, ref_type, target_ver=None):
    """Find the metainfo in the repo's file list instead of guessing ~100 names."""
    files = list_tree_via_api(provider, repo, ref)
    if not files:
        return None
    paths = find_metainfo_paths_in_git(files)[:12]
    urls = [raw_url(provider, instance, repo, ref, p, ref_type) for p in paths]
    return fetch_first_valid_match(urls, mode, target_ver)


def fetch_first_valid_match(urls, mode, target_ver=None, workers=16):
    if not urls:
        return None
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=min(workers, len(urls)))
    try:
        futures = [executor.submit(fetch_and_parse, url, mode, target_ver) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                return result
    finally:
        executor.shutdown(wait=False, cancel_futures=True)
    return None

def get_api_changelog(provider, instance, repo, target_ver):
    encoded_repo = urllib.parse.quote(repo, safe='')

    api_config = {
        "github": (
            f"https://api.github.com/repos/{repo}/releases/latest",
            lambda data: (data.get("tag_name", "") or data.get("name", ""), data.get("body", ""))
        ),
        "gitlab": (
            f"https://{instance}/api/v4/projects/{encoded_repo}/releases",
            lambda data: (data[0].get("tag_name", "") or data[0].get("name", ""), data[0].get("description", "")) if isinstance(data, list) and data else ("", "")
        ),
        "codeberg": (
            f"https://codeberg.org/api/v1/repos/{repo}/releases/latest",
            lambda data: (data.get("tag_name", "") or data.get("name", ""), data.get("body", ""))
        )
    }

    if provider not in api_config:
        return None

    url, extract_info = api_config[provider]

    try:
        raw = fetch_url(url, timeout=8)
        if not raw:
            return None

        tag_name, body = extract_info(json.loads(raw))
        if not tag_name or not body:
            return None

        # Confirm the forge's latest release tag corresponds to the requested version
        clean_tag = re.sub(r'^[vV]\.?', '', tag_name).strip()
        if clean_tag != target_ver:
            return None

        clean_text = re.sub(r'<[^>]*>', '', body)
        clean_text = re.sub(r'^#*\s+', '', clean_text, flags=re.MULTILINE)
        lines = [re.sub(r'^\s*[-*•]\s*', '', l).strip() for l in clean_text.splitlines() if l.strip()]
        return "\n".join([f"- {l}" for l in lines]) if lines else None
    except Exception:
        return None

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    first_arg = sys.argv[1].lower()

    if first_arg == "get-version":
        if len(sys.argv) < 6:
            sys.exit(1)

        provider, instance, repo, app_id = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

        version = None

        # 1. PRIMARY: Flathub Appstream API
        try:
            raw = fetch_url(f"https://flathub.org/api/v2/appstream/{app_id}", timeout=8)
            if raw:
                data = json.loads(raw)
                releases = data.get("releases", [])
                if releases:
                    version = releases[0].get("version", "").strip()
        except Exception:
            pass

        git_only = instance in GIT_ONLY_HOSTS

        # 2. SECONDARY: AppStream XML from upstream repo
        if not version and not git_only:
            urls = generate_candidate_urls(provider, instance, repo, app_id)
            if urls:
                version = fetch_first_valid_match(urls, "get-version")

        if not version and git_only:
            version = fetch_via_git(provider, instance, repo, app_id, "get-version")

        if version:
            print(version)

        sys.exit(0)

    elif first_arg == "get-changelog" or len(sys.argv) >= 6:
        if first_arg == "get-changelog":
            if len(sys.argv) < 7:
                sys.exit(0)
            provider, instance, repo, app_id, raw_ver = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
        else:
            # Legacy command interface support
            provider, instance, repo, app_id, raw_ver = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

        clean_ver = re.sub(r'^[vV]\.?', '', raw_ver)

        git_only = instance in GIT_ONLY_HOSTS

        changelog = None
        if git_only:
            changelog = fetch_via_git(provider, instance, repo, app_id, "get-changelog", clean_ver, ref=raw_ver)
        else:
            changelog = fetch_via_tree(provider, instance, repo, "get-changelog",
                                       raw_ver, "tag", clean_ver)
            if not changelog:
                urls = generate_candidate_urls(provider, instance, repo, app_id,
                                               refs=(raw_ver,), ref_type="tag")
                changelog = fetch_first_valid_match(urls, "get-changelog", clean_ver)
            if not changelog:
                changelog = get_api_changelog(provider, instance, repo, clean_ver)
        if not changelog:
            changelog = f"- Update to {clean_ver}"

        lines = changelog.splitlines()
        if len(lines) > 10:
            changelog = "\n".join(lines[:10]) + "\n- ... (see upstream for full release notes)"

        print(changelog)
        sys.exit(0)

if __name__ == "__main__":
    main()