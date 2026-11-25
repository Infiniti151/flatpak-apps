%global         app_id        io.github.revisto.drum-machine
%global         forgeurl      https://github.com/Revisto/drum-machine
%global         tag           v%{version}
%global         mido_ver      1.3.3

Name:           drum-machine
Version:        0
Release:        1%{?dist}
Summary:        Create and play drum beats
License:        GPL-3.0-or-later AND MIT
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}
# mido is not packaged in Fedora; bundle the pure-Python wheel
Source1:        https://files.pythonhosted.org/packages/py3/m/mido/mido-%{mido_ver}-py3-none-any.whl

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3
Requires:       python3-pygame
Requires:       python3-numpy
Requires:       python3-packaging
Requires:       python3-setuptools_scm
Requires:       python3-gobject

Provides:       bundled(python3dist(mido)) = %{mido_ver}

%description
Drum Machine is a modern and intuitive application for creating, playing, and managing drum patterns. Perfect for musicians, producers, and anyone interested in rhythm creation, this application provides a simple interface for drum pattern programming. Have fun!

Features:
- Intuitive grid-based pattern editor with infinite pages
- Custom samples: Add your own drum sounds with MIDI note mapping
- Adjustable BPM control
- Volume control for overall mix
- Save and load patterns
- Multiple drum sounds including kick, snare, hi-hat, and more
- Audio and MIDI export with support for WAV, FLAC, Ogg, MP3, and MIDI formats
- Metadata support for embedding artist name, song title, and cover art
- Keyboard shortcuts for quick access to all functions

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}

# Install the bundled wheel into the buildroot
pip3 install --no-deps --no-index --ignore-installed --root-user-action=ignore --prefix=%{buildroot}%{_prefix} %{SOURCE1}

# Drop mido's CLI tools, only the library is needed
rm -f %{buildroot}%{_bindir}/mido-*

%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

# Keep mido's license only under %%license
mv %{buildroot}%{python3_sitelib}/mido-%{mido_ver}.dist-info/LICENSE mido-LICENSE

%check
%meson_test

%files -f %{name}.lang
%license COPYING mido-LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{python3_sitelib}/mido/
%{python3_sitelib}/mido-*.dist-info/
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml
