%global         forgeurl      https://github.com/ryonakano/ryokucha
%global         tag           %{version}

Name:           libryokucha
Version:        0.4.0
Release:        1%{?dist}
Summary:        GTK4 library that includes customized widgets
License:        LGPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.58.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  vala
BuildRequires:  forge-srpm-macros
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= 2.74
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(pango)

%description
Ryokucha (green tea in Japanese) is a GTK4 library that includes customized
widgets.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config file and Vala bindings for building applications against
%{name}.

%prep
%forgesetup

%conf
%meson -Ddemo=false -Ddoc=false

%build
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_libdir}/libryokucha.so

%files devel
%{_includedir}/ryokucha.h
%{_libdir}/pkgconfig/ryokucha.pc
%{_datadir}/vala/vapi/ryokucha.*

%changelog
* Thu Nov 19 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.4.0-1
- fix: DropDownText: Add missing default values of active_id, max_width_chars, and ellipsize (#13)
- NOTE: This is an API breaking change since it changes the behavior if you don't set values to these properties explicitly
