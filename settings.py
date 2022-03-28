chord_configs = {
    # The list of keys you can select from turning the rotary dial
    'keys': [ "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"], # Chromatic C
    # The list of progressions you can select by press & turning on the rotary dial
    'progressions': [
        ["I",  "V",   "vi", "IV"], # The "pop" progression
        ["I",  "IV",  "vi", "V" ], # Alternate Western pop
        ["vi", "IV",  "I",  "V" ], # Minor pop progression
        ["IV", "V",   "I",  "vi"], # Coldplay progression
        ["I",  "vi",  "IV", "V" ], # The '50s progression
        ["I",  "IV",  "ii", "V" ], # The Montgomery Ward bridge
        ["I",  "iii", "vi", "IV"], # A-ha progression
        ["I",  "iii", "vi", "V" ]  # Blues progression
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
    def __init__(self):
        self.chords = chord_configs
        self.midi = midi_configs
        self.display = display_configs
