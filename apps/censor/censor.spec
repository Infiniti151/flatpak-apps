%global         app_id        page.codeberg.censor.Censor
%global         forgeurl      https://codeberg.org/censor/censor
%global         tag           v%{version}

Name:           censor
Version:        0.10.2
Release:        1%{?dist}
Summary:        Redact PDF documents
License:        GPL-3.0-or-later AND AGPL-3.0-only AND CC-BY-SA-4.0 AND CC0-1.0
BugURL:         https://github.com/Infiniti151/flatpak-apps

BuildArch:      noarch

%forgemeta

URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  git-core
BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  appstream
BuildRequires:  desktop-file-utils
BuildRequires:  desktop-rpm-macros
BuildRequires:  forge-srpm-macros
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  glibc-langpack-en
BuildRequires:  gtk-update-icon-cache
BuildRequires:  python3-devel
BuildRequires:  python3-pymupdf
BuildRequires:  python3-pytest

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       libadwaita
Requires:       python3-gobject
Requires:       python3-pymupdf

%description
Censor is a PDF document redaction tool. It permanently removes text and images in redacted areas and can draw rectangles over them.

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

%conf
%meson

%build
%meson_build

%install
%meson_install
install -d %{buildroot}%{_licensedir}/%{name}
install -pm 0644 LICENSES/GPL-3.0-or-later.txt \
                 LICENSES/CC-BY-SA-4.0.txt \
                 LICENSES/CC0-1.0.txt \
                 data/AGPL-3.0-only.txt \
                 %{buildroot}%{_licensedir}/%{name}/
rm -rf %{buildroot}%{_licensedir}/%{app_id}
%find_lang %{name}
%py3_shebang_fix %{buildroot}%{_bindir}/%{name} %{buildroot}%{_datadir}/%{name}

%check
%meson_test

%files -f %{name}.lang
%license %{_licensedir}/%{name}
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_appsdir}/*.desktop
%{_scalableiconsdir}/*.svg
%{_symboliciconsdir}/*.svg
%{_gschemasdir}/*.gschema.xml
%{_dbusservicesdir}/*.service
%{_metainfodir}/*.metainfo.xml


%changelog
* Wed Nov 18 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 0.10.2-1
- Censor with latest runtime
- Run Censor’s Flatpak package with GNOME 51 and updated translations

