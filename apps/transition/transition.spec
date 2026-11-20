%global         app_id        page.codeberg.grinka.Transition
%global         forgeurl      https://codeberg.org/grinka/transition
%global         tag           v%{version}

Name:           transition
Version:        4.0
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
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       hicolor-icon-theme
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

%conf
%meson -Dprofile=release

%build
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
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Sat Sep 19 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 4.0-1
- Updated GNOME Runtime to 51
- Store page can now be translated

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

