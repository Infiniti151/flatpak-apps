%global         app_id        net.codelogistics.clicker
%global         tag           %{version}

Name:           clicker
Version:        0.2.0
Release:        1%{?dist}
Summary:        Simulate user input repeatedly
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

URL:            https://gitlab.gnome.org/eyekay/clicker

BuildArch:      noarch

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel

Requires:       gtk4
Requires:       gtksourceview5
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       libportal
Requires:       python3
Requires:       python3-gobject
Requires:       python3-libevdev

%description
Clicker is an auto clicker - it can simulate user input like mouse clicks and key presses repeatedly at given intervals for a given duration. This is useful in some video games.

Clicker works on both Wayland and X11 by simulating a remote desktop session. The user will need to grant this permission each time they start an automation.

The automation can be paused at any point by pressing the F5 key, if the user's desktop environment provides support for the Global Shortcuts portal and the user grants permission for this hotkey to be registered.

%prep
rm -rf %{name}-%{version}
git clone --depth 1 --branch %{tag} %{url}.git %{name}-%{version}
rm -rf %{name}-%{version}/.git
%setup -T -D -n %{name}-%{version}

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
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_metainfodir}/*.metainfo.xml


%changelog
* Tue Nov 17 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.2.0-1
- Automations can now be stopped at any point by pressing "F5".
- The app now remembers the previously set values for delay, duration of automation etc.
- Added Japanese (camegone), Italian (Albano Battistella) and Brazilian Portuguese (johnpetersa19) translations.

