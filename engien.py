import dearpygui.dearpygui as dpg
import sys
import os
from functools import partial
from lib.Logger import logger
from windows.FileManager import FileManager
from windows.SceneEditor import SceneEditor
from windows.GameRunner import GameRunner

class Engine:
    def __init__(self):
        self.file_manager = None
        self.scene_editor = None
        self.game_runner = None
        self._init_dpg()
    
    def _get_system_font(self):
        local_font = os.path.join(os.path.dirname(__file__), "Roboto.ttf")
        if os.path.exists(local_font):
            return local_font
        return None

    def _open_file_manager_window(self):
        if self.file_manager is None:
            self.file_manager = FileManager()
        self.file_manager.show()

    def _open_scene_editor_window(self):
        if self.scene_editor is None:
            self.scene_editor = SceneEditor()
        self.scene_editor.show()

    def _open_game_runner_window(self):
        if self.game_runner is None:
            self.game_runner = GameRunner()
        self.game_runner.show()
    
    def _global_left_click_handler(self, sender, app_data):
        """Закрывает контекстное меню при левом клике в любом месте"""
        if (self.file_manager and 
            dpg.does_item_exist("context_menu") and 
            dpg.is_item_shown("context_menu")):
            dpg.configure_item("context_menu", show=False)
            logger.info("Context menu closed by global click")
    
    def _init_dpg(self):
        dpg.create_context()
        dpg.create_viewport(title='Text RPG Game Engine', width=1200, height=800)
        dpg.setup_dearpygui()
        
        # Глобальный обработчик для закрытия контекстных меню
        with dpg.handler_registry():
            dpg.add_mouse_click_handler(
                button=dpg.mvMouseButton_Left, 
                callback=self._global_left_click_handler
            )
        
        font_path = self._get_system_font()
        if font_path:
            with dpg.font_registry():
                self.default_font = dpg.add_font(font_path, 18)
            dpg.bind_font(self.default_font)
        else:
            logger.warning("Default font not found, using system font.")
        
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Exit", callback=self._exit_engine)
            with dpg.menu(label="Game"):  # Новое меню
                dpg.add_menu_item(label="Launch Game", callback=self._open_game_runner_window)
                dpg.add_separator()
                dpg.add_menu_item(label="Open Game Folder", callback=self._open_assets_folder)
            with dpg.menu(label="Tools"):  # Переименовываем Window в Tools
                dpg.add_menu_item(label="File Manager", callback=self._open_file_manager_window)
                dpg.add_menu_item(label="Scene Editor", callback=self._open_scene_editor_window)
            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="About", callback=self._show_about)
        
        # Автоматически открываем файл-менеджер при запуске
        self._open_file_manager_window()
        
        logger.info("DearPyGUI initialized")
        dpg.show_viewport()

    def _open_assets_folder(self):
        """Открывает папку Assets"""
        try:
            assets_path = os.path.join(os.path.dirname(__file__), "Assets")
            if sys.platform.startswith('win'):
                os.startfile(assets_path)
            elif sys.platform == 'darwin':  # macOS
                import subprocess
                subprocess.run(['open', assets_path])
            else:  # Linux
                import subprocess
                subprocess.run(['xdg-open', assets_path])
        except Exception as e:
            logger.error(f"Error opening Assets folder: {e}")

    def _show_about(self):
        """Показывает информацию о движке"""
        if dpg.does_item_exist("about_dialog"):
            dpg.delete_item("about_dialog")
            
        with dpg.window(label="About Game Engine", modal=True, width=400, height=200, tag="about_dialog"):
            dpg.add_text("Text RPG Game Engine", color=[100, 200, 255])
            dpg.add_text("Version 1.0.0")
            dpg.add_separator()
            dpg.add_text("Features:")
            dpg.add_text("• File Manager")
            dpg.add_text("• Scene Editor") 
            dpg.add_text("• Game Runner")
            dpg.add_separator()
            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("about_dialog"))

    def _exit_engine(self):
        """Выход из движка с очисткой ресурсов"""
        logger.info("Shutting down engine...")
        
        # Очищаем ресурсы GameRunner
        if self.game_runner:
            self.game_runner.cleanup()
        
        dpg.stop_dearpygui()
    
    def run(self):
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
        
        # Очистка при выходе
        if self.game_runner:
            self.game_runner.cleanup()
            
        dpg.destroy_context()

if __name__ == "__main__":
    engine = Engine()
    engine.run()