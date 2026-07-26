%global         debug_package %{nil}
%global         _enable_debug_package 0

Name:           pods
Version:        3.1.1
Release:        1%{?dist}
Summary:        A powerful Podman manager for GNOME
License:        GPL-3.0-or-later
URL:            https://github.com/marhkb/Pods
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson >= 0.59
BuildRequires:  gcc
BuildRequires:  rust-packaging
BuildRequires:  cargo
BuildRequires:  blueprint-compiler
BuildRequires:  pkgconfig(gtk4) >= 4.18.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.7
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(vte-2.91-gtk4)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       podman
Requires:       hicolor-icon-theme

%description
Pods is a GTK application that allows you to manage podman
containers, pods, and images with a clean, native GNOME interface.

%prep
%autosetup

%build
%meson \
    -Dprofile=default
%meson_build

%install
%meson_install
%find_lang %{name}

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*.svg
%{_metainfodir}/*.metainfo.xml
%{_datadir}/glib-2.0/schemas/*.gschema.xml

%changelog
* Thu Jul 16 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v3.1.1-1
- Pods 3.1.1 contains the following changes:
- Fixed an issue where active terminal exec sessions were unexpectedly terminated when the window was resized and the sidebar collapsed. (#965)
- Removed empty image tag markup in the search response row when using Podman. (#967)
- Improved text alignment for errors in the action dialog and increased the height of the repo tag push view. (#968)
- Added a link to the source repository in the application metainfo. (Thanks to @salim-b, #884)

* Wed Jul 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v3.1.0-1
- Pods 3.1.0 contains the following changes:
- Features
- Overhauled the internal background action system to use a dedicated modal dialog and stateful, editable actions. (#961)
- Implemented an AutoScrolledWindow widget and ported the container log view to it, improving automatic terminal scrolling. (#932)
- Introduced the ImageSuggestionEntryRow widget, featuring focus-leave handling, Ctrl+Space activation, and increased width alignment. (#933, #934, #943)
- Added bi-directional timestamp synchronization and a visually improved numeric layout style to the date-time row widget. (#947, #951)
- Updated the connection creation view with dynamic descriptions and modified the default podman-tcp.service template to bind strictly to localhost (127.0.0.1). (Thanks to @anli5005, #948)
- Added interactive documentation links for podman-system-service configurations when setting up rootful instances. (Thanks to @anli5005, #946)
- Enhanced image search result rows by ellipsizing long image names in the UI. (#945)
- Fixes
- ... (see upstream for full release notes)

* Fri May 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v3.0.0-1
- Pods 3.0.0 contains the following changes:
- Implemented a new backend architecture to support multiple container engines. (#927)
- Experimental Docker support &#x2013; please report any issues on GitHub. (#927)
