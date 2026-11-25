ARG FEDORA_VER=version

FROM fedora:${FEDORA_VER}

ENV TERM="xterm-256color" \
    CCACHE_COMPILERCHECK=content \
    CCACHE_MAXSIZE=2G \
    CARGO_INCREMENTAL=0

# Layer 1: DNF/rpmlint config & COPR repos (only re-runs if this layer changes or cache is busted)
RUN echo -e "color=always\nmax_parallel_downloads=10" >> /etc/dnf/dnf.conf && \
    mkdir -p /etc/xdg/rpmlint && \
    dnf copr enable -y infiniti151/flatpak-apps && \
    dnf copr enable -y infiniti151/rpmcrab && \
    cat > /etc/xdg/rpmlint/rpmcrab.toml <<'EOF'
Filters = [
"no-copyright-comment",
]
EOF

# Layer 2: Protected base dependencies (re-runs when protected deps change or Layer 1 changes, picking up updates)
RUN dnf install -y \
        ccache \
        dnf-plugins-core \
        desktop-rpm-macros \
        glibc-langpack-en \
        npm \
        rpm-build \
        rpmdevtools \
        rpmcrab \
        sccache && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*

# Layer 3: App-specific build dependencies (managed by scripts/update_dockerfile.py)
# --- APP_DEPS_START ---
RUN dnf install -y \
    # --- mousam dependencies --- \
    appstream \
    desktop-file-utils \
    forge-srpm-macros \
    gettext \
    glib2-devel \
    gtk-update-icon-cache \
    meson \
    ninja-build \
    python3-devel \
    python3-gobject \
    python3-requests \
    tzdata && \
    dnf clean all && \
    rm -rf /var/cache/dnf/*
# --- APP_DEPS_END ---

WORKDIR /github/workspace