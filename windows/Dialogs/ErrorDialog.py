from .Dialog import Dialog

class ErroreDialog(Dialog):
    def __init__(self):
        super().__init__(title="Error")

    def show(self, on_confirm, message, on_cancel=None, YesButton=False, no_label="OK", text_box=False):
        super().show(
            label_text=[message],
            text_box=text_box,
            default_value="///",
            on_confirm=on_confirm,
            on_cancel=on_cancel,
            YesButton=YesButton,
            no_label=no_label
        )