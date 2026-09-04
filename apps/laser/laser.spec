%global         app_id        nl.andreasknoben.Laser
%global         forgeurl      https://codeberg.org/andreasknoben/laser
%global         tag           v%{version}

Name:           laser
Version:        0
Release:        1%{?dist}
Summary:        Rip CDs with ease
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps
BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  libappstream-glib
BuildRequires:  python3-devel
BuildRequires:  libcdio-devel
BuildRequires:  cdparanoia-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  libdiscid-devel
BuildRequires:  swig
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3
Requires:       cdrdao
Requires:       cd-discid
Requires:       gstreamer1-plugins-ugly
Requires:       python3-pycdio
Requires:       python3-discid
Requires:       python3-musicbrainzngs

%description
Laser is a simple CD ripper program developed for the GNOME desktop.

Features:
- Automatically retrieve CD information
- Rip tracks to aac, flac, mp3, opus, or wav
- Rip CDs to image formats with cue sheet
- Download and embed album cover art
- Modern design using Libadwaita and GTK4

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{name}
%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/dbus-1/services/*.service
%{_metainfodir}/*.metainfo.xml
