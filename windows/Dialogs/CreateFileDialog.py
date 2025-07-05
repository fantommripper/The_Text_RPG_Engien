from .Dialog import Dialog

class CreateFileDialog(Dialog):
    def __init__(self):
        super().__init__(title="Create Python File")

    def show(self, on_confirm, on_cancel=None):
        super().show(
            label_text=["Enter file name:"],
            default_value="new_file.py",
            on_confirm=on_confirm,
            on_cancel=on_cancel
        )