import curses

from lib.Logger import logger

class Terminalium():
    def __init__(self, win):
        self.stdscr = win
        self.height, self.width = self.stdscr.getmaxyx()

    def show_terminal(self):
        logger.info("Terminalium initialized")
        logger.info(f"Terminal size: {self.height}x{self.width}")

        self.win = curses.newwin(self.height-2, self.width-2, 1, 1)
        self.win.box()

        self.win.addstr(0, 4, "Terminalium")

        self.win.refresh()

    def close_terminal(self):
        logger.info("Closing terminalium")

        if hasattr(self, 'win'):
            self.win.clear()
            self.win.refresh()
            del self.win