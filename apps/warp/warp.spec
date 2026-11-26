%if 0%{?eln}
%global         debug_package       %{nil}
%endif
%global         app_id              app.drey.Warp
%global         tag                 v%{version}

Name:           warp
Version:        1.0.0
Release:        1%{?dist}
Summary:        Fast and secure file transfer
License:        GPL-3.0-only
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            https://gitlab.gnome.org/World/warp

BuildRequires:  meson >= 1.1.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  git-core
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel
BuildRequires:  itstool
BuildRequires:  pkgconfig(gio-2.0) >= 2.82.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.82.0
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 1.20
BuildRequires:  pkgconfig(gtk4) >= 4.20.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8

Requires:       hicolor-icon-theme
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugins-bad-free

%description
Warp allows you to securely send files to each other via the internet or local network by exchanging a word-based code.

The best transfer method will be determined using the “Magic Wormhole” protocol which includes local network transfer if possible.

Features
- Send files between multiple devices
- Every file transfer is encrypted
- Directly transfer files on the local network if possible
- An internet connection is required
- QR Code support
- Compatibility with the Magic Wormhole command line client and all other compatible apps

%prep
rm -rf %{name}-%{version}
git clone --depth 1 --branch %{tag} %{url}.git %{name}-%{version}
rm -rf %{name}-%{version}/.git
%setup -T -D -n %{name}-%{version}

# fix gresource path lookup
sed -i 's|from_appdata("app/drey|from_appdata("/app/drey|' src/ui/window.rs

%conf
%meson

%build
%meson_build
env CARGO_HOME=%{_vpath_builddir}/cargo-home cargo tree -e normal --prefix none --format '{p}: {l}' | sed -E 's/ \(\*\)$//; s/ \(\/[^)]*\)//' | sort -u > LICENSE.dependencies

%install
%meson_install
%find_lang %{name} --with-gnome

%check
%meson_test

%files -f %{name}.lang
%license LICENSE LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_dbusservicesdir}/%{app_id}.service
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Thu Nov 26 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.0.0-1
- Version 1.0.0
- Use new libadwaita shortcuts dialog
- Update to the GNOME 50 runtime
- Translation Updates
- Remove unused flatpak permission
