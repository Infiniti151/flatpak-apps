Name:           extension-manager
Version:        0.6.5
Release:        1%{?dist}
Summary:        A utility for browsing and installing GNOME Shell Extensions
License:        GPL-3.0-or-later
URL:            https://github.com/mjakeman/extension-manager
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc
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
A native desktop application for managing GNOME Shell Extensions.

%prep
%autosetup -n %{name}-%{version}

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
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*.svg
%{_metainfodir}/*.metainfo.xml
%{_datadir}/glib-2.0/schemas/*.gschema.xml

%changelog
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
