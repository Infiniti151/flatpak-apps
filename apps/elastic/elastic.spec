%global         app_id        app.drey.Elastic
%global         forgeurl      https://gitlab.gnome.org/World/elastic
%global         tag           %{version}

Name:           elastic
Version:        0
Release:        1%{?dist}
Summary:        Design spring animations
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gtk4) >= 4.17.5
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.rc
BuildRequires:  pkgconfig(template-glib-1.0)
BuildRequires:  valac

Requires:       hicolor-icon-theme

%description
Elastic allows to design and export spring physics-based animations to use with libadwaita.

Features:
- Preview translation, rotation and scaling transformations.
- See the animation curve and duration on a graph.
- Drag a handle to see it return back with the spring physics.
- Export C, JavaScript, Python, Vala or Rust code.

%prep
%forgesetup

%build
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
%license COPYING
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/dbus-1/services/*.service
%{_metainfodir}/*.metainfo.xml
