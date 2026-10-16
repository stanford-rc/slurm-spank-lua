#!/bin/bash

# Build against the installed SchedMD Slurm development package.
set -e

[[ $EUID -ne 0 ]] || { echo "Run this build as an unprivileged user"; exit 1; }

SRC_DIR="$(dirname "$(readlink -f "$0")")"
cd "$SRC_DIR"
dpkg-checkbuilddeps
SLURM_VER="$(dpkg-query -W -f='${Version}' slurm-smd-dev)"
SLURM_SERIES="$(echo "$SLURM_VER" | cut -d. -f1,2)"
DEB_VER="$(dpkg-parsechangelog -S Version)+slurm${SLURM_SERIES}"
OUT_DIR="$(readlink -m "${OUT_DIR:-$SRC_DIR/pkg}")/$DEB_VER"
[[ ! -e "$OUT_DIR" ]] || { echo "$OUT_DIR already exists"; exit 1; }

BUILD_DIR="$(mktemp -d /tmp/slurm-spank-lua.XXXXXX)"
echo ">>> Building $DEB_VER in $BUILD_DIR"
mkdir "$BUILD_DIR/source"
cp -a Makefile lua.c lib scripts spank-lua.8 LICENSE README.md debian \
    "$BUILD_DIR/source/"
cd "$BUILD_DIR/source"
dch --maintmaint --newversion "$DEB_VER" --distribution trixie \
    "Build against Slurm $SLURM_VER."
dpkg-buildpackage -us -uc -b > "$BUILD_DIR/build.log" 2>&1
mkdir -p "$OUT_DIR"
dcmd cp "$BUILD_DIR"/*.changes "$OUT_DIR/"
cp "$BUILD_DIR/build.log" "$OUT_DIR/"
rm -rf "$BUILD_DIR"
echo ">>> Packages: $OUT_DIR"
