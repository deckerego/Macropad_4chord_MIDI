import time
from settings import Settings
from adafruit_macropad import MacroPad

from chords import Chords
from autochords import AutoChords
from scales import Scales
from drums import Drums
from controls import Controls

macropad = MacroPad()
settings = Settings()
modes = []
mode_current = Chords(macropad)
mode_current_idx = 0
encoder_last_position = 0
encoder_last_down = False
encoder_last_pressed = 0
last_time_seconds = time.monotonic()

modes.append(Chords)
modes.append(AutoChords)
modes.append(Scales)
modes.append(Drums)
modes.append(Controls)

sleep_seconds = settings.display['sleep_seconds']
sleep_active = False

# Seconds (floating) since last invocation
def elapsed_seconds():
    global last_time_seconds
    current_seconds = time.monotonic()
    elapsed_seconds = current_seconds - last_time_seconds
    last_time_seconds = current_seconds
    return elapsed_seconds

# The current mode has changed, update the MacroPad
def refresh():
    global mode_current
    if hasattr(mode_current, 'channel'): 
        macropad.midi.out_channel = mode_current.channel
    mode_current.refresh()

# A click occurs when the dial is pressed ONLY (no rotation or keypress)
def click_event():
    global macropad, mode_current, mode_current_idx
    mode_current_idx = (mode_current_idx + 1) % len(modes)
    del mode_current
    mode_current = modes[mode_current_idx](macropad)
    refresh()

def wake_event():
    global sleep_seconds, sleep_active
    sleep_seconds = settings.display['sleep_seconds']
    sleep_active = False

def sleep_event():
    global sleep_active
    mode_current.sleep_event()
    sleep_active = True


refresh()
while True:
    # Process all available key events at once
    key_events = []
    key_event = macropad.keys.events.get()
    while key_event:
        key_events.append(key_event)
        key_event = macropad.keys.events.get()
    if key_events:
        mode_current.keypad_events(key_events)
        wake_event()

    if macropad.encoder_switch != encoder_last_down:
        if not macropad.encoder_switch and encoder_last_pressed > 0:
            click_event()
        encoder_last_down = macropad.encoder_switch
        encoder_last_pressed = time.time() if macropad.encoder_switch else 0
        wake_event()
    elif macropad.encoder != encoder_last_position:
        mode_current.rotate_event(macropad.encoder, encoder_last_position, macropad.encoder_switch);
        encoder_last_position = macropad.encoder
        encoder_last_pressed = 0
        wake_event()
    
    elapsed = elapsed_seconds()
    if hasattr(mode_current, 'tick') and not sleep_active: 
        mode_current.tick(elapsed)

    if sleep_seconds:
        sleep_seconds -= elapsed
        if not sleep_active and sleep_seconds <= 0: 
            sleep_event()

    if sleep_active: time.sleep(1.0)
