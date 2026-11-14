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
    # --- emergency-alerts dependencies --- \
    'pkgconfig(granite-7)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(json-glib-1.0)' \
    'pkgconfig(libadwaita-1)' \
    'pkgconfig(libportal)' \
    'pkgconfig(libsoup-3.0)' \
    'pkgconfig(shumate-1.0)' \
    appstream \
    desktop-file-utils \
    forge-srpm-macros \
    gcc \
    gettext \
    glib2-devel \
    gtk-update-icon-cache \
    meson \
    ninja-build \
    valac && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace