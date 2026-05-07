%global app_id com.github.ryonakano.konbucase

Name:           konbucase
Version:        4.5.0
Release:        1%{?dist}
Summary:        A tool for case conversion and string manipulation
License:        GPL-3.0-or-later
URL:            https://github.com/ryonakano/konbucase
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/%{version}.tar.gz
Source1:        https://github.com/ryonakano/chcase/archive/2.4.0/chcase-2.4.0.tar.gz

# Compilers and Build Tools
BuildRequires:  meson >= 0.58.0
BuildRequires:  gcc
BuildRequires:  vala
BuildRequires:  gettext
BuildRequires:  blueprint-compiler

# Desktop Libraries (Development Files)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5
BuildRequires:  pkgconfig(glib-2.0) >= 2.74
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtksourceview-5)

# Validation and Integration Tools
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gtk-update-icon-cache

%description
Konbucase is a native Linux application for converting strings between 
various cases like camelCase, snake_case, and PascalCase.

%prep
%setup -q
mkdir -p subprojects/chcase
tar -xf %{SOURCE1} -C subprojects/chcase --strip-components=1

sed -i "s/allow_fallback: get_option('use_submodule')/allow_fallback: true/" meson.build

%build
%meson \
    -Dgranite=disabled \
    -Duse_submodule=false \
    --wrap-mode=nodownload
%meson_build

%install
%meson_install
%find_lang %{app_id}

rm -rf %{buildroot}%{_includedir}/chcase.h
rm -rf %{buildroot}%{_libdir}/pkgconfig/chcase.pc
rm -rf %{buildroot}%{_datadir}/vala/vapi/chcase.*

%check
%meson_test

%files -f %{app_id}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{app_id}
%{_libdir}/libchcase.so
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/metainfo/%{app_id}.metainfo.xml