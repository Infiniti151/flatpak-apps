%global         app_id        io.github.tfuxu.Halftone
%global         forgeurl      https://github.com/tfuxu/Halftone
%global         tag           %{version}

Name:           halftone
Version:        0.7.1
Release:        1%{?dist}
Summary:        Dither your images
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59.0
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4) >= 4.12.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5.0
BuildRequires:  pkgconfig(pygobject-3.0) >= 3.48.0

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3-gobject

%description
A simple Libadwaita app for lossy image compression using dithering technique. Give your images a pixel art-like style and reduce the file size in the process with Halftone.

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}
%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc CHANGELOG.md README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Sat Nov 28 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.7.1-1
- Test
