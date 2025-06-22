from controller.LibController import lib_controller

from lib.Logger import logger
from lib.Consolas import PlayerMapConfig

from data.LevelMap import Levels

class WorldMapTest():
    def __init__(self):
        self.level = Levels.Level0()

        self.map_config = PlayerMapConfig(
            map = self.level
        )

    def run(self):
        lib_controller.consolas.create_player_map(config=self.map_config)

world_map_test = WorldMapTest()