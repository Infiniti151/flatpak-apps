%define debug_package %{nil}

Name:           concessio
Version:        0.0.0
Release:        1%{?dist}
Summary:        Understand and convert UNIX file permissions
License:        GPL-3.0-or-later
URL:            https://github.com/ronniedroid/concessio
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  meson
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  gjs
BuildRequires:  blueprint-compiler
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       gjs
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Concessio is a simple utility to help you understand UNIX file permissions.
It allows you to convert between symbolic and numeric representations 
(e.g., rwx------ to 700) using an intuitive GTK4 interface.

%prep
%autosetup

%build
%meson -Dforce_fallback_for=blueprint-compiler
%meson_build

%install
%meson_install
%find_lang io.github.ronniedroid.concessio %{name}.lang

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.xml

%files -f %{name}.lang
%{_bindir}/io.github.ronniedroid.concessio
%{_datadir}/io.github.ronniedroid.concessio/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*.svg
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/metainfo/*.xml
%{_datadir}/dbus-1/services/*.service
%license LICENSE
%doc README.md
