%if 0%{?eln}
%global         debug_package       %{nil}
%endif
%global         app_id              de.haeckerfelix.Shortwave
%global         tag                 %{version}

Name:           shortwave
Version:        0
Release:        1%{?dist}
Summary:        Listen to internet radio
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            https://gitlab.gnome.org/World/Shortwave

BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  git-core
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  openssl3-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.16
BuildRequires:  pkgconfig(gstreamer-audio-1.0) >= 1.16
BuildRequires:  pkgconfig(gstreamer-bad-audio-1.0) >= 1.16
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.16
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0) >= 1.16
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 1.16
BuildRequires:  pkgconfig(gtk4) >= 4.16
BuildRequires:  pkgconfig(lcms2) >= 2.12.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.alpha
BuildRequires:  pkgconfig(libseccomp) >= 2.5.0
BuildRequires:  pkgconfig(shumate-1.0) >= 1.3
BuildRequires:  pkgconfig(sqlite3) >= 3.20
BuildRequires:  pkgconfig(glycin-gtk4-2) >= 2.0.1

Requires:       hicolor-icon-theme
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugins-bad-free

%description
Shortwave is an internet radio player that provides access to a station database with over 50,000 stations.

Features:
- Create your own library where you can add your favorite stations
- Easily search and discover new radio stations
- Automatic recognition of tracks, with the possibility to save them individually
- Responsive application layout, compatible for small and large screens
- Play audio on supported network devices (e.g. Google Chromecasts)
- Seamless integration into the GNOME desktop environment

%prep
rm -rf %{name}-%{version}
git clone --depth 1 --branch %{tag} %{url}.git %{name}-%{version}
rm -rf %{name}-%{version}/.git
%setup -T -D -n %{name}-%{version}

%conf
%meson

%build
%meson_build
env CARGO_HOME=%{_vpath_builddir}/cargo-home cargo tree -e normal --prefix none --format '{p}: {l}' | sed -E 's/ \(\*\)$//; s/ \(\/[^)]*\)//' | sort -u > LICENSE.dependencies

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license COPYING.md LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_dbusservicesdir}/%{app_id}.service
%{_metainfodir}/%{app_id}.metainfo.xml
