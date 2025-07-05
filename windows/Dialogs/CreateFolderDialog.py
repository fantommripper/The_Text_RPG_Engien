from .Dialog import Dialog

class CreateFolderDialog(Dialog):
    def __init__(self):
        super().__init__(title="Create Folder")

    def show(self, on_confirm, on_cancel=None):
        super().show(
            label_text=["Enter folder name:"],
            default_value="new_folder",
            on_confirm=on_confirm,
            on_cancel=on_cancel
        )