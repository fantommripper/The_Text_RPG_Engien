import curses

from lib.ConsoleSettings import console_settings
from lib.Logger import logger

from controller.MenuController import menu_controller
from controller.LibController import lib_controller
from controller.InputController import input_controller

from data.GameFlags import game_flags

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

        lib_controller.loud_lib(self.win)
        input_controller.start_getting_input()

        self.run()

    def run(self):
        menu_controller.show_audio_test_menu()


if __name__ == '__main__':
    try:
        console_settings.open_terminal_fullscreen()

        app = App()
        curses.wrapper(app.start)
    except Exception as e:
        logger.error(f'ERROR: {str(e)}', exc_info=True)

    curses.endwin()
    input_controller.stop_getting_input()

