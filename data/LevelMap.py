

class Levels:

    class BaseLevel:
        def __init__(self, level_id: int, name: str, description: str):
            self.level_id = level_id
            self.name = name

            self.PlayerSpawnX = 0
            self.PlayerSpawnY = 0

            self.level_map = []

    class Level0(BaseLevel):
        def __init__(self):
            super().__init__(0, "Test Level", "This is a TEST!")
            self.level_map = [
                "             *********************             ",
                "         *****                   *****         ",
                "      ****                           ****      ",
                "    ***                        _________***    ",
                "   **                         /           **   ",
                "  **                         /     ʘ       **  ",
                " **                         /               ** ",
                " *                  _______/                 * ",
                "**          ₩      /                         **",
                "*                 /                           *",
                "*                /                            *",
                "*          _____/                             *",
                "*\        /              ƒ                    *",
                "* ‾‾‾\   /                                    *",
                "**    ‾‾‾‾‾‾\                                **",
                " *           ‾‾‾‾\                           * ",
                " **               \        /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾** ",
                "  **     ₲         ‾Y‾‾‾‾‾‾                **  ",
                "   **               \                     **   ",
                "    ***              |                  ***    ",
                "      ****           |               ****      ",
                "         *****       |           *****         ",
                "             *********************             "
            ]
            self.PlayerSpawnX = 25
            self.PlayerSpawnY = 12