%global         app_id          io.missioncenter.MissionCenter
%global         forgeurl        https://gitlab.com/mission-center-devs/mission-center
%global         tag             v%{version}

%global         debug_package   %{nil}
%global         __spec_install_post /usr/lib/rpm/brp-compress
%global         build_cc        clang
%global         build_cxx       clang++
%global         nethogs_bin     %{_bindir}/nethogs
%global         powercap_rules  %{_sysconfdir}/udev/rules.d/99-powercap.rules

Name:           missioncenter
Version:        1.2.0
Release:        1%{?dist}
Summary:        Monitor your CPU, Memory, Disk, Network and GPU usage
License:        GPLv3
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

# 1. Build Systems & Language Toolchains
%if 0%{?fedora} && ! 0%{?eln}
BuildRequires:  upx
%endif
BuildRequires:  git-core
BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  clang
BuildRequires:  lld
BuildRequires:  compiler-rt
BuildRequires:  rustc
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  forge-srpm-macros
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

Requires:       nethogs
Requires:       lm_sensors
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Mission Center is a system monitor written in Rust using GTK4 and Libadwaita.
It provides a highly detailed view of system performance, including per-thread
CPU usage and hardware-accelerated GPU monitoring.

%prep
%forgesetup

# Initialize Git context to fetch submodules (required for CI builds from forge tarballs)
if [ ! -d ".git" ]; then
    git init -q
    git remote add origin %{forgeurl}
    git fetch -q --depth 1 origin %{tag}
    git checkout -q -f FETCH_HEAD
fi
git submodule update --init --recursive

%build
export CARGO_NET_OFFLINE=false
export CC=%{build_cc}
export CXX=%{build_cxx}
export LDFLAGS="-fuse-ld=lld"
export RUSTFLAGS="$RUSTFLAGS -C linker=clang -C link-arg=$LDFLAGS -C lto=fat -C embed-bitcode=yes -C opt-level=z -C strip=symbols"

%meson \
  -Db_lto=true \
  -Dflatpak=false

%meson_build

%install
%meson_install
strip --strip-unneeded %{buildroot}%{_bindir}/%{name}
strip --strip-unneeded %{buildroot}%{_bindir}/%{name}-magpie
%if 0%{?fedora} && ! 0%{?eln}
upx --best --lzma %{buildroot}%{_bindir}/%{name}
upx --best --lzma %{buildroot}%{_bindir}/%{name}-magpie
%endif
%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml

%postun
if [ $1 -eq 0 ]; then
    if [ -x %{nethogs_bin} ]; then
        setcap -r %{nethogs_bin} 2>/dev/null || :
    fi

    if [ -f %{powercap_rules} ]; then
        rm -f %{powercap_rules}
        udevadm control --reload-rules 2>/dev/null || :
        udevadm trigger --subsystem-match=powercap 2>/dev/null || :
    fi
fi

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-magpie
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_metainfodir}/*.xml

%changelog
* Sun Jul 26 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.2.0-1
- This release brings a long-requested Battery page, a big overhaul of the graphing backend, per-partition disk usage, and much smarter app detection, alongside a healthy pile of quality-of-life features and bug fixes.
- Read the full release notes [here](https://gitlab.com/mission-center-devs/mission-center/-/wikis/Release-Notes/v1.2.0).

* Fri May 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.1.0-1
- Release notes available [here](https://gitlab.com/mission-center-devs/mission-center/-/wikis/Release-Notes/v1.1.0)