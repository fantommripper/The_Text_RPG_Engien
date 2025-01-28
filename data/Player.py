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

    def to_dict(self):
        return {
            "name" : self.name,
            "heroClass" : self.heroClass,
            "Dm" : self.Dm,
            "Hp" : self.Hp,
            "maxHp" : self.maxHp,
            "gold" : self.gold,
            "Xp" : self.Xp,
            "XpToLv" : self.XpToLv,
            "Lv" : self.Lv,
            "improvementStar" : self.improvementStar,
            "points" : self.points,
            "layer" : self.layer,
            "playerMap" : self.playerMap,
            "playerMonstronomicon" : self.playerMonstronomicon,
            "Px" : self.Px,
            "Py" : self.Py,
            "Effects" : self.Effects,
            "mana" : self.mana,
            "maxMana" : self.maxMana,
            "speed" : self.speed,
            "item" : self.item,
            "helmet" : self.helmet,
            "chestplate" : self.chestplate,
            "weapon" : self.weapon,
            "weapon2" : self.weapon2,
            "luck" : self.luck,
            "spells" : self.spells

        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['name'],
            data['heroClass'],
            data['Dm'],
            data['Hp'],
            data['maxHp'],
            data['gold'],
            data['Xp'],
            data['XpToLv'],
            data['Lv'],
            data['improvementStar'],
            data['points'],
            data['layer'],
            data['playerMap'],
            data['playerMonstronomicon'],
            data['Px'],
            data['Py'],
            data['Effects'],
            data['mana'],
            data['maxMana'],
            data['speed'],
            data['item'],
            data['helmet'],
            data['chestplate'],
            data['weapon'],
            data['weapon2'],
            data['luck'],
            data['spells']

        )


player = Player()