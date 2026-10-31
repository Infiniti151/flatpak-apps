%if 0%{?eln}
%global         _empty_manifest_terminate_build 0
%endif
%global         app_id          io.gitlab.news_flash.NewsFlash
%global         forgeurl        https://gitlab.com/news-flash/news_flash_gtk
%global         tag             v.%{version}

%global         __brp_mangle_shebangs %{nil}
%global         debug_package %{nil}
%global         __spec_install_post /usr/lib/rpm/brp-compress

Name:           newsflash
Version:        6.0.0
Release:        1%{?dist}
Summary:        Keep up with your feeds
License:        GPLv3
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

# Compression Tools
%if 0%{?fedora} && ! 0%{?eln}
BuildRequires:  upx
%endif

# Build tools & utilities
BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  clang-devel
BuildRequires:  gettext
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  forge-srpm-macros

# Development libraries (-devel equivalent pkgconfig dependencies)
BuildRequires:  pkgconfig(glib-2.0) >= 2.70
BuildRequires:  pkgconfig(gio-2.0) >= 2.70
BuildRequires:  pkgconfig(gtk4) >= 4.12.0
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.4.0
BuildRequires:  pkgconfig(webkitgtk-6.0) >= 2.42.0
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(clapper-gtk-0.0)

# Runtime Requirements
Requires:       hicolor-icon-theme
Requires:       xdg-utils
Requires:       clapper
Requires:       libmicrodns
Requires:       libpeas

%description
Newsflash is a program designed to complement an already existing web-based RSS reader account.

It combines all the advantages of web based services like syncing across all your devices with everything you expect from a modern desktop program: Desktop notifications, fast search and filtering, tagging, handy keyboard shortcuts andhaving access to all your articles for as long as you like.

%prep
%forgesetup
mkdir -p cargo-home

%build
export CARGO_HOME=$(pwd)/cargo-home
%meson -Dprofile=default
%meson_build

%install
%meson_install

# Strip unneeded symbols and compress binary using UPX
strip --strip-unneeded %{buildroot}%{_bindir}/%{app_id}
%if 0%{?fedora} && ! 0%{?eln}
upx --best --lzma %{buildroot}%{_bindir}/%{app_id}
%endif

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/dbus-1/services/*.service
%{_metainfodir}/*.xml

%changelog
* Sat Oct 31 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 6.0.0-1
- Migrations
- As usual, there are database migrations. In addition, all secrets that were previously stored in Newsflash's own configuration files are moved into the system keyring. Expect a keyring unlock prompt on first start.
- Article View: Much Improved Display of HTML Content
- Support for details, summary, hr, svg, mark, q, del/ins and abbr tags
- More list styles (letters, Roman numerals, custom start values, reversed lists)
- Pick up lazy-loaded images
- Display non-video iframes as a link to the external content
- Improved styling of inline code
- Syntax highlighting of code blocks matches the article theme
- Improved math rendering
- ... (see upstream for full release notes)

* Sun Aug 02 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v.5.2.5-1
- Update to v.5.2.5

* Mon Jul 27 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v.5.2.4-1
- Update to v.5.2.4

