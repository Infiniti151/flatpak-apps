%global         app_id        nl.emphisia.icon
%global         app_name      Iconic
%global         forgeurl      https://github.com/youpie/%{app_name}
%global         tag           v%{version}

Name:           iconic
Version:        0
Release:        1%{?dist}
Summary:        Add icons on top of folders
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  blueprint-compiler
BuildRequires:  cairo-devel
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  appstream
BuildRequires:  pango-devel
BuildRequires:  rustc
BuildRequires:  gcc-c++

Requires:       cairo
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       pango

%description
This program allows an easy and intuitive way to add an icon on top of a folder to help you differentiate it better.

This program works best in combination with the app "Icon library" found on flathub and "Adwaita Colors" found on github

This program is written in Rust and Libadwaita and is my first attempt at creating an application

%prep
%forgesetup
# Fix hardcoded Flatpak path for RPM/system installs
sed -i 's|/app/share/Iconic/folders/|/usr/share/Iconic/folders/|g' src/windows/file_handling.rs
mkdir -p cargo-home

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson
%meson_build

%install
%meson_install
%find_lang %{app_name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{app_name}.lang
%license COPYING
%doc README.md changelog.md
%{_bindir}/%{app_name}
%{_datadir}/%{app_name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_metainfodir}/*.metainfo.xml
