ARG FEDORA_VER=version

FROM fedora:${FEDORA_VER}

ENV TERM="xterm-256color"
RUN echo "color=always" >> /etc/dnf/dnf.conf
RUN echo "max_parallel_downloads=10" >> /etc/dnf/dnf.conf

RUN dnf install -y ccache \
    dnf-plugins-core \
    git-core \
    glibc-langpack-en \
    npm \
    rpm-build \
    rpmdevtools \
    rpmlint \
    sccache \
    # --- clairvoyant dependencies --- \
    'pkgconfig(glib-2.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    appstream \
    desktop-file-utils \
    forge-srpm-macros \
    gcc \
    gettext \
    glib2-devel \
    meson \
    ninja-build \
    python3-devel \
    valac \
    && dnf clean all

ENV CCACHE_COMPILERCHECK=content
ENV CCACHE_MAXSIZE=2G
ENV CARGO_INCREMENTAL=0

WORKDIR /github/workspace
