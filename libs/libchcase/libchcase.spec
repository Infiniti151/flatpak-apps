%global         forgeurl      https://github.com/ryonakano/chcase
%global         tag           %{version}

Name:           libchcase
Version:        3.0.0
Release:        1%{?dist}
Summary:        Small library to convert case of a given string
License:        LGPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.56.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  vala
BuildRequires:  forge-srpm-macros
BuildRequires:  pkgconfig(glib-2.0)

%description
ChCase is a small library to convert case of a given string between camelCase,
PascalCase, snake_case, kebab-case, Sentence case, and space-separated.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, pkg-config file and Vala bindings for building applications against
%{name}.

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
%license LICENSE
%doc README.md
%{_libdir}/libchcase.so

%files devel
%{_includedir}/chcase.h
%{_libdir}/pkgconfig/chcase.pc
%{_datadir}/vala/vapi/chcase.*

%changelog
* Thu Nov 19 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 3.0.0-1
- API Breaking Changes
- Correct the prefix of all APIs in C: ch_case_ to chcase_ (#27)
- You wouldn't be affected to this change unless you're using ChCase from C or writing bindings for it
- Bugfixes
- Fix build error in user projects when building with -Werror=missing-include-dirs (#29)
- Other Changes
- Improve documentation
