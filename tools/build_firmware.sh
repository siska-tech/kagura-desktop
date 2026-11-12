#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Builds KAGURA MicroPython v1.26.0 firmware with the desktop: the SDK's board
# (KAGURA_PICO by default) and its modules, plus kagura_desktop
# (firmware/usermods.cmake) and the kdesk package (firmware/manifest.py).
# Needs the Arm GNU toolchain, the KAGURA SDK checkout (KAGURA_SDK_DIR, default
# ../kagura) and an initialised MicroPython tree (MPY_DIR, default the SDK's
# build/micropython-src; see the SDK's software/micropython/README.md). WSL/Linux:
#   bash tools/build_firmware.sh [BOARD] [BUILD_DIR_NAME]
# Prints the UF2 path; the SDK's tools/rp2040-firmware.py flashes it with checks.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
. "$ROOT/sdk/paths.sh"
BOARD="${1:-KAGURA_PICO}"
BUILD="${2:-build-$BOARD-desktop}"
export PATH="${ARM_GCC_BIN:-$HOME/opt/arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi/bin}:$PATH"
make -C "$MPY_DIR/ports/rp2" BOARD="$BOARD" BOARD_DIR="$SDK_BOARDS/$BOARD" \
    BUILD="$BUILD" USER_C_MODULES="$ROOT/firmware/usermods.cmake" FROZEN_MANIFEST="$ROOT/firmware/manifest.py" \
    -j"$(nproc)" >&2
arm-none-eabi-size "$MPY_DIR/ports/rp2/$BUILD/firmware.elf" >&2
echo "$MPY_DIR/ports/rp2/$BUILD/firmware.uf2"
