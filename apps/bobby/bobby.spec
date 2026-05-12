%if 0%{?eln}
%define _empty_manifest_terminate_build 0
%endif

Name:           bobby
Version:        0.0.0
Release:        1%{?dist}
Summary:        A Rust-based SQLite database viewer for GNOME
License:        GPL-3.0-or-later
URL:            https://github.com/hbons/Bobby
BugURL:	        https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson >= 1.1
BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext

%description
Bobby lets you open SQLite database files (.db, .sqlite) and browse the tables inside. Handy for app development or inspecting downloaded databases.

%prep
%autosetup -n Bobby-%{version}

%build
export CARGO_HOME="$(pwd)/cargo-home"
%meson -Dnightly=false
%meson_build

%install
export CARGO_HOME="$(pwd)/cargo-home"
%meson_install

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg