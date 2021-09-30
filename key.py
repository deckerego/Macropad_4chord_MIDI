MAJOR_SCALE = [2, 2, 1, 2, 2, 2, 1]
MINOR_SCALE = [2, 1, 2, 2, 1, 2, 2]
CHROMATIC_SCALE_NAMES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
SCALE_LENGTH = len(CHROMATIC_SCALE_NAMES)
DEGREES = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']

# I'm considering MIDI note 60 (middle C) to be C4.
# If we want to include all full scales starting at A and going to G#,
# that means we start at A-1 (note #9) and end at G#8 (note #116)
START_NOTE = 9
# However, MIDI 1.0 only goes to note 127 and so if we use a seventh degree's
# perfect fifth, that means we max out at note 111 (D#8).
END_NOTE = 111

# Calculations for chords based on the selected key
class Key:
    def __init__(self, key, octave):
        self.octave = octave
        self.key = key
        self.key_offset = CHROMATIC_SCALE_NAMES.index(key.upper())
        self.octave_offset = START_NOTE + (octave * SCALE_LENGTH)
        self.number = self.octave_offset + self.key_offset

    def chord(self, numeral):
        scale = MINOR_SCALE if numeral.islower() else MAJOR_SCALE
        degree = Key.to_degree(numeral)
        root = self.number + sum(offset for offset in MAJOR_SCALE[:degree])
        third = root + sum(offset for offset in scale[:2])
        fifth = root + sum(offset for offset in scale[:4])
        return [root, third, fifth]

    def chords(self, progression):
        return [self.chord(degree) for degree in progression]

    def advance(self, index):
        key_index = self.key_offset + index
        octave = self.octave + key_index // SCALE_LENGTH
        key = CHROMATIC_SCALE_NAMES[key_index % SCALE_LENGTH]
        new_key = Key(key, octave)
        if new_key.number >=0 and new_key.number <= END_NOTE:
            return new_key
        else: # We are out of range of allowed roots
            return self

    @staticmethod
    def to_name(number):
        octave = (number - START_NOTE) // SCALE_LENGTH
        note_idx = (number - START_NOTE) % SCALE_LENGTH
        return "%s%i" % (CHROMATIC_SCALE_NAMES[note_idx], octave)

    @staticmethod
    def to_degree(numeral):
        return DEGREES.index(numeral)
