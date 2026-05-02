ARG FEDORA_VER=version

FROM fedora:${FEDORA_VER}

RUN echo "max_parallel_downloads=10" >> /etc/dnf/dnf.conf

RUN dnf copr enable -y @vaniiiiii/extension-manager

RUN dnf install -y \
    # --- 1. Build Systems & Language Toolchains ---
    meson cmake gcc gcc-c++ sccache ccache upx clang lld \
    compiler-rt rust cargo cargo-rpm-macros blueprint-compiler \
    
    # --- 2. GNOME / Desktop Integration Tools ---
    desktop-file-utils gettext glib2-devel gtk-update-icon-cache \
    libappstream-glib gjs \
    
    # --- 3. System Libraries (Explicitly added from your Meson file) ---
    systemd-devel libinput-devel mesa-libgbm-devel libdrm-devel \
    libxkbcommon-devel libadwaita-devel libbacktrace-devel \
    json-glib-devel libsoup3-devel libxml2-devel \
    
    # --- Extras for CI/CD Utility ---
    dnf-plugins-core rpm-build rpmdevtools git-core nodejs \
    && dnf clean all

ENV CCACHE_DIR=/github/workspace/.ccache \
    SCCACHE_DIR=/github/workspace/.sccache \
    CARGO_HOME=/github/home/.cargo \
    CARGO_INCREMENTAL=0 \
    CCACHE_COMPILERCHECK=content

WORKDIR /github/workspace