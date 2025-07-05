import dearpygui.dearpygui as dpg

class TextEditor:
    def __init__(self, title, content, on_save, on_cancel=None, tag="scene_edit_dialog"):
        self.title = title
        self.content = content
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.tag = tag

    def show(self):
        if dpg.does_item_exist(self.tag):
            dpg.delete_item(self.tag)
        with dpg.window(
            label=self.title,
            width=900,
            height=700,
            tag=self.tag
        ):
            with dpg.group(horizontal=True):
                dpg.add_text(self.title)
                dpg.add_separator()
                dpg.add_button(
                    label="Save",
                    width=70,
                    callback=self.on_save
                )
                dpg.add_button(
                    label="Cancel",
                    width=70,
                    callback=self.on_cancel if self.on_cancel else lambda: dpg.delete_item(self.tag)
                )
            dpg.add_input_text(
                tag=f"{self.tag}_content",
                multiline=True,
                height=-1,
                width=-1,
                default_value=self.content
            )