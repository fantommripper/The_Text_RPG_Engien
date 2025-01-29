import curses

from lib.ConsoleSettings import console_settings
from lib.Logger import logger
from lib.SaveManager import save_manager

from controller.MenuController import menu_controller
from controller.LibController import lib_controller
from controller.InputController import input_controller
from controller.AudioController import audio_controller

from data.Config import config

class App():
    def __init__(self):
        self.win = None

    def start(self, stdscr):
        logger.info("Starting game")
        curses.resize_term(0, 0)
        curses.curs_set(0)

        self.win = console_settings.create_fullscreen_window(stdscr)
        if not self.win:
            logger.error("Failed to create window!")
            return

        self.win.keypad(True)
        self.win.clear()
        self.win.refresh()

        lib_controller.load_lib(self.win)
        input_controller.add_all_hotkeys()

        self.run()

    def run(self):
        save_manager.load_all_game_data()

        if config.loading == 0:
            lib_controller.consolas.loading_animation()
        else:
            lib_controller.consolas.fast_loading()

        config.loading += 1

        audio_controller.play_background_music()
        menu_controller.show_main_menu()



if __name__ == '__main__':
    try:
        console_settings.open_terminal_fullscreen()

        app = App()
        curses.wrapper(app.start)

    except Exception as e:
        logger.error(f'ERROR: {str(e)}', exc_info=True)

        curses.endwin()
        audio_controller.stop_music()
        quit(1)



