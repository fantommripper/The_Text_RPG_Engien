from data.Config import Config

class LibController():
    _instance = None

    def __init__(self):
        self.consolas = None
        self.input_controller = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_consolas(self, win):
        from lib.Consolas import Consolas
        self.consolas = Consolas(Config.get_instance(), win)

    def load_input_controller(self, win):
        from lib.InputController import InputController
        self.input_controller = InputController()

    def load_lib(self, win):
        self.load_input_controller(win)
        self.load_consolas(win)