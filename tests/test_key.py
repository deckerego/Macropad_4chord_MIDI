from key import Key
import unittest

class TestChords(unittest.TestCase):

    def test_1st_degree(self):
        key = Key('C', 4)
        self.assertEqual(key.chord('I'), [60, 64, 67])

    def test_6th_degree(self):
        key = Key('C', 4)
        self.assertEqual(key.chord('vi'), [69, 72, 76])

class TestChord(unittest.TestCase):

    def test_chord_list(self):
        key = Key('C', 4)
        self.assertEqual(key.chords(['I', 'vi']), [[60, 64, 67], [69, 72, 76]])    

class TestName(unittest.TestCase):

    def test_c_four(self):
        name = Key.to_name(60)
        self.assertEqual(name, "C4")

    def test_f_sharp_two(self):
        name = Key.to_name(42)
        self.assertEqual(name, "F#2" )

class TestAdvance(unittest.TestCase):

    def test_next_note(self):
        start = Key('C', 4)
        next = start.advance(1)
        self.assertEqual(next.key, "C#")
        self.assertEqual(next.octave, 4)
        self.assertEqual(next.number, 61)

    def test_next_octave(self):
        start = Key('G#', 4)
        next = start.advance(1)
        self.assertEqual(next.key, "A")
        self.assertEqual(next.octave, 5)
        self.assertEqual(next.number, 69)

    def test_prev_note(self):
        start = Key('C', 4)
        next = start.advance(-1)
        self.assertEqual(next.key, "B")
        self.assertEqual(next.octave, 4)
        self.assertEqual(next.number, 59)

    def test_prev_octave(self):
        start = Key('A', 4)
        next = start.advance(-1)
        self.assertEqual(next.key, "G#")
        self.assertEqual(next.octave, 3)
        self.assertEqual(next.number, 56)

    def test_max(self):
        start = Key('D#', 8)
        next = start.advance(1)
        self.assertEqual(next.key, "D#")
        self.assertEqual(next.octave, 8)
        self.assertEqual(next.number, 111)

    def test_min(self):
        start = Key('C', -1)
        next = start.advance(-1)
        self.assertEqual(next.key, "C")
        self.assertEqual(next.octave, -1)
        self.assertEqual(next.number, 0)
