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
    # --- planify dependencies --- \
    'pkgconfig(gee-0.8)' \
    'pkgconfig(gio-2.0)' \
    'pkgconfig(glib-2.0)' \
    'pkgconfig(gtk4)' \
    'pkgconfig(gtksourceview-5)' \
    'pkgconfig(icu-uc)' \
    'pkgconfig(json-glib-1.0)' \
    'pkgconfig(libadwaita-1)' \
    'pkgconfig(libecal-2.0)' \
    'pkgconfig(libedataserver-1.2)' \
    'pkgconfig(libical-glib)' \
    'pkgconfig(libportal)' \
    'pkgconfig(libportal-gtk4)' \
    'pkgconfig(libsecret-1)' \
    'pkgconfig(libsoup-3.0)' \
    'pkgconfig(libspelling-1)' \
    'pkgconfig(sqlite3)' \
    desktop-file-utils \
    gcc \
    gettext \
    libappstream-glib \
    meson \
    python3 \
    vala \
    && dnf clean all

ENV CCACHE_COMPILERCHECK=content
ENV CCACHE_MAXSIZE=2G
ENV CARGO_INCREMENTAL=0

WORKDIR /github/workspace
