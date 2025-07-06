from lib.ConsoleSettings import console_settings
from lib.Logger import logger
from lib.Localization import loc

from data.Logo import Logo

from controller.MenuController import MenuController
from controller.LibController import LibController


class MainMenu():
    def __init__(self):
        self.consolas = LibController.get_instance().consolas
        self.main_menu = None

    def _stop_menu(self):
        self.main_menu.stop()

    def _show_new_game_menu(self):
        logger.info("new game")
        self._stop_menu()
        MenuController.get_instance().show_hero_create_menu()

    def _show_load_game_menu(self):
        logger.info("load game")
        self._stop_menu()

    def _show_options_menu(self):
        logger.info("options")
        self._stop_menu()
        MenuController.get_instance().show_setting_menu()

    def _show_autors_menu(self):
        logger.info("autors")
        self._stop_menu()
        MenuController.get_instance().show_autors_menu()

    def _exit_menu(self):
        logger.info("exit")
        self._stop_menu()
        console_settings.exit_terminal()

    def run(self):
        self.display_logo = self.consolas.play_animation(
                       frames = Logo.get_instance().text_rpg_logo,
                       y=10,
                       Ydo="-"
        )
        self.main_menu = self.consolas.create_menu(
                        clear=False,
                        title=loc.t("menu"),
                        options={
                            loc.t("new_game") : self._show_new_game_menu,
                            loc.t("load_game") : self._show_load_game_menu,
                            loc.t("options") : self._show_options_menu,
                            loc.t("autors") : self._show_autors_menu,
                            loc.t("exit") : self._exit_menu
                        },
                        tips=False,
        )

main_menu = MainMenu()



