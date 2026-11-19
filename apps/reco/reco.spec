%global         app_id        com.github.ryonakano.reco
%global         forgeurl      https://github.com/ryonakano/reco
%global         tag           %{version}

Name:           reco
Version:        0
Release:        1%{?dist}
Summary:        Focus on recording
License:        GPL-3.0-or-later AND MIT
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  git
BuildRequires:  meson >= 0.58.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  vala
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(glib-2.0) >= 2.74
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.20
BuildRequires:  pkgconfig(gtk4) >= 4.12
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8
BuildRequires:  pkgconfig(ryokucha)

Requires:       hicolor-icon-theme
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Recommends:     gstreamer1-plugin-libav

%description
Reco is an audio recorder focused on being concise and simple to use.

You can use it to record and remember spoken words, system audio, improvised
melodies, and anything else you can do with a microphone, speaker, or both.

Features include:
- Recording sounds from both your microphone and system at the same time
- Saving in many commonly used formats: ALAC, FLAC, MP3, Ogg Vorbis, Opus, WAV
- Timed recording with a delay before recording and a maximum length
- Adding artist and year metadata to recording files
- Choosing where to save recordings, automatically or manually
- Saving recordings when the app quits

%prep
%forgesetup
meson subprojects download $(basename -s .wrap subprojects/live*.wrap)

%build
%meson -Duse_submodule=true
%meson_build

%install
DESTDIR=%{buildroot} %{__meson} install -C %{_vpath_builddir} --no-rebuild --skip-subprojects
%find_lang %{app_id}

install -Dpm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dpm 0644 subprojects/live*/LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE.live-chart

%check
meson test -C %{_vpath_builddir} --print-errorlogs --no-suite live-chart
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{app_id}.lang
%license %{_licensedir}/%{name}
%doc README.md
%{_bindir}/%{app_id}
%{_appsdir}/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_gschemasdir}/*.gschema.xml
%{_metainfodir}/*.metainfo.xml

