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
    # --- identity dependencies --- \
    'pkgconfig(dav1d)' \
    'pkgconfig(gio-2.0)' \
    'pkgconfig(glib-2.0)' \
    'pkgconfig(glycin-2)' \
    'pkgconfig(glycin-gtk4-2)' \
    'pkgconfig(gstreamer-1.0)' \
    'pkgconfig(gstreamer-video-1.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    'pkgconfig(libwebpdemux)' \
    appstream \
    blueprint-compiler \
    cairo-devel \
    cargo \
    cargo-rpm-macros \
    desktop-file-utils \
    desktop-rpm-macros \
    forge-srpm-macros \
    gcc \
    gcc-c++ \
    gdk-pixbuf2-devel \
    gettext \
    gtk-update-icon-cache \
    meson \
    ninja-build \
    pango-devel \
    rustc && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace