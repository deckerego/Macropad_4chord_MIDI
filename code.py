import settings
import time
from key import Key
from adafruit_macropad import MacroPad
from pixels import Pixels
from display import Display

macropad = MacroPad()
display = Display(macropad)
pixels = Pixels(macropad)

key = Key(settings.conf['keys'][0], 4)
chords = None
progression = settings.conf['progressions'][0]
note_velocity = settings.conf['velocity']
active_notes = [None for i in range(12)]
encoder_last_position = 0
last_time_seconds = time.time()
sleep_seconds = settings.conf['sleep_seconds']

def elapsed_seconds():
    global last_time_seconds
    current_seconds = time.time()
    elapsed_seconds = current_seconds - last_time_seconds
    last_time_seconds = current_seconds
    return elapsed_seconds

def keypad_events(events):
    global active_notes

    # Send as many MIDI operations as you can at once
    for event in events:
        if event.pressed:
            row = event.key_number // 3
            column = event.key_number % 3
            note = chords[row][column]
            macropad.midi.send(macropad.NoteOn(note, note_velocity))
            active_notes[event.key_number] = note

        else: # event.released
            note = active_notes[event.key_number]
            macropad.midi.send(macropad.NoteOff(note, 0))
            active_notes[event.key_number] = None

    display.set_playing(active_notes)
    pixels.set_playing(active_notes)

def switch_progression(position):
    global progression, chords
    index = position % len(settings.conf['progressions'])
    progression = settings.conf['progressions'][index]
    chords = key.chords(progression)
    pixels.set_progression(progression)
    display.set_progression(progression)

def switch_key(position_change):
    global key, chords
    if position_change:
        key = key.advance(position_change)
    else: # No change - reset to default
        key = Key(settings.conf['keys'][0], 4)
    chords = key.chords(progression)
    pixels.wake()
    display.set_key(key)

def sleep_event():
    pixels.sleep()
    display.sleep()

switch_progression(encoder_last_position)
switch_key(encoder_last_position)
keypad_events([])

while True:
    # Process all available key events at once
    key_events = []
    key_event = macropad.keys.events.get()
    while key_event:
        key_events.append(key_event)
        key_event = macropad.keys.events.get()
    if key_events:
        keypad_events(key_events)
        sleep_seconds = settings.conf['sleep_seconds']

    # See if the encoder dial has rotated
    encoder_position = macropad.encoder
    if encoder_position != encoder_last_position:
        encoder_switch = macropad.encoder_switch
        if encoder_switch: # The encoder button is pushed down
            switch_progression(encoder_position)
        else: # The encoder button is not pressed
            switch_key(encoder_position - encoder_last_position)
        encoder_last_position = encoder_position
        sleep_seconds = settings.conf['sleep_seconds']

    # Let the keypad go dark if it has timed out
    if sleep_seconds: # Always on if None
        sleep_seconds -= elapsed_seconds()
        if sleep_seconds <= 0: sleep_event()
