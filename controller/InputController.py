import keyboard

from lib.Terminalium import terminalium
from lib.Logger import logger

class InputController():
    def __init__(self):
        pass

    def add_all_hotkeys(self):
        keyboard.add_hotkey('t', terminalium.show_terminal)

input_controller = InputController()