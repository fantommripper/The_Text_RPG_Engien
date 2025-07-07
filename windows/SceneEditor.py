import dearpygui.dearpygui as dpg
import os
import json
import re
import uuid

from lib.Logger import logger

from .Dialogs.ErrorDialog import ErroreDialog
from .Dialogs.SuccessDialog import SuccessDialog
from .Dialogs.InfoDialog import InfoDialog
from .Dialogs.ConfirmationDeleteDialog import ConfirmationDeleteDialog
from .TextEditor import TextEditor

class SceneEditor:
    def __init__(self):
        self.window_id = None
        self.assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Assets")
        self.scenes_path = os.path.join(self.assets_path, "event", "menu")
        self.controller_path = os.path.join("controller", "MenuController.py")
        self.current_scene_type = "test_world_menu"  # по умолчанию
        self.existing_scenes = {}
        self.safe_name_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')  # Валидные имена классов Python

    def show(self):
        if self.window_id and dpg.does_item_exist(self.window_id):
            dpg.show_item(self.window_id)
            return

        self._create_window()

    def _create_window(self):
        with dpg.window(label="Scene Editor", width=600, height=700, pos=[420, 50]) as self.window_id:
            dpg.add_text("Scene Creator & Manager")
            dpg.add_separator()

            # Выбор типа сцены
            with dpg.group(horizontal=True):
                dpg.add_text("Scene Type:")
                dpg.add_radio_button(
                    items=["test_world_menu", "game_menu"],
                    default_value=0,
                    horizontal=True,
                    callback=self._on_scene_type_change,
                    tag="scene_type_radio"
                )

            dpg.add_separator()

            # Создание новой сцены
            with dpg.collapsing_header(label="Create New Scene", default_open=True):
                dpg.add_input_text(
                    label="Scene Name",
                    hint="e.g., MyAwesomeMenu",
                    tag="scene_name_input",
                    width=300
                )
                dpg.add_input_text(
                    label="Display Title",
                    hint="e.g., My Awesome Menu",
                    tag="scene_title_input",
                    width=300
                )
                
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Create Scene",
                        callback=self._create_scene,
                        width=120
                    )
                    dpg.add_button(
                        label="Preview Code",
                        callback=self._preview_scene_code,
                        width=120
                    )

            dpg.add_separator()

            # Список существующих сцен
            with dpg.collapsing_header(label="Existing Scenes", default_open=True):
                dpg.add_button(label="Refresh List", callback=self._refresh_scenes_list)
                with dpg.child_window(height=200, tag="scenes_list_container"):
                    self._populate_scenes_list()
            
            dpg.add_separator()

            # Предварительный просмотр кода - ИСПРАВЛЕНО: делаем растягиваемым
            with dpg.collapsing_header(label="Code Preview"):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Copy Code", callback=self._copy_code_to_clipboard, width=100)
                    dpg.add_button(label="Clear Preview", callback=self._clear_code_preview, width=100)

                # Используем input_text с multiline вместо обычного text
                dpg.add_input_text(
                    tag="code_preview_input",
                    multiline=True,
                    readonly=True,
                    height=-1,
                    width=-1,
                    default_value="Select 'Preview Code' to see generated code"
                )

    def _on_scene_type_change(self, sender, app_data):
        """Обработчик изменения типа сцены"""
        scene_types = ["test_world_menu", "game_menu"]
        self.current_scene_type = scene_types[app_data]
        logger.info(f"Scene type changed to: {self.current_scene_type}")
        self._refresh_scenes_list()

    def _is_valid_class_name(self, name):
        """Проверяет, является ли имя валидным для класса Python"""
        if not name or name.strip() == "":
            return False, "Name cannot be empty"
        
        if not self.safe_name_pattern.match(name):
            return False, "Invalid class name. Use only letters, numbers, and underscores. Must start with letter or underscore."
        
        if name[0].islower():
            return False, "Class name should start with uppercase letter"
        
        # Проверяем зарезервированные слова Python
        reserved_words = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue',
            'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 
            'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 
            'raise', 'return', 'try', 'while', 'with', 'yield'
        ]
        
        if name in reserved_words:
            return False, f"'{name}' is a reserved Python keyword"
            
        return True, ""

    def _generate_scene_code(self, class_name, display_title):
        """Генерирует код для новой сцены"""
        snake_case_name = self._camel_to_snake(class_name)
        
        code = f'''from lib.BaseScene import BaseScene
from lib.ConsoleSettings import console_settings
from lib.Logger import logger
from lib.Localization import loc

from controller.MenuController import menu_controller
from controller.LibController import lib_controller

class {class_name}(BaseScene):
    def __init__(self):
        super().__init__("{display_title}")
        self.consolas = lib_controller.consolas

    def run(self):
        """Start the scene"""
        logger.info(f"Starting scene: {{self.scene_name}}")

    def _stop_menu(self):
        """Stop current menu"""
        pass

{snake_case_name} = {class_name}()
'''
        return code

    def _camel_to_snake(self, name):
        """Конвертирует CamelCase в snake_case"""
        return ''.join(["_" + l.lower() if l.isupper() else l for l in name])

    def _generate_controller_method(self, class_name, file_name):
        """Генерирует метод для MenuController"""
        snake_case_name = self._camel_to_snake(class_name)
        method_name = f"show{snake_case_name}"

        method_code = f'''
    def {method_name}(self):
        from Assets.event.menu.{self.current_scene_type}.{file_name} import {snake_case_name}
        {snake_case_name}.run()'''
        
        return method_name, method_code

    def _preview_scene_code(self):
        """Показывает предварительный просмотр кода"""
        scene_name = dpg.get_value("scene_name_input").strip()
        display_title = dpg.get_value("scene_title_input").strip()

        if not scene_name:
            self._show_error_dialog("Please enter a scene name")
            return

        is_valid, error_msg = self._is_valid_class_name(scene_name)
        if not is_valid:
            self._show_error_dialog(f"Invalid scene name: {error_msg}")
            return

        if not display_title:
            display_title = scene_name

        # Генерируем код
        scene_code = self._generate_scene_code(scene_name, display_title)
        
        # Показываем в превью
        dpg.set_value("code_preview_input", scene_code)

    def _copy_code_to_clipboard(self):
        """Копирует код в буфер обмена"""
        try:
            code = dpg.get_value("code_preview_input")
            if code and code != "Select 'Preview Code' to see generated code":
                # Простая реализация копирования (может не работать на всех системах)
                import subprocess
                import platform

                system = platform.system()
                if system == "Windows":
                    subprocess.run(['clip'], input=code, text=True, check=True)
                elif system == "Darwin":  # macOS
                    subprocess.run(['pbcopy'], input=code, text=True, check=True)
                elif system == "Linux":
                    subprocess.run(['xclip', '-selection', 'clipboard'], input=code, text=True, check=True)

                self._show_success_dialog("Code copied to clipboard!")
            else:
                self._show_error_dialog("No code to copy. Generate preview first.")
        except Exception as e:
            logger.error(f"Error copying to clipboard: {e}")
            self._show_error_dialog("Failed to copy to clipboard. Copy manually from the preview.")

    def _clear_code_preview(self):
        """Очищает предварительный просмотр кода"""
        dpg.set_value("code_preview_input", "Select 'Preview Code' to see generated code")

    def _create_scene(self):
        """Создает новую сцену"""
        scene_name = dpg.get_value("scene_name_input").strip()
        display_title = dpg.get_value("scene_title_input").strip()
        
        if not scene_name:
            self._show_error_dialog("Please enter a scene name")
            return
        
        is_valid, error_msg = self._is_valid_class_name(scene_name)
        if not is_valid:
            self._show_error_dialog(f"Invalid scene name: {error_msg}")
            return
        
        if not display_title:
            display_title = scene_name
        
        try:
            # Создаем директорию если нужно
            scene_dir = os.path.join(self.scenes_path, self.current_scene_type)
            os.makedirs(scene_dir, exist_ok=True)
            
            # Создаем файл сцены
            file_name = f"{scene_name}.py"
            scene_file_path = os.path.join(scene_dir, file_name)
            
            if os.path.exists(scene_file_path):
                self._show_error_dialog(f"Scene file '{file_name}' already exists!")
                return
            
            # Генерируем и записываем код сцены
            scene_code = self._generate_scene_code(scene_name, display_title)
            with open(scene_file_path, 'w', encoding='utf-8') as f:
                f.write(scene_code)
            
            # Добавляем метод в MenuController
            self._add_method_to_controller(scene_name, file_name)
            
            logger.info(f"Created new scene: {scene_file_path}")
            self._show_success_dialog(f"Scene '{scene_name}' created successfully!")
            
            # Очищаем поля ввода
            dpg.set_value("scene_name_input", "")
            dpg.set_value("scene_title_input", "")
            
            # Обновляем список сцен
            self._refresh_scenes_list()
            
        except Exception as e:
            logger.error(f"Error creating scene: {e}")
            self._show_error_dialog(f"Failed to create scene: {str(e)}")

    def _add_method_to_controller(self, class_name, file_name):
        """Добавляет метод в MenuController перед строкой menu_controller = MenuController()"""
        try:
            if not os.path.exists(self.controller_path):
                logger.warning(f"MenuController not found at {self.controller_path}")
                return

            # Читаем существующий файл
            with open(self.controller_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Генерируем новый метод
            method_name, method_code = self._generate_controller_method(class_name, file_name[:-3])  # убираем .py

            # Проверяем, что метод еще не существует
            if method_name in content:
                logger.info(f"Method {method_name} already exists in MenuController")
                return

            # Находим место для вставки (перед строкой menu_controller = MenuController())
            lines = content.split('\n')
            insert_index = -1

            for i, line in enumerate(lines):
                if line.strip().startswith('menu_controller = MenuController()'):
                    insert_index = i
                    break

            if insert_index == -1:
                # Если не нашли, добавляем в конец класса
                insert_index = len(lines)

            # Вставляем новый метод
            lines.insert(insert_index, method_code)

            # Записываем обновленный файл
            with open(self.controller_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            logger.info(f"Added method {method_name} to MenuController")

        except Exception as e:
            logger.error(f"Error updating MenuController: {e}")

    def _remove_method_from_controller(self, class_name):
        """Удаляет метод для сцены из MenuController.py, не трогая menu_controller = MenuController()"""
        try:
            if not os.path.exists(self.controller_path):
                logger.warning(f"MenuController not found at {self.controller_path}")
                return

            with open(self.controller_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            snake_case_name = self._camel_to_snake(class_name)
            method_name = f"show{snake_case_name}"

            # Найти начало метода
            start_idx = None
            for i, line in enumerate(lines):
                if line.strip().startswith(f"def {method_name}("):
                    start_idx = i
                    break

            if start_idx is None:
                logger.info(f"Method {method_name} not found in MenuController")
                return

            # Найти конец метода (следующий def на том же уровне или строка menu_controller = ...)
            end_idx = start_idx + 1
            while end_idx < len(lines):
                stripped = lines[end_idx].strip()
                if (stripped.startswith("def ") and not lines[end_idx].startswith("    ")) or \
                stripped.startswith("menu_controller = MenuController()"):
                    break
                end_idx += 1

            # Удалить строки метода
            del lines[start_idx:end_idx]

            with open(self.controller_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            logger.info(f"Removed method {method_name} from MenuController")
        except Exception as e:
            logger.error(f"Error removing method from MenuController: {e}")

    def _populate_scenes_list(self):
        """Заполняет список существующих сцен"""
        # Очищаем контейнер
        if dpg.does_item_exist("scenes_list_container"):
            children = dpg.get_item_children("scenes_list_container", slot=1)
            if children:
                for child in children:
                    try:
                        if dpg.does_item_exist(child):
                            dpg.delete_item(child)
                    except:
                        pass  # Игнорируем ошибки при удалении
        
        scene_dir = os.path.join(self.scenes_path, self.current_scene_type)
        
        if not os.path.exists(scene_dir):
            dpg.add_text(f"Directory '{self.current_scene_type}' not found",
                        parent="scenes_list_container", color=[255, 100, 100])
            return
        
        try:
            files = [f for f in os.listdir(scene_dir) if f.endswith('.py')]
            
            if not files:
                dpg.add_text(f"No scenes found in '{self.current_scene_type}'", 
                            parent="scenes_list_container", color=[200, 200, 200])
                return
            
            dpg.add_text(f"Scenes in '{self.current_scene_type}':",
                        parent="scenes_list_container", color=[100, 255, 100])

            for i, file in enumerate(sorted(files)):
                # Создаем уникальные теги для каждой строки
                group_tag = f"scene_group_{i}_{file}"
                edit_tag = f"edit_btn_{i}_{file}"
                delete_tag = f"delete_btn_{i}_{file}"

                with dpg.group(horizontal=True, parent="scenes_list_container", tag=group_tag):
                    dpg.add_text(f"[FILE] {file}")
                    dpg.add_button(
                        label="Edit",
                        width=50,
                        tag=edit_tag,
                        user_data=file,  # Передаем имя файла через user_data
                        callback=self._edit_scene_callback
                    )
                    dpg.add_button(
                        label="Delete", 
                        width=60,
                        tag=delete_tag,
                        user_data=file,  # Передаем имя файла через user_data
                        callback=self._delete_scene_callback
                    )

        except Exception as e:
            logger.error(f"Error loading scenes list: {e}")
            dpg.add_text(f"Error: {str(e)}", parent="scenes_list_container", color=[255, 100, 100])

    def _edit_scene_callback(self, sender, app_data, user_data):
        """Callback для кнопки Edit"""
        filename = user_data
        self._edit_scene(filename)

    def _delete_scene_callback(self, sender, app_data, user_data):
        """Callback для кнопки Delete"""
        filename = user_data
        self._confirm_delete_scene(filename)

    def _refresh_scenes_list(self):
        """Обновляет список сцен"""
        self._populate_scenes_list()

    def _edit_scene(self, filename):
        """Открывает сцену для редактирования"""
        scene_path = os.path.join(self.scenes_path, self.current_scene_type, filename)
        logger.info(f"Editing scene: {scene_path}")

        try:
            with open(scene_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Генерируем уникальный тег для окна и поля ввода
            unique_id = str(uuid.uuid4())
            window_tag = f"scene_edit_dialog_{unique_id}"

            def on_save():
                self._save_edited_scene(scene_path, filename, window_tag)

            def on_cancel():
                dpg.delete_item(window_tag)

            editor = TextEditor(
                title=f"Edit Scene: {filename}",
                content=content,
                on_save=on_save,
                on_cancel=on_cancel,
                tag=window_tag
            )
            editor.show()
        except Exception as e:
            logger.error(f"Error opening scene for edit: {e}")
            self._show_error_dialog(f"Failed to open scene for editing: {str(e)}")

    def _save_edited_scene(self, scene_path, filename, window_tag):
        try:
            new_content = dpg.get_value(f"{window_tag}_content")
            with open(scene_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            logger.info(f"Saved edited scene: {scene_path}")
            self._show_success_dialog(f"Scene '{filename}' saved successfully!")
            dpg.delete_item(window_tag)
        except Exception as e:
            logger.error(f"Error saving edited scene: {e}")
            self._show_error_dialog(f"Failed to save scene: {str(e)}")

    def _confirm_delete_scene(self, filename):
        """Подтверждение удаления сцены"""
        dialog = ConfirmationDeleteDialog(
            item_name=filename,
            item_type="scene",
            item_path=os.path.join(self.scenes_path, self.current_scene_type, filename)
        )
        dialog.show(
            on_confirm=lambda sender, app_data, user_data=filename: self._delete_scene_confirmed(sender, app_data, user_data),
        )

    def _delete_scene_confirmed(self, sender, app_data, user_data):
        """Подтвержденное удаление сцены"""
        filename = user_data

        try:
            scene_path = os.path.join(self.scenes_path, self.current_scene_type, filename)
            os.remove(scene_path)
            logger.info(f"Deleted scene: {scene_path}")

            # Удаляем метод из MenuController
            class_name = filename[:-3]  # убираем .py
            self._remove_method_from_controller(class_name)

            self._show_success_dialog(f"Scene '{filename}' deleted successfully!")
            self._refresh_scenes_list()
        except Exception as e:
            logger.error(f"Error deleting scene: {e}")
            self._show_error_dialog(f"Failed to delete scene: {str(e)}")

    def _show_error_dialog(self, message):
        """Показывает диалог ошибки"""
        dialog = ErroreDialog()
        dialog.show(
            message=message,
            on_confirm=lambda sender, app_data: dpg.delete_item(dialog.dialog_id),
        )

    def _show_success_dialog(self, message):
        """Показывает диалог успеха"""
        dialog = SuccessDialog()
        dialog.show(
            message=message,
            on_confirm=lambda sender, app_data: dpg.delete_item(dialog.dialog_id),
        )

    def _show_info_dialog(self, message):
        """Показывает информационный диалог"""
        dialog = InfoDialog()
        dialog.show(
            message=message,
            on_confirm=lambda sender, app_data: dpg.delete_item(dialog.dialog_id),
        )