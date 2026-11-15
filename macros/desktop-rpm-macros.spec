Name:           desktop-rpm-macros
Version:        1.1.0
Release:        1%{?dist}
Summary:        Custom RPM macros for desktop application packaging
License:        MIT

BuildArch:      noarch

Source0:        https://raw.githubusercontent.com/Infiniti151/flatpak-apps/main/macros/macros.desktop

%description
Provides shorthand path macros (%_appsdir, %_scalableiconsdir, %_searchprovidersdir, etc.) for GNOME and GTK RPM packaging on Fedora and COPR.

%prep
# Nothing to unpack

%build
# Nothing to compile

%check
# Nothing to test

%install
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -pm 0644 %{SOURCE0} %{buildroot}%{_rpmconfigdir}/macros.d/macros.desktop

%files
%{_rpmconfigdir}/macros.d/macros.desktop

%changelog
* Sun Nov 15 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.1.0-1
- Added desktop packaging macros for autostart entries, themes, backgrounds, wallpapers, MIME packages, D-Bus interfaces, GNOME Shell extensions and Nautilus extensions.

* Sat Nov 14 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v1.0.0-1
- Initial release