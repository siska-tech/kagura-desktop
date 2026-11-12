# SPDX-License-Identifier: Apache-2.0
# The KAGURA SDK's kagura_audio (the tracker and kdesk sessions use it):
# KAGURA_SDK_DIR, else a sibling checkout ../kagura.
include $(USERMOD_DIR)/../../sdk/kagura_sdk.mk
USERMOD_DIR := $(KAGURA_SDK_AUDIO_BINDING)
include $(USERMOD_DIR)/micropython.mk
