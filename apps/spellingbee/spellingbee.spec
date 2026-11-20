%global         app_id          io.github.josephmawa.SpellingBee
%global         forgeurl        https://github.com/josephmawa/SpellingBee
%global         tag             v%{version}

Name:           spellingbee
Version:        0.1.8
Release:        1%{?dist}
Summary:        Learn new English words
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildArch:      noarch

BuildRequires:  meson >= 1.0.0
BuildRequires:  gcc
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gjs-1.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  desktop-file-utils
BuildRequires:  appstream
BuildRequires:  gettext

Requires:       gjs
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Use Spelling Bee to enhance your English vocabulary while having fun.

Below are the main features:
- Provides thousands of words
- You can play it offline
- It provides links to the meaning of words
- You can view puzzle history
- You can view your score
- Switch to dark, light, or system mode

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/%{name}/
%{_appsdir}/*.desktop
%{_gschemasdir}/*.gschema.xml
%{_metainfodir}/*.xml
%{_dbusservicesdir}/*.service
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg

%changelog
* Fri Nov 20 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.1.8-1
- Add Spanish translation

* Wed Oct 21 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.1.7-1
- Upgrade to Gnome runtime version 51

* Fri May 29 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.1.6-1
- Update to v0.1.6

* Sun May 10 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.1.5-1
- Update to v0.1.5

