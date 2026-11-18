ARG FEDORA_VER=version

FROM fedora:${FEDORA_VER}

ENV TERM="xterm-256color" \
    CCACHE_COMPILERCHECK=content \
    CCACHE_MAXSIZE=2G \
    CARGO_INCREMENTAL=0

RUN echo -e "color=always\nmax_parallel_downloads=10" >> /etc/dnf/dnf.conf && \
    dnf copr enable -y infiniti151/flatpak-apps && \
    dnf install -y ccache \
    dnf-plugins-core \
    glibc-langpack-en \
    npm \
    rpm-build \
    rpmdevtools \
    rpmlint \
    sccache \
    # --- mundi dependencies --- \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    cargo \
    desktop-file-utils \
    desktop-rpm-macros \
    forge-srpm-macros \
    gettext \
    libappstream-glib \
    meson \
    pkgconfig \
    rustc && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace