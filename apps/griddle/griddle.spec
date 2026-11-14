%global         app_id        page.codeberg.petsoi.griddle
%global         forgeurl      https://codeberg.org/petsoi/griddle
%global         tag           v%{version}

Name:           griddle
Version:        0.3.4
Release:        1%{?dist}
Summary:        Solve picture logic puzzles
License:        GPL-3
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.1.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  cairo-devel
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pango-devel
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.20
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9
BuildRequires:  rustc

Requires:       cairo
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       pango

%description
Griddle is a picture logic puzzle game. Fill in cells on a grid according to numeric clues along each row and column to reveal a hidden picture.

Left-click a cell to fill it in, right-click to cross out a cell you know must stay empty. A clue lights up once its line is complete.

%prep
%forgesetup
mkdir -p cargo-home

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%license LICENSE
%doc readme.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_scalableiconsdir}/*.svg
%{_hicolordir}/symbolic/apps/*.svg
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_metainfodir}/*.metainfo.xml


%changelog
* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.3.4-1
- Fixed new puzzles sometimes being harder than intended, especially on the larger boards.
- When no puzzle can be solved by logic alone, the closest one is used.

