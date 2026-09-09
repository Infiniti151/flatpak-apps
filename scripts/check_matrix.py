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
    COPR Matrix Consistency Checker

    Scans the local 'apps/' directory and cross-references folders against
    the matrix configuration defined in apps.json.
    Prevents unconfigured app directories from being committed without
    matrix representation.

    Usage:
        python3 scripts/check_matrix.py
"""
import json
import os
import sys

APPS_JSON_PATH = "apps.json"
IGNORE_LIST = {'.git', '.github', '.vscode', 'scripts', '__pycache__', 'build'}

def check_matrix():
    if not os.path.exists(APPS_JSON_PATH):
        print(f"Error: apps.json not found at {APPS_JSON_PATH}")
        sys.exit(1)

    with open(APPS_JSON_PATH, 'r', encoding='utf-8') as f:
        try:
            matrix = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            sys.exit(1)

    try:
        configured_apps = {item['app_name'] for item in matrix}
    except (KeyError, TypeError):
        print("Error: Could not find valid 'app_name' entries in apps.json.")
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

    missing = actual_app_folders - configured_apps
    if missing:
        print(f"❌ Commit Blocked: New app folders detected in '{apps_dir}/' but not added to matrix:")
        for folder in sorted(missing):
            print(f"  - {folder}")
        print(f"\nUpdate {APPS_JSON_PATH} (or run the update script) to proceed.")
        sys.exit(1)

    print(f"✅ Matrix in {APPS_JSON_PATH} matches app folders in '{apps_dir}/'.")

if __name__ == "__main__":
    check_matrix()