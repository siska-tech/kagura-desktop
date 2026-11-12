# SPDX-License-Identifier: Apache-2.0
"""kdesk.desktop (the hardware session) against a recording tile plane.

The session reaches the KAGURA-9 only through the SDK's public
kagura.tileplane.TilePlane, whose register and VRAM layout the SDK tests
(software/micropython/tests/test_tileplane.py). Here a recording plane checks
what the session asks of it: a 40x25 grid with the desktop palette in the
chosen bank; open(), then the first frame, then show(); that the patterns it
sends always equal the desktop's TILE4 image, inside a held frame, with
ERROR_CODE checked when tiles were sent; that a failing device leaves the
console resumed; and close() hands the screen back to the console.

  MICROPYPATH=<sdk>/software/micropython:python micropython tests/test_session.py
"""
import sys

import kdesk.desktop as session
from kdesk.desktop import Desktop, PALETTE

failed = 0


class FakeDevice:
    abi, height = (0, 6), 240

    def _link(self):
        return None


class RecordingPlane:
    fail_after = None          # raise OSError on this many-th write

    def __init__(self, device, cols, rows, palette=0, colors=None):
        self.device, self.cols, self.rows, self.palette, self.colors = device, cols, rows, palette, colors
        self.image = bytearray(cols * rows * 32)
        self.log, self.depth, self.writes, self.checks = [], 0, 0, 0
        self.shown_image = None
        RecordingPlane.last = self

    def open(self):
        self.log.append('open')

    def show(self):
        self.log.append('show')
        self.shown_image = bytes(self.image)

    def write(self, first, data):
        assert self.depth > 0, 'write outside a held frame'
        assert 'open' in self.log, 'write before open'
        self.writes += 1
        if self.fail_after is not None and self.writes > self.fail_after:
            raise OSError(5)
        assert len(data) % 32 == 0 and first + len(data) // 32 <= self.cols * self.rows
        self.image[first * 32:first * 32 + len(data)] = data
        if self.log[-1] != 'write':
            self.log.append('write')

    def check(self):
        self.checks += 1

    def __enter__(self):
        self.depth += 1
        return self

    def __exit__(self, *exc):
        self.depth -= 1


class FailingPlane(RecordingPlane):
    fail_after = 0             # the first frame's first run fails


class FakeConsole:
    def __init__(self, device):
        self.screen = type('S', (), {'device': device})()
        self.paused = False
        self.resumed = 0

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        self.resumed += 1


def check(cond, what):
    global failed
    if not cond:
        failed += 1
        print('FAIL', what)


def test_setup_and_frames():
    session.TilePlane = RecordingPlane
    dev = FakeDevice()
    con = FakeConsole(dev)
    desk = Desktop(console=con, menus=(('ファイル', ('開く',)),), palette=2)
    plane = RecordingPlane.last
    check(con.paused, 'console paused while the desktop is open')
    check(plane.device is dev and desk.plane is plane, 'the console device, one plane')
    check((plane.cols, plane.rows, plane.palette, plane.colors) == (40, 25, 2, PALETTE),
          '40x25 grid, palette bank, desktop colours')
    check(plane.log == ['open', 'write', 'show'], 'open, first frame, then show: %r' % plane.log)
    image = bytearray(32000)
    desk.tile4(image)
    check(plane.shown_image == image, 'first frame: every pattern sent before show')
    check(plane.depth == 0, 'frame released')
    w = desk.create_window('神楽デスクトップ', 20, 30, 200, 100)
    w.text(8, 8, 'こんにちは', 1)
    checks = plane.checks
    tiles = desk.present()
    desk.tile4(image)
    check(tiles > 0 and plane.image == image, 'updates: changed patterns sent')
    check(plane.checks == checks + 1, 'ERROR_CODE checked once per frame with tiles')
    check(desk.present() == 0 and plane.checks == checks + 1, 'nothing to send or check when idle')
    desk.close()
    check(not con.paused and con.resumed == 1, 'console resumed on close')
    desk.close()
    check(con.resumed == 1, 'close twice is harmless')


def test_failure_releases():
    session.TilePlane = FailingPlane
    dev = FakeDevice()
    con = FakeConsole(dev)
    try:
        Desktop(console=con)
        check(False, 'a failing device raises')
    except OSError:
        pass
    check(not con.paused and con.resumed == 1, 'console resumed after a failed start')
    check('show' not in FailingPlane.last.log, 'nothing shown after a failed first frame')


def test_wrong_mode():
    session.TilePlane = TilePlane          # the SDK's: checks the mode, no I/O
    dev = FakeDevice()
    dev.height = 480
    con = FakeConsole(dev)
    try:
        Desktop(device=dev, console=con)
        check(False, 'wrong mode rejected')
    except ValueError:
        pass
    check(not con.paused and con.resumed == 0, 'console untouched by a rejected mode')


TilePlane = session.TilePlane
for name, fn in sorted((k, v) for k, v in globals().items() if k.startswith('test_')):
    before = failed
    fn()
    print('%-4s %s' % ('ok' if failed == before else 'FAIL', name[5:]))
session.TilePlane = TilePlane
print('session tests, %d failed' % failed)
sys.exit(1 if failed else 0)
