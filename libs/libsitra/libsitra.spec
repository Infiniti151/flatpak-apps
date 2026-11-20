%global         forgeurl      https://github.com/sitraorg/libsitra
%global         tag           v%{version}

Name:           libsitra
Version:        0.1.0
Release:        1%{?dist}
Summary:        A library to list and manage online fonts on your system
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  valac

%description
A library to list and manage online fonts on your system.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING
%doc README.md
%{_libdir}/libsitra.so.*

%files devel
%{_includedir}/libsitra.h
%{_libdir}/libsitra.so
%{_libdir}/pkgconfig/libsitra-0.1.pc
%{_datadir}/vala/vapi/libsitra-0.1.vapi
%{_datadir}/gir-1.0/Libsitra-0.1.gir

%changelog
* Mon Nov 16 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.1.0-1
- Update to version 0.1.0
