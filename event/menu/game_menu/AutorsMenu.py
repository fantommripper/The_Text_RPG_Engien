from controller.LibController import lib_controller
from controller.MenuController import menu_controller

from lib.Logger import logger
from lib.Localization import loc

class AutorsMenu():
    def __init__(self):
        self.consolas = lib_controller.consolas

        self.autors_table = None
        self.main_menu = None

    def _show_main_menu(self):
        self.main_menu.stop()
        menu_controller.show_main_menu()

    def run(self):
        self.autors_table = self.consolas.create_table(
            loc.t("autors"),
            "perri?",
            "fantomm",
            tableAlignment="c",
            y=8,
            Ydo="-",
            separator_positions=[0],
            textAlignment={0: "c"}
        )

        self.main_menu = self.consolas.create_menu(
            clear=False,
            title=loc.t("menu"),
            options={loc.t("back") : self._show_main_menu},
            tips=False
        )

autors_menu = AutorsMenu()