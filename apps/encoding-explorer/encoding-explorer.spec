%global         app_id        io.github.josephmawa.EncodingExplorer
%global         upstream_name EncodingExplorer
%global         forgeurl      https://github.com/josephmawa/EncodingExplorer
%global         tag           v%{version}

Name:           encoding-explorer
Version:        0.1.5
Release:        1%{?dist}
Summary:        Transform characters into binary
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.0.0
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
Encoding Explorer is a tool for learning character encoding. Below are the main features:
- Encode characters to ASCII, UTF-8, UTF-16, and UTF-32
- Encode numbers to IEEE-754 half, single, and double precision format
- Supports real-time encoding
- Change the endianness of a multi-byte encoding
- Provides user-friendly interface for exploring encodings
- Switch to light, dark, or system mode

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{upstream_name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{upstream_name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/encodingexplorer
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml


%changelog
* Fri Nov 20 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.1.5-1
- Upgrade Gnome runtime to version 50

