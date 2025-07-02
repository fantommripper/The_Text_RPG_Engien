import curses

class WorldValues:
    def __init__(self):
        self.chances = {
            "monstr": 40,
            "shop": 15,
            "void": 45
        }
        self.shop_types = ["blacksmith", "alchemist"]

        self.center_x = round(curses.COLS / 2)
        self.center_y = round(curses.LINES / 2)


world_values = WorldValues()