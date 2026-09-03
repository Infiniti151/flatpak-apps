%global         app_id        xyz.safeworlds.hiit
%global         app_name      hiit
%global         forgeurl      https://gitlab.gnome.org/World/exercise-timer
%global         tag           v%{version}

Name:           exercise-timer
Version:        1.10.0
Release:        1%{?dist}
Summary:        Train and rest with high intensity
License:        GPL-3.0
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59
BuildRequires:  ninja-build
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(gtk4) >= 4.0.0
BuildRequires:  pkgconfig(json-glib-1.0) >= 1.0.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.0.0
BuildRequires:  valac

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita

%description
Exercise Timer is a simple utility to conduct high intensity interval training. Following a short preparation period, a prescribed number of exercise sets are played. In between each exercise, there is a resting period. The app does not make an assumption about the kind of the exercise.

Features:
- Save and recall presets containing the number of sets and the duration of the exercise, rest and preparation periods.
- A beeping sound is played at- and prior to each transition.
- The volume of the sound can be adjusted.
- Light and dark mode follows the system's setting.

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{app_name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{app_name}.lang
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/%{app_name}
%{_datadir}/%{app_name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_metainfodir}/*.metainfo.xml

%changelog
* Thu Sep 03 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.10.0-1
- Test Build
