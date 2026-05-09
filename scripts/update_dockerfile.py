#!/usr/bin/env python3
import re
import sys
import os

# Foundation tools. 
# We only list 'npm' because it correctly pulls nodejs24 on Fedora 44.
PROTECTED_DEPS = {
    'dnf-plugins-core', 'rpm-build', 'rpmdevtools', 'git-core', 
    'npm', 'sccache', 'ccache'
}

def update_dockerfile(app_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    spec_path = os.path.join(project_root, "apps", app_name, f"{app_name}.spec")
    dockerfile_path = os.path.join(project_root, "Dockerfile")

    if not os.path.exists(spec_path):
        print(f"Error: {spec_path} not found.")
        sys.exit(1)

    app_deps = set()

    # 1. Extract BuildRequires from Spec
    with open(spec_path, 'r') as f:
        for line in f:
            match = re.match(r'^\s*BuildRequires:\s+(.+)', line, re.IGNORECASE)
            if match:
                dep = match.group(1).split('>=')[0].split('>')[0].split('=')[0].strip()
                if '(' in dep:
                    dep = f"'{dep}'"
                
                # Deduplication: Don't add to app section if it's protected
                # Also handle the common case where spec might say nodejs but we use npm
                if dep not in PROTECTED_DEPS and dep != 'nodejs':
                    app_deps.add(dep)

    # 2. Read Dockerfile
    with open(dockerfile_path, 'r') as f:
        content = f.read()

    dnf_pattern = re.compile(r'(dnf install -y\s+)(.*?)(\s+&& dnf clean all)', re.DOTALL)
    match = dnf_pattern.search(content)
    
    if not match:
        print("Error: Could not find dnf block.")
        sys.exit(1)

    prefix, _, suffix = match.groups()

    # 3. Format and Group
    protected_list = sorted(list(PROTECTED_DEPS))
    app_list = sorted(list(app_deps))

    formatted_block = " \\\n    ".join(protected_list)
    formatted_block += f" \\\n    # --- {app_name} dependencies --- \\\n    "
    formatted_block += " \\\n    ".join(app_list)

    # 4. Write back
    new_content = dnf_pattern.sub(f"{prefix}\\\n    {formatted_block}{suffix}", content)
    with open(dockerfile_path, 'w') as f:
        f.write(new_content)

    print(f"✅ Success! Dockerfile synced for {app_name} using Node.js 24 via npm.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./scripts/update_dockerfile.py <app_name>")
        sys.exit(1)
    update_dockerfile(sys.argv[1])