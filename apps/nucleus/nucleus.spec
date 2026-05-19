Name:           nucleus
Version:        3
Release:        1%{?dist}
Summary:        A GNOME application to explore periodic table data
License:        GPLv3+
URL:            https://codeberg.org/lo_vely/nucleus
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}

BuildArch:      noarch

BuildRequires:  meson >= 1.0.0
BuildRequires:  python3-devel
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  gettext
BuildRequires:  git-core

Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Nucleus is a modern GNOME application designed to display interactive
periodic table data, element information, and electron shell configurations.

%prep
%setup -c -T

git clone %{url} .
git checkout v%{version}

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%doc README.md
%license COPYING
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/*.xml
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/dbus-1/services/*.service
%{_datadir}/icons/hicolor/*/apps/*.svg

%changelog
* Mon May 18 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 3-1
- Test build