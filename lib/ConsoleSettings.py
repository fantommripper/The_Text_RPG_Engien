import curses

class ConsoleSettings():
    def __init__(self):
        pass

    def create_fullscreen_window(self, stdscr):
        height, width = stdscr.getmaxyx()
        win = curses.newwin(height, width, 0, 0)
        return win


console_settings = ConsoleSettings()