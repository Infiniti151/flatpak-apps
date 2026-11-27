%global         app_id        com.rafaelmardojai.SharePreview
%global         forgeurl      https://github.com/rafaelmardojai/share-preview
%global         tag           %{version}

Name:           share-preview
Version:        1.0.0
Release:        1%{?dist}
Summary:        Test social media cards locally
License:        GPL-3.0-or-later AND CC0-1.0 AND 0BSD AND Apache-2.0 AND (Apache-2.0 WITH LLVM-exception) AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND ISC AND MIT AND MPL-2.0 AND MPL-2.0-or-later AND Unlicense AND Unicode-3.0 AND Zlib
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.63.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  cargo
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  openssl3-devel
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.0.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.0.0-alpha.1

Requires:       hicolor-icon-theme

%description
Preview and debug websites metadata tags for social media share.

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
* Fri Nov 27 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.0.0-1
- Support opening HTTP URLs from desktop and cli
- Improve handling of multiple windows
