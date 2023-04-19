# Bootstrap the settings for the tests to run under
import settings
settings.key_configs['middle_octave'] = 3

from key import Key
import unittest

class TestDefaults(unittest.TestCase):
    def test_default_constructor(self):
        key = Key()
        self.assertEqual(key.key, "C")

    def test_no_scale(self):
        key = Key()
        self.assertEqual(key.chord('I'), [60, 60, 60])

class TestDegrees(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_1st_degree(self):
        key = Key('C', self.major, 3)
        self.assertEqual(key.chord('I'), [60, 64, 67])

    def test_2nd_degree(self):
        key = Key('C', self.major, 3)
        self.assertEqual(key.chord('ii'), [62, 65, 69])

    def test_3rd_degree(self):
        key = Key('C', self.major, 3)
        self.assertEqual(key.chord('iii'), [64, 67, 71])

    def test_4th_degree(self):
        key = Key('C', self.major, 3)
        self.assertEqual(key.chord('IV'), [65, 69, 72])

    def test_5th_degree(self):
        key = Key('C', self.major, 3)
        self.assertEqual(key.chord('V'), [67, 71, 74])

    def test_6th_degree(self):
        key = Key('C', self.major, 3)
        self.assertEqual(key.chord('vi'), [69, 72, 76])

class TestChords(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_chord_list(self):
        key = Key('C', self.major, 3)
        self.assertEqual(key.chords(['I', 'vi']), [[60, 64, 67], [69, 72, 76]])    

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

    def test_lowest(self):
        name = Key.to_name(0)
        self.assertEqual(name, "C-2")

    def test_highest(self):
        name = Key.to_name(116)
        self.assertEqual(name, "G#7")

class TestDegreeNumber(unittest.TestCase):

    def test_second_major(self):
        degree = Key.to_degree('II')
        self.assertEqual(degree, 1)

    def test_second_minor(self):
        degree = Key.to_degree('ii')
        self.assertEqual(degree, 1)

    def test_seventh_diminished(self):
        degree = Key.to_degree('vii˚')
        self.assertEqual(degree, 6)
    
    def test_sixth_augmented_diminished(self):
        degree = Key.to_degree('vi7˚')
        self.assertEqual(degree, 5)

class TestAdvanceMajor(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_next_note(self):
        key = Key('C', self.major, 3)
        key.advance(1)
        self.assertEqual(key.key, "C#")
        self.assertEqual(key.octave, 3)
        self.assertEqual(key.number, 61)

    def test_next_octave(self):
        key = Key('B', self.major, 3)
        key.advance(1)
        self.assertEqual(key.key, "C")
        self.assertEqual(key.octave, 4)
        self.assertEqual(key.number, 72)

    def test_prev_note(self):
        key = Key('F', self.major, 3)
        key.advance(-1)
        self.assertEqual(key.key, "E")
        self.assertEqual(key.octave, 3)
        self.assertEqual(key.number, 64)

    def test_prev_octave(self):
        key = Key('C', self.major, 3)
        key.advance(-1)
        self.assertEqual(key.key, "B")
        self.assertEqual(key.octave, 2)
        self.assertEqual(key.number, 59)

    def test_max(self):
        key = Key('G#', self.major, 7)
        key.advance(1)
        self.assertEqual(key.key, "G#")
        self.assertEqual(key.octave, 7)
        self.assertEqual(key.number, 116)

    def test_min(self):
        key = Key('C', self.major, -2)
        key.advance(-1)
        self.assertEqual(key.key, "C")
        self.assertEqual(key.octave, -2)
        self.assertEqual(key.number, 0)

class TestAdvancePentatonic(unittest.TestCase):
    pentatonic = [ 2, 2, 3, 2, 3 ]

    def test_next_note(self):
        key = Key('C', self.pentatonic, 3)
        key.advance(1)
        self.assertEqual(key.key, "C#")
        self.assertEqual(key.octave, 3)
        self.assertEqual(key.number, 61)

    def test_next_octave(self):
        key = Key('B', self.pentatonic, 3)
        key.advance(1)
        self.assertEqual(key.key, "C")
        self.assertEqual(key.octave, 4)
        self.assertEqual(key.number, 72)

    def test_prev_note(self):
        key = Key('F', self.pentatonic, 3)
        key.advance(-1)
        self.assertEqual(key.key, "E")
        self.assertEqual(key.octave, 3)
        self.assertEqual(key.number, 64)

    def test_prev_octave(self):
        key = Key('C', self.pentatonic, 3)
        key.advance(-1)
        self.assertEqual(key.key, "B")
        self.assertEqual(key.octave, 2)
        self.assertEqual(key.number, 59)

    def test_max(self):
        key = Key('G#', self.pentatonic, 7)
        key.advance(1)
        self.assertEqual(key.key, "G#")
        self.assertEqual(key.octave, 7)
        self.assertEqual(key.number, 116)

    def test_min(self):
        key = Key('C', self.pentatonic, -2)
        key.advance(-1)
        self.assertEqual(key.key, "C")
        self.assertEqual(key.octave, -2)
        self.assertEqual(key.number, 0)

class TestDorian(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_1st_degree(self):
        key = Key('C', self.major, 3, 1)
        self.assertEqual(key.chord('i'), [60, 63, 67])

    def test_2nd_degree(self):
        key = Key('C', self.major, 3, 1)
        self.assertEqual(key.chord('ii'), [62, 65, 69])

    def test_3rd_degree(self):
        key = Key('C', self.major, 3, 1)
        self.assertEqual(key.chord('III'), [63, 67, 70])

    def test_4th_degree(self):
        key = Key('C', self.major, 3, 1)
        self.assertEqual(key.chord('IV'), [65, 69, 72])

    def test_5th_degree(self):
        key = Key('C', self.major, 3, 1)
        self.assertEqual(key.chord('v'), [67, 70, 74])

    def test_6th_degree(self):
        key = Key('C', self.major, 3, 1)
        self.assertEqual(key.chord('vi'), [69, 72, 75])

class TestSwitchScale(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_scale_from_default(self):
        key = Key()
        self.assertEqual(key.chord('I'), [60, 60, 60])

        key.set_scale(self.major)
        self.assertEqual(key.chord('I'), [60, 64, 67])

    def test_scale_from_constructor(self):
        key = Key('C', [ 3, 2, 1, 1, 3, 2 ], 3, 0)
        self.assertEqual(key.chord('I'), [60, 65, 67])

        key.set_scale(self.major)
        self.assertEqual(key.chord('I'), [60, 64, 67])

    def test_mode_from_constructor(self):
        key = Key('C', [ 3, 2, 1, 1, 3, 2 ], 3, 0)
        self.assertEqual(key.chord('I'), [60, 65, 67])

        key.set_scale(self.major, 1)
        self.assertEqual(key.chord('I'), [60, 63, 67])

class TestMajorChord(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_major_c(self):
        key = Key('C', self.major)
        self.assertEqual(key.chord_major(), [60, 64, 67])

    def test_major_a(self):
        key = Key('A', self.major)
        self.assertEqual(key.chord_major(), [69, 73, 76])

class TestMinorChord(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_minor_c(self):
        key = Key('C', self.major)
        self.assertEqual(key.chord_minor(), [60, 63, 67])

    def test_minor_a(self):
        key = Key('A', self.major)
        self.assertEqual(key.chord_minor(), [69, 72, 76])

class TestAugmentedChord(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_minor_c(self):
        key = Key('C', self.major)
        self.assertEqual(key.chord_augmented(), [60, 64, 68])

    def test_minor_a(self):
        key = Key('A', self.major)
        self.assertEqual(key.chord_augmented(), [69, 73, 77])

class TestDiminishedChord(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_minor_c(self):
        key = Key('C', self.major)
        self.assertEqual(key.chord_diminished(), [60, 63, 66])

    def test_minor_a(self):
        key = Key('A', self.major)
        self.assertEqual(key.chord_diminished(), [69, 72, 75])

class TestSeventhChords(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_dom_seventh_c(self):
        key = Key('C', self.major)
        self.assertEqual(key.chord_seventh(), [60, 64, 67, 70])

    def test_dom_seventh_a(self):
        key = Key('A', self.major)
        self.assertEqual(key.chord_seventh(), [69, 73, 76, 79])

    def test_maj_seventh_c(self):
        key = Key('C', self.major)
        self.assertEqual(key.chord_seventh_maj(), [60, 64, 67, 71])

    def test_maj_seventh_a(self):
        key = Key('A', self.major)
        self.assertEqual(key.chord_seventh_maj(), [69, 73, 76, 80])

    def test_min_seventh_c(self):
        key = Key('C', self.major)
        self.assertEqual(key.chord_seventh_min(), [60, 63, 67, 70])

    def test_min_seventh_a(self):
        key = Key('A', self.major)
        self.assertEqual(key.chord_seventh_min(), [69, 72, 76, 79])

class TestNumberConstructor(unittest.TestCase):
    major = [ 2, 2, 1, 2, 2, 2, 1 ]

    def test_middle_c(self):
        key = Key(number=60)
        self.assertEqual(key.key, "C")
        self.assertEqual(key.octave, 3)
        self.assertEqual(key.number, 60)

    def test_octave_c(self):
        key = Key(number=72)
        self.assertEqual(key.key, "C")
        self.assertEqual(key.octave, 4)
        self.assertEqual(key.number, 72)

    def test_a(self):
        key = Key(number=57)
        self.assertEqual(key.key, "A")
        self.assertEqual(key.octave, 2)
        self.assertEqual(key.number, 57)

    def test_scale(self):
        key = Key(scale=self.major, number=57)
        self.assertEqual(key.number, 57)
        self.assertEqual(key.scale, [ 2, 2, 1, 2, 2, 2, 1 ])

class TestBassLine(unittest.TestCase):
    
    def test_nothing(self):
        self.assertEqual(Key.to_bassline(None), [])
        self.assertEqual(Key.to_bassline([]), [])

    def test_c_chord(self):
        self.assertEqual(Key.to_bassline([60, 64, 67]), [48, 55])

    def test_seventh_chord(self):
        self.assertEqual(Key.to_bassline([60, 64, 67, 70]), [48, 55])

    def test_low_fifth(self):
        self.assertEqual(Key.to_bassline([4, 8, 11]), [4, 11])

    def test_low_third(self):
        self.assertEqual(Key.to_bassline([8, 12, 15]), [8, 15])