%global         app_id        io.github.getnf.embellish
%global         forgeurl      https://github.com/getnf/embellish
%global         tag           v%{version}

Name:           embellish
Version:        1.2.0
Release:        1%{?dist}
Summary:        Install nerd fonts
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
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.4
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  valac

Requires:       hicolor-icon-theme

%description
User-friendly application designed for managing Nerd Fonts on your system. With a sleek GTK4 user interface enhanced by libadwaita, Embellish provides a seamless experience for installing, uninstalling and updating of Nerd Fonts.
- List all available Nerd Fonts
- Download and install a Font
- Uninstall an installed Font
- preview fonts
- Browse icons (icon's cheat sheet)
- Search fonts
- Read font's license(s)
- Add custom fonts
- Import and export custom fonts

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{app_id}

%check
%meson_test

%files -f %{app_id}.lang
%license LICENSE
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
* Mon Nov 16 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.2.0-1
- Updated to GNOME runtime 51
- Updated to NerdFonts V3.5.1
- Added the missing Devicons
- Other minor upstream fixes
- Fonts need to be reinstalled to be updated

