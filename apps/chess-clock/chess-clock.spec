%global         app_id        eu.fortysixandtwo.chessclock
%global         tag           v%{version}

Name:           chess-clock
Version:        0.6.3
Release:        1%{?dist}
Summary:        Time games of over-the-board chess
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps
URL:            https://gitlab.gnome.org/World/chess-clock

BuildArch:      noarch

BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  git-core
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gsound) >= 1.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.4
BuildRequires:  python3-devel

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3
Requires:       python3-gobject
Requires:       gsound
Requires:       libcanberra-backend-pulse

%description
Chess Clock is a simple application to provide time control for over-the-board chess games. Intended for mobile use, players select the time control settings desired for their game, then the black player taps their clock to start white's timer. After each player's turn, they tap the clock to start their opponent's, until the game is finished or one of the clocks reaches zero.

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
%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}/

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
* Fri Nov 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.6.3-1
- Runtime update and translations
- Update to GNOME 51 runtime
- Add brandcolors and maintenance updates, thanks to Brage Fuglseth
- New and updated translations.

