%global         app_id        page.codeberg.petsoi.coronet
%global         forgeurl      https://codeberg.org/petsoi/coronet
%global         tag           v%{version}

Name:           coronet
Version:        0.8.1
Release:        1%{?dist}
Summary:        Place crowns in a logic puzzle
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
Coronet is a logic puzzle game. The grid is divided into colored regions; place exactly one crown in every row, every column, and every colored region, with no two crowns touching, not even diagonally.

Left-click a cell to place or remove a crown, drag a crown to move it, right-click (or long-press on touch) to mark a cell you've deduced can't hold one. Crowns that break a rule are outlined in red.

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
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_metainfodir}/*.metainfo.xml


%changelog
* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.8.1-1
- Shrink the app size by letting GTK render the crown images.

