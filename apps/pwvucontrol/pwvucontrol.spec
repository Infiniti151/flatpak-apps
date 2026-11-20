%global         app_id        com.saivert.pwvucontrol
%global         forgeurl      https://github.com/saivert/pwvucontrol
%global         tag           %{version}

Name:           pwvucontrol
Version:        0.5.3
Release:        1%{?dist}
Summary:        Volume control for pipewire
License:        GPL-3.0-or-later AND MIT AND Unicode-3.0 AND MPL-2.0
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  blueprint-compiler
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  libappstream-glib
BuildRequires:  clang-devel
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.0.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.2
BuildRequires:  pkgconfig(libpipewire-0.3) >= 0.3.83
BuildRequires:  pkgconfig(wireplumber-0.5) >= 0.5.11

Requires:       hicolor-icon-theme

%description
A native volume control app made with GTK + Rust.

%prep
%forgesetup

%conf
%meson

%build
%meson_build
env CARGO_HOME=%{_vpath_builddir}/cargo-home cargo tree -e normal --prefix none --format '{p}: {l}' | sed -E 's/ \(\*\)$//; s/ \(\/[^)]*\)//' | sort -u > LICENSE.dependencies

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license COPYING LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml


%changelog
* Fri Nov 20 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.5.3-1
- Changelog since 0.5.2
- Fixes so system color scheme is respected.

