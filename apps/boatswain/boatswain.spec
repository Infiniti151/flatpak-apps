%global         app_id        com.feaneron.Boatswain
%global         tag           %{version}

Name:           boatswain
Version:        0
Release:        1%{?dist}
Summary:        Control your Elgato Stream Decks
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            https://gitlab.gnome.org/World/boatswain

BuildRequires:  meson >= 0.59
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(glycin-2) >= 2.0.alpha.4
BuildRequires:  pkgconfig(graphene-gobject-1.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(hidapi-libusb)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9.0
BuildRequires:  pkgconfig(libdex-1)
BuildRequires:  pkgconfig(libpeas-2)
BuildRequires:  pkgconfig(libportal-gtk4)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libsoup-3.0)

Requires:       hicolor-icon-theme

%description
Boatswain allows you to control Elgato Stream Deck devices.

With Boatswain you will be able to:
- Organize your actions in pages and profiles
- Set custom icons to actions
- Control your music player
- Play sound effects during your streams
- Control OBS Studio using Stream Deck (requires the obs-websocket extension)
- Send network requests
- Keep track of your gaming score
- Open files and launch applications

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains the headers and GObject Introspection
data needed to develop against libboatswain.

%prep
rm -rf %{name}-%{version}
git clone --depth 1 --branch %{tag} %{url}.git %{name}-%{version}
rm -rf %{name}-%{version}/.git
%setup -T -D -n %{name}-%{version}

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}

rm -f %{buildroot}%{_scalableiconsdir}/%{app_id}.Devel.svg

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/girepository-1.0/Bs-0.typelib
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml

%files devel
%{_includedir}/%{name}/
%{_includedir}/bs-enum-types.h
%{_datadir}/gir-1.0/Bs-0.gir