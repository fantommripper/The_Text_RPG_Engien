class Ability:
    _instance = None

    def __init__(self):
        self.DoublePunch = False
        self.ManaRecovery = False
        self.EarningCoinsAndXP = False

    def to_dict(self):
        return {
            'DoublePunch': self.DoublePunch,
            'ManaRecovery': self.ManaRecovery,
            'EarningCoinsAndXP': self.EarningCoinsAndXP
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['DoublePunch'], data['ManaRecovery'], data['EarningCoinsAndXP'])

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance