%define debug_package %{nil}

Name:           aerion
Version:        0.2.5
Release:        1%{?dist}
Summary:        Desktop Mail Client (Official Binary)
License:        GPLv3
URL:            https://github.com/hkdb/aerion
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

ExclusiveArch:  x86_64

Source0:        https://github.com/hkdb/aerion/releases/download/v%{version}/aerion-v%{version}-linux-x86_64
Source1:        https://raw.githubusercontent.com/hkdb/aerion/main/brand/icon-beautyline.png
Source2:        https://raw.githubusercontent.com/hkdb/aerion/main/build/linux/aerion.desktop

Requires:       desktop-file-utils
Requires:       shared-mime-info

%description
Aerion is a desktop mail client. This package contains the official binary
release.

%prep
cp %{SOURCE0} .
cp %{SOURCE1} .
cp %{SOURCE2} .

%build
# No-op: packaging a prebuilt binary

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps

install -m 755 aerion-v%{version}-linux-x86_64 %{buildroot}%{_bindir}/aerion

install -m 644 icon-beautyline.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/io.github.hkdb.Aerion.png

install -m 644 aerion.desktop %{buildroot}%{_datadir}/applications/io.github.hkdb.Aerion.desktop

%check
echo "==> Checking dynamic library dependencies..."
ldd %{buildroot}%{_bindir}/aerion

%post
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%files
%{_bindir}/aerion
%{_datadir}/applications/io.github.hkdb.Aerion.desktop
%{_datadir}/icons/hicolor/256x256/apps/io.github.hkdb.Aerion.png

%changelog
* Wed May 27 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.2.5-1
- Sync progress indication redesign and shifting folder tree fix - [#204](https://github.com/hkdb/aerion/issues/204)
- Added German translation - PR [#194](https://github.com/hkdb/aerion/pull/194)
- Added Italian translation - PR [#208](https://github.com/hkdb/aerion/pull/208)
- Dark content auto bg color and overrides - [#195](https://github.com/hkdb/aerion/issues/195)
- Added guard rails to prevent accidental close of dialogs - [#201](https://github.com/hkdb/aerion/issues/201) - [#198](https://github.com/hkdb/aerion/issues/198)
- Fixed message list on folder switch bug - [#200](https://github.com/hkdb/aerion/issues/200)
- Fixed detached composer draft ops - [#213](https://github.com/hkdb/aerion/issues/213) - [#214](https://github.com/hkdb/aerion/issues/214)
- Fixed send receipt feature
- Fixed dark themes composer lists - [#215](https://github.com/hkdb/aerion/issues/215)
- Fixed setting dialog layout - [#203](https://github.com/hkdb/aerion/issues/203)
- ... (see upstream for full release notes)

* Wed May 20 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.2.4-1
- Improved oAuth browser open - [#120](https://github.com/hkdb/aerion/issues/120)
- Added copy link for oAuth - [#120](https://github.com/hkdb/aerion/issues/120)
- Added dark mail content option - [#49](https://github.com/hkdb/aerion/issues/49)
- Use desktop portal for email links first and fallback to xdg-open if it fails
- Added -version flag - [#167](https://github.com/hkdb/aerion/issues/167)
- Added setup exe and default app registration for Windows - [#149](https://github.com/hkdb/aerion/issues/149)
- Added Norwegian translation - [#150](https://github.com/hkdb/aerion/issues/150)
- Fixed dark to light core theme switch bug - [#187](https://github.com/hkdb/aerion/issues/187)

* Sat May 16 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.2.3-1
- Added Czech translation
- Added drag-and-drop to move messages to another folder
- Added cross account copy/move mail - [#108](https://github.com/hkdb/aerion/issues/108)
- Added draggable recipients in composer - [#111](https://github.com/hkdb/aerion/issues/111)
- Added auto-commit recipient on lost focus - [#85](https://github.com/hkdb/aerion/issues/85)
- Added composer del/backspace guard to prevent accidental message delete
- Fixed detached composer system theme detection - [#153](https://github.com/hkdb/aerion/issues/153)
- Fixed launch flow - [#154](https://github.com/hkdb/aerion/issues/154)
- Fixed dark theme rendering - [#155](https://github.com/hkdb/aerion/issues/155)
- Added unread count update after background sync to ensure accuracy

