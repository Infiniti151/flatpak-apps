%if 0%{?eln}
%define _empty_manifest_terminate_build 0
%endif

%global app_id com.digitalgex.RustDiff

Name:           rustdiff
Version:        0.1.8
Release:        1%{?dist}
Summary:        A simple GTK-based diff viewer written in Rust
License:        GPLv3
URL:            https://github.com/jereok91/rustdiff
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

# Runtime Requirements
Requires:       gtk4
Requires:       libadwaita
Requires:       gtksourceview5
Requires:       hicolor-icon-theme

%description
RustDiff is a graphical tool to compare files and directories,
built with Rust and GTK4. It features syntax highlighting via gtksourceview5.

%prep
%autosetup -n rustdiff-%{version}
mkdir -p cargo-home

%build
export CARGO_HOME=$(pwd)/cargo-home
cargo build --release %{?_smp_mflags}

%install
install -Dm755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm644 data/%{app_id}.desktop \
    %{buildroot}%{_datadir}/applications/%{app_id}.desktop
install -Dm644 data/%{app_id}.metainfo.xml \
    %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml
install -Dm644 data/icons/%{app_id}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg

mkdir -p %{buildroot}%{_datadir}/%{name}/locales
install -m 644 locales/*.yml %{buildroot}%{_datadir}/%{name}/locales/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Thu May 28 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.1.8-1
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.1.7...v0.1.8

* Fri May 15 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.1.7-1
- **Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.1.6...v0.1.7
- **Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.1.6...v0.1.7

