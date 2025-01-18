import ctypes
import curses
import os
import time
import pyautogui
import keyboard
import pygetwindow as gw

from lib.Logger import logger

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
        # Получаем активное окно
        active_window = gw.getActiveWindow()
        if active_window:
            return active_window.title
        return None

    def maximize_terminal(self):
        # Находим текущее окно терминала
        windows = gw.getWindowsWithTitle(self.get_current_window_title())  # Замените название, если нужно
        if not windows:
            print("Окно терминала не найдено.")
            return

        terminal_window = windows[0]

        # Максимизируем окно
        terminal_window.maximize()
        print("Терминал растянут на весь экран.")

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



console_settings = ConsoleSettings()