%global         app_id        net.ffkkinos.Wildcard
%global         forgeurl      https://gitlab.gnome.org/World/Wildcard
%global         tag           v%{version}

Name:           wildcard
Version:        0.3.5
Release:        1%{?dist}
Summary:        Test your regular expressions
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  cairo-devel
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pango-devel
BuildRequires:  pkgconfig(gtk4) >= 4.10
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5
BuildRequires:  rustc

Requires:       cairo
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       pango

%description
Wildcard gives you a nice and simple to use interface to test/practice regular expressions.

%prep
%forgesetup
mkdir -p cargo-home

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/dbus-1/services/*.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.3.5-1
- Test
