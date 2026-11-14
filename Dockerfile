ARG FEDORA_VER=version

FROM fedora:${FEDORA_VER}

ENV TERM="xterm-256color" \
    CCACHE_COMPILERCHECK=content \
    CCACHE_MAXSIZE=2G \
    CARGO_INCREMENTAL=0

RUN echo -e "color=always\nmax_parallel_downloads=10" >> /etc/dnf/dnf.conf && \
    dnf install -y ccache \
    dnf-plugins-core \
    git-core \
    glibc-langpack-en \
    npm \
    rpm-build \
    rpmdevtools \
    rpmlint \
    sccache \
    # --- graphs dependencies --- \
    'pkgconfig(gio-2.0)' \
    'pkgconfig(glib-2.0)' \
    'pkgconfig(gobject-2.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    'pkgconfig(libgsf-1)' \
    'pkgconfig(libxml-2.0)' \
    'pkgconfig(sqlite3)' \
    appstream \
    blueprint-compiler \
    desktop-file-utils \
    forge-srpm-macros \
    gcc \
    gettext \
    gobject-introspection \
    gtk-update-icon-cache \
    meson \
    python3-devel \
    python3-gobject \
    python3-matplotlib \
    python3-numpy \
    python3-pip \
    python3-pytest \
    python3-scipy \
    python3-sympy \
    vala && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

WORKDIR /github/workspace