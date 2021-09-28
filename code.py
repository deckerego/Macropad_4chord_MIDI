import settings
from key import Key
from adafruit_macropad import MacroPad

macropad = MacroPad()
macropad.pixels.brightness = 0.1
macropad.pixels.fill(0x0F0F0F)

progression = settings.conf['progression']
text_lines = macropad.display_text("Macropad 4chord MIDI")
text_lines[1].text = "Chords: " + ' '.join(progression)
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
encoder_last_position = 0
pressed_notes = []

switch_key(encoder_last_position)

while True:
    position = macropad.encoder
    if position != encoder_last_position:
        switch_key(position - encoder_last_position)
        encoder_last_position = position

    key_event = macropad.keys.events.get()
    if key_event:
        key_pressed(key_event)
