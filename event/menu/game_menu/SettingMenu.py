from lib.Logger import logger
from controller.MenuController import menu_controller
from controller.LibController import lib_controller
from lib.SaveManager import save_manager
from data.Config import config

class SettingMenu:
    def __init__(self):
        self.consolas = lib_controller.consolas

        self.main_menu = None
        self.delay_menu = None
        self.language_menu = None
        self.cheats_menu = None

    def run(self):
        while True:
            self.main_menu = self.consolas.create_menu(
                title="Setting",
                options=["output delay", "language", "cheats", "back"],
                tips=False,
            )
            action = self.main_menu.get_menu_result()

            if action is not None:
                logger.info(f"Selected option: {action}")

                if action == "0":
                    self.set_output_delay()
                elif action == "1":
                    self.set_language()
                elif action == "2":
                    self.set_cheats()
                elif action == "3":
                    logger.info("back")
                    save_manager.save_all_game_data()
                    menu_controller.show_main_menu()
                    break

    def set_output_delay(self):
        self.delay_menu = self.consolas.create_menu(
            clear=False,
            title="output delay",
            options=["0", "0.01", "0.02", "0.03", "back"],
            tips=False,
            Xdo="+",
            Ydo="+",
            x=2,
            y=3,
        )
        result = self.delay_menu.get_menu_result()
        if result is not None:
            if result == "0":
                logger.info("output delay = 0")
                config.delayOutput = 0
            elif result == "1":
                logger.info("output delay = 0.01")
                config.delayOutput = 0.01
            elif result == "2":
                logger.info("output delay = 0.02")
                config.delayOutput = 0.02
            elif result == "3":
                logger.info("output delay = 0.03")
                config.delayOutput = 0.03
            elif result == "4":
                logger.info("back from output delay")


    def set_language(self):
        self.language_menu = self.consolas.create_menu(
            clear=False,
            title="Language",
            options=["English", "back"],
            tips=False,
            Xdo="+",
            Ydo="+",
            x=2,
            y=1,
        )
        result = self.language_menu.get_menu_result()
        if result is not None:
            if result == "0":
                logger.info("Language = En")
                config.language = "EN"
            elif result == "1":
                logger.info("back from language")


    def set_cheats(self):
        self.cheats_menu = self.consolas.create_menu(
            clear=False,
            title="Cheats",
            options=["On", "Off", "back"],
            tips=False,
            Xdo="+",
            Ydo="+",
            x=2,
            y=2,
        )
        result = self.cheats_menu.get_menu_result()
        if result is not None:
            if result == "0":
                logger.info("Cheats On")
                config.cheats = True
            elif result == "1":
                logger.info("Cheats Off")
                config.cheats = False
            elif result == "2":
                logger.info("back from cheats")


setting_menu = SettingMenu()
