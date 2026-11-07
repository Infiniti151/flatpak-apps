%global         app_id          com.mattjakeman.ExtensionManager
%global         forgeurl        https://github.com/mjakeman/extension-manager
%global         tag             v%{version}

Name:           extension-manager
Version:        0.7.0
Release:        1%{?dist}
Summary:        Install GNOME Extensions
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  forge-srpm-macros
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.alpha
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  blueprint-compiler
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

%description
Browse and install GNOME Shell extensions to customise your desktop.
Features:
- Browse extensions.gnome.org right inside the app
- Manage the extensions you already have installed

%prep
%forgesetup

%build
%meson -Dbacktrace=false
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
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_metainfodir}/*.metainfo.xml
%{_datadir}/glib-2.0/schemas/*.gschema.xml

%changelog
* Sat Nov 07 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.7.0-1
- Redesigned extension details, unifying local and web information in a single view
- Search installed extensions from the GNOME Shell overview
- Show extension errors in a dedicated dialog
- Supported GNOME versions are now shown in a dialog, including the installed version
- Selection mode to manage several installed extensions at once
- Open extension folders in Files and copy the path of system extensions
- Animated screenshots
- Bring back filtering of unsupported extensions
- Detect when GNOME Shell is not running
- Faster loading thanks to response and image caching
- ... (see upstream for full release notes)

* Fri May 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.6.5-1
- Minor update to fix search regressions
- Extension Manager lets you browse, install, and manage GNOME Shell Extensions. It is written with GTK 4 and libadwaita.
- It is recommended that you install Extension Manager via [Flathub](https://flathub.org/apps/com.mattjakeman.ExtensionManager) for automatic updates.
- What's Changed
- * Update it.po by @espositofabian in https://github.com/mjakeman/extension-manager/pull/885
- * Fix search regressions by @oscfdezdz in https://github.com/mjakeman/extension-manager/pull/881
- * po: Update template by @github-actions[bot] in https://github.com/mjakeman/extension-manager/pull/879
- * Translations update from Hosted Weblate by @weblate in https://github.com/mjakeman/extension-manager/pull/880
- * Update for v0.6.5 by @oscfdezdz in https://github.com/mjakeman/extension-manager/pull/888
- New Contributors
