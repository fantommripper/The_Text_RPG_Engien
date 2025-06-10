import curses
from typing import Dict, List, Callable
import time as t

from lib.widgets.BaseActiveWidget import BaseActiveWidget
from controller.AudioController import audio_controller
from controller.LibController import lib_controller
from data.Config import config

class MenuWidget(BaseActiveWidget):
    def __init__(self, parent, title: str, options: Dict[str, Callable],
                 additional_info: List[str] = None, tableAlignment: str = "c",
                 x: int = None, y: int = None, color: str = 'cyan',
                 tips: bool = True, clear: bool = True,
                 info_width: int = 50, table_width: int = 22,
                 Xdo: str = "=", Ydo: str = "="):

        self.title = title
        self.option_handlers = options
        self.options = list(options.keys())
        self.additional_info = additional_info or ["" for _ in options]
        self.color = color
        self.tips = tips
        self.info_width = info_width

        self.option = 0
        self.is_first_display = True
        self.win = parent.win
        self.menu_win = None
        self.info_win = None

        self._input_event_up = None
        self._input_event_down = None
        self._input_event_enter = []

        self._register_input_handlers()

        super().__init__(parent, clear, tableAlignment, table_width, len(options) + 5, x, y, Xdo, Ydo)

        self._init_colors()

        self._init_windows()

        self.draw()

    def _init_windows(self):
        if self._clear:
            self._win.clear()
            self._win.refresh()

        table_x, table_y = self._calculate_position()

        self.menu_win = curses.newwin(len(self.options) + 5, 30, table_y, table_x)

        if self.tips:
            self.info_x, self.info_y = table_x + 35, table_y
            self.info_win = curses.newwin(len(self.options) + 5, self.info_width, self.info_y, self.info_x)

    def _init_colors(self):
        icol = {1: 'red', 2: 'green', 3: 'yellow', 4: 'blue',
                5: 'magenta', 6: 'cyan', 7: 'white'}
        col = {v: k for k, v in icol.items()}
        bc = curses.COLOR_BLACK

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, bc)
        curses.init_pair(2, col[self.color], bc)
        curses.init_pair(3, curses.COLOR_WHITE, bc)

    def _register_input_handlers(self):
        self._input_event_up = lib_controller.input_controller.add_input_event(curses.KEY_UP, self._option_up)
        self._input_event_down = lib_controller.input_controller.add_input_event(curses.KEY_DOWN, self._option_down)
        self._input_event_enter = [
            lib_controller.input_controller.add_input_event(curses.KEY_ENTER, self._option_enter),
            lib_controller.input_controller.add_input_event(10, self._option_enter),
            lib_controller.input_controller.add_input_event(13, self._option_enter)
        ]

    def draw(self):
        if not self.menu_win:
            self._init_windows()

        self._update_menu()

    def _update_screen(self):
        if self.menu_win:
            self.menu_win.refresh()
        if self.tips and self.info_win:
            self.info_win.refresh()

    def _update_menu(self):
        if not self.menu_win:
            return
            
        self.menu_win.erase()
        if self.tips:
            self._update_info_window()
        self._create_table()
        self._update_screen()
        self.is_first_display = False

    def _update_info_window(self):
        self.info_win.erase()
        box_color = curses.color_pair(3) if self._pause else curses.color_pair(1)
        self.info_win.attron(box_color)
        self.info_win.box()
        self.info_win.attroff(box_color)
        self._display_info()

    def _display_info(self):
        color = 3 if self._pause else 1
        self.info_win.attron(curses.color_pair(color))
        info_lines = self.additional_info[self.option].split('\n')
        for i, line in enumerate(info_lines, start=1):
            self.info_win.addstr(i, 1, line)
        self.info_win.attroff(curses.color_pair(color))

    def _create_table(self):
        main_color = 3 if self._pause else 1
        selected_color = 3 if self._pause else 2

        self.menu_win.addstr("Xx" + "_" * (self._width + 2) + "xX\n", curses.color_pair(main_color))
        if self.is_first_display:
            t.sleep(config.delayOutput)
            audio_controller.play_random_print_sound()
            self.menu_win.refresh()

        self.menu_win.addstr("|| {:^{width}} ||\n".format(self.title, width=self._width),
                            curses.color_pair(main_color))
        if self.is_first_display:
            t.sleep(config.delayOutput)
            audio_controller.play_random_print_sound()
            self.menu_win.refresh()

        self.menu_win.addstr("||" + "-" * (self._width + 2) + "||\n", curses.color_pair(main_color))
        if self.is_first_display:
            t.sleep(config.delayOutput)
            audio_controller.play_random_print_sound()
            self.menu_win.refresh()

        for index, option in enumerate(self.options):
            if index == self.option and not self._pause:
                option_str = "> {:<{width}}".format(option, width=self._width - 2)
                self.menu_win.addstr("|| ", curses.color_pair(main_color))
                self.menu_win.addstr(option_str, curses.color_pair(selected_color))
                self.menu_win.addstr(" ||\n", curses.color_pair(main_color))
            else:
                option_str = "  {:<{width}}".format(option, width=self._width - 2)
                self.menu_win.addstr("|| ", curses.color_pair(main_color))
                self.menu_win.addstr(option_str, curses.color_pair(main_color))
                self.menu_win.addstr(" ||\n", curses.color_pair(main_color))
            
            if self.is_first_display:
                t.sleep(config.delayOutput)
                audio_controller.play_random_print_sound()
                self.menu_win.refresh()

        self.menu_win.addstr("Xx" + "¯" * (self._width + 2) + "xX\n", curses.color_pair(main_color))

    def _option_up(self):
        if not self._pause:
            self.option = (self.option - 1) % len(self.options)
            audio_controller.play_random_print_sound()
            self._update_menu()

    def _option_down(self):
        if not self._pause:
            self.option = (self.option + 1) % len(self.options)
            audio_controller.play_random_print_sound()
            self._update_menu()

    def _option_enter(self):
        if not self._pause:
            selected_option = self.options[self.option]
            self.option_handlers[selected_option]()
            audio_controller.play_random_print_sound()

    def set_pause(self, pause: bool):
        super().set_pause(pause)
        self._input_event_up.set_pause(pause)
        self._input_event_down.set_pause(pause)
        for eid in self._input_event_enter:
            eid.set_pause(pause)

        if not pause:
            curses.curs_set(0)
        self._update_menu()

    def stop(self):
        self._input_event_up.remove()
        self._input_event_down.remove()
        for eid in self._input_event_enter:
            eid.remove()
        super().stop()