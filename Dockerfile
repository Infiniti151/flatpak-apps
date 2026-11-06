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
    # --- crosspipe dependencies --- \
    'pkgconfig(gee-0.8)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    'pkgconfig(libpipewire-0.3)' \
    'pkgconfig(libxml-2.0)' \
    desktop-file-utils \
    forge-srpm-macros \
    gcc \
    gettext \
    libappstream-glib \
    meson \
    ninja-build \
    valac \
    && dnf clean all

ENV CCACHE_COMPILERCHECK=content
ENV CCACHE_MAXSIZE=2G
ENV CARGO_INCREMENTAL=0

WORKDIR /github/workspace
