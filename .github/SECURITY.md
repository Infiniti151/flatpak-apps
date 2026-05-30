# Security Policy

## Supported Versions

This project focuses on providing native RPM packaging for Fedora and Enterprise Linux environments. Security updates are prioritized for active Fedora releases.

| Version | Supported          |
| ------- | ------------------ |
| Fedora 44 | ✅ Yes             |
| Fedora 43 | ✅ Yes             |
| Rawhide | 🧪 Best Effort     |
| ELN     | 🧪 Best Effort     |

---

## Security Model & Scope

This repository converts applications from the **Flatpak** ecosystem into native **RPM** packages via spec files.

### 🛡️ Sandboxing Disclaimer
By design, **Flatpaks** run in a containerized sandbox (using `bubblewrap`). By converting these to **RPMs**, the application runs with **native system permissions**.
- Users should trust the upstream application source before installation.
- Native execution allows for better system integration but removes the isolation layer provided by the Flatpak runtime.

### 🔍 Supply Chain Security
*   **Sources:** All spec files pull directly from official upstream GitHub/GitLab releases or verified Flatpak manifests.
*   **Build Process:** Packages are intended to be built in clean environments (like `mock` or Fedora COPR) to ensure no host-system contamination.
*   **No Binary Blobs:** I prioritize building from source. If a pre-compiled binary is used (e.g., for proprietary tools), it is clearly defined in the `Source` of the spec file.

---

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

If you discover a security risk related to the **packaging** (e.g., insecure file permissions, dangerous `%post` scripts, or hardcoded secrets), please report it privately:

1.  **Contact:** Email me at **[43163551+Infiniti151@users.noreply.github.com]**.
2.  **Encrypted Communication:** My public key is available on `keyserver.ubuntu.com` under my email address.
3.  **Timeline:** I will acknowledge your report within 48 hours and work toward a fix as a high priority.

### Upstream Application Vulnerabilities
If the vulnerability exists within the application code itself (not the RPM packaging), please report it directly to the **original upstream developer**. Once they release a patched version, I will update the RPM build here as soon as possible.

---

## Best Practices for Users
*   **Audit the Spec:** I encourage users to inspect the `%build` and `%install` sections of the spec files in this repo.
*   **Verify GPG:** When installing from my COPR, always verify the GPG key when prompted by `dnf`.
*   **Runtime Monitoring:** Use tools like `systemd-coredump` or `strace` if you suspect an application is behaving unexpectedly.
