# Contributing Guidelines

First off, thank you for helping maintain and expand this repository! Your contributions help make more applications available as native RPMs for the Fedora community.

## ⚒️ How You Can Help

### 1. Adding New Apps
- Open an **App Request** issue first to discuss the feasibility.
- Ensure the app is available via a stable source (GitHub or a Flatpak manifest).
- Submit a PR with the new spec file and any necessary patches.

### 2. Improving Existing App Packaging
- Optimize existing sections of the spec file like `%build` or `%install`.
- Add new sections to the spec file like `%pre` or `%post`.
- Fix missing dependencies found via `rpmlint`.
- Submit a PR with the updated spec file with a detailed description of the updates.

---

## 📝 Packaging Guidelines
- **Clean Specs:** Focus on the build logic and metadata. Follow [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/).
- **Naming:** Name files `app-name.spec`.
- **No Manual Changelogs:** **Do not edit the `%changelog` section for updates to an existing app.** We use a custom script in our GitHub Actions workflow to automatically inject changelogs from the upstream source into the spec file. Although, for a new app you'll need to add
a test changelog for the build to succeed.
- **ELN Specific Config:** If you're adding a spec file for a Rust app, you need to add this to the top of the file for the build to pass on ELN
  ```
  %if 0%{?eln}
  %define _empty_manifest_terminate_build 0
  %endif
  ```
- **PR Descriptions:** Describe your packaging tweaks clearly in your Pull Request.

---

## 🚀 Local Testing
Before submitting a Pull Request, ensure your changes build correctly on a Fedora system.

1. **Install Required Tools:**
   ```bash
   sudo dnf install mock rpm-build rpmlint rpmdevtools
   sudo usermod -aG mock $USER  # Requires a re-login to take effect
   ```
2. **Download Sources:**
   Download the files defined in the `Source` tags of your spec:
   `spectool -g -R app-name.spec`

3. **Build Source RPM:**
   Generate the `.src.rpm` needed for mock:
   `rpmbuild -bs app-name.spec`

4. **Mock Build:**
   Verify the build in a clean environment (change 44 to your target version):
   `mock -r fedora-44-x86_64 rebuild ~/rpmbuild/SRPMS/app-name-*.src.rpm`

5. **Lint the Spec:**
   `rpmlint app-name.spec`

---

## ⤴️ Submitting a Pull Request
1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/add-new-app`).
3. If you're adding a new app, you'll also need to update the CI matrix in `copr-build` workflow in .github/workflows and add an entry for the app in the README App List (App, Icon, Source, version, COPR Badge). The badge would show `unknown` status when the PR is open as there's no COPR package existing at that time (I'll create it after testing your changes locally. The badge may take upto 24 hrs to update status due to Github's image caching).
4. Commit your changes. If you are fixing a bug, reference the issue number in the commit message or PR title.
5. Push to your fork and open a Pull Request.

---

## ⚖️ Scope Reminder
This repository is for **packaging issues only**. If you find a bug in the application's internal code, please contribute those fixes directly to the upstream developer's repository.

---

## ❔ Questions
If you're unsure about a specific packaging rule or have questions/suggestions about app spec files/workflows, feel free to start a discussion in [Discussions](https://github.com/Infiniti151/flatpak-apps/discussions).
