%global         app_id        re.sonny.Commit
%global         forgeurl      https://github.com/sonnyp/Commit
%global         tag           v%{version}

Name:           commit
Version:        4.6
Release:        1%{?dist}
Summary:        Commit message editor
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  gjs
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(gtksourceview-5)

Requires:       gjs
Requires:       gtk4
Requires:       gtksourceview5
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       libportal
Requires:       libsoup3
Requires:       libspelling

%description
Commit is an editor that helps you write better Git and Mercurial commit messages.

After installing make sure to launch the application and follow the instructions.

Commit will pop up automatically when you make a commit in one of your projects. To save your commit message, press the Commit button or the Ctrl+Return shortcut. To abort and dismiss Commit, press the Abort button or the Escape key.

Features:
- Highlights overflow of the commit title
- Smart body wrapping
- Inserts a blank line between title and body
- Spell checking
- Comments are read-only and excluded from "Select All"
- Displays project folder and branch in window header
- Dark mode support
- Keyboard navigation and shortcuts
- Undo/Redo support
- Emoji picker
- Supports git commit, merge, tag --annotate, add --patch, rebase --interactive
- Supports Mercurial commit
- Auto capitalize the commit title
- Welcome window with settings and instructions
- Highlight syntax for Git, Mercurial and diffs

%prep
%forgesetup

# Re-initialize git context for forge tarballs to resolve submodules
if [ ! -d ".git" ]; then
    git init -q
    git remote add origin %{forgeurl}
    git fetch -q --depth 1 origin %{tag}
    git checkout -q -f FETCH_HEAD
fi
git submodule update --init --recursive

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{app_id}

%check
%meson_test
desktop-file-validate %{buildroot}%{_appsdir}/*.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/*.metainfo.xml
glib-compile-schemas --dry-run --strict %{buildroot}%{_gschemasdir}/

%files -f %{app_id}.lang
%license COPYING
%doc README.md
%{_bindir}/%{app_id}
%{_datadir}/%{app_id}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_metainfodir}/*.metainfo.xml


%changelog
* Wed Nov 18 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 4.6-1
- GNOME Platform 51

