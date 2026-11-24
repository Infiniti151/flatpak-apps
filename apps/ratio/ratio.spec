%global         app_id          com.markwyner.ratio
%global         forgeurl        https://codeberg.org/markwyner/ratio-for-linux
%global         tag             v%{version}

Name:           ratio
Version:        1.0.4
Release:        1%{?dist}
Summary:        Validate color contrast
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  forge-srpm-macros
BuildRequires:  desktop-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  desktop-file-utils
BuildRequires:  appstream

Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Ratio uses WCAG algorithms to validate color contrast for accessibility.
Using an eyedropper and a color picker, it shows you the contrast ratio
of your colors. You can toggle between text, large text, and non-text
(to meet WCAG Success Criteria 1.4.3, 1.4.11, and 2.4.13). I made it for
myself, but it is also my gift to you. (There’s also a macOS version available.)

%prep
%forgesetup

%build
%make_build PREFIX=%{_prefix}

%install
%make_install PREFIX=%{_prefix}

%py3_shebang_fix \
    %{buildroot}%{_bindir}/%{name} \
    %{buildroot}%{_datadir}/%{name}/

%check
desktop-file-validate %{buildroot}%{_appsdir}/%{app_id}.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_appsdir}/%{app_id}.desktop
%{_metainfodir}/%{app_id}.metainfo.xml
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_hicolordir}/actions/*.svg

%changelog
* Tue Nov 24 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.1.0-1
- Test