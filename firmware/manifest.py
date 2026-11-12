# SPDX-License-Identifier: Apache-2.0
# FROZEN_MANIFEST for tools/build_firmware.sh: the SDK board's manifest (its
# BOARD_DIR: the kagura package, frozen as the SDK builds it), then kdesk.
# Relative paths are relative to this file.
include("$(BOARD_DIR)/manifest.py")
freeze("../python", (
    "kdesk/__init__.py",
    "kdesk/desktop.py",
    "kdesk/keyinput.py",
    "kdesk/skk.py",
))
