# SPDX-License-Identifier: Apache-2.0
"""Native GEM-style desktop on KAGURA-9 (C module kagura_desktop).

The desktop's 320x200 4bpp plane, windows, menus, compositor and Japanese
text live in C (core/, retained/, text/); this module puts it on the display
through the KAGURA SDK's public tile plane (kagura.tileplane.TilePlane), on
the same device the HDMI console uses, so there is one hardware owner and one
transport:

    from kdesk.desktop import Desktop
    desk = Desktop(menus=(('ファイル', ('開く', '-', '終了')),))
    win = desk.create_window('神楽デスクトップ', 20, 30, 200, 100)
    win.text(8, 8, 'こんにちは', 1)
    desk.present()        # composes the damage, sends only changed tiles
    ...
    desk.close()          # the console takes the screen back

Ownership: while open, the desktop owns the tile plane (TilePlane: patterns,
BG map, scroll, raster scroll, BACKDROP and the 16 colours of its palette
bank), like KAGURA-UI's App(exclusive=True). The console is paused and
resumed on close(), which reclaims its tiles, map and palette. Sprites stay
disabled.

Placement: the 1,000 tiles (40x25) are patterns 0..999 of a 40x25 TilePlane,
centred in the 320x240 output on lines 20..219. Everything else shows the
plane's blank pattern, colour 0: BACKDROP, the desk colour.

Music: set desk.audio to a kagura.music.AudioSession and present() pumps it
at its start and after every run of tiles. (Splitting long runs further was
measured and did not help: a window move's time is in the compositor, before
the first run.) The session must use the same device.

Everything else (create_window, sprite, pointer, key, poll, ...) is the
kagura_desktop.Desktop API, see README.md.
"""
import kagura_desktop as _kd

from kagura import console as _console
from kagura.tileplane import TilePlane

# core/kd_gfx.c kd_palette_rgb444
PALETTE = (0x0A5, 0x000, 0xFFF, 0xBBB, 0x666, 0x23C, 0xD22, 0xEC2,
           0x063, 0x2BC, 0xC4C, 0x842, 0x8AF, 0x8E8, 0xF82, 0xFFC)
COLUMNS, ROWS = 40, 25
# Runs separated by at most this many clean tiles are sent as one: on the
# accelerated link a run costs about 1.1 ms and an extra tile about 24 us.
MAX_GAP = 32


class Desktop:
    def __init__(self, device=None, console=None, menus=None, cursor=True, palette=0, outline_drag=False):
        if console is None:
            console = _console.active()
        if device is None:
            screen = getattr(console, 'screen', None)
            if screen is None:
                raise RuntimeError('no KAGURA device (pass device=, or start the console)')
            device = screen.device
        # Checks the mode and the palette bank; touches no hardware.
        plane = TilePlane(device, COLUMNS, ROWS, palette=palette, colors=PALETTE)
        # Native state next: a failure here touches no hardware either.
        self._kd = _kd.Desktop(COLUMNS * 8, ROWS * 8, menus=menus, cursor=cursor, outline_drag=outline_drag)
        self.device, self.plane, self.console, self.palette = device, plane, console, palette
        self._open = False
        self.audio = None              # kagura.music.AudioSession, pumped by present()
        self._sink = self._write_run   # one bound method, not one per present()
        self._write = plane.write
        if console is not None:
            console.pause()
        try:
            plane.open()
            with plane:
                self._kd.present(self._sink, MAX_GAP)   # every tile: the first frame
            plane.show()
        except BaseException:
            self._release()
            raise
        self._open = True

    def _write_run(self, first, data):
        # One run of consecutive patterns (0..999), valid during the call, fenced
        # by the plane; ERROR_CODE is checked once per present().
        self._write(first, data)
        if self.audio is not None:
            self.audio.pump()          # the queue is empty after the FENCE

    def present(self):
        """Compose all damage and send the changed patterns. Returns the tile count."""
        plane = self.plane
        with plane:
            if self.audio is not None:
                self.audio.pump()
            tiles = self._kd.present(self._sink, MAX_GAP)
            if tiles:
                plane.check()
            return tiles

    def _release(self):
        try:
            self._kd.close()
        finally:
            if self.console is not None:
                self.console.resume()

    def close(self):
        """Ends the desktop; the console (if any) reclaims the screen."""
        if self._open:
            self._open = False
            self._release()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def __getattr__(self, name):
        return getattr(self._kd, name)
