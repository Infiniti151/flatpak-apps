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
    # --- missioncenter dependencies --- \
    blueprint-compiler \
    cargo \
    cargo-rpm-macros \
    clang \
    cmake \
    compiler-rt \
    desktop-file-utils \
    gcc \
    gettext \
    glib2-devel \
    gtk-update-icon-cache \
    libadwaita-devel \
    libappstream-glib \
    libdrm-devel \
    libinput-devel \
    libxkbcommon-devel \
    lld \
    mesa-libgbm-devel \
    meson \
    rustc \
    systemd-devel \
    upx \
    && dnf clean all

ENV CCACHE_COMPILERCHECK=content
ENV CCACHE_MAXSIZE=2G
ENV CARGO_INCREMENTAL=0

WORKDIR /github/workspace
