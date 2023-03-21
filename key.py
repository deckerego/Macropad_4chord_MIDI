from settings import Settings
settings = Settings()

CHROMATIC_SCALE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
CHROMATIC_SCALE_LENGTH = len(CHROMATIC_SCALE_NAMES)
NUMERALS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']

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
    
    def __init__(self, key, scale, octave=MIDDLE_OCTAVE, mode=1):
        self.octave = octave
        # Expand our scale to be three octaves long since we have
        # calculate the major 7th of the 7th degree of the 7th mode
        self.scale = [ *scale, *scale, *scale ]
        self.key = key
        self.mode = mode - 1
        self.key_offset = CHROMATIC_SCALE_NAMES.index(key.upper())
        self.octave_offset = START_NOTE + ((octave - START_OCTAVE) * CHROMATIC_SCALE_LENGTH)
        self.number = self.octave_offset + self.key_offset

    def chord(self, numeral):
        degree = Key.to_degree(numeral)
        root =  self.number + sum(self.scale[self.mode:degree + self.mode + 0])
        third = self.number + sum(self.scale[self.mode:degree + self.mode + 2])
        fifth = self.number + sum(self.scale[self.mode:degree + self.mode + 4])
        return [root, third, fifth]

    def chords(self, progression):
        return [self.chord(degree) for degree in progression]

    def advance(self, index):
        new_number = self.number + index
        if new_number >=0 and new_number <= END_NOTE:
            key_index = self.key_offset + index
            octave = self.octave + (key_index // CHROMATIC_SCALE_LENGTH)
            key = CHROMATIC_SCALE_NAMES[key_index % CHROMATIC_SCALE_LENGTH]
            self.__init__(key, self.scale, octave, self.mode)

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
        return NUMERALS.index(numeral.lower())
