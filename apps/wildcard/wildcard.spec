%global         app_id        net.ffkkinos.Wildcard
%global         tag           v%{version}

Name:           wildcard
Version:        0.3.5
Release:        1%{?dist}
Summary:        Test your regular expressions
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            https://gitlab.gnome.org/World/Wildcard

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  git-core
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gtk4) >= 4.10
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5

Requires:       hicolor-icon-theme

%description
Wildcard gives you a nice and simple to use interface to test/practice regular expressions.

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
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.3.5-1
- Bigger release:
- Added highlighting of matched regex groups in text view.
- Added match information (overall match and groups) to the sidebar
- Quick reference panel now available as a dialog
- Updated translations
- If you would like to come with suggestions, report bugs, translate the app, or contribute otherwise, feel free to reach out!

