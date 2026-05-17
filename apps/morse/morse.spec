%if 0%{?eln}
%define _empty_manifest_terminate_build 0
%endif

Name:           morse
Version:        1.3.0
Release:        1%{?dist}
Summary:        Morse is an open-source program for learning Morse code
License:        GPL-3.0-only
URL:            https://github.com/teacond/Morse
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson >= 1.0.0
BuildRequires:  cargo
BuildRequires:  rustc
BuildRequires:  pkgconfig
BuildRequires:  gettext
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(gtk4) >= 4.22
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9
BuildRequires:  pkgconfig(alsa)

Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Morse is an app for learning Morse code and training High Speed Telegraphy skills written in Rust language using GTK4 and Adwaita.

%prep
%autosetup -n Morse-%{version}
sed -i "/run_command('git'/d" meson.build

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson -Dprofile=default
%meson_build

%install
%meson_install

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.xml

%files -f %{name}.lang
%license COPYING.md
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg
%{_datadir}/metainfo/*.xml
%{_datadir}/morse/

%changelog
* Sun May 17 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.3.0-1
- What's Changed
- Small PL l10n cleanups by @dawkagaming in https://github.com/teacond/Morse/pull/6
- Initial packaging for Debian/Ubuntu by @dawkagaming in https://github.com/teacond/Morse/pull/7
- Add Debian packaging to workflow by @teacond in https://github.com/teacond/Morse/pull/8
- Add saving latest text speed to the gschema by @teacond in https://github.com/teacond/Morse/pull/14
- Add alphabet playing ability by @teacond in https://github.com/teacond/Morse/pull/15
- Alphabet enhancement by @teacond in https://github.com/teacond/Morse/pull/16
- New Contributors
- @dawkagaming made their first contribution in https://github.com/teacond/Morse/pull/6
- *Full Changelog**: https://github.com/teacond/Morse/compare/v1.2.0...v1.3.0

