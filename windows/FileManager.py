import dearpygui.dearpygui as dpg
import os
from lib.Logger import logger

class FileManager:
    def __init__(self):
        self.window_id = None
        self.assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Assets")
        self.selected_path = self.assets_path
        self.window_handler = None
        self.path_mapping = {}  # Словарь для хранения соответствия тегов и путей

        if not os.path.exists(self.assets_path):
            os.makedirs(self.assets_path)
            logger.info(f"Created Assets folder at: {self.assets_path}")

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

        # Контекстное меню
        with dpg.window(label="Context Menu", tag="context_menu", modal=True, show=False, no_title_bar=True, 
                      no_move=True, no_resize=True, width=180, height=150):
            dpg.add_button(label="Open", callback=lambda: self._handle_menu_action("open"))
            dpg.add_button(label="Create File", callback=lambda: self._handle_menu_action("create_file"))
            dpg.add_button(label="Create Folder", callback=lambda: self._handle_menu_action("create_folder"))
            dpg.add_button(label="Refresh", callback=lambda: self._handle_menu_action("refresh"))

    def _populate_files(self):
        try:
            # Очищаем контейнер
            if dpg.does_item_exist("file_list_container"):
                children = dpg.get_item_children("file_list_container", slot=1)
                if children:
                    for child in children:
                        dpg.delete_item(child)

            # Добавляем корневую папку Assets
            with dpg.tree_node(label="📁 Assets", tag="assets_root", default_open=True, parent="file_list_container") as node:
                # Сохраняем путь для корневой папки
                self.path_mapping["assets_root"] = self.assets_path
                
                # Обработчик правого клика для корневой папки
                with dpg.item_handler_registry() as handler:
                    dpg.add_item_clicked_handler(
                        button=dpg.mvMouseButton_Right,
                        callback=lambda: self._on_right_click(self.assets_path)
                    )
                dpg.bind_item_handler_registry(node, handler)
                
                # Заполняем содержимое Assets
                self._add_directory_contents(self.assets_path, "assets_root")
            
        except Exception as e:
            logger.error(f"Error populating files: {e}")
            dpg.add_text(f"Error: {str(e)}", parent="file_list_container", color=[255, 100, 100])
    
    def _add_directory_contents(self, path, parent_tag):
        try:
            if not os.path.exists(path):
                return
                
            items = os.listdir(path)
            items.sort()
            
            # Сначала папки
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    folder_tag = f"folder_{abs(hash(item_path))}"
                    self.path_mapping[folder_tag] = item_path
                    
                    with dpg.tree_node(label=f"📁 {item}", tag=folder_tag, parent=parent_tag, default_open=False) as node:
                        # Обработчик правого клика для папки
                        with dpg.item_handler_registry() as handler:
                            dpg.add_item_clicked_handler(
                                button=dpg.mvMouseButton_Right,
                                callback=lambda: self._on_right_click(item_path)
                            )
                        dpg.bind_item_handler_registry(node, handler)
                        
                        # Рекурсивно добавляем содержимое папки
                        self._add_directory_contents(item_path, folder_tag)
            
            # Затем файлы
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    file_icon = self._get_file_icon(item)
                    file_tag = f"file_{abs(hash(item_path))}"
                    self.path_mapping[file_tag] = item_path
                    
                    # Создаем элемент для файла
                    node = dpg.add_text(f"{file_icon} {item}", parent=parent_tag, tag=file_tag)
                    
                    # Обработчик правого клика для файла
                    with dpg.item_handler_registry() as handler:
                        dpg.add_item_clicked_handler(
                            button=dpg.mvMouseButton_Right,
                            callback=lambda: self._on_right_click(item_path)
                        )
                    dpg.bind_item_handler_registry(node, handler)
                    
        except Exception as e:
            logger.error(f"Error adding directory contents for {path}: {e}")
    
    def _get_file_icon(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        icons = {
            '.py': '🐍',
            '.txt': '📄',
            '.json': '📋',
            '.png': '🖼️',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
            '.gif': '🖼️',
            '.mp3': '🎵',
            '.wav': '🎵',
            '.mp4': '🎬',
            '.avi': '🎬',
        }
        return icons.get(ext, '📄')
    
    def _on_right_click(self, path):
        """Обработчик правого клика мыши"""
        if path and os.path.exists(path):
            self.selected_path = path
            logger.info(f"Right clicked on: {self.selected_path}")
            mouse_pos = dpg.get_mouse_pos()
            if dpg.does_item_exist("context_menu"):
                dpg.configure_item("context_menu", pos=mouse_pos, show=True)
        else:
            logger.warning(f"Invalid path on right click: {path}")
    
    def _handle_menu_action(self, action):
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
        
        with dpg.window(label="Create Python File", modal=True, width=300, height=150) as dialog:
            dpg.add_text("Enter file name:")
            file_name_input = dpg.add_input_text(label="Name", default_value="new_file.py", width=200)
            
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
        
        with dpg.window(label="Create Folder", modal=True, width=300, height=150) as dialog:
            dpg.add_text("Enter folder name:")
            folder_name_input = dpg.add_input_text(label="Name", default_value="new_folder", width=200)
            
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Create", 
                             callback=lambda: self._confirm_create_folder(dialog, folder_name_input, target_path))
                dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item(dialog))
    
    def _confirm_create_file(self, dialog, input_field, target_path):
        file_name = dpg.get_value(input_field)
        if not file_name:
            return
        
        if not file_name.endswith('.py'):
            file_name += '.py'
        
        file_path = os.path.join(target_path, file_name)
        
        try:
            if not os.path.exists(target_path):
                os.makedirs(target_path, exist_ok=True)
                logger.warning(f"Created missing directory: {target_path}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('# New Python file\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()\n')
            
            logger.info(f"Created new Python file: {file_path}")
            self._refresh_files()
            
        except Exception as e:
            logger.error(f"Error creating file: {e}")
        
        dpg.delete_item(dialog)
    
    def _confirm_create_folder(self, dialog, input_field, target_path):
        folder_name = dpg.get_value(input_field)
        if not folder_name:
            return
        
        folder_path = os.path.join(target_path, folder_name)
        
        try:
            if not os.path.exists(target_path):
                os.makedirs(target_path, exist_ok=True)
                logger.warning(f"Created missing directory: {target_path}")
            
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"Created new folder: {folder_path}")
            self._refresh_files()
            
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
        
        dpg.delete_item(dialog)
    
    def _refresh_files(self):
        logger.info("Refreshing file list...")
        if dpg.does_item_exist(self.window_id):
            self._populate_files()
        else:
            logger.warning("Skipping refresh - file manager window not created")