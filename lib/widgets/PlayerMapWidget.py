import curses

from Assets.data.LevelMap import Levels
from lib.widgets.BaseActiveWidget import BaseActiveWidget
from lib.Logger import logger
from Assets.controller.LibController import lib_controller


class PlayerMapWidget(BaseActiveWidget):
    def __init__(self, parent, level_map: Levels.BaseLevel, width: int = None, height: int = None, 
                 clear=True, tableAlignment="c", x=None, y=None, Xdo="=", Ydo="="):

        # Проверяем, что level_map передан и не None
        if level_map is None:
            raise ValueError("level_map parameter is required and cannot be None")
        
        self.level_map = level_map
        if not hasattr(self.level_map, 'level_map') or not self.level_map.level_map:
            raise ValueError("Map data cannot be empty")

        self._input_events = []
        self.map_win = None

        # Устанавливаем начальную позицию игрока
        self.player_x = getattr(self.level_map, 'PlayerSpawnX', 0)
        self.player_y = getattr(self.level_map, 'PlayerSpawnY', 0)

        # Вычисляем размеры карты
        self.map_width = len(self.level_map.level_map[0]) if self.level_map.level_map else 0
        self.map_height = len(self.level_map.level_map)

        # Устанавливаем размеры виджета (добавляем +2 для рамки)
        if width is None:
            width = self.map_width + 2
        if height is None:
            height = self.map_height + 2

        # Вызываем конструктор родительского класса
        super().__init__(parent, clear, tableAlignment, width, height, x, y, Xdo, Ydo)

        # Инициализируем цвета и обработчики
        self._init_colors()
        self._register_input_handlers()
        
        # Проверяем начальную позицию игрока
        if not self._can_move_to(self.player_x, self.player_y):
            # Если начальная позиция недоступна, ищем первое свободное место
            self._find_valid_spawn_position()
        
        self.draw()
    
    def _find_valid_spawn_position(self):
        """Находит первую доступную позицию для спавна игрока"""
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self._can_move_to(x, y):
                    self.player_x = x
                    self.player_y = y
                    logger.info(f"Player spawn position set to ({x}, {y})")
                    return
        
        # Если не найдено свободного места, устанавливаем в (0, 0)
        self.player_x = 0
        self.player_y = 0
        logger.warning("No valid spawn position found, setting to (0, 0)")
    
    def _init_colors(self):
        """Инициализация цветовых пар"""
        try:
            curses.start_color()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Обычный текст
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)      # Стены/препятствия
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Игрок (активный)
            curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)     # Игрок (на паузе)
            curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Специальные объекты
        except curses.error as e:
            logger.warning(f"Color initialization failed: {e}")
    
    def _register_input_handlers(self):
        """Регистрация обработчиков ввода для движения игрока"""
        try:
            # Очищаем старые обработчики если они есть
            self._clear_input_handlers()

            movement_keys = [
                # WASD + диагонали (Q W E / A D / Z X C)
                ('q', self._move_up_left),    ('Q', self._move_up_left),
                ('w', self._move_up),         ('W', self._move_up),
                ('e', self._move_up_right),   ('E', self._move_up_right),
                ('a', self._move_left),       ('A', self._move_left),
                ('d', self._move_right),      ('D', self._move_right),
                ('z', self._move_down_left),  ('Z', self._move_down_left),
                ('x', self._move_down),       ('X', self._move_down),
                ('c', self._move_down_right), ('C', self._move_down_right),
                
                # Numpad альтернатива
                ('7', self._move_up_left),    ('8', self._move_up),
                ('9', self._move_up_right),   ('4', self._move_left),
                ('6', self._move_right),      ('1', self._move_down_left),
                ('2', self._move_down),       ('3', self._move_down_right),
            ]
            
            self._input_events = []
            for key, handler in movement_keys:
                try:
                    event = lib_controller.input_controller.add_input_event(ord(key), handler)
                    if event:
                        self._input_events.append(event)
                except Exception as e:
                    logger.warning(f"Failed to register key '{key}': {e}")
                    
        except Exception as e:
            logger.error(f"Failed to register input handlers: {e}")
            self._input_events = []
    
    def _clear_input_handlers(self):
        """Очищает все зарегистрированные обработчики ввода"""
        if hasattr(self, '_input_events') and self._input_events:
            for event in self._input_events:
                try:
                    if event and hasattr(event, 'remove'):
                        event.remove()
                except Exception as e:
                    logger.warning(f"Failed to remove input event: {e}")
            self._input_events = []
    
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
        cell = self.level_map.level_map[y][x]
        return cell != '*' and cell != '#'  # Добавляем проверку на '#' как альтернативный символ стены
    
    def _move_player(self, dx: int, dy: int):
        """Универсальный метод движения игрока"""
        if hasattr(self, '_pause') and self._pause:
            return
            
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        
        if self._can_move_to(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y
            self.draw()
            logger.debug(f"Player moved to ({self.player_x}, {self.player_y})")

    # Методы движения (используют универсальный _move_player)
    def _move_up(self):           self._move_player(0, -1)
    def _move_down(self):         self._move_player(0, 1)
    def _move_left(self):         self._move_player(-1, 0)
    def _move_right(self):        self._move_player(1, 0)
    def _move_up_left(self):      self._move_player(-1, -1)
    def _move_up_right(self):     self._move_player(1, -1)
    def _move_down_left(self):    self._move_player(-1, 1)
    def _move_down_right(self):   self._move_player(1, 1)
    
    def draw(self):
        """Отрисовка карты с игроком"""
        try:
            if not self.map_win:
                self._init_window()
            
            if self.map_win:
                self._draw_map()
                self._update_screen()
        except Exception as e:
            logger.error(f"Error drawing map: {e}")
    
    def _init_window(self):
        """Инициализация окна для отображения карты"""
        try:
            # Очищаем родительское окно если нужно
            if hasattr(self, '_clear') and self._clear and hasattr(self, '_win') and self._win:
                self._win.clear()
                self._win.refresh()
            
            # Вычисляем позицию и создаем окно
            table_x, table_y = self._calculate_position()
            
            # Проверяем, что позиция корректна
            if table_x >= 0 and table_y >= 0:
                self.map_win = curses.newwin(self._height, self._width, table_y, table_x)
                logger.debug(f"Map window created at ({table_x}, {table_y}) with size {self._width}x{self._height}")
            else:
                logger.error(f"Invalid window position: ({table_x}, {table_y})")
                
        except Exception as e:
            logger.error(f"Error initializing window: {e}")
            self.map_win = None
    
    def _draw_map(self):
        """Отрисовка карты"""
        if not self.map_win:
            logger.warning("Map window not initialized")
            return
            
        try:
            self.map_win.erase()
            
            # Определяем цвет рамки в зависимости от состояния паузы
            pause_state = getattr(self, '_pause', False)
            border_color = curses.color_pair(4) if pause_state else curses.color_pair(1)
            
            # Рисуем рамку
            try:
                self.map_win.attron(border_color)
                self.map_win.box()  # Включаем рамку
                self.map_win.attroff(border_color)
            except curses.error:
                logger.warning("Failed to draw border")

            # Отрисовываем содержимое карты
            if self.level_map.level_map:
                self._draw_map_content(pause_state)
                
        except Exception as e:
            logger.error(f"Error drawing map content: {e}")
    
    def _draw_map_content(self, pause_state: bool):
        """Отрисовка содержимого карты"""
        for y, row in enumerate(self.level_map.level_map):
            if y >= self.map_height:
                break
                
            for x, cell in enumerate(row):
                if x >= self.map_width:
                    break
                
                # Определяем что отображать и каким цветом
                display_char, color_pair = self._get_cell_display(x, y, cell, pause_state)
                
                # Отображаем символ (смещение +1 для рамки)
                try:
                    screen_y = y + 1
                    screen_x = x + 1
                    
                    if (0 < screen_y < self._height - 1 and 
                        0 < screen_x < self._width - 1):
                        self.map_win.addch(screen_y, screen_x, display_char, color_pair)
                        
                except curses.error:
                    # Игнорируем ошибки позиционирования
                    pass
    
    def _get_cell_display(self, x: int, y: int, cell: str, pause_state: bool) -> tuple[str, int]:
        """Определяет символ и цвет для отображения ячейки"""
        # Если это позиция игрока
        if x == self.player_x and y == self.player_y:
            display_char = '@'
            color_pair = curses.color_pair(4) if pause_state else curses.color_pair(3)
        else:
            display_char = cell
            if cell in ['*', '#']:  # Стены
                color_pair = curses.color_pair(2)
            else:
                color_pair = curses.color_pair(1)

            if pause_state:
                color_pair = curses.color_pair(4)
        
        return display_char, color_pair
    
    def _update_screen(self):
        """Обновление экрана"""
        try:
            if self.map_win:
                self.map_win.refresh()
        except Exception as e:
            logger.error(f"Error refreshing screen: {e}")

    def set_pause(self, pause: bool):
        """Установка состояния паузы"""
        try:
            super().set_pause(pause)
            
            # Устанавливаем паузу для всех обработчиков ввода
            if hasattr(self, '_input_events') and self._input_events:
                for event in self._input_events:
                    try:
                        if event and hasattr(event, 'set_pause'):
                            event.set_pause(pause)
                    except Exception as e:
                        logger.warning(f"Error setting pause for event: {e}")
            
            # Перерисовываем карту с учетом нового состояния
            self.draw()
            
        except Exception as e:
            logger.error(f"Error in set_pause: {e}")
    
    def stop(self):
        """Остановка виджета и очистка ресурсов"""
        try:
            # Очищаем все обработчики ввода
            self._clear_input_handlers()
            
            # Удаляем окно карты
            if self.map_win:
                try:
                    self.map_win.clear()
                    self.map_win.refresh()
                except curses.error:
                    pass
                self.map_win = None
            
            # Вызываем родительский метод
            super().stop()
            
        except Exception as e:
            logger.error(f"Error in stop method: {e}")
    
    def get_player_position(self) -> tuple[int, int]:
        """Возвращает текущую позицию игрока"""
        return self.player_x, self.player_y
    
    def set_player_position(self, x: int, y: int) -> bool:
        """
        Устанавливает позицию игрока (если позиция допустима)
        
        Returns:
            bool: True если позиция установлена успешно, False если позиция недоступна
        """
        if self._can_move_to(x, y):
            self.player_x = x
            self.player_y = y
            self.draw()
            logger.info(f"Player position set to ({x}, {y})")
            return True
        else:
            logger.warning(f"Cannot move player to position ({x}, {y}) - position not available")
            return False
    
    def get_map_info(self) -> dict:
        """Возвращает информацию о карте"""
        return {
            'width': self.map_width,
            'height': self.map_height,
            'player_x': self.player_x,
            'player_y': self.player_y,
            'spawn_x': getattr(self.level_map, 'PlayerSpawnX', 0),
            'spawn_y': getattr(self.level_map, 'PlayerSpawnY', 0)
        }