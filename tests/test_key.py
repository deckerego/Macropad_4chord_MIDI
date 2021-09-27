from key import Key
import unittest

class TestChords(unittest.TestCase):

    def test_1st_degree(self):
        key = Key('C', 4)
        self.assertEqual(key.chord('I'), [60, 64, 67])

    def test_6th_degree(self):
        key = Key('C', 4)
        self.assertEqual(key.chord('vi'), [69, 72, 76])

class TestName(unittest.TestCase):

    def test_c_four(self):
        name = Key.to_name(60)
        self.assertEqual(name, "C4")

    def test_f_sharp_two(self):
        name = Key.to_name(42)
        self.assertEqual(name, "F#2" )
