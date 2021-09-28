import settings
from key import Key
from adafruit_macropad import MacroPad

macropad = MacroPad()
macropad.pixels.brightness = 0.1
macropad.pixels.fill(0x0F0F0F)

text_lines = macropad.display_text("Macropad 4chord MIDI")
text_lines[1].text = "Chords: "
text_lines[2].text = "Pressed: "
text_lines.show()

def key_pressed(event):
    global pressed_notes
    row = key_event.key_number // 3
    column = key_event.key_number % 3
    note = chords[row][column]

    if key_event.pressed:
        macropad.midi.send(macropad.NoteOn(note, settings.conf['velocity']))
        macropad.pixels[key_event.key_number] = 0x00FF00
        pressed_notes.append(note)

    if key_event.released:
        macropad.midi.send(macropad.NoteOff(note, 0))
        macropad.pixels[key_event.key_number] = 0x0F0F0F
        pressed_notes.remove(note)

    note_names = [Key.to_name(note) for note in pressed_notes]
    text_lines[2].text = "Pressed: " + ' '.join(note_names)

def switch_progression(position):
    global progression
    index = position % len(settings.conf['progressions'])
    progression = settings.conf['progressions'][index]
    text_lines[1].text = "Chords: " + ' '.join(progression)

def switch_key(position_change):
    global key, chords
    if position_change:
        key = key.advance(position_change)
    else: # No change - reset to default
        key = Key(settings.conf['keys'][0], 4)
    chords = [key.chord(degree) for degree in progression]
    text_lines[0].text = "Key: %s Oct: %i" % (key.key, key.octave)

key = None
chords = None
progression = None
encoder_last_position = 0
pressed_notes = []

switch_progression(encoder_last_position)
switch_key(encoder_last_position)

while True:
    encoder_switch = macropad.encoder_switch
    encoder_position = macropad.encoder
    if encoder_position != encoder_last_position:
        if encoder_switch: # Change progressions
            switch_progression(encoder_position)
        else: # Change key / octave
            switch_key(encoder_position - encoder_last_position)
            encoder_last_position = encoder_position

    key_event = macropad.keys.events.get()
    if key_event:
        key_pressed(key_event)
