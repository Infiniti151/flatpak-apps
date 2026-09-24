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
    # --- decoder dependencies --- \
    'pkgconfig(gio-2.0)' \
    'pkgconfig(glib-2.0)' \
    'pkgconfig(gstreamer-1.0)' \
    'pkgconfig(gstreamer-base-1.0)' \
    'pkgconfig(gstreamer-plugins-bad-1.0)' \
    'pkgconfig(gstreamer-plugins-base-1.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    appstream \
    cairo-devel \
    cargo \
    cargo-rpm-macros \
    desktop-file-utils \
    forge-srpm-macros \
    gdk-pixbuf2-devel \
    gettext \
    glibc-langpack-en \
    gtk-update-icon-cache \
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
