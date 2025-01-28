class Config:
    def __init__(self):
        self.delayOutput = 0.02
        self.language = "EN"
        self.anim = True
        self.loading = 0

    def to_dict(self):
        return {
            'delayOutput': self.delayOutput,
            'language': self.language,
            'anim': self.anim,
            'loading': self.loading
        }

    def from_dict(self, data):
        self.delayOutput = data['delayOutput']
        self.language = data['language']
        self.anim = data['anim']
        self.loading = data['loading']



config = Config()