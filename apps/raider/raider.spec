%global         app_id        com.github.ADBeveridge.Raider
%global         forgeurl      https://github.com/ADBeveridge/raider
%global         tag           v%{version}

Name:           raider
Version:        3.1.0
Release:        1%{?dist}
Summary:        Permanently delete your files
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gtk4) >= 4.18.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.7.0

Requires:       hicolor-icon-theme

%description
File Shredder is a file deletion program designed to permanently remove sensitive files from your computer, enhancing data privacy.

Within a certain limit, it is effective. However, modern SSDs use certain technologies to extend its lifetime, which has the side effect of ensuring that shredding is never perfect, and no software can fix that. But shredding significantly increases the difficulty of data recovery since it requires specialized software and hardware.

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
%license LICENSE.md
%doc README.md
%{_bindir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_dbusservicesdir}/%{app_id}.service
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Wed Nov 25 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 3.1.0-1
- GNOME 48 Update
- Modernize circular progress indicator
- Fix various small memory leaks
- Support launching from DBus
