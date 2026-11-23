%global         app_id        org.gnome.World.Citations
%global         tag           %{version}

Name:           citations
Version:        0.11.0
Release:        1%{?dist}
Summary:        Manage your bibliography
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            https://gitlab.gnome.org/World/citations

BuildRequires:  meson >= 1.7
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  clippy
BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-2.0) >= 2.76
BuildRequires:  pkgconfig(glib-2.0) >= 2.76
BuildRequires:  pkgconfig(gtk4) >= 4.23
BuildRequires:  pkgconfig(gtksourceview-5) >= 5
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.alpha
BuildRequires:  pkgconfig(poppler)
BuildRequires:  pkgconfig(poppler-glib)

Requires:       hicolor-icon-theme

%description
Manage your bibliographies using the BibTeX format.

%prep
rm -rf %{name}-%{version}
git clone --depth 1 --branch %{tag} %{url}.git %{name}-%{version}
rm -rf %{name}-%{version}/.git
%setup -T -D -n %{name}-%{version}

%conf
%meson

%build
%meson_build
env CARGO_HOME=%{_vpath_builddir}/cargo-home cargo tree -e normal --prefix none --format '{p}: {l}' | sed -E 's/ \(\*\)$//; s/ \(\/[^)]*\)//' | sort -u > LICENSE.dependencies

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license LICENSE LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_dbusservicesdir}/%{app_id}.service
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Mon Nov 23 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.11.0-1
- Test
