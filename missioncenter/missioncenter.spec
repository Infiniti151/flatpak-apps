%global         debug_package %{nil}

Name:           missioncenter
Version:        1.1.0
Release:        1%{?dist}
Summary:        Monitor your CPU, Memory, Disk, Network and GPU usage

License:        GPLv3
URL:            https://gitlab.com/mission-center-devs/mission-center
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/-/archive/v%{version}/mission-center-v%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(blueprint-compiler)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  gcc
BuildRequires:  gettext

# Added for magpie/nng
BuildRequires:  cmake
BuildRequires:  nng-devel
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(udev)

Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Mission Center is a system monitor written in Rust using GTK4 and Libadwaita.
It provides a highly detailed view of system performance, including per-thread 
CPU usage and hardware-accelerated GPU monitoring.

%prep
%autosetup -n mission-center-v%{version}

%build
export CARGO_NET_OFFLINE=false
%meson -Dflatpak=false
%meson_build

%install
%meson_install
%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml

%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/%{name}-magpie
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_metainfodir}/*.xml
%doc README.md

%changelog
* Thu Apr 30 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.1.0-1
- Initial RPM release for Fedora from GitLab source
