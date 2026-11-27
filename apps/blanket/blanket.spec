%global         app_id        com.rafaelmardojai.Blanket
%global         forgeurl      https://github.com/rafaelmardojai/blanket
%global         tag           %{version}

Name:           blanket
Version:        0.8.0
Release:        1%{?dist}
Summary:        Listen to ambient sounds
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3
Requires:       python3-gobject

%description
Improve focus and increase your productivity by listening to different ambient sounds

Also can help you to fall asleep in a noisy environment.

Features:
- Save presets
- Add custom sounds
- Auto start in background
- MPRIS integration

Included Sounds in the App:
- Birds
- Boat
- City
- Coffee Shop
- Fireplace
- Pink Noise
- Rain
- Summer Night
- Storm
- Stream
- Train
- Waves
- White Noise
- Wind

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
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Fri Nov 27 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.8.0-1
- Allow renaming custom sounds
- Make suspension inhibition optional and disabled by default
- Bug fixes
