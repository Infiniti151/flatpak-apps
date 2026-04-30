%define debug_package %{nil}

Name:           text-compare
Version:        0.0.0
Release:        1%{?dist}
Summary:        A simple text comparison tool
License:        GPL-3.0-or-later
URL:            https://github.com/josephmawa/TextCompare
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gjs
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
%autosetup -n TextCompare-%{version}

%build
%meson
%meson_build

%install
%meson_install
%find_lang TextCompare %{name}.lang

%check
%meson_test

%files -f %{name}.lang
%{_bindir}/io.github.josephmawa.TextCompare
%{_datadir}/TextCompare/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/dbus-1/services/*.service
%doc README.md