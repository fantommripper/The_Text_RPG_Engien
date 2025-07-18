from abc import ABC, abstractmethod
from lib.Logger import logger

class BaseScene(ABC):
    """Base class for all scenes"""
    
    def __init__(self, scene_name: str = "Unknown Scene"):
        self.scene_name = scene_name
        self.consolas = None

    @abstractmethod
    def run(self):
        """Run the scene logic"""
        pass

    @abstractmethod
    def _stop_menu(self):
        """Stop the current menu"""
        pass

    def get_scene_info(self):
        """Returns scene information"""
        return {
            "class_name": self.__class__.__name__,
            "module": self.__class__.__module__
        }