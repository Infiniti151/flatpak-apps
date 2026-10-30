%if 0%{?eln}
%global         _empty_manifest_terminate_build 0
%endif
%global         app_id          com.github.finefindus.eyedropper
%global         forgeurl        https://github.com/finefindus/eyedropper
%global         tag             v%{version}

Name:           eyedropper
Version:        2.2.1
Release:        1%{?dist}
Summary:        Pick and format colors
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  forge-srpm-macros
BuildRequires:  pkgconfig(gtk4) >= 4.22.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  blueprint-compiler >= 0.20
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext

%description
Enter or pick a color and view it in different formats.

Features
- Pick a Color
- Edit the viewed color in a simple HSL editor
- Enter a color in various formats
- Convert colors into other formats such as Hex, RGB, HSV, HSL, CMYK, XYZ, CIE-Lab…

%prep
%forgesetup

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson -Dprofile=default
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_metainfodir}/*.metainfo.xml
%{_datadir}/dbus-1/services/*.service
%{_datadir}/gnome-shell/search-providers/*.search-provider.ini

%changelog
* Sat May 09 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v2.2.1-1
- What's Changed
- * fix(i18n/it): remove additional translation in app name @espositofabian in https://github.com/FineFindus/eyedropper/pull/227
- New Contributors
- * @espositofabian made their first contribution in https://github.com/FineFindus/eyedropper/pull/227
- **Full Changelog**: https://github.com/FineFindus/eyedropper/compare/v2.2.0...v2.2.1

