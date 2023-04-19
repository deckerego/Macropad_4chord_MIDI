import board
import digitalio
import storage

# Mount the CIRCUITPY drive as read-only unless the encoder switch is held down
encoder_switch = digitalio.DigitalInOut(board.BUTTON)
encoder_switch.switch_to_input(pull=digitalio.Pull.UP)
if(encoder_switch.value):
    print("Storage Disabled")
    storage.disable_usb_drive()
else:
    print("Enabling Updates")
