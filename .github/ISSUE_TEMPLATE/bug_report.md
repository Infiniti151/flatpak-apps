---
name: 🐛 Bug Report
about: Report a problem with an existing app
title: '[BUG]: '
labels: bug
assignees: ''
---

**App Name**
<!-- e.g., text-compare -->

**Describe the bug**
A clear and concise description of what the bug is.

**Environment Details**
- **Fedora Version:** <!-- e.g., 44 -->
- **Session Type:** <!-- Wayland or X11 -->
- **Kernel Version:** `uname -r`

**Steps to Reproduce**
- Write detailed steps on how you encountered the bug

**Terminal Checks**
Please run the following commands and paste the output:
1. `rpm -qi <app-name>`
2. `rpm -q --requires <app-name>`
3. `rpm -ql <app-name>`
4. `rpm -V <app-name>`

**Relevant Logs**
Provide output from `journalctl -f | grep -i "$(rpm -ql <app-name> | grep '/bin/' | xargs -n 1 basename)"`
```javascript
// Paste logs here