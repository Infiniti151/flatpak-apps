%global         app_id        dev.geopjr.Calligraphy
%global         forgeurl      https://codeberg.org/GeopJr/calligraphy
%global         tag           v%{version}

Name:           calligraphy
Version:        1.3.0
Release:        1%{?dist}
Summary:        Turn text into ASCII banners
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  appstream
BuildRequires:  python3-devel

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3

%description
Calligraphy turns short texts into large, impressive banners made up of ASCII Characters, ready to be copied or exported to images. Spice up your online conversations by adding some extra oompf to your messages!

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install

%find_lang %{name}.lang

%py3_shebang_fix \
    %{buildroot}%{_bindir}/%{name} \
    %{buildroot}%{_datadir}/%{app_id}/

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstreamcli validate --no-net %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{app_id}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_metainfodir}/*metainfo.xml

%changelog
* Sat Nov 07 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.3.0-1
- Test build
