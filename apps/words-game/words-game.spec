%if 0%{?eln}
%global         _empty_manifest_terminate_build 0
%endif
%global         app_id          page.codeberg.petsoi.words
%global         forgeurl        https://codeberg.org/petsoi/words
%global         tag             v%{version}

Name:           words-game
Version:        0.8.1
Release:        1%{?dist}
Summary:        A word puzzle game
License:        GPL-3.0-only
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.1.0
BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  appstream
BuildRequires:  libappstream-glib
BuildRequires:  forge-srpm-macros
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.18.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5.5

%description
An elegant word game puzzle built natively using
Rust, GTK4, and Libadwaita.

%prep
%forgesetup
find . -name "*metainfo.xml*" -exec sed -i '/<releases>/,/<\/releases>/d' {} +

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson -Dprofile=default
%meson_build

%install
%meson_install
%find_lang words

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml

%files -f words.lang
%license LICENSE
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/%{app_id}/
%{_datadir}/applications/*.desktop
%{_metainfodir}/*.xml
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/words/
%{_datadir}/word-lists/
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Mon Oct 26 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.8.1-1
- Link the solution to its Wiktionary entry on the game-over screen.
- Fix letter feedback colors with custom GTK themes.
- Install the binary and word lists under the application ID to avoid conflicts outside Flatpak.

* Sun Oct 11 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.8.0-1
- Improve layout: keyboard stays at the bottom and the letter grid keeps square cells.
- Update to GNOME 51.

* Wed Sep 02 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.7.9-1
- Update to 0.7.9

* Fri May 22 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.7.9.1-1
- Update to v0.7.9.1

