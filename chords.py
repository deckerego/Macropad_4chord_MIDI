import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from rainbowio import colorwheel
from key import Key
from settings import Settings

class Chords:
    def __init__(self, macropad):
        self.settings = Settings()
        self.display = Display(macropad, self.settings.display['brightness'])
        self.pixels = Pixels(macropad, self.settings.display['brightness'])
        self.macropad = macropad
        self.key = Key()
        self.chords = None
        self.progression_idx = 0
        self.pitch_bend = 8192
        self.channel = self.settings.chords['channel']

    def refresh(self):
        self.active_notes = [None for i in range(12)]
        self.display.refresh()
        self.pixels.refresh()
        self.switch_progression(0)
        self.switch_key(0)

    def keypad_events(self, events):
        note_velocity = self.settings.midi['Velocity']

        for event in events:
            if event.pressed:
                row = event.key_number // 3
                column = event.key_number % 3
                note = self.chords[row][column]
                self.macropad.midi.send(self.macropad.NoteOn(note, note_velocity, channel=self.channel))
                self.active_notes[event.key_number] = note
            else: # event.released
                note = self.active_notes[event.key_number]
                self.macropad.midi.send(self.macropad.NoteOff(note, note_velocity, channel=self.channel))
                self.active_notes[event.key_number] = None
                notes_active = len(list(filter(lambda n: n is not None, self.active_notes)))
                if notes_active == 0: self.pitch_bend = 8192

        self.display.set_playing(self.active_notes)
        self.pixels.set_playing(self.active_notes)

    def rotate_event(self, encoder_position, encoder_last_position, encoder_switch):
        notes_active = len(list(filter(lambda n: n is not None, self.active_notes)))
        if encoder_switch and notes_active == 0:
            self.switch_progression(encoder_position - encoder_last_position)
        elif notes_active == 0:
            self.switch_key(encoder_position - encoder_last_position)
        else:
            self.pitch_bend = (self.pitch_bend + ((encoder_position - encoder_last_position) * 400)) % 16383
            self.macropad.midi.send(self.macropad.PitchBend(self.pitch_bend))

    def sleep_event(self):
        self.pixels.sleep()
        self.display.sleep()

    def switch_progression(self, position_change):
        self.progression_idx = (self.progression_idx + position_change) % len(self.settings.chords['progressions'])
        name, progression, scale_name, mode = self.settings.chords['progressions'][self.progression_idx]
        self.key.set_scale(self.find_scale(scale_name), mode)
        self.chords = self.key.chords(progression)
        self.pixels.set_progression(progression)
        self.display.set_progression(name, progression)

    def switch_key(self, position_change):
        self.key.advance(position_change)
        name, progression, scale_name, mode = self.settings.chords['progressions'][self.progression_idx]
        self.key.set_scale(self.find_scale(scale_name), mode)
        self.chords = self.key.chords(progression)
        self.pixels.wake()
        self.display.set_key(self.key)

    def find_scale(self, name):
        _, scale = next(filter(lambda s: s[0] == name, self.settings.keys['scale_degrees']))
        return scale

class Display:
    def __init__(self, macropad, brightness):
        self.display = macropad.display
        self.scaled_brightness = 0.5 + (brightness * 0.5)
        self.group = displayio.Group()
        self.group.append(Rect(0, 0, self.display.width, 12, fill=0xFFFFFF))
        self.group.append(Display.create_label('Macropad 4chord MIDI', (self.display.width//2, -1), (0.5, 0.0), 0x000000))
        self.group.append(Display.create_label("Key:", (0, self.display.height - 36), (0, 1.0)))
        self.group.append(Display.create_label("X#", (30, self.display.height - 36), (0, 1.0)))
        self.group.append(Display.create_label("Oct:", (self.display.width / 2, self.display.height - 36), (0, 1.0)))
        self.group.append(Display.create_label("00", ((self.display.width / 2) + 30, self.display.height - 36), (0, 1.0)))
        self.group.append(Display.create_label("Chords:", (0, self.display.height - 22), (0, 1.0)))
        self.group.append(Display.create_label("", (42, self.display.height - 22), (0, 1.0)))
        self.group.append(Display.create_label("Triad Mode", (0, self.display.height - 8), (0, 1.0)))
        self.group.append(Display.create_label("", (40, self.display.height - 8), (0, 1.0)))

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
        self.display.brightness = self.scaled_brightness
        self.display.root_group = self.group
        self.display.refresh()

    def wake(self):
        if self.display.brightness <= 0:
            self.display.brightness = self.scaled_brightness
            self.display.refresh()

    def sleep(self):
        self.display.brightness = 0
        self.display.refresh()

    def set_progression(self, name, progression):
        self.wake()
        self.group[1].text = name
        self.group[7].text = ' '.join(progression)
        self.display.refresh()

    def set_key(self, key):
        self.wake()
        self.group[3].text = key.key
        self.group[5].text = str(key.octave)
        self.display.refresh()

    def set_welcome(self, text):
        self.group[8].text = text if text else ''
        
    def set_playing(self, notes):
        self.wake()
        note_names = [Key.to_name(note) for note in notes if note is not None]
        self.group[8].text = 'Notes:'
        self.group[9].text = ' '.join(note_names)
        self.display.refresh()

SEGMENT_SIZE = 255 // 7
SUBSEGMENT_SIZE = SEGMENT_SIZE // 3

class Pixels:
    def __init__(self, macropad, brightness):
        self.pixels = macropad.pixels
        self.brightness = brightness

    def refresh(self):
        self.pixels.auto_write = False
        self.pixels.brightness = self.brightness
        self.palette = [0x0F0F0F for i in range(12)]
        self.reset()

    def wake(self):
        if self.pixels.brightness <= 0:
            self.pixels.brightness = self.brightness
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
            self.pixels[index] = 0xFFFFFF if active_notes[index] is not None else self.palette[index]
        self.pixels.show()

    def reset(self):
        self.wake()
        for index in range(12):
            self.pixels[index] = self.palette[index]
        self.pixels.show()
