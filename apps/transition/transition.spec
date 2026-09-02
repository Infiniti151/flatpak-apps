%global         app_id        page.codeberg.grinka.Transition
%global         forgeurl      https://codeberg.org/grinka/transition
%global         tag           v%{version}

Name:           transition
Version:        3.0
Release:        1%{?dist}
Summary:        Multimedia to audio conversion
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.9
BuildRequires:  ninja-build
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  libappstream-glib
BuildRequires:  rustc

Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme
Requires:       cairo
Requires:       pango
Requires:       gdk-pixbuf2
Requires:       gstreamer1
Requires:       gstreamer1-plugins-base

%description
Transition is a simple application for converting multimedia files to various audio formats, that can handle large amounts of arbitrary input and provides a few output options.

Transition supports converting to:
- OGG/Opus
- OGG/Vorbis
- MP3
- FLAC
- WAV

%prep
%forgesetup

%build
%meson -Dprofile=release
%meson_build

%install
%meson_install

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/dbus-1/services/*.service
%{_metainfodir}/*.metainfo.xml


%changelog
* Wed Sep 02 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 3.0-1
- New features:
- Audio channels, now you can select how much channels converted file would have
- Persistent settings (2 new settings!)
- Smart quality: if quality or channels is lower than is currently set it would preserve this quality (you can disable this in settings)
- UX Improvements:
- Changed layout to be more accessible for mobile devices
- Fixes:
- File paths now displayed correctly
- Fixed 'Low' quality for OGG/Vorbis
- Warning banner after conversion in replace mode now hides after clearing file list
- ... (see upstream for full release notes)

