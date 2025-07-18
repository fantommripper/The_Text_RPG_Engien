import ctypes
import curses
import os
import sys
from typing import Optional, Tuple, Any, Protocol, runtime_checkable
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

import pyautogui
import keyboard
import pygetwindow as gw

from lib.Logger import logger
from lib.SaveManager import save_manager
from controller.AudioController import AudioController


class TerminalState(Enum):
    """Terminal states"""
    NORMAL = "normal"
    MAXIMIZED = "maximized" 
    FULLSCREEN = "fullscreen"
    MINIMIZED = "minimized"


class ExitCode(Enum):
    """Exit codes"""
    SUCCESS = 0
    ERROR = 1
    FORCE_EXIT = 2


@dataclass(frozen=True)
class WindowDimensions:
    """Window dimensions"""
    width: int
    height: int
    
    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Window dimensions must be positive")


@dataclass(frozen=True)
class WindowPosition:
    """Window position"""
    x: int
    y: int


@dataclass
class TerminalInfo:
    """Terminal information"""
    title: Optional[str]
    dimensions: Optional[WindowDimensions]
    position: Optional[WindowPosition]
    state: TerminalState
    is_active: bool


# Windows API структуры с правильной типизацией
class COORD(ctypes.Structure):
    """Windows console coordinates"""
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
    
    def __repr__(self) -> str:
        return f"COORD(X={self.X}, Y={self.Y})"


class SMALL_RECT(ctypes.Structure):
    """Windows console rectangle"""
    _fields_ = [
        ("Left", ctypes.c_short),
        ("Top", ctypes.c_short),
        ("Right", ctypes.c_short),
        ("Bottom", ctypes.c_short)
    ]
    
    def __repr__(self) -> str:
        return f"SMALL_RECT(Left={self.Left}, Top={self.Top}, Right={self.Right}, Bottom={self.Bottom})"


class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    """Windows console screen buffer information"""
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD), 
        ("wAttributes", ctypes.c_ushort),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD)
    ]
    
    def __repr__(self) -> str:
        return (f"CONSOLE_SCREEN_BUFFER_INFO("
                f"dwSize={self.dwSize}, "
                f"dwCursorPosition={self.dwCursorPosition}, "
                f"wAttributes={self.wAttributes}, "
                f"srWindow={self.srWindow}, "
                f"dwMaximumWindowSize={self.dwMaximumWindowSize})")


@runtime_checkable
class WindowProtocol(Protocol):
    """Window protocol"""
    title: str
    
    def maximize(self) -> None: ...
    def minimize(self) -> None: ...
    def close(self) -> None: ...


class ConsoleSettingsError(Exception):
    """Base exception class for ConsoleSettings"""
    pass


class WindowNotFoundError(ConsoleSettingsError):
    """Window not found error"""
    pass


class TerminalOperationError(ConsoleSettingsError):
    """Terminal operation error"""
    pass


class CursesWindowError(ConsoleSettingsError):
    """Curses window error"""
    pass


class IWindowManager(ABC):
    """Abstract interface for window management"""
    
    @abstractmethod
    def get_active_window_title(self) -> Optional[str]:
        """Получить заголовок активного окна"""
        pass
    
    @abstractmethod
    def find_windows_by_title(self, title: str) -> list:
        """Найти окна по заголовку"""
        pass
    
    @abstractmethod
    def maximize_window(self, window: Any) -> bool:
        """Максимизировать окно"""
        pass


class WindowManager(IWindowManager):
    """Window manager implementation using pygetwindow"""
    
    def __init__(self) -> None:
        self._last_active_window: Optional[str] = None
        self._window_cache: dict = {}
    
    def get_active_window_title(self) -> Optional[str]:
        """
        Получить заголовок активного окна
        
        Returns:
            Optional[str]: Заголовок окна или None
        """
        try:
            active_window = gw.getActiveWindow()
            if active_window and hasattr(active_window, 'title'):
                title = active_window.title
                self._last_active_window = title
                logger.debug(f"Active window title: '{title}'")
                return title
            
            logger.warning("No active window found or window has no title")
            return None
            
        except Exception as e:
            logger.error(f"Failed to get active window title: {e}")
            return self._last_active_window
    
    def find_windows_by_title(self, title: str) -> list:
        """
        Найти окна по заголовку
        
        Args:
            title: Заголовок для поиска
            
        Returns:
            list: Список найденных окон
        """
        try:
            if not title:
                return []
            
            windows = gw.getWindowsWithTitle(title)
            logger.debug(f"Found {len(windows)} windows with title '{title}'")
            return windows
            
        except Exception as e:
            logger.error(f"Failed to find windows with title '{title}': {e}")
            return []
    
    def maximize_window(self, window: Any) -> bool:
        """
        Максимизировать окно
        
        Args:
            window: Объект окна
            
        Returns:
            bool: True если успешно
        """
        try:
            if hasattr(window, 'maximize'):
                window.maximize()
                logger.debug(f"Window '{window.title}' maximized")
                return True
            else:
                logger.error("Window object doesn't support maximize operation")
                return False
                
        except Exception as e:
            logger.error(f"Failed to maximize window: {e}")
            return False


class ConsoleSettings:
    """
    Class for managing console and terminal settings
    
    Provides methods for working with terminal windows,
    managing fullscreen mode, and exiting the application.
    """
    
    def __init__(self, window_manager: Optional[IWindowManager] = None) -> None:
        """
        Инициализация ConsoleSettings
        
        Args:
            window_manager: Менеджер окон (по умолчанию WindowManager)
        """
        self._window_manager = window_manager or WindowManager()
        self._current_state = TerminalState.NORMAL
        self._blocked_keys: set = set()
        self._original_terminal_size: Optional[WindowDimensions] = None
        self._is_fullscreen_active = False
        self._exit_handlers: list = []
        
        logger.info("ConsoleSettings initialized")
    
    @property
    def current_state(self) -> TerminalState:
        """Получить текущее состояние терминала"""
        return self._current_state
    
    @property
    def is_fullscreen_active(self) -> bool:
        """Проверить активен ли полноэкранный режим"""
        return self._is_fullscreen_active
    
    def add_exit_handler(self, handler: callable) -> None:
        """
        Add an exit handler
        
        Args:
            handler: Exit handler function
        """
        if callable(handler):
            self._exit_handlers.append(handler)
            logger.debug("Exit handler added")
        else:
            raise ValueError("Handler must be callable")
    
    def remove_exit_handler(self, handler: callable) -> bool:
        """
        Remove an exit handler
        
        Args:
            handler: Exit handler function
            
        Returns:
            bool: True if removed
        """
        try:
            self._exit_handlers.remove(handler)
            logger.debug("Exit handler removed")
            return True
        except ValueError:
            return False
    
    def get_current_window_title(self) -> Optional[str]:
        """
        Get the title of the current active window
        
        Returns:
            Optional[str]: Window title or None
        """
        try:
            title = self._window_manager.get_active_window_title()
            if title:
                logger.debug(f"Current window title: '{title}'")
            return title
        except Exception as e:
            logger.error(f"Failed to get current window title: {e}")
            raise WindowNotFoundError(f"Cannot get current window title: {e}")
    
    def get_terminal_info(self) -> TerminalInfo:
        """
        Get terminal information
        
        Returns:
            TerminalInfo: Terminal information
        """
        try:
            title = self.get_current_window_title()
            
            # Попытка получить размеры через curses если доступно
            dimensions = None
            try:
                if curses.isendwin():
                    curses.initscr()
                height, width = curses.LINES, curses.COLS
                dimensions = WindowDimensions(width, height)
            except:
                pass
            
            return TerminalInfo(
                title=title,
                dimensions=dimensions,
                position=None,  # Можно расширить позже
                state=self._current_state,
                is_active=title is not None
            )
            
        except Exception as e:
            logger.error(f"Failed to get terminal info: {e}")
            return TerminalInfo(None, None, None, self._current_state, False)
    
    def _find_terminal_window(self) -> Optional[Any]:
        """
        Find the terminal window
        
        Returns:
            Optional[Any]: Window object or None
        """
        try:
            title = self.get_current_window_title()
            if not title:
                logger.warning("Cannot find terminal window: no active window title")
                return None
            
            windows = self._window_manager.find_windows_by_title(title)
            if not windows:
                logger.warning(f"No windows found with title: '{title}'")
                return None
            
            terminal_window = windows[0]
            logger.debug(f"Terminal window found: '{terminal_window.title}'")
            return terminal_window
            
        except Exception as e:
            logger.error(f"Failed to find terminal window: {e}")
            return None
    
    def maximize_terminal(self) -> bool:
        """
        Maximize the terminal window
        
        Returns:
            bool: True if maximized successfully
            
        Raises:
            TerminalOperationError: If maximization fails
        """
        try:
            terminal_window = self._find_terminal_window()
            if not terminal_window:
                raise WindowNotFoundError("Terminal window not found")
            
            success = self._window_manager.maximize_window(terminal_window)
            if success:
                self._current_state = TerminalState.MAXIMIZED
                logger.info("Terminal maximized successfully")
            else:
                logger.error("Failed to maximize terminal")
                
            return success
            
        except Exception as e:
            logger.error(f"Terminal maximization failed: {e}")
            raise TerminalOperationError(f"Cannot maximize terminal: {e}")
    
    def _block_key(self, key: str) -> None:
        """
        Block a key
        
        Args:
            key: Key to block
        """
        try:
            if key not in self._blocked_keys:
                keyboard.block_key(key)
                self._blocked_keys.add(key)
                logger.debug(f"Key '{key}' blocked")
        except Exception as e:
            logger.error(f"Failed to block key '{key}': {e}")
    
    def _unblock_all_keys(self) -> None:
        """Unblock all blocked keys"""
        for key in self._blocked_keys.copy():
            try:
                keyboard.unblock_key(key)
                self._blocked_keys.remove(key)
                logger.debug(f"Key '{key}' unblocked")
            except Exception as e:
                logger.error(f"Failed to unblock key '{key}': {e}")
    
    def open_terminal_fullscreen(self) -> bool:
        """
        Open terminal in fullscreen mode
        
        Returns:
            bool: True if switched to fullscreen successfully
            
        Raises:
            TerminalOperationError: If switching fails
        """
        try:
            # Сначала максимизируем
            if not self.maximize_terminal():
                logger.warning("Failed to maximize terminal before fullscreen")
            
            # Сохраняем текущий размер
            try:
                height, width = curses.LINES, curses.COLS
                self._original_terminal_size = WindowDimensions(width, height)
            except:
                pass
            
            # Переключаем в полноэкранный режим
            try:
                pyautogui.press('f11')
                self._block_key('f11')
                
                self._current_state = TerminalState.FULLSCREEN
                self._is_fullscreen_active = True
                
                logger.info("Terminal switched to fullscreen mode")
                return True
                
            except Exception as e:
                logger.error(f"Failed to press F11 or block key: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Fullscreen operation failed: {e}")
            raise TerminalOperationError(f"Cannot switch to fullscreen: {e}")
    
    def exit_fullscreen(self) -> bool:
        """
        Exit fullscreen mode
        
        Returns:
            bool: True if successful
        """
        try:
            if not self._is_fullscreen_active:
                logger.debug("Terminal is not in fullscreen mode")
                return True
            
            # Разблокируем F11 и нажимаем для выхода
            if 'f11' in self._blocked_keys:
                keyboard.unblock_key('f11')
                self._blocked_keys.remove('f11')
            
            pyautogui.press('f11')
            
            self._current_state = TerminalState.MAXIMIZED
            self._is_fullscreen_active = False
            
            logger.info("Exited fullscreen mode")
            return True
            
        except Exception as e:
            logger.error(f"Failed to exit fullscreen: {e}")
            return False
    
    def create_fullscreen_window(self, stdscr: Any) -> Any:
        """
        Create a fullscreen curses window
        
        Args:
            stdscr: Standard curses screen
            
        Returns:
            Any: New curses window
            
        Raises:
            CursesWindowError: If window creation fails
        """
        try:
            if stdscr is None:
                raise ValueError("stdscr cannot be None")
            
            stdscr.refresh()
            height, width = stdscr.getmaxyx()
            
            if height <= 0 or width <= 0:
                raise ValueError(f"Invalid terminal dimensions: {height}x{width}")
            
            logger.info(f"Terminal size after adjustment: {height}x{width}")
            
            # Создаем новое окно на весь экран
            win = curses.newwin(height, width, 0, 0)
            if win is None:
                raise CursesWindowError("Failed to create curses window")
            
            # Настраиваем окно
            win.keypad(True)
            win.nodelay(False)
            
            logger.debug(f"Fullscreen curses window created: {height}x{width}")
            return win
            
        except Exception as e:
            logger.error(f"Failed to create fullscreen window: {e}")
            raise CursesWindowError(f"Cannot create fullscreen window: {e}")
    
    def _execute_exit_handlers(self) -> None:
        """Execute all exit handlers"""
        for handler in self._exit_handlers:
            try:
                handler()
                logger.debug("Exit handler executed successfully")
            except Exception as e:
                logger.error(f"Exit handler failed: {e}")
    
    def _cleanup_resources(self) -> None:
        """Clean up resources before exit"""
        try:
            # Разблокируем все клавиши
            self._unblock_all_keys()
            
            # Выходим из полноэкранного режима если нужно
            if self._is_fullscreen_active:
                self.exit_fullscreen()
            
            # Сохраняем данные игры
            save_manager.save_all_game_data()
            logger.info("Game data saved successfully")
            
            # Останавливаем музыку
            AudioController.get_instance().stop_music()
            logger.info("Audio stopped successfully")
            
            # Завершаем curses
            curses.endwin()
            logger.info("Curses terminated successfully")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def exit_terminal(self, exit_code: ExitCode = ExitCode.SUCCESS,
                    show_message: bool = True) -> None:
        """
        Terminate the terminal and application
        
        Args:
            exit_code: Exit code
            show_message: Show exit message
            
        Raises:
            TerminalOperationError: If a critical exit error occurs
        """
        try:
            logger.info(f"Terminal exit initiated with code: {exit_code}")
            
            # Выполняем пользовательские обработчики
            self._execute_exit_handlers()
            
            # Очищаем ресурсы
            self._cleanup_resources()
            
            # Показываем сообщение если нужно
            if show_message:
                print("\n" + "="*50)
                print("🎮 Game session ended successfully!")
                print("💾 All data has been saved")
                print("🔊 Audio stopped")
                
                if exit_code != ExitCode.SUCCESS:
                    print("⚠️  If you see this message, press Alt+F4 to exit")
                
                print("="*50)
            
            # Завершаем программу
            logger.info("Application terminating...")
            sys.exit(exit_code.value)
            
        except KeyboardInterrupt:
            logger.warning("Force exit requested by user")
            self._cleanup_resources()
            sys.exit(ExitCode.FORCE_EXIT.value)
            
        except Exception as e:
            logger.critical(f"Critical error during exit: {e}")
            # Попытка экстренного выхода
            try:
                curses.endwin()
                AudioController.get_instance().stop_music()
            except:
                pass
            raise TerminalOperationError(f"Critical exit error: {e}")
    
    def force_exit(self) -> None:
        """Force exit the application"""
        logger.warning("Force exit initiated")
        try:
            self._cleanup_resources()
        except:
            pass
        finally:
            os._exit(ExitCode.FORCE_EXIT.value)
    
    def __enter__(self):
        """Context manager: enter"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager: exit"""
        if exc_type is not None:
            logger.error(f"Exception in context: {exc_type.__name__}: {exc_val}")
        self.exit_terminal(ExitCode.ERROR if exc_type else ExitCode.SUCCESS)


# Создаем глобальный экземпляр с использованием паттерна Singleton
class _ConsoleSingleton:
    """Singleton для глобального доступа к ConsoleSettings"""
    _instance: Optional[ConsoleSettings] = None
    
    def __new__(cls) -> ConsoleSettings:
        if cls._instance is None:
            cls._instance = ConsoleSettings()
        return cls._instance


# Global instance for backward compatibility
console_settings = _ConsoleSingleton()


# Удобные функции для быстрого доступа
def get_console_settings() -> ConsoleSettings:
    """Get ConsoleSettings instance"""
    return console_settings


def initialize_console_settings(window_manager: Optional[IWindowManager] = None) -> ConsoleSettings:
    """
    Initialize a new ConsoleSettings instance
    
    Args:
        window_manager: Custom window manager
        
    Returns:
        ConsoleSettings: New instance
    """
    return ConsoleSettings(window_manager)