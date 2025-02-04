from lib.Logger import logger

class MenuController():
    def __init__(self):
        pass

   
    def show_audio_test_menu(self):
        from event.menu.test_world_menu.AudioTestMenu import audio_test_menu
        audio_test_menu.run()

    def show_main_menu(self):
        from event.menu.game_menu.MainMenu import main_menu 
        main_menu.run()

    def show_autors_menu(self):
        from event.menu.game_menu.AutorsMenu import autors_menu
        autors_menu.run()

    def show_widget_test_menu(self):
        from event.menu.test_world_menu.WidgetTestMenu import widget_test_menu
        widget_test_menu.run()

    def show_setting_menu(self):
        from event.menu.game_menu.SettingMenu import setting_menu
        setting_menu.run()


menu_controller = MenuController()