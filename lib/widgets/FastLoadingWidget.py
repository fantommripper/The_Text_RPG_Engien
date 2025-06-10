from lib.widgets.BasePassiveWidget import BasePassiveWidget
import time
import random as r

class FastLoadingWidget(BasePassiveWidget):
    def __init__(self, parent, speed=0.04):
        super().__init__(parent, width=24, height=3, Xdo="-", Ydo="-")
        self._speed = speed

        self.draw()

    def draw(self):
        if self._clear:
            self._win.clear()

        table_x, table_y = self._calculate_position()
        procent = 0

        self._win.addstr(table_y, table_x, "Xx____________________xX")
        self._win.addstr(table_y + 1, table_x, "||                    ||")
        self._win.addstr(table_y + 2, table_x, "Xx¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯xX")

        while procent < 100:
            bar_length = 20
            filled_length = int(bar_length * procent / 100)
            bar = "=" * filled_length + " " * (bar_length - filled_length)

            progress_display = f"Xx________{procent:03d}%________xX"
            self._win.addstr(table_y, table_x, progress_display)
            self._win.addstr(table_y + 1, table_x + 2, bar)
            self._win.refresh()

            procent += r.randint(1, 3)
            procent = min(procent, 100)

            time.sleep(self._speed)

        progress_display = "Xx________100%________xX"
        bar = "=" * bar_length
        self._win.addstr(table_y, table_x, progress_display)
        self._win.addstr(table_y + 1, table_x + 2, bar)
        self._win.refresh()

        time.sleep(0.5)
        self._win.clear() 