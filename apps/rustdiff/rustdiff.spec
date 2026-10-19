%if 0%{?eln}
%global         _empty_manifest_terminate_build 0
%endif
%global         app_id com.digitalgex.RustDiff
%global         forgeurl        https://github.com/jereok91/rustdiff
%global         tag             v%{version}

Name:           rustdiff
Version:        1.0.3
Release:        1%{?dist}
Summary:        Semantic JSON, XML and SQL comparator
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        %{forgeurl}/releases/download/%{tag}/%{name}-frontend-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

# Runtime Requirements
Requires:       hicolor-icon-theme

%description
RustDiff is a desktop application that compares two JSON, XML or SQL
documents by their structure — keys, array indices, XML nodes and
attributes, SQL statements — instead of by raw text lines, and
highlights the differences in a clear, visual way. The diff engine is
written in Rust; the interface is a Tauri app with a web-based UI.

Main features:
- Semantic diff for JSON (key by key), XML (nodes, attributes and text) and SQL (statement by statement), with a line-by-line fallback for plain text.
- Split editor with syntax highlighting, automatic pretty-print and in-editor search.
- Inline and full-line highlighting for added, removed and changed items.
- Filterable table of differences, clickable to jump to the exact location.
- Graph view of JSON and XML documents with pan, zoom and node search.
- Light and dark themes that follow the system, and adjustable text size.
- Export to plain text or styled HTML.
- Session history backed by SQLite, searchable, with per-entry and bulk deletion.

%prep
%forgesetup

rm -rf desktop/dist

tar -xzf %{SOURCE1}
mv %{name}-frontend-%{version}/dist desktop/

mkdir -p cargo-home

%build
export CARGO_HOME=$(pwd)/cargo-home

cargo build --release \
    --features custom-protocol \
    -p %{name}-desktop

%install
install -Dm755 target/release/%{name} \
    %{buildroot}%{_bindir}/%{name}

install -Dm644 \
    data/%{app_id}.desktop \
    %{buildroot}%{_datadir}/applications/%{app_id}.desktop

install -Dm644 \
    data/%{app_id}.metainfo.xml \
    %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

install -Dm644 \
    data/icons/%{app_id}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg

mkdir -p %{buildroot}%{_datadir}/%{name}/locales
install -m644 locales/*.yml \
    %{buildroot}%{_datadir}/%{name}/locales/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_metainfodir}/*.metainfo.xml

%changelog
* Mon Oct 19 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.0.3-1
- Desktop-integration and editor-highlight fixes.
- The window announces the application id, so the desktop shows its real icon and groups it with its launcher.
- Editor highlighting is anchored to the diff paths, so a modified element is no longer painted as a whole added block when the other document appends a copy of it.
- The focused editor's ring closes on all four sides.

* Sun Oct 18 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.0.1-1
- Packaging fix: the application icon now ships as a PNG set alongside the SVG, because the Flatpak builder runtime decodes icons through a pipeline that cannot read the SVG.

* Tue Jul 28 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.4.0-1
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.3.3...v0.4.0
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.3.3...v0.4.0

* Thu Jul 23 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.3.3-1
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.3.2...v0.3.3
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.3.2...v0.3.3

* Tue Jul 21 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.3.2-1
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.3.1...v0.3.2
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.3.1...v0.3.2

* Sun Jul 05 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.2.2-1
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.2.1...v0.2.2
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.2.1...v0.2.2

* Fri Jul 03 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.2.1-1
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.2.0...v0.2.1

* Thu May 28 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.1.8-1
- *Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.1.7...v0.1.8

* Fri May 15 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.1.7-1
- **Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.1.6...v0.1.7
- **Full Changelog**: https://github.com/jereok91/rustdiff/compare/v0.1.6...v0.1.7

