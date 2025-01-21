from controller.LibController import lib_controller
from lib.Logger import logger
from data.Logo import logo

class AutorsMenu():
    def __init__(self):
        pass

    def run(self):
        while True:
            
            lib_controller.consolas.create_table(
                "Autors",
                "perri", 
                "fantomm",
                y=8,
                Ydo="-",
                separator_positions=[0],
                alignment={0: "center"},
                x=1,
                Xdo="-"
            
            )
                
            lib_controller.table_menu.menu(
                clear=False,
                title="Menu",
                options=["back"],
                tips=False
            )

            self.action = lib_controller.table_menu.get_menu_result()

            if self.action: 
                logger.debug(f"Selected option: {self.action}")

                if self.action == "0":
                    logger.debug("back")
                    break

autors_menu = AutorsMenu()