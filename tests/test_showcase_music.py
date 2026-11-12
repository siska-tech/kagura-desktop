# SPDX-License-Identifier: Apache-2.0
"""The showcase's background music (apps/desktop_showcase.interlude) plays
the notes and timing of the raw-register interlude it replaced: every 125 ms
the arpeggio voice 0 plays chord[n % 3] + 12 and voice 2 holds chord[0] - 12
(MIDI numbers), chord = CHORDS[n // 16 & 3], with a loop of 192 steps.

    micropython tests/test_showcase_music.py      (MICROPYPATH with the SDK and apps)
"""
from kagura.music import Song, NONE
import desktop_showcase

CHORDS = ((57, 60, 64), (57, 60, 65), (55, 60, 64), (55, 59, 62))

song = Song.from_bytes(desktop_showcase.interlude())
assert list(song.voices) == [0, 2], song.voices
assert song.loop and song.loop_order == 0
# One row = speed ticks of 2500000 / tempo us (software/audio/seq/ks_player.h).
assert song.speed * 2500000 // song.tempo == 125000, (song.tempo, song.speed)
assert [bytes(i)[:3] for i in song.instruments] == [bytes((0, 64, 1)), bytes((0, 128, 1))]

held = [None, None]
n = 0
for order in song.orders:
    pat = song.patterns[order]
    for row in range(pat.rows):
        for track in (0, 1):
            o = pat.offset(row, track)
            note = pat.cells[o]
            if note:
                assert pat.cells[o + 1] == track, (n, track)   # instrument per track
                assert pat.cells[o + 2] == NONE and pat.cells[o + 3] == 0, (n, track)
                held[track] = note + 11                         # back to MIDI
        chord = CHORDS[n // 16 & 3]
        assert held == [chord[n % 3] + 12, chord[0] - 12], (n, held)
        n += 1
assert n == 192, n
print('showcase music: 192 steps match the original interlude')
