---
name: 🐛 Bug Report
about: Report a problem with an existing app
title: '[BUG]: '
labels: bug
assignees: ''
---

> [!IMPORTANT]
> **Packaging Scope Only:** This tracker is strictly for issues related to the **RPM package** (e.g., app fails to launch, missing dependencies, installation errors, broken shortcuts).
>
> **Upstream Bugs:** If the app opens but has a bug in its internal features (e.g., a button inside the app doesn't work, a UI glitch in the menus), please report it to the original developer with the source link in the README instead.

**App Name:**
<!-- e.g., text-compare -->


**Describe the bug:**
<!-- A clear and concise description of what the bug is -->


**Environment Details:**
- **Fedora Version:** <!-- 43, 44, ELN, or Rawhide -->
- **Kernel Version:** <!-- output of `uname -r` -->

**Steps to Reproduce:**
<!-- Write detailed steps on how you encountered the bug -->


**Terminal Checks:**
Please run the following commands and paste the output:
1. `rpm -qil --requires --provides <app-name>`:
```
// Paste output here
```

2. `ldd $(rpm -ql <app-name> | grep -E '^/(usr/)?s?bin/')` (If the app fails to start):
```
// Paste output here
```

**Relevant Logs:**
Provide output from `journalctl -f | grep -i "$(rpm -ql <app-name> | grep -E '^/(usr/)?s?bin/' | xargs -n 1 basename)"` (run this command and click on the app icon):
```
// Paste logs here
```

### Validation
- [ ] I confirm that this is a packaging issue (e.g., the app fails to start) and not a bug with the app's internal features.