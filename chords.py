import settings
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from rainbowio import colorwheel
from key import Key
from adafruit_macropad import MacroPad

class Chords:
    def __init__(self, macropad):
        self.display = Display(macropad)
        self.pixels = Pixels(macropad)
        self.macropad = macropad

    def refresh(self):
        self.key = Key(settings.conf['keys'][0], 4)
        self.chords = None
        self.progression = settings.conf['progressions'][0]
        self.note_velocity = settings.conf['velocity']
        self.active_notes = [None for i in range(12)]

        self.display.refresh()
        self.pixels.refresh()
        self.switch_progression(0)
        self.switch_key(0)
        self.keypad_events([])

    def keypad_events(self, events):
        for event in events:
            if event.pressed:
                row = event.key_number // 3
                column = event.key_number % 3
                note = self.chords[row][column]
                self.macropad.midi.send(self.macropad.NoteOn(note, self.note_velocity))
                self.active_notes[event.key_number] = note
            else: # event.released
                note = self.active_notes[event.key_number]
                self.macropad.midi.send(self.macropad.NoteOff(note, self.note_velocity))
                self.active_notes[event.key_number] = None

        self.display.set_playing(self.active_notes)
        self.pixels.set_playing(self.active_notes)

    def rotate_event(self, encoder_position, encoder_last_position, encoder_switch):
        if encoder_switch: # The encoder button is pushed down
            self.switch_progression(encoder_position)
        else: # The encoder button is not pressed
            self.switch_key(encoder_position - encoder_last_position)

    def sleep_event(self):
        self.pixels.sleep()
        self.display.sleep()

    def switch_progression(self, position):
        index = position % len(settings.conf['progressions'])
        self.progression = settings.conf['progressions'][index]
        self.chords = self.key.chords(self.progression)
        self.pixels.set_progression(self.progression)
        self.display.set_progression(self.progression)

    def switch_key(self, position_change):
        if position_change:
            self.key = self.key.advance(position_change)
        else: # No change - reset to default
            self.key = Key(settings.conf['keys'][0], 4)
        self.chords = self.key.chords(self.progression)
        self.pixels.wake()
        self.display.set_key(self.key)

class Display:
    def __init__(self, macropad):
        self.display = macropad.display
        self.scaled_brightness = 0.5 + (settings.conf['brightness'] * 0.5)
        self.group = displayio.Group()
        self.group.append(Rect(0, 0, self.display.width, 12, fill=0xFFFFFF))
        self.group.append(Display.create_label('Macropad 4chord MIDI', (self.display.width//2, -2), (0.5, 0.0), 0x000000))
        self.group.append(Display.create_label("Key:", (0, self.display.height - 36), (0, 1.0)))
        self.group.append(Display.create_label("X#", (30, self.display.height - 36), (0, 1.0)))
        self.group.append(Display.create_label("Oct:", (self.display.width / 2, self.display.height - 36), (0, 1.0)))
        self.group.append(Display.create_label("00", ((self.display.width / 2) + 30, self.display.height - 36), (0, 1.0)))
        self.group.append(Display.create_label("Chords:", (0, self.display.height - 22), (0, 1.0)))
        self.group.append(Display.create_label("III III III III", (42, self.display.height - 22), (0, 1.0)))
        self.group.append(Display.create_label("Notes:", (0, self.display.height - 8), (0, 1.0)))
        self.group.append(Display.create_label("Xm# Xm# Xm# Xm#", (40, self.display.height - 8), (0, 1.0)))

    @staticmethod
    def create_label(text, anchor_position, anchor_point, color=0xFFFFFF):
        return label.Label(
            terminalio.FONT,
            text=text,
            color=color,
            anchored_position=anchor_position,
            anchor_point=anchor_point
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

    def set_progression(self, progression):
        self.wake()
        self.group[7].text = ' '.join(progression)
        self.display.refresh()

    def set_key(self, key):
        self.wake()
        self.group[3].text = key.key
        self.group[5].text = str(key.octave)
        self.display.refresh()

    def set_playing(self, notes):
        self.wake()
        note_names = [Key.to_name(note) for note in notes if note]
        self.group[9].text = ' '.join(note_names)
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