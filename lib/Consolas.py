from typing import List, Dict, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum

from Assets.data.LevelMap import Levels

from lib.widgets.MenuWidget import MenuWidget
from lib.widgets.TextBoxWidget import TextBoxWidget
from lib.widgets.TableWidget import TableWidget
from lib.widgets.FastLoadingWidget import FastLoadingWidget
from lib.widgets.AnimationWidget import AnimationWidget
from lib.widgets.LoadingAnimationWidget import LoadingAnimationWidget
from lib.widgets.PlayerMapWidget import PlayerMapWidget
from lib.Logger import logger


class AlignmentType(Enum):
    """Типы выравнивания для виджетов"""
    CENTER = 'c'
    RIGHT = 'r'
    LEFT = 'l'


class PositionOperation(Enum):
    """Операции для позиционирования"""
    SET = "="
    ADD = "+"
    SUBTRACT = "-"


@dataclass
class Position:
    """Структура для хранения позиции"""
    x: int
    y: int


@dataclass
class WindowDimensions:
    """Размеры окна"""
    width: int
    height: int


@dataclass
class WidgetConfig:
    """Базовая конфигурация для всех виджетов"""
    alignment: AlignmentType = AlignmentType.CENTER
    x: Optional[int] = None
    y: Optional[int] = None
    x_operation: PositionOperation = PositionOperation.SET
    y_operation: PositionOperation = PositionOperation.SET
    clear: bool = True
    width: int = None
    height: int = None

@dataclass
class PlayerMapConfig:
    """Базовая конфигурация для карты"""
    map: Levels.BaseLevel = None
    alignment: AlignmentType = AlignmentType.CENTER
    x: Optional[int] = None
    y: Optional[int] = None
    x_operation: PositionOperation = PositionOperation.SET
    y_operation: PositionOperation = PositionOperation.SET
    clear: bool = True

@dataclass
class TableConfig(WidgetConfig):
    """Конфигурация для таблиц"""
    style: str = "info"
    separator_positions: Optional[List[int]] = None
    text_alignment: Optional[Dict[int, AlignmentType]] = None
    width: int = 22
    animation: bool = True


@dataclass
class MenuConfig(WidgetConfig):
    """Конфигурация для меню"""
    color: str = 'cyan'
    tips: bool = True
    info_width: int = 50
    table_width: int = 22


@dataclass
class TextBoxConfig(WidgetConfig):
    """Конфигурация для текстовых полей"""
    width: int = 22
    max_symbol: int = 22
    input_type: str = "str"
    function: Optional[Any] = None


@dataclass
class AnimationConfig(WidgetConfig):
    """Конфигурация для анимации"""
    delay: float = 0.3
    audio: bool = True


class ConsolasError(Exception):
    """Базовый класс исключений для Consolas"""
    pass


class PositionCalculationError(ConsolasError):
    """Ошибка при вычислении позиции"""
    pass


class WidgetCreationError(ConsolasError):
    """Ошибка при создании виджета"""
    pass


class Consolas:
    """
    Основной класс для управления консольным интерфейсом
    
    Предоставляет методы для создания различных виджетов UI
    и управления их позиционированием на экране.
    """
    
    def __init__(self, config: Any, win: Any) -> None:
        """
        Инициализация Consolas
        
        Args:
            config: Конфигурация приложения
            win: Окно curses
        """
        self._config = config
        self._win = win
        self._current_focus: int = 0
        self._tab_input_event: Optional[Any] = None
        self._btab_input_event: Optional[Any] = None
        self._window_dimensions_cache: Optional[WindowDimensions] = None
        
        logger.info("Consolas initialized successfully")
    
    @property
    def config(self) -> Any:
        """Получить конфигурацию"""
        return self._config

    @property
    def win(self) -> Any:
        """Получить окно curses"""
        return self._win
    
    @property
    def current_focus(self) -> int:
        """Получить текущий фокус"""
        return self._current_focus
    
    @current_focus.setter
    def current_focus(self, value: int) -> None:
        """Установить текущий фокус"""
        self._current_focus = value
    
    def clear_window(self) -> None:
        """Очистить окно и обновить отображение"""
        try:
            self._win.clear()
            self._win.refresh()
            self._window_dimensions_cache = None
            logger.debug("Window cleared successfully")
        except Exception as e:
            logger.error(f"Failed to clear window: {e}")
            raise ConsolasError(f"Window clearing failed: {e}")
    
    def _get_window_dimensions(self) -> WindowDimensions:
        """
        Получить размеры окна с кэшированием
        
        Returns:
            WindowDimensions: Размеры окна
        """
        if self._window_dimensions_cache is None:
            try:
                max_y, max_x = self._win.getmaxyx()
                self._window_dimensions_cache = WindowDimensions(max_x, max_y)
            except Exception as e:
                logger.error(f"Failed to get window dimensions: {e}")
                raise PositionCalculationError(f"Cannot get window dimensions: {e}")
        
        return self._window_dimensions_cache
    
    def _calculate_center_position(self, width: int, height: int) -> Position:
        """
        Вычислить центральную позицию
        
        Args:
            width: Ширина виджета
            height: Высота виджета
            
        Returns:
            Position: Центральная позиция
        """
        dimensions = self._get_window_dimensions()
        center_x = (dimensions.width - width) // 2
        center_y = (dimensions.height - height) // 2
        return Position(center_x, center_y)
    
    def _apply_position_operation(self, base_value: int, offset: Optional[int], 
                                 operation: PositionOperation) -> int:
        """
        Применить операцию позиционирования
        
        Args:
            base_value: Базовое значение
            offset: Смещение
            operation: Тип операции
            
        Returns:
            int: Результирующее значение
        """
        if offset is None:
            return base_value
        
        if operation == PositionOperation.SET:
            return offset
        elif operation == PositionOperation.ADD:
            return base_value + offset
        elif operation == PositionOperation.SUBTRACT:
            return base_value - offset
        else:
            raise PositionCalculationError(f"Unknown position operation: {operation}")
    
    def calculate_position(self, 
                          width: int, 
                          height: int, 
                          alignment: Union[str, AlignmentType], 
                          x: Optional[int] = None, 
                          y: Optional[int] = None, 
                          x_operation: Union[str, PositionOperation] = PositionOperation.SET, 
                          y_operation: Union[str, PositionOperation] = PositionOperation.SET) -> Tuple[int, int]:
        """
        Вычислить позицию виджета на экране
        
        Args:
            width: Ширина виджета
            height: Высота виджета
            alignment: Тип выравнивания
            x: X координата
            y: Y координата
            x_operation: Операция для X
            y_operation: Операция для Y
            
        Returns:
            Tuple[int, int]: Координаты (x, y)
            
        Raises:
            PositionCalculationError: При ошибке вычисления позиции
        """
        try:
            # Преобразуем строки в enum
            if isinstance(alignment, str):
                alignment = AlignmentType(alignment)
            if isinstance(x_operation, str):
                x_operation = PositionOperation(x_operation)
            if isinstance(y_operation, str):
                y_operation = PositionOperation(y_operation)
            
            dimensions = self._get_window_dimensions()
            
            # Базовые позиции в зависимости от выравнивания
            if alignment == AlignmentType.CENTER:
                base_position = self._calculate_center_position(width, height)
            elif alignment == AlignmentType.RIGHT:
                base_position = Position(
                    dimensions.width - width - 1,
                    self._calculate_center_position(width, height).y
                )
            elif alignment == AlignmentType.LEFT:
                base_position = Position(1, 1)
            else:
                raise PositionCalculationError(f"Unknown alignment type: {alignment}")
            
            # Применяем операции позиционирования
            final_x = self._apply_position_operation(base_position.x, x, x_operation)
            final_y = self._apply_position_operation(base_position.y, y, y_operation)
            
            # Проверяем границы
            final_x = max(0, min(final_x, dimensions.width - width))
            final_y = max(0, min(final_y, dimensions.height - height))
            
            logger.debug(f"Position calculated: ({final_x}, {final_y}) for {width}x{height} widget")
            return final_x, final_y
            
        except Exception as e:
            logger.error(f"Position calculation failed: {e}")
            raise PositionCalculationError(f"Cannot calculate position: {e}")
    
# —————————————————————————————— создание виджетов ——————————————————————————————
    
    def create_fast_loading(self, speed: float = 0.04) -> FastLoadingWidget:
        """
        Создать виджет быстрой загрузки
        
        Args:
            speed: Скорость анимации
            
        Returns:
            FastLoadingWidget: Виджет быстрой загрузки
        """
        try:
            widget = FastLoadingWidget(self, speed)
            logger.debug(f"FastLoadingWidget created with speed: {speed}")
            return widget
        except Exception as e:
            logger.error(f"Failed to create FastLoadingWidget: {e}")
            raise WidgetCreationError(f"FastLoadingWidget creation failed: {e}")
    
    def create_table(self,
                     *args: str,
                     config: Optional[TableConfig] = None,
                     **kwargs) -> TableWidget:
        """
        Создать виджет таблицы

        Args:
            *args: Содержимое таблицы
            config: Конфигурация таблицы
            **kwargs: Дополнительные параметры (для обратной совместимости)

        Returns:
            TableWidget: Виджет таблицы
        """
        try:
            # Если конфигурация не передана, создаем из kwargs
            if config is None:
                config = TableConfig(
                    style=kwargs.get('style', 'info'),
                    clear=kwargs.get('clear', True),
                    separator_positions=kwargs.get('separator_positions'),
                    text_alignment=kwargs.get('textAlignment'),
                    alignment=AlignmentType(kwargs.get('tableAlignment', 'c')),
                    width=kwargs.get('width', 22),
                    x=kwargs.get('x'),
                    y=kwargs.get('y'),
                    x_operation=PositionOperation(kwargs.get('Xdo', '=')),
                    y_operation=PositionOperation(kwargs.get('Ydo', '=')),
                    animation=kwargs.get('animation', True)
                )

            widget = TableWidget(
                self, *args,
                style=config.style,
                clear=config.clear,
                separator_positions=config.separator_positions,
                textAlignment=config.text_alignment,
                tableAlignment=config.alignment.value,
                width=config.width,
                x=config.x,
                y=config.y,
                Xdo=config.x_operation.value,
                Ydo=config.y_operation.value,
                animation=config.animation
            )

            logger.debug(f"TableWidget created with {len(args)} rows")
            return widget

        except Exception as e:
            logger.error(f"Failed to create TableWidget: {e}")
            raise WidgetCreationError(f"TableWidget creation failed: {e}")

    def create_player_map(self,
                    level_map: Levels.BaseLevel = None,  # Добавляем обязательный параметр
                    config: Optional[PlayerMapConfig] = None,
                    **kwargs) -> PlayerMapWidget:
        """
        создать виджет карты мира

        Args:
            level_map: Карта уровня (обязательный параметр)
            config: Конфигурация карты
            **kwargs: Дополнительные параметры (для обратной совместимости)

        Returns:
            PlayerMapWidget: Виджет карты мира
        """
        try:
            # Проверяем, что карта передана
            if level_map is None and 'map' not in kwargs:
                raise ValueError("level_map parameter is required")
            
            # Если конфигурация не передана, создаем из kwargs
            if config is None:
                config = PlayerMapConfig(
                    # Убираем лишний self из dataclass
                    map=level_map or kwargs.get('map', Levels.Level0()),
                    clear=kwargs.get('clear', True),
                    alignment=AlignmentType(kwargs.get('tableAlignment', 'c')),
                    x=kwargs.get('x'),
                    y=kwargs.get('y'),
                    x_operation=PositionOperation(kwargs.get('Xdo', '=')),
                    y_operation=PositionOperation(kwargs.get('Ydo', '=')),
                )

            widget = PlayerMapWidget(
                self,
                level_map=config.map or level_map,  # Используем переданную карту
                clear=config.clear,
                tableAlignment=config.alignment.value,
                x=config.x,
                y=config.y,
                Xdo=config.x_operation.value,
                Ydo=config.y_operation.value,
            )

            logger.debug(f"PlayerMapWidget created successfully")
            return widget

        except Exception as e:
            logger.error(f"Failed to create PlayerMapWidget: {e}")
            raise WidgetCreationError(f"PlayerMapWidget creation failed: {e}")

    def create_animation(self, 
                        frames: List[str], 
                        config: Optional[AnimationConfig] = None,
                        **kwargs) -> AnimationWidget:
        """
        Создать виджет анимации
        
        Args:
            frames: Кадры анимации
            config: Конфигурация анимации
            **kwargs: Дополнительные параметры (для обратной совместимости)
            
        Returns:
            AnimationWidget: Виджет анимации
        """
        try:
            if config is None:
                config = AnimationConfig(
                    delay=kwargs.get('delay', 0.3),
                    alignment=AlignmentType(kwargs.get('alignmentTable', 'c')),
                    x=kwargs.get('x'),
                    y=kwargs.get('y'),
                    clear=kwargs.get('clear', True),
                    x_operation=PositionOperation(kwargs.get('Xdo', '=')),
                    y_operation=PositionOperation(kwargs.get('Ydo', '=')),
                    audio=kwargs.get('audio', True)
                )
            
            widget = AnimationWidget(
                self, frames, config.delay, config.alignment.value,
                config.x, config.y, config.clear,
                config.x_operation.value, config.y_operation.value, config.audio
            )
            
            logger.debug(f"AnimationWidget created with {len(frames)} frames")
            return widget
            
        except Exception as e:
            logger.error(f"Failed to create AnimationWidget: {e}")
            raise WidgetCreationError(f"AnimationWidget creation failed: {e}")
    
    def create_loading_animation(self) -> LoadingAnimationWidget:
        """
        Создать виджет анимации загрузки
        
        Returns:
            LoadingAnimationWidget: Виджет анимации загрузки
        """
        try:
            widget = LoadingAnimationWidget(self)
            logger.debug("LoadingAnimationWidget created")
            return widget
        except Exception as e:
            logger.error(f"Failed to create LoadingAnimationWidget: {e}")
            raise WidgetCreationError(f"LoadingAnimationWidget creation failed: {e}")
    
    def create_menu(self, 
                    title: str, 
                    options: List[str], 
                    additional_info: Optional[Any] = None,
                    config: Optional[MenuConfig] = None,
                    **kwargs) -> MenuWidget:
        """
        Создать виджет меню
        
        Args:
            title: Заголовок меню
            options: Опции меню
            additional_info: Дополнительная информация
            config: Конфигурация меню
            **kwargs: Дополнительные параметры (для обратной совместимости)
            
        Returns:
            MenuWidget: Виджет меню
        """
        try:
            if config is None:
                config = MenuConfig(
                    alignment=AlignmentType(kwargs.get('alignment', 'c')),
                    x=kwargs.get('x'),
                    y=kwargs.get('y'),
                    color=kwargs.get('color', 'cyan'),
                    tips=kwargs.get('tips', True),
                    clear=kwargs.get('clear', True),
                    info_width=kwargs.get('info_width', 50),
                    table_width=kwargs.get('table_width', 22),
                    x_operation=PositionOperation(kwargs.get('Xdo', '=')),
                    y_operation=PositionOperation(kwargs.get('Ydo', '='))
                )
            
            widget = MenuWidget(
                self, title, options, additional_info,
                config.alignment.value, config.x, config.y, config.color,
                config.tips, config.clear, config.info_width, config.table_width,
                config.x_operation.value, config.y_operation.value
            )
            
            logger.debug(f"MenuWidget '{title}' created with {len(options)} options")
            return widget
            
        except Exception as e:
            logger.error(f"Failed to create MenuWidget: {e}")
            raise WidgetCreationError(f"MenuWidget creation failed: {e}")
    
    def create_text_box(self, 
                        config: Optional[TextBoxConfig] = None,
                        **kwargs) -> TextBoxWidget:
        """
        Создать виджет текстового поля
        
        Args:
            config: Конфигурация текстового поля
            **kwargs: Дополнительные параметры (для обратной совместимости)
            
        Returns:
            TextBoxWidget: Виджет текстового поля
        """
        try:
            if config is None:
                config = TextBoxConfig(
                    alignment=AlignmentType(kwargs.get('table_alignment', 'c')),
                    clear=kwargs.get('clear', True),
                    x=kwargs.get('x'),
                    y=kwargs.get('y'),
                    width=kwargs.get('width', 22),
                    max_symbol=kwargs.get('max_symbol', 22),
                    input_type=kwargs.get('input_type', 'str'),
                    x_operation=PositionOperation(kwargs.get('Xdo', '=')),
                    y_operation=PositionOperation(kwargs.get('Ydo', '=')),
                    function=kwargs.get('function')
                )
            
            widget = TextBoxWidget(
                self, config.alignment.value, config.clear, config.x, config.y,
                config.width, config.max_symbol, config.input_type,
                config.x_operation.value, config.y_operation.value, config.function
            )
            
            logger.debug(f"TextBoxWidget created with width: {config.width}")
            return widget
            
        except Exception as e:
            logger.error(f"Failed to create TextBoxWidget: {e}")
            raise WidgetCreationError(f"TextBoxWidget creation failed: {e}")
    
    # Методы для обратной совместимости с оригинальными названиями
    fast_loading = create_fast_loading
    play_animation = create_animation
    loading_animation = create_loading_animation