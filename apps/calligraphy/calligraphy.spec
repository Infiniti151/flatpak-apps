%global         app_id        dev.geopjr.Calligraphy
%global         forgeurl      https://codeberg.org/GeopJr/calligraphy
%global         tag           v%{version}

Name:           calligraphy
Version:        1.3.0
Release:        1%{?dist}
Summary:        Turn text into ASCII banners
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        https://files.pythonhosted.org/packages/a0/f2/2649b2acace54f861eccd4ab163bfd914236fc93ddb1df02dad2a2552b14/pyfiglet-1.0.2.tar.gz

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  appstream
BuildRequires:  python3-devel
BuildRequires:  python3-pip

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3

%description
Calligraphy turns short texts into large, impressive banners made up of ASCII Characters, ready to be copied or exported to images. Spice up your online conversations by adding some extra oompf to your messages!

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install

%find_lang %{name} %{name}.lang

# Normalize the python shebang
%py3_shebang_fix \
    %{buildroot}%{_bindir}/%{name} \
    %{buildroot}%{_datadir}/%{app_id}/

# Install pyfiglet directly into the app's main directory
pip3 install --no-deps --ignore-installed --target=%{buildroot}%{_datadir}/%{app_id} %{SOURCE1}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstreamcli validate --no-net %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{app_id}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_scalableiconsdir}/*.svg
%{_hicolordir}/symbolic/apps/*.svg
%{_metainfodir}/*metainfo.xml


%changelog
* Mon Nov 09 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.3.0-1
- Visual refinements to match the state of the art of GNOME apps
- We moved to Codeberg!
- The font preview view will now display more fonts if they fit in the current window size
- Fixed a race condition with the font previews on the latest versions of the stack
- Updated translations

