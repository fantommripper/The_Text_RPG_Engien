from abc import ABC

class Spells(ABC):
    def __init__(self, name: str, description: str, mana_cost: int, value: int):
        self.name = name
        self.description = description
        self.mana_cost = mana_cost  # Mana cost to cast the spell
        self.value = value  # Damage or effect value of the spell

    #TODO: Зделать когда-нибудь (когда будет минимальный функционал игры)