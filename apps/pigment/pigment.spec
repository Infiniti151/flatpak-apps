%global         app_id          com.jeffser.Pigment
%global         forgeurl        https://github.com/Jeffser/Pigment
%global         tag             %{version}
%global         colorthief_ver  0.2.1

Name:           pigment
Version:        0.5.6
Release:        1%{?dist}
Summary:        Get color palettes from images
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}
# colorthief is not packaged in Fedora; bundle the pure-Python wheel
Source1:        https://files.pythonhosted.org/packages/56/18/be03b7058e65f9df479b14e7af4e73945ce311e07aaad45cf2536e14791a/colorthief-%{colorthief_ver}-py2.py3-none-any.whl

BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel
BuildRequires:  python3-pip

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3
Requires:       python3-gobject
Requires:       python3-pillow
Requires:       python3-pydbus

Provides:       bundled(python3dist(colorthief)) = %{colorthief_ver}

%description
Pigment allows you to extract a palette of colors from your images offline. You can select the speed and accuracy by modifying the number and quality of colors.

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
# Install the bundled wheel into the buildroot
pip3 install --no-deps --no-index --ignore-installed --root-user-action=ignore --prefix=%{buildroot}%{_prefix} %{SOURCE1}

%find_lang %{name}
%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{python3_sitelib}/colorthief.py
%{python3_sitelib}/__pycache__/colorthief.*
%{python3_sitelib}/colorthief-*.dist-info/
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Sat Nov 14 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.5.6-1
- Update runtime to Gnome 50

