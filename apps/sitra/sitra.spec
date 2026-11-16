%global         app_id        io.github.sitraorg.sitra
%global         forgeurl      https://github.com/sitraorg/sitra
%global         tag           v%{version}

Name:           sitra
Version:        0.2.0
Release:        1%{?dist}
Summary:        Get fonts from online sources
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.4
BuildRequires:  pkgconfig(libsitra-0.1)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(webkitgtk-6.0)
BuildRequires:  valac

Requires:       hicolor-icon-theme

%description
Get your fonts from online sources with a sleek, friendly user interface. Sitra provides a seamless experience for installing, uninstalling and previewing fonts.
- List fonts available on Google Fonts
- Preview the fonts using Fontsource CDN for privacy
- Get code to use the font in your project, via CDN or npm from fontsource
- Download the fonts on your device in ttf format from google
- Filter font by category using the toggle buttons or by family and subset using search

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{app_id}

%check
%meson_test
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{app_id}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml
%{_fontsdir}/%{app_id}/


%changelog
* Mon Nov 16 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.2.0-1
- Updated GNOME runtime to version 51

