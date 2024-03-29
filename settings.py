key_configs = {
    # MIDI note 60 is considered to be "middle C," but not everyone agrees
    # what octave note 60 is in. I go with the GarageBand value of C3 by default,
    # but some DAWs (like Renoise) or controllers consider C4 to be "middle C" 
    # at note 60. If it bugs you, change it here.
    'middle_octave': 3,
    # The offset of the degrees within each scale. You can think of 2 as "whole"
    # and 1 as "half," so a "2" on index 0 would mean two notes from the root.
    # Special thanks to https://pulse.berklee.edu/?lesson=73&id=4 for helping me double-check
    'scale_degrees': [
        ('Pentatonic',      [ 2, 2, 3, 2, 3 ]),      # Pentatonic Major
        ('Minor Pentatonic',[ 3, 2, 2, 3, 2 ]),      # Pentatonic Minor
        ('Major Blues',     [ 2, 1, 1, 3, 2, 3 ]),   # Pentatonic Major + Chromatic
        ('Minor Blues',     [ 3, 2, 1, 1, 3, 2 ]),   # Pentatonic Minor + Chromatic
        ('Major Scale',     [ 2, 2, 1, 2, 2, 2, 1 ]),# Heptatonic Major
        ('Minor Scale',     [ 2, 1, 2, 2, 1, 2, 2 ]),# Heptatonic Minor
        ('Harmonic Minor',  [ 2, 1, 2, 2, 1, 3, 1 ]),# Harmonic Minor
        ('Chromatic Scale', [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ])
    ]
}

melody_configs = {
    # The *index* of the MIDI Channel for notes (e.g. 0 is actually MIDI Channel 1)
    'channel': 0
}

autochord_configs = {
    # Bass notes to add to the chord (empty array is none, otherwise specify as offsets to the cord).
    # For example [0, 2] would be the root note and perfect fifth of a triad but one octave lower,
    # or [1] would be the second note of the chord (so for a triad the third note). 
    # If we can't go any lower than the current octave, the bass notes are omitted.
    'bass_notes': [ 0, 2 ] # Bass notes on root and perfect 5th of triad
}

harmony_configs = {
    # The *index* of the MIDI Channel for notes (e.g. 0 is actually MIDI Channel 1)
    'channel': 0,
    # The list of root keys you can select from turning the rotary dial
    'keys': [ "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
    # The list of progressions you can select by press & turning on the rotary dial
    # Format: (Display Name, [ Degree List ], Scale Name, Mode Number)
    'progressions': [
        ('Pop Progression',       ["I",  "V",   "vi", "IV" ], 'Major Scale', 0),
        ('Two Five One',          ["ii", "V",   "I",  "IV"], 'Major Scale', 0),
        ('Minor Pop',             ["vi", "IV",  "I",  "V"  ], 'Major Scale', 0),
        ('Royal Road',            ["IV", "V",   "iii","vi" ], 'Major Scale', 0),
        ('Alternate Western Pop', ["I",  "IV",  "vi", "V"  ], 'Major Scale', 0),
        ('Coldplay Progression',  ["IV", "V",   "I",  "vi" ], 'Major Scale', 0),
        ('\'50s Progression',     ["I",  "vi",  "IV", "V"  ], 'Major Scale', 0),
        ('Montgomery Ward Bridge',["I",  "IV",  "ii", "V"  ], 'Major Scale', 0),
        ('Blues Progression',     ["I",  "iii", "vi", "V"  ], 'Major Scale', 0),
        ('Take Me On',            ["I",  "iii", "vi", "IV" ], 'Major Scale', 0),
        ('Mixolydian Foo',        ["I",  "v",   "IV", "ii" ], 'Major Scale', 4)
    ]
}

rhythm_configs = {
    # The *index* of the MIDI Channel for percussion (e.g. 9 is actually MIDI Channel 10)
    'channel': 9,
    # List of pads as they show on the display, stored as (LED color, name, MIDI number)
    # See also https://www.midi.org/specifications-old/item/gm-level-1-sound-set
    'kits': [
        ('Acoustic Drum Kit', [
            # Layout is intended to be similar to a standard drum kit, as illustrated at:
            # https://macprovideo.com/article/audio-software/everything-producers-need-to-know-about-drum-maps
            [(0xFFF500, 'HHClose', 42), (0xFFF500, 'HHPedal', 44), (0xFFF500, 'HHOpen',  46)],
            [(0xFFF500, 'Crash',   49), (0xFFF500, 'Ride',    51), (0xFFF500, 'LgCrash', 57)],
            [(0x12B0FF, 'Snare',   38), (0x12B0FF, 'SmolTom', 50), (0x12B0FF, 'LgTom',   45)],
            [(0xFF1930, 'Kick',    35), (0xFF1930, 'LoFlTom', 41), (0xFF1930, 'HiFlTom', 43)]
        ]),
        ('Rhythm Composer', [
            # Layout inspired by the instruments of the TR-808, MIDI details at:
            # https://www.roland.com/global/support/by_product/rc_tr-808/owners_manuals/
            # Some pads adjusted to work with the GarageBand "Roland TR-808" electronic drum kit
            [(0xFFF500, 'HHClose', 42), (0xFFF500, 'HHOpen',  46), (0xFFF500, 'Cymbal',  49)],
            [(0xF200FF, 'Clap',    39), (0xF200FF, 'Claves',  37), (0xF200FF, 'Cowbell', 56)],
            [(0x12B0FF, 'LoTom',   41), (0x12B0FF, 'MdTom',   45), (0x12B0FF, 'HiTom',   48)],
            [(0xFF1930, 'Kick',    36), (0xFF1930, 'Snare',   40), (0x12B0FF, 'LowMid',  47)]
        ]),
        ('Percussion', [
            # A grab bag of other useful percussion instruments
            [(0xFFF500, 'Bells',   59), (0xF200FF, 'Claves',  75), (0xF200FF, 'Maraca',  70)],
            [(0x12B0FF, 'HBongo',  60), (0x12B0FF, 'Conga',   63), (0x12B0FF, 'HTimbl',  65)],
            [(0x12B0FF, 'LBongo',  61), (0x12B0FF, 'CongaD',  62), (0x12B0FF, 'LTimbl',  66)],
            [(0xFF1930, 'Stomp',   57), (0xFF1930, 'Wdblck',  77), (0x00FF9E, 'Snap',    58)]
        ])
    ]
}

# MIDI control defaults accessible in the MIDI Controls section
midi_configs = {
    'Velocity': 96,        # Note velocity to be sent with each note
    'Attack': 16,          # Envelope attack time
    'Release': 16,         # Envelope release time
    'Brightness': 0,       # Filter cutoff frequency
    'Timbre': 0,           # Filter envelope levels
    'TimePortamento': 0,   # Rate that portamento slides the pitch between notes
    'CtlPortamento': 0,    # Portamento on/off
    'ChorusSend': 0,       # Chorus effect level
    'PanL/R': 64,          # Pan left/right channel (64 is center)
    'Volume': 90,          # Volume of the send
    'Arpeggio': 0,         # Delay between each note played in autochord (strum effect)
    'Celeste': 0           # Detune level
}

display_configs = {
    'brightness': 0.2,     # Brightness of LEDs and screen from 0.0 to 1.0
    'sleep_seconds': 300,  # Seconds before going into low power mode, None to disable
}

class Settings:
    def __init__(self):
        self.chords = harmony_configs
        self.scales = melody_configs
        self.midi = midi_configs
        self.drums = rhythm_configs
        self.display = display_configs
        self.keys = key_configs
        self.autochord = autochord_configs
