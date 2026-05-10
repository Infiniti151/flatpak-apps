Name:           amberol
Version:        2026.1
Release:        1%{?dist}
Summary:        A small and simple music player
License:        GPL-3.0-or-later AND CC-BY-SA-3.0 AND CC0-1.0
URL:            https://gitlab.gnome.org/World/amberol

Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  meson >= 0.59.0
BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pkgconfig(gtk4) >= 4.19.5
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-play-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext

Requires:       gtk4 >= 4.19.5
Requires:       libadwaita
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugins-bad-free
Requires:       hicolor-icon-theme

%description
Amberol is a music player with no delusions of grandeur. If you want
to play music and nothing else, Amberol is the right tool.

%prep
%autosetup -n %{name}-%{version}

%build
export CARGO_HOME="$(pwd)/cargo-home"
%meson -Dprofile=default
%meson_build

%install
export CARGO_HOME="$(pwd)/cargo-home"
%meson_install
%find_lang %{name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

%files -f %{name}.lang
%license LICENSES/CC-BY-SA-3.0.txt
%license LICENSES/CC0-1.0.txt
%license LICENSES/GPL-3.0-or-later.txt
%doc README.md
%{_bindir}/*
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/dbus-1/services/*.service
%{_datadir}/icons/hicolor/*/apps/*.*

%changelog
* Sun May 10 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 2026.1-1
- Initial RPM release for Amberol on Fedora 44