# 神楽トラッカー

`apps/desktop_tracker.py`, a music tracker in the native desktop's visual language. One window holds:

- **The pattern grid** (4×8 font): 16 rows and 4 of the 6 tracks at a time. The view pages to follow the cursor, and the playing row during playback.
- **The order list and the instruments** (8×8 font).
- **A status line**: state, BPM, speed, octave, instrument.

The cursor, its field and the playback row are movable fills under transparent text, so moving the cursor redraws a few tiles.

- **Keys** (FastTracker II layout): `z s x … /` and `q 2 w … p` are notes, `1` is note off, and hex digits fill the instrument, volume and effect fields. Delete clears a field; Insert and Backspace insert and delete rows.
  - `[ ]` change the octave and `- =` the instrument; Space plays the song and Enter the pattern, Esc stops.
  - Ctrl+Left/Right move through the order list, Ctrl+Up/Down change its pattern.
  - Ctrl+S, Ctrl+O and Ctrl+N save, open and start anew; F10 opens the menus.
- **Editing while playing** reloads the song at once, keeping the position.
- **Dialogs**: an instrument editor (kind, duty or wave, volume, pan, ADSR) and song settings (tempo, speed, loop, loop order, pattern length).
- **The wave editor** (instrument editor > 波形を編集…) draws a wave instrument's table: signed 8-bit samples, 32 to 256 of them (the FPGA's format), as bars on a 256×128 grid.
  - **Keys:** Left/Right choose a sample and Up/Down change it (Shift: ×16; PgUp/PgDn ±32; Home/End the extremes; Delete 0). Shift+Left/Right carry the value along, which draws with the keyboard.
  - **Presets:** 1 sine, 2 triangle, 3 sawtooth, 4 square, 0 flat. L changes the length (resampled); N copies the wave as a new one for the instrument.
  - **Sound:** Space plays a note with it. Every change goes to the HAL at once, so the note sounding plays the new wave from the next frame.
  - **Pointer:** pressing and dragging in the canvas draws, with interpolated lines. It is wired to POINTER_DOWN/MOVE/UP and tested by injecting them, so it works when a pointer is connected.
  - **Drawing cost:** one fill record per sample, so an edit redraws that column only (a few tiles). A 256-sample wave uses 256 of the desktop's 320 records. No framebuffer is allocated.
  - **Saving:** waves are saved in the song (KSNG wave records) and reload byte for byte.
- **The scope** (lower right) shows a synthesized waveform: the mix, one track, or off (再生 > スコープ cycles).
  - `kagura_audio.render()` computes what the HAL has set the voices to play, each from phase 0. It is **not** captured audio: the hardware has no read-back path without RTL changes, and the label says SYNTH.
  - `Desktop.trace()` draws it in C into 8 sprites (64×32 px) on the tile grid, redrawing only changed pixels.
  - It updates at up to 10 Hz. The rate halves when the running average of its cost exceeds 6 ms, or the music's average lateness exceeds 3 ms, down to OFF(auto); it recovers below half and two thirds of those.
  - It is hidden while a dialog is open.
- **Redrawing during playback**: the grid's text is rebuilt only when what it shows changes. While music plays, a page turn is drawn 4 rows per loop.
- **Files**: `NAME.KSN` in one folder with write-then-rename. 書き出し also writes `NAME.H`. `ram_songs()` keeps them in RAM.
  - File I/O goes in 512-byte pieces with the audio pumped between them, so a save while the music plays is mostly in time; single littlefs operations can still take tens of ms.
- **A scripted session** (`main(script=True)`, `--host` on a PC) composes the demo song with the tracker's own keys. It plays two loops, saves, reopens and exports, printing a CRC per scene.

## Tests and acceptance

- `tests/test_tracker.py` (run by `tools/test.sh`): editing keys, the composed demo song, files, guards and playback on the unix port. The scripted session must compose the SDK's `software/audio/songs/demo.ksn` and `demo.h` byte for byte.
- `tools/kagura-audio-board.py` runs the board measurements (bench, tracker, wave, scope). Their logs are kept with the audio module in the SDK: `software/audio/docs/hardware.md`.
