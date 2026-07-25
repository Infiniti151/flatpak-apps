%global debug_package %{nil}

Name:           sudoku
Version:        1.8.0
Release:        1%{?dist}
Summary:        Sudoku Game application
License:        GPL-3.0-or-later
URL:            https://github.com/sepehr-rs/Sudoku
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz
Source1:        https://files.pythonhosted.org/packages/0c/4f/e5de816646174cdd8c5db5e2422d4b3eb7cd38bcc398aa0e57047ece6db8/sudoku_engine-2.0.0-py3-none-any.whl

BuildRequires:  meson >= 1.4.0
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  gettext
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-iniconfig
BuildRequires:  python3-packaging
BuildRequires:  python3-pluggy

Provides:       python3-sudoku-engine = %{version}-%{release}

Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme
Requires:       python3

%description
A beautiful, modern Sudoku application featuring classic and diagonal variants.

%prep
%autosetup -n Sudoku-%{version}

%build
%meson
%meson_build

%install
%meson_install
sed -i 's|/usr/sbin/python3|/usr/bin/python3|g' %{buildroot}%{_bindir}/sudokugame
find %{buildroot}%{_datadir}/sudokugame/ -type f -name "*.py" -exec sed -i 's|/usr/sbin/python3|/usr/bin/python3|g' {} +
pip3 install --no-deps --ignore-installed --prefix=%{buildroot}%{_prefix} %{SOURCE1}

%find_lang sudokugame

%check
export PYTHONPATH="%{buildroot}%{python3_sitelib}:src:."
%meson_test --suite unit
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.xml

%files -f sudokugame.lang
%license COPYING
%doc README.md
%{_bindir}/sudokugame
%{_datadir}/sudokugame/
%{python3_sitelib}/sudoku/
%{python3_sitelib}/sudoku_engine-*.dist-info/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg
%{_datadir}/metainfo/*.xml

%changelog
* Sat Jul 25 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.8.0-1
- What's New ?
- You can now place pencil marks automatically with Shift + P.
- You can now set a mistake limit in Preferences.
- The Continue Game button is now disabled when the current game is complete.
- You can now disable popovers in Preferences.
- Plus many more improvements and bug fixes!
- 📦 Installation
- The recommended way to install Sudoku is through Flathub:
- [![Download on Flathub](https://flathub.org/api/badge?svg&locale=en)](https://flathub.org/apps/io.github.sepehr_rs.Sudoku)
- ```bash
- ... (see upstream for full release notes)

* Sun May 17 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.7.0-1
- What's New ?
- Pencil notes affected by a correct entry are now automatically removed
- Each editable cell's popover now shows remaining valid inputs for that number
- Preferences and Shortcuts dialogs updated to modern libadwaita style, thanks to @Wartybix
- Added Chinese translation, thanks to @uaiqop
- Fixed a game state saving bug, thanks to @jammie-jelly
- And many more improvements and fixes!
- 📦 Installation
- The recommended way to install Sudoku is through Flathub:
- [![Download on Flathub](https://flathub.org/api/badge?svg&locale=en)](https://flathub.org/apps/io.github.sepehr_rs.Sudoku)
- ... (see upstream for full release notes)

