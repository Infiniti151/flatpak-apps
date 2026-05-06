Name:           tomatillo
Version:        0.1.0
Release:        1%{?dist}
Summary:        Tomatillo is a Pomodoro Timer app for your productivity tasks.
License:        GPL-3.0-or-later
URL:            https://github.com/diegopvlk/Tomatillo
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildArch:      noarch

# Build Requirements
BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  blueprint-compiler
BuildRequires:  python3-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  appstream

# Runtime Requirements
Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Tomatillo helps to set individual timer durations for focus sessions, short breaks, and long breaks. It can also adjust the amount of cycles before a long break and automatically begin the next focus/break cycle.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%{_bindir}/tomatillo
%{_datadir}/tomatillo/
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/*.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/dbus-1/services/*.service

%changelog
* Thu May 07 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.1.0-1
- Update to 0.1.0-1