%global         app_id        com.jeffser.Popcorn
%global         forgeurl      https://github.com/Jeffser/Popcorn
%global         tag           %{version}

# bundled Python wheels (pinned to what the Flatpak manifest uses)
%global         segno_ver       1.6.6
%global         segno_sha256    28c7d081ed0cf935e0411293a465efd4d500704072cdb039778a2ab8736190c7
%global         strenum_ver     0.4.15
%global         strenum_sha256  a30cda4af7cc6b5bf52c8055bc4bf4b2b6b14a93b574626da33df53cf7740659
%global         mpris_ver       0.10.0
%global         mpris_sha256    14b3c2fd057ca5cf8110d4fe0256a5bc6ad1ccf23474daf31c44728416e6cbbc
%global         mpris_tag       v0.9.1

Name:           popcorn
Version:        0.2.2
Release:        1%{?dist}
Summary:        Explore Jellyfin with style
# GPL-3.0-or-later: Popcorn; LGPL-3.0-only: mpris_server; BSD-3-Clause: segno; MIT: StrEnum
License:        GPL-3.0-or-later AND LGPL-3.0-only AND BSD-3-Clause AND MIT
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}
# Not packaged in Fedora; bundle the pure-Python wheels pinned by the Flatpak manifest
Source1:        https://files.pythonhosted.org/packages/py3/s/segno/segno-%{segno_ver}-py3-none-any.whl
Source2:        https://files.pythonhosted.org/packages/py3/S/StrEnum/StrEnum-%{strenum_ver}-py3-none-any.whl
Source3:        https://github.com/Jeffser/mpris_server/releases/download/%{mpris_tag}/mpris_server-%{mpris_ver}-py3-none-any.whl

BuildRequires:  meson >= 1.0.0
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3-gobject
Requires:       python3-requests
Requires:       python3-pillow
Requires:       python3-pycountry
Requires:       python3-pydbus
Requires:       python3-emoji
Requires:       python3-unidecode

Provides:       bundled(python3dist(segno)) = %{segno_ver}
Provides:       bundled(python3dist(strenum)) = %{strenum_ver}
Provides:       bundled(python3dist(mpris-server)) = %{mpris_ver}

%description
A modern Jellyfin client

Features
- Dedicated pages for all types of elements
- VTT subtitle support
- Player gestures
- Picture-in-Picture playback
- Trickplay (scrobbing thumbnails)
- Intro / Outro skipper
- Cool interface

%prep
%forgesetup
# the bundled wheels must match what the Flatpak manifest pins (release assets can be replaced)
echo "%{segno_sha256}  %{SOURCE1}" | sha256sum -c -
echo "%{strenum_sha256}  %{SOURCE2}" | sha256sum -c -
echo "%{mpris_sha256}  %{SOURCE3}" | sha256sum -c -

%build
%meson
%meson_build

%install
%meson_install
pip3 install --no-deps --no-index --ignore-installed --root-user-action=ignore --prefix=%{buildroot}%{_prefix} %{SOURCE1} %{SOURCE2} %{SOURCE3}
# segno installs a command-line script and manpage the app does not use
rm -f %{buildroot}%{_bindir}/segno
rm -f %{buildroot}%{_mandir}/man1/segno.1.gz

%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

%check
%meson_test
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/popcorn_search_provider
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_searchprovidersdir}/*.ini
%{_metainfodir}/*.metainfo.xml
%{python3_sitelib}/segno/
%{python3_sitelib}/segno-*.dist-info/
%{python3_sitelib}/strenum/
%{python3_sitelib}/StrEnum-*.dist-info/
%{python3_sitelib}/mpris_server/
%{python3_sitelib}/mpris_server-*.dist-info/

%changelog
* Sun Nov 15 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.2.2-1
- Initial Copr build