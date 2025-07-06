class Ability:
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


ability = Ability()