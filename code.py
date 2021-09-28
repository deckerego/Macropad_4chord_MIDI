import settings
from key import Key
from adafruit_macropad import MacroPad
from pixels import Pixels
from display import Display

macropad = MacroPad()
display = Display(macropad)
pixels = Pixels(macropad)

key = None
chords = None
progression = None
active_notes = [None for i in range(12)]
encoder_last_position = 0

def key_pressed(event):
    global active_notes

    if event.pressed:
        row = event.key_number // 3
        column = event.key_number % 3
        note = chords[row][column]
        macropad.midi.send(macropad.NoteOn(note, settings.conf['velocity']))
        active_notes[event.key_number] = note
        pixels.highlight(event.key_number)

    if event.released:
        note = active_notes[event.key_number]
        macropad.midi.send(macropad.NoteOff(note, 0))
        active_notes[event.key_number] = None
        pixels.off(event.key_number)

    display.set_playing(active_notes)

def switch_progression(position):
    global progression
    index = position % len(settings.conf['progressions'])
    progression = settings.conf['progressions'][index]
    pixels.set_progression(progression)
    display.set_progression(progression)

def switch_key(position_change):
    global key, chords
    if position_change:
        key = key.advance(position_change)
    else: # No change - reset to default
        key = Key(settings.conf['keys'][0], 4)
    chords = [key.chord(degree) for degree in progression]
    display.set_key(key)

switch_progression(encoder_last_position)
switch_key(encoder_last_position)

while True:
    encoder_position = macropad.encoder
    if encoder_position != encoder_last_position:
        encoder_switch = macropad.encoder_switch
        if encoder_switch: # Change progressions
            switch_progression(encoder_position)
        else: # Change key / octave
            switch_key(encoder_position - encoder_last_position)
        encoder_last_position = encoder_position

    key_event = macropad.keys.events.get()
    if key_event:
        key_pressed(key_event)
