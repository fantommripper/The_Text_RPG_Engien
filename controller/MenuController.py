from lib.Logger import logger

class MenuController():
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def show_audio_test_menu(self):
        from Assets.event.menu.test_world_menu.AudioTestMenu import audio_test_menu
        audio_test_menu.run()

    def show_widget_test_menu(self):
        from Assets.event.menu.test_world_menu.WidgetTestMenu import widget_test_menu
        widget_test_menu.run()

    def show_multiply_widget_test(self):
        from Assets.event.menu.test_world_menu.multiplyWidgetTest import multiply_widget_test
        multiply_widget_test.run()

    def show_world_map_test(self):
        from Assets.event.menu.test_world_menu.WorldMapTest import world_map_test
        world_map_test.run()


    def show_main_menu(self):
        from Assets.event.menu.game_menu.MainMenu import main_menu
        main_menu.run()

    def show_autors_menu(self):
        from Assets.event.menu.game_menu.AutorsMenu import autors_menu
        autors_menu.run()

    def show_setting_menu(self):
        from Assets.event.menu.game_menu.SettingMenu import setting_menu
        setting_menu.run()

    def show_hero_create_menu(self):
        from Assets.event.menu.game_menu.HeroCreateMenu import hero_create_menu
        hero_create_menu.run()

