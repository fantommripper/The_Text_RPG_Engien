class Resistances:
    _instance = None

    def __init__(self):
        self.MagicResistInt = -0.8
        self.PhysicalResistInt = -0.8
        self.PoisonResistInt = -0.8
        self.ToxinResistInt = -0.8
        self.helmetResistInt = 0
        self.chestplateResistInt = 0
        self.shieldResistInt = 0
        self.MagicPhysicalResistInt = 0

    def to_dict(self):
        return {
            'MagicResistInt': self.MagicResistInt,
            'PhysicalResistInt': self.PhysicalResistInt,
            'PoisonResistInt': self.PoisonResistInt,
            'ToxinResistInt': self.ToxinResistInt,
            'helmetResistInt': self.helmetResistInt,
            'chestplateResistInt': self.chestplateResistInt,
            'shieldResistInt': self.shieldResistInt,
            'MagicPhysicalResistInt': self.MagicPhysicalResistInt,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['MagicResistInt'],
            data['PhysicalResistInt'],
            data['PoisonResistInt'],
            data['ToxinResistInt'],
            data['helmetResistInt'],
            data['chestplateResistInt'],
            data['shieldResistInt'],
            data['MagicPhysicalResistInt'],
        )

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance