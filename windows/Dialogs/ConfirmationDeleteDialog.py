from .Dialog import Dialog

class ConfirmationDeleteDialog(Dialog):
    def __init__(self, item_name, item_type, item_path):
        self.item_type = item_type
        self.item_name = item_name
        self.item_path = item_path

        super().__init__(title="Confirm Deletion", height=160, width=500)

    def show(self, on_confirm, on_cancel=None):
        super().show(
            label_text=[
                f"Are you sure you want to delete this {self.item_type}?",
                f"Name: {self.item_name}",
                "This action cannot be undone!"
            ],
            on_confirm=on_confirm,
            text_box=False,
            yes_label="Delete",
            on_cancel=on_cancel
        )