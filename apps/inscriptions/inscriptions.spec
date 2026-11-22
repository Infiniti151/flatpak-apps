%global         app_id        page.codeberg.elly_code.inscriptions
%global         forgeurl      https://codeberg.org/elly-code/inscriptions
%global         tag           %{version}

Name:           inscriptions
Version:        0
Release:        1%{?dist}
Summary:        Translate text elegantly
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.1
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  valac
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(granite-7) >= 7.7.0
BuildRequires:  pkgconfig(gtk4) >= 4.14
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libsoup-3.0)

Requires:       hicolor-icon-theme
Requires:       elementary-icon-theme

%description
A fast, pretty, and ready translation app using DeepL free and paid API

Some points of note:
- Nimble: Paste your DeepL api key (Whichever the plan), and here you go!
- Thoughtful: Just what you need, out of your way and a click away
- Comprehensive: No scary angry dialogs - If something goes wrong, explain nicely
- Lean: Limiting resource usage and internet communications to the minimum
- Supported languages: All those available via DeepL API!

If you like this app please do not hesitate to donate to encourage its development!

Libretranslate support is considered, but a heavy time and energy investment, so may or may not happen.

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{app_id}

%check
%meson_test

%files -f %{app_id}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{app_id}
%{_appsdir}/%{app_id}.desktop
%{_hicolordir}/*/apps/%{app_id}.png
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml
