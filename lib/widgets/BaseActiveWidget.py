from abc import abstractmethod
from lib.widgets.BasePassiveWidget import BasePassiveWidget
from lib.TabControl import TabControl

class BaseActiveWidget(BasePassiveWidget):
    def __init__(self, parent, clear: bool = True, tableAlignment: str = "c", width: int = 22, height: int = 3, x: int = None, y: int = None, Xdo: str = "=", Ydo: str = "="):
        super().__init__(parent, clear, tableAlignment, width, height, x, y, Xdo, Ydo)
        self._tab_control = TabControl.get_instance()
        self._pause = False
        self._tab_control.add_widget(self)

    def toggle_pause(self):
        self.set_pause(not self._pause)

    def set_pause(self, pause: bool):
        """
        Set the pause state of the widget.
        :param pause: True to pause, False to resume.
        """
        self._pause = pause
        self.draw()

    @property
    def paused(self) -> bool:
        """
        Get the current pause state of the widget.
        :return: True if paused, False otherwise.
        """
        return self._pause

    def stop(self):
        try:
            self._tab_control.remove_widget(self)
            del self
        except ValueError:
            # Widget was not in TabControl, that's fine
            pass

    @abstractmethod
    def draw(self):
        """
        Draw the widget on the parent window.
        This method should be implemented by subclasses.
        """
        pass

    @abstractmethod
    def _update_screen(self):
        """
        Update the screen by redrawing the widget.
        This method is called after drawing the widget to refresh the display.
        """
        pass

    def _calculate_position(self) -> tuple[int, int]:
        max_y, max_x = self._win.getmaxyx()
        absolute_center_x = (max_x - self._width) // 2
        absolute_center_y = (max_y - self._height) // 2

        table_x = 0
        table_y = 0

        if self._tableAlignment == 'c':
            table_x, table_y = absolute_center_x, absolute_center_y
        elif self._tableAlignment == 'r':
            table_x = max_x - self._width - 1
            table_y = absolute_center_y
        elif self._tableAlignment == 'l':
            table_x, table_y = 1, 1

        if self._x is not None:
            table_x = self._x if self._Xdo == "=" else table_x + self._x * (1 if self._Xdo == "+" else -1)
        if self._y is not None:
            table_y = self._y if self._Ydo == "=" else table_y + self._y * (1 if self._Ydo == "+" else -1)

        return table_x, table_y