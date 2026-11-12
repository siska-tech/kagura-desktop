#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Tests of kagura-desktop, from anywhere (WSL/Linux). Needs the KAGURA SDK
# checkout (KAGURA_SDK_DIR, default ../kagura) and MicroPython v1.26.0 with
# mpy-cross (MPY_DIR, default the SDK's build/micropython-src); sdk/paths.sh:
#   1. host build: text engine (UTF-8, all Misaki glyphs), editing core and
#      4 mutants, kdm (with fields, the editor and keyboard focus) and 10 mutants;
#   2. the unix MicroPython port with kagura_desktop and the SDK's kagura_audio;
#   3. tests/test_binding.py on it (API, lifetimes, GC, errors, Japanese),
#      tests/test_session.py (kdesk.desktop against a recording tile plane),
#      tests/test_keyinput.py (terminal keyboard decoding, end to end),
#      tests/test_editor.py (the text editor: files, dialogs, sessions, SKK),
#      tests/test_skk.py (the SKK input method),
#      tests/test_tracker.py (神楽トラッカー; its scripted session must compose
#      the SDK's software/audio/songs/demo.ksn and demo.h byte for byte), and
#      the Japanese desktop demo (apps/desktop_ja.py), the keyboard demo
#      (apps/desktop_keys.py), the SKK demo and the video showcase
#      (apps/desktop_showcase.py) without hardware.
#   bash tools/test.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
. "$ROOT/sdk/paths.sh"
PIN="$(cat "$ROOT/sdk/kagura.ref")"
HEAD="$(git -C "$SDK" rev-parse HEAD 2>/dev/null || echo unknown)"
[ "$HEAD" = "$PIN" ] || echo "note: the SDK is at $HEAD; CI tests sdk/kagura.ref $PIN" >&2
OUT="${OUT:-$ROOT/build/desktop}"
cmake -S "$ROOT" -B "$OUT" -DCMAKE_BUILD_TYPE=Release -DKAGURA_SDK_DIR="$KAGURA_SDK_DIR" >/dev/null
cmake --build "$OUT" -j"$(nproc)" >/dev/null
ctest --test-dir "$OUT" --output-on-failure
MP="$(bash "$ROOT/tools/build_unix.sh")"
PY="$SDK_PYTHON:$ROOT/python"
APPS="$PY:$ROOT/apps"
"$MP" "$ROOT/tests/test_binding.py" "$SDK_FONT"
MICROPYPATH="$PY" "$MP" "$ROOT/tests/test_session.py"
MICROPYPATH="$APPS" "$MP" "$ROOT/tests/test_keyinput.py"
MICROPYPATH="$APPS" "$MP" "$ROOT/tests/test_editor.py"
MICROPYPATH="$PY" "$MP" "$ROOT/tests/test_skk.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
MICROPYPATH="$APPS" "$MP" "$ROOT/tests/test_tracker.py" "$TMP"
cmp "$TMP/demo/DEMO.KSN" "$SDK_SONGS/demo.ksn"
cmp "$TMP/demo/DEMO.H" "$SDK_SONGS/demo.h"
"$MP" "$ROOT/apps/desktop_ja.py" --host
MICROPYPATH="$APPS" "$MP" "$ROOT/apps/desktop_keys.py" --host
MICROPYPATH="$APPS" "$MP" "$ROOT/apps/desktop_skk.py" --host
mkdir "$TMP/show"
MICROPYPATH="$APPS" "$MP" "$ROOT/apps/desktop_showcase.py" --host "$TMP/show"
echo "kagura-desktop: all tests passed"
