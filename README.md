# Macropad 4chord MIDI

[![Macropad 4chord MIDI](https://github.com/deckerego/Macropad_4chord_MIDI/actions/workflows/pullrequest-unittest.yml/badge.svg)](https://github.com/deckerego/Macropad_4chord_MIDI/actions/workflows/pullrequest-unittest.yml)

## Contents

* **[About the Macropad 4chord MIDI](#about)**
* **[Playing Harmonies, Melodies, and Rhythms](#playing)**
* **[Installing on an Adafruit Macropad](#installing)**
* **[Updating an Existing Installation](#updating)**
* **[How to configure progressions, drum kits, MIDI settings](#configuring)**
* **[Building & Testing This Project](#building)**

## About

> "All the greatest hits from the past forty years just use four chords. Same four chords for every song. It's dead simple to write a pop hit."
 -- Benny, Axis of Awesome

A four-chord MIDI device that allows you to rapidly churn out catchy tunes.
Set your root key & chord progression, then off you go. Includes drum pads
so you can provide a backing beat to your tracks.

Huge thanks to so many who have inspired this idea, especially:
- [Sven Gregori](https://github.com/sgreg) and his [4 Chord USB MIDI Keyboard](https://hackaday.io/project/26078-4chord-midi)
- Paul David's [The Four Chord Song](https://youtu.be/6U8-Y7DEzOE) music theory video
- [iSongs' Take On Me with iOS' GarageBand](https://youtu.be/U3aiBukp_E4)
- The [Omnichord System Two](https://suzukimusic-global.com/products_single.php?parent_cate_cd=3&products_cate_cd=34&products_cd=315)
- The [Yamaha QY20](https://soundprogramming.net/sequencers/yamaha/yamaha-qy20/)
- Roland's [TR-808, TB-303, and SH-101](https://roland50.studio/)
- ...and of course [Axis of Awesome's Four Chord Song](https://youtu.be/5pidokakU4I)

Would you like to learn more about music theory and music composition? May I recommend:
- Andrew Huang's [learn music theory in half an hour](https://youtu.be/rgaTLrZGlk0) video
- Nice Stick's [Bon! Music](https://nicestick.io/) beginner guide to music composition
- [ArcAttach](https://youtu.be/d2OsF86fcKQ) and their [StringTheory project](https://arcattack.com/stringtheory/)
- Goodhertz' [Funklet](https://goodhertz.com/funklet/)
- Mike Hadlow's [Guitar Dashboard](https://guitardashboard.com/)


## Playing

The Macropad 4chord MIDI is built to play simple chord progressions, follow scales to build
melodies, and act as a drum kit as a MIDI device. You can connect the Macropad to any studio 
recording software or DAW accepts MIDI devices, such as GarageBand or Abelton Live.

The 4chord MIDI has five different modes: a "harmony" mode that allows you to select 
progressions and root keys to play chords, the "autochord" mode that lets you play an
entire chord with a single key (like the sequencers of the 80's and 90's), a "melody" 
mode that highlights different scales you can play, a "rhythm" mode that
allows you to use the MacroPad as an acoustic drum / electric drum /
percussion pad, and the "MIDI controls" mode that lets you set MIDI command
controls (including note velocity). You can switch between each mode by
clicking on the rotary dial.

There are a few quick demos showing how to use the MacroPad 4chord MIDI in a DAW:
* GarageBand: https://youtu.be/goyia2EYv0Q
* Renoise: https://youtu.be/5VwU2DpjD-4
* Zenbeats Mobile: https://youtu.be/n5oL5MZPpwQ
* Hookpad: https://youtu.be/Ifc-n-RV3Ag

![Switching between triad, autochord, melody, drum pad, and MIDI settings modes](./docs/images/modes.gif)

### Chord Keyboard (Triad Mode)

Once you power on the Macropad a default progression is loaded into "Triad Mode", 
with the root on middle C (I'm a assuming middle C is on the third octave). 
The root note is at the top left, with the major (or minor) third and 
perfect fifth on the middle and right keys. The key and octave can be changed 
by rotating the encoder dial, going up or down the chromatic scale.

As you go down the keypad, the notes follow the four chord progression listed
on the screen. By default this is a I-V-vi-IV progression, so with the root
at C3 you will have G3, A3, and F3 as you go down the keypad. You can rotate
through some four chord progressions by pressing down on the encoder button
while rotating the dial.

Thanks to the RP2040, all the keys can be pressed simultaneously. You can
play the triad chords for each degree, or arpeggiate the chords however
you like. The list of notes currently being played are displayed on screen
if you want to check my math.

You can bend the current notes being played by rotating the dial while keys
are being held down. Rotating counter-clockwise will bend the pitch down,
rotating clockwise will bend the pitch up.

### AutoChord Mode

Clicking once on the rotary dial after the Macropad boots loads the
"AutoChord" mode. In this mode each button does **not** correspond to
a note, instead each button corresponds to a _chord_.

This mode does load a chord progression just as the previous "Triad Mode"
does, however each combination of keys you press in a row corresponds to a
different type of cord. The map is:

| Key 1 | Key 2 | Key 3 | Chord Type         |
|-------|-------|-------|--------------------|
| Press |       |       | Major Chord        |
|       | Press |       | Minor Chord        |
|       |       | Press | Dominant 7th Chord |
| Press |       | Press | Major 7th Chord    |
|       | Press | Press | Minor 7th Chord    |
| Press | Press |       | Diminshed Chord    |
| Press | Press | Press | Augmented Chord    |

Each chord also has an accompanying bass chord, where the 1st
and 5th one octave lower are played alongside the chord. This can be
configured to be just the root, or the 3rd, or disabled entirely 
in `settings.py`.

AutoChord mode also allows you to arpeggiate chords, so that there is a
slight delay between each note as it is played. This works well with
guitar voices, since it provides a more realistic strum-like effect. This
can be configured within the [MIDI Controls](#midi-controls) configuration
screen, and defaults can be configured within `settings.py`.

### Highlight Scales (Melody Mode)

Clicking again on the rotary dial brings up a keyboard where a selected
scale is highlighted on the keypad so you can type out a melody.
Each of the 12 buttons on the Macropad will correspond to a note on the 
chromatic scale, with the root note you have selected in the top left. 

The buttons that are illuminated correspond to the scale selected while
in this mode. You can play as many notes as you wish simultaneously,
however only the highlighted notes are part of the selected scale.
To change to a different scale (pentatonic major, relative minor, 
blues major, etc.) press down on the encoder button and rotate the dial.
The name and first seven notes of the scale will be shown on the display.

Just as when playing chord progressions, you can bend the current notes 
being played by rotating the dial while keys are being held down. 
Rotating counter-clockwise will bend the pitch down, rotating clockwise 
will bend the pitch up.

### Drum Pads

If you click three times on the rotary dial after the Macropad boots, it will move
into the drum pad mode. Rotating the dial will allow you to select from
a number of drum or percussion presets where MIDI notes match an acoustic drum,
a rhythm composer (such as the classic TR-808), or percussion strikes.
Actual percussion sounds depend on the MIDI controller or DAW you are using,
so you may need to make some [configuration tweaks](#configuring)
with the MIDI mapping to match what instrument you want to use.

### MIDI Controls

Clicking four times after booting the Macropad will take you into the MIDI controls
mode, where you can adjust MIDI controls that are transferred to your DAW
when recording. This includes global settings (such as attack or release time)
as well as note settings (such as velocity). The AutoChord setting that
allows you to arpeggiate a chord is also listed here.

Bear in mind that not all DAWs will register MIDI commands from devices in the
same way. Some DAWs register the commands so long as your device is connected,
others will not register any commands until you begin recording. If you find
that your DAW isn't picking up the values you set, start recording while the
"MIDI Controls" mode is showing on the Macropad, then single-click to return
to the chords mode immediately after. This will re-send all the MIDI commands
to your DAW.


## Installing

First make sure that your Macropad has the
[latest version of CircuitPython 10.0.x installed](https://circuitpython.org/board/adafruit_macropad_rp2040/).
See [https://learn.adafruit.com/adafruit-macropad-rp2040/circuitpython](https://learn.adafruit.com/adafruit-macropad-rp2040/circuitpython)
for instructions on how to update the Macropad to have the latest version of
CircuitPython.

When installing the Macropad 4chord for the first time, extract the latest
[MacroPad 4chord MIDI.zip](https://github.com/deckerego/Macropad_4chord_MIDI/releases/latest)
into a directory, then copy the contents of that extracted archive
into the CIRCUITPY drive that appears when you plug in your Macropad.
Ensure that the contents of the `lib/` subdirectory are also copied - these are
the precompiled Adafruit libraries that power the Macropad.


## Updating

After you first install this version of Macropad 4chord MIDI and reboot,
the Macropad will no longer mount as a removable drive. This ensures that 
Windows and MacOS won't complain if you unplug or reboot the device, 
making it behave more like pure MIDI device. This also helps mobile devices
as well, as sometimes Android can't tell if the Macropad 4chord MIDI is
a input device, a flash drive, or a MIDI keyboard.

To update or edit the code on the device, or to modify the settings, you first
need to reboot the device with the Macropad's drive mounted in read/write mode.
To do that, reboot the device using the boot switch on the left of the
Macropad, and then after releasing the button immediately hold down the
blinking top-left key on the keypad (KEY1). You should see the text "Enabling Updates" 
quickly appear on the screen, and then a removable drive will mount in read/write 
mode that contains some documentation and the Macropad's CircuitPython code.

## Configuring

The `settings.py` file has several settings you can tweak, including
MIDI note configurations, MIDI channel settings, and a list of the progressions 
you can scroll through. If you would like to add your own chord progressions or 
would like to keep a shorter list of possible keys, you can make those changes 
in the `settings.py` file within the CIRCUITPY drive. Just make sure to mount 
your Macropad in read/write mode (see [Updating](#updating)).


## Building

There is no build process since the Python files are distributed in
.py form and are not compiled to Micropython. All files are packaged as-is.

### Packaging

The necessary Adafruit CircuitPython libraries are provided in the
releases package but not included in the Git repository for obvious reasons.
If you are installing from this repo directly, review
[lib/README.md](./lib/README.md) for details on how to add the
necessary libraries.

### Unit Testing

Unit testing can be run with:

    python3 -m unittest discover
