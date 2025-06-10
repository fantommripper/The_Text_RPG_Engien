from lib.widgets.BasePassiveWidget import BasePassiveWidget
import time
from controller.AudioController import audio_controller

class AnimationWidget(BasePassiveWidget):
    def __init__(self, parent, frames, delay=0.3, alignmentTable="c", x=None, y=None, clear=True, Xdo="=", Ydo="=", audio=True):
        width = len(frames[0]) if frames else 0
        height = len(frames)
        super().__init__(parent, clear, alignmentTable, width, height, x, y, Xdo, Ydo)
        
        self._frames = frames
        self._delay = delay
        self._audio = audio

        self.draw()

    def draw(self):
        if self._clear:
            self._win.clear()

        table_x, table_y = self._calculate_position()
        current_y = table_y

        for frame in self._frames:
            self._win.addstr(current_y, table_x, frame)
            if self._audio:
                audio_controller.play_random_print_sound()
            self._win.refresh()
            time.sleep(self._delay)
            current_y += 1

        self._win.refresh() 