import dearpygui.dearpygui as dpg
import os
import re
import time
import shutil

from .ConfirmationDeleteDialog import ConfirmationDeleteDialog
from .CreateFileDialog import CreateFileDialog
from .CreateFolderDialog import CreateFolderDialog
from lib.Logger import logger

class FileManager:
    def __init__(self):
        self.window_id = None
        self.assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Assets")
        self.selected_path = self.assets_path
        self.selected_item_path = None  # Для отслеживания выбранного элемента
        self.window_handler = None
        self.path_mapping = {}
        self.expanded_nodes = {}
        self.safe_name_pattern = re.compile(r'^[\w\-\.\s]+$')  # Разрешенные символы в именах
        self.dialog_counter = 0  # Счетчик для уникальных ID диалогов
        self.highlighted_item = None  # Для отслеживания подсвеченного элемента

    def show(self):
        if self.window_id and dpg.does_item_exist(self.window_id):
            dpg.show_item(self.window_id)
            return

        self._create_window()

    def _create_window(self):
        with dpg.window(label="File Manager", width=400, height=600, pos=[10, 50]) as self.window_id:
            dpg.add_text("Project Files:")
            dpg.add_separator()

            with dpg.group(horizontal=True):
                dpg.add_button(label="Create Python File",
                            callback=lambda: self._create_python_file_in_assets())
                dpg.add_button(label="Create Folder",
                            callback=lambda: self._create_folder_in_assets())
                dpg.add_button(label="Refresh", callback=self._refresh_files)

            dpg.add_separator()

            with dpg.group(tag="file_list_container"):
                self._populate_files()

            self.context_menu_id = f"context_menu_{int(time.time() * 1000)}"
            with dpg.popup(parent="file_list_container", tag=self.context_menu_id, modal=False, no_move=True):
                dpg.add_menu_item(label="Open", callback=lambda: self._handle_menu_action("open", self.context_menu_id))
                with dpg.menu(label="Create"):
                    dpg.add_menu_item(label="Empty Python File", callback=lambda: self._handle_menu_action("create_file", self.context_menu_id))
                    dpg.add_menu_item(label="Folder", callback=lambda: self._handle_menu_action("create_folder", self.context_menu_id))
                dpg.add_menu_item(label="Delete", callback=lambda: self._handle_menu_action("delete", self.context_menu_id))
                dpg.add_menu_item(label="Refresh", callback=lambda: self._handle_menu_action("refresh", self.context_menu_id))

    def _populate_files(self):
        try:
            self._save_expanded_state()
            
            if dpg.does_item_exist("file_list_container"):
                children = dpg.get_item_children("file_list_container", slot=1)
                if children:
                    for child in children:
                        dpg.delete_item(child)

            self.path_mapping = {}

            with dpg.tree_node(label="[DIR] Assets", tag="assets_root", default_open=True, parent="file_list_container") as node:
                self.path_mapping["assets_root"] = self.assets_path
                
                with dpg.item_handler_registry() as handler:
                    dpg.add_item_clicked_handler(
                        button=dpg.mvMouseButton_Right,
                        callback=lambda: self._on_right_click(self.assets_path)
                    )
                dpg.bind_item_handler_registry(node, handler)
                
                self._add_directory_contents(self.assets_path, "assets_root")

        except Exception as e:
            logger.error(f"Error populating files: {e}")
            dpg.add_text(f"Error: {str(e)}", parent="file_list_container", color=[255, 100, 100])
    
    def _save_expanded_state(self):
        """Сохраняет пути раскрытых папок"""
        self.expanded_nodes = set()
        for tag, path in self.path_mapping.items():
            # Проверяем, что это папка и она раскрыта (через value)
            if dpg.does_item_exist(tag):
                value = dpg.get_value(tag)
                if value:  # True если раскрыта
                    self.expanded_nodes.add(path)

    def _add_directory_contents(self, path, parent_tag):
        try:
            if not os.path.exists(path):
                return

            items = os.listdir(path)
            items.sort()

            # Сначала добавляем папки
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    folder_tag = f"folder_{abs(hash(item_path))}"
                    self.path_mapping[folder_tag] = item_path

                    was_expanded = item_path in self.expanded_nodes

                    with dpg.tree_node(label=f"[D] {item}", tag=folder_tag,
                                    parent=parent_tag, default_open=was_expanded) as node:
                        with dpg.item_handler_registry() as handler:
                            dpg.add_item_clicked_handler(
                                button=dpg.mvMouseButton_Right,
                                callback=lambda sender, app_data, user_data: self._on_right_click(user_data),
                                user_data=item_path
                            )
                        dpg.bind_item_handler_registry(node, handler)

                        self._add_directory_contents(item_path, folder_tag)

            # Затем добавляем файлы
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    file_icon = self._get_file_icon(item)
                    file_tag = f"file_{abs(hash(item_path))}"
                    self.path_mapping[file_tag] = item_path
                    
                    node = dpg.add_text(f"{file_icon} {item}", parent=parent_tag, tag=file_tag)
                    
                    with dpg.item_handler_registry() as handler:
                        dpg.add_item_clicked_handler(
                            button=dpg.mvMouseButton_Right,
                            callback=lambda sender, app_data, user_data: self._on_right_click(user_data),
                            user_data=item_path
                        )
                    dpg.bind_item_handler_registry(node, handler)

        except Exception as e:
            logger.error(f"Error adding directory contents for {path}: {e}")

    def _get_file_icon(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        icons = {
            '.py': '[PY]',
            '.txt': '[TXT]',
            '.json': '[JSON]',
            '.json5': '[JSON5]',
            '.png': '[PNG]',
            '.jpg': '[JPG]',
            '.jpeg': '[JPEG]',
            '.gif': '[GIF]',
            '.mp3': '[MP3]',
            '.wav': '[WAV]',
            '.mp4': '[MP4]',
            '.avi': '[AVI]',
        }
        return icons.get(ext, '[FILE]')

    def _on_right_click(self, path):
        if path and os.path.exists(path):
            self.selected_item_path = path
            if os.path.isfile(path):
                self.selected_path = os.path.dirname(path)
            else:
                self.selected_path = path

            if not os.path.isdir(self.selected_path):
                self.selected_path = self.assets_path
                logger.warning(f"Selected path is not a directory, using assets: {self.selected_path}")

            # Показываем контекстное меню
            mouse_pos = dpg.get_mouse_pos(local=False)
            menu_x = mouse_pos[0] + 10
            menu_y = mouse_pos[1] + 10

            # Корректируем если выходит за границы
            viewport_width = dpg.get_viewport_width()
            viewport_height = dpg.get_viewport_height()
            menu_width = 200
            menu_height = 200

            if menu_x + menu_width > viewport_width:
                menu_x = mouse_pos[0] - menu_width - 10
            if menu_y + menu_height > viewport_height:
                menu_y = mouse_pos[1] - menu_height - 10

            menu_x = max(10, menu_x)
            menu_y = max(10, menu_y)

            dpg.configure_item(self.context_menu_id, pos=[menu_x, menu_y], show=True)
        else:
            logger.warning(f"Invalid path on right click: {path}")
            self.selected_path = self.assets_path

    def _handle_menu_action(self, action, menu_id):
        if dpg.does_item_exist(menu_id):
            dpg.configure_item(menu_id, show=False)

        if not self.selected_path or not os.path.exists(self.selected_path):
            self.selected_path = self.assets_path

        if action == "delete":
            self._delete_item()
        elif action == "refresh":
            self._refresh_files()
        elif action == "open":
            logger.info(f"Opening file: {self.selected_item_path}")
            # TODO: Реализовать открытие файла в редакторе
        elif action == "create_file":
            self._create_python_file()
        elif action == "create_folder":
            self._create_folder()

    def _delete_item(self):
        """Удаляет выбранный файл или папку"""
        if not self.selected_item_path or not os.path.exists(self.selected_item_path):
            logger.warning("No valid item selected for deletion")
            return
        
        # Нельзя удалить корневую папку Assets
        if self.selected_item_path == self.assets_path:
            self._show_error_dialog("Cannot delete the root Assets folder!")
            return
        
        item_name = os.path.basename(self.selected_item_path)
        item_type = "folder" if os.path.isdir(self.selected_item_path) else "file"

        dialog = ConfirmationDeleteDialog(item_name, item_type, self.selected_item_path)
        dialog.show(
            on_confirm=lambda dialog_id, _: self._confirm_delete(dialog_id, self.selected_item_path)
        )

    def _confirm_delete(self, dialog_id, item_path):
        """Подтверждает и выполняет удаление"""
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logger.info(f"Deleted folder: {item_path}")
            else:
                os.remove(item_path)
                logger.info(f"Deleted file: {item_path}")
            
            # Сбрасываем выделение
            self.selected_item_path = None
            self.highlighted_item = None
            
            # Обновляем список файлов
            self._refresh_files()
            
        except Exception as e:
            logger.error(f"Error deleting item: {e}")
            self._show_error_dialog(f"Failed to delete item: {str(e)}")

    def _create_python_file_in_assets(self):
        self.selected_path = self.assets_path
        self._create_python_file()
    
    def _create_folder_in_assets(self):
        self.selected_path = self.assets_path
        self._create_folder()
    
    def _create_python_file(self):
        dialog = CreateFileDialog()
        dialog.show(
            on_confirm=lambda dialog_id, input_id: self._confirm_create_file(dialog_id, input_id, self.selected_path)
        )
    
    def _create_folder(self):
        dialog = CreateFolderDialog()
        dialog.show(
            on_confirm=lambda dialog_id, input_id: self._confirm_create_folder(dialog_id, input_id, self.selected_path)
        )
    
    def _cleanup_old_dialogs(self):
        """Удаляет старые диалоги для предотвращения конфликтов"""
        dialog_patterns = [
            "create_file_dialog_",
            "create_folder_dialog_",
            "error_dialog_",
            "delete_confirmation_"
        ]
        
        for pattern in dialog_patterns:
            for i in range(max(0, self.dialog_counter - 5), self.dialog_counter):
                dialog_id = f"{pattern}{i}"
                if dpg.does_item_exist(dialog_id):
                    dpg.delete_item(dialog_id)
    
    def _is_valid_name(self, name):
        """Проверяет, является ли имя безопасным для файловой системы"""
        if not name or name.strip() == "":
            return False, "Name cannot be empty"
        
        if not self.safe_name_pattern.match(name):
            return False, "Name contains invalid characters"
        
        # Запрещенные имена в Windows
        forbidden_names = [
            "CON", "PRN", "AUX", "NUL",
            "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
            "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
        ]
        if name.upper() in forbidden_names:
            return False, "This name is reserved by the system"
            
        return True, ""
    
    def _confirm_create_file(self, dialog_id, input_id, target_path):
        file_name = dpg.get_value(input_id).strip()
        
        # Проверка имени
        is_valid, error_msg = self._is_valid_name(file_name)
        if not is_valid:
            self._show_error_dialog(f"Invalid file name: {error_msg}")
            return
        
        # Убедимся, что есть расширение .py
        if not file_name.endswith('.py'):
            file_name += '.py'
        
        file_path = os.path.join(target_path, file_name)
        
        # Проверка существования файла
        if os.path.exists(file_path):
            self._show_error_dialog(f"File '{file_name}' already exists!")
            return
        
        try:
            # Создаем директорию, если ее нет
            os.makedirs(target_path, exist_ok=True)
            
            # Создаем файл
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('# New Python file\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()\n')
            
            logger.info(f"Created new Python file: {file_path}")
            self._refresh_files()
            
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            self._show_error_dialog(f"Failed to create file: {str(e)}")

    def _confirm_create_folder(self, dialog_id, input_id, target_path):
        folder_name = dpg.get_value(input_id).strip()

        logger.info(f"Attempting to create folder '{folder_name}' in '{target_path}'")

        # Проверка имени
        is_valid, error_msg = self._is_valid_name(folder_name)
        if not is_valid:
            logger.error(f"Invalid folder name: {error_msg}")
            self._show_error_dialog(f"Invalid folder name: {error_msg}")
            return
        
        folder_path = os.path.join(target_path, folder_name)
        logger.info(f"Full folder path will be: {folder_path}")

        # Проверка существования папки
        if os.path.exists(folder_path):
            logger.warning(f"Folder already exists: {folder_path}")
            self._show_error_dialog(f"Folder '{folder_name}' already exists!")
            return
        
        try:
            # Проверяем, что target_path существует и является директорией
            if not os.path.isdir(target_path):
                logger.error(f"Target path is not a directory: {target_path}")
                self._show_error_dialog(f"Invalid target directory: {target_path}")
                return

            # Создаем папку
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"Successfully created folder: {folder_path}")
            self._refresh_files()

        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            self._show_error_dialog(f"Failed to create folder: {str(e)}")

    def _show_error_dialog(self, message):
        self.dialog_counter += 1
        error_dialog_id = f"error_dialog_{self.dialog_counter}"
        
        with dpg.window(label="Error", modal=True, width=300, height=100, 
                       tag=error_dialog_id, pos=[250, 250]):
            dpg.add_text(message)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="OK", width=75, 
                             callback=lambda: dpg.delete_item(error_dialog_id))
        
        dpg.focus_item(error_dialog_id)
    
    def _refresh_files(self):
        logger.info("Refreshing file list...")
        if dpg.does_item_exist(self.window_id):
            self._populate_files()
        else:
            logger.warning("Skipping refresh - file manager window not created")