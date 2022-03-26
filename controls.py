import settings
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_midi import control_change_values
from rainbowio import colorwheel
from adafruit_macropad import MacroPad

# Several of these can be removed after https://github.com/adafruit/Adafruit_CircuitPython_MIDI/pull/49
ATTACK_TIME = 73
PORTAMENTO_TIME = 37
CHORUS = 93
DETUNE = 94
PHASER = 95

controls = [
    ('Attack', ATTACK_TIME), ('Release', control_change_values.RELEASE_TIME), ('Brightness', control_change_values.CUTOFF_FREQUENCY),
    ('Timbre', control_change_values.FILTER_RESONANCE), ('TimePortamento', PORTAMENTO_TIME), ('CtlPortamento', control_change_values.PORTAMENTO),
    ('Chorus Send', CHORUS), ('PanL/R', control_change_values.PAN), ('Volume', control_change_values.VOLUME),
    ('Breath', control_change_values.BREATH_CONTROL), ('Celeste', DETUNE), ('Phaser', PHASER)
]

class Controls:
    def __init__(self, macropad, settings):
        self.settings = settings
        self.display = Display(macropad, self.settings.display['brightness'])
        self.pixels = Pixels(macropad, self.settings.display['brightness'])
        self.pressed = None


    def refresh(self):
        self.display.reload()
        self.pixels.refresh()

    def keypad_events(self, events):
        for event in events:
            if event.pressed:
                self.pressed = event.key_number
                self.display.adjust(event.key_number)
                self.pixels.press(event.key_number)
            else: # event.released
                if event.key_number == self.pressed:
                    self.pressed = None
                if not self.pressed:
                    self.display.reload()
                self.pixels.release(event.key_number)

    def rotate_event(self, encoder_position, encoder_last_position, encoder_switch):
        print("Rotation")

    def sleep_event(self):
        self.pixels.sleep()
        self.display.sleep()

class Display:
    def __init__(self, macropad, brightness):
        self.display = macropad.display
        self.scaled_brightness = 0.5 + (brightness * 0.5)
        self.group = displayio.Group()
        for key_index in range(12):
            x = key_index % 3
            y = key_index // 3
            self.group.append(
                label.Label(terminalio.FONT,
                    text='',
                    color=0xFFFFFF,
                    anchored_position=((self.display.width - 1) * x / 2,
                    self.display.height - 1 - (3 - y) * 12),
                    anchor_point=(x / 2, 1.0)
                )
            )
        self.group.append(Rect(0, 0, self.display.width, 12, fill=0xFFFFFF))
        self.group.append(
            label.Label(
                terminalio.FONT,
                text='',
                color=0x000000,
                anchored_position=(self.display.width//2, -2),
                anchor_point=(0.5, 0.0)
            )
        )

    def adjust(self, key):
        control_name, _ = controls[key]
        control_value = 64
        self.group[13].anchored_position=(5, -2)
        self.group[13].anchor_point=(0, 0)
        self.group[13].text = "%s: %d" % (control_name, control_value)
        self.display.show(self.group)
        self.display.refresh()

    def reload(self):
        self.display.auto_refresh = False
        self.display.auto_brightness = True
        self.display.brightness = self.scaled_brightness

        self.group[13].anchored_position=(self.display.width//2, -2)
        self.group[13].anchor_point=(0.5, 0.0)
        self.group[13].text = 'MIDI Controls'
        for i in range(12):
            control_name, _ = controls[i]
            self.group[i].text = control_name[:6]

        self.display.show(self.group)
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
    def __init__(self, macropad, brightness):
        self.pixels = macropad.pixels
        self.brightness = brightness
        self.default_color = 0x0F0F0F
        self.highlight_color = 0xFFFFFF

    def refresh(self):
        self.pixels.auto_write = False
        self.pixels.brightness = self.brightness
        self.palette = [self.default_color for i in range(12)]
        self.reset()

    def press(self, key):
        self.palette[key] = self.highlight_color
        self.reset()

    def release(self, key):
        self.palette[key] = self.default_color
        self.reset()

    def wake(self):
        if self.pixels.brightness <= 0:
            self.pixels.brightness = self.brightness
            self.pixels.show()

    def sleep(self):
        self.pixels.brightness = 0
        self.pixels.show()

    def reset(self):
        self.wake()
        for index in range(12):
            self.pixels[index] = self.palette[index]
        self.pixels.show()
