%global         app_id        io.github.flattool.Ignition
%global         upstream_name ignition
%global         forgeurl      https://github.com/flattool/ignition
%global         tag           %{version}

Name:           flattool-ignition
Version:        2.4.1
Release:        1%{?dist}
Summary:        Manage startup apps and scripts
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  gjs
BuildRequires:  git
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel
BuildRequires:  typescript
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       gtk4
Requires:       gjs
Requires:       hicolor-icon-theme
Requires:       libadwaita

%description
Ignition provides a simple UI to add, remove, and modify startup entries on your computer. Ignition can add apps, scripts, and arbitrary commands to run at login.

%prep
%forgesetup

# Re-initialize git context for forge tarballs to resolve submodules
if [ ! -d ".git" ]; then
    git init -q
    git remote add origin %{forgeurl}
    git fetch -q --depth 1 origin %{tag}
    git checkout -q -f FETCH_HEAD
fi
git submodule update --init --recursive

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{upstream_name}

%check
%meson_test
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{upstream_name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/%{upstream_name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml


%changelog
* Thu Nov 19 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 2.4.1-1
- New Features
- Added ability to open a script to fill in the Command or Script
- Added better support for NixOS and other Nix setups
- Bug Fixes and Changes
- Added fallback option to delete a file if trashing the file does not work
- Fixed minor issue causing some new entries to not be allowed to be created
- Better handle cases where the system autostart folder is missing
- Fixed incorrectly titled "About Descriptive" menu item
- Improved reliability of the Installed Apps list and its automatic refreshing
- Added and updated translations

