%global         app_id        io.github.unrud.RecentFilter
%global         forgeurl      https://github.com/Unrud/recent-filter
%global         tag           v%{version}

Name:           recent-filter
Version:        0.1.10
Release:        1%{?dist}
Summary:        Exclude files and folders from recently used files
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}
Patch0:         https://raw.githubusercontent.com/Infiniti151/flatpak-apps/main/apps/recent-filter/rpm-unsandboxed-portal.patch

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  libappstream-glib
BuildRequires:  librsvg2-tools
BuildRequires:  python3-devel
BuildRequires:  python3-gobject

Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme
Requires:       python3-gobject

%description
Exclude specific files and folders from appearing in the list of recently used files.

Paths can be specified using wildcards, just like in a .gitignore file. This means you can use patterns such as "*.txt".

%prep
%forgeautosetup -p1

%conf
%meson

%build
%meson_build

%install
%meson_install

%find_lang %{name}

%py3_shebang_fix \
    %{buildroot}%{_bindir}/%{name} \
    %{buildroot}%{_datadir}/%{name}

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_appsdir}/%{app_id}.desktop
%{_gschemasdir}/%{app_id}.gschema.xml
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_hicolordir}/*/apps/%{app_id}.png
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Sat Nov 21 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.1.10-1
- Add Czech translation
- Flatpak: Update runtime to 50

