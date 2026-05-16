%define debug_package %{nil}

Name:           aerion
Version:        0.2.3
Release:        1%{?dist}
Summary:        Desktop Mail Client (Official Binary)
License:        GPLv3
URL:            https://github.com/hkdb/aerion
BugURL:	        https://github.com/Infiniti151/flatpak-apps/issues

BuildArch:      x86_64

Source0:        https://github.com/hkdb/aerion/releases/download/v%{version}/aerion-v%{version}-linux-x86_64
Source1:        https://raw.githubusercontent.com/hkdb/aerion/main/brand/icon-beautyline.png

Requires:       desktop-file-utils
Requires:       shared-mime-info

%description
Aerion is a desktop mail client. This package contains the official binary
release.

%prep
cp %{SOURCE0} .
cp %{SOURCE1} .

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps

install -m 755 aerion-v%{version}-linux-x86_64 %{buildroot}%{_bindir}/aerion

install -m 644 icon-beautyline.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/aerion.png

cat <<EOF > %{buildroot}%{_datadir}/applications/io.github.hkdb.Aerion.desktop
[Desktop Entry]
Name=Aerion
Comment=Desktop Mail Client
Exec=aerion
Icon=aerion
Type=Application
Terminal=false
Categories=Network;Email;
StartupWMClass=Aerion
X-GNOME-UsesNotifications=true
MimeType=x-scheme-handler/mailto;message/rfc822;application/x-extension-eml;
EOF

%post
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%files
%{_bindir}/aerion
%{_datadir}/applications/io.github.hkdb.Aerion.desktop
%{_datadir}/icons/hicolor/256x256/apps/aerion.png


%changelog
* Sat May 16 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.2.3-1
- - Added Czech translation
- - Added drag-and-drop to move messages to another folder
- - Added cross account copy/move mail - [#108](https://github.com/hkdb/aerion/issues/108)
- - Added draggable recipients in composer - [#111](https://github.com/hkdb/aerion/issues/111)
- - Added auto-commit recipient on lost focus - [#85](https://github.com/hkdb/aerion/issues/85)
- - Added composer del/backspace guard to prevent accidental message delete
- - Fixed detached composer system theme detection - [#153](https://github.com/hkdb/aerion/issues/153)
- - Fixed launch flow - [#154](https://github.com/hkdb/aerion/issues/154)
- - Fixed dark theme rendering - [#155](https://github.com/hkdb/aerion/issues/155)
- - Added unread count update after background sync to ensure accuracy

* Sat May 16 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - v0.2.3-build1-1
- - Added Czech translation
- - Added drag-and-drop to move messages to another folder
- - Added cross account copy/move mail - [#108](https://github.com/hkdb/aerion/issues/108)
- - Added draggable recipients in composer - [#111](https://github.com/hkdb/aerion/issues/111)
- - Added auto-commit recipient on lost focus - [#85](https://github.com/hkdb/aerion/issues/85)
- - Added composer del/backspace guard to prevent accidental message delete
- - Fixed detached composer system theme detection - [#153](https://github.com/hkdb/aerion/issues/153)
- - Fixed launch flow - [#154](https://github.com/hkdb/aerion/issues/154)
- - Fixed dark theme rendering - [#155](https://github.com/hkdb/aerion/issues/155)
- - Added unread count update after background sync to ensure accuracy

