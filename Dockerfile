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
    # --- railway dependencies --- \
    'pkgconfig(gio-2.0)' \
    'pkgconfig(glib-2.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    appstream \
    blueprint-compiler \
    cairo-devel \
    cargo \
    cargo-rpm-macros \
    desktop-file-utils \
    env \
    forge-srpm-macros \
    gdk-pixbuf2-devel \
    gettext \
    gtk-update-icon-cache \
    meson \
    ninja-build \
    pango-devel \
    rustc && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace