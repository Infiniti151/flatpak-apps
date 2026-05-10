import yaml
import os
import sys

WORKFLOW_PATH = ".github/workflows/copr-build.yml"
IGNORE_LIST = {'.git', '.github', '.vscode', 'scripts', '__pycache__', 'build'}

def check_matrix():
    if not os.path.exists(WORKFLOW_PATH):
        print(f"Error: Workflow file not found at {WORKFLOW_PATH}")
        sys.exit(1)

    with open(WORKFLOW_PATH, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            sys.exit(1)

    try:
        jobs = data.get('jobs', {})
        target_job = next(job for job in jobs.values() if 'strategy' in job)
        matrix_include = target_job['strategy']['matrix']['include']
        configured_apps = {item['app_name'] for item in matrix_include}
    except (KeyError, StopIteration, TypeError):
        print("Error: Could not find matrix 'include' list in workflow.")
        sys.exit(1)

    apps_dir = 'apps'
    if not os.path.exists(apps_dir):
        print(f"Error: Apps directory '{apps_dir}' not found.")
        sys.exit(1)

    # Scan the apps/ folder
    app_entities = os.listdir(apps_dir)
    actual_app_folders = {
        d for d in app_entities
        if os.path.isdir(os.path.join(apps_dir, d)) and d not in IGNORE_LIST
    }
    # ------------------------------

    missing = actual_app_folders - configured_apps
    if missing:
        print(f"❌ Commit Blocked: New app folders detected in '{apps_dir}/' but not added to CI matrix:")
        for folder in missing:
            print(f"  - {folder}")
        print(f"\nUpdate the 'include' section in {WORKFLOW_PATH} to proceed. Also update the APP variable for the Test environment.")
        sys.exit(1)

    print(f"✅ CI matrix matches app folders in '{apps_dir}/'.")

if __name__ == "__main__":
    check_matrix()