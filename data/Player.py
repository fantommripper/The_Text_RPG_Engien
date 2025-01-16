class Player:
    def __init__(self):
        self.name = "NULL"
        self.heroClass = "NULL"
        self.Dm = 10
        self.Hp = 70
        self.maxHp = 70
        self.gold = 0
        self.Xp = 0
        self.XpToLv = 50
        self.Lv = 0
        self.improvementStar = 0
        self.points = 0
        self.layer = 1
        self.playerMap = True
        self.playerMonstronomicon = False
        self.Px = 0
        self.Py = 0
        self.Effects = []
        self.mana = 50
        self.maxMana = 50
        self.speed = 1
        self.item = []
        self.helmet = ""
        self.chestplate = ""
        self.weapon = ""
        self.weapon2 = ""
        self.luck = 0
        self.spells = [0]
        self.maxGoWeight = 100
        self.goWeight = 0

player = Player()