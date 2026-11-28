%if 0%{?eln}
%global         debug_package       %{nil}
%endif
%global         app_id              io.github.tfuxu.floodit
%global         forgeurl            https://github.com/tfuxu/floodit
%global         tag                 %{version}

Name:           floodit
Version:        0
Release:        1%{?dist}
Summary:        Flood the board
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.64.0
BuildRequires:  go
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4) >= 4.18.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.0

Requires:       hicolor-icon-theme

%description
Flood It is a game with the simple premise of flooding the entire board with one color in the least amount of moves possible. Challenge yourself with this simple, yet addictive strategy game, where you need to flood-it as efficiently as you can!

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
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml

