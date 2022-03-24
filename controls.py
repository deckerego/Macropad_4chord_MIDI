import settings
import displayio
from rainbowio import colorwheel
from adafruit_macropad import MacroPad

class Controls:
    def __init__(self, macropad):
        self.display = Display(macropad)
        self.pixels = Pixels(macropad)

    def refresh(self):
        self.display.refresh()
        self.pixels.refresh()

    def keypad_events(self, events):
        for event in events:
            if event.pressed:
                print("Pressed")
            else: # event.released
                print("Released")

    def rotate_event(self, encoder_position, encoder_last_position, encoder_switch):
        print("Rotation")

    def sleep_event(self):
        self.pixels.sleep()
        self.display.sleep()

class Display:
    def __init__(self, macropad):
        self.display = macropad.display
        self.scaled_brightness = 0.5 + (settings.conf['brightness'] * 0.5)
        self.text_lines = macropad.display_text("")

    def refresh(self):
        self.display.auto_refresh = False
        self.display.auto_brightness = True
        self.display.brightness = self.scaled_brightness
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

SEGMENT_SIZE = 255 // 7
SUBSEGMENT_SIZE = SEGMENT_SIZE // 3

class Pixels:
    def __init__(self, macropad):
        self.pixels = macropad.pixels

    def refresh(self):
        self.pixels.auto_write = False
        self.pixels.brightness = settings.conf['brightness']
        self.palette = [0x0F0F0F for i in range(12)]
        self.reset()

    def wake(self):
        if self.pixels.brightness <= 0:
            self.pixels.brightness = settings.conf['brightness']
            self.pixels.show()

    def sleep(self):
        self.pixels.brightness = 0
        self.pixels.show()

    def reset(self):
        self.wake()
        for index in range(12):
            self.pixels[index] = self.palette[index]
        self.pixels.show()
