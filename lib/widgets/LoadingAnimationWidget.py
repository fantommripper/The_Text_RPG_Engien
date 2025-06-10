from lib.widgets.BasePassiveWidget import BasePassiveWidget
import time
import random as r

class LoadingAnimationWidget(BasePassiveWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._imports = [
            "controller.AudioController",
            "controller.LibController",
            "controller.InputController",
            "controller.MenuController",
            "lib.SaveManager",
            "lib.Logger",
            "lib.Consolas",
            "lib.SaveManager",
            "lib.Terminalium",
            "data.Config",
            "data.Player",
            "data.Ability",
            "data.Item",
            "data.Quest",
            "data.Skill",
            "data.Spell",
            "data.WorldValues",
        ]

        self.draw()

    def draw(self):
        animation_symbols = ['|', '/', '-', '\\']
        max_length = max(len(module) for module in self._imports)
        height, width = self._win.getmaxyx()
        y = 0

        for module in self._imports:
            module_text = f"| {module}{' '*(max_length - len(module))} "
            if len(module_text) + max_length + 6 > width - 1:
                module_text = module_text[:width - max_length - 7]
            self._win.addstr(y, 0, module_text)
            for i in range(r.randint(2, 6)):
                if max_length + 4 < width - 1:
                    self._win.addstr(y, max_length + 4, animation_symbols[i % len(animation_symbols)])
                self._win.refresh()
                time.sleep(0.1)
                if max_length + 4 < width - 1:
                    self._win.addstr(y, max_length + 4, ' ')
            if max_length + 4 < width - 1:
                self._win.addstr(y, max_length + 4, "DONE |")
            self._win.refresh()
            time.sleep(r.uniform(0.02, 0.09))
            y += 1

        self._win.refresh() 