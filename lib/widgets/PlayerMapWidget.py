import curses

from data.LevelMap import Levels
from lib.widgets.BaseActiveWidget import BaseActiveWidget
from lib.Logger import logger
from controller.LibController import lib_controller


class PlayerMapWidget(BaseActiveWidget):
    def __init__(self, parent, level_map: Levels.BaseLevel, width:int = None, height:int = None, clear=True, tableAlignment="c",
                 x=None, y=None, Xdo="=", Ydo="="):

        self.level_map = level_map
        if not self.level_map:
            raise ValueError("Map cannot be empty")

        self._input_events = []

        self.player_x = self.level_map.PlayerSpawnX
        self.player_y = self.level_map.PlayerSpawnY

        self.map_width = len(self.level_map.level_map[0]) if self.level_map.level_map else 0
        self.map_height = len(self.level_map.level_map)

        if width is None:
            width = self.map_width + 2
        if height is None:
            height = self.map_height + 2

        self.map_win = None

        super().__init__(parent, clear, tableAlignment, width, height, x, y, Xdo, Ydo)

        self._register_input_handlers()

        self._init_colors()
        
        self.draw()
    
    def _init_colors(self):
        """Инициализация цветовых пар"""
        try:
            curses.start_color()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        except curses.error:
            pass
    
    def _register_input_handlers(self):
        """Регистрация обработчиков ввода для движения игрока"""
        try:
            self._input_events = [
                # Диагональное управление Q W E / A D / Z X C
                # Верхний ряд
                lib_controller.input_controller.add_input_event(ord('q'), self._move_up_left),     # q - вверх-влево
                lib_controller.input_controller.add_input_event(ord('Q'), self._move_up_left),
                lib_controller.input_controller.add_input_event(ord('w'), self._move_up),          # w - вверх
                lib_controller.input_controller.add_input_event(ord('W'), self._move_up),
                lib_controller.input_controller.add_input_event(ord('e'), self._move_up_right),    # e - вверх-вправо
                lib_controller.input_controller.add_input_event(ord('E'), self._move_up_right),
                
                # Средний ряд
                lib_controller.input_controller.add_input_event(ord('a'), self._move_left),        # a - влево
                lib_controller.input_controller.add_input_event(ord('A'), self._move_left),
                lib_controller.input_controller.add_input_event(ord('d'), self._move_right),       # d - вправо
                lib_controller.input_controller.add_input_event(ord('D'), self._move_right),
                
                # Нижний ряд
                lib_controller.input_controller.add_input_event(ord('z'), self._move_down_left),   # z - вниз-влево
                lib_controller.input_controller.add_input_event(ord('Z'), self._move_down_left),
                lib_controller.input_controller.add_input_event(ord('x'), self._move_down),        # x - вниз
                lib_controller.input_controller.add_input_event(ord('X'), self._move_down),
                lib_controller.input_controller.add_input_event(ord('c'), self._move_down_right),  # c - вниз-вправо
                lib_controller.input_controller.add_input_event(ord('C'), self._move_down_right),
                
                # Альтернативное управление на numpad (7 8 9 / 4 6 / 1 2 3)
                lib_controller.input_controller.add_input_event(ord('7'), self._move_up_left),     # 7 - вверх-влево
                lib_controller.input_controller.add_input_event(ord('8'), self._move_up),          # 8 - вверх
                lib_controller.input_controller.add_input_event(ord('9'), self._move_up_right),    # 9 - вверх-вправо
                lib_controller.input_controller.add_input_event(ord('4'), self._move_left),        # 4 - влево
                lib_controller.input_controller.add_input_event(ord('6'), self._move_right),       # 6 - вправо
                lib_controller.input_controller.add_input_event(ord('1'), self._move_down_left),   # 1 - вниз-влево
                lib_controller.input_controller.add_input_event(ord('2'), self._move_down),        # 2 - вниз
                lib_controller.input_controller.add_input_event(ord('3'), self._move_down_right),  # 3 - вниз-вправо

            ]
        except Exception as e:
            self._input_events = []
            logger.warning(f"Failed to register input handlers: {e}")
    
    def _can_move_to(self, x: int, y: int) -> bool:
        """Проверяет, можно ли переместиться в указанную позицию"""
        # Проверяем границы карты
        if y < 0 or y >= self.map_height or x < 0 or x >= self.map_width:
            return False
        
        # Проверяем, что карта существует и имеет нужную строку
        if not self.level_map.level_map or y >= len(self.level_map.level_map):
            return False
            
        # Проверяем, что строка имеет нужную длину
        if x >= len(self.level_map.level_map[y]):
            return False
        
        # Проверяем, что это не стена (символ '*')
        if self.level_map.level_map[y][x] == '*':
            return False
        
        return True
    
    def _move_up(self):
        """Движение вверх"""
        if hasattr(self, '_pause') and not self._pause and self._can_move_to(self.player_x, self.player_y - 1):
            self.player_y -= 1
            self.draw()
    
    def _move_down(self):
        """Движение вниз"""
        if hasattr(self, '_pause') and not self._pause and self._can_move_to(self.player_x, self.player_y + 1):
            self.player_y += 1
            self.draw()
    
    def _move_left(self):
        """Движение влево"""
        if hasattr(self, '_pause') and not self._pause and self._can_move_to(self.player_x - 1, self.player_y):
            self.player_x -= 1
            self.draw()
    
    def _move_right(self):
        """Движение вправо"""
        if hasattr(self, '_pause') and not self._pause and self._can_move_to(self.player_x + 1, self.player_y):
            self.player_x += 1
            self.draw()
    
    def _move_up_left(self):
        """Движение вверх-влево (диагональ)"""
        if (hasattr(self, '_pause') and not self._pause and 
            self._can_move_to(self.player_x - 1, self.player_y - 1)):
            self.player_x -= 1
            self.player_y -= 1
            self.draw()
    
    def _move_up_right(self):
        """Движение вверх-вправо (диагональ)"""
        if (hasattr(self, '_pause') and not self._pause and 
            self._can_move_to(self.player_x + 1, self.player_y - 1)):
            self.player_x += 1
            self.player_y -= 1
            self.draw()
    
    def _move_down_left(self):
        """Движение вниз-влево (диагональ)"""
        if (hasattr(self, '_pause') and not self._pause and 
            self._can_move_to(self.player_x - 1, self.player_y + 1)):
            self.player_x -= 1
            self.player_y += 1
            self.draw()
    
    def _move_down_right(self):
        """Движение вниз-вправо (диагональ)"""
        if (hasattr(self, '_pause') and not self._pause and 
            self._can_move_to(self.player_x + 1, self.player_y + 1)):
            self.player_x += 1
            self.player_y += 1
            self.draw()
    
    def draw(self):
        """Отрисовка карты с игроком"""
        try:
            if not self.map_win:
                self._init_window()
            
            self._draw_map()
            self._update_screen()
        except Exception as e:
            logger.error(f"drawing map: {e}")
    
    def _init_window(self):
        """Инициализация окна для отображения карты"""
        try:
            if hasattr(self, '_clear') and self._clear and hasattr(self, '_win') and self._win:
                self._win.clear()
                self._win.refresh()
            
            table_x, table_y = self._calculate_position()
            self.map_win = curses.newwin(self._height, self._width, table_y, table_x)
        except Exception as e:
            logger.error(f"initializing window: {e}")
    
    def _draw_map(self):
        """Отрисовка карты"""
        if not self.map_win:
            return
            
        try:
            self.map_win.erase()
            
            # Цвет для рамки и текста (зависит от состояния паузы)
            pause_state = getattr(self, '_pause', False)
            border_color = curses.color_pair(4) if pause_state else curses.color_pair(1)
            
            # Рисуем рамку
            self.map_win.attron(border_color)
            #self.map_win.box()
            self.map_win.attroff(border_color)

            # Отрисовываем каждую строку карты
            if self.level_map.level_map:
                for y, row in enumerate(self.level_map.level_map):
                    if y >= self.map_height:
                        break
                    for x, char in enumerate(row):
                        if x >= self.map_width:
                            break
                            
                        # Определяем, что отображать в этой позиции
                        display_char = char
                        color_pair = curses.color_pair(1)  # По умолчанию белый
                        
                        # Если это позиция игрока, отображаем игрока
                        if x == self.player_x and y == self.player_y:
                            display_char = '@'
                            color_pair = curses.color_pair(3) if not pause_state else curses.color_pair(4)
                        # Остальные символы обычным цветом
                        else:
                            color_pair = curses.color_pair(1) if not pause_state else curses.color_pair(4)
                        
                        # Отображаем символ (смещение +1 для рамки)
                        try:
                            # Проверяем, что позиция находится в пределах окна
                            if y + 1 < self._height - 1 and x + 1 < self._width - 1:
                                self.map_win.addch(y + 1, x + 1, display_char, color_pair)
                        except curses.error:
                            # Игнорируем ошибки, если символ не помещается
                            pass
        except Exception as e:
            logger.error(f"drawing map content: {e}")
    
    def _update_screen(self):
        """Обновление экрана"""
        try:
            if self.map_win:
                self.map_win.refresh()
        except Exception as e:
            logger.error(f"refreshing screen: {e}")

    def set_pause(self, pause: bool):
        """Установка состояния паузы"""
        try:
            super().set_pause(pause)
            
            # Устанавливаем паузу для всех обработчиков ввода
            # Проверяем, что _input_events существует и является списком
            if hasattr(self, '_input_events') and isinstance(self._input_events, list):
                for event in self._input_events:
                    if event and hasattr(event, 'set_pause'):
                        try:
                            event.set_pause(pause)
                        except Exception as e:
                            logger.error(f"setting pause for event: {e}")
            
            # Перерисовываем карту с учетом нового состояния
            self.draw()
        except Exception as e:
            logger.error(f"in set_pause: {e}")
    
    def stop(self):
        """Остановка виджета и очистка ресурсов"""
        try:
            # Удаляем все обработчики ввода
            if hasattr(self, '_input_events') and isinstance(self._input_events, list):
                for event in self._input_events:
                    if event and hasattr(event, 'remove'):
                        try:
                            event.remove()
                        except Exception as e:
                            logger.error(f"removing event: {e}")
            
            # Очищаем список обработчиков
            self._input_events = []
            
            super().stop()
        except Exception as e:
            logger.error(f"in stop method: {e}")
    
    def get_player_position(self) -> tuple[int, int]:
        """Возвращает текущую позицию игрока"""
        return self.player_x, self.player_y
    
    def set_player_position(self, x: int, y: int):
        """Устанавливает позицию игрока (если позиция допустима)"""
        if self._can_move_to(x, y):
            self.player_x = x
            self.player_y = y
            self.draw()
        else:
            raise ValueError(f"Cannot move player to position ({x}, {y})")