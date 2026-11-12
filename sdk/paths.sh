# SPDX-License-Identifier: Apache-2.0
# The KAGURA SDK's layout for shell scripts (sdk/README.md). Source it after
# setting ROOT to this repository's root. Exports KAGURA_SDK_DIR (absolute).
export KAGURA_SDK_DIR="$(cd "${KAGURA_SDK_DIR:-$ROOT/../kagura-sdk}" && pwd)"
SDK="$KAGURA_SDK_DIR"
SDK_PYTHON="$SDK/software/micropython"
SDK_BOARDS="$SDK_PYTHON/boards"
SDK_FONT="$SDK_PYTHON/fonts/misaki8.kfnt"
SDK_AUDIO_BINDING="$SDK/software/audio/binding"
SDK_SONGS="$SDK/software/audio/songs"
SDK_TOOLS="$SDK/tools"
export MPY_DIR="${MPY_DIR:-$SDK/build/micropython-src}"
