from data.Config import config
from data.Player import player

class LibController():
    def __init__(self):
        self.consolas = None
        self.input_controller = None

    def load_consolas(self, win):
        from lib.Consolas import Consolas
        self.consolas = Consolas(config, player, win)

    def load_input_controller(self, win):
        from lib.InputController import InputController
        self.input_controller = InputController()

    def load_lib(self, win):
        self.load_input_controller(win)
        self.load_consolas(win)


lib_controller = LibController()