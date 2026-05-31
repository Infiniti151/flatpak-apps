#!/usr/bin/env python3
import re
import sys
import os
import argparse

CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

# Foundation tools.
PROTECTED_DEPS = {
    'dnf-plugins-core', 'rpm-build', 'rpmdevtools', 'rpmlint', 'git-core',
    'npm', 'sccache', 'ccache'
}

def update_dockerfile(app_name, reset_mode=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    dockerfile_path = os.path.join(project_root, "Dockerfile")
    app_deps = set()

    if not reset_mode:
        spec_path = os.path.join(project_root, "apps", app_name, f"{app_name}.spec")
        if not os.path.exists(spec_path):
            print(f"Error: {spec_path} not found.")
            sys.exit(1)

        # 1. Extract BuildRequires from Spec
        with open(spec_path, 'r') as f:
            for line in f:
                match = re.match(r'^\s*BuildRequires:\s+(.+)', line, re.IGNORECASE)
                if match:
                    dep = match.group(1).split('>=')[0].split('>')[0].split('=')[0].strip()
                    if '(' in dep:
                        dep = f"'{dep}'"

                    if dep not in PROTECTED_DEPS and dep != 'nodejs':
                        app_deps.add(dep)

    # 2. Read Dockerfile
    if not os.path.exists(dockerfile_path):
        print(f"Error: {dockerfile_path} not found.")
        sys.exit(1)

    with open(dockerfile_path, 'r') as f:
        content = f.read()

    # Capture: (prefix), (the package list), (the cleanup command)
    dnf_pattern = re.compile(r'(dnf install -y\s+)(.*?)(\s+&& dnf clean all)', re.DOTALL)
    match = dnf_pattern.search(content)

    if not match:
        print("Error: Could not find dnf block.")
        sys.exit(1)

    prefix, _, suffix = match.groups()

    # 3. Format and Group
    protected_list = sorted(list(PROTECTED_DEPS))

    if reset_mode:
        # Only include protected dependencies
        formatted_block = " \\\n    ".join(protected_list) + " \\"
    else:
        # Include both protected and app-specific dependencies
        app_list = sorted(list(app_deps))
        formatted_block = " \\\n    ".join(protected_list)
        if app_list:
            formatted_block += f" \\\n    # --- {app_name} dependencies --- \\\n    "
            formatted_block += " \\\n    ".join(app_list)
        formatted_block += " \\"

    # 4. Write back
    new_content = dnf_pattern.sub(f"{prefix}\\\n    {formatted_block}{suffix}", content)
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
    parser.add_argument(
        "app_name",
        nargs="?",
        help="The name of the application to sync."
    )
    parser.add_argument(
        "-r", "--reset",
        action="store_true",
        help="Reset the Dockerfile to only keep the protected dependencies."
    )

    args = parser.parse_args()

    if not args.reset and not args.app_name:
        parser.error(f"{RED}The following arguments are required: app_name (unless using -r/--reset){RESET}")

    update_dockerfile(args.app_name, reset_mode=args.reset)