Name:           tomatillo
Version:        1.1.0
Release:        1%{?dist}
Summary:        Tomatillo is a Pomodoro Timer app for your productivity tasks.
License:        GPL-3.0-or-later
URL:            https://github.com/diegopvlk/Tomatillo
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildArch:      noarch

# Compilers and Build Tools
BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  blueprint-compiler
BuildRequires:  python3-devel

# Desktop Libraries (Development Files)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

# Validation and Integration Tools
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  appstream
BuildRequires:  gtk-update-icon-cache

# Runtime Requirements
Requires:  gtk4
Requires:  libadwaita
Requires:  hicolor-icon-theme

%description
Tomatillo helps to set individual timer durations for focus sessions, short breaks, and long breaks. It can also adjust the amount of cycles before a long break and automatically begin the next focus/break cycle.

%prep
%autosetup -n Tomatillo-%{version}

%build
%meson
%meson_build

%install
%meson_install
python3 %{_rpmconfigdir}/redhat/pathfix.py -pni "%{__python3}" %{buildroot}%{_bindir}/tomatillo
%find_lang %{name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/tomatillo
%{_datadir}/tomatillo/
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/*.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/dbus-1/services/*.service

%changelog
* Thu May 28 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.1.0-1
- Update to v1.1.0

* Thu May 14 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.0.5-1
- Update to v1.0.5

* Fri May 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.0.4-1
- Update to v1.0.4
