import curses
import time as t

from lib.widgets.BasePassiveWidget import BasePassiveWidget
from lib.Logger import logger
from Assets.controller.AudioController import audio_controller
from Assets.data.Config import config

class TableWidget(BasePassiveWidget):
    def __init__(self, parent, *args, style="info", clear=True, separator_positions=None,
                    textAlignment=None, tableAlignment="c", width=22, x=None, y=None,
                    Xdo="=", Ydo="=", animation:bool = True):

        self._text = [arg for arg in args if isinstance(arg, str)]
        self._style = style
        self._separator_positions = separator_positions or []
        self._textAlignment = textAlignment or {0: "l"}
        self._animation = animation

        super().__init__(parent, clear, tableAlignment, width + 7, len(self._text) + 2, x, y, Xdo, Ydo)
        self._width = width

        self._init_pad()
        self.draw()

    def _init_pad(self):
        self.table_x, self.table_y = self._calculate_position()
        self.table_pad = curses.newpad(self._height + 10, self._width + 20)

    def draw(self):
        if self._clear:
            self._win.clear()
            self._win.refresh()

        if not self.table_pad:
            self._init_pad()
        self.table_pad.refresh(0, 0, self.table_y, self.table_x,
                               self.table_y + self._height + 1,
                               self.table_x + self._width + 6)

        self.table_y_pad = 0
        self._draw_table_header()
        self._draw_table_content()
        self._draw_table_footer()
        self.table_pad.refresh(0, 0, self.table_y, self.table_x,
                               self.table_y + self._height + 1,
                               self.table_x + self._width + 6)

    def _draw_table_header(self):
        if self._style == "info":
            self._separator_up_info()
        elif self._style == "error":
            self._separator_up_error()

        if self._animation : t.sleep(config.delayOutput)
        audio_controller.play_random_print_sound()
        self.table_pad.refresh(0, 0, self.table_y, self.table_x,
                               self.table_y + self._height + 1,
                               self.table_x + self._width + 6)

    def _draw_table_content(self):
        for index, row in enumerate(self._text):
            if self._animation : t.sleep(config.delayOutput)
            self.table_pad.refresh(0, 0, self.table_y, self.table_x,
                                   self.table_y + self._height + 1,
                                   self.table_x + self._width + 6)

            if len(row) > self._width:
                self._draw_long_row(row)
            else:
                self._draw_short_row(row, index)

            if self._separator_positions and index in self._separator_positions:
                self._draw_separator()

    def _draw_table_footer(self):
        if self._animation : t.sleep(config.delayOutput)
        audio_controller.play_random_print_sound()

        if self._style == "info":
            self._separator_down_info()
        elif self._style == "error":
            self._separator_down_error()
        self.table_pad.refresh(0, 0, self.table_y, self.table_x,
                               self.table_y + self._height + 1,
                               self.table_x + self._width + 6)

    def _draw_long_row(self, row):
        words = row.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= self._width:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        for line in lines:
            formatted_line = " ".join(line.strip().split())
            self._write_line(formatted_line)

    def _draw_short_row(self, row, index):
        if self._textAlignment and index in self._textAlignment:
            align = self._textAlignment[index]
            if align == "c":
                format_spec = "{:^{width}}"
            elif align == "r":
                format_spec = "{:>{width}}"
            elif align == "l":
                format_spec = "{:<{width}}"
            else:
                logger.warning(f"Invalid alignment '{align}' for row {index}, defaulting to left alignment.")
                format_spec = "{:<{width}}"
        else:
            format_spec = "{:<{width}}"

        self._write_line(row, format_spec)

    def _write_line(self, text, format_spec="{:<{width}}"):
        border = "||" if self._style == "info" else "!!!"
        try:
            line = f"{border} {format_spec.format(text, width=self._width)} {border}"
            max_w = self.table_pad.getmaxyx()[1]
            if len(line) > max_w:
                line = line[:max_w]
            self.table_pad.addstr(self.table_y_pad, 0, line)
            self.table_y_pad += 1
            audio_controller.play_random_print_sound()
        except ValueError as e:
            logger.error(f"Error formatting line with text='{text}', format_spec='{format_spec}': {e}")
            raise

    def _draw_separator(self):
        if self._style == "info":
            self._separator_center_info()
        elif self._style == "error":
            self._separator_center_error()

    def _separator_up_info(self):
        self._draw_separator_line("Xx", "_", "xX")

    def _separator_center_info(self):
        self._draw_separator_line("||", "-", "||")

    def _separator_down_info(self):
        self._draw_separator_line("Xx", "¯", "xX")

    def _separator_up_error(self):
        self._draw_separator_line(">>>", "═", "<<<")

    def _separator_center_error(self):
        self._draw_separator_line("!!!", "-", "!!!")

    def _separator_down_error(self):
        self._draw_separator_line(">>>", "═", "<<<")

    def _draw_separator_line(self, left, middle, right):
        line = f"{left}{middle * (self._width + 2)}{right}"
        max_w = self.table_pad.getmaxyx()[1]
        if len(line) > max_w:
            line = line[:max_w]
        self.table_pad.addstr(self.table_y_pad, 0, line)
        self.table_y_pad += 1