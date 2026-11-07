%global app_id        dev.geopjr.Collision
%global forgeurl      https://codeberg.org/GeopJr/collision
%global tag           v%{version}

Name:                 collision
Version:              0
Release:              1%{?dist}
Summary:              Check hashes for your files
BugURL:               https://github.com/Infiniti151/flatpak-apps
License:              BSD-2-Clause

%forgemeta

URL:                  %{forgeurl}
Source0:              %{forgesource}

ExclusiveArch:        x86_64

BuildRequires:        make
BuildRequires:        gettext
BuildRequires:        desktop-file-utils
BuildRequires:        appstream
BuildRequires:        glib2-devel
BuildRequires:        pkgconfig(gtk4)
BuildRequires:        pkgconfig(libadwaita-1)
BuildRequires:        pkgconfig(gobject-introspection-1.0)
BuildRequires:        libyaml-devel
BuildRequires:        openssl-devel
BuildRequires:        blake3-devel

Requires:             nautilus-python

%description
Verifying that a file you downloaded or received is actually the one you were
expecting is often overlooked or too time-consuming to do. At the same time, it
has become very easy to get your hands on a file that has been tampered with, due
to the mass increase of malicious webpages and other actors.

This tool aims to solve that. Collision comes with a simple & clean UI, allowing
anyone, from any age and experience group, to generate, compare and verify MD5,
SHA-256, SHA-512, SHA-1, Blake3, CRC32 and Adler32 hashes.

%prep
%forgesetup

CRYSTAL_VERSION="$(awk '/^crystal:/ {print $2}' shard.yml)"

curl -fLo crystal.tar.gz \
    "https://github.com/crystal-lang/crystal/releases/download/${CRYSTAL_VERSION}/crystal-${CRYSTAL_VERSION}-1-linux-x86_64.tar.gz"

tar -xf crystal.tar.gz

%build
CRYSTAL_VERSION="$(awk '/^crystal:/ {print $2}' shard.yml)"

export PATH="$PWD/crystal-${CRYSTAL_VERSION}-1/bin:$PATH"
export CRYSTAL_CACHE_DIR="$PWD/.crystal-cache"

make
make metainfo

%install
install -Dpm755 \
    bin/%{name} \
    %{buildroot}%{_bindir}/%{name}

install -Dpm644 \
    data/%{app_id}.gschema.xml \
    %{buildroot}%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml

install -Dpm644 \
    data/%{app_id}.desktop \
    %{buildroot}%{_datadir}/applications/%{app_id}.desktop

install -Dpm644 \
    data/%{app_id}.metainfo.xml \
    %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

install -Dpm644 \
    data/icons/%{app_id}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg

install -Dpm644 \
    data/icons/%{app_id}-symbolic.svg \
    %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/%{app_id}-symbolic.svg

install -Dpm644 \
    nautilus-extension/%{name}-extension.py \
    %{buildroot}%{_datadir}/nautilus-python/extensions/%{name}-extension.py

mkdir -p %{buildroot}%{_datadir}/locale

for lang in $(cat po/LINGUAS); do
    [ "$lang" = "en" ] && continue
    [ -z "$lang" ] && continue

    msgfmt po/$lang.po -o $lang.mo

    install -Dpm644 \
        $lang.mo \
        %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/%{app_id}.mo
done

%find_lang %{app_id} %{name}.lang

%check
CRYSTAL_VERSION="$(awk '/^crystal:/ {print $2}' shard.yml)"

export PATH="$PWD/crystal-${CRYSTAL_VERSION}-1/bin:$PATH"
export CRYSTAL_CACHE_DIR="$PWD/.crystal-cache"

make test

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/nautilus-python/extensions/%{name}-extension.py
%{_metainfodir}/%{app_id}.metainfo.xml