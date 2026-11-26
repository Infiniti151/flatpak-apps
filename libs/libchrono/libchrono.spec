%global         forgeurl      https://github.com/alainm23/chrono
%global         tag           %{version}

Name:           libchrono
Version:        1.0.0
Release:        1%{?dist}
Summary:        Natural language date and time parser library for Vala/GLib applications
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.56
BuildRequires:  ninja-build
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  valac
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(glib-2.0) >= 2.70
BuildRequires:  pkgconfig(gobject-2.0)

%description
chrono parses natural language date and time strings such as "tomorrow", "next Monday", or "in 3 days" into GLib.DateTime objects. It supports recurrence rules and multiple languages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains the header, pkg-config file and Vala bindings
needed to develop applications that use chrono.

%prep
%forgesetup

%conf
%meson -Ddocs=false

%build
%meson_build

%install
%meson_install

# Library only: the metainfo is not needed
rm -f %{buildroot}%{_metainfodir}/io.github.alainm23.chrono.metainfo.xml

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_libdir}/%{name}.so

%files devel
%{_includedir}/chrono.h
%{_libdir}/pkgconfig/chrono.pc
%{_datadir}/vala/vapi/chrono.*

%changelog
* Thu Nov 26 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.0.0-1
- Initial release. Extracted from Planify with English and Spanish support.