%global         app_id        xyz.slothlife.Diveboard
%global         forgeurl      https://codeberg.org/baarkerlounger/diveboard-gtk
%global         tag           v%{version}

Name:           diveboard
Version:        0
Release:        1%{?dist}
Summary:        A Scuba Diving Logbook
License:        GPL-3.0-or-later AND 0BSD AND Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-3-Clause AND ISC AND MIT AND MIT-0 AND Unicode-3.0 AND Unlicense AND Zlib
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(shumate-1.0)
BuildRequires:  pkgconfig(sqlite3)

Requires:       hicolor-icon-theme

%description
A GTK app for Diveboard.com. A mobile Scuba Diving Logbook.

%prep
%forgesetup

%conf
%meson --buildtype=release

%build
%meson_build
env CARGO_HOME=%{_vpath_builddir}/cargo-home cargo tree -e normal --prefix none --format '{p}: {l}' | sed -E 's/ \(\*\)$//; s/ \(\/[^)]*\)//' | sort -u > LICENSE.dependencies

%install
find %{_vpath_builddir}/cargo-home -name '*.rs' -perm /111 -exec chmod a-x {} +
%meson_install

%check
%meson_test

%files
%license COPYING LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_hicolordir}/*/apps/%{app_id}.png
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml

