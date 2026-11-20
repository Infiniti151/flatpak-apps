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
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.20
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9

Requires:       hicolor-icon-theme

%description
Griddle is a picture logic puzzle game. Fill in cells on a grid according to numeric clues along each row and column to reveal a hidden picture.

Left-click a cell to fill it in, right-click to cross out a cell you know must stay empty. A clue lights up once its line is complete.

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license LICENSE
%doc readme.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_metainfodir}/*.metainfo.xml

%changelog
* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.3.4-1
- Fixed new puzzles sometimes being harder than intended, especially on the larger boards.
- When no puzzle can be solved by logic alone, the closest one is used.

