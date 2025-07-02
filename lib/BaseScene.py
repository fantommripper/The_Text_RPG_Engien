from abc import ABC, abstractmethod
from lib.Logger import logger

class BaseScene(ABC):
    """Базовый класс для всех сцен"""
    
    def __init__(self, scene_name: str = "Unknown Scene"):
        self.scene_name = scene_name
        self.consolas = None

    @abstractmethod
    def run(self):
        """Основной метод запуска сцены"""
        pass

    @abstractmethod
    def _stop_menu(self):
        """Остановка текущего меню"""
        pass

    def get_scene_info(self):
        """Возвращает информацию о сцене"""
        return {
            "class_name": self.__class__.__name__,
            "module": self.__class__.__module__
        }