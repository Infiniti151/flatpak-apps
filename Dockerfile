ARG FEDORA_VER=version

FROM fedora:${FEDORA_VER}

ENV TERM="xterm-256color"
RUN echo "color=always" >> /etc/dnf/dnf.conf
RUN echo "max_parallel_downloads=10" >> /etc/dnf/dnf.conf

RUN dnf install -y ccache \
    dnf-plugins-core \
    git-core \
    npm \
    rpm-build \
    rpmdevtools \
    rpmlint \
    sccache \
    # --- transition dependencies --- \
    cairo-devel \
    cargo \
    cargo-rpm-macros \
    desktop-file-utils \
    forge-srpm-macros \
    gdk-pixbuf2-devel \
    gettext \
    glib2-devel \
    glibc-langpack-en \
    gstreamer1-devel \
    gstreamer1-plugins-base-devel \
    gtk-update-icon-cache \
    gtk4-devel \
    libadwaita-devel \
    libappstream-glib \
    meson \
    ninja-build \
    pango-devel \
    rustc \
    && dnf clean all

ENV CCACHE_COMPILERCHECK=content
ENV CCACHE_MAXSIZE=2G
ENV CARGO_INCREMENTAL=0

WORKDIR /github/workspace
