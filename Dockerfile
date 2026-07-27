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
    # --- newsflash dependencies --- \
    'pkgconfig(clapper-gtk-0.0)' \
    'pkgconfig(gio-2.0)' \
    'pkgconfig(glib-2.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(libadwaita-1)' \
    'pkgconfig(libxml-2.0)' \
    'pkgconfig(openssl)' \
    'pkgconfig(sqlite3)' \
    'pkgconfig(webkitgtk-6.0)' \
    blueprint-compiler \
    cargo \
    clang-devel \
    desktop-file-utils \
    gcc \
    gettext \
    libappstream-glib \
    meson \
    ninja-build \
    rust \
    && dnf clean all

ENV CCACHE_COMPILERCHECK=content
ENV CCACHE_MAXSIZE=2G
ENV CARGO_INCREMENTAL=0

WORKDIR /github/workspace
