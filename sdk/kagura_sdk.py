# SPDX-License-Identifier: Apache-2.0
"""The KAGURA SDK's layout for Python tools (sdk/README.md).

    sys.path.insert(0, str(ROOT / 'sdk')); import kagura_sdk
"""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DIR = Path(os.environ.get('KAGURA_SDK_DIR') or REPO.parent / 'kagura-sdk').resolve()
PYTHON = DIR / 'software/micropython'
BOARDS = PYTHON / 'boards'
FONT = PYTHON / 'fonts/misaki8.kfnt'
SONGS = DIR / 'software/audio/songs'
TOOLS = DIR / 'tools'
