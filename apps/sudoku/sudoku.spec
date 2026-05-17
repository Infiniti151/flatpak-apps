%global debug_package %{nil}

Name:           sudoku
Version:        1.7.0
Release:        1%{?dist}
Summary:        Sudoku Game application
License:        GPL-3.0-or-later
URL:            https://github.com/sepehr-rs/Sudoku
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson >= 1.4.0
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  gettext
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme
Requires:       python3

%description
A beautiful, modern Sudoku application featuring classic and diagonal variants.

%prep
%autosetup -n Sudoku-%{version}

%build
%meson
%meson_build

%install
%meson_install
sed -i 's|/usr/sbin/python3|/usr/bin/python3|g' %{buildroot}%{_bindir}/sudokugame
find %{buildroot}%{_datadir}/sudokugame/ -type f -name "*.py" -exec sed -i 's|/usr/sbin/python3|/usr/bin/python3|g' {} +
ln -s sudokugame %{buildroot}%{_datadir}/sudoku

%find_lang sudokugame

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.xml

%files -f sudokugame.lang
%license COPYING
%doc README.md
%{_bindir}/sudokugame
%{_datadir}/sudokugame/
%{_datadir}/sudoku
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg
%{_datadir}/metainfo/*.xml

%changelog
* Sun May 17 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.7.0-1
- Initial packaging for sudoku version 1.7.0