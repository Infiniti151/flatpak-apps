#!/usr/bin/env python3
"""
    SPDX-FileCopyrightText: 2026 Infiniti151
    SPDX-License-Identifier: GPL-3.0-or-later
    ---
    Dockerfile Dependency Sync & Reset Utility

    Parses 'BuildRequires' lines from an app's RPM spec file and injects
    them into the root 'Dockerfile' dnf installation block. Also supports
    resetting the Dockerfile back to base foundation packages.

    Usage:
        python3 scripts/update_dockerfile.py <app_name>
        python3 scripts/update_dockerfile.py -r

    Examples:
        python3 scripts/update_dockerfile.py netpeek
        python3 scripts/update_dockerfile.py --reset
"""
import re
import sys
import os
import argparse

CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

PROTECTED_DEPS = {
    'dnf-plugins-core', 'rpm-build', 'rpmdevtools', 'rpmlint',
    'npm', 'sccache', 'ccache', 'glibc-langpack-en'
}

LINE_JOINER = " \\\n    "
BLOCK_PATTERN = re.compile(
    r'(# --- APP_DEPS_START ---\n)(.*?)(# --- APP_DEPS_END ---)',
    re.DOTALL
)


def extract_spec_dependencies(spec_path):
    if not os.path.exists(spec_path):
        print(f"{RED}Error: {spec_path} not found.{RESET}")
        sys.exit(1)

    app_deps = set()
    with open(spec_path, 'r') as f:
        for line in f:
            match = re.match(r'^\s*BuildRequires:\s+(.+)', line, re.IGNORECASE)
            if match:
                dep = match.group(1).split('>=')[0].split('>')[0].split('=')[0].strip()
                if '(' in dep:
                    dep = f"'{dep}'"

                if dep not in PROTECTED_DEPS and dep != 'nodejs':
                    app_deps.add(dep)
    return app_deps


def generate_layer3_block(app_deps, app_name, reset_mode):
    if reset_mode or not app_deps:
        return ""

    app_list = sorted(app_deps)
    pkg_lines = LINE_JOINER.join(app_list)

    return (
        "RUN dnf install -y \\\n"
        f"    # --- {app_name} dependencies --- \\\n"
        f"    {pkg_lines} && \\\n"
        "    dnf clean all && \\\n"
        "    rm -rf /var/cache/dnf/*\n"
    )


def update_dockerfile(app_name, reset_mode=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    dockerfile_path = os.path.join(project_root, "Dockerfile")

    # 1. Gather Dependencies
    app_deps = set()
    if not reset_mode:
        spec_path = os.path.join(project_root, "apps", app_name, f"{app_name}.spec")
        app_deps = extract_spec_dependencies(spec_path)

    # 2. Read Dockerfile
    if not os.path.exists(dockerfile_path):
        print(f"{RED}Error: {dockerfile_path} not found.{RESET}")
        sys.exit(1)

    with open(dockerfile_path, 'r') as f:
        content = f.read()

    if not BLOCK_PATTERN.search(content):
        print(f"{RED}Error: Could not find APP_DEPS_START / APP_DEPS_END markers.{RESET}")
        sys.exit(1)

    # 3. Format and Write Back
    layer3_body = generate_layer3_block(app_deps, app_name, reset_mode)
    new_content = BLOCK_PATTERN.sub(rf"\g<1>{layer3_body}\g<3>", content, count=1)

    with open(dockerfile_path, 'w') as f:
        f.write(new_content)

    if reset_mode:
        print(f"{CYAN}🧹 Success! Cleared APP_DEPS block in Dockerfile.{RESET}")
    else:
        print(f"{GREEN}✅ Success! Dockerfile synced for {app_name}.{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync or reset app dependencies in Layer 3 of the Dockerfile."
    )
    parser.add_argument("app_name", nargs="?", help="The name of the application to sync.")
    parser.add_argument("-r", "--reset", action="store_true", help="Remove everything inside the APP_DEPS block.")

    args = parser.parse_args()

    if not args.reset and not args.app_name:
        parser.error(f"{RED}The following arguments are required: app_name (unless using -r/--reset){RESET}")

    update_dockerfile(args.app_name, reset_mode=args.reset)