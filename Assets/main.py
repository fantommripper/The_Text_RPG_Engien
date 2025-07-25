import curses
import time

from lib.ConsoleSettings import console_settings
from lib.Logger import logger
from lib.SaveManager import save_manager
from lib.Localization import loc

from controller.MenuController import MenuController
from controller.LibController import LibController
from controller.AudioController import AudioController

from data.Config import Config

class App():
    def __init__(self):
        self.win = None
        self.lib_controller = LibController.get_instance()
        self.config = Config.get_instance()

    def start(self, stdscr):
        logger.info("Starting game")
        curses.resize_term(0, 0)
        curses.curs_set(0)

        self.win = console_settings.create_fullscreen_window(stdscr)
        if not self.win:
            logger.error("Failed to create window!")
            return

        self.win.keypad(True)
        self.win.nodelay(True)
        self.win.clear()
        self.win.refresh()

        self.lib_controller.load_lib(self.win)

        self.run()

    def run(self):
        save_manager.load_all_game_data()
        loc.set_language(self.config.language)

        if self.config.loading == 0:
            self.lib_controller.consolas.loading_animation()
        else:
            self.lib_controller.consolas.fast_loading()

        self.config.loading += 1

        AudioController.get_instance().play_music("background")
        #MenuController.get_instance().show_world_map_test()
        MenuController.get_instance().show_main_menu()

        while True:
            c = self.win.getch()
            if c != -1:
                self.lib_controller.input_controller.handle_key(c)
            time.sleep(0.01)

def main():
    try:
        console_settings.open_terminal_fullscreen()

        app = App()
        curses.wrapper(app.start)

    except Exception as e:
        logger.error(f'ERROR: {str(e)}', exc_info=True)

        curses.endwin()
        AudioController.get_instance().stop_music()
        quit(1)

if __name__ == '__main__':
    main()