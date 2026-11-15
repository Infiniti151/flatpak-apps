%global         app_id        re.sonny.Junction
%global         forgeurl      https://github.com/sonnyp/Junction
%global         tag           v%{version}

Name:           junction
Version:        1.13
Release:        1%{?dist}
Summary:        Application chooser
License:        GPL-3.0-only
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  desktop-rpm-macros
BuildRequires:  gettext
BuildRequires:  gjs
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       gjs
Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita

%description
Junction pops up automatically when you open a file or link in another app. Use the mouse or keyboard navigation to choose which app you want to open it with.

Features:
- Choose the app to open with
- Show the location before opening
- Edit the URL before opening
- Show a hint for insecure links
- Keyboard navigation
- Supports desktop actions on right click
- Middle Click or Ctrl + Click to open in multiple applications
- Linux Mobile support

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

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{app_id}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Sun Nov 15 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.13-1
- Test
