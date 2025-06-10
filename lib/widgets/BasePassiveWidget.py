from abc import ABC, abstractmethod

class BasePassiveWidget(ABC):
    def __init__(self, parent, clear: bool = True, tableAlignment: str = "c", width: int = 22, height: int = 3, x: int = None, y: int = None, Xdo: str = "=", Ydo: str = "="):
        self._parent = parent
        self._win = parent.win

        self._clear = clear

        self._tableAlignment = tableAlignment
        self._width = width
        self._height = height
        self._x, self._y = x, y
        self._Xdo, self._Ydo = Xdo, Ydo

    @abstractmethod
    def draw(self):
        """
        Draw the widget on the parent window.
        This method should be implemented by subclasses.
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
