%if 0%{?eln}
%global         debug_package       %{nil}
%endif
%global         app_id              xyz.slothlife.Jogger
%global         forgeurl            https://codeberg.org/baarkerlounger/jogger
%global         upstream_name       Jogger
%global         tag                 %{version}

Name:           jogger
Version:        0
Release:        1%{?dist}
Summary:        Fitness tracker
License:        GPL-3.0-or-later AND 0BSD AND Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-3-Clause AND CC0-1.0 AND ISC AND MIT AND MIT-0 AND MPL-2.0 AND Unlicense AND Zlib
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  clippy
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  clang-devel
BuildRequires:  pkgconfig(espeak-ng)
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.14.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9
BuildRequires:  pkgconfig(shumate-1.0)
BuildRequires:  pkgconfig(alsa)

Requires:       hicolor-icon-theme

%description
Track and view your runs, walks, cycles, swims, and other workouts on mobile Linux.

%prep
%forgesetup

%conf
%meson

%build
%meson_build
env CARGO_HOME=%{_vpath_builddir}/cargo-home cargo tree -e normal --prefix none --format '{p}: {l}' | sed -E 's/ \(\*\)$//; s/ \(\/[^)]*\)//' | sort -u > LICENSE.dependencies

%install
%meson_install
%find_lang %{upstream_name}

%check
%meson_test

%files -f %{upstream_name}.lang
%license LICENSE LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_datadir}/appdata/%{app_id}.appdata.xml

