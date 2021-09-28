# I'm considering MIDI note 60 (middle C) to be C4
major_scale = [2, 2, 1, 2, 2, 2, 1]
minor_scale = [2, 1, 2, 2, 1, 2, 2]
chromatic_scale_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
degrees = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']

class Key:
    def __init__(self, key, octave):
        self.octave = octave
        self.key = key
        self.key_offset = chromatic_scale_names.index(key.upper())
        self.octave_offset = 9 + (octave * 12)
        self.number = self.octave_offset + self.key_offset

    def chord(self, numeral):
        scale = minor_scale if numeral.islower() else major_scale
        degree = degrees.index(numeral)
        root = self.number + sum(offset for offset in major_scale[:degree])
        third = root + sum(offset for offset in scale[:2])
        fifth = root + sum(offset for offset in scale[:4])
        return [root, third, fifth]

    def advance(self, index):
        scale_length = len(chromatic_scale_names)
        key_index = self.key_offset + index
        octave = self.octave + key_index // scale_length
        key = chromatic_scale_names[key_index % scale_length]
        new_key = Key(key, octave)
        if new_key.number >=0 and new_key.number < 112:
            return new_key
        else: # Must be between C-1 and D#7
            return self

    @staticmethod
    def to_name(number):
        octave = (number - 9) // 12
        note_idx = (number - 9) % 12
        return "%s%i" % (chromatic_scale_names[note_idx], octave)
