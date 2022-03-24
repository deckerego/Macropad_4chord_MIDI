conf = {
    'velocity': 96,        # MIDI note velocity to be sent with each note
    'pitch_bend': 8195,    # MIDI pitch bend to be sent with each note
    'brightness': 0.2,     # Brightness of LEDs and screen from 0.0 to 1.0
    'sleep_seconds': 300,  # Seconds before the LEDs turn off, None if they are always on
    # The list of keys you can select from turning the rotary dial
    'keys': [ "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
    # The list of progressions you can select by press & turning on the rotary dial
    'progressions': [
        ["I",  "V",   "vi", "IV"], # The "pop" progression
        ["I",  "IV",  "vi", "V" ], # Alternate Western pop
        ["vi", "IV",  "I",  "V" ], # Minor pop progression
        ["IV", "V",   "I",  "vi"], # Coldplay progression
        ["I",  "vi",  "IV", "V" ], # The '50s progression
        ["I",  "IV",  "ii", "V" ], # The Montgomery Ward bridge
        ["I",  "iii", "vi", "V" ]  # Blues progression
    ]
}
