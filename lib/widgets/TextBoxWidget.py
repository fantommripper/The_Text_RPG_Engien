import curses
import time as t
from typing import Callable, List

from lib.widgets.BaseActiveWidget import BaseActiveWidget

from controller.LibController import lib_controller
from controller.AudioController import audio_controller

from data.Config import config

class TextBoxWidget(BaseActiveWidget):
    def __init__(self, parent, tableAlignment: str = "c", clear: bool = True,
                 x: int = None, y: int = None, width: int = 22,
                 max_symbol: int = 22, input_type: str = "str",
                 Xdo: str = "=", Ydo: str = "=", function: Callable = None):

        self._text = ""
        self._done = False
        self._max_symbol = max_symbol
        self._input_type = input_type
        self._function = function
        self.is_first_display = True
        self.text_box_win = None

        self._input_events = []

        super().__init__(parent, clear, tableAlignment, width, 3, x, y, Xdo, Ydo)

        self._init_window()

        self._register_input_handlers()

        self.draw()

    def _init_window(self):
        if self._clear:
            self._win.clear()
            self._win.refresh()

        table_x, table_y = self._calculate_position()

        self.text_box_win = curses.newwin(4, self._width + 7, table_y, table_x)

        self._cursor_x = table_x + 3
        self._cursor_y = table_y + 1
        self._win.move(self._cursor_y, self._cursor_x)

    def _register_input_handlers(self):
        for k in list(range(32, 127)) + [curses.KEY_ENTER, 10, 13, curses.KEY_BACKSPACE, 127, 8]:
            eid = lib_controller.input_controller.add_input_event(k, lambda k=k: self._on_key(k))
            self._input_events.append(eid)

    def draw(self):
        if not self.text_box_win:
            self._init_window()

        self._update_text_box()

    def _update_screen(self):
        if self.text_box_win:
            self.text_box_win.refresh()

    def _update_text_box(self):
        if not self.text_box_win:
            return

        self.text_box_win.erase()
        self._create_text_box()
        self._update_screen()

    def _create_text_box(self):
        self.text_box_win.addstr("Xx" + "_" * (self._width + 2) + "xX\n")
        if self.is_first_display:
            t.sleep(config.delayOutput)
            audio_controller.play_random_print_sound()
            self.text_box_win.refresh()

        self.text_box_win.addstr("||" + " " * (self._width + 2) + "||\n")
        if self.is_first_display:
            t.sleep(config.delayOutput)
            audio_controller.play_random_print_sound()
            self.text_box_win.refresh()

        self.text_box_win.addstr("Xx" + "¯" * (self._width + 2) + "xX\n")
        if self.is_first_display:
            t.sleep(config.delayOutput)
            audio_controller.play_random_print_sound()
            self.text_box_win.refresh()

        self.is_first_display = False
        self.text_box_win.addstr(1, 3, self._text.ljust(self._max_symbol))

    def _on_key(self, key):
        if self._pause:
            return

        if key in (curses.KEY_ENTER, 10, 13):
            self._done = True
            if self._function:
                self._function(self._text)
            return

        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if len(self._text) > 0:
                self._text = self._text[:-1]
                audio_controller.play_random_print_sound()

        elif 32 <= key <= 126:
            char = chr(key)
            if self._input_type == "int" and not char.isdigit():
                return
            if self._input_type == "float" and not (char.isdigit() or char in ".,"):
                return
            if len(self._text) < self._max_symbol:
                if self._input_type == "float" and char == ',':
                    char = '.'
                if self._input_type == "float" and char == '.' and '.' in self._text:
                    return
                self._text += char
                audio_controller.play_random_print_sound()

        self._win.move(self._cursor_y, self._cursor_x)
        self._update_text_box()
        self._win.move(self._cursor_y, self._cursor_x + len(self._text))

    def set_pause(self, pause: bool):
        super().set_pause(pause)
        for eid in self._input_events:
            eid.set_pause(pause)

        if not pause:
            curses.curs_set(1)
        else:
            curses.curs_set(0)
            
        self._update_text_box()

    def stop(self):
        for eid in self._input_events:
            eid.remove()
        super().stop()

    @property
    def text(self) -> str:
        """Получить введенный текст"""
        return self._text

    @property
    def done(self) -> bool:
        """Проверить, завершен ли ввод"""
        return self._done 