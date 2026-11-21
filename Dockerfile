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
    # --- recent-filter dependencies --- \
    desktop-file-utils \
    desktop-rpm-macros \
    forge-srpm-macros \
    gettext \
    glib2-devel \
    gtk-update-icon-cache \
    libappstream-glib \
    meson \
    ninja-build \
    python3-devel && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace