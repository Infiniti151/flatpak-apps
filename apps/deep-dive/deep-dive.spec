%global         app_id        io.github.tanaybhomia.DeepDive
%global         upstream_name deepdive
%global         forgeurl      https://github.com/tanaybhomia/DeepDive
%global         tag           v%{version}

Name:           deep-dive
Version:        0
Release:        1%{?dist}
Summary:        Stay focused with strict limits
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.50.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  python3-devel

Requires:       hicolor-icon-theme
Requires:       python3-gobject
Requires:       python3-cairo
Requires:       gtk4
Requires:       libadwaita

%description
Deep Dive is an active productivity timer built for the GNOME desktop. Based on the concept of "Submerging," it operates on the principle that deep work requires strict boundaries.

When you start a timer, you are going underwater where distractions cannot reach you. You either finish the dive, or you deliberately "Give Up" and surface early.
- Submerge Mode: Locks the timer, preventing pausing or skipping.
- Break Overlays: Forces you to take a screen break with a full-screen overlay.
- Do Not Disturb: Automatically silences system notifications during work blocks.
- Project Tracking and Stats: Logs focused time against specific projects securely on your device.

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%py3_shebang_fix %{buildroot}%{_bindir}/%{upstream_name} %{buildroot}%{_datadir}/%{upstream_name}/

%check
%meson_test
desktop-file-validate %{buildroot}%{_appsdir}/%{app_id}.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/%{upstream_name}
%{_datadir}/%{upstream_name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/*-symbolic.svg
%{_metainfodir}/%{app_id}.metainfo.xml
