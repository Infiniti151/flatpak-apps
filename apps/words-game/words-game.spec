%if 0%{?eln}
%global         _empty_manifest_terminate_build 0
%endif

Name:           words-game
Version:        0.7.9.1
Release:        1%{?dist}
Summary:        A word puzzle game
License:        GPL-3.0-only
URL:            https://codeberg.org/petsoi/words
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson >= 1.1.0
BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  appstream
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.18.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5.5

%description
An elegant word game puzzle built natively using
Rust, GTK4, and Libadwaita.

%prep
%autosetup -n words -p1
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
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.xml

%files -f words.lang
%license LICENSE
%doc README.md
%{_bindir}/words
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/*.xml
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/words/
%{_datadir}/word-lists/
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Fri May 22 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.7.9.1-1
- Update to v0.7.9.1

