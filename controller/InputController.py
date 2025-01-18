import threading
import keyboard

from data.GameFlags import game_flags
from controller.LibController import lib_controller
from lib.Logger import logger

class InputController():
    def __init__(self):
        self.input_thread = None
        self.input_active = False

        self.key_pressed = False

    def _get_input(self):
        while self.input_active:
            pass
    def start_getting_input(self):
        logger.info('Starting input controller')

        self.input_active = True
        self.input_thread = threading.Thread(target=self._get_input)
        self.input_thread.start()

    def stop_getting_input(self):
        if self.input_active:
            self.input_active = False
            if self.input_thread is not None:
                self.input_thread.join()

input_controller = InputController()
