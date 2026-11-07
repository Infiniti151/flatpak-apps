%global app_id         dev.geopjr.Collision
%global forgeurl       https://codeberg.org/GeopJr/Collision

Name:                 collision
Version:              1.0.0
Release:              1%{?dist}
Summary:              GTK application written in Crystal

License:              GPL-3.0-or-later
URL:                  %{forgeurl}
Source0:              %{forgeurl}/archive/v%{version}.tar.gz

ExclusiveArch:        x86_64

BuildRequires:        gettext
BuildRequires:        desktop-file-utils
BuildRequires:        appstream
BuildRequires:        glib2-devel
BuildRequires:        pkgconfig(gtk4)
BuildRequires:        pkgconfig(libadwaita-1)

Requires:       nautilus-python

%description
Collision is a GTK application written in Crystal.

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

# Generate bindings if required
if ! ./bin/gi-crystal; then
    shards install
    ./bin/gi-crystal
fi

# Desktop file
msgfmt --desktop \
    --template data/%{app_id}.desktop.in \
    -d po \
    -o data/%{app_id}.desktop

# AppStream metadata
msgfmt --xml \
    --template data/%{app_id}.metainfo.xml.in \
    -d po \
    -o data/%{app_id}.metainfo.xml

# Build application
COLLISION_LOCALE_LOCATION="%{_datadir}/locale" \
shards build \
    -Dpreview_mt \
    -Dexecution_context \
    --release \
    --no-debug

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
crystal spec \
    -Dpreview_mt \
    -Dexecution_context \
    --order random

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/nautilus-python/extensions/%{name}-extension.py
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Sat Nov 07 2026 Infiniti151 <43163551+Infiniti151@users.noreply.github.com> - 1.0.0-1
- Initial package