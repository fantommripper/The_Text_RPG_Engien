from lib.Logger import logger
from controller.MenuController import menu_controller
from controller.LibController import lib_controller
from lib.SaveManager import save_manager
from data.Config import config

class SettingMenu:
    def __init__(self):
        self.consolas = lib_controller.consolas
        self.menu = None

    def _stop_menu(self):
        if self.menu:
            self.menu.stop()

    def _show_main_menu(self):
        self._stop_menu()
        menu_controller.show_main_menu()
        save_manager.save_all_game_data()

    def run(self):
        self._stop_menu()
        self.menu = self.consolas.create_menu(
            title="Settings",
            options={
                "output delay": self._output_delay_menu,
                "language": self._language_menu,
                "cheats": self._cheats_menu,
                "back": self._show_main_menu
            },
            tips=False,
        )
        self.consolas.start_tab_control([self.menu])

    def _output_delay_menu(self):
        self._stop_menu()
        def set_delay(delay):
            config.delayOutput = float(delay)
            logger.info(f"Set output delay: {delay}")
            self.run()
        self.menu = self.consolas.create_menu(
            title="Output Delay",
            options={
                "0": lambda: set_delay("0"),
                "0.01": lambda: set_delay("0.01"),
                "0.02": lambda: set_delay("0.02"),
                "0.03": lambda: set_delay("0.03"),
                "back": self.run
            },
            tips=False,
        )
        self.consolas.start_tab_control([self.menu])

    def _language_menu(self):
        self._stop_menu()
        def set_lang(lang):
            config.language = lang
            logger.info(f"Set language: {lang}")
            self.run()
        self.menu = self.consolas.create_menu(
            title="Language",
            options={
                "English": lambda: set_lang("EN"),
                "Русский": lambda: set_lang("RU"),
                "back": self.run
            },
            tips=False,
        )
        self.consolas.start_tab_control([self.menu])

    def _cheats_menu(self):
        self._stop_menu()
        def set_cheats(val):
            config.cheats = val
            logger.info(f"Set cheats: {val}")
            self.run()
        self.menu = self.consolas.create_menu(
            title="Cheats",
            options={
                "On": lambda: set_cheats(True),
                "Off": lambda: set_cheats(False),
                "back": self.run
            },
            tips=False,
        )
        self.consolas.start_tab_control([self.menu])

setting_menu = SettingMenu()