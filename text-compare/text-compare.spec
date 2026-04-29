Name:           text-compare
Version:        %{?_version}%{!?_version:0.0.0}
Release:        1%{?dist}
Summary:        A simple text comparison tool
URL:            https://github.com/josephmawa/TextCompare
BugURL:			https://github.com/Infiniti151/flatpak-apps/issues
# This pulls code directly from the original author
Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  blueprint-compiler
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  glib2-devel
Requires:       gjs
Requires:       libadwaita
Requires:       gtk4

%description
A simple text comparison tool built with GJS and Adwaita.

%prep
%autosetup -n TextCompare-%{version}

%build
%meson
%meson_build

%install
%meson_install

%check
%meson_test

%files
%{_bindir}/io.github.josephmawa.TextCompare
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/TextCompare/
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/locale/*/LC_MESSAGES/*.mo
