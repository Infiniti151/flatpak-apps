%global         app_id        com.cassidyjames.clairvoyant
%global         forgeurl      https://github.com/cassidyjames/clairvoyant
%global         tag           %{version}

Name:           clairvoyant
Version:        3.1.14
Release:        1%{?dist}
Summary:        Ask questions, get psychic answers
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.5.2
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  pkgconfig(glib-2.0) >= 2.82.0
BuildRequires:  pkgconfig(gtk4) >= 4.19.4
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8.1
BuildRequires:  python3-devel
BuildRequires:  valac

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita

%description
Does he love you? Should you have pizza for dinner? Is there such thing as a stupid question? Discover the answers to these questions and more with Clairvoyant, the magic 8-ball inspired fortune teller.
- Ask a question, then open Clairvoyant for an answer.
- Not satisfied? Ask again, then hit "Ask Again" to try again.
- Do what you'd like with the answers—just don't shoot the messenger!

Warning: it has been noted that “such a program can lead people away from God, as they are making an idol of an application and putting their faith into a virtual 8 ball.” Proceed at your own risk!

%prep
%forgesetup

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{app_id}

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml

%files -f %{app_id}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/applications/*.desktop
%{_scalableiconsdir}/*.svg
%{_hicolordir}/symbolic/apps/*.svg
%{_metainfodir}/*.metainfo.xml


%changelog
* Tue Nov 10 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 3.1.14-1
- Translations are flowing again! “Don’t count on it.” finally shows up in Persian, and translators can once again translate the latest store listing and release notes.
- https://github.com/cassidyjames/clairvoyant/compare/3.1.13...3.1.14

