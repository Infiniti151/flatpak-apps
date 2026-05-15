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
    sccache \
    # --- rustdiff dependencies --- \
    'pkgconfig(gtk4)' \
    'pkgconfig(gtksourceview-5)' \
    'pkgconfig(libadwaita-1)' \
    cargo \
    desktop-file-utils \
    libappstream-glib \
    rust \
    && dnf clean all

ENV CCACHE_DIR=/github/workspace/.ccache \
    SCCACHE_DIR=/github/workspace/.sccache \
    CARGO_HOME=**/rpmbuild/BUILD/**/redhat-linux-build/cargo-home \
    CARGO_INCREMENTAL=0 \
    CCACHE_COMPILERCHECK=content

WORKDIR /github/workspace