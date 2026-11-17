%global         app_id                             com.belmoussaoui.Decoder
%global         tag                                %{version}
%global         __brp_mangle_shebangs_exclude_from ^/usr/src/debug/.*$

Name:           decoder
Version:        0.10.0
Release:        1%{?dist}
Summary:        Scan and generate QR codes
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            https://gitlab.gnome.org/World/decoder

BuildRequires:  meson >= 1.7
BuildRequires:  ninja-build
BuildRequires:  git-core
BuildRequires:  appstream
BuildRequires:  cairo-devel
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
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

%description
Fancy yet simple QR Codes scanner and generator.

Features:
- QR Code generation
- Scanning with a camera
- Scanning from a screenshot
- Parses and displays QR code content when possible

%prep
rm -rf %{name}-%{version}
git clone --depth 1 --branch %{tag} %{url}.git %{name}-%{version}
rm -rf %{name}-%{version}/.git
%setup -T -D -n %{name}-%{version}
mkdir -p cargo-home

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test validate-desktop 'Validate schema file' validate-metainfo cargo-test
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.10.0-1
- Minor release.
- Focus text when app starts
- Update translations

