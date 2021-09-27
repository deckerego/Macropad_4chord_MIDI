# I'm considering MIDI note 60 (middle C) to be C4
major_scale = [2, 2, 1, 2, 2, 2, 1]
minor_scale = [2, 1, 2, 2, 1, 2, 2]
chromatic_scale_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
degrees = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']

class Key:
    def __init__(self, key, octave):
        self.octave = octave
        self.key = key
        self.key_offset = chromatic_scale_names.index(key.upper())
        self.octave_offset = 12 + (octave * 12)
        self.number = self.octave_offset + self.key_offset

    def chord(self, numeral):
        scale = minor_scale if numeral.islower() else major_scale
        degree = degrees.index(numeral)
        root = self.number + sum(offset for offset in major_scale[:degree])
        third = root + sum(offset for offset in scale[:2])
        fifth = root + sum(offset for offset in scale[:4])
        return [root, third, fifth]

    @staticmethod
    def to_name(number):
        octave = int((number - 12) / 12)
        note_idx = int(number % 12)
        return "%s%i" % (chromatic_scale_names[note_idx], octave)
