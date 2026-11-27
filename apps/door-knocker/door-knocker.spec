%global         app_id        xyz.tytanium.DoorKnocker
%global         forgeurl      https://codeberg.org/tytan652/door-knocker
%global         tag           %{version}

Name:           door-knocker
Version:        0.9.0
Release:        1%{?dist}
Summary:        Check the availability of portals
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  blueprint-compiler
BuildRequires:  coreutils
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(gio-2.0) >= 2.84
BuildRequires:  pkgconfig(gtk4) >= 4.22
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9

Requires:       hicolor-icon-theme

%description
Door Knocker allows you to check availability of all portals provided by xdg-desktop-portal.

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
%license LICENSES/*
%doc README.md
%{_bindir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Fri Nov 27 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.9.0-1
- Style cleanup
- Update widget styling
- Update translations
