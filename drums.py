import settings
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from rainbowio import colorwheel
from drumkits import DrumKits

class Drums:

    def __init__(self, macropad):
        self.display = Display(macropad)
        self.pixels = Pixels(macropad)
        self.macropad = macropad
        self.kits = DrumKits()
        self.note_velocity = settings.conf['velocity']
        self.active_notes = [None for i in range(12)]

    def refresh(self):
        self.display.refresh()
        self.pixels.refresh()

        name, kit = self.kits.get()
        self.display.set_kit(name, kit)
        self.pixels.set_kit(kit)

    def keypad_events(self, events):
        _, kit = self.kits.get()
        for event in events:
            if event.pressed:
                row = event.key_number // 3
                column = event.key_number % 3
                if row < len(kit) and column < len(kit[row]):
                    color, _, note = kit[row][column]
                    self.macropad.midi.send(self.macropad.NoteOn(note, self.note_velocity))
                    self.active_notes[event.key_number] = note
            else: # event.released
                note = self.active_notes[event.key_number]
                self.macropad.midi.send(self.macropad.NoteOff(note, self.note_velocity))
                self.active_notes[event.key_number] = None
        self.pixels.set_playing(self.active_notes)

    def rotate_event(self, encoder_position, encoder_last_position, encoder_switch):
        change = encoder_position - encoder_last_position
        name, kit = self.kits.prev() if change < 0 else self.kits.next()
        self.display.set_kit(name, kit)
        self.pixels.set_kit(kit)

    def sleep_event(self):
        self.pixels.sleep()
        self.display.sleep()

class Display:
    def __init__(self, macropad):
        self.display = macropad.display
        self.scaled_brightness = 0.5 + (settings.conf['brightness'] * 0.5)
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

    def refresh(self):
        self.display.auto_refresh = False
        self.display.auto_brightness = True
        self.display.brightness = self.scaled_brightness
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

    def set_kit(self, name, kit):
        self.group[13].text = name
        for i in range(12):
            row = i // 3
            column = i % 3
            if row < len(kit) and column < len(kit[row]):
                _, self.group[i].text, _ = kit[row][column]
        self.refresh()


SEGMENT_SIZE = 255 // 7
SUBSEGMENT_SIZE = SEGMENT_SIZE // 3

class Pixels:
    def __init__(self, macropad):
        self.pixels = macropad.pixels
        self.palette = [0x0F0F0F for i in range(12)]

    def refresh(self):
        self.pixels.auto_write = False
        self.pixels.brightness = settings.conf['brightness']
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

    def set_kit(self, kit):
        for i in range(12):
            row = i // 3
            column = i % 3
            if row < len(kit) and column < len(kit[row]):
                self.palette[i], _, _ = kit[row][column]
        self.reset()

    def set_playing(self, active_notes):
        self.wake()
        for index in range(12):
            self.pixels[index] = 0xFFFFFF if active_notes[index] else self.palette[index]
        self.pixels.show()
