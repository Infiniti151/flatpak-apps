%global         app_id        io.github.unrud.RecentFilter
%global         forgeurl      https://github.com/Unrud/recent-filter
%global         tag           v%{version}

Name:           recent-filter
Version:        0.1.10
Release:        1%{?dist}
Summary:        Exclude files and folders from recently used files
License:        GPL-3.0-or-later
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson >= 0.62.0
BuildRequires:  ninja-build
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  libappstream-glib
BuildRequires:  librsvg2-tools
BuildRequires:  python3-devel
BuildRequires:  python3-gobject

Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme
Requires:       python3
Requires:       python3-gobject

%description
Exclude specific files and folders from appearing in the list of recently used files.

Paths can be specified using wildcards, just like in a .gitignore file. This means you can use patterns such as "*.txt".

%prep
%forgesetup
sed -i "s|'discover', '-p', '\*_test.py'\],|'discover', '-s', meson.current_source_dir() / 'src', '-p', '*_test.py'], env: {'PYTHONPATH': meson.current_source_dir()},|" meson.build
sed -i 's/os\.expanduser/os.path.expanduser/g' src/filter_test.py
python3 - <<'PY'
from pathlib import Path

p_portal = Path("src/background_portal.py")
text_portal = p_portal.read_text()

old_status = """        except GLib.Error as e:
            if e.matches(Gio.DBusError.quark(), Gio.DBusError.UNKNOWN_METHOD):
                g_log('background-portal', GLib.LogLevelFlags.LEVEL_WARNING,
                      'Can\\'t set status message because method not available')
                return
            raise"""

new_status = """        except GLib.Error as e:
            g_log('background-portal', GLib.LogLevelFlags.LEVEL_WARNING,
                  'Can\\'t set status message: %s', e.message)
            return"""

old_req = """        self._background_proxy.call_sync(
            'RequestBackground', parameters, Gio.DBusCallFlags.NONE, -1)"""

new_req = """        try:
            self._background_proxy.call_sync(
                'RequestBackground', parameters, Gio.DBusCallFlags.NONE, -1)
        except GLib.Error as e:
            g_log('background-portal', GLib.LogLevelFlags.LEVEL_WARNING,
                  'Can\\'t request background execution: %s', e.message)"""

assert old_status in text_portal, "old_status not found"
assert old_req in text_portal, "old_req not found"
p_portal.write_text(
    text_portal.replace(old_status, new_status, 1).replace(old_req, new_req, 1)
)

p_service = Path("src/service.py")
text_service = p_service.read_text()

old_activate = """    def activate(self, window):
        def handle_response(autostart, background):
            self.active = autostart and background
        # TODO: No public API to get window handle
        window_handle = ''
        self._bg_portal.request_background(
            window_handle, N_('Activate background service'), True, True,
            [*COMMANDLINE, '--service'], handle_response)"""

new_activate = """    def activate(self, window):
        def handle_response(autostart, background):
            if autostart and background:
                self.active = True
        # TODO: No public API to get window handle
        window_handle = ''
        self.active = True
        self._bg_portal.request_background(
            window_handle, N_('Activate background service'), True, True,
            [*COMMANDLINE, '--service'], handle_response)"""

assert old_activate in text_service, "old_activate not found"
p_service.write_text(text_service.replace(old_activate, new_activate, 1))
PY

%conf
%meson

%build
%meson_build

%install
%meson_install

%find_lang %{name}

%py3_shebang_fix \
    %{buildroot}%{_bindir}/%{name} \
    %{buildroot}%{_datadir}/%{name}

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_appsdir}/%{app_id}.desktop
%{_gschemasdir}/%{app_id}.gschema.xml
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_hicolordir}/*/apps/%{app_id}.png
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Sat Nov 21 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.1.10-1
- Test