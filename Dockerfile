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
    # --- exercise-timer dependencies --- \
    'pkgconfig(gtk4)' \
    'pkgconfig(json-glib-1.0)' \
    'pkgconfig(libadwaita-1)' \
    blueprint-compiler \
    desktop-file-utils \
    forge-srpm-macros \
    gcc \
    gettext \
    glib2-devel \
    glibc-langpack-en \
    gtk-update-icon-cache \
    libappstream-glib \
    meson \
    ninja-build \
    valac \
    && dnf clean all

ENV CCACHE_COMPILERCHECK=content
ENV CCACHE_MAXSIZE=2G
ENV CARGO_INCREMENTAL=0

WORKDIR /github/workspace
