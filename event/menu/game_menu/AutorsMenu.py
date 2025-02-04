from controller.LibController import lib_controller
from controller.MenuController import menu_controller

from lib.Logger import logger

class AutorsMenu():
    def __init__(self):
        pass

    def run(self):
        while True:
            self.autors_table = lib_controller.consolas.create_table(
                "Autors",
                "perri",
                "fantomm",
                y=8,
                Ydo="-",
                separator_positions=[0],
                alignment={0: "c"},
            )

            self.main_menu = lib_controller.consolas.create_menu(
                clear=False,
                title="Menu",
                options=["back"],
                tips=False
            )

            self.action = self.main_menu.get_menu_result()


            if self.action:
                logger.info(f"Selected option: {self.action}")

                if self.action == "0":
                    logger.info("back")
                    menu_controller.show_main_menu()

autors_menu = AutorsMenu()