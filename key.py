from settings import Settings
settings = Settings()

CHROMATIC_SCALE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
CHROMATIC_SCALE_LENGTH = len(CHROMATIC_SCALE_NAMES)
DEGREES = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']

# Set the octove for MIDI note 60 (middle C)
MIDDLE_OCTAVE = settings.keys['middle_octave']
MIDDLE_C = 60
START_OCTAVE = MIDDLE_OCTAVE - (MIDDLE_C // 12)

# We want to include all full scales starting at A and going to G#,
# which would end with note 116. MIDI 1.0 goes to note 127,
# but we need room for a seventh degree chord's perfect fifth, 
# so let's max out at note 111 (D#).
END_NOTE = 116 - 5
START_NOTE = 0

# Calculations for chords based on the selected key
class Key:
    
    def __init__(self, key, octave=MIDDLE_OCTAVE):
        self.octave = octave
        self.key = key
        self.key_offset = CHROMATIC_SCALE_NAMES.index(key.upper())
        self.octave_offset = START_NOTE + ((octave - START_OCTAVE) * CHROMATIC_SCALE_LENGTH)
        self.number = self.octave_offset + self.key_offset

    def chord(self, numeral, scale):
        degree = Key.to_degree(numeral)
        root =  self.number + scale[degree    ]
        third = self.number + scale[degree + 2]
        fifth = self.number + scale[degree + 4]
        return [root, third, fifth]

    def chords(self, progression, scale):
        return [self.chord(degree, scale) for degree in progression]

    def advance(self, index):
        key_index = self.key_offset + index
        octave = self.octave + (key_index // CHROMATIC_SCALE_LENGTH)
        key = CHROMATIC_SCALE_NAMES[key_index % CHROMATIC_SCALE_LENGTH]
        new_key = Key(key, octave)
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
