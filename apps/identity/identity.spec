%global         app_id        org.gnome.gitlab.YaLTeR.Identity
%global         forgeurl      https://gitlab.gnome.org/YaLTeR/identity
%global         tag           v%{version}

Name:           identity
Version:        26.03
Release:        1%{?dist}
Summary:        Compare images and videos
License:        GPL3+
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  cairo-devel
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pango-devel
BuildRequires:  pkgconfig(dav1d) >= 1.0.0
BuildRequires:  pkgconfig(gio-2.0) >= 2.74
BuildRequires:  pkgconfig(glib-2.0) >= 2.74
BuildRequires:  pkgconfig(glycin-2) >= 2
BuildRequires:  pkgconfig(glycin-gtk4-2) >= 2
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.24.0
BuildRequires:  pkgconfig(gstreamer-video-1.0) >= 1.24.0
BuildRequires:  pkgconfig(gtk4) >= 4.16.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.0
BuildRequires:  pkgconfig(libwebpdemux) >= 0.5
BuildRequires:  rustc

Requires:       gstreamer1-plugin-gtk4
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       hicolor-icon-theme

%description
A program for comparing multiple versions of an image or video.

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_metainfodir}/*.metainfo.xml


%changelog
* Mon Nov 16 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 26.03-1
- This release adds a time hover display, CLI flags, and more zoom shortcuts.
- Added a time display when hovering over the video seek bar.
- Added --display and --zoom CLI flags for starting Identity with a given display mode and zoom.
- Added Ctrl+2..9 shortcuts to set zoom level to increments from 200%% to 900%%.
- The window title now shows the current file name, which is convenient when opening many tabs.
- Increased the default window size to make the video 960×540.
- Updated to the GNOME 50 platform.
- Updated translations.

