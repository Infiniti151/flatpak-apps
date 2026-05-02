%define         debug_package %{nil}

Name:           extension-manager
Version:        0.6.5
Release:        1%{?dist}
Summary:        A utility for browsing and installing GNOME Shell Extensions
License:        GPL-3.0-or-later
URL:            https://github.com/mjakeman/extension-manager
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.alpha
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  blueprint-compiler
BuildRequires:  libbacktrace-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

%description
A native desktop application for managing GNOME Shell Extensions.

%prep
%autosetup -n %{name}-%{version}

%build
%meson
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
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*.svg
%{_metainfodir}/*.metainfo.xml
%{_datadir}/glib-2.0/schemas/*.gschema.xml

%changelog
* Sat May 02 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.6.5-1
- Update to 0.6.5