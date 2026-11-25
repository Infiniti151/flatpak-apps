%global         app_id        io.github.dprietob.queue
%global         forgeurl      https://github.com/dprietob/queue
%global         tag           %{version}

Name:           queue
Version:        1.1.0
Release:        1%{?dist}
Summary:        Manage and organize tasks
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gcc
BuildRequires:  valac
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  pkgconfig(gtk4) >= 4.12
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5
BuildRequires:  pkgconfig(sqlite3)

Requires:       hicolor-icon-theme

%description
Queue is a simple, fast task manager.

Organize your tasks into groups, mark them as done or important, reorder them with drag and drop, and keep your data safe with built-in backups.

Features:
- Organize tasks into custom, color-coded groups.
- Mark tasks as completed or important.
- Write rich task descriptions with headings, text styles, colors and lists.
- See the date when each task was completed.
- Reorder groups and tasks with drag and drop.
- Export and restore all your data as JSON.
- Light and dark styles, available in several languages.

%prep
%forgesetup

%conf
%meson

%build
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_hicolordir}/*/apps/%{app_id}.png
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Wed Nov 25 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.1.0-1
- This release brings rich text descriptions and several refinements:
- Format task descriptions with headings, bold, italic, underline, strikethrough, text color and lists.
- See the completion date of finished tasks.
- Edit and delete tasks and groups from a per-item menu.
- The task list now uses the full width of the window.
- Task descriptions can now hold much longer text.
- Added Polish, Russian, Korean, Norwegian, Swedish, Hindi and Greek translations.
