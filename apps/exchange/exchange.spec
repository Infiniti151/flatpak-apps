%global         app_id        io.github.shonebinu.Exchange
%global         forgeurl      https://github.com/shonebinu/Exchange
%global         tag           v%{version}

Name:           exchange
Version:        0.2.2
Release:        1%{?dist}
Summary:        Convert between XML and Blueprint
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel
BuildRequires:  python3-gobject
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(gtksourceview-5)

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       gtksourceview5
Requires:       python3
Requires:       python3-gobject

%description
Exchange lets you convert between GTK UI definition formats such as XML and Blueprint.

Features:
- Convert XML to Blueprint
- Convert Blueprint to XML
- Automatically detects format when pasting or opening files

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{name}
%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

%check
%meson_test
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{name}.lang
%license COPYING
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
* Mon Nov 16 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.2.2-1
- Test
