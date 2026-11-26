%global         app_id        io.github.diegopvlk.Dosage
%global         forgeurl      https://github.com/diegopvlk/Dosage
%global         tag           v%{version}

Name:           dosage
Version:        2.1.9
Release:        1%{?dist}
Summary:        Keep track of your treatments
License:        GPL-3.0-only
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  gjs
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       gtk4
Requires:       gjs
Requires:       hicolor-icon-theme
Requires:       libadwaita

%description
Easily manage and track treatments with Dosage: notifications, history, multiple doses, flexible frequency, customization, stock monitoring, and duration control

Features:
- Notifications — Get reminders at the right time
- History — See which medications you took, skipped or missed
- Dosage management — Multiple doses with different times
- Frequency modes — Every day, specific days, cycle or just when necessary
- Color and icon — Give a shape for your treatment
- Inventory tracking — Monitor your stock and get reminded when it's low
- Duration — Define the start and end dates

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.appdata.xml

%changelog
* Thu Nov 26 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 2.1.9-1
- Added Greek translation
- Updated translations
- Updated GNOME runtime to 51
- Fixed "Ended Last" sorting so only ended treatments move to the bottom (@hazelcore)
