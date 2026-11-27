%global         app_id        app.drey.Biblioteca
%global         forgeurl      https://github.com/sonnyp/Biblioteca
%global         tag           v%{version}

Name:           biblioteca
Version:        1.8
Release:        1%{?dist}
Summary:        Read GNOME documentation offline
License:        GPL-3.0-only
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}
Patch0:         https://raw.githubusercontent.com/Infiniti151/flatpak-apps/main/apps/biblioteca/rpm-doc-index-paths.patch
Patch1:         https://raw.githubusercontent.com/Infiniti151/flatpak-apps/main/apps/biblioteca/rpm-runtime-compatibility.patch

BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  flatpak
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  git-core
BuildRequires:  gjs
BuildRequires:  glib2-devel
BuildRequires:  gtk-update-icon-cache
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(webkitgtk-6.0)

Requires:       gtk4
Requires:       gjs
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       webkitgtk6.0

%description
Biblioteca lets you browse and read GNOME documentation. Among other things, Biblioteca comes with
- Offline documentation
- Web browsing
- Tabs
- Dark mode support
- Fuzzy search
- Mobile / adaptive

%prep
%forgesetup

# Re-initialize git context for forge tarballs to resolve submodules
if [ ! -d ".git" ]; then
	git init -q
	git remote add origin %{forgeurl}
	git fetch -q --depth 1 origin %{tag}
	git checkout -q -f FETCH_HEAD
fi
git submodule update --init --recursive --depth 1

# Apply RPM-specific patches after the checkout
%autopatch -p1

# Fetch the same docs the Flatpak ships
export FLATPAK_USER_DIR=%{_builddir}/flatpak-user
SDK_BRANCH=$(sed -n 's/.*"runtime-version": *"\([^"]*\)".*/\1/p' build-aux/%{app_id}.json)
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user -y --noninteractive --no-deps --no-related flathub \
  org.gnome.Sdk.Docs//"$SDK_BRANCH" %{app_id}//stable

%conf
%meson

%build
%meson_build

%install
DOCDIR=%{buildroot}%{_datadir}/%{app_id}/doc
install -d "$DOCDIR"

# Collect indexed API documentation from the GNOME SDK Docs extension and
# supplement it with documentation bundled by the application Flatpak.
APP_DOCS=%{_builddir}/flatpak-user/app/%{app_id}/x86_64/stable/active/files/share/doc
for d in %{_builddir}/flatpak-user/runtime/org.gnome.Sdk.Docs/x86_64/*/active/files/doc/*/ \
         "$APP_DOCS"/gom-1.0/ "$APP_DOCS"/jsonrpc-glib/ "$APP_DOCS"/libshumate-1.0/ \
         "$APP_DOCS"/libspelling-1/ "$APP_DOCS"/vte-2.91-gtk4/; do
  name=$(basename "$d")
  case "$name" in
    atk|libhandy-1|webkit2gtk-4.1|webkit2gtk-web-extension-4.1|javascriptcoregtk-4.1|gcr-3|gcr-ui-3|gck-1) continue ;;
  esac
  if [ -f "$d/index.json" ]; then
    cp -a "$d" "$DOCDIR/"
  fi
done

%meson_install

# Remove the temporary buildroot prefix from documentation file URIs.
sed -i 's|file://%{buildroot}|file://|g' %{buildroot}%{_datadir}/%{app_id}/doc-index.json

# Remove the development application icon, which is not needed for the RPM.
rm -f %{buildroot}%{_scalableiconsdir}/%{app_id}.Devel.svg

%check
%meson_test 'Validate desktop file' 'Validate schema file' 'Validate metainfo file'

%files
%license COPYING
%doc README.md
%{_bindir}/%{app_id}
%{_bindir}/%{name}
%{_datadir}/%{app_id}
%{_appsdir}/%{app_id}.desktop
%{_scalableiconsdir}/%{app_id}.svg
%{_symboliciconsdir}/%{app_id}-symbolic.svg
%{_gschemasdir}/%{app_id}.gschema.xml
%{_dbusservicesdir}/%{app_id}.service
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Fri Nov 27 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.8-1
- Update to 1.8
