from settings import Settings
settings = Settings()

NUMERALS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
CHROMATIC_SCALE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
CHROMATIC_SCALE_LENGTH = len(CHROMATIC_SCALE_NAMES)

# Set the octove for MIDI note 60 (middle C)
MIDDLE_OCTAVE = settings.keys['middle_octave']
MIDDLE_C = 60
START_OCTAVE = MIDDLE_OCTAVE - (MIDDLE_C // 12)

# We want to include all full scales starting at A and going to G#,
# which would end with note 116. MIDI 1.0 goes to note 127,
# but we need room for a seventh degree chord's perfect fifth, 
# so let's max out at note 111 (D#).
START_NOTE, END_NOTE = 0, 116 - 5

# Calculations for chords based on the selected key
class Key:

    # Create a new root "key."
    # key:    The root key (given as a letter in the chromatic scale)
    # scale:  A scale, defined as offsets to the degrees within each scale (see settings.py)
    # octave: The "middle" octave as a single-digit number (most MIDI controllers assume this to be 3)
    # mode:   The zero-indexed mode number of the scale (e.g. 0 would be Ionian, 1 would be Dorian)
    def __init__(self, key=CHROMATIC_SCALE_NAMES[0], scale=[], octave=MIDDLE_OCTAVE, mode=0, number=None):
        if number:
            self.octave = Key.to_octave(number)
            self.key = Key.to_note(number)
        else:
            self.octave = octave
            self.key = key
        self.scale = scale
        self.mode = mode
        self.circle = self.scale[self.mode:] + self.scale[:self.mode]
        self.circle += self.circle
        self.key_offset = CHROMATIC_SCALE_NAMES.index(self.key.upper())
        self.octave_offset = START_NOTE + ((self.octave - START_OCTAVE) * CHROMATIC_SCALE_LENGTH)
        self.number = self.octave_offset + self.key_offset

    def __third(self): return self.number + sum(self.circle[:2])
    def __third_minor(self): return self.__third() - 1
    def __fifth(self): return self.number + sum(self.circle[:4])
    def __fifth_augmented(self): return self.__fifth() + 1
    def __fifth_diminished(self): return self.__fifth() - 1
    def __seventh(self): return self.number + sum(self.circle[:6])
    def __seventh_minor(self): return self.__seventh() - 1

    def chord_major(self): return [self.number, self.__third(), self.__fifth()]
    def chord_minor(self): return [self.number, self.__third_minor(), self.__fifth()]
    def chord_seventh(self): return [self.number, self.__third(), self.__fifth(), self.__seventh_minor()]
    def chord_seventh_maj(self): return [self.number, self.__third(), self.__fifth(), self.__seventh()]
    def chord_seventh_min(self): return [self.number, self.__third_minor(), self.__fifth(), self.__seventh_minor()]
    def chord_augmented(self): return [self.number, self.__third(), self.__fifth_augmented()]
    def chord_diminished(self): return [self.number, self.__third_minor(), self.__fifth_diminished()]

    def chord(self, numeral):
        degree = Key.to_degree(numeral)
        root = self.number + sum(self.circle[:degree + 0])
        third = self.number + sum(self.circle[:degree + 2])
        fifth = self.number + sum(self.circle[:degree + 4])
        return [root, third, fifth]

    def set_scale(self, scale, mode=0):
        self.__init__(self.key, scale, self.octave, mode)

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
    def to_bassline(chord):
        bassline = []
        if not chord or len(chord) <= 0: return bassline

        first = chord[0]
        fifth = chord[2] if len(chord) >= 3 else None

        bassline.append(first if first < 12 else first - 12)
        if fifth: bassline.append(fifth if first < 12 else fifth - 12)
        return bassline

    @staticmethod
    def to_name(number):
        return "%s%i" % (Key.to_note(number), Key.to_octave(number))

    @staticmethod
    def to_octave(number):
        octave_idx = (number - START_NOTE) // CHROMATIC_SCALE_LENGTH
        return octave_idx + START_OCTAVE

    @staticmethod
    def to_note(number):
        note_idx = (number - START_NOTE) % CHROMATIC_SCALE_LENGTH
        return CHROMATIC_SCALE_NAMES[note_idx]

    @staticmethod
    def to_degree(numeral):
        numeral_sanitized = ''.join(filter(lambda c: c.isalpha(), numeral.lower()))
        return NUMERALS.index(numeral_sanitized)
