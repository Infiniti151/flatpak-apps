ARG FEDORA_VER=version

FROM fedora:${FEDORA_VER}

ENV TERM="xterm-256color" \
    CCACHE_COMPILERCHECK=content \
    CCACHE_MAXSIZE=2G \
    CARGO_INCREMENTAL=0

RUN echo -e "color=always\nmax_parallel_downloads=10" >> /etc/dnf/dnf.conf && \
    dnf install -y ccache \
    dnf-plugins-core \
    git-core \
    glibc-langpack-en \
    npm \
    rpm-build \
    rpmdevtools \
    rpmlint \
    sccache \
    # --- eartag dependencies --- \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    appstream \
    blueprint-compiler \
    desktop-file-utils \
    forge-srpm-macros \
    gettext \
    glib2-devel \
    meson \
    ninja-build \
    python3-acoustid \
    python3-aiofiles \
    python3-aiohttp \
    python3-aiohttp-retry \
    python3-audioread \
    python3-devel \
    python3-filetype \
    python3-gobject \
    python3-mutagen \
    python3-pillow \
    python3-pytest \
    python3-pytest-asyncio \
    python3-xxhash && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace