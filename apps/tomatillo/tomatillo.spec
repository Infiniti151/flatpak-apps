%global         app_id          io.github.diegopvlk.Tomatillo
%global         forgeurl        https://github.com/diegopvlk/Tomatillo
%global         tag             v%{version}

Name:           tomatillo
Version:        1.1.1
Release:        1%{?dist}
Summary:        Focus better, work smarter
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildArch:      noarch

# Compilers and Build Tools
BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  blueprint-compiler
BuildRequires:  python3-devel
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros

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
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme
Requires:       python3
Requires:       python3-gobject

%description
Tomatillo is a Pomodoro Timer app for your productivity tasks. Work for a set time, then take a short break. After some cycles, take a longer break.

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%py3_shebang_fix %{buildroot}%{_bindir}/%{name}
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_appsdir}/*.desktop
%{_metainfodir}/*.xml
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service

%changelog
* Tue Jun 23 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.1.1-1
- Update to v1.1.1

* Thu May 28 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.1.0-1
- Update to v1.1.0

* Thu May 14 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.0.5-1
- Update to v1.0.5

* Fri May 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.0.4-1
- Update to v1.0.4
