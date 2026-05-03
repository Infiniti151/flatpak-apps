Name:           pods
Version:        3.0.0
Release:        1%{?dist}
Summary:        A powerful Podman manager for GNOME
License:        GPL-3.0-or-later
URL:            https://github.com/marhkb/Pods
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson >= 0.59
BuildRequires:  gcc
BuildRequires:  rust-packaging
BuildRequires:  cargo
BuildRequires:  blueprint-compiler
BuildRequires:  pkgconfig(gtk4) >= 4.18.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.7
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(vte-2.91-gtk4)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       podman
Requires:       hicolor-icon-theme

%description
Pods is a GTK application that allows you to manage podman 
containers, pods, and images with a clean, native GNOME interface.

%prep
%autosetup

%build
%meson \
    -Dprofile=default
%meson_build

%install
%meson_install
%find_lang %{name}

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*.svg
%{_metainfodir}/*.metainfo.xml
%{_datadir}/glib-2.0/schemas/*.gschema.xml

%changelog
* Sun May 03 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 3.0.0-1
- Update to 3.0.0