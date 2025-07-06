class Equipment:
    _instance = None

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

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Удаляю строку создания глобального экземпляра, если есть