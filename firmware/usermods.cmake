# SPDX-License-Identifier: Apache-2.0
# USER_C_MODULES for the rp2 port (tools/build_firmware.sh): kagura_desktop
# from this repository and kagura_audio from the KAGURA SDK, as the SDK's own
# boards add it. The SDK is $KAGURA_SDK_DIR, else a sibling checkout ../kagura.
include(${CMAKE_CURRENT_LIST_DIR}/../sdk/kagura_sdk.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/../binding/micropython.cmake)
include(${KAGURA_SDK_AUDIO_BINDING}/micropython.cmake)
