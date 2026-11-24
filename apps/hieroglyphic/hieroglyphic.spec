%global         app_id        io.github.finefindus.Hieroglyphic
%global         forgeurl      https://github.com/FineFindus/Hieroglyphic
%global         tag           v%{version}

Name:           hieroglyphic
Version:        2.3.0
Release:        1%{?dist}
Summary:        Find LaTeX and Typst symbols
License:        GPL-3.0
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-2.0) >= 2.70
BuildRequires:  pkgconfig(glib-2.0) >= 2.70
BuildRequires:  pkgconfig(gtk4) >= 4.20.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8
BuildRequires:  pkgconfig(libonnxruntime) >= 1.23

Requires:       hicolor-icon-theme

%description
If you work with LaTeX or Typst, you know it's difficult to memorize the names of all the symbols. Hieroglyphic allows you to search through over 1000 different symbols by sketching.

%prep
%forgesetup

%conf
%meson

%build
export ORT_LIB_PATH="%{_libdir}"
export ORT_PREFER_DYNAMIC_LINK=1
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
* Tue Nov 24 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 2.3.0-1
- Support Typst symbols
- Use hardware-acceleration (NPUs) when available
- Updated to newest GNOME styling
