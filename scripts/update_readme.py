#!/usr/bin/env python3
import argparse
import os
import re
import sys
from urllib.parse import urlparse

def parse_spec_file(spec_path, app_name):
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
        print(f"Parsed metadata found so far: {metadata}", file=sys.stderr)
        sys.exit(1)

    url = metadata["URL"]
    url = url.replace("%{name}", metadata["NAME"]).replace("%{version}", metadata["VERSION"])

    return metadata["NAME"], metadata["VERSION"], url

def get_icon_url(url, app_name):
    """Generates the structured icon asset URL based on the upstream host."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path_parts = [p for p in parsed.path.strip("/").split("/") if p]

    if len(path_parts) < 2:
        return f"https://raw.githubusercontent.com/{parsed.path.strip('/')}/main/data/icons/hicolor/scalable/apps/{app_name}.svg"

    owner = path_parts[0]
    repo = path_parts[1]

    if "github.com" in host:
        return f"https://raw.githubusercontent.com/{owner}/{repo}/main/data/icons/hicolor/scalable/apps/{app_name}.svg"
    elif "gitlab.com" in host:
        return f"https://gitlab.com/{owner}/{repo}/-/raw/main/data/icons/hicolor/scalable/apps/{app_name}.svg"
    elif "codeberg.org" in host:
        return f"https://codeberg.org/{owner}/{repo}/raw/branch/main/data/icons/hicolor/scalable/apps/{app_name}.svg"
    else:
        return f"{url.rstrip('/')}/raw/main/{app_name}.svg"

def main():
    parser = argparse.ArgumentParser(description="Add or update an app entry into the project README matrix.")
    parser.add_argument("app_name", help="The name of the application directory")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)

    spec_path = os.path.join(root_dir, "apps", args.app_name, f"{args.app_name}.spec")
    readme_path = os.path.join(root_dir, "README.md")

    if not os.path.exists(readme_path):
        print(f"Error: README.md not found at {readme_path}", file=sys.stderr)
        sys.exit(1)

    name, version, url = parse_spec_file(spec_path, args.app_name)

    parsed_url = urlparse(url)
    repo_display = parsed_url.path.strip("/")

    icon_url = get_icon_url(url, args.app_name)
    copr_badge = f"[![COPR Status](https://copr.fedorainfracloud.org/coprs/infiniti151/flatpak-apps/package/{args.app_name}/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/infiniti151/flatpak-apps/package/{args.app_name}/)"

    markdown_entry = f'| {name} | <p align="center"><img src="{icon_url}" width="48" style="vertical-align:middle"></p> | [{repo_display}]({url}) | {version} | {copr_badge} |\n'

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_lines = f.readlines()

    existing_entry_pattern = re.compile(r"^\|\s*" + re.escape(name) + r"\s*\|", re.IGNORECASE)

    entry_exists = False
    new_readme_lines = []

    for line in readme_lines:
        if existing_entry_pattern.match(line):
            new_readme_lines.append(markdown_entry)
            entry_exists = True
        else:
            new_readme_lines.append(line)

    if not entry_exists:
        final_readme_lines = []
        target_found = False

        for line in new_readme_lines:
            if "> [!WARNING]" in line and not target_found:
                while final_readme_lines and not final_readme_lines[-1].strip():
                    final_readme_lines.pop()

                final_readme_lines.append(markdown_entry)
                final_readme_lines.append("\n")
                target_found = True
            final_readme_lines.append(line)

        if not target_found:
            final_readme_lines.append("\n" + markdown_entry)
        new_readme_lines = final_readme_lines

    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(new_readme_lines)

    if entry_exists:
        print(f"Successfully updated existing entry for '{name}' to v{version} in README.md!")
    else:
        print(f"Successfully added new entry for '{name}' (v{version}) into README.md!")

if __name__ == "__main__":
    main()