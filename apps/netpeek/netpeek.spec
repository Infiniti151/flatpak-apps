%define app_id io.github.zingytomato.netpeek

Name:           netpeek
Version:        0.2.9
Release:        1%{?dist}
Summary:        Modern network scanner for GNOME

License:        GPL-3.0-or-later
URL:            https://github.com/ZingyTomato/NetPeek
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  python3-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       python3
Requires:       python3-gobject
Requires:       python3-nmap
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
NetPeek is a modern network scanner designed for the GNOME desktop, built with Python, GTK4, and Libadwaita.

%prep
%autosetup -n NetPeek-%{version}

%build
%meson
%meson_build

%install
%meson_install

%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/dbus-1/services/%{app_id}.service
%{_datadir}/metainfo/%{app_id}.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{app_id}-symbolic.svg

%changelog
* Fri Jul 24 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.2.9-1
- Release 0.2.9