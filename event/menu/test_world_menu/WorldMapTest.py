from controller.LibController import lib_controller

from lib.Logger import logger
from lib.Consolas import PlayerMapConfig

from data.LevelMap import Levels

class WorldMapTest():
    def __init__(self):
        self.level = Levels.Level0()

    def run(self):
        lib_controller.consolas.create_player_map(level_map=self.level)

world_map_test = WorldMapTest()