# Reproduction results

Environment: Windows NT 10.0.26200.0, PowerShell 7.6.9, Git for Windows
2.55.0.windows.5, current workspace sandbox, offline. No historical WSL
environment was used. Results below describe this preparation run.

| Check | Result | Evidence or reason |
|---|---|---|
| Snapshot provenance | PASS | All ten pinned commits resolved locally. Every ZIP file entry matched the original Git blob SHA-1 and every expected path was present. |
| License and font provenance | PASS | Apache-2.0 LICENSE, Wren MIT and upstream manifest, native-text Misaki notice and original font README present. Font SHA-256 verified. |
| Device backup exclusion | PASS | Tracked path allowlist only. ZIP entry checks rejected backup names and raw image/binary extensions. Historical public logs and screenshots retained. |
| Archive isolation | PASS | Commit contains only documentation and metadata under experiments/wren. Source package is separate from the desktop build tree. The audited desktop CMake, firmware module lists and CI use explicit source paths. |
| Host Release suites | BLOCKED | CMake, CTest and GCC/Clang unavailable on PATH. Python resolves to a WindowsApps alias, with the historical Python environment unavailable. |
| Host ASan/UBSan and runtime-free suites | BLOCKED | Same host toolchain gap. |
| ARM allocator, stack and lifecycle tests | BLOCKED | Arm GNU 14.2.Rel1 and qemu-arm unavailable on PATH. |
| Pico SRAM offline build and ELF/UF2 layout checks | BLOCKED | Pinned ARM/Pico SDK/CMake and picotool packaging environment unavailable in this run. |
| Flash-resident offline builds and load-segment comparisons | BLOCKED | Same ARM/Pico toolchain gap. |
| Fresh CRC and image golden comparisons | BLOCKED | No freshly built host or ARM binaries. |
| HDMI capture reanalysis | BLOCKED | Historical Windows Python, Pillow, NumPy and FFmpeg versions remain unverified. |
| Complete ELF byte identity | BLOCKED | No independent rebuild. |
| Physical reproduction | BLOCKED | Deferred milestone. Historical runs and failures are preserved. |

For reruns, use each snapshot's README. For #74 start with
software/desktop/tools/validate.sh for the retained host suites and native-only
build, then follow the ARM and Pico instructions in that snapshot's docs.
For #69 use experiments/wren-rp2040/pico/ACCEPTANCE.md for the offline
image and layout checks. Hardware commands are outside the offline procedure.
