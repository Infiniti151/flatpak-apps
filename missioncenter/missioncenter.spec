%global         debug_package %{nil}

Name:           missioncenter
Version:        1.1.0
Release:        1%{?dist}
Summary:        Monitor your CPU, Memory, Disk, Network and GPU usage

License:        GPLv3
URL:            https://gitlab.com/mission-center-devs/mission-center
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/-/archive/v%{version}/mission-center-v%{version}.tar.gz

# 1. Build Systems & Language Toolchains
BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  rustc
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  blueprint-compiler

# 2. GNOME / Desktop Integration Tools
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gtk-update-icon-cache
BuildRequires:  libappstream-glib

# 3. System Libraries (for Magpie & Mission Center)
BuildRequires:  systemd-devel
BuildRequires:  libinput-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libdrm-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libadwaita-devel

Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Mission Center is a system monitor written in Rust using GTK4 and Libadwaita.
It provides a highly detailed view of system performance, including per-thread 
CPU usage and hardware-accelerated GPU monitoring.

%prep
%autosetup -n mission-center-v%{version}

git init
git remote add origin %{url}
git fetch --depth 1 origin v%{version}
git checkout -f FETCH_HEAD
git submodule update --init --recursive

%build
export CARGO_NET_OFFLINE=false
export RUSTFLAGS="-C opt-level=z -C codegen-units=1 -C lto=fat -C embed-bitcode=yes -C strip=symbols"
%meson -Dflatpak=false --wrap-mode=nodownload
%meson_build

%install
%meson_install
strip --strip-unneeded %{buildroot}%{_bindir}/%{name}
strip --strip-unneeded %{buildroot}%{_bindir}/%{name}-magpie
%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml

%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/%{name}-magpie
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_metainfodir}/*.xml
%doc README.md

%changelog
* Thu Apr 30 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.1.0-1
- Initial RPM release for Fedora from GitLab source
