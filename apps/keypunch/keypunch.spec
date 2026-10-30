%global         app_id          no.bragefuglseth.Keypunch
%global         forgeurl        https://github.com/bragefuglseth/keypunch
%global         tag             v%{version}

Name:           keypunch
Version:        7.0
Release:        1%{?dist}
Summary:        Practice your typing skills
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  forge-srpm-macros
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext

%description
There is no doubt that typing on a keyboard is an essential skill in the digital age. Typing fast and accurately gives you more opportunities, more time for what matters to you, and a sense of self-accomplishment.

Keypunch lets you practice typing. Thanks to fast-paced sessions with instant feedback afterwards and a plethora of available languages, you might even have a little fun doing so. With determination, proper technique and some time, youwill observe a noticeable increase in both the speed and the accuracy of which your thoughts and ideas are put into words on the screen.

If you are already a racer at typing, Keypunch still has something for you. Try practicing with numbers and punctuation, or choose your own text to type out as fast as you can.

Get ready to accelerate your typing!

Keypunch is proudly part of GNOME Circle, an initiative that champions the great software that is available for the GNOME platform. For more information, visit the GNOME Circle website.

%prep
%forgesetup

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
%{_datadir}/icons/hicolor/*/apps/*
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

