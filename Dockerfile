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
    # --- sitra dependencies --- \
    'pkgconfig(gee-0.8)' \
    'pkgconfig(gio-2.0)' \
    'pkgconfig(glib-2.0)' \
    'pkgconfig(gobject-2.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(json-glib-1.0)' \
    'pkgconfig(libadwaita-1)' \
    'pkgconfig(libsitra-0.1)' \
    'pkgconfig(libsoup-3.0)' \
    'pkgconfig(webkitgtk-6.0)' \
    appstream \
    blueprint-compiler \
    desktop-file-utils \
    desktop-rpm-macros \
    forge-srpm-macros \
    gcc \
    gettext \
    gtk-update-icon-cache \
    meson \
    ninja-build \
    valac && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace