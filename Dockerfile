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
    # --- laser dependencies --- \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    appstream \
    blueprint-compiler \
    cdparanoia-devel \
    desktop-file-utils \
    forge-srpm-macros \
    gettext \
    glib2-devel \
    glibc-langpack-en \
    gstreamer1-plugins-base-devel \
    gtk-update-icon-cache \
    libappstream-glib \
    libcdio-devel \
    libdiscid-devel \
    meson \
    ninja-build \
    python3-devel \
    swig \
    && dnf clean all

ENV CCACHE_COMPILERCHECK=content
ENV CCACHE_MAXSIZE=2G
ENV CARGO_INCREMENTAL=0

WORKDIR /github/workspace
