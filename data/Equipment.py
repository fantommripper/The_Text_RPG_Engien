class Equipment:
    def __init__(self):
        self.helmetID = None
        self.chestplateID = None
        self.weaponID = None
        self.weapon2ID = None

    def to_dict(self):
        return {
            'helmetID': self.helmetID,
            'chestplateID': self.chestplateID,
            'weaponID': self.weaponID,
            'weapon2ID': self.weapon2ID
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['helmetID'],
            data['chestplateID'],
            data['weaponID'],
            data['weapon2ID']
        )


equipment = Equipment()