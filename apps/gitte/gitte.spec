%global         app_id          de.wwwtech.gitte

Name:           gitte
Version:        0.10.1
Release:        1%{?dist}
Summary:        A GTK4/libadwaita Git client for the GNOME desktop
License:        GPL-3.0-or-later
URL:            https://codeberg.org/ckruse/Gitte
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libgit2)
BuildRequires:  pkgconfig(libssh2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  openssl-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext

%description
A modern, feature-rich Git client designed for the GNOME desktop.
Built with GTK4 and libadwaita, it provides a seamless and
intuitive interface for managing repositories, branches,
and stashes.

%prep
%setup -q -n %{name}

%build
export LIBGIT2_SYS_USE_PKG_CONFIG=0
export LIBSSH2_SYS_USE_PKG_CONFIG=1

%meson
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/dbus-1/services/*.service

%changelog
* Sun Sep 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.10.1-1
- This bugfix release fixes signing in Flatpak builds and adds small UI improvements.
- Fixes:
- Flatpak builds now respect the configured signing program for OpenPGP, SSH and X.509 signatures
- Git operations now use temporary files accessible to both the Flatpak sandbox and the host system, fixing failures when host programs need to read them
- UI improvements:
- Release dates in the release notes dialog now use a human-readable format
- The remotes button is now vertically centred when it is the only collapsed sidebar section
- Under the hood:
- Updated dependencies

* Sat Sep 12 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.10.0-1
- This release adds side-by-side diffs, Git LFS and submodule support, signing configuration, remote management, and major performance improvements.
- New features:
- Side-by-side diffs, configurable independently for the working copy and history views
- Set up Git LFS, manage tracked patterns, inspect its status, and track files directly from the working copy
- Add, update, sync, configure, deinitialise and remove submodules
- Add, rename, delete and fetch individual remotes, and delete remote branches, optionally together with their tracking configuration
- Configure commit and tag signing per repository, including the signing format and key
- Open the current repository in a terminal with F4
- Toggle between showing the whole file and only the changed context in diff views with Ctrl+Shift+E
- Optionally open a repository found in the current working directory when starting Gitte without a path
- ... (see upstream for full release notes)

* Thu Sep 03 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.9.1-1
- Update to 0.9.1

* Wed Sep 02 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.9.0-1
- Rewrite history more freely: reorder commits by drag and drop, edit a commit from the commit log, and squash & fixup, drop or cherry-pick commits (including several at once via multi-selection) directly in the commit graph view
- Rename stashes
- New “Discard all” actions in the working copy view and the sync-with-mainline dialog
- New “Open in external editor” context-menu entries
- Context menu for stashes in the commit graph view; stashes are shown directly above their parent commit
- Copy button on error toasts
- New setting to auto-expand the staged / unstaged lists depending on whether they are empty
- The branch name is now shown in the success toast when checking out
- Revamped stashing: a single dialog to choose between tracked and untracked files with a message, plus refined shortcuts (Ctrl+Shift+S and Ctrl+Shift+U) and a new stash action icon
- Overhauled context menus and menu toggles
- ... (see upstream for full release notes)

* Wed Jul 22 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.9.1-1
- Update to 0.9.1

* Fri Jul 17 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.9.0-1
- Update to 0.9.0

* Thu Jun 25 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.8.1-1
- Update to 0.8.1

* Tue Jun 23 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.8.0-1
- Update to 0.8.0

* Thu Jun 18 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.7.2-1
- Update to 0.7.2

* Tue Jun 16 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.7.1-1
- Update to 0.7.1

* Sun Jun 14 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.7.0-1
- Update to 0.7.0

* Thu Jun 04 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.6.1-1
- Update to 0.6.1

* Thu Jun 04 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.6.0-1
- Update to 0.6.0

* Thu May 28 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.5.0-1
- Update to 0.5.0

* Thu May 21 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.4.1-1
- Update to 0.4.1

* Wed May 20 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.4.0-1
- Update to 0.4.0

* Wed May 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.3.0-1
- Update to 0.3.0

* Fri May 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.2.0-1
- Update to 0.2.0

