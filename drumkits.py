class DrumKits:
    def __init__(self):
        self.index = 0
        self.names = [
            "Acoustic Drum Kit",
            "Electric Drum Kit",
            "Percussion",
        ]
        self.kits = [
            [
                [(0x544408, 'CrashC',  49), (0x544408, 'HatCls',  42), (0x544408, 'HatOpn',  46)],
                [(0x04541B, 'XStick',  37), (0x095E06, 'Snare',   38), (0x04541B, 'SnrRod',  91)],
                [(0x000754, 'FlorTom', 43), (0x000754, 'LowTom',  45), (0x000754, 'HiTom',   50)],
                [(0x540908, 'Bass',    35), (0x540908, 'Kick',    36), (0x04541B, 'Cowbell', 56)]
            ],
            [
                [(0x544408, 'CrashC',  49), (0x544408, 'HatCls',  42), (0x544408, 'HatOpn',  46)],
                [(0x095E06, 'Snare',   38), (0x095E06, 'ESnare',  40), (0x095E06, 'XStick',  37)],
                [(0x000754, 'Tom1',    41), (0x000754, 'Tom2',    43), (0x000754, 'LTom',    45)],
                [(0x04541B, 'Clap',    39), (0x540908, 'Kick',    36), (0x04541B, 'Cowbell', 47)]
            ],
            [
                [(0x544408, 'Bells',   59), (0x544408, 'Claves',  75), (0x544408, 'Maraca',  70)],
                [(0x095E06, 'HBongo',  60), (0x000754, 'Conga',   63), (0x04541B, 'HTimbl',  65)],
                [(0x095E06, 'LBongo',  61), (0x000754, 'CongaD',  62), (0x04541B, 'LTimbl',  66)],
                [(0x540908, 'Stomp',   57), (0x540908, 'Wdblck',  77), (0x540908, 'Snap', 58)]
            ]
        ]

    def get(self):
        return self.names[self.index], self.kits[self.index]

    def next(self):
        self.index = (self.index + 1) % len(self.kits)
        return self.get()

    def prev(self):
        self.index = self.index - 1 if self.index > 0 else len(self.kits) - 1
        return self.get()
