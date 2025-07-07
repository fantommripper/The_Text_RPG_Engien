from lib.Logger import logger
from lib.SaveManager import save_manager
from lib.Localization import loc

from controller.MenuController import MenuController
from controller.LibController import LibController

from data.Config import Config

class SettingMenu:
    def __init__(self):
        self.consolas = LibController.get_instance().consolas
        self.config = Config.get_instance()
        self.menu = None

    def _stop_menu(self):
        if self.menu:
            self.menu.stop()

    def _show_main_menu(self):
        self._stop_menu()
        MenuController.get_instance().show_main_menu()
        save_manager.save_all_game_data()

    def run(self):
        self._stop_menu()
        self.menu = self.consolas.create_menu(
            title=loc.t("options"),
            options={
                loc.t("output_delay"): self._output_delay_menu,
                loc.t("language"): self._language_menu,
                loc.t("cheats"): self._cheats_menu,
                loc.t("back"): self._show_main_menu
            },
            tips=False
        )

    def _output_delay_menu(self):
        self._stop_menu()
        def set_delay(delay):
            self.config.delayOutput = float(delay)
            logger.info(f"Set output delay: {delay}")
            self.run()

        self.menu = self.consolas.create_menu(
            title=loc.t("output_delay"),
            options={
                "0": lambda: set_delay("0"),
                "0.01": lambda: set_delay("0.01"),
                "0.02": lambda: set_delay("0.02"),
                "0.03": lambda: set_delay("0.03"),
                loc.t("back"): self.run
            },
            tips=False
        )

    def _language_menu(self):
        self._stop_menu()
        def set_lang(lang):
            self.config.language = lang
            loc.set_language(self.config.language)
            logger.info(f"Set language: {lang}")
            self.run()

        self.menu = self.consolas.create_menu(
            loc.t("language"),
            options={
                "English": lambda: set_lang("EN"),
                "Русский": lambda: set_lang("RU"),
                loc.t("back"): self.run
            },
            tips=False
        )

    def _cheats_menu(self):
        self._stop_menu()
        def set_cheats(val):
            self.config.cheats = val
            logger.info(f"Set cheats: {val}")
            self.run()

        self.menu = self.consolas.create_menu(
            loc.t("cheats"),
            options={
                loc.t("on"): lambda: set_cheats(True),
                loc.t("off"): lambda: set_cheats(False),
                loc.t("back"): self.run
            },
            tips=False
        )

setting_menu = SettingMenu()