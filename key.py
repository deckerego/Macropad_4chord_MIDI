CHROMATIC_SCALE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
CHROMATIC_SCALE_LENGTH = len(CHROMATIC_SCALE_NAMES)
DEGREES = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']

# I'm considering MIDI note 60 (middle C) to be C3.
# If we want to include all full scales starting at A and going to G#,
# that means we start at C-2 (note #0) and end at G#7 (note #116)
START_NOTE = 0
START_OCTAVE = -2
# However, MIDI 1.0 only goes to note 127 and so if we use a seventh degree's
# perfect fifth, that means we max out at note 111 (D#7).
END_NOTE = 111

# Calculations for chords based on the selected key
class Key:
    def __init__(self, key, octave, scale):
        self.scale = scale
        self.octave = octave
        self.key = key
        self.key_offset = CHROMATIC_SCALE_NAMES.index(key.upper())
        self.octave_offset = START_NOTE + ((octave - START_OCTAVE) * CHROMATIC_SCALE_LENGTH)
        self.number = self.octave_offset + self.key_offset

    def chord(self, numeral):
        degree = Key.to_degree(numeral)
        root =  self.number + self.scale[degree    ]
        third = self.number + self.scale[degree + 2]
        fifth = self.number + self.scale[degree + 4]
        return [root, third, fifth]

    def chords(self, progression):
        return [self.chord(degree) for degree in progression]

    def advance(self, index):
        key_index = self.key_offset + index
        octave = self.octave + (key_index // CHROMATIC_SCALE_LENGTH)
        key = CHROMATIC_SCALE_NAMES[key_index % CHROMATIC_SCALE_LENGTH]
        new_key = Key(key, octave, self.scale)
        if new_key.number >=0 and new_key.number <= END_NOTE:
            return new_key
        else: # We are out of range of allowed roots
            return self

    @staticmethod
    def to_name(number):
        octave_idx = (number - START_NOTE) // CHROMATIC_SCALE_LENGTH
        return "%s%i" % (Key.to_note(number), octave_idx + START_OCTAVE)

    @staticmethod
    def to_note(number):
        note_idx = (number - START_NOTE) % CHROMATIC_SCALE_LENGTH
        return CHROMATIC_SCALE_NAMES[note_idx]

    @staticmethod
    def to_degree(numeral):
        return DEGREES.index(numeral)
