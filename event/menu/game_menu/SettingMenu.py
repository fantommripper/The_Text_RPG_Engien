from lib.ConsoleSettings import console_settings
from lib.Logger import logger

from data.Logo import logo

from controller.MenuController import menu_controller
from controller.LibController import lib_controller
from lib.SaveManager import save_manager

from data.Config import config

class SettingMenu():
    def __init__(self):
        pass

    def run(self):
        while True:
            self.main_menu = lib_controller.consolas.create_menu(
                            title="Setting",
                            options=["output delay", "language", "cheats", "back"],
                            tips=False,
            )

            self.action = self.main_menu.get_menu_result()

            if self.action:
                logger.info(f"Selected option: {self.action}")

                if self.action == "0":
                    logger.info("output delay")
                    output_delay_widget = lib_controller.consolas.create_menu(
                                            clear=False,
                                            title="output delay",
                                            options=["0", "0.01", "0.02", "0.03", "back"],
                                            tips=False,
                                            Xdo="+",
                                            x=23,
                                            y=1,
                                            Ydo="+",
                                        )
                    
                    self.output_delay_action = output_delay_widget.get_menu_result()
                
                    if self.output_delay_action:
                        if self.output_delay_action == "0":
                            logger.info("output delay = 0")
                            config.delayOutput = 0
                        
                        elif self.output_delay_action == "1":
                            logger.info("output delay = 0.01")
                            config.delayOutput = 0.01
                        
                        elif self.output_delay_action == "2":
                            logger.info("output delay = 0.02")
                            config.delayOutput = 0.02
                        
                        elif self.output_delay_action == "3":
                            logger.info("output delay = 0.03")
                            config.delayOutput = 0.03
                        
                        elif self.output_delay_action == "4":
                            pass

                elif self.action == "1":
                    logger.info("language")
                    language_widget = lib_controller.consolas.create_menu(
                                            clear=False,
                                            title="Language",
                                            options=["English", "back"],
                                            tips=False,
                                            Xdo="+",
                                            x=23,
                                            y=1,
                                            Ydo="+",
                                        )
                    
                    self.language_action = language_widget.get_menu_result()

                    if self.language_action:
                        if self.language_action == "0":
                            logger.info("Language = En")
                            config.language = "EN"
                        
                        elif self.language_action == "1":
                            pass

                elif self.action == "2":
                    logger.info("cheats")
                    cheats_widget = lib_controller.consolas.create_menu(
                                            clear=False,
                                            title="Cheats",
                                            options=["On", "OfF", "back"],
                                            tips=False,
                                            Xdo="+",
                                            x=23,
                                            y=1,
                                            Ydo="+",
                                        )
                    
                    self.cheats_action = cheats_widget.get_menu_result()

                    if self.cheats_action:
                        if self.cheats_action == "0":
                            logger.info("Cheats On")
                            config.cheats = True
                        
                        elif self.cheats_action == "1":
                            logger.info("Cheats Off")
                            config.cheats = False

                        elif self.cheats_action == "2":
                            pass
                    
                elif self.action == "3":
                    logger.info("back")
                    save_manager.save_all_game_data()
                    menu_controller.show_main_menu()

setting_menu = SettingMenu()