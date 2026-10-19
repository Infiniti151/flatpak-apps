ARG FEDORA_VER=version

FROM fedora:${FEDORA_VER}

ENV TERM="xterm-256color"
RUN echo "color=always" >> /etc/dnf/dnf.conf
RUN echo "max_parallel_downloads=10" >> /etc/dnf/dnf.conf

RUN dnf install -y ccache \
    dnf-plugins-core \
    git-core \
    glibc-langpack-en \
    npm \
    rpm-build \
    rpmdevtools \
    rpmlint \
    sccache \
    # --- rustdiff dependencies --- \
    'pkgconfig(gio-2.0)' \
    'pkgconfig(gobject-2.0)' \
    'pkgconfig(javascriptcoregtk-4.1)' \
    'pkgconfig(libsoup-3.0)' \
    'pkgconfig(webkit2gtk-4.1)' \
    cargo \
    desktop-file-utils \
    libappstream-glib \
    rust \
    && dnf clean all

ENV CCACHE_COMPILERCHECK=content
ENV CCACHE_MAXSIZE=2G
ENV CARGO_INCREMENTAL=0

WORKDIR /github/workspace
