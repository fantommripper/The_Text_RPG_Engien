from abc import ABC

class Item(ABC):
    def __init__(self, name: str, description: str, item_type: str, value: int):
        self.name = name
        self.description = description
        self.item_type = item_type  # e.g., "weapon", "armor", "potion"
        self.value = value  # e.g., damage for weapons, defense for armor

    # TODO: Зделать когда-нибудь (когда будет минимальный функционал игры)