%if 0%{?eln}
%global         _empty_manifest_terminate_build 0
%endif

%global         app_id io.gitlab.news_flash.NewsFlash
%global         __brp_mangle_shebangs %{nil}
%global         debug_package %{nil}
%global         __spec_install_post /usr/lib/rpm/brp-compress

Name:           newsflash
Version:        0
Release:        1%{?dist}
Summary:        Modern feed reader designed for the GNOME desktop
License:        GPLv3
URL:            https://gitlab.com/news-flash/news_flash_gtk
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/-/archive/v.%{version}/news_flash_gtk-v.%{version}.tar.gz

# Compression Tools
%if 0%{?fedora} && ! 0%{?eln}
BuildRequires:  upx
%endif

# Build tools & utilities
BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  clang-devel
BuildRequires:  gettext
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

# Development libraries (-devel equivalent pkgconfig dependencies)
BuildRequires:  pkgconfig(glib-2.0) >= 2.70
BuildRequires:  pkgconfig(gio-2.0) >= 2.70
BuildRequires:  pkgconfig(gtk4) >= 4.12.0
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.4.0
BuildRequires:  pkgconfig(webkitgtk-6.0) >= 2.42.0
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(clapper-gtk-0.0)

# Runtime Requirements
Requires:       hicolor-icon-theme
Requires:       xdg-utils
Requires:       clapper
Requires:       libmicrodns
Requires:       libpeas

%description
NewsFlash is a modern RSS feed reader designed to work with web-based feed accounts.
It combines the advantages of web-based services with desktop apps: notifications,
fast UI, background sync, and offline support.

%prep
%autosetup -n news_flash_gtk-v.%{version}
mkdir -p cargo-home

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson -Dprofile=default
%meson_build

%install
%meson_install

# Strip unneeded symbols and compress binary using UPX
strip --strip-unneeded %{buildroot}%{_bindir}/%{app_id}
%if 0%{?fedora} && ! 0%{?eln}
upx --best --lzma %{buildroot}%{_bindir}/%{app_id}
%endif

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{app_id}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{app_id}.appdata.xml

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}*.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{app_id}-symbolic.svg
%{_datadir}/dbus-1/services/%{app_id}.service
%{_metainfodir}/%{app_id}.appdata.xml