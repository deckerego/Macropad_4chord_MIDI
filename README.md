# Macropad 4chord MIDI

With thanks to the [4 Chord USB MIDI Keyboard](http://old.sgreg.fi//projects/4chord-midi)
by [Sven Gregori](http://old.sgreg.fi).


## Installing

When installing for the first time, extract the latest
[MacroPad 4chord MIDI.zip](https://github.com/deckerego/Macropad_4chord_MIDI/releases/latest)
into a directory, then copy the contents of that extracted archive
into the CIRCUITPY drive that appears when you plug in your Macropad.
Ensure that the contents of the `lib/` subdirectory are also copied - these are
the precompiled Adafruit libraries that power the Macropad.


## Updating

After you first install this version of Macropad 4chord MIDI and reboot the Macropad,
the CIRCUITPY filesystem will be mounted as read-only. When mounting the device
as read-only, Windows and MacOS won't complain if you unplug or reboot the device
without unmounting it, making it more like a regular old HID device.

To update or edit the code on the device, or to modify the macros, you first
need to reboot the device with the CIRCUITPY drive mounted in read/write mode.
To do that, reboot the device using the boot switch on the left of the
Macropad, and then after releasing the button immediately hold down the
rotary encoder button. You should see the text "Mounting Read/Write" quickly
appear on the screen, and then the CIRCUITPY drive will mount in read/write mode.


## Playing

The Macropad 4chord MIDI is built to play simple chord progressions as a MIDI
device. You can connect the Macropad to any studio recording software that
accepts MIDI devices, such as GarageBand.

Once you power on the Macropad a default progression is restored, with the root
on middle C (I'm a assuming middle C is on the fourth octave). The root note
is at the top left, with the major (or minor) third and perfect fifth on the
middle and right keys. The key and octave can be changed by rotating the
encoder dial, going up or down the chromatic scale.

As you go down the keypad, the notes follow the four chord progression listed
on the screen. By default this is a I-V-vi-IV progression, so with the root
at C4 you will have G4, A5, and F4 as you go down the keypad. You can rotate
through some four chord progressions by pressing down on the encoder button
while rotating the dial.

Thanks to the RP2040, all the keys can be pressed simultaneously. You can
play the triad chords for each degree, or arpeggiate the chords however
you like. The list of notes currently being played are displayed on screen
if you want to check my math.


## Unit Testing

Unit testing can be run with:

    python3 -m unittest discover
