%global         app_id        com.belmoussaoui.Decoder
%global         forgeurl      https://gitlab.gnome.org/World/decoder
%global         tag           %{version}

Name:           decoder
Version:        0.10.0
Release:        1%{?dist}
Summary:        Scan and generate QR codes
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.7
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  cairo-devel
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  libappstream-glib
BuildRequires:  pango-devel
BuildRequires:  pkgconfig(gio-2.0) >= 2.76
BuildRequires:  pkgconfig(glib-2.0) >= 2.76
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 1.20
BuildRequires:  pkgconfig(gtk4) >= 4.23
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.alpha
BuildRequires:  rustc

Requires:       cairo
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       pango
Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-bad

%description
Fancy yet simple QR Codes scanner and generator.

Features:
- QR Code generation
- Scanning with a camera
- Scanning from a screenshot
- Parses and displays QR code content when possible

%prep
%forgesetup

%build
%meson
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
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/dbus-1/services/*.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Thu Sep 24 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.10.0-1
- Test release
