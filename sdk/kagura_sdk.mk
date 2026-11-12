# SPDX-License-Identifier: Apache-2.0
# The KAGURA SDK's layout for Make (sdk/README.md): KAGURA_SDK_DIR, else the
# sibling directory ../kagura.
KAGURA_SDK_MK_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
KAGURA_SDK_DIR ?= $(abspath $(KAGURA_SDK_MK_DIR)../../kagura)
KAGURA_SDK_FONT := $(abspath $(KAGURA_SDK_DIR)/software/micropython/fonts/misaki8.kfnt)
KAGURA_SDK_AUDIO_BINDING := $(abspath $(KAGURA_SDK_DIR)/software/audio/binding)
