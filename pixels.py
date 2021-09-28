import settings
from rainbowio import colorwheel
from key import Key

SEGMENT_SIZE = 255 // 7
SUBSEGMENT_SIZE = SEGMENT_SIZE // 3

class Pixels:
    def __init__(self, macropad):
        self.pixels = macropad.pixels
        self.pixels.auto_write = False
        self.pixels.brightness = settings.conf['led_brightness']
        self.palette = [0x0F0F0F for i in range(12)]
        self.reset()

    def set_brightness(self, brightness):
        self.pixels.brightness = brightness
        self.pixels.show()

    def set_progression(self, progression):
        for row in range(4):
            for column in range(3):
                degree = Key.to_degree(progression[row])
                segment = SEGMENT_SIZE * degree
                subsegment = SUBSEGMENT_SIZE * column
                self.palette[(row * 3) + column] = colorwheel(segment + subsegment)
        self.reset()

    def off(self, index):
        self.pixels[index] = self.palette[index]
        self.pixels.show()

    def highlight(self, index):
        self.pixels[index] = 0xFFFFFF
        self.pixels.show()

    def reset(self):
        for index in range(12):
            self.pixels[index] = self.palette[index]
        self.pixels.show()
