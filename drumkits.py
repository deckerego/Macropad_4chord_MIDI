class DrumKits:
    def __init__(self):
        self.index = 0
        self.names = [
            "Acoustic Drum Kit",
            "Electric Drum Kit",
        ]
        self.kits = [
            [
                [(0x544408, 'HatFot',  44), (0x544408, 'HatCls',  42), (0x544408, 'HatOpn',  46)],
                [(0x04541B, 'XStick',  37), (0x095E06, 'Snare',   38), (0x04541B, 'Rod',     91)],
                [(0x000754, 'FlorTom', 43), (0x000754, 'LowTom',  47), (0x000754, 'HiTom',   48)],
                [(0x540908, 'Bass',    35), (0x540908, 'Kick',    36), (0x04541B, 'Cowbell', 56)]
            ],
            [
                [(0x544408, 'HatFot',  44), (0x544408, 'CrashC',  49), (0x544408, 'RideCy',  51)],
                [(0x04541B, 'Clap',    39), (0x095E06, 'Snare',   40), (0x04541B, 'Rod',     91)],
                [(0x000754, 'FlorTom', 43), (0x000754, 'LowTom',  47), (0x000754, 'HiTom',   48)],
                [(0x540908, 'Bass',    36), (0x540908, 'Kick',    36), (0x04541B, 'VibSlap', 58)]
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
