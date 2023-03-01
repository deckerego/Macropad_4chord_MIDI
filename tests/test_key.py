# Bootstrap the settings for the tests to run under
import settings
settings.key_configs['middle_octave'] = 3

from key import Key
import unittest

class TestDegrees(unittest.TestCase):
    heptatonic_major = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16]

    def test_1st_degree(self):
        key = Key('C', 3)
        self.assertEqual(key.chord('I', self.heptatonic_major), [60, 64, 67])

    def test_2st_degree(self):
        key = Key('C', 3)
        self.assertEqual(key.chord('ii', self.heptatonic_major), [62, 65, 69])

    def test_3rd_degree(self):
        key = Key('C', 3)
        self.assertEqual(key.chord('iii', self.heptatonic_major), [64, 67, 71])

    def test_4th_degree(self):
        key = Key('C', 3)
        self.assertEqual(key.chord('IV', self.heptatonic_major), [65, 69, 72])

    def test_5th_degree(self):
        key = Key('C', 3)
        self.assertEqual(key.chord('V', self.heptatonic_major), [67, 71, 74])

    def test_6th_degree(self):
        key = Key('C', 3)
        self.assertEqual(key.chord('vi', self.heptatonic_major), [69, 72, 76])

class TestChords(unittest.TestCase):
    heptatonic_major = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16]

    def test_chord_list(self):
        key = Key('C', 3)
        self.assertEqual(key.chords(['I', 'vi'], self.heptatonic_major), [[60, 64, 67], [69, 72, 76]])    

class TestName(unittest.TestCase):

    def test_c_three(self):
        name = Key.to_name(60)
        self.assertEqual(name, "C3")

    def test_f_sharp_one(self):
        name = Key.to_name(42)
        self.assertEqual(name, "F#1" )

    def test_f_sharp(self):
        name = Key.to_note(42)
        self.assertEqual(name, "F#" )

class TestAdvanceMajor(unittest.TestCase):
    heptatonic_major = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16]

    def test_next_note(self):
        start = Key('C', 3)
        next = start.advance(1)
        self.assertEqual(next.key, "C#")
        self.assertEqual(next.octave, 3)
        self.assertEqual(next.number, 61)

    def test_next_octave(self):
        start = Key('B', 3)
        next = start.advance(1)
        self.assertEqual(next.key, "C")
        self.assertEqual(next.octave, 4)
        self.assertEqual(next.number, 72)

    def test_prev_note(self):
        start = Key('F', 3)
        next = start.advance(-1)
        self.assertEqual(next.key, "E")
        self.assertEqual(next.octave, 3)
        self.assertEqual(next.number, 64)

    def test_prev_octave(self):
        start = Key('C', 3)
        next = start.advance(-1)
        self.assertEqual(next.key, "B")
        self.assertEqual(next.octave, 2)
        self.assertEqual(next.number, 59)

    def test_max(self):
        start = Key('G#', 7)
        next = start.advance(1)
        self.assertEqual(next.key, "G#")
        self.assertEqual(next.octave, 7)
        self.assertEqual(next.number, 116)

    def test_min(self):
        start = Key('C', -2)
        next = start.advance(-1)
        self.assertEqual(next.key, "C")
        self.assertEqual(next.octave, -2)
        self.assertEqual(next.number, 0)

class TestAdvancePentatonic(unittest.TestCase):
    heptatonic_major = [0, 1, 2, 4, 5, 9, 11, 12, 14, 16]

    def test_next_note(self):
        start = Key('C', 3)
        next = start.advance(1)
        self.assertEqual(next.key, "C#")
        self.assertEqual(next.octave, 3)
        self.assertEqual(next.number, 61)

    def test_next_octave(self):
        start = Key('B', 3)
        next = start.advance(1)
        self.assertEqual(next.key, "C")
        self.assertEqual(next.octave, 4)
        self.assertEqual(next.number, 72)

    def test_prev_note(self):
        start = Key('F', 3)
        next = start.advance(-1)
        self.assertEqual(next.key, "E")
        self.assertEqual(next.octave, 3)
        self.assertEqual(next.number, 64)

    def test_prev_octave(self):
        start = Key('C', 3)
        next = start.advance(-1)
        self.assertEqual(next.key, "B")
        self.assertEqual(next.octave, 2)
        self.assertEqual(next.number, 59)

    def test_max(self):
        start = Key('G#', 7)
        next = start.advance(1)
        self.assertEqual(next.key, "G#")
        self.assertEqual(next.octave, 7)
        self.assertEqual(next.number, 116)

    def test_min(self):
        start = Key('C', -2)
        next = start.advance(-1)
        self.assertEqual(next.key, "C")
        self.assertEqual(next.octave, -2)
        self.assertEqual(next.number, 0)