from lib.Consolas import Consolas
from lib.Terminalium import Terminalium

from data.Config import config
from data.Player import player

class LibController():
    def __init__(self):
        self.consolas = None
        self.terminalium = None

    def load_consolas(self, win):
        self.consolas = Consolas(config, player, win)

    def load_terminalium(self, win):
        self.terminalium = Terminalium(win)

    def load_lib(self, win):
        self.load_consolas(win)
        self.load_terminalium(win)


lib_controller = LibController()