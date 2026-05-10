Name:           spellingbee
Version:        0.0.0
Release:        1%{?dist}
Summary:        A word game application
License:        GPL-3.0-or-later
URL:            https://github.com/josephmawa/SpellingBee
BugURL:	        https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  meson >= 1.0.0
BuildRequires:  gcc
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gjs-1.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext

Requires:       gjs
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
SpellingBee is a GNOME-based word game written in JavaScript using GJS.

%prep
%autosetup -n SpellingBee-%{version}

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/*
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/dbus-1/services/*.service
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg