%global         app_id io.github.zingytomato.netpeek

Name:           netpeek
Version:        0.3.3
Release:        1%{?dist}
Summary:        Modern network scanner for GNOME

License:        GPL-3.0-or-later
URL:            https://github.com/ZingyTomato/NetPeek
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  python3-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gtk-update-icon-cache
BuildRequires:  glibc-langpack-en

Requires:       python3
Requires:       python3-gobject
Requires:       python3-nmap
Requires:       nmap
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
NetPeek is a modern network scanner designed for the GNOME desktop, built with Python, GTK4, and Libadwaita.

%prep
%autosetup -n NetPeek-%{version}

%build
%meson
%meson_build

%install
%meson_install

%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/dbus-1/services/%{app_id}.service
%{_datadir}/metainfo/%{app_id}.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{app_id}-symbolic.svg

%changelog
* Mon Aug 24 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.3.3-1
- What's Changed
- Grouped all IP presets into a single button.
- Added date filters and custom date ranges to scan history.
- *Full Changelog**: https://github.com/ZingyTomato/NetPeek/compare/v0.3.2...v0.3.3

* Sat Aug 15 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.3.2-1
- What's Changed
- Updated Estonian and Czech translations - @p-bo, Priit Jõerüüt
- Added search functionality to all scan pages.
- Implemented a new scan info dialog for current and previous scans.
- Results view format is now preserved when resizing the window.
- Updated nmap to version [7.991](https://nmap.org/changelog.html#7.991).
- Updated screenshots.
- Removed MAC address collection due to lack of consistent detection.
- *Full Changelog**: https://github.com/ZingyTomato/NetPeek/compare/v0.3.1...v0.3.2

* Sun Aug 02 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.3.1-1
- What's Changed?
- Device cards now cap System Information and Services at one line, with expand/collapse buttons to reveal the full text.
- Moved the thread count picker into the main menu.
- Added better indication throughout the UI that a deep scan is taking place.
- Added a Translate link to the About dialog.
- Now using Weblate for translations - https://hosted.weblate.org/engage/netpeek/
- New Contributors
- @weblate made their first contribution in https://github.com/ZingyTomato/NetPeek/pull/34
- *Full Changelog**: https://github.com/ZingyTomato/NetPeek/compare/v0.3.0...v0.3.1

* Sun Jul 26 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.3.0-1
- What's Changed?
- New Deep Scan mode for additional information like OS identification, software versions and more.
- Expanded service detection for common self-hosted and DevOps services (MySQL, PostgreSQL, Redis, Home Assistant, Plex, etc.). Only services which have "unique" ports (not commonly used ports) are chosen.
- Improved UI adaptability for smaller screens.
- All sorting options now default to descending once clicked.
- Fixed a bug where rescanning after cancelling a running scan would not find all devices in the given IP range.
- Cards in the card view should not vary in size by great amounts.
- Removed the "Examples: 192.168.x.x" subtitle from the homepage.
- *Full Changelog**: https://github.com/ZingyTomato/NetPeek/compare/v0.2.9...v0.3.0

* Fri Jul 24 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.2.9-1
- What's Changed?
- New app icon.
- Redesigned the light, dark and system style switcher.
- Cockpit instances are now detected and shown alongside SMB shares in a combined Services row instead of the old SMB row.
- Header actions move into a bottom bar when the window is narrow to better assist with smaller screens.
- Custom device names now apply retroactively to previous scans.
- Added an Open Folder shortcut to the CSV export notification.
- Removed most toast notifications, keeping only copy, export and error messages.
- The active sort option is now highlighted and shows its direction.
- Sorting is disabled while scanning and when no devices are found.
- ... (see upstream for full release notes)

