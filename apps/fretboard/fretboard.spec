%global         app_id        dev.bragefuglseth.Fretboard
%global         forgeurl      https://github.com/bragefuglseth/fretboard
%global         tag           v%{version}

Name:           fretboard
Version:        0
Release:        1%{?dist}
Summary:        Look up guitar chords
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  sed
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-2.0) >= 2.76
BuildRequires:  pkgconfig(glib-2.0) >= 2.76
BuildRequires:  pkgconfig(gtk4) >= 4.10.1
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5.alpha

Requires:       hicolor-icon-theme

%description
How was that chord played, again? Fretboard lets you find guitar chords by typing their names or plotting them on an interactive guitar neck. When you have identified a chord, you can experiment with changing it, see more ways to play it, or bookmark it to save it for later. No matter if you are a beginner or an advanced guitarist, you can use Fretboard to practice, learn, and master your favorite songs!

Fretboard is proudly part of GNOME Circle, an initiative that champions the great software that is available for the GNOME platform. For more information, visit the GNOME Circle website.

%prep
%forgesetup

%conf
%meson

%build
%meson_build
env CARGO_HOME=%{_vpath_builddir}/cargo-home cargo tree -e normal --prefix none --format '{p}: {l}' | sed -E 's/ \(\*\)$//; s/ \(\/[^)]*\)//' | sort -u > LICENSE.dependencies

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml
