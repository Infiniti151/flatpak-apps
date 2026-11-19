%global         app_id        io.github.flattool.Warehouse
%global         forgeurl      https://github.com/flattool/warehouse
%global         tag           %{version}

Name:           warehouse
Version:        0
Release:        1%{?dist}
Summary:        Manage all things Flatpak
License:        GPL-3.0-only
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.64.0
BuildRequires:  ninja-build
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  libappstream-glib
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       dconf
Requires:       flatpak
Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3-gobject
Requires:       flatpak-xdg-utils

%description
Warehouse provides a simple UI to control complex Flatpak options, all without resorting to the command line.

Features:
- Manage installed Flatpaks and view properties of any package
- Change versions of a Flatpak to rollback any unwanted updates
- Pin runtimes and mask Flatpaks
- Filter packages and sort data, to help find anything easily
- See current app user data, and cleanup any unused data left behind
- Add popular Flatpak remotes with a few clicks or add custom remotes instead
- Take snapshots of your apps' user data, saving your data
- Install new packages from any remote, or from your system
- Responsive UI to fit large and small screen sizes

%prep
%forgesetup
sed -i "s/args: \['validate', appstream_file\]/args: ['validate-relax', '--nonet', appstream_file]/g" data/meson.build

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{name}
%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

%check
%meson_test
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_metainfodir}/*.metainfo.xml

