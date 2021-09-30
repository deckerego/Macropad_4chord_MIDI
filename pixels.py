import settings
from rainbowio import colorwheel
from key import Key

SEGMENT_SIZE = 255 // 7
SUBSEGMENT_SIZE = SEGMENT_SIZE // 3

# Everything related to lighting the Macropad's keypad
class Pixels:
    def __init__(self, macropad):
        self.pixels = macropad.pixels
        self.pixels.auto_write = False
        self.palette = [0x0F0F0F for i in range(12)]
        self.pixels.brightness = settings.conf['brightness']
        self.reset()

    def wake(self):
        if self.pixels.brightness <= 0:
            self.pixels.brightness = settings.conf['brightness']
            self.pixels.show()

    def sleep(self):
        self.pixels.brightness = 0
        self.pixels.show()

    def set_progression(self, progression):
        for row in range(4):
            for column in range(3):
                degree = Key.to_degree(progression[row])
                segment = SEGMENT_SIZE * degree
                subsegment = SUBSEGMENT_SIZE * column
                self.palette[(row * 3) + column] = colorwheel(segment + subsegment)
        self.reset()

    def set_playing(self, active_notes):
        self.wake()
        for index in range(12):
            self.pixels[index] = 0xFFFFFF if active_notes[index] else self.palette[index]
        self.pixels.show()

    def reset(self):
        self.wake()
        for index in range(12):
            self.pixels[index] = self.palette[index]
        self.pixels.show()