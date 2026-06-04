Name:           planify
Version:        4.19.4
Release:        1%{?dist}
Summary:        Task manager with Todoist and CalDAV support
License:        GPL-3.0-or-later
URL:            https://github.com/alainm23/%{name}
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%global app_id io.github.alainm23.%{name}
%global __requires_exclude ^libgxml-0.20.*$
%global __provides_exclude ^libgxml-0.20.*$

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  vala
BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext
BuildRequires:  python3
BuildRequires:  git-core

# Dependencies
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.7.0
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libical-glib)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libspelling-1)
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libportal)
BuildRequires:  pkgconfig(libportal-gtk4)
BuildRequires:  pkgconfig(libecal-2.0) >= 3.45.1
BuildRequires:  pkgconfig(libedataserver-1.2) >= 3.45.1

Requires:       hicolor-icon-theme
Requires:       glib2

%description
Planify is a modern task manager designed for GNOME, featuring synchronization
capabilities with Todoist and CalDAV servers, planning views, and extensive integration.

%package        libs
Summary:        Shared libraries for %{name}

%description    libs
The %{name}-libs package contains the shared libraries used by applications
built around the Planify ecosystem.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, header files, and Vala bindings
for developing applications that use Planify's core API.

%prep
%setup -q -n %{name}-%{version}

git init

if [ -f "subprojects/chrono.wrap" ]; then
    CHRONO_URL=$(sed -n 's/^url=//p' subprojects/chrono.wrap)
    CHRONO_REV=$(sed -n 's/^revision=//p' subprojects/chrono.wrap)
    git clone --depth 1 -b "$CHRONO_REV" "$CHRONO_URL" subprojects/chrono
else
    echo "Notice: subprojects/chrono.wrap not found for this version. Skipping."
fi

GXML_URL=$(sed -n 's/^url=//p' subprojects/gxml-0.20.wrap)
GXML_REV=$(sed -n 's/^revision=//p' subprojects/gxml-0.20.wrap)
git clone --depth 1 -b "$GXML_REV" "$GXML_URL" subprojects/gxml-0.20

if [ -f scripts/update-translations.py ]; then
    python3 scripts/update-translations.py
fi

%build
%meson \
    -Dprofile=default \
    -Dportal=true \
    -Devolution=true \
    -Dspelling=enabled \
    -Dmanpage=false \
    -Dgxml:default_library=static \
    --wrap-mode=nodownload
%meson_build

%install
%meson_install
%find_lang %{app_id}

rm -rf %{buildroot}%{_includedir}/gxml-0.20/
rm -rf %{buildroot}%{_libdir}/pkgconfig/gxml-0.20.pc
rm -rf %{buildroot}%{_datadir}/vala/vapi/gxml-0.20.*
rm -f %{buildroot}%{_libdir}/libgxml-0.20.so

%check
%meson_test --suite cli
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.xml

%files -f %{app_id}.lang
%license LICENSE
%doc README.md

%{_bindir}/%{app_id}*
%{_libexecdir}/%{app_id}-search-provider

%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/metainfo/%{app_id}.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/*.{svg,png}

%{_datadir}/dbus-1/services/%{app_id}.SearchProvider.service
%{_datadir}/gnome-shell/search-providers/%{app_id}.SearchProvider.ini

%{_libdir}/girepository-1.0/GXml-*.typelib
%{_datadir}/gir-1.0/GXml-*.gir
%{_datadir}/locale/*/LC_MESSAGES/GXml-*.mo

%files libs
%{_libdir}/libplanify.so.*
%{_libdir}/libgxml-0.20.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/libplanify.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/vala/vapi/%{name}.*

%changelog
* Thu Jun 04 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v4.19.4-1
- Initial test build