%global         _description  %{expand:
Granite is a companion library for GTK and GLib. Among other things, it
provides complex widgets and convenience functions designed for use in
apps built for elementary OS.}
%global         app_id        io.elementary.granite-7
%global         forgeurl      https://github.com/elementary/granite
%global         tag           %{version}

Name:           granite-7
Version:        7.8.1
Release:        1%{?dist}
Summary:        Extend GTK with common widgets and utilities
License:        LGPL-3.0-or-later AND LGPL-2.1-or-later AND GPL-2.0-or-later AND GPL-3.0-or-later

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  meson >= 0.57.0
BuildRequires:  sassc
BuildRequires:  vala >= 0.48.2

BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(glib-2.0) >= 2.50
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk4) >= 4.4.0
BuildRequires:  pkgconfig(shumate-1.0)

%description    %{_description}


%package        devel
Summary:        Granite Toolkit (development headers)

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hicolor-icon-theme

%description    devel %{_description}

This package contains the development headers.


%prep
%forgesetup


%build
%meson -D gtk-stylesheets=true
%meson_build


%install
%meson_install

%find_lang %{name}

# remove the specified stock icon from appdata (invalid for desktop components)
sed -i '/icon type="stock"/d' %{buildroot}/%{_datadir}/metainfo/%{name}.metainfo.xml


%check
desktop-file-validate \
    %{buildroot}/%{_datadir}/applications/%{app_id}.demo.desktop

appstream-util validate-relax --nonet \
    %{buildroot}/%{_metainfodir}/%{name}.metainfo.xml


%files -f %{name}.lang
%license COPYING
%doc README.md

%{_libdir}/libgranite-7.so.7
%{_libdir}/libgranite-7.so.7.*
%{_libdir}/girepository-1.0/Granite-7.0.typelib

%{_datadir}/themes/Granite/

%{_metainfodir}/%{name}.metainfo.xml

%files devel
%{_bindir}/%{name}-demo

%{_libdir}/libgranite-7.so
%{_libdir}/pkgconfig/%{name}.pc

%{_includedir}/%{name}/

%{_datadir}/applications/%{app_id}.demo.desktop
%{_datadir}/icons/hicolor/*/apps/%{app_id}.svg
%{_datadir}/gir-1.0/Granite-7.0.gir
%{_datadir}/vala/vapi/%{name}.deps
%{_datadir}/vala/vapi/%{name}.vapi


%changelog
* Sat Nov 14 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 7.8.1-1
- Initial Copr build (granite-7 was orphaned and retired from Fedora Rawhide)
