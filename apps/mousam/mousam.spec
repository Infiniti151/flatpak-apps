%global         app_id        io.github.amit9838.mousam
%global         forgeurl      https://github.com/amit9838/mousam
%global         tag           v%{version}

Name:           mousam
Version:        3.1.0
Release:        1%{?dist}
Summary:        Weather at a glance
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.61.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel
BuildRequires:  python3-gobject
BuildRequires:  python3-requests
BuildRequires:  tzdata

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3
Requires:       python3-gobject
Requires:       python3-requests

%description
Mousam shows the current weather and forecasts for the places you care about, with hourly and 7-day graphs, air quality and a short overview of the hours ahead. All data comes from Open-Meteo, with no account needed.

Features:
- Current temperature, feels like, humidity, wind, pressure, UV index, dew point and visibility
- A one-line overview of the coming hours, such as when rain starts, also sent as a notification while the window is out of sight
- Hourly temperature, wind and precipitation graphs
- Tomorrow and 7-day forecasts with temperature ranges, chance of rain and snow
- Air quality (US and EU AQI) with pollutants, pollen and health advice
- The sun's path through the day, moon phase and twilight
- Saved locations with their weather and local time, in the order you choose
- Compact mode for a minimal, focused view
- Option to keep running in the background when the window is closed
- Dynamic backgrounds that follow the weather, and a choice of default or Material icons
- Metric and imperial units, and 12- or 24-hour clock

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
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_hicolordir}/scalable/default_icons/
%{_hicolordir}/scalable/material_icons/
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.appdata.xml

%changelog
* Wed Nov 25 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 3.1.0-1
- Improved weather overview and fixes
- Improved weather overview: combines related events, reminds less often, and describes the weather at sunrise and sunset.
- Notifications are on by default, one per topic.
- New app icon.
- Ctrl+Shift+R refreshes without cached data.
- Faster loading on networks with broken IPv6.
- Fixed sunrise and sunset times west of UTC, precipitation bars in inches, and the hourly list.
- Updated translations.
