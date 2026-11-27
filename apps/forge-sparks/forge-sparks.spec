%global         app_id        com.mardojai.ForgeSparks
%global         forgeurl      https://github.com/rafaelmardojai/forge-sparks
%global         tag           %{version}

Name:           forge-sparks
Version:        0
Release:        1%{?dist}
Summary:        Get Git forges notifications
License:        MIT
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.63.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  gjs
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       gtk4
Requires:       gjs
Requires:       hicolor-icon-theme
Requires:       libadwaita

%description
Simple notifier app with support for GitLab, Github, Gitea and Forgejo.

%prep
%forgesetup

# Re-initialize git context for forge tarballs to resolve submodules
if [ ! -d ".git" ]; then
	git init -q
	git remote add origin %{forgeurl}
	git fetch -q --depth 1 origin %{tag}
	git checkout -q -f FETCH_HEAD
fi
git submodule update --init --recursive --depth 1

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{app_id}

%check
%meson_test

%files -f %{app_id}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{app_id}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_hicolordir}/scalable/status/%{app_id}-*-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_dbusservicesdir}/%{app_id}.service
%{_metainfodir}/%{app_id}.metainfo.xml

