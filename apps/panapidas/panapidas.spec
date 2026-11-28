%global         app_id        dev.eltonarodrigues.panapidas
%global         forgeurl      https://codeberg.org/eltonarodrigues/panapidas
%global         tag           v%{version}
%global         dukpy_ver     0.6.0
%global         debug_package %{nil}

Name:           panapidas
Version:        1.0.0
Release:        1%{?dist}
Summary:        HTTP client for APIs
License:        GPL-3.0-only AND MIT
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}
# dukpy is not packaged in Fedora; bundle and build from source
Source1:        https://files.pythonhosted.org/packages/85/f5/0d731f71f68a784e9637c74bfd93ee36666f303da1ad32fed5dc26a54bed/dukpy-%{dukpy_ver}.tar.gz

BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(gtksourceview-5)

Requires:       gtk4
Requires:       libadwaita
Requires:       gtksourceview5
Requires:       hicolor-icon-theme
Requires:       libsecret
Requires:       libsoup3
Requires:       python3-gobject

Provides:       bundled(python3dist(dukpy)) = %{dukpy_ver}

%description
A simple HTTP client written in GTK/LibAdwaita. Panapidas focuses on being a simple client with the essentials for using and testing APIs.

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}

pip3 install --no-deps --no-build-isolation --ignore-installed \
    --prefix=%{_prefix} --root=%{buildroot} %{SOURCE1}

%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

%check
%meson_test "Validate desktop file" "Validate schema file" "Validate appstream file"

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/dukpy
%{_bindir}/dukpy-install
%{_datadir}/%{name}
%{python3_sitelib}/%{name}/
%{python3_sitearch}/dukpy/
%{python3_sitearch}/dukpy-*.dist-info/
%{_datadir}/gtksourceview-5/language-specs/request_custom_json.lang
%{_datadir}/gtksourceview-5/styles/json-variable-style.xml
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_dbusservicesdir}/%{app_id}.service
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Sat Nov 28 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.0.0-1
- First Release
- Create requests
- Support for HTTP + REST requests
- Group requests
- Add certificates
- Use of variables in requests
- Pre/post-request JavaScript scripts
