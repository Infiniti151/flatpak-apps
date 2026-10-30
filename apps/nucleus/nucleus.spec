%global         app_id          page.codeberg.lo_vely.Nucleus
%global         forgeurl        https://codeberg.org/lo-vely/nucleus
%global         tag             v%{version}

Name:           nucleus
Version:        3
Release:        1%{?dist}
Summary:        Browse the chemical elements
License:        GPLv3+
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildArch:      noarch

BuildRequires:  meson >= 1.0.0
BuildRequires:  python3-devel
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  forge-srpm-macros
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  gettext
BuildRequires:  git-core

Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Nucleus gives you the ability to view the periodic table of the elements, as well as a variety of properties for each element, some with a visual representation. There is also search functionality which gives you the elements in a list for efficient viewing

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_metainfodir}/*.xml
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/dbus-1/services/*.service
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Tue May 19 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v3-1
- Aligned the "no-results" page to the top
- Added theoretical indicator to Ununennium
- Updated boil, electronegativity pauling and ionization energies properties for Ununennium
- Add Chemistry, Science and Education categories to the desktop file, by @radmorecameron
- Updated to GNOME 50 runtime
- Added French Translation, by @MXC480
- Added Italian translation, by Davide Ferracin

