#!/usr/bin/env python3
"""
    SPDX-FileCopyrightText: 2026 Infiniti151
    SPDX-License-Identifier: GPL-3.0-or-later
    ---
    COPR Build Status Monitor & Telegram Notifier

    Monitors COPR build progress across specified chroots, polls all builds
    together against one shared deadline, converts SVG/PNG app icons, builds
    formatted monospace status tables, and delivers comprehensive build alerts
    directly to Telegram.

    Usage:
        python3 scripts/check_copr_builds.py <builds_file.txt>
"""
import html
import io
import os
import pathlib
import re
import sys
import time

import cairosvg
import requests

COPR_API = "https://copr.fedorainfracloud.org/api_3"

CHROOTS = {
    "fedora-43-x86_64": "Fedora 43",
    "fedora-44-x86_64": "Fedora 44",
    "fedora-45-x86_64": "Fedora 45",
    "fedora-eln-x86_64": "Fedora ELN",
    "fedora-rawhide-x86_64": "Fedora Rawhide",
}

SUPPORTED = {
    "fedora-44-x86_64",
    "fedora-45-x86_64",
    "fedora-eln-x86_64",
    "fedora-rawhide-x86_64",
}

# States after which a build will not change anymore.
TERMINAL_STATES = {"succeeded", "failed", "canceled", "skipped"}

POLL_INTERVAL = 180      # 3 min between polling rounds
MAX_WAIT = 30 * 60       # 30 min shared deadline for ALL builds


def get_json(url, tries=3):
    """GET a JSON document, retrying transient request errors."""
    for i in range(tries):
        try:
            res = requests.get(url, timeout=30)
            res.raise_for_status()
            return res.json()
        except requests.RequestException:
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def get_build(build_id):
    return get_json(f"{COPR_API}/build/{build_id}")


def get_chroot_state(build_id, chroot):
    try:
        data = get_json(
            f"{COPR_API}/build-chroot?build_id={build_id}&chrootname={chroot}"
        )
        return data.get("state", "unknown")
    except Exception:
        return "unknown"


def get_chroot_states(build_id):
    return {chroot: get_chroot_state(build_id, chroot) for chroot in CHROOTS}


def get_icon_url(readme, app):
    """Finds the <img src> inside the README table row of `app` (row only)."""
    row_pattern = rf"^\|\s*{re.escape(app)}\s*\|.*$"
    row = re.search(row_pattern, readme, re.IGNORECASE | re.MULTILINE)
    if not row:
        return None
    img = re.search(r'<img src="([^"]+)"', row.group(0))
    return img.group(1) if img else None


def fetch_icon_png(icon_url):
    """Downloads an icon and converts it to a 256x256 PNG buffer if it is an SVG."""
    res = requests.get(icon_url, timeout=30)
    res.raise_for_status()

    content_type = res.headers.get("Content-Type", "").lower()
    if icon_url.lower().endswith(".svg") or "svg" in content_type:
        png_bytes = cairosvg.svg2png(
            bytestring=res.content,
            output_width=256,
            output_height=256,
        )
        return io.BytesIO(png_bytes)

    return io.BytesIO(res.content)


def send_photo(token, chat_id, photo_buf, caption):
    requests.post(
        f"https://api.telegram.org/bot{token}/sendPhoto",
        data={
            "chat_id": chat_id,
            "caption": caption,
            "parse_mode": "HTML",
        },
        files={"photo": ("icon.png", photo_buf, "image/png")},
        timeout=60,
    ).raise_for_status()


def send_message(token, chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        },
        timeout=60,
    ).raise_for_status()


def build_table(states):
    """Renders a monospace ASCII table inside <pre> tags for Telegram."""
    col1_width = 16
    col2_width = 8

    rows = [
        f"{'Chroot':<{col1_width}} | {'Status':<{col2_width}}",
        f"{'-' * col1_width}-+-{'-' * col2_width}",
    ]

    for chroot, label in CHROOTS.items():
        state = states.get(chroot, "unknown")
        if state == "succeeded":
            status_str = "✅"
        elif state == "failed":
            status_str = "❌"
        else:
            status_str = "⏳"
        rows.append(f"{label:<{col1_width}} | {status_str}")

    table_str = "\n".join(rows)
    return f"\n<pre>{html.escape(table_str)}</pre>"


def notify(token, chat_id, readme, build, overall, states):
    app = build["app"]
    old_ver = build["old_ver"]
    new_ver = build["new_ver"]
    build_id = build["build_id"]

    supported_failed = any(states.get(c) == "failed" for c in SUPPORTED)
    fedora43_failed = states.get("fedora-43-x86_64") == "failed"

    if overall == "succeeded":
        status = "✅"
    elif overall == "timeout":
        status = "⏳"
    elif supported_failed:
        status = "❌"
    elif fedora43_failed:
        status = "✅ (Fedora 43 failed ⚠️)"
    else:
        status = "❌"

    url = f"https://copr.fedorainfracloud.org/coprs/build/{build_id}/"

    lines = [
        f"<b>{html.escape(app)}</b>",
        "",
        f"<b>Overall:</b> {status}",
        f"<b>Version:</b> <code>{html.escape(old_ver)}</code> → <code>{html.escape(new_ver)}</code>",
    ]

    if status == "❌":
        lines.append(build_table(states))

    lines.extend([
        f"<b>Build ID:</b> <code>{html.escape(build_id)}</code>",
        f'<a href="{url}">View Build on Copr</a>',
    ])

    message = "\n".join(lines)
    icon_url = get_icon_url(readme, app)

    if icon_url and icon_url.startswith("http"):
        try:
            photo_buf = fetch_icon_png(icon_url)
            send_photo(token, chat_id, photo_buf, message)
            return
        except Exception as e:
            print(
                f"Warning: Failed to send icon photo for {app} ({e}), "
                "falling back to text.",
                file=sys.stderr,
            )

    send_message(token, chat_id, message)


def parse_builds(path):
    """Reads `app|old_ver|new_ver|build_id` lines, skipping blank/bad ones."""
    builds = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.strip().split("|")
        if len(parts) != 4:
            print(f"Warning: skipping malformed line: {line!r}", file=sys.stderr)
            continue
        app, old_ver, new_ver, build_id = parts
        builds.append({
            "app": app,
            "old_ver": old_ver,
            "new_ver": new_ver,
            "build_id": build_id,
        })
    return builds


def safe_notify(token, chat_id, readme, build, overall, states):
    """Sends one notification; returns False instead of raising on failure."""
    try:
        notify(token, chat_id, readme, build, overall, states)
        return True
    except Exception as e:
        print(f"Error: notification failed for {build['app']}: {e}", file=sys.stderr)
        return False


def monitor(token, chat_id, readme, builds):
    """
    Polls every pending build each round and notifies as soon as one finishes.
    Whatever is still pending at the shared deadline is reported as a timeout.
    Returns the number of failed notifications.
    """
    pending = {b["build_id"]: b for b in builds}
    notify_failures = 0
    deadline = time.monotonic() + MAX_WAIT

    while pending:
        for build_id in list(pending): # NOSONAR “copy needed: dict is modified in loop"
            try:
                overall = get_build(build_id).get("state", "unknown")
            except Exception as e:
                # Keep the build pending and try again next round.
                print(f"Warning: could not read build {build_id}: {e}", file=sys.stderr)
                continue

            if overall in TERMINAL_STATES:
                build = pending.pop(build_id)
                states = get_chroot_states(build_id)
                if not safe_notify(token, chat_id, readme, build, overall, states):
                    notify_failures += 1

        remaining = deadline - time.monotonic()
        if not pending or remaining <= 0:
            break
        time.sleep(min(POLL_INTERVAL, remaining))

    for build_id, build in pending.items():
        states = get_chroot_states(build_id)
        if not safe_notify(token, chat_id, readme, build, "timeout", states):
            notify_failures += 1

    return notify_failures


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    readme_path = pathlib.Path("README.md")
    readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    builds = parse_builds(pathlib.Path(sys.argv[1]))
    if not builds:
        print("No builds to monitor.")
        return

    failures = monitor(token, chat_id, readme, builds)
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()