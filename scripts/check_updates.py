#!/usr/bin/env python3
import json
import subprocess
import os
import re
import concurrent.futures

def get_app_id(spec_path):
    try:
        result = subprocess.check_output(
            f"grep -E '^\\s*%global\\s+(app_id|rdnn)\\s+' {spec_path} | awk '{{print $3}}'",
            shell=True
        ).decode('utf-8').strip()
        return result
    except subprocess.CalledProcessError:
        return None

def check_app(app):
    app_name = app['app_name']
    spec_path = f"apps/{app_name}/{app_name}.spec"

    if not os.path.exists(spec_path):
        return None

    # 1. Get current version from spec
    old_ver = None
    with open(spec_path, 'r') as f:
        for line in f:
            if line.startswith('Version:'):
                old_ver = line.split()[1].strip()
                break

    if not old_ver:
        return None

    # 2. Get APP_ID
    app_id = get_app_id(spec_path)
    if not app_id:
        return None

    # 3. Fetch Upstream Version
    provider = app.get('provider', '')
    instance = app.get('instance', '')
    repo = app.get('upstream_repo', '')

    try:
        raw_new_ver = subprocess.check_output(
            ['python3', 'scripts/changelog_scraper.py', 'get-version', provider, instance, repo, app_id],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

    if not raw_new_ver or raw_new_ver == 'null':
        return None

    # Clean the version string (strip 'v' or 'V')
    clean_new_ver = re.sub(r'^[vV]\.?', '', raw_new_ver)

    # 4. Compare and return updated app dict if update is needed
    if old_ver != clean_new_ver:
        app['old_ver'] = old_ver
        app['new_ver'] = clean_new_ver
        app['raw_new_ver'] = raw_new_ver
        print(f"[INFO] Update found for {app_name}: {old_ver} -> {clean_new_ver}")
        return app
    else:
        print(f"[OK] {app_name} is up to date ({old_ver})")
        return None

def main():
    with open('apps.json', 'r') as f:
        apps = json.load(f)

    updates_needed = []

    # Run checks concurrently with 15 workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        # Map the apps to the executor and collect results
        results = executor.map(check_app, apps)

        for result in results:
            if result is not None:
                updates_needed.append(result)

    matrix_json = json.dumps(updates_needed)
    github_output = os.environ.get('GITHUB_OUTPUT')

    # Output the dynamic matrix for GitHub Actions OR local console
    if github_output:
        with open(github_output, 'a') as fh:
            fh.write(f"matrix={matrix_json}\n")
    else:
        print("\n--- LOCAL EXECUTION: GitHub Output ---")
        print(f"matrix={matrix_json}")

if __name__ == "__main__":
    main()