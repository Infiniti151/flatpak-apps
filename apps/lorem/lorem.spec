%global         app_id        org.gnome.design.Lorem
%global         tag           %{version}

Name:           lorem
Version:        1.7
Release:        1%{?dist}
Summary:        Generate placeholder text
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            https://gitlab.gnome.org/World/design/lorem

BuildRequires:  meson >= 1.7
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  cargo
BuildRequires:  clippy
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gio-2.0) >= 2.76
BuildRequires:  pkgconfig(glib-2.0) >= 2.76
BuildRequires:  pkgconfig(gtk4) >= 4.23
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.alpha

Requires:       hicolor-icon-theme

%description
Simple app to generate the well-known Lorem Ipsum placeholder text.

%prep
rm -rf %{name}-%{version}
git clone --depth 1 --branch %{tag} %{url}.git %{name}-%{version}
rm -rf %{name}-%{version}/.git
%setup -T -D -n %{name}-%{version}

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_fontsdir}/SourceSerif4.ttf
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Thu Nov 19 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.7-1
- Update to 1.7

