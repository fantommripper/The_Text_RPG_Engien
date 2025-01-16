from event.menu.TestWorldMeny.AudioTestMenu import audio_test_menu
from lib.Logger import logger

class MenuController():
    def __init__(self):
        pass

    def show_audio_test_menu(self):
        audio_test_menu.run()

menu_controller = MenuController()