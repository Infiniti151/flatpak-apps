%global         app_id        com.rafaelmardojai.WebfontKitGenerator
%global         upstream_name webfontkitgenerator
%global         forgeurl      https://github.com/rafaelmardojai/webfont-kit-generator
%global         tag           %{version}

Name:           webfont-kit-generator
Version:        0
Release:        1%{?dist}
Summary:        Create @font-face kits easily
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.60.0
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
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 1.35.0
BuildRequires:  pkgconfig(gtk4) >= 4.12
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.4
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(pygobject-3.0) >= 3.40

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3
Requires:       python3-gobject
Requires:       python3-fonttools
Requires:       python3-brotli

%description
Webfont Bundler is a simple utility that allows you to generate woff, woff2 and the necessary CSS boilerplate from non-web font formats (otf and ttf).

Webfont Bundler also includes a tool to Download fonts from Google Fonts for self-hosting.

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{upstream_name}
%py3_shebang_fix %{buildroot}%{_bindir}/%{upstream_name} %{buildroot}%{_datadir}/%{upstream_name}/

%check
%meson_test

%files -f %{upstream_name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{upstream_name}
%{_datadir}/%{upstream_name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_dbusservicesdir}/%{app_id}.service
%{_metainfodir}/%{app_id}.metainfo.xml

