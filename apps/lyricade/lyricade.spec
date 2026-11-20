%global         app_id        io.github.weiteck.Lyricade
%global         forgeurl      https://github.com/weiteck/lyricade
%global         tag           v%{version}

Name:           lyricade
Version:        0.7.1
Release:        1%{?dist}
Summary:        Download and manage lyrics for your music library
License:        Apache-2.0 AND MIT AND ISC AND BSD-3-Clause AND Unicode-3.0 AND MPL-2.0
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cargo-rpm-macros
BuildRequires:  cargo
BuildRequires:  rustc
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  glibc-langpack-en
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(alsa)

Requires:       hicolor-icon-theme

%description
Scan your music library and download missing lyrics, in either synchronised LRC
or plain text format, at your preference. It also assists in managing your
existing embedded and external lyrics.

Features:
- Scan your music and find missing lyrics from several providers
- Download either synchronised LRC or plain TXT lyrics
- Embed lyrics to the metadata tag and/or save as a sidecar file
- Embed existing sidecar LRC and TXT files into lyrics tags
- Remove existing lyrics files if a file is already tagged
- Convert LRC lyrics to plain TXT lyrics
- Lyrics viewer with playback and lyric highlighting for LRC lyrics
- Supports multiple music libraries

%prep
%forgesetup
%cargo_prep -N

%build
export CARGO_NET_OFFLINE=false
%cargo_build
env CARGO_HOME=.cargo cargo tree -e normal --prefix none --format '{p}: {l}' | sort -u > LICENSE.dependencies

%install
export CARGO_NET_OFFLINE=false
%cargo_install
install -Dpm0644 data/icons/%{app_id}.svg %{buildroot}%{_scalableiconsdir}/%{app_id}.svg
install -Dpm0644 data/icons/symbolic/%{app_id}-symbolic.svg %{buildroot}%{_symboliciconsdir}/%{app_id}-symbolic.svg
install -Dpm0644 data/%{app_id}.desktop %{buildroot}%{_appsdir}/%{app_id}.desktop
install -Dpm0644 data/%{app_id}.metainfo.xml %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

%check
export CARGO_NET_OFFLINE=false
%cargo_test -- -- --skip provider::manager::tests
desktop-file-validate %{buildroot}%{_appsdir}/%{app_id}.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_metainfodir}/%{app_id}.metainfo.xml

* Fri Nov 20 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 4.3.2-1
- Test
