import dearpygui.dearpygui as dpg
import os
import re
from lib.Logger import logger

class FileManager:
    def __init__(self):
        self.window_id = None
        self.assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Assets")
        self.selected_path = self.assets_path
        self.window_handler = None
        self.path_mapping = {}
        self.expanded_nodes = {}
        self.safe_name_pattern = re.compile(r'^[\w\-\.\s]+$')  # Разрешенные символы в именах

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

        with dpg.window(label="Context Menu", tag="context_menu", modal=True, show=False, no_title_bar=True,
                    no_move=True, no_resize=True, width=180, height=150):
            dpg.add_button(label="Open", callback=lambda: self._handle_menu_action("open"))
            dpg.add_button(label="Create File", callback=lambda: self._handle_menu_action("create_file"))
            dpg.add_button(label="Create Folder", callback=lambda: self._handle_menu_action("create_folder"))
            dpg.add_button(label="Refresh", callback=lambda: self._handle_menu_action("refresh"))

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
            
            self._restore_expanded_state()
            
        except Exception as e:
            logger.error(f"Error populating files: {e}")
            dpg.add_text(f"Error: {str(e)}", parent="file_list_container", color=[255, 100, 100])
    
    def _save_expanded_state(self):
        self.expanded_nodes = {}
        for tag, path in self.path_mapping.items():
            if dpg.does_item_exist(tag) and dpg.is_item_container(tag):
                self.expanded_nodes[path] = dpg.get_item_configuration(tag)["default_open"]
    
    def _restore_expanded_state(self):
        for tag, path in self.path_mapping.items():
            if path in self.expanded_nodes:
                dpg.configure_item(tag, default_open=self.expanded_nodes[path])
    
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
                    
                    was_expanded = self.expanded_nodes.get(item_path, False)

                    with dpg.tree_node(label=f"[D] {item}", tag=folder_tag,
                                    parent=parent_tag, default_open=was_expanded) as node:
                        with dpg.item_handler_registry() as handler:
                            # ИСПРАВЛЕНИЕ: используем user_data для передачи пути
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
                        # ИСПРАВЛЕНИЕ: используем user_data для передачи пути
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
            # Если кликнули на файле, используем его директорию
            if os.path.isfile(path):
                self.selected_path = os.path.dirname(path)
            else:
                self.selected_path = path

            logger.info(f"Right clicked on: {path}, selected path: {self.selected_path}")

            # Проверяем, что selected_path действительно директория
            if not os.path.isdir(self.selected_path):
                self.selected_path = self.assets_path
                logger.warning(f"Selected path is not a directory, using assets: {self.selected_path}")

            # Получаем глобальную позицию мыши (относительно viewport)
            mouse_pos = dpg.get_mouse_pos(local=False)

            # Получаем позицию окна FileManager для отладки
            if dpg.does_item_exist(self.window_id):
                window_pos = dpg.get_item_pos(self.window_id)
                logger.info(f"Window pos: {window_pos}, Mouse pos: {mouse_pos}")

            # Используем глобальные координаты мыши
            menu_x = mouse_pos[0] + 10  # небольшой отступ
            menu_y = mouse_pos[1] + 10

            # Проверяем границы viewport
            viewport_width = dpg.get_viewport_width()
            viewport_height = dpg.get_viewport_height()

            menu_width = 180
            menu_height = 150

            # Корректируем если выходит за границы
            if menu_x + menu_width > viewport_width:
                menu_x = mouse_pos[0] - menu_width - 10
            
            if menu_y + menu_height > viewport_height:
                menu_y = mouse_pos[1] - menu_height - 10

            menu_x = max(10, menu_x)  # минимальный отступ от края
            menu_y = max(10, menu_y)

            if dpg.does_item_exist("context_menu"):
                dpg.configure_item("context_menu", pos=[menu_x, menu_y], show=True)
        else:
            logger.warning(f"Invalid path on right click: {path}")
            self.selected_path = self.assets_path

    def _handle_menu_action(self, action):
        # Закрываем контекстное меню
        if dpg.does_item_exist("context_menu"):
            dpg.configure_item("context_menu", show=False)

        if not self.selected_path or not os.path.exists(self.selected_path):
            self.selected_path = self.assets_path

        if action == "create_file":
            dpg.split_frame()
            self._create_python_file()
        elif action == "create_folder":
            dpg.split_frame()
            self._create_folder()
        elif action == "refresh":
            self._refresh_files()
        elif action == "open":
            logger.info(f"Opening file: {self.selected_path}")
    
    def _create_python_file_in_assets(self):
        self.selected_path = self.assets_path
        self._create_python_file()
    
    def _create_folder_in_assets(self):
        self.selected_path = self.assets_path
        self._create_folder()
    
    def _create_python_file(self):
        if not self.selected_path or not os.path.isdir(self.selected_path):
            self.selected_path = self.assets_path
            logger.warning(f"Invalid path, using assets: {self.selected_path}")
        
        target_path = self.selected_path
        
        with dpg.window(label="Create Python File", modal=True, width=300, height=150, tag="create_file_dialog") as dialog:
            dpg.add_text("Enter file name:")
            file_name_input = dpg.add_input_text(label="Name", default_value="new_file.py", width=200, tag="file_name_input")
            
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Create", 
                             callback=lambda: self._confirm_create_file(dialog, file_name_input, target_path))
                dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item(dialog))
    
    def _create_folder(self):
        if not self.selected_path or not os.path.isdir(self.selected_path):
            self.selected_path = self.assets_path
            logger.warning(f"Invalid path, using assets: {self.selected_path}")
        
        target_path = self.selected_path
        
        with dpg.window(label="Create Folder", modal=True, width=300, height=150, tag="create_folder_dialog") as dialog:
            dpg.add_text("Enter folder name:")
            folder_name_input = dpg.add_input_text(label="Name", default_value="new_folder", width=200, tag="folder_name_input")
            
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Create", 
                             callback=lambda: self._confirm_create_folder(dialog, folder_name_input, target_path))
                dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item(dialog))
    
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
    
    def _confirm_create_file(self, dialog, input_field, target_path):
        file_name = dpg.get_value(input_field).strip()
        
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
        finally:
            dpg.delete_item(dialog)

    def _confirm_create_folder(self, dialog, input_field, target_path):
        folder_name = dpg.get_value(input_field).strip()

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
        finally:
            dpg.delete_item(dialog)
    
    def _show_error_dialog(self, message):
        with dpg.window(label="Error", modal=True, width=300, height=100, tag="error_dialog"):
            dpg.add_text(message)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="OK", width=75, callback=lambda: dpg.delete_item("error_dialog"))
    
    def _refresh_files(self):
        logger.info("Refreshing file list...")
        if dpg.does_item_exist(self.window_id):
            self._populate_files()
        else:
            logger.warning("Skipping refresh - file manager window not created")