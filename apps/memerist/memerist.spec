%global         app_id        io.github.vani_tty1.memerist
%global         forgeurl      https://github.com/vani-tty1/memerist
%global         tag           v%{version}

Name:           memerist
Version:        2.6.1
Release:        1%{?dist}
Summary:        A simple and modern meme editor
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.7.0
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
BuildRequires:  pkgconfig(MagickWand)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       ImageMagick

%description
A lightweight photo editor focused entirely on editing memes. Yes, just memes, nothing more, nothing less.

Features:
- Text and Image layers
- Real-time preview as you type
- Add Filters
- GIF support
- Transform tool
- Freehand annotation tool
- Let it Happen

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
%{_bindir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_metainfodir}/*.metainfo.xml


%changelog
* Sun Nov 15 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 2.6.1-1
- This is a stable release with the following changes:
- Sort recently added templates by added date including built in ones
- Adjust initial window size
- Add more templates

