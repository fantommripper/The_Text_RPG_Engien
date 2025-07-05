import dearpygui.dearpygui as dpg

class Dialog:
    def __init__(self, title, width=-1, height=-1, modal=True):
        self.dialog_id = f"{self.__class__.__name__}_{id(self)}"
        self.input_id = f"{self.dialog_id}_input"
        self.title = title
        self.width = width
        self.height = height
        self.modal = modal

    def show(self, on_confirm, label_text=[], default_value="value", on_cancel=None, text_box=True, yes_label="Create", no_label="Cancel", YesButton=True, NoButton=True):

        with dpg.window(label=self.title, modal=self.modal, width=self.width, height=self.height,
                        tag=self.dialog_id, pos=[200, 200]):
            for line in label_text:
                dpg.add_text(line)

            if text_box:
                dpg.add_input_text(label="Name", default_value=default_value, width=200, tag=self.input_id)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                if YesButton:
                    dpg.add_button(
                        label=yes_label,
                        callback=lambda: self._on_confirm_and_close(on_confirm)
                    )
                if NoButton:
                    dpg.add_button(
                        label=no_label,
                        callback=lambda: self._close(on_cancel)
                    )
        dpg.focus_item(self.dialog_id)

    def _on_confirm_and_close(self, on_confirm):
        if on_confirm:
            on_confirm(self.dialog_id, self.input_id)
        self._close()

    def _close(self, on_cancel=None):
        if on_cancel:
            on_cancel()
        if dpg.does_item_exist(self.dialog_id):
            dpg.delete_item(self.dialog_id)