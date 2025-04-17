from controller.LibController import lib_controller
from controller.MenuController import menu_controller

from lib.Logger import logger

from data.Config import config

class HeroCreateMenu():
    def __init__(self):
        pass

    def run(self):
        while True:
            self.tips_table = lib_controller.consolas.create_table(
                "tips",
                "Entry your name",
                y=8,
                Ydo="-",
                separator_positions=[0],
                alignment={0: "c"},
            )



hero_create_menu = HeroCreateMenu()