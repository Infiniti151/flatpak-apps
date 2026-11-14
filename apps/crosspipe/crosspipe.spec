%global         app_id        io.github.dp0sk.Crosspipe
%global         forgeurl      https://github.com/dp0sk/Crosspipe
%global         tag           %{version}

Name:           crosspipe
Version:        0.1.1
Release:        1%{?dist}
Summary:        PipeWire graph GTK4/Libadwaita GUI
License:        GPL-3.0-only
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gtk4) >= 4.10
BuildRequires:  pkgconfig(libadwaita-1) >= 1.4
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  valac

Requires:       hicolor-icon-theme

%description
Crosspipe is a visual graph manager for PipeWire, built with GTK4/Libadwaita and Vala, following the GNOME Human Interface Guidelines.

Features:
- Visual graph of PipeWire nodes and connections
- Drag-and-drop connection management
- Native GTK4/Libadwaita interface, following GNOME HIG

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_scalableiconsdir}/*.svg
%{_hicolordir}/symbolic/apps/*.svg
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_metainfodir}/*.metainfo.xml


%changelog
* Fri Nov 06 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.1.1-1
- Fixes
- Fixed memory leak, caused by pipewire backend not freeing itself on exit
- Fixed tiny default zoom level
- Changes
- New icon
- Added panning with middle mouse button and space key
- Added shortcuts view

