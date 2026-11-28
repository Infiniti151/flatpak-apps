%global         app_id        io.github.vmkspv.lenspect
%global         forgeurl      https://github.com/vmkspv/lenspect
%global         tag           v%{version}

Name:           lenspect
Version:        1.0.7
Release:        1%{?dist}
Summary:        Scan files for threats
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.2.0
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3-gobject

%description
A lightweight security threat scanner intended to make malware detection more accessible and efficient.

%prep
%forgesetup

# Remove strict gschema check
sed -i "s/'--strict', *//g" data/meson.build

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}
%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}_search_provider %{buildroot}%{_datadir}/%{name}/

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/{%{name},%{name}_search_provider}
%{_datadir}/%{name}
%{_appsdir}/{%{app_id}.desktop,%{app_id}.SearchProvider.desktop}
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_hicolordir}/scalable/actions/*-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_dbusservicesdir}/{%{app_id}.service,%{app_id}.SearchProvider.service}
%{_searchprovidersdir}/%{app_id}.search-provider.ini
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Sat Nov 28 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.0.7-1
- Updated GNOME runtime
- Added known filename
- Added crowdsourced AI results
- Added suggested threat label
- Added file reputation
- Added sandbox verdicts
- Added upload percentage
- Added selected file size
- Added clear history undo
- Minor code optimization/fixes
- ... (see upstream for full release notes)
