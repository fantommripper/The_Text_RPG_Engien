class Config:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.delayOutput = 0.02
        self.language = "en"
        self.anim = True
        self.loading = 0
        self.cheats = True

    def to_dict(self):
        return {
            'delayOutput': self.delayOutput,
            'language': self.language,
            'anim': self.anim,
            'loading': self.loading,
            'cheats': self.cheats
        }

    def from_dict(self, data):
        self.delayOutput = data['delayOutput']
        self.language = data['language']
        self.anim = data['anim']
        self.loading = data['loading']
        self.cheats = data['cheats']



config = Config.get_instance()