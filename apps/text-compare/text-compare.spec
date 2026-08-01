%global         debug_package %{nil}
%global         forgeurl      https://github.com/josephmawa/TextCompare

Name:           text-compare
Version:        0.1.11
Release:        1%{?dist}
Summary:        A simple text comparison tool
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildArch:      noarch

%forgemeta

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gjs
BuildRequires:  forge-srpm-macros
BuildRequires:  blueprint-compiler
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  glib2-devel

Requires:       gjs
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
A simple text comparison tool built with GJS and Adwaita.

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang TextCompare %{name}.lang

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/io.github.josephmawa.TextCompare
%{_datadir}/TextCompare/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/dbus-1/services/*.service
%doc README.md

%changelog
* Fri May 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.1.11-1
- Update to v0.1.11
