import dearpygui.dearpygui as dpg
import sys
import os
from functools import partial
from lib.Logger import logger
from windows.FileManager import FileManager

class Engine:
    def __init__(self):
        self.file_manager = None
        self._init_dpg()
    
    def _get_system_font(self):
        local_font = os.path.join(os.path.dirname(__file__), "HackNerdFont.ttf")
        if os.path.exists(local_font):
            return local_font
        return None

    def _open_file_manager_window(self):
        if self.file_manager is None:
            self.file_manager = FileManager()
        self.file_manager.show()
    
    def _init_dpg(self):
        dpg.create_context()
        dpg.create_viewport(title='Game Engine', width=1200, height=800)
        dpg.setup_dearpygui()
        
        font_path = self._get_system_font()
        if font_path:
            with dpg.font_registry():
                self.default_font = dpg.add_font(font_path, 18)
            dpg.bind_font(self.default_font)
        else:
            logger.warning("Default font not found, using system font.")
        
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())
            with dpg.menu(label="Window"):
                dpg.add_menu_item(label="File Manager", callback=self._open_file_manager_window)
            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="About")
        
        # Автоматически открываем файл-менеджер при запуске
        self._open_file_manager_window()
        
        logger.info("DearPyGUI initialized")
        dpg.show_viewport()
    
    def run(self):
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

if __name__ == "__main__":
    engine = Engine()
    engine.run()