# The KAGURA SDK's layout

kagura-desktop uses the KAGURA SDK only through the files listed here. These four files are the only ones that know where things are inside the SDK checkout; when the SDK's layout changes (for example when it moves to its own repository), only they change.

| File | For |
|---|---|
| `paths.sh` | shell scripts (`tools/*.sh`), sourced after `ROOT` is set |
| `kagura_sdk.cmake` | CMake: the host build, `binding/micropython.cmake`, `firmware/usermods.cmake`, the experiments |
| `kagura_sdk.mk` | Make: the unix port's `binding/micropython.mk` and `usermods/` |
| `kagura_sdk.py` | Python tools (`tools/*.py`, the experiments' tools) |

The checkout is `KAGURA_SDK_DIR`, by default the sibling directory `../kagura-sdk`.

`kagura-sdk.ref` pins the SDK commit this repository is tested with: CI checks it out, and `tools/test.sh` says so when the local checkout is elsewhere. Move it forward in its own commit, after the desktop's tests pass against the new SDK commit.

| Name | Path in the SDK | What |
|---|---|---|
| `PYTHON` | `software/micropython` | the `kagura` package (MicroPython path) |
| `BOARDS` | `software/micropython/boards` | board directories (`KAGURA_PICO`, `KAGURA_PICO_W`) |
| `FONT` | `software/micropython/fonts/misaki8.kfnt` | the Misaki font, embedded unchanged |
| `AUDIO_BINDING` | `software/audio/binding` | the `kagura_audio` module (`micropython.cmake`, `micropython.mk`) |
| `SONGS` | `software/audio/songs` | `demo.ksn`/`.h` (the tracker test's fixture), `click.ksn` |
| `TOOLS` | `tools` | `build-micropython-unix.sh`, `rp2040-firmware.py`, `rp2040_sram_bench.py`, audio analysis tools |
| `PICO`, `INCLUDE` | `software/pico`, `software/include` | the C transport and headers (experiments only) |
| `MPY_DIR` (default) | `build/micropython-src` | the MicroPython v1.26.0 checkout, unless `MPY_DIR` is set |
