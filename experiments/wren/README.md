# Historical Wren research

Source: https://github.com/siska-tech/kagura/pulls (PRs 69–74).
Production uses the native desktop and MicroPython. This archive has no build
entry point and is not included by firmware, SDK APIs, or CI.

| PR | Original head | Evidence |
|---|---|---|
| 69 | d03912b4339495379302b286383eb40cf8a6d53e | experiments/wren-rp2040: MEMORY_ANALYSIS.md, results, rejected SRAM-only layouts |
| 70 | 1c089f2b5d22c4cded5a87f96c8ad74dd3a55914 | experiments/wren-desktop: HARDWARE.md, failed malloc-panic run, corrected run and restoration |
| 71 | 99c4250f124c0f3c86e5e8fb77554f015744e799 | experiments/native-text: portable UTF-8 engine, oracle, ROM/stack reports, font notice |
| 72 | e2ff7ead9144136e95096a92e0d024ee051b3f66 | experiments/wren-japanese-desktop: HARDWARE.md, failed capture and successful settled capture |
| 73 | 0214429bd0cde433fab111e7acb78bc1b3f22a3a | software/desktop: architecture, runtime-free validation and load equivalence |
| 74 | ed6e0b650ad69e08be99bd93805ccae8f99aa624 | software/desktop: source ownership and frozen regression comparisons |

Tested sources: #70 initial fdd45fbfc31453032d22930e3dcde2ea79c42a25,
corrected 0aa0974938a150d84bccf98dae7482977f17926c;
#72 25c7e9c03a5bfe6508dea91ee3faeebb0a57874d.
Native prerequisite #68: be344f5c742101f0cff170a29f63d09c0a17c441.

Only #70 and #72 contain physical Wren acceptance. The loaded FPGA bitstream
hash is unknown; the measured ABI was 0.6 and CAPS 0x5b. The original HDMI
classifier still reports 46 unexplained thin-red outline pixels despite exact
FPGA plane readback. Private flash backups are excluded. These results do not
qualify production firmware, long runs, or arbitrary application workloads.

Project code is Apache-2.0. Retain the Wren MIT license and upstream.sha256
under experiments/wren-rp2040, and preserve the independent Misaki notice
under experiments/native-text. The font is LicenseRef-Misaki.

## Historical dependencies

- Wren 99d2f0b8fc2686134b32b18166e037639f7e9f2c (meta/random disabled).
- Rejected Wren 0.4.0: 4a18fc489f9ea3d253b20dd40f4cdad0d6bb40eb.
- Pico SDK 2.2.0 a1438dff1d38bd9c65dbd693f0e5db4b9ae91779; TinyUSB 86ad6e56c1700e85f1c5678607a762cfe3aa2f47.
- Arm GNU 14.2.Rel1 (GCC 14.2.1 20241119), CMake 3.31.6.
- Recorded consolidation host: GCC 15.2.0-16ubuntu1, CMake 4.2.3, Python 3.14.4.
- qemu-arm 10.2.1 (1:10.2.1+ds-1ubuntu3.3).
- Offline packaging: picotool 2.2.0 a7eb3988f0645239185fadb4e25d8279478c2dbb.
- Historical Windows hardware programmer: picotool 2.3.1.
- Misaki asset SHA-256 cbfb1071801f7ed3b6637bb6763219e59d86c13bd149169bbbab5bca753d9238.

Exact Windows capture dependencies (FFmpeg, Python, NumPy/Pillow) and
programmer binary hash remain unverified. A Git bundle restores tracked files
and commit history; it does not supply external dependencies.

The source/evidence package includes ten selective, tracked snapshots with
original paths and Git tree manifests. See snapshots.json for file counts,
commit IDs and inner ZIP SHA-256 values. Verify the outer ZIP against the
published SHA256SUMS. Extract a selected snapshot into a disposable directory
and use its historical README and build tools. Acquire external dependencies at
the documented pins before running builds offline. Keep generated outputs in
the disposable copy. Git-dependent historical provenance scripts need the
original commit objects. Use the supplied tree manifests to verify snapshot
files without a Git bundle.

The snapshots cover the C GEM, Wren, native text and consolidation experiment
trees, historical Pico HAL, register header, font assets and license notices.
They exclude unrelated monorepo paths and private device backups. No history
bundle or physical rerun is required to use this archive.
