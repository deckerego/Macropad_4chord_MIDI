import settings
import displayio
from adafruit_macropad import MacroPad
from key import Key

class Display:
    def __init__(self, macropad):
        self.display = macropad.display
        self.scaled_brightness = 0.5 + (settings.conf['brightness'] * 0.5)
        self.display.auto_refresh = False
        self.display.auto_brightness = True
        self.display.brightness = self.scaled_brightness
        self.text_lines = macropad.display_text("Macropad 4chord MIDI")
        self.text_lines.show()
        self.display.refresh()

    def wake(self):
        if self.display.brightness <= 0:
            self.display.brightness = self.scaled_brightness
            self.display.refresh()

    def sleep(self):
        self.display.auto_brightness = False
        self.display.brightness = 0
        self.display.refresh()

    def set_progression(self, progression):
        self.wake()
        self.text_lines[1].text = "Chords: " + ' '.join(progression)
        self.display.refresh()

    def set_key(self, key):
        self.wake()
        self.text_lines[0].text = "Key: %s Oct: %i" % (key.key, key.octave)
        self.display.refresh()

    def set_playing(self, notes):
        self.wake()
        note_names = [Key.to_name(note) for note in notes if note]
        self.text_lines[2].text = "Pressed: " + ' '.join(note_names)
        self.display.refresh()
