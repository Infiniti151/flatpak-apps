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
    'dnf-plugins-core', 'rpm-build', 'rpmdevtools', 'rpmlint', 'git-core',
    'npm', 'sccache', 'ccache'
}

LINE_JOINER = " \\\n    "

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

def generate_dockerfile_block(app_deps, app_name, reset_mode):
    protected_list = sorted(PROTECTED_DEPS)

    if reset_mode:
        return LINE_JOINER.join(protected_list) + " \\"

    app_list = sorted(app_deps)
    block = LINE_JOINER.join(protected_list)

    if app_list:
        block += f" \\\n    # --- {app_name} dependencies --- \\\n    "
        block += LINE_JOINER.join(app_list)

    return block + " \\"

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

    start_match = re.search(r'dnf install -y\s+', content)
    end_match = re.search(r'&& dnf clean all', content)

    if not start_match or not end_match or start_match.end() > end_match.start():
        print(f"{RED}Error: Could not find valid dnf block bounds.{RESET}")
        sys.exit(1)

    prefix = content[:start_match.end()]
    suffix = "\n    " + content[end_match.start():]

    # 3. Format and Write Back
    formatted_block = generate_dockerfile_block(app_deps, app_name, reset_mode)
    new_content = f"{prefix}{formatted_block}{suffix}"

    with open(dockerfile_path, 'w') as f:
        f.write(new_content)

    if reset_mode:
        print(f"{CYAN}🧹 Success! Dockerfile reset to protected dependencies only.{RESET}")
    else:
        print(f"{GREEN}✅ Success! Dockerfile synced for {app_name}.{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync or reset app dependencies in the Dockerfile."
    )
    parser.add_argument("app_name", nargs="?", help="The name of the application to sync.")
    parser.add_argument("-r", "--reset", action="store_true", help="Reset the Dockerfile to only keep the protected dependencies.")

    args = parser.parse_args()

    if not args.reset and not args.app_name:
        parser.error(f"{RED}The following arguments are required: app_name (unless using -r/--reset){RESET}")

    update_dockerfile(args.app_name, reset_mode=args.reset)