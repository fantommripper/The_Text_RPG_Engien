import ctypes
import curses
import os
import pyautogui
import keyboard
import pygetwindow as gw

from lib.Logger import logger
from lib.SaveManager import save_manager

from controller.InputController import input_controller
from controller.AudioController import audio_controller

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class SMALL_RECT(ctypes.Structure):
    _fields_ = [("Left", ctypes.c_short),
                ("Top", ctypes.c_short),
                ("Right", ctypes.c_short),
                ("Bottom", ctypes.c_short)]

class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [("dwSize", COORD),
                ("dwCursorPosition", COORD),
                ("wAttributes", ctypes.c_ushort),
                ("srWindow", SMALL_RECT),
                ("dwMaximumWindowSize", COORD)]

class ConsoleSettings():
    def __init__(self):
        pass

    def get_current_window_title(self):
        active_window = gw.getActiveWindow()
        if active_window:
            return active_window.title
        return None

    def maximize_terminal(self):
        windows = gw.getWindowsWithTitle(self.get_current_window_title())
        if not windows:
            return

        terminal_window = windows[0]

        terminal_window.maximize()

    def open_terminal_fullscreen(self):
        self.maximize_terminal()
        pyautogui.press('f11')
        keyboard.block_key('f11')

    def create_fullscreen_window(self, stdscr):
        stdscr.refresh()
        height, width = stdscr.getmaxyx()
        logger.info(f"Terminal size after adjustment: {height}x{width}")
        win = curses.newwin(height, width, 0, 0)
        return win

    def exit_terminal(self):
        save_manager.save_all_game_data()

        curses.endwin()
        input_controller.stop_getting_input()
        audio_controller.stop_music()

        quit(0)




console_settings = ConsoleSettings()