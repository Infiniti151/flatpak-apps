Name:           eyedropper
Version:        2.2.1
Release:        1%{?dist}
Summary:        Pick and format colors from your desktop
License:        GPL-3.0-or-later
URL:            https://github.com/finefindus/eyedropper
BugURL:	        https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pkgconfig(gtk4) >= 4.22.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  blueprint-compiler >= 0.20
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext

%description
A powerful color picker for the GNOME desktop that allows you to pick colors 
from any pixel on your screen and format them for your development needs.

%prep
%autosetup

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson -Dprofile=default
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg
%{_metainfodir}/*.metainfo.xml
%{_datadir}/dbus-1/services/*.service
%{_datadir}/gnome-shell/search-providers/*.search-provider.ini

%changelog
* Sat May 09 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 2.2.1-1
- Initial build of Eyedropper 2.2.1