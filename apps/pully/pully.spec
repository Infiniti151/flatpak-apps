%global         app_id        page.codeberg.petsoi.pully
%global         forgeurl      https://codeberg.org/petsoi/pully
%global         tag           v%{version}

Name:           pully
Version:        0.2.2
Release:        1%{?dist}
Summary:        Draw a single line through every square of a puzzle grid
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
Pully is a Numberlink-style logic puzzle game. Draw a single line through every square of the grid, visiting each one exactly once, while passing through numbered checkpoints in order.

Drag from square to square to extend the line, and press an earlier square on the line to jump back to it. Higher levels bring bigger grids, fewer checkpoints, walls that block the line from crossing between two squares, and tunnels that let it jump to a matching square elsewhere on the grid.

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
* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.2.2-1
- Flash missed squares and checkpoints red instead of showing a toast.
- Smaller code improvements.

