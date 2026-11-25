%global         app_id        org.gnome.design.IconLibrary
%global         tag           %{version}

Name:           icon-library
Version:        0.0.23
Release:        1%{?dist}
Summary:        Symbolic icons for your apps
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            https://gitlab.gnome.org/World/design/icon-library

BuildRequires:  meson >= 1.7
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  git-core
BuildRequires:  clippy
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.15.3
BuildRequires:  pkgconfig(gtksourceview-5) >= 5.0.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.alpha

Requires:       hicolor-icon-theme

%description
Find the right icon to use on your GNOME application.

%prep
rm -rf %{name}-%{version}
git clone --depth 1 --branch %{tag} %{url}.git %{name}-%{version}
rm -rf %{name}-%{version}/.git
%setup -T -D -n %{name}-%{version}

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}
env CARGO_HOME=.cargo cargo tree -e normal --prefix none --format '{p}: {l}' | sed -E 's/ \(\*\)$//; s/ \(\/[^)]*\)//' | sort -u > LICENSE.dependencies

%check
%meson_test

%files -f %{name}.lang
%license LICENSE.md LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_dbusservicesdir}/{%{app_id}.service,%{app_id}.SearchProvider.service}
%{_searchprovidersdir}/%{app_id}.search-provider.ini
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Wed Nov 25 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.0.23-1
- Update to 0.0.23
