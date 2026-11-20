%global         app_id        io.gitlab.liferooter.TextPieces
%global         upstream_name textpieces
%global         forgeurl      https://gitlab.com/liferooter/textpieces
%global         tag           %{version}

Name:           text-pieces
Version:        4.3.2
Release:        1%{?dist}
Summary:        Developer's scratchpad
License:        GPL-3.0-or-later AND MIT AND Apache-2.0 AND Unicode-3.0 AND 0BSD AND MPL-2.0
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-2.0) >= 2.80
BuildRequires:  pkgconfig(glib-2.0) >= 2.80
BuildRequires:  pkgconfig(gtk4) >= 4.20
BuildRequires:  pkgconfig(gtksourceview-5) >= 5.10
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.0
BuildRequires:  rustc

Requires:       hicolor-icon-theme

%description
Powerful scratchpad with ability to perform a lot of text transformations, such as:
- Calculate hashes
- Encode text
- Decode text
- Remove trailing spaces and lines
- Count lines, symbols and words
- Format JSON and XML
- Escape and unescape strings
- Convert JSON to YAML and vice versa
- Filter lines
- And so on.

The application is extendable with your own script-based actions.

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{upstream_name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{upstream_name}.lang
%license LICENSE LICENSES
%doc README.md
%{_bindir}/%{upstream_name}
%{_datadir}/%{upstream_name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml


%changelog
* Fri Nov 20 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 4.3.2-1
- Dependencies are updated

