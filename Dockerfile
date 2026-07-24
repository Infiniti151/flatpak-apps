ARG FEDORA_VER=version

FROM fedora:${FEDORA_VER}

ENV TERM="xterm-256color"
RUN echo "color=always" >> /etc/dnf/dnf.conf
RUN echo "max_parallel_downloads=10" >> /etc/dnf/dnf.conf

RUN dnf install -y \
    ccache \
    dnf-plugins-core \
    git-core \
    npm \
    rpm-build \
    rpmdevtools \
    rpmlint \
    sccache \
    # --- sudoku dependencies --- \
    'pkgconfig(glib-2.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    blueprint-compiler \
    desktop-file-utils \
    gcc \
    gettext \
    libappstream-glib \
    meson \
    pkgconfig \
    python3-devel \
    python3-iniconfig \
    python3-packaging \
    python3-pip \
    python3-pluggy \
    python3-pytest \
    python3-wheel \
    && dnf clean all

ENV CCACHE_COMPILERCHECK=content
ENV CCACHE_MAXSIZE=2G
ENV CARGO_INCREMENTAL=0

WORKDIR /github/workspace
