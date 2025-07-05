from .Dialog import Dialog

class RenameDialog(Dialog):
    def __init__(self, old_name):
        super().__init__(title="Rename Item")
        self.old_name = old_name

    def show(self, on_confirm, on_cancel=None):
        super().show(
            label_text=[f"Rename '{self.old_name}' to:"],
            default_value=self.old_name,
            on_confirm=on_confirm,
            on_cancel=on_cancel,
            yes_label="Rename"
        )