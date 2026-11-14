%global         app_id        app.drey.EarTag
%global         forgeurl      https://gitlab.gnome.org/World/eartag
%global         tag           %{version}

Name:           eartag
Version:        1.0.3
Release:        1%{?dist}
Summary:        Edit audio file tags
License:        MIT
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.58.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-asyncio
BuildRequires:  python3-mutagen
BuildRequires:  python3-aiohttp
BuildRequires:  python3-aiohttp-retry
BuildRequires:  python3-aiofiles
BuildRequires:  python3-pillow
BuildRequires:  python3-filetype
BuildRequires:  python3-acoustid
BuildRequires:  python3-audioread
BuildRequires:  python3-xxhash
BuildRequires:  python3-gobject
BuildRequires:  pkgconfig(gtk4) >= 4.16.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.0

Requires:       gtk4 >= 4.16.0
Requires:       libadwaita >= 1.8.0
Requires:       hicolor-icon-theme
Requires:       python3 >= 3.11
Requires:       python3-gobject >= 3.51.0
Requires:       python3-pillow
Requires:       python3-mutagen
Requires:       python3-filetype
Requires:       python3-acoustid
Requires:       python3-audioread
Requires:       python3-aiohttp
Requires:       python3-aiohttp-retry
Requires:       python3-aiofiles
Requires:       python3-xxhash

%description
Fixed an issue where files loading would freeze, and an error when changing cover art. From 1.0.0 notes:

General stability and speed improvements. Loading files is now considerably faster. The Identify option has been updated and should provide more accurate results, while being 4x as fast.

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{app_id}
%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml

%files -f %{app_id}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_scalableiconsdir}/*.svg
%{_hicolordir}/symbolic/apps/*.svg
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/dbus-1/services/*.service
%{_metainfodir}/*.metainfo.xml


%changelog
* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.0.3-1
- Fixed an issue where files loading would freeze, and an error when changing cover art. From 1.0.0 notes:
- General stability and speed improvements. Loading files is now considerably faster. The Identify option has been updated and should provide more accurate results, while being 4x as fast.

