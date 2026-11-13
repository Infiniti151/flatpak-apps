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
    # --- chess-clock dependencies --- \
    'pkgconfig(gsound)' \
    'pkgconfig(libadwaita-1)' \
    appstream \
    desktop-file-utils \
    forge-srpm-macros \
    gettext \
    glib2-devel \
    gtk-update-icon-cache \
    meson \
    ninja-build \
    python3-devel && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace