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
    # --- extension-manager dependencies --- \
    'pkgconfig(gio-unix-2.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(json-glib-1.0)' \
    'pkgconfig(libadwaita-1)' \
    'pkgconfig(libsoup-3.0)' \
    'pkgconfig(libxml-2.0)' \
    appstream \
    blueprint-compiler \
    cmake \
    desktop-file-utils \
    forge-srpm-macros \
    gcc \
    gettext \
    glycin-gtk4-devel \
    meson && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace