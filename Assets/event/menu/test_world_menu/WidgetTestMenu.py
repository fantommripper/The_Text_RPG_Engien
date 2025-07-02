from controller.LibController import lib_controller

from lib.Logger import logger
from lib.ConsoleSettings import console_settings

class WidgetTestMenu():
    def __init__(self):
        pass

    def run(self):
        while True:
            main_menu_widget = lib_controller.consolas.create_menu(
                            title="Menu",
                            options=["exit", "doble menu"],
                            tips=False,
                        )
            self.action = main_menu_widget.get_menu_result()

            if self.action:
                logger.info(f"Selected option: {self.action}")

                if self.action == "0":
                    logger.info("Exiting audio test menu")
                    console_settings.exit_terminal()
                    break

                elif self.action == "1":
                    logger.info("open double menu")
                    double_menu_widget = lib_controller.consolas.create_menu(
                                            clear=False,
                                            title="double menu",
                                            options=["exit"],
                                            tips=False,
                                            Xdo="+",
                                            x=23,
                                            y=1,
                                            Ydo="+",
                                        )
                    self.double_menu_action = double_menu_widget.get_menu_result()

                    if self.double_menu_action:
                        logger.info(f"Selected option: {self.double_menu_action}")
                        if self.double_menu_action == "0":
                            logger.info("Exiting double menu")
                            double_menu_widget.stop_menu()


widget_test_menu = WidgetTestMenu()