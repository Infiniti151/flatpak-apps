%global         app_id        io.github.leolost2605.emergency-alerts
%global         forgeurl      https://github.com/leolost2605/emergency-alerts
%global         tag           %{version}

Name:           emergency-alerts
Version:        2.1.0
Release:        1%{?dist}
Summary:        Receive emergency alerts
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  appstream
BuildRequires:  pkgconfig(granite-7)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libportal)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(shumate-1.0)
BuildRequires:  valac

Requires:       hicolor-icon-theme

%description
Emergency Alerts is a simple app that sends you alerts for your locations. Supported countries include Germany, the US (only weather alerts) and Ukraine (only air raid alerts) with more countries coming soon!

Features:
- Receive flood and weather warnings
- Receive alerts from your local civil protection authority
- Quickly view alerts for your favorite locations on the dashboard
- View alerts from all over the world on the map
- Get notifications when new alerts are issued for your saved locations
- Support for Germany, the US (only weather alerts) and Ukraine (only air raid alerts) with more countries coming soon

%prep
%forgesetup

%build
%meson -Dadwaita=true
%meson_build

%install
%meson_install
%find_lang %{app_id}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{app_id}.lang
%license COPYING
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_metainfodir}/*.metainfo.xml


%changelog
* Sat Nov 14 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 2.1.0-1
- Enable alerts for your current location and the app will follow you, showing alerts as long as you're in a supported area. This release also brings quality-of-life improvements that make it easier to add locations and share alert information.
- Highlights:
- Get alerts for your current location
- Select and copy alert descriptions to share them easily
- Click a fact to copy it to the clipboard
- Add locations more easily with the new location dialog
- Added metadata about supported device form factors

