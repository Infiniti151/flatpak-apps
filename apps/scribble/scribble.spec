%global         app_id                             page.codeberg.petsoi.scribble
%global         forgeurl                           https://codeberg.org/petsoi/scribble
%global         tag                                v%{version}
%global         __brp_mangle_shebangs_exclude_from ^/usr/src/debug/.*$

Name:           scribble
Version:        1.15.0
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
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
BuildRequires:  pkgconfig(gtk4) >= 4.20
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9
BuildRequires:  pkgconfig(librsvg-2.0) >= 2.50

Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Requires:       hicolor-icon-theme

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
%license LICENSE
%doc readme.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_hicolordir}/*/*/*
%{_gschemasdir}/*.gschema.xml
%{_mimepackagesdir}/*.xml
%{_metainfodir}/*.metainfo.xml


%changelog
* Sat Nov 28 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.15.0-1
- Update to 1.15.0

* Tue Nov 24 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.14.0-1
- A release for printing, select all and copying into other programs.
- Print from the menu or with Ctrl+P: the print dialog covers every page, applies page ranges, copies, collate and reverse order, and can print to a PDF file
- Ctrl+A selects everything on the active page
- Pasting a copied note into Inkscape keeps its ink inside the note
- Copied stickers keep their proportions and show only what is inside their view box
- A move no longer latches onto grid snaps until it leaves its grab radius, and guides stay hidden until then
- Pictures dropped in come out at most 2.5 times the size of a sticker
- While the last document loads, only the gray ground is drawn at startup

* Sat Nov 14 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.13.1-1
- A bug fix release for the page menus and Fit Page.
- A page's own menu changes the background or imports a PDF into that page, even when another page became active meanwhile
- Fit Page frames the active page instead of always returning to the first page

* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.12.5-1
- A release for the narrow window layout.
- On a narrow window the left rail gives way to a panel button in the header bar; it opens the panels with a back button and a switcher for Open, Stickers, Pictures, Objects, Animation and Audio
- Dropped notes, tables, calendars, stickers and pictures, and their preview while you drag, come out smaller on narrow windows
- The shadow of a note scales with the paper when you zoom

