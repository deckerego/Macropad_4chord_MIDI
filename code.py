import settings
import time
from adafruit_macropad import MacroPad
from chords import Chords
from drums import Drums
from controls import Controls

macropad = MacroPad()
modes = [Chords(macropad), Drums(macropad), Controls(macropad)]
mode_current = 0

encoder_last_position = 0
encoder_last_down = False
encoder_last_pressed = 0
last_time_seconds = time.time()
sleep_seconds = settings.conf['sleep_seconds']

def elapsed_seconds():
    global last_time_seconds
    current_seconds = time.time()
    elapsed_seconds = current_seconds - last_time_seconds
    last_time_seconds = current_seconds
    return elapsed_seconds

def click_event():
    global mode_current
    mode_current = (mode_current + 1) % 3
    modes[mode_current].refresh()

modes[mode_current].refresh()
while True:
    # Process all available key events at once
    key_events = []
    key_event = macropad.keys.events.get()
    while key_event:
        key_events.append(key_event)
        key_event = macropad.keys.events.get()
    if key_events:
        modes[mode_current].keypad_events(key_events)
        sleep_seconds = settings.conf['sleep_seconds']

    if macropad.encoder_switch != encoder_last_down:
        if not macropad.encoder_switch and encoder_last_pressed > 0:
            click_event()
        encoder_last_down = macropad.encoder_switch
        encoder_last_pressed = time.time() if macropad.encoder_switch else 0
        sleep_seconds = settings.conf['sleep_seconds']
    elif macropad.encoder != encoder_last_position:
        modes[mode_current].rotate_event(macropad.encoder, encoder_last_position, macropad.encoder_switch);
        encoder_last_position = macropad.encoder
        encoder_last_pressed = 0
        sleep_seconds = settings.conf['sleep_seconds']

    # Let the keypad go dark if it has timed out
    if sleep_seconds: # Always on if None
        sleep_seconds -= elapsed_seconds()
        if sleep_seconds <= 0: modes[mode_current].sleep_event()
