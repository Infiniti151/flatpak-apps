%global         app_id        org.gnome.gitlab.YaLTeR.VideoTrimmer
%global         tag           v%{version}

Name:           video-trimmer
Version:        0
Release:        1%{?dist}
Summary:        Trim videos quickly
License:        GPL3+
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            https://gitlab.gnome.org/YaLTeR/video-trimmer

BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-2.0) >= 2.80.0
BuildRequires:  pkgconfig(gtk4) >= 4.16.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.0

Requires:       %{_bindir}/ffmpeg
Requires:       hicolor-icon-theme

%description
Video Trimmer cuts out a fragment of a video given the start and end timestamps. The video is never re-encoded, so the process is very fast and does not reduce the video quality.

%prep
rm -rf %{name}-%{version}
git clone --depth 1 --branch %{tag} %{url}.git %{name}-%{version}
rm -rf %{name}-%{version}/.git
%setup -T -D -n %{name}-%{version}

%conf
%meson

%build
%meson_build
env CARGO_HOME=.cargo cargo tree -e normal --prefix none --format '{p}: {l}' | sed -E 's/ \(\*\)$//; s/ \(\/[^)]*\)//' | sort -u > LICENSE.dependencies

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license COPYING LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml
