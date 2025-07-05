import dearpygui.dearpygui as dpg
import os
from .Dialog import Dialog

class MoveDialog(Dialog):
    def __init__(self, assets_path):
        super().__init__(title="Move Item", width=400, height=300)
        self.assets_path = assets_path
        self.folder_tree = {}

    def show(self, on_confirm, on_cancel=None):
        with dpg.window(
            label=self.title, 
            modal=True, 
            width=self.width, 
            height=self.height,
            tag=self.dialog_id
        ):
            dpg.add_text("Select destination folder:")
            with dpg.child_window(height=200, width=-1):
                self._build_folder_tree(self.assets_path)
            
            dpg.add_input_text(
                label="Path:",
                tag=self.input_id,
                width=-1,
                readonly=True
            )
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Move",
                    callback=lambda: self._on_confirm_and_close(on_confirm)
                )
                dpg.add_button(
                    label="Cancel",
                    callback=lambda: self._close(on_cancel)
                )

    def _build_folder_tree(self, path, parent="root"):
        with dpg.tree_node(label=os.path.basename(path), parent=parent):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    self._build_folder_tree(item_path)
                    dpg.add_selectable(
                        label=item,
                        callback=lambda s, a, p=item_path: dpg.set_value(self.input_id, p)
                    )