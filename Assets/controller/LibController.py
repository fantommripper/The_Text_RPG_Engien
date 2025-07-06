from data.Config import config
from lib.Logger import logger

class LibController():
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LibController()
        return cls._instance

    def __init__(self):
        self.consolas = None
        self.input_controller = None
        logger.warning("LibController initialized")

    def load_consolas(self, win):
        from lib.Consolas import Consolas
        self.consolas = Consolas(config, win)

    def load_input_controller(self):
        from lib.InputController import InputController
        self.input_controller = InputController()

    def load_lib(self, win):
        self.load_input_controller()
        self.load_consolas(win)

        if self.input_controller is None:
            logger.error("InputController initialization failed!")
        if self.consolas is None:
            logger.error("Consolas initialization failed!")
