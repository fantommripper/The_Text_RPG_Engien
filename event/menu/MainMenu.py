from controller.LibController import lib_controller
from lib.Logger import logger
from data.Logo import logo

class MainMenu():
    def __init__(self):
        pass

    def run(self):
        while True:
            lib_controller.consolas.play_animation(
                frames = logo.text_rpg_logo,
                y = 1
            )
            

            lib_controller.table_menu.menu(
                clear=False,
                title="Menu",
                options=["new game", "loud game", "options", "autors", "exit"],
                y=10,
                tips=False
                
            )
            self.action = lib_controller.table_menu.get_menu_result()
            
            if self.action: 
                logger.debug(f"Selected option: {self.action}")

                if self.action == "0":
                    logger.debug("new game")
                
                elif self.action == "1":
                    logger.debug("loud game")

                elif self.action == "2":
                    logger.debug("options")
                
                elif self.action == "3":
                    logger.debug("autors")

                elif self.action == "4":
                    logger.debug("exit")
                    break

main_menu = MainMenu()



