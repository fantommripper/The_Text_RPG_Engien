from controller.LibController import lib_controller
from controller.MenuController import menu_controller

from lib.Logger import logger

class AutorsMenu():
    def __init__(self):
        self.consolas = lib_controller.consolas

        self.autors_table = None
        self.main_menu = None
        self.tab_control = False

    def _stop_menu(self):
        self.consolas.stop_tab_control()
        self.main_menu.stop()
        self.tab_control = False

    def _show_main_menu(self):
        logger.info("main menu")
        self._stop_menu()
        menu_controller.show_main_menu()

    def run(self):
        self.autors_table = self.consolas.create_table(
            "Autors",
            "perri?",
            "fantomm",
            y=8,
            Ydo="-",
            separator_positions=[0],
            alignment={0: "c"},
        )

        self.main_menu = self.consolas.create_menu(
            clear=False,
            title="Menu",
            options={"back" : self._show_main_menu},
            tips=False
        )

        if not self.tab_control:
            self.widgets_list = [self.main_menu]
            self.consolas.start_tab_control(self.widgets_list)
            self.tab_control = True

autors_menu = AutorsMenu()