#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Builds the MicroPython v1.26.0 unix port with kagura_desktop and the SDK's
# kagura_audio (usermods/), through the SDK's tools/build-micropython-unix.sh,
# and prints the binary's path. From anywhere (WSL/Linux):
#   bash tools/build_unix.sh
# KAGURA_SDK_DIR defaults to ../kagura; MPY_DIR to the SDK's build/micropython-src.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
. "$ROOT/sdk/paths.sh"
export BUILD="${BUILD:-build-kagura-desktop}"
USER_C_MODULES="$ROOT/usermods" bash "$SDK_TOOLS/build-micropython-unix.sh" "$@"
