from abc import ABC, abstractmethod

class HeroClass(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": 0,
            "Hp": 0,
            "maxHp": 0,
            "speed": 0,
            "maxMana": 0,
            "mana": 0
        }

class Swordsman(HeroClass):
    @property
    def name(self) -> str:
        return "swordsman"

    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": 3,
            "Hp": 30,
            "maxHp": 30,
            "speed": 0,
            "maxMana": -5,
            "mana": -5
        }

class Magician(HeroClass):
    @property
    def name(self) -> str:
        return "magician"

    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": -1,
            "Hp": -5,
            "maxHp": -5,
            "speed": 0,
            "maxMana": 20,
            "mana": 20
        }

class Thief(HeroClass):
    @property
    def name(self) -> str:
        return "thief"

    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": 3,
            "Hp": -5,
            "maxHp": -5,
            "speed": 2,
            "maxMana": 0,
            "mana": 0
        }

class Archer(HeroClass):
    @property
    def name(self) -> str:
        return "archer"

    @property
    def stat_modifiers(self) -> dict:
        return {
            "Dm": 1,
            "Hp": 0,
            "maxHp": 0,
            "speed": 1,
            "maxMana": 0,
            "mana": 0
        }

AVAILABLE_CLASSES = {
    "swordsman": Swordsman,
    "magician": Magician,
    "thief": Thief,
    "archer": Archer
} 