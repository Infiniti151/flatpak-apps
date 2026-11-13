%global         app_id        page.codeberg.petsoi.pully
%global         forgeurl      https://codeberg.org/petsoi/pully
%global         tag           v%{version}

Name:           pully
Version:        0
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
Pully is a Numberlink-style logic puzzle game. Draw a single line through every square of the grid, visiting each one exactly once, while passing through numbered checkpoints in order.

Drag from square to square to extend the line, and press an earlier square on the line to jump back to it. Higher levels bring bigger grids, fewer checkpoints, walls that block the line from crossing between two squares, and tunnels that let it jump to a matching square elsewhere on the grid.

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
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_metainfodir}/*.metainfo.xml
