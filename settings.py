chord_configs = {
    # The *index* of the MIDI Channel for notes (e.g. 0 is actually MIDI Channel 1)
    'channel': 0,
    # The list of root keys you can select from turning the rotary dial
    'keys': [ "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
    # The list of progressions you can select by press & turning on the rotary dial
    'progressions': {
        'Pop Progression':          ["I",  "V",   "vi", "IV" ],
        'Minor Pop':                ["vi", "IV",  "I",  "V"  ],
        'Royal Road':               ["IV", "V",   "iii","vi" ],
        'Alternate Western Pop':    ["I",  "IV",  "vi", "V"  ],
        'Coldplay Progression':     ["IV", "V",   "I",  "vi" ],
        '\'50s Progression':        ["I",  "vi",  "IV", "V"  ],
        'Montgomery Ward Bridge':   ["I",  "IV",  "ii", "V"  ],
        'Blues Progression':        ["I",  "iii", "vi", "V"  ],
        'Take Me On':               ["I",  "iii", "vi", "IV" ],
        'Minor TOM':                ["ii", "V",   "I",  "iii"]
    }
}

drum_configs = {
    # The *index* of the MIDI Channel for percussion (e.g. 9 is actually MIDI Channel 10)
    'channel': 9,
    # List of pads as they show on the display, stored as (LED color, name, MIDI number)
    # See also https://www.midi.org/specifications-old/item/gm-level-1-sound-set
    'kits': {
        'Acoustic Drum Kit': [
            [(0x544408, 'CrashC',  49), (0x544408, 'HatCls',  42), (0x544408, 'HatOpn',  46)],
            [(0x04541B, 'XStick',  37), (0x095E06, 'Snare',   38), (0x04541B, 'SnrRod',  91)],
            [(0x000754, 'FlorTom', 43), (0x000754, 'LowTom',  45), (0x000754, 'HiTom',   50)],
            [(0x540908, 'Bass',    35), (0x540908, 'Kick',    36), (0x04541B, 'Cowbell', 56)]
        ],
        'Electric Drum Kit': [
            [(0x544408, 'CrashC',  49), (0x544408, 'HatCls',  42), (0x544408, 'HatOpn',  46)],
            [(0x095E06, 'Snare',   38), (0x095E06, 'ESnare',  40), (0x095E06, 'XStick',  37)],
            [(0x000754, 'Tom1',    41), (0x000754, 'Tom2',    43), (0x000754, 'LTom',    45)],
            [(0x04541B, 'Clap',    39), (0x540908, 'Kick',    36), (0x04541B, 'Cowbell', 47)]
        ],
        'Percussion': [
            [(0x544408, 'Bells',   59), (0x544408, 'Claves',  75), (0x544408, 'Maraca',  70)],
            [(0x095E06, 'HBongo',  60), (0x000754, 'Conga',   63), (0x04541B, 'HTimbl',  65)],
            [(0x095E06, 'LBongo',  61), (0x000754, 'CongaD',  62), (0x04541B, 'LTimbl',  66)],
            [(0x540908, 'Stomp',   57), (0x540908, 'Wdblck',  77), (0x540908, 'Snap',    58)]
        ]
    }
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
    'Breath': 0,           # Wind instrument breath control
    'Celeste': 0           # Detune level
}

display_configs = {
    'brightness': 0.2,     # Brightness of LEDs and screen from 0.0 to 1.0
    'sleep_seconds': 300,  # Seconds before the LEDs turn off, None if they are always on
}

class Settings:
    def __init__(self):
        self.chords = chord_configs
        self.midi = midi_configs
        self.drums = drum_configs
        self.display = display_configs
