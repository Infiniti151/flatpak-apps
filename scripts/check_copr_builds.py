#!/usr/bin/env python3
"""
    SPDX-FileCopyrightText: 2026 Infiniti151
    SPDX-License-Identifier: GPL-3.0-or-later
    ---
    COPR Build Status Monitor & Telegram Notifier

    Monitors COPR build progress across specified chroots, handles periodic polling,
    converts SVG/PNG app icons, builds formatted monospace status tables, and delivers
    comprehensive build alerts directly to Telegram.

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

POLL_INTERVAL = 300  # 5 min
MAX_POLLS = 6        # 30 min total


def get_build(build_id):
    res = requests.get(f"{COPR_API}/build/{build_id}", timeout=30)
    res.raise_for_status()
    return res.json()


def get_chroot_state(build_id, chroot):
    try:
        res = requests.get(
            f"{COPR_API}/build-chroot?build_id={build_id}&chrootname={chroot}",
            timeout=30,
        )
        res.raise_for_status()
        return res.json().get("state", "unknown")
    except Exception:
        return "unknown"


def get_icon_url(readme, app):
    pattern = rf"\|\s*{re.escape(app)}\s*\|.*?<img src=\"([^\"]+)\""
    match = re.search(pattern, readme, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else None


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


def wait_for_completion(build_id):
    states = {}
    for _ in range(MAX_POLLS):
        build = get_build(build_id)
        overall = build["state"]

        for chroot in CHROOTS:
            states[chroot] = get_chroot_state(build_id, chroot)

        if overall in ("succeeded", "failed"):
            return overall, states

        time.sleep(POLL_INTERVAL)

    return "timeout", states


def notify(token, chat_id, readme, app, old_ver, new_ver, build_id):
    overall, states = wait_for_completion(build_id)

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
        build_table(states),
        f"<b>Build ID:</b> <code>{build_id}</code>",
        f'<a href="{url}">View Build on Copr</a>',
    ]

    message = "\n".join(lines)
    icon_url = get_icon_url(readme, app)

    if icon_url and icon_url.startswith("http"):
        try:
            photo_buf = fetch_icon_png(icon_url)
            send_photo(token, chat_id, photo_buf, message)
            return
        except Exception as e:
            print(f"Warning: Failed to send icon photo ({e}), falling back to text.", file=sys.stderr)

    send_message(token, chat_id, message)


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    readme_path = pathlib.Path("README.md")
    readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    builds_file = pathlib.Path(sys.argv[1])

    for line in builds_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        app, old_ver, new_ver, build_id = line.strip().split("|")
        notify(token, chat_id, readme, app, old_ver, new_ver, build_id)


if __name__ == "__main__":
    main()