# SPDX-License-Identifier: Apache-2.0
# The KAGURA SDK's layout for CMake (sdk/README.md): KAGURA_SDK_DIR, else
# $KAGURA_SDK_DIR, else the sibling directory ../kagura.
if(NOT KAGURA_SDK_DIR)
    if(DEFINED ENV{KAGURA_SDK_DIR})
        set(KAGURA_SDK_DIR $ENV{KAGURA_SDK_DIR})
    else()
        get_filename_component(KAGURA_SDK_DIR ${CMAKE_CURRENT_LIST_DIR}/../../kagura ABSOLUTE)
    endif()
endif()
set(KAGURA_SDK_FONT ${KAGURA_SDK_DIR}/software/micropython/fonts/misaki8.kfnt)
set(KAGURA_SDK_AUDIO_BINDING ${KAGURA_SDK_DIR}/software/audio/binding)
set(KAGURA_SDK_PICO ${KAGURA_SDK_DIR}/software/pico)
set(KAGURA_SDK_INCLUDE ${KAGURA_SDK_DIR}/software/include)
if(NOT EXISTS ${KAGURA_SDK_FONT})
    message(FATAL_ERROR "KAGURA SDK not found at ${KAGURA_SDK_DIR} (set KAGURA_SDK_DIR)")
endif()
