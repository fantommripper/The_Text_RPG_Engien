from .races import AVAILABLE_RACES, Race
from .classes import AVAILABLE_CLASSES, HeroClass
from .Effects import Effects
from .Item import Item
from .Spells import Spells

from typing import List

class Player:
    def __init__(self):
        self.name = "NULL"
        self._race: Race | None = None
        self._class: HeroClass | None = None
        
        # Base stats
        self.Dm:int = 10
        self.Hp:int = 70
        self.maxHp:int = 70
        self.gold:int = 0
        self.Xp:int = 0
        self.XpToLv:int = 50
        self.Lv:int = 0
        self.improvementStar:int = 0
        self.points:int = 0
        self.layer:int = 1
        self.playerMap:bool = True
        self.playerMonstronomicon:bool = False
        self.Px:int = 0
        self.Py:int = 0
        self.Effects:List[Effects] = []
        self.mana:int = 50
        self.maxMana:int = 50
        self.speed:int = 1
        self.item:List[Item] = []
        self.helmet:str = ""
        self.chestplate:str = ""
        self.weapon:str = ""
        self.weapon2:str = ""
        self.luck:int = 0
        self.spells:List[Spells] = []

    def set_name(self, name):
        self.name = name

    def set_class(self, hero_class_name: str):
        if hero_class_name not in AVAILABLE_CLASSES:
            raise ValueError(f"Invalid hero class: {hero_class_name}. Choose from {list(AVAILABLE_CLASSES.keys())}.")

        self._class = AVAILABLE_CLASSES[hero_class_name]()
        modifiers = self._class.stat_modifiers

        self.Dm += modifiers["Dm"]
        self.Hp += modifiers["Hp"]
        self.maxHp += modifiers["maxHp"]
        self.maxMana += modifiers["maxMana"]
        self.mana += modifiers["mana"]
        self.speed += modifiers["speed"]

    def set_race(self, race_name: str):
        if race_name not in AVAILABLE_RACES:
            raise ValueError(f"Invalid hero race: {race_name}. Choose from {list(AVAILABLE_RACES.keys())}.")

        self._race = AVAILABLE_RACES[race_name]()
        stats = self._race.base_stats

        self.Dm = stats["Dm"]
        self.Hp = stats["Hp"]
        self.maxHp = stats["maxHp"]
        self.speed = stats["speed"]
        self.maxMana = stats["maxMana"]
        self.mana = stats["mana"]

    @property
    def heroClass(self):
        return self._class.name if self._class else "NULL"

    @property
    def heroRace(self):
        return self._race.name if self._race else "NULL"

    def to_dict(self):
        return {
            "name": self.name,
            "heroClass": self.heroClass,
            "heroRace": self.heroRace,
            "Dm": self.Dm,
            "Hp": self.Hp,
            "maxHp": self.maxHp,
            "gold": self.gold,
            "Xp": self.Xp,
            "XpToLv": self.XpToLv,
            "Lv": self.Lv,
            "improvementStar": self.improvementStar,
            "points": self.points,
            "layer": self.layer,
            "playerMap": self.playerMap,
            "playerMonstronomicon": self.playerMonstronomicon,
            "Px": self.Px,
            "Py": self.Py,
            "Effects": self.Effects,
            "mana": self.mana,
            "maxMana": self.maxMana,
            "speed": self.speed,
            "item": self.item,
            "helmet": self.helmet,
            "chestplate": self.chestplate,
            "weapon": self.weapon,
            "weapon2": self.weapon2,
            "luck": self.luck,
            "spells": self.spells
        }

    @classmethod
    def from_dict(cls, data):
        player = cls()
        player.name = data["name"]
        if data["heroClass"] != "NULL":
            player.set_class(data["heroClass"])
        if data["heroRace"] != "NULL":
            player.set_race(data["heroRace"])
            
        # Restore all other attributes
        for key, value in data.items():
            if key not in ["name", "heroClass", "heroRace"]:
                setattr(player, key, value)
        
        return player


player = Player()