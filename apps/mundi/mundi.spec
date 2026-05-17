%if 0%{?eln}
%define _empty_manifest_terminate_build 0
%endif

Name:           mundi
Version:        0.9.0
Release:        1%{?dist}
Summary:        A geography learning application for GNOME
License:        GPL-3.0-or-later
URL:            https://github.com/nacho/mundi
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson >= 0.59.0
BuildRequires:  cargo
BuildRequires:  rustc
BuildRequires:  pkgconfig
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(gtk4) >= 4.14
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5

Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Mundi helps you test your knowledge of world regions by clicking on an interactive map.

%prep
%autosetup

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson
%meson_build

%install
%meson_install

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.xml

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/metainfo/*.xml

%changelog
* Sun May 17 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.9.0-1
- Update to v0.9.0

