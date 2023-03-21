key_configs = {
    # MIDI note 60 is considered to be "middle C," but not everyone agrees
    # what octave note 60 is in. I go with the GarageBand value of C3 by default,
    # but some DAWs (like Renoise) or controllers consider C4 to be "middle C" 
    # at note 60. If it bugs you, change it here.
    'middle_octave': 3
}

melody_configs = {
    # The *index* of the MIDI Channel for notes (e.g. 0 is actually MIDI Channel 1)
    'channel': 0,
    # The offset of the degrees within each scale. You can think of 2 as "whole"
    # and 1 as "half," so a "2" on index 0 would mean two notes from the root.
    # Special thanks to https://pulse.berklee.edu/?lesson=73&id=4 for helping me double-check
    'scale_degrees': [
        ('Major Scale',     [ 2, 2, 1, 2, 2, 2, 1 ]), # Heptatonic Major
    ]
}

harmony_configs = {
    # The *index* of the MIDI Channel for notes (e.g. 0 is actually MIDI Channel 1)
    'channel': 0,
    # The list of root keys you can select from turning the rotary dial
    'keys': [ "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
    # The list of progressions you can select by press & turning on the rotary dial
    'progressions': [
        ('Pop Progression',       ["I",  "V",   "vi", "IV" ]),
        ('Minor Pop',             ["vi", "IV",  "I",  "V"  ]),
        ('Royal Road',            ["IV", "V",   "iii","vi" ]),
        ('Alternate Western Pop', ["I",  "IV",  "vi", "V"  ]),
        ('Coldplay Progression',  ["IV", "V",   "I",  "vi" ]),
        ('\'50s Progression',     ["I",  "vi",  "IV", "V"  ]),
        ('Montgomery Ward Bridge',["I",  "IV",  "ii", "V"  ]),
        ('Blues Progression',     ["I",  "iii", "vi", "V"  ]),
        ('Take Me On',            ["I",  "iii", "vi", "IV" ]),
        ('Minor TOM',             ["ii", "V",   "I",  "iii"])
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
    'Breath': 0,           # Wind instrument breath control
    'Celeste': 0           # Detune level
}

display_configs = {
    'brightness': 0.2,     # Brightness of LEDs and screen from 0.0 to 1.0
    'sleep_seconds': 300,  # Seconds before the LEDs turn off, None if they are always on
}

class Settings:
    chords = harmony_configs
    scales = melody_configs
    midi = midi_configs
    drums = rhythm_configs
    display = display_configs
    keys = key_configs
