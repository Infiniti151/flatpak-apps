%global         app_id          no.bragefuglseth.Keypunch

Name:           keypunch
Version:        7.0
Release:        1%{?dist}
Summary:        A GTK4/Adwaita typing practice application
License:        GPL-3.0-or-later
URL:            https://github.com/bragefuglseth/keypunch
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext

%description
Keypunch is a simple typing practice application for the GNOME desktop,
built with Rust and GTK4. It allows users to improve their typing speed
and accuracy through a clean, modern interface.

%prep
%autosetup

%build
%meson -Dsandboxed=false
%meson_build

%install
%meson_install
%find_lang keypunch

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f keypunch.lang
%license COPYING
%doc README.md
%{_bindir}/keypunch
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_metainfodir}/*.metainfo.xml

%changelog
* Sat Jul 18 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v7.0-1
- Language additions and various modernizations:
- Text generation for programming languages: C++, JavaScript, Python, and Rust
- New and modern keyboard shortcuts dialog
- Minor text generation corrections for various languages
- Basque text generation
- User interface translations for Cornish, Esperanto, Greek, Kazakh, and Uzbek, making Keypunch available in a total of 38 languages

* Fri May 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v6.3-1
- Miscellaneous bug fixes and improvements:
- The “Enable Entry” button is now shown whenever it should be
- Greek tests now use proper Greek punctuation in advanced mode
- Kabyle tests now use the proper “open E” letter in all cases
- Updated user interface translations

