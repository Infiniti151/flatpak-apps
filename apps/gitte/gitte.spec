Name:           gitte
Version:        0.3.0
Release:        1%{?dist}
Summary:        A GTK4/libadwaita Git client for the GNOME desktop
License:        GPL-3.0-or-later
URL:            https://codeberg.org/ckruse/Gitte
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libgit2)
BuildRequires:  pkgconfig(libssh2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  openssl-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext

%description
A modern, feature-rich Git client designed for the GNOME desktop.
Built with GTK4 and libadwaita, it provides a seamless and
intuitive interface for managing repositories, branches,
and stashes.

%prep
%setup -q -n %{name}

%build
export LIBGIT2_SYS_USE_PKG_CONFIG=0
export LIBSSH2_SYS_USE_PKG_CONFIG=1

%meson
%meson_build

%install
%meson_install
%find_lang gitte

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/dbus-1/services/*.service

%changelog
* Wed May 13 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.3.0-1
- Update to 0.3.0

* Fri May 08 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.2.0-1
- Update to 0.2.0

