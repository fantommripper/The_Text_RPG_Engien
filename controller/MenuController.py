from lib.Logger import logger

class MenuController():
    def __init__(self):
        pass

    def show_audio_test_menu(self):
        from event.menu.test_world_menu.AudioTestMenu import audio_test_menu
        audio_test_menu.run()

menu_controller = MenuController()