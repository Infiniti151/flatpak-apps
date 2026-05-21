%if 0%{?eln}
%define _empty_manifest_terminate_build 0
%endif

Name:           words
Version:        0.7.9
Release:        1%{?dist}
Summary:        A word puzzle game
License:        GPL-3.0-only
URL:            https://codeberg.org/petsoi/words
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson >= 1.1.0
BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.18.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5.5

%description
An elegant word game puzzle built natively using
Rust, GTK4, and Libadwaita.

%prep
%autosetup -n %{name} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

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
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/*.xml
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/%{name}/
%{_datadir}/word-lists/
%{_datadir}/icons/hicolor/*/*/*

%changelog
* Thu May 21 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.7.9-1
- Initial release 0.7.9