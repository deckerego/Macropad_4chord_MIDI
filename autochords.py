import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from rainbowio import colorwheel
from key import Key
from settings import Settings

class AutoChords:
    LATCH_TIME = 0.05

    def __init__(self, macropad):
        self.settings = Settings()
        self.display = Display(macropad, self.settings.display['brightness'])
        self.pixels = Pixels(macropad, self.settings.display['brightness'])
        self.macropad = macropad
        self.key = Key()
        self.roots = None
        self.masks_live = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.masks_buffer = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.latch_time = None
        self.progression_idx = 0
        self.pitch_bend = 8192
        self.channel = self.settings.chords['channel']

    def refresh(self):
        self.active_notes = [None for i in range(12)]
        self.display.refresh()
        self.pixels.refresh()
        self.switch_progression(0)
        self.switch_key(0)

    def tick(self, elapsed_seconds):
        if self.latch_time: # Latch keypresses to "debounce" them
            self.latch_time = self.latch_time - elapsed_seconds
            if self.latch_time <= 0:
                self.mask_flip()
                self.pixels.set_playing(self.masks_live)
                self.latch_time = None

    def mask_flip(self):
        for row in range(4):
            mask_live = self.masks_live[row]
            mask_buffer = self.masks_buffer[row]
            if mask_live != mask_buffer:
                self.send_command(self.macropad.NoteOff, self.roots[row], mask_live)
                self.send_command(self.macropad.NoteOn, self.roots[row], mask_buffer)
            self.masks_live[row] = self.masks_buffer[row].copy()

    def keypad_events(self, events):
        for event in events:
            row = event.key_number // 3
            column = event.key_number % 3
            self.masks_buffer[row][column] = 1 if event.pressed else 0
            if not self.latch_time: self.latch_time = AutoChords.LATCH_TIME

    def send_command(self, command, root, mask):
        note_velocity = self.settings.midi['Velocity']
        enum = 0

        for col, state in enumerate(mask):
            enum += state << col
        name, chord = self.to_chord(root, enum)
        bassline = Key.to_bassline(chord)

        for note in chord + bassline:
            self.macropad.midi.send(command(note, note_velocity, channel=self.channel))
            
        self.display.set_playing(name, chord)

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
        self.roots = [chord[0] for chord in self.key.chords(progression)]
        self.pixels.set_progression(progression)
        self.display.set_progression(name, progression)

    def switch_key(self, position_change):
        self.key.advance(position_change)
        name, progression, scale_name, mode = self.settings.chords['progressions'][self.progression_idx]
        self.key.set_scale(self.find_scale(scale_name), mode)
        self.roots = [chord[0] for chord in self.key.chords(progression)]
        self.pixels.wake()
        self.display.set_key(self.key)

    def find_scale(self, name):
        _, scale = next(filter(lambda s: s[0] == name, self.settings.keys['scale_degrees']))
        return scale

    def to_chord(self, root, enum):
        key = Key(scale=self.key.scale, mode=self.key.mode, number=root)
        note = Key.to_note(root)
        if   enum == 0: return None, []
        elif enum == 4: return '%s7' % note, key.chord_seventh()
        elif enum == 2: return '%sm' % note, key.chord_minor()
        elif enum == 6: return '%sm7' % note, key.chord_seventh_min()
        elif enum == 1: return '%s' % note, key.chord_major()
        elif enum == 5: return '%smaj7' % note, key.chord_seventh_maj()
        elif enum == 3: return '%sdim' % note, key.chord_diminished()
        elif enum == 7: return '%saug' % note, key.chord_augmented()

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
        self.group.append(Display.create_label("AutoChord Mode", (0, self.display.height - 8), (0, 1.0)))
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
        self.display.show(self.group)
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

    def set_playing(self, name, notes):
        self.wake()
        self.group[8].text = '%s: ' % name if name else ''
        note_names = [Key.to_name(note) for note in notes if note is not None]
        self.group[9].text = ' '.join(note_names)
        self.display.refresh()

SEGMENT_SIZE = 255 // 7
SUBSEGMENT_SIZE = (SEGMENT_SIZE // 3) * 2

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

                if column == 1 and progression[row].islower(): # Highlight minor key
                    self.palette[(row * 3) + column] = colorwheel(segment + SUBSEGMENT_SIZE)
                elif column == 0 and progression[row].isupper(): # Highlight major key
                    self.palette[(row * 3) + column] = colorwheel(segment + SUBSEGMENT_SIZE)
                else:
                    self.palette[(row * 3) + column] = colorwheel(segment)
        self.reset()

    def set_playing(self, masks):
        self.wake()
        for row in range(4):
            for col in range(3):
                index = (row * 3) + col
                self.pixels[index] = 0xFFFFFF if masks[row][col] else self.palette[index]
        self.pixels.show()

    def reset(self):
        self.wake()
        for index in range(12):
            self.pixels[index] = self.palette[index]
        self.pixels.show()
