%define debug_package %{nil}

Name:           aerion
Version:        0.0.0
Release:        1%{?dist}
Summary:        Desktop Mail Client (Official Binary)
License:        GPLv3
URL:            https://github.com/hkdb/aerion
BugURL:         https://github.com/Infiniti151/flatpak-apps/issues

ExclusiveArch:      x86_64

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

%build
# No-op: packaging a prebuilt binary

%check
echo "==> Checking dynamic library dependencies..."
ldd %{buildroot}%{_bindir}/aerion

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


