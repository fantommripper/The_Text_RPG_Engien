import curses

class WorldValues:
    _instance = None

    def __init__(self):
        self.chances = {
            "monstr": 40,
            "shop": 15,
            "void": 45
        }
        self.shop_types = ["blacksmith", "alchemist"]

        self.center_x = round(curses.COLS / 2)
        self.center_y = round(curses.LINES / 2)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance