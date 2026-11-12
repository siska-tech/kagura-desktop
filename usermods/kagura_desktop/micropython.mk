# SPDX-License-Identifier: Apache-2.0
# Make ports (unix) take one USER_C_MODULES directory: each subdirectory names
# one module and includes the module's own file (binding/ here; kagura_audio
# from the KAGURA SDK).
USERMOD_DIR := $(USERMOD_DIR)/../../binding
include $(USERMOD_DIR)/micropython.mk
