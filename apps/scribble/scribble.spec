%global         app_id                             page.codeberg.petsoi.scribble
%global         forgeurl                           https://codeberg.org/petsoi/scribble
%global         tag                                v%{version}
%global         __brp_mangle_shebangs_exclude_from ^/usr/src/debug/.*$

Name:           scribble
Version:        1.12.5
Release:        1%{?dist}
Summary:        Take handwritten notes and homework
License:        GPL-3
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.1.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  cairo-devel
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pango-devel
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.20
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9
BuildRequires:  pkgconfig(librsvg-2.0) >= 2.50
BuildRequires:  rustc

Requires:       cairo
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       pango

%description
Scribble is a handwriting canvas for school kids: take notes, do your homework, or work through exercises with a pen on a touchscreen.

Write and draw freehand on pages with ruled, squared, music, and other school-paper backgrounds, or import a worksheet as a PDF and write right on it. Hold the pen still after drawing a shape, arrow, or diagram and it turns into a clean version that can be reshaped afterwards, and scribbling over a drawing deletes it.
- A pen and a highlighter, with your own colors; scribble over a drawing to erase it
- Select with gestures, then move, resize, and rotate your drawings, with alignment guides
- Record audio while you write, so you don't miss anything
- Crop a photo of a whiteboard or paper so it is straight and clear, and make the background white with strong contrast
- Add stickers, pictures, sticky notes, and coordinate grids
- An endless zoomable canvas with many pages you can reorder
- Present your pages step by step, and export everything as a PDF

Made for a pen and a touchscreen used together: the pen draws, and your finger pans, zooms, and selects. A touchpad or mouse works to some degree, but drawing with them is difficult. A built-in Help explains the gestures.

%prep
%forgesetup
mkdir -p cargo-home

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%license LICENSE
%doc readme.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/mime/packages/*.xml
%{_metainfodir}/*.metainfo.xml


%changelog
* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.12.5-1
- A release for the narrow window layout.
- On a narrow window the left rail gives way to a panel button in the header bar; it opens the panels with a back button and a switcher for Open, Stickers, Pictures, Objects, Animation and Audio
- Dropped notes, tables, calendars, stickers and pictures, and their preview while you drag, come out smaller on narrow windows
- The shadow of a note scales with the paper when you zoom

