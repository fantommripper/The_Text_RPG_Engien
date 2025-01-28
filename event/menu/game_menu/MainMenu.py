
from lib.Logger import logger

from data.Logo import logo

from controller.MenuController import menu_controller
from controller.LibController import lib_controller

from lib.ConsoleSettings import console_settings
class MainMenu():
    def __init__(self):
        pass

    def run(self):
        self.display_logo = lib_controller.consolas.play_animation(
                        frames = logo.text_rpg_logo,
                        y=10,
                        Ydo="-"
        )

        self.main_menu = lib_controller.consolas.create_menu(
                        clear=False,
                        title="Menu",
                        options=["new game", "load game", "options", "autors", "exit"],
                        tips=False,
        )
        self.action = self.main_menu.get_menu_result()

        while True:

            if self.action:
                logger.info(f"Selected option: {self.action}")

                if self.action == "0":
                    logger.info("new game")

                elif self.action == "1":
                    logger.info("load game")

                elif self.action == "2":
                    logger.info("options")
                
                elif self.action == "3":
                    logger.info("autors")
                    menu_controller.show_autors_menu()

                elif self.action == "4":
                    logger.info("exit")
                    console_settings.exit_terminal()

main_menu = MainMenu()



