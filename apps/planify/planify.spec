%global         app_id              io.github.alainm23.planify
%global         forgeurl            https://github.com/alainm23/planify
%global         tag                 v%{version}

Name:           planify
Version:        4.21.0
Release:        1%{?dist}
Summary:        Forget about forgetting things
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  vala
BuildRequires:  valadoc
BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  appstream
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  python3
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  pkgconfig(chrono)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= 2.70
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(goa-1.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.7.0
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libical-glib)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libspelling-1)
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(libportal)
BuildRequires:  pkgconfig(libportal-gtk4)
BuildRequires:  pkgconfig(libecal-2.0) >= 3.45.1
BuildRequires:  pkgconfig(libedataserver-1.2) >= 3.45.1

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       hicolor-icon-theme

%description
Planify is your modern and powerful task manager that helps you keep your life organized. With a clean and intuitive interface, cloud synchronization, and advanced features, you'll never forget what matters again.

Core Features:
- Modern and clean interface designed with GTK4 and libadwaita
- Drag and drop to organize tasks and projects effortlessly
- Visual progress indicators for each project
- Smart organization with sections and custom labels
- Calendar integration to visualize your schedule
- Multiple reminders per task to never miss a deadline
- Dark mode with seamless system theme integration
- Quick and powerful search to find anything instantly
- Recurring tasks with flexible patterns
- Attachments and links in your tasks

Cloud Synchronization:
- Full synchronization with Todoist to access your tasks from anywhere
- Support for Nextcloud and CalDAV servers (Radicale, Baïkal) to keep your data private
- Offline mode: work without internet and sync when you're back online
- Cross-platform synchronization to access from any device

* Planify is not created by, affiliated with, or supported by Doist

%package        libs
Summary:        Shared libraries for %{name}

%description    libs
The %{name}-libs package contains the shared libraries used by applications
built around the Planify ecosystem.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, header files, and Vala bindings
for developing applications that use Planify's core API.

%prep
%forgesetup

# chrono is packaged separately (libchrono); never fall back to a bundled copy
rm -f subprojects/chrono.wrap

if [ -f scripts/update-translations.py ]; then
    python3 scripts/update-translations.py
fi

%conf
%meson \
    -Dprofile=default \
    -Dportal=true \
    -Devolution=true \
    -Dgoa=true \
    -Dspelling=enabled \
    -Dmanpage=false

%build
%meson_build

%install
%meson_install
%find_lang %{app_id}

rm -f %{buildroot}%{_scalableiconsdir}/%{app_id}.Devel.svg

%check
%meson_test --suite cli
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

%files -f %{app_id}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{app_id}*
%{_libexecdir}/%{app_id}-search-provider
%{_appsdir}/%{app_id}.desktop
%{_gschemasdir}/%{app_id}.gschema.xml
%{_metainfodir}/%{app_id}.metainfo.xml
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_dbusservicesdir}/{%{app_id}.service,%{app_id}.SearchProvider.service}
%{_searchprovidersdir}/%{app_id}.SearchProvider.ini

%files libs
%{_libdir}/libplanify.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/libplanify.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/vala/vapi/%{name}.*

%changelog
* Thu Nov 26 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 4.20.0-1
- Planify 4.20.0 is a big release with Nextcloud Deck integration, CalDAV reminder sync, productivity goals, GNOME Online Accounts detection, and many features, fixes and performance improvements. Update now and enjoy a smoother experience.
- New Features:
- Added Nextcloud Deck integration — boards, stacks and cards sync two-way as projects, sections and tasks, with labels, archive, drag and drop between stacks and boards, and order preservation.
- Added a productivity goals system — daily and weekly targets (fixed or dynamic), a mini progress widget in the app menu, and an 8-week activity heatmap in the productivity report.
- Added "Repeat from completion date" — recurring tasks can repeat from the day they are completed instead of their due date, per task, matching how apps like Tasks.org behave (local and Todoist).
- Added detection and import of CalDAV accounts from GNOME Online Accounts — a subtle link under the account list imports Nextcloud/ownCloud (via Login Flow v2) or generic CalDAV accounts with the server URL prefilled.
- Added a completed tasks section to the Today view, toggleable from the view settings.
- Added a project filter to the Completed view and sort/filter controls to the All Tasks view, matching the project views.
- Added All Tasks and Labels as Home View options in Preferences.
- Added a calendar sources preferences page to choose which calendars are shown.
- ... (see upstream for full release notes)

* Thu Nov 26 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 4.21.0-1
- Planify 4.21.0 brings offline support for CalDAV, Nextcloud and Nextcloud Deck, a more reliable Todoist sync, client certificates (mTLS), attachments that keep working after the original file moves, and many fixes and memory improvements.
- New Features:
- Added offline support for CalDAV and Nextcloud: tasks, sections and calendars can be created, edited, completed, moved and deleted without a connection, and are sent on the next sync.
- Added offline support for Nextcloud Deck: cards, stacks and boards work without a connection, including moving cards between boards.
- Added client certificate (mTLS) authentication for CalDAV and Nextcloud, with .pem and .p12/.pfx files.
- Attachments are now copied into Planify's data folder, so they keep opening after the original file is moved or deleted. Files can also be attached while creating a task.
- Added dragging tasks in All Tasks onto sidebar lists and onto other tasks to make them subtasks.
- Added sort and filter options to the Label view.
- Added sorting by deadline in projects, Today, Scheduled, filters and labels.
- Added setting a deadline on multiple selected tasks.
- ... (see upstream for full release notes)

* Sat Sep 12 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 4.20.0-1
- Planify 4.20.0 is a big release with Nextcloud Deck integration, CalDAV reminder sync, productivity goals, GNOME Online Accounts detection, and many features, fixes and performance improvements. Update now and enjoy a smoother experience.
- New Features:
- Added Nextcloud Deck integration — boards, stacks and cards sync two-way as projects, sections and tasks, with labels, archive, drag and drop between stacks and boards, and order preservation.
- Added a productivity goals system — daily and weekly targets (fixed or dynamic), a mini progress widget in the app menu, and an 8-week activity heatmap in the productivity report.
- Added "Repeat from completion date" — recurring tasks can repeat from the day they are completed instead of their due date, per task, matching how apps like Tasks.org behave (local and Todoist).
- Added detection and import of CalDAV accounts from GNOME Online Accounts — a subtle link under the account list imports Nextcloud/ownCloud (via Login Flow v2) or generic CalDAV accounts with the server URL prefilled.
- Added a completed tasks section to the Today view, toggleable from the view settings.
- Added a project filter to the Completed view and sort/filter controls to the All Tasks view, matching the project views.
- Added All Tasks and Labels as Home View options in Preferences.
- Added a calendar sources preferences page to choose which calendars are shown.
- ... (see upstream for full release notes)

* Thu Sep 03 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 4.19.5-1
- Planify 4.19.5 is a maintenance release focused on bug fixes, reliability improvements, and new features.
- Bug Fixes:
- Fixed missed automatic backup on startup — if Planify was closed at midnight, the scheduled backup was silently skipped. Now, if automatic backup is enabled and no backup has run today, one is triggered immediately on startup.
- Fixed completing a recurring task from a notification — it was marking the task as fully completed instead of advancing to the next occurrence. Now correctly calls update_next_recurrency() as the UI does.
- Fixed keyboard navigation UX — Tab in EditableTextView now moves focus to the next widget instead of inserting spaces, and pressing Enter on a focused checkbox now completes the task.
- Fixed attachment file_size integer overflow — file_size is now treated as a string throughout, preventing unhandled overflow errors for values ≥ 2^63.
- Fixed drag and drop reliability and visual feedback in ReorderChild — softer background, subtle border, and rounder corners using the accent color.
- Fixed CalDAV related-to parsing — uses the already known related-id from libical and checks the reltype param to determine if a task is a parent.
- Fixed reading X-PINNED and X-APPLE-SORT-ORDER from CalDAV — replaced ICal.PropertyKind.from_string() with iteration over X_PROPERTY kind and matching by get_x_name(), fixing pin status and sort order persistence with Radicale and other servers.
- New Features:
- ... (see upstream for full release notes)

* Wed Sep 02 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 4.18.0-1
- Refactored Quick Find to use ListView, significantly improving search performance with large result sets, thanks to @byquanton.
- Improved task rendering performance by lazily loading task details and batching ItemRow creation,reducing UI overhead and improving responsiveness, thanks to @byquanton.
- Fixed a crash when typing dates with years below 1000 in the due date picker, thanks to @pgrit.
- Optimized database operations by batching inserts when importing projects and batching deletes when removing them, improving overall performance, thanks to @byquanton.
- Fixed Quick Find getting stuck in multi-select mode by improving Ctrl key detection during mouse events, thanks to @pgrit.
- Added support for Todoist assignment filtering in the Today view, allowing filtering by assigned and unassigned tasks, thanks to @alyraffauf.
- Added a mandatory Todoist API migration flow with a warning and re-login option to ensure continued sync support, thanks to @alainm23.
- Improved Radicale CalDAV compatibility by accepting HTTP 201 responses for PUT requests, fixing sync issues when updating tasks, thanks to @mntmn.
- Fixed filtering by labels in Today and other non-project views, thanks to @byquanton.
- Fixed manual task ordering synchronization with CalDAV and Nextcloud, ensuring consistent ordering after drag and drop actions, thanks to @pgrit.
- ... (see upstream for full release notes)

* Sat Jul 18 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v4.19.5-1
- Planify 4.19.5 is a maintenance release focused on bug fixes, reliability improvements, and new features.
- Bug Fixes:
- Fixed missed automatic backup on startup — if Planify was closed at midnight, the scheduled backup was silently skipped. Now, if automatic backup is enabled and no backup has run today, one is triggered immediately on startup.
- Fixed completing a recurring task from a notification — it was marking the task as fully completed instead of advancing to the next occurrence. Now correctly calls update_next_recurrency() as the UI does.
- Fixed keyboard navigation UX — Tab in EditableTextView now moves focus to the next widget instead of inserting spaces, and pressing Enter on a focused checkbox now completes the task.
- Fixed attachment file_size integer overflow — file_size is now treated as a string throughout, preventing unhandled overflow errors for values ≥ 2^63.
- Fixed drag and drop reliability and visual feedback in ReorderChild — softer background, subtle border, and rounder corners using the accent color.
- Fixed CalDAV related-to parsing — uses the already known related-id from libical and checks the reltype param to determine if a task is a parent.
- Fixed reading X-PINNED and X-APPLE-SORT-ORDER from CalDAV — replaced ICal.PropertyKind.from_string() with iteration over X_PROPERTY kind and matching by get_x_name(), fixing pin status and sort order persistence with Radicale and other servers.
- New Features:
- ... (see upstream for full release notes)

* Thu Jun 04 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v4.19.4-1
- Planify 4.19.4 is a maintenance release focused on bug fixes.
- Bug Fixes:
- Fixed a crash when updating a task with no priority set on Mailbox.org and Open-Xchange servers.
- Fixed completed tasks generating an ambiguous local timestamp in the VTODO — now uses UTC with the Z suffix, fixing sync errors with DAVx5 on Android.
- Fixed inconsistent accent colors across the app — accent color logic is now centralized and correctly follows the system accent color setting.

