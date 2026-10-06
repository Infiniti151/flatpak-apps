%global app_id         io.github.ronniedroid.concessio
%global forgeurl       https://github.com/ronniedroid/concessio
%global tag            v%{version}

Name:           concessio
Version:        1.0.0
Release:        1%{?dist}
Summary:        Understand and convert UNIX file permissions
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  /usr/bin/node
BuildRequires:  /usr/bin/npm
BuildRequires:  meson
BuildRequires:  gjs
BuildRequires:  forge-srpm-macros
BuildRequires:  blueprint-compiler
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  libgee-devel
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
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{app_id} %{name}.lang

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_metainfodir}/*.metainfo.xml

%changelog
* Sun Oct 04 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.0.0-1
- Redesigned the file opening workflow
- Added drag and drop support for opening files
- Added support for changing file permissions, with the ability to undo changes
- Improved the umask calculator to calculate from umask, file, or directory permissions
- Improved accessibility throughout the app
- Improved input validation and editing behavior
- Updated translations

* Fri May 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.3.0-1
- Update to v0.3.0

