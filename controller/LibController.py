from lib.Consolas import Consolas
from lib.TableMenu import TableMenu
from lib.Terminalium import Terminalium

from data.Config import config
from data.Player import player

class LibController():
    def __init__(self):
        self.consolas = None
        self.table_menu = None
        self.terminalium = None

    def loud_consolas(self, win):
        self.consolas = Consolas(config, player, win)

    def loud_table_menu(self, win):
        self.table_menu = TableMenu(config, win)

    def loud_terminalium(self, win):
        self.terminalium = Terminalium(win)

    def loud_lib(self, win):
        self.loud_consolas(win)
        self.loud_table_menu(win)
        self.loud_terminalium(win)


lib_controller = LibController()