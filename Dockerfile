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
    # --- graphs dependencies --- \
    'pkgconfig(gee-0.8)' \
    'pkgconfig(gio-2.0)' \
    'pkgconfig(glib-2.0)' \
    'pkgconfig(gobject-2.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    'pkgconfig(sqlite3)' \
    appstream \
    blueprint-compiler \
    desktop-file-utils \
    forge-srpm-macros \
    g-ir-compiler \
    gcc \
    gettext \
    gtk-update-icon-cache \
    meson \
    ninja-build \
    pytest \
    python3-devel \
    python3-numpy \
    valac && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace