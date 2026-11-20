%global         app_id        io.github.josephmawa.Egghead
%global         forgeurl      https://github.com/josephmawa/Egghead
%global         tag           v%{version}

Name:           egghead
Version:        0
Release:        1%{?dist}
Summary:        Learn while having fun
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.5.2
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  gjs
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache

Requires:       gtk4
Requires:       gjs
Requires:       hicolor-icon-theme
Requires:       libadwaita

%description
A simple trivia app to enjoy in your free time

Below are the main features of Egghead:
- Download quiz
- Save downloaded quiz
- Delete saved quiz
- Switch to dark, light, or system mode

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
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml
