from abc import ABC, abstractmethod

class Race(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def base_stats(self) -> dict:
        return {
            "Dm": 0,
            "Hp": 0,
            "maxHp": 0,
            "speed": 0,
            "maxMana": 0,
            "mana": 0
        }

class Human(Race):
    @property
    def name(self) -> str:
        return "Human"

    @property
    def base_stats(self) -> dict:
        return {
            "Dm": 10,
            "Hp": 110,
            "maxHp": 110,
            "speed": 2,
            "maxMana": 20,
            "mana": 20
        }

class Kobold(Race):
    @property
    def name(self) -> str:
        return "Kobold"

    @property
    def base_stats(self) -> dict:
        return {
            "Dm": 9,
            "Hp": 110,
            "maxHp": 110,
            "speed": 3,
            "maxMana": 25,
            "mana": 25
        }

class Owlin(Race):
    @property
    def name(self) -> str:
        return "Owlin"

    @property
    def base_stats(self) -> dict:
        return {
            "Dm": 9,
            "Hp": 70,
            "maxHp": 70,
            "speed": 6,
            "maxMana": 35,
            "mana": 35
        }

class Naga(Race):
    @property
    def name(self) -> str:
        return "Naga"

    @property
    def base_stats(self) -> dict:
        return {
            "Dm": 9,
            "Hp": 130,
            "maxHp": 130,
            "speed": 1,
            "maxMana": 15,
            "mana": 15
        }

AVAILABLE_RACES = {
    "Human": Human,
    "Kobold": Kobold,
    "Owlin": Owlin,
    "Naga": Naga
} 