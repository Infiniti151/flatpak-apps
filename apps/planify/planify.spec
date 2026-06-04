%global app_id io.github.alainm23.planify

Name:           planify
Version:        4.19.4
Release:        1%{?dist}
Summary:        Task manager with Todoist and CalDAV support
License:        GPL-3.0-or-later
URL:            https://github.com/alainm23/planify
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

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
%setup -q -c -n %{name}-%{version}

echo "=== Listing extracted contents ==="
ls -la
echo "=================================="

mv %{name}-*/* . 2>/dev/null ||:

if [ ! -f "meson.build" ]; then
    echo "==> meson.build not found here. Checking parent directory..."
    if [ -f "../meson.build" ]; then
        cd ..
    fi
fi

git init

CHRONO_URL=$(sed -n 's/^url=//p' subprojects/chrono.wrap)
CHRONO_REV=$(sed -n 's/^revision=//p' subprojects/chrono.wrap)
git clone --depth 1 -b "$CHRONO_REV" "$CHRONO_URL" subprojects/chrono

GXML_URL=$(sed -n 's/^url=//p' subprojects/gxml-0.20.wrap)
GXML_REV=$(sed -n 's/^revision=//p' subprojects/gxml-0.20.wrap)
git clone --depth 1 -b "$GXML_REV" "$GXML_URL" subprojects/gxml

python3 scripts/update-translations.py ||:

%build
%meson \
    -Dprofile=default \
    -Dportal=true \
    -Devolution=true \
    -Dspelling=enabled \
    -Dmanpage=false \
    --wrap-mode=nodownload
%meson_build

%install
%meson_install
%find_lang %{app_id}

rm -rf %{buildroot}%{_includedir}/gxml-0.20/
rm -rf %{buildroot}%{_libdir}/pkgconfig/gxml-0.20.pc
rm -rf %{buildroot}%{_libdir}/libgxml-0.20.so*
rm -rf %{buildroot}%{_datadir}/vala/vapi/gxml-0.20.*

%check
%meson_test --suite cli
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.xml

%files -f %{app_id}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{app_id}.cli
%{_bindir}/%{app_id}.quick-add
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*.{svg,png}
%{_datadir}/metainfo/*.xml

%files libs
%{_libdir}/libplanify.so.*

%files devel
%{_includedir}/planify/
%{_libdir}/libplanify.so
%{_libdir}/pkgconfig/planify.pc
%{_datadir}/vala/vapi/planify.*

%changelog
* Thu Jun 04 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v4.19.4-1
- Initial test build